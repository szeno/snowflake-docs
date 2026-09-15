# Best practices

This topic provides best practices for working with Apache Iceberg™ tables in Snowflake.

## Create enough external volumes for your use case

Each external volume is associated with a particular [Active storage location](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-ext-vol-active-storage-location),
and a single external volume can support multiple Iceberg tables. However, the number of external volumes you need depends on how you want to store,
organize, and secure your table data.

You can use a single external volume if you want the data and metadata
for *all* of your Snowflake-Iceberg tables in subdirectories under the same storage location (for example, in the same S3 bucket).
To configure these directories for Snowflake-managed tables, see [Data and metadata directories](/user-guide/tables-iceberg-managing-external-volumes#label-tables-iceberg-configure-external-volume-base-location).

Alternatively, you can create multiple external volumes to secure various storage locations differently. For example,
you might create the following external volumes:

- A read-only external volume for externally managed Iceberg tables.
- An external volume configured with read and write access for Snowflake-managed tables.

## Use the recommended file format options for data loading

For data loading with [COPY INTO <table>](/sql-reference/sql/copy-into-table)
and [Snowpipe](/user-guide/data-load-snowpipe-intro),
use the following format options for your Parquet data files:

- `BINARY_AS_TEXT = FALSE`
- `USE_LOGICAL_TYPE = TRUE`
- `USE_VECTORIZED_SCANNER = TRUE`
- `REPLACE_INVALID_CHARACTERS = TRUE`

## Refresh externally managed tables often

To prevent long refresh times and get the most up-to-date table data quickly,
perform frequent refreshes on Iceberg tables that use an external catalog.

Snowflake attempts to optimize table refreshes when it expects the operation to take a long time.
However, refresh time ultimately depends on the number of snapshots associated with a table, and the number of data
files that belong to a table.

It’s also important to align your Snowflake refresh schedule with table maintenance operations such as snapshot expiration or compaction.
Refresh the metadata each time you perform a maintenance operation.

For instructions, see [Refresh the table metadata](/user-guide/tables-iceberg-manage#label-tables-iceberg-refresh-metadata).

## Write complete statistics

To optimize query runtime performance for tables that aren’t managed by Snowflake,
make sure your Parquet file statistics are as complete as possible.

Ensure that the Parquet file writer you use (for example, Spark or Trino) is configured to write statistics.
You might also need to update your writer to the latest version.

Missing statistics like the following degrade query performance:

- Minimum and maximum values.
- Number of distinct values (NDV). The number of distinct values is used to determine the join order in complex joins. Missing NDV statistics
  can lead to join explosion.
- Number of NULL counts.

## Increase warehouse size

When you create an Iceberg table that uses an external catalog, Snowflake attempts to read statistics from the table manifest files
to provide faster performance.

In some situations, such as when there are missing or incorrect statistics in the manifest files, Snowflake
scans the table data files for statistics. Scanning a large number of data files can slow down table creation.
To accelerate the table creation process, use a larger warehouse that can scan table files in parallel.

Note

Snowflake doesn’t parallelize table column scanning. Switching to a larger warehouse doesn’t result in faster query runtime.

## Choose the right storage serialization policy for your use case

Choose an appropriate `STORAGE_SERIALIZATION_POLICY` for your use case.
When you create a Snowflake-managed table (or convert a table to use Snowflake as the catalog), you set a storage serialization policy for
that table. The serialization policy tells Snowflake what kind of encoding and compression to perform on the table data files.

An unsuitable policy might make a table incompatible with external engines or cause performance degradation in Snowflake.

For more information, see [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-snowflake).

## Use a catalog-linked database to access your remote Iceberg tables

To bring your external data from a remote Apache Iceberg™ REST catalog into Snowflake, use a catalog-linked database. A catalog-linked database
automatically discovers and stays in sync with the namespaces and tables in your remote catalog. You can use a catalog-linked database to
read and write to the tables in your remote catalog from Snowflake, while preserving full interoperability with your existing Iceberg ecosystem.

In addition, a catalog-linked database lets you create new remote Iceberg tables from Snowflake.

For more information, see the following topics:

- [Use a catalog-linked database for Apache Iceberg™ tables](/user-guide/tables-iceberg-catalog-linked-database)
- If your external data is in Unity Catalog, see [Tutorial: Set up bidirectional access to Apache Iceberg™ tables in Databricks Unity Catalog](/user-guide/tutorials/tables-iceberg-set-up-bidirectional-access-to-unity-catalog)
- If your external data is in AWS Glue, see [Build Data Lakes using Apache Iceberg with Snowflake and AWS Glue](https://www.snowflake.com/en/developers/guides/data-lake-using-apache-iceberg-with-snowflake-and-aws-glue/)
