# MCP Connectors

MCP Connectors allow CoCo in Snowsight to use external tools and data sources through the Model Context Protocol (MCP). When MCP Connectors are configured for your account, CoCo can invoke external services such as Jira, Confluence, GitHub, Google Calendar, and others as part of its agentic workflows.

## How it works

An administrator creates External MCP Server objects at the account level and grants access to appropriate roles. Once configured, users can connect their own accounts to authorized MCP servers and use their tools directly from a CoCo conversation.

MCP tools are executed server-side by Snowflake. OAuth tokens and credentials are stored server-side and never reach the browser client.

## Connecting to MCP Connectors

When MCP Connectors are available for your account:

1. In the CoCo composer, select the **+** menu to see available MCP Connectors.
2. This opens the settings menu to the MCP Connectors page (also accessible through the bottom-left menu) where you can see a list of accessible MCP Connectors.
3. Select a connector to initiate the OAuth connection flow.
4. Once connected, the connector’s tools are available for the current and future conversations.

You can disconnect a connector at any time. Disconnecting removes the connector from subsequent requests and revokes the underlying OAuth authorization.

## Visibility and access control

- **Role-based discovery.** You only see MCP servers that your active role has USAGE privilege on.
- **Per-user OAuth.** Each user must independently authorize their connection to an MCP server. One user’s authorization does not carry over to another.

## User preferences

You can curate which connected MCP servers are included in your conversations. This helps reduce tool-selection noise when many connectors are available. Preferences persist across sessions until you change them.

## Administrator setup

### Using SQL

Administrators configure MCP Connectors using SQL:

1. Create an External MCP Server object.
2. Create an API integration for OAuth.
3. Grant USAGE on the MCP server to appropriate roles.

For detailed setup instructions, see [MCP server documentation](/user-guide/snowflake-cortex/cortex-agents-mcp-connectors).

### Using the UI

Administrators can also configure MCP Connectors using the Snowsight interface:

1. Click the **User** icon in the bottom-left corner of Snowsight.
2. Click **Settings**.
3. Click **MCP Connectors** under **Account**.

From this page, you can enable web search, manage existing MCP connectors, and add custom ones.
