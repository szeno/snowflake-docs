Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# STAGE\_DIRECTORY\_FILE\_REGISTRATION\_HISTORY

This table function can be used to query information about the metadata history for a directory table, including:

- Files added or removed automatically as part of a metadata refresh.
- Any errors found when refreshing the metadata.

## Syntax

Copy code

```
STAGE_DIRECTORY_FILE_REGISTRATION_HISTORY (
      STAGE_NAME => '<string>'
      [, START_TIME => <constant_expr> ] )
```

## Arguments

**Required:**

`STAGE_NAME => 'string'`
:   A string specifying the name of a stage that has a directory table.

**Optional:**

`START_TIME => constant_expr`
:   Timestamp (in TIMESTAMP\_LTZ format), within the last 14 days, marking the start of the time range for retrieving metadata update events.

    Note

    - If no start time is specified, the function returns all update events within the last 14 days.
    - If the start time falls outside the last 14 days, the function returns empty results.

## Usage notes

- Returns results for the stage owner (i.e. the role with the OWNERSHIP privilege on the stage), or a higher role,
  or a role that has the USAGE privilege on the database and schema that contain a stage with a directory
  table and any privilege on the stage.
- The table function cannot retrieve metadata about staged data files until the directory table is refreshed
  (i.e. synched) to include the data files in its metadata.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in
  use or the function name must be fully-qualified. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| JOB\_CREATED\_TIME | TIMESTAMP\_LTZ | Timestamp when the operation occurred. |
| FILE\_NAME | TEXT | Name of the staged source file and relative path to the file. |
| OPERATION\_STATUS | TEXT | Status: REGISTERED\_NEW, REGISTERED\_UPDATE, REGISTER\_SKIPPED, REGISTER\_FAILED, UNREGISTERED, or UNREGISTER\_FAILED. |
| MESSAGE | TEXT | Message accompanying the operation status. |
| FILE\_SIZE | NUMBER | Size of the file (in bytes) added to the directory table. |
| LAST\_MODIFIED | TIMESTAMP\_LTZ | Timestamp when the file was last updated in the stage. |

Expand

Show lessSee more

## Examples

Retrieve the metadata stored for all data files referenced by the `mystage` stage:

> Copy code
>
> ```
> SELECT *
>   FROM TABLE(information_schema.stage_directory_file_registration_history(
>   STAGE_NAME=>'MYSTAGE'));
> ```

Retrieve the registration events for the directory table on the `mydb.public.mystage` stage that started within the last hour:

> Copy code
>
> ```
> SELECT *
>   FROM TABLE(information_schema.stage_directory_file_registration_history(
>     START_TIME=>DATEADD('hour',-1,current_timestamp()),
>     STAGE_NAME=>'mydb.public.mystage'));
> ```
