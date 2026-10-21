Categories:
:   [Table functions](/sql-reference/functions-table)

# ICEBERG\_TABLE\_FILE\_REGISTRATION\_HISTORY

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns information about the Apache Parquet™ files that Snowflake registered or unregistered for a
[Parquet Direct](/user-guide/tables-iceberg-parquet-direct) table, including the status of each operation and any
error message. Use this function to verify that files were registered, and to diagnose files that failed to register.

See also:
:   [ICEBERG\_TABLE\_FILES](/sql-reference/functions/iceberg_table_files) , [SYSTEM$PARQUET\_DIRECT\_AUTO\_REFRESH\_STATUS](/sql-reference/functions/system_parquet_direct_auto_refresh_status) , [Parquet Direct](/user-guide/tables-iceberg-parquet-direct)

## Syntax

Copy code

```
ICEBERG_TABLE_FILE_REGISTRATION_HISTORY(
  TABLE_NAME => '<string>'
  [ , START_TIME => <constant_expr> ]
)
```

## Arguments

**Required:**

`TABLE_NAME => 'string'`
:   The name of the Parquet Direct table.

    If the name is case-sensitive or includes special characters or spaces, enclose it in double quotes within the single
    quotes; for example, `'"My_Table"'`.

**Optional:**

`START_TIME => constant_expr`
:   Timestamp (in TIMESTAMP\_LTZ format) that marks the beginning of the time range for retrieving registration events.
    Snowflake retains registration history for 65 days, so the function doesn’t return events older than 65 days, even if
    you specify an earlier start time.

    Default: All available history (the last 65 days).

## Output

The function returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| OPERATION\_TIME | TIMESTAMP\_LTZ | Time when the registration operation occurred. |
| FILE\_NAME | TEXT | Path of the Parquet file. |
| OPERATION\_STATUS | TEXT | Status of the operation. Valid values: - `REGISTERED_NEW`: The file was registered. - `REGISTERED_UPDATE`: The file was registered again because it changed. - `REGISTER_SKIPPED`: The file was already registered. - `REGISTER_SKIPPED_PATTERN_MISMATCH`: The file path didn’t match the table’s `PATTERN`. - `REGISTER_FAILED`: The file couldn’t be registered. `MESSAGE` contains the reason. - `UNREGISTERED`: The file was removed from the table. - `UNREGISTER_FAILED`: The file couldn’t be removed from the table. `MESSAGE` contains the reason. |
| MESSAGE | TEXT | Message that accompanies the operation status; for example, the reason a file failed to register. |
| FILE\_SIZE | NUMBER | Size of the file, in bytes. |
| ROW\_COUNT | NUMBER | Number of rows in the file. |
| LAST\_MODIFIED | TIMESTAMP\_LTZ | Time when the file was last modified in cloud storage. |

Expand

Show lessSee more

## Usage notes

- This function only works with Parquet Direct tables (tables that use a catalog integration with `TABLE_FORMAT = NONE` or
  `TABLE_FORMAT = HIVE`).
- Snowflake retains file registration history for Parquet Direct tables for 65 days.
- When you call an Information Schema table function, the session must have an Information Schema in use, or the function
  name must be fully qualified. For more information, see [Snowflake Information Schema](/sql-reference/info-schema).
- To call this function, use a role that has any privilege on the table.

## Examples

Retrieve the file registration history for the table `my_parquet_table` for the last day:

Copy code

```
SELECT *
  FROM TABLE(INFORMATION_SCHEMA.ICEBERG_TABLE_FILE_REGISTRATION_HISTORY(
    TABLE_NAME => 'my_db.my_schema.my_parquet_table',
    START_TIME => DATEADD(day, -1, CURRENT_TIMESTAMP())))
  ORDER BY operation_time DESC;
```

Find files that have an error message, which can indicate a failed registration:

Copy code

```
SELECT operation_time, file_name, operation_status, message
  FROM TABLE(INFORMATION_SCHEMA.ICEBERG_TABLE_FILE_REGISTRATION_HISTORY(
    TABLE_NAME => 'my_parquet_table'))
  WHERE message IS NOT NULL AND message <> ''
  ORDER BY operation_time DESC;
```
