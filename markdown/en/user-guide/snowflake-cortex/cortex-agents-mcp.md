# Snowflake-managed MCP server

Feature — Generally Available

Not supported in government regions.

## Overview

Note

Snowflake supports Model Context Protocol revision `2025-11-25`.

Model Context Protocol (MCP) is an [open-source standard](https://modelcontextprotocol.io/docs/getting-started/intro) that lets AI agents securely interact with business applications and external data systems, such as databases and content repositories. MCP lets enterprise businesses reduce integration challenges and quickly deliver outcomes from models. Since its launch, MCP has become foundational for agentic applications, providing a consistent and secure mechanism for invoking tools and retrieving data.

The Snowflake-managed MCP server lets AI agents securely retrieve data from Snowflake accounts without needing to deploy separate infrastructure. You can configure the MCP server to serve Cortex Analyst, Cortex Search, and Cortex Agents as tools, along with custom tools and SQL executions on the standards-based interface. MCP clients discover and invoke these tools, and retrieve data required for the application. With managed MCP servers on Snowflake, you can build scalable enterprise-grade applications while maintaining access and privacy controls. The MCP server on Snowflake provides:

- **Standardized integration:** Unified interface for tool discovery and invocation, in compliance with the rapidly evolving standards.
- **Comprehensive authentication:** Snowflake OAuth by default, with optional External OAuth so MCP clients can authenticate against your organization’s identity provider.
- **Robust governance:** role-based access control (RBAC) for the MCP server and tools to manage tool discovery and invocation.

For information about the MCP lifecycle, see [Lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle). For an example of an MCP implementation, see the [Getting Started with Managed Snowflake MCP Server](https://quickstarts.snowflake.com/guide/getting-started-with-snowflake-mcp-server/index.html) Quickstart.

## MCP server security recommendations

Important

When you configure hostnames for MCP server connections, use hyphens (`-`) instead of underscores (`_`). MCP servers have connection issues with hostnames containing underscores.

Using multiple MCP servers without verifying tools and descriptions could lead to vulnerabilities such as tool poisoning or tool shadowing. Snowflake recommends verifying third-party MCP servers before using them. This includes any MCP server from another Snowflake user or account. Verify all tools offered by third-party MCP servers.

We recommend using OAuth as the authentication method. Using hardcoded tokens can lead to token leakage.

When using a Programmatic Access Token (PAT), set it to use the least-privileged role allowed to work with MCP. This will help prevent leaking a secret with access to a highly-privileged role.

Configure proper permissions for the MCP server and tools following the least-privilege principle. Access to the MCP Server does not give access to the tools. Permission needs to be granted for each tool.

Avoid configurations that can create recursive loops. For example, an external client calling a Cortex Agent tool through MCP, which in turn invokes another MCP server that calls back into a Cortex Agent, can produce expensive, unbounded loops. Snowflake enforces a maximum recursion depth of 10 invocations. Ensure your agent and tool configurations don’t create circular invocation paths.

## Create an MCP server object

Create an object, specifying the tools and other metadata. MCP clients that connect with the server, after requisite authentication, are able to discover and invoke these tools.

1. Navigate to the database and schema where you want to create the MCP server.
2. Create the MCP server by using the following syntax:

   Copy code

   ```
   CREATE [ OR REPLACE ] MCP SERVER [ IF NOT EXISTS ] <server_name>
     FROM SPECIFICATION $$ <specification_yaml> $$;
   ```

For business data applications that require governed orchestration, Snowflake recommends exposing a Cortex Agent as the client-facing MCP tool. Configure the agent with the Cortex Analyst, Cortex Search, and custom tools that it needs, and then expose the agent through the MCP server. This configuration gives the external MCP client one governed interface and lets the agent select the appropriate resources for each request.

The following example exposes only a Cortex Agent:

Copy code

```
CREATE OR REPLACE MCP SERVER <database_name>.<schema_name>.<server_name>
  FROM SPECIFICATION $$
  tools:
    - title: "Governed business data agent"
      name: "business_data_agent"
      type: "CORTEX_AGENT_RUN"
      identifier: "<database_name>.<schema_name>.<agent_name>"
      description: "Use this agent for governed business data questions."
  $$;
```

When an MCP client sends a question, the client selects the agent based on its name and description. The MCP server passes the question to the agent. The agent then selects and orchestrates its configured Cortex Analyst, Cortex Search, or custom tools and returns the response to the client.

Use precise, domain-specific names and descriptions when you expose multiple agents. This information helps the MCP client select the correct agent.

Expose Cortex Analyst or Cortex Search directly when you want the external MCP client to select those resources independently. A directly exposed Cortex Analyst tool generates SQL and returns the statement to the client. A SQL execution tool runs queries without Cortex Agent orchestration.

### Configure tool types

Snowflake currently supports the following tool types:

- **CORTEX\_AGENT\_RUN:** Cortex Agent tool
- **CORTEX\_SEARCH\_SERVICE\_QUERY:** Cortex Search Service tool
- **CORTEX\_ANALYST\_MESSAGE:** Cortex Analyst tool
- **SYSTEM\_EXECUTE\_SQL:** SQL execution
- **GENERIC:** tool for UDFs and stored procedures

The following examples show how to configure different tool types:

Agent toolAnalyst toolSearch toolSQL execution toolUDF / Stored Procedure

For the Agent tool, your client passes a message to the agent. The agent processes the request and returns a response. Use the following code to specify the tool configuration.

Copy code

```
tools:
  - title: "Governed business data agent"
    name: "business_data_agent"
    type: "CORTEX_AGENT_RUN"
    identifier: "<database_name>.<schema_name>.<agent_name>"
    description: "Answers governed business data questions by using configured Cortex Analyst and Cortex Search resources."
```

The agent tool response includes all intermediate steps by design: reasoning traces, tool calls, search results, and citations.
This can result in large response payloads (200 KB or more). To reduce the payload size when the agent uses Cortex Search,
configure `max_results` in the agent’s search tool resources to limit the number of search results returned per query.

Using the Analyst tool, your client can generate SQL from natural language text. Use the following code to specify the tool configuration.

Note

The Snowflake-managed MCP server only supports using semantic views with Cortex Analyst. It does not support semantic models.

Copy code

```
tools:
  - name: "revenue-semantic-view"
    type: "CORTEX_ANALYST_MESSAGE"
    identifier: "database1.schema1.Semantic_View_1"
    description: "Semantic view for all revenue tables"
    title: "Semantic view for revenue"
```

Using the Search tool requests, your client can perform unstructured search on their data.

Copy code

```
tools:
  - name: "product-search"
    type: "CORTEX_SEARCH_SERVICE_QUERY"
    identifier: "database1.schema1.Cortex_Search_Service1"
    description: "cortex search service for all products"
    title: "Product Search"
```

For the SQL execution tool, your client can execute SQL queries on Snowflake. You can optionally configure the following options:

- `read_only`: When set to `true`, only read operations (SELECT queries) are allowed. Defaults to `true`.
- `query_timeout`: Maximum time in seconds for query execution.
- `warehouse`: The warehouse to use for query execution. If not specified, the default warehouse is used.

Important

Snowflake generally recommends exposing a Cortex Agent as the only client-facing tool on a given MCP server used for governed business questions. Exposing `SYSTEM_EXECUTE_SQL` on the same server allows the MCP client to bypass the agent’s semantic views, verified queries, and orchestration; if direct SQL is required, expose it through a separate MCP server with a dedicated least-privileged role.

Use the following code to specify the tool configuration:

Copy code

```
tools:
  - title: "SQL Execution Tool"
    name: "sql_exec_tool"
    type: "SYSTEM_EXECUTE_SQL"
    description: "A tool to execute SQL queries against the connected Snowflake database."
    config:
      read_only: true
      query_timeout: 600
      warehouse: "<warehouse_name>"
```

For your custom tools, you must provide the user-defined function (UDF) or stored procedure signature in the tool configuration. The custom tool enables you to invoke UDFs and stored procedures as tools through the MCP server.

You can specify the following in the tool configuration:

- `type`: `function` for UDF, `procedure` for stored procedure
- `warehouse`: The warehouse to use. If you don’t specify a warehouse, the default warehouse is used.
- `query_timeout`: Maximum time in seconds for tool execution.
- `input_schema`: Corresponds to the function signature.

Copy code

```
tools:
  - name: "my_custom_tool"
    identifier: "db.schema.my_function"
    type: "GENERIC"
    description: "Custom tool description"
    config:
      type: "function"
      query_timeout: 120
      warehouse: "WAREHOUSE"
      input_schema:
        type: "object"
        properties:
          query:
            type: "string"
```

Use the following examples to create and configure custom tools using UDFs and stored procedures:

UDF examplesStored procedure examplesTool configuration examples

The following examples demonstrate creating UDFs that can be used as custom tools:

Copy code

```
-- create a simple udf
CREATE OR REPLACE FUNCTION MULTIPLY_BY_TEN(x FLOAT)
RETURNS FLOAT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.13'
HANDLER = 'multiply_by_ten'
AS
$$
def multiply_by_ten(x: float) -> float:
  return x * 10
$$;

SHOW FUNCTIONS LIKE 'MULTIPLY_BY_TEN';

-- test return json/variant
CREATE OR REPLACE FUNCTION CALCULATE_PRODUCT_AND_SUM(x FLOAT, y FLOAT)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.13'
HANDLER = 'calculate_values'
AS
$$
import json

def calculate_values(x: float, y: float) -> dict:
  """
  Calculates the product and sum of two numbers and returns them in a dictionary.
  The dictionary is converted to a VARIANT (JSON) in the SQL return.
  """
  product = x * y
  sum_val = x + y

  return {
      "product": product,
      "sum": sum_val
  }
$$;

-- test return list/array
CREATE OR REPLACE FUNCTION GET_NUMBERS_IN_RANGE(x FLOAT, y FLOAT)
RETURNS ARRAY -- Use ARRAY to explicitly state a list is being returned
LANGUAGE PYTHON
RUNTIME_VERSION = '3.13'
HANDLER = 'get_numbers'
AS
$$
def get_numbers(x: float, y: float) -> list:
  """
  Returns a list of integers between x (exclusive) and y (inclusive).
  Assumes x < y.
  """
  # Ensure x and y are treated as integers for range generation
  start = int(x) + 1
  end = int(y) + 1 # range() is exclusive on the stop value

  # Use a list comprehension to generate the numbers
  # The Python list will be converted to a Snowflake ARRAY.
  return list(range(start, end))
$$;
```

The following examples demonstrate creating stored procedures that can be used as custom tools:

Copy code

```
-- create a simple stored procedure
CREATE OR REPLACE PROCEDURE MULTIPLY_BY_TEN_SP(x FLOAT)
RETURNS FLOAT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.13'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'multiply_by_ten'
AS
$$
# The handler logic is identical to the UDF for a scalar return
def multiply_by_ten(x: float) -> float:
      return x * 10
$$;

-- test return json/variant
CREATE OR REPLACE PROCEDURE CALCULATE_VALUES_SP(x FLOAT, y FLOAT)
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.13'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'calculate_values'
AS
$$
# The handler logic is identical to the UDF for a VARIANT return
def calculate_values(x: float, y: float) -> dict:
      """
      Calculates the product and sum of two numbers and returns them in a dictionary.
      The dictionary is converted to a VARIANT (JSON) in the SQL return.
      """
      product = x * y
      sum_val = x + y

      return {
          "product": product,
          "sum": sum_val
      }
$$;

-- test return list/array
CREATE OR REPLACE PROCEDURE GET_NUMBERS_SP(x FLOAT, y FLOAT)
RETURNS ARRAY
LANGUAGE PYTHON
RUNTIME_VERSION = '3.13'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'get_numbers'
AS
$$
def get_numbers(x: float, y: float) -> list:
      """
      Returns a list of integers between x (exclusive) and y (inclusive).
      The Python list will be converted to a Snowflake ARRAY.
      """
      # Ensure x and y are treated as integers for range generation
      start = int(x) + 1
      end = int(y) + 1 # range() is exclusive on the stop value

      # Use a list comprehension to generate the numbers
      return list(range(start, end))
$$;
```

The following examples demonstrate configuring custom tools for UDFs and stored procedures:

Copy code

```
CREATE MCP SERVER my_mcp_server
  FROM SPECIFICATION $$
    tools:
      - title: "Custom Tool 1"
        identifier: "EXAMPLE_DATABASE.AGENTS.MULTIPLY_BY_TEN"
        name: "multiply_by_ten"
        type: "GENERIC"
        description: "Multiplied input value by ten and returns the result."
        config:
          type: "function"
          warehouse: "COMPUTE_SERVICE_WAREHOUSE"
          input_schema:
            type: "object"
            properties:
              x:
                description: "A number to be multiplied by ten"
                type: "number"
      - title: "Custom Tool 2"
        identifier: "EXAMPLE_DATABASE.AGENTS.CALCULATE_PRODUCT_AND_SUM"
        name: "calculate_product_and_sum"
        type: "GENERIC"
        description: "Calculates the product and sum of two numbers and returns them in a JSON object."
        config:
          type: "function"
          warehouse: "COMPUTE_SERVICE_WAREHOUSE"
          input_schema:
            type: "object"
            properties:
              x:
                description: "First number"
                type: "number"
              y:
                description: "Second number"
                type: "number"
      - title: "Custom Tool 3"
        identifier: "EXAMPLE_DATABASE.AGENTS.GET_NUMBERS_IN_RANGE"
        name: "get_numbers_in_range"
        type: "GENERIC"
        description: "Returns a list of integers between two numbers."
        config:
          type: "function"
          warehouse: "COMPUTE_SERVICE_WAREHOUSE"
          input_schema:
            type: "object"
            properties:
              x:
                description: "Start number (exclusive)"
                type: "number"
              y:
                description: "End number (inclusive)"
                type: "number"
      - title: "Custom Tool 4"
        identifier: "EXAMPLE_DATABASE.AGENTS.MULTIPLY_BY_TEN_SP"
        name: "multiply_by_ten_sp"
        type: "GENERIC"
        description: "Multiplied input value by ten and returns the result."
        config:
          type: "procedure"
          warehouse: "COMPUTE_SERVICE_WAREHOUSE"
          input_schema:
            type: "object"
            properties:
              x:
                description: "A number to be multiplied by ten"
                type: "number"
      - title: "Custom Tool 5"
        identifier: "EXAMPLE_DATABASE.AGENTS.CALCULATE_PRODUCT_AND_SUM_SP"
        name: "calculate_product_and_sum_sp"
        type: "GENERIC"
        description: "Calculates the product and sum of two numbers and returns them in a JSON object."
        config:
          type: "procedure"
          warehouse: "COMPUTE_SERVICE_WAREHOUSE"
          input_schema:
            type: "object"
            properties:
              x:
                description: "First number"
                type: "number"
              y:
                description: "Second number"
                type: "number"
      - title: "Custom Tool 6"
        identifier: "EXAMPLE_DATABASE.AGENTS.GET_NUMBERS_IN_RANGE_SP"
        name: "get_numbers_in_range_sp"
        type: "GENERIC"
        description: "Returns a list of integers between two numbers."
        config:
          type: "procedure"
          warehouse: "COMPUTE_SERVICE_WAREHOUSE"
          input_schema:
            type: "object"
            properties:
              x:
                description: "Start number (exclusive)"
                type: "number"
              y:
                description: "End number (inclusive)"
                type: "number"
  $$;
```

### Manage MCP server objects

After you create an MCP server, use the following commands to inspect or remove it:

1. To show MCP servers, use the following commands:

   Copy code

   ```
   SHOW MCP SERVERS IN DATABASE <database_name>;
   SHOW MCP SERVERS IN SCHEMA <schema_name>;
   SHOW MCP SERVERS IN ACCOUNT;
   ```

   The following shows the output of the command:

   ```
   |               created_on               |       name        | database_name | schema_name |    owner     |           comment            |
   ------------------------------------------+-------------------+---------------+-------------+--------------+------------------------------
   | Fri, 23 Jun 1967 07:00:00.123000 +0000 | TEST_MCP_SERVER   | TEST_DATABASE | TEST_SCHEMA | ACCOUNTADMIN | [NULL]                       |
   | Fri, 23 Jun 1967 07:00:00.123000 +0000 | TEST_MCP_SERVER_2 | TEST_DATABASE | TEST_SCHEMA | ACCOUNTADMIN | Test MCP server with comment |
   ```
2. To describe an MCP server, use the following command:

   Copy code

   ```
   DESCRIBE MCP SERVER <server_name>;
   ```

   The following shows the output of the command:

   ```
   |      name       | database_name | schema_name |    owner     | comment |     server_spec        |               created_on               |
   ------------------------------------------------------------------------------------------------------+-------------------------------------
   | TEST_MCP_SERVER | TEST_DATABASE | TEST_SCHEMA | ACCOUNTADMIN | [NULL]  | {"version":1,"tools":[{"name":"product-search","identifier":"db.schema.search_service","type":"CORTEX_SEARCH_SERVICE_QUERY"}]} | Fri, 23 Jun 1967 07:00:00.123000 +0000 |
   ```
3. To drop an MCP server, use the following command:

   Copy code

   ```
   DROP MCP SERVER <server_name>;
   ```

## MCP server URL

To connect to the MCP server, use the URL endpoint with the following format:

Copy code

```
https://<account_url>/api/v2/databases/{database}/schemas/{schema}/mcp-servers/{name}
```

For information about formatting your account URL, see [Account identifiers](/user-guide/admin-account-identifier).

## Access control

### Required privileges

You can use the following privileges to manage access to the MCP server and the underlying tools.

| Privilege | Object | Description |
| --- | --- | --- |
| CREATE | MCP SERVER | Required to create the MCP server |
| OWNERSHIP | MCP SERVER | Required to update the object configuration |
| MODIFY | MCP SERVER | Provides update, drop, describe, show, and use (`tools/list` and `tools/call`) on the object configuration |
| USAGE | MCP SERVER | Required to connect with the MCP server and discover tools |
| USAGE | Cortex Search Service | Required to invoke the Cortex Search tool in the MCP server |
| SELECT | Semantic View | Required to invoke the Cortex Analyst tool in the MCP server |
| USAGE | Cortex Agent | Required to invoke the Cortex Agent as a tool in the MCP server |
| USAGE | User-defined function (UDF) or stored procedure | Required to invoke the UDF or stored procedure as a tool in the MCP server |

Expand

Show lessSee more

### Grant access to a Cortex Agent-based MCP server

The following example creates a dedicated access role and grants it access to an MCP server that exposes a Cortex Agent:

Copy code

```
CREATE ROLE <mcp_access_role>;

GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE <mcp_access_role>;

GRANT USAGE ON WAREHOUSE <warehouse_name> TO ROLE <mcp_access_role>;
GRANT USAGE ON DATABASE <database_name> TO ROLE <mcp_access_role>;
GRANT USAGE ON SCHEMA <database_name>.<schema_name> TO ROLE <mcp_access_role>;
GRANT USAGE ON MCP SERVER <database_name>.<schema_name>.<server_name> TO ROLE <mcp_access_role>;
GRANT USAGE ON AGENT <database_name>.<schema_name>.<agent_name> TO ROLE <mcp_access_role>;

GRANT ROLE <mcp_access_role> TO USER <username>;
```

The role also needs privileges on the resources configured for the agent. Grant only the privileges for the resources that the agent uses. For example:

Copy code

```
GRANT USAGE ON CORTEX SEARCH SERVICE <database_name>.<schema_name>.<search_service_name>
  TO ROLE <mcp_access_role>;

GRANT SELECT ON SEMANTIC VIEW <database_name>.<schema_name>.<semantic_view_name>
  TO ROLE <mcp_access_role>;

GRANT SELECT ON TABLE <database_name>.<schema_name>.<table_name>
  TO ROLE <mcp_access_role>;

GRANT USAGE ON FUNCTION <database_name>.<schema_name>.<function_name>(<argument_type>)
  TO ROLE <mcp_access_role>;

GRANT USAGE ON PROCEDURE <database_name>.<schema_name>.<procedure_name>(<argument_type>)
  TO ROLE <mcp_access_role>;
```

For more information about agent privileges and the privileges required by agent tools, see [Access control and authentication](/user-guide/snowflake-cortex/cortex-agents-setup).

Grant the MCP access role only to users who need it. Don’t grant the role to `PUBLIC` or grant broad access to all current and future tables solely to support an MCP client.

## Set up OAuth authentication

Configure authentication on the MCP client. The Snowflake-managed MCP server supports [OAuth 2.0](/user-guide/oauth-snowflake-overview) aligned with the [authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization) recommendation in the MCP protocol. The Snowflake-managed MCP server doesn’t support dynamic client registration.

By default, MCP servers use Snowflake OAuth. To bind MCP servers to an External OAuth identity provider such as Okta or Microsoft Entra ID, see [Configure External OAuth authentication](#label-cortex-mcp-external-oauth).

A single OAuth security integration (client ID and secret) can be shared across all users in an account. Each user still authenticates individually with their own credentials to obtain an access token, but the client ID and secret from the integration are the same for everyone. A single integration can also issue tokens that work across multiple MCP servers within the same account.

Note

If your Snowflake account uses PrivateLink and you are connecting from a SaaS MCP client
(such as Claude.ai or ChatGPT), configure your MCP client with the **public** MCP server
URL, not the PrivateLink URL. Additionally, enable
`USE_PRIVATELINK_FOR_AUTHORIZATION_ENDPOINT = TRUE` on your OAuth security integration.
This causes Snowflake to redirect the user’s browser to the PrivateLink authorization
endpoint while the token endpoint remains on the public URL so the SaaS vendor’s server
can reach it. For details, see
[Using Snowflake OAuth with PrivateLink and SaaS clients](/user-guide/oauth-snowflake-overview#label-oauth-private-connectivity).

1. First, create the security integration. For information about this command, see [CREATE SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/create-security-integration-oauth-snowflake).

   Copy code

   ```
   CREATE [ OR REPLACE ] SECURITY INTEGRATION [IF NOT EXISTS] <integration_name>
     TYPE = OAUTH
     OAUTH_CLIENT = CUSTOM
     ENABLED = TRUE
     OAUTH_CLIENT_TYPE = 'CONFIDENTIAL'
     OAUTH_REDIRECT_URI = '<redirect_URI>'
     OAUTH_USE_SECONDARY_ROLES = NONE
     ALLOWED_ROLES_LIST = ('<mcp_access_role>')
   ```

   `ALLOWED_ROLES_LIST` restricts the integration to the roles intended for MCP access. If the integration serves MCP servers with different access roles, include each role in the list.

   If your MCP client requires multiple redirect URIs (for example, VS Code registers more than one callback URL),
   use `OAUTH_ALTERNATE_REDIRECT_URIS` to specify additional URIs:

   Copy code

   ```
   CREATE [ OR REPLACE ] SECURITY INTEGRATION [IF NOT EXISTS] <integration_name>
     TYPE = OAUTH
     OAUTH_CLIENT = CUSTOM
     ENABLED = TRUE
     OAUTH_CLIENT_TYPE = 'CONFIDENTIAL'
     OAUTH_REDIRECT_URI = '<primary_redirect_URI>'
     OAUTH_ALTERNATE_REDIRECT_URIS = ('<alternate_URI_1>', '<alternate_URI_2>')
     OAUTH_USE_SECONDARY_ROLES = NONE
     ALLOWED_ROLES_LIST = ('<mcp_access_role>')
   ```
2. Then, call the system function to retrieve your client id and keys for client configuration. The integration name is case sensitive and must be in uppercase.

   Copy code

   ```
   SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS('<integration_name>');
   ```

### Role behavior in OAuth sessions

OAuth scopes control only the **primary** role for the MCP session. Secondary roles are separate
and are controlled by the OAuth security integration, not by `OAUTH_SCOPES_SUPPORTED`.

By default, MCP servers advertise `session:role:all` in Protected Resource Metadata, and the OAuth session uses the connecting user’s `DEFAULT_ROLE` as the primary role.

Special primary-role scopes:

- `session:role:all`: Use the user’s `DEFAULT_ROLE` as the primary role. Despite the name, this
  doesn’t activate every role or secondary roles.
- `session:role-any`: Allow any primary role granted to the user, when any-role mode is enabled on
  the authorization server. For External OAuth, that requires
  `EXTERNAL_OAUTH_ANY_ROLE_MODE = ENABLE` or `ENABLE_FOR_PRIVILEGE` on the security integration.
- `session:role:<role_name>`: Use that named role as the primary role.

To control which primary-role scopes MCP clients discover, set the `OAUTH_SCOPES_SUPPORTED` parameter at the account, database, or schema level. This parameter is independent of External OAuth: set it alone to customize scopes for Snowflake OAuth, or set it together with `OAUTH_AUTHORIZATION_SERVER` when you bind MCP servers to an external identity provider (IdP). For accepted scope values and SET-time validation rules, see [OAUTH\_SCOPES\_SUPPORTED](/sql-reference/parameters#label-oauth-scopes-supported).

Copy code

```
ALTER SCHEMA analytics_db.mcp_schema
  SET OAUTH_SCOPES_SUPPORTED = 'session:role:ANALYST,session:role:DATA_ENGINEER';
```

Whether the advertised primary role is used in the session depends on the MCP client:

- Clients that request one of the advertised `session:role:<role_name>` scopes use that role as the primary role for the session.
- Some MCP clients (such as Claude) don’t support specifying a role in the OAuth scope and request `session:role:all` instead, so the session uses the user’s `DEFAULT_ROLE` even when other scopes are advertised.

Secondary roles aren’t controlled by OAuth scopes. For Snowflake OAuth, they follow
`OAUTH_USE_SECONDARY_ROLES` on the security integration:

- Recommended for MCP: leave `OAUTH_USE_SECONDARY_ROLES = NONE` (the default) and restrict
  `ALLOWED_ROLES_LIST` to the MCP access role, so the session uses only the user’s
  `DEFAULT_ROLE` as the primary role. See [Prefer a least-privileged MCP OAuth configuration](#label-cortex-mcp-migrate-oauth-integration).
- To activate the user’s default secondary roles when the session opens, set
  `OAUTH_USE_SECONDARY_ROLES = IMPLICIT`. Snowflake OAuth doesn’t support in-session secondary
  role switching with [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles). For details,
  see [CREATE SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/create-security-integration-oauth-snowflake).
- For External OAuth, see [Using secondary roles with External OAuth](/user-guide/oauth-ext-overview#label-ext-oauth-secondary-roles).

To ensure the correct primary role is used when clients rely on `session:role:all` or the user’s `DEFAULT_ROLE`:

- Set each user’s `DEFAULT_ROLE` to the role that has the required privileges on the MCP server and its tools.
- Ensure each user has a `DEFAULT_WAREHOUSE` set (sessions fail to initialize if this is null).

Copy code

```
ALTER USER <username> SET DEFAULT_ROLE = '<mcp_access_role>' DEFAULT_WAREHOUSE = '<warehouse_name>';
```

If you need different data access levels per user and clients don’t honor role scopes, use separate MCP servers with dedicated roles.

Note

If an MCP client (such as Claude) requests the `session:role:all` OAuth scope, the consent screen
might display “secondary roles = ALL” even when your security integration has
`OAUTH_USE_SECONDARY_ROLES = NONE`. That label is cosmetic and doesn’t mean the scope activates
secondary roles. Snowflake enforces the security integration setting regardless of what the client
requests, so default secondary roles aren’t activated unless you set
`OAUTH_USE_SECONDARY_ROLES = IMPLICIT`.

### Configure External OAuth authentication

By default, MCP servers use Snowflake OAuth for authentication. To let MCP clients authenticate against your organization’s existing identity provider (IdP) such as Okta or Microsoft Entra ID, set `OAUTH_AUTHORIZATION_SERVER` to bind MCP servers to an External OAuth security integration. Optionally set `OAUTH_SCOPES_SUPPORTED` to advertise specific scopes in Protected Resource Metadata. You can also set `OAUTH_SCOPES_SUPPORTED` on its own for Snowflake OAuth; see [Role behavior in OAuth sessions](#label-cortex-mcp-role-behavior).

When an External OAuth integration is bound to a schema, database, or account, Snowflake advertises the external issuer’s metadata in [Protected Resource Metadata (RFC 9728)](https://www.rfc-editor.org/rfc/rfc9728). MCP clients that support OAuth resource metadata discovery fetch this information automatically to find the correct authorization server and scopes.

#### Default behavior

When neither parameter is set, MCP servers use Snowflake OAuth and advertise `session:role:all` as the supported scope.

#### Steps to configure External OAuth for MCP servers

1. Create an External OAuth security integration for your IdP. For details, see [CREATE SECURITY INTEGRATION (External OAuth)](/sql-reference/sql/create-security-integration-oauth-external).

   Copy code

   ```
   CREATE OR REPLACE SECURITY INTEGRATION external_oauth_okta
     TYPE = EXTERNAL_OAUTH
     ENABLED = TRUE
     EXTERNAL_OAUTH_TYPE = OKTA
     EXTERNAL_OAUTH_ISSUER = '<OKTA_ISSUER>'
     EXTERNAL_OAUTH_JWS_KEYS_URL = '<OKTA_JWS_KEY_ENDPOINT>'
     EXTERNAL_OAUTH_AUDIENCE_LIST = ('https://<orgname>-<account_name>.snowflakecomputing.com')
     EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM = 'sub'
     EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = 'login_name';
   ```
2. Set `OAUTH_AUTHORIZATION_SERVER` at the account, database, or schema level to bind MCP servers in that scope to the integration. For parameter details, see [OAUTH\_AUTHORIZATION\_SERVER](/sql-reference/parameters#label-oauth-authorization-server).

   Copy code

   ```
   -- Schema level (applies to all MCP servers in the schema)
   ALTER SCHEMA analytics_db.mcp_schema SET OAUTH_AUTHORIZATION_SERVER = external_oauth_okta;

   -- Database level (applies to all MCP servers in the database)
   ALTER DATABASE analytics_db SET OAUTH_AUTHORIZATION_SERVER = external_oauth_okta;

   -- Account level (applies to all MCP servers in the account)
   ALTER ACCOUNT SET OAUTH_AUTHORIZATION_SERVER = external_oauth_okta;
   ```
3. Optionally, set `OAUTH_SCOPES_SUPPORTED` to advertise specific scopes in the Protected Resource Metadata response. This parameter is independent of `OAUTH_AUTHORIZATION_SERVER`: you can set it alone for Snowflake OAuth, or together with an External OAuth binding as shown here. For accepted scope values, see [OAUTH\_SCOPES\_SUPPORTED](/sql-reference/parameters#label-oauth-scopes-supported). For how scopes interact with primary and secondary roles, see [Role behavior in OAuth sessions](#label-cortex-mcp-role-behavior).

   Copy code

   ```
   ALTER SCHEMA analytics_db.mcp_schema SET OAUTH_SCOPES_SUPPORTED = 'session:role:ANALYST,session:role:DATA_ENGINEER';
   ```
4. Create the MCP server. The server inherits the OAuth binding from the enclosing schema, database, or account.

   Copy code

   ```
   CREATE MCP SERVER analytics_db.mcp_schema.docs_mcp_server
     FROM SPECIFICATION $$
     tools:
       - name: "docs-search"
         type: "CORTEX_SEARCH_SERVICE_QUERY"
         identifier: "analytics_db.mcp_schema.docs_search_service"
         description: "Search service for internal documentation"
         title: "Documentation Search"
     $$;
   ```

When a client connects to `docs_mcp_server`, Snowflake returns a `401` response with a `WWW-Authenticate` header pointing to the Protected Resource Metadata endpoint. The client fetches the metadata document, which advertises the Okta issuer URL from `external_oauth_okta` in `authorization_servers`, and then initiates the Okta OAuth flow. After obtaining a token, the client retries the request. Snowflake accepts the OAuth token only when it was issued by the bound External OAuth integration; a Snowflake OAuth token, or a token from a different External OAuth integration, is rejected. This issuer check applies only to OAuth calls against MCP server endpoints; other authenticators and non-MCP endpoints aren’t affected.

#### Parameter inheritance

`OAUTH_AUTHORIZATION_SERVER` and `OAUTH_SCOPES_SUPPORTED` follow Snowflake’s standard parameter inheritance. Each parameter resolves independently by checking the following levels in order:

1. Schema
2. Database
3. Account

This means you can set a default authorization server at the account level and override it for specific schemas, or have some schemas use External OAuth while others use Snowflake OAuth (no parameter set).

When `OAUTH_AUTHORIZATION_SERVER` is set and `OAUTH_SCOPES_SUPPORTED` isn’t, Snowflake doesn’t advertise `session:role:all`. Instead:

- If the bound integration has `EXTERNAL_OAUTH_ANY_ROLE_MODE = ENABLE` or `ENABLE_FOR_PRIVILEGE`, the Protected Resource Metadata response includes `session:role-any`.
- Otherwise, the Protected Resource Metadata response includes an empty `scopes_supported` list, and the MCP client uses its own configured scopes or prompts the user.

#### Failure modes

The following conditions change what Snowflake advertises in the Protected Resource Metadata response, and how token enforcement behaves:

| Condition | Behavior |
| --- | --- |
| The integration named in `OAUTH_AUTHORIZATION_SERVER` is dropped | The Protected Resource Metadata response includes an empty `authorization_servers` list. Snowflake doesn’t fall back to Snowflake OAuth. Inbound OAuth requests to MCP servers in that scope are rejected. |
| The integration is disabled | Same as when the integration is dropped. |
| A role specified in `OAUTH_SCOPES_SUPPORTED` is dropped or renamed | Snowflake continues to publish the configured scope string in Protected Resource Metadata. Authentication using that scope fails during the OAuth flow. |
| `OAUTH_SCOPES_SUPPORTED` is set but `OAUTH_AUTHORIZATION_SERVER` isn’t | The scopes apply to Snowflake OAuth discovery. |

Expand

Show lessSee more

For information about External OAuth, see [External OAuth overview](/user-guide/oauth-ext-overview#label-ext-oauth-mcp-integration).

For information about the parameters, see [OAUTH\_AUTHORIZATION\_SERVER](/sql-reference/parameters#label-oauth-authorization-server) and [OAUTH\_SCOPES\_SUPPORTED](/sql-reference/parameters#label-oauth-scopes-supported).

### Prefer a least-privileged MCP OAuth configuration

Snowflake recommends configuring MCP OAuth so the session uses the connecting user’s
`DEFAULT_ROLE` without activating default secondary roles. That pattern matches the
`OAUTH_USE_SECONDARY_ROLES = NONE` and `ALLOWED_ROLES_LIST` settings in the earlier CREATE examples.
Secondary roles still work when you set `OAUTH_USE_SECONDARY_ROLES = IMPLICIT`; the
recommendation is to avoid that for MCP unless you intentionally need broader privileges.

If an existing MCP OAuth integration uses `OAUTH_USE_SECONDARY_ROLES = IMPLICIT`, update it as follows:

1. Configure or select a Cortex Agent with the governed resources that the client needs.
2. Update the primary MCP server to expose the agent. Remove direct SQL execution from that server unless the client requires it.
3. Create or select a least-privileged MCP access role and grant access to the MCP server, agent, and agent resources.
4. Set the access role and warehouse as the user’s defaults.
5. Disable secondary roles and restrict the integration to the MCP access role:

   Copy code

   ```
   ALTER SECURITY INTEGRATION <integration_name>
     SET OAUTH_USE_SECONDARY_ROLES = NONE;

   ALTER SECURITY INTEGRATION <integration_name>
     SET ALLOWED_ROLES_LIST = ('<mcp_access_role>');
   ```
6. Reconnect the MCP client and verify the effective role, visible tools, agent routing, and resource access.

## Connect from common MCP clients

Once you have created the MCP server and the OAuth security integration, you can connect from any MCP-compatible client by pointing it at your MCP server URL:

Copy code

```
https://<account_url>/api/v2/databases/<database>/schemas/<schema>/mcp-servers/<name>
```

Important

You may need to use hyphens (`-`) instead of underscores (`_`) in your account URL with some clients.

The following examples show how to register the Snowflake-hosted MCP server in commonly used clients. Replace the URL with your own MCP server URL.

Claude.ai / Claude DesktopChatGPTCursorOther clients

Claude (both `claude.ai` and Claude Desktop) supports Snowflake MCP servers in the Claude Directory or as a Custom Connector. Claude handles the OAuth flow against the security integration you created above. For Anthropic’s general guidance, see [Get started with custom connectors using remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).

1. In Claude, open **Settings** → **Connectors**.
2. Click **Add custom connector** or search for Snowflake in **Browse connectors**.
3. Provide a **Name** (for example, `Snowflake`) and the **MCP Server URL**:

   Copy code

   ```
   https://<account_url>/api/v2/databases/<database>/schemas/<schema>/mcp-servers/<name>
   ```
4. Add the client ID and secret from the security integration you created.
5. Click **Add**. Claude opens a browser window and prompts you to sign in to Snowflake and approve the OAuth consent screen.
6. After approving, the Snowflake tools appear in the connector list and can be used in any Claude conversation.

Note

When configuring the OAuth security integration for Claude, set `OAUTH_REDIRECT_URI` to the redirect URI shown by Claude during connector setup (typically `https://claude.ai/api/mcp/auth_callback` for `claude.ai` and a localhost URI for Claude Desktop). Claude requests the `session:role:all` scope; the session still uses the user’s `DEFAULT_ROLE`.

ChatGPT supports remote MCP servers as **Connectors** in Developer Mode. For OpenAI’s general guidance on adding remote MCP servers, see [Remote MCP servers](https://platform.openai.com/docs/guides/tools-remote-mcp) in the OpenAI documentation.

1. In ChatGPT, open **Settings** → **Connectors** → **Advanced**, and enable **Developer mode**.
2. Return to **Settings** → **Connectors** and click **Create**.
3. Fill in the connector form:
   - **Name**: `Snowflake` (or any label).
   - **MCP Server URL**:

     Copy code

     ```
     https://<account_url>/api/v2/databases/<database>/schemas/<schema>/mcp-servers/<name>
     ```
   - **Authentication**: select **OAuth**.
   - Fill in the client ID and secret from the security integration you created.
4. Click **Create**. ChatGPT opens a browser window for you to sign in to Snowflake and approve the OAuth consent screen.
5. The Snowflake tools become available in chats that have the connector enabled.

Note

Set `OAUTH_REDIRECT_URI` on your security integration to the redirect URI ChatGPT displays during connector creation.

Cursor supports remote MCP servers via `mcp.json`. For the full Cursor configuration reference, see [Model Context Protocol](https://cursor.com/docs/mcp) in the Cursor documentation. You can also browse for the Snowflake plugin in the Cursor marketplace.

Edit `~/.cursor/mcp.json` (global) or `<project>/.cursor/mcp.json` (project) and add an entry under `mcpServers`:

Copy code

```
{
  "mcpServers": {
    "snowflake": {
      "url": "https://<account_url>/api/v2/databases/<database>/schemas/<schema>/mcp-servers/<name>",
      "auth": {
        "CLIENT_ID": "${env:MCP_CLIENT_ID}",
        "CLIENT_SECRET": "${env:MCP_CLIENT_SECRET}"
      }
    }
  }
}
```

After saving, open **Cursor Settings** → **MCP**, locate the `snowflake` server, and click **Sign in**. Cursor opens a browser window to complete the Snowflake OAuth flow. Once connected, the Snowflake tools appear in Cursor’s tool list.

For any other MCP client that supports remote (HTTP) MCP servers, register the Snowflake-hosted MCP server using your URL:

Copy code

```
https://<account_url>/api/v2/databases/<database>/schemas/<schema>/mcp-servers/<name>
```

## Network policies for MCP clients

If your Snowflake account has [network policies](/user-guide/network-policies) enabled, you must allow inbound connections from your MCP client’s outbound IP addresses. When a remote MCP client (such as Claude, ChatGPT, or Cursor) connects to your Snowflake-managed MCP server, the request originates from the client provider’s infrastructure, not from the end user’s browser. If those IP addresses are not permitted by your network policy, the connection will be blocked.

When a network policy blocks the token request, Snowflake can return `error: invalid_client` from the `/oauth/token-request` endpoint. That
error is the same response clients see for incorrect credentials or an unsupported authentication method, so check your network policy if
client credentials and authentication method look correct.

To allow an MCP client to reach your Snowflake account, create a [network rule](/user-guide/network-rules) that includes the client provider’s outbound IP addresses, then add that rule to your account’s network policy:

Copy code

```
CREATE NETWORK RULE mcp_client_ingress_rule
  MODE = INGRESS
  TYPE = IPV4
  VALUE_LIST = ('<client_provider_ip_1>', '<client_provider_ip_2>', ...);

ALTER NETWORK POLICY <your_policy_name> ADD ALLOWED_NETWORK_RULE_LIST = ('mcp_client_ingress_rule');
```

Replace the IP addresses with the outbound IPs published by your MCP client provider. For example, Anthropic publishes the outbound IP addresses used by Claude at <https://platform.claude.com/docs/en/api/ip-addresses>.

Note

This applies to all MCP client providers, not just Claude. Check your provider’s documentation for their outbound IP addresses used for remote MCP connections.

For Snowflake OAuth client authentication at the token endpoint, see
[Configure Snowflake OAuth for custom clients](/user-guide/oauth-custom#label-oauth-client-authentication).

## Troubleshoot MCP client connections

If your MCP client can’t connect or a tool doesn’t behave as expected, use this table to identify the likely cause:

| Symptom | Likely cause | Recommended check |
| --- | --- | --- |
| OAuth consent or connection fails | The redirect URI doesn’t match the client configuration | Set `OAUTH_REDIRECT_URI` to the exact callback URI shown by the MCP client. |
| Authentication succeeds, but the MCP server doesn’t connect | The MCP server URL is incomplete | Use the fully qualified database, schema, and MCP server path. |
| The client reports a hostname-related connection failure | The account hostname contains underscores | Replace underscores (`_`) with hyphens (`-`) in the account hostname. |
| The session fails to initialize | The user doesn’t have a default warehouse | Set `DEFAULT_WAREHOUSE` on the user and grant the default role `USAGE` on that warehouse. |
| The session uses the wrong data access role | The user’s default role isn’t the MCP access role | Set and verify the user’s `DEFAULT_ROLE`. |
| Tools aren’t visible | The default role doesn’t have access to the MCP server | Grant `USAGE` on the MCP server to the user’s default role. |
| A visible tool can’t be invoked | The default role is missing an underlying object privilege | Grant the privilege required by the agent, search service, semantic view, function, or procedure. |
| A SaaS client can’t reach a PrivateLink account | The client is using a private endpoint | Use the public MCP server URL and set `USE_PRIVATELINK_FOR_AUTHORIZATION_ENDPOINT = TRUE` on the OAuth integration. |
| A remote MCP client is blocked by a network policy | The client’s outbound IP addresses aren’t allowed | Add the MCP client provider’s outbound IP addresses to the account network policy. |

Expand

Show lessSee more

## Interact with the MCP server using a custom MCP client

For information about building a custom MCP client, see [Build an MCP client](https://modelcontextprotocol.io/docs/develop/build-client).

Note

The Snowflake MCP server currently only supports tool capabilities.

### Discover and invoke tools

The MCP clients can discover and invoke tools with `tools/list` and `tools/call` requests.

To discover or invoke tools, issue a POST call as shown in the [tools/list request](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#calling-tools):

As of August 20, 2026, the server returns `tools/call` responses as a
[Server-Sent Events (SSE)](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
stream rather than a single JSON body. Your client must list both content types in the `Accept` header:

```
Accept: application/json, text/event-stream
```

The response examples in this section show the JSON payload that the server sends in each `data:` event.
The stream closes with a `data: [DONE]` event. Clients that follow the MCP specification (2025-11-25)
handle this automatically. For details, see
[MCP: Streaming responses for tool calls (August 2026)](/release-notes/bcr-bundles/un-bundled/bcr-2405).

For the Analyst tool, your client passes messages in the request. The SQL statement is listed in the output. You must pass the name of the tool that you’re invoking in the request in the `name` parameter.

Copy code

```
POST /api/v2/databases/<database>/schemas/<schema>/mcp-servers/<name>
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "test-analyst",
            "arguments": {
                "message": "text"
            }
        }
    }
```

The following example shows the response:

Copy code

```
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "content": [
            {
                "type": "text",
                "text": "string"
            }
        ]
    }
}
```

For Search tool requests, your client can pass the query and the following optional arguments:

- columns
- limit

The search results and request ID are returned in the output. You must pass the name of the tool that you’re invoking in the request as the `name` parameter.

Copy code

```
POST /api/v2/databases/{database}/schemas/{schema}/mcp-servers/{name}
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "product-search",
            "arguments": {
                "query": "Hotels in NYC",
                "columns": array of strings,
                "limit": int
            }
        }
  }
```

The following example shows the response:

Copy code

```
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "results": {}
    }
}
```

## Limitations

Snowflake-managed MCP server does not support the following constructs in the MCP protocol: resources, prompts, roots, notifications, version negotiations, life cycle phases, and sampling.

Each MCP server supports a maximum of 50 tools. This limit includes all tool types: Cortex Search, Cortex Analyst, Cortex Agents, SQL execution, and custom (generic) tools. If you need more tools, create additional MCP servers. Higher tool counts can degrade tool-selection accuracy.

Tool responses are subject to size limits to prevent LLM context window saturation:

- **Generic tools**: Responses are truncated at 250 KB.
- **SQL execution tool**: Responses are truncated at 250 KB.

If a query result exceeds the size limit, the response is truncated. To work around this limit, use narrower queries that return fewer columns or rows.

By default, MCP OAuth sessions use the connecting user’s `DEFAULT_ROLE` as the primary role.
You can advertise other primary-role scopes with `OAUTH_SCOPES_SUPPORTED`. Secondary roles are
controlled by the OAuth security integration; the recommended MCP configuration leaves them
disabled (`OAUTH_USE_SECONDARY_ROLES = NONE`). For details, see
[Role behavior in OAuth sessions](#label-cortex-mcp-role-behavior).

MCP server objects aren’t replicated in failover groups. If you use replication, you must recreate MCP server objects on the secondary account. OAuth security integrations are replicated.
