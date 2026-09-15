Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SNAPSHOT\_OPERATION\_HISTORY view — *Deprecated*

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The SNAPSHOT\_OPERATION\_HISTORY view is deprecated. See [BACKUP\_OPERATION\_HISTORY view](/sql-reference/organization-usage/backup_operation_history).

This Organization Usage view provides information on operations performed on snapshots.

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
| START\_TIME | TIMESTAMP\_LTZ | The timestamp at which the snapshot operation started. |
| END\_TIME | TIMESTAMP\_LTZ | The timestamp at which the snapshot operation ended. |
| SNAPSHOT\_SET\_ID | NUMBER | The local snapshot set ID. |
| SNAPSHOT\_ID | VARCHAR | The unique identifier of snapshot being worked on. |
| OPERATION\_TYPE | VARCHAR | Could be either of the below operations:   - CREATE - EXPIRE - RESTORE - ADD\_LEGAL\_HOLD - REMOVE\_LEGAL\_HOLD |
| QUERY\_ID | VARCHAR | Internal system-generated identifier for the SQL statement. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
