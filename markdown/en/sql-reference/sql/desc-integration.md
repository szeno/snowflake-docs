# DESCRIBE INTEGRATION

Describes the properties of an integration.

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE INTEGRATION](/sql-reference/sql/create-integration), [DROP INTEGRATION](/sql-reference/sql/drop-integration), [ALTER INTEGRATION](/sql-reference/sql/alter-integration), [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations)

API integrations:
:   [ALTER API INTEGRATION](/sql-reference/sql/alter-api-integration), [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration)

Catalog integrations:
:   [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration), [CREATE CATALOG INTEGRATION](/sql-reference/sql/create-catalog-integration)

External access integrations:
:   [ALTER EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/alter-external-access-integration), [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration)

Notification integrations:
:   [ALTER NOTIFICATION INTEGRATION](/sql-reference/sql/alter-notification-integration), [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration)

Security integrations:
:   [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration), [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration)

Storage integrations:
:   [ALTER STORAGE INTEGRATION](/sql-reference/sql/alter-storage-integration), [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration)

## Syntax

Copy code

```
{ DESC | DESCRIBE } [ { API | CATALOG | EXTERNAL ACCESS | NOTIFICATION | SECURITY | STORAGE } ] INTEGRATION <name>
```

## Parameters

`{ API | CATALOG | EXTERNAL ACCESS | NOTIFICATION | SECURITY | STORAGE }`
:   Describes an integration of the specified type.

    For more information about some of these types, see the following topics:

    - [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration)
    - [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration)

`name`
:   Specifies the identifier for the integration to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

- If the integration is an API integration, then the output includes the API\_KEY column. The API\_KEY displays a masked value if an
  [API key](/sql-reference/external-functions-security#label-external-functions-api-key) was entered. (This does not display either the original unencrypted key or the
  encrypted version of the key.)
- If the security integration has the `TYPE` property set to `OAUTH` (that is, Snowflake OAuth), Snowflake returns two additional security
  integration properties in the query result that cannot be set with either a CREATE SECURITY INTEGRATION or an ALTER SECURITY INTEGRATION
  command:

  `OAUTH_ALLOWED_AUTHORIZATION_ENDPOINTS`
  :   A list of all supported endpoints for a client application to receive an authorization code from Snowflake.

  `OAUTH_ALLOWED_TOKEN_ENDPOINTS`
  :   A list of all supported endpoints for a client application to exchange an authorization code for an access token or to obtain a refresh
      token.
- If the security integration has the `TYPE` property set to `OIDC`, Snowflake returns OIDC-specific properties in the query result with
  the columns `property`, `property_type`, `property_value`, and `property_default`. `OIDC_CLIENT_SECRET` is never returned.
  `OIDC_REDIRECT_URIS` is returned but can’t be set with CREATE or ALTER. For sample output and property behavior, see
  [CREATE SECURITY INTEGRATION (OIDC)](/sql-reference/sql/create-security-integration-oidc#label-create-security-integration-oidc-desc-output).

## Examples

Describe the properties of an integration named `my_int`:

Copy code

```
DESC INTEGRATION my_int;
```
