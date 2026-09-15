# SNAPSHOT\_SETS view — *Deprecated*

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The SNAPSHOT\_SETS view is deprecated. See [BACKUP\_SETS view](/sql-reference/info-schema/backup_sets).

This Information Schema view provides information on snapshot sets.

## Columns

| Column name | Data type | Description |
| --- | --- | --- |
| SNAPSHOT\_SET\_NAME | VARCHAR | Name of the snapshot set. |
| SNAPSHOT\_SET\_SCHEMA | VARCHAR | Schema that the snapshot set belongs to. |
| SNAPSHOT\_SET\_CATALOG | VARCHAR | Database that the snapshot set belongs to. |
| OBJECT\_KIND | VARCHAR | Type of object that the snapshot set is snapshotting. |
| OBJECT\_NAME | VARCHAR | Name of object that the snapshot set is snapshotting. |
| OBJECT\_SCHEMA | VARCHAR | Name of schema that contains the object being snapshotted by this snapshot set. |
| OBJECT\_CATALOG | VARCHAR | Name of database that contains the object being snapshotted by this snapshot set. |
| SNAPSHOT\_POLICY\_NAME | VARCHAR | Name of snapshot policy attached to this snapshot set. |
| SNAPSHOT\_POLICY\_SCHEMA | VARCHAR | Name of the schema that contains the snapshot policy. |
| SNAPSHOT\_POLICY\_CATALOG | VARCHAR | Name of the database that contains the snapshot policy. |
| OWNER | VARCHAR | Name of the role that owns the snapshot set. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of role that owns the snapshot set. Account role or Database role. |
| CREATED | TIMESTAMP | Date and time when the snapshot set was created. |
| LAST\_ALTERED | TIMESTAMP | Date and time the object was last altered by a DML, DDL, or background metadata operation. See `Usage Notes`\_. |
| COMMENT | VARCHAR | Comment for the snapshot set. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
