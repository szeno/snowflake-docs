# Configuring tool availability for an MCP server

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP) commercial regions, with the exception of AWS Europe (Spain). For the full list of commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

As an administrator, you control which tools each MCP server exposes to your users’ AI clients. Configuring tool availability lets you limit what AI can do with a given server. For example, you can allow read-only tools while keeping write or delete tools unavailable.

When a user’s AI client connects to an MCP server through Cortex Tools, it only receives the tools you’ve enabled. Tools that aren’t enabled are not visible to the client and can’t be invoked.

Note

If you don’t configure tool availability for an app, all tools are available by default.

## Configure available tools

Currently, only users with the `ACCOUNTADMIN` role can administer MCP servers in Cortex Tools, including configuring tool availability.

1. Sign in to Snowsight.
2. Select **AI & ML** > **AI Gateway** > **MCP & Tools**.
3. In the new tab, select **Access**.
4. Find the policy for the MCP server you want to configure.
5. Select **Edit**.
6. Under **Tools**, select the tools you want to enable:
   - **Specific tools**: only the tools you select are visible to users’ AI clients
   - **All currently published tools**: all tools the server currently exposes are available. Tools the provider adds in the future are not automatically included.
   - **All current and future tools**: all existing tools and any tools the provider adds in the future are automatically available
7. Select **Save**.

## Next step

[Viewing agent activity](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-activity)
