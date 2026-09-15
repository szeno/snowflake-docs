Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# DATABASE\_REFRESH\_PROGRESS , DATABASE\_REFRESH\_PROGRESS\_BY\_JOB

The DATABASE\_REFRESH\_PROGRESS family of functions can be used to query the status of a database refresh along various dimensions:

- DATABASE\_REFRESH\_PROGRESS returns a JSON object indicating the current refresh status for a secondary database by name.
- DATABASE\_REFRESH\_PROGRESS\_BY\_JOB returns a JSON object indicating the current refresh status for a secondary database by refresh query.

Each function is optimized for querying along the specified dimension.

Note

- DATABASE\_REFRESH\_PROGRESS only returns the database refresh activity for the most recent database refresh if it occurred within the last
  14 days.
- DATABASE\_REFRESH\_PROGRESS\_BY\_JOB returns database refresh activity within the last 14 days.

See also:
:   [DATABASE\_REFRESH\_HISTORY](/sql-reference/functions/database_refresh_history)

## Syntax

Copy code

```
DATABASE_REFRESH_PROGRESS( '<secondary_db_name>' )

DATABASE_REFRESH_PROGRESS_BY_JOB( '<query_id>' )
```

## Arguments

`secondary_db_name`
:   Name of the secondary database. This argument is optional if the secondary database is the active database in the current session.

    Note that the entire name must be enclosed in single quotes.

`query_id`
:   ID of the database refresh query. The query ID can be obtained from the **History** [![History tab](/static/images/screens/ui-navigation-history-icon.svg)](/static/images/screens/ui-navigation-history-icon.svg) page in the web interface.

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
| PHASE\_NAME | TEXT | Name of the replication phases completed (or in progress) so far. For the list of phases, see the usage notes. |
| RESULT | TEXT | Status of the replication phase. Valid statuses are `EXECUTING`, `SUCCEEDED`, `CANCELLED`, `FAILED`. |
| START\_TIME | NUMBER | Time when the replication phase began. Format is epoch time. |
| END\_TIME | NUMBER | Time when the phase finished, if applicable. Format is epoch time. |
| DETAILS | VARIANT | Returned by the DATABASE\_REFRESH\_PROGRESS function only. A JSON object that provides detailed information for the following phases:   - **Primary uploading data**: The timestamp of the current snapshot of the primary database.   - **Primary uploading data** and **Secondary downloading data**: Total number of bytes in the database refresh as well as the number of bytes copied so far in the phase.   - **Secondary downloading metadata**: The number of tables, table columns, and all database objects (including tables and table columns) in the latest snapshot of the primary database. |

Expand

Show lessSee more

## Examples

Retrieve the current progress of the database refresh for the `mydb1` database:

> Copy code
>
> ```
> select *
> from table(information_schema.database_refresh_progress(mydb1));
> ```

Retrieve the current progress of a database refresh by query ID:

> Copy code
>
> ```
> select *
> from table(information_schema.database_refresh_progress_by_job('012a3b45-1234-a12b-0000-1aa200012345'));
> ```
