# Apr 30, 2026: Catalog-linked databases: Double-quoted identifiers no longer required for DDL commands

When you work with identifiers inside a catalog-linked database that uses CASE\_INSENSITIVE mode
(the default for case-insensitive catalogs like AWS Glue and Unity Catalog), you no longer need to
surround schema, table, and column names in double quotes for DDL commands. Identifiers outside
the catalog-linked database continue to follow standard Snowflake identifier resolution rules.

Previously, the following commands required double-quoted identifiers inside a catalog-linked database:

- CREATE ICEBERG TABLE
- CREATE SCHEMA
- ALTER ICEBERG TABLE ADD COLUMN
- ALTER ICEBERG TABLE RENAME COLUMN

With this update, Snowflake resolves unquoted identifiers in a case-insensitive manner for all SQL statements
that target objects inside the catalog-linked database, including DDL. Identifiers that refer to objects outside
that database still follow the usual Snowflake identifier rules. Snowflake normalizes identifiers to lowercase when creating
objects on the remote catalog. For example, the following commands now work without quoting:

Copy code

```
CREATE SCHEMA My_Schema;
CREATE ICEBERG TABLE My_Schema.My_Table (Col1 INT, Col2 STRING);
```

In both cases, Snowflake creates the objects with lowercase names (`my_schema`, `my_table`, `col1`,
`col2`) on the remote catalog.

For more information, see [Requirements for identifier resolution in a catalog-linked database](/user-guide/tables-iceberg-catalog-linked-database#label-catalog-linked-identifier-requirements).
