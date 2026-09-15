# April 13, 2026: Dynamic Apache Iceberg™ tables now support PARTITION BY, TARGET\_FILE\_SIZE, and PATH\_LAYOUT (*General availability*)

Dynamic Apache Iceberg™ tables now support the following table properties:

- `PARTITION BY`: Partition the table using Iceberg partition expressions such as identity, bucket, truncate, year, month, day, and hour transforms.
- `TARGET_FILE_SIZE`: Control the target Parquet file size for table writes. Defaults to `AUTO`, which lets Snowflake choose the optimal file size.
- `PATH_LAYOUT`: Choose between a flat or hierarchical (Hive-style) directory layout for data files. Use `HIERARCHICAL` together with `PARTITION BY` to write data to partition-aware paths.

For more information, see [Create a dynamic Iceberg table with Snowflake-managed storage](/user-guide/dynamic-tables/create-iceberg#label-dynamic-tables-tasks-create-iceberg-partitioning) and [CREATE DYNAMIC ICEBERG TABLE](/sql-reference/sql/create-dynamic-table#label-create-dt-iceberg-syntax).
