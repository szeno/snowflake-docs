# CREATE SECURITY INTEGRATION (OIDC)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates a new OIDC security integration in the account or replaces an existing integration. An OIDC security integration provides
single sign-on (SSO) workflows by creating an interface between Snowflake and an OpenID Connect identity provider (IdP).

For information about creating other types of security integrations (for example, SAML2), see [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration).

For conceptual information and configuration walkthroughs, see [Configuring OpenID Connect (OIDC) federated authentication](/user-guide/admin-security-fed-auth-oidc).

See also:
:   [ALTER SECURITY INTEGRATION (OIDC)](/sql-reference/sql/alter-security-integration-oidc) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations) , [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

## Syntax

The required parameters depend on the value of `OIDC_PROVIDER`:

- When `OIDC_PROVIDER='CUSTOM'`, you must specify `OIDC_ISSUER`, `OIDC_CLIENT_ID`, and `OIDC_CLIENT_SECRET`.
- When `OIDC_PROVIDER='GOOGLE'` or `OIDC_PROVIDER='MICROSOFT'`, do not specify `OIDC_ISSUER`, `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`, `OIDC_SCOPES`, the endpoint parameters, the user-mapping parameters (`OIDC_TOKEN_USER_MAPPING_CLAIM`, `OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE`), or `OIDC_LOGIN_PAGE_LABEL`. Snowflake manages these for the managed provider, fixes user mapping to the `email` claim → `EMAIL_ADDRESS`, and displays the official provider logo and default login label (for example, Sign in with Microsoft).
- Each managed provider requires its own sign-in allow-list: `OIDC_PROVIDER='GOOGLE'` requires `OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS`, and `OIDC_PROVIDER='MICROSOFT'` requires `OIDC_ALLOWED_MSFT_TENANTS`. Each option applies only to its own provider, so specifying the other provider’s option, or either option with `OIDC_PROVIDER='CUSTOM'`, causes the CREATE to fail.

### Custom provider

Copy code

```
CREATE [ OR REPLACE ] SECURITY INTEGRATION [ IF NOT EXISTS ]
    <name>
    TYPE = OIDC
    [ ENABLED = { TRUE | FALSE } ]
    OIDC_PROVIDER = 'CUSTOM'
    OIDC_ISSUER = '<string_literal>'
    OIDC_CLIENT_ID = '<string_literal>'
    OIDC_CLIENT_SECRET = '<string_literal>'
    OIDC_TOKEN_USER_MAPPING_CLAIM = '<string_literal>'
    OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = { 'LOGIN_NAME' | 'EMAIL_ADDRESS' }
    [ OIDC_LOGIN_PAGE_LABEL = '<string_literal>' ]
    [ OIDC_ENABLE_SSO_LOGIN_PAGE = { TRUE | FALSE } ]
    [ OIDC_SCOPES = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ OIDC_AUTHORIZATION_ENDPOINT = '<string_literal>' ]
    [ OIDC_TOKEN_ENDPOINT = '<string_literal>' ]
    [ OIDC_JWKS_URI = '<string_literal>' ]
    [ OIDC_USERINFO_ENDPOINT = '<string_literal>' ]
    [ ALLOWED_USER_DOMAINS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ ALLOWED_EMAIL_PATTERNS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ COMMENT = '<string_literal>' ]
```

### Managed provider (Google)

Copy code

```
CREATE [ OR REPLACE ] SECURITY INTEGRATION [ IF NOT EXISTS ]
    <name>
    TYPE = OIDC
    [ ENABLED = { TRUE | FALSE } ]
    OIDC_PROVIDER = 'GOOGLE'
    OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS = ( '<string_literal>' [ , '<string_literal>' , ... ] )
    [ OIDC_ENABLE_SSO_LOGIN_PAGE = { TRUE | FALSE } ]
    [ ALLOWED_USER_DOMAINS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ ALLOWED_EMAIL_PATTERNS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ COMMENT = '<string_literal>' ]
```

### Managed provider (Microsoft)

Copy code

```
CREATE [ OR REPLACE ] SECURITY INTEGRATION [ IF NOT EXISTS ]
    <name>
    TYPE = OIDC
    [ ENABLED = { TRUE | FALSE } ]
    OIDC_PROVIDER = 'MICROSOFT'
    OIDC_ALLOWED_MSFT_TENANTS = ( '<string_literal>' [ , '<string_literal>' , ... ] )
    [ OIDC_ENABLE_SSO_LOGIN_PAGE = { TRUE | FALSE } ]
    [ ALLOWED_USER_DOMAINS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ ALLOWED_EMAIL_PATTERNS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (that is, name) for the integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and can’t contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TYPE = OIDC`
:   Specify the type of integration:

    - `OIDC`: Creates a security interface between Snowflake and an OpenID Connect identity provider.

`OIDC_PROVIDER = { 'CUSTOM' | 'GOOGLE' | 'MICROSOFT' }`
:   The identity provider type. Valid values:

    - `CUSTOM`: Any OpenID Connect-compliant identity provider. You provide client credentials and either an issuer URL (for endpoint discovery) or explicit endpoints.
    - `GOOGLE`: Google as a managed provider. Snowflake manages the OAuth client configuration.
    - `MICROSOFT`: Microsoft as a managed provider. Snowflake manages the OAuth client configuration for Microsoft Entra ID.

    Default: `CUSTOM`.

    Immutable after creation. To change the provider, drop and recreate the integration.

    Case-insensitive.

### Required parameters (custom providers only)

The following parameters are required when `OIDC_PROVIDER='CUSTOM'`. They are rejected for managed providers (`GOOGLE`, `MICROSOFT`). For managed providers, Snowflake fixes user mapping to the `email` claim → `EMAIL_ADDRESS`, so the mapping parameters can’t be set. Users must verify their email in the IdP tenant; see [Verified email requirement](/user-guide/admin-security-fed-auth-oidc#label-oidc-verified-email).

`OIDC_ISSUER = 'string_literal'`
:   The IdP issuer URL. Must be HTTPS. Used for token validation and endpoint discovery.

    Immutable after creation.

`OIDC_CLIENT_ID = 'string_literal'`
:   The OAuth 2.0 client ID registered with the IdP.

    Immutable after creation.

`OIDC_CLIENT_SECRET = 'string_literal'`
:   The OAuth 2.0 client secret registered with the IdP. Encrypted at rest. Not returned by [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration). Can be rotated using [ALTER SECURITY INTEGRATION (OIDC)](/sql-reference/sql/alter-security-integration-oidc).

`OIDC_TOKEN_USER_MAPPING_CLAIM = 'string_literal'`
:   The ID token claim used to identify the Snowflake user. Specify a single claim name (for example, `'email'`), or an ordered list of claim
    names (for example, `('email', 'sub')`). Custom claim names are also accepted. Only string-valued claims are supported; a non-string claim
    (number, boolean, or object) is stringified and typically won’t match any Snowflake user attribute.

    When you specify a list, Snowflake extracts all non-empty values from the listed claims in order, then attempts user lookup with each value
    against `OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE`, using the first successful match. If a claim is absent from the ID token, Snowflake skips it
    and tries the next.

`OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = { 'LOGIN_NAME' | 'EMAIL_ADDRESS' }`
:   The Snowflake user attribute to match against the token claim value. For `EMAIL_ADDRESS`, additional rules apply; see
    [Verified email requirement](/user-guide/admin-security-fed-auth-oidc#label-oidc-verified-email).

### Required parameters (managed providers only)

Each managed provider requires an allow-list that restricts which identity provider organization can sign in through the integration. These
options are required at creation and optional on [ALTER SECURITY INTEGRATION (OIDC)](/sql-reference/sql/alter-security-integration-oidc).

`OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS = ( 'string_literal' [ , 'string_literal' , ... ] )`
:   The Google Workspace hosted domains allowed to sign in through this integration, checked against the `hd` claim in the ID token. Required when
    `OIDC_PROVIDER='GOOGLE'`.

    Each entry is either a hosted domain (for example, `'mycompany.com'`) or the literal `'personal'`, which allows personal or unmanaged Google
    accounts, whose ID tokens carry no `hd` claim. Matching is case-insensitive. The list can’t be empty.

`OIDC_ALLOWED_MSFT_TENANTS = ( 'string_literal' [ , 'string_literal' , ... ] )`
:   The Microsoft Entra ID tenants allowed to sign in through this integration, checked against the `tid` claim in the ID token. Required when
    `OIDC_PROVIDER='MICROSOFT'`.

    Each entry is either a tenant UUID (for example, `'a1b2c3d4-e5f6-4789-a012-3456789abcde'`) or the literal `'personal'`, which allows personal
    Microsoft accounts. Matching is case-insensitive. The list can’t be empty.

## Optional parameters

`ENABLED = { TRUE | FALSE }`
:   Whether the integration is active. Set to `TRUE` to expose the integration on the login page (subject to `OIDC_ENABLE_SSO_LOGIN_PAGE` and any allow-lists).

    Default: `TRUE`.

`OIDC_SCOPES = ( 'string_literal' [ , 'string_literal' , ... ] )`
:   The OAuth scopes to request. Must include `openid`.

    Default: `('openid', 'profile', 'email')`.

    Custom providers only. Managed providers reject this option.

`OIDC_AUTHORIZATION_ENDPOINT = 'string_literal'`
:   The IdP authorization endpoint URL. If not provided, discovered from the issuer metadata. Must be HTTPS.

    Immutable after creation. Custom providers only.

`OIDC_TOKEN_ENDPOINT = 'string_literal'`
:   The IdP token endpoint URL. If not provided, discovered from the issuer metadata. Must be HTTPS.

    Immutable after creation. Custom providers only.

`OIDC_JWKS_URI = 'string_literal'`
:   The IdP JWKS (JSON Web Key Set) endpoint URL for ID token signature verification. If not provided, discovered from the issuer metadata. Must be HTTPS.

    Immutable after creation. Custom providers only.

`OIDC_USERINFO_ENDPOINT = 'string_literal'`
:   The IdP UserInfo endpoint URL. Reserved for forward compatibility. Snowflake does not call this endpoint during authentication in the
    current release. User resolution uses claims in the ID token only (`OIDC_TOKEN_USER_MAPPING_CLAIM`); there is no UserInfo fallback for
    missing claims. If not provided, Snowflake may populate this value from issuer discovery metadata. The URL must use HTTPS. Returned by
    [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) only when set or discovered. Custom providers only.

`OIDC_LOGIN_PAGE_LABEL = 'string_literal'`
:   The label displayed on the Snowflake login page for this IdP (for example, `Sign in with Okta`). If not provided, the integration name is used as the label. Custom providers only. For managed providers (`GOOGLE`, `MICROSOFT`), Snowflake displays the official provider logo and a default label (for example, Sign in with Google).

`OIDC_ENABLE_SSO_LOGIN_PAGE = { TRUE | FALSE }`
:   Whether to display this integration on the Snowflake login page. When `FALSE`, the integration exists and is enabled but is not rendered as a **Sign in with X** button.

    Default: `TRUE`.

`ALLOWED_USER_DOMAINS = ( 'string_literal' [ , 'string_literal' , ... ] )`
:   Restricts authentication to users whose email domain exactly matches one of the specified domains (for example, `('mycompany.com', 'subsidiary.com')`). Matching is case-insensitive and exact: `mycompany.com` matches `user@mycompany.com` but not `user@evil-mycompany.com` or `user@mycompany.com.attacker.com`. The filter applies both at the login-page selection step and at user resolution after the IdP returns.

    This parameter can be used to associate a user with an IdP for configurations that use multiple IdPs. For details, see [Using multiple identity providers for federated authentication](/user-guide/admin-security-fed-auth-security-integration-multiple).

`ALLOWED_EMAIL_PATTERNS = ( 'string_literal' [ , 'string_literal' , ... ] )`
:   Restricts authentication to users whose email matches one of the specified regex patterns. Patterns use Java `Pattern.find()` semantics. Anchor with `^...$` for full-string matching.

    Requires the `ENABLE_IDENTIFIER_FIRST_LOGIN` account parameter to be enabled.

    This parameter can be used to associate a user with an IdP for configurations that use multiple IdPs. For details, see [Using multiple identity providers for federated authentication](/user-guide/admin-security-fed-auth-security-integration-multiple).

`COMMENT = 'string_literal'`
:   Specifies a comment for the integration.

    Default: No value

### Read-only properties

The following property is returned by [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) but can’t be set in a CREATE or ALTER command:

`OIDC_REDIRECT_URIS`
:   The callback URL(s) that Snowflake generates for this account. This property is always a list. Provide the appropriate URL to your IdP when
    registering Snowflake as a custom OAuth client. For custom providers the format is `https://<account_url>/oauth2/oidc/callback`. An account
    may expose more than one callback host (for example, account-locator, organization, and Private Link URLs), so register each URI your users
    might connect through. For managed providers, [DESC INTEGRATION](/sql-reference/sql/desc-integration) returns the Snowflake-managed callback
    host (typically `https://identity.snowflake.com/oauth2/callback`); you do not register it with the IdP.

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

- Unless [identifier-first login](/user-guide/identifier-first-login) is enabled, only one SSO integration (SAML2 or OIDC) can be `ENABLED=TRUE` at a time. For details, see [Configuring an OIDC security integration](/user-guide/admin-security-fed-auth-oidc#label-oidc-sso-create-integration).
- For managed providers (`OIDC_PROVIDER='GOOGLE'` or `OIDC_PROVIDER='MICROSOFT'`), you can’t set `OIDC_ISSUER`, `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`, `OIDC_SCOPES`, the endpoint parameters (`OIDC_AUTHORIZATION_ENDPOINT`, `OIDC_TOKEN_ENDPOINT`, `OIDC_JWKS_URI`, `OIDC_USERINFO_ENDPOINT`), the user-mapping parameters (`OIDC_TOKEN_USER_MAPPING_CLAIM`, `OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE`), or `OIDC_LOGIN_PAGE_LABEL`. Snowflake manages these values, fixes user mapping to the `email` claim → `EMAIL_ADDRESS`, and displays the official provider logo and default login label. Setting any of these options causes the CREATE or ALTER statement to fail.
- Each managed provider requires its own allow-list at creation: `OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS` for `OIDC_PROVIDER='GOOGLE'`, and `OIDC_ALLOWED_MSFT_TENANTS` for `OIDC_PROVIDER='MICROSOFT'`. See [Required parameters (managed providers only)](#label-create-security-integration-oidc-managed-required-parameters).
- If you signed up for your Snowflake account using Google or Microsoft, Snowflake populates the allow-list of the managed OIDC integration it creates during account creation, from the hosted domain (Google) or tenant (Microsoft) in the ID token you signed up with. See [Creating a managed OIDC integration (Google)](/user-guide/admin-security-fed-auth-oidc#label-oidc-google-managed-provider).
- If you do not provide the endpoint parameters (`OIDC_AUTHORIZATION_ENDPOINT`, `OIDC_TOKEN_ENDPOINT`, `OIDC_JWKS_URI`), Snowflake automatically discovers them from the issuer’s `.well-known/openid-configuration` metadata document. See [OpenID Connect discovery](/user-guide/admin-security-fed-auth-oidc#label-oidc-discovery). If you provide some but not all of the three required endpoints, the CREATE is rejected.
- If you create an integration with placeholder credentials before retrieving the real client ID from your IdP, and the real client ID does not match the placeholder, you must drop the integration and recreate it with the real value.
- The following properties are immutable after creation. To change any of them, drop the integration and recreate it: `OIDC_PROVIDER`, `OIDC_ISSUER`, `OIDC_CLIENT_ID`, `OIDC_AUTHORIZATION_ENDPOINT`, `OIDC_TOKEN_ENDPOINT`, `OIDC_JWKS_URI`. The read-only `OIDC_REDIRECT_URIS` property is generated by Snowflake and can’t be set.

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Example

### Custom provider

Copy code

```
CREATE SECURITY INTEGRATION my_okta_oidc
  TYPE = OIDC
  ENABLED = TRUE
  OIDC_PROVIDER = 'CUSTOM'
  OIDC_ISSUER = 'https://mycompany.okta.com/oauth2/default'
  OIDC_CLIENT_ID = '0oab1cdef2ghij3klm4n'
  OIDC_CLIENT_SECRET = 'AbCdEfGhIjKlMnOpQrStUvWxYz0123456789'
  OIDC_TOKEN_USER_MAPPING_CLAIM = 'email'
  OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = 'EMAIL_ADDRESS'
  OIDC_LOGIN_PAGE_LABEL = 'Sign in with Okta';
```

### Custom provider with explicit endpoints

Copy code

```
CREATE SECURITY INTEGRATION my_okta_oidc
  TYPE = OIDC
  ENABLED = TRUE
  OIDC_PROVIDER = 'CUSTOM'
  OIDC_ISSUER = 'https://okta.mycompany.com/oauth2/default'
  OIDC_CLIENT_ID = '0oab1cdef2ghij3klm4n'
  OIDC_CLIENT_SECRET = 'AbCdEfGhIjKlMnOpQrStUvWxYz0123456789'
  OIDC_AUTHORIZATION_ENDPOINT = 'https://mycompany.okta.com/oauth2/default/v1/authorize'
  OIDC_TOKEN_ENDPOINT = 'https://mycompany.okta.com/oauth2/default/v1/token'
  OIDC_JWKS_URI = 'https://mycompany.okta.com/oauth2/default/v1/keys'
  OIDC_TOKEN_USER_MAPPING_CLAIM = 'preferred_username'
  OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = 'LOGIN_NAME'
  OIDC_SCOPES = ('openid', 'profile', 'email')
  OIDC_LOGIN_PAGE_LABEL = 'Sign in with okta';
```

### Managed provider (Google)

Copy code

```
CREATE SECURITY INTEGRATION my_google_oidc
  TYPE = OIDC
  ENABLED = TRUE
  OIDC_PROVIDER = 'GOOGLE'
  OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS = ('mycompany.com', 'subsidiary.com');
```

### Managed provider (Microsoft)

Copy code

```
CREATE SECURITY INTEGRATION my_microsoft_oidc
  TYPE = OIDC
  ENABLED = TRUE
  OIDC_PROVIDER = 'MICROSOFT'
  OIDC_ALLOWED_MSFT_TENANTS = ('a1b2c3d4-e5f6-4789-a012-3456789abcde');
```

View the integration settings using [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration):

> Copy code
>
> ```
> DESC SECURITY INTEGRATION my_okta_oidc;
> ```

The command returns one row per integration property with the columns `property`, `property_type`, `property_value`, and
`property_default`. `OIDC_CLIENT_SECRET` is never returned.

Output behavior:

- `OIDC_REDIRECT_URIS` is always returned. For custom providers, the value lists one or more callback URLs of the form
  `https://<account_identifier>.snowflakecomputing.com/oauth2/oidc/callback`.
- `OIDC_PROVIDER` is always returned. If you omit it in CREATE, the value is `CUSTOM`.
- `COMMENT` is always returned, even when unset (empty `property_value`).
- `OIDC_USERINFO_ENDPOINT` appears only when you set it explicitly or when issuer discovery populates it. It is omitted from output for
  minimal integrations that do not use it.
- `ALLOWED_USER_DOMAINS` and `ALLOWED_EMAIL_PATTERNS` appear only when configured.
- `OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS` is returned only for `OIDC_PROVIDER='GOOGLE'`, and `OIDC_ALLOWED_MSFT_TENANTS` only for
  `OIDC_PROVIDER='MICROSOFT'`. `OIDC_ALLOWED_MSFT_TENANTS` returns the `'personal'` literal rather than the underlying consumer tenant UUID.
  List order isn’t preserved.
- For `OIDC_SCOPES`, `property_default` shows the framework default (`[openid, profile, email]`) and `property_value` shows the configured
  value.
- For boolean properties with defaults (for example, `ENABLED`, `OIDC_ENABLE_SSO_LOGIN_PAGE`), `property_default` reflects the CREATE default
  (`true`).

### Custom provider (`OIDC_PROVIDER='CUSTOM'`)

The following example shows output for a fully configured custom integration (representative values):

| property | property\_type | property\_value | property\_default |
| --- | --- | --- | --- |
| ENABLED | Boolean | true | true |
| OIDC\_ISSUER | String | <https://okta.mycompany.com/oauth2/default> |  |
| OIDC\_CLIENT\_ID | String | 0oab1cdef2ghij3klm4n |  |
| OIDC\_JWKS\_URI | String | <https://mycompany.okta.com/oauth2/default/v1/keys> |  |
| OIDC\_AUTHORIZATION\_ENDPOINT | String | <https://mycompany.okta.com/oauth2/default/v1/authorize> |  |
| OIDC\_TOKEN\_ENDPOINT | String | <https://mycompany.okta.com/oauth2/default/v1/token> |  |
| OIDC\_USERINFO\_ENDPOINT | String | <https://mycompany.okta.com/oauth2/default/v1/userinfo> |  |
| OIDC\_SCOPES | List | [openid, profile, email, groups] | [openid, profile, email] |
| OIDC\_REDIRECT\_URIS | List | [<https://mycompany.snowflakecomputing.com/oauth2/oidc/callback>] |  |
| OIDC\_ENABLE\_SSO\_LOGIN\_PAGE | Boolean | true | true |
| OIDC\_LOGIN\_PAGE\_LABEL | String | Sign in with Okta |  |
| OIDC\_PROVIDER | String | CUSTOM |  |
| OIDC\_TOKEN\_USER\_MAPPING\_CLAIM | List | [email, sub] |  |
| OIDC\_SNOWFLAKE\_USER\_MAPPING\_ATTRIBUTE | String | EMAIL\_ADDRESS |  |
| COMMENT | String | Test custom OIDC integration |  |

Expand

Show lessSee more

`OIDC_TOKEN_USER_MAPPING_CLAIM` is returned as a list when multiple claims are configured (for example, `[email, sub]`).

### Managed provider (`OIDC_PROVIDER='GOOGLE'` or `OIDC_PROVIDER='MICROSOFT'`)

Managed integrations return a smaller property set. Snowflake-managed OAuth settings are not exposed as separate properties. The following example shows output for `OIDC_PROVIDER='GOOGLE'`; for `MICROSOFT`, the property set is the same except that `OIDC_PROVIDER` is `MICROSOFT` and the allow-list property is `OIDC_ALLOWED_MSFT_TENANTS`.

```
+--------------------------------+---------------+------------------------------------------+------------------+
| property                       | property_type | property_value                             | property_default |
|--------------------------------+---------------+------------------------------------------+------------------|
| ENABLED                        | Boolean       | true                                     | true             |
| OIDC_REDIRECT_URIS             | List          | [https://identity.snowflake.com/oauth2/callback] |          |
| OIDC_ENABLE_SSO_LOGIN_PAGE     | Boolean       | true                                     | true             |
| OIDC_PROVIDER                  | String        | GOOGLE                                   |                  |
| OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS | List      | [mycompany.com, subsidiary.com]          |                  |
| OIDC_TOKEN_USER_MAPPING_CLAIM  | String        | email                                    |                  |
| OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE | String | EMAIL_ADDRESS                            |                  |
| COMMENT                        | String        |                                          |                  |
+--------------------------------+---------------+------------------------------------------+------------------+
```
