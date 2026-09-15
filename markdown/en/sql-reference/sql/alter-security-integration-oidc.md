# ALTER SECURITY INTEGRATION (OIDC)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Modifies the properties of an existing OIDC security integration. For information about modifying other types of
security integrations (for example, SAML2), see [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration).

For conceptual information, see [Configuring OpenID Connect (OIDC) federated authentication](/user-guide/admin-security-fed-auth-oidc).

See also:
:   [CREATE SECURITY INTEGRATION (OIDC)](/sql-reference/sql/create-security-integration-oidc), [DROP INTEGRATION](/sql-reference/sql/drop-integration), [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations), [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

## Syntax

Copy code

```
ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name> SET
    [ ENABLED = { TRUE | FALSE } ]
    [ OIDC_CLIENT_SECRET = '<string_literal>' ]
    [ OIDC_SCOPES = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ OIDC_USERINFO_ENDPOINT = '<string_literal>' ]
    [ OIDC_ENABLE_SSO_LOGIN_PAGE = { TRUE | FALSE } ]
    [ OIDC_LOGIN_PAGE_LABEL = '<string_literal>' ]
    [ OIDC_TOKEN_USER_MAPPING_CLAIM = '<string_literal>' ]
    [ OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = { 'LOGIN_NAME' | 'EMAIL_ADDRESS' } ]
    [ ALLOWED_USER_DOMAINS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ ALLOWED_EMAIL_PATTERNS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ OIDC_ALLOWED_MSFT_TENANTS = ( '<string_literal>' [ , '<string_literal>' , ... ] ) ]
    [ COMMENT = '<string_literal>' ]

ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name> UNSET {
    ALLOWED_EMAIL_PATTERNS |
    ALLOWED_USER_DOMAINS |
    COMMENT |
    ENABLED |
    OIDC_ENABLE_SSO_LOGIN_PAGE |
    OIDC_LOGIN_PAGE_LABEL |
    OIDC_SCOPES |
    OIDC_USERINFO_ENDPOINT |
    [ , ... ]
    }

ALTER [ SECURITY ] INTEGRATION <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER [ SECURITY ] INTEGRATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   Identifier for the integration to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`SET ...`
:   Specifies one or more properties or parameters to set for the integration (separated by blank spaces, commas, or new lines):

    `ENABLED = { TRUE | FALSE }`
    :   Specifies whether to initiate operation of the integration or suspend it.

        - `TRUE` allows the integration to run based on the parameters specified in the integration definition.
        - `FALSE` suspends the integration for maintenance. Any integration between Snowflake and a third-party service fails to work.

    `OIDC_CLIENT_SECRET = 'string_literal'`
    :   Updates the OAuth 2.0 client secret registered with the IdP. Custom providers only.

    `OIDC_SCOPES = ( 'string_literal' [ , 'string_literal' , ... ] )`
    :   The OAuth scopes to request. Must include `openid`. Custom providers only.

    `OIDC_USERINFO_ENDPOINT = 'string_literal'`
    :   The IdP UserInfo endpoint URL. Reserved for forward compatibility; not used at sign-in. For user-resolution behavior, see
        [CREATE SECURITY INTEGRATION (OIDC)](/sql-reference/sql/create-security-integration-oidc) (`OIDC_USERINFO_ENDPOINT`). Returned by
        [DESC INTEGRATION](/sql-reference/sql/desc-integration) only when set or discovered. Custom providers only.

    `OIDC_ENABLE_SSO_LOGIN_PAGE = { TRUE | FALSE }`
    :   Whether to display this integration on the Snowflake login page. When `FALSE`, the integration exists and is enabled but is not rendered as a **Sign in with X** button.

    `OIDC_LOGIN_PAGE_LABEL = 'string_literal'`
    :   The label displayed on the Snowflake login page for this IdP. Custom providers only. For managed providers (`GOOGLE`, `MICROSOFT`), Snowflake displays the official provider logo and a default label. Setting or unsetting this parameter on a managed integration fails.

    `OIDC_TOKEN_USER_MAPPING_CLAIM = 'string_literal'`
    :   The ID token claim used to identify the Snowflake user. Specify a single claim name (for example, `'email'`), or an ordered list of claim
        names (for example, `('email', 'sub')`). When you specify a list, Snowflake extracts all non-empty values from the listed claims in order,
        then attempts user lookup with each value against `OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE`, using the first successful match. If a claim is
        absent from the ID token, Snowflake skips it and tries the next. Only string-valued claims are supported. Custom providers only.

    `OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = { 'LOGIN_NAME' | 'EMAIL_ADDRESS' }`
    :   The Snowflake user attribute to match against the token claim value.

    `ALLOWED_USER_DOMAINS = ( 'string_literal' [ , 'string_literal' , ... ] )`
    :   Restricts authentication to users whose email domain exactly matches one of the specified domains. Matching is case-insensitive and exact: `mycompany.com` matches `user@mycompany.com` but not `user@evil-mycompany.com`.

        This parameter can be used to associate a user with an IdP for configurations that use multiple IdPs. For details, see [Using multiple identity providers for federated authentication](/user-guide/admin-security-fed-auth-security-integration-multiple).

    `ALLOWED_EMAIL_PATTERNS = ( 'string_literal' [ , 'string_literal' , ... ] )`
    :   Restricts authentication to users whose email matches one of the specified regex patterns. Requires the `ENABLE_IDENTIFIER_FIRST_LOGIN` account parameter to be enabled.

        This parameter can be used to associate a user with an IdP for configurations that use multiple IdPs. For details, see [Using multiple identity providers for federated authentication](/user-guide/admin-security-fed-auth-security-integration-multiple).

    `OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS = ( 'string_literal' [ , 'string_literal' , ... ] )`
    :   The Google Workspace hosted domains allowed to sign in through this integration, checked against the `hd` claim in the ID token. Setting this
        option replaces the existing list, so include every entry you want to keep. `OIDC_PROVIDER='GOOGLE'` only. For entry formats, see
        [CREATE SECURITY INTEGRATION (OIDC)](/sql-reference/sql/create-security-integration-oidc#label-create-security-integration-oidc-managed-required-parameters).

    `OIDC_ALLOWED_MSFT_TENANTS = ( 'string_literal' [ , 'string_literal' , ... ] )`
    :   The Microsoft Entra ID tenants allowed to sign in through this integration, checked against the `tid` claim in the ID token. Setting this option
        replaces the existing list, so include every entry you want to keep. `OIDC_PROVIDER='MICROSOFT'` only. For entry formats, see
        [CREATE SECURITY INTEGRATION (OIDC)](/sql-reference/sql/create-security-integration-oidc#label-create-security-integration-oidc-managed-required-parameters).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the integration.

        Default: No value

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies one or more properties or parameters to unset for the security integration, which resets them back to their defaults:

    - `ALLOWED_EMAIL_PATTERNS`
    - `ALLOWED_USER_DOMAINS`
    - `COMMENT`
    - `ENABLED`
    - `OIDC_ENABLE_SSO_LOGIN_PAGE`
    - `OIDC_LOGIN_PAGE_LABEL`
    - `OIDC_SCOPES`
    - `OIDC_USERINFO_ENDPOINT`
    - `TAG tag_name [ , tag_name ... ]`

## Usage notes

- The following properties can’t be modified via ALTER. To change any of them, drop the integration and recreate it: `OIDC_PROVIDER`, `OIDC_ISSUER`, `OIDC_CLIENT_ID`, `OIDC_AUTHORIZATION_ENDPOINT`, `OIDC_TOKEN_ENDPOINT`, `OIDC_JWKS_URI`. The read-only `OIDC_REDIRECT_URIS` property is generated by Snowflake and can’t be set.
- If you create an integration with placeholder credentials before retrieving the real client ID from your IdP, and the real client ID does not match the placeholder, you must drop the integration and recreate it with the real value.
- Dropping an active OIDC integration immediately prevents all users from authenticating via that IdP. If an authentication policy explicitly references the integration in its `SECURITY_INTEGRATIONS` list, the drop is rejected until the policy is updated. See [DROP INTEGRATION](/sql-reference/sql/drop-integration).
- For a list of OIDC properties returned by [DESC INTEGRATION](/sql-reference/sql/desc-integration), see [CREATE SECURITY INTEGRATION (OIDC)](/sql-reference/sql/create-security-integration-oidc#label-create-security-integration-oidc-desc-output).
- For managed providers (`OIDC_PROVIDER='GOOGLE'` or `OIDC_PROVIDER='MICROSOFT'`), you can’t set or unset `OIDC_LOGIN_PAGE_LABEL`, `OIDC_CLIENT_SECRET`, `OIDC_SCOPES`, `OIDC_USERINFO_ENDPOINT`, or the user-mapping parameters (`OIDC_TOKEN_USER_MAPPING_CLAIM`, `OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE`). Snowflake manages these values for managed providers.
- The managed-provider allow-lists (`OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS` for `GOOGLE`, `OIDC_ALLOWED_MSFT_TENANTS` for `MICROSOFT`) are required at creation and optional here. Setting either option on an integration with a different provider fails.

## Examples

- The following example disables an integration:

  Copy code

  ```
  ALTER SECURITY INTEGRATION my_okta_oidc
    SET ENABLED = FALSE;
  ```
- The following example updates the client secret:

  Copy code

  ```
  ALTER SECURITY INTEGRATION my_okta_oidc
    SET OIDC_CLIENT_SECRET = '<new_client_secret>';
  ```
- The following example changes the user mapping claim:

  Copy code

  ```
  ALTER SECURITY INTEGRATION my_okta_oidc
    SET OIDC_TOKEN_USER_MAPPING_CLAIM = 'preferred_username',
        OIDC_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = 'LOGIN_NAME';
  ```
- The following example restricts authentication by domain:

  Copy code

  ```
  ALTER SECURITY INTEGRATION my_okta_oidc
    SET ALLOWED_USER_DOMAINS = ('mycompany.com', 'subsidiary.com');
  ```
- The following example removes an email pattern restriction:

  Copy code

  ```
  ALTER SECURITY INTEGRATION my_okta_oidc
    UNSET ALLOWED_EMAIL_PATTERNS;
  ```
- The following example replaces the allowed Google Workspace hosted domains:

  Copy code

  ```
  ALTER SECURITY INTEGRATION my_google_oidc
    SET OIDC_ALLOWED_GOOGLE_HOSTED_DOMAINS = ('mycompany.com', 'subsidiary.com');
  ```
- The following example allows personal Microsoft accounts alongside a work tenant:

  Copy code

  ```
  ALTER SECURITY INTEGRATION my_microsoft_oidc
    SET OIDC_ALLOWED_MSFT_TENANTS = ('a1b2c3d4-e5f6-4789-a012-3456789abcde', 'personal');
  ```
