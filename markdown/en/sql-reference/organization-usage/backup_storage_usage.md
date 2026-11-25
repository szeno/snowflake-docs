Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# BACKUP\_STORAGE\_USAGE view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Organization Usage view provides information on storage used for backup-related objects.

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
| BACKUP\_SET\_ID | NUMBER | Internal system-generated identifier for the backup set. |
| BACKUP\_ID | VARCHAR | Internal system-generated identifier for the backup. |
| LOGICAL\_BYTES | NUMBER | Number of bytes created when this backup is restored. |
| INCREMENTAL\_BYTES\_FROM\_PREVIOUS\_BACKUP | NUMBER | Number of logical bytes of the micro-partitions that *are* in this backup, but *aren’t* in the previous backup within the same backup set.  For the oldest active backup in a backup set, this is 0. |
| DECREMENTAL\_BYTES\_FROM\_PREVIOUS\_BACKUP | NUMBER | Number of logical bytes of the micro-partitions that *aren’t* in this backup, but *are* in the previous backup within the same backup set.  For the oldest active backup in a backup set, this is 0. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
