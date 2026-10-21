# Delta Direct

**Delta Direct** lets you create a read-only [Apache Iceberg™ table](/user-guide/tables-iceberg) in Snowflake from a Delta
Lake table in external cloud object storage. Snowflake reads the Delta transaction log (`_delta_log/`) and registers the
table’s Parquet data files without copying or rewriting them, so you can query your Delta Lake data with Snowflake while
other engines continue to write to it.

Delta Direct is one type of [Direct Iceberg table](/user-guide/tables-iceberg-direct).

## Create a Delta Direct table

To create a Delta Direct table, complete the following steps:

1. Create an external volume that points to the cloud storage location of your Delta table. For instructions, see
   [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume).
2. Create a catalog integration with `CATALOG_SOURCE = OBJECT_STORE` and `TABLE_FORMAT = DELTA`. For instructions, see
   [Delta Lake table files](/user-guide/tables-iceberg-configure-catalog-integration-object-storage#label-tables-iceberg-create-cat-int-delta).
3. Create an Iceberg table with [CREATE ICEBERG TABLE (Delta files in object storage)](/sql-reference/sql/create-iceberg-table-delta).

The following example shows these steps:

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

## Refresh a Delta Direct table

To keep the table in sync with your Delta table, set a refresh interval on the catalog integration and use automated
refresh, or refresh the table manually with [ALTER ICEBERG TABLE … REFRESH](/sql-reference/sql/alter-iceberg-table-refresh). For more information,
see [Automatically refresh Apache Iceberg™ tables](/user-guide/tables-iceberg-auto-refresh).

## Storage access and metadata writes

Delta Direct only needs read access to your storage. If your external volume allows writes, Snowflake can also write
Iceberg metadata for the table to your storage. For more information, see [Delta-based tables](/user-guide/tables-iceberg-metadata#label-tables-iceberg-metadata-delta) and
[Read-only vs write access for Delta Direct on each storage provider](/user-guide/tables-iceberg-metadata#label-tables-iceberg-ev-delta-read-write-options).

## Data types

For how Delta data types map to Snowflake data types, see [Delta data types](/user-guide/tables-iceberg-data-types#label-tables-iceberg-delta-source-data-types).

## Considerations and limitations

For limitations, see the following sections:

- [Usage notes](/sql-reference/sql/create-iceberg-table-delta#label-tables-iceberg-create-delta-limitations)
- [Refresh](/sql-reference/sql/create-iceberg-table-delta#label-tables-iceberg-delta-refresh-limitations)
