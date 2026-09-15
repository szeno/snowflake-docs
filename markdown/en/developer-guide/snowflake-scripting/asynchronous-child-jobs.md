# Working with asynchronous child jobs

This topic explains how to use asynchronous child jobs in Snowflake Scripting.

## Introduction to asynchronous child jobs

In Snowflake Scripting, an asynchronous child job is a query that runs in the background while code in a block
continues to run. The query can be any valid SQL statement, including SELECT statements and DML statements, such
as INSERT or UPDATE.

To run a query as an asynchronous child job, place the ASYNC keyword before the query. When this keyword is omitted,
the Snowflake Scripting block runs child jobs sequentially, and each child job waits for the running child job to finish before
it starts. Asynchronous child jobs can run concurrently, which can improve efficiency and reduce overall run time.

You can use the ASYNC keyword in the following ways:

- For a query that is run for a [RESULTSET](/developer-guide/snowflake-scripting/resultsets).
- For a query that is run independent of a RESULTSET.

To manage asynchronous child jobs, use the [AWAIT](/sql-reference/snowflake-scripting/await) and
[CANCEL](/sql-reference/snowflake-scripting/cancel) statements:

- The AWAIT statement waits for all asynchronous child jobs that are running to finish or for a specific child job that is
  running for a RESULTSET to finish, then returns when the all jobs have finished or the specific job has finished, respectively.
- The CANCEL statement cancels an asynchronous child job that is running for a RESULTSET.

You can check the status of an asynchronous child job that is running for a RESULTSET by calling the
[SYSTEM$GET\_RESULTSET\_STATUS](/sql-reference/functions/system_get_resultset_status) function.

Currently, up to 4,000 asynchronous child jobs can run concurrently. An error is returned if the number of concurrent
asynchronous child jobs exceeds this limit.

Note

When multiple asynchronous child jobs run concurrently in the same session, the job completion order isn’t
known until the jobs have finished running. Since the completion order can vary, using the
[LAST\_QUERY\_ID](/sql-reference/functions/last_query_id) function with asynchronous child jobs is
non-deterministic.

## Examples of using asynchronous child jobs

The following sections provide examples of using asynchronous child jobs:

- [Example: Running child jobs that query tables concurrently](#label-snowscript-asynchronous-child-jobs-example-resultset-query)
- [Example: Running child jobs that insert rows into tables concurrently](#label-snowscript-asynchronous-child-jobs-example-resultset-insert)
- [Example: Running child jobs in stored procedures with AWAIT ALL statements](#label-snowscript-asynchronous-child-jobs-await-all-stored-procedures)
- [Example: Running child jobs for inserts in a loop](#label-snowscript-asynchronous-child-jobs-example-loop)

### Example: Running child jobs that query tables concurrently

The following code shows how to use the ASYNC keyword to run multiple child jobs that query
tables concurrently. The example specifies the ASYNC keyword for queries that are run for
RESULTSETs.

This example uses the data in the following tables:

Copy code

```
CREATE OR REPLACE TABLE orders_q1_2024 (
  order_id INT,
  order_amount NUMBER(12,2));

INSERT INTO orders_q1_2024 VALUES (1, 500.00);
INSERT INTO orders_q1_2024 VALUES (2, 225.00);
INSERT INTO orders_q1_2024 VALUES (3, 725.00);
INSERT INTO orders_q1_2024 VALUES (4, 150.00);
INSERT INTO orders_q1_2024 VALUES (5, 900.00);

CREATE OR REPLACE TABLE orders_q2_2024 (
  order_id INT,
  order_amount NUMBER(12,2));

INSERT INTO orders_q2_2024 VALUES (1, 100.00);
INSERT INTO orders_q2_2024 VALUES (2, 645.00);
INSERT INTO orders_q2_2024 VALUES (3, 275.00);
INSERT INTO orders_q2_2024 VALUES (4, 800.00);
INSERT INTO orders_q2_2024 VALUES (5, 250.00);
```

The following stored procedure performs the following actions:

- Queries both tables for the `order_amount` values in all rows and returns the results to
  different RESULTSETs (one for each table).
- Specifies that the queries run as concurrent child jobs by using the ASYNC keyword.
- Executes the AWAIT statement for each RESULTSET so
  that the procedure waits for the queries to finish before proceeding. Query results for a
  RESULTSET can’t be accessed until AWAIT is run for the RESULTSET.
- Uses a cursor to calculate the sum of the `order_amount` rows for each table.
- Adds the totals for the tables and returns the value.

Copy code

```
CREATE OR REPLACE PROCEDURE test_sp_async_child_jobs_query()
RETURNS INTEGER
LANGUAGE SQL
AS
DECLARE
  accumulator1 INTEGER DEFAULT 0;
  accumulator2 INTEGER DEFAULT 0;
  res1 RESULTSET DEFAULT ASYNC (SELECT order_amount FROM orders_q1_2024);
  res2 RESULTSET DEFAULT ASYNC (SELECT order_amount FROM orders_q2_2024);
BEGIN
  AWAIT res1;
  LET cur1 CURSOR FOR res1;
  OPEN cur1;
  AWAIT res2;
  LET cur2 CURSOR FOR res2;
  OPEN cur2;
  FOR row_variable IN cur1 DO
      accumulator1 := accumulator1 + row_variable.order_amount;
  END FOR;
  FOR row_variable IN cur2 DO
      accumulator2 := accumulator2 + row_variable.order_amount;
  END FOR;
  RETURN accumulator1 + accumulator2;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE test_sp_async_child_jobs_query()
RETURNS INTEGER
LANGUAGE SQL
AS
$$
  DECLARE
    accumulator1 INTEGER DEFAULT 0;
    accumulator2 INTEGER DEFAULT 0;
    res1 RESULTSET DEFAULT ASYNC (SELECT order_amount FROM orders_q1_2024);
    res2 RESULTSET DEFAULT ASYNC (SELECT order_amount FROM orders_q2_2024);
  BEGIN
    AWAIT res1;
    LET cur1 CURSOR FOR res1;
    OPEN cur1;
    AWAIT res2;
    LET cur2 CURSOR FOR res2;
    OPEN cur2;
    FOR row_variable IN cur1 DO
        accumulator1 := accumulator1 + row_variable.order_amount;
    END FOR;
    FOR row_variable IN cur2 DO
        accumulator2 := accumulator2 + row_variable.order_amount;
    END FOR;
    RETURN accumulator1 + accumulator2;
  END;
$$;
```

Call the stored procedure:

Copy code

```
CALL test_sp_async_child_jobs_query();
```

```
+--------------------------------+
| TEST_SP_ASYNC_CHILD_JOBS_QUERY |
|--------------------------------|
|                           4570 |
+--------------------------------+
```

### Example: Running child jobs that insert rows into tables concurrently

The following code shows how to use the ASYNC keyword to run multiple child jobs that insert
rows into a table concurrently. The example specifies the ASYNC keyword for queries that are run for
RESULTSETs.

The following stored procedure performs the following actions:

- Creates the `orders_q3_2024` table if it doesn’t exist.
- Creates two RESULTSETs, `insert_1` and `insert_2`, that hold the results of inserts into the table.
  The stored procedure arguments specify the values that are inserted into the table.
- Specifies that the inserts run as concurrent child jobs by using the ASYNC keyword.
- Executes the AWAIT statement for each RESULTSET so
  that the procedure waits for the inserts to finish before proceeding. The results of a
  RESULTSET can’t be accessed until AWAIT is run for the RESULTSET.
- Creates a new RESULTSET `res` that holds the results of a query on the `orders_q3_2024` table.
- Returns the results of the query.

Copy code

```
CREATE OR REPLACE PROCEDURE test_sp_async_child_jobs_insert(
  arg1 INT,
  arg2 NUMBER(12,2),
  arg3 INT,
  arg4 NUMBER(12,2))
RETURNS TABLE()
LANGUAGE SQL
AS
  BEGIN
   CREATE TABLE IF NOT EXISTS orders_q3_2024 (
      order_id INT,
      order_amount NUMBER(12,2));
    LET insert_1 RESULTSET := ASYNC (INSERT INTO orders_q3_2024 SELECT :arg1, :arg2);
    LET insert_2 RESULTSET := ASYNC (INSERT INTO orders_q3_2024 SELECT :arg3, :arg4);
    AWAIT insert_1;
    AWAIT insert_2;
    LET res RESULTSET := (SELECT * FROM orders_q3_2024 ORDER BY order_id);
    RETURN TABLE(res);
  END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE test_sp_async_child_jobs_insert(
  arg1 INT,
  arg2 NUMBER(12,2),
  arg3 INT,
  arg4 NUMBER(12,2))
RETURNS TABLE()
LANGUAGE SQL
AS
$$
  BEGIN
   CREATE TABLE IF NOT EXISTS orders_q3_2024 (
      order_id INT,
      order_amount NUMBER(12,2));
    LET insert_1 RESULTSET := ASYNC (INSERT INTO orders_q3_2024 SELECT :arg1, :arg2);
    LET insert_2 RESULTSET := ASYNC (INSERT INTO orders_q3_2024 SELECT :arg3, :arg4);
    AWAIT insert_1;
    AWAIT insert_2;
    LET res RESULTSET := (SELECT * FROM orders_q3_2024 ORDER BY order_id);
    RETURN TABLE(res);
  END;
$$;
```

Call the stored procedure:

Copy code

```
CALL test_sp_async_child_jobs_insert(1, 325, 2, 241);
```

```
+----------+--------------+
| ORDER_ID | ORDER_AMOUNT |
|----------+--------------|
|        1 |       325.00 |
|        2 |       241.00 |
+----------+--------------+
```

### Example: Running child jobs in stored procedures with AWAIT ALL statements

The following examples use the ASYNC keyword to run multiple child jobs concurrently in stored
procedures. The examples specify the ASYNC keyword for statements that aren’t associated with a
RESULTSET, then use the AWAIT ALL statement so that the stored procedure code waits for all of the
asynchronous child jobs to complete.

- [Create a stored procedure that inserts values concurrently](#label-snowscript-asynchronous-child-jobs-await-all-stored-procedures-insert)
- [Create a stored procedure that updates values concurrently](#label-snowscript-asynchronous-child-jobs-await-all-stored-procedures-update)
- [Create a stored procedure that calls other stored procedures concurrently](#label-snowscript-asynchronous-child-jobs-await-all-stored-procedures-call)

#### Create a stored procedure that inserts values concurrently

The following stored procedure uses the ASYNC keyword to run multiple child jobs that insert rows
into a table concurrently. The example specifies the ASYNC keyword for the INSERT statements. The
example also uses the AWAIT ALL statement so that the stored procedure waits for all of the
asynchronous child jobs to complete.

Copy code

```
CREATE OR REPLACE PROCEDURE test_async_child_job_inserts()
RETURNS VARCHAR
LANGUAGE SQL
AS
BEGIN
  CREATE OR REPLACE TABLE test_child_job_queries1 (col1 INT);
  ASYNC (INSERT INTO test_child_job_queries1(col1) VALUES(1));
  ASYNC (INSERT INTO test_child_job_queries1(col1) VALUES(2));
  ASYNC (INSERT INTO test_child_job_queries1(col1) VALUES(3));
  AWAIT ALL;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE test_async_child_job_inserts()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
  CREATE OR REPLACE TABLE test_child_job_queries1 (col1 INT);
  ASYNC (INSERT INTO test_child_job_queries1(col1) VALUES(1));
  ASYNC (INSERT INTO test_child_job_queries1(col1) VALUES(2));
  ASYNC (INSERT INTO test_child_job_queries1(col1) VALUES(3));
  AWAIT ALL;
END;
$$
;
```

#### Create a stored procedure that updates values concurrently

The following stored procedure uses the ASYNC keyword to run multiple child jobs that update rows
in a table concurrently. The example specifies the ASYNC keyword for the UPDATE statements. The
example also uses the AWAIT ALL statement so that the stored procedure waits for all of the
asynchronous child jobs to complete.

Create a table and insert data:

Copy code

```
CREATE OR REPLACE TABLE test_child_job_queries2 (id INT, cola INT);

INSERT INTO test_child_job_queries2 VALUES
  (1, 100), (2, 101), (3, 102);
```

Create the stored procedure:

Copy code

```
CREATE OR REPLACE PROCEDURE test_async_child_job_updates()
RETURNS VARCHAR
LANGUAGE SQL
AS
BEGIN
  ASYNC (UPDATE test_child_job_queries2 SET cola=200 WHERE id=1);
  ASYNC (UPDATE test_child_job_queries2 SET cola=201 WHERE id=2);
  ASYNC (UPDATE test_child_job_queries2 SET cola=202 WHERE id=3);
  AWAIT ALL;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE test_async_child_job_updates()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
  ASYNC (UPDATE test_child_job_queries2 SET cola=200 WHERE id=1);
  ASYNC (UPDATE test_child_job_queries2 SET cola=201 WHERE id=2);
  ASYNC (UPDATE test_child_job_queries2 SET cola=202 WHERE id=3);
  AWAIT ALL;
END;
$$
;
```

#### Create a stored procedure that calls other stored procedures concurrently

Copy code

```
CREATE OR REPLACE PROCEDURE test_async_child_job_calls()
RETURNS VARCHAR
LANGUAGE SQL
AS
BEGIN
  ASYNC (CALL test_async_child_job_inserts());
  ASYNC (CALL test_async_child_job_updates());
  AWAIT ALL;
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE test_async_child_job_calls()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
  ASYNC (CALL test_async_child_job_inserts());
  ASYNC (CALL test_async_child_job_updates());
  AWAIT ALL;
END;
$$
;
```

Call the `test_async_child_job_calls` stored procedure:

Copy code

```
CALL test_async_child_job_calls();
```

Query the tables to see the results:

Copy code

```
SELECT col1 FROM test_child_job_queries1 ORDER BY col1;
```

```
+------+
| COL1 |
|------|
|    1 |
|    2 |
|    3 |
+------+
```

Copy code

```
SELECT * FROM test_child_job_queries2 ORDER BY id;
```

```
+----+------+
| ID | COLA |
|----+------|
|  1 |  200 |
|  2 |  201 |
|  3 |  202 |
+----+------+
```

### Example: Running child jobs for inserts in a loop

The following code shows how to use the ASYNC keyword in a loop to run multiple child jobs that insert
rows into a table concurrently.

This example uses the data in the following tables:

Copy code

```
CREATE OR REPLACE TABLE async_loop_test1(col1 VARCHAR, col2 INT);

INSERT INTO async_loop_test1 VALUES
  ('child', 0),
  ('job', 1),
  ('loop', 2),
  ('test', 3);

CREATE OR REPLACE TABLE async_loop_test2(col1 INT, col2 VARCHAR);
```

Create a stored procedure that inserts values from `async_loop_test1`, concatenated with the text
`async_` into `async_loop_test2` using asynchronous child jobs in a FOR loop. The loop creates a
separate asynchronous child job on each iteration. The AWAIT ALL statement blocks progress in the
stored procedure until all of the child jobs are done.

Copy code

```
CREATE OR REPLACE PROCEDURE async_insert()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
begin
  LET res RESULTSET := (SELECT * FROM async_loop_test1 ORDER BY 1);

  FOR record IN res DO
    LET v VARCHAR := record.col1;
    LET x INT := record.col2;
      ASYNC (INSERT INTO async_loop_test2(col1, col2) VALUES (:x, (SELECT 'async_' || :v)));
    END FOR;

    AWAIT ALL;
    RETURN 'Success';
END;
```

Note: If you use [Snowflake CLI](/developer-guide/snowflake-cli/index), [SnowSQL](/user-guide/snowsql), the Classic Console, or the
`execute_stream` or `execute_string` method in [Python Connector](/developer-guide/python-connector/python-connector)
code, use this example instead (see [Using Snowflake Scripting in Snowflake CLI, SnowSQL, and Python Connector](/developer-guide/snowflake-scripting/running-examples)):

Copy code

```
CREATE OR REPLACE PROCEDURE async_insert()
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
begin
  LET res RESULTSET := (SELECT * FROM async_loop_test1 ORDER BY 1);

  FOR record IN res DO
    LET v VARCHAR := record.col1;
    LET x INT := record.col2;
      ASYNC (INSERT INTO async_loop_test2(col1, col2) VALUES (:x, (SELECT 'async_' || :v)));
    END FOR;

    AWAIT ALL;
    RETURN 'Success';
END;
$$;
```

Call the stored procedure:

Copy code

```
CALL async_insert();
```

```
+--------------+
| ASYNC_INSERT |
|--------------|
| Success      |
+--------------+
```

Query the `async_loop_test2` table to see the results:

Copy code

```
SELECT * FROM async_loop_test2 ORDER BY col1;
```

```
+------+-------------+
| COL1 | COL2        |
|------+-------------|
|    0 | async_child |
|    1 | async_job   |
|    2 | async_loop  |
|    3 | async_test  |
+------+-------------+
```
