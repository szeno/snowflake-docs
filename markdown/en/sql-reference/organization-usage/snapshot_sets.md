Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SNAPSHOT\_SETS view — *Deprecated*

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The SNAPSHOT\_SETS view is deprecated. See [BACKUP\_SETS view](/sql-reference/organization-usage/backup_sets).

This Organization Usage view provides information on snapshot sets.

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column name | Data type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal system-generated identifier for the snapshot set. |
| NAME | VARCHAR | Name of the snapshot set. |
| SCHEMA\_ID | NUMBER | Internal system-generated identifier for the schema of the snapshot set. |
| SCHEMA\_NAME | VARCHAR | Schema that the snapshot set belongs to. |
| CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database of the snapshot set. |
| CATALOG\_NAME | VARCHAR | Database that the snapshot set belongs to. |
| OBJECT\_KIND | VARCHAR | Type of object that the snapshot set is snapshotting. |
| OBJECT\_ID | NUMBER | ID of object that the snapshot set is snapshotting. |
| OBJECT\_NAME | VARCHAR | Name of object that the snapshot set is snapshotting. |
| OBJECT\_SCHEMA\_ID | NUMBER | ID of schema that contains the object being snapshotted by this snapshot set. |
| OBJECT\_SCHEMA\_NAME | VARCHAR | Name of schema that contains the object being snapshotted by this snapshot set. |
| OBJECT\_CATALOG\_ID | NUMBER | ID of database that contains the object being snapshotted by this snapshot set. |
| OBJECT\_CATALOG\_NAME | VARCHAR | Name of database that contains the object being snapshotted by this snapshot set. |
| SNAPSHOT\_POLICY\_ID | NUMBER | ID of snapshot policy attached to this snapshot set. |
| SNAPSHOT\_POLICY\_NAME | VARCHAR | Name of snapshot policy attached to this snapshot set. |
| SNAPSHOT\_POLICY\_SCHEMA\_ID | NUMBER | ID of the schema that contains the snapshot policy. |
| SNAPSHOT\_POLICY\_SCHEMA\_NAME | VARCHAR | Name of the schema that contains the snapshot policy. |
| SNAPSHOT\_POLICY\_CATALOG\_ID | NUMBER | ID of the database that contains the snapshot policy. |
| SNAPSHOT\_POLICY\_CATALOG\_NAME | VARCHAR | Name of the database that contains the snapshot policy. |
| OWNER | VARCHAR | Name of the role that owns the snapshot set. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of role that owns the snapshot set. Account role or Database role. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the snapshot set was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the snapshot set was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the snapshot set was deleted. |
| COMMENT | VARCHAR | Comment for the snapshot set. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
