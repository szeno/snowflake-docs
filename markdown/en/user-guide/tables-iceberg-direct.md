# Direct Iceberg tables

A Direct Iceberg table is a read-only [Apache Iceberg™ table](/user-guide/tables-iceberg) in Snowflake that reads data in
your data lake in place, in a format other than Iceberg. Snowflake registers your existing data files without copying or
rewriting them, so you can query your data lake with Snowflake while your existing pipelines and other engines continue to
write the data.

## When to use Direct Iceberg tables

Use a Direct Iceberg table when you want to:

- **Query a data lake in place.** Analyze Delta Lake or Parquet data with Snowflake without building an ingestion pipeline
  or keeping a second copy of the data.
- **Get Iceberg table performance on existing data.** Direct Iceberg tables use the same query engine as other Iceberg tables
  in Snowflake, which performs better than [external tables](/user-guide/tables-external-intro).
- **Keep your data current automatically.** Snowflake can refresh the table as files in your storage change.
- **Modernize toward Iceberg incrementally.** Bring existing data lake tables under Snowflake governance and access control
  today, and convert to the Iceberg format on your own timeline. Because the data stays in place, you can adopt Snowflake
  without disrupting the engines and pipelines that produce your data.

## Types of Direct Iceberg tables

| Type | Source data | Catalog integration | Learn more |
| --- | --- | --- | --- |
| Delta Direct | Delta Lake tables: Parquet data files and a Delta transaction log (`_delta_log/`). | `CATALOG_SOURCE = OBJECT_STORE` `TABLE_FORMAT = DELTA` | [Delta Direct](/user-guide/tables-iceberg-delta-direct) [CREATE ICEBERG TABLE (Delta files in object storage)](/sql-reference/sql/create-iceberg-table-delta) |
| Parquet Direct (preview) | Plain Apache Parquet™ files with no table format, optionally organized with Hive-style `key=value` partitions. | `CATALOG_SOURCE = OBJECT_STORE` `TABLE_FORMAT = NONE` or `HIVE` | [Parquet Direct](/user-guide/tables-iceberg-parquet-direct) [CREATE ICEBERG TABLE (Parquet files in object storage)](/sql-reference/sql/create-iceberg-table-parquet) |

Expand

Show lessSee more

## Requirements

All Direct Iceberg tables need the following objects:

- An [external volume](/user-guide/tables-iceberg-storage) that gives Snowflake access to the storage location of your data.
- A [catalog integration for object storage](/sql-reference/sql/create-catalog-integration-object-storage) with the
  `TABLE_FORMAT` for your source data.
