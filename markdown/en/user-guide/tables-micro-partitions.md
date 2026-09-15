# Understanding Snowflake Table Structures

All data in Snowflake is stored in database tables, logically structured as collections of columns and rows. To best utilize Snowflake tables, particularly large tables, it is helpful to have an
understanding of the physical structure behind the logical structure.

These topics describe *micro-partitions* and *data clustering*, two of the principal concepts utilized in Snowflake physical table structures. They also provide guidance for explicitly defining
*clustering keys* for very large tables (in the multi-terabyte range) to help optimize table maintenance and query performance.

**Next Topics:**

- [Micro-partitions & Data Clustering](/user-guide/tables-clustering-micropartitions)
- [Clustering Keys & Clustered Tables](/user-guide/tables-clustering-keys)
- [Automatic Clustering](/user-guide/tables-auto-reclustering)
- [Manual Reclustering — Deprecated](/user-guide/tables-clustering-manual)
