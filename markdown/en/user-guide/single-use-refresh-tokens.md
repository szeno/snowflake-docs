# Single-use refresh tokens for Snowflake OAuth security integrations

This topic describes how to enable single-use refresh tokens for [Snowflake OAuth security integrations](/user-guide/oauth-snowflake-overview).

Single-use refresh tokens are a feature that you can enable to prevent stolen refresh tokens from being reused in your Snowflake account.
When you enable single-use refresh tokens, the following changes occur to the behavior of the refresh token grant flow:

- You can only use a refresh token one time during the 90 days that the refresh token is valid.
- After you use a refresh token, the refresh token becomes invalid.
- The refresh token grant flow returns a new refresh token and a new access token, instead of only a new access token. The new refresh token
  will have the same expiration time as specified by OAUTH\_REFRESH\_TOKEN\_VALIDITY when the [integration was created](/sql-reference/sql/create-security-integration-oauth-snowflake)
  (or the default system validity period, if not specified).
- After you get a new refresh token, all previous refresh tokens and access tokens become invalid.

## Benefits of single-use refresh tokens

Single-use refresh tokens offer the following security benefits:

- **Reduced effective token lifetime**: When a legitimate application uses a refresh token, any stolen copies of the refresh token become invalidated. This single-use behavior
  makes distributing stolen tokens and using stolen tokens in timed attacks more difficult.

  For example, if your application uses the refresh token grant flow one time every 10 minutes, then a malicious actor who steals the
  refresh token can only use the stolen token within 10 minutes, or before the application gets a new refresh token, even if the token is
  valid for 90 days.
- **Intrusion detection**: You cannot reuse a refresh token. When a refresh token is reused, all previous refresh tokens and access tokens
  become invalid.

  For example, if a malicious actor steals a single-use refresh token and attempts to reuse the token, then the attempt to reuse the
  single-use refresh token invalidates all previous refresh tokens and access tokens, which exposes the malicious use of a refresh token.

## Enabling single-use refresh tokens

You can enable refresh token rotation when you exchange an authorization code for an access token and a refresh token using an authorization
code grant flow.

You can enable single-use refresh tokens by using any of the following methods:

- [Use a request parameter in the body of an HTTP request](#label-enable-refresh-token-rotation-in-an-http-request)
- [Set a property in a Snowflake OAuth security integration](#label-enable-refresh-token-rotation-in-a-snowflake-oauth-security-integration)

### Use a request parameter in the body of an HTTP request

A client application can set the `enable_single_use_refresh_tokens` request parameter to `TRUE` in the body of an HTTP POST request to
the token request endpoint for [Snowflake OAuth](/user-guide/oauth-snowflake-overview) during the authorization code grant flow.

After a client application sets the `enable_single_use_refresh_tokens` request parameter to `TRUE` during the authorization code grant
flow, all future refresh token grant flows return a new refresh token and a new access token, and invalidate all previous access tokens and
refresh tokens.

For example, you can make the following HTTP POST request to do an **authorization code grant flow** and set the
`enable_single_use_refresh_tokens` request parameter to `TRUE` to get your first access token and refresh token:

HTTP requestHTTP response

Copy code

```
POST /oauth/token-request HTTP/1.1
Host: <my_subdomain>.snowflakecomputing.com
Authorization: Basic Base64(urlencode(<client_id>) + ':' + urlencode(<client_secret>))
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&code=123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ12345&redirect_uri=http://127.0.0.1:8080&enable_single_use_refresh_tokens=true
```

Copy code

```
{
  "access_token":  "<your_new_access_token>",
  "expires_in": 600,
  "refresh_token": "<your_new_refresh_token>",
  "token_type": "Bearer",
  "username": "<user1>",
}
```

You can then make the following HTTP POST request to do a **refresh token grant flow**, using your old refresh token, to get a new access
token and a new refresh token:

HTTP requestHTTP response

Copy code

```
POST /oauth/token-request HTTP/1.1
Host: <my_subdomain>.snowflakecomputing.com
Authorization: Basic Base64(urlencode(<client_id>) + ':' + urlencode(<client_secret>))
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&refresh_token=<your_old_refresh_token>
```

Copy code

```
{
  "access_token":  "<your_new_access_token>",
  "expires_in": 600,
  "refresh_token": "<your_new_refresh_token>",
  "token_type": "Bearer",
}
```

### Set a property in a Snowflake OAuth security integration

If a client application updates its cached refresh token after each refresh token grant flow, then you can enable single-use refresh tokens
for a [Snowflake OAuth security integration](/user-guide/oauth-snowflake-overview) by setting the
`OAUTH_SINGLE_USE_REFRESH_TOKENS_REQUIRED` property to `TRUE`.

After you enable single-use refresh tokens for a Snowflake OAuth security integration, all authorization code grant flows and refresh token
grant flows that use the `client_id` of the security integration issue single-use refresh tokens, regardless of whether the client
application specifies the `enable_single_use_refresh_tokens` request parameter during an authorization code grant flow.

For example, you can use [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-oauth-snowflake) to enable
single-use refresh tokens for a Snowflake OAuth security integration:

Copy code

```
ALTER SECURITY INTEGRATION my_integration
  SET OAUTH_SINGLE_USE_REFRESH_TOKENS_REQUIRED = TRUE;
```
