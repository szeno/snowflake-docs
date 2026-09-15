# Sep 22, 2025: Prevent data compaction on Snowflake-managed Apache Iceberg™ tables

Use the new ENABLE\_DATA\_COMPACTION parameter to specify whether Snowflake should perform data compaction on Snowflake-managed Apache Iceberg™
tables. Snowflake still performs compaction on these tables by default.

In most cases, compaction doesn’t have a significant impact on table optimization costs, but if it is a concern, you
can disable compaction. For example, you might want to disable it if you ingest a large number of small files for which compaction needs to
rewrite the files.

You can set this parameter at the account, database, schema, and table level.

For more information, see:

- [Set data compaction](/user-guide/tables-iceberg-manage#label-tables-iceberg-manage-set-data-compaction)
- [ENABLE\_DATA\_COMPACTION](/sql-reference/parameters#label-enable-data-compaction)
