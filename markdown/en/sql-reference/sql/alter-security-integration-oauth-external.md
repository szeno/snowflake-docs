# ALTER SECURITY INTEGRATION (External OAuth)

Attention

Mentions of Microsoft Azure Active Directory refer to Microsoft Entra ID.

Modifies the properties of an existing security integration created for External OAuth. For information about modifying other types of
security integrations (e.g. Snowflake OAuth), see [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration).

See also:
:   [CREATE SECURITY INTEGRATION (External OAuth)](/sql-reference/sql/create-security-integration-oauth-external) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations) , [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

## Syntax

Copy code

```
ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name> SET
  [ TYPE = EXTERNAL_OAUTH ]
  [ ENABLED = { TRUE | FALSE } ]
  [ EXTERNAL_OAUTH_TYPE = { OKTA | AZURE | PING_FEDERATE | CUSTOM } ]
  [ EXTERNAL_OAUTH_ISSUER = '<string_literal>' ]
  [ EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM = '<string_literal>' | ('<string_literal>', '<string_literal>' [ , ... ] ) ]
  [ EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = 'LOGIN_NAME | EMAIL_ADDRESS' ]
  [ EXTERNAL_OAUTH_JWS_KEYS_URL = '<string_literal>' ] -- For OKTA | PING_FEDERATE | CUSTOM
  [ EXTERNAL_OAUTH_JWS_KEYS_URL = '<string_literal>' | ('<string_literal>' [ , '<string_literal>' ... ] ) ] -- For Azure
  [ EXTERNAL_OAUTH_RSA_PUBLIC_KEY = <public_key1> ]
  [ EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2 = <public_key2> ]
  [ EXTERNAL_OAUTH_BLOCKED_ROLES_LIST = ( '<role_name>' [ , '<role_name>' , ... ] ) ]
  [ EXTERNAL_OAUTH_ALLOWED_ROLES_LIST = ( '<role_name>' [ , '<role_name>' , ... ] ) ]
  [ EXTERNAL_OAUTH_AUDIENCE_LIST = ('<string_literal>') ]
  [ EXTERNAL_OAUTH_ANY_ROLE_MODE = DISABLE | ENABLE | ENABLE_FOR_PRIVILEGE ]
  [ EXTERNAL_OAUTH_SCOPE_DELIMITER = '<string_literal>' ] -- Only for EXTERNAL_OAUTH_TYPE = CUSTOM
  [ IS_AGENTIC = { TRUE | FALSE } ]
  [ NETWORK_POLICY = '<network_policy>' ]
  [ COMMENT = '<string_literal>' ]

ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name>  UNSET {
                                                            ENABLED                      |
                                                            EXTERNAL_OAUTH_AUDIENCE_LIST |
                                                            IS_AGENTIC                   |
                                                            }
                                                            [ , ... ]

ALTER [ SECURITY ] INTEGRATION <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER [ SECURITY ] INTEGRATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   Identifier for the integration to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`SET ...`
:   Specifies one or more properties/parameters to set for the integration (separated by blank spaces, commas, or new lines):

    `TYPE = EXTERNAL_OAUTH`
    :   Distinguishes the [External OAuth](/user-guide/oauth-ext-overview) integration from a
        [Snowflake OAuth](/user-guide/oauth-snowflake-overview) integration.

    `ENABLED = { TRUE | FALSE }`
    :   Specifies whether to initiate operation of the integration or suspend it.

        - `TRUE` allows the integration to run based on the parameters specified in the pipe definition.
        - `FALSE` suspends the integration for maintenance. Any integration between Snowflake and a third-party service fails to work.

    `EXTERNAL_OAUTH_TYPE = { OKTA | AZURE | PING_FEDERATE | CUSTOM }`
    :   Specifies the OAuth 2.0 authorization server to be Okta, Microsoft Entra ID, Ping Identity PingFederate, or a Custom OAuth 2.0
        authorization server.

    `EXTERNAL_OAUTH_ISSUER = 'string_literal'`
    :   Specifies the URL to define the OAuth 2.0 authorization server.

    `EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM = { 'string_literal' | ('string_literal', 'string_literal' [ , ... ] ) }`
    :   Specifies the access token claim or claims that can be used to map the access token to a Snowflake user record.

        The data type of the claim must be a string or a list of strings.

    `EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE = { 'LOGIN_NAME | EMAIL_ADDRESS' }`
    :   Indicates which Snowflake user record attribute should be used to map the access token to a Snowflake user record.

    `EXTERNAL_OAUTH_JWS_KEYS_URL = 'string_literal'`
    :   Specifies the endpoint from which to download public keys or certificates to validate an External OAuth access token.

        This syntax applies to security integrations where `EXTERNAL_OAUTH_TYPE = { OKTA | PING_FEDERATE | CUSTOM }`

    `EXTERNAL_OAUTH_JWS_KEYS_URL = { 'string_literal' | ('string_literal' [ , 'string_literal' ... ] ) }`
    :   Specifies the endpoint or a list of endpoints from which to download public keys or certificates to validate an External OAuth access
        token. The maximum number of URLs that can be specified in the list is 3.

        This syntax applies to security integrations where `EXTERNAL_OAUTH_TYPE = AZURE`

    `EXTERNAL_OAUTH_RSA_PUBLIC_KEY = public_key1`
    :   Specifies a Base64-encoded RSA public key, without the `-----BEGIN PUBLIC KEY-----` and `-----END PUBLIC KEY-----` headers.

    `EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2 = public_key2`
    :   Specifies a second RSA public key, without the `-----BEGIN PUBLIC KEY-----` and `-----END PUBLIC KEY-----` headers. Used
        for key rotation.

    `EXTERNAL_OAUTH_BLOCKED_ROLES_LIST = ( 'role_name' [ , 'role_name' , ... ] )`
    :   Specifies the list of roles that a client cannot set as the [primary role](/user-guide/security-access-control-overview#label-access-control-role-enforcement). A role
        in this list cannot be used when creating a Snowflake session based on the access token from the External OAuth
        authorization server.

        By default, this list includes the ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, and SECURITYADMIN roles. To remove these privileged roles from the list, use
        the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command to set the [EXTERNAL\_OAUTH\_ADD\_PRIVILEGED\_ROLES\_TO\_BLOCKED\_LIST](/sql-reference/parameters#label-external-oauth-add-privileged-roles-to-blocked-list) account parameter to
        `FALSE`.

    `EXTERNAL_OAUTH_ALLOWED_ROLES_LIST = ( 'role_name' [ , 'role_name' , ... ] )`
    :   Specifies the list of roles that the client can set as the primary role.

        A role in this list can be used when creating a Snowflake session based on the access token from the External OAuth authorization
        server.

        Caution

        This parameter supports the ACCOUNTADMIN, ORGADMIN, GLOBALORGADMIN, and SECURITYADMIN system roles.

        Exercise caution when creating a Snowflake session with these highly privileged roles set as the primary role.

    `EXTERNAL_OAUTH_AUDIENCE_LIST = ('string_literal')`
    :   Specifies additional values that can be used for the access token’s audience validation on top of using the Customer’s Snowflake
        Account URL (i.e. `<account_identifier>.snowflakecomputing.com`). For more information, see
        [Account identifiers](/user-guide/admin-account-identifier).

        For details on this property when using Power BI SSO, refer to
        [Power BI SSO security integrations](/user-guide/oauth-powerbi#label-powerbi-create-security-integration).

        Currently, multiple audience URLs can be specified for [External OAuth Custom Clients](/user-guide/oauth-ext-custom) only. Each
        URL must be enclosed in single quotes, with a comma separating each URL. For example:

        > Copy code
        >
        > ```
        > external_oauth_audience_list = ('https://example.com/api/v2/', 'https://example.com')
        > ```

    `EXTERNAL_OAUTH_ANY_ROLE_MODE = { DISABLE | ENABLE | ENABLE_FOR_PRIVILEGE }`
    :   Specifies whether the OAuth client or user can use a role that is not defined in the OAuth access token. Note that with a
        [Power BI to Snowflake integration](/user-guide/oauth-powerbi), the PowerBI user cannot switch roles even when this parameter is enabled.

        - `DISABLE` does not allow the OAuth client or user to switch roles (i.e. `USE ROLE role;`). Default.
        - `ENABLE` allows the OAuth client or user to switch roles.
        - `ENABLE_FOR_PRIVILEGE` allows the OAuth client or user to switch roles only for a client or user with the USE\_ANY\_ROLE
          privilege. This privilege can be granted and revoked to one or more roles available to the user. For example:

          Copy code

          ```
          GRANT USE_ANY_ROLE ON INTEGRATION external_oauth_1 TO role1;
          ```

          Copy code

          ```
          REVOKE USE_ANY_ROLE ON INTEGRATION external_oauth_1 FROM role1;
          ```

        Note that the value can be optionally enclosed in single quotes (e.g. either `DISABLE` or `'DISABLE'`).

    `EXTERNAL_OAUTH_SCOPE_DELIMITER = 'string_literal'`
    :   Specifies the scope delimiter in the authorization token.

        The delimiter can be any single character, such as comma (`','`) or space (`' '`).

        This security integration property is optional and can be used to override the default comma delimiter. Note that this property is only
        supported for custom External OAuth integrations, where:

        > `EXTERNAL_OAUTH_TYPE = CUSTOM`

        Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) to enable this
        property in your Snowflake account.

    `IS_AGENTIC = { TRUE | FALSE }`
    :   Specifies whether sessions authenticated through this integration should be treated as agent sessions.

        When set to `TRUE`, Snowflake automatically recognizes all sessions authenticated through this integration as agent sessions, causing [IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated) to return `TRUE` for those sessions.

        Default: `FALSE`

    `NETWORK_POLICY = 'network_policy'`
    :   Specifies an existing [network policy](/user-guide/network-policies). This network policy controls network traffic from the client
        to Snowflake.

        For more information, see [Restricting network traffic for External OAuth](/user-guide/oauth-ext-overview#label-ext-oauth-network-policies).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the integration.

        Default: No value

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies one or more properties/parameters to unset for the security integration, which resets them back to their defaults:

    - `ENABLED`
    - `EXTERNAL_OAUTH_AUDIENCE_LIST`
    - `IS_AGENTIC`
    - `TAG tag_name [ , tag_name ... ]`

## Usage notes

Regarding metadata:

> Attention
>
> Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example initiates operation of a suspended integration:

Copy code

```
ALTER SECURITY INTEGRATION myint SET ENABLED = TRUE;
```
