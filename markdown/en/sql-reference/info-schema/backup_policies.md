# BACKUP\_POLICIES view

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Information Schema view provides information on backup policies.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| BACKUP\_POLICY\_NAME | VARCHAR | Name of the backup policy. |
| BACKUP\_POLICY\_SCHEMA | VARCHAR | Schema that the backup policy belongs to. |
| BACKUP\_POLICY\_CATALOG | VARCHAR | Database that the backup policy belongs to. |
| SCHEDULE | VARCHAR | Schedule for backup creation. |
| EXPIRE\_AFTER\_DAYS | NUMBER | Days after backup creation when backup should be expired and automatically deleted. |
| HAS\_RETENTION\_LOCK | VARCHAR | Indicates whether the policy includes a retention lock. Y if the policy has a retention lock; N otherwise.  Retention lock protects backups from being deleted by anyone for the defined retention period. The retention lock also prevents the retention period from being decreased on the policy. |
| OWNER | VARCHAR | Name of the role that owns the backup policy. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of role that owns the backup policy. Account role or Database role. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the backup policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| COMMENT | VARCHAR | Comment for the backup policy. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
