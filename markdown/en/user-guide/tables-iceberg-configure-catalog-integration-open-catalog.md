# Configure a catalog integration for Snowflake Open Catalog

Note

These instructions also apply to configuring a catalog integration for Apache Polaris™.

Create a catalog integration for [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview), which you can use to query a
table in Snowflake Open Catalog using Snowflake or sync a Snowflake-managed table with Open Catalog.
For more information, see [Use Apache Iceberg™ tables with Snowflake Open Catalog in Snowflake](/user-guide/tables-iceberg-open-catalog).

A catalog integration for Open Catalog is associated with a specific catalog and service connection in your Open Catalog account.

For more information about creating a catalog integration to connect Open Catalog to Snowflake, see the following topics:

- [Query a table in Snowflake Open Catalog using Snowflake](/user-guide/tables-iceberg-open-catalog-query)
- [Sync a Snowflake-managed table with Snowflake Open Catalog](/user-guide/tables-iceberg-open-catalog-sync)

## Example: Create a catalog integration for Open Catalog

To create a catalog integration for Open Catalog, use the [CREATE CATALOG INTEGRATION](/sql-reference/sql/create-catalog-integration-open-catalog) command.

For example:

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION my_open_catalog_int
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'myOpenCatalogCatalogNamespace'
  REST_CONFIG = (
    CATALOG_URI = 'https://ABCDEFG-ACCOUNT1.snowflakecomputing.com/polaris/api/catalog'
    CATALOG_NAME = 'myOpenCatalogExternalCatalogName'
  )
  REST_AUTHENTICATION = (
    TYPE = OAUTH
    OAUTH_CLIENT_ID = 'myClientId'
    OAUTH_CLIENT_SECRET = 'myClientSecret'
    OAUTH_ALLOWED_SCOPES = ('PRINCIPAL_ROLE:ALL')
  )
  ENABLED = TRUE;
```

- The value for CATALOG\_URI is your Open Catalog account URL. For more information, see the
  [CATALOG\_URI](/sql-reference/sql/create-catalog-integration-open-catalog#label-create-catalog-integration-open-catalog-catalog-uri) parameter description.
- If you’re [syncing a Snowflake-managed table with Open Catalog](/user-guide/tables-iceberg-open-catalog-sync), the
  CATALOG\_NAMESPACE parameter isn’t required and doesn’t affect how you sync the table with Open Catalog. Snowflake syncs
  the table to the external catalog in Open Catalog that you specify in the catalog integration, along with its parent namespace
  from Snowflake.

  For example, if you have a `db1.public.table1` Iceberg table registered in Snowflake and you specify `catalog1`
  in the catalog integration, Snowflake syncs the table with Open Catalog with the following fully qualified name: `catalog1.db1.public.table1`.

Note

To check your authentication configuration, see [Check a configuration for OAuth](/user-guide/tables-iceberg-configure-catalog-integration-rest-check-config#label-tables-iceberg-rest-catalog-integration-verify-oauth).
