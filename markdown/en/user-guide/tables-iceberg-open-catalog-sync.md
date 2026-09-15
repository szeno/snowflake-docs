# Sync a Snowflake-managed table with Snowflake Open Catalog

Note

New customers should use [Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon)
for Apache Iceberg™ tables and multi-engine interoperability with Iceberg. Customers who
haven’t previously created a Snowflake Open Catalog account can’t sign up for their first Open
Catalog account.

Existing Snowflake Open Catalog customers can continue to use and can create additional
Open Catalog accounts if necessary.

This topic explains how to sync a Snowflake-managed Apache Iceberg™ table with [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview)
so that a third-party engine such as Apache Spark™ can query it.

Important

Snowflake recommends that you query Snowflake-managed Iceberg tables from a third-party engine through
[Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon) instead of syncing the tables with
Open Catalog. With Horizon Catalog, you don’t need to sync the tables with Open Catalog. Syncing Snowflake-managed Iceberg tables with
Open Catalog is no longer recommended.

Important

If your third-party engine can only query tables located up to the second namespace level in a catalog, you must sync
the Snowflake-managed Iceberg table to Open Catalog with one parent namespace. Otherwise, Snowflake will sync the table to the third namespace
level in Open Catalog and you can’t query the table.

To sync a Snowflake-managed Iceberg table with one parent namespace instead of two, set the CATALOG\_SYNC\_NAMESPACE\_MODE property to *FLATTEN*
when you create the database. For information, see [CREATE DATABASE](/sql-reference/sql/create-database). You can’t alter this mode for an existing database.
Tables in an existing database with CATALOG\_SYNC enabled will sync to Open Catalog with two parent namespaces.

## Step 1: Set a BASE\_LOCATION\_PREFIX

Snowflake writes the files for each Iceberg table under a directory that includes a dynamically generated
string (random ID).

To ensure that Open Catalog can see all of the Snowflake-managed tables that you sync, we recommend that you use a
[BASE\_LOCATION\_PREFIX](/sql-reference/parameters#label-base-location-prefix) (such as `my-open-catalog-tables`) at the account, database, or schema level, and
omit the BASE\_LOCATION parameter in your CREATE ICEBERG TABLE statements. Doing so organizes the files for all Iceberg tables
that you create in the account, database, or schema under a known directory with the same name as the prefix. For more information, see
[Data and metadata directories for Snowflake-managed tables](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-base-location).

The following statement sets a BASE\_LOCATION\_PREFIX for a schema named `open_catalog`:

Copy code

```
ALTER SCHEMA open_catalog
  SET BASE_LOCATION_PREFIX = 'my-open-catalog-tables';
```

## Step 2: Create an external volume

If you don’t have one already, start by creating an external volume in Snowflake that provides access to the
cloud storage location where you want to store your table data and metadata.

Note

Don’t include the BASE\_LOCATION\_PREFIX in the path that you specify for the STORAGE\_BASE\_URL.

Complete the instructions for your cloud storage service:

- [Amazon S3](/user-guide/tables-iceberg-configure-external-volume-s3)
- [Google Cloud Storage](/user-guide/tables-iceberg-configure-external-volume-gcs)
- [Azure Storage](/user-guide/tables-iceberg-configure-external-volume-azure)

## Step 3: Configure Open Catalog resources

Next, complete the steps in this section to create an external catalog and service connection in your Open Catalog account.

1. Follow the instructions in [Create a catalog](https://other-docs.snowflake.com/en/opencatalog/create-catalog)
   to create an external catalog in your Open Catalog account. Make sure that the following settings for the external catalog are configured:

   - The **External** toggle is enabled.
   - The **Default base location** combines the `STORAGE_BASE_URL`
     for the external volume you created in [Step 2: Create an external volume](#label-tables-iceberg-open-catalog-sync-create-external-volume) and the `BASE_LOCATION_PREFIX`
     that you set for the schema; for example `s3://<storage_base_url>/<base_url_prefix>/`.

   Open Catalog syncs your Snowflake-managed tables to this external catalog.
2. If you don’t already have a service connection for Snowflake, follow the instructions in [Configure a service connection](https://other-docs.snowflake.com/en/opencatalog/configure-service-connection#configure-a-service-connection)
   to create a connection for the Snowflake engine in your Open Catalog account.
3. Configure a catalog role for your external catalog with privileges that allow access to your external catalog.
   For instructions, see [Grant privileges to a catalog](https://other-docs.snowflake.com/en/opencatalog/secure-catalogs#step-2-grant-privileges-to-a-catalog).

   The catalog role must have the following privileges on the catalog:

   - TABLE\_CREATE
   - TABLE\_WRITE\_PROPERTIES
   - TABLE\_DROP
   - NAMESPACE\_CREATE
   - NAMESPACE\_DROP

   You can either grant each of these privileges to the catalog role, or grant the CATALOG\_MANAGE\_CONTENT privilege, which includes
   these privileges. For more information, see
   [Catalog privileges for Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/access-control#catalog-privileges).
4. Attach the catalog role to the principal role for your service connection. This lets the service connection access the catalog.
   For instructions, see [Grant a catalog role to a principal role](https://other-docs.snowflake.com/en/opencatalog/secure-catalogs#step-3-grant-a-catalog-role-to-a-principal-role).

## Step 4: Create a catalog integration for Open Catalog

Create a catalog integration for Open Catalog by using the [CREATE CATALOG INTEGRATION (Snowflake Open Catalog)](/sql-reference/sql/create-catalog-integration-open-catalog) command.

For CATALOG\_NAME, specify the name of the external catalog that you configured in your Open Catalog account. Snowflake syncs the table and its parent
namespace in Snowflake to this external catalog in Open Catalog. For example, if you have a `db1.public.table1` Iceberg table registered in
Snowflake and you specify `catalog1` in the catalog integration, Snowflake syncs the table with Open Catalog with the following fully
qualified name: `catalog1.db1.public.table1`.

To troubleshoot issues with creating a catalog integration, see [You can’t create a catalog integration for Open Catalog](/user-guide/tables-iceberg-open-catalog-troubleshooting#label-create-catalog-integration-open-catalog-troubleshooting).

Copy code

```
CREATE OR REPLACE CATALOG INTEGRATION my_open_catalog_int
  CATALOG_SOURCE = POLARIS
  TABLE_FORMAT = ICEBERG
  REST_CONFIG = (
    CATALOG_URI = 'https://<orgname>-<my-snowflake-open-catalog-account-name>.snowflakecomputing.com/polaris/api/catalog'
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

Note

You can use this catalog integration to sync one or more Snowflake-managed tables.

## Step 5: Set up catalog sync

For Snowflake to sync Snowflake-managed Iceberg tables to Open Catalog, you must specify the external catalog in Open Catalog that Snowflake
should sync the tables to. To configure this, you set the CATALOG\_SYNC parameter to the name of a catalog integration for Open Catalog.

- [Set CATALOG\_SYNC at the database level](#label-set-up-catalog-sync-at-database-level)
- [Set CATALOG\_SYNC at the schema level](#label-set-up-catalog-sync-at-schema-level)

### Set CATALOG\_SYNC at the database level

This example sets the CATALOG\_SYNC parameter at the database level. After you run these statements, Snowflake syncs all Snowflake-managed Iceberg tables in
the `db1` database to the external catalog in Open Catalog that you specified for the `my_open_catalog_int` catalog integration.
For more information, see the [ALTER DATABASE](/sql-reference/sql/alter-database) command.

Copy code

```
ALTER DATABASE db1 SET CATALOG_SYNC = 'my_open_catalog_int';
```

You can also set CATALOG\_SYNC at the database level when you create a database. For example:

Copy code

```
CREATE DATABASE db2
  CATALOG_SYNC = 'my_open_catalog_int';
```

For more information, see [CREATE DATABASE](/sql-reference/sql/create-database).

### Set CATALOG\_SYNC at the schema level

This example sets the CATALOG\_SYNC parameter at the schema level. After you run these statements, Snowflake syncs all Snowflake-managed Iceberg tables in the
`public` schema to the external catalog in Open Catalog that you specified for the `my_open_catalog_int` catalog integration. For more
information, see the [ALTER SCHEMA](/sql-reference/sql/alter-schema) command.

Copy code

```
ALTER SCHEMA public SET CATALOG_SYNC = 'my_open_catalog_int';
```

You can also set CATALOG\_SYNC at the schema level when you create a schema. For example:

Copy code

```
CREATE SCHEMA schema1
  CATALOG_SYNC = 'my_open_catalog_int';
```

For more information, see [CREATE SCHEMA](/sql-reference/sql/create-schema).

Note

- You can also do the following:

  - Set CATALOG\_SYNC at the account or table level.
  - Override CATALOG\_SYNC at different levels. For example, you can set CATALOG\_SYNC
    at the database level but then override its value for the `myschema` schema within the database. As a result, the Snowflake-managed
    Iceberg tables in the `myschema` schema sync to a different external catalog in Open Catalog than the other Snowflake-managed
    Iceberg tables in the database.

  For more information, see [CATALOG\_SYNC](/sql-reference/parameters#label-catalog-sync) and [Parameter hierarchy and types](/sql-reference/parameters#label-parameter-hierarchy-and-types).
- To see the name of the catalog integration for Open Catalog that a Snowflake-managed Iceberg table syncs to, run the [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables)
  command and see the `catalog_sync_name` column in the output.

## Step 6: Create a Snowflake-managed table

Create a Snowflake-managed Iceberg table by using the [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-snowflake) command.

Important

To ensure that access privileges in Open Catalog are enforced correctly on the table, make sure the table meets certain conditions
before creating it. These conditions relate to the directory structure hierarchy for the catalog. For these conditions and instructions on
how to meet them, see the note in
[Organize catalog content](https://other-docs.snowflake.com/en/opencatalog/organize-catalog-content#conditions-correct-access-privileges)
in the Snowflake Open Catalog documentation.

Copy code

```
USE SCHEMA open_catalog;

CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (col1 INT)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_external_volume';
```

For the BASE\_LOCATION\_PREFIX (`my-open-catalog-tables`) and table name (`my_iceberg_table`) used in the previous example statements,
Snowflake writes the table files to the following paths:

- `STORAGE_BASE_URL/my-open-catalog-tables/my_iceberg_table.randomId/data/`
- `STORAGE_BASE_URL/my-open-catalog-tables/my_iceberg_table.randomId/metadata/`

When you modify the table in Snowflake, the changes are automatically synchronized with the external catalog in your Open Catalog account. Other
engines such as Apache Spark™ can query the table by connecting to Open Catalog.

To troubleshoot issues with creating a Snowflake-managed table, see [You can’t create a Snowflake-managed table](/user-guide/tables-iceberg-open-catalog-troubleshooting#label-create-iceberg-table-snowflake-troubleshooting).
