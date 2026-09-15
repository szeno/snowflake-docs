# June 26, 2026: SQL queries as logical tables in semantic views (*General availability*)

You can now use an SQL query (rather than a physical table) as a logical table in a semantic view. This lets you
define logical tables based on joins, transformations, or any SQL expression without creating a separate view first.

Specify the SQL query in the TABLES clause of the [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view)
command, or use the `definition` property under `base_table` in the
[YAML specification](/user-guide/views-semantic/semantic-view-yaml-spec).

For more information, see [Using an SQL query as a logical table in a semantic view](/user-guide/views-semantic/inline-view).
