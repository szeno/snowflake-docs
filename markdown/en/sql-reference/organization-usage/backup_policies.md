Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# BACKUP\_POLICIES view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Organization Usage view provides information on backup policies.

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
| ID | NUMBER | Internal system-generated identifier for the backup policy. |
| NAME | VARCHAR | Name of the backup policy. |
| SCHEMA\_ID | NUMBER | Internal system-generated identifier for the schema of the backup policy. |
| SCHEMA\_NAME | VARCHAR | Schema that the backup policy belongs to. |
| CATALOG\_ID | NUMBER | Internal system-generated identifier for the database of the backup policy. |
| CATALOG\_NAME | VARCHAR | Database that the backup policy belongs to. |
| SCHEDULE | VARCHAR | Schedule for backup creation. |
| EXPIRE\_AFTER\_DAYS | NUMBER | Days after backup creation when backup should be expired. |
| HAS\_RETENTION\_LOCK | VARCHAR | Indicates whether the policy includes a retention lock. Y if policy has retention lock; N otherwise.  Retention lock protects backups from being deleted by anyone for the defined retention period. The retention lock also prevents the retention period from being decreased on the policy. |
| OWNER | VARCHAR | Name of the role that owns the backup policy. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of role that owns the backup policy. Account role or Database role. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the backup policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the backup policy was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the backup policy was deleted. |
| COMMENT | VARCHAR | Comment for the backup policy. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
