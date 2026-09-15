Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# BACKUPS view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Backups are available for all Snowflake editions.
- Backups with retention lock and backups with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Organization Usage view provides information on backups.

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
| ID | VARCHAR | Snowflake-generated identifier of the backup.  Note: this is not the local ID, this is the globally unique UUID of the Backup. |
| BACKUP\_SET\_ID | NUMBER | ID of backup set that contains the backup. |
| BACKUP\_SET\_NAME | VARCHAR | Name of backup set that contains the backup. |
| BACKUP\_SET\_SCHEMA\_ID | NUMBER | ID of schema that the backup set belongs to. |
| BACKUP\_SET\_SCHEMA | VARCHAR | Name of schema that the backup set belongs to. |
| BACKUP\_SET\_CATALOG\_ID | NUMBER | ID of database that the backup set belongs to. |
| BACKUP\_SET\_CATALOG | VARCHAR | Name of database that the backup set belongs to. |
| CREATED | TIMESTAMP\_LTZ | Timestamp at which backup was created. |
| DELETED | TIMESTAMP\_LTZ | Timestamp at which backup was deleted. |
| EXPIRATION\_SCHEDULED\_FOR | TIMESTAMP\_LTZ | Timestamp at which backup will be expired. |
| IS\_UNDER\_LEGAL\_HOLD | BOOLEAN | Y if backup is under legal hold; N otherwise. |
| COMMENT | VARCHAR | Comment for the backup. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
