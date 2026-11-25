# Nov 20, 2026: Simplify selective data replacement with DELETING WHERE in SQL and Dynamic Tables with custom incrementalization

You can now replace groups of rows or a selected range of data in a single SQL statement without writing separate delete
and insert statements. The feature is available in DML and Dynamic Table with custom incrementalization.

Use `INSERT OVERWRITE ... DELETING WHERE` to specify which existing rows to remove and provide a query that inserts the new
results. Deletion and insertion happen together.

For Custom Incremental Dynamic Tables, this makes it easier to recompute groups of rows. For
example, when a changed record joins to fewer matching rows, you can replace the old results for that record without leaving
stale rows behind. You can also recompute and replace a recent window of data to incorporate late-arriving updates.

For more information, see [INSERT](/sql-reference/sql/insert) and [Custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization).
