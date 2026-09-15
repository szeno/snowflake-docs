# Snowflake OAuth overview

Snowflake OAuth uses Snowflake’s built-in OAuth service to provide OAuth-based authentication.

This topic describes Snowflake OAuth and how to use Snowflake as an OAuth resource and authorization server for accessing Snowflake data
securely.

Snowflake OAuth uses Snowflake’s built-in OAuth service and supports the following applications:

- [Tableau Desktop, Tableau Cloud](/user-guide/oauth-partner)
- [Looker](/user-guide/oauth-partner)
- [Alation](/user-guide/oauth-partner)
- [ThoughtSpot](/user-guide/oauth-partner)
- [Custom clients configured by your organization](/user-guide/oauth-custom)

## Snowflake OAuth authorization flow

The OAuth authorization flow is as follows:

![Snowflake OAuth workflow](/static/images/oauth2-workflow.png)

1. In the client, the user attempts to connect to Snowflake using OAuth.

   The application sends an authorization request to the Snowflake authorization server, which in turn displays an authorization screen
   that asks the user to authorize access.
2. The user submits the Snowflake login name and password, and is in turn presented with a consent screen to allow the client access to
   Snowflake using a specific role in a user session (for example, SYSADMIN or CUSTOM\_ROLE1).

   The user submits consent to use the specific role in a session.

   The Snowflake authorization server sends an authorization code back to the client.
3. The client sends the authorization code back to the Snowflake authorization server to request an access token and, optionally, a refresh
   token that allows the client to obtain new access tokens.

   The Snowflake authorization server accepts the authorization code and provides the client with an access token specific to the user
   resources in the Snowflake resource server. Based on the settings in the authorization request, the authorization server issues a
   refresh token to obtain new access tokens tied to the specific resource.
4. The client sends the access token to the Snowflake resource server.

   The resource server recognizes the valid access token and creates a user session with the authorized role. The client now has access to
   the Snowflake resources limited by the role specified by the access token.

   By default, Snowflake prevents the ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, and SECURITYADMIN roles from authenticating. To allow these
   privileged roles to authenticate, use the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command to set the [OAUTH\_ADD\_PRIVILEGED\_ROLES\_TO\_BLOCKED\_LIST](/sql-reference/parameters#label-oauth-add-privileged-roles-to-blocked-list) account parameter to `FALSE`.

Access tokens have a short life: typically 10 minutes. When the access token expires, the client can send a refresh token to obtain new
access tokens. A refresh token is sent to the Snowflake authorization server to request a new access token each time the current access
token expires (Steps 3-6). If the integration is configured to prevent sending refresh tokens, the user must repeat the above steps to
re-authorize the client. If you want to limit the risk posed by long-lived tokens in your Snowflake OAuth flow, you can use single-use
refresh tokens.

## Single-use refresh tokens

You can use single-use refresh tokens to mitigate theft or reuse of refresh tokens. For more information, see [Single-use refresh tokens for Snowflake OAuth security integrations](/user-guide/single-use-refresh-tokens).

## Local applications

Snowflake provides a simplified way to set up local applications — that is, desktop applications — to use Snowflake OAuth to
authenticate. The application can authenticate by setting a single connection option; no additional setup is required. For more information,
see [Using Snowflake OAuth for local applications](/user-guide/oauth-local-applications).

## Partner applications

To configure support, refer to [Configure Snowflake OAuth for partner applications](/user-guide/oauth-partner).

To learn about using OAuth without traversing the public internet, refer to [Using Snowflake OAuth with PrivateLink and SaaS clients](#label-oauth-private-connectivity).

## Custom clients

Snowflake supports custom clients configured by your organization. To configure support, refer to [Configure Snowflake OAuth for custom clients](/user-guide/oauth-custom).

## Restricting network traffic for Snowflake OAuth

You can associate a [network policy](/user-guide/network-policies) with the Snowflake OAuth security integration to restrict network
traffic when the client requests a token from Snowflake as the authorization server. This network policy also governs network traffic when
the client queries Snowflake as the resource server.

To associate a network policy with the Snowflake OAuth security integration, set the NETWORK\_POLICY parameter when creating or updating the integration. For example:

Copy code

```
CREATE SECURITY INTEGRATION td_oauth_int2
  TYPE = oauth
  ENABLED = true
  OAUTH_CLIENT = tableau_desktop
  OAUTH_REFRESH_TOKEN_VALIDITY = 36000
  BLOCKED_ROLES_LIST = ('SYSADMIN')
  NETWORK_POLICY = 'allow_private_ip_only';
```

A network policy associated with the Snowflake OAuth security integration does not affect network traffic between the user and Snowflake as
the authorization server. When the user authenticates by using a browser, the network traffic is restricted by a network policy associated
with the user.

The following diagram shows which network policy governs network traffic from the client and user.

![Snowflake OAuth workflow](/static/images/oauth-snowflake-network-policy.png)

1. Network policy associated with the user governs. If no user-level network policy exists, the account-level policy governs.
2. Network policy associated with the security integration governs. If no integration-level network policy exists, the account-level
   policy governs.

### Network policy for local applications

For the built-in `SNOWFLAKE$LOCAL_APPLICATION` integration, the user-level network policy is also considered for token requests
because the local application runs in the user’s network environment due to the lack of a separate
authorization server. The precedence for these requests is: user, then integration, then account.

For more information about local applications, see [Using Snowflake OAuth for local applications](/user-guide/oauth-local-applications).

## Using Snowflake OAuth with PrivateLink and SaaS clients

When using Snowflake OAuth with a SaaS-hosted client such as Claude.ai or a ChatGPT connector,
the authorization code flow runs across two different network contexts:

- The **authorization request** is made from the user’s browser. The browser runs on the user’s
  network and can reach a PrivateLink account URL to complete the authorization step.
- The **token request** is a server-to-server call made from the SaaS vendor’s backend directly
  to Snowflake. Because that server is on the public internet, it can’t resolve a PrivateLink
  hostname. The token endpoint must therefore be a public Snowflake URL.

When configuring a SaaS MCP client, use the **public** Snowflake account URL — not a
PrivateLink URL. If you want Snowflake to redirect the user’s browser to the PrivateLink
authorization endpoint during the authorization step, enable
`USE_PRIVATELINK_FOR_AUTHORIZATION_ENDPOINT = TRUE` on the OAuth security integration.

Note

This constraint applies to SaaS clients only. Clients that run on the user’s machine, such as
Claude Desktop or Cursor, connect from the user’s network and can use a PrivateLink URL
directly.

For information about setting `USE_PRIVATELINK_FOR_AUTHORIZATION_ENDPOINT`, see
[CREATE SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/create-security-integration-oauth-snowflake) and
[ALTER SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/alter-security-integration-oauth-snowflake).

## Error codes

Refer to the table below for descriptions of error codes associated with Snowflake OAuth:

| Error Code | Error | Description |
| --- | --- | --- |
| 390302 | OAUTH\_CONSENT\_INVALID | Issue generating or validating consent for a given user. |
| 390303 | OAUTH\_ACCESS\_TOKEN\_INVALID | Access token provided when attempting to create a Snowflake session is expired or invalid. |
| 390304 | OAUTH\_AUTHORIZE\_INVALID\_RESPONSE\_TYPE | Invalid `response_type` was provided as a parameter to the authorization endpoint (it should most likely be `code`). |
| 390305 | OAUTH\_AUTHORIZE\_INVALID\_STATE\_LENGTH | State parameter provided as a parameter to the authorization endpoint exceeds 2048 characters. |
| 390306 | OAUTH\_AUTHORIZE\_INVALID\_CLIENT\_ID | Integration associated with a provided `client_id` does not exist. |
| 390307 | OAUTH\_AUTHORIZE\_INVALID\_REDIRECT\_URI | `redirect_uri` given as a parameter to the authorization endpoint does not match the `redirect_uri` of the integration associated with the provided `client_id` or the `redirect_uri` is not properly formatted. |
| 390308 | OAUTH\_AUTHORIZE\_INVALID\_SCOPE | Either the scope requested is not a valid scope, or the scopes requested cannot fully be granted to the user. |
| 390309 | OAUTH\_USERNAMES\_MISMATCH | The user you were trying to authenticate as differs from the user tied to the access token. |
| 390311 | OAUTH\_AUTHORIZE\_INVALID\_CODE\_CHALLENGE\_PARAMS | Either the code challenge or code challenge method is missing, invalid, or not supported. |

Expand

Show lessSee more

Additionally, the following errors are taken from the RFC and are returned in the JSON blob generated during an unsuccessful token request
or exchange:

| Error | Description |
| --- | --- |
| invalid\_client | There was a failure relating to client authentication, such as the client being unknown, a client secret mismatch, or incorrect `client_secret_basic` encoding. A network policy that blocks the client’s IP address can also return this error. For supported methods and encoding, see [Client authentication](/user-guide/oauth-custom#label-oauth-client-authentication). |
| invalid\_grant | The provided authorization grant or refresh token is invalid, expired, revoked, does not match the redirection URI used in the authorization request, or was issued to another client. |
| unsupported\_grant\_type | A grant type was provided that Snowflake currently does not support (“refresh\_token” and “authorization\_code” are the only two supported grant types at the moment). |
| invalid\_request | The request was malformed or could not be processed. |

Expand

Show lessSee more
