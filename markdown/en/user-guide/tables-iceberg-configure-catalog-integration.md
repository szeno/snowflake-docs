# Configure a catalog integration

A catalog integration is a named, account-level Snowflake object that stores information about how your table metadata is organized for the
following scenarios:

- When you don’t use [Snowflake as the Iceberg catalog](/user-guide/tables-iceberg#label-tables-iceberg-snowflake-as-catalog). For example, you need a
  catalog integration if your table is managed by AWS Glue.
- When you want to integrate with [Snowflake Open Catalog](https://other-docs.snowflake.com/en/opencatalog/overview) to:
  - Query an Iceberg table in Snowflake Open Catalog using Snowflake.
  - Sync a Snowflake-managed Iceberg table with Snowflake Open Catalog so that third-party compute engines can query the table.

A single catalog integration can support one or more Iceberg tables that use the same external catalog.

You must specify a catalog integration to create an Apache Iceberg™ table in Snowflake for the following scenarios:

- Use an external Iceberg catalog.
- Create a table from files in object storage.
- Integrate with Snowflake Open Catalog.
- Use an Iceberg REST catalog.

  Tip

  If you use an Iceberg REST catalog, you can use a Apache Iceberg™ REST catalog integration with a catalog-linked database to bring your external data
  from a remote Iceberg REST catalog into Snowflake.

  A catalog-linked database automatically discovers and stays in sync with the namespaces and tables in your remote catalog. You can use the
  catalog-linked database to read and write to the tables in your remote catalog from Snowflake, while preserving full interoperability
  with your existing Iceberg ecosystem. For more information, see the following topics:

  - [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database)
  - If your external data is in Unity Catalog, see [Tutorial: Set up bidirectional access to Apache Iceberg™ tables in Databricks Unity Catalog](/user-guide/tutorials/tables-iceberg-set-up-bidirectional-access-to-unity-catalog)
  - If your external data is in AWS Glue, see [Build Data Lakes using Apache Iceberg with Snowflake and AWS Glue](https://www.snowflake.com/en/developers/guides/data-lake-using-apache-iceberg-with-snowflake-and-aws-glue/)

## Create a catalog integration

You can create and configure a catalog integration to use with one or more Iceberg tables.

For specific instructions, see the following topics:

- [Configure a catalog integration for Delta Sharing](/user-guide/tables-iceberg-configure-catalog-integration-delta-sharing)
- [Configure a catalog integration for files in object storage](/user-guide/tables-iceberg-configure-catalog-integration-object-storage)
- [Configure a catalog integration for Snowflake Open Catalog](/user-guide/tables-iceberg-configure-catalog-integration-open-catalog)
- [Configure a catalog integration for Apache Iceberg™ REST catalogs](/user-guide/tables-iceberg-configure-catalog-integration-rest)

## Set a default catalog at the account, database, or schema level

To define which catalog to use as the default for Iceberg tables,
you can set the [CATALOG](/sql-reference/parameters#label-catalog) parameter at the following levels:

Account:
:   Account administrators can use the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command to set the parameter for the account.
    If the value is set for the account, all Iceberg tables created in the account that use an external catalog use this
    catalog integration by default.

Object:
:   Users can execute the appropriate [CREATE <object>](/sql-reference/sql/create) or [ALTER <object>](/sql-reference/sql/alter) command
    to override the [CATALOG](/sql-reference/parameters#label-catalog) parameter value at the database or schema level.
    The lowest-scoped declaration is used: schema > database > account.

    In addition to the minimum privileges required to modify an object using the appropriate ALTER *<object\_type>* command,
    a role must have the USAGE privilege on the catalog integration.

Note

Changes to the CATALOG parameter only apply to tables created *after* the change. Existing tables continue to use the
catalog integration specified when they were created.

### Example

The following statement sets a catalog integration (`shared_catalog_integration`) for a database named `my_database_1`:

Copy code

```
ALTER DATABASE my_database_1
  SET CATALOG = 'shared_catalog_integration';
```

After setting a catalog integration at the database level, you can create an Iceberg table in that database
without specifying a catalog integration. The following statement creates an Iceberg table from metadata in object storage in `my_database_1`
that uses the default catalog integration (`shared_catalog_integration`) set for the database.

Copy code

```
CREATE ICEBERG TABLE my_iceberg_table
   EXTERNAL_VOLUME='my_external_volume'
   METADATA_FILE_PATH='path/to/metadata/v1.metadata.json';
```
