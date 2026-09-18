# Sep 18, 2026: Apache Iceberg™ tables: Partition evolution (*General availability*)

With this release, we’re pleased to announce the general availability of partition evolution for Snowflake-managed Iceberg tables. You can now change a table’s partition specification after you create the table by adding, dropping, or replacing partition fields, without rewriting existing data.

New data written after you evolve the partition spec uses the updated spec, while existing data stays in place. Snowflake supports all partition transforms in version 2 of the Apache Iceberg specification.

For more information, see [ALTER ICEBERG TABLE … ADD | DROP | REPLACE PARTITION BY](/sql-reference/sql/alter-iceberg-table-partition-evolution).
