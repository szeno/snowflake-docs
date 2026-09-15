# Working with RESULTSETs

This topic explains how to use a RESULTSET in Snowflake Scripting.

## Introduction

In Snowflake Scripting, a RESULTSET is a SQL data type that points to the result set of a query.

Because a RESULTSET is just a pointer to the results, you must do one of the following to access the results through the
RESULTSET:

- Use the `TABLE(...)` syntax to retrieve the results as a table.
- Iterate over the RESULTSET with a [cursor](/developer-guide/snowflake-scripting/cursors).

Examples of both of these are included below.

## Understanding the differences between a cursor and a RESULTSET

A RESULTSET and a [cursor](/developer-guide/snowflake-scripting/cursors) both provide access to the result set of a query. However, these objects differ in the
following ways:

- The point in time when the query is executed.

  - For a cursor, the query is executed when you execute the [OPEN](/sql-reference/snowflake-scripting/open) command on the
    cursor.
  - For a RESULTSET, the query is executed when you assign the query to the RESULTSET (either in the DECLARE section
    or in the BEGIN … END block).
- Support for binding in the OPEN command.

  - When you declare a cursor, you can specify bind parameters (`?` characters). Later, when you execute the
    [OPEN](/sql-reference/snowflake-scripting/open) command, you can bind variables to those parameters in the USING clause.
  - RESULTSET does not support the OPEN command. However, you can bind variables in SQL commands before returning the
    result set.

In general, it is simpler to use a RESULTSET when you want to return a table that contains the result set of a query. However,
you can also return a table from a Snowflake Scripting block with a cursor. To do so, you can pass the cursor to
`RESULTSET_FROM_CURSOR(cursor)` to return a RESULTSET and pass that RESULTSET to `TABLE(...)`. See
[Returning a table for a cursor](/developer-guide/snowflake-scripting/cursors#label-snowscript-cursors-return-table).

## Declaring a RESULTSET

You can declare a RESULTSET in the [DECLARE](/sql-reference/snowflake-scripting/declare) section of a block or in the
[BEGIN … END](/sql-reference/snowflake-scripting/begin) section of the block.

- Within the DECLARE section, use the syntax described in [RESULTSET declaration syntax](/sql-reference/snowflake-scripting/declare#label-snowscript-declare-syntax-resultset). For example:

  Copy code

  ```
  DECLARE
    ...
    res RESULTSET DEFAULT (SELECT col1 FROM mytable ORDER BY col1);
  ```
- Within the BEGIN … END block, use the syntax described in [RESULTSET assignment syntax](/sql-reference/snowflake-scripting/let#label-snowscript-let-syntax-resultset). For example:

  Copy code

  ```
  BEGIN
    ...
    LET res RESULTSET := (SELECT col1 FROM mytable ORDER BY col1);
  ```

## Assigning a query to a declared RESULTSET

To assign the result of a query to a RESULTSET that has already been declared, use the following syntax:

Copy code

```
<resultset_name> := [ ASYNC ] ( <query> ) ;
```

Where:

> `resultset_name`
> :   The name of the RESULTSET.
>
>     The name must be unique within the current scope.
>
>     The name must follow the naming rules for [Object identifiers](/sql-reference/identifiers).
>
> `ASYNC`
> :   Runs the query as an [asynchronous child job](/developer-guide/snowflake-scripting/asynchronous-child-jobs).
>
> `query`
> :   The query to assign to the RESULTSET.

To assign a query to a RESULTSET:

Copy code

```
DECLARE
  res RESULTSET;
BEGIN
  res := (SELECT col1 FROM mytable ORDER BY col1);
  ...
```

To assign a query to a RESULTSET and run the query as an asynchronous child job:

Copy code

```
DECLARE
  res RESULTSET;
BEGIN
  res := ASYNC (SELECT col1 FROM mytable ORDER BY col1);
  ...
```

To build a SQL string dynamically for the query, set `query` to
`(EXECUTE IMMEDIATE string_of_sql)`. For example:

Copy code

```
DECLARE
  res RESULTSET;
  col_name VARCHAR;
  select_statement VARCHAR;
BEGIN
  col_name := 'col1';
  select_statement := 'SELECT ' || col_name || ' FROM mytable';
  res := (EXECUTE IMMEDIATE :select_statement);
  RETURN TABLE(res);
END;
```

Although you can set `query` to an EXECUTE IMMEDIATE statement for a RESULTSET, you can’t do this for a
cursor.

## Using a RESULTSET

The query for a RESULTSET is executed when the object is associated with that query. For example:

- When you declare a RESULTSET and set the DEFAULT clause to a query, the query is executed at that point in time.
- When you use the `:=` operator to assign a query to a RESULTSET, the query is executed at that point in time.

Note

Because a RESULTSET points to the result set of a query (and does not contain the result set of a query), a RESULTSET
is valid only as long as the query results are cached (typically 24 hours). For details about query result caching,
see [Using Persisted Query Results](/user-guide/querying-persisted-results).

Once the query is executed, you can access the results by using a cursor. You can also return the results as a table from a stored
procedure.

- [Using a cursor to access data from a RESULTSET](#label-snowscript-resultsets-use-cursor)
- [Returning a RESULTSET as a table](#label-snowscript-resultsets-use-return-table)

### Using a cursor to access data from a RESULTSET

To use a cursor to access the data from a RESULTSET, [declare the cursor](/developer-guide/snowflake-scripting/cursors#label-snowscript-cursors-declare) on the
object. For example:

Copy code

```
DECLARE
  ...
  res RESULTSET DEFAULT (SELECT col1 FROM mytable ORDER BY col1);
  c1 CURSOR FOR res;
```

When you declare a cursor on a RESULTSET, the cursor gets access to the data already in the RESULTSET. Executing
the [OPEN](/sql-reference/snowflake-scripting/open) command on the cursor does not execute the query for the RESULTSET
again.

You can then [open the cursor](/developer-guide/snowflake-scripting/cursors#label-snowscript-cursors-open) and use the cursor to
[fetch the data](/developer-guide/snowflake-scripting/cursors#label-snowscript-cursors-fetch).

Note

If the results include GEOGRAPHY values, you must cast the values to the GEOGRAPHY type before passing the values to any
functions that expect GEOGRAPHY input values. See [Using a cursor to retrieve a GEOGRAPHY value](/developer-guide/snowflake-scripting/cursors#label-snowscript-cursors-geography).

### Returning a RESULTSET as a table

If you want to return the results that the RESULTSET points to, pass the RESULTSET to `TABLE(...)`. For example:

Copy code

```
CREATE PROCEDURE f()
  RETURNS TABLE(column_1 INTEGER, column_2 VARCHAR)
  ...
    RETURN TABLE(my_resultset_1);
  ...
```

This is similar to the way that `TABLE(...)` is used with
[table functions](/sql-reference/functions-table) (such as [RESULT\_SCAN](/sql-reference/functions/result_scan)).

As shown in the example, if you write a stored procedure that returns a table, you must declare the stored procedure as returning
a table.

Note

Currently, the `TABLE(resultset_name)` syntax is supported only in the
[RETURN](/sql-reference/snowflake-scripting/return) statement.

Even if you have used a cursor to [fetch rows from the RESULTSET](#label-snowscript-resultsets-use-cursor), the
table returned by `TABLE(resultset_name)` still contains all of the rows (not just the rows starting from the cursor’s
internal row pointer).

## Limitations of the RESULTSET data type

Although RESULTSET is a data type, Snowflake does not yet support:

- Declaring a column of type RESULTSET.
- Declaring a parameter of type RESULTSET.
- Declaring a stored procedure’s return type as a RESULTSET.

Snowflake supports RESULTSET only inside Snowflake Scripting.

In addition, you can’t use a RESULTSET directly as a table. For example, the following is invalid:

Copy code

```
SELECT * FROM my_result_set;
```

## Examples of using a RESULTSET

The following sections provide examples of using a RESULTSET:

- [Setting up the data for the examples](#label-snowscript-resultsets-example-setup)
- [Example: Returning a table from a stored procedure](#label-snowscript-resultsets-example-sp-table)
- [Example: Constructing the SQL statement dynamically](#label-snowscript-resultsets-example-dynamic-sql)
- [Example: Declaring a RESULTSET variable without a DEFAULT clause](#label-snowscript-resultsets-example-resultset-no-default)
- [Example: Using a CURSOR with a RESULTSET](#label-snowscript-resultsets-example-resultset-cursor)
- [Additional examples that use a RESULTSET](#label-snowscript-resultsets-additional-examples)

For examples that use the ASYNC keyword to run queries specified for RESULTSETs as asynchronous child jobs,
see [Examples of using asynchronous child jobs](/developer-guide/snowflake-scripting/asynchronous-child-jobs#label-snowscript-asynchronous-child-jobs-examples).

### Setting up the data for the examples

Many of the examples below use the table and data shown below:

Copy code

```
CREATE OR REPLACE TABLE t001 (a INTEGER, b VARCHAR);
INSERT INTO t001 (a, b) VALUES
  (1, 'row1'),
  (2, 'row2');
```

### Example: Returning a table from a stored procedure

The following code shows how to declare a RESULTSET and return the results that the RESULTSET points to. The RETURNS
clause in the CREATE PROCEDURE command declares that the stored procedure returns a table, which contains one column of
type INTEGER.

The RETURN statement inside the block uses the `TABLE(...)` syntax to return the results as a table.

Create the stored procedure:

Copy code

```
CREATE OR REPLACE PROCEDURE test_sp()
RETURNS TABLE(a INTEGER)
LANGUAGE SQL
AS
  DECLARE
    res RESULTSET DEFAULT (SELECT a FROM t001 ORDER BY a);
  BEGIN
    RETURN TABLE(res);
  END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE test_sp()
RETURNS TABLE(a INTEGER)
LANGUAGE SQL
AS
$$
  DECLARE
      res RESULTSET default (SELECT a FROM t001 ORDER BY a);
  BEGIN
      RETURN TABLE(res);
  END;
$$;
```

Call the stored procedure:

Copy code

```
CALL test_sp();
```

```
+---+
| A |
|---|
| 1 |
| 2 |
+---+
```

You can use the [pipe operator](/sql-reference/operators-flow) (`->>`) to process the results of the stored procedure
call:

Copy code

```
CALL test_sp()
  ->> SELECT *
        FROM $1
        WHERE a > 1;
```

```
+---+
| A |
|---|
| 2 |
+---+
```

You can also use the [RESULT\_SCAN](/sql-reference/functions/result_scan) function to process the results after you call the
stored procedure:

Copy code

```
CALL test_sp();
```

```
+---+
| A |
|---|
| 1 |
| 2 |
+---+
```

Copy code

```
SELECT *
  FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
  WHERE a < 2;
```

```
+---+
| A |
|---|
| 1 |
+---+
```

### Example: Constructing the SQL statement dynamically

You can construct the SQL dynamically. The following is an example that executes the same query as the previous stored procedure
but that uses a SQL statement that is constructed dynamically:

Copy code

```
CREATE OR REPLACE PROCEDURE test_sp_dynamic(table_name VARCHAR)
  RETURNS TABLE(a INTEGER)
  LANGUAGE SQL
AS
DECLARE
  res RESULTSET;
  query VARCHAR DEFAULT 'SELECT a FROM IDENTIFIER(?) ORDER BY a;';
BEGIN
  res := (EXECUTE IMMEDIATE :query USING(table_name));
  RETURN TABLE(res);
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE test_sp_dynamic(table_name VARCHAR)
RETURNS TABLE(a INTEGER)
LANGUAGE SQL
AS
$$
  DECLARE
    res RESULTSET;
    query VARCHAR DEFAULT 'SELECT a FROM IDENTIFIER(?) ORDER BY a;';
  BEGIN
    res := (EXECUTE IMMEDIATE :query USING(table_name));
    RETURN TABLE(res);
  END
$$
;
```

To run the example, call the stored procedure and pass in the table name:

Copy code

```
CALL test_sp_dynamic('t001');
```

```
+---+
| A |
|---|
| 1 |
| 2 |
+---+
```

### Example: Declaring a RESULTSET variable without a DEFAULT clause

The following code shows how to declare a RESULTSET without a DEFAULT clause (i.e. without associating a query with the RESULTSET),
and then associate the RESULTSET with a query later.

Copy code

```
CREATE OR REPLACE PROCEDURE test_sp_02()
RETURNS TABLE(a INTEGER)
LANGUAGE SQL
AS
  DECLARE
    res RESULTSET;
  BEGIN
    res := (SELECT a FROM t001 ORDER BY a);
    RETURN TABLE(res);
  END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE test_sp_02()
RETURNS TABLE(a INTEGER)
LANGUAGE SQL
AS
$$
  DECLARE
      res RESULTSET;
  BEGIN
      res := (SELECT a FROM t001 ORDER BY a);
      RETURN TABLE(res);
  END;
$$;
```

To run the example, call the stored procedure:

Copy code

```
CALL test_sp_02();
```

```
+---+
| A |
|---|
| 1 |
| 2 |
+---+
```

### Example: Using a CURSOR with a RESULTSET

The following code shows how to use a [cursor](/developer-guide/snowflake-scripting/cursors) to iterate over the rows in a RESULTSET:

Create the stored procedure:

Copy code

```
CREATE OR REPLACE PROCEDURE test_sp_03()
RETURNS VARCHAR
LANGUAGE SQL
AS

DECLARE
  accumulator INTEGER DEFAULT 0;
  res1 RESULTSET DEFAULT (SELECT a FROM t001 ORDER BY a);
  cur1 CURSOR FOR res1;
BEGIN
  FOR row_variable IN cur1 DO
    accumulator := accumulator + row_variable.a;
  END FOR;
  RETURN accumulator::VARCHAR;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE test_sp_03()
RETURNS INTEGER
LANGUAGE SQL
AS
$$
  DECLARE
    accumulator INTEGER DEFAULT 0;
    res1 RESULTSET DEFAULT (SELECT a FROM t001 ORDER BY a);
    cur1 CURSOR FOR res1;
  BEGIN
    FOR row_variable IN cur1 DO
        accumulator := accumulator + row_variable.a;
    END FOR;
    RETURN accumulator;
  END;
$$;
```

Call the stored procedure, and the results add the values for `a` in the table (1 + 2):

Copy code

```
CALL test_sp_03();
```

```
+------------+
| TEST_SP_03 |
|------------|
| 3          |
+------------+
```

### Additional examples that use a RESULTSET

Here are additional examples that use a RESULTSET:

- [Use a RESULTSET-based FOR loop](/developer-guide/snowflake-scripting/loops#label-snowscript-loop-for-resultset)

  This example shows you how to use a FOR loop that iterates over a RESULTSET.
- [Return a table for a cursor](/developer-guide/snowflake-scripting/cursors#label-snowscript-cursors-return-table)

  This example shows you how to use a cursor to return a table of data in a RESULTSET.
- [Update table data with user input](/developer-guide/snowflake-scripting/use-cases#label-snowscript-loop-for-conditional-logic-bind-variables)

  This example shows you how to use bind variables based on user input to update
  data in a table. It uses a FOR loop with conditional logic to iterate over the rows
  in a RESULTSET.
- [Filter and collect data](/developer-guide/snowflake-scripting/use-cases#label-snowscript-example-filter-and-collect-data)

  This example shows you how to use a RESULTSET to collect data and insert that
  data into a table to track historical trends.
