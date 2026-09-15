# Flow operators

Flow operators chain SQL statements together, where the results of one statement serve as the input to another statement.
Currently, the pipe operator (`->>`) is the only flow operator supported by Snowflake.

## Pipe

Pipe operators are similar to Unix pipes (`|`) on the command line, but for SQL statements instead of Unix
commands. To use the pipe operator, specify a series of SQL statements separated by the operator. You can specify any
valid SQL statement, such as SHOW, SELECT, CREATE, INSERT, and so on. After the first SQL statement, each
subsequent statement can take the results of any previous statement as input. In the FROM clause, a previous SQL
statement is referenced by a parameter with the dollar sign (`$`) and the pipe number, which is the relative
position of the statement in the chain counting back from the current statement.

The pipe operator chains the following series of SQL statements together, and the comments show the relative
reference numbers for each statement:

Copy code

```
first_st -- Referenced as $4 in last_st, $3 in fourth_st, $2 in third_st, and $1 in second_st
  ->> second_st -- Referenced as $3 in last_st, $2 in fourth_st, and $1 in third_st
  ->> third_st  -- Referenced as $2 in last_st and $1 in fourth_st
  ->> fourth_st -- Referenced as $1 in last_st
  ->> last_st;
```

For example, this series of SQL statements has a pipe number reference in three SELECT statements, and each one takes
the results of the first SELECT statement as input:

Copy code

```
SELECT ...
  ->> SELECT ... FROM $1
  ->> SELECT ... FROM $2
  ->> SELECT ... FROM $3;
```

As shown, you end the chain of SQL statements by placing a semicolon after the last statement. Don’t place a semicolon
after the previous statements in the chain. The output of the entire chain is the final result of the last SQL statement.
Client tools, such as SnowSQL, treat the chain of statements as a single statement.

The pipe operator provides the following benefits:

- Simplifies the execution of dependent SQL statements.
- Improves the readability and flexibility of complex SQL operations.

### Syntax

Copy code

```
<sql_statement_1> ->> <sql_statement_2> [ ->> <sql_statement_n> ... ]
```

### Usage notes

- Each statement produces a result that can only be consumed by a subsequent statement in the chain.
- Statements are executed in their specified order. Unlike `RESULT_SCAN(LAST_QUERY_ID())`, the pipe number
  resolves to the correct result set in the chain, whether other queries were run concurrently
  outside of the chain or not.
- When a statement consumes the results of a previous statement, the result set consumed is equivalent to the
  result set returned by the [RESULT\_SCAN](/sql-reference/functions/result_scan) function that was passed the query
  ID of the previous statement.

  For example, these statements limit the output of the SHOW WAREHOUSES command to specific columns:

  Copy code

  ```
  SHOW WAREHOUSES;

  SELECT "name", "state", "type", "size"
    FROM TABLE(RESULT_SCAN(LAST_QUERY_ID(-1)));
  ```

  This statement uses the pipe operator to produce the same results:

  Copy code

  ```
  SHOW WAREHOUSES
    ->> SELECT "name", "state", "type", "size" FROM $1;
  ```

  The output column names for SHOW and DESCRIBE commands are generated in lowercase. If you consume a
  result set from a SHOW or DESCRIBE command with the pipe operator or the RESULT\_SCAN function,
  use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for the column names in the query to
  ensure that they match the column names in the output that was scanned. For example, if the name of an
  output column is `type`, then specify `"type"` for the identifier.
- A query that uses the pipe operator isn’t guaranteed to return rows in the same order as the input result set of
  a previous query in the chain. You can include an ORDER BY clause with the query to specify the order.
- An error raised by any SQL statement stops the execution of the chain, and that error is returned to the client.
- The last statement result is returned to the client.
- The statements are executed as a [Snowflake Scripting](/developer-guide/snowflake-scripting/index)
  anonymous block.

### Limitations

- The `$n` parameter is only valid in the FROM clause of a SQL statement.
- Each SQL statement produces a result that can only be consumed by a subsequent statement in the pipe
  chain. The results can’t be consumed outside of the pipe chain, except for the results of the last
  statement.
- Bind variables aren’t supported.
- Using the pipe operator in a multi-statement execution (that is, submitting multiple statements
  separated by `;` rather than `->>` in a single call) from Snowflake client drivers isn’t supported.
- When you use the pipe operator with [Snowflake Scripting](/developer-guide/snowflake-scripting/index),
  you can’t combine declaration and assignment of a RESULTSET if you use the pipe operator in the SQL statement.

  For example, the following code returns an error:

  Copy code

  ```
  LET res RESULTSET := (SELECT 'myvalue' ->> SELECT $1 FROM $1);
  RETURN TABLE(res);
  ```

  The following example succeeds because it separates the declaration and assignment of a RESULTSET:

  Copy code

  ```
  LET res RESULTSET;
  res := (SELECT 'myvalue' ->> SELECT $1 FROM $1);
  RETURN TABLE(res);
  ```

### Examples

The following examples use the pipe operator:

- [Select a list of columns for the output of a SHOW command](#label-pipe-operator-example-show)
- [Execute queries that take input from queries on multiple tables](#label-pipe-operator-example-queries)
- [Return the row counts for DML operations in a transaction](#label-pipe-operator-example-dml)
- [Return the results for inserts into a table that is later dropped](#label-pipe-operator-example-ddl)

#### Select a list of columns for the output of a SHOW command

Run a SHOW TABLES command, and use the pipe operator to limit the output to the `created_on`, `name`, and
`owner` columns for tables created after April 15, 2025.

Copy code

```
SHOW TABLES
  ->> SELECT "created_on" AS creation_date,
             "name" AS table_name,
             "owner" AS table_owner
        FROM $1
        WHERE creation_date > '2025-04-15'::DATE;
```

```
+-------------------------------+-------------+--------------+
| CREATION_DATE                 | TABLE_NAME  | TABLE_OWNER  |
|-------------------------------+-------------+--------------|
| 2025-04-16 08:46:16.130 -0700 | TEST_TABLE1 | ACCOUNTADMIN |
| 2025-04-16 09:44:13.701 -0700 | MYTABLE1    | USER_ROLE    |
| 2025-04-16 08:46:32.092 -0700 | MYTABLE2    | USER_ROLE    |
+-------------------------------+-------------+--------------+
```

#### Execute queries that take input from queries on multiple tables

First, create a `dept_pipe_demo` table and an `emp_pipe_demo` table, and insert data into each one:

Copy code

```
CREATE OR REPLACE TABLE dept_pipe_demo (
  deptno NUMBER(2),
  dname VARCHAR(14),
  loc VARCHAR(13)
  ) AS SELECT * FROM VALUES
     (10, 'ACCOUNTING', 'NEW YORK'),
     (20, 'RESEARCH', 'DALLAS'),
     (30, 'SALES', 'CHICAGO'),
     (40, 'OPERATIONS', 'BOSTON');

CREATE OR REPLACE TABLE emp_pipe_demo (
  empno NUMBER(4),
  ename VARCHAR(10),
  sal NUMBER(7,2),
  deptno NUMBER(2)
  ) AS SELECT * FROM VALUES
    (7369, 'SMITH', 800, 20),
    (7499, 'ALLEN', 1600, 30),
    (7521, 'WARD', 1250, 30),
    (7698, 'BLAKE', 2850, 30),
    (7782, 'CLARK', 2450, 10);
```

The following example uses the pipe operator for a chain of SQL statements that perform the following operations:

1. Query the `dept_pipe_demo` table to return rows where `dname` equals `SALES`.
2. Query the `emp_pipe_demo` table for employees with a salary greater than `1500` in the `SALES` department,
   using the results of the previous query as input by specifying `$1` in the WHERE condition of a FROM clause.
3. Run a query that returns the `ename` and `sal` values using the results of the previous query as input
   by specifying `$1` in the FROM clause.

Copy code

```
SELECT * FROM dept_pipe_demo WHERE dname = 'SALES'
  ->> SELECT * FROM emp_pipe_demo WHERE sal > 1500 AND deptno IN (SELECT deptno FROM $1)
  ->> SELECT ename, sal FROM $1 ORDER BY 2 DESC;
```

```
+-------+---------+
| ENAME |     SAL |
|-------+---------|
| BLAKE | 2850.00 |
| ALLEN | 1600.00 |
+-------+---------+
```

Note

The purpose of this example is to show how to combine a series of queries with the pipe operator. However, the
same output can be achieved with a join query, and join queries typically perform better than queries combined
with the pipe operator.

#### Return the row counts for DML operations in a transaction

Create a table and insert rows one by one. Chaining all the statements lets you use the
pipe operator to examine the result of each INSERT statement, which represents the total number of
rows inserted.

In each of the SELECT statements in the example, the `$1` in the SELECT list is a shorthand reference for
the first column, not a previous result in the pipe. The `$n` parameter for a pipe number is only
valid in the FROM clause.

Copy code

```
CREATE OR REPLACE TABLE test_sql_pipe_dml (a INT, b INT)
  ->> INSERT INTO test_sql_pipe_dml VALUES (1, 2)
  ->> INSERT INTO test_sql_pipe_dml VALUES (3, 4)
  ->> INSERT INTO test_sql_pipe_dml VALUES (5, 6)
  ->> INSERT INTO test_sql_pipe_dml VALUES (7, 8)
  ->> SELECT (SELECT $1 FROM $4) +
             (SELECT $1 FROM $3) +
             (SELECT $1 FROM $2) +
             (SELECT $1 FROM $1)
        AS "Number of rows";
```

```
+----------------+
| Number of rows |
|----------------|
|              4 |
+----------------+
```

The following example uses the pipe operator for a chain of SQL statements that perform the following operations:

1. Begin a transaction.
2. Insert a row into the previously created table.
3. Delete rows from the table.
4. Update rows in the table.
5. Commit the transaction.
6. Query the number of rows that were affected by each DML operation.

Copy code

```
BEGIN TRANSACTION
  ->> INSERT INTO test_sql_pipe_dml VALUES (1, 2)
  ->> DELETE FROM test_sql_pipe_dml WHERE a = 1
  ->> UPDATE test_sql_pipe_dml SET b = 2
  ->> COMMIT
  ->> SELECT
        (SELECT $1 FROM $4) AS "Inserted rows",
        (SELECT $1 FROM $3) AS "Deleted rows",
        (SELECT $1 FROM $2) AS "Updated rows";
```

```
+---------------+--------------+--------------+
| Inserted rows | Deleted rows | Updated rows |
|---------------+--------------+--------------|
|             1 |            2 |            3 |
+---------------+--------------+--------------+
```

#### Return the results for inserts into a table that is later dropped

This example uses the pipe operator for a chain of SQL statements that performs the following operations:

1. Create a table with an IDENTITY column.
2. Insert rows into the table.
3. Query the table.
4. Drop the table.
5. Query the results of pipe number `$2` (the SELECT statement).

The result set consumed in the last SELECT statement is equivalent to the result set returned by the
[RESULT\_SCAN](/sql-reference/functions/result_scan) function for the query ID of the previous SELECT statement.

Copy code

```
CREATE OR REPLACE TABLE test_sql_pipe_drop (
    id INT IDENTITY START 10 INCREMENT 1,
    data VARCHAR)
  ->> INSERT INTO test_sql_pipe_drop (data) VALUES ('row1'), ('row2'), ('row3')
  ->> SELECT * FROM test_sql_pipe_drop
  ->> DROP TABLE test_sql_pipe_drop
  ->> SELECT COUNT(*) "Number of rows", MAX(id) AS "Last ID" FROM $2;
```

```
+----------------+---------+
| Number of rows | Last ID |
|----------------+---------|
|              3 |      12 |
+----------------+---------+
```
