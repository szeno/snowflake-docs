Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$DATABASE\_REFRESH\_HISTORY — *Deprecated*

Deprecated Feature

This function has been deprecated. Use [DATABASE\_REFRESH\_HISTORY](/sql-reference/functions/database_refresh_history) instead.

Returns a JSON object showing the refresh history for a secondary database.

Note

This function returns database refresh activity within the last 14 days.

## Syntax

Copy code

```
SYSTEM$DATABASE_REFRESH_HISTORY( '<secondary_db_name>' )
```

## Arguments

`secondary_db_name`
:   Name of the secondary database. This argument is optional if the secondary database is the active database in the current session.

    Note that the entire name must be enclosed in single quotes.

## Output

The function returns the following elements in a JSON object:

| Column Name | Data Type | Description |
| --- | --- | --- |
| startTimeUTC | NUMBER | Time when the replication operation began. Format is epoch time. |
| endTimeUTC | NUMBER | Time when the replication operation finished, if applicable. Format is epoch time. |
| currentPhase | TEXT | Current replication phase. For the list of phases, see the usage notes. |
| jobUUID | TEXT | Query ID for the secondary database refresh job. |
| copy\_bytes | NUMBER | Number of bytes copied during the replication operation. |
| object\_count | NUMBER | Number of database objects copied during the replication operation. |

Expand

Show lessSee more

## Usage notes

- Only returns results for account administrators (users with the ACCOUNTADMIN role).
- Following is the list of phases in the order processed:
  1. SECONDARY\_UPLOADING\_INVENTORY
  2. PRIMARY\_UPLOADING\_METADATA
  3. PRIMARY\_UPLOADING\_DATA
  4. SECONDARY\_DOWNLOADING\_METADATA
  5. SECONDARY\_DOWNLOADING\_DATA
  6. COMPLETED / FAILED / CANCELED

## Examples

The following example retrieves the refresh history for the `mydb` secondary database. The results are returned in a JSON object:

> Copy code
>
> ```
> SELECT SYSTEM$DATABASE_REFRESH_HISTORY('mydb');
> ```

The following example retrieves the same details as in the previous example, but the results are flattened into relational form:

> Copy code
>
> ```
> SELECT
>     to_timestamp_ltz(value:startTimeUTC::numeric,3) AS "start_time"
>     , to_timestamp_ltz(value:endTimeUTC::numeric,3) AS "end_time"
>     , value:currentPhase::string AS "phase"
>   , value:jobUUID::string AS "query_ID"
>   , value:copy_bytes::integer AS "bytes_transferred"
> FROM TABLE(flatten(INPUT=> PARSE_JSON(SYSTEM$DATABASE_REFRESH_HISTORY('mydb'))));
> ```
