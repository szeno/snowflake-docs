# Adding a custom MCP server

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP) commercial regions, with the exception of AWS Europe (Spain). For the full list of commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

As an administrator, you can connect any MCP server not already in the catalog by providing its URL. This is useful for internal tools, custom integrations, or servers that aren’t yet listed in the Cortex Tools catalog.

## Requirements

Currently, only users with the `ACCOUNTADMIN` role can administer MCP servers in Cortex Tools, including adding custom servers.

The server must:

- Support streamable HTTP transport with an endpoint ending in `/mcp`
- Support OAuth

## Add a custom MCP server

1. Sign in to Snowsight.
2. Select **AI & ML** > **AI Gateway**.
3. Select **MCP & Tools**. Cortex Tools opens in a new tab.
4. Select **Add app** > **Remote URL**.
5. Enter the server URL. The URL must end with `/mcp`.
6. Enter an app name.
7. Select **Save**.

After saving, follow the standard steps to enable the server for your users. See [Distributing access to MCP servers](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections).

## Connection URL and identifier

The default identifier for a custom server is `custom-{appName}`, where `{appName}` is the name you gave the app in lowercase with hyphens replacing spaces. For example, an app named `My Internal Tool` gets the identifier `custom-my-internal-tool`.

After an administrator enables the server and grants the `SNOWFLAKE$OPS.MCP$USER` database role to the account roles that have server access, CoCo Desktop and CLI discover it automatically. Users still complete any required authorization.

For other MCP clients, users select **AI & ML** > **AI Gateway** > **MCP & Tools** in Snowsight, then select **MCP Connections** in the new tab. Find the server to view its connection URL and client instructions.

See [Adding an MCP server to your AI client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/user-configure-client) for instructions on adding this URL to a specific client.

## Next step

[Configuring tool availability for an MCP server](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-tool-policies)
