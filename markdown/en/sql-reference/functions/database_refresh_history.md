Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# DATABASE\_REFRESH\_HISTORY

Returns the refresh history for a secondary database.

Note

This function returns database refresh activity within the last 14 days.

See also:
:   [DATABASE\_REFRESH\_PROGRESS , DATABASE\_REFRESH\_PROGRESS\_BY\_JOB](/sql-reference/functions/database_refresh_progress)

## Syntax

Copy code

```
DATABASE_REFRESH_HISTORY( '<secondary_db_name>' )
```

## Arguments

`secondary_db_name`
:   Name of the secondary database. This argument is optional if the secondary database is the active database in the current session.

    Note that the entire name must be enclosed in single quotes.

## Usage notes

- Only returns results for account administrators (users with the ACCOUNTADMIN role).
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).
- Following is the list of phases in the order processed:
  1. SECONDARY\_UPLOADING\_INVENTORY
  2. PRIMARY\_UPLOADING\_METADATA
  3. PRIMARY\_UPLOADING\_DATA
  4. SECONDARY\_DOWNLOADING\_METADATA
  5. SECONDARY\_DOWNLOADING\_DATA
  6. COMPLETED / FAILED / CANCELED

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| CURRENT\_PHASE | TEXT | Current replication phase. For the list of phases, see the usage notes. |
| START\_TIME | NUMBER | Time when the replication operation began. Format is epoch time. |
| END\_TIME | NUMBER | Time when the replication operation finished, if applicable. Format is epoch time. |
| JOB\_UUID | TEXT | Query ID for the secondary database refresh job. |
| COPY\_BYTES | NUMBER | Number of bytes copied during the replication operation. |
| OBJECT\_COUNT | NUMBER | Number of database objects copied during the replication operation. |

Expand

Show lessSee more

## Examples

Retrieve the database refresh history for the database that is currently active in the user session:

> Copy code
>
> ```
> select *
> from table(information_schema.database_refresh_history());
> ```
