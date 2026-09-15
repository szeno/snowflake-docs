Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# STAGE\_STORAGE\_USAGE\_DETAILS view

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only.

This Account Usage view displays information about storage usage for internal named stages, table stages, and user stages
in your account.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| USAGE\_DATE | DATE | Date (in the local time zone) for the storage usage record. We recommend changing your session to use the UTC time zone by using `ALTER SESSION SET TIMEZONE='UTC'`. |
| CATALOG\_NAME | VARCHAR | Database that the stage belongs to. NULL for user stages. |
| CATALOG\_ID | NUMBER | Internal, system-generated identifier for the database that the stage belongs to (NULL for user stages). |
| SCHEMA\_NAME | VARCHAR | Schema that the stage belongs to (NULL for user stages). |
| SCHEMA\_ID | NUMBER | Internal, system-generated identifier for the schema that the stage belongs to (NULL for user stages). |
| ENTITY\_NAME | VARCHAR | Name of the entity, depending on the stage type. For user stages, displays the name of the user that the stage belongs to. For table stages, displays the name of the table that the stage belongs to. For internal named stages, displays the name of the stage. |
| STAGE\_TYPE | VARCHAR | The type of internal stage: `User`, `Internal Named`, or `Table`. |
| ENTITY\_ID | NUMBER | Unique identifier for the entity. For user stages, displays the ID of the user that the stage belongs to. For table stages, displays the ID of the table that the stage belongs to. For internal named stages, displays the ID of the stage. The combination of ENTITY\_ID, STAGE\_TYPE, and USAGE\_DATE forms a composite key. |
| BYTES | NUMBER | Bytes used by the stage. |
| FILE\_COUNT | NUMBER | Number of files on the stage. |
| STAGE\_CREATED | TIMESTAMP\_LTZ | Date and time at which the stage was created. For user stages, this is the time when the user was created. For table stages, this is the time when the table was created. |
| STAGE\_DROPPED | TIMESTAMP\_LTZ | Date and time at which the stage was dropped. NULL if the stage has not been dropped. |
| CATALOG\_CREATED | TIMESTAMP\_LTZ | Date and time at which the database containing the stage was created. NULL for user stages. |
| CATALOG\_DROPPED | TIMESTAMP\_LTZ | Date and time at which the database containing the stage was dropped. NULL for user stages or if the database has not been dropped. |
| SCHEMA\_CREATED | TIMESTAMP\_LTZ | Date and time at which the schema containing the stage was created. NULL for user stages. |
| SCHEMA\_DROPPED | TIMESTAMP\_LTZ | Date and time at which the schema containing the stage was dropped. NULL for user stages or if the schema has not been dropped. |
| COMMENT | VARCHAR | Comment for the stage. Only available for internal named stages, otherwise NULL. |
| MAX\_LAST\_MODIFIED | TIMESTAMP\_LTZ | Most recent file modification timestamp among all files in the stage for the given usage date. |
| MIN\_LAST\_MODIFIED | TIMESTAMP\_LTZ | Oldest file modification timestamp among all files in the stage for the given usage date. |

Expand

Show lessSee more

## Usage notes

- Latency for the view is up to 2 days.
- This view is available for accounts hosted on AWS and Azure. It is not supported on GCP.
- The view contains historical data for the last 90 days. Data accumulation began on the date this feature became generally available.
- The view displays information about named, table, and user stages.
- Snowflake makes a best effort to provide information for all days. However, there might be days
  for which stage usage details aren’t available.
- When you filter by a single USAGE\_DATE value, queries might take several minutes on large warehouses.
  If you need to query this view regularly or want to keep more than 90 days of history, consider using a daily task to materialize one usage day into a separate table.
  For more information, see [Introduction to tasks](/user-guide/tasks-intro).
- The combination of ENTITY\_ID, STAGE\_TYPE, and USAGE\_DATE forms a composite key that uniquely identifies each row.
- User stages are not associated with a database or schema. As a result, the `CATALOG_NAME`, `CATALOG_ID`,
  `SCHEMA_NAME`, and `SCHEMA_ID` columns are NULL for rows where `STAGE_TYPE` is `User`.

## Examples

Return the count of stages grouped by stage type for a specific date:

Copy code

```
SELECT stage_type, COUNT(*) as cnt
FROM snowflake.account_usage.stage_storage_usage_details
WHERE usage_date = '2026-07-29'
GROUP BY stage_type;
```

Return all storage details for internal named stages for a specific date:

Copy code

```
SELECT *
FROM snowflake.account_usage.stage_storage_usage_details
WHERE usage_date = '2026-07-29'
AND stage_type = 'Internal Named';
```

Return the stages consuming the most storage for a specific date:

Copy code

```
SELECT *
FROM snowflake.account_usage.stage_storage_usage_details
WHERE usage_date = '2026-07-29'
ORDER BY bytes DESC;
```
