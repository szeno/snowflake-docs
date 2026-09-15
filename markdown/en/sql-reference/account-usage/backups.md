Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# BACKUPS view

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view provides information on [backups](/user-guide/backups).

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| ID | VARCHAR | Snowflake-generated identifier of the backup.  Note: this is not the local ID, this is the globally unique UUID of the Backup. |
| BACKUP\_SET\_ID | NUMBER | ID of backup set that contains the backup. |
| BACKUP\_SET\_NAME | VARCHAR | Name of backup set that contains the backup. |
| BACKUP\_SET\_SCHEMA\_ID | NUMBER | ID of schema that the backup set belongs to. |
| BACKUP\_SET\_SCHEMA | VARCHAR | Name of schema that the backup set belongs to. |
| BACKUP\_SET\_CATALOG\_ID | NUMBER | ID of database that the backup set belongs to. |
| BACKUP\_SET\_CATALOG | VARCHAR | Name of database that the backup set belongs to. |
| CREATED | TIMESTAMP\_LTZ | Timestamp at which backup was created. |
| DELETED | TIMESTAMP\_LTZ | Timestamp at which the backup was deleted.  This column isn’t displayed by the SHOW command, because the SHOW command output doesn’t include deleted objects. |
| EXPIRATION\_SCHEDULED\_FOR | TIMESTAMP\_LTZ | Timestamp at which backup will be expired and deleted. |
| IS\_UNDER\_LEGAL\_HOLD | BOOLEAN | True if backup is under legal hold; False otherwise. |
| COMMENT | VARCHAR | Comment for the backup. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
