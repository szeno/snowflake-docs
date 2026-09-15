Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# BACKUP\_SETS view

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view provides information about [backup sets](/user-guide/backups#label-backups-concept-backup-set) and their properties.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal system-generated identifier for the backup set. |
| NAME | VARCHAR | Name of the backup set |
| SCHEMA\_ID | NUMBER | Internal system-generated identifier for the schema of the backup set. |
| SCHEMA\_NAME | VARCHAR | Schema that the backup set belongs to. |
| CATALOG\_ID | NUMBER | Internal system-generated identifier for the database of the backup set. |
| CATALOG\_NAME | VARCHAR | Database that the backup set belongs to. |
| OBJECT\_KIND | VARCHAR | Type of object that the backup set is backing up. |
| OBJECT\_ID | NUMBER | ID of object that the backup set is backing up. |
| OBJECT\_NAME | VARCHAR | Name of object that the backup set is backing up. |
| OBJECT\_SCHEMA\_ID | NUMBER | ID of schema that contains the object that is backed up by this backup set. |
| OBJECT\_SCHEMA\_NAME | VARCHAR | Name of schema that contains the object that is backed up by this backup set. |
| OBJECT\_CATALOG\_ID | NUMBER | ID of database that contains the object that is backed up by this backup set. |
| OBJECT\_CATALOG\_NAME | VARCHAR | Name of database that contains the object that is backed up by this backup set. |
| BACKUP\_POLICY\_ID | NUMBER | ID of backup policy attached to this backup set. |
| BACKUP\_POLICY\_NAME | VARCHAR | Name of backup policy attached to this backup set. |
| BACKUP\_POLICY\_SCHEMA\_ID | NUMBER | ID of the schema that contains the backup policy. |
| BACKUP\_POLICY\_SCHEMA\_NAME | VARCHAR | Name of the schema that contains the backup policy. |
| BACKUP\_POLICY\_CATALOG\_ID | NUMBER | ID of the database that contains the backup policy. |
| BACKUP\_POLICY\_CATALOG\_NAME | VARCHAR | Name of the database that contains the backup policy. |
| OWNER | VARCHAR | Name of the role that owns the backup set. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of role that owns the backup set. Account role or Database role. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the backup set was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the backup set was deleted. |
| COMMENT | VARCHAR | Comment for the backup set. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
