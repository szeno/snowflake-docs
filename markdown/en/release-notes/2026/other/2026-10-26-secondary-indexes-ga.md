# Oct 26, 2026: Secondary indexes (*General availability*)

With this release, secondary indexes are generally available.

Secondary indexes speed up highly selective point lookups and range queries on columns or expressions. A secondary index maps those values to the micro-partitions that contain them, so Snowflake can skip data that the query doesn’t need. You can create more than one secondary index on a standard table. Secondary indexes aren’t supported on Iceberg tables.

A secondary index can return a result directly when the query is covered by the index, or it can prune micro-partitions in the base table. Snowflake maintains the index automatically. Index maintenance is billed as part of the search optimization service.

These indexes aren’t secondary indexes on hybrid tables.

For more information, see [Secondary indexes](/user-guide/search-optimization/secondary-indexes).
