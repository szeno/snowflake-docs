# June 8, 2026: Apache Iceberg™ tables: Partitioned writes with a hierarchical path layout (*General availability*)

Partitioned writes with a hierarchical path layout for Apache Iceberg™ tables are now generally available.

With this feature, Snowflake writes data to partitioned Iceberg tables by using a hierarchical (Hive-style) directory path layout, where
each partition column is represented as a directory level under the `data/` directory.

This release includes the following updates:

- You can now use the ALTER ICEBERG TABLE command to set PATH\_LAYOUT for an existing table.
- Positional delete files are written into the same directory as the corresponding data file.
- Puffin files containing deletion vectors are always written into the table `data/` directory.

For more information, see [Partitioning with hierarchical paths](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning-hierarchical-paths).
