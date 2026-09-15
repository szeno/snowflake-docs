# BACKUPS view

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Information Schema view provides information on backups.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| ID | VARCHAR | Snowflake-generated identifier of the backup.  Note: this is not the local ID, this is the globally unique UUID of the backup. |
| CREATED | TIMESTAMP\_LTZ | Timestamp at which backup was created. |
| BACKUP\_SET\_NAME | VARCHAR | Name of backup set that contains the backup. |
| BACKUP\_SET\_SCHEMA | VARCHAR | Name of schema that the backup set belongs to. |
| BACKUP\_SET\_CATALOG | VARCHAR | Name of database that the backup set belongs to. |
| EXPIRATION\_SCHEDULED\_FOR | TIMESTAMP\_LTZ | Timestamp at which backup will be expired and deleted. |
| IS\_UNDER\_LEGAL\_HOLD | BOOLEAN | Y if backup is under legal hold; N otherwise. |
| COMMENT | VARCHAR | Comment for the backup. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
