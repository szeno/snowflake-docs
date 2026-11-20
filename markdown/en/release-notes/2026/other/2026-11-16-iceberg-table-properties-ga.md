# Nov 16, 2026: Iceberg table properties in SQL (*General availability*)

With this release, you can set Iceberg table properties on Snowflake-managed and writable externally managed
Apache Iceberg™ tables with the `TABLE_PROPERTIES` clause:

- `CREATE ICEBERG TABLE ... TABLE_PROPERTIES = ('<key>' = '<value>' [ , ... ])`
- `ALTER ICEBERG TABLE ... SET TABLE_PROPERTIES = ('<key>' = '<value>' [ , ... ])`
- `ALTER ICEBERG TABLE ... UNSET TABLE_PROPERTIES ('<key>' [ , ... ])`

Some properties map to Snowflake parameters, such as `TARGET_FILE_SIZE` and
`DATA_RETENTION_TIME_IN_DAYS`. You can read the properties stored in a table’s metadata file with
[SYSTEM$READ\_ICEBERG\_TABLE\_PROPERTY](/sql-reference/functions/system_read_iceberg_table_property).

For more information, see [Iceberg table properties](/user-guide/tables-iceberg-table-properties).
