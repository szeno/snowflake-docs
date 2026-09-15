# BACKUP\_SETS view

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Information Schema view provides information on backup sets.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| BACKUP\_SET\_NAME | VARCHAR | Name of the backup set. |
| BACKUP\_SET\_SCHEMA | VARCHAR | Schema that the backup set belongs to. |
| BACKUP\_SET\_CATALOG | VARCHAR | Database that the backup set belongs to. |
| OBJECT\_KIND | VARCHAR | Type of object that the backup set is backing up. |
| OBJECT\_NAME | VARCHAR | Name of object that the backup set is backing up. |
| OBJECT\_SCHEMA | VARCHAR | Name of schema that contains the object that is backed up by this backup set. |
| OBJECT\_CATALOG | VARCHAR | Name of database that contains the object that is backed up by this backup set. |
| BACKUP\_POLICY\_NAME | VARCHAR | Name of backup policy attached to this backup set. |
| BACKUP\_POLICY\_SCHEMA | VARCHAR | Name of the schema that contains the backup policy. |
| BACKUP\_POLICY\_CATALOG | VARCHAR | Name of the database that contains the backup policy. |
| OWNER | VARCHAR | Name of the role that owns the backup set. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of role that owns the backup set. Account role or Database role. |
| CREATED | TIMESTAMP | Date and time when the backup set was created. |
| LAST\_ALTERED | TIMESTAMP | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| COMMENT | VARCHAR | Comment for the backup set. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
