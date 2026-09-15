Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SNAPSHOT\_POLICIES view — *Deprecated*

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The SNAPSHOT\_POLICIES view is deprecated. See [BACKUP\_POLICIES view](/sql-reference/organization-usage/backup_policies).

This Organization Usage view provides information on snapshot policies.

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
| ID | NUMBER | Internal system-generated identifier for the snapshot policy. |
| NAME | VARCHAR | Name of the snapshot policy. |
| SCHEMA\_ID | NUMBER | Internal system-generated identifier for the schema of the snapshot policy. |
| SCHEMA\_NAME | VARCHAR | Schema that the snapshot policy belongs to. |
| CATALOG\_ID | NUMBER | Internal system-generated identifier for the database of the snapshot policy. |
| CATALOG\_NAME | VARCHAR | Database that the snapshot policy belongs to. |
| SCHEDULE | VARCHAR | Schedule for snapshot creation. |
| EXPIRE\_AFTER\_DAYS | NUMBER | Days after snapshot creation when snapshot should be expired. |
| HAS\_RETENTION\_LOCK | VARCHAR | Indicates whether the policy includes a retention lock. Y if policy has retention lock; N otherwise.  Retention lock protects snapshots from being deleted by anyone for the defined retention period. The retention lock also prevents the retention period from being decreased on the policy. |
| OWNER | VARCHAR | Name of the role that owns the snapshot policy. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of role that owns the snapshot policy. Account role or Database role. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the snapshot policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the snapshot policy was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the snapshot policy was deleted. |
| COMMENT | VARCHAR | Comment for the snapshot policy. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
