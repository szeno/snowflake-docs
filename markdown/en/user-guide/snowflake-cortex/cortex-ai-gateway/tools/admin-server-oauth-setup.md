# Setting up MCP servers needing additional configuration

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in Amazon Web Services (AWS) commercial regions only, excluding Asia Pacific (New Zealand), Asia Pacific (Malaysia), and Europe (Spain). For the full list of AWS commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

Currently, only users with the `ACCOUNTADMIN` role can administer MCP servers in Tools. Provider-side setup can also require administrator permissions in the third-party service.

Server setup can include instance-specific configuration values, provider-side permissions, and OAuth application or service-account credentials. Check both sections below: a server with no required configuration fields can still need setup in the third-party service.

- [Instance-specific configuration values](#label-gateway-tools-setup-values)
- [Provider setup and OAuth applications](#label-gateway-tools-own-oauth-app)

| Provider | Setup guidance |
| --- | --- |
| Apollo | [Review GraphQL deployment and authorization](#label-gateway-tools-oauth-apollo) |
| Asana | [Configure an MCP app and workspace access](#label-gateway-tools-oauth-asana) |
| BigQuery | [Enable APIs and configure OAuth](#label-gateway-tools-oauth-bigquery) |
| GitHub | [Configure an application](#label-gateway-tools-oauth-github) |
| Google Workspace | [Enable APIs and configure OAuth](#label-gateway-tools-oauth-google) |
| Okta (Cortex) | [Configure an app integration and API scopes](#label-gateway-tools-oauth-okta) |
| Snowflake | [Create an MCP server and configure OAuth](#label-gateway-tools-snowflake-server) |
| Salesforce | [Create an External Client App](#label-gateway-tools-oauth-salesforce) |
| Slack | [Configure an application and scopes](#label-gateway-tools-oauth-slack) |
| Upwind | [Generate API credentials](#label-gateway-tools-oauth-upwind) |
| Wiz | [Create a service account](#label-gateway-tools-oauth-wiz) |
| Wrike | [Register an OAuth app](#label-gateway-tools-oauth-wrike) |
| Zoom | [Configure an application and scopes](#label-gateway-tools-oauth-zoom) |

Expand

Show lessSee more

After you finish the setup for a server, follow the steps in [Distributing access to MCP servers](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-personal-connections) to enable it for your organization.

## Servers that require a configuration value

The following servers require the values shown before you can enable them. This is a list of instance-specific fields, not a complete list of provider-side setup requirements. Also check [Provider setup and OAuth applications](#label-gateway-tools-own-oauth-app).

| Server | Value | What to enter |
| --- | --- | --- |
| [Azure DevOps](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-azure-devops) | `adoOrg` | Azure DevOps organization name (for example, `contoso` for `dev.azure.com/contoso`) |
| [Datadog](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-datadog) | `host` | Datadog MCP host, which must start with `mcp.` (for example, `mcp.us3.datadoghq.com` if you sign in at `us3.datadoghq.com`) |
| [dbt Labs](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-dbt-labs) | `dbtHostUrl` | dbt Cloud host (for example, `cloud.getdbt.com`, or `ACCOUNT_PREFIX.us1.dbt.com` for multi-cell accounts). Find it in **Account settings** > **Access URLs** > **MCP Endpoint URL**. |
| [Microsoft OneDrive](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-microsoft-onedrive) | `tenantId` | Microsoft Entra tenant ID (Directory ID) for your organization |
| [Microsoft Outlook](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-microsoft-outlook) | `tenantId` | Microsoft Entra tenant ID (Directory ID) for your organization |
| [Microsoft SharePoint](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-microsoft-sharepoint) | `tenantId` | Microsoft Entra tenant ID (Directory ID) for your organization |
| [Microsoft Teams](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-microsoft-teams) | `tenantId` | Microsoft Entra tenant ID (Directory ID) for your organization |
| [Okta (Cortex)](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-n-okta) | `oktaDomain` | Okta organization domain (for example, `your-org.okta.com`, `your-org.okta-emea.com`, or `your-org.oktapreview.com`) |
| [Sigma](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-sigma) | `sigmaMcpUrl` | Your Sigma MCP URL, found in Sigma under **Profile** > **MCP** > **Sigma MCP** |
| [Snowflake](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-snowflake) | `host`, `database`, `schema`, `name` | Your Snowflake account URL, plus the database, schema, and name of the MCP server object |

Expand

Show lessSee more

### Enter a configuration value

1. Sign in to Snowsight.
2. Select **AI & ML** > **AI Gateway**.
3. Select **MCP & Tools**. Tools opens in a new tab.
4. Find the server you want to configure.
5. Enter the required value or values, then save.

### Snowflake

The Snowflake MCP server exposes Cortex Search, Cortex Analyst, and SQL execution from your own Snowflake account.

1. Follow [Snowflake-managed MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp) to create an MCP server object and grant access to the tools it exposes.
2. Follow [Snowflake OAuth for custom clients](/user-guide/oauth-custom) to configure an OAuth client. Set its redirect URI to `https://identity.snowflake.com/oauth2/callback`.
3. Collect the account URL, database, schema, and MCP server name. Securely retrieve the OAuth client ID and client secret.
4. Enter these values for the Snowflake server in Tools.
5. Have users authorize with a Snowflake account and role that can use the configured MCP server and its tools.

## Provider setup and OAuth applications

Complete the provider-side prerequisites for the server you’re enabling. Where a Snowflake-managed OAuth application is available, you don’t need to register a replacement unless your organization requires its own application. The OAuth registration steps below apply when you supply your own client credentials. Provider permissions, API enablement, and consent requirements still apply even when you use a preconfigured application.

To enter client credentials, select **AI & ML** > **AI Gateway** > **MCP & Tools** in Snowsight. In the new tab, open the server’s configuration, enter the client ID and client secret, and save. Use `https://identity.snowflake.com/oauth2/callback` for authorization-code clients. Don’t copy callback URLs from older Natoma instructions.

For authorization-code flows that require a callback URL, register the following URL with the provider. Upwind and Wiz use client credentials instead and don’t require a callback URL or per-user consent:

```
https://identity.snowflake.com/oauth2/callback
```

### Review provider access and consent

Before enabling an OAuth server, confirm that the intended users can access the provider resources they need. Check the provider’s application approval policy, consent restrictions, and any plan or administrator requirements for MCP access. Authorizing an application doesn’t grant access to resources the user can’t otherwise access.

When a preconfigured OAuth application is available, use its authorization flow unless your organization requires its own client. If you supply a custom client, follow the provider-specific instructions below, configure the exact callback URL, and grant only the scopes required for the tools you intend to enable. The server catalog links to these instructions where additional setup is known; other entries require a provider access review rather than assuming no setup is needed.

### Asana

Users need access to the Asana workspaces they want to connect. If you supply your own OAuth client:

1. Open the [Asana developer console](https://app.asana.com/0/my-apps) and create an **MCP app**.
2. Add `https://identity.snowflake.com/oauth2/callback` under **OAuth** > **Redirect URLs**.
3. Under **Manage distribution**, choose the workspaces where the application can be used. If you restrict distribution to specific workspaces, add at least one.
4. Securely copy the client ID and client secret into the Asana server configuration in Tools.

See [Integrating with Asana’s MCP Server](https://developers.asana.com/docs/integrating-with-asanas-mcp-server) for application requirements. If a user can’t authorize, check that the app’s distribution includes their workspace.

### Okta (Cortex)

An Okta administrator must configure the app integration; granting Okta API scopes to the app requires the **Super Admin** role. Supply your Okta organization domain as `oktaDomain`.

For a custom OAuth client, follow [Implement OAuth for Okta](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/) to create an OIDC web application for user authorization. Register `https://identity.snowflake.com/oauth2/callback`, assign the intended users, and grant the required Okta API scopes. Enter the client ID and client secret in Tools.

For read-only operations, grant the relevant read scopes, such as `okta.users.read`, `okta.groups.read`, `okta.apps.read`, `okta.policies.read`, or `okta.logs.read`. Grant the corresponding management scopes only for tools that need to change resources. The authorizing user’s Okta permissions also constrain access.

### Google Workspace servers

You can configure the Google Workspace servers listed below using a single Google Cloud OAuth 2.0 app, which is simpler to manage, or a separate OAuth app for each server, which allows narrower permission scoping. These steps apply to both approaches.

#### Step 1: Enable the required Google APIs

1. Sign in to the [Google Cloud Console](https://console.cloud.google.com/).
2. Select your project.
3. Go to **APIs & Services** > **Library** and enable each API that corresponds to the servers you want to use:

| Server | API to enable |
| --- | --- |
| Gmail (Cortex) | Gmail API |
| Google Calendar (Cortex) | Google Calendar API |
| Google Docs (Cortex) | Google Docs API |
| Google Drive (Cortex) | Google Drive API |
| Google Forms (Cortex) | Google Forms API |
| Google Sheets (Cortex) | Google Sheets API |
| Google Slides (Cortex) | Google Slides API |
| Google Tasks (Cortex) | Tasks API |
| Google Chat | Google Chat API |
| Google People | People API |

Expand

Show lessSee more

#### Step 2: Configure the OAuth consent screen

1. Go to **Google Auth Platform** > **Branding**, or **APIs & Services** > **OAuth consent screen**.
2. Fill in the app name and support email.
3. Set **User type** to **Internal** so only users in your Google Workspace can authorize.
4. Under **Data Access**, add the scopes for the servers you’re enabling:

| Server | Scopes required |
| --- | --- |
| Gmail (Cortex) | `https://mail.google.com/` |
| Google Calendar (Cortex) | `https://www.googleapis.com/auth/calendar.readonly`, `https://www.googleapis.com/auth/calendar.events` |
| Google Docs (Cortex) | `https://www.googleapis.com/auth/documents` |
| Google Drive (Cortex) | `https://www.googleapis.com/auth/drive` |
| Google Forms (Cortex) | `https://www.googleapis.com/auth/forms.body`, `https://www.googleapis.com/auth/forms.responses.readonly` |
| Google Sheets (Cortex) | `https://www.googleapis.com/auth/spreadsheets` |
| Google Slides (Cortex) | `https://www.googleapis.com/auth/presentations` |
| Google Tasks (Cortex) | `https://www.googleapis.com/auth/tasks` |
| Google Chat | `https://www.googleapis.com/auth/chat.spaces.readonly`, `https://www.googleapis.com/auth/chat.memberships.readonly`, `https://www.googleapis.com/auth/chat.messages.readonly`, `https://www.googleapis.com/auth/chat.users.readstate.readonly` |
| Google People | `https://www.googleapis.com/auth/directory.readonly`, `https://www.googleapis.com/auth/userinfo.profile`, `https://www.googleapis.com/auth/contacts.readonly` |

Expand

Show lessSee more

For current OAuth client registration and consent requirements, see Google’s [Using OAuth 2.0 to access Google APIs](https://developers.google.com/identity/protocols/oauth2). Confirm that your Workspace administrator permits the requested API scopes.

#### Step 3: Create an OAuth 2.0 client ID

1. Go to **Google Auth Platform** > **Clients**, or **APIs & Services** > **Credentials**.
2. Select **Create client** > **Web application**.
3. Under **Authorized redirect URIs**, add `https://identity.snowflake.com/oauth2/callback`.
4. Select **Create**, then copy the **Client ID** and **Client Secret**.

#### Step 4: Configure each server

1. In Snowsight, select **AI & ML** > **AI Gateway** > **MCP & Tools**.
2. In the new tab, find the Google server you want to enable.
3. Enter the **Client ID** and **Client Secret** from Step 3.
4. Save, then repeat for each Google Workspace server you want to enable.

### BigQuery

BigQuery uses Google’s officially hosted MCP endpoint. Using your own OAuth app also requires the BigQuery MCP feature on your project.

#### Step 1: Enable the BigQuery API and BigQuery MCP

1. In the [Google Cloud Console](https://console.cloud.google.com/), go to **APIs & Services** > **Library** and enable the **BigQuery API** (`bigquery.googleapis.com`).
2. Enable the BigQuery remote MCP feature. The easiest way is to use Cloud Shell:

   Copy code

   ```
   gcloud beta services mcp enable bigquery.googleapis.com \
       --project=YOUR_PROJECT_ID
   ```

#### Step 2: Grant IAM roles

Grant the following roles to each user who will connect to BigQuery:

| Role | Purpose |
| --- | --- |
| `roles/mcp.toolUser` | Invoke MCP tools |
| `roles/bigquery.jobUser` | Run BigQuery query jobs |
| `roles/bigquery.dataViewer` | Read table data |

Expand

Show lessSee more

#### Step 3: Create an OAuth 2.0 client ID

1. Go to **APIs & Services** > **Credentials** > **Create Credentials** > **OAuth client ID**.
2. Set **Application type** to **Web application**.
3. Under **Authorized redirect URIs**, add `https://identity.snowflake.com/oauth2/callback`.
4. Copy the **Client ID** and **Client Secret**, then enter them for the BigQuery server in Cortex AI Gateway.

### GitHub

For a custom client, follow GitHub’s [Creating a GitHub App](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app) guidance. Configure repository and organization permissions for the tools you intend to use.

1. In GitHub, go to **Settings** > **Developer Settings** > **GitHub Apps**.
2. Select **New GitHub App** and fill in an app name and homepage URL.
3. For **Authorization Callback URL**, enter `https://identity.snowflake.com/oauth2/callback`.
4. Select **Create GitHub App**.
5. Copy the **Client ID**, generate a **Client Secret**, then enter both for the GitHub server in Cortex AI Gateway.

### Salesforce

Use an **External Client App** for Salesforce-hosted MCP servers. See Salesforce’s [Create an External Client App](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/create-external-client-app.html) for current prerequisites and security settings.

1. Sign in to Salesforce as an administrator. In **Setup**, search for and select **External Client App Manager**.
2. Select **New External Client App** and fill in **Basic Information**.
3. Under **API (Enable OAuth Settings)**, select **Enable OAuth**.
4. Set **Callback URL** to `https://identity.snowflake.com/oauth2/callback`.
5. Include the `mcp_api` and `refresh_token` OAuth scopes required by Salesforce’s hosted MCP setup.
6. Under **Security**, select **Issue JSON Web Token (JWT)-based access tokens for named users**. Configure the other security options according to Salesforce’s guidance and your organization’s requirements.
7. Select **Create**. Salesforce notes that the app can take up to 30 minutes to become available.
8. Select **Settings** > **OAuth Settings** > **Consumer Key and Secret**. Securely retrieve the client credentials and enter them for the Salesforce server in Cortex AI Gateway.

Note

The `mcp_api` scope is required. Without it, connecting to the Salesforce server fails with a `Mismatched Scope or Scope not allowed` error.

### Slack

1. Go to [api.slack.com/apps](https://api.slack.com/apps).
2. Select **Create New App** > **From Scratch**, name the app, select your workspace, then select **Create App**.
3. In the left sidebar, select **Agents & AI Apps** and toggle on **Model Context Protocol**.
4. Select **OAuth & Permissions**. Under **Redirect URLs**, add `https://identity.snowflake.com/oauth2/callback`, then select **Save URLs**.
5. Under **Scopes**, add at least one Bot Token Scope, for example `channels:read`.
6. From **Basic Information**, copy the **Client ID** and **Client Secret**.
7. Enter the **Client ID**, **Client Secret**, and the minimum required scopes (`openid`, `profile`, `email`) for the Slack server in Cortex AI Gateway.

### Zoom

1. Go to [marketplace.zoom.us](https://marketplace.zoom.us).
2. Select **Develop** > **Build App** > **General App** and fill in an app name.
3. Under **Basic Information** > **OAuth Information**, add `https://identity.snowflake.com/oauth2/callback` as the redirect URL.
4. Under **Scopes**, add the following:
   - `meeting:read:search`
   - `ai_companion:read:search`
   - `meeting:read:assets`
   - `cloud_recording:read:list_user_recordings`
   - `cloud_recording:read:list_recording_files`
   - `cloud_recording:read:content`
   - `docs:read:export`
   - `docs:write:import`
5. From **App Credentials**, copy the **Client ID** and **Client Secret**, then enter them and the scopes above for the Zoom server in Cortex AI Gateway.

Note

The scopes you enter in Cortex AI Gateway must match exactly what you added in the Zoom Marketplace app. A mismatch causes tool calls to fail with authorization errors.

### Apollo GraphQL

Apollo MCP Server exposes GraphQL operations as MCP tools. Its setup depends on the GraphQL API and the Apollo MCP Server deployment you use, not on an Apollo.io sales account.

Review Apollo’s [MCP Server overview](https://www.apollographql.com/docs/apollo-mcp-server), [deployment guidance](https://www.apollographql.com/docs/apollo-mcp-server/deploy), and [authorization guidance](https://www.apollographql.com/docs/apollo-mcp-server/auth) with the administrator of your graph. Confirm the endpoint and authentication requirements for that deployment before connecting. For a server you host yourself, see [Adding a custom MCP server](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-custom-apps).

### Upwind

Use an Upwind account with permission to generate credentials. Upwind uses client credentials for this connection, so there is no callback URL or user consent step.

1. In the Upwind console, select **Settings** > **Credentials** > **Generate Credential**.
2. Choose **API** as the credential type and give the credential a descriptive name.
3. Assign the scope and roles needed for the tools you plan to enable. Credentials can’t exceed the generating user’s access.
4. Copy the **Client ID** and **Client Secret** and store them securely. The secret is displayed only once.
5. Collect your Upwind organization ID and region. The organization ID is available in Settings or the console URL.
6. Use these values when configuring the Upwind connection in Cortex AI Gateway.

Resetting a credential invalidates the old credential wherever it is used. Update affected connections when rotating it.

### Wiz

Use a Wiz account with the **Project Admin** or **Global Admin** role. This connection uses client credentials, not a callback URL or per-user consent flow.

1. In the Wiz portal, select **Settings** > **Service Accounts**. Some versions place **Service Accounts** under **Access Management**.
2. Select **Add Service Account**, enter a descriptive name, and choose **Custom Integration (GraphQL API)**.
3. Restrict the account to the projects and API scopes required by the tools you plan to enable. Common read scopes include `read:issues`, `read:vulnerabilities`, `read:resources`, `read:inventory`, and `read:cloud_configuration`; add `admin:audit` only if you need audit-log access. Leaving the project selection empty makes the account apply to all projects.
4. Create the service account and securely save its **Client ID** and **Client Secret**. The secret isn’t shown again.
5. Under the user icon’s tenant settings, copy the GraphQL API endpoint for your tenant, such as `https://api.<region>.app.wiz.io/graphql`.
6. Use the endpoint and credentials when configuring the Wiz connection in Cortex AI Gateway.

### Wrike

Wrike uses an authorization-code flow. When you supply your own OAuth client, register an app using the steps below. Users authorize their own connections whether you use a preconfigured client or your own. See [Wrike OAuth 2.0](https://developers.wrike.com/oauth-20-authorization/) for the provider’s registration and authorization requirements.

1. In Wrike, select your profile image > **Apps & Integrations** > **API** > **+ App**. You can also open the [Wrike App Console](https://www.wrike.com/appconsole.htm#/api).
2. Enter an app name, such as `Tools`.
3. Set **Redirect URI** to `https://identity.snowflake.com/oauth2/callback` and save the app.
4. Securely copy the **Client ID** and **Client Secret** from the app configuration and enter them for the Wrike connection in Cortex AI Gateway.
5. Request only the scopes required by the tools you plan to use. Wrike scopes are case-sensitive.

When users connect, they sign in to Wrike and approve the consent request. A password reset or account deactivation can invalidate their tokens and require reauthorization.

## Next step

[Adding a custom MCP server](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/admin-custom-apps)
