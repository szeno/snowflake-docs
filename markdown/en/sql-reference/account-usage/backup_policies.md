Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# BACKUP\_POLICIES view

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view provides information about [backup policies](/user-guide/backups#label-snapshots-concept-backup-policy)
and their properties.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal system-generated identifier for the backup policy. |
| NAME | VARCHAR | Name of the backup policy. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the backup policy. |
| SCHEMA\_NAME | VARCHAR | Schema that the backup policy belongs to. |
| CATALOG\_ID | NUMBER | Internal system-generated identifier for the database of the backup policy. |
| CATALOG\_NAME | VARCHAR | Database that the backup policy belongs to. |
| SCHEDULE | VARCHAR | Schedule for backup creation. |
| EXPIRE\_AFTER\_DAYS | NUMBER | Days after backup creation when backup should be expired and automatically deleted. |
| HAS\_RETENTION\_LOCK | VARCHAR | Indicates whether the policy includes a retention lock. Y if the policy has a retention lock; N otherwise.  Retention lock protects backups from being deleted by anyone for the defined retention period. The retention lock also prevents the retention period from being decreased on the policy. |
| OWNER | VARCHAR | Name of the role that owns the backup policy. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of role that owns the backup policy. Account role or Database role. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the backup policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the backup policy was deleted. |
| COMMENT | VARCHAR | Comment for the backup policy. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
