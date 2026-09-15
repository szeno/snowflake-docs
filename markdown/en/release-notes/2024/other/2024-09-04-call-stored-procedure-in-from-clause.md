# September 04, 2024 — Calling stored procedures in the FROM clause of SELECT statements

You can now call a stored procedure that returns tabular data directly in the FROM clause
of a SELECT statement. You can use this technique to simplify the SQL statements for saving
results to a table. For example, rather than using the
[SQLID](/developer-guide/snowflake-scripting/query-id) Snowflake Scripting variable with the
[RESULT\_SCAN](/sql-reference/functions/result_scan) function to create a table containing these results,
you can use a query that directly selects from the results.

When calling the stored procedure, omit the [CALL](/sql-reference/sql/call) command. Instead, put the call
in parentheses, preceded by the TABLE keyword.

For more information, see [Selecting from a stored procedure](/developer-guide/stored-procedure/stored-procedures-selecting-from).
