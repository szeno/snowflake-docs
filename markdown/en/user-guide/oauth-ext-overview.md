# External OAuth overview

This topic teaches you how to configure External OAuth servers that use OAuth 2.0 for accessing Snowflake.

External OAuth integrates the customer’s OAuth 2.0 server to provide a seamless SSO experience, enabling external client access to
Snowflake.

Snowflake supports the following external authorization servers, custom clients, and partner applications:

- [Okta](/user-guide/oauth-okta)
- [Microsoft Entra ID](/user-guide/oauth-azure)
- [Ping Identity PingFederate](/user-guide/oauth-pingfed)
- [External OAuth Custom Clients](/user-guide/oauth-ext-custom)
- [Microsoft Power BI](/user-guide/oauth-powerbi)
- [Sigma](/user-guide/oauth-ext-partner)

After configuring your organization’s External OAuth server, which includes any necessary [OAuth 2.0 Scopes](https://oauth.net/2/scope/)
mapping to Snowflake roles, the user can connect to Snowflake securely and programmatically without having to enter any additional
authentication or authorization factors or methods. The user’s access to Snowflake data is dependent on both their role and the role being
integrated into the access token for the session. For more information, refer to [Scopes](#scopes) (in this topic).

## Use cases and benefits

1. Snowflake delegates the token issuance to a dedicated authorization server to ensure that the OAuth Client and user properly
   authenticate. The result is centralized management of tokens issued to Snowflake.
2. Customers can integrate their policies for authentication (for example, multi-factor, subnet, biometric) and authorization
   (for example, no approval, manager approval required) into the authorization server. The result is greater security leading to more robust data
   protection by issuing challenges to the user. If the user doesn’t pass the policy challenges, the Snowflake session is not
   instantiated, and access to Snowflake data does not occur.
3. For programmatic clients that can access Snowflake and users that only initiate their Snowflake sessions through External OAuth, no
   additional authentication configuration (that is, set a password) is necessary in Snowflake. The result is that service accounts or users
   used exclusively for programmatic access will only ever be able to use Snowflake data when going through the External OAuth configured
   service.
4. Clients can authenticate to Snowflake without browser access, allowing ease of integration with the External OAuth server.
5. Snowflake’s integration with External OAuth servers is cloud-agnostic.
   - It does not matter whether the authorization server exists in a cloud provider’s cloud or if the authorization server is on-premises.
     The result is that customers have many options in terms of configuring the authorization server to interact with Snowflake.

## General workflow

For each of the supported identity providers, the workflow for OAuth relating to External OAuth authorization servers can be summarized as
follows. Note that the first step only occurs once and the remaining steps occur with each attempt to access Snowflake data.

![workflow overview](/static/images/oauth-third-party.png)

1. Configure your External OAuth authorization server in your environment and the security integration in Snowflake to establish a trust.
2. A user attempts to access Snowflake data through their business intelligence application, and the application attempts to verify the
   user.
3. On verification, the authorization server sends a JSON Web Token (that is, an OAuth token) to the client application.
4. The Snowflake driver passes a connection string to Snowflake with the OAuth token.
5. Snowflake validates the OAuth token.
6. Snowflake performs a user lookup.
7. On verification, Snowflake instantiates a session for the user to access data in Snowflake based on their role.

## MCP server integration

External OAuth security integrations can be bound to [Snowflake MCP servers](/user-guide/snowflake-cortex/cortex-agents-mcp) to let
MCP clients (such as Claude, Cursor, and other AI tools) authenticate against your organization’s existing identity provider (IdP) instead of
Snowflake OAuth.

When an MCP server has an External OAuth integration bound to it, the server advertises your IdP’s issuer URL in its
Protected Resource Metadata (RFC 9728). MCP clients that support RFC 9728 discovery automatically discover the correct authorization
server and obtain tokens from your IdP rather than from Snowflake.

### How it works

Set two hierarchical parameters that bind an External OAuth integration to MCP servers:

- `OAUTH_AUTHORIZATION_SERVER`: The name of an existing External OAuth security integration.
- `OAUTH_SCOPES_SUPPORTED`: A comma-separated list of OAuth scopes the MCP server advertises (optional). For accepted values, see [OAUTH\_SCOPES\_SUPPORTED](/sql-reference/parameters#label-oauth-scopes-supported).

Both parameters follow Snowflake’s standard account/database/schema lineage. A single configuration can cover all MCP servers in an
account, a database, or a specific schema. MCP servers inherit the OAuth binding from the enclosing account, database, or schema.

### Example

The following example binds an Okta-based External OAuth integration to all MCP servers in a database:

Copy code

```
CREATE SECURITY INTEGRATION external_oauth_okta
  TYPE = EXTERNAL_OAUTH
  ENABLED = TRUE
  EXTERNAL_OAUTH_TYPE = OKTA
  EXTERNAL_OAUTH_ISSUER = '<OKTA_ISSUER>'
  EXTERNAL_OAUTH_JWS_KEYS_URL = '<OKTA_JWS_KEY_ENDPOINT>'
  EXTERNAL_OAUTH_AUDIENCE_LIST = ('https://<orgname>-<account_name>.snowflakecomputing.com')
  EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM = 'sub'
  EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = 'login_name';

ALTER DATABASE analytics_db SET OAUTH_AUTHORIZATION_SERVER = external_oauth_okta;

ALTER DATABASE analytics_db SET OAUTH_SCOPES_SUPPORTED = 'session:role:ANALYST,session:role:DATA_SCIENTIST';
```

After this configuration, all MCP servers created in `analytics_db` advertise the Okta issuer from `external_oauth_okta` in
`authorization_servers`.

For the full workflow, parameter inheritance details, and failure modes, see
[Configure External OAuth authentication for MCP servers](/user-guide/snowflake-cortex/cortex-agents-mcp#label-cortex-mcp-external-oauth).

## Scopes

The scope parameter in the authorization server limits the operations and roles permitted by the access token and what the user can access
after instantiating a Snowflake session.

The ACCOUNTADMIN, GLOBALORGADMIN, ORGADMIN, and SECURITYADMIN roles are blocked by default. If it is necessary to use one or more of these roles,
use the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command to set the [EXTERNAL\_OAUTH\_ADD\_PRIVILEGED\_ROLES\_TO\_BLOCKED\_LIST](/sql-reference/parameters#label-external-oauth-add-privileged-roles-to-blocked-list) account
parameter to FALSE.

- For Okta, PingFederate, and Custom, use the role scope pattern in the following table.
- For Microsoft Entra ID, refer to [Determine the OAuth flow in Microsoft Entra ID](/user-guide/oauth-azure#label-ext-oauth-azure-flow).
- If you do not want to manage Snowflake roles in your External OAuth server, pass the static value of SESSION:ROLE-ANY in the scope
  attribute of the token.

The following table summarizes External OAuth scopes. Note that
if you do not define a scope, the connection attempt to Snowflake will fail.

| Scope/Role Connection Parameter | Description |
| --- | --- |
| `session:role-any` | Maps to the ANY role in Snowflake.  Use this scope if the user’s default role in Snowflake is desirable.  The `external_oauth_any_role_mode` security integration parameter must be configured in order to enable ANY role for a given External OAuth Provider. For configuration details, refer to the ANY role section in [Okta](/user-guide/oauth-okta#label-any-role-okta), [Microsoft Entra ID](/user-guide/oauth-azure#label-any-role-aad), [PingFederate](/user-guide/oauth-pingfed#label-any-role-pingfed), or [Custom](/user-guide/oauth-ext-custom#label-any-role-ext-oauth-custom).  Note that with a [Power BI to Snowflake integration](/user-guide/oauth-powerbi), a Power BI user cannot switch roles using this scope. |
| `session:role:custom_role` | Maps to a custom Snowflake role. For example, if your custom role is ANALYST, your scope is `session:role:analyst`. |
| `session:role:public` | Maps to the PUBLIC Snowflake role. |

Expand

Show lessSee more

### Using secondary roles with External OAuth

Snowflake supports using [secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement) with External OAuth.

Snowflake OAuth does not support in-session role switching to secondary roles.

For more information, refer to:

- [Secondary roles with Okta](/user-guide/oauth-okta#label-secondary-roles-okta)
- [Secondary roles with Microsoft Entra ID](/user-guide/oauth-azure#label-secondary-roles-azure)
- [Secondary roles with PingFederate](/user-guide/oauth-pingfed#label-secondary-roles-pingfed)
- [Secondary roles with Custom Clients](/user-guide/oauth-ext-custom#label-secondary-roles-ext-custom)
- [Using secondary roles with Power BI SSO to Snowflake](/user-guide/oauth-powerbi#label-secondary-roles-powerbi)

## Configuring External OAuth support

Snowflake supports the use of partner applications and custom clients that support External OAuth.

Refer to the list below if you need to configure partner applications or custom clients:

- [Configuring partner applications](/user-guide/oauth-ext-partner).
- [Configuring custom clients configured by your organization](/user-guide/oauth-ext-custom).

## Restricting network traffic for External OAuth

You can associate a [network policy](/user-guide/network-policies) with the External OAuth security integration to restrict network traffic from the client to Snowflake as the resource server. This network policy governs login requests and queries against Snowflake.

When you associate a network policy with the security integration, it overrides network policies associated with the user or the account. For more information, see [Network policy precedence](/user-guide/network-policies#label-network-policy-precedence).

To associate a network policy with the External OAuth security integration, set the NETWORK\_POLICY parameter when creating or updating the integration. For example:

Copy code

```
CREATE SECURITY INTEGRATION external_oauth_azure_1
  TYPE = external_oauth
  ENABLED = true
  EXTERNAL_OAUTH_TYPE = azure
  EXTERNAL_OAUTH_ISSUER = '<AZURE_AD_ISSUER>'
  EXTERNAL_OAUTH_JWS_KEYS_URL = '<AZURE_AD_JWS_KEY_ENDPOINT>'
  EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM = 'upn'
  EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = 'login_name'
  NETWORK_POLICY = 'allow_private_ip_only';
```

## Error codes

Refer to the table below for descriptions of error codes associated with External OAuth:

| Error Code | Error | Description |
| --- | --- | --- |
| 390318 | OAUTH\_ACCESS\_TOKEN\_EXPIRED | OAuth access token expired. {0} |
| 390144 | JWT\_TOKEN\_INVALID | JWT token is invalid. |

Expand

Show lessSee more

## Troubleshooting

- Use the [SYSTEM$VERIFY\_EXTERNAL\_OAUTH\_TOKEN](/sql-reference/functions/system_verify_ext_oauth_token) function to determine whether your External OAuth access token is
  valid or needs to be regenerated.
- If you encounter an error message associated with a failed External OAuth login attempt, and the error message has a UUID, you can
  ask an
  administrator that has a MONITOR privilege assigned to their role to use the UUID from the error message to get a more detailed
  description of the error using the [SYSTEM$GET\_LOGIN\_FAILURE\_DETAILS](/sql-reference/functions/system_get_login_failure_details#label-system-get-login-failure-details-example)
  function.
