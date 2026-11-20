# Query load errors

When error logging is turned on for a table, `COPY INTO` and Snowpipe record the rows that they reject in the table’s
error table, as described in [Which errors are recorded](/user-guide/data-load-error-tables#label-data-load-error-tables-on-error). Query the
error table to find out why rows were rejected and to monitor your loads for new errors. To correct the rejected rows
and load them again, see [Correct and reload rejected rows](/user-guide/data-load-error-tables-reload). For the privileges that you need to query the
error table, see [Access control requirements](/user-guide/data-load-error-tables#label-data-load-error-tables-access-control).

The examples on this page use the `orders` table from
[Turn on error logging and add CHECK constraints](/user-guide/data-load-error-tables#label-data-load-error-tables-turn-on) and the `orders_pipe` pipe from
[Load files with ON\_ERROR = CONTINUE](/user-guide/data-load-error-tables#label-data-load-error-tables-load-files).

## Query the error table

To query an error table, use the `ERROR_TABLE` table function with the name of the target table. To see only the
errors from file loads, filter on the `error_metadata:service` field, which is `copy` for `COPY INTO` and `snowpipe`
for Snowpipe:

Copy code

```
SELECT *
  FROM ERROR_TABLE(orders)
  WHERE error_metadata:service IN ('copy', 'snowpipe')
  ORDER BY timestamp DESC;
```

To see the errors from the `COPY INTO` statement that you just ran in the same session, filter on its query ID:

Copy code

```
SELECT *
  FROM ERROR_TABLE(orders)
  WHERE query_id = LAST_QUERY_ID();
```

If the `COPY INTO` statement ran in another session, such as in a scheduled task, find its query ID in the error
table. All of the errors from one `COPY INTO` statement have the same `query_id` and `timestamp` values:

Copy code

```
SELECT query_id, timestamp, COUNT(*) AS error_count
  FROM ERROR_TABLE(orders)
  WHERE error_metadata:service = 'copy'
  GROUP BY query_id, timestamp
  ORDER BY timestamp DESC;
```

The following query returns the errors from `COPY INTO` statements that started in the past hour, with the file and
the record that caused each error. Don’t use a time window for errors from Snowpipe, because their `timestamp` value
can be earlier than the time when the error was recorded. Filter on the `pipe_name` field instead, as the comment in
the query shows:

Copy code

```
SELECT
    timestamp,
    error_metadata:service::STRING AS service,
    error_metadata:details:pipe_name::STRING AS pipe_name,
    error_metadata:details:file_name::STRING AS file_name,
    error_metadata:details:row_number::NUMBER AS record_number,
    error_code,
    error_metadata:error_message::STRING AS error_message,
    COALESCE(error_data:"$1"::STRING, TO_JSON(error_data)) AS source_record
  FROM ERROR_TABLE(orders)
  -- For the errors from a pipe, replace both lines of this WHERE clause with:
  -- WHERE error_metadata:details:pipe_name = 'MYDB.MYSCHEMA.ORDERS_PIPE'
  WHERE error_metadata:service = 'copy'
    AND timestamp >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
  ORDER BY timestamp DESC;
```

The `pipe_name` value is the fully qualified name of the pipe, so replace `MYDB.MYSCHEMA` with the database and schema
that contain your pipe. For a description of each field, see [Error table fields for file loads](#label-data-load-error-tables-fields).

To find the files with the most errors and the most common types of error, count the errors by file and error code:

Copy code

```
SELECT
    error_metadata:service::STRING AS service,
    error_metadata:details:stage_location::STRING AS stage_location,
    error_metadata:details:file_name::STRING AS file_name,
    error_code,
    ANY_VALUE(error_metadata:error_message::STRING) AS example_error_message,
    COUNT(*) AS error_count
  FROM ERROR_TABLE(orders)
  WHERE error_metadata:service IN ('copy', 'snowpipe')
  GROUP BY ALL
  ORDER BY error_count DESC;
```

## Find rows that violate CHECK constraints

To find CHECK constraint violations, filter on the error code `100320` and on the error message, which names the
constraint and the condition. Other types of errors can also have the code `100320`:

Copy code

```
SELECT
    timestamp,
    error_metadata:service::STRING AS service,
    error_metadata:details:file_name::STRING AS file_name,
    error_metadata:error_message::STRING AS error_message,
    COALESCE(error_data:"$1"::STRING, TO_JSON(error_data)) AS source_record
  FROM ERROR_TABLE(orders)
  WHERE error_metadata:service IN ('copy', 'snowpipe')
    AND error_code = 100320
    AND error_metadata:error_message::STRING ILIKE '%CHECK constraint%'
  ORDER BY timestamp DESC;
```

To also return violations from DML statements, such as an `INSERT` statement that loads corrected rows, remove the
condition on the `service` field.

## Process new errors with a stream

To process new errors as they arrive, create a stream on a view of the error table. The view uses the privileges of its
owner, so grant access to the view and the stream only to roles that are allowed to see the source data. For example,
the following statements create a view on the error table of the `orders` table and a stream on the view, and then query
the new errors:

Copy code

```
CREATE VIEW orders_errors_view AS
  SELECT timestamp, query_id, error_code, error_metadata, error_data
    FROM ERROR_TABLE(mydb.myschema.orders);

CREATE STREAM orders_errors_stream ON VIEW orders_errors_view;

SELECT *
  FROM orders_errors_stream
  WHERE METADATA$ACTION = 'INSERT';
```

Process only the rows where `METADATA$ACTION` is `INSERT`, because clearing the error table adds a `DELETE` row for each
error. Consume the stream before you clear the error table, or the stream misses the errors that you clear. To consume
the stream, use it in a DML statement, as described in
[Streams on error tables](/user-guide/data-engineering/error-tables#label-dml-error-logging-streams). If you replace the view, or if the error
table is dropped, for example because you turned off error logging or replaced the table with `CREATE OR REPLACE TABLE`,
create the view and the stream again.

## Get notified about errors

To find out when the error table contains errors, create an [alert](/user-guide/alerts) that checks the error table on
a schedule.

You need an [email notification integration](/user-guide/notifications/email-notifications), such as `my_email_int` in
the following example, and a role that can [create alerts](/user-guide/alerts#label-alerts-privileges-granting). The
email address must belong to a user in the account and be
[verified](/user-guide/notifications/email-notifications#label-email-notification-verify-address). The role that owns
the alert needs the `USAGE` privilege on the integration and the
[privileges to query the error table](/user-guide/data-load-error-tables#label-data-load-error-tables-access-control).
Without the privileges to query the error table, the condition fails, and the alert doesn’t send the email. To find
these failures, check the [alert history](/sql-reference/functions/alert_history) for the `CONDITION_FAILED` state.

For example, the following alert sends an email every hour while the error table contains errors from `COPY INTO` or
Snowpipe:

Copy code

```
CREATE ALERT orders_load_errors_alert
  WAREHOUSE = my_alert_wh
  SCHEDULE = '60 MINUTE'
  IF (EXISTS (
    SELECT 1
      FROM ERROR_TABLE(orders)
      WHERE error_metadata:service IN ('copy', 'snowpipe')
  ))
  THEN
    CALL SYSTEM$SEND_EMAIL(
      'my_email_int',
      'first.last@example.com',
      'The orders table has rejected rows',
      'Query ERROR_TABLE(orders) to see the rows that loads rejected.');

ALTER ALERT orders_load_errors_alert RESUME;
```

The alert sends the email each time that it runs until you clear the error table. To be notified only about new errors,
check a [stream on a view of the error table](#label-data-load-error-tables-stream) in the alert condition instead. In
the alert action, consume the stream before you send the email, such as with an `INSERT` statement that copies the
stream’s rows to another table.

Error messages and source records can contain sensitive data, so don’t include them in the email.

## Troubleshoot missing errors

If the error table doesn’t contain the errors from a load that rejected rows, check the following:

- Error logging was turned on for the target table before the load ran. If a pipe already loaded the table, the pipe
  can take up to 15 minutes to start recording errors after you turn on error logging.
- The load used `ON_ERROR = CONTINUE` or `ON_ERROR = SKIP_FILE`. If you don’t set `ON_ERROR`, `COPY INTO` uses
  `ABORT_STATEMENT`, which records no errors. With `SKIP_FILE`, which is the default for pipes, the error table
  contains only one error for each file that the load skipped, not one for each rejected row.
- The files are CSV, JSON, or Parquet files.
- The [OPT\_OUT\_ERROR\_LOGGING](/sql-reference/parameters#label-opt-out-error-logging) parameter isn’t `TRUE`:
  - For a `COPY INTO` statement, check the value in the session that ran the statement. The session can inherit the
    value from the user or the account.
  - For a pipe, check the value for the account. Values that are set for a user or a session don’t affect pipes.
- The `COPY INTO` statement didn’t run in a transaction that was rolled back. Errors that a statement records are
  rolled back with the transaction.
- Nobody cleared the error table, turned error logging off and on again, or replaced the table with
  `CREATE OR REPLACE TABLE` after the load.
- Your query doesn’t filter errors from a pipe by query ID or by time. For errors from Snowpipe, the `query_id` value
  is `NULL`, and a time window can miss recent errors. Filter on the `pipe_name` field instead.
- The rows weren’t affected by a limitation of error logging, such as a file that Snowflake couldn’t read or a copy
  option that loads a row instead of rejecting it. For more information, see
  [Limitations](/user-guide/data-load-error-tables#label-data-load-error-tables-limitations).

## Error table fields for file loads

Errors from `COPY INTO` and Snowpipe use the same
[error table columns](/user-guide/data-engineering/error-tables#label-dml-error-logging-error-table-definition)
as errors from DML statements: `timestamp`, `query_id`, `error_code`, `error_metadata`, and `error_data`. For file
loads, the `error_metadata` and `error_data` values contain additional fields, which are described in the following
sections. In these sections, a *record* is one row of data in the source file. In a CSV or JSON file, a record can
span several lines.

For errors from `COPY INTO`, the `query_id` column contains the query ID of the `COPY INTO` statement. For errors from
Snowpipe, the `query_id` column is `NULL`, so use the `pipe_name` field and, if it’s included, the `file_name` field to
identify the load. For errors from `COPY INTO`, the `timestamp` column contains the time when the statement started, so
all of the errors from one statement have the same timestamp. For errors from Snowpipe, the `timestamp` value can be
earlier than the time when the error was recorded, and errors from different loads can have the same value.

### Error metadata

As with errors from DML statements, the `error_metadata` value contains an `error_message` field, which explains why
the record was rejected, and the other fields that are described in
[Error table columns](/user-guide/data-engineering/error-tables#label-dml-error-logging-error-table-definition). The error message can
contain values from the record. To get a field, use a path such as `error_metadata:error_message` or
`error_metadata:details:file_name`.

For file loads, the `error_metadata` value also contains a `service` field:

- `copy`: Errors from `COPY INTO` statements, including statements that tasks and stored procedures run.
- `snowpipe`: Errors from Snowpipe, including loads that start from automated loading, the Snowpipe REST API, or
  `ALTER PIPE ... REFRESH`, and loads by the [classic Kafka connector](/user-guide/kafka-connector/classic/index) when
  it uses Snowpipe to load data.

The `error_metadata` value also contains a `details` object with the following fields:

| Field | Description |
| --- | --- |
| `pipe_name` | The fully qualified name of the pipe, such as `MYDB.MYSCHEMA.ORDERS_PIPE`. This field is included only for errors from Snowpipe. To select the errors from one pipe, compare the full name, such as `error_metadata:details:pipe_name = 'MYDB.MYSCHEMA.ORDERS_PIPE'`. |
| `stage_location` | The stage location that the file was loaded from. To match an error with a file in the [COPY\_HISTORY](/sql-reference/functions/copy_history) output, compare the full path, which is the stage location followed by the file name, because the copy history can split the same path differently. |
| `file_name` | The path of the source file, relative to the stage. |
| `file_format_type` | The type of file format that was used to read the source file, such as `CSV`, `JSON`, or `PARQUET`. |
| `on_error` | The `ON_ERROR` value that the load used: `CONTINUE` or `SKIP_FILE`. For a pipe that doesn’t set `ON_ERROR`, the value is `SKIP_FILE`. |
| `row_number` | The number of the record in the file, starting from 1. Header lines that the `SKIP_HEADER` file format option skips aren’t counted. |
| `row_start_line` | The line in the file where the record starts. |
| `line` | The line in the file where the error occurred, counting every line in the file, including header lines. If a record spans several lines, this value can be greater than the `row_start_line` value. |
| `character` | The position in the line where the error occurred. |
| `byte_offset` | The byte offset where the error occurred, counted from the start of the uncompressed file. |

Expand

Show lessSee more

The `row_start_line`, `line`, `character`, and `byte_offset` fields describe positions in a text file. They’re included
for parsing errors in CSV and JSON files and for conversion errors in CSV files. For other errors, and for Parquet
files, use the `row_number` field, if it’s included, to find the record.

Fields that Snowflake can’t determine for an error are omitted. For example, CHECK constraint violations might not
include the file name, the record number, or the position in the file. Errors in large CSV files that Snowflake reads
in parallel might not include the record number or the position. In these cases, use the source record in the
`error_data:"$1"` field to find the record in the file.

### Error data

For file loads, the `error_data:"$1"` field contains the source record that caused the error:

- For CSV files, the raw text of the record, including quotes and field delimiters, without the record delimiter.
- For JSON files, the text of the JSON record.
- For Parquet files, a JSON representation of the record. The JSON uses the field names from the Parquet file.

The `$1` value is text. To work with a JSON or Parquet record as semi-structured data, parse the value with
[TRY\_PARSE\_JSON](/sql-reference/functions/try_parse_json).

For JSON and Parquet files, the `$1` field usually contains the source record, even if the load uses a
[transformation](/user-guide/data-load-transform). In some cases, the `error_data` value contains the column values
that the load tried to insert instead, the same as for an error from a DML statement.

If Snowflake can’t store the source record, the `$1` field is `NULL` or omitted. If the JSON representation of a
Parquet record is too large to store, Snowflake shortens the value. A shortened value doesn’t contain the complete
record and might not be valid JSON.
