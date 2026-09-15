# ALTER SECURITY INTEGRATION (External API Authentication)

Modifies the properties of an existing security integration created for External API Authentication.

For information about modifying other types of security integrations (e.g. Snowflake OAuth), see [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration).

See also:
:   [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth) , [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations)

## Syntax

### OAuth: Client credentials

Copy code

```
ALTER SECURITY INTEGRATION <name> SET
  [ ENABLED = { TRUE | FALSE } ]
  [ OAUTH_TOKEN_ENDPOINT = '<string_literal>' ]
  [ OAUTH_CLIENT_AUTH_METHOD = { CLIENT_SECRET_BASIC | CLIENT_SECRET_POST } ]
  [ OAUTH_CLIENT_ID = '<string_literal>' ]
  [ OAUTH_CLIENT_SECRET = '<string_literal>' ]
  [ OAUTH_GRANT = 'CLIENT_CREDENTIALS']
  [ OAUTH_ACCESS_TOKEN_VALIDITY = <integer> ]
  [ OAUTH_ALLOWED_SCOPES = ( '<scope_1>' [ , '<scope_2>' ... ] ) ]
  [ COMMENT = '<string_literal>' ]

ALTER [ SECURITY ] INTEGRATION <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER [ SECURITY ] INTEGRATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name> UNSET {
  ENABLED | [ , ... ]
}
```

### OAuth: Authorization code grant flow

Copy code

```
ALTER SECURITY INTEGRATION <name> SET
  [ ENABLED = { TRUE | FALSE } ]
  [ OAUTH_AUTHORIZATION_ENDPOINT = '<string_literal>' ]
  [ OAUTH_TOKEN_ENDPOINT = '<string_literal>' ]
  [ OAUTH_CLIENT_AUTH_METHOD = { CLIENT_SECRET_BASIC | CLIENT_SECRET_POST } ]
  [ OAUTH_CLIENT_ID = '<string_literal>' ]
  [ OAUTH_CLIENT_SECRET = '<string_literal>' ]
  [ OAUTH_GRANT = 'AUTHORIZATION_CODE']
  [ OAUTH_ACCESS_TOKEN_VALIDITY = <integer> ]
  [ OAUTH_REFRESH_TOKEN_VALIDITY = <integer> ]
  [ COMMENT = '<string_literal>' ]

ALTER [ SECURITY ] INTEGRATION <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER [ SECURITY ] INTEGRATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name> UNSET {
  ENABLED | [ , ... ]
}
```

### OAuth: JWT bearer flow

Copy code

```
ALTER SECURITY INTEGRATION <name> SET
  [ ENABLED = { TRUE | FALSE } ]
  [ OAUTH_AUTHORIZATION_ENDPOINT = '<string_literal>' ]
  [ OAUTH_TOKEN_ENDPOINT = '<string_literal>' ]
  [ OAUTH_CLIENT_AUTH_METHOD = { CLIENT_SECRET_BASIC | CLIENT_SECRET_POST } ]
  [ OAUTH_CLIENT_ID = '<string_literal>' ]
  [ OAUTH_CLIENT_SECRET = '<string_literal>' ]
  [ OAUTH_GRANT = 'JWT_BEARER']
  [ OAUTH_ACCESS_TOKEN_VALIDITY = <integer> ]
  [ OAUTH_REFRESH_TOKEN_VALIDITY = <integer> ]
  [ COMMENT = '<string_literal>' ]

ALTER [ SECURITY ] INTEGRATION <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER [ SECURITY ] INTEGRATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name> UNSET {
  ENABLED | [ , ... ]
}
```

## Parameters

`name`
:   String that specifies the identifier (i.e. name) for the integration.

`SET ...`
:   Specifies one or more properties/parameters to set for the integration (separated by blank spaces, commas, or new lines):

    `ENABLED = { TRUE | FALSE }`
    :   Specifies whether this security integration is enabled or disabled.

        `TRUE`
        :   Allows the integration to run based on the parameters specified in the integration definition.

        `FALSE`
        :   Suspends the integration for maintenance. Any integration between Snowflake and a third-party service fails to work.

    `OAUTH_AUTHORIZATION_ENDPOINT = 'string_literal'`
    :   Specifies the URL for authenticating to the external service. For example, to connect to the ServiceNow instance, the URL should be in
        the following format:

        Copy code

        ```
        https://<instance_name>.service-now.com/oauth_token.do
        ```

        Where `instance_name` is the name of your ServiceNow instance.

    `OAUTH_TOKEN_ENDPOINT = 'string_literal'`
    :   Specifies the token endpoint used by the client to obtain an access token by presenting its authorization grant or refresh token.
        The token endpoint is used with every authorization grant except for the implicit grant type (since an access token is issued directly).

`OAUTH_CLIENT_AUTH_METHOD = { CLIENT_SECRET_BASIC | CLIENT_SECRET_POST }`
:   Controls how client credentials are sent to the external service.

    `CLIENT_SECRET_BASIC`
    :   Specifies that client credentials are sent using the HTTP Basic Authentication Scheme.

    `CLIENT_SECRET_POST`
    :   Specifies that client credentials are sent in the HTTP request body of a POST request.

    Default: `CLIENT_SECRET_BASIC`

    `OAUTH_CLIENT_ID = 'string_literal'`
    :   Specifies the client ID for the OAuth application in the external service.

    `OAUTH_CLIENT_SECRET = 'string_literal'`
    :   Specifies the client secret for the OAuth application in the ServiceNow instance. The connector uses this to request an access token
        from the ServiceNow instance.

    `OAUTH_GRANT = 'string_literal'`
    :   Specifies the type of OAuth flow. One of the following:

        - `'CLIENT_CREDENTIALS'` when the integration will use client credentials.
        - `'AUTHORIZATION_CODE'` when the integration will use an authorization code.
        - `'JWT_BEARER'` when the integration will use a JWT bearer token.

    `OAUTH_ACCESS_TOKEN_VALIDITY = integer`
    :   Specifies the default lifetime of the OAuth access token (in seconds) issued by an OAuth server.

        The value set in this property is used if the access token lifetime is not returned as part of OAuth token response. When both
        values are available, the smaller value will be used to refresh the access token.

    `OAUTH_REFRESH_TOKEN_VALIDITY = integer`
    :   Specifies the value to determine the validity of the refresh token obtained from the OAuth server.

    `OAUTH_ALLOWED_SCOPES = ( list )`
    :   Specifies a comma-separated list of scopes, with single quotes surrounding each scope, to use when making a request from the OAuth by a
        role with USAGE on the integration during the OAuth client credentials flow.

        This list must be a subset of the scopes defined in the `OAUTH_ALLOWED_SCOPES` property of the security integration. If the
        `OAUTH_SCOPES` property values are not specified, the secret inherits all of the scopes that are specified in the security
        integration.

        For the ServiceNow connector, the only possible scope value is `'useraccount'`.

        Default: Empty list (i.e. `[]`).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the integration.

        Default: No value

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Integration | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example initiates operation of a suspended integration:

> Copy code
>
> ```
> ALTER SECURITY INTEGRATION myint SET ENABLED = TRUE;
> ```
