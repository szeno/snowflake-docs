# Adding an MCP server to your AI client

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP) commercial regions, with the exception of AWS Europe (Spain). For the full list of commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

This page is for end users connecting to servers that their administrator has enabled in Cortex Tools. CoCo Desktop and CoCo CLI discover enabled servers automatically when your account role has the required access and database-role grant. You don’t need to copy a server URL or add a configuration file entry for those servers, but you must authorize your own connection when the server requires user authentication.

Before you begin, confirm that your administrator has enabled the server, completed any provider-specific setup, and granted the `SNOWFLAKE$OPS.MCP$USER` database role to the account role you use to access the server. See [Grant access for automatic client configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections#label-gateway-tools-client-access-role). You also need an account with access to the third-party service when it requires user authorization. See [Available MCP servers](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers).

## CoCo Desktop and CLI

Automatic discovery makes an enabled server available in your client. It doesn’t authorize access to your third-party account or complete a provider’s consent flow on your behalf.

### CoCo Desktop

1. Open **Agent Settings** > **MCP** and find the server under **Snowflake Managed**.
2. Connect to the server you want to use. If prompted, complete the authorization flow with your own account in the third-party service.
3. Check the server’s connection status and available tools in the MCP panel.
4. Ask CoCo to perform a task with that service, such as finding an issue or searching a document.

For client controls and troubleshooting, see [MCP support in CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop/mcp-support). Its manual server configuration instructions are for servers you add yourself, not a prerequisite for automatically discovered Cortex Tools servers.

### CoCo CLI

1. In a CoCo session, enter `/mcp` and find the server in the **Managed** list.
2. Connect to the enabled server you want to use. If prompted, complete the authorization flow with your own account in the third-party service.
3. Return to the session and ask CoCo to perform a task with that service.

For MCP commands, connection management, and troubleshooting, see [MCP support in CoCo CLI](/user-guide/cortex-code/cortex-code-mcp). You don’t need to run `cortex mcp add` for a server that Cortex Tools has already made available to the client.

## Other MCP clients

For any other MCP-compatible client, including Claude Desktop, Claude Code, Cursor, and VS Code, add the server using its connection URL.

### Copy the connection URL

1. Sign in to Snowsight.
2. Select **AI & ML** > **AI Gateway** > **MCP & Tools**. Cortex Tools opens in a new tab.
3. Select **MCP Connections**.
4. Find the server you want to connect to and review its client instructions.
5. Copy the connection URL shown for that server.

### Add the URL to your client

Add the URL you copied using your client’s own process for adding a remote MCP server. Most clients accept either a configuration file entry or a command. For example, a configuration file entry usually takes this shape, where `<connection-url>` is the URL you copied:

Copy code

```
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "<connection-url>"
    }
  }
}
```

For the exact file location, field names, and any client-specific requirements, see your client’s documentation.

If the server uses per-user OAuth, complete the authorization prompt with your own account in the third-party service.

## If a server doesn’t appear

If a server you expect isn’t available in your client, check the following:

- Your administrator has enabled the server for your organization. See [Distributing access to MCP servers](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections).
- Your account role has access to the server and has been granted the `SNOWFLAKE$OPS.MCP$USER` database role. Ask your administrator to check both requirements.
- You’re using the Snowflake account where the administrator enabled the server.
- You completed any required authorization prompt with an account that can access the third-party service. Discovery alone doesn’t complete authorization.
- The tools you expect are enabled for that server. Your administrator can limit which tools a server exposes. See [Configuring tool availability for an MCP server](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-tool-policies).
