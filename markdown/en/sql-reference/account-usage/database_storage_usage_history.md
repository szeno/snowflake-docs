Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DATABASE\_STORAGE\_USAGE\_HISTORY view

This Account Usage view can be used to query the average daily storage usage, in bytes, for databases in the account for the last 365 days (1 year). The data includes:

- All data stored in tables in the database(s).
- All historical data maintained in Fail-safe for the database(s).

See also:
:   [STORAGE\_DAILY\_HISTORY view](/sql-reference/organization-usage/storage_daily_history) , [STORAGE\_USAGE view](/sql-reference/account-usage/storage_usage) , [TABLE\_STORAGE\_METRICS view](/sql-reference/account-usage/table_storage_metrics)

Note

This view isn’t designed to reconcile with your Snowflake bill. As a result, the sum of database-level usage in this view won’t equal the billed storage for your account.

For a view that more closely reflects billed storage at the account and organization level, see [STORAGE\_DAILY\_HISTORY view](/sql-reference/organization-usage/storage_daily_history).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| USAGE\_DATE | DATE | Date (in the local time zone) of this storage usage record. It is recommended that you change the query session to use the UTC time zone instead (e.g. `ALTER SESSION SET TIMEZONE='UTC'`). |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database. |
| DATABASE\_NAME | VARCHAR | Name of the database. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the database was dropped; NULL for active databases. |
| AVERAGE\_DATABASE\_BYTES | FLOAT | Number of bytes of database storage used, including bytes currently in Time Travel. |
| AVERAGE\_FAILSAFE\_BYTES | FLOAT | Number of bytes of Fail-safe storage used. |
| AVERAGE\_HYBRID\_TABLE\_STORAGE\_BYTES | FLOAT | Number of bytes of hybrid table storage used (data in the row store). |
| AVERAGE\_ARCHIVE\_STORAGE\_COOL\_BYTES | FLOAT | Average number of bytes (including active bytes, time travel bytes, and bytes subject to [minimum storage duration charges](/user-guide/storage-management/storage-lifecycle-policies-billing#label-slp-billing-penalty-bytes)) of table storage used in the COOL storage tier. |
| AVERAGE\_ARCHIVE\_STORAGE\_COLD\_BYTES | FLOAT | Average number of bytes (including active bytes, time travel bytes, and bytes subject to [minimum storage duration charges](/user-guide/storage-management/storage-lifecycle-policies-billing#label-slp-billing-penalty-bytes)) of table storage used in the COLD storage tier. |
| AVERAGE\_COOL\_FAILSAFE\_BYTES | FLOAT | Average number of bytes of Fail-safe storage used in the COOL storage tier. |
| AVERAGE\_COLD\_FAILSAFE\_BYTES | FLOAT | Average number of bytes of Fail-safe storage used in the COLD storage tier. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- This view is suitable for comparing relative storage usage between databases in an account over time. It isn’t suitable for calculating exact database-level storage charges.
- To approximate database-level storage costs for chargeback, combine each database’s share of usage in this view with your total billed storage from [STORAGE\_DAILY\_HISTORY view](/sql-reference/organization-usage/storage_daily_history) or your invoice. Treat the result as an approximation, not an exact billing figure.
- Note

  With [BCR-2127](/release-notes/bcr-bundles/2025_07/bcr-2127),
  this view includes new columns for storage lifecycle policies.
  To view storage lifecycle policy columns, you must enable the 2025\_07 behavior change bundle
  in your account.

  To [enable this bundle in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-enable-bundle),
  execute the following statement:

  Copy code

  ```
  SELECT SYSTEM$ENABLE_BEHAVIOR_CHANGE_BUNDLE('2025_07');
  ```
