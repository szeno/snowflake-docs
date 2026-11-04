# Tools

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in Amazon Web Services (AWS) commercial regions only, excluding Asia Pacific (New Zealand) and Middle East (UAE). For the full list of AWS commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

Tools is a capability of Cortex AI Gateway that connects AI clients to the business tools your organization already uses through the Model Context Protocol (MCP). Tools works with any agent that supports MCP, including CoCo (CLI and Desktop), ChatGPT, Claude, Cursor, and more.

Currently, only users with the `ACCOUNTADMIN` role can administer MCP servers in Tools. Administrators enable servers and configure access. End users connect to enabled servers and complete any required authorization with the third-party service.

## Get started

1. **Administrators:** [Choose a server](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers), complete its setup, and [enable it and grant access](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections).
2. **End users:** [Connect from your AI client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/user-configure-client) and complete any required third-party authorization. CoCo Desktop and CLI discover servers automatically after your administrator configures access.

## What you can do

| Task | Who this is for |
| --- | --- |
| [Browse available MCP servers](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers) | Administrator and end user |
| [Distributing access to MCP servers](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections) | Administrator |
| [Setting up MCP servers needing additional configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup) | Administrator |
| [Adding a custom MCP server](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-custom-apps) | Administrator |
| [Configuring tool availability for an MCP server](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-tool-policies) | Administrator |
| [Viewing agent activity](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-activity) | Administrator |
| [Adding an MCP server to your AI client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/user-configure-client) | End user |

Expand

Show lessSee more

## Regional availability

Tools is available in Public Preview to accounts in Amazon Web Services (AWS) commercial regions only, excluding Asia Pacific (New Zealand) and Middle East (UAE). For the full list of AWS commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

## Related MCP features

Tools connects your AI clients outward to third-party business tools. If instead you want to expose data in your Snowflake account to an AI client, see [Snowflake-managed MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp).

## Next step

[Browse available MCP servers](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers)
