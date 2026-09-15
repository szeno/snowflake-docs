# June 25, 2024 — New TO\_QUERY table function

The [TO\_QUERY](/sql-reference/functions/to_query) table function returns a result set based on SQL text and an optional
set of arguments that are passed to the SQL text if it is parameterized. The function compiles the SQL text as the
definition of a subquery in the FROM clause. When writing an application or a stored procedure, you can call this
function to construct a SQL statement.
