Categories:
:   [Table functions](/sql-reference/functions-table)

# TO\_QUERY

Returns a result set based on SQL text and an optional set of arguments that are passed to the SQL text if
it is parameterized. The function compiles the SQL text as the definition of a subquery in the FROM clause.
When writing an application or a stored procedure, you can call this function to construct a SQL statement.

Note

This function can include user input in query statements, which has potential security risks, such as
SQL injection. If inputs to the function come from external sources, make sure they are validated.
For more information, see [SQL injection](/developer-guide/stored-procedure/stored-procedures-usage#label-sql-injection).

See also:
:   [Constructing SQL at runtime](/user-guide/querying-construct-at-runtime)

## Syntax

Copy code

```
TO_QUERY( SQL => '<string>' [ , <arg> => '<value>' [, <arg> => '<value>' ...] ] )
```

## Arguments

**Required**

`SQL => 'string'`
:   String representation of the subquery.

**Optional**

`arg => 'value'`
:   [Bind variables](/sql-reference/bind-variables) passed to the SQL `string`.

## Returns

Returns the result set produced by the execution of the specified SQL text or NULL. If any argument is NULL,
the function returns NULL without reporting any error.

## Usage notes

- All arguments must be one of the following:

  - Constant strings.
  - [SQL variables](/sql-reference/session-variables) or
    [Snowflake Scripting variables](/developer-guide/snowflake-scripting/variables) that resolve to strings.
- If you need to convert a string passed in an argument to a different data type, you can use a
  [conversion function](/sql-reference/functions-conversion) in the SQL `string` to
  convert the string to another data type.
- The set of columns defining the result set is derived from the SELECT list of the compiled SQL statement.
- The function is valid only in the FROM clause of a SQL statement.

## Examples

Create a table and insert data into it.

Copy code

```
CREATE OR REPLACE TABLE to_query_example (
  deptno NUMBER(2),
  dname  VARCHAR(14),
  loc    VARCHAR(13))
AS SELECT
  column1,
  column2,
  column3
FROM
  VALUES
    (10, 'ACCOUNTING', 'NEW YORK'),
    (20, 'RESEARCH',   'DALLAS'  ),
    (30, 'SALES',      'CHICAGO' ),
    (40, 'OPERATIONS', 'BOSTON'  );
```

The examples use the data in this table.

### Using TO\_QUERY in SQL statements

First, set a session variable (SQL variable) for the table name:

Copy code

```
SET table_name = 'to_query_example';
```

The examples use the session variable and [IDENTIFIER()](/sql-reference/identifier-literal) to
identify the table.

Using IDENTIFIER() to identify database objects is a best practice because it can make
code more reusable and help to prevent [SQL injection](/developer-guide/stored-procedure/stored-procedures-usage#label-sql-injection) risks.

The following example uses the TO\_QUERY function to return all of the data in the `to_query_example` table:

Copy code

```
SELECT * FROM TABLE(TO_QUERY('SELECT * FROM IDENTIFIER($table_name)'));
```

```
+--------+------------+----------+
| DEPTNO | DNAME      | LOC      |
|--------+------------+----------|
|     10 | ACCOUNTING | NEW YORK |
|     20 | RESEARCH   | DALLAS   |
|     30 | SALES      | CHICAGO  |
|     40 | OPERATIONS | BOSTON   |
+--------+------------+----------+
```

The following example uses the TO\_QUERY function to return all of the values in the `deptno` column of
the `to_query_example` table:

Copy code

```
SELECT deptno FROM TABLE(TO_QUERY('SELECT * FROM IDENTIFIER($table_name)'));
```

```
+--------+
| DEPTNO |
|--------|
|     10 |
|     20 |
|     30 |
|     40 |
+--------+
```

The following example uses the TO\_QUERY function to pass an argument to a SQL statement so that it returns the row
where `deptno` equals `10` in the `to_query_example` table:

Copy code

```
SELECT * FROM TABLE(
  TO_QUERY(
    'SELECT * FROM IDENTIFIER($table_name)
    WHERE deptno = TO_NUMBER(:dno)', dno => '10'
    )
  );
```

```
+--------+------------+----------+
| DEPTNO | DNAME      | LOC      |
|--------+------------+----------|
|     10 | ACCOUNTING | NEW YORK |
+--------+------------+----------+
```

The following example is the same as the previous example, but it uses a session variable to pass
the `deptno` value to the TO\_QUERY function:

Copy code

```
SET dept = '10';

SELECT * FROM TABLE(
  TO_QUERY(
    'SELECT * FROM IDENTIFIER($table_name)
    WHERE deptno = TO_NUMBER(:dno)', dno => $dept
    )
  );
```

```
+--------+------------+----------+
| DEPTNO | DNAME      | LOC      |
|--------+------------+----------|
|     10 | ACCOUNTING | NEW YORK |
+--------+------------+----------+
```

The following example uses the TO\_QUERY function to pass two arguments to a SQL statement so that it returns the rows
where `deptno` equals `10` or `dname` equals `SALES` in the `to_query_example` table:

Copy code

```
SELECT * FROM TABLE(
  TO_QUERY(
    'SELECT * FROM IDENTIFIER($table_name)
    WHERE deptno = TO_NUMBER(:dno) OR dname = :dnm',
    dno => '10', dnm => 'SALES'
    )
  );
```

```
+--------+------------+----------+
| DEPTNO | DNAME      | LOC      |
|--------+------------+----------|
|     10 | ACCOUNTING | NEW YORK |
|     30 | SALES      | CHICAGO  |
+--------+------------+----------+
```

### Using TO\_QUERY in stored procedures

The following example uses the TO\_QUERY function in a stored procedure:

Copy code

```
CREATE OR REPLACE PROCEDURE get_num_results_tq(query VARCHAR)
RETURNS TABLE ()
LANGUAGE SQL
AS
DECLARE
  res RESULTSET DEFAULT (SELECT COUNT(*) FROM TABLE(TO_QUERY(:query)));
BEGIN
  RETURN TABLE(res);
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE get_num_results_tq(query VARCHAR)
RETURNS TABLE ()
LANGUAGE SQL
AS
$$
DECLARE
  res RESULTSET DEFAULT (SELECT COUNT(*) FROM TABLE(TO_QUERY(:query)));
BEGIN
  RETURN TABLE(res);
END;
$$
;
```

Call the stored procedure:

Copy code

```
CALL get_num_results_tq('SELECT * FROM to_query_example');
```

```
+----------+
| COUNT(*) |
|----------|
|        4 |
+----------+
```

Copy code

```
CALL get_num_results_tq('SELECT * FROM to_query_example WHERE deptno = 20');
```

```
+----------+
| COUNT(*) |
|----------|
|        1 |
+----------+
```

The following example uses the TO\_QUERY function in a stored procedure with a bind variable:

Copy code

```
CREATE OR REPLACE PROCEDURE get_results_tqbnd(dno VARCHAR)
RETURNS TABLE ()
LANGUAGE SQL
AS
DECLARE
  res RESULTSET DEFAULT (SELECT * FROM TABLE(
    TO_QUERY(
      'SELECT * FROM to_query_example
      WHERE deptno = TO_NUMBER(:dnoval)', dnoval => :dno
    )
  ));
BEGIN
  RETURN TABLE(res);
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE get_results_tqbnd(dno VARCHAR)
RETURNS TABLE ()
LANGUAGE SQL
AS
$$
DECLARE
  res RESULTSET DEFAULT (SELECT * FROM TABLE(
    TO_QUERY(
      'SELECT * FROM to_query_example
      WHERE deptno = TO_NUMBER(:dnoval)', dnoval => :dno
    )
  ));
BEGIN
  RETURN TABLE(res);
END;
$$
;
```

Call the stored procedure:

Copy code

```
CALL get_results_tqbnd('40');
```

```
+--------+------------+--------+
| DEPTNO | DNAME      | LOC    |
|--------+------------+--------|
|     40 | OPERATIONS | BOSTON |
+--------+------------+--------+
```

Call the stored procedure using a session variable:

Copy code

```
SET dept = '20';

CALL get_results_tqbnd($dept);
```

```
+--------+----------+--------+
| DEPTNO | DNAME    | LOC    |
|--------+----------+--------|
|     20 | RESEARCH | DALLAS |
+--------+----------+--------+
```
