# SNAPSHOTS view — *Deprecated*

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The SNAPSHOTS view is deprecated. See [BACKUPS view](/sql-reference/info-schema/backups).

This Information Schema view provides information on snapshots.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| ID | VARCHAR | Snowflake-generated identifier of the snapshot.  Note: this is not the local ID, this is the globally unique UUID of the Snapshot |
| CREATED | TIMESTAMP\_LTZ | Timestamp at which snapshot was created. |
| SNAPSHOT\_SET\_NAME | VARCHAR | Name of snapshot set that contains the snapshot. |
| SNAPSHOT\_SET\_SCHEMA | VARCHAR | Name of schema that the snapshot set belongs to. |
| SNAPSHOT\_SET\_CATALOG | VARCHAR | Name of database that the snapshot set belongs to. |
| EXPIRATION\_SCHEDULED\_FOR | TIMESTAMP\_LTZ | Timestamp at which snapshot will be expired and deleted. |
| IS\_UNDER\_LEGAL\_HOLD | BOOLEAN | Y if snapshot is under legal hold; N otherwise. |
| COMMENT | VARCHAR | Comment for the snapshot. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
