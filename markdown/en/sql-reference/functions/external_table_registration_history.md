Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# EXTERNAL\_TABLE\_FILE\_REGISTRATION\_HISTORY

This table function can be used to query information about the metadata history for an external table, including:

- Files added or removed automatically as part of a metadata refresh.
- Any errors found when refreshing the metadata.

## Syntax

Copy code

```
EXTERNAL_TABLE_FILE_REGISTRATION_HISTORY (
      TABLE_NAME => '<string>'
      [, START_TIME => <constant_expr> ] )
```

## Arguments

**Required:**

`TABLE_NAME => 'string'`
:   A string specifying an external table name.

**Optional:**

`START_TIME => constant_expr`
:   Timestamp (in TIMESTAMP\_LTZ format), within the last 30 days, marking the start of the time range for retrieving metadata update events.

    Note

    - If no start time is specified, the function returns all update events within the last 30 days.
    - If the start time falls outside the last 30 days, the function returns results within the last 30 days.
    - If the start time is not a timestamp, it is ignored.

## Usage notes

- Returns results for the external table owner (i.e. the role with the OWNERSHIP privilege on the external table), or a higher role,
  or a role that has the USAGE privilege on the database and schema that contain an external table and any privilege on the external
  table.
- The table function cannot retrieve metadata about staged data files until the external table is refreshed (i.e. synched) to include the data files in its metadata.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| JOB\_CREATED\_TIME | TIMESTAMP\_LTZ | Timestamp when the operation occurred |
| FILE\_NAME | TEXT | Name of the staged source file and relative path to the file |
| OPERATION\_STATUS | TEXT | Status: REGISTERED\_NEW, REGISTERED\_UPDATE, REGISTER\_SKIPPED, REGISTER\_FAILED, UNREGISTERED, or UNREGISTER\_FAILED |
| MESSAGE | TEXT | Message accompanying the operation status |
| FILE\_SIZE | NUMBER | Size of the file (in bytes) added to the external table |
| LAST\_MODIFIED | TIMESTAMP\_LTZ | Timestamp when the file was last updated in the stage |

Expand

Show lessSee more

## Examples

Retrieve the metadata stored for all data files referenced by the `mytable` external table:

> Copy code
>
> ```
> select *
> from table(information_schema.external_table_file_registration_history(TABLE_NAME=>'MYTABLE'));
> ```

Retrieve the registration events for external table `mydb.public.external_table_name` that started within the last hour:

> Copy code
>
> ```
> select *
>   from table(information_schema.external_table_file_registration_history(
>     start_time=>dateadd('hour',-1,current_timestamp()),
>     table_name=>'mydb.public.external_table_name'));
> ```

Retrieve the registration events for external table `mydb.public.external_table_name` starting at midnight on April 25, 2022:

> Copy code
>
> ```
> select *
>   from table(information_schema.external_table_file_registration_history(
>     start_time=>cast('2022-04-25' as timestamp),
>     table_name=>'mydb.public.external_table_name'));
> ```
