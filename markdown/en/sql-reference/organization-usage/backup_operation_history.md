Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# BACKUP\_OPERATION\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Organization Usage view provides information on operations performed on backups.

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column name | Data type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The timestamp at which the backup operation started. |
| END\_TIME | TIMESTAMP\_LTZ | The timestamp at which the backup operation ended. |
| BACKUP\_SET\_ID | NUMBER | The local backup set ID. |
| BACKUP\_ID | VARCHAR | The unique identifier of backup being worked on. |
| OPERATION\_TYPE | VARCHAR | Could be either of the below operations:   - CREATE - EXPIRE - RESTORE - ADD\_LEGAL\_HOLD - REMOVE\_LEGAL\_HOLD |
| QUERY\_ID | VARCHAR | Internal system-generated identifier for the SQL statement. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).

## Examples

Use the `QUERY_ID` column to join with `SNOWFLAKE.ORGANIZATION_USAGE.QUERY_HISTORY` and retrieve
the execution status for backup operations across accounts. For example, to find failed backup
creation operations:

Copy code

```
SELECT
  boh.account_locator,
  boh.account_name,
  boh.start_time,
  boh.end_time,
  boh.backup_set_id,
  boh.backup_id,
  boh.operation_type,
  boh.query_id,
  qh.execution_status,
  qh.error_code,
  qh.error_message
FROM SNOWFLAKE.ORGANIZATION_USAGE.BACKUP_OPERATION_HISTORY AS boh
JOIN SNOWFLAKE.ORGANIZATION_USAGE.QUERY_HISTORY AS qh
  ON boh.account_locator = qh.account_locator
 AND boh.query_id = qh.query_id
WHERE boh.operation_type = 'CREATE'
  AND qh.execution_status = 'FAIL'
ORDER BY boh.start_time DESC;
```
