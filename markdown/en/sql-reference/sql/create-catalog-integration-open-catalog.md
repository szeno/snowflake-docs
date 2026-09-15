# CREATE CATALOG INTEGRATION (Snowflake Open Catalog)

Creates a new [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def) for [Apache Iceberg™ tables](/user-guide/tables-iceberg)
that integrate with [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview) in the account or replaces an existing catalog integration.

You can also use this command to create a catalog integration for Iceberg tables in [Apache Polaris™](https://polaris.apache.org/).

See also:
:   [ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration) , [DROP CATALOG INTEGRATION](/sql-reference/sql/drop-catalog-integration) , [SHOW CATALOG INTEGRATIONS](/sql-reference/sql/show-catalog-integrations), [DESCRIBE CATALOG INTEGRATION](/sql-reference/sql/desc-catalog-integration)

## Syntax

### CATALOG\_API\_TYPE: PUBLIC

Use this catalog integration to connect Snowflake to Open Catalog through the public internet. The default for the CATALOG\_API\_TYPE
parameter is PUBLIC, so you don’t have to specify this parameter.

Copy code

```
CREATE [ OR REPLACE ] CATALOG INTEGRATION [ IF NOT EXISTS ]
  <name>
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  [ CATALOG_NAMESPACE = '<open_catalog_namespace>' ]
  REST_CONFIG = (
    CATALOG_URI = '<open_catalog_account_url>'
    [ CATALOG_API_TYPE = PUBLIC ]
    CATALOG_NAME = '<open_catalog_catalog_name>'
    [ ACCESS_DELEGATION_MODE = { VENDED_CREDENTIALS | EXTERNAL_VOLUME_CREDENTIALS } ]
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    [ OAUTH_TOKEN_URI = 'https://<token_server_uri>' ]
    OAUTH_CLIENT_ID = '<oauth_client_id>'
    OAUTH_CLIENT_SECRET = '<oauth_secret>'
    OAUTH_ALLOWED_SCOPES = ('<scope 1>', '<scope 2>')
  )
  ENABLED = { TRUE | FALSE }
  [ REFRESH_INTERVAL_SECONDS = <value> ]
  [ COMMENT = '<string_literal>' ]
```

### CATALOG\_API\_TYPE: PRIVATE

If you use [private connectivity for inbound network traffic in Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/private-connectivity-inbound),
use this catalog integration to connect Snowflake to Open Catalog through a private IP address.

Copy code

```
CREATE [ OR REPLACE ] CATALOG INTEGRATION [ IF NOT EXISTS ]
  <name>
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  [ CATALOG_NAMESPACE = '<open_catalog_namespace>' ]
  REST_CONFIG = (
    CATALOG_URI = '<open_catalog_account_url>'
    CATALOG_API_TYPE = PRIVATE
    CATALOG_NAME = '<open_catalog_catalog_name>'
    [ ACCESS_DELEGATION_MODE = { VENDED_CREDENTIALS | EXTERNAL_VOLUME_CREDENTIALS } ]
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_CLIENT_ID = '<oauth_client_id>'
    OAUTH_CLIENT_SECRET = '<oauth_secret>'
    OAUTH_ALLOWED_SCOPES = ('<scope 1>', '<scope 2>')
  )
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
:   Specifies Snowflake Open Catalog as the catalog source.

`TABLE_FORMAT = ICEBERG`
:   Specifies Apache Iceberg™ as the table format supplied by the catalog.

`REST_CONFIG = ( ... )`
:   Specifies information about your Open Catalog account and catalog name.

> `CATALOG_URI = 'https://open_catalog_account_url'`
> :   Your Open Catalog account URL. Supported values are:
>
>     - `https://<open_catalog_account_identifier>.snowflakecomputing.com/polaris/api/catalog`: When `CATALOG_API_TYPE = PUBLIC`. Examples values:
>
>       - `https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com/polaris/api/catalog`
>       - `https://<account_locator>.<cloud_region_id>.<cloud>.snowflakecomputing.com/polaris/api/catalog`
>
>       Note
>
>       - To find your Snowflake organization name (`orgname`), follow the steps in [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).
>       - To find `<my-snowflake-open-catalog-account-name`,
>         see [Find the account name for a Snowflake Open Catalog account](https://other-docs.snowflake.com/en/opencatalog/find-account-name) in
>         the Snowflake Open Catalog documentation.
>
>       - To find your `<account_locator>`, `<cloud_region_id>`, and `<cloud>`, see [Format 2: Account locator in a region](/user-guide/admin-account-identifier#label-account-locator).
>     - `https://<open_catalog_privatelink_account_url>/polaris/api/catalog`: When `CATALOG_API_TYPE = PRIVATE`.
>
>       Note
>
>       For `open_catalog_privatelink_account_url`, enter one of the following values:
>
>       - **PrivateLink Account URL**
>       - **Regionless PrivateLink Account URL**
>
>       To obtain these values, retrieve your Open Catalog account settings for private connectivity. For details, see the instructions for the
>       cloud platform where your Open Catalog account is hosted:
>
>       - [AWS](http://docs.snowflake.com/user-guide/opencatalog/private-connectivity-inbound-configure-aws#step-3-retrieve-your-open-catalog-account-settings)
>       - [Azure](http://docs.snowflake.com/user-guide/opencatalog/private-connectivity-inbound-configure-azure#step-1-retrieve-your-open-catalog-account-settings)
>
> `CATALOG_API_TYPE = { PRIVATE | PUBLIC }`
> :   Specifies the catalog API type. If your connection between Snowflake and Open Catalog should be routed through the public internet, this
>     parameter is optional.
>
>     > - `PRIVATE`: If you’re using [private connectivity for inbound network traffic in Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/private-connectivity-inbound),
>     >   connects Snowflake to Open Catalog through a private IP address.
>     > - `PUBLIC`: Connects Snowflake to Open Catalog through the public internet.
>
>     Default: `PUBLIC`
>
> `CATALOG_NAME = 'open_catalog_name'`
> :   Specifies the name of the catalog to use in Open Catalog.
>
> `ACCESS_DELEGATION_MODE = { VENDED_CREDENTIALS | EXTERNAL_VOLUME_CREDENTIALS }`
> :   Specifies the access delegation mode to use for accessing Iceberg table files in your external cloud storage.
>
>     - `VENDED_CREDENTIALS` specifies that Snowflake should use vended credentials.
>     - `EXTERNAL_VOLUME_CREDENTIALS` specifies that Snowflake should use an external volume.
>
>     Default: `EXTERNAL_VOLUME_CREDENTIALS`

`REST_AUTHENTICATION = ( ... )`
:   Specifies authentication details that Snowflake uses to connect to Open Catalog.

    `TYPE = OAUTH`
    :   Specifies OAuth as the authentication type to use.

    `OAUTH_TOKEN_URI = token_server_uri`
    :   Optional URL for your third-party identity provider. To configure a third-party identity provider, see [External OAuth](https://other-docs.snowflake.com/en/opencatalog/oauth-ext-overview)
        in the Snowflake Open Catalog documentation. If the OAuth identity provider is not specified, Snowflake assumes that it is the remote catalog provider.

        Important

        If you’re using External OAuth with private connectivity (CATALOG\_API\_TYPE=PRIVATE), Snowflake routes the token requests for External
        OAuth over the public internet.

    `OAUTH_CLIENT_ID = 'oauth_client_id'`
    :   The client ID of the OAuth2 credential associated with your Open Catalog service connection.

    `OAUTH_CLIENT_SECRET = 'oauth_secret'`
    :   The secret of the OAuth2 credential associated with your Open Catalog service connection.

    `OAUTH_ALLOWED_SCOPES = ( 'scope_1', 'scope_2')`
    :   One or more scopes for the OAuth token.

`ENABLED = {TRUE | FALSE}`
:   Specifies whether the catalog integration is available to use for Iceberg tables.

    > - `TRUE` allows users to create new Iceberg tables that reference this integration. Existing Iceberg tables that reference
    >   this integration function normally.
    > - `FALSE` prevents users from creating new Iceberg tables that reference this integration. Existing Iceberg tables that
    >   reference this integration cannot access the catalog in the table definition.

    The value is case-insensitive.

    The default is `TRUE`.

## Optional parameters

`CATALOG_NAMESPACE = 'open_catalog_namespace'`
:   - If you’re creating the catalog integration to [query a table in Snowflake Open Catalog using Snowflake](/user-guide/tables-iceberg-open-catalog-query),
      you can optionally specify the namespace from Open Catalog. Snowflake uses this namespace for all Iceberg tables that you associate with
      this catalog integration.

      If specified, you can override this value at the table level when you create a table. If not specified, you
      must set a namespace at the table level when you create a table.
    - If you’re creating the catalog integration to [sync a Snowflake-managed table with Snowflake Open Catalog](/user-guide/tables-iceberg-open-catalog-sync),
      this parameter has no effect on how you sync the table with Open Catalog. Snowflake syncs the table to the external catalog in Open Catalog
      that you specify in the catalog integration by using a predefined rule.

      For example, if you have a `db1.public.table1`
      Iceberg table registered in Snowflake and you specify `catalog1` in the catalog integration, Snowflake syncs the table with Open Catalog
      with the following fully qualified name: `catalog1.db1.public.table1`.

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
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

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

- To troubleshoot issues with creating a catalog integration, see [You can’t create a catalog integration for Open Catalog](/user-guide/tables-iceberg-open-catalog-troubleshooting#label-create-catalog-integration-open-catalog-troubleshooting).

## Examples

The following example creates a catalog integration for Open Catalog for a particular namespace in an internal catalog
in Open Catalog to query tables grouped under this namespace in Snowflake. For more information about internal catalogs in Open Catalog, see
[Catalog types](https://other-docs.snowflake.com/en/opencatalog/overview#catalog-types) in the Open Catalog documentation.

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION open_catalog_int
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'my_catalog_namespace'
  REST_CONFIG = (
    CATALOG_URI = 'https://my_org_name-my_snowflake_open_catalog_account_name.snowflakecomputing.com/polaris/api/catalog'
    CATALOG_NAME = 'my_catalog_name'
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_CLIENT_ID = 'my_client_id'
    OAUTH_CLIENT_SECRET = 'my_client_secret'
    OAUTH_ALLOWED_SCOPES = ('PRINCIPAL_ROLE:ALL')
  )
  ENABLED = TRUE;
```

The following example creates a catalog integration for Open Catalog to sync Snowflake-managed tables to the `customers` catalog in
Open Catalog, which is an external catalog. For more information about external catalogs in Open Catalog, see
[Catalog types](https://other-docs.snowflake.com/en/opencatalog/overview#catalog-types) in the Open Catalog documentation.

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION open_catalog_int2
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = 'https://my_org_name-my_snowflake_open_catalog_account_name.snowflakecomputing.com/polaris/api/catalog'
    CATALOG_NAME = 'customers'
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_CLIENT_ID = 'my_client_id'
    OAUTH_CLIENT_SECRET = 'my_client_secret'
    OAUTH_ALLOWED_SCOPES = ('PRINCIPAL_ROLE:my-principal-role', 'PRINCIPAL_ROLE:my-principal-role2', 'PRINCIPAL_ROLE:my-principal-role3')
  )
  ENABLED = TRUE;
```
