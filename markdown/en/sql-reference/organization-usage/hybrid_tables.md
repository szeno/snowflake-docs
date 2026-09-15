[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# HYBRID\_TABLES view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

This Organization Usage view displays a row for each hybrid table defined in each account in your organization.

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

| Column Name | Data Type | Description |
| --- | --- | --- |
| ID | NUMBER | ID of the hybrid table. |
| NAME | TEXT | Name of the hybrid table. |
| SCHEMA\_ID | NUMBER | ID of the schema to which the hybrid table belongs. |
| SCHEMA\_NAME | TEXT | Schema to which the hybrid table belongs. |
| DATABASE\_ID | NUMBER | ID of the database to which the hybrid table belongs. |
| DATABASE\_NAME | TEXT | Database to which the hybrid table belongs. |
| OWNER | TEXT | Owner of the hybrid table. |
| ROW\_COUNT | NUMBER | Approximate row count of the hybrid table. |
| BYTES | NUMBER | Approximate size in bytes of the row store of the hybrid table. |
| RETENTION\_TIME | NUMBER | Retention time for data in the hybrid table. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the hybrid table. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Last time this hybrid table was altered by a DDL statement, a TRUNCATE or INSERT OVERWRITE statement, or a compaction job. Note that regular DML operations are not recorded here. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the hybrid table was dropped. |
| COMMENT | TEXT | Comment for the hybrid table. |
| OWNER\_ROLE\_TYPE | TEXT | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 5 hours.
