Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SNAPSHOT\_STORAGE\_USAGE view — *Deprecated*

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The SNAPSHOT\_STORAGE\_USAGE view is deprecated. See [BACKUP\_STORAGE\_USAGE view](/sql-reference/account-usage/backup_storage_usage).

This Account Usage view provides information about storage usage for [snapshots](/user-guide/backups).

Note

The same tables might be included in multiple table snapshots, schema snapshots, and database snapshots.
Therefore, the numbers of bytes shown in this view don’t entirely answer questions about how much storage
you can save by deleting a snapshot or a snapshot set. The same data files might be retained as part of
a different snapshot set.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| SNAPSHOT\_SET\_ID | NUMBER | Internal system-generated identifier for the snapshot set. |
| SNAPSHOT\_ID | VARCHAR | Internal system-generated identifier for the snapshot. |
| LOGICAL\_BYTES | NUMBER | Number of bytes created when this snapshot is restored. |
| INCREMENTAL\_BYTES\_FROM\_PREVIOUS\_SNAPSHOT | NUMBER | Number of logical bytes of the micro-partitions that *are* in this snapshot, but *aren’t* in the previous snapshot within the same snapshot set.  For the oldest active snapshot in a snapshot set, this is 0. |
| DECREMENTAL\_BYTES\_FROM\_PREVIOUS\_SNAPSHOT | NUMBER | Number of logical bytes of the micro-partitions that *aren’t* in this snapshot, but *are* in the previous snapshot within the same snapshot set.  For the oldest active snapshot in a snapshot set, this is 0. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
