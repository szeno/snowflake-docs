[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# STORAGE\_USAGE view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view displays the average daily data storage usage, in bytes, for each account in your organization for the last 365 days (1 year). Each row is the storage for a single account on a given date, including data in:

- Database tables.
- Files in all internal stages.

See also:
:   [STORAGE\_DAILY\_HISTORY view](/sql-reference/organization-usage/storage_daily_history) , [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/organization-usage/database_storage_usage_history) , [STAGE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/organization-usage/stage_storage_usage_history)

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
| USAGE\_DATE | DATE | Date of this storage usage record. The date is based on the local time zone. It is recommended that you change the query session to use the UTC time zone instead (for example, `ALTER SESSION SET TIMEZONE='UTC'`). |
| STORAGE\_BYTES | NUMBER | Number of bytes of table storage used, including bytes currently in Time Travel. |
| STAGE\_BYTES | NUMBER | Number of bytes of stage storage used by files in all internal stages (named, table, and user). |
| FAILSAFE\_BYTES | NUMBER | Number of bytes of Fail-safe storage used. |
| HYBRID\_TABLE\_STORAGE\_BYTES | NUMBER | Number of bytes of hybrid table storage used (data in the row store). |
| ARCHIVE\_STORAGE\_COOL\_BYTES | NUMBER | Number of all bytes of table storage used in the COOL storage tier, including active bytes, Fail-safe bytes, Time Travel bytes, and bytes subject to [minimum storage duration charges](/user-guide/storage-management/storage-lifecycle-policies-billing#label-slp-billing-penalty-bytes). |
| ARCHIVE\_STORAGE\_COLD\_BYTES | NUMBER | Number of all bytes of table storage used in the COLD storage tier, including active bytes, Fail-safe bytes, Time Travel bytes, and bytes subject to [minimum storage duration charges](/user-guide/storage-management/storage-lifecycle-policies-billing#label-slp-billing-penalty-bytes). |
| ARCHIVE\_STORAGE\_RETRIEVAL\_TEMP\_BYTES | NUMBER | Number of bytes used in the standard storage tier, during data retrieval from the COLD storage tier. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 240 minutes (4 hours).
- This view uses a different measurement approach than the one used for billing, so the values here won’t match your invoice exactly. For the storage view that most closely reflects billed storage at the account and organization level, see [STORAGE\_DAILY\_HISTORY view](/sql-reference/organization-usage/storage_daily_history).
