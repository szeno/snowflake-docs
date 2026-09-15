# MCP Connectors

## Overview

An MCP connector in Snowflake connects Snowflake CoWork and Cortex Agents to a remote Model Context Protocol (MCP) server,
letting the agent discover and invoke tools hosted by providers such as Atlassian Jira, Salesforce,
or your own custom applications. With MCP connectors, your agents can go beyond answering questions to taking action across
enterprise systems, such as creating Jira tickets, updating Salesforce records, or posting to Slack, all within
Snowflake’s governed environment.

### How MCP connectors work

Admins create an external MCP server object that references an [API integration](/sql-reference/sql/create-api-integration), which contains OAuth credentials.
Snowflake supports Standard OAuth with credentials (client ID, client secret), as well as Dynamic Client
Registration (DCR). You can select from a set of available MCP connectors or build your custom connector.
After the MCP connector is added to the agent, users can authenticate with the third-party service and use the
tools directly with Cortex Agents and in Snowflake CoWork.

### Setup flow

To create an MCP connector and use it in your Snowflake workflows, complete the following steps:

1. **Provider setup**: The account admin creates an MCP server on the provider’s dashboard (for example, Salesforce or Atlassian) and obtains OAuth credentials.
2. **API integration**: The account admin creates an API integration in Snowflake that stores the server URL, client ID, client secret, and OAuth endpoints.
3. **External MCP server creation**: The account admin creates an external MCP server object that references the API integration.
4. **Agent configuration**: The agent developer adds the external MCP server to a Cortex Agent’s specification.
5. **User authentication**: Snowflake CoWork users connect to the MCP server through the Snowflake CoWork interface, authenticating with the third-party service using OAuth.

### Tool discovery and invocation

When an agent is invoked, it retrieves the list of available tools from each configured external MCP server
using the `tools/list` method. During orchestration, the agent invokes specific tools using the `tools/call`
method and passing the required arguments. Snowflake checks that both the MCP server and its underlying API
integration are enabled before executing any tool call.

### Access control

The following table describes the privileges required for external MCP server operations:

| Privilege | Object | Required for |
| --- | --- | --- |
| CREATE EXTERNAL MCP SERVER | Schema | Creating an external MCP server |
| OWNERSHIP | MCP Server | Dropping the MCP server |
| MODIFY | MCP Server | Updating, dropping, describing, showing, and using the MCP server |
| USAGE | MCP Server | Connecting to the MCP server and discovering tools |
| USAGE | API Integration | Connecting to the MCP server and discovering tools |
| OWNERSHIP or MODIFY | API Integration | Enabling, disabling, or dropping the API integration |

Expand

Show lessSee more

By default, only account admins have these privileges.

To grant another role access to an external MCP server, you must grant USAGE on both the MCP server and its underlying API integration:

Copy code

```
-- Find the API integration name
DESCRIBE EXTERNAL MCP SERVER <mcp_server_name>;

-- Grant access to the MCP server
GRANT USAGE ON EXTERNAL MCP SERVER <mcp_server_name> TO ROLE <role_name>;

-- Grant access to the underlying API integration
GRANT USAGE ON INTEGRATION <integration_name> TO ROLE <role_name>;
```

To view external MCP servers available to your current role, use `SHOW EXTERNAL MCP SERVERS`.

Important

External MCP servers are not provided, maintained, or verified by Snowflake. By connecting to an
external MCP server, you are responsible for verifying the server’s trustworthiness, ensuring you
have the rights to access and process the data it provides, and complying with all applicable laws
and third-party terms governing that data. Snowflake does not warrant or support any external MCP
server, and is not responsible for any errors, data loss, or security incidents arising from its use.

## Set up supported MCP connectors

You can connect with the following MCP servers with minimal configuration:

- Atlassian
- GitHub
- Glean
- Linear
- Salesforce

With these MCP providers, you complete the following workflow:

1. Specify the provider detail in the `API_USER_AUTHENTICATION` type field.
2. Set up the provider configuration, which is unique to each provider.
3. Reference this API integration in the external MCP server object creation.

Note

For OAuth authorization code flows, the client needs to supply a callback URL after consent is given to the external service provider. The external service provider will send the user to the callback URL to finish the flow. Register the following callback URL with your OAuth app:

`https://identity.snowflake.com/oauth2/callback`

Some third-party MCP providers also require you to allowlist this URL in their configuration.

For PrivateLink specifically, use `SYSTEM$ALLOWLIST_PRIVATELINK` and pick the entry that starts with `app.<region>.privatelink.snowflakecomputing`. Append `/oauth/complete-secret` to finish creating the callback URL.

AtlassianGitHubGleanLinearSalesforce

1. Navigate to `Admin.atlassian.com`.
2. From the left navigation, select **Apps > AI Settings > Rovo MCP Server**.
3. Under **Your domains**, select **Add Domain** to add two callback URLs as described in the note above.
4. Select **Add**.
5. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
6. In the navigation menu, select **AI & ML** » **Agents**.
7. Select **Settings**.
8. Select **Tools and Connectors**.
9. Select **Browse Connectors**.
10. Select **Atlassian**.
11. Enter a name and description for the MCP Server.
12. For **Server URL**, enter `https://mcp.atlassian.com/v1/mcp`.
13. Select the database and schema where the MCP Server will be created.
14. Select **Add**.

The following example shows the SQL commands to create the API integration and MCP server for Atlassian:

Copy code

```
-- Create the API integration using dynamic client registration (DCR)
CREATE API INTEGRATION jira_mcp_api_integration
  API_PROVIDER = external_mcp
  API_ALLOWED_PREFIXES = ('https://mcp.jira.atlassian.com')
  API_USER_AUTHENTICATION = (
    TYPE=OAUTH_DYNAMIC_CLIENT,
    OAUTH_RESOURCE_URL='https://mcp.atlassian.com/v1/mcp'
  )
  ENABLED = TRUE;

-- Create the external MCP server
CREATE EXTERNAL MCP SERVER atlassian_mcp_server
  WITH DISPLAY_NAME = 'Atlassian (Jira & Confluence)'
  URL='https://mcp.atlassian.com/v1/mcp'
  API_INTEGRATION = jira_mcp_api_integration;
```

1. Sign in to GitHub.
2. Navigate to the top right avatar, and select **Settings**.
3. Select **Developer Settings**.
4. Select **New GitHub App**. Provide a name, homepage URL, and supply two callback URLs as described previously.
5. You can disable Webhook and set custom permissions (scopes).
6. Create the app. You should see the app appear in **GitHub Apps** in the **Developer Settings**.
7. Select **Edit** and **Generate a new client secret**. Write the client ID and secret down.
8. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
9. In the navigation menu, select **AI & ML** » **Agents**.
10. Select **Settings**.
11. Select **Tools and Connectors**.
12. Select **Browse Connectors**.
13. Select **GitHub**.
14. Enter a description for the MCP Server.
15. For **Server URL**, enter `https://api.githubcopilot.com/mcp`.
16. For the **Token endpoint**, enter `https://github.com/login/oauth/access_token`.
17. For the **Authorization endpoint**, enter `https://github.com/login/oauth/authorize`.
18. For the **Client ID**, enter the client ID you wrote down.
19. For the **Client secret**, enter the client secret you wrote down.
20. Select the database and schema where the MCP Server will be created.
21. Select **Add**.

1. Navigate to `app.glean.com/settings/install`.
2. Select **Configure MCP Server**.
3. In the **Host application** select **Custom**. For the MCP server select the desired server (can be default).
4. Copy the server URL.
5. Select **Save**.
6. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
7. In the navigation menu, select **AI & ML** » **Agents**.
8. Select **Settings**.
9. Select **Tools and Connectors**.
10. Select **Browse Connectors**.
11. Select **Glean**.
12. Enter a description for the MCP Server.
13. For the **Server URL**, enter the server URL you copied.
14. Select the database and schema where the MCP Server will be created.
15. Select **Add**.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **Agents**.
3. Select **Settings**.
4. Select **Tools and Connectors**.
5. Select **Browse Connectors**.
6. Select **Linear**.
7. Enter a description for the MCP Server.
8. Select the database and schema where the MCP Server will be created.
9. Select **Add**.

Note

You must have Admin access to your Salesforce (sandbox) organization. For the latest Salesforce-side setup instructions,
see [Create an External Client App](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/create-external-client-app.html)
in the Salesforce documentation.

1. Navigate to your Salesforce organization.
2. Go to **Setup** from the gear icon.
3. Search for **External Client App Manager** in the search bar of the new page.
4. Select **New External Client App** and check **Enable OAuth**.
5. After the app is created, navigate to the **OAuth Settings** of the app.
6. Configure the scopes (ensure `mcp_api` is included) and the callback URI to be `https://identity.snowflake.com/oauth2/callback`.
7. Note the **Consumer Key and Secret**, which are the OAuth client ID and client secret to be used in the Snowflake external API integration.
8. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
9. In the navigation menu, select **AI & ML** » **Agents**.
10. Select **Settings**.
11. Select **Tools and Connectors**.
12. Select **Browse Connectors**.
13. Select **Salesforce**.
14. Enter a description for the MCP Server.
15. Enter the MCP server URL. Salesforce exposes its MCP servers through individual URLs, and the user needs to know what server/tools to access. The OAuth tokens retrieved from the last step can be used for all servers and tools, as long as the scopes permit.

The base URL for each hosted MCP server is:

- `https://api.salesforce.com/platform/mcp/v1/sandbox/<server_name>` if your organization is a sandbox
- `https://api.salesforce.com/platform/mcp/v1/platform/<server_name>` with no `/sandbox` suffix otherwise

Because the test organization is a sandbox, use `test.salesforce.com` as the domain of the OAuth endpoints,
and `https://api.salesforce.com/platform/mcp/v1/sandbox/<server_name>` as the base URL
in the `EXTERNAL MCP SERVER` object.

You can construct the desired MCP server URLs with the base. For example:

- `https://api.salesforce.com/platform/mcp/v1/sandbox/sobject-all`
- `https://api.salesforce.com/platform/mcp/v1/sandbox/query`
- `https://api.salesforce.com/platform/mcp/v1/sandbox/search`

16. Enter the token and authorization endpoints:

- For the **Token endpoint**, enter `https://<domain>/services/oauth2/token`.
- For the **Authorization endpoint**, enter `https://<domain>/services/oauth2/authorize`.

Note

`<domain>` can be one of `test.salesforce.com` if the Salesforce organization is a sandbox
or `login.salesforce.com` otherwise.

17. Enter the client ID and client secret you noted.
18. Select the database and schema where the MCP Server will be created.
19. Select **Add**.

## Custom MCP connectors

You can also manually configure custom connectors to connect to any MCP-compatible endpoint.

1. Provide the full OAuth configuration as part of the API integration creation:

Important

When you use `TYPE = OAUTH2`, specify `OAUTH_REFRESH_TOKEN_VALIDITY`
(in seconds) in the `API_USER_AUTHENTICATION` block to control how long
the OAuth refresh token issued by the external MCP service stays valid
before users must re-authenticate. The value must be at least `3600`
(one hour). If you don’t set this parameter, the value defaults to `0`,
which Snowflake treats as a refresh token that never expires. Snowflake
recommends setting an explicit, finite value so users periodically
re-authenticate to the external MCP service.

This parameter does not apply to `TYPE = OAUTH_DYNAMIC_CLIENT`.

Copy code

```
 -- Create the API integration with full OAuth configuration
CREATE API INTEGRATION custom_mcp_api_integration
API_PROVIDER = external_mcp
API_ALLOWED_PREFIXES = ('https://internal.mycompany.com/mcp')
API_USER_AUTHENTICATION = (
  TYPE = OAUTH2
  OAUTH_CLIENT_ID = 'your_client_id'
  OAUTH_CLIENT_SECRET = 'your_client_secret'
  OAUTH_TOKEN_ENDPOINT = 'https://internal.mycompany.com/oauth/token'
  OAUTH_CLIENT_AUTH_METHOD = CLIENT_SECRET_BASIC
  OAUTH_AUTHORIZATION_ENDPOINT = 'https://internal.mycompany.com/oauth/authorize'
  OAUTH_ALLOWED_SCOPES = ('scope1', 'scope2')
  OAUTH_REFRESH_TOKEN_VALIDITY = 86400
)
ENABLED = TRUE;
```

For providers that issue a static client ID without a client secret (a public client), set
`OAUTH_CLIENT_AUTH_METHOD` to `NONE`:

Copy code

```
CREATE API INTEGRATION custom_mcp_integration
  API_PROVIDER = external_mcp
  API_ALLOWED_PREFIXES = ('https://internal.mycompany.com')
  API_USER_AUTHENTICATION = (
    TYPE = OAUTH2
    OAUTH_CLIENT_ID = 'your_static_client_id'
    OAUTH_CLIENT_AUTH_METHOD = NONE
    OAUTH_AUTHORIZATION_ENDPOINT = 'https://internal.mycompany.com/oauth/authorize'
    OAUTH_TOKEN_ENDPOINT = 'https://internal.mycompany.com/oauth/token'
  )
  ENABLED = TRUE;
```

Alternatively, you can use API integration with DCR:

Copy code

```
CREATE API INTEGRATION custom_mcp_api_integration
  API_PROVIDER = external_mcp
  API_ALLOWED_PREFIXES = ('https://internal.mycompany.com/mcp')
  API_USER_AUTHENTICATION = (
 TYPE = OAUTH_DYNAMIC_CLIENT
 OAUTH_RESOURCE_URL='https://internal.mycompany.com/mcp'
  )
  ENABLED = TRUE;
```

The following example shows a Google Workspace integration with `OAUTH_ALLOWED_SCOPES` specifying the required Google API scopes.
You must enable the corresponding APIs (Gmail, Drive, Calendar, Contacts) on the Google Cloud project.
Include only the scopes for the services you need:

Copy code

```
CREATE API INTEGRATION google_mcp_integration
  API_PROVIDER = EXTERNAL_MCP
  API_ALLOWED_PREFIXES = (
    'https://gmail.mcp.snowflake.com/mcp',
    'https://gcal.mcp.snowflake.com/mcp',
    'https://gdrive.mcp.snowflake.com/mcp',
    'https://gcontacts.mcp.snowflake.com/mcp'
  )
  API_USER_AUTHENTICATION = (
    TYPE = OAUTH2
    OAUTH_CLIENT_ID = '<client_id>'
    OAUTH_CLIENT_SECRET = '<client_secret>'
    OAUTH_TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'
    OAUTH_AUTHORIZATION_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'
    OAUTH_ALLOWED_SCOPES = (
      'https://www.googleapis.com/auth/userinfo.email',
      'https://www.googleapis.com/auth/userinfo.profile',
      'https://www.googleapis.com/auth/gmail.readonly',
      'https://www.googleapis.com/auth/gmail.compose',
      'https://www.googleapis.com/auth/gmail.labels',
      'https://www.googleapis.com/auth/gmail.modify',
      'https://www.googleapis.com/auth/drive.readonly',
      'https://www.googleapis.com/auth/drive.file',
      'https://www.googleapis.com/auth/calendar.readonly',
      'https://www.googleapis.com/auth/contacts.readonly'
    )
  )
  ENABLED = TRUE;
```

The `userinfo.email` and `userinfo.profile` scopes are required for every Google MCP connection. The remaining scopes each pair with a Snowflake-hosted MCP server URL for one Google service. Include only the scopes for the services your agent needs in `OAUTH_ALLOWED_SCOPES`, and register each service separately with `CREATE EXTERNAL MCP SERVER` (see step 2) using its matching URL:

| Service | Scopes | MCP server URL |
| --- | --- | --- |
| Gmail | `gmail.readonly`, `gmail.compose`, `gmail.labels`, `gmail.modify` | `https://gmail.mcp.snowflake.com/mcp` |
| Google Drive | `drive.readonly`, `drive.file` | `https://gdrive.mcp.snowflake.com/mcp` |
| Google Calendar | `calendar.readonly` | `https://gcal.mcp.snowflake.com/mcp` |
| Google Contacts | `contacts.readonly` | `https://gcontacts.mcp.snowflake.com/mcp` |

Expand

Show lessSee more

For more information about configuring a Google OAuth web client, see [Using OAuth 2.0 to Access Google APIs](https://developers.google.com/identity/protocols/oauth2) in the Google documentation.

2. Create the MCP server object:

   Copy code

   ```
   -- Create the external MCP server
   CREATE EXTERNAL MCP SERVER mycompany_mcp_server
     WITH DISPLAY_NAME = 'Mycompany MCP server'
     URL = 'https://internal.mycompany.com/mcp'
     API_INTEGRATION = custom_mcp_api_integration;
   ```

   For a Google Workspace integration, create one external MCP server per service you want to use, with `URL` set to the matching value from the service table above. For example, the following statements register Gmail and Google Calendar against the `google_mcp_integration` defined earlier:

   Copy code

   ```
   CREATE EXTERNAL MCP SERVER google_gmail
     WITH DISPLAY_NAME = 'Gmail'
     URL = 'https://gmail.mcp.snowflake.com/mcp'
     API_INTEGRATION = google_mcp_integration;

   CREATE EXTERNAL MCP SERVER google_calendar
     WITH DISPLAY_NAME = 'Google Calendar'
     URL = 'https://gcal.mcp.snowflake.com/mcp'
     API_INTEGRATION = google_mcp_integration;
   ```
3. Reference the MCP server in the Agent configuration:

   Copy code

   ```
   -- Add MCP server to agent
   ALTER AGENT my_support_agent
     ADD MCP_SERVER = 'db.schema.MCP server';
   ```

### OAuth parameters for custom MCP servers

The following table describes the OAuth parameters for custom MCP servers:

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| OAUTH\_CLIENT\_ID | STRING | Yes | None | Client ID from the MCP server provider |
| OAUTH\_CLIENT\_SECRET | STRING | Yes | None | Client secret from the MCP server provider |
| OAUTH\_DISCOVERY\_URL | STRING | No | None | OpenID Connect discovery URL for automatic endpoint resolution |
| OAUTH\_TOKEN\_ENDPOINT | STRING | Yes | None | Endpoint for exchanging authorization codes for access tokens |
| OAUTH\_AUTHORIZATION\_ENDPOINT | STRING | Yes | None | Endpoint where users authorize the connection |
| OAUTH\_CLIENT\_AUTH\_METHOD | STRING | No | CLIENT\_SECRET\_BASIC | Authentication method: `CLIENT_SECRET_BASIC`, `CLIENT_SECRET_POST`, or `NONE` for a public client that authenticates with a static client ID and no client secret. `NONE` applies only when `TYPE = OAUTH2`. |
| OAUTH\_ALLOWED\_SCOPES | LIST | No | None | List of OAuth scopes to request from the external service provider. Required by some providers to grant access to specific APIs or resources. |
| OAUTH\_REFRESH\_TOKEN\_VALIDITY | INTEGER | No | 0 (never expires) | Validity period, in seconds, of the OAuth refresh token issued by the external MCP service. When set, the value must be at least 3600 (one hour). The default of 0 is treated as a refresh token that never expires, so set this value explicitly to ensure users re-authenticate periodically. |

Expand

Show lessSee more

## Add MCP connectors to the Cortex Agent

After MCP server object creation, the agent developer references it in the Cortex Agent config. MCP Connectors are available in the Agent Admin UI, where developers can browse and select from MCP connectors configured at the account level. You can also use SQL or API to add MCP connectors to your agents.

Snowsight UISQLREST API

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **Agents**.
3. Select the agent name from the list of agents.
4. Select **MCP Connectors**.
5. From the list of **Available Connectors**, select the connector you want to add.
6. Review the connector details and select **Add to agent**.

Copy code

```
ALTER AGENT [ IF EXISTS ] <name> MODIFY LIVE VERSION SET SPECIFICATION $$
    <previous_spec>
    mcp_servers:
      - server_spec:
         name: "db.schema.mcp_server1"
      - server_spec:
         name: "db.schema.mcp_server2"
$$;
```

Agent developers add external MCP servers to a Cortex Agent’s specification using the Agent object REST API:

Copy code

```
PUT /api/v2/databases/{database}/schemas/{schema}/agents/{name}

{
    "comment": "An agent to answer questions about all my data",
    "profile": {
        "display_name": "My Agent"
    },
    "models": {
        "orchestration": "claude-sonnet-4-6"
    },
    "mcp_servers": [
        {"server_spec": "prod_db.integrations.jira_mcp_server"},
        {"server_spec": "prod_db.integrations.github_mcp_server"}
    ]
}
```

Cortex Agents that reference these MCP servers can access tools provided by the provider. For example, with Atlassian, tools include creating Jira issues, commenting on issues, creating Confluence pages, and updating existing pages.

When the agent is invoked, it retrieves the tool list from each MCP server and includes those tools in its orchestration. The agent selects and invokes tools based on the user’s query and the tool descriptions provided by the MCP server.

## Use MCP connectors in Snowflake CoWork

Snowflake CoWork users connect to external MCP servers through the Snowflake CoWork interface:

1. Navigate to the Snowflake CoWork interface by following the instructions in [Access the agent](/user-guide/snowflake-cortex/snowflake-cowork/deploy-agents#label-snowflake-intelligence-use-agent).
2. Open the sources panel and select **Connectors**.
3. Select **Connect** next to the connector of choice. You can also select **Manage Connections** and then select **Connect**.
4. The user is redirected to the third-party service’s authentication page to approve the connection.
5. After authentication, the connector appears as **Connected** in the sources list. You can now interact
   with the Agent to get information from the external MCP server.

To disconnect the server, the user can complete the following:

1. Select **Manage Connections**.
2. Select **MCP Server** and then select **Disconnect**.

Users can connect and disconnect connectors in the sources dropdown to include or exclude them from
the agent’s orchestration. Connectors that aren’t in the **Connected** state aren’t included in orchestration.

When a user’s authentication token expires, Snowflake CoWork prompts the user to re-authenticate.

## Use MCP connectors in Agent:run API

The Agent:run API connects to MCP servers through the client interface. Use the following functions to authenticate users with the third-party service:

- Function to start OAuth flow:

  Copy code

  ```
  -- Returns authorization URI to authenticate through the third-party service
  SELECT SYSTEM$START_USER_OAUTH_FLOW('<API_INTEGRATION_NAME>');
  ```
- Function to finish OAuth flow:

  Copy code

  ```
  SYSTEM$FINISH_OAUTH_FLOW( '<query_string>' )
  ```

`SYSTEM$START_USER_OAUTH_FLOW` returns an authorization URL for API integrations with `API_PROVIDER = EXTERNAL_MCP`. Open the URL in a browser to complete consent, then run `SYSTEM$FINISH_OAUTH_FLOW` in the same session with the query string from the redirect URL. For more information about `SYSTEM$FINISH_OAUTH_FLOW`, see [SYSTEM$FINISH\_OAUTH\_FLOW](/sql-reference/functions/system_finish_oauth_flow).

## Manage MCP servers

### List and describe MCP servers

List all external MCP servers at different scopes:

Copy code

```
-- List all MCP servers in the account
SHOW EXTERNAL MCP SERVERS IN ACCOUNT;

-- List MCP servers in a specific database or schema
SHOW EXTERNAL MCP SERVERS IN DATABASE prod_db;
SHOW EXTERNAL MCP SERVERS IN SCHEMA prod_db.integrations;
```

The output includes the server name, database, schema, owner, type (pre-built or custom), MCP server URL,
state (enabled or disabled), and associated API integration.

To view the full configuration of a specific server:

Copy code

```
DESCRIBE EXTERNAL MCP SERVER mycompany_mcp_server;
```

### Disable and enable MCP servers

Disable an MCP server by altering its underlying API integration. Disabling immediately invalidates all
user tokens and triggers a call to the MCP server’s revocation endpoint. Secrets aren’t deleted when you
disable an integration. They expire naturally if the integration remains disabled long enough.

Copy code

```
-- Disable the MCP server
ALTER API INTEGRATION mycompany_mcp_integration SET ENABLED = FALSE;

-- Re-enable the MCP server
ALTER API INTEGRATION mycompany_mcp_integration SET ENABLED = TRUE;
```

Warning

When you disable an API integration, all agents using that MCP server lose access to its tools immediately.
Snowflake CoWork surfaces an alert to users when a connector is disabled. Re-enabling requires users
to re-authenticate as if connecting for the first time.

You can’t create a new MCP server that references a disabled API integration. During agent execution,
Snowflake checks both the MCP server and API integration states and only uses enabled servers.

### Drop an MCP server

Drop the MCP server first, then drop the API integration. Only roles with the OWNERSHIP privilege can issue drops.

Copy code

```
-- Drop the MCP server
DROP EXTERNAL MCP SERVER mycompany_mcp_server;

-- Drop the API integration (permanently deletes OAuth configuration and secrets)
DROP API INTEGRATION mycompany_mcp_integration;
```

Warning

Dropping an API integration permanently deletes all OAuth configuration and stored secrets.
Ensure no agents are currently using the MCP server before dropping it. You must recreate both
objects from scratch if you need them again.

## Key considerations and best practices

- **Custom MCP servers:** Use custom servers when connecting to MCP endpoints not in the available MCP
  connectors list. Snowflake supports user authentication types for Atlassian, GitHub, Glean, Linear, and Salesforce in the API integration.
- **Least-privilege access:** Grant only the minimum required privileges for each role. Access to an MCP
  server doesn’t automatically grant access to its tools. You must grant permissions separately for each tool.
- **OAuth authentication:** Snowflake supports only OAuth for MCP server connections.
- **Refresh token validity:** When using `TYPE = OAUTH2`, set `OAUTH_REFRESH_TOKEN_VALIDITY`
  (in seconds, minimum `3600`) in the API integration’s `API_USER_AUTHENTICATION` block.
  The default of `0` is treated as a refresh token that never expires, so setting an explicit
  value ensures users periodically re-authenticate to the external MCP service.
- **Disabling or dropping:** Disabling an API integration preserves its configuration, but immediately
  invalidates all user tokens and blocks tool invocations. Dropping an API integration permanently deletes
  it along with all stored secrets. Disable the integration when performing maintenance. Drop the integration when decommissioning.
- **Hostname formatting:** Use hyphens (`-`) instead of underscores (`_`) in hostnames when configuring
  MCP server connections. Hostnames containing underscores cause connection issues.

## Monitoring

When an agent invokes an MCP connector tool, Snowflake records the call in `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS` as part of the agent trace. You can review MCP connector spans in the agent **Observability** tab in Snowsight or query with [GET\_AI\_OBSERVABILITY\_EVENTS](/sql-reference/functions/get_ai_observability_events-snowflake-local). See [Monitor Cortex Agents](/user-guide/snowflake-cortex/cortex-agents-monitor).

Tool names, latency, and token usage are visible to roles with `MONITOR` on the agent. Full MCP tool inputs and outputs may be redacted unless the role also has **READ UNREDACTED AI OBSERVABILITY EVENTS TABLE**. For details, see [Account Privilege READ UNREDACTED AI OBSERVABILITY EVENTS TABLE](/release-notes/bcr-bundles/un-bundled/bcr-read-unredacted-ai-observability-events).

## Limitations

The following limitations apply to MCP connectors:

- **MCP protocol scope:** External MCP servers support tool capabilities only. Resources, prompts, roots,
  notifications, version negotiations, lifecycle phases, and sampling are not supported.
- **Disabled integrations:** You can’t create an MCP server that references a disabled API integration.
- **Hostname format:** Hostnames must use hyphens, not underscores.
