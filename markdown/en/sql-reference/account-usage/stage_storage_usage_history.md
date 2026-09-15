Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# STAGE\_STORAGE\_USAGE\_HISTORY view

This Account Usage view can be used to query the average daily data storage usage, in bytes, within the last 365 days (1 year) for all the Snowflake internal stages in the account, including:

- Named internal stages.
- Default staging areas (for tables and users).

Note

This view returns stage storage usage within the last 365 days (1 year).

See also:
:   [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/database_storage_usage_history) , [STORAGE\_USAGE view](/sql-reference/account-usage/storage_usage) , [WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| USAGE\_DATE | DATE | Date of this storage usage record. |
| AVERAGE\_STAGE\_BYTES | NUMBER | Number of bytes of stage storage used. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).
