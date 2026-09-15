# Create an Apache Iceberg™ table in Snowflake

Create [Apache Iceberg™ tables](/user-guide/tables-iceberg) in Snowflake for different [Catalog options](/user-guide/tables-iceberg#label-tables-iceberg-catalog-options).
You can create an Iceberg table by using the [CREATE ICEBERG TABLE](/sql-reference/sql/create-iceberg-table) command.

Note

To create an Iceberg table, you must have a running warehouse that is specified as the current warehouse for your session.
Errors might occur if no running warehouse is specified when you create an Iceberg table.
For more information, see [Working with Warehouses](/user-guide/warehouses-tasks).

## Snowflake storage for Apache Iceberg™ tables

Snowflake storage is the recommended way to create a Snowflake-managed Iceberg table.
Snowflake stores and manages the Iceberg table files for you, so you don’t configure or grant access to
external cloud storage. Set `EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'` (or rely on defaults when the catalog
is Snowflake). You don’t create a separate external volume object.

The following example creates an Iceberg table that uses Snowflake storage:

Copy code

```
CREATE ICEBERG TABLE my_iceberg_table (col1 int)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED';
```

For more information, see [Snowflake storage for Apache Iceberg™ tables](/user-guide/tables-iceberg-internal-storage).

## Snowflake-managed tables in your own cloud storage

To create a Snowflake-managed Iceberg table and keep the table files in your own cloud storage, specify an
[external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) and a base location (directory on the external volume)
where Snowflake can write table data and metadata. Create an [external volume](/sql-reference/sql/create-external-volume)
and reference it from the table. For instructions, see [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).

To define table columns, you can use Iceberg data types. For more information, see [Data types for Apache Iceberg™ tables](/user-guide/tables-iceberg-data-types).

The following example creates an Iceberg table with Snowflake as the Iceberg catalog, and uses the value of the column named `int_col`
to [partition the table](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning):

Copy code

```
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
    boolean_col boolean,
    int_col int,
    long_col long,
    float_col float,
    double_col double,
    decimal_col decimal(10,5),
    string_col string,
    fixed_col fixed(10),
    binary_col binary,
    date_col date,
    time_col time,
    timestamp_ntz_col timestamp_ntz(6),
    timestamp_ltz_col timestamp_ltz(6)
  )
  PARTITION BY (int_col)
  CATALOG = 'SNOWFLAKE'
  EXTERNAL_VOLUME = 'my_ext_vol'
  BASE_LOCATION = 'my/relative/path/from/extvol';
```

Note

Alternatively, use variant syntax.
For more information, see [CREATE TABLE … AS SELECT](/sql-reference/sql/create-iceberg-table-snowflake#label-iceberg-create-table-as-select-syntax) and
[CREATE ICEBERG TABLE … LIKE](/sql-reference/sql/create-iceberg-table-snowflake#label-iceberg-ctlike).

After you create a table that uses Snowflake as the catalog, you can take actions such as:

- [Generating snapshots](/user-guide/tables-iceberg-manage#label-tables-iceberg-generate-snapshots)
- [Querying the table](/user-guide/tables-iceberg-manage#label-tables-iceberg-manage-query)
- [Updating the table](/user-guide/tables-iceberg-manage#label-tables-iceberg-manage-update)

For more information, see [Manage Apache Iceberg™ tables](/user-guide/tables-iceberg-manage).

## External catalog

To create an Iceberg table that uses an external catalog, or no catalog at all, you must specify an
[external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) and a [catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def).
If you use an external Iceberg catalog, you might also need to specify additional parameters. For example, when you use AWS Glue as the catalog,
you must specify a catalog table name.

When you create an Iceberg table that uses an external catalog, Snowflake performs an initial metadata refresh.
You can also manually refresh the table metadata using the [ALTER ICEBERG TABLE … REFRESH](/sql-reference/sql/alter-iceberg-table-refresh) command to
synchronize the metadata with the most recent table changes. For more information, see [Refresh the table metadata](/user-guide/tables-iceberg-manage#label-tables-iceberg-refresh-metadata).

Note

The CREATE ICEBERG TABLE command supports different options for different external catalogs. The examples in this section specify only
some of the available options. To view the full syntax, see the following pages:

> - [CREATE ICEBERG TABLE (AWS Glue as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-aws-glue)
> - [CREATE ICEBERG TABLE (Iceberg files in object storage)](/sql-reference/sql/create-iceberg-table-iceberg-files)
> - [CREATE ICEBERG TABLE (Delta files in object storage)](/sql-reference/sql/create-iceberg-table-delta) (Delta Direct)
> - [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest)

You can also configure data governance (for example, masking or row access policies)
for externally managed tables by using [ALTER ICEBERG TABLE](/sql-reference/sql/alter-iceberg-table).

### Iceberg files in object storage

The following example creates an Iceberg table from Iceberg metadata in external cloud storage,
specifying a relative path to the table metadata on the external volume (`METADATA_FILE_PATH`).

Copy code

```
CREATE ICEBERG TABLE myIcebergTable
  EXTERNAL_VOLUME='icebergMetadataVolume'
  CATALOG='icebergCatalogInt'
  METADATA_FILE_PATH='path/to/metadata/v1.metadata.json';
```

### Delta files in object storage (Delta Direct)

**Delta Direct** is the Snowflake documentation name for this workflow: you store Delta Lake data in external object storage,
configure a catalog integration with `TABLE_FORMAT = DELTA`, and create an Iceberg table that points at the Delta log and
Parquet files. For full syntax, prerequisites, and usage notes, see [CREATE ICEBERG TABLE (Delta files in object storage)](/sql-reference/sql/create-iceberg-table-delta).

The following example command creates an Iceberg table from Delta table files in object storage with
[automated refresh](/user-guide/tables-iceberg-auto-refresh).

The example specifies an external volume associated with the cloud location of the Delta table files,
a [catalog integration configured for Delta](/user-guide/tables-iceberg-configure-catalog-integration-object-storage#label-tables-iceberg-create-cat-int-delta),
and a value for the required `BASE_LOCATION` parameter.

Copy code

```
CREATE ICEBERG TABLE my_delta_iceberg_table
  CATALOG = delta_catalog_integration
  EXTERNAL_VOLUME = delta_external_volume
  BASE_LOCATION = 'relative/path/from/ext/vol/'
  AUTO_REFRESH = TRUE;
```

If the Delta table uses a partitioning scheme, Snowflake automatically interprets the scheme from the Delta log.

### Apache Iceberg™ REST catalog

The following example creates a table that uses a remote
[Iceberg REST catalog](/user-guide/tables-iceberg-configure-catalog-integration-rest).

Copy code

```
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table
  EXTERNAL_VOLUME = 'my_external_volume'
  CATALOG = 'my_rest_catalog_integration'
  CATALOG_TABLE_NAME = 'my_remote_table'
  AUTO_REFRESH = TRUE;
```

For more examples by use case, see the following topics:

- [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database)
- [Write support for externally managed Apache Iceberg™ tables](/user-guide/tables-iceberg-externally-managed-writes)
- [Use catalog-vended credentials for Apache Iceberg™ tables](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials)
- [Query a table in Snowflake Open Catalog using Snowflake](/user-guide/tables-iceberg-open-catalog-query)
