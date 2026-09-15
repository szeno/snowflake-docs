# Integrate tools and data

In some cases, you may want to integrate other tools and data sources with your agents in Snowflake CoWork. Snowflake CoWork supports the Model Context Protocol (MCP), which is an [open-source standard](https://modelcontextprotocol.io/docs/getting-started/intro) that lets AI agents securely interact with business applications and external data systems, such as databases and content repositories.

The MCP server provides a standards-based interface that allows AI agents to discover and invoke tools, such as Cortex Analyst and Cortex Search, and retrieve the data they need. For more information, see [Snowflake-managed MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp).

With MCP, you can:

- Allow your agent to retrieve data from Snowflake accounts using a Snowflake-managed MCP server without needing to deploy separate infrastructure. You can configure the MCP server to serve Cortex Analyst, Cortex Search, and Cortex Agents as tools, along with custom tools and SQL executions on the standards-based interface.
- Connect to your agents in Snowflake CoWork from external MCP clients.

For information about creating and managing the Snowflake-managed MCP server, see [Snowflake-managed MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp).

## Use the Snowflake-managed MCP server to connect to your agents from external MCP clients

Any agent that you create in Snowflake, or the tools that the agent is connected to, can have a managed endpoint for other systems to connect to your agent with MCP. This provides a seamless integration layer for tools like Claude Desktop, Langgraph, and other tools that integrate with MCP.

When connecting to your agents from an external MCP client, you must use the URL endpoint with the following format:

Copy code

```
https://<account_URL>/api/v2/databases/{database}/schemas/{schema}/mcp-servers/{name}
```

For information about formatting your account URL, see [Account identifiers](/user-guide/admin-account-identifier).

For information about interacting with the MCP server, see [Build an MCP client](https://modelcontextprotocol.io/docs/develop/build-client).
