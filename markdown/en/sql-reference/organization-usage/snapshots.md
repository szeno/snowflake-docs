Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# SNAPSHOTS view — *Deprecated*

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Snapshots are available for all Snowflake editions.
- Snapshots with retention lock and snapshots with legal holds are available for Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Deprecated Feature

The SNAPSHOTS view is deprecated. See [BACKUPS view](/sql-reference/organization-usage/backups).

This Organization Usage view provides information on snapshots.

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
| ID | VARCHAR | Snowflake-generated identifier of the snapshot.  Note: this is not the local ID, this is the globally unique UUID of the Snapshot. |
| SNAPSHOT\_SET\_ID | NUMBER | ID of snapshot set that contains the snapshot. |
| SNAPSHOT\_SET\_NAME | VARCHAR | Name of snapshot set that contains the snapshot. |
| SNAPSHOT\_SET\_SCHEMA\_ID | NUMBER | ID of schema that the snapshot set belongs to. |
| SNAPSHOT\_SET\_SCHEMA | VARCHAR | Name of schema that the snapshot set belongs to. |
| SNAPSHOT\_SET\_CATALOG\_ID | NUMBER | ID of database that the snapshot set belongs to. |
| SNAPSHOT\_SET\_CATALOG | VARCHAR | Name of database that the snapshot set belongs to. |
| CREATED | TIMESTAMP\_LTZ | Timestamp at which snapshot was created. |
| DELETED | TIMESTAMP\_LTZ | Timestamp at which snapshot was deleted.  This column isn’t displayed by the SHOW command, because the SHOW command output doesn’t include deleted objects. |
| EXPIRATION\_SCHEDULED\_FOR | TIMESTAMP\_LTZ | Timestamp at which snapshot will be expired. |
| IS\_UNDER\_LEGAL\_HOLD | BOOLEAN | Y if snapshot is under legal hold; N otherwise. |
| COMMENT | VARCHAR | Comment for the snapshot. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 360 minutes (6 hours).
