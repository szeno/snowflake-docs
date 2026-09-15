# CREATE CATALOG INTEGRATION (Delta Sharing)

Creates a new [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) in the account, or replaces an existing
catalog integration, for [Delta tables](/sql-reference/sql/create-iceberg-table-delta) that are shared from a remote
[Delta Sharing](https://delta.io/sharing/) server.

After you create a Delta Sharing catalog integration, you can use it with a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database)
to read the shared Delta tables from Snowflake.

See also:
:   [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration) , [DROP CATALOG INTEGRATION](/sql-reference/sql/drop-catalog-integration) , [SHOW CATALOG INTEGRATIONS](/sql-reference/sql/show-catalog-integrations), [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] CATALOG INTEGRATION [ IF NOT EXISTS ] <name>
  CATALOG_SOURCE = DELTA_SHARING
  TABLE_FORMAT = DELTA
  REST_CONFIG = (
    CATALOG_URI = '<delta_sharing_endpoint_url>'
    CATALOG_NAME = 'shares/<share_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    restAuthenticationParams
  )
  ENABLED = { TRUE | FALSE }
  [ COMMENT = '<string_literal>' ]
```

Where `restAuthenticationParams` depends on your authentication method:

**Bearer token**

Copy code

```
restAuthenticationParams (for Bearer token) ::=

  TYPE = BEARER
  BEARER_TOKEN = '<bearer_token>'
```

**OIDC**

Copy code

```
restAuthenticationParams (for OIDC) ::=

  TYPE = OIDC
  OIDC_AUDIENCE = '<audience>'
```

**OAuth**

Copy code

```
restAuthenticationParams (for OAuth) ::=

  TYPE = OAUTH
  OAUTH_CLIENT_ID = '<oauth_client_id>'
  OAUTH_CLIENT_SECRET = '<oauth_client_secret>'
  OAUTH_TOKEN_URI = 'https://<token_server_uri>'
```

## Parameters

`name`
:   String that specifies the identifier (name) for the catalog integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`CATALOG_SOURCE = DELTA_SHARING`
:   Specifies that the catalog source is a server that complies with the open source
    [Delta Sharing protocol](https://github.com/delta-io/delta-sharing).

`TABLE_FORMAT = DELTA`
:   Specifies DELTA as the table format supplied by the catalog. Delta Sharing catalog integrations support only Delta tables.

`ENABLED = { TRUE | FALSE }`
:   Specifies whether the catalog integration is available to use.

    > - `TRUE` allows users to use this integration with a catalog-linked database.
    > - `FALSE` prevents users from using this integration with a catalog-linked database.

    The value is case-insensitive.

    The default is `TRUE`.

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the integration.

    Default: No value

### REST configuration parameters (restConfigParams)

`CATALOG_URI = 'delta_sharing_endpoint_url'`
:   The endpoint URL for your Delta Sharing server. For Databricks Unity Catalog, this is the `endpoint` value from the
    recipient credential file that Databricks generates.

    For example:

    Copy code

    ```
    https://oregon.cloud.databricks.com/api/2.0/delta-sharing/metastores/46d301b9-1b7d-48ea-9d2a-48efb54bd280
    ```

`CATALOG_NAME = 'shares/share_name'`
:   Specifies the Delta Sharing share to use, in the form `shares/<share_name>`. The share name is the name of the share that
    the Delta Sharing server exposes to the recipient.

    For example, if your share is named `sales_share`, specify `CATALOG_NAME = 'shares/sales_share'`.

`ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS`
:   Specifies that the catalog integration uses vended credentials returned by the Delta Sharing server to access the underlying
    table data in cloud storage.

    For Delta Sharing, vended credentials are the only supported access delegation mode.

### REST authentication parameters (restAuthenticationParams)

Delta Sharing catalog integrations support bearer-token, OIDC federation, or OAuth client-credentials authentication.

**Bearer token**

> `TYPE = BEARER`
> :   Specifies a bearer token as the authentication type for Snowflake to use to connect to the Delta Sharing server.
>
> `BEARER_TOKEN = 'bearer_token'`
> :   The bearer token that the Delta Sharing server issued to the recipient. For Databricks Unity Catalog, this is the
>     `bearerToken` value from the recipient credential file that Databricks generates.

**OIDC**

> `TYPE = OIDC`
> :   Specifies [OpenID Connect](https://openid.net/connect/) federation as the authentication type. Snowflake acts as the workload
>     identity provider and presents short-lived JWT tokens to the Delta Sharing server.
>
>     After you create the catalog integration with OIDC authentication, run [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration) to
>     retrieve the `WORKLOAD_IDENTITY_FEDERATION_ISSUER` and `WORKLOAD_IDENTITY_FEDERATION_SUBJECT` values. Provide these values,
>     together with the `OIDC_AUDIENCE` value, to the Delta Sharing provider so that the provider can configure the OIDC recipient
>     policy.
>
> `OIDC_AUDIENCE = 'audience'`
> :   The audience value that the Delta Sharing server’s OIDC recipient policy expects in the JWT tokens that Snowflake presents.
>
>     The audience value must match the audience that the Delta Sharing provider configures in the OIDC recipient policy.

**OAuth**

> `TYPE = OAUTH`
> :   Specifies OAuth client-credentials as the authentication type. Snowflake exchanges the client ID and secret with the configured token endpoint for an access token, then uses that token to authenticate to the Delta Sharing server.
>
> `OAUTH_CLIENT_ID = 'oauth_client_id'`
> :   Your OAuth2 client ID, as issued by the Delta Sharing provider’s identity provider.
>
> `OAUTH_CLIENT_SECRET = 'oauth_client_secret'`
> :   Your OAuth2 client secret, as issued by the Delta Sharing provider’s identity provider.
>
> `OAUTH_TOKEN_URI = 'https://token_server_uri'`
> :   The token endpoint URL of the OAuth identity provider that issues access tokens for the Delta Sharing server.

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

- A Delta Sharing catalog integration provides read-only access to shared Delta tables. A catalog-linked database that uses
  a Delta Sharing catalog integration doesn’t support write operations.
- You can’t modify an existing catalog integration; use a CREATE OR REPLACE CATALOG INTEGRATION statement instead.
- You can’t drop or replace a catalog integration if one or more Apache Iceberg™ tables
  are associated with the catalog integration.

  To view the tables that depend on a catalog integration,
  you can use the [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) command and
  a query using the [pipe operator](/sql-reference/operators-flow) (`->>`) that filters on
  the `catalog_name` column.

  Note

  The column identifier (`catalog_name`) is case-sensitive.
  Specify the column identifier exactly as it appears in the SHOW ICEBERG TABLES output.

  For example:

  Copy code

  ```
  SHOW ICEBERG TABLES
    ->> SELECT *
          FROM $1
          WHERE "catalog_name" = 'my_catalog_integration_1';
  ```
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

The following example creates a Delta Sharing catalog integration with bearer-token authentication:

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION my_delta_sharing_int
  CATALOG_SOURCE = DELTA_SHARING
  TABLE_FORMAT = DELTA
  REST_CONFIG = (
    CATALOG_URI = '<endpoint_from_credential>'
    CATALOG_NAME = 'shares/<share_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = BEARER
    BEARER_TOKEN = '<bearer_token_from_credential>'
  )
  ENABLED = TRUE;
```

The following example creates a Delta Sharing catalog integration with OIDC federation authentication:

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION my_delta_sharing_int_oidc
  CATALOG_SOURCE = DELTA_SHARING
  TABLE_FORMAT = DELTA
  REST_CONFIG = (
    CATALOG_URI = '<recipient_endpoint>'
    CATALOG_NAME = 'shares/<share_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = OIDC
    OIDC_AUDIENCE = '<audience>'
  )
  ENABLED = TRUE;
```

The following example creates a Delta Sharing catalog integration with OAuth client-credentials authentication:

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION my_delta_sharing_int_oauth
  CATALOG_SOURCE = DELTA_SHARING
  TABLE_FORMAT = DELTA
  REST_CONFIG = (
    CATALOG_URI = '<recipient_endpoint>'
    CATALOG_NAME = 'shares/<share_name>'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_CLIENT_ID = '<oauth_client_id>'
    OAUTH_CLIENT_SECRET = '<oauth_client_secret>'
    OAUTH_TOKEN_URI = 'https://<token_server_uri>'
  )
  ENABLED = TRUE;
```

For a step-by-step walkthrough, see [Configure a catalog integration for Delta Sharing](/user-guide/tables-iceberg-configure-catalog-integration-delta-sharing).
