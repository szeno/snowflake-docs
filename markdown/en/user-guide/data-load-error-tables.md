# Error logging for COPY INTO and Snowpipe

Turn on error logging for a table to keep the rows that `COPY INTO` and Snowpipe reject, so that you can see why they
were rejected, correct them, and load them again with SQL. A row is *rejected* when `COPY INTO` or Snowpipe can’t load
it from a staged file. For example, a row is rejected if it can’t be parsed, if a value can’t be converted to the data
type of its column, or if a value violates a NOT NULL or CHECK constraint. Snowflake records rejected rows in the
table’s *error table*, along with the error, the source data, and, when Snowflake can determine it, the location of the
row in the file. The `ON_ERROR` copy option determines which rejected rows are recorded.

Error logging is a property of the target table, which is also called the *base table*. You can turn it on for
Snowflake-managed Apache Iceberg™ tables and for standard tables, including transient tables. It records errors from CSV,
JSON, and Parquet files. A table that has error logging turned on has one error table, which also records errors from
other sources, such as DML statements. For the error table columns and other details that apply to every source of
errors, see [Error tables](/user-guide/data-engineering/error-tables). For error logging in Snowpipe Streaming with high-performance
architecture, see [Error logging in Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).

## Get started

The examples on this page and on the related pages use the `orders` table that’s created in
[Turn on error logging and add CHECK constraints](#label-data-load-error-tables-turn-on), and they load CSV and JSON files from the `csv/` and `json/` paths of a stage
named `orders_stage`.

Before you start, make sure that your role has the following privileges:

- To turn on error logging: `OWNERSHIP` on the target table.
- To query the error table: `OWNERSHIP` on the target table, or both `SELECT` and `SELECT ERROR TABLE` on it. If a
  masking policy, a row access policy, or a projection policy is set on the table or on its columns, see
  [Access control requirements](#label-data-load-error-tables-access-control) before you continue.

The error table stores the source data of each rejected row, including values in columns that have a masking policy, so
grant access only to roles that are allowed to see that data. Roles that have `ALL` privileges on the table can also
query it, so check which roles have these privileges before you turn on error logging, as described in
[Access control requirements](#label-data-load-error-tables-access-control).

To start recording the rows that are rejected when you load files into a table, do the following:

1. Turn on error logging for the target table:

   Copy code

   ```
   ALTER TABLE orders SET ERROR_LOGGING = TRUE;
   ```

   Error logging also applies to `INSERT`, `UPDATE`, and `MERGE` statements on the table. When one of these statements
   encounters a supported error, such as a CHECK constraint violation, it writes the other rows and records the error
   instead of failing. If a job detects bad data by checking whether these statements fail, see
   [Detect errors in a scheduled job](/user-guide/data-engineering/error-logging-dml#label-dml-error-logging-detect-errors) first.
2. Optional: To reject the rows that don’t meet a rule, such as a list of allowed values, add a CHECK constraint. Add it
   before you create the pipes that load the table, because you can’t add one to a table that a pipe loads. For an
   example, see [Turn on error logging and add CHECK constraints](#label-data-load-error-tables-turn-on). If a pipe already loads the table, see
   [Change the CHECK constraints on a table that a pipe loads](/user-guide/data-load-error-tables-pipes#label-data-load-error-tables-add-check).
3. The default for `COPY INTO`, `ABORT_STATEMENT`, records no errors, so load the files with `ON_ERROR = CONTINUE`,
   which loads the valid rows and records every rejected row:

   Copy code

   ```
   COPY INTO orders
     FROM @orders_stage/csv/
     FILE_FORMAT = (TYPE = CSV)
     ON_ERROR = CONTINUE;
   ```

   With `CONTINUE`, the statement doesn’t fail when it rejects rows. A scheduled job that checks whether the statement
   fails no longer detects bad data, so check the error table after each load instead, as described in
   [Detect errors in a scheduled job](/user-guide/data-engineering/error-logging-dml#label-dml-error-logging-detect-errors), or create an
   [alert](/user-guide/data-load-error-tables-query#label-data-load-error-tables-alert).

   For a pipe, the default, `SKIP_FILE`, records one error for each file that the pipe skips. To record every rejected
   row, set `ON_ERROR = CONTINUE` in the pipe’s `COPY INTO` statement. This setting changes the error notifications and
   events for files that contain errors, so see [Choose an ON\_ERROR value for a pipe](#label-data-load-error-tables-pipe-on-error) first. For a pipe that
   already loads the table, see
   [Record errors from an existing pipe](/user-guide/data-load-error-tables-pipes#label-data-load-error-tables-existing-pipes).
4. After a load rejects rows, query the error table. The following query returns one row for each error, with the
   file, the number of the record in the file, the reason that the record was rejected, and the record as it appears
   in the file:

   Copy code

   ```
   SELECT
       error_metadata:details:file_name::STRING AS file_name,
       error_metadata:details:row_number::NUMBER AS record_number,
       error_metadata:error_message::STRING AS error_message,
       COALESCE(error_data:"$1"::STRING, TO_JSON(error_data)) AS source_record
     FROM ERROR_TABLE(orders)
     WHERE error_metadata:service IN ('copy', 'snowpipe')
     ORDER BY timestamp DESC;
   ```

   The `service` filter returns only the errors from `COPY INTO` and Snowpipe. Snowflake omits the fields that it can’t
   determine for an error, so some values can be `NULL`. For a description of each field, see
   [Error table fields for file loads](/user-guide/data-load-error-tables-query#label-data-load-error-tables-fields).

To monitor loads for new errors, see [Query load errors](/user-guide/data-load-error-tables-query). If the error table doesn’t contain
the errors that you expect, see
[Troubleshoot missing errors](/user-guide/data-load-error-tables-query#label-data-load-error-tables-missing-errors). To correct the rejected rows
and load them, see [Correct and reload rejected rows](/user-guide/data-load-error-tables-reload).

## When to use error tables

Use error tables when you want to keep the rows that `COPY INTO` and Snowpipe reject, so that you can analyze them with
SQL and load them again. The following table compares error tables with the other tools that report errors in the files
that `COPY INTO` and Snowpipe load:

| Tool | What it reports |
| --- | --- |
| Error tables | Rejected rows from CSV, JSON, and Parquet files, including CHECK constraint violations and rows from loads that transform data. Each error includes the source data and, when Snowflake can determine it, the location of the row in the file. Which rows are recorded depends on the `ON_ERROR` value. |
| `COPY INTO` output and [COPY\_HISTORY](/sql-reference/functions/copy_history) | The load status of each file and the first error in the file. |
| `VALIDATION_MODE` parameter of [COPY INTO <table>](/sql-reference/sql/copy-into-table) | Errors in staged files before you load them, except CHECK constraint violations. Doesn’t support loads that transform data or loads into Iceberg tables. |
| [VALIDATE](/sql-reference/functions/validate) | The errors from an earlier `COPY INTO` statement, except CHECK constraint violations. Returns no results for loads that use `ON_ERROR = ABORT_STATEMENT`, and doesn’t support loads that transform data. |
| [VALIDATE\_PIPE\_LOAD](/sql-reference/functions/validate_pipe_load) | Errors in the files that a pipe processed in the last 14 days, except CHECK constraint violations. Doesn’t support pipes that transform semi-structured data, such as JSON or Parquet data, or that use `MATCH_BY_COLUMN_NAME`. |
| [Snowpipe error notifications](/user-guide/data-load-snowpipe-errors) | A message to your cloud messaging service that lists the files that a pipe failed to load, with the first error in each file. Files that load partially don’t trigger a message. |
| [Snowpipe events](/user-guide/data-load-snowpipe-monitor-events) | Pipe errors and file errors, recorded in an event table. |

Expand

Show lessSee more

## Which errors are recorded

Error logging records errors in individual rows. It doesn’t record problems that prevent a file from being read, or
problems with a pipe, as described in [Limitations](#label-data-load-error-tables-limitations). Error logging also doesn’t change
which rows or files are loaded. The `ON_ERROR` copy option still controls how a load handles errors, and it also
determines which errors are recorded in the error table:

| `ON_ERROR` value | Rows loaded from a file that contains errors | Errors recorded in the error table |
| --- | --- | --- |
| `CONTINUE` | Every row that doesn’t contain an error. | Every rejected row. |
| `SKIP_FILE` (default for pipes) | None. | One error for the file. |
| `ABORT_STATEMENT` (default for `COPY INTO`) | None. The statement fails. | None. |
| `SKIP_FILE_<num>` or `'SKIP_FILE_<num>%'` | Depends on the value. For more information, see [ON\_ERROR](/sql-reference/sql/copy-into-table#label-copy-into-table-copyoptions). | Not supported. The error table might contain no errors or only some errors from these loads. |

Expand

Show lessSee more

For a `COPY INTO` statement, use `ON_ERROR = SKIP_FILE` instead of `CONTINUE` if the target table must never contain
part of a file. To load the rows of a skipped file, see
[Load files skipped with ON\_ERROR = SKIP\_FILE](/user-guide/data-load-error-tables-reload#label-data-load-error-tables-reload-skip-file).

## Choose an ON\_ERROR value for a pipe

For a pipe, `ON_ERROR = CONTINUE` also changes how files that contain errors are reported, because the pipe loads the
valid rows from each file. The following table compares the two values for a file that contains some rows with errors:

| Behavior | `ON_ERROR = SKIP_FILE` (default for pipes) | `ON_ERROR = CONTINUE` |
| --- | --- | --- |
| [Error notifications](/user-guide/data-load-snowpipe-errors#label-snowpipe-errors-what-reported) | Sent for the file. | Sent only if no rows from the file load. |
| Status in the [copy history](/sql-reference/functions/copy_history) | `Load failed`. | `Partially loaded`, or `Load failed` if no rows from the file load. |
| [Snowpipe events](/user-guide/data-load-snowpipe-monitor-events) | A `FAILED` event. | A `FAILED` event only if no rows from the file load. |
| How you load the rejected rows | Load the file again. | Correct the rows and insert them from the error table. |

Expand

Show lessSee more

Choose the value as follows:

- Keep `ON_ERROR = SKIP_FILE` if you rely on error notifications, the `Load failed` status, or `FAILED` events to
  report every file that contains an error, or if the target table must never contain part of a file.
- Use `ON_ERROR = CONTINUE` if you want to load the valid rows from each file and keep every rejected row. Then monitor
  the error table instead, for example with an
  [alert](/user-guide/data-load-error-tables-query#label-data-load-error-tables-alert).

To change the `ON_ERROR` value of an existing pipe,
[recreate the pipe](/user-guide/data-load-error-tables-pipes#label-data-load-error-tables-existing-pipes).

## Turn on error logging and add CHECK constraints

To turn on error logging, set the `ERROR_LOGGING` property of the target table to `TRUE`. For example, the following
statement creates an `orders` table with error logging turned on. The CHECK constraint on the `order_status` column
accepts only three values, so a load rejects any row with a different value:

Copy code

```
CREATE TABLE orders (
  order_id NUMBER,
  order_status STRING CONSTRAINT orders_status_check CHECK (order_status IN ('NEW', 'SHIPPED', 'CANCELED'))
)
ERROR_LOGGING = TRUE;
```

For an existing table, run `ALTER TABLE orders SET ERROR_LOGGING = TRUE`. For more information, see
[Introduction to error logging](/user-guide/data-engineering/error-logging).

Keep the following points in mind:

- A CHECK constraint accepts a row when its condition evaluates to `NULL`, so a row with no `order_status` value is
  loaded unless the column is also `NOT NULL`.
- On a Snowflake-managed Iceberg table, a CHECK constraint makes writes from external engines fail. For more
  information, see [Overview of constraints](/sql-reference/constraints-overview).
- Error logging records errors only from loads that run after you turn it on. To find the files from which earlier loads
  rejected rows, check the [copy history](/sql-reference/functions/copy_history) for files with the `Load failed` or
  `Partially loaded` status.

## Load files with ON\_ERROR = CONTINUE

You don’t need to add an error logging option to a `COPY INTO` statement or a pipe definition. To record every rejected
row, however, the load must use `ON_ERROR = CONTINUE`.

If your files have a header line, set the `SKIP_HEADER` file format option, such as
`FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1)`. Otherwise, the load handles the header line of each file as a row of
data, and it either inserts the line or records it in the error table.

If a load rejects every row in a file, the file gets the `Load failed` status, so the next `COPY INTO` statement that
loads from the same path loads the file again and records its errors again. If you run the statement on a schedule,
move these files out of its path, or specify the files to load with the `FILES` or `PATTERN` parameter. If the
statement uses `PURGE = TRUE`, it also removes the files that it loads partially, so the error table might contain the
only copy of the rejected rows.

The following pipe loads JSON files from the `json/` path of the same stage into the `orders` table when new files
arrive:

Copy code

```
CREATE PIPE orders_pipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO orders
    FROM @orders_stage/json/
    FILE_FORMAT = (TYPE = JSON)
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
    ON_ERROR = CONTINUE;
```

The pipe example assumes that `orders_stage` is an external stage and that event notifications are set up for its
storage location, as described in [Automate Snowpipe with cloud event notifications](/user-guide/data-load-snowpipe-auto). If a pipe already loads the table, don’t
replace it with a statement like this one, because the new pipe can skip files or load them twice. Follow
[Record errors from an existing pipe](/user-guide/data-load-error-tables-pipes#label-data-load-error-tables-existing-pipes) instead.

Don’t load the same path with both a `COPY INTO` statement and a pipe. Snowflake separately tracks the files that each
one loads, so both load the same files, and the rows are loaded twice. For more information, see
[load metadata for Snowpipe](/user-guide/data-load-snowpipe-intro#label-snowpipe-intro-load-metadata).

## Access control requirements

The following table lists the privileges that a role needs to work with the errors from `COPY INTO` and Snowpipe:

| Task | Required privileges |
| --- | --- |
| Turn on or turn off error logging | `OWNERSHIP` on the target table. |
| Record errors in the error table | None. The role that runs `COPY INTO` or owns the pipe doesn’t need additional privileges. |
| Query the error table | - `OWNERSHIP`, or both `SELECT` and `SELECT ERROR TABLE`, on the target table. - If a [masking policy](/user-guide/security-column-intro), a row access policy, or a projection policy is set directly   on the target table or on its columns, also the global `READ UNREDACTED ERROR TABLE` privilege, which must be granted   by the `ACCOUNTADMIN` role. Without this privilege, the query fails. Masking policies that are assigned through tags   don’t require this privilege, so any role that can query the error table sees the original values of the columns that   these policies mask. For more information, see   [Global privileges (account privileges)](/user-guide/security-access-control-privileges#label-global-privileges). |
| Query the error table from an alert, a task, or a view | The role that owns the alert, the task, or the view needs the privileges to query the error table. |
| Pause and resume the pipes that load the table | `OPERATE` or `OWNERSHIP` on each pipe. To pause or resume all of the pipes in a schema with `ALTER SCHEMA`, `MODIFY` on the schema. |
| Suspend and resume the tasks that load the table | `OPERATE` or `OWNERSHIP` on each task. For more information, see [ALTER TASK](/sql-reference/sql/alter-task). |
| List the files that a pipe skipped with the `COPY_HISTORY` table function | The privileges that [COPY\_HISTORY](/sql-reference/functions/copy_history) requires, and `MONITOR` or `OWNERSHIP` on the pipe. Without either privilege, the `pipe_name` column is `NULL`. |
| List the files that a pipe skipped with the `COPY_HISTORY` view | Access to the ACCOUNT\_USAGE schema. For more information, see [Enabling other roles to use schemas in the SNOWFLAKE database](/sql-reference/account-usage#label-enabling-usage-for-other-roles). |
| Load skipped files again | The privileges to run `COPY INTO` for the target table and the stage. |
| Insert corrected rows from the error table | The privileges to query the error table, and `INSERT` on the target table. |
| Clear the error table | `OWNERSHIP` or `TRUNCATE` on the target table. The `SELECT ERROR TABLE` privilege isn’t enough. The `TRUNCATE` privilege also allows a role to run `TRUNCATE TABLE` on the target table, which deletes its rows and its load metadata. |

Expand

Show lessSee more

For example, if the `load_monitor` role has the `USAGE` privilege on the database, the schema, and a warehouse, the
following statements let it query the error table of the `orders` table:

Copy code

```
GRANT SELECT ON TABLE orders TO ROLE load_monitor;
GRANT SELECT ERROR TABLE ON TABLE orders TO ROLE load_monitor;
```

Granting `ALL` privileges on a table also grants the `SELECT ERROR TABLE` privilege, including when you grant the
privileges on all tables or on future tables in a schema or database. For the privileges that apply to every source of
errors, see [Access control requirements for error tables](/user-guide/data-engineering/error-tables#label-dml-error-logging-access-control-error-tables).

The error table stores the complete source record for each rejected row, including values for columns that have a
masking policy on the target table and fields that the load doesn’t insert into the table. Error messages can also
contain values from the record. Grant the
`SELECT ERROR TABLE` privilege only to roles that are allowed to see the source data. A view on the error table uses
the privileges of the view owner, so any role that can query the view can see the errors.

## Cost considerations

Snowflake doesn’t remove errors from the error table automatically. Snowflake charges for data stored in the error
table at the standard storage rate, the same as any other table. To see how much storage an error table uses, query
the [TABLE\_STORAGE\_METRICS view](/sql-reference/account-usage/table_storage_metrics). To remove errors, clear the error table, as described in
[Clear the error table and resume loads](/user-guide/data-load-error-tables-reload#label-data-load-error-tables-clear).

Snowpipe bills for the bytes that it scans in each source file, including the bytes in rows that it rejects.
Recording errors in the error table doesn’t add Snowpipe charges. For more information, see
[Snowpipe costs](/user-guide/data-load-snowpipe-billing).

## Usage notes

- If the [OPT\_OUT\_ERROR\_LOGGING](/sql-reference/parameters#label-opt-out-error-logging) parameter is set to `TRUE` for a session, `COPY INTO` statements in the
  session don’t record errors in the error table. Pipes stop recording errors only if you set the parameter for the
  account, which stops error logging for every Snowpipe pipe in the account. Unlike turning off error logging, the
  parameter doesn’t drop the error table. For more information, see
  [Prevent or limit error logging](/user-guide/data-engineering/error-logging#label-error-logging-prevent).
- If you turn off error logging for a table, drop the table, or replace the table with `CREATE OR REPLACE TABLE`,
  Snowflake drops the error table and the errors in it. To keep the errors, copy them to another table first. To keep
  recording errors after `CREATE OR REPLACE TABLE`, include `ERROR_LOGGING = TRUE` in the statement. If you restore a
  dropped table with [UNDROP TABLE](/sql-reference/sql/undrop-table), its errors are restored too. Errors that you remove with
  `TRUNCATE`, or that are dropped when you turn off error logging, can’t be recovered. For more information, see
  [Error table lifecycle](/user-guide/data-engineering/error-tables#label-error-logging-error-table-lifecycle).
- When you clone a table that has error logging turned on, the errors aren’t cloned. The clone has an empty error
  table.
- To find every table that has error logging turned on, see
  [Find and monitor tables that have error logging turned on](/user-guide/data-engineering/error-logging#label-error-logging-find-tables).
- When you replicate a database, its error tables and the errors in them are replicated with it, so the source records
  in the errors are copied to every account that the database is replicated to. If the source records must not leave
  the account, clear the error tables before each refresh, or don’t turn on error logging for those tables. Before
  you clear an error table, stop the loads and statements that write to its target table, as described in
  [Stop loads into the table](/user-guide/data-load-error-tables-reload#label-data-load-error-tables-stop-loads). For more information, see
  [Replicated database objects](/user-guide/account-replication-intro#label-replicated-database-objects).

## Limitations

- Error tables record errors only in individual rows. They don’t record problems that prevent a file from being read,
  such as a stage or file that Snowflake can’t access. They also don’t record problems with a pipe, such as
  configuration or event notification issues. To find these problems, use [COPY\_HISTORY](/sql-reference/functions/copy_history),
  [Snowpipe error notifications](/user-guide/data-load-snowpipe-errors), or
  [Snowpipe events](/user-guide/data-load-snowpipe-monitor-events).
- Error logging for `COPY INTO` and Snowpipe supports only CSV, JSON, and Parquet files, and only the `CONTINUE` and
  `SKIP_FILE` values of `ON_ERROR`. For more information, see [Which errors are recorded](#label-data-load-error-tables-on-error).
- Error tables record only the rows that a load rejects. Copy options that load a row instead of rejecting it, such as
  `ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE` and `TRUNCATECOLUMNS = TRUE`, change which rows are recorded.
- In some cases, such as loads that use `SELECT DISTINCT`, loads into clustered tables, and CSV loads into a table that
  has a stream, the `ON_ERROR` copy option might not work as expected, so the error table might not record every
  rejected row. For the full list, see the
  [usage notes for COPY INTO](/sql-reference/sql/copy-into-table#label-copy-into-table-usage-notes).
- Large Parquet records might be shortened. For more information, see
  [Error data](/user-guide/data-load-error-tables-query#label-data-load-error-tables-error-data).
- Loads into Iceberg tables that use `LOAD_MODE = ADD_FILES_COPY` don’t record errors in the error table. To record
  errors, use the default, `LOAD_MODE = FULL_INGEST`.
- Hybrid tables don’t support error logging. For a hybrid table, `COPY INTO` supports only
  `ON_ERROR = ABORT_STATEMENT`, so a row that violates a CHECK constraint causes the load to fail.
- You can’t add CHECK constraints to a table that any pipe loads, or drop or change them on a table that a Snowpipe pipe
  loads, even if the pipe is paused. For the steps to change them, see
  [Change the CHECK constraints on a table that a pipe loads](/user-guide/data-load-error-tables-pipes#label-data-load-error-tables-add-check).
