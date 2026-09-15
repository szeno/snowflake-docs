Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# VALIDATE\_PIPE\_LOAD

This table function can be used to validate data files processed by [Snowpipe](/user-guide/data-load-snowpipe-intro) within a specified time range. The function returns details about any errors encountered during an attempted data load into Snowflake tables.

Note

This function returns pipe activity within the last 14 days.

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
- If the COPY statement in the pipe description includes a query to further transform the data during the load (i.e. a COPY transformation), then the function currently returns a user error.
- If the specified date range falls outside the last 15 days, an error is returned.

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| ERROR | TEXT | First error in the source file. |
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
