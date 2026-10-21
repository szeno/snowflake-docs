# Viewing agent activity

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP) commercial regions, with the exception of AWS Europe (Spain). For the full list of commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

Cortex Tools records tool-call activity in your Snowflake account. Use the `AGENT_TRACE_TABLE` table function to review these traces. For how to query traces and the access requirements, see [Cortex AI Gateway observability](/user-guide/snowflake-cortex/cortex-ai-gateway/observability).

You can also use the Activity catalog to review tool-call activity for AI clients connected through Cortex Tools.

## View activity in Cortex Tools

1. Sign in to Snowsight.
2. Select **AI & ML** > **AI Gateway** > **MCP & Tools**.
3. In the new tab, select **Activity**.

The Activity page has two tabs: **Dashboard** and **Connections**.

## Dashboard tab

The Dashboard tab provides a high-level summary of AI activity in your organization:

- Which apps are installed
- The total number of tool calls made
- Any AI access discovered outside of Cortex Tools

Use this tab for a quick overview of adoption and usage patterns.

## Connections tab

The Connections tab lets you review recorded tool-call activity by app, tool, and call status, such as success or policy violation.

Tool calls that belong to the same prompt are grouped together to help you follow the sequence of actions.

## Next step

[Adding an MCP server to your AI client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/user-configure-client)
