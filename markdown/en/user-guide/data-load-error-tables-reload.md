# Correct and reload rejected rows

When error logging is turned on for a table, you can correct the rows that `COPY INTO` and Snowpipe rejected and load
them again, without loading any rows twice. To find out which rows were rejected and why, see
[Query load errors](/user-guide/data-load-error-tables-query). The error table doesn’t contain the rows that loads rejected before error
logging started recording errors. To load the files that those rows came from, see
[Reload a file that Snowpipe already processed](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-reload-files).

The examples on this page use the `orders` table and the `orders_pipe` pipe, which loads JSON files from
`@orders_stage/json/` with `MATCH_BY_COLUMN_NAME`. For their definitions, see
[Turn on error logging and add CHECK constraints](/user-guide/data-load-error-tables#label-data-load-error-tables-turn-on) and
[Load files with ON\_ERROR = CONTINUE](/user-guide/data-load-error-tables#label-data-load-error-tables-load-files). Replace `mydb` and `myschema` with the
database and schema that contain your table.

How you load rejected rows again depends on the `ON_ERROR` value of the load that rejected them:

- With `ON_ERROR = CONTINUE`, the load inserted the valid rows from the file, and the error table contains every
  rejected row. Correct the rejected rows and insert them from the error table.
- With `ON_ERROR = SKIP_FILE`, the default for pipes, the load didn’t insert any rows from the file, and the error table
  contains only one error for the file. Load the file again.
- If loads used both values, for example because you recreated a pipe with `ON_ERROR = CONTINUE`, do both, in the
  order described in [Reload rejected rows in order](#label-data-load-error-tables-reload-steps).

To see which of these cases apply, count the errors in the error table by source and by `ON_ERROR` value:

Copy code

```
SELECT
    error_metadata:service::STRING AS service,
    error_metadata:details:on_error::STRING AS on_error,
    COUNT(*) AS error_count
  FROM ERROR_TABLE(orders)
  GROUP BY ALL;
```

Errors from DML statements and `CREATE TABLE ... AS SELECT` statements have a `NULL` service. If the error table
contains these errors, correct and write those rows separately before you clear the error table, as described in
[Correct and write rows again](/user-guide/data-engineering/error-logging-dml#label-dml-error-logging-correct-rows).

## Reload rejected rows in order

Before you start, check the following:

- Your role has the privileges that these steps require. For more information, see
  [Access control requirements](/user-guide/data-load-error-tables#label-data-load-error-tables-access-control).
- The stage still contains the files that the loads skipped. Pause any storage lifecycle rule or cleanup job that
  removes files from the stage until you finish.
- No `COPY INTO` statement used `PURGE = TRUE`. If one did, it also removed the files that it loaded partially, so
  the error table might contain the only copy of the rejected rows. Don’t clear the error table until you insert or
  copy those rows.

Work in the following order, so that you don’t lose the list of skipped files or insert the same rows twice:

1. Stop the loads that record errors in the table, as described in [Stop loads into the table](#label-data-load-error-tables-stop-loads). To
   confirm that they stopped, run the earlier query that counts the errors, and run it again a few minutes later. If the
   counts change, a load is still recording errors.
2. If any load used `ON_ERROR = SKIP_FILE`, load the files that it skipped, as described in
   [Load files skipped with ON\_ERROR = SKIP\_FILE](#label-data-load-error-tables-reload-skip-file). A load used `SKIP_FILE` if its `COPY INTO` statement or pipe
   definition, including the definition that a pipe had before you recreated it, sets `SKIP_FILE`, or if a pipe
   definition doesn’t set `ON_ERROR`. Don’t rely on the error table alone, because it might not list every skipped file.
3. Insert the corrected rows from the error table once, including any rows that the loads in step 2 rejected, as
   described in [Insert rows rejected with ON\_ERROR = CONTINUE](#label-data-load-error-tables-reload-continue).
4. Clear the error table, and then resume the loads, as described in [Clear the error table and resume loads](#label-data-load-error-tables-clear).
5. After new files arrive, confirm that the loads work again: the `lastIngestedTimestamp` value that
   `SYSTEM$PIPE_STATUS` returns for each pipe is later than the time that you resumed the pipe, and the next run of
   each task that you resumed succeeds.

## Stop loads into the table

Stop every load and statement that records errors in the table, and keep them stopped until you clear the error table.
Otherwise, `TRUNCATE` also removes the new errors that they record, so you can’t load those rows again.

A `NULL` pipe name in the following query stands for all of the `COPY INTO` statements, and for pipes on which your role
doesn’t have the `MONITOR` or `OWNERSHIP` privilege. To find the pipes that loaded the table in the last 14 days, and
whether `COPY INTO` statements loaded it, run the following query:

Copy code

```
SELECT pipe_name,
       COUNT(DISTINCT file_name) AS file_count,
       MAX(last_load_time) AS last_load_time
  FROM TABLE(mydb.INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'myschema.orders',
    START_TIME => DATEADD(day, -14, CURRENT_TIMESTAMP())))
  GROUP BY pipe_name;
```

The query doesn’t list pipes that haven’t loaded the table in the last 14 days. To find them, check the `definition`
column of the [SHOW PIPES](/sql-reference/sql/show-pipes) output.

Then do the following:

- Pause each pipe that loads the table:

  Copy code

  ```
  ALTER PIPE orders_pipe SET PIPE_EXECUTION_PAUSED = TRUE;
  ```

  Files that a pipe is loading when you pause it can still finish loading and record errors, so wait a few minutes,
  and then check that the pipe’s `executionState` is `PAUSED`:

  Copy code

  ```
  SELECT PARSE_JSON(SYSTEM$PIPE_STATUS('orders_pipe')):executionState::STRING AS execution_state;
  ```

  A paused pipe keeps adding new files to its queue and loads them after you resume it. Resume the pipe within 14
  days, or it becomes stale, as described in [Resume a stale pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-resume-stale-pipe).
  If you pause the pipes by setting `PIPE_EXECUTION_PAUSED` for the schema, check the status of each pipe, because
  the schema setting doesn’t pause a pipe that someone resumed directly with `ALTER PIPE`.
- Suspend any tasks that run `COPY INTO` for the table, and wait until their runs in progress finish. To find runs in
  progress, query [TASK\_HISTORY](/sql-reference/functions/task_history) for runs with the `EXECUTING` state:

  Copy code

  ```
  ALTER TASK load_orders_task SUSPEND;

  SELECT name, state, scheduled_time
    FROM TABLE(mydb.INFORMATION_SCHEMA.TASK_HISTORY(TASK_NAME => 'LOAD_ORDERS_TASK'))
    WHERE state = 'EXECUTING';
  ```
- Don’t run other `COPY INTO` statements for the table, except the statements that load skipped files again.
- Stop the other applications and tasks that write to the table, such as those that run `INSERT`, `UPDATE`, or
  `MERGE` statements on it. These statements record errors in the same error table.
- Don’t recreate a pipe until you clear the error table and resume the loads. A new pipe has no load metadata, so it can
  load the same files that you reload.
- Tell anyone who sends files to the stage not to send corrected copies of the files whose rows you’re reloading to a
  path that a pipe, a task, or an application loads from. A load treats a corrected copy that has a new name as a new
  file, so the rows are loaded twice.

## Load files skipped with ON\_ERROR = SKIP\_FILE

If every load used `ON_ERROR = CONTINUE`, including pipes before you recreated them, go to
[Insert rows rejected with ON\_ERROR = CONTINUE](#label-data-load-error-tables-reload-continue). When a load skips a file, none of its rows are loaded, and the error
table contains only one error for the file. To load the rows, list the skipped files, and then load each file again.

### List the skipped files

Start with the error table. To list the files that loads skipped, run the following query:

Copy code

```
SELECT DISTINCT
    error_metadata:service::STRING AS service,
    error_metadata:details:pipe_name::STRING AS pipe_name,
    error_metadata:details:stage_location::STRING AS stage_location,
    error_metadata:details:file_name::STRING AS file_name
  FROM ERROR_TABLE(orders)
  WHERE error_metadata:details:on_error = 'SKIP_FILE';
```

The error table lists only the files that loads skipped after error logging started recording errors, and some errors
don’t include the file name. To find every skipped file, also check the copy history for files with the `Load failed`
status. Don’t load a file again if a load with `ON_ERROR = CONTINUE` rejected all of its rows, because its rows are
already in the error table. For more information, see [Files with the Load failed status](#label-data-load-error-tables-load-failed).

If you haven’t recreated or dropped the pipe, use the following query. It uses the
[COPY\_HISTORY](/sql-reference/functions/copy_history) table function, which covers the last 14 days and doesn’t return a recreated
pipe’s earlier loads. Use a role that owns the pipe or has the `MONITOR` privilege on it. With any other role, the
`pipe_name` column is `NULL`, and the query returns no rows:

Copy code

```
SELECT DISTINCT stage_location, file_name
  FROM TABLE(mydb.INFORMATION_SCHEMA.COPY_HISTORY(
    TABLE_NAME => 'myschema.orders',
    START_TIME => DATEADD(day, -14, CURRENT_TIMESTAMP())))
  WHERE pipe_name = 'ORDERS_PIPE'
    AND status = 'Load failed';
```

In the copy history, the `pipe_name` value doesn’t include the database and schema, and the `file_name` value is
relative to the path that the pipe loads from. For example, the copy history shows `orders_0001.json` for the file that
the error table shows as `json/orders_0001.json`.

For a pipe that was dropped or recreated, and for files that a pipe skipped more than 14 days ago, query the
[COPY\_HISTORY view](/sql-reference/account-usage/copy_history) in the ACCOUNT\_USAGE schema instead. The view can take up to 2 hours, or
for some tables up to 2 days, to show a load. If you recreated the pipe with `ON_ERROR = CONTINUE`, the new pipe also
gives the `Load failed` status to files from which it loads no rows. To list only the old pipe’s files, filter on a
`last_load_time` value earlier than the `created_on` time of the new pipe in the [SHOW PIPES](/sql-reference/sql/show-pipes)
output. The following query uses an example time:

Copy code

```
SELECT DISTINCT stage_location, file_name
  FROM SNOWFLAKE.ACCOUNT_USAGE.COPY_HISTORY
  WHERE table_catalog_name = 'MYDB'
    AND table_schema_name = 'MYSCHEMA'
    AND table_name = 'ORDERS'
    AND pipe_name = 'ORDERS_PIPE'
    AND status = 'Load failed'
    AND last_load_time < '2026-10-02T21:45:00+00:00';
```

To list the files that a `COPY INTO` statement skipped, such as a statement that a task runs, filter on
`pipe_name IS NULL` instead. With the table function, use a role that has the `MONITOR` or `OWNERSHIP` privilege on
every pipe that loads the table, so that the files that the pipes skipped aren’t listed with a `NULL` pipe name.

Before you load a file from this list, check the copy history for a later load of the same file, such as a load by a
recreated pipe or an earlier reload. If a later load loaded the file, don’t load it again. Keep a list of the files that
you load, because the copy history still lists them with the `Load failed` status.

### Load each skipped file

Load the file unchanged with `ON_ERROR = CONTINUE`. The load inserts each valid row once, and the error table records
every rejected row, which you can correct as described in [Insert rows rejected with ON\_ERROR = CONTINUE](#label-data-load-error-tables-reload-continue).

To load a file that a pipe or a `COPY INTO` statement skipped, write a `COPY INTO` statement as follows:

1. Start from the `COPY INTO` statement in the pipe definition or the task, including any column list or
   transformation.
2. Set `ON_ERROR = CONTINUE`.
3. In the `FROM` clause, specify only the stage, such as `@orders_stage`, not the path that the pipe loads from, such as
   `@orders_stage/json/`. In the `FILES` parameter, specify the error table’s `file_name` value, which is relative to
   the stage. If you listed the file with the copy history instead, add the pipe’s path to the file name. The `FILES`
   parameter accepts up to 1,000 file names, so load longer lists in batches.
4. If the file was last modified more than 64 days ago, add `LOAD_UNCERTAIN_FILES = TRUE`. Otherwise, `COPY INTO`
   might skip the file, because bulk load metadata expires after 64 days. For more information, see
   [Loading older files](/user-guide/data-load-considerations-load#label-loading-older-files).

For example, the following statement loads a file that the `orders_pipe` pipe skipped before you recreated it with
`ON_ERROR = CONTINUE`:

Copy code

```
COPY INTO orders
  FROM @orders_stage
  FILES = ('json/orders_0001.json')
  FILE_FORMAT = (TYPE = JSON)
  MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
  ON_ERROR = CONTINUE;
```

Check the output of the statement. If a file isn’t listed in the output, the statement didn’t load it.

To instead correct a file before you load it, find its errors with [VALIDATE\_PIPE\_LOAD](/sql-reference/functions/validate_pipe_load) or
with a `COPY INTO` statement that sets `VALIDATION_MODE = RETURN_ALL_ERRORS`. Neither one returns CHECK constraint
violations or supports loads that use `MATCH_BY_COLUMN_NAME`, such as the `orders_pipe` pipe. Stage the corrected file
in a path that no pipe loads from, and load it from there. Otherwise, a pipe that has no load metadata for the file,
such as a recreated pipe, can also load it, and the rows are loaded twice.

## Insert rows rejected with ON\_ERROR = CONTINUE

Before you write an `INSERT` statement, keep the following points in mind:

- Select only the errors that you want to correct:
  - Select only the errors from loads that used `ON_ERROR = CONTINUE`, as the following examples do with the
    `on_error` field. The files that `SKIP_FILE` errors came from weren’t loaded, so load those files again instead,
    as described in [Load files skipped with ON\_ERROR = SKIP\_FILE](#label-data-load-error-tables-reload-skip-file). If you insert the rows and also load the
    files, the rows are loaded twice.
  - Select only the rows that your correction fixes, as the following examples do by checking both the original value
    and the corrected value.
  - If several pipes or other loads write to the table, also filter on fields such as `pipe_name`, which contains the
    fully qualified name of the pipe, such as `'MYDB.MYSCHEMA.ORDERS_PIPE'`. A filter on `file_name` misses errors that
    have no file name, such as some CHECK constraint violations, and a filter on `pipe_name` misses errors from
    `COPY INTO` statements.
- The `INSERT` statement doesn’t apply the load’s file format options, such as `NULL_IF` or `DATE_FORMAT`, or the
  load’s transformations. List every column that the load sets, and apply the same conversions in the `SELECT`
  statement. Columns that you don’t list get their default value or `NULL`, including columns that the load sets from
  metadata such as `METADATA$FILENAME`. If you can’t reproduce the load’s conversions, put the corrected records in a
  new file, stage it in a path that no pipe loads from, and load it with the load’s column list, transformations, file
  format options, and copy options.
- If a `COPY INTO` statement loaded the same file more than once, such as a statement that a task runs on a schedule,
  the error table contains the file’s rejected rows once for each load. To insert each row only once, select only the
  errors from the most recent load of each file by filtering on the `query_id` value of that load.
- Run the `INSERT` statement only once for each set of errors. The statement selects every matching row in the error
  table, so running it again inserts the rows again. If you aren’t sure whether a statement already ran, check the
  [query history](/user-guide/ui-snowsight-activity).
- Don’t also load a corrected copy of the source file. The load with `ON_ERROR = CONTINUE` already inserted the
  file’s valid rows, so they would be loaded twice. For the same reason, don’t correct a file in place in a path that a
  load reads from, because a later load handles the modified file as a new file.

For example, suppose that the `orders_pipe` pipe rejects rows because their `order_status` value is lowercase, such as
`'shipped'`. The CHECK constraint accepts only `'NEW'`, `'SHIPPED'`, and `'CANCELED'`. The following statement
changes the `order_status` value to uppercase and inserts only the rows that the change corrects:

Copy code

```
INSERT INTO orders (order_id, order_status)
  SELECT
      TRY_TO_NUMBER(src:order_id::STRING),
      UPPER(src:order_status::STRING)
    FROM (
      SELECT TRY_PARSE_JSON(error_data:"$1"::STRING) AS src
        FROM ERROR_TABLE(orders)
        WHERE error_metadata:details:file_format_type = 'JSON'
          AND error_metadata:details:on_error = 'CONTINUE'
    )
    WHERE src:order_status::STRING NOT IN ('NEW', 'SHIPPED', 'CANCELED')
      AND UPPER(src:order_status::STRING) IN ('NEW', 'SHIPPED', 'CANCELED')
      AND TRY_TO_NUMBER(src:order_id::STRING) IS NOT NULL;
```

Key names in a path such as `src:order_id` are case-sensitive, even though the pipe matches keys to columns
case-insensitively. Use the key names exactly as they appear in your files.

For a CSV file, the `$1` field contains the raw text of the record, so split the text into fields. For example, the
following statement corrects records such as `1002,shipped` that the `COPY INTO` example in
[Get started](/user-guide/data-load-error-tables#label-data-load-error-tables-get-started) rejects. It selects only records that
have two fields, so it doesn’t insert records that were rejected because they have the wrong number of fields:

Copy code

```
INSERT INTO orders (order_id, order_status)
  SELECT
      TRY_TO_NUMBER(SPLIT_PART(record, ',', 1)),
      UPPER(SPLIT_PART(record, ',', 2))
    FROM (
      SELECT error_data:"$1"::STRING AS record
        FROM ERROR_TABLE(orders)
        WHERE error_metadata:details:file_format_type = 'CSV'
          AND error_metadata:details:on_error = 'CONTINUE'
    )
    WHERE ARRAY_SIZE(SPLIT(record, ',')) = 2
      AND SPLIT_PART(record, ',', 2) NOT IN ('NEW', 'SHIPPED', 'CANCELED')
      AND UPPER(SPLIT_PART(record, ',', 2)) IN ('NEW', 'SHIPPED', 'CANCELED')
      AND TRY_TO_NUMBER(SPLIT_PART(record, ',', 1)) IS NOT NULL;
```

`SPLIT_PART` doesn’t handle fields that are enclosed in quotes and contain the delimiter. If your records contain
fields like these, put the corrected records in a new file and load that file.

Error logging is still turned on, so a corrected row that still has an error is recorded in the error table again
instead of failing the statement. These errors don’t have the `on_error` field, so the examples in this section don’t
select them. Immediately after you run an `INSERT` statement, run the following query in the same session to check that
the statement didn’t record new errors:

Copy code

```
SELECT
    query_id,
    error_metadata:error_message::STRING AS error_message,
    error_data
  FROM ERROR_TABLE(orders)
  WHERE query_id = LAST_QUERY_ID();
```

If the query returns rows, the `INSERT` statement still inserted the other rows, so don’t run the `INSERT` statement
again. Before you clear the error table, correct the rows that the query returns, and insert only those rows, as
described in steps 1 to 3 of [Correct and write rows again](/user-guide/data-engineering/error-logging-dml#label-dml-error-logging-correct-rows).

## Clear the error table and resume loads

After you load the rows again, remove the errors from the error table so that you don’t load the same rows twice. You
can’t delete individual rows from an error table. `TRUNCATE` removes every row from the error table, including errors
from DML statements, errors from other loads, and errors that a load records after you query the error table. Before
you clear the error table, do the following:

- If you process errors with a
  [stream on a view of the error table](/user-guide/data-load-error-tables-query#label-data-load-error-tables-stream),
  consume the stream first. Errors that are recorded and then cleared before you consume the stream don’t appear in it.
- Run the earlier query that counts the errors, and confirm that you handled each kind of error. For `SKIP_FILE` errors,
  you loaded the files again. For `CONTINUE` errors, you inserted the corrected rows. For errors that have a `NULL`
  service, including errors that your `INSERT` statements recorded, you corrected the rows.
- If a task or an application runs a `COPY INTO` statement for the table on a schedule, move the files from which it
  loaded no rows to a location that no pipe, task, or application loads from. With `ON_ERROR = CONTINUE`, these files
  have the `Load failed` status in the copy history, so the next run loads them again. To list the files from which
  these statements rejected rows, run the following query:

  Copy code

  ```
  SELECT DISTINCT
      error_metadata:details:stage_location::STRING AS stage_location,
      error_metadata:details:file_name::STRING AS file_name
    FROM ERROR_TABLE(orders)
    WHERE error_metadata:service = 'copy'
      AND error_metadata:details:on_error = 'CONTINUE';
  ```

  If the query returns a row whose `file_name` value is `NULL`, also use the copy history to list the files in the
  scheduled statement’s path from which a load with `ON_ERROR = CONTINUE` loaded no rows. Don’t list a file that
  Snowflake couldn’t read, as described in [Files with the Load failed status](#label-data-load-error-tables-load-failed). Fix the problem instead, so
  that the scheduled statement loads the file again.
- To keep the errors that you didn’t load again, such as errors that your correction doesn’t fix, copy them to
  another table. For example, the following statement copies every error, with the time that you archived it:

  Copy code

  ```
  CREATE TABLE orders_errors_archive AS
    SELECT CURRENT_TIMESTAMP() AS archived_at, *
      FROM ERROR_TABLE(orders);
  ```

  The next time that you archive errors, add them to the same table with
  `INSERT INTO orders_errors_archive SELECT CURRENT_TIMESTAMP(), * FROM ERROR_TABLE(orders)`. The copy is a regular
  table, so the access controls on the error table don’t apply to it. Grant access to the copy only to roles that are
  allowed to see the source data, and check whether grants on future tables in the schema give other roles access to
  it.

Warning

`TRUNCATE` removes every error in the error table, and you can’t recover the errors afterward. Before you run it,
check that the loads are still stopped and that you copied any errors that you want to keep.

To clear the error table, run the following statement. The role that runs it must have the `TRUNCATE` privilege on
the target table or own the table. The `SELECT ERROR TABLE` privilege isn’t enough.

Copy code

```
TRUNCATE ERROR_TABLE(orders);
```

Check that the statement specifies `ERROR_TABLE(orders)`. The statement `TRUNCATE TABLE orders` deletes the rows in
the `orders` table instead.

After you clear the error table, resume the loads that you stopped:

1. Resume each paused pipe with `ALTER PIPE orders_pipe SET PIPE_EXECUTION_PAUSED = FALSE`. If you paused the pipes for
   the schema, resume them with `ALTER SCHEMA mydb.myschema SET PIPE_EXECUTION_PAUSED = FALSE` instead. Then check that
   each pipe’s `executionState` is `RUNNING`. If a pipe was paused for more than 14 days, resume it with
   `SYSTEM$PIPE_FORCE_RESUME`, as described in
   [Resume a stale pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-resume-stale-pipe).
2. Resume the tasks that you suspended, such as with `ALTER TASK load_orders_task RESUME`, including tasks that run
   `INSERT`, `UPDATE`, or `MERGE` statements on the table.
3. Restart the applications that you stopped.

## Files with the Load failed status

In the copy history, a file can have the `Load failed` status for several reasons. How you load the file’s rows again
depends on the reason:

| Reason | What the error table contains | What to do |
| --- | --- | --- |
| A load with `ON_ERROR = SKIP_FILE` skipped the file. | One error for the file, with `SKIP_FILE` in the `on_error` field. | Load the file again, as described in [Load files skipped with ON\_ERROR = SKIP\_FILE](#label-data-load-error-tables-reload-skip-file). |
| A load with `ON_ERROR = CONTINUE` rejected every row in the file. | Every rejected row from the file, with `CONTINUE` in the `on_error` field. | Don’t load the file again. If you do, the error table records the rows twice. Insert the corrected rows from the error table, as described in [Insert rows rejected with ON\_ERROR = CONTINUE](#label-data-load-error-tables-reload-continue). |
| Snowflake couldn’t read the file, for example because Snowflake couldn’t access it. | No errors that show the name of the file. | To find out why the file failed, check the `first_error_message` column of the copy history. Fix the problem, and then load the file again. A pipe doesn’t load the file again on its own. For a file that a pipe processed, see [Reload a file that Snowpipe already processed](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-reload-files). |

Expand

Show lessSee more

Some errors don’t include the file name, so Snowflake might have read a file even if no error shows its name.
