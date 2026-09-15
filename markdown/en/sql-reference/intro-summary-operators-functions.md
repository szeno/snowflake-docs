# Summary of functions

Snowflake supports most of the standard functions defined in SQL:1999, as well as parts of the SQL:2003 analytic extensions.

## Scalar functions

A scalar function is a function that returns one value per invocation; in most cases, you can think of this as returning
one value per row. This contrasts with [Aggregate functions](/sql-reference/functions-aggregation), which return one value per group of rows.

For a complete list of scalar function categories, see [Scalar functions](/sql-reference/functions).

## Aggregate functions

Snowflake supports aggregate functions to operate on values across rows to perform mathematical calculations such as sum, average,
counting, minimum/maximum values, standard deviation, and estimation, as well as some non-mathematical operations.

For a complete list, see [Aggregate functions](/sql-reference/functions-aggregation).

## Window functions

Window functions are [aggregate functions](/sql-reference/functions-aggregation) that can operate on a subset of rows within the set of input rows.

## Table functions

Snowflake supports many [Table functions](/sql-reference/functions-table) to obtain information about Snowflake features and services.

For a complete summary, see [List of system-defined table functions](/sql-reference/functions-table#label-list-of-system-defined-table-functions).

## System functions

For a complete list of system functions, see [System functions](/sql-reference/functions-system).

## User-defined functions (UDFs)

In addition to the system-defined functions provided by Snowflake, you can create user-defined functions (UDFs). See
[User-defined functions overview](/developer-guide/udf/udf-overview) for more information.

## External functions

Snowflake also supports [Writing external functions](/sql-reference/external-functions), which are stored and executed outside Snowflake.
