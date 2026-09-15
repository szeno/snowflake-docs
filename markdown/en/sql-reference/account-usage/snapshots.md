Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SNAPSHOTS view — *Deprecated*

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The SNAPSHOTS view is deprecated. See [BACKUPS view](/sql-reference/account-usage/backups).

This Account Usage view provides information on [snapshots](/user-guide/backups).

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| ID | VARCHAR | Snowflake-generated identifier of the snapshot.  Note: this is not the local ID, this is the globally unique UUID of the Snapshot. |
| SNAPSHOT\_SET\_ID | NUMBER | ID of snapshot set that contains the snapshot. |
| SNAPSHOT\_SET\_NAME | VARCHAR | Name of snapshot set that contains the snapshot. |
| SNAPSHOT\_SET\_SCHEMA\_ID | NUMBER | ID of schema that the snapshot set belongs to. |
| SNAPSHOT\_SET\_SCHEMA | VARCHAR | Name of schema that the snapshot set belongs to. |
| SNAPSHOT\_SET\_CATALOG\_ID | NUMBER | ID of database that the snapshot set belongs to. |
| SNAPSHOT\_SET\_CATALOG | VARCHAR | Name of database that the snapshot set belongs to. |
| CREATED | TIMESTAMP\_LTZ | Timestamp at which snapshot was created. |
| DELETED | TIMESTAMP\_LTZ | Timestamp at which the snapshot was deleted.  This column isn’t displayed by the SHOW command, because the SHOW command output doesn’t include deleted objects. |
| EXPIRATION\_SCHEDULED\_FOR | TIMESTAMP\_LTZ | Timestamp at which snapshot will be expired and deleted. |
| IS\_UNDER\_LEGAL\_HOLD | BOOLEAN | True if snapshot is under legal hold; False otherwise. |
| COMMENT | VARCHAR | Comment for the snapshot. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
