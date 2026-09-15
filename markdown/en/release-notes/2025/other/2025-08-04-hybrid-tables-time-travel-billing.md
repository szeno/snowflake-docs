# Aug 04, 2025: Hybrid table storage for Time Travel data

Consumption for hybrid table storage now takes into account the data that is retained by
[Time Travel](/user-guide/data-time-travel).
Data retained by Time Travel is included in the following storage metrics:

- STORAGE\_BYTES column in the [STORAGE\_USAGE view](/sql-reference/account-usage/storage_usage)
- AVERAGE\_DATABASE\_BYTES column in:
  - The Account Usage [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/database_storage_usage_history)
  - The Organization Usage [DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/organization-usage/database_storage_usage_history)
  - The Information Schema [DATABASE\_STORAGE\_USAGE\_HISTORY](/sql-reference/functions/database_storage_usage_history) function

Time Travel data is stored in object storage, not the row store, and is charged at the standard table rate,
not the higher hybrid table rate.
