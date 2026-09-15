# Configure Snowflake OAuth for custom clients

This topic describes how to configure OAuth support for custom clients.

## Workflow

The following high-level steps are required to configure OAuth for custom clients:

1. Register your client with Snowflake. To register your client, create an integration. An integration is a Snowflake object that provides
   an interface between Snowflake and third-party services, such as a client that supports OAuth.

   The registration process defines a client ID and client secrets.
2. Configure calls to the Snowflake OAuth endpoints to request authorization codes from the Snowflake authorization server and to request
   and refresh access tokens.

   The optional “scope” parameters in the initial authorization request limit the role permitted by the access token and can additionally
   be used to configure the refresh token behavior. Clients can request the `session:role-any` scope when they need [in-session role switching](#label-oauth-custom-role-switching). Activation of secondary roles ([USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles)) is controlled separately by the
   OAUTH\_USE\_SECONDARY\_ROLES parameter.

## Create a Snowflake OAuth integration

Create a Snowflake OAuth integration using the
[CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-oauth-snowflake) command. Be sure to
specify `OAUTH_CLIENT = CUSTOM` when creating the integration.

Note

Only account administrators (users with the ACCOUNTADMIN role) or a role with the global CREATE INTEGRATION privilege can execute this
SQL command.

### Blocking specific roles from using the integration

The optional BLOCKED\_ROLES\_LIST parameter allows you to list Snowflake roles that a user cannot explicitly consent to using with
the integration.

By default, the ACCOUNTADMIN, SECURITYADMIN, GLOBALORGADMIN, and ORGADMIN roles are included in this list and cannot be removed. If you have a business
need to allow users to use Snowflake OAuth with these roles, and your security team allows it, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to request that these roles be allowed for your account.

### Restricting the integration to a specific list of roles

The optional ALLOWED\_ROLES\_LIST parameter lets you specify the set of Snowflake roles a user can consent
to for applications to access Snowflake data via the integration. When this list is set, all roles outside of it are implicitly blocked.

ALLOWED\_ROLES\_LIST is complementary to BLOCKED\_ROLES\_LIST: if you specify both, a role must appear in ALLOWED\_ROLES\_LIST and not
appear in BLOCKED\_ROLES\_LIST to be used. The default privileged roles (ACCOUNTADMIN, SECURITYADMIN, GLOBALORGADMIN, and ORGADMIN) remain
blocked by BLOCKED\_ROLES\_LIST even if you list them in ALLOWED\_ROLES\_LIST. For more information about BLOCKED\_ROLES\_LIST, see
[Blocking specific roles from using the integration](#label-oauth-custom-blocking-specific-roles-from-using-the-integration).

ALLOWED\_ROLES\_LIST and `OAUTH_USE_SECONDARY_ROLES = IMPLICIT` are alternative mechanisms for controlling which roles activate in OAuth
sessions, and you can’t combine them. `IMPLICIT` auto-activates the user’s default secondary roles, which would bypass the allowlist,
so you can only set ALLOWED\_ROLES\_LIST when `OAUTH_USE_SECONDARY_ROLES = NONE` (the default).

### Allowing clients to switch roles

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Snowflake OAuth sessions are single-role by default: [USE ROLE](/sql-reference/sql/use-role) is blocked unless you enable role switching on the integration. Set OAUTH\_ANY\_ROLE\_MODE in [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-oauth-snowflake) or [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-oauth-snowflake).

- `DISABLE` (default): the session can’t switch roles.
- `ENABLE`: the session can switch roles.
- `ENABLE_FOR_PRIVILEGE`: the session can switch roles only if the user holds the `USE_ANY_ROLE` privilege on the integration (through
  any role granted to the user). This privilege determines whether the session can switch roles at all; it doesn’t restrict which
  roles the session can switch to.

In addition to enabling the mode, the client must request the `session:role-any` scope in the authorization request (see
[Scope](#label-oauth-custom-scope)). A session can only switch to roles that are granted to the user and permitted by
ALLOWED\_ROLES\_LIST and BLOCKED\_ROLES\_LIST.

If the integration also uses role selection (`OAUTH_ENABLE_ROLE_SELECTION`), the roles the user consents to further bound switching:
the session can switch only among the consented roles. When the user consents to all roles — or the integration doesn’t use role
selection — switching is bounded only by the user’s grants and the allow/block lists.

Snowflake re-checks the integration’s role-switching configuration each time the session switches roles, so disabling role switching
(setting OAUTH\_ANY\_ROLE\_MODE to DISABLE) or revoking a required privilege prevents further switches in existing sessions.

The OAUTH\_ANY\_ROLE\_MODE controls the session’s primary role. Activation of secondary roles
([USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles)) is controlled separately by the OAUTH\_USE\_SECONDARY\_ROLES parameter
and the user’s consent.

To revoke a user’s consent to switch roles for an integration, use
[ALTER USER … REMOVE DELEGATED AUTHORIZATIONS OF ANY ROLE](/sql-reference/sql/alter-user).

### Letting users select roles during authorization

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

When a client omits a `session:role:role_name` scope in the authorization requests, the session uses the user’s
default role. To let the user pick the session role(s) during the OAuth authorization flow, set
the OAUTH\_ENABLE\_ROLE\_SELECTION parameter to TRUE when you create the integration (using
[CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration-oauth-snowflake)) or later (using
[ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-oauth-snowflake)).

When OAUTH\_ENABLE\_ROLE\_SELECTION is TRUE, Snowflake presents a role-selection step during authorization. The user can select and consent to one or
more roles — or to all of their roles — and the session is bound to the consented set: the session can use only those roles, and role
switching with [USE ROLE](/sql-reference/sql/use-role) is limited to the roles the user consented to. If the user consents to all
roles, the session can use any role granted to the user.

The roles offered for selection are bounded by the roles granted to the user and by the integration’s ALLOWED\_ROLES\_LIST and
BLOCKED\_ROLES\_LIST. When a user consents to more than one role, the consented roles form the session’s role universe: they are available both as
the session’s primary role (selectable with USE ROLE) and as its secondary roles (activated with USE SECONDARY ROLES). If a user
consents to a single role, the session is fixed to that role: it can’t switch roles with USE ROLE and can’t activate secondary roles
with USE SECONDARY ROLES.

When role selection is in effect, the consented roles govern the session’s secondary roles, and the OAUTH\_USE\_SECONDARY\_ROLES
parameter does not apply. Changing OAUTH\_USE\_SECONDARY\_ROLES does not affect a session that was already created from a role-selection
consent.

Note

Consent is additive. Re-authorizing expands a user’s consented set of roles; it never removes roles, and consenting to all roles
persists until revoked. To reduce or reset a user’s consented roles, the user or an administrator must revoke the delegated
authorization with [ALTER USER … REMOVE DELEGATED AUTHORIZATIONS](/sql-reference/sql/alter-user).

### Supporting multiple redirect URIs

The optional OAUTH\_ALTERNATE\_REDIRECT\_URIS parameter lets you register additional client redirect URIs for the integration. The URI in
the client’s authorization request must match either OAUTH\_REDIRECT\_URI or one of the URIs in OAUTH\_ALTERNATE\_REDIRECT\_URIS.

Use this parameter when a single integration must serve clients reached at multiple URIs (for example, separate URIs for staging and
production environments, or for different hostnames). Each URI must be protected by TLS unless OAUTH\_ALLOW\_NON\_TLS\_REDIRECT\_URI is set
to TRUE.

### Using Client Redirect with Snowflake OAuth custom clients

Snowflake supports using Client Redirect with Snowflake OAuth Custom Clients, including using Client Redirect and OAuth with supported
Snowflake Clients.

For more information, see [Redirecting client connections](/user-guide/client-redirect).

### Managing network policies

Snowflake supports network policies for OAuth. For more information, see [Restricting network traffic for Snowflake OAuth](/user-guide/oauth-snowflake-overview#label-snow-oauth-network-policies).

### Controlling access token validity

The optional `OAUTH_ACCESS_TOKEN_VALIDITY` parameter specifies how long an access token is valid (in seconds). Access tokens are
short-lived. The default is 600 seconds (10 minutes). You can set the value anywhere between 60 seconds (1 minute) and 3600 seconds
(1 hour).

When an access token expires, the client can use a refresh token to request a new access token without prompting the user to log in
again, as long as the refresh token is still valid. For the full parameter description, see
[CREATE SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/create-security-integration-oauth-snowflake).

### Integration example

The following example creates an OAuth integration that uses key pair authentication. The integration allows refresh tokens, which expire
after 1 day (86400 seconds). The integration blocks users from starting a session with SYSADMIN as the active role:

Copy code

```
CREATE SECURITY INTEGRATION oauth_kp_int
  TYPE = OAUTH
  ENABLED = TRUE
  OAUTH_CLIENT = CUSTOM
  OAUTH_CLIENT_TYPE = 'CONFIDENTIAL'
  OAUTH_REDIRECT_URI = 'https://localhost.com'
  OAUTH_ISSUE_REFRESH_TOKENS = TRUE
  OAUTH_REFRESH_TOKEN_VALIDITY = 86400
  BLOCKED_ROLES_LIST = ('SYSADMIN')
  OAUTH_CLIENT_RSA_PUBLIC_KEY ='
  MIIBI
  ...
  ';
```

## Call the OAuth endpoints

OAuth endpoints are the URLs that clients call to request authorization codes and to request and refresh access tokens. These endpoints
refer to specific OAuth 2.0 policies that execute when the endpoint is called.

Snowflake provides the following OAuth endpoints:

Authorization:
:   `<snowflake_account_url>/oauth/authorize`

Token requests:
:   `<snowflake_account_url>/oauth/token-request`

Where `<snowflake_account_url>` is a valid Snowflake account URL. For example, you might use the endpoints
`https://myorg-account_xyz.snowflakecomputing.com/oauth/authorize` and
`https://myorg-account_xyz.snowflakecomputing.com/oauth/token-request`. For a list of supported formats for the Snowflake account URL,
see [Connecting with a URL](/user-guide/organizations-connect#label-connecting-via-url).

To see a list of valid OAuth endpoints for a security integration, execute [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration),
and then view the values in the `OAUTH_ALLOWED_AUTHORIZATION_ENDPOINTS` and `OAUTH_ALLOWED_TOKEN_ENDPOINTS` properties.

### Authorization endpoint

The authorization endpoint is used to obtain an authorization grant after a user successfully authorizes a client with Snowflake.

> Important
>
> The authorization endpoint must be opened in a browser that the user can interact with. Do not use cURL with this endpoint.

The authorization endpoint is as follows:

Copy code

```
<snowflake_account_url>/oauth/authorize
```

Where:

> `snowflake_account_url`
> :   Specifies a valid [Snowflake account URL](/user-guide/organizations-connect#label-connecting-via-url). For example,
>     `https://myorg-account_xyz.snowflakecomputing.com/oauth/authorize`.

#### HTTP method

`GET`

#### Query parameters

Note

The following parameters should be URL encoded.

| Parameter | Data Type | Required? | Description |
| --- | --- | --- | --- |
| `client_id` | String | Yes | Client ID (provided by Snowflake when the client is registered) |
| `response_type` | String | Yes | Response type created. Currently supports `code` value, because Snowflake only issues authorization codes. |
| `redirect_uri` | String | Yes | URI where the user is redirected to after successfully authorizing. In general, this should match the value of the OAUTH\_REDIRECT\_URI parameter of the security integration. If the integration also defines OAUTH\_ALTERNATE\_REDIRECT\_URIS, the URI can match OAUTH\_REDIRECT\_URI or any URI in that list.  However, if the `redirect_uri` includes query parameters, do not include those query parameters when defining the OAUTH\_REDIRECT\_URI parameter of the security integration. For example, if the value of the `redirect_uri` query parameter in the request to the authorization endpoint is `https://www.example.com/connect?authType=snowflake`, make sure the OAUTH\_REDIRECT\_URI parameter in the security integration is set to `https://www.example.com/connect`. |
| `state` | String | No | String of no more than 2048 ASCII characters that is returned with the response from the Snowflake authorization server. Typically used to prevent cross-site request forgery attacks. |
| `scope` | String | No | Space-delimited string that is used to limit the scope of the access request. For more information, refer to [Scope](#scope) (in this topic). |
| `code_challenge` | String | No | Challenge for Proof Key for Code Exchange (PKCE). String generated via a secret and a code challenge method. For more information, refer to [Proof key for code exchange](#label-proof-key-for-code-exchange) (in this topic). |
| `code_challenge_method` | String | No | String indicating the method used to derive the code challenge for PKCE. For more information, refer to [Proof key for code exchange](#label-proof-key-for-code-exchange) (in this topic). |

Expand

Show lessSee more

When a user authorizes the client, a redirect is made to the `redirect_uri` that contains the following in a GET request:

> | Query Parameter | Description |
> | --- | --- |
> | `code` | Short-lived authorization code, which can be exchanged at the token endpoint for an access token. |
> | `state` | `state` value provided in the original request, unmodified. |
> | `scope` | Scope of the access request; currently the same as the `scope` value in the initial authorization request, but might differ in the future. For more information, see [Scope](#scope) (in this topic). |
>
> Expand
>
> Show lessSee more

##### Scope

The `scope` query parameter in the initial authorization request optionally limits the operations and role permitted by the access token.

Scope is validated immediately when making an authorization request with respect to semantics, but not necessarily validity. That is, any
invalid scopes (for example, “bogus\_scope”) are rejected before the user authenticates, but a scope the user does not have access to (a
particular role, etc.) does not result in an error until after the user authenticates.

The following are the possible values of the `scope` query parameter:

| Scope Value | Required? | Description |
| --- | --- | --- |
| `refresh_token` | No | If included in the authorization URL, Snowflake presents the user with the option to consent to offline access. In this context, offline access refers to allowing the client to refresh access tokens when the user is not present. With user consent, the authorization server returns a refresh token in addition to an access token when redeeming the authorization code. |
| `session:role:role_name` | No | Used to limit the access token to a single role that the user can consent to for the session. Only one session role scope can be specified. If this scope is omitted, then the default role for the user is used instead. When a user authorizes consent, Snowflake always displays the role for the session regardless if this scope is included in the authorization URL.  Note that `role_name` is case-sensitive and must be input in all uppercase unless the role name was enclosed in quotes when it was created using [CREATE ROLE](/sql-reference/sql/create-role). To verify the case, execute [SHOW ROLES](/sql-reference/sql/show-roles) in Snowflake and see the role name in the output.  If the role name contains characters that are reserved in a query parameter URL, you must use a `session:role-encoded:role_name` syntax, where `role_name` is a URL-encoded string. For example, if the role name is `AUTH SNOWFLAKE` (with a space), then the value of the `scope` query parameter must be `session:role-encoded:AUTH%20SNOWFLAKE`. |
| `session:role-any` | No | Requests a session that can switch its primary role at runtime (using [USE ROLE](/sql-reference/sql/use-role)) instead of being fixed to a single role. The user consents to this capability, and the session can then switch to any role granted to the user that is permitted by the integration’s `ALLOWED_ROLES_LIST` and `BLOCKED_ROLES_LIST`.  This scope is honored only when the security integration sets `OAUTH_ANY_ROLE_MODE` to `ENABLE` or `ENABLE_FOR_PRIVILEGE`; otherwise the authorization request is rejected. You can combine this scope with a `session:role:role_name` scope to select the initial primary role. If you omit the role scope, the user’s default role is used.  For more information, see [Allowing clients to switch roles](#label-oauth-custom-role-switching). |

Expand

Show lessSee more

The following example limits authorization to the custom R1 role:

> Copy code
>
> ```
> scope=session:role:R1
> ```

The following example indicates that access/refresh tokens should use the default role for the user and requests a refresh token so that
offline access can occur:

> Copy code
>
> ```
> scope=refresh_token
> ```

The following example limits authorization to the custom R1 role and requests a refresh token so that offline access can occur:

> Copy code
>
> ```
> scope=refresh_token session:role:R1
> ```

### Token endpoint

This endpoint returns access tokens or refresh tokens depending on the request parameters. The token endpoint is as follows:

Copy code

```
<snowflake_account_url>/oauth/token-request
```

Where:

> `snowflake_account_url`
> :   Specifies a valid [Snowflake account URL](/user-guide/organizations-connect#label-connecting-via-url). For example,
>     `https://myorg-account_xyz.snowflakecomputing.com/oauth/token-request`.

#### HTTP method

`POST`

Ensure that the content-type header in the POST request is set as follows:

Copy code

```
Content-type: application/x-www-form-urlencoded
```

#### Client authentication

Snowflake OAuth supports the following client authentication methods at the token endpoint
(`token_endpoint_auth_methods_supported` in OAuth metadata):

- `client_secret_basic`: Send the client credentials in the HTTP `Authorization` header using the
  [Basic Authentication Scheme](https://tools.ietf.org/html/rfc2617).
- `client_secret_post`: Send the client credentials in the POST request body as form parameters.
- `private_key_jwt`: Authenticate with a JWT signed by the client’s RSA private key instead of a client secret. Send the JWT in the
  `client_assertion` request parameter, as defined by [RFC 7523](https://datatracker.ietf.org/doc/html/rfc7523). Snowflake recommends this
  method for clients that authenticate with a key pair. For setup and examples, see
  [Authenticate with a client assertion](#label-oauth-client-assertion).

  Snowflake also accepts the same signed JWT in an `Authorization: Bearer` header. That method predates Snowflake’s support for
  `client_assertion` and isn’t part of the OAuth specifications, so use it only for clients that already depend on it. For more information,
  see [Authenticate with a JWT in the Authorization header](#label-oauth-key-pair-jwt-header).

For `client_secret_basic` and `client_secret_post`, retrieve the client ID and client secret with the
[SYSTEM$SHOW\_OAUTH\_CLIENT\_SECRETS](/sql-reference/functions/system_show_oauth_client_secrets) function.

##### HTTP Basic authentication (`client_secret_basic`)

Include an `Authorization` header whose value is:

`Basic Base64(urlencode(client_id) + ':' + urlencode(client_secret))`

Where:

| Header Value | Data Type | Required | Description |
| --- | --- | --- | --- |
| `client_id` | String | Yes | Client ID of the integration. |
| `client_secret` | String | Yes | Client secret for the integration. |

Expand

Show lessSee more

That is, apply `urlencode` to each credential, join the results with a literal `:` character, apply `Base64` to the joined string, and
prefix the result with `Basic` followed by a space. Secrets from [SYSTEM$SHOW\_OAUTH\_CLIENT\_SECRETS](/sql-reference/functions/system_show_oauth_client_secrets) often contain characters that
`urlencode` rewrites, so skipping that step can cause `invalid_client` errors.

##### Request body authentication (`client_secret_post`)

Omit the `Authorization` header and include `client_id` and `client_secret` as form parameters in the request body together with the other
token-request parameters. See [Request body](#request-body).

#### Request body

| Parameter | Data Type | Required | Description |
| --- | --- | --- | --- |
| `grant_type` | String | Yes | Type of grant requested:   `authorization_code` indicates that an authorization code should be exchanged for an access token.   `refresh_token` indicates a request to refresh an access token. |
| `client_id` | String | Conditional | Client ID of the integration. Required when using `client_secret_post` client authentication. Don’t include this parameter when using `client_secret_basic`. Not required when using `client_assertion`, because Snowflake reads the client ID from the assertion. |
| `client_secret` | String | Conditional | Client secret for the integration. Required when using `client_secret_post` client authentication. Don’t include this parameter when using `client_secret_basic`. |
| `client_assertion` | String | Conditional | Signed JWT that authenticates the client. Required when using `private_key_jwt` client authentication with a client assertion. For more information, see [Authenticate with a client assertion](#label-oauth-client-assertion). |
| `client_assertion_type` | String | Conditional | Format of the `client_assertion` value. Required whenever `client_assertion` is present, and must be set to `urn:ietf:params:oauth:client-assertion-type:jwt-bearer`. |
| `code` | String | Yes | Authorization code returned from the token endpoint. Used and required when `grant_type` is set to `authorization_code`. |
| `refresh_token` | String | Yes | Refresh token returned from an earlier request to the token endpoint when redeeming the authorization code. Used and required when `grant_type` is set to `refresh_token`. |
| `redirect_uri` | String | Yes | Redirect URI as used in the authorization URL when requesting an authorization code. Used and required when `grant_type` is set to `authorization_code`. |
| `code_verifier` | String | No | Required only if the authorization request was sent to the [Authorization Endpoint](#authorization-endpoint) with a `code_challenge` parameter value. Code verifier for PKCE. For more information, see [Proof key for code exchange](#label-proof-key-for-code-exchange) (in this topic). |

Expand

Show lessSee more

#### Response

A JSON object is returned with the following fields:

| Field | Data Type | Description |
| --- | --- | --- |
| `access_token` | String | Access token used to establish a Snowflake session |
| `refresh_token` | String | Refresh token. Not issued if the client is configured to not issue refresh tokens or if the user did not consent to the `refresh_token` scope. |
| `expires_in` | Integer | Number of seconds remaining until the token expires |
| `token_type` | String | Access token type. Currently, always `Bearer`. |
| `username` | String | Username that the access token belongs to. Currently only returned when exchanging an authorization code for an access token. |

Expand

Show lessSee more

##### Successful response example

The following example shows a successful response when exchanging an authorization code for an access and refresh token:

Copy code

```
{
  "access_token":  "ACCESS_TOKEN",
  "expires_in": 600,
  "refresh_token": "REFRESH_TOKEN",
  "token_type": "Bearer",
  "username": "user1"
}
```

##### Unsuccessful response example

The following example shows an unsuccessful response:

Copy code

```
{
  "data" : null,
  "message" : "This is an invalid client.",
  "code" : null,
  "success" : false,
  "error" : "invalid_client"
}
```

The `message` string value is a description of the error and `error` is the error type. For more information on the types of
errors returned, see [OAuth Error Codes](/user-guide/oauth-snowflake-overview#label-oauth-snowflake-error-codes).

### Token exchange

This endpoint returns an OAuth access token in exchange for a JSON Web Token (JWT). For an example, see [Tutorial 1 (step 5)](/developer-guide/snowpark-container-services/tutorials/tutorial-1). In the tutorial you send a request to this endpoint to exchange a JWT token for an OAuth token and use the OAuth token to access a public endpoint exposed by a Snowpark Container Services service.

The token endpoint is as follows:

Copy code

```
<snowflake_account_url>/oauth/token
```

Where:

> `snowflake_account_url`
> :   Specifies a valid [Snowflake account URL](/user-guide/organizations-connect#label-connecting-via-url). For example,
>     `https://myorg-account_xyz.snowflakecomputing.com/oauth/token`.

#### HTTP method

`POST`

Ensure that the content-type header in the POST request is set as follows:

Copy code

```
Content-type: application/x-www-form-urlencoded
```

#### Request body

| Parameter | Data Type | Required | Description |
| --- | --- | --- | --- |
| `grant_type` | String | Yes | Pass this as string `urn:ietf:params:oauth:grant-type:jwt-bearer` |
| `scope` | String | Yes | Pass this as string `session:role:role_name <ingress-endpoint-url>`. Note that the `role_name` is case-sensitive. Use the [SHOW ENDPOINTS IN SERVICE](/sql-reference/sql/show-endpoints) command to find the ingress endpoint URL. |
| `assertion` | String | Yes | Pass the JWT token. |

Expand

Show lessSee more

For example,

Copy code

```
{
    'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    'scope': 'session:role:TEST_ROLE ab12-orgname-acctname.snowflakecomputing.app',
    'assertion': '<token>'
}
```

When specifying `scope`, the `session:role:role_name` is optional. If not provided, the default role of the user is used.

Copy code

```
{
    'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    'scope': 'ab12-orgname-acctname.snowflakecomputing.app',
    'assertion': '<token>'
}
```

#### Response

An OAuth access token is returned.

## Proof key for code exchange

Snowflake supports Proof Key for Code Exchange (PKCE) for obtaining access tokens using the `authorization_code` grant type as
described in [RFC 7636](https://tools.ietf.org/html/rfc7636). PKCE can be used to lessen the possibility of an authorization code
interception attack, and is suitable for clients that might not be able to fully keep the client secret secure.

By default, PKCE is optional and is enforced only if the `code_challenge` and `code_challenge_method` parameters are both
included in the authorization endpoint URL. However, Snowflake highly recommends that your client require PKCE for all authorizations to
make the OAuth flow more secure.

The following describes how PKCE for Snowflake works:

1. The client creates a secret called the *code verifier* and performs a transformation on it to generate the *code challenge*. The client
   holds onto the secret.

   Important

   Generate the *code verifier* from the allowed ASCII characters according to
   [Section 4.1 of RFC 7636](https://tools.ietf.org/html/rfc7636#section-4.1).
2. The client directing the user to the Authorization URL appends the following two query parameters:

   `code_challenge`
   :   Specifies the code challenge generated in Step 1.

   `code_challenge_method`
   :   Specifies the transformations used on the code verifier in Step 1 to generate the code challenge. Currently, Snowflake only supports
       SHA256, so this value must be set to `S256`. The transformation algorithm for SHA256 is
       `BASE64URL-ENCODE(SHA256(ASCII(code_verifier)))`.
3. After the user consents to the requested scopes or Snowflake determines that consent is present for that user, the authorization code
   is issued.
4. The client receives the authorization code from the Snowflake authorization server, which it then submits along with the
   `code_verifier` in the request to the token endpoint.
5. Snowflake transforms the `code_verifier` value and verifies that the transformed value matches the `code_challenge` value
   used when generating authorizations. If these values match, then the authorization server issues the access and refresh tokens.

## Using key-pair authentication

Snowflake supports key-pair authentication (`private_key_jwt`) rather than a client ID and client secret when calling the OAuth token
endpoint. You assign a public key to the OAuth security integration, and your client signs a short-lived JWT with the matching private key.
Because the private key never leaves the client, there’s no shared secret to distribute, rotate, or leak.

Snowflake accepts the signed JWT in either of the following ways:

| Method | Description |
| --- | --- |
| [Client assertion](#label-oauth-client-assertion) (recommended) | Send the JWT in the `client_assertion` request parameter. This method implements [RFC 7523](https://datatracker.ietf.org/doc/html/rfc7523), the standard JWT profile for OAuth client authentication, so standard OAuth client libraries can use it without Snowflake-specific code. |
| [Authorization header](#label-oauth-key-pair-jwt-header) (legacy) | Send the JWT in an `Authorization: Bearer` header. This method predates Snowflake’s support for `client_assertion` and isn’t part of the OAuth specifications. It remains supported for existing clients. |

Expand

Show lessSee more

Note

Snowflake recommends the client assertion for all new clients, and recommends migrating existing clients to it. Both methods use the same
key pair and the same security integration, so migrating means changing how your client transmits the JWT and which claims it sets. You
don’t need to generate new keys or reconfigure the integration.

### Generate and register an RSA key pair

Both methods require a 2048-bit (minimum) RSA key pair. Generate the PEM (Privacy Enhanced Mail) public-private key pair using OpenSSL, then
assign the public key to the OAuth security integration.

To configure the public/private key pair:

1. From the command line in a terminal window, generate an encrypted private key:

   Copy code

   ```
   $ openssl genrsa 2048 | openssl pkcs8 -topk8 -v2 des3 -inform PEM -out rsa_key.p8
   ```

   OpenSSL prompts for a passphrase used to encrypt the private key file. Snowflake recommends using a strong passphrase to protect the private
   key. Record this passphrase. You must input it when connecting to Snowflake. Note that the passphrase is only used for protecting
   the private key and is never sent to Snowflake.

   **Sample PEM private key**

   Copy code

   ```
   -----BEGIN ENCRYPTED PRIVATE KEY-----
   MIIE6TAbBgkqhkiG9w0BBQMwDgQILYPyCppzOwECAggABIIEyLiGSpeeGSe3xHP1
   wHLjfCYycUPennlX2bd8yX8xOxGSGfvB+99+PmSlex0FmY9ov1J8H1H9Y3lMWXbL
   ...
   -----END ENCRYPTED PRIVATE KEY-----
   ```
2. From the command line, generate the public key by referencing the private key:

   Copy code

   ```
   $ openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
   ```

   **Sample PEM public key**

   Copy code

   ```
   -----BEGIN PUBLIC KEY-----
   MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy+Fw2qv4Roud3l6tjPH4
   zxybHjmZ5rhtCz9jppCV8UTWvEXxa88IGRIHbJ/PwKW/mR8LXdfI7l/9vCMXX4mk
   ...
   -----END PUBLIC KEY-----
   ```
3. Copy the public and private key files to a local directory for storage. Record the path to the files.

   Note that the private key is stored using the PKCS#8 (Public Key Cryptography Standards) format and is encrypted using the passphrase
   you specified in the previous step; however, the file should still be protected from unauthorized access using the file permission
   mechanism provided by your operating system. It is your responsibility to secure the file when it is not being used.
4. Assign the public key to the integration object using [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-oauth-snowflake). For example:

   Copy code

   ```
   ALTER SECURITY INTEGRATION myint SET OAUTH_CLIENT_RSA_PUBLIC_KEY='MIIBIjANBgkqh...';
   ```

   Note

   - Only account administrators can execute the ALTER SECURITY INTEGRATION command.
   - Exclude the public key header and footer in the command.

   Verify the public key fingerprint using [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration):

   Copy code

   ```
   DESC SECURITY INTEGRATION myint;

   +----------------------------------+---------------+----------------------------------------------------------------------+------------------+
   | property                         | property_type | property_value                                                       | property_default |
   |----------------------------------+---------------+----------------------------------------------------------------------+------------------|
   ...
   | OAUTH_CLIENT_RSA_PUBLIC_KEY_FP   | String        | SHA256:MRItnbO/123abc/abcdefghijklmn12345678901234=                  |                  |
   | OAUTH_CLIENT_RSA_PUBLIC_KEY_2_FP | String        |                                                                      |                  |
   ...
   +----------------------------------+---------------+----------------------------------------------------------------------+------------------+
   ```

   Note

   The `OAUTH_CLIENT_RSA_PUBLIC_KEY_2_FP` property is described in [Key Rotation](#key-rotation) (in this topic).

### Authenticate with a client assertion

A client assertion is a JWT that your client signs with its private key and sends to the token endpoint to prove its identity. Snowflake
implements the client assertion exactly as [RFC 7523](https://datatracker.ietf.org/doc/html/rfc7523) defines it, which is the same
mechanism that OpenID Connect calls `private_key_jwt`. Standard OAuth client libraries that support `private_key_jwt` can therefore
authenticate to Snowflake without Snowflake-specific code.

To authenticate with a client assertion, include the following form parameters in the token request body, in addition to the
grant-specific parameters described in [Request body](#request-body):

- `client_assertion_type`, set to `urn:ietf:params:oauth:client-assertion-type:jwt-bearer`.
- `client_assertion`, set to the signed JWT.

Don’t send a `client_secret`, and don’t send an `Authorization` header. The `client_id` parameter isn’t required either, because Snowflake
identifies the client from the assertion.

#### Client assertion claims

Sign the assertion with the `RS256` algorithm, using the private key whose public key is registered on the integration. `RS256` is the only
signature algorithm Snowflake accepts for a client assertion.

Set the following claims:

| Claim | Data type | Required | Description |
| --- | --- | --- | --- |
| `iss` | String | Yes | Issuer of the assertion. Must be the client ID of the OAuth integration. Retrieve the client ID with the [SYSTEM$SHOW\_OAUTH\_CLIENT\_SECRETS](/sql-reference/functions/system_show_oauth_client_secrets) function. |
| `sub` | String | Yes | Subject of the assertion. Must be the same client ID as `iss`, because the client issues the assertion about itself. |
| `aud` | String | Yes | Audience of the assertion. Must be your account’s token endpoint URL, in the form `https://account_name.snowflakecomputing.com/oauth/token-request`, where `account_name` uses the organization name and account name format of your account identifier (for example, `myorg-account_xyz`). Don’t use the account locator format. If the claim holds a list of audiences, one of them must be this URL. |
| `exp` | Timestamp | Yes | Time when the assertion expires. Must be in the future and no more than one hour ahead. Keep the lifetime short, such as a few minutes. |
| `iat` | Timestamp | No | Time when the assertion was issued. When present, must be within the last 10 minutes, and must not be in the future beyond a small allowance for clock skew. |
| `nbf` | Timestamp | No | Time before which the assertion isn’t valid. When present, must not be in the future. |

Expand

Show lessSee more

Snowflake ignores any other claims in the assertion.

Note

Unlike the [legacy Authorization header method](#label-oauth-key-pair-jwt-header), the client assertion doesn’t include the public key
fingerprint or the account locator in its claims. Snowflake tries each public key registered on the integration, so key rotation works
without changing the claims your client sets.

#### Client assertion example

The following example builds a client assertion and uses it to exchange an authorization code for an access token, then to refresh that
access token. Before running it, set the following values:

- `<account_name>`: The organization name and account name format of your account identifier, for example `myorg-account_xyz`.
- `<client_id>`: The client ID of your OAuth integration, retrieved with the
  [SYSTEM$SHOW\_OAUTH\_CLIENT\_SECRETS](/sql-reference/functions/system_show_oauth_client_secrets) function.
- `<private_key>`: Contents of the decrypted *rsa\_key.p8*, including the `-----BEGIN` header and `-----END` footer, which you can obtain by
  executing *openssl rsa -in rsa\_key.p8 -text*.
- `<redirect_uri>`: The redirect URI your integration is configured with. Execute the DESC SECURITY INTEGRATION command to obtain it.
- `<oauth_az_code>`: An authorization code obtained from the [Authorization endpoint](#label-oauth-authorization-endpoint). This code needs to be refreshed
  periodically.

Copy code

```
import datetime
import urllib.parse

import jwt
import requests

ACCOUNT_NAME = "<account_name>"
CLIENT_ID = "<client_id>"
TOKEN_URL = f"https://{ACCOUNT_NAME}.snowflakecomputing.com/oauth/token-request"

CLIENT_ASSERTION_TYPE = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"

private_key = """
<private_key>
"""

def build_client_assertion():
    """Build a short-lived RFC 7523 client assertion for the token endpoint."""
    now = datetime.datetime.now(datetime.timezone.utc)
    claims = {
        "iss": CLIENT_ID,
        "sub": CLIENT_ID,
        "aud": TOKEN_URL,
        "iat": now,
        "exp": now + datetime.timedelta(minutes=5),
    }
    return jwt.encode(claims, private_key, algorithm="RS256")

def _make_request(payload):
    """Send a token request, authenticating the client with a fresh assertion."""
    payload = {
        **payload,
        "client_assertion_type": CLIENT_ASSERTION_TYPE,
        "client_assertion": build_client_assertion(),
    }
    response = requests.post(
        TOKEN_URL,
        headers={"content-type": "application/x-www-form-urlencoded"},
        data=urllib.parse.urlencode(payload),
    )
    return response.json()

def make_request_for_access_token(oauth_az_code, redirect_uri):
    """Given an authorization code, request an access token and a refresh token."""
    return _make_request({
        "grant_type": "authorization_code",
        "code": oauth_az_code,
        "redirect_uri": redirect_uri,
    })

def make_request_for_refresh_token(refresh_token):
    """Given a refresh token, request another access token."""
    return _make_request({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    })

def main():
    data = make_request_for_access_token("<oauth_az_code>", "<redirect_uri>")
    refresh_token = data["refresh_token"]
    data = make_request_for_refresh_token(refresh_token)
    access_token = data["access_token"]

if __name__ == "__main__":
    main()
```

Each token request must carry its own freshly signed assertion. Snowflake rejects an assertion whose `exp` has passed, so don’t cache and
reuse one across requests.

The following example shows the equivalent request without a client library, where `<signed_jwt>` is the assertion you built:

Copy code

```
curl -X POST \
  -H "Content-type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=authorization_code" \
  --data-urlencode "code=<oauth_az_code>" \
  --data-urlencode "redirect_uri=<redirect_uri>" \
  --data-urlencode "client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer" \
  --data-urlencode "client_assertion=<signed_jwt>" \
  "https://<account_name>.snowflakecomputing.com/oauth/token-request"
```

### Authenticate with a JWT in the Authorization header

Note

This method predates Snowflake’s support for [client assertions](#label-oauth-client-assertion) and isn’t part of the OAuth
specifications. It remains supported, but Snowflake recommends the client assertion for new clients. Note that this method requires
different `iss` and `sub` claims than a client assertion, and requires the public key fingerprint.

To authenticate with this method, send the signed JWT in the `Authorization` header as a bearer token:

1. Modify and execute the sample code below. The code uses the private key to encode a JWT and then passes that token to the Snowflake
   authorization server:

   - Update the security parameters:

     - `<private_key>`: Contents of the decrypted *rsa\_key.p8* (including BEGIN and END), which you can obtain by executing *openssl rsa -in rsa\_key.p8 -text*.
   - Update the session parameters:

     - `<account_locator>`: Your account locator code, for example `CIB07125`.
       You cannot use the account name (for example, `myorg-account_xyz`).
   - Update the token-request endpoint in the `_make_request()` function:

     - `<account_name>`: This is the account name format of your account’s identifier (for example, `myorg-account_xyz`).
   - Update the public key fingerprint:

     - `<public_key_fp>`: Retrieved by executing the DESC SECURITY INTEGRATION command.
       There can be 2 public keys, so ensure you’re referencing the correct key.
   - Update the redirect URI:

     - `<redirect_uri>`: The redirect URI your integration is configured with. Execute the DESC SECURITY INTEGRATION command to obtain it.
   - Obtain an OAuth authorization code:

     - `<oauth_az_code>`: Obtained after authenticating with your */authorize* endpoint.
       Note: this code needs to be refreshed periodically.
   - Update the JSON Web Token (JWT) fields:

     post body
     :   A JSON object with the following standard fields (“claims”):

     | Attribute | Data Type | Required | Description |
     | --- | --- | --- | --- |
     | `iss` | String | Yes | Specifies the principal that issued the JWT in the format `client_id.public_key_fp` where `client_id` is the client ID of the OAuth client integration and `public_key_fp` is the fingerprint of the public key that is used during verification. |
     | `sub` | String | Yes | Subject of the JWT in the format `account_locator.client_id` where `account_locator` is your Snowflake account locator and `client_id` is the client ID of the OAuth client integration. Depending on the cloud platform (AWS or Azure) and region where your account is hosted, the full account name might require additional segments. For more information, see the `account` variable description under [Token endpoint](#label-oauth-token-endpoint). |
     | `iat` | Timestamp | No | Time when the token was issued. |
     | `exp` | Timestamp | Yes | Time when the token should expire. This period should be relatively short (for example, a few minutes). |

     Expand

     Show lessSee more

   **Sample code**

   Note that the `private_key` value (decrypted) includes the `-----BEGIN` header and the `-----END` footer.

   Copy code

   ```
   import datetime
   import json
   import urllib

   import jwt
   import requests

   private_key = """
   <private_key>
   """

   public_key_fp = "<public_key_fp>" # SHA256:MR...

   def _make_request(payload, encoded_jwt_token):
       token_url = "https://<account_name>.snowflakecomputing.com/oauth/token-request"
       headers = {
               u'Authorization': "Bearer %s" % (encoded_jwt_token),
               u'content-type': u'application/x-www-form-urlencoded'
       }
       r = requests.post(
               token_url,
               headers=headers,
               data=urllib.urlencode(payload))
       return r.json()

   def make_request_for_access_token(oauth_az_code, encoded_jwt_token):
       """ Given an Authorization Code, make a request for an Access Token
       and a Refresh Token."""
       payload = {
           'grant_type': 'authorization_code',
           'code': oauth_az_code,
           'redirect_uri': <redirect_uri>
       }
       return _make_request(payload, encoded_jwt_token)

   def make_request_for_refresh_token(refresh_token, encoded_jwt_token):
       """ Given a Refresh Token, make a request for another Access Token."""
       payload = {
           'grant_type': 'refresh_token',
           'refresh_token': refresh_token
       }
       return _make_request(payload, encoded_jwt_token)

   def main():
       account_locator = "<account_locator>"
       client_id = "1234"  # found by running DESC SECURITY INTEGRATION
       issuer = "{}.{}".format(client_id, public_key_fp)
       subject = "{}.{}".format(account_locator, client_id)
       payload = {
           'iss': issuer,
           'sub': subject,
           'iat': datetime.datetime.utcnow(),
           'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
       }
       encoded_jwt_token = jwt.encode(
               payload,
               private_key,
               algorithm='RS256')

       data = make_request_for_access_token(<oauth_az_code>, encoded_jwt_token)
       refresh_token = data['refresh_token']
       data = make_request_for_refresh_token(refresh_token, encoded_jwt_token)
       access_token = data['access_token']

   if __name__ == '__main__':
       main()
   ```

   After the token is created, submit it in requests to the token endpoint. Requests require the Bearer authorization format as the
   authorization header instead of the basic authorization format normally used for the client ID and client secret, as follows:

   Copy code

   ```
   "Authorization: Bearer JWT_TOKEN"
   ```

### Key rotation

Snowflake supports multiple active keys to allow for uninterrupted rotation. Rotate and replace your public and private keys based on the
expiration schedule you follow internally.

Currently, you can use the `OAUTH_CLIENT_RSA_PUBLIC_KEY` and `OAUTH_CLIENT_RSA_PUBLIC_KEY_2` parameters for
[ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration-oauth-snowflake) to associate up to 2 public keys with a single user.

To rotate your keys:

1. Complete the steps in [Generate and register an RSA key pair](#label-oauth-key-pair-authentication) (in this topic):

   - Generate a new private and public key set.
   - Assign the public key to the integration. Set the public key value to either `OAUTH_CLIENT_RSA_PUBLIC_KEY` or
     `OAUTH_CLIENT_RSA_PUBLIC_KEY_2` (whichever key value is not currently in use). For example:

     Copy code

     ```
     alter integration myint set oauth_client_rsa_public_key_2='JERUEHtcve...';
     ```
2. Update the code to connect to Snowflake. Specify the new private key.

   Snowflake verifies the correct active public key for authentication based on the submitted private key.
3. Remove the old public key from the integration. For example:

   Copy code

   ```
   alter integration myint unset oauth_client_rsa_public_key;
   ```

## Configuring agent sessions

Snowflake supports designating custom OAuth integrations as agentic. When an integration is configured with `IS_AGENTIC = TRUE`, Snowflake automatically recognizes and treats all incoming requests from that client as an AI agent acting on behalf of a user.

As a result, the system function [IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated) will return `TRUE` for these sessions.

Set `IS_AGENTIC = TRUE` if you expect all authentication requests for this integration to be agentic. This enables enhanced auditing and specialized governance for your AI workflows, ensuring that agent-driven data access is explicitly tracked, monitored, and secured.

For an overview of agent identity, including other ways Snowflake marks sessions as agentic, see
[Agent identity](/user-guide/agent-identity). For more information about the OAuth parameters, see
[CREATE SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/create-security-integration-oauth-snowflake) and
[ALTER SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/alter-security-integration-oauth-snowflake).

## Error codes

See the [Error codes](/user-guide/oauth-snowflake-overview#label-oauth-snowflake-error-codes) for a list of error codes associated with OAuth, as well as errors that are returned in the JSON
blob, during the authorization flow, token request or exchange, or when creating a Snowflake session after completing the OAuth flow.

## Pre-authorizing user consent for a role

Security administrators (that is, users with the SECURITYADMIN role) or higher can pre-authorize consent for a client to initiate a session for
a user using a specified role and integration. This consent is granted using [ALTER USER](/sql-reference/sql/alter-user) with the ADD DELEGATED
AUTHORIZATION keywords. Without this delegated authorization, a user must authorize consent for the role after authentication. This
delegated authorization can also be revoked.

For more information, see [Managing user consent for OAuth](/user-guide/oauth-consent).
