# June 5, 2026: Default metadata write format for Apache Iceberg™ tables (*General availability*)

You can now set a default metadata write format at the account, database, or schema level so that `CREATE TABLE` and
`ALTER TABLE` create Apache Iceberg™ tables without the `ICEBERG` keyword. This release includes the following capabilities:

- **DEFAULT\_METADATA\_WRITE\_FORMAT** parameter to default new tables to the Snowflake table format or the Apache Iceberg™ table format.
- Automatic DDL promotion in catalog-linked databases so `CREATE TABLE` creates Apache Iceberg™ tables without the `ICEBERG` keyword.

For more information, see [Configure Iceberg as the default metadata format for tables](/user-guide/tables-iceberg-default-metadata-format).
