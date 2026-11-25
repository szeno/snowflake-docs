# Setting up MCP servers needing additional configuration

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in Amazon Web Services (AWS) commercial regions only, excluding Asia Pacific (New Zealand) and Middle East (UAE). For the full list of AWS commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

Currently, only users with the `ACCOUNTADMIN` role can administer MCP servers in Tools. Provider-side setup can also require administrator permissions in the third-party service.

Server setup can include instance-specific configuration values, provider-side permissions, and OAuth application or service-account credentials. Check both sections below: a server with no required configuration fields can still need setup in the third-party service.

- [Instance-specific configuration values](#label-gateway-tools-setup-values)
- [Provider setup and OAuth applications](#label-gateway-tools-own-oauth-app)

| Provider | Setup guidance |
| --- | --- |
| Apollo | [Review GraphQL deployment and authorization](#label-gateway-tools-oauth-apollo) |
| Asana | [Configure an MCP app and workspace access](#label-gateway-tools-oauth-asana) |
| Bigdata.com | [Create an OAuth client](#label-gateway-tools-oauth-bigdata) |
| BigQuery | [Enable APIs and configure OAuth](#label-gateway-tools-oauth-bigquery) |
| Collibra | [Register a user application](#label-gateway-tools-oauth-collibra) |
| GitHub | [Configure an application](#label-gateway-tools-oauth-github) |
| Google Workspace | [Enable APIs and configure OAuth](#label-gateway-tools-oauth-google) |
| Microsoft Work IQ | [Register an Entra app and grant consent](#label-gateway-tools-oauth-work-iq) |
| Okta (Cortex) | [Configure an app integration and API scopes](#label-gateway-tools-oauth-okta) |
| S&P Global Energy: AI Ready Data | [Request OAuth client credentials](#label-gateway-tools-oauth-sp-global-energy) |
| ServiceNow | [Register an inbound OAuth integration](#label-gateway-tools-oauth-servicenow) |
| Smartsheet | [Register a Developer Tools app](#label-gateway-tools-oauth-smartsheet) |
| Snowflake | [Create an MCP server and configure OAuth](#label-gateway-tools-snowflake-server) |
| Salesforce | [Create an External Client App](#label-gateway-tools-oauth-salesforce) |
| Slack | [Configure an application and scopes](#label-gateway-tools-oauth-slack) |
| Upwind | [Generate API credentials](#label-gateway-tools-oauth-upwind) |
| Wiz | [Create a service account](#label-gateway-tools-oauth-wiz) |
| Workday | [Register an external agent](#label-gateway-tools-oauth-workday) |
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
| [Collibra](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-collibra) | `collibraHost` | Collibra tenant host (for example, `mycompany.collibra.com`), without `https://` or a path |
| [Datadog](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-datadog) | `host` | Datadog MCP host, which must start with `mcp.` (for example, `mcp.us3.datadoghq.com` if you sign in at `us3.datadoghq.com`) |
| [dbt Labs](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-dbt-labs) | `dbtHostUrl` | dbt Cloud host (for example, `cloud.getdbt.com`, or `ACCOUNT_PREFIX.us1.dbt.com` for multi-cell accounts). Find it in **Account settings** > **Access URLs** > **MCP Endpoint URL**. |
| [Glean](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-glean) | `gleanInstanceName` | Glean instance name, the part before `-be.glean.com` (for example, `snowflake` for `snowflake-be.glean.com`) |
| [Microsoft OneDrive](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-microsoft-onedrive) | `tenantId` | Microsoft Entra tenant ID (Directory ID) for your organization |
| [Microsoft Outlook](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-microsoft-outlook) | `tenantId` | Microsoft Entra tenant ID (Directory ID) for your organization |
| [Microsoft SharePoint](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-microsoft-sharepoint) | `tenantId` | Microsoft Entra tenant ID (Directory ID) for your organization |
| [Microsoft Teams](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-microsoft-teams) | `tenantId` | Microsoft Entra tenant ID (Directory ID) for your organization |
| [Observe](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-observe) | `host` | Observe tenant host that you sign in at (for example, `123456789.observeinc.com`) |
| [Okta (Cortex)](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-n-okta) | `oktaDomain` | Okta organization domain (for example, `your-org.okta.com`, `your-org.okta-emea.com`, or `your-org.oktapreview.com`) |
| [Pantomath](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-pantomath) | `pantomathHost` | Pantomath workspace host (for example, `mycompany.pantomath.app`), without `https://` or a path |
| [ServiceNow](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-servicenow) | `serviceNowInstanceUrl` | ServiceNow instance hostname (for example, `your-company.service-now.com`). Optionally, also set `mcpServerName` if you don’t use `sn_mcp_server_default`. |
| [Sigma](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-sigma) | `sigmaMcpUrl` | Your Sigma MCP URL, found in Sigma under **Profile** > **MCP** > **Sigma MCP** |
| [Snowflake](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-snowflake) | `host`, `database`, `schema`, `name` | Your Snowflake account URL, plus the database, schema, and name of the MCP server object |
| [Supernova.io](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-supernova) | `designSystemId` | Supernova design system ID, from your `app.supernova.io` URL (for example, `60216`) |
| [Workday](/user-guide/snowflake-cortex/cortex-ai-gateway/tools/available-servers#label-gateway-tools-server-workday) | `region`, `tenantAlias` | Workday Agent Gateway region (`us`, `eu`, `uk`, `ca`, `au`, `sg`, `in`, `jp`, or `sales`) and tenant alias (for example, `acme_prod1`) |

Expand

Show lessSee more

### Enter a configuration value

1. Sign in to Snowsight.
2. Select **AI Gateway**.
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

To enter client credentials, select **AI Gateway** > **MCP & Tools** in Snowsight. In the new tab, open the server’s configuration, enter the client ID and client secret, and save. Use `https://identity.snowflake.com/oauth2/callback` for authorization-code clients. Don’t copy callback URLs from older Natoma instructions.

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

### Bigdata.com

Bigdata.com doesn’t support dynamic client registration. One OAuth client serves your whole organization, and each user signs in with their own Bigdata.com account when they connect.

1. In the Bigdata.com Developer Platform, go to **OAuth Clients** and select **Create OAuth Client**.
2. Enter a **Client Name**, and under **Redirect URIs** add `https://identity.snowflake.com/oauth2/callback`.
3. Select **Create**, then copy the **Client ID** and **Client Secret**. The client secret is shown only once. If you lose it, delete the client and create a new one.
4. In Snowsight, select **AI Gateway** > **MCP & Tools**. In the new tab, open the Bigdata.com server’s configuration, enter the client ID and client secret, and save.

For more information, see Bigdata.com’s [MCP integration guide](https://docs.bigdata.com/mcp-reference/api-integrations/perplexity-mcp-integration).

### Collibra

Collibra doesn’t support dynamic client registration. You need Collibra administrator privileges to register an OAuth application, and you also enter your Collibra host as a [configuration value](#label-gateway-tools-setup-values).

1. In Collibra, go to **Settings** > **OAuth applications** and select **New Application**.
2. Under **User Application**, select **Register user application**. Don’t select an integration application, which uses the client credentials flow instead of user sign-in.
3. Enter an **Application name**, and under **Redirect URI** add `https://identity.snowflake.com/oauth2/callback`.
4. Select **Register**, then copy the client ID and client secret from the **Registration Confirmation** dialog. The client secret is shown only once.
5. In Snowsight, select **AI Gateway** > **MCP & Tools**. In the new tab, open the Collibra server’s configuration, enter the client ID and client secret, and save.

Collibra assigns all scopes to the application, so you don’t select scopes. For more information, see Collibra’s [OAuth applications](https://productresources.collibra.com/docs/collibra/latest/Content/Settings/OAuth/co_oauth-settings.htm) and [Collibra MCP](https://productresources.collibra.com/docs/collibra/latest/Content/ModelContextProtocol/co_integrating-with-collibra-mcp.htm) documentation.

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

1. In Snowsight, select **AI Gateway** > **MCP & Tools**.
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

### Microsoft Work IQ

Microsoft Work IQ requires your own Microsoft Entra app registration. Every request runs as the signed-in user and is limited to that user’s Microsoft 365 permissions.

Before you start, confirm the following:

- A Microsoft Entra administrator who can create app registrations and grant admin consent (Global Administrator, Privileged Role Administrator, Cloud Application Administrator, or Application Administrator).
- Work IQ is enabled for your tenant. See Microsoft’s [Enable your tenant for Work IQ](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/enable-work-iq).
- Users are assigned to a usage-based billing plan for Copilot Credits. Some Microsoft documentation also requires a Microsoft 365 Copilot license for each user; confirm which applies to your tenant.

#### Step 1: Register an app in Microsoft Entra

Use **App registrations**, not **Enterprise applications**. Client secrets and redirect URIs can only be configured on an app registration.

1. In the Microsoft Entra admin center, go to **App registrations** > **New registration**.
2. Enter a name, and set **Supported account types** to **Single tenant**.
3. Under **Redirect URI**, select the **Web** platform and enter `https://identity.snowflake.com/oauth2/callback`. Don’t use the **Single-page application** or **Mobile and desktop** platforms; they don’t accept a client secret.
4. Select **Register**, then copy the **Application (client) ID** from the **Overview** page.

#### Step 2: Create a client secret

1. In the app registration, go to **Certificates & secrets** > **Client secrets** > **New client secret**.
2. Enter a description and expiry, then select **Add**.
3. Copy the secret **Value** immediately. It’s shown only once. Don’t use the **Secret ID**.

Record the expiry date. When the secret expires, connections fail until you enter a new secret in Cortex AI Gateway.

#### Step 3: Add API permissions and grant admin consent

1. Go to **API permissions** > **Add a permission**.
2. Under **APIs my organization uses**, search for **Work IQ** and add these delegated permissions:

   | Permission | Purpose |
   | --- | --- |
   | `WorkIQAgent.Ask` | Required to connect |
   | `WorkIQ.Read` | Read Microsoft 365 data |
   | `WorkIQ.Act` | Create, update, and delete data and run actions such as sending mail |

   Expand

   Show lessSee more
3. Under **Microsoft Graph**, add the delegated permissions for the Microsoft 365 products you want users to reach:

   | Product | Permissions |
   | --- | --- |
   | Sign-in and profile | `User.Read`, `offline_access` |
   | OneDrive and SharePoint | `Files.Read.All`, `Sites.Read.All` |
   | Outlook mail | `Mail.Read` |
   | Teams chats | `Chat.Read` |
   | Teams channels | `ChannelMessage.Read.All` |
   | Teams meeting transcripts | `OnlineMeetingTranscript.Read.All` |
   | People and contacts | `People.Read.All` |
   | Graph connectors (external content) | `ExternalItem.Read.All` (optional) |

   Expand

   Show lessSee more
4. Select **Grant admin consent** for your tenant, and confirm that every permission shows a **Granted** status.

If **Work IQ** doesn’t appear in the API search, Work IQ isn’t enabled for your tenant yet.

#### Step 4: Configure the server in Cortex AI Gateway

1. In Snowsight, select **AI Gateway** > **MCP & Tools**.
2. In the new tab, find the Microsoft Work IQ server and enter the following values:

   | Field | Value |
   | --- | --- |
   | Client ID | The application (client) ID from Step 1 |
   | Client secret | The secret value from Step 2 |
   | Scopes | `api://workiq.svc.cloud.microsoft/WorkIQAgent.Ask api://workiq.svc.cloud.microsoft/WorkIQ.Read api://workiq.svc.cloud.microsoft/WorkIQ.Act offline_access` |

   Expand

   Show lessSee more

   Enter only the Work IQ scopes and `offline_access` in the scopes field. Don’t add Microsoft Graph scopes here: Microsoft Entra issues a token for a single API, and the Graph permissions only need admin consent on the app registration.
3. Save.

If you add Graph permissions later, grant admin consent again, then have users disconnect and reconnect Microsoft Work IQ so that a new token is issued.

#### Step 5: Configure the Work IQ policy in Microsoft 365

1. In the Microsoft 365 admin center, go to **Agents** > **Tools** > **Work IQ MCP**.
2. Confirm that the server is available and assigned to the intended users.
3. Write operations (create, update, delete, and send) are off by default. To allow them, enable **Allow write actions** and **Allow create** under **Policy**. Write tools stay blocked by this policy even when they’re enabled in Cortex AI Gateway.

For more information, see Microsoft’s [Work IQ MCP overview](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/mcp/overview) and [Work IQ API permissions](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/permissions).

### S&P Global Energy: AI Ready Data

S&P Global Energy doesn’t support dynamic client registration or publish a self-service client registration flow. Access requires an S&P Global Energy subscription that includes AI Ready Data.

1. Request MCP access and OAuth client credentials from S&P Global. Start from the S&P Global [MCP getting started](https://developer.spglobal.com/energy/delivery-solutions/mcp/getting-started) page, or contact your S&P Global account team.
2. Ask for an authorization code client with `https://identity.snowflake.com/oauth2/callback` registered as the redirect URL.
3. In Snowsight, select **AI Gateway** > **MCP & Tools**. In the new tab, open the S&P Global Energy: AI Ready Data server’s configuration, enter the client ID and client secret, and save.

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

### ServiceNow

ServiceNow doesn’t support dynamic client registration and supports only the authorization code grant. Before you start, confirm the following:

- The **Model Context Protocol Server** app (MCP Server Console) is installed on your instance, and an MCP server is configured in MCP Server Console. Its name is the `mcpServerName` [configuration value](#label-gateway-tools-setup-values).
- You have the `oauth_admin`, `mi_admin`, or `admin` role.

1. In ServiceNow, go to **All** > **Machine Identity Console** > **Inbound integrations** and create a new integration.
2. Select **OAuth - Authorization code grant**.
3. Enter `https://identity.snowflake.com/oauth2/callback` as the redirect URL. It must match exactly.
4. Under **Advanced Options**, set **Token Format** to **JWT**.
5. Save the integration, then copy its client ID and client secret.
6. In Snowsight, select **AI Gateway** > **MCP & Tools**. In the new tab, open the ServiceNow server’s configuration, enter the client ID and client secret, and save.

Users connect with their own ServiceNow accounts, and their roles and ACLs determine which tools and data they can access. For more information, see ServiceNow’s [MCP Server Console FAQ](https://www.servicenow.com/community/now-assist-articles/mcp-server-console-faq/ta-p/3550125).

### Slack

1. Go to [api.slack.com/apps](https://api.slack.com/apps).
2. Select **Create New App** > **From Scratch**, name the app, select your workspace, then select **Create App**.
3. In the left sidebar, select **Agents & AI Apps** and toggle on **Model Context Protocol**.
4. Select **OAuth & Permissions**. Under **Redirect URLs**, add `https://identity.snowflake.com/oauth2/callback`, then select **Save URLs**.
5. Under **Scopes**, add at least one Bot Token Scope, for example `channels:read`.
6. From **Basic Information**, copy the **Client ID** and **Client Secret**.
7. Enter the **Client ID**, **Client Secret**, and the minimum required scopes (`openid`, `profile`, `email`) for the Slack server in Cortex AI Gateway.

### Smartsheet

Smartsheet doesn’t support dynamic client registration. Developer Tools requires a Business, Enterprise, or Advanced Work Management plan, and Smartsheet must approve your Developer Tools access.

1. In Smartsheet, select your account icon, then **Developer Tools**. If you don’t have a developer profile yet, select **Create Developer Profile**.
2. Select **Create New App**, and enter an app name, description, app URL, and contact.
3. In **App redirect URL**, enter `https://identity.snowflake.com/oauth2/callback`.
4. Select **Save**, then copy the **App client ID** and **App secret**. You can view them again later in **Developer Tools**.
5. In Snowsight, select **AI Gateway** > **MCP & Tools**. In the new tab, open the Smartsheet server’s configuration, enter the client ID and client secret, and save.

Smartsheet administrators control MCP access for the organization, including whether write tools are available. For more information, see Smartsheet’s [OAuth guide](https://developers.smartsheet.com/api/smartsheet/guides/advanced-topics/oauth) and [Smartsheet MCP server](https://developers.smartsheet.com/ai-mcp/smartsheet/install-the-smartsheet-mcp-server) documentation.

### Workday

Workday doesn’t support dynamic client registration. Workday generates the OAuth client when you register Cortex AI Gateway as an external agent in Agent System of Record. This functionality is available to Workday Extend Professional customers, and customers on a Main Service Agreement (MSA) must first complete the **Enable Innovation Services Feature and AI Data Contributions for MSA Customers** task. You need access to the **Agent Management Hub** domain. You also enter your Workday region and tenant alias as [configuration values](#label-gateway-tools-setup-values).

1. Set up Agent System of Record, and register Cortex AI Gateway as an external agent.
2. Open the **Agent Management Hub** report, select the **Agent Registry** tab, select the agent, and then select **Configure Agent**.
3. Enable the skills you want, and for each delegate skill, select the security groups in **Available To**.
4. Enter `https://identity.snowflake.com/oauth2/callback` as the redirect URI.
5. Copy the **OAuth Client ID** and **OAuth Client Secret**. Workday shows these values only once.
6. Select **Activate Agent**, and configure the security policies for the agent skills.
7. In Snowsight, select **AI Gateway** > **MCP & Tools**. In the new tab, open the Workday server’s configuration, enter the client ID and client secret, and save.

Workday refresh tokens expire after 30 days, so users might need to authorize again periodically. For more information, see Workday’s [Connect an external agent with Workday MCP](https://doc.workday.com/admin-guide/en-us/workday-ai/agents/external-agents/connect-an-external-agent-with-workday-mcp.html) and [Configure external agents](https://doc.workday.com/admin-guide/en-us/workday-ai/agents/external-agents/configure-external-agents.html).

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
