Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# VALIDATE\_PIPE\_LOAD

This table function can be used to validate data files processed by [Snowpipe](/user-guide/data-load-snowpipe-intro) within a specified time range. The function returns details about any errors encountered during an attempted data load into Snowflake tables.

Note

This function returns errors only for files in the pipe’s load history, which covers the last 14 days. For a time range
before the last 14 days, the function returns no results. Recreating a pipe removes its load history, so the function
also returns no results for files that the pipe processed before you recreated it.

## Syntax

Copy code

```
VALIDATE_PIPE_LOAD(
      PIPE_NAME => '<string>'
       , START_TIME => <constant_expr>
      [, END_TIME => <constant_expr> ] )
```

## Arguments

`PIPE_NAME => string`
:   A string specifying a pipe. The function returns results for the specified pipe only.

`START_TIME => constant_expr`
:   Timestamp (in TIMESTAMP\_LTZ format), within the last 14 days, marking the start of the time range for retrieving error events.

**Optional:**

`END_TIME => constant_expr`
:   Timestamp (in TIMESTAMP\_LTZ format), within the last 14 days, marking the end of the time range for retrieving error events.

## Usage notes

- Returns results only for the pipe owner (i.e. the role with the OWNERSHIP privilege on the pipe) or a role with the following minimum permissions:

  | Privilege | Object | Notes |
  | --- | --- | --- |
  | MONITOR | Pipe | Alternatively, the global MONITOR EXECUTION privilege is supported. |
  | USAGE | Stage in the pipe definition | External stages only |
  | READ | Stage in the pipe definition | Internal stages only |
  | SELECT | Table in the pipe definition |  |
  | INSERT | Table in the pipe definition |  |
  | SQL operations on schema objects also require USAGE or any other privilege on the database and schema that contain the object. |  |  |

  Expand

  Show lessSee more
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).
- If Snowpipe encountered no errors while processing data files within the specified time range, the function returns no results.
- If the COPY statement in the pipe definition transforms semi-structured data, such as JSON or Parquet data, during the load (that is, a COPY transformation), or if it uses `MATCH_BY_COLUMN_NAME`, the function returns a user error. The function supports pipes that transform CSV data.
- The function doesn’t return rows that violate CHECK constraints.
- To record every row that a pipe rejects, including rows from pipes that transform data and rows that violate CHECK constraints, turn on error logging for the pipe’s target table and use `ON_ERROR = CONTINUE` in the pipe. To change the `ON_ERROR` value of an existing pipe, [recreate the pipe](/user-guide/data-load-error-tables-pipes#label-data-load-error-tables-existing-pipes). Error logging supports CSV, JSON, and Parquet files. For more information, see [Error logging for COPY INTO and Snowpipe](/user-guide/data-load-error-tables).

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| ERROR | TEXT | Error in the source file. The function returns a row for each error in the file. |
| FILE | TEXT | Name of the source file where the error was encountered. |
| LINE | NUMBER | Number of the line in the source file where the error was encountered. |
| CHARACTER | NUMBER | Position of the character where the error was encountered. |
| BYTE\_OFFSET | NUMBER | Byte offset to the character where the error was encountered. |
| CATEGORY | TEXT | Category of the operation when the error was produced. |
| CODE | NUMBER | ID for the error message displayed in the ERROR column. |
| SQL\_STATE | NUMBER | SQL state code. |
| COLUMN\_NAME | TEXT | Name and order of the column that contained the error. |
| ROW\_NUMBER | NUMBER | Number of the row in the source file where the error was encountered. |
| ROW\_START\_LINE | NUMBER | Number of the first line of the row where the error was encountered. |
| REJECTED\_RECORD | TEXT | Record that contained the error. |

Expand

Show lessSee more

## Examples

Validate any loads for the `mypipe` pipe within the previous hour:

> Copy code
>
> ```
> select * from table(validate_pipe_load(
>   pipe_name=>'MY_DB.PUBLIC.MYPIPE',
>   start_time=>dateadd(hour, -1, current_timestamp())));
> ```
