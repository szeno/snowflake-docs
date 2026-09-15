# Nov 04, 2025: Snowflake-managed MCP server (*General availability*)

With this release, we are pleased to announce the general availability of the Snowflake-managed MCP server, which was previously available as a preview feature. The Snowflake-managed MCP server is a standards-based interface that lets AI agents securely retrieve data from Snowflake accounts without needing to deploy separate infrastructure.

Model Context Protocol (MCP) is an open-source standard that lets AI agents securely interact with business applications and external data systems, such as databases and content repositories. The Snowflake-managed MCP server provides:

- **Standardized integration:** Unified interface for tool discovery and invocation, in compliance with the rapidly evolving standards.
- **Comprehensive authentication:** Snowflake’s built-in OAuth service to enable OAuth-based authentication for MCP integrations.
- **Robust governance:** Role-based access control (RBAC) for the MCP server and tools to manage tool discovery and invocation.

You can configure the MCP server to serve Cortex Analyst and Cortex Search as tools on the standards-based interface. MCP clients discover and invoke these tools, and retrieve data required for the application.

For more information, see [Snowflake-managed MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp).
