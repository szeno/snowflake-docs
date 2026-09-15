Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# STORAGE\_DAILY\_HISTORY view

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

The STORAGE\_DAILY\_HISTORY view in the ORGANIZATION\_USAGE schema can be used to query the average daily storage usage, in bytes, for all accounts in the organization for the last 365 days (1 year).

Of the storage views that Snowflake provides, this view most closely reflects the storage that contributes to your bill at the account and organization level. Use it for high-level analysis and reporting of billed storage trends.

See also:
:   [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/database_storage_usage_history) , [STORAGE\_USAGE view](/sql-reference/account-usage/storage_usage)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| SERVICE\_TYPE | VARCHAR | The type of service, which can be one of `STORAGE`, `STORAGE_READER`. |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_NAME | VARCHAR | Name of the account (user-defined). |
| USAGE\_DATE | DATE | The date (in the UTC time zone) on which the usage took place. |
| AVERAGE\_BYTES | NUMBER | Average number of bytes of database storage and stage storage used on this date, including data in Time Travel and Fail-safe. |
| REGION | VARCHAR | ID of the Snowflake Region where the account is located. |
| ACCOUNT\_LOCATOR | VARCHAR | Locator for the account (system-defined). |
| CREDITS | NUMBER | Total number of storage credits used for the account on this date. (Calculated as AVERAGE\_BYTES, converted to tebibytes, divided by the number of days in the month.) |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).
- The data is retained for 365 days (1 year).
- For the authoritative record of storage charges, refer to your invoice.
- Other storage views, such as [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/database_storage_usage_history) and [STORAGE\_USAGE view](/sql-reference/account-usage/storage_usage), use different measurement approaches and won’t match the values in this view.
