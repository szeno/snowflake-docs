# Oct 28, 2026: Time Travel for Apache Iceberg™ tables (*Preview*)

You can now query a historical snapshot of an Apache Iceberg™ table. In addition to a timestamp, the
[AT | BEFORE](/sql-reference/constructs/at-before) clause accepts an Iceberg snapshot ID, a reference name, or a version tag.

Version tags let you give a snapshot a stable name and keep it queryable for a period that you choose, independent of the table’s
data retention period. Use [ALTER ICEBERG TABLE … VERSION\_TAG](/sql-reference/sql/alter-iceberg-table-version-tag) to create, repoint, and drop tags:

Copy code

```
ALTER ICEBERG TABLE my_iceberg_table
  CREATE VERSION_TAG audit_2026_q1 AS OF VERSION 3821550127947089009 RETAIN 7 DAYS;

SELECT * FROM my_iceberg_table AT(VERSION_TAG => 'audit_2026_q1');
```

To find snapshots and list the tags and branches on a table, use
[GET\_TABLE\_VERSIONS](/sql-reference/functions/get_table_versions) and [GET\_TABLE\_VERSION\_REFS](/sql-reference/functions/get_table_version_refs).

For more information, see [Time Travel for Apache Iceberg™ tables](/user-guide/tables-iceberg-time-travel).
