# Oct 16, 2026: Parquet Direct (*Preview*)

We’re introducing Parquet Direct in preview. With Parquet Direct, you can create read-only Apache Iceberg™ tables in
Snowflake from Apache Parquet™ files in your cloud object storage. Snowflake registers your existing files in place, so you can query
your data without copying it or rewriting it, and with better query performance than external
tables.

This release includes the following capabilities:

- **Schema inference and evolution.** Snowflake automatically infers column definitions from your Parquet files. When you create
  the table with `ENABLE_SCHEMA_EVOLUTION = TRUE`, Snowflake also evolves the table schema as new columns and widened
  types appear.
- **Hive partition inference.** With a catalog integration that uses `TABLE_FORMAT = HIVE`, Snowflake infers partition
  columns from Hive-style `key=value` paths. For other layouts, use `TABLE_FORMAT = NONE` and define partition columns with
  expressions.
- **Event-driven auto-refresh.** Keep tables in sync with files that are added, changed, or deleted in Amazon S3, Azure Blob
  Storage, or Google Cloud Storage.
- **Monitoring.** Track auto-refresh with event tables, the SYSTEM$PARQUET\_DIRECT\_AUTO\_REFRESH\_STATUS function, and the
  ICEBERG\_TABLE\_FILE\_REGISTRATION\_HISTORY table function.

For more information, see the following topics:

- [Parquet Direct](/user-guide/tables-iceberg-parquet-direct)
- [Direct Iceberg tables](/user-guide/tables-iceberg-direct)
- [CREATE ICEBERG TABLE (Parquet files in object storage)](/sql-reference/sql/create-iceberg-table-parquet)

See the following tutorials for step-by-step instructions:

- [Tutorial: Auto-refresh a Parquet Direct table from Amazon S3](/user-guide/tutorials/parquet-direct-auto-refresh-s3)
- [Tutorial: Auto-refresh a Parquet Direct table from Azure Blob Storage](/user-guide/tutorials/parquet-direct-auto-refresh-azure)
- [Tutorial: Auto-refresh a Parquet Direct table from Google Cloud Storage](/user-guide/tutorials/parquet-direct-auto-refresh-gcs)
