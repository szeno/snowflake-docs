Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# BACKUP\_SETS view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Organization Usage view provides information on backup sets.

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
| ID | NUMBER | Internal system-generated identifier for the backup set. |
| NAME | VARCHAR | Name of the backup set |
| SCHEMA\_ID | NUMBER | Internal system-generated identifier for the schema of the backup set. |
| SCHEMA\_NAME | VARCHAR | Schema that the backup set belongs to. |
| CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database of the backup set. |
| CATALOG\_NAME | VARCHAR | Database that the backup set belongs to. |
| OBJECT\_KIND | VARCHAR | Type of object that the backup set backs up. |
| OBJECT\_ID | NUMBER | ID of object that the backup set backs up. |
| OBJECT\_NAME | VARCHAR | Name of object that the backup set backs up. |
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
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the backup set was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the backup set was deleted. |
| COMMENT | VARCHAR | Comment for the backup set. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
