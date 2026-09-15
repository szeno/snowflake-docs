# Aug 7, 2026: Snowflake Native Apps: Cortex Agents and MCP servers (*General availability*)

Cortex Agents and MCP servers in Snowflake Native Apps are now generally available.

Providers can create the following objects in an app’s setup script:

- A Cortex Agent, so the app offers a conversational experience over its shared data and functionality.
- A Snowflake-managed MCP server, which exposes app-owned objects such as Cortex Search services,
  semantic views, procedures, and UDFs as MCP tools.
- An SPCS-hosted MCP server, which registers an existing Snowpark Container Services endpoint
  as an MCP server.

Apps can also use inter-app communication so that one app’s agent calls another app’s agent or MCP
server. Each app keeps its own data and logic private: agents reach across apps only through the
tools that providers expose and consumers approve.

Consumers control app-created agents and MCP servers with caller grants and feature policies, and
can delegate agent access to specific user roles.

For more information, see the following topics:

- [Use Cortex Agents and MCP servers in an app](/developer-guide/native-apps/agents-mcp-servers)
- [Use inter-app agents and MCP servers](/developer-guide/native-apps/inter-app-agents)
- [Use app-created Cortex Agents and MCP servers](/developer-guide/native-apps/ui-consumer-agents-mcp)
