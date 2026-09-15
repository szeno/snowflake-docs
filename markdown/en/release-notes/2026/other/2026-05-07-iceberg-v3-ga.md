# May 7, 2026: Support for Apache Iceberg™ version 3 (*General availability*)

Support for version 3 (v3) of the Apache Iceberg™ table specification is now generally available.

The following v3 data types are supported:

- `geography`
- `geometry`
- `nanosecond timestamp`
- `variant`

The following additional features are supported:

- **Default values**: Define default values for columns in Iceberg tables. For more information, see [Use default values with Iceberg tables](/user-guide/tables-iceberg-manage#label-tables-iceberg-default-values).
- **Deletion vectors**: Use deletion vectors to improve performance for update and delete operations on Iceberg tables. For more information, see [Deletion vectors](/user-guide/tables-iceberg-manage#tables-iceberg-deletion-vectors).
- **Row lineage**: Track row-level lineage information for change data capture. For more information, see [Use row lineage with Iceberg tables](/user-guide/tables-iceberg-manage#label-tables-iceberg-row-lineage).

Reading Snowflake-managed Iceberg v3 tables by using an external engine and the Horizon Iceberg REST Catalog API is also generally available. Writes from external engines to Snowflake-managed Iceberg v3 tables through Horizon Catalog aren’t supported yet.

The [GET\_DDL](/sql-reference/functions/get_ddl) function now returns the `ICEBERG_VERSION` property in its output for all Iceberg tables that are Snowflake-managed or part of a catalog-linked database, regardless of format version. For example, a v2 table includes `ICEBERG_VERSION = 2` in the output.

For more information, see [Apache Iceberg™ tables: Support for Apache Iceberg™ v3](/user-guide/tables-iceberg-v3-specification-support).
