# Available MCP servers

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in Amazon Web Services (AWS) commercial regions only, excluding Asia Pacific (New Zealand), Asia Pacific (Malaysia), and Europe (Spain). For the full list of AWS commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

Tools provides the following MCP servers. Select a server in the table for its connection details and any setup it requires.

To add a server that isn’t listed here, see [Adding a custom MCP server](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-custom-apps).

## Connecting to a server

Before you can connect to any of these servers, an administrator must enable it for your organization. Currently, only users with the `ACCOUNTADMIN` role can administer MCP servers in Tools. See [Distributing access to MCP servers](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections).

When a user access to a role that has been granted the `SNOWFLAKE$OPS.MCP$USER` database role, MCP servers they can access are automatically discoverable in CoCo Desktop and CLI. Users must still authorize the servers before they can be used by any agent.

For any other MCP client, select **AI & ML** > **AI Gateway** > **MCP & Tools** in Snowsight. In the new tab, select **MCP Connections** to find the server’s connection URL and client instructions. See [Adding an MCP server to your AI client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/user-configure-client).

## All servers

The below section provides information on MCP servers available via Cortex AI Gateway. Certain **Private Preview** must be enabled for your account - please reach out to your account representative or support if interested.

In some cases, **additional administrator setup** links to instructions to set up permissions, OAuth clients, credentials, or instance-specific configuration for an MCP server. All servers also require enablement and access grants.

All serversPrivate Preview

| Server | Status | Authentication | Additional administrator setup |
| --- | --- | --- | --- |
| [Amplitude](#label-gateway-tools-server-amplitude) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Apiiro](#label-gateway-tools-server-apiiro) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Apollo](#label-gateway-tools-server-apollo) | Private Preview | OAuth | [GraphQL deployment and authorization](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-apollo) |
| [Asana](#label-gateway-tools-server-asana) | Generally available | OAuth | [Workspace access; custom OAuth client if needed](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-asana) |
| [Ashby](#label-gateway-tools-server-ashby) | Private Preview | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Atlassian](#label-gateway-tools-server-atlassian) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Avalara Dev Documentation](#label-gateway-tools-server-avalara-dev-documentation) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Avalara Tax Content](#label-gateway-tools-server-avalara-tax-content) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [AvaTax](#label-gateway-tools-server-avatax) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Azure DevOps](#label-gateway-tools-server-azure-devops) | Private Preview | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [BigQuery](#label-gateway-tools-server-bigquery) | Generally available | OAuth | [API and MCP enablement; IAM roles; OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-bigquery) |
| [Box](#label-gateway-tools-server-box) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Buildkite](#label-gateway-tools-server-buildkite) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Canva](#label-gateway-tools-server-canva) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [ClickUp](#label-gateway-tools-server-clickup) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Cloudflare Audit Logs](#label-gateway-tools-server-cloudflare-audit-logs) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Cloudflare Workers Observability](#label-gateway-tools-server-cloudflare-workers-observability) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [CloudZero](#label-gateway-tools-server-cloudzero) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Context7](#label-gateway-tools-server-context7) | Generally available | None | [No provider credentials](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections) |
| [Context7 (Authenticated)](#label-gateway-tools-server-context7-oauth) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Datadog](#label-gateway-tools-server-datadog) | Generally available | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [dbt Labs](#label-gateway-tools-server-dbt-labs) | Generally available | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [Draw.io](#label-gateway-tools-server-drawio) | Generally available | None | [No provider credentials](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections) |
| [Fireflies.ai](#label-gateway-tools-server-fireflies) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [GitHub](#label-gateway-tools-server-github) | Generally available | OAuth | [Repository access; custom OAuth client if needed](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-github) |
| [GitLab](#label-gateway-tools-server-gitlab) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Gmail (Cortex)](#label-gateway-tools-server-n-google-gmail) | Generally available | OAuth | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |
| [Gong](#label-gateway-tools-server-gong) | Private Preview | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Google Calendar (Cortex)](#label-gateway-tools-server-n-google-calendar) | Generally available | OAuth | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |
| [Google Chat](#label-gateway-tools-server-google-chat) | Generally available | OAuth | [Google API, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |
| [Google Docs (Cortex)](#label-gateway-tools-server-n-google-docs) | Generally available | OAuth | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |
| [Google Drive (Cortex)](#label-gateway-tools-server-n-google-drive) | Generally available | OAuth | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |
| [Google Forms (Cortex)](#label-gateway-tools-server-n-google-forms) | Generally available | OAuth | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |
| [Google People](#label-gateway-tools-server-google-people) | Generally available | OAuth | [Google API, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |
| [Google Sheets (Cortex)](#label-gateway-tools-server-n-google-sheets) | Generally available | OAuth | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |
| [Google Slides (Cortex)](#label-gateway-tools-server-n-google-slides) | Generally available | OAuth | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |
| [Google Tasks (Cortex)](#label-gateway-tools-server-n-google-tasks) | Generally available | OAuth | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |
| [Honeycomb](#label-gateway-tools-server-honeycomb) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [incident.io](#label-gateway-tools-server-incidentio) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Intercom](#label-gateway-tools-server-intercom) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [LaunchDarkly](#label-gateway-tools-server-launchdarkly) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Linear](#label-gateway-tools-server-linear) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Linx](#label-gateway-tools-server-linx) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Lucid](#label-gateway-tools-server-lucid) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Meta Ads](#label-gateway-tools-server-meta-ads) | Private Preview | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Microsoft OneDrive](#label-gateway-tools-server-microsoft-onedrive) | Private Preview | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [Microsoft Outlook](#label-gateway-tools-server-microsoft-outlook) | Private Preview | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [Microsoft SharePoint](#label-gateway-tools-server-microsoft-sharepoint) | Private Preview | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [Microsoft Teams](#label-gateway-tools-server-microsoft-teams) | Private Preview | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [Mixpanel](#label-gateway-tools-server-mixpanel) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Monday.com](#label-gateway-tools-server-monday) | Private Preview | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Neon](#label-gateway-tools-server-neon) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [New Relic](#label-gateway-tools-server-new-relic) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Notion](#label-gateway-tools-server-notion) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Okta (Cortex)](#label-gateway-tools-server-n-okta) | Generally available | OAuth | [Organization domain; app integration and scopes](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-okta) |
| [Outreach](#label-gateway-tools-server-outreach) | Private Preview | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [PagerDuty](#label-gateway-tools-server-pagerduty) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [PayPal](#label-gateway-tools-server-paypal) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Prisma](#label-gateway-tools-server-prisma) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Salesforce](#label-gateway-tools-server-salesforce) | Generally available | OAuth | [External Client App and MCP scopes](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-salesforce) |
| [Semgrep](#label-gateway-tools-server-semgrep) | Generally available | None | [No provider credentials](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections) |
| [Sentry](#label-gateway-tools-server-sentry) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Sigma](#label-gateway-tools-server-sigma) | Private Preview | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [Slack](#label-gateway-tools-server-slack) | Generally available | OAuth | [MCP-enabled application and scopes](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-slack) |
| [Snowflake](#label-gateway-tools-server-snowflake) | Generally available | OAuth | [MCP server object, privileges, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-snowflake-server) |
| [Spinach](#label-gateway-tools-server-spinach) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Statsig](#label-gateway-tools-server-statsig) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Stripe](#label-gateway-tools-server-stripe) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Torii](#label-gateway-tools-server-torii) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Upwind](#label-gateway-tools-server-upwind) | Generally available | Client credentials | [API credentials, organization, and region](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-upwind) |
| [Webflow](#label-gateway-tools-server-webflow) | Generally available | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Wiz](#label-gateway-tools-server-wiz) | Generally available | Client credentials | [Service account, scopes, and API endpoint](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-wiz) |
| [Wrike](#label-gateway-tools-server-wrike) | Generally available | OAuth | [Custom OAuth client if needed; user consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-wrike) |
| [Zoom](#label-gateway-tools-server-zoom) | Generally available | OAuth | [General App and matching scopes](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-zoom) |
| [ZoomInfo](#label-gateway-tools-server-zoominfo) | Private Preview | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

| Server | Status | Authentication | Additional administrator setup |
| --- | --- | --- | --- |
| [Apollo](#label-gateway-tools-server-apollo) | Private Preview | OAuth | [GraphQL deployment and authorization](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-apollo) |
| [Ashby](#label-gateway-tools-server-ashby) | Private Preview | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Azure DevOps](#label-gateway-tools-server-azure-devops) | Private Preview | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [Gong](#label-gateway-tools-server-gong) | Private Preview | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Meta Ads](#label-gateway-tools-server-meta-ads) | Private Preview | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Microsoft OneDrive](#label-gateway-tools-server-microsoft-onedrive) | Private Preview | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [Microsoft Outlook](#label-gateway-tools-server-microsoft-outlook) | Private Preview | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [Microsoft SharePoint](#label-gateway-tools-server-microsoft-sharepoint) | Private Preview | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [Microsoft Teams](#label-gateway-tools-server-microsoft-teams) | Private Preview | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [Monday.com](#label-gateway-tools-server-monday) | Private Preview | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Outreach](#label-gateway-tools-server-outreach) | Private Preview | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |
| [Sigma](#label-gateway-tools-server-sigma) | Private Preview | OAuth | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |
| [ZoomInfo](#label-gateway-tools-server-zoominfo) | Private Preview | OAuth | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

## Amplitude

Query and create Amplitude analytics content — charts, dashboards, experiments, cohorts, and more — using natural language via the Model Context Protocol.

| Property | Value |
| --- | --- |
| Server identifier | `amplitude` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Amplitude resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Apiiro

Apiiro Guardian Agent — Application Security Posture Management (ASPM) for AI coding assistants. Write secure code, query security risks, trigger diff scans, and manage findings.

| Property | Value |
| --- | --- |
| Server identifier | `apiiro` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Apiiro resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Apollo

Note

This server is in Private Preview. Its available tools and behavior might change.

Apollo GraphQL MCP Server makes GraphQL API operations available as tools for AI clients. The available operations depend on the schema and tools configured for your graph.

| Property | Value |
| --- | --- |
| Server identifier | `apollo` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [GraphQL deployment and authorization](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-apollo) |

Expand

Show lessSee more

### Setup and authorization

Review the [Apollo GraphQL setup guidance](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-apollo) with the administrator of your graph before connecting. Don’t use Apollo.io sales-platform registration instructions for this server.

For more information, see [Apollo GraphQL deployment and authorization](https://www.apollographql.com/docs/apollo-mcp-server). For connection steps specific to Tools, use the workflow above.

## Asana

Work with Asana tasks, projects, workspaces, and comments from your AI client. Use it to find work, update tasks, and review project context.

| Property | Value |
| --- | --- |
| Server identifier | `asana` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Workspace access; custom OAuth client if needed](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-asana) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Asana resources you want the AI client to use. Review [workspace access; custom oauth client if needed](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-asana) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

For more information, see [Asana MCP setup](https://developers.asana.com/docs/integrating-with-asanas-mcp-server). For connection steps specific to Tools, use the workflow above.

## Ashby

Note

This server is in Private Preview. Its available tools and behavior might change.

Official Ashby MCP server. Query your recruiting pipeline, prepare for interviews, and take actions in Ashby — all via OAuth, no API key required.

| Property | Value |
| --- | --- |
| Server identifier | `ashby` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Ashby resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Atlassian

Connect Jira issues and Confluence documentation to your AI client. Search enterprise knowledge, summarize work, and create issues or pages.

| Property | Value |
| --- | --- |
| Server identifier | `atlassian` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Atlassian resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

For more information, see [Atlassian connector capabilities](https://docs.natoma.ai/apps/atlassian-remote). For connection steps specific to Tools, use the workflow above.

## Avalara Dev Documentation

Avalara’s official remote MCP server for searching and navigating Avalara’s developer documentation. Read-only — surfaces API reference, guides, and code samples to AI assistants.

| Property | Value |
| --- | --- |
| Server identifier | `avalara-dev-documentation` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Avalara Dev Documentation resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Avalara Tax Content

Avalara’s official remote MCP server for Tax Content — query Avalara’s tax rate, rule, and product taxability content directly from your AI assistant.

| Property | Value |
| --- | --- |
| Server identifier | `avalara-tax-content` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Avalara Tax Content resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## AvaTax

Avalara’s official remote MCP server for AvaTax — query tax calculation, transactions, and reporting data across your Avalara account.

| Property | Value |
| --- | --- |
| Server identifier | `avatax` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the AvaTax resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Azure DevOps

Note

This server is in Private Preview. Its available tools and behavior might change.

Official Azure DevOps remote MCP server hosted by Microsoft. Access work items, pull requests, pipelines, repos, wikis, and test plans via Microsoft Entra OAuth — no local installation required.

| Property | Value |
| --- | --- |
| Server identifier | `azure-devops` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |

Expand

Show lessSee more

An administrator provides the following values before this server can be enabled:

| Value | Description | Default |
| --- | --- | --- |
| `adoOrg` | Azure DevOps organization name (for example, “contoso” for dev.azure.com/contoso) | None |

Expand

Show lessSee more

For the full setup procedure, see [Setting up MCP servers needing additional configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup).

### Setup and authorization

Use an account with access to the Azure DevOps resources you want the AI client to use. Review [instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## BigQuery

Explore BigQuery datasets and table schemas and run SQL queries through Google’s hosted MCP server. Access to the underlying data depends on Google Cloud IAM permissions.

| Property | Value |
| --- | --- |
| Server identifier | `bigquery` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [API and MCP enablement; IAM roles; OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-bigquery) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the BigQuery resources you want the AI client to use. Review [api and mcp enablement; iam roles; oauth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-bigquery) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Box

Access files, folders, and collaboration features in Box from your AI client. Use it to work with content in the Box account you authorize.

| Property | Value |
| --- | --- |
| Server identifier | `box` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Box resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

For more information, see [Box connector capabilities](https://docs.natoma.ai/apps/box). For connection steps specific to Tools, use the workflow above.

## Buildkite

Buildkite MCP Server - Connect to your CI/CD pipelines, builds, and jobs

| Property | Value |
| --- | --- |
| Server identifier | `buildkite` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Buildkite resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Canva

Official Canva remote MCP server. Search designs, create and export content, manage brand templates, upload assets, and collaborate with comments.

| Property | Value |
| --- | --- |
| Server identifier | `canva` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Canva resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## ClickUp

ClickUp MCP Server for task management and project collaboration

| Property | Value |
| --- | --- |
| Server identifier | `clickup` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the ClickUp resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Cloudflare Audit Logs

Access Cloudflare account audit logs from your AI client to investigate recorded account activity.

| Property | Value |
| --- | --- |
| Server identifier | `cloudflare-audit-logs` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Cloudflare Audit Logs resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Cloudflare Workers Observability

Access observability information for Cloudflare Workers from your AI client to investigate your applications.

| Property | Value |
| --- | --- |
| Server identifier | `cloudflare-workers-observability` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Cloudflare Workers Observability resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## CloudZero

Query cloud cost data, get optimization recommendations, and access telemetry metrics from CloudZero using the Model Context Protocol.

| Property | Value |
| --- | --- |
| Server identifier | `cloudzero` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the CloudZero resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Context7

Retrieve current library documentation and code examples for coding tasks. This server doesn’t require a user sign-in.

| Property | Value |
| --- | --- |
| Server identifier | `context7` |
| Authentication | None |
| Additional administrator setup | [No provider credentials](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections) |

Expand

Show lessSee more

### Setup and authorization

No provider credentials are required. An administrator must still enable this server and grant access before users can discover it in CoCo.

## Context7 (Authenticated)

Retrieve current library documentation and code examples through an authenticated Context7 connection.

| Property | Value |
| --- | --- |
| Server identifier | `context7-oauth` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Context7 (Authenticated) resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Datadog

Official Datadog remote MCP server. Query and retrieve observability insights — logs, metrics, traces, monitors, dashboards, incidents, and more — directly from AI-powered clients via OAuth.

| Property | Value |
| --- | --- |
| Server identifier | `datadog` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |

Expand

Show lessSee more

An administrator provides the following values before this server can be enabled:

| Value | Description | Default |
| --- | --- | --- |
| `host` | Datadog MCP host: must start with “mcp.” (for example, mcp.us3.datadoghq.com if you sign in at us3.datadoghq.com) | None |

Expand

Show lessSee more

For the full setup procedure, see [Setting up MCP servers needing additional configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup).

### Setup and authorization

Use an account with access to the Datadog resources you want the AI client to use. Review [instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## dbt Labs

Query metrics, explore metadata, view lineage, and run semantic-layer queries against your dbt Cloud project via the remote dbt MCP server.

| Property | Value |
| --- | --- |
| Server identifier | `dbt-labs` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |

Expand

Show lessSee more

An administrator provides the following values before this server can be enabled:

| Value | Description | Default |
| --- | --- | --- |
| `dbtHostUrl` | dbt Cloud host (for example, cloud.getdbt.com, or ACCOUNT\_PREFIX.us1.dbt.com for multi-cell accounts). Find it in Account settings > Access URLs > MCP Endpoint URL. | None |

Expand

Show lessSee more

For the full setup procedure, see [Setting up MCP servers needing additional configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup).

### Setup and authorization

Use an account with access to the dbt Labs resources you want the AI client to use. Review [instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Draw.io

Draw.io MCP App Server - create and render diagrams inline in chat. Renders draw.io XML as interactive diagrams with zoom, pan, layers, and an “Open in draw.io” button for editing.

| Property | Value |
| --- | --- |
| Server identifier | `drawio` |
| Authentication | None |
| Additional administrator setup | [No provider credentials](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections) |

Expand

Show lessSee more

### Setup and authorization

No provider credentials are required. An administrator must still enable this server and grant access before users can discover it in CoCo.

## Fireflies.ai

Search meeting recordings, transcripts, and AI-generated notes in Fireflies.ai. Use meeting context to find decisions and follow-up work.

| Property | Value |
| --- | --- |
| Server identifier | `fireflies` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Fireflies.ai resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

For more information, see [Fireflies.ai connector capabilities](https://docs.natoma.ai/apps/fireflies). For connection steps specific to Tools, use the workflow above.

## GitHub

Work with GitHub repositories, issues, and pull requests through the remote GitHub MCP server. Use it to retrieve development context and perform repository collaboration tasks.

| Property | Value |
| --- | --- |
| Server identifier | `github` |
| Authentication | OAuth |
| Additional administrator setup | [Repository access; custom OAuth client if needed](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-github) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the GitHub resources you want the AI client to use. Review [repository access; custom oauth client if needed](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-github) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## GitLab

Connect your AI client to GitLab through its OAuth-enabled MCP server. Review the tools available for your authorized account before using it for development work.

| Property | Value |
| --- | --- |
| Server identifier | `gitlab` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the GitLab resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Gmail (Cortex)

Gmail MCP Server for searching, reading, sending, and managing email messages, threads, and labels

| Property | Value |
| --- | --- |
| Server identifier | `n-google-gmail` |
| Authentication | OAuth |
| Additional administrator setup | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Gmail (Cortex) resources you want the AI client to use. Review [google apis, scopes, and oauth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Gong

Note

This server is in Private Preview. Its available tools and behavior might change.

Official Gong remote MCP Server with OAuth. Access call recordings, transcripts, and conversation intelligence directly from your AI assistant.

| Property | Value |
| --- | --- |
| Server identifier | `gong` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Gong resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Google Calendar (Cortex)

Google Calendar MCP Server for listing calendars, managing events, and finding free time slots

| Property | Value |
| --- | --- |
| Server identifier | `n-google-calendar` |
| Authentication | OAuth |
| Additional administrator setup | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Google Calendar (Cortex) resources you want the AI client to use. Review [google apis, scopes, and oauth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Google Chat

Official Google-hosted Chat MCP Server for searching conversations and listing messages

| Property | Value |
| --- | --- |
| Server identifier | `google-chat` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Google API, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Google Chat resources you want the AI client to use. Review [google api, scopes, and oauth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Google Docs (Cortex)

Google Docs MCP Server for searching, reading, creating, and editing documents

| Property | Value |
| --- | --- |
| Server identifier | `n-google-docs` |
| Authentication | OAuth |
| Additional administrator setup | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Google Docs (Cortex) resources you want the AI client to use. Review [google apis, scopes, and oauth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Google Drive (Cortex)

Google Drive MCP Server for searching, reading, creating, and managing files and permissions

| Property | Value |
| --- | --- |
| Server identifier | `n-google-drive` |
| Authentication | OAuth |
| Additional administrator setup | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Google Drive (Cortex) resources you want the AI client to use. Review [google apis, scopes, and oauth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Google Forms (Cortex)

Google Forms MCP Server for creating forms, managing questions, and retrieving responses

| Property | Value |
| --- | --- |
| Server identifier | `n-google-forms` |
| Authentication | OAuth |
| Additional administrator setup | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Google Forms (Cortex) resources you want the AI client to use. Review [google apis, scopes, and oauth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Google People

Official Google-hosted People API MCP Server for accessing user profiles, contacts, and directory people

| Property | Value |
| --- | --- |
| Server identifier | `google-people` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Google API, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Google People resources you want the AI client to use. Review [google api, scopes, and oauth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Google Sheets (Cortex)

Google Sheets MCP Server for reading, writing, and managing spreadsheets

| Property | Value |
| --- | --- |
| Server identifier | `n-google-sheets` |
| Authentication | OAuth |
| Additional administrator setup | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Google Sheets (Cortex) resources you want the AI client to use. Review [google apis, scopes, and oauth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Google Slides (Cortex)

Google Slides MCP Server for creating and editing presentations

| Property | Value |
| --- | --- |
| Server identifier | `n-google-slides` |
| Authentication | OAuth |
| Additional administrator setup | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Google Slides (Cortex) resources you want the AI client to use. Review [google apis, scopes, and oauth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Google Tasks (Cortex)

Google Tasks MCP Server for reading and managing task lists and tasks

| Property | Value |
| --- | --- |
| Server identifier | `n-google-tasks` |
| Authentication | OAuth |
| Additional administrator setup | [Google APIs, scopes, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Google Tasks (Cortex) resources you want the AI client to use. Review [google apis, scopes, and oauth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-google) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Honeycomb

Honeycomb MCP Server - Query, analyze, and visualize observability data including traces, triggers, and SLOs using natural language.

| Property | Value |
| --- | --- |
| Server identifier | `honeycomb` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Honeycomb resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## incident.io

incident.io MCP Server for comprehensive incident management, alerts, workflows, and more

| Property | Value |
| --- | --- |
| Server identifier | `incidentio` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the incident.io resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Intercom

Manage customer conversations, access support tickets, retrieve customer profiles, analyze conversation patterns, and handle customer service workflows through Intercom’s messaging platform.

| Property | Value |
| --- | --- |
| Server identifier | `intercom` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Intercom resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## LaunchDarkly

Official LaunchDarkly hosted MCP server for managing feature flags, AgentControl configs, and observability. Uses OAuth — no API key required.

| Property | Value |
| --- | --- |
| Server identifier | `launchdarkly` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the LaunchDarkly resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Linear

Create, update, and query Linear issues and projects from your AI client. Use it to retrieve project context and maintain work items.

| Property | Value |
| --- | --- |
| Server identifier | `linear` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Linear resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

For more information, see [Linear connector capabilities](https://docs.natoma.ai/apps/linear). For connection steps specific to Tools, use the workflow above.

## Linx

Connect to Linx Security for identity governance context across identities, access, and permissions. Review the server’s available tools for the identity workflows you want to use.

| Property | Value |
| --- | --- |
| Server identifier | `linx` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Linx resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

For more information, see [Linx Security connector capabilities](https://docs.natoma.ai/apps/linx). For connection steps specific to Tools, use the workflow above.

## Lucid

Official Lucid remote MCP server. Search Lucidchart diagrams and Lucidspark boards, summarize documents, create shareable links, and generate diagrams from datasets or descriptions.

| Property | Value |
| --- | --- |
| Server identifier | `lucid` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Lucid resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Meta Ads

Note

This server is in Private Preview. Its available tools and behavior might change.

Meta Ads MCP server for managing Facebook and Instagram advertising campaigns, ad sets, and performance data.

| Property | Value |
| --- | --- |
| Server identifier | `meta-ads` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Meta Ads resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Microsoft OneDrive

Note

This server is in Private Preview. Its available tools and behavior might change.

Official Microsoft Work IQ OneDrive MCP server. Manage files and folders in the user’s personal OneDrive via the Microsoft Graph API.

| Property | Value |
| --- | --- |
| Server identifier | `microsoft-onedrive` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |

Expand

Show lessSee more

An administrator provides the following values before this server can be enabled:

| Value | Description | Default |
| --- | --- | --- |
| `tenantId` | Microsoft Entra tenant ID (Directory ID) for your organization (for example, xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx) | None |

Expand

Show lessSee more

For the full setup procedure, see [Setting up MCP servers needing additional configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup).

### Setup and authorization

Use an account with access to the Microsoft OneDrive resources you want the AI client to use. Review [instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Microsoft Outlook

Note

This server is in Private Preview. Its available tools and behavior might change.

Official Microsoft Work IQ Mail MCP server. Create, send, reply to, and manage Outlook email messages via the Microsoft Graph API.

| Property | Value |
| --- | --- |
| Server identifier | `microsoft-outlook` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |

Expand

Show lessSee more

An administrator provides the following values before this server can be enabled:

| Value | Description | Default |
| --- | --- | --- |
| `tenantId` | Microsoft Entra tenant ID (Directory ID) for your organization (for example, xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx) | None |

Expand

Show lessSee more

For the full setup procedure, see [Setting up MCP servers needing additional configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup).

### Setup and authorization

Use an account with access to the Microsoft Outlook resources you want the AI client to use. Review [instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Microsoft SharePoint

Note

This server is in Private Preview. Its available tools and behavior might change.

Official Microsoft Work IQ SharePoint MCP server. Manage SharePoint sites, lists, document libraries, files, and folders across your Microsoft tenant via the Microsoft Graph API.

| Property | Value |
| --- | --- |
| Server identifier | `microsoft-sharepoint` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |

Expand

Show lessSee more

An administrator provides the following values before this server can be enabled:

| Value | Description | Default |
| --- | --- | --- |
| `tenantId` | Microsoft Entra tenant ID (Directory ID) for your organization (for example, xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx) | None |

Expand

Show lessSee more

For the full setup procedure, see [Setting up MCP servers needing additional configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup).

### Setup and authorization

Use an account with access to the Microsoft SharePoint resources you want the AI client to use. Review [instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Microsoft Teams

Note

This server is in Private Preview. Its available tools and behavior might change.

Official Microsoft Work IQ Teams MCP server. Manage chats, channels, messages, and members across your Microsoft Teams tenant via the Microsoft Graph API.

| Property | Value |
| --- | --- |
| Server identifier | `microsoft-teams` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |

Expand

Show lessSee more

An administrator provides the following values before this server can be enabled:

| Value | Description | Default |
| --- | --- | --- |
| `tenantId` | Microsoft Entra tenant ID (Directory ID) for your organization (for example, xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx) | None |

Expand

Show lessSee more

For the full setup procedure, see [Setting up MCP servers needing additional configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup).

### Setup and authorization

Use an account with access to the Microsoft Teams resources you want the AI client to use. Review [instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Mixpanel

Mixpanel MCP Server - Analyze product and replay data using conversational AI. Query events, session replays, funnels, and user behavior through natural language.

| Property | Value |
| --- | --- |
| Server identifier | `mixpanel` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Mixpanel resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Monday.com

Note

This server is in Private Preview. Its available tools and behavior might change.

Manage Monday.com boards, items, and workflows from your AI client through the platform MCP server. Authorize with the account whose work you want to access.

| Property | Value |
| --- | --- |
| Server identifier | `monday` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Monday.com resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

For more information, see [Monday.com MCP servers](https://developer.monday.com/apps/docs/mcp-servers). For connection steps specific to Tools, use the workflow above.

## Neon

MCP server for interacting with Neon Management API and databases.

| Property | Value |
| --- | --- |
| Server identifier | `neon` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Neon resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## New Relic

New Relic MCP Server - Access and analyze your observability data including entities, NRQL queries, alerts, and performance analytics using natural language.

| Property | Value |
| --- | --- |
| Server identifier | `new-relic` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the New Relic resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Notion

Read, create, and update content in Notion pages, databases, and blocks. Use it to retrieve workspace knowledge and maintain documents.

| Property | Value |
| --- | --- |
| Server identifier | `notion` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Notion resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

For more information, see [Notion connector capabilities](https://docs.natoma.ai/apps/notion). For connection steps specific to Tools, use the workflow above.

## Okta (Cortex)

Okta MCP Server — manage users, groups, applications, policies, and system logs via user-consent OAuth

| Property | Value |
| --- | --- |
| Server identifier | `n-okta` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Organization domain; app integration and scopes](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-okta) |

Expand

Show lessSee more

An administrator provides the following values before this server can be enabled:

| Value | Description | Default |
| --- | --- | --- |
| `oktaDomain` | Okta organization domain (for example, your-org.okta.com, your-org.okta-emea.com, your-org.oktapreview.com) | None |

Expand

Show lessSee more

For the full setup procedure, see [Setting up MCP servers needing additional configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup).

### Setup and authorization

Use an account with access to the Okta (Cortex) resources you want the AI client to use. Review [organization domain; app integration and scopes](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-okta) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Outreach

Note

This server is in Private Preview. Its available tools and behavior might change.

Official Outreach remote MCP server. Manage prospects, accounts, opportunities, sequences, tasks, meetings, and deal intelligence via the Outreach Sales Execution Platform.

| Property | Value |
| --- | --- |
| Server identifier | `outreach` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Outreach resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## PagerDuty

Official PagerDuty remote MCP server. Manage incidents, services, teams, schedules, escalation policies, on-call rotations, and alert grouping for incident response automation.

| Property | Value |
| --- | --- |
| Server identifier | `pagerduty` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the PagerDuty resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## PayPal

Interact with PayPal’s payment ecosystem to process transactions, manage subscriptions, handle disputes, access customer payment data, generate financial reports, and monitor payment flows.

| Property | Value |
| --- | --- |
| Server identifier | `paypal` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the PayPal resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Prisma

Connect your AI client to Prisma’s remote MCP server for database development workflows. Review the tools available to your authorized Prisma account before enabling database operations.

| Property | Value |
| --- | --- |
| Server identifier | `prisma` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Prisma resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Salesforce

Connect AI clients to Salesforce-hosted MCP tools using OAuth. The tools and records you can access depend on the Salesforce server and the authorizing user’s permissions.

| Property | Value |
| --- | --- |
| Server identifier | `salesforce` |
| Authentication | OAuth |
| Additional administrator setup | [External Client App and MCP scopes](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-salesforce) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Salesforce resources you want the AI client to use. Review [external client app and mcp scopes](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-salesforce) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Semgrep

Semgrep MCP Server - AI-powered code security scanning and vulnerability detection

| Property | Value |
| --- | --- |
| Server identifier | `semgrep` |
| Authentication | None |
| Additional administrator setup | [No provider credentials](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections) |

Expand

Show lessSee more

### Setup and authorization

No provider credentials are required. An administrator must still enable this server and grant access before users can discover it in CoCo.

## Sentry

Retrieve and analyze issues and errors from your Sentry.io projects. Create and retrieve projects, query issue details, trigger Seer issue fix runs and query their status. Get application debugging context quickly and improve application reliability.

| Property | Value |
| --- | --- |
| Server identifier | `sentry` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Sentry resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Sigma

Note

This server is in Private Preview. Its available tools and behavior might change.

Official Sigma Computing MCP server. Search, explore, and query data in your Sigma organization — locate data sources, describe workbooks and data models, and run analysis using natural language.

| Property | Value |
| --- | --- |
| Server identifier | `sigma` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) |

Expand

Show lessSee more

An administrator provides the following values before this server can be enabled:

| Value | Description | Default |
| --- | --- | --- |
| `sigmaMcpUrl` | Your Sigma MCP URL (found in Sigma > Profile > MCP > Sigma MCP). Format: https://<cloud>-api.sigmacomputing.com/mcp | None |

Expand

Show lessSee more

For the full setup procedure, see [Setting up MCP servers needing additional configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup).

### Setup and authorization

Use an account with access to the Sigma resources you want the AI client to use. Review [instance values; provider access requirements](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-setup-values) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Slack

Search Slack conversations and work with messages from your AI client. Authorize access to the workspace you intend to use and review the tools before enabling actions that post or modify content.

| Property | Value |
| --- | --- |
| Server identifier | `slack` |
| Authentication | OAuth |
| Additional administrator setup | [MCP-enabled application and scopes](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-slack) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Slack resources you want the AI client to use. Review [mcp-enabled application and scopes](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-slack) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Snowflake

Connect to an MCP server object in your Snowflake account. Expose configured Cortex Search services, Cortex Analyst semantic views, SQL execution, and supported custom tools to AI clients through a Snowflake-hosted endpoint.

| Property | Value |
| --- | --- |
| Server identifier | `snowflake` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [MCP server object, privileges, and OAuth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-snowflake-server) |

Expand

Show lessSee more

An administrator provides the following values before this server can be enabled:

| Value | Description | Default |
| --- | --- | --- |
| `host` | Snowflake account URL (for example, myorg-myaccount.snowflakecomputing.com) | None |
| `database` | Snowflake database name (for example, my\_database) | None |
| `schema` | Snowflake schema name (for example, my\_schema) | None |
| `name` | Name of the Snowflake MCP server (for example, my\_mcp\_server) | None |

Expand

Show lessSee more

For the full setup procedure, see [Setting up MCP servers needing additional configuration](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup).

### Setup and authorization

Use an account with access to the Snowflake resources you want the AI client to use. Review [mcp server object, privileges, and oauth client](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-snowflake-server) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Spinach

Query insights and transcripts from your recent Spinach meetings via OAuth.

| Property | Value |
| --- | --- |
| Server identifier | `spinach` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Spinach resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Statsig

Statsig MCP Server - Access feature flags (gates), A/B experiments, dynamic configs, metrics, segments, and audit logs. Manage your Statsig project from AI tools like Cursor and Claude.

| Property | Value |
| --- | --- |
| Server identifier | `statsig` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Statsig resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Stripe

Access Stripe payment data, customers, subscriptions, and transaction history from your AI client. Use it for payment operations and reporting workflows.

| Property | Value |
| --- | --- |
| Server identifier | `stripe` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Stripe resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

For more information, see [Stripe connector capabilities](https://docs.natoma.ai/apps/stripe). For connection steps specific to Tools, use the workflow above.

## Torii

Query SaaS applications, contracts, and spend data in Torii. The server also supports actions such as updating users, creating contracts, and running workflows, subject to your Torii permissions.

| Property | Value |
| --- | --- |
| Server identifier | `torii` |
| Authentication | OAuth |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Torii resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

For more information, see [Torii MCP capabilities and permissions](https://developers.toriihq.com/docs/connect-claude-to-torii). For connection steps specific to Tools, use the workflow above.

## Upwind

Upwind’s official remote MCP server for runtime cloud security — query findings, investigate incidents, and surface asset context across your cloud workloads.

| Property | Value |
| --- | --- |
| Server identifier | `upwind` |
| Authentication | Client credentials |
| Additional administrator setup | [API credentials, organization, and region](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-upwind) |

Expand

Show lessSee more

### Setup and authorization

An administrator supplies scoped service credentials. Follow [Upwind setup](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-upwind); this flow doesn’t use a callback URL or per-user consent.

## Webflow

Interact with Webflow to manage your websites and more.

| Property | Value |
| --- | --- |
| Server identifier | `webflow` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Webflow resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Wiz

Wiz cloud security platform MCP Server with comprehensive security, compliance, and cost optimization tools

| Property | Value |
| --- | --- |
| Server identifier | `wiz` |
| Authentication | Client credentials |
| Additional administrator setup | [Service account, scopes, and API endpoint](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-wiz) |

Expand

Show lessSee more

### Setup and authorization

An administrator supplies scoped service credentials. Follow [Wiz setup](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-wiz); this flow doesn’t use a callback URL or per-user consent.

## Wrike

Create and update tasks and projects, manage folders and spaces, and retrieve work-management context in Wrike. Users authorize access with their own Wrike accounts.

| Property | Value |
| --- | --- |
| Server identifier | `wrike` |
| Authentication | OAuth |
| Additional administrator setup | [Custom OAuth client if needed; user consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-wrike) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Wrike resources you want the AI client to use. Review [custom oauth client if needed; user consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-wrike) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Zoom

Official Zoom remote MCP server. Search meetings, access recordings and transcripts, manage Zoom Docs, and search across chat and docs.

| Property | Value |
| --- | --- |
| Server identifier | `zoom` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [General App and matching scopes](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-zoom) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the Zoom resources you want the AI client to use. Review [general app and matching scopes](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-oauth-zoom) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## ZoomInfo

Note

This server is in Private Preview. Its available tools and behavior might change.

Official ZoomInfo remote MCP server. Search 100M+ companies and 300M+ contacts, enrich profiles, and access CRM and conversation history.

| Property | Value |
| --- | --- |
| Server identifier | `zoominfo` |
| Authentication | OAuth |
| Transport | Streamable HTTP |
| Additional administrator setup | [Review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) |

Expand

Show lessSee more

### Setup and authorization

Use an account with access to the ZoomInfo resources you want the AI client to use. Review [review provider access and consent](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-server-oauth-setup#label-gateway-tools-provider-access) before enabling the server.

When connecting, complete the provider’s authorization flow and review the requested permissions. If consent is blocked, ask the provider administrator to check application approval and the authorizing account’s access.

## Next step

[Distributing access to MCP servers](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections)
