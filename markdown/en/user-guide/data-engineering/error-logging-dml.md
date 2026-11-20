# Error logging for DML statements

By default, when a DML statement encounters an error in one row, the statement fails, and Snowflake rolls back the
changes that the statement made. When you turn on error logging for the target table, a statement that encounters a
supported error writes the other rows instead of failing, and records the error in an *error table*. The table for
which error logging is turned on is called the *base table*.

Error logging records errors from the following statements:

- `INSERT`, including [multi-table INSERT](/sql-reference/sql/insert-multi-table): The statement inserts the other
  rows. In a multi-table `INSERT`, an error in a row for a target table that doesn’t have error logging turned on fails
  the whole statement.
- `UPDATE`: The statement updates the other rows and leaves the row that caused the error unchanged.
- `MERGE`: The statement applies the other changes and doesn’t apply the update or the insert for the row that caused
  the error.
- `CREATE TABLE ... AS SELECT` (CTAS) that sets `ERROR_LOGGING = TRUE`: The statement creates the table with the other
  rows. For an example, see [Record errors when creating a table from a query](#label-dml-error-logging-ctas).

The error table also records errors from other sources, such as `COPY INTO` and Snowpipe. For those errors, see
[Error logging for COPY INTO and Snowpipe](/user-guide/data-load-error-tables). To see only the errors from DML and CTAS statements, filter on
`error_metadata:service IS NULL`.

For the columns of the error table, see
[Error table columns](/user-guide/data-engineering/error-tables#label-dml-error-logging-error-table-definition). For the privileges that
you need to query the error table, see
[Access control requirements for error tables](/user-guide/data-engineering/error-tables#label-dml-error-logging-access-control-error-tables).

## Use cases for DML error logging

You might use DML error logging to avoid failures on errors for the following use cases:

- Migration of workloads that rely on DML error logging in another database, such as Oracle.
- Enforcement of some table constraints, such as NOT NULL and CHECK constraints, during data ingestion.

## Supported errors

Error logging records only errors that are directly related to the base table:

- NOT NULL table constraint violations.
- [CHECK constraint](/sql-reference/constraints-overview#label-constraints-check) violations.
- Type conversion errors, which occur when a value can’t be converted to the data type of the base table column.
- Incompatible precision and scale values.
- Incompatible length for string and binary types.
- Some expression evaluation failures, such as division by zero or `PARSE_JSON` function failures.

Other errors fail the statement, the same as when error logging is turned off. For example, a division by zero in the
`ON` condition or in a `WHEN MATCHED AND` condition of a `MERGE` statement fails the statement. A statement that has a
compilation error fails, and no errors are recorded. Snowflake doesn’t enforce PRIMARY KEY, UNIQUE, or FOREIGN KEY
constraints on standard tables, so rows that violate these constraints are written, not recorded as errors. For the
errors that are recorded when you load files with `COPY INTO` or Snowpipe, see
[Which errors are recorded](/user-guide/data-load-error-tables#label-data-load-error-tables-supported).

## Turn on error logging for the target table

Before you turn on error logging, check whether an application or a pipeline relies on a failed statement to detect
bad data. If one does, check the error table instead, as described in [Detect errors in a scheduled job](#label-dml-error-logging-detect-errors), or
opt out of error logging for its sessions, as described in
[Prevent or limit error logging](/user-guide/data-engineering/error-logging#label-error-logging-prevent).

To turn on error logging for an existing table, use a role that owns the table, and run `ALTER TABLE`:

Copy code

```
ALTER TABLE my_table SET ERROR_LOGGING = TRUE;
```

Use `ALTER TABLE`, not `CREATE OR ALTER TABLE`, which doesn’t change the `ERROR_LOGGING` property of a table that
already exists. To create a table with error logging turned on, set `ERROR_LOGGING = TRUE` in the `CREATE TABLE`
statement. For more information, see [Turn on error logging](/user-guide/data-engineering/error-logging#label-dml-error-logging-configure).

## Find the errors from a statement

To see the errors from a statement that you just ran in the same session, filter on its query ID:

Copy code

```
SELECT * FROM ERROR_TABLE(my_table)
  WHERE query_id = LAST_QUERY_ID();
```

`LAST_QUERY_ID()` returns the ID of the most recent statement in the session, so run the query right after the
statement. In a [Snowflake Scripting](/developer-guide/snowflake-scripting/index) block, save the query ID of the
statement from the [SQLID](/developer-guide/snowflake-scripting/query-id) variable instead. For an example, see
[Detect errors in a scheduled job](#label-dml-error-logging-detect-errors).

If you don’t have the query ID, find it in the error table. All of the errors from one statement have the same
`query_id` and `timestamp` values, and the `timestamp` value is the time when the statement started:

Copy code

```
SELECT query_id, timestamp, COUNT(*) AS error_count
  FROM ERROR_TABLE(my_table)
  WHERE error_metadata:service IS NULL
  GROUP BY query_id, timestamp
  ORDER BY timestamp DESC;
```

## Detect errors in a scheduled job

When error logging is turned on, a statement that encounters a supported error doesn’t fail, so a task or a job that
relies on the statement failing doesn’t detect the error. To detect errors, check the error table for errors from the
statement. For example, the following Snowflake Scripting block runs a `MERGE` statement, and then raises an exception
if the statement recorded any errors. The block uses an `orders` table that has error logging turned on, and an
`orders_staging` table that has the same `order_id` and `order_status` columns. In a task, the exception makes the run
fail, so the run appears as failed in the task history and triggers error notifications if you set them up for the task:

Copy code

```
EXECUTE IMMEDIATE $$
DECLARE
  merge_query_id STRING;
  error_count NUMBER;
  merge_errors EXCEPTION (-20001, 'The MERGE statement recorded errors in the error table of the orders table.');
BEGIN
  MERGE INTO orders t
    USING orders_staging s
    ON t.order_id = s.order_id
    WHEN MATCHED THEN UPDATE SET t.order_status = s.order_status
    WHEN NOT MATCHED THEN INSERT (order_id, order_status) VALUES (s.order_id, s.order_status);
  merge_query_id := SQLID;
  SELECT COUNT(*) INTO :error_count
    FROM ERROR_TABLE(orders)
    WHERE query_id = :merge_query_id;
  IF (error_count > 0) THEN
    RAISE merge_errors;
  END IF;
  RETURN 'No errors';
END;
$$;
```

To use the block as the body of a task or a stored procedure, use the part from `DECLARE` to `END;`, with the
delimiters that your client requires, as described in [Using Snowflake Scripting in Snowflake CLI and Python Connector](/developer-guide/snowflake-scripting/running-examples).

The exception doesn’t roll back the `MERGE` statement, which already wrote the other rows. To correct the rows that
the statement couldn’t write, see [Correct and write rows again](#label-dml-error-logging-correct-rows).

## Examples

The following examples turn on DML error logging for tables and show how errors are recorded in error tables.

### Record errors when inserting rows directly

The following example records errors from an `INSERT` statement that inserts values directly into a table:

1. Create a table and turn on error logging for it:

   Copy code

   ```
   CREATE TABLE test_dml_error_logging (
     n NUMBER(4, 0) NOT NULL,
     t VARCHAR(5)
   )
   ERROR_LOGGING = TRUE;
   ```
2. Run an `INSERT` statement that tries to insert several rows, including both valid and invalid
   values:

   Copy code

   ```
   INSERT INTO test_dml_error_logging
     VALUES
       ('invalid_cast', '1'),
       (10, 'valid'),
       (NULL, 'toolong');
   ```

   ```
   +-------------------------+
   | number of rows inserted |
   |-------------------------|
   |                       1 |
   +-------------------------+
   ```
3. Query the table to confirm that one valid row was inserted:

   Copy code

   ```
   SELECT * FROM test_dml_error_logging;
   ```

   ```
   +----+-------+
   |  N | T     |
   |----+-------|
   | 10 | valid |
   +----+-------+
   ```
4. Query the error table for the `test_dml_error_logging` base table to view the errors that
   were recorded:

   Copy code

   ```
   SELECT * FROM ERROR_TABLE(test_dml_error_logging);
   ```

   ```
   +-------------------------------+--------------------------------------+------------+----------------------------------------------------------------------+--------------------+
   | TIMESTAMP                     | QUERY_ID                             | ERROR_CODE | ERROR_METADATA                                                       | ERROR_DATA         |
   |-------------------------------+--------------------------------------+------------+----------------------------------------------------------------------+--------------------|
   | 2026-03-12 12:18:39.470 -0700 | 01c2fc06-000e-6668-0000-76b90170a28e |     100038 | {                                                                    | {                  |
   |                               |                                      |            |   "error_code": 100038,                                              |   "N": [           |
   |                               |                                      |            |   "error_message": "Numeric value 'invalid_cast' is not recognized", |     "invalid_cast" |
   |                               |                                      |            |   "error_source": "N",                                               |   ],               |
   |                               |                                      |            |   "sql_state": "22018"                                               |   "T": "1"         |
   |                               |                                      |            | }                                                                    | }                  |
   | 2026-03-12 12:18:39.470 -0700 | 01c2fc06-000e-6668-0000-76b90170a28e |     100072 | {                                                                    | {                  |
   |                               |                                      |            |   "error_code": 100072,                                              |   "N": [           |
   |                               |                                      |            |   "error_message": "NULL result in a non-nullable column",           |     null           |
   |                               |                                      |            |   "error_source": "N",                                               |   ],               |
   |                               |                                      |            |   "sql_state": "22000"                                               |   "T": [           |
   |                               |                                      |            | }                                                                    |     "toolong"      |
   |                               |                                      |            |                                                                      |   ]                |
   |                               |                                      |            |                                                                      | }                  |
   +-------------------------------+--------------------------------------+------------+----------------------------------------------------------------------+--------------------+
   ```

   The error table contains one error for each row that the statement didn’t insert. In the `error_data` value, each
   invalid value is in an array, and each valid value is shown directly. The second row contains two invalid values,
   `NULL` for the NOT NULL column `N` and `'toolong'` for the `VARCHAR(5)` column `T`. The `error_code` and
   `error_metadata` values describe only the first error, but the `error_data` value shows both invalid values.
5. Turn off error logging for the `test_dml_error_logging` table. Turning off error logging drops the error table and
   the errors in it:

   Copy code

   ```
   ALTER TABLE test_dml_error_logging
     SET ERROR_LOGGING = FALSE;
   ```
6. Run the same `INSERT` statement again. The statement fails, and no errors are recorded:

   Copy code

   ```
   INSERT INTO test_dml_error_logging
     VALUES
       ('invalid_cast', '1'),
       (10, 'valid'),
       (NULL, 'toolong');
   ```

   ```
   100038 (22018): DML operation to table TEST_DML_ERROR_LOGGING failed on column N with error: Numeric value 'invalid_cast' is not recognized
   ```

### Record errors when inserting rows from one table into another table

The following example records errors from an `INSERT` statement that selects rows from one table and inserts them into
another table:

1. Create a source table and insert values:

   Copy code

   ```
   CREATE TABLE dml_error_logging_source(col1 INT);

   INSERT INTO dml_error_logging_source VALUES (1), (0), (-1);
   ```
2. Create a target table with the same definition as the source table:

   Copy code

   ```
   CREATE TABLE dml_error_logging_target(col1 INT);
   ```
3. Turn on error logging for the `dml_error_logging_target` table:

   Copy code

   ```
   ALTER TABLE dml_error_logging_target
     SET ERROR_LOGGING = TRUE;
   ```
4. Insert values into the target table by querying the source table so that one of the inserts
   results in a division-by-zero error:

   Copy code

   ```
   INSERT INTO dml_error_logging_target(col1)
     SELECT 1/col1 FROM dml_error_logging_source;
   ```

   ```
   +-------------------------+
   | number of rows inserted |
   |-------------------------|
   |                       2 |
   +-------------------------+
   ```
5. Query the table to confirm that two valid rows were inserted:

   Copy code

   ```
   SELECT * FROM dml_error_logging_target;
   ```

   ```
   +------+
   | COL1 |
   |------|
   |    1 |
   |   -1 |
   +------+
   ```
6. Query the error table for the `dml_error_logging_target` base table to view the errors that
   were recorded:

   Copy code

   ```
   SELECT * FROM ERROR_TABLE(dml_error_logging_target);
   ```

   ```
   +-------------------------------+--------------------------------------+------------+----------------------------------------+-------------+
   | TIMESTAMP                     | QUERY_ID                             | ERROR_CODE | ERROR_METADATA                         | ERROR_DATA  |
   |-------------------------------+--------------------------------------+------------+----------------------------------------+-------------|
   | 2026-03-12 12:25:56.297 -0700 | 01c2fc0d-000e-6696-0000-76b90170b64a |     100051 | {                                      | {           |
   |                               |                                      |            |   "error_code": 100051,                |   "COL1": [ |
   |                               |                                      |            |   "error_message": "Division by zero", |     1,      |
   |                               |                                      |            |   "error_source": "COL1",              |     0       |
   |                               |                                      |            |   "sql_state": "22012"                 |   ]         |
   |                               |                                      |            | }                                      | }           |
   +-------------------------------+--------------------------------------+------------+----------------------------------------+-------------+
   ```

### Record errors when creating a table from a query

A `CREATE TABLE ... AS SELECT` statement that sets `ERROR_LOGGING = TRUE` creates the table with the rows that don’t
cause errors, and records the errors in the error table of the new table. For example, the following statements create
an `orders_raw` table and then create an `orders_clean` table from it. The row whose `amount` value can’t be
converted to a number isn’t written to the new table, and its error is recorded in the error table:

Copy code

```
CREATE TABLE orders_raw (order_id NUMBER, amount VARCHAR);
INSERT INTO orders_raw VALUES (1, '19.99'), (2, 'n/a');

CREATE TABLE orders_clean (order_id NUMBER, amount NUMBER(10, 2))
  ERROR_LOGGING = TRUE
  AS SELECT order_id, amount FROM orders_raw;
```

To see the errors, query the error table of the new table:

Copy code

```
SELECT * FROM ERROR_TABLE(orders_clean);
```

Error logging stays turned on for the new table, so later `INSERT`, `UPDATE`, and `MERGE` statements on the table also
record errors instead of failing. To turn it off, use `ALTER TABLE orders_clean SET ERROR_LOGGING = FALSE`, which drops
the error table.

A `CREATE OR REPLACE TABLE ... AS SELECT` statement that sets `ERROR_LOGGING = TRUE` works the same way. It drops the
existing table and its error table, so the new error table contains only the errors from the new statement.

A `CREATE TABLE ... AS SELECT` statement that sets `ERROR_LOGGING = TRUE` doesn’t fail when a row has a supported
error. If a job relies on the statement failing, check the error table of the new table after the statement, as
described in [Detect errors in a scheduled job](#label-dml-error-logging-detect-errors). To keep the statement failing on these errors, omit
`ERROR_LOGGING = TRUE` from it, and then turn on error logging for the new table with
`ALTER TABLE ... SET ERROR_LOGGING = TRUE`.

## Correct and write rows again

A statement that records errors already wrote its other rows, so don’t run the whole statement again. Otherwise, it
writes those rows a second time. If the statement runs again before you correct the rows, for example on a schedule,
it records the same errors again, so correct the source data or filter the rows that cause errors out of the statement.

To correct and write the rows, do the following:

1. Query the errors from the statement by filtering on its query ID. The following query gets the values of the `n`
   and `t` columns of a table like the one in [Record errors when inserting rows directly](#label-dml-error-logging-direct-inserts):

   Copy code

   ```
   SELECT
       COALESCE(error_data:N[0], error_data:N)::STRING AS n_value,
       COALESCE(error_data:T[0], error_data:T)::STRING AS t_value,
       error_metadata:error_message::STRING AS error_message
     FROM ERROR_TABLE(my_table)
     WHERE query_id = '<query_id>';
   ```

   Keep the following points in mind:

   - In the `error_data` value, each invalid value is in an array, and each valid value is shown directly. An
     expression such as `COALESCE(error_data:T[0], error_data:T)` gets the column value either way.
   - The keys in the `error_data` value are the column names, which are uppercase unless the columns were created with
     quoted, lowercase names.
   - For an expression evaluation error, such as division by zero, the array can contain more than one value. For
     example, in [Record errors when inserting rows from one table into another table](#label-dml-error-logging-inserts-from-table), the array `[1, 0]` contains both inputs of `1/col1`,
     so `[0]` returns `1`, not the source value `0`. For a column that the statement computes with an expression, get
     the source values from the statement’s source data instead, such as by joining on the key values in the
     `error_data` value.
2. Correct the values, either in the source data or in a statement that converts them.
3. Write only the corrected rows. For an `INSERT` statement, insert the corrected rows. For an `UPDATE` or a `MERGE`
   statement, run the statement again with a condition that selects only the rows that failed, such as a condition on
   the key values of the rows in the error table.

   Error logging is still turned on, so a corrected row that still has an error is recorded in the error table again
   instead of causing the statement to fail. Right after the statement, run the following query in the same session:

   Copy code

   ```
   SELECT
       query_id,
       error_metadata:error_message::STRING AS error_message,
       error_data
     FROM ERROR_TABLE(my_table)
     WHERE query_id = LAST_QUERY_ID();
   ```

   If the query returns rows, the statement didn’t write the rows that the query returns, but it wrote the other
   corrected rows. Don’t run the statement again for all of the corrected rows, because it writes the other rows a
   second time. Instead, repeat this procedure from step 1 for these rows, with the `query_id` value that the query
   returns.
4. Remove the errors from the error table, so that you don’t correct and write the same rows again later. `TRUNCATE`
   removes every error, including errors from loads and from statements that run while you work, and you can’t delete
   individual errors.

   If pipes or `COPY INTO` statements also load the table, follow
   [Stop loads into the table](/user-guide/data-load-error-tables-reload#label-data-load-error-tables-stop-loads) and
   [Clear the error table and resume loads](/user-guide/data-load-error-tables-reload#label-data-load-error-tables-clear) instead. Otherwise, do the
   following:

   - Suspend the tasks and stop the applications that run `INSERT`, `UPDATE`, or `MERGE` statements on the table.
   - Copy the errors that you want to keep to another table, and then truncate the error table. The copy is a regular
     table, so grant access to it only to roles that are allowed to see the source data:

     Copy code

     ```
     CREATE TABLE my_table_errors_archive AS
       SELECT CURRENT_TIMESTAMP() AS archived_at, *
         FROM ERROR_TABLE(my_table);

     TRUNCATE ERROR_TABLE(my_table);
     ```

     The next time that you archive errors, add them to the same table with
     `INSERT INTO my_table_errors_archive SELECT CURRENT_TIMESTAMP(), * FROM ERROR_TABLE(my_table)`.
   - Resume the tasks and applications that you stopped.

   For more information, see [Query and truncate an error table](/user-guide/data-engineering/error-tables#label-error-logging-query-truncate).

## Comparison with Oracle LOG ERRORS INTO

If you’re migrating from Oracle, DML error logging is similar to the `LOG ERRORS INTO` clause, with the following
differences:

- You turn on error logging as a property of the table, not in each statement. Every `INSERT`, `UPDATE`, and `MERGE`
  statement on the table records supported errors instead of failing.
- Snowflake creates the error table automatically, and each base table has one error table. To query it, use the
  `ERROR_TABLE` table function. There’s no tag for each statement. To find the errors from one statement, filter on
  the `query_id` column.
- There’s no reject limit. A statement records every supported error and writes the other rows. To fail a job when a
  statement records errors, check the error table after the statement, as described in
  [Detect errors in a scheduled job](#label-dml-error-logging-detect-errors).
- Errors that a statement records are rolled back if the transaction that contains the statement is rolled back.
  Oracle writes errors in an autonomous transaction, so they’re kept even if the transaction is rolled back.
- Snowflake doesn’t enforce PRIMARY KEY, UNIQUE, or FOREIGN KEY constraints on standard tables, so rows that violate
  these constraints are written, not recorded as errors. For the types of errors that are recorded, see
  [Supported errors](#label-dml-error-logging-supported-errors).

The following table lists the Snowflake equivalents of the Oracle elements:

| Oracle | Snowflake |
| --- | --- |
| `LOG ERRORS INTO <error_table>` in each statement | `ALTER TABLE <table_name> SET ERROR_LOGGING = TRUE`, once for the table. |
| `DBMS_ERRLOG.CREATE_ERROR_LOG` | None. Snowflake creates the error table when you turn on error logging. |
| The tag in `LOG ERRORS INTO <error_table> ('<tag>')` and the `ORA_ERR_TAG$` column | The `query_id` column. |
| The `ORA_ERR_NUMBER$` and `ORA_ERR_MESG$` columns | The `error_code` column and the `error_metadata:error_message` field. |
| The columns for the values of the row | The `error_data` column. |
| `REJECT LIMIT` | None. Check the error table after the statement. |

Expand

Show lessSee more

## Usage notes

The following usage notes apply when error logging is turned on for a table:

- There’s no limit on the number of errors that a statement records. To fail a job when a statement records errors,
  check the error table after the statement, as described in [Detect errors in a scheduled job](#label-dml-error-logging-detect-errors).
- Errors that a statement records are rolled back if the transaction that contains the statement is rolled back.
- If you replace the table with `CREATE OR REPLACE TABLE`, for example to rebuild it, Snowflake drops its error table
  and the errors in it. Copy the errors that you want to keep first, and set `ERROR_LOGGING = TRUE` in the statement
  if the new table must record errors. For more information, see
  [Error table lifecycle](/user-guide/data-engineering/error-tables#label-error-logging-error-table-lifecycle).
- If the [OPT\_OUT\_ERROR\_LOGGING](/sql-reference/parameters#label-opt-out-error-logging) parameter is set to `TRUE` for a session, statements in the session don’t
  record errors. A statement that encounters a supported error fails, as if error logging were turned off.
- The following are considerations related to DML error logging and performance:
  - When error logging is turned on for a base table, and there are *no* errors in a DML statement that is run on the
    base table, there’s little or no difference in performance.
  - When error logging is turned on for a base table, and there *are* errors in a DML statement that is run on the
    base table, additional time is required to complete the DML statement because the error information is inserted into
    the error table.
