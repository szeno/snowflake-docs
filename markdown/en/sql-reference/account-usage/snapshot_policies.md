Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SNAPSHOT\_POLICIES view — *Deprecated*

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The SNAPSHOT\_POLICIES view is deprecated. See [BACKUP\_POLICIES view](/sql-reference/account-usage/backup_policies).

This Account Usage view provides information about [snapshot policies](/user-guide/backups#label-snapshots-concept-snapshot-policy)
and their properties.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal system-generated identifier for the snapshot policy. |
| NAME | VARCHAR | Name of the snapshot policy. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the snapshot policy. |
| SCHEMA\_NAME | VARCHAR | Schema that the snapshot policy belongs to. |
| CATALOG\_ID | NUMBER | Internal system-generated identifier for the database of the snapshot policy. |
| CATALOG\_NAME | VARCHAR | Database that the snapshot policy belongs to. |
| SCHEDULE | VARCHAR | Schedule for snapshot creation. |
| EXPIRE\_AFTER\_DAYS | NUMBER | Days after snapshot creation when snapshot should be expired and automatically deleted. |
| HAS\_RETENTION\_LOCK | VARCHAR | Indicates whether the policy includes a retention lock. Y if the policy has a retention lock; N otherwise.  Retention lock protects snapshots from being deleted by anyone for the defined retention period. The retention lock also prevents the retention period from being decreased on the policy. |
| OWNER | VARCHAR | Name of the role that owns the snapshot policy. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of role that owns the snapshot policy. Account role or Database role. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the snapshot policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the snapshot policy was deleted. |
| COMMENT | VARCHAR | Comment for the snapshot policy. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
