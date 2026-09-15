Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$DATABASE\_REFRESH\_PROGRESS , SYSTEM$DATABASE\_REFRESH\_PROGRESS\_BY\_JOB — *Deprecated*

Deprecated Feature

These functions have been deprecated. Use [DATABASE\_REFRESH\_PROGRESS , DATABASE\_REFRESH\_PROGRESS\_BY\_JOB](/sql-reference/functions/database_refresh_progress) instead.

The SYSTEM$DATABASE\_REFRESH\_PROGRESS family of functions can be used to query the status of a database refresh along various dimensions:

- SYSTEM$DATABASE\_REFRESH\_PROGRESS returns a JSON object indicating the current refresh status for a secondary database by name.
- SYSTEM$DATABASE\_REFRESH\_PROGRESS\_BY\_JOB returns a JSON object indicating the current refresh status for a secondary database by refresh query.

Note

These functions return database refresh activity within the last 14 days.

## Syntax

Copy code

```
SYSTEM$DATABASE_REFRESH_PROGRESS( '<secondary_db_name>' )

SYSTEM$DATABASE_REFRESH_PROGRESS_BY_JOB( '<query_id>' )
```

## Arguments

`secondary_db_name`
:   Name of the secondary database. This argument is optional if the secondary database is the active database in the current session.

    Note that the entire name must be enclosed in single quotes.

`query_id`
:   ID of the database refresh query. The query ID can be obtained from the **History** [![History tab](/static/images/screens/ui-navigation-history-icon.svg)](/static/images/screens/ui-navigation-history-icon.svg) page in the web interface.

## Output

The function returns the following elements in a JSON object:

| Column Name | Data Type | Description |
| --- | --- | --- |
| phaseName | TEXT | Name of the replication phases completed (or in progress) so far. For the list of phases, see the usage notes. |
| resultName | TEXT | Status of the replication phase. |
| startTimeUTC | NUMBER | Time when the replication phase began. Format is epoch time. |
| endTimeUTC | NUMBER | Time when the phase finished, if applicable. Format is epoch time. |
| details | VARIANT | A separate JSON object that shows the total number of bytes in the data refresh as well as the number of bytes copied so far in the phase. If the refresh statement previously failed or was cancelled and was initiated again, the object indicates the number of bytes skipped in the second attempt. The `details` object is included in the `Copying Primary Data` and `Copying Replica Data` phase information. |

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

The following example retrieves the current refresh status for the specified secondary database. The results are returned in a JSON object:

> Copy code
>
> ```
> SELECT SYSTEM$DATABASE_REFRESH_PROGRESS('mydb');
> ```

The following example retrieves the same details as in the previous example, but the results are separated into relational columns and the timestamps are cast as TIMESTAMP\_LTZ:

> Copy code
>
> ```
> SELECT value:phaseName::string AS "Phase",
>   value:resultName::string AS "Result",
>   TO_TIMESTAMP_LTZ(value:startTimeUTC::numeric,3) AS "startTime",
>   TO_TIMESTAMP_LTZ(value:endTimeUTC::numeric,3) AS "endTime",
>   value:details AS "details"
>   FROM table(flatten(INPUT=> PARSE_JSON(SYSTEM$DATABASE_REFRESH_PROGRESS('mydb1'))));
> ```

The following example retrieves the status for the specified database refresh query. The results are returned in a JSON object:

> Copy code
>
> ```
> SELECT SYSTEM$DATABASE_REFRESH_PROGRESS_BY_JOB('4cbd7187-51f6-446c-9814-92d7f57d939b');
> ```

The following example retrieves the same details as in the previous example, but the results are separated into relational columns and the timestamps are cast as TIMESTAMP\_LTZ:

> Copy code
>
> ```
> SELECT value:phaseName::string AS "Phase",
>   value:resultName::string AS "Result",
>   TO_TIMESTAMP_LTZ(value:startTimeUTC::numeric,3) AS "startTime",
>   TO_TIMESTAMP_LTZ(value:endTimeUTC::numeric,3) AS "endTime",
>   value:details AS "details"
>   FROM TABLE(FLATTEN(input=> PARSE_JSON(SYSTEM$DATABASE_REFRESH_PROGRESS_BY_JOB('4cbd7187-51f6-446c-9814-92d7f57d939b'))));
> ```
