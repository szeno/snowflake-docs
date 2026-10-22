# Distributing access to MCP servers

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in Amazon Web Services (AWS) commercial regions only, excluding Asia Pacific (New Zealand), Asia Pacific (Malaysia), and Europe (Spain). For the full list of AWS commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

As an administrator, you enable MCP servers in Tools and configure which account roles can access them. Users complete any required authorization with the third-party service.

With the required role grants in place, enabling a server makes it discoverable to CoCo Desktop and CLI users.

For a list of all available servers and their authentication requirements, see [Available MCP servers](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers). Some servers require additional setup before you can enable them. See [Setting up MCP servers needing additional configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup).

## Administrator requirement

Currently, only users with the `ACCOUNTADMIN` role can administer MCP servers in Tools. This requirement applies to server configuration, enablement, and access management. It is separate from the role grants that end users need to connect to a server.

## Grant access for automatic client configuration

For automatic configuration in CoCo Desktop and CLI, grant the `SNOWFLAKE$OPS.MCP$USER` database role to each account role that has access to the MCP server. Grant it to the roles your intended users use to access that server, not directly to individual users.

This database-role grant is required in addition to access to the individual MCP server. It doesn’t replace server enablement, server-specific access, or any required third-party authorization. For database-role grant syntax, see [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role).

## Enable an MCP server

1. Sign in to Snowsight.
2. Select **AI & ML** > **AI Gateway** > **MCP & Tools**. Tools opens in a new tab.
3. Find the MCP server you want to make available to your users.
4. Complete any [provider-specific setup](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup).
5. Enable the server.

Users also need access to the server through their account roles. Automatic configuration in CoCo Desktop and CLI requires the database-role grant described above.

## What Desktop and CLI users do next

CoCo Desktop and CLI discover enabled servers automatically when the user’s account role has server access and the [required database-role grant](#label-gateway-tools-client-access-role). Users don’t need to copy an MCP URL or create a configuration entry for those servers, but they still complete any required authorization. In Desktop, users find these servers under **Agent Settings** > **MCP** > **Snowflake Managed**. In CLI, users enter `/mcp` and find them in the **Managed** list.

Users of other MCP clients select **AI & ML** > **AI Gateway** > **MCP & Tools** in Snowsight, then select **MCP Connections** in the new tab for connection details and client instructions. Share [Adding an MCP server to your AI client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/user-configure-client#label-gateway-tools-third-party-clients) with these users.

## Next step

[Setting up MCP servers needing additional configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup)
