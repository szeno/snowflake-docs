# CREATE CATALOG INTEGRATION (Snowflake Horizon Catalog)

Creates a new [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) in the consumer account to access
Apache Iceberg™ tables managed by another Snowflake account through Snowflake Horizon Catalog, or replaces an existing catalog integration.

The account that contains the tables is the **provider account**. The account where you create the integration is the **consumer account**.
The integration authenticates with workload identity federation, so you don’t create, store, or rotate a secret. For the complete setup,
see [Access Apache Iceberg™ tables in another Snowflake account](/user-guide/tables-iceberg-configure-catalog-integration-rest-horizon).

See also:
:   [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration), [DROP CATALOG INTEGRATION](/sql-reference/sql/drop-catalog-integration),
    [SHOW CATALOG INTEGRATIONS](/sql-reference/sql/show-catalog-integrations), [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] CATALOG INTEGRATION [ IF NOT EXISTS ]
  <name>
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = '<horizon_account_url>'
    [ CATALOG_API_TYPE = { PUBLIC | PRIVATE } ]
    CATALOG_NAME = '<database_name>'
    [ ACCESS_DELEGATION_MODE = { VENDED_CREDENTIALS | EXTERNAL_VOLUME_CREDENTIALS } ]
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_GRANT_TYPE = TOKEN_EXCHANGE
    OAUTH_ALLOWED_SCOPES = ('session:role:<role_name>')
    [ OAUTH_AUDIENCE = '<audience>' ]
  )
  [ DEFAULT_STORAGE_CONFIG = (
      USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE }
    ) ]
  ENABLED = { TRUE | FALSE }
  [ REFRESH_INTERVAL_SECONDS = <value> ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (name) for the catalog integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`CATALOG_SOURCE = POLARIS`
:   Specifies Snowflake Horizon Catalog as the catalog source.

`TABLE_FORMAT = ICEBERG`
:   Specifies Apache Iceberg™ as the table format supplied by the catalog.

`REST_CONFIG = ( ... )`
:   Specifies the Horizon Catalog endpoint, provider database, and storage access configuration.

    `CATALOG_URI = 'horizon_account_url'`
    :   The Horizon Iceberg REST Catalog API URL of the provider account. Use one of the following formats:

        - Public account name URL: `https://<orgname>-<provider_account_name>.snowflakecomputing.com/polaris/api/catalog`.
        - Public account locator URL: `https://<account_locator>.<cloud_region_id>.<cloud>.snowflakecomputing.com/polaris/api/catalog`.
        - PrivateLink account name URL: `https://<orgname>-<provider_account_name>.privatelink.snowflakecomputing.com/polaris/api/catalog`.
          Use this URL only with `CATALOG_API_TYPE = PRIVATE`.

        To retrieve the URL, see [Get the Horizon Catalog endpoint](/user-guide/tables-iceberg-configure-catalog-integration-rest-horizon#label-tables-iceberg-catalog-integration-horizon-get-url) or
        [Use private connectivity for the catalog API](/user-guide/tables-iceberg-configure-catalog-integration-rest-horizon#label-tables-iceberg-catalog-integration-horizon-private).
        For account URL formats, see [Account identifiers](/user-guide/admin-account-identifier).

    `CATALOG_NAME = 'database_name'`
    :   Specifies the name of the database in the provider account that contains the Iceberg tables.

    `CATALOG_API_TYPE = { PUBLIC | PRIVATE }`
    :   Optionally specifies the connection type for the Horizon Catalog API:

        - `PUBLIC`: Uses the provider’s regular account URL. Requests to a provider in the same region route internally; requests to a provider
          in another region use the public endpoint.
        - `PRIVATE`: Uses private connectivity. Requests to a provider in the same region route internally. For accounts in different regions,
          provision a private endpoint in the consumer account. Both accounts must be hosted on the same cloud provider, either AWS or Azure.

        For endpoint setup, see [Use private connectivity for the catalog API](/user-guide/tables-iceberg-configure-catalog-integration-rest-horizon#label-tables-iceberg-catalog-integration-horizon-private).

        Default: `PUBLIC`

    `ACCESS_DELEGATION_MODE = { VENDED_CREDENTIALS | EXTERNAL_VOLUME_CREDENTIALS }`
    :   Optionally specifies how the consumer account accesses the provider’s table files:

        - `VENDED_CREDENTIALS`: Uses storage credentials provided by Horizon Catalog. Recommended.
        - `EXTERNAL_VOLUME_CREDENTIALS`: Uses an external volume configured in the consumer account. Specify `EXTERNAL_VOLUME` when creating
          an Iceberg table or a catalog-linked database.

        Default: `EXTERNAL_VOLUME_CREDENTIALS`

`REST_AUTHENTICATION = ( ... )`
:   Specifies authentication details for the connection to Horizon Catalog.

    `TYPE = OAUTH`
    :   Specifies OAuth as the authentication type.

    `OAUTH_GRANT_TYPE = TOKEN_EXCHANGE`
    :   Specifies that Snowflake issues an ID token for the catalog integration and exchanges it for an access token in the provider account.
        The provider account trusts the integration’s identity through a service user whose `WORKLOAD_IDENTITY` matches the
        `WORKLOAD_IDENTITY_FEDERATION_ISSUER` and `WORKLOAD_IDENTITY_FEDERATION_SUBJECT` properties in the output of
        [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration).

        You don’t specify `OAUTH_TOKEN_URI`, `OAUTH_CLIENT_ID`, or `OAUTH_CLIENT_SECRET`.

    `OAUTH_ALLOWED_SCOPES = ( 'session:role:role_name' )`
    :   The role in the provider account that the access token is scoped to. Grant this role to the service user that trusts the integration’s
        identity. The role’s privileges determine which databases, schemas, and tables the consumer can access and which operations it can
        perform.

    `OAUTH_AUDIENCE = 'audience'`
    :   Optionally specifies the audience (`aud` claim) of the ID token that Snowflake issues for the integration. To restrict token use to the
        provider account, specify a custom audience and include the same value in the service user’s `OIDC_AUDIENCE_LIST` in the provider
        account. For instructions, see [Restrict token use to the provider account](/user-guide/tables-iceberg-configure-catalog-integration-rest-horizon#label-tables-iceberg-catalog-integration-horizon-audience).

        Default: `snowflakecomputing.com`

`ENABLED = { TRUE | FALSE }`
:   Specifies whether the catalog integration is available for use:

    - `TRUE`: Allows users to create Iceberg tables that reference the integration. Existing tables continue to access Horizon Catalog.
    - `FALSE`: Prevents users from creating Iceberg tables that reference the integration. Existing tables can’t access Horizon Catalog
      through the integration.

## Optional parameters

`DEFAULT_STORAGE_CONFIG = ( USE_PRIVATELINK_ENDPOINT = { TRUE | FALSE } )`
:   Specifies whether the consumer account uses private connectivity to access table storage with vended credentials. Set
    `USE_PRIVATELINK_ENDPOINT = TRUE` to use private connectivity to storage. The integration must use
    `ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS`.

    This setting is independent of `CATALOG_API_TYPE`, which controls the connection to the catalog API. For cloud requirements and endpoint
    setup, see [Use private connectivity for storage with vended credentials](/user-guide/tables-iceberg-configure-catalog-integration-rest-horizon#label-tables-iceberg-catalog-integration-horizon-private-storage).

    Default: No value. Snowflake uses public connectivity to storage.

`REFRESH_INTERVAL_SECONDS = value`
:   Specifies the number of seconds that Snowflake waits between attempts to poll the external Iceberg catalog for metadata updates
    for [automated refresh](/user-guide/tables-iceberg-auto-refresh).

    For Delta-based tables, specifies the number of seconds that Snowflake waits between attempts to poll your external cloud storage for
    new metadata.

    Values: 30 to 86400, inclusive

    Default: 30 seconds

`COMMENT = 'string_literal'`
:   String (literal) that specifies a comment for the integration.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| `CREATE INTEGRATION` | Account | Required in the consumer account. Granted to `ACCOUNTADMIN` by default. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- After creating the integration, retrieve its identity with [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration), then create a service user
  in the provider account that trusts that identity. Grant the role specified in `OAUTH_ALLOWED_SCOPES` to the service user. For the
  complete workflow, see [Access Apache Iceberg™ tables in another Snowflake account](/user-guide/tables-iceberg-configure-catalog-integration-rest-horizon).
- Specify the provider’s schema with `CATALOG_NAMESPACE` when creating an individual Iceberg table, or use a catalog-linked database to
  discover schemas and tables. Don’t set `CATALOG_NAMESPACE` on this integration.
- This integration doesn’t support accessing provider tables that require policy-based filtering or masking. See
  [Limitations](/user-guide/tables-iceberg-configure-catalog-integration-rest-horizon#label-tables-iceberg-catalog-integration-horizon-limitations).
- Use [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration) to change supported properties. To change a property that command doesn’t support,
  use `CREATE OR REPLACE CATALOG INTEGRATION`.
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
- - The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
  - CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Create a catalog integration in the consumer account that connects to the `my_database` database in the provider account. Horizon Catalog
provides the storage credentials, and the access token is scoped to the provider’s `iceberg_reader` role:

Copy code

```
CREATE CATALOG INTEGRATION horizon_catalog_int
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = 'https://myorg-provider_account.snowflakecomputing.com/polaris/api/catalog'
    CATALOG_NAME = 'my_database'
    ACCESS_DELEGATION_MODE = VENDED_CREDENTIALS
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_GRANT_TYPE = TOKEN_EXCHANGE
    OAUTH_ALLOWED_SCOPES = ('session:role:iceberg_reader')
  )
  ENABLED = TRUE;
```

For complete creation examples with a custom audience, an external volume, or private connectivity, see
[Optional configurations](/user-guide/tables-iceberg-configure-catalog-integration-rest-horizon#label-tables-iceberg-catalog-integration-horizon-options).
