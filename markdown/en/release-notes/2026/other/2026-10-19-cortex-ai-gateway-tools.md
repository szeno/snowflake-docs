# Oct 19, 2026: Tools for Cortex AI Gateway (*Preview*)

We are pleased to announce the preview of Tools for Cortex AI Gateway, which connects AI clients
to the business tools your organization already uses through the Model Context Protocol (MCP).
Supported clients include CoCo Desktop, CoCo CLI, Claude, and Cursor.

Currently, only users with the `ACCOUNTADMIN` role can administer MCP servers in Tools.
As an administrator, you control which MCP servers your users can reach, which tools each server
exposes, and review tool-call activity.

With this preview, you can:

- **Enable servers from a curated catalog** of MCP servers for services such as Atlassian, GitHub,
  Google Workspace, Salesforce, Slack, and Snowflake. Complete any provider-specific setup before
  enabling a server. For the full list,
  see [Available MCP servers](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers).
- **Distribute access to end users** by enabling servers that CoCo Desktop and CLI discover
  automatically. For automatic Snowflake client configuration, grant the `SNOWFLAKE$OPS.MCP$USER`
  database role to each account role that has access to the MCP server. Users still complete any
  required authorization with the third-party service. For details, see
  [Distributing access to MCP servers](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections).
- **Limit what AI can do** by configuring which tools a server exposes, for example allowing
  read-only tools while keeping write and delete tools unavailable. For details, see
  [Configuring tool availability for an MCP server](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-tool-policies).
- **Add a custom MCP server** that isn’t in the catalog by providing its URL, which is useful for
  internal tools and your own integrations. For details, see
  [Adding a custom MCP server](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-custom-apps).
- **Review tool-call activity** in your Snowflake account with the `AGENT_TRACE_TABLE` table function, or use the Activity catalog.
  For details, see [Viewing agent activity](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-activity).

To get started, sign in to Snowsight and select **AI & ML** > **AI Gateway** >
**MCP & Tools**.

For more information, see [Tools](/user-guide/snowflake-cortex/cortex-ai-gateway/tools).
