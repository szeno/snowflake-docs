Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# BACKUP\_STORAGE\_USAGE view

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view provides information about storage usage for [backups](/user-guide/backups).

Note

The same tables might be included in multiple table backups, schema backups, and database backups.
Therefore, the numbers of bytes shown in this view don’t entirely answer questions about how much storage
you can save by deleting a backup or a backup set. The same data files might be retained as part of
a different backup set.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| BACKUP\_SET\_ID | NUMBER | Internal system-generated identifier for the backup set. |
| BACKUP\_ID | VARCHAR | Internal system-generated identifier for the backup. |
| LOGICAL\_BYTES | NUMBER | Number of bytes created when this backup is restored. |
| INCREMENTAL\_BYTES\_FROM\_PREVIOUS\_BACKUP | NUMBER | Number of logical bytes of the micro-partitions that *are* in this backup, but *aren’t* in the previous backup within the same backup set.  For the oldest active backup in a backup set, this is 0. |
| DECREMENTAL\_BYTES\_FROM\_PREVIOUS\_BACKUP | NUMBER | Number of logical bytes of the micro-partitions that *aren’t* in this backup, but *are* in the previous backup within the same backup set.  For the oldest active backup in a backup set, this is 0. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
