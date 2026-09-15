# CREATE SECURITY INTEGRATION (Snowflake OAuth)

Creates a new Snowflake OAuth security integration in the account or replaces an existing integration. A Snowflake OAuth security
integration enables clients that support OAuth to redirect users to an authorization page and generate access tokens (and optionally,
refresh tokens) for access to Snowflake.

For information about creating other types of security integrations (for example, External OAuth), see [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration).

See also:
:   [ALTER SECURITY INTEGRATION (Snowflake OAuth)](/sql-reference/sql/alter-security-integration-oauth-snowflake), [DROP INTEGRATION](/sql-reference/sql/drop-integration), [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations)

## Syntax

**Snowflake OAuth for partner applications**

Copy code

```
CREATE [ OR REPLACE ] SECURITY INTEGRATION [IF NOT EXISTS]
  <name>
  TYPE = OAUTH
  OAUTH_CLIENT = <partner_application>
  OAUTH_REDIRECT_URI = '<uri>'  -- Required when OAUTH_CLIENT=LOOKER
  [ ENABLED = { TRUE | FALSE } ]
  [ OAUTH_ISSUE_REFRESH_TOKENS = { TRUE | FALSE } ]
  [ OAUTH_ACCESS_TOKEN_VALIDITY = <integer> ]
  [ OAUTH_REFRESH_TOKEN_VALIDITY = <integer> ]
  [ OAUTH_SINGLE_USE_REFRESH_TOKENS_REQUIRED = { TRUE | FALSE } ]
  [ OAUTH_USE_SECONDARY_ROLES = { IMPLICIT | NONE } ]
  [ NETWORK_POLICY = '<network_policy>' ]
  [ ALLOWED_ROLES_LIST = ( '<role_name>' [ , '<role_name>' , ... ] ) ]
  [ BLOCKED_ROLES_LIST = ( '<role_name>' [ , '<role_name>' , ... ] ) ]
  [ USE_PRIVATELINK_FOR_AUTHORIZATION_ENDPOINT = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
```

**Snowflake OAuth for custom clients**

Copy code

```
CREATE [ OR REPLACE ] SECURITY INTEGRATION [IF NOT EXISTS]
  <name>
  TYPE = OAUTH
  OAUTH_CLIENT = CUSTOM
  OAUTH_CLIENT_TYPE = 'CONFIDENTIAL' | 'PUBLIC'
  OAUTH_REDIRECT_URI = '<uri>'
  [ ENABLED = { TRUE | FALSE } ]
  [ OAUTH_ALLOW_NON_TLS_REDIRECT_URI = { TRUE | FALSE } ]
  [ OAUTH_ALTERNATE_REDIRECT_URIS = ( '<uri>' [ , '<uri>' , ... ] ) ]
  [ OAUTH_ENFORCE_PKCE = { TRUE | FALSE } ]
  [ OAUTH_ENABLE_ROLE_SELECTION = { TRUE | FALSE } ]
  [ OAUTH_SINGLE_USE_REFRESH_TOKENS_REQUIRED = { TRUE | FALSE } ]
  [ OAUTH_USE_SECONDARY_ROLES = { IMPLICIT | NONE } ]
  [ PRE_AUTHORIZED_ROLES_LIST = ( '<role_name>' [ , '<role_name>' , ... ] ) ]
  [ ALLOWED_ROLES_LIST = ( '<role_name>' [ , '<role_name>' , ... ] ) ]
  [ BLOCKED_ROLES_LIST = ( '<role_name>' [ , '<role_name>' , ... ] ) ]
  [ OAUTH_ANY_ROLE_MODE = { DISABLE | ENABLE | ENABLE_FOR_PRIVILEGE } ]
  [ OAUTH_ISSUE_REFRESH_TOKENS = { TRUE | FALSE } ]
  [ OAUTH_ACCESS_TOKEN_VALIDITY = <integer> ]
  [ OAUTH_REFRESH_TOKEN_VALIDITY = <integer> ]
  [ NETWORK_POLICY = '<network_policy>' ]
  [ OAUTH_CLIENT_RSA_PUBLIC_KEY = <public_key1> ]
  [ OAUTH_CLIENT_RSA_PUBLIC_KEY_2 = <public_key2> ]
  [ IS_AGENTIC = { TRUE | FALSE } ]
  [ USE_PRIVATELINK_FOR_AUTHORIZATION_ENDPOINT = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters (all OAuth clients)

`name`
:   String that specifies the identifier (that is, name) for the integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes
    (for example, `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TYPE = OAUTH`
:   Specify the type of integration:

    - `OAUTH`: Creates a security interface between Snowflake and a client that supports OAuth.

`OAUTH_CLIENT = { CUSTOM | partner_application }`
:   Specify the client type:

    - `CUSTOM`: Creates an OAuth interface between Snowflake and a custom client.
    - `partner_application`: Creates an OAuth interface between Snowflake and a partner application. Supported values are:
      - `TABLEAU_DESKTOP`: Tableau Desktop version 2019.1 or higher.
      - `TABLEAU_SERVER`: Tableau Cloud. If Tableau Cloud is connecting to Snowflake using private connectivity to
        the Snowflake service, be sure to specify `OAUTH_CLIENT = CUSTOM` instead.
      - `LOOKER`: The Looker business intelligence tool.

`OAUTH_REDIRECT_URI = 'uri'`
:   Specifies the client URI. After a user is authenticated, the web browser is redirected to this URI.

    This parameter is required when `OAUTH_CLIENT = LOOKER`. For details, see the example in the
    [Looker documentation](https://docs.looker.com/setup-and-management/database-config/snowflake#oauth).

## Additional required parameters (custom clients)

Required only when OAUTH\_CLIENT = CUSTOM (that is, when creating an integration for a custom client)

`OAUTH_CLIENT_TYPE = { 'CONFIDENTIAL' | 'PUBLIC' }`
:   Specifies the type of client being registered. Snowflake supports both confidential and public clients. Confidential clients can store a
    secret. They run in a protected area where end users cannot access them. For example, a secured service deployed on the cloud could be a
    confidential client, whereas a client running on a desktop or distributed through an app store could be a public client.

`OAUTH_REDIRECT_URI = 'uri'`
:   Specifies the client URI. After a user is authenticated, the web browser is redirected to this URI. The URI must be protected by TLS
    (Transport Layer Security) unless the optional `OAUTH_ALLOW_NON_TLS_REDIRECT_URI` parameter is set to `TRUE`.

    Do not include query parameters sent with the redirect URI in the request to the
    [authorization endpoint](/user-guide/oauth-custom#label-oauth-authorization-endpoint). For example, if the value of the `redirect_uri` query parameter
    in the request to the authorization endpoint is `https://www.example.com/connect?authType=snowflake`, make sure the OAUTH\_REDIRECT\_URI
    parameter is set to `https://www.example.com/connect`.

## Optional parameters (all OAuth clients)

`ENABLED = { TRUE | FALSE }`
:   Specifies whether to initiate operation of the integration or suspend it.

    - `TRUE` enables the integration.
    - `FALSE` disables the integration for maintenance. Any integration between Snowflake and a third-party service fails to work.

    The value is case-insensitive.

    The default is `TRUE`.

`OAUTH_SINGLE_USE_REFRESH_TOKENS_REQUIRED = { TRUE | FALSE }`
:   Specifies whether [single-use refresh tokens](/user-guide/single-use-refresh-tokens) should be used.

    Default: `FALSE`

`USE_PRIVATELINK_FOR_AUTHORIZATION_ENDPOINT = { TRUE | FALSE }`
:   When TRUE, the interaction between Snowflake as the authorization server and the user who is authenticating uses
    [private connectivity](/user-guide/private-connectivity-inbound). Interactions between Snowflake and the client, including the
    initial request to the authorization endpoint, still happen over the public internet.

    Default: FALSE

`NETWORK_POLICY = 'network_policy'`
:   Specifies an existing [network policy](/user-guide/network-policies). This network policy controls network traffic that is
    attempting to exchange an authorization code for an access or refresh token, use a refresh token to obtain a new
    access token, or obtain Snowflake resources with an access token.

    For more information, see [Restricting network traffic for Snowflake OAuth](/user-guide/oauth-snowflake-overview#label-snow-oauth-network-policies).

## Additional optional parameters (partner applications)

Valid when OAUTH\_CLIENT = <partner\_application> (that is, when creating an integration for a partner application)

`OAUTH_ISSUE_REFRESH_TOKENS = { TRUE | FALSE }`
:   Boolean that specifies whether to allow the client to exchange a refresh token for an access token when the current access token has
    expired. If set to `FALSE`, a refresh token is not issued regardless of the integer value set in
    `OAUTH_REFRESH_TOKEN_VALIDITY`. User consent is revoked, and the user must confirm authorization again.

    Default: `TRUE`

    Note

    If this parameter is set to `FALSE` and the security integration also has `ENABLED = TRUE`, the Snowflake OAuth flow
    repeats and an access token is issued. The access token is valid for the duration specified by `OAUTH_ACCESS_TOKEN_VALIDITY`
    (600 seconds by default). After this access token expires, the user must authenticate again.

    Setting this parameter to `FALSE` and `ENABLED = FALSE` results in no tokens being issued and the integration is disabled.

`OAUTH_ACCESS_TOKEN_VALIDITY = integer`
:   Integer that specifies how long access tokens should be valid (in seconds).

    The supported minimum, maximum, and default values are as follows:

    - Minimum: `60` (1 minute)
    - Maximum: `3600` (1 hour)
    - Default: `600` (10 minutes)

`OAUTH_REFRESH_TOKEN_VALIDITY = integer`
:   Integer that specifies how long refresh tokens should be valid (in seconds). This can be used to expire the refresh token periodically.
    Note that OAUTH\_ISSUE\_REFRESH\_TOKENS must be set to `TRUE`.

    When a refresh token expires, the application will need to direct the user through the authorization flow again to obtain a new refresh
    token.

    The supported minimum, maximum, and default values are as follows:

    - Minimum: `3600` (1 hour)
    - Maximum: `7776000` (90 days)
    - Default: `7776000` (90 days)

    If you have a business need to lower the minimum value or raise the maximum value, ask your account administrator to send a request to
    [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

`OAUTH_USE_SECONDARY_ROLES = { IMPLICIT | NONE }`
:   - `IMPLICIT`: Default secondary roles set in the user properties are activated by default in the session being opened.
    - `NONE`: Default secondary roles are not supported in the session being opened.

    Default: `NONE`

`BLOCKED_ROLES_LIST = ( 'role_name' [ , 'role_name' , ... ] )`
:   Comma-separated list of Snowflake roles that a user cannot explicitly consent to using after authenticating
    (for example, `BLOCKED_ROLES_LIST = ('custom_role1', 'custom_role2')`). This restriction applies only to the primary role of the session.

    By default, Snowflake prevents the ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, and SECURITYADMIN roles from authenticating. To allow these
    privileged roles to authenticate, use the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command to set the [OAUTH\_ADD\_PRIVILEGED\_ROLES\_TO\_BLOCKED\_LIST](/sql-reference/parameters#label-oauth-add-privileged-roles-to-blocked-list) account parameter to `FALSE`.

`ALLOWED_ROLES_LIST = ( 'role_name' [ , 'role_name' , ... ] )`
:   Comma-separated list of Snowflake roles that a user can consent to an application or service to use
    on their behalf via Snowflake OAuth (for example, `'custom_role1', 'custom_role2'`). When this parameter is set, only roles in the
    list can be used by a service using the security integration to access Snowflake data; all other roles are implicitly blocked. The
    user must consent to the role before the service can use it. This parameter is complementary to `BLOCKED_ROLES_LIST`. If both are
    specified, a role must be in `ALLOWED_ROLES_LIST` and not in `BLOCKED_ROLES_LIST` to be used.

    This parameter can only be set when `OAUTH_USE_SECONDARY_ROLES` is set to `NONE` (the default). If `OAUTH_USE_SECONDARY_ROLES` were
    set to `IMPLICIT`, the user’s default secondary roles would be auto-activated in the session and could include roles outside
    `ALLOWED_ROLES_LIST`, which would defeat the purpose of the list.

    Default: empty list (all roles other than those in `BLOCKED_ROLES_LIST` are allowed)

`COMMENT = 'string_literal'`
:   Specifies a comment for the integration.

    Default: No value

## Additional optional parameters (custom clients)

Valid when OAUTH\_CLIENT = CUSTOM (that is, when creating an integration for a custom client)

`OAUTH_ALLOW_NON_TLS_REDIRECT_URI = { TRUE | FALSE }`
:   If `TRUE`, allows setting `OAUTH_REDIRECT_URI` to a URI not protected by TLS. We highly recommend use of TLS to
    prevent man-in-the-middle OAuth redirects for use in phishing attacks.

    Default: `FALSE`

`OAUTH_ALTERNATE_REDIRECT_URIS = ( 'uri' [ , 'uri' , ... ] )`
:   Comma-separated list of additional client redirect URIs accepted by the integration. The URI in the client’s authorization request
    must match either `OAUTH_REDIRECT_URI` or one of the URIs in `OAUTH_ALTERNATE_REDIRECT_URIS`. Use this parameter when a single
    integration must serve clients that are reached at multiple URIs (for example, multiple environments or hostnames).

    Each URI must be protected by TLS unless `OAUTH_ALLOW_NON_TLS_REDIRECT_URI` is set to `TRUE`.

    Default: empty list

`OAUTH_ENFORCE_PKCE = { TRUE | FALSE }`
:   Boolean that specifies whether Proof Key for Code Exchange (PKCE) should be required for the integration.

    By default, PKCE is optional and is enforced only if the `code_challenge` and `code_challenge_method` parameters are both
    included in the authorization endpoint URL. However, we highly recommend that your client require PKCE for all authorizations
    to make the OAuth flow more secure. For more information, see [Configure Snowflake OAuth for custom clients](/user-guide/oauth-custom).

    Default: `FALSE`

`OAUTH_ENABLE_ROLE_SELECTION = { TRUE | FALSE }`
:   [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

    Controls whether the user can choose the role(s) for the session during the OAuth authorization flow, instead of the
    integration using the user’s default role. When `TRUE`, if the client does not request a specific role (that is, no
    `session:role:role_name` scope), Snowflake presents a role-selection step during authorization where the user consents to one or more
    roles or to all of their roles. The session is bound to the consented set: it can use only those roles, and role switching (with
    `USE ROLE`) is limited to the consented roles. Selectable roles are bounded by the roles granted to the user
    and the integration’s `ALLOWED_ROLES_LIST` and `BLOCKED_ROLES_LIST`.

    For more information, see [Letting users select roles during authorization](/user-guide/oauth-custom#label-oauth-custom-role-selection).

    Default: `FALSE`

`OAUTH_USE_SECONDARY_ROLES = { IMPLICIT | NONE }`
:   - `IMPLICIT`: Default secondary roles set in the user properties are activated by default in the session being opened.
    - `NONE`: Default secondary roles are not supported in the session being opened.

    Default: `NONE`

`PRE_AUTHORIZED_ROLES_LIST = ( 'role_name' [ , 'role_name' , ... ] )`
:   Comma-separated list of Snowflake roles that a user does not need to explicitly consent to using after authenticating (for example,
    `PRE_AUTHORIZED_ROLES_LIST = ('custom_role1', 'custom_role2')`). The ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, and
    SECURITYADMIN roles cannot be included in this list.

    Note

    This parameter is supported for confidential clients only.

`BLOCKED_ROLES_LIST = ( 'role_name' [ , 'role_name' , ... ] )`
:   Comma-separated list of Snowflake roles that a user cannot explicitly consent to using after authenticating. For example,
    `BLOCKED_ROLES_LIST = ('custom_role1', 'custom_role2')`. This restriction applies only to the primary role of the session.

    The ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, and SECURITYADMIN roles are included in this list by default; however, if these roles should
    be removed for your account, ask your account administrator to send a request to [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

`ALLOWED_ROLES_LIST = ( 'role_name' [ , 'role_name' , ... ] )`
:   Comma-separated list of Snowflake roles that a user can consent to an application or service to use
    on their behalf via Snowflake OAuth (for example, `'custom_role1', 'custom_role2'`). When this parameter is set, only roles in the
    list can be used by a service using the security integration to access Snowflake data; all other roles are implicitly blocked. The
    user must consent to the role before the service can use it. This parameter is complementary to `BLOCKED_ROLES_LIST`. If both are
    specified, a role must be in `ALLOWED_ROLES_LIST` and not in `BLOCKED_ROLES_LIST` to be used.

    This parameter can only be set when `OAUTH_USE_SECONDARY_ROLES` is set to `NONE` (the default). If `OAUTH_USE_SECONDARY_ROLES` were
    set to `IMPLICIT`, the user’s default secondary roles would be auto-activated in the session and could include roles outside
    `ALLOWED_ROLES_LIST`, which would defeat the purpose of the list.

    Default: empty list (all roles other than those in `BLOCKED_ROLES_LIST` are allowed)

`OAUTH_ANY_ROLE_MODE = { DISABLE | ENABLE | ENABLE_FOR_PRIVILEGE }`
:   [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

    Available to all accounts.

    Controls whether a client or user can switch the session’s primary role (using `USE ROLE role;`) to a role
    other than the one bound to the OAuth access token. To switch roles, the client must also request the `session:role-any` scope in the
    authorization request. Role switching is always restricted to roles granted to the user and permitted by `ALLOWED_ROLES_LIST` and
    `BLOCKED_ROLES_LIST`.

    - `DISABLE` does not allow the client or user to switch roles (that is, `USE ROLE role;`). Default.
    - `ENABLE` allows the client or user to switch roles.
    - `ENABLE_FOR_PRIVILEGE` allows the client or user to switch roles only for a client or user with the `USE_ANY_ROLE`
      privilege on the integration. This privilege can be granted and revoked to one or more roles available to the user. For example:

      Copy code

      ```
      GRANT USE_ANY_ROLE ON INTEGRATION oauth_custom_1 TO role1;
      ```

      Copy code

      ```
      REVOKE USE_ANY_ROLE ON INTEGRATION oauth_custom_1 FROM role1;
      ```

    This parameter applies only to the primary role of the session; secondary roles are controlled separately by
    `OAUTH_USE_SECONDARY_ROLES`. You can only set this parameter when `OAUTH_CLIENT = CUSTOM`. The value can be optionally enclosed in
    single quotes (for example, either `DISABLE` or `'DISABLE'`).

    Default: `DISABLE`

`OAUTH_ISSUE_REFRESH_TOKENS = { TRUE | FALSE }`
:   Boolean that specifies whether to allow the client to exchange a refresh token for an access token when the current access token has
    expired. If set to `FALSE`, a refresh token is not issued. User consent is revoked, and the user must confirm authorization again.

    Default: `TRUE`

`OAUTH_ACCESS_TOKEN_VALIDITY = integer`
:   Integer that specifies how long access tokens should be valid (in seconds).

    The supported minimum, maximum, and default values are as follows:

    - Minimum: `60` (1 minute)
    - Maximum: `3600` (1 hour)
    - Default: `600` (10 minutes)

`OAUTH_REFRESH_TOKEN_VALIDITY = integer`
:   Integer that specifies how long refresh tokens should be valid (in seconds). This can be used to expire the refresh token periodically.
    Note that OAUTH\_ISSUE\_REFRESH\_TOKENS must be set to `TRUE`.

    Note that if your organization would like the minimum or maximum values lowered or raised, respectively, ask your account administrator
    to send a request to [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

    Values:
    :   `86400` (1 day) to `7776000` (90 days)

    Default:
    :   `7776000`

`NETWORK_POLICY = 'network_policy'`
:   Specifies an existing [network policy](/user-guide/network-policies). This network policy controls network traffic that is
    attempting to exchange an authorization code for an access or refresh token, use a refresh token to obtain a new
    access token, or obtain Snowflake resources with an access token.

    For more information, see [Restricting network traffic for Snowflake OAuth](/user-guide/oauth-snowflake-overview#label-snow-oauth-network-policies).

    `network_policy` is a string literal that you must enclose in single quotes. If the network policy name is
    [case-sensitive or includes any special characters or spaces](/sql-reference/identifiers-syntax#label-delimited-identifier), then you must enclose the
    name in double quotes, and then enclose the double-quoted name in single quotes. For example,
    `NETWORK_POLICY = '"Case-Sensitive Name"'`.

`OAUTH_CLIENT_RSA_PUBLIC_KEY = public_key1`
:   Specifies an RSA public key.

`OAUTH_CLIENT_RSA_PUBLIC_KEY_2 = public_key2`
:   Specifies a second RSA public key. Used for key rotation.

`IS_AGENTIC = { TRUE | FALSE }`
:   Specifies whether sessions authenticated through this integration should be treated as agent sessions.

    When set to `TRUE`, Snowflake automatically recognizes all sessions authenticated through this integration as agent sessions, causing [IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated) to return `TRUE` for those sessions.

    Default: `FALSE`

`COMMENT = 'string_literal'`
:   Specifies a comment for the integration.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

### Tableau Desktop example

The following example creates an OAuth integration with the default settings:

> Copy code
>
> ```
> CREATE SECURITY INTEGRATION td_oauth_int1
>   TYPE = oauth
>   ENABLED = true
>   OAUTH_CLIENT = tableau_desktop;
> ```

View the integration settings using [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration):

Copy code

```
DESC SECURITY INTEGRATION td_oauth_int1;
```

The following example creates an OAuth integration with refresh tokens that expire after 10 hours (36000 seconds). The integration blocks
users from starting a session with SYSADMIN as the active role:

> Copy code
>
> ```
> CREATE SECURITY INTEGRATION td_oauth_int2
>   TYPE = oauth
>   ENABLED = true
>   OAUTH_CLIENT = tableau_desktop
>   OAUTH_REFRESH_TOKEN_VALIDITY = 36000
>   BLOCKED_ROLES_LIST = ('SYSADMIN');
> ```

### Tableau Cloud example

The following example creates an OAuth integration with the default settings:

> Copy code
>
> ```
> CREATE SECURITY INTEGRATION ts_oauth_int1
>   TYPE = oauth
>   ENABLED = true
>   OAUTH_CLIENT = tableau_server;
> ```

View the integration settings using [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration):

Copy code

```
DESC SECURITY INTEGRATION ts_oauth_int1;
```

The following example creates an OAuth integration with refresh tokens that expire after 1 day (86400 seconds). The integration blocks
users from starting a session with SYSADMIN as the active role:

> Copy code
>
> ```
> CREATE SECURITY INTEGRATION ts_oauth_int2
>   TYPE = oauth
>   ENABLED = true
>   OAUTH_CLIENT = tableau_server
>   OAUTH_REFRESH_TOKEN_VALIDITY = 86400
>   BLOCKED_ROLES_LIST = ('SYSADMIN');
> ```

### Custom client example

The following example creates an OAuth integration that uses key pair authentication. The integration allows refresh tokens, which expire
after 1 day (86400 seconds). The integration blocks users from starting a session with SYSADMIN as the active role:

> Copy code
>
> ```
> CREATE SECURITY INTEGRATION oauth_kp_int
>   TYPE = oauth
>   ENABLED = true
>   OAUTH_CLIENT = custom
>   OAUTH_CLIENT_TYPE = 'CONFIDENTIAL'
>   OAUTH_REDIRECT_URI = 'https://localhost.com'
>   OAUTH_ISSUE_REFRESH_TOKENS = TRUE
>   OAUTH_REFRESH_TOKEN_VALIDITY = 86400
>   PRE_AUTHORIZED_ROLES_LIST = ('MYROLE')
>   BLOCKED_ROLES_LIST = ('SYSADMIN');
> ```
