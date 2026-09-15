Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# COPY\_HISTORY

This table function can be used to query Snowflake data loading history along various dimensions within the last 14 days.
The function returns load activity for both [COPY INTO <table>](/sql-reference/sql/copy-into-table) statements and
continuous data loading using [Snowpipe](/user-guide/data-load-snowpipe-intro). The table function avoids the 10,000 row limitation
of the [LOAD\_HISTORY view](/sql-reference/info-schema/load_history). The results can be filtered using SQL predicates.

You can also view data loading details in Snowsight. See [Monitor data loading activity by using Copy History](/user-guide/data-load-monitor).

## Syntax

Copy code

```
COPY_HISTORY(
      TABLE_NAME => '<string>'
       , START_TIME => <constant_expr>
      [, END_TIME => <constant_expr> ]
      [, PIPE_NAME => '<string>' ] )
```

## Arguments

**Required:**

`TABLE_NAME => 'string'`
:   A string specifying a table name.

`START_TIME => constant_expr`
:   Timestamp (in TIMESTAMP\_LTZ format), within the last 14 days, marking the start of the time range for retrieving load events.

**Optional:**

`END_TIME => constant_expr`
:   Timestamp (in TIMESTAMP\_LTZ format), within the last 14 days, marking the end of the time range for retrieving load events.

    Default: [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp).

`PIPE_NAME => 'string'`
:   A string specifying a pipe name.

## Usage notes

- For bulk data loads, this function returns results for a role that has MONITOR privilege on your Snowflake account,
  or a role with USAGE privilege on schema and database and any privilege on table.
- For Snowpipe data loads, this function returns results for a role that has MONITOR privilege on your Snowflake account,
  or a role with USAGE privilege on schema and database that contains the pipe and any privilege on table.
  In addition, if MONITOR on pipe is not available, pipe name, pipe table name, pipe schema name and pipe catalog name are masked as NULL.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).
- This view returns a limit of 14 days of copy history. To avoid this limitation, use the [COPY\_HISTORY view](/sql-reference/account-usage/copy_history) (Account Usage).
- The function only includes COPY INTO commands that executed to completion, with or without errors.
- Dropping or recreating a table object removes the historical data for bulk data loads (COPY INTO *<table>* statements) into the table.
- Dropping or recreating a pipe object removes the historical data for Snowpipe data loads using the pipe.

- The COPY\_HISTORY view shows copy history only after the latest truncate operation on the target table. This applies to the COPY\_HISTORY views before and after
  [replication](/user-guide/account-replication-intro).

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| FILE\_NAME | TEXT | Name of the source file and relative path to the file. |
| STAGE\_LOCATION | TEXT | Name of the stage where the source file is located. |
| LAST\_LOAD\_TIME | TIMESTAMP\_LTZ | Date and time of when the file finished loading. |
| ROW\_COUNT | NUMBER | Number of rows loaded from the source file. |
| ROW\_PARSED | NUMBER | Number of rows parsed from the source file; `NULL` if STATUS is `Load in progress`. |
| FILE\_SIZE | NUMBER | Size of the source file loaded (in bytes). |
| FIRST\_ERROR\_MESSAGE | TEXT | First error of the source file. |
| FIRST\_ERROR\_LINE\_NUMBER | NUMBER | Line number of the first error. |
| FIRST\_ERROR\_CHARACTER\_POS | NUMBER | Position of the first error character. |
| FIRST\_ERROR\_COLUMN\_NAME | TEXT | Column name of the first error. |
| ERROR\_COUNT | NUMBER | Number of error rows in the source file. |
| ERROR\_LIMIT | NUMBER | If the number of errors reaches this limit, then abort. |
| STATUS | TEXT | Status: `Load in progress`, `Loaded`, `Load failed`, `Partially loaded`, or `Load skipped`. |
| TABLE\_CATALOG\_NAME | TEXT | Name of the database in which the target table resides. |
| TABLE\_SCHEMA\_NAME | TEXT | Name of the schema in which the target table resides. |
| TABLE\_NAME | TEXT | Name of the target table. |
| PIPE\_CATALOG\_NAME | TEXT | Name of the database in which the pipe resides. |
| PIPE\_SCHEMA\_NAME | TEXT | Name of the schema in which the pipe resides. |
| PIPE\_NAME | TEXT | Name of the pipe defining the load parameters; `NULL` for COPY statement loads. |
| PIPE\_RECEIVED\_TIME | TIMESTAMP\_LTZ | Date and time when the INSERT request for the file loaded through the pipe was received; `NULL` for COPY statement loads. |
| BYTES\_BILLED | NUMBER | Represents the number of bytes Snowpipe uses for billing purposes, providing visibility into Snowpipe’s cost implications directly within these history views. |

Expand

Show lessSee more

## Examples

Retrieve details about all loading activity in the last hour:

> Copy code
>
> ```
> select *
> from table(information_schema.copy_history(TABLE_NAME=>'MYTABLE', START_TIME=> DATEADD(hours, -1, CURRENT_TIMESTAMP())));
> ```
