# Use inter-app agents and MCP servers

This topic describes how a Snowflake Native App can use inter-app communication (IAC) to
let its Cortex Agent call another app’s agent or MCP server.

When apps include Cortex Agents and MCP servers, two inter-app patterns become
available:

- **Agent-to-agent**: one app’s agent runs another app’s agent through a wrapper
  procedure.
- **Agent-to-MCP server**: one app’s agent uses another app’s MCP server as a tool.

Each app keeps its own data and logic private. Agents can only reach across apps
through the tools and permissions that providers expose and consumers approve.

### Before you begin

Before using inter-app agent communication, you should be familiar with the following
topics:

- [Inter-app communication](/developer-guide/native-apps/inter-app-communication)
- [Use Cortex Agents and MCP servers in an app](/developer-guide/native-apps/agents-mcp-servers)
- [About caller grants](/developer-guide/restricted-callers-rights#about-caller-grants)

## How it works

Inter-app agent communication builds on the IAC connection handshake:

1. The client app (the app whose agent initiates calls) requests a connection to the
   server app (the app that provides agents and/or MCP servers).
2. The consumer admin approves the connection, granting the server app’s application
   roles to the client app.
3. With the server’s application roles, the client app’s agent can use the server
   app’s agents and MCP servers in its own agent specification.

## Example: inter-app portfolio analysis

This example uses two apps:

- **Financial Toolbox App** (server): provides historical market data through a
  Cortex Agent, and ML-based price forecasting through a custom MCP server on SPCS.
- **Portfolio App** (client): knows the consumer’s stock holdings and orchestrates
  across both apps to answer questions.

The Portfolio agent is the entry point (for example, in Snowflake CoWork, select
the Portfolio agent). It can look up the consumer’s holdings locally, delegate
historical analysis to the Financial Toolbox agent (agent-to-agent), and request
price forecasts from the Financial Toolbox MCP server (agent-to-MCP).

### Server app: Financial Toolbox

The Financial Toolbox app exposes two inter-app capabilities: an agent (wrapped in a
stored procedure) and a custom MCP server. Both are created in the app’s setup script
and granted to an application role so that connected client apps can use them.

#### Agent for historical market analysis

Copy code

```
-- In the Financial Toolbox setup script
CREATE AGENT IF NOT EXISTS core.financial_agent
  FROM SPECIFICATION $$
  models:
    orchestration: auto

  instructions:
    system: "You are a financial analysis assistant with access to historical
             stock market data."

  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "MarketData"
        description: "Query historical stock market data"

  tool_resources:
    MarketData:
      semantic_view: "core.market_data_sv"
      execution_environment:
        type: warehouse
        warehouse: "TOOLBOX_WH"
  $$;

-- Wrapper procedure that client apps call to run the agent
CREATE OR REPLACE PROCEDURE core.run_financial_agent(message STRING)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.11'
  PACKAGES = ('snowflake-snowpark-python')
  HANDLER = 'run'
  EXECUTE AS OWNER
AS
$$
import json

def run(session, message):
    body = json.dumps({
        "messages": [{"role": "user", "content": [{"type": "text", "text": message}]}]
    })
    escaped = body.replace("'", "''")
    result = session.sql(
        f"SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN("
        f"  'FINANCIAL_TOOLBOX.CORE.MARKET_ANALYST',"
        f"  '{escaped}'"
        f")"
    ).collect()
    return str(result[0][0]) if result else ''
$$;

GRANT USAGE ON PROCEDURE core.run_financial_agent(STRING) TO APPLICATION ROLE fin_app_user;
```

#### Custom MCP server for price forecasting

The Financial Toolbox also runs an ML forecasting model on SPCS, registered as a
custom MCP server:

Copy code

```
-- SPCS service running the ML forecasting model
CREATE SERVICE IF NOT EXISTS services.forecast_service
  IN COMPUTE POOL toolbox_pool
  FROM SPECIFICATION '
  spec:
    containers:
      - name: forecast
        image: /TOOLBOX_PKG/IMG/REPO/forecast-server:latest
        readinessProbe:
          port: 8081
          path: /health
    endpoints:
      - name: mcp_endpoint
        port: 8080
        public: true
  ';

GRANT SERVICE ROLE services.forecast_service!ALL_ENDPOINTS_USAGE
  TO APPLICATION ROLE fin_app_user;

-- Register the SPCS endpoint as a custom MCP server
CREATE CUSTOM MCP SERVER IF NOT EXISTS services.forecast_mcp
  SERVICE = services.forecast_service
  ENDPOINT = mcp_endpoint
  PATH = '/mcp';

GRANT USAGE ON CUSTOM MCP SERVER services.forecast_mcp TO APPLICATION ROLE fin_app_user;
```

### Client app: Portfolio App

The Portfolio app wires up inter-app tools in two parts: an `APPLICATION_NAME`
configuration definition to request the server app name from the consumer, and an
agent specification that references the Financial Toolbox’s agent and MCP server.

#### Connection request

The setup script creates an `APPLICATION_NAME` configuration definition to request
the server app name from the consumer. This follows the standard
[IAC connection request workflow](/developer-guide/native-apps/inter-app-communication#label-native-apps-iac-request-and-approve-connection).

Copy code

```
-- Request the Financial Toolbox app name from the consumer
ALTER APPLICATION SET CONFIGURATION DEFINITION financial_toolbox_config
  TYPE = APPLICATION_NAME
  LABEL = 'Financial Toolbox App'
  DESCRIPTION = 'Connection to the Financial Toolbox app for market data
                 and forecasting'
  APPLICATION_ROLES = (portfolio_app_user);
```

A `before_configuration_change` callback then creates the connection request and the
Portfolio agent. When the consumer provides the server app name, this callback runs
automatically. It uses the server app name to build fully qualified references to
the Financial Toolbox’s wrapper procedure and MCP server:

Copy code

```
-- Callback that creates the connection request and the portfolio agent
CREATE OR REPLACE PROCEDURE core.before_config_change(config_name STRING, config_value STRING)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.11'
  PACKAGES = ('snowflake-snowpark-python')
  HANDLER = 'run'
AS
$$
def run(session, config_name, config_value):
    if config_value is None or config_name != 'FINANCIAL_TOOLBOX_CONFIG':
        return 'skipped'

    server_app = config_value
    dollar_quote = chr(36) * 2  # creating a string of "$$" this way to escape, to not interfere with the outer $$...$$

    # 1. Create the connection request
    session.sql(f"""
        ALTER APPLICATION SET SPECIFICATION CONNECTION_FINANCIAL_TOOLBOX
          TYPE = CONNECTION
          LABEL = 'Financial Toolbox App'
          DESCRIPTION = 'Connection to the Financial Toolbox app for market
                         data and forecasting'
          SERVER_APPLICATION = {server_app}
          SERVER_APPLICATION_ROLES = (fin_app_user)
    """).collect()

    # 2. Create the portfolio agent with inter-app tool references.
    #    Tool identifiers are resolved at runtime, not creation time,
    #    so the agent can be created before the connection is approved.
    session.sql(f"""
        CREATE OR REPLACE AGENT core.portfolio_agent
          FROM SPECIFICATION {dollar_quote}
          models:
            orchestration: auto

          instructions:
            system: "You are a portfolio management assistant. You can look up
                     the user's stock holdings, call the Financial Toolbox agent
                     for historical analysis, and use the forecast MCP server
                     for price predictions."

          tools:
            - tool_spec:
                type: "cortex_analyst_text_to_sql"
                name: "PortfolioLookup"
                description: "Look up the user's stock holdings and cost basis"
            - tool_spec:
                type: "generic"
                name: "FinancialToolboxAgent"
                description: "Call the Financial Toolbox agent for historical
                              stock market data"
                input_schema:
                  type: object
                  properties:
                    message:
                      type: string
                      description: "Message to send to the Financial Toolbox agent"
                  required: ["message"]

          tool_resources:
            PortfolioLookup:
              semantic_view: "core.holdings_sv"
              execution_environment:
                type: warehouse
                warehouse: "PORTFOLIO_WH"
            FinancialToolboxAgent:
              identifier: "{server_app}.CORE.RUN_FINANCIAL_AGENT"
              type: procedure
              execution_environment:
                type: warehouse
                warehouse: "PORTFOLIO_WH"

          mcp_servers:
            - server_spec:
                name: "{server_app}.SERVICES.FORECAST_MCP"
          {dollar_quote}
    """).collect()

    session.sql("""
        GRANT USAGE ON AGENT core.portfolio_agent TO APPLICATION ROLE portfolio_app_user
    """).collect()

    return 'success'
$$;
```

The app’s `manifest.yml` registers this callback:

Copy code

```
lifecycle_callbacks:
  before_configuration_change: core.before_config_change
```

Because tool identifiers in the agent specification are resolved at runtime (not
creation time), the agent can be created before the connection is approved. The
fully qualified names (for example, `FINANCIAL_TOOLBOX.CORE.RUN_FINANCIAL_AGENT`)
only need to be accessible when the agent actually invokes those tools.

When the consumer approves the connection, the Portfolio app is granted the Financial
Toolbox’s `fin_app_user` role, which includes USAGE on the agent-wrapper procedure
and the MCP server.

### Consumer setup

The consumer installs both apps and approves the connection:

Copy code

```
-- Approve the connection between Portfolio and Financial Toolbox
ALTER APPLICATION financial_toolbox
  APPROVE SPECIFICATION connection_financial_toolbox
  SEQUENCE_NUMBER = 1;
```

The consumer also configures caller grants so that the Portfolio app can use
Financial Toolbox objects on the consumer’s behalf:

Copy code

```
-- Allow PORTFOLIO_APP to manage objects in FINANCIAL_TOOLBOX app.
-- This high-level caller privilege covers the custom MCP server and its underlying service.
GRANT CALLER OBJECT MANAGEMENT ON APPLICATION FINANCIAL_TOOLBOX TO APPLICATION PORTFOLIO_APP;

-- Allow PORTFOLIO_APP to run programs in FINANCIAL_TOOLBOX app.
-- This high-level caller privilege covers the stored procedure run_financial_agent(STRING).
GRANT CALLER PROGRAM USAGE ON APPLICATION FINANCIAL_TOOLBOX TO APPLICATION PORTFOLIO_APP;
```

After the caller grants are configured, the Portfolio agent can run the Financial
Toolbox agent and use its MCP server. The agent is available in Snowflake
Intelligence, through the REST API, or through SQL (`SNOWFLAKE.CORTEX.DATA_AGENT_RUN`).

## Runtime behavior

With the connection approved, the Portfolio agent orchestrates across both apps at
runtime.

### Agent-to-agent: historical analysis

When a consumer asks “What are the top 3 stocks in my portfolio by returns over the
past 6 months?”, the Portfolio agent:

1. Calls `PortfolioLookup` to retrieve the consumer’s holdings from the Portfolio
   app’s data.
2. Calls `FinancialToolboxAgent`, which triggers the Financial Toolbox agent. That
   agent uses its own `MarketData` tool to query historical stock data.
3. Combines the results and returns an analysis.

The invocation chain is: Portfolio agent → Financial Toolbox agent-wrapper procedure
(`FINANCIAL_TOOLBOX.CORE.RUN_FINANCIAL_AGENT`) → Financial Toolbox agent.

Note

While both agents run in restricted caller’s rights (RCR) mode, caller grant
requirements do not chain through this flow. The owner’s-rights wrapper procedure
resets the caller context, so each RCR agent’s caller grant requirement applies
independently.

In this example, the Financial Toolbox agent is invoked by its own app’s owner’s-rights
procedure, so the caller of the RCR agent is the Financial Toolbox app itself. As a
result, unlike the Portfolio agent, the Financial Toolbox agent can access the
consumer’s data only if regular grants of that data are granted directly to the
Financial Toolbox app, in addition to the caller grants.

### Agent-to-MCP: price forecasting

When the consumer asks “Given my average cost basis of a certain stock, should I buy,
hold, or sell tomorrow?”, the Portfolio agent:

1. Calls `PortfolioLookup` to get the consumer’s cost basis for the stock.
2. Calls a tool from `FINANCIAL_TOOLBOX.SERVICES.FORECAST_MCP` to get the predicted
   price for the next day.
3. Returns a recommendation based on the cost basis and forecast.
