Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views) , [READER\_ACCOUNT\_USAGE](/sql-reference/account-usage#label-reader-account-usage-views)

# STORAGE\_USAGE view

This Account Usage view displays the average daily data storage usage, in bytes, within the last 365 days (1 year) across the entire account, including data in:

- Database tables.
- Files in all internal stages.

See also:
:   [STORAGE\_DAILY\_HISTORY view](/sql-reference/organization-usage/storage_daily_history) , [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/database_storage_usage_history) , [STAGE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/stage_storage_usage_history)

## Columns

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

- In the ACCOUNT\_USAGE schema, latency for the view is up to 120 minutes (2 hours).
- In the READER\_ACCOUNT\_USAGE schema, latency is up to 24 hours.
- This view uses a different measurement approach than the one used for billing, so the values here won’t match your invoice exactly. For the storage view that most closely reflects billed storage at the account and organization level, see [STORAGE\_DAILY\_HISTORY view](/sql-reference/organization-usage/storage_daily_history).
