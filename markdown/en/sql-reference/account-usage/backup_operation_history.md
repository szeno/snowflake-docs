Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# BACKUP\_OPERATION\_HISTORY view

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view provides information about the backup operations that were performed for
[backup sets](/user-guide/backups#label-backups-concept-backup-set).
Snowflake returns one row for each operation performed on backups within backup sets over the last year.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The timestamp at which the backup operation started. |
| END\_TIME | TIMESTAMP\_LTZ | The timestamp at which the backup operation ended. |
| BACKUP\_SET\_ID | NUMBER | The local backup set ID. |
| BACKUP\_ID | VARCHAR | The unique identifier of backup being worked on. |
| OPERATION\_TYPE | VARCHAR | Could be one of the below operations:   - CREATE - EXPIRE - RESTORE - ADD\_LEGAL\_HOLD - REMOVE\_LEGAL\_HOLD |
| Query\_ID | VARCHAR | Internal system-generated identifier for the SQL statement. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
- Snowflake retains the history data for 365 days (approximately one year).

## Examples

Use the `QUERY_ID` column to join with `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` and retrieve the
execution status for backup operations. For example, to find failed backup creation operations:

Copy code

```
SELECT
  boh.start_time,
  boh.end_time,
  boh.backup_set_id,
  boh.backup_id,
  boh.operation_type,
  boh.query_id,
  qh.execution_status,
  qh.error_code,
  qh.error_message
FROM SNOWFLAKE.ACCOUNT_USAGE.BACKUP_OPERATION_HISTORY AS boh
JOIN SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY AS qh
  ON boh.query_id = qh.query_id
WHERE boh.operation_type = 'CREATE'
  AND qh.execution_status = 'FAIL'
ORDER BY boh.start_time DESC;
```
