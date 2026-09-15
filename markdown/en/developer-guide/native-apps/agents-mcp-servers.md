# Use Cortex Agents and MCP servers in an app

This topic describes how a Snowflake Native App can create [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents)
and [Snowflake-managed MCP servers](/user-guide/snowflake-cortex/cortex-agents-mcp),
and how a provider can register an SPCS service endpoint as an SPCS-hosted MCP
server. With these capabilities, an app can offer a conversational experience
over its shared data and functionality, and expose its tools to other agents
inside or outside Snowflake.

## Overview

A Snowflake Native App can include three kinds of AI objects:

Cortex Agents
:   Agents that the app creates in its setup script or at runtime. App-created
    agents appear in Snowflake CoWork and are callable from the REST,
    Python, and SQL APIs, just like standalone agents.

Snowflake-managed MCP servers
:   MCP servers that wrap Snowflake-native objects (Cortex Search services, Cortex
    Analyst semantic views, Cortex Agents, UDFs, and stored procedures) as MCP
    tools. The app creates these by using
    [CREATE MCP SERVER](/sql-reference/sql/create-mcp-server).

SPCS-hosted MCP servers
:   MCP servers that register an SPCS service endpoint with the MCP client
    infrastructure used by Cortex Agents and Snowflake CoWork. They let
    the app expose arbitrary code (in any language or framework) running in
    Snowpark Container Services as MCP tools. The app creates these by using
    `CREATE CUSTOM MCP SERVER`.

These capabilities are separate from, and complementary to, sharing agents
created in the provider account. For information about sharing standalone
agents, see [Share Cortex Agents](/user-guide/snowflake-cortex/cortex-agents-sharing).

### Security model

Cortex Agents created by an app run under
[restricted caller’s rights](/developer-guide/native-apps/restricted-callers-rights) (RCR). RCR enforces
that an app’s agent can’t access consumer data without an explicit grant from
the consumer.

Every tool invocation from an app-created agent requires both of the following:

- **Consumer privilege**: a user in the consumer account has the privilege
  needed on the target object. This is the same caller’s-rights model used by
  standalone agents.
- **App caller grant**: the consumer admin has performed a caller grant to
  the app for the object. For more information, see
  [GRANT CALLER](/sql-reference/sql/grant-caller).

Key points:

- The app gets implicit caller grants on objects that it owns. The provider
  doesn’t need to request explicit caller grants for in-app objects.
- Consumer-owned objects require explicit `GRANT CALLER ... TO APPLICATION`
  from the consumer admin.
- When a tool runs in owner’s rights (for example, a procedure created with
  `EXECUTE AS OWNER`), execution switches to the owner’s identity. RCR
  restrictions don’t apply within that tool’s scope.
- When a tool runs in restricted caller’s rights, for example a procedure
  created with `EXECUTE AS RESTRICTED CALLER` and owned by a role other
  than the app, RCR restrictions compose by intersection. Each link in a
  chain makes the effective access stricter, never looser.
- Owner’s rights agents aren’t supported. A provider can still surface an agent
  through an owner’s-rights code entity (for example, a Streamlit app or an
  Snowpark Container Services service) that calls the agent using the app’s identity.

Snowflake-managed MCP servers created by an app are restricted to app-owned
tools. They can’t expose tools that aren’t owned by the app, and they can’t
include the `SYSTEM_EXECUTE_SQL` tool. This restriction prevents an installed
app’s MCP server from being used as a way to access consumer data or run
arbitrary SQL in the consumer’s account.

### Before you begin

To use Cortex Agents in a Snowflake Native App, the consumer account must have both
Cortex Agents and Snowflake CoWork enabled. For more information, see
[Cortex Agents](/user-guide/snowflake-cortex/cortex-agents).

## Cortex Agents in a Native App

This section describes the provider and consumer admin workflows for creating
and using a Cortex Agent in a Snowflake Native App.

### Provider: Create the agent

A provider creates an agent in the app’s setup script, or at runtime in a
code entity. The following example creates an agent that includes a Cortex
Analyst tool backed by an app-owned semantic view, a second Cortex Analyst tool
backed by a consumer-owned semantic view, and a custom procedure tool that calls
an app-owned procedure:

Copy code

```
CREATE OR REPLACE AGENT core.my_agent
  FROM SPECIFICATION $$
models:
  orchestration: auto
instructions:
  response: "Provide concise, accurate financial analysis answers."
  orchestration: "Use the Cortex Analyst tools for financial data questions."
tools:
  - tool_spec:
      type: "cortex_analyst_text_to_sql"
      name: "Analyst1"
      description: "Answers questions about the app's financial data"
  - tool_spec:
      type: "cortex_analyst_text_to_sql"
      name: "Analyst2"
      description: "Answers questions about the consumer's portfolio data"
  - tool_spec:
      type: generic
      name: Procedure1
      description: "Return current app metadata about the specified category"
      input_schema:
        type: object
        properties:
          category:
            type: string
            description: "Category of metadata to return"
        required: ["category"]
tool_resources:
  Analyst1:
    semantic_view: "core.my_semantic_view"
    execution_environment:
      type: warehouse
      warehouse: "MY_APP_WH"
  Analyst2:
    semantic_view: "consumer_db.public.consumer_semantic_view"
    execution_environment:
      type: warehouse
      warehouse: "MY_APP_WH"
  Procedure1:
    identifier: core.get_app_metadata
    type: procedure
    execution_environment:
      type: warehouse
      warehouse: "MY_APP_WH"
$$;
```

Notes:

- Partially qualified identifiers (such as `core.my_semantic_view`) are
  resolved relative to the agent’s database and schema. This is the
  recommended pattern inside a Snowflake Native App, because the app database name is
  only known at install time.
- Tool identifiers aren’t resolved when the agent is created. A provider can
  declare tools before the underlying objects are created or before the app
  has access to them.
- We recommend using `orchestration: auto` instead of a specific model name.
  A specific model might not be available in the consumer’s region.

For information about Cortex Agent SQL commands, see
[Cortex Agent commands](/sql-reference/commands-cortex-agent).

### Provider: Ship skills with the app

You can ship [agent skills](/user-guide/snowflake-cortex/cortex-agents-skills)
with a Snowflake Native App by writing `SKILL.md` files to an app-owned internal stage
in the setup script, then referencing that stage from the agent specification.

Because the setup script runs in the consumer account, you can’t use `PUT` to
upload files from a local machine. Create an internal stage, unload the skill
content with [COPY INTO <location>](/sql-reference/sql/copy-into-location), and grant `READ` on
the stage to the application roles that should use the agent.

Each `SKILL.md` file uses YAML frontmatter for `name` and `description`. Put
the skill’s execution instructions in the Markdown body after the closing
`---`. Cortex Agents ignore an `instructions` key in the frontmatter.

The file format options in the following example write the skill content as
plain, uncompressed text. `TYPE = CSV` is the text-based unload format, and
setting `COMPRESSION`, `RECORD_DELIMITER`, and `FIELD_DELIMITER` to `NONE`
prevents Snowflake from compressing the output or inserting CSV delimiters into
the Markdown. `SINGLE = TRUE` writes one file instead of multiple files, and
the `SKILL.md` filename in the target path gives that file its name.

Copy code

```
CREATE STAGE IF NOT EXISTS core.skills_stage;

COPY INTO @core.skills_stage/app_skill/SKILL.md
  FROM (
    SELECT $$---
name: app_skill
description: Answers questions that match this skill's description.
---
Follow the app-specific workflow in this skill.
$$
  )
  FILE_FORMAT = (
    TYPE = CSV
    COMPRESSION = NONE
    RECORD_DELIMITER = NONE
    FIELD_DELIMITER = NONE
  )
  OVERWRITE = TRUE
  SINGLE = TRUE;

GRANT READ ON STAGE core.skills_stage TO APPLICATION ROLE my_app_role;
```

Then reference the skill folder (not the `SKILL.md` file) in the agent
specification. Use a partially qualified stage path so the path doesn’t depend
on the installed application database name:

Copy code

```
CREATE OR REPLACE AGENT core.my_agent
  FROM SPECIFICATION $$
models:
  orchestration: auto
instructions:
  response: "Provide concise answers. Use the app_skill when the question matches its description."
skills:
  - name: app_skill
    source:
      type: STAGE
      path: @core.skills_stage/app_skill
$$;
```

Repeat the `COPY INTO` statement for each skill, using a distinct folder under
the stage (for example `@core.skills_stage/another_skill/SKILL.md`). If a skill
includes supporting files, unload each file into the same folder with a
separate `COPY INTO` statement.

For general skill authoring and stage layout, see
[Agent skills](/user-guide/snowflake-cortex/cortex-agents-skills).

### Provider: Create the tools and grant access

The application also creates the tools that the agent uses and grants access
to them through application roles:

Copy code

```
CREATE SEMANTIC VIEW core.my_semantic_view ...;
CREATE PROCEDURE core.get_app_metadata(category STRING) RETURNS STRING ...;

GRANT USAGE ON AGENT core.my_agent TO APPLICATION ROLE my_app_role;

GRANT SELECT ON SEMANTIC VIEW core.my_semantic_view
  TO APPLICATION ROLE my_app_role;
GRANT USAGE ON PROCEDURE core.get_app_metadata(STRING)
  TO APPLICATION ROLE my_app_role;
```

### Consumer admin: Audit the agent before granting access

Before granting users access to an app-created agent, the consumer admin should
review the agent’s full specification (model, tools, system prompt, and
referenced objects) by using [DESCRIBE AGENT](/sql-reference/sql/desc-agent) or through
the agent UI:

Copy code

```
DESC AGENT my_app.core.my_agent;
```

### Consumer admin: Grant caller access on consumer objects

Without caller grants, the agent can’t use consumer objects, even if the
consumer user has privileges on them. The following example grants the app the
caller privileges that the agent needs:

Copy code

```
GRANT CALLER USAGE ON WAREHOUSE my_app_wh TO APPLICATION my_app;

GRANT CALLER USAGE ON DATABASE my_db TO APPLICATION my_app;
GRANT CALLER USAGE ON SCHEMA my_db.my_schema TO APPLICATION my_app;

GRANT INHERITED CALLER SELECT ON ALL SEMANTIC VIEWS IN SCHEMA my_db.my_schema
  TO APPLICATION my_app;
GRANT INHERITED CALLER SELECT ON ALL TABLES IN SCHEMA my_db.my_schema
  TO APPLICATION my_app;
```

Alternatively, grant access to individual objects:

Copy code

```
GRANT CALLER SELECT ON SEMANTIC VIEW my_db.my_schema.consumer_semantic_view
  TO APPLICATION my_app;
GRANT CALLER SELECT ON TABLE my_db.my_schema.my_sv_underlying_table
  TO APPLICATION my_app;
```

For more information about caller grants, see
[GRANT CALLER](/sql-reference/sql/grant-caller).

### Consumer admin: Delegate to user roles

After granting caller access to the app, delegate access to the underlying
objects and the application role to the user roles that should be allowed to
use the agent:

Copy code

```
GRANT USAGE ON DATABASE my_db TO ROLE analyst_role;
GRANT USAGE ON SCHEMA my_db.my_schema TO ROLE analyst_role;
GRANT SELECT ON SEMANTIC VIEW my_db.my_schema.my_sv TO ROLE analyst_role;
GRANT SELECT ON TABLE my_db.my_schema.my_sv_underlying_table
  TO ROLE analyst_role;

GRANT APPLICATION ROLE my_app.app_public TO ROLE analyst_role;
```

### Use the agent

After the consumer admin grants the application role to a user role, the agent
is available in all the same places as a standalone agent. For example:

- [Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork).
  The agent appears automatically.
- The Cortex Agents REST API. Send a request to
  `POST /api/v2/databases/{app}/schemas/{schema}/agents/{name}:run`.
  For more information, see [Cortex Agents REST API](/user-guide/snowflake-cortex/cortex-agents-rest-api).
- SQL. Call [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex).

## MCP servers in a Native App

A Snowflake Native App can create two kinds of MCP servers:

| Kind | What it wraps | Use when |
| --- | --- | --- |
| SPCS-hosted MCP server (`CREATE CUSTOM MCP SERVER`) | The app’s own SPCS service endpoint | You need arbitrary compute, such as ML inference, proprietary algorithms, external API calls, or a custom language or framework. |
| Snowflake-managed MCP server ([CREATE MCP SERVER](/sql-reference/sql/create-mcp-server)) | Existing Snowflake objects (Cortex Search, Cortex Analyst, Cortex Agents, UDFs, and stored procedures) | Your tools are expressible as Snowflake-native objects. |

Expand

Show lessSee more

The following sections describe how to create each kind. For a detailed
breakdown of when to use each, see [When to use SPCS-hosted or Snowflake-managed MCP](#label-native-apps-mcp-when-to-use).

### SPCS-hosted MCP servers

An SPCS-hosted MCP server is a metadata object that links an SPCS service
endpoint to the MCP client infrastructure used by Cortex Agents and Snowflake
Intelligence. It doesn’t deploy a service. It registers an existing SPCS
endpoint as MCP-discoverable. For information about how to deploy SPCS
services in a Snowflake Native App, see
[Tutorial 2: Create an app with containers](/developer-guide/native-apps/tutorials/na-spcs-tutorial).

#### Provider: Write the MCP server

The following example shows a minimal MCP echo server that uses the Streamable
HTTP transport on port 8080, with a separate health check endpoint on port 8081
for SPCS readiness probes:

Copy code

```
"""Example MCP echo server -- Streamable HTTP transport on port 8080."""

import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from mcp.server.fastmcp import FastMCP

os.environ.setdefault("FASTMCP_PORT", "8080")
os.environ.setdefault("FASTMCP_HOST", "0.0.0.0")

mcp = FastMCP("echo-server", host="0.0.0.0", port=8080)

@mcp.tool()
def echo(message: str) -> str:
    """Echo back the provided message."""
    return f"Echo: {message}"

@mcp.tool()
def reverse(text: str) -> str:
    """Reverse the provided text string."""
    return text[::-1]

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

def start_health_server():
    server = HTTPServer(("0.0.0.0", 8081), HealthHandler)
    server.serve_forever()

if __name__ == "__main__":
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    mcp.run(transport="streamable-http")
```

#### Provider: Create the SPCS service

In the app’s setup script, create the SPCS service that hosts the MCP server,
and grant access to its endpoint:

Copy code

```
CREATE SERVICE IF NOT EXISTS services.my_service
  IN COMPUTE POOL my_app_pool
  FROM SPECIFICATION '
spec:
  containers:
    - name: server
      image: /MY_APP_PKG/IMG/REPO/my-server:latest
      readinessProbe:
        port: 8081
        path: /health
  endpoints:
    - name: mcp_endpoint
      port: 8080
      public: true
';

GRANT SERVICE ROLE services.my_service!ALL_ENDPOINTS
  TO APPLICATION ROLE my_app_role;
```

For more information about SPCS in a Snowflake Native App, see
[Add services to an app](/developer-guide/native-apps/container-services).

#### Provider: Create the SPCS-hosted MCP server object

After the SPCS service is created, create the SPCS-hosted MCP server object
that points to the service endpoint, and grant `USAGE` to the application
role:

Copy code

```
CREATE CUSTOM MCP SERVER IF NOT EXISTS services.my_mcp_server
  SERVICE = services.my_service
  ENDPOINT = mcp_endpoint
  PATH = '/mcp';

GRANT USAGE ON CUSTOM MCP SERVER services.my_mcp_server
  TO APPLICATION ROLE my_app_role;
```

Verify the MCP server:

Copy code

```
SHOW CUSTOM MCP SERVERS IN APPLICATION my_app;

-- Display the URL of the SPCS-hosted MCP server.
DESC CUSTOM MCP SERVER my_app.services.my_mcp_server;
```

#### Use the SPCS-hosted MCP server from a Cortex Agent

To reference the SPCS-hosted MCP server from a Cortex Agent specification,
include it under `mcp_servers`:

Copy code

```
mcp_servers:
  - server_spec:
      name: "MY_APP.SERVICES.MY_MCP_SERVER"
```

When a Cortex Agent calls an SPCS-hosted MCP server, the role that runs the
agent must have `USAGE` on the `CUSTOM MCP SERVER` object and access to
the SPCS service endpoint that backs the MCP server. For the service endpoint,
grant a service role that provides access to the endpoint.

Snowflake authorizes access in two places:

1. **When resolving the backing ingress URL.** Snowflake checks the invoking
   role’s privileges on the `CUSTOM MCP SERVER` object, and checks that
   both the invoking role and the `CUSTOM MCP SERVER` owner role have
   access to the SPCS service endpoint. This check occurs at the start of
   each `agent:run` request.
2. **When sending the request to the ingress URL.** Snowflake checks that
   the invoking role has access to the SPCS service endpoint. This check
   occurs at each tool discovery call (`tools/list`) and tool invocation
   (`tools/call`).

If the required privileges are revoked before a request starts, the request
can’t use the MCP server. If privileges are revoked after the ingress URL has
already been resolved for an in-progress request, the change applies to
subsequent requests.

External MCP clients can interact with an SPCS-hosted MCP server directly
through the SPCS ingress URL, but OAuth isn’t supported yet for this path.

### Snowflake-managed MCP servers

A Snowflake-managed MCP server (created with
[CREATE MCP SERVER](/sql-reference/sql/create-mcp-server)) wraps Snowflake-native objects as
MCP tools. For general information about Snowflake-managed MCP servers, see
[Snowflake-managed MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp).

#### Restrictions in a Native App

App-created Snowflake-managed MCP servers have stricter rules than standalone
Snowflake-managed MCP servers:

- Tools must reference objects that are owned by the app. The MCP server
  can’t expose tools that the app doesn’t own.
- The `SYSTEM_EXECUTE_SQL` tool isn’t supported.

These restrictions ensure that an installed app’s MCP server can only expose
the app’s own capabilities. The MCP server can’t be used as a way to access
consumer data or run arbitrary SQL in the consumer’s account.

#### Provider: Create the MCP server

The following example creates a Snowflake-managed MCP server in the app that
exposes an app-owned Cortex Search service and an app-owned Cortex Analyst
semantic view as tools:

Copy code

```
CREATE MCP SERVER core.my_mcp
  FROM SPECIFICATION $$
tools:
  - name: "product-search"
    type: "CORTEX_SEARCH_SERVICE_QUERY"
    identifier: "core.my_search_service"
    description: "Cortex Search service for all products"
    title: "Product Search"
  - name: "revenue-semantic-view"
    type: "CORTEX_ANALYST_MESSAGE"
    identifier: "core.my_semantic_view"
    description: "Semantic view for all revenue tables"
    title: "Semantic view for revenue"
$$;

GRANT USAGE ON MCP SERVER core.my_mcp TO APPLICATION ROLE app_public;
```

#### Use the Snowflake-managed MCP server

After the consumer admin grants the application role to a user role, the MCP
server is available the same way as a standalone Snowflake-managed MCP server.
External MCP clients (with OAuth) and Cortex Agents in the consumer account
can use it through the following endpoint:

```
https://<account>/api/v2/databases/{app}/schemas/{schema}/mcp-servers/{name}
```

For more information about the endpoint and how MCP clients connect, see
[Snowflake-managed MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp).

## When to use SPCS-hosted or Snowflake-managed MCP

The following table compares the two kinds of MCP servers in a Snowflake Native App:

| Criteria | SPCS-hosted MCP server | Snowflake-managed MCP server |
| --- | --- | --- |
| Tool implementation | Arbitrary code (any language, any framework) running in Snowpark Container Services. | Snowflake-native objects: UDFs, stored procedures, Cortex Search, Cortex Analyst, Cortex Agents. |
| Compute | Runs on your Snowpark Container Services compute pool. | Runs on a warehouse or Snowflake-managed compute. |
| Use when | You need ML inference, proprietary algorithms, external API calls, stateful services, or custom protocols. | Your tools map cleanly to SQL functions, search services, or semantic views. |
| Consumer access in a Snowflake Native App | Primarily for Cortex Agents. External MCP clients can interact directly with the Snowpark Container Services ingress URL, but OAuth isn’t supported yet. | Both external MCP client usage with OAuth and Cortex Agent usage are supported. |

Expand

Show lessSee more

Start with a Snowflake-managed MCP server if your app’s MCP tools are wrappers
around Snowflake objects that you already have, such as search services,
semantic views, or procedures. This option requires less infrastructure and
simpler deployment. Use an SPCS-hosted MCP server when your tools require
arbitrary compute, an external dependency, or a custom protocol.

## Best practices for providers

When you build agents and MCP servers in a Snowflake Native App, follow these
practices:

- **Scope tools minimally.** Declare only the tools that the agent needs.
  Each tool widens the agent’s access surface.
- **Write tool descriptions carefully.** Agent orchestration uses tool names
  and descriptions to decide when to call tools. Keep descriptions specific,
  accurate, and limited to the tool’s intended use.
- **Validate inputs to custom tools.** If the agent calls stored procedures
  or user-defined functions (UDFs), validate arguments. Prompt injection can
  cause unexpected inputs.
- **Don’t embed secrets in system prompts.** Consumers can inspect the full
  agent specification by using `DESC AGENT`.
- **Use RBAC to protect app objects and intellectual property.** Even if an
  agent is manipulated through prompt injection, restricted caller’s rights
  prevent it from exceeding its granted privileges on Snowflake objects.
  Don’t use prompt instructions, such as “do not reveal internal data,” as
  a security control.
- **Use owner’s rights objects when needed.** Cortex Agents don’t run with
  owner’s rights. If an agent needs access to internal app objects that
  aren’t exposed to consumers, wrap the agent call in an owner’s-rights
  stored procedure or Snowpark Container Services service.
- **Use event logging and event sharing for observability.** For more
  information, see [Logging messages from functions and procedures](/developer-guide/logging-tracing/logging) and
  [Use logging and event tracing for an app](/developer-guide/native-apps/event-about).

For best practices that apply to consumers (auditing, granting caller
privileges, monitoring, and feature policies), see
[Use app-created Cortex Agents and MCP servers](/developer-guide/native-apps/ui-consumer-agents-mcp).

## SQL reference

The following SQL commands are used to manage Cortex Agents and MCP servers in
a Snowflake Native App:

- [CREATE AGENT](/sql-reference/sql/create-agent),
  [ALTER AGENT](/sql-reference/sql/alter-agent),
  [DESCRIBE AGENT](/sql-reference/sql/desc-agent),
  [DROP AGENT](/sql-reference/sql/drop-agent),
  [SHOW AGENTS](/sql-reference/sql/show-agents)
- [CREATE MCP SERVER](/sql-reference/sql/create-mcp-server),
  [DESCRIBE MCP SERVER](/sql-reference/sql/desc-mcp-server),
  [DROP MCP SERVER](/sql-reference/sql/drop-mcp-server),
  [SHOW MCP SERVERS](/sql-reference/sql/show-mcp-servers)
- [GRANT CALLER](/sql-reference/sql/grant-caller),
  [REVOKE CALLER](/sql-reference/sql/revoke-caller),
  [SHOW CALLER GRANTS](/sql-reference/sql/show-caller-grants)
- [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex)
