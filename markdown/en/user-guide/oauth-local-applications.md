# Using Snowflake OAuth for local applications

This topic describes the preferred authentication method for local applications, including desktop applications and local scripts.

[Snowflake OAuth](/user-guide/oauth-snowflake-overview) is implemented by creating a *security integration* that defines an interface
between Snowflake as the OAuth authorization server and the application that is authenticating on behalf of a user by using the OAuth
authorization code flow. Snowflake OAuth is a strong authentication option because the application doesn’t have to store or manage secrets,
and you don’t have to configure a third-party identity provider like External OAuth.

To simplify how a local application uses Snowflake OAuth to authenticate, your account has a built-in
security integration called `SNOWFLAKE$LOCAL_APPLICATION`. Because the security integration already exists, if a local application
uses a Snowflake client like the Python driver or Snowflake CLI, the application can authenticate to Snowflake by setting a property or
parameter of the client. No further set up is required. The built-in integration also simplifies the setup for local applications that call
the OAuth endpoints directly rather than use a Snowflake client.

An administrator can change the parameters of the `SNOWFLAKE$LOCAL_APPLICATION` integration to adjust its behavior, such as specifying
how long OAuth access tokens and refresh tokens are valid.

Snowflake OAuth for local applications has the following additional advantages:

- Unlike user-created Snowflake OAuth integrations, in-role session switching *is* supported.
- It is a straightforward replacement for applications that are currently using passwords only to authenticate users. Snowflake is
  [deprecating single-factor passwords](/user-guide/security-mfa-rollout), so Snowflake OAuth for local applications provides a path to
  using a more secure form of authentication without requiring a lot of set up.

Note

The `SNOWFLAKE$LOCAL_APPLICATION` security integration is being rolled out slowly to all accounts. To determine if this built-in
integration exists in your account, run the following command:

Copy code

```
SHOW SECURITY INTEGRATIONS LIKE 'SNOWFLAKE$LOCAL_APPLICATION';
```

## Configuring the Snowflake OAuth integration

The built-in `SNOWFLAKE$LOCAL_APPLICATION` security integration is owned by the system but can be configured by security
administrators (that is, users granted the SECURITYADMIN system role).

Security administrators can configure the following parameters of the security integration:

| Parameter | Description |
| --- | --- |
| `ENABLED` | Controls whether the integration is enabled. If the integration is disabled, local applications must use a different authentication method. |
| `OAUTH_ISSUE_REFRESH_TOKENS` | Controls whether the authorization server issues refresh tokens. |
| `OAUTH_ACCESS_TOKEN_VALIDITY` | Sets the validity duration of access tokens, in seconds. Valid values: `60` (1 minute) to `3600` (1 hour). Default: `600` (10 minutes). |
| `OAUTH_REFRESH_TOKEN_VALIDITY` | Sets the validity duration of refresh tokens, in seconds. |
| `OAUTH_SINGLE_USE_REFRESH_TOKENS_REQUIRED` | Controls whether the authorization server issues single-use refresh tokens. |

Expand

Show lessSee more

For example, to modify the built-in security integration so that the authorization server starts issuing single-use refresh tokens, run the
following commands:

Copy code

```
USE ROLE SECURITYADMIN;

ALTER SECURITY INTEGRATION SNOWFLAKE$LOCAL_APPLICATION
  SET OAUTH_SINGLE_USE_REFRESH_TOKENS_REQUIRED = TRUE;
```

For more information about setting these parameters, see [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-oauth-snowflake).

### Controlling the login frequency

When `OAUTH_ISSUE_REFRESH_TOKENS = TRUE`, applications can use refresh tokens to obtain new access tokens without prompting users to log
in again. Users only need to re-authenticate when the refresh token expires after the duration that is specified by the
`OAUTH_REFRESH_TOKEN_VALIDITY` parameter.

Access tokens are short-lived. By default, they expire after 600 seconds (10 minutes). Use `OAUTH_ACCESS_TOKEN_VALIDITY` to set the
validity anywhere between 60 seconds (1 minute) and 3600 seconds (1 hour). For example:

Copy code

```
ALTER SECURITY INTEGRATION SNOWFLAKE$LOCAL_APPLICATION
  SET OAUTH_ACCESS_TOKEN_VALIDITY = 3600;
```

## Setting up a local application to use Snowflake OAuth

This section provides the details a developer needs to configure a local application to authenticate with Snowflake OAuth. The following
types of local applications can authenticate by using the built-in integration:

- A local application that uses a Snowflake client like the Python driver or Snowflake CLI. See [Applications that use a Snowflake client](#label-snowflake-oauth-local-app-client).
- A local application that makes REST requests to the OAuth authorization endpoint and token endpoint directly, without the use of a
  Snowflake client. See [Applications that call OAuth endpoints directly](#label-snowflake-oauth-local-app-direct).

### Applications that use a Snowflake client

When a local application uses a Snowflake client like the Snowflake ODBC driver, it can authenticate with Snowflake OAuth by setting the
`authenticator` connection option to `oauth_authorization_code`. Additional development work isn’t required.

#### Prerequisite

With Snowflake OAuth for local applications, the Snowflake client must be able to open
the user’s web browser. For this reason, both the Snowflake client and the local application that uses it must be installed on the
user’s computer. Snowflake OAuth for local applications doesn’t work if the Snowflake client is used by code that runs on a server.

#### Supported clients

Your local application can use the following Snowflake clients to authenticate with Snowflake OAuth for local applications:

| Client | Minimum required version | Required configuration |
| --- | --- | --- |
| .NET | v4.8.0 | Set `authenticator=oauth_authorization_code` in the connection string. |
| Go | v1.14.1 | Set `authenticator=oauth_authorization_code` in the connection configuration. |
| JDBC | v3.24.1 | Set ``` authenticator=``oauth_authorization_code ``` in the connection string for the driver. |
| Node.js | v2.1.0 | Set `authenticator: 'oauth_authorization_code'` in the connection options. |
| ODBC | v3.9.0 | - For Linux and macOS, set `authenticator=oauth_authorization_code` in the `odbc.ini` file. - For Windows, in the ODBC Data Source Administrator tool, edit the DSN for Snowflake and set Authenticator to   `oauth_authorization_code`. |
| Python | v3.16.0 | Pass `AUTHENTICATOR=OAUTH_AUTHORIZATION_CODE` to the `snowflake.connector.connect()` function. |
| Snowflake CLI | v3.8.1 | Add the `authenticator = "OAUTH_AUTHORIZATION_CODE"` option to the connection definition. |
| SnowSQL | v1.4.0 | Add the `authenticator = "OAUTH_AUTHORIZATION_CODE"` parameter in the configuration file. |

Expand

Show lessSee more

### Applications that call OAuth endpoints directly

Your local application can use Snowflake OAuth by making requests to the authorization endpoint and token endpoint of Snowflake as the
authorization server. You don’t need to use a Snowflake client. The application sends a request to Snowflake’s authorization endpoint to
authenticate the user and receive an authorization code, and then sends a request to the token endpoint to exchange that code for an access
token.

For more information about making REST requests to Snowflake’s authorization and token endpoints, see [Call the OAuth endpoints](/user-guide/oauth-custom#label-snowflake-oauth-endpoints).

#### Request requirements

Your application’s REST requests to the authorization and token endpoints must conform to the following requirements:

- The redirect URL in the request to the authorization endpoint must be `http://127.0.0.1[:port][/path]`. That is, your local application
  must be listening on a loopback address for the authorization code that is returned by Snowflake as the authorization server.
- Requests to the authorization and token endpoints must implement Proof Key for Code Exchange (PKCE). For more information, see
  [Proof key for code exchange](/user-guide/oauth-custom#label-proof-key-for-code-exchange).
- When calling the token endpoint to exchange an authorization code for an access token, the application must provide the proper client ID
  and client secret. This requirement varies slightly depending on how you choose to send these client credentials:
  - If you send client credentials in the request header, the client ID must be `LOCAL_APPLICATION` and the client secret must be
    `LOCAL_APPLICATION`.
  - If you send client credentials in the POST body, the client ID must be `LOCAL_APPLICATION`. The built-in integration configures
    the local application as a public client, so the client secret isn’t necessary if you provide the client ID as
    `client_id=LOCAL_APPLICATION` in the POST body.

## Network policies for local applications

Network policy enforcement for the built-in `SNOWFLAKE$LOCAL_APPLICATION` integration differs from other Snowflake OAuth
integrations. When a local application sends a token request, the user-level network policy is enforced
with highest precedence, followed by the integration-level network policy, then the account-level network policy.

For general information about restricting network traffic for Snowflake OAuth, see [Restricting network traffic for Snowflake OAuth](/user-guide/oauth-snowflake-overview#label-snow-oauth-network-policies).

## Usage notes

Every account has a `SNOWFLAKE$LOCAL_APPLICATION` integration, so this integration isn’t replicated. The
configuration of the built-in integration is unique to each account.
