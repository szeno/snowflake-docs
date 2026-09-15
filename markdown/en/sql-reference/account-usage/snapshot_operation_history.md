Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SNAPSHOT\_OPERATION\_HISTORY view — *Deprecated*

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The SNAPSHOT\_OPERATION\_HISTORY view is deprecated. See [BACKUP\_OPERATION\_HISTORY view](/sql-reference/account-usage/backup_operation_history).

This Account Usage view provides information about the snapshot operations that were performed for
[snapshot sets](/user-guide/backups#label-snapshots-concept-snapshot-set).
Snowflake returns one row for each operation performed on snapshots within snapshot sets over the last year.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The timestamp at which the snapshot operation started. |
| END\_TIME | TIMESTAMP\_LTZ | The timestamp at which the snapshot operation ended. |
| SNAPSHOT\_SET\_ID | NUMBER | The local snapshot set ID. |
| SNAPSHOT\_ID | VARCHAR | The unique identifier of snapshot being worked on. |
| OPERATION\_TYPE | VARCHAR | Could be one of the below operations:   - CREATE - EXPIRE - RESTORE - ADD\_LEGAL\_HOLD - REMOVE\_LEGAL\_HOLD |
| Query\_ID | VARCHAR | Internal system-generated identifier for the SQL statement. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
- Snowflake retains the history data for 365 days (approximately one year).
