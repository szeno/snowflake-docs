# Write support for externally managed Apache Iceberg™ tables

Write support for externally managed [Apache Iceberg™ tables](/user-guide/tables-iceberg) lets you perform write operations on tables managed by an external
Iceberg REST catalog. The Iceberg table in Snowflake is linked to a table in your remote catalog.
When you make changes to the table in Snowflake, Snowflake commits the same changes to your remote catalog.

This feature expands interoperability between Snowflake and third-party systems,
so that you can use Snowflake for data engineering workloads with Iceberg even when you use an external Iceberg catalog.

The following list shows some key use cases:

- **Building complex data engineering pipelines with Iceberg tables**: Writing to Iceberg tables in external catalogs from Snowflake
  allows you to use Snowpark or Snowflake SQL to build complex pipelines that ingest, transform, and process data for Iceberg tables.
  You can query the data by using Snowflake or other engines.
  Similarly, you can use Snowflake [partner tools](https://www.snowflake.com/en/why-snowflake/partners/all-partners/) to build your Iceberg data engineering pipelines.
- **Making your data available to the Iceberg ecosystem**: The ability to write to Iceberg tables in external catalogs lets you make your
  data available to the Iceberg ecosystem. You can query data that’s already in Snowflake and write it to Iceberg tables.
  To keep your Iceberg tables in sync with your Snowflake tables, you can use operations like INSERT INTO … SELECT FROM to do the following:
  - Copy existing data from a standard Snowflake table into an Iceberg table.
  - Insert data with Snowflake streams.

## Workflow

Use the workflow in this section to get started with this feature:

1. Configure a catalog integration with vended credentials.
   For instructions, see
   [Use catalog-vended credentials for Apache Iceberg™ tables](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials).

   The following topics explain how to configure a catalog integration for specific catalogs:

   - [Databricks Unity Catalog](/user-guide/tables-iceberg-configure-catalog-integration-rest-unity)
   - [AWS Glue](/user-guide/tables-iceberg-configure-catalog-integration-rest-glue)
   - [Snowflake Open Catalog](/user-guide/tables-iceberg-configure-catalog-integration-open-catalog)

   Note

   If your remote Iceberg catalog doesn’t support credential vending, you must configure an
   [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) and a
   [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def).

   First,
   [configure an external volume for your cloud storage provider](/user-guide/tables-iceberg-configure-external-volume).
   Ensure that both read and write operations are allowed for the external volume by setting the ALLOW\_WRITES parameter to `TRUE`,
   which is the default. For more information about the required permissions, see [Granting Snowflake access to your storage](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-grant-access-to-storage).

   If your Databricks workspace is on Azure and you use an external volume instead of vended credentials, configure the external volume to
   connect to Data Lake Storage Gen2 for write operations. For more information, see
   [Enable interoperability with remote catalogs that use Data Lake Storage](/user-guide/tables-iceberg-configure-external-volume-azure#label-tables-iceberg-configure-external-volume-azure-catalog-compatibility).

   Then,
   [configure an Apache Iceberg™ REST catalog integration for your remote Iceberg catalog](/user-guide/tables-iceberg-configure-catalog-integration-rest).
   Your remote catalog must comply with the
   open source [Apache Iceberg REST OpenAPI specification](https://github.com/apache/iceberg/blob/main/open-api/rest-catalog-open-api.yaml),
   If you currently use a [catalog integration for AWS Glue](/user-guide/tables-iceberg-configure-catalog-integration-glue),
   you must create a new REST catalog integration for the AWS Glue Iceberg REST endpoint.
2. Choose from the following options:

   - [Create a catalog-linked database](#label-tables-iceberg-external-writes-create-cld). With this option,
     you can write to auto-discovered Iceberg tables in your catalog, or use the catalog-linked database to create additional Iceberg tables.
   - [Create an Iceberg table](#label-tables-iceberg-external-writes-create-table) in a standard Snowflake database.
     With this option, you must first create a table in your remote catalog before you create an externally managed Iceberg table in Snowflake.

After you complete these steps, you can perform [write operations](#label-tables-iceberg-externally-managed-write-operations)
on your Iceberg tables.

## Create a catalog-linked database

Snowflake supports creating writable externally managed tables in a catalog-linked database, which
is a Snowflake database that you sync with an external Iceberg REST catalog. You can also write to Iceberg tables that Snowflake
automatically discovers in your remote catalog. For more information, see [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database).

Note

Alternatively, you can create writable externally managed Iceberg tables in a [standard Snowflake database](#label-tables-iceberg-external-writes-create-table-standard-db).

The following example uses the [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked) command to
create a catalog-linked database that uses catalog-vended credentials. This works with any REST catalog, including
Databricks Unity Catalog, AWS Glue, and Snowflake Open Catalog.

Copy code

```
CREATE DATABASE my_catalog_linked_db
  LINKED_CATALOG = (
    CATALOG = 'my_rest_catalog_int'
  );
```

Note

- If you’re using an external volume to connect to your remote catalog, you must specify the `EXTERNAL_VOLUME` parameter with the
  CREATE DATABASE (catalog-linked) command.
- For a complete tutorial on setting up a writable catalog-linked database with Unity Catalog, see
  [Tutorial: Set up bidirectional access to Apache Iceberg™ tables in Databricks Unity Catalog](/user-guide/tutorials/tables-iceberg-set-up-bidirectional-access-to-unity-catalog).

### Use CREATE SCHEMA to create namespaces in your external catalog

To create a namespace for organizing Iceberg tables in your external catalog, you can use the
[CREATE SCHEMA](/sql-reference/sql/create-schema) command with a catalog-linked database.
The command creates a namespace in your linked Iceberg REST catalog and a corresponding schema in your Snowflake database.

Copy code

```
CREATE SCHEMA 'my_namespace';
```

Note

Schema names must be alphanumeric and can’t include delimiters.

#### DROP SCHEMA

You can also use the [DROP SCHEMA](/sql-reference/sql/drop-schema) command to simultaneously drop a
schema from your catalog-linked database and its corresponding namespace from your remote catalog.

Copy code

```
DROP SCHEMA 'my_namespace';
```

## Create an Iceberg table

Creating an externally managed Iceberg table that you can write to from Snowflake varies, depending on the kind of database you use:

- If you use a catalog-linked database, you can use the [Variant syntax](/sql-reference/sql/create-iceberg-table-rest#label-tables-iceberg-external-write-create-table-syntax) to create a table
  *and* register it in your remote catalog. For instructions, see [Create an Iceberg table in a catalog-linked database](#label-tables-iceberg-external-writes-create-table-cld).
- If you use a standard Snowflake database (not linked to a catalog), you must first create a
  table in your remote catalog. Then, you can use the [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest) syntax to create
  an Iceberg table in Snowflake and write to it. For instructions, see [Create an Iceberg table in a standard Snowflake database](#label-tables-iceberg-external-writes-create-table-standard-db).

### Create an Iceberg table in a catalog-linked database

To create a table in Snowflake and in your external catalog at the same time, use the [Variant syntax](/sql-reference/sql/create-iceberg-table-rest#label-tables-iceberg-external-write-create-table-syntax) command.

The following example creates a writable
Iceberg table by using the previously created catalog integration for AWS Glue REST that is configured with catalog-vended credentials.
It also uses the value of a
column named `first_name` to partition the table. For more information, see [Iceberg partitioning](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning).

Copy code

```
USE DATABASE my_catalog_linked_db;

USE SCHEMA my_namespace;

CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
  first_name STRING,
  last_name STRING,
  amount INT,
  create_date DATE
)
TARGET_FILE_SIZE = '64MB'
PARTITION BY (first_name);
```

When you run the command, Snowflake creates a new Iceberg table in your remote catalog and a linked, writable, externally managed table
in Snowflake.

### Create an Iceberg table in a catalog-linked database with hierarchical path layout

To create a table in Snowflake and in your external catalog at the same time with hierarchical path layout for the data files,
use the [Variant syntax](/sql-reference/sql/create-iceberg-table-rest#label-tables-iceberg-external-write-create-table-syntax) command.

The following example creates a writable
Iceberg table by using the previously created catalog integration for AWS Glue REST that is configured with catalog-vended credentials.
It also uses the value of a
column named `first_name` to partition the table. For more information, see [Partitioning with hierarchical paths](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning-hierarchical-paths).

Copy code

```
USE DATABASE my_catalog_linked_db;

USE SCHEMA my_namespace;

CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
  first_name STRING,
  last_name STRING,
  amount INT,
  create_date DATE
)
TARGET_FILE_SIZE = '64MB'
PARTITION BY (first_name)
PATH_LAYOUT = HIERARCHICAL;
```

When you run the command, Snowflake creates a new Iceberg table in your remote catalog and a linked, writable, externally managed table
in Snowflake.

With this option, Snowflake writes data to partitioned Iceberg tables by using a hierarchical path layout
for files where partitioning information is included in the file paths. You might use this option when you need to use both Snowflake and
external engines to write to the same Iceberg table by using a hierarchical path layout for partitions.

### Create an Iceberg table in a standard Snowflake database

If using a standard Snowflake database, you must first create a table in your remote catalog. For example, you might use Spark to write
an Iceberg table to Open Catalog.

After you create the table in your remote catalog, use the [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest) command to create an
Iceberg table object in Snowflake. For the CATALOG\_TABLE\_NAME, specify the name of the table as it appears in your remote catalog.

For example:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table
  EXTERNAL_VOLUME = 'my_external_volume'
  CATALOG = 'my_rest_catalog_integration'
  CATALOG_TABLE_NAME = 'my_remote_table_name';
```

When you run the command, Snowflake creates a writable, externally managed table
in Snowflake that is linked to the existing table in your remote catalog.

Note

If you create partition columns on the table outside of Snowflake,
Snowflake infers the partitions from the table metadata.
For more information about partitioning, see [Iceberg partitioning](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning).

## Dropping an Iceberg table

You can drop a writable externally managed Iceberg table by using the [DROP ICEBERG TABLE](/sql-reference/sql/drop-iceberg-table) command.

Copy code

```
DROP ICEBERG TABLE my_iceberg_table;
```

For a table in a [catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database), Snowflake drops the table entry
in Snowflake and instructs your remote Iceberg catalog to drop the table entry there as well. By default, Snowflake does not
signal the catalog to delete the table’s underlying data and metadata files from storage. Snowflake only drops the table in
Snowflake after confirming that the table has successfully been dropped from the remote catalog.

Note

For a writable externally managed Iceberg table in a standard Snowflake database (not a catalog-linked database),
`DROP ICEBERG TABLE` removes only the table entry in Snowflake. It doesn’t drop or deregister the table in your remote
catalog. To remove the table from the remote catalog, use the catalog’s own API or tooling.

### Deleting underlying data files on drop (PURGE)

To also remove the underlying data and metadata files from storage when a table is dropped, use the `PURGE` keyword
or the `PURGE_ON_DROP_TABLE` parameter.

When purge is requested, Snowflake forwards purge intent in the drop-table request to the external catalog.
Snowflake never deletes external data files directly — the external catalog is responsible for the actual
file deletion. Whether files are actually removed depends on the catalog implementation.

#### PURGE keyword

Specify `PURGE` on individual `DROP TABLE` statements to forward the purge intent on a case-by-case basis:

Copy code

```
DROP ICEBERG TABLE my_iceberg_table PURGE;
```

You can also use `PURGE` with `CREATE OR REPLACE ICEBERG TABLE` to forward the purge intent on the implicit drop
of the replaced table:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (id INT, name STRING) PURGE;
```

#### PURGE\_ON\_DROP\_TABLE parameter

For catalogs that always require purge on drop — such as Amazon S3 Tables, which does not support dropping a table
without deleting its files — set `PURGE_ON_DROP_TABLE = TRUE` on the catalog-linked database. This way, every
`DROP TABLE` and every implicit drop from `CREATE OR REPLACE TABLE` in that database automatically forwards the
purge intent to the catalog, without requiring the explicit `PURGE` keyword each time.

Copy code

```
-- Set PURGE_ON_DROP_TABLE at the catalog-linked database level so that
-- all tables in this database are automatically purged on DROP.
-- This is useful for catalogs like Amazon S3 Tables that require purge on drop.
ALTER DATABASE my_s3tables_cld SET PURGE_ON_DROP_TABLE = TRUE;

-- DROP TABLE automatically forwards purge=true to the catalog.
DROP ICEBERG TABLE my_iceberg_table;

-- CREATE OR REPLACE TABLE also forwards purge=true to the catalog on the
-- implicit drop of the replaced table.
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (id INT, name STRING);
```

You can also set `PURGE_ON_DROP_TABLE` at the schema or table level for finer-grained control.

Note

- If you use the AWS Glue Data Catalog as your external catalog, the catalog does not honor the purge flag, so
  the underlying table files are retained regardless of whether `PURGE` is specified or `PURGE_ON_DROP_TABLE`
  is set to `TRUE`. This behavior is specific to the AWS Glue Data Catalog implementation.
- Dropping an Amazon S3 Table isn’t currently supported without specifying `PURGE` or setting
  `PURGE_ON_DROP_TABLE = TRUE` on the containing database.

## Writing to externally managed Iceberg tables

You can use the following DML commands for externally managed Iceberg tables:

- [INSERT](/sql-reference/sql/insert)

  - [Example: Multi-row insert using a query (INSERT INTO … SELECT FROM)](/sql-reference/sql/insert#label-insert-multi-row-query-example)
  - [Example: INSERT INTO … SELECT FROM (stream)](/user-guide/streams-examples#label-stream-examples-tables)
- [UPDATE](/sql-reference/sql/update)
- [DELETE](/sql-reference/sql/delete)
- [MERGE](/sql-reference/sql/merge)
- [TRUNCATE TABLE](/sql-reference/sql/truncate-table)
- [COPY INTO <table>](/sql-reference/sql/copy-into-table). For more information, see [Load data into Apache Iceberg™ tables](/user-guide/tables-iceberg-load).

You can also use the [Snowpark API](/developer-guide/snowpark/index) to process Iceberg tables.

### Examples

You can use the following basic examples to get started with writing to Iceberg tables.

#### INSERT

Use [INSERT](/sql-reference/sql/insert) to insert values into an Iceberg table:

Copy code

```
INSERT INTO my_iceberg_table VALUES (1, 'a');
INSERT INTO my_iceberg_table VALUES (2, 'b');
INSERT INTO my_iceberg_table VALUES (3, 'c');
```

#### UPDATE

Use [UPDATE](/sql-reference/sql/update) to update the values in an Iceberg table:

Copy code

```
UPDATE my_iceberg_table
  SET a = 10
  WHERE b = 'b';
```

#### DELETE

Use [DELETE](/sql-reference/sql/delete) to remove values from an Iceberg table:

Copy code

```
DELETE my_iceberg_table
  WHERE b = 'a';
```

#### MERGE

Use [MERGE](/sql-reference/sql/merge) on an Iceberg table:

Copy code

```
MERGE INTO my_iceberg_table USING my_snowflake_table
  ON my_iceberg_table.a = my_snowflake_table.a
  WHEN MATCHED THEN
      UPDATE SET my_iceberg_table.b = my_snowflake_table.b
  WHEN NOT MATCHED THEN
      INSERT VALUES (my_snowflake_table.a, my_snowflake_table.b);
```

#### COPY INTO <table>

Use [COPY INTO <table>](/sql-reference/sql/copy-into-table) to load data into an Iceberg table.

Copy code

```
COPY INTO customer_iceberg_ingest
  FROM @my_parquet_stage
  FILE_FORMAT = 'my_parquet_format'
  MATCH_BY_COLUMN_NAME = CASE_SENSITIVE;
```

For more information, see [Load data into Apache Iceberg™ tables](/user-guide/tables-iceberg-load).

#### Change Data Capture using streams

A [table stream](/user-guide/streams-intro) tracks changes made to rows in a source table for Change Data Capture (CDC).
The source table can be a standard Snowflake table, a Snowflake-managed Iceberg table, or an externally managed Iceberg table.
You can insert the changes into an externally managed Iceberg table using the INSERT INTO… SELECT FROM… command.

Note

If your source table is an externally managed Iceberg table, you must use INSERT\_ONLY = TRUE when you create the stream.

Copy code

```
CREATE OR REPLACE STREAM my_stream ON TABLE my_snowflake_table;

//...

INSERT INTO my_iceberg_table(id,name)
  SELECT id, name
  FROM my_stream;
```

#### Using Snowpark

Create a function to copy data into an Iceberg table from a Snowflake table by using Snowpark Python.

Copy code

```
def copy_into_iceberg():

  try:
      df = session.table("my_snowflake_table")

      df.write.save_as_table("my_iceberg_table")

  except Exception as e:
      print(f"Error processing {table_name}: {e}")
```

## Troubleshooting

If an issue occurs when Snowflake attempts to commit table changes to your external catalog, Snowflake returns one of the
following error messages.

|  |  |
| --- | --- |
| Error | ``` 004185=SQL Execution Error: Failed while committing transaction to external catalog. Error:''{0}'' ```  Or:  ``` 004185=SQL Execution Error: Failed while committing transaction to external catalog with unresolvable commit conflicts. Error:''{0}'' ``` |
| Cause | A commit to the external catalog failed, where `{0}` is the exception returned by the external catalog (if available); otherwise, Snowflake reports `Exception unavailable` as the cause. The error message includes `with unresolvable commit conflicts` if Snowflake encountered an unresolvable commit conflict while attempting to commit a transaction to the external catalog. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` 004500=SQL Execution Error: Cannot verify the status of transaction from external catalog. The statement ''{0}'' with transaction id {1} may or may not have committed to external catalog. Error:''{2}'' ``` |
| Cause | A commit to the external catalog resulted in no response from the external catalog. The message includes the exception returned by the external catalog (if available); otherwise, Snowflake reports `Exception unavailable` as the cause. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` SQL Execution Error: An error occurred while interacting with the external catalog. Please check the external catalogs logs for more details: Entity size has exceeded the maximum allowed size. ``` |
| Cause | AWS Glue has limits on the size of metadata that can be stored for a table. When the table’s accumulated metadata — such as old snapshots and associated manifest files — exceeds this limit, Glue rejects the commit. |
| Solution | Reduce the table’s metadata size by expiring old snapshots. You can use an Apache Spark procedure to expire snapshots for the affected table. For example:  Copy code  ``` CALL catalog_name.system.expire_snapshots('db_name.table_name'); ```  For more information, see [Expire Snapshots](https://iceberg.apache.org/docs/latest/spark-procedures/#expire_snapshots) in the Apache Iceberg™ documentation. |

Expand

Show lessSee more

## Considerations

Consider the following when you use write support for externally managed Iceberg tables:

- Snowflake supports externally managed writes for Iceberg tables that use version 2 or version 3 of the
  [Iceberg table specification](https://iceberg.apache.org/spec/).
- Snowflake provides Data Definition Language (DDL) and Data Manipulation Language (DML) commands for externally managed tables. However,
  you configure metadata and data retention using your external catalog and the tools provided by your external storage provider.
  For more information, see [Tables that use an external catalog](/user-guide/tables-iceberg-metadata#label-tables-iceberg-metadata-externally-managed).

  For writes, Snowflake ensures that changes are committed to your remote catalog before updating the table in Snowflake.
- If you use a catalog-linked database, you can use the CREATE ICEBERG TABLE syntax with column definitions to create a table in Snowflake
  *and* in your remote catalog. If you use a standard Snowflake database (not linked to a catalog), you must first create a
  table in your remote catalog. After that, you can use the [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest) syntax to create
  an Iceberg table in Snowflake and write to it.
- When you use `CREATE OR REPLACE` to create an Iceberg table, behavior depends on the database type:

  - **Catalog-linked database:** Snowflake drops and recreates the table in the remote catalog. The new table has a new `table-uuid`.
  - **Standard Snowflake database (not linked to a catalog):** Snowflake drops and recreates only the Snowflake table object. The table in the remote catalog is unchanged.
- For the AWS Glue Data Catalog: Dropping an externally managed table through Snowflake doesn’t delete
  the underlying table files. This behavior is specific to the AWS Glue Data Catalog implementation.
- [Position row-level deletes](https://iceberg.apache.org/spec/#row-level-deletes) are supported for tables stored on
  Amazon S3, Azure, or Google Cloud. Row-level deletes with equality delete files aren’t supported. For more information about row-level deletes,
  see [Use row-level deletes](/user-guide/tables-iceberg-manage#label-tables-iceberg-row-level-deletes). To run DML operations in copy-on-write mode by disabling position deletes, set the
  `ICEBERG_MERGE_ON_READ_BEHAVIOR` parameter to `'DISABLED'` at the table, schema, or database level.
- The following features aren’t currently supported when you use Snowflake to write to externally managed Iceberg tables:

  - Server-side encryption (SSE) for Azure external volumes.
  - Multi-statement transactions. Snowflake supports autocommit transactions only.
  - Conversion to Snowflake-managed tables.
  - External Iceberg catalogs that don’t conform to the Iceberg REST protocol.
  - Using the CREATE ICEBERG TABLE (catalog-linked database) … AS SELECT syntax if you use one of the following catalogs as your remote catalog:

    - AWS Glue
    - Databricks Unity Catalog

    Alternatively, you can use the [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest) syntax to create an empty Iceberg table and then use
    an [INSERT INTO … SELECT](/sql-reference/sql/insert) statement to insert data into the empty table. However, this alternative
    uses two separate transactions, so it doesn’t guarantee atomicity.
- For creating schemas in a catalog-linked database, be aware of the following:

  - The CREATE SCHEMA command creates a corresponding namespace in your remote catalog only when you use a catalog-linked database.
  - The ALTER and CLONE options aren’t supported.
  - Delimiters aren’t supported for schema names. Only alphanumeric schema names are supported.

- You can set a target file size for a table’s Parquet files. For more information, see [Set a target file size](/user-guide/tables-iceberg-manage#label-tables-iceberg-target-file-size).
- For Azure cloud storage services: Snowflake only supports externally managed writes for Iceberg tables that use the following services for external storage:

  - Blob Storage
  - Data Lake Storage Gen2
  - General-purpose v1
  - General-purpose v2
  - Microsoft Fabric OneLake
- Sharing:

  - Sharing with a listing isn’t currently supported.
  - Direct sharing isn’t currently supported.
