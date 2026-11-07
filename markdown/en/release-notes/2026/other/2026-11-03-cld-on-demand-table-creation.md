# Nov 3, 2026: On-demand table creation for catalog-linked databases (*General availability*)

On-demand table creation for catalog-linked databases is now generally available.

If you reference a table that exists in your remote catalog but isn’t registered in your catalog-linked
database yet, Snowflake creates the table (and its schema, if needed) as part of running your statement.
You don’t need to wait for the next catalog sync. For example, you can create a table with Apache Spark
and query it from Snowflake immediately. This applies to `SELECT`, `CREATE TABLE ... AS SELECT`,
`CREATE VIEW`, `DESCRIBE`, and DML statements such as `INSERT`, `UPDATE`, `DELETE`, and `MERGE`.

On-demand table creation is enabled for all catalog-linked databases. You don’t need to change any
configuration or SQL.

For more information, see [On-demand table creation](/user-guide/tables-iceberg-catalog-linked-database#label-catalog-linked-db-on-demand-creation).
