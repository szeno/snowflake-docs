# Mar 16, 2026: Metering disabled for hybrid table requests

As a follow-up to the announcement of
[simplified pricing for hybrid tables](/release-notes/2026/other/2026-03-02-hybrid-tables-pricing),
Snowflake has disabled metering for hybrid table requests. You will no longer see new
events in the following views:

- [HYBRID\_TABLE\_USAGE\_HISTORY](/sql-reference/account-usage/hybrid_table_usage_history)
- Account Usage [METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history)
- Organization Usage [METERING\_DAILY\_HISTORY](/sql-reference/organization-usage/metering_daily_history)

Historical consumption data that was recorded before this change is still available in these views and can be queried.
