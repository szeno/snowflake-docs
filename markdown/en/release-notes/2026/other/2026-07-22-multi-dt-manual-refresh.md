# Jul 22, 2026: Refresh multiple dynamic tables in one ALTER statement

You can now refresh multiple dynamic tables in a single `ALTER DYNAMIC TABLE ... REFRESH` statement
by supplying a comma-separated list of table names. Snowflake merges the
upstream dependencies of every listed dynamic table into one pipeline and refreshes
all of them at a single data timestamp. Shared upstreams refresh exactly once.

For more information, see
[Refresh multiple dynamic tables in one statement](/user-guide/dynamic-tables/manage#label-dynamic-tables-manage-multi-refresh) and
[Semantics for a multi-table list](/sql-reference/sql/alter-dynamic-table#label-alter-dynamic-table-refresh-multi).
