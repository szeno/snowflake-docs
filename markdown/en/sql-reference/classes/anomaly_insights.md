# ANOMALY\_INSIGHTS (SNOWFLAKE.LOCAL)

The ANOMALY\_INSIGHTS [class](/sql-reference/snowflake-db-classes) is used to identify and investigate [cost anomalies](/user-guide/cost-anomalies).

Snowflake instantiates a single instance of the ANOMALY\_INSIGHTS class. You never create an instance of the class.

## Account-level and organization-level cost anomaly methods

- [ANOMALY\_INSIGHTS!ADD\_NOTIFICATION\_INTEGRATION](/sql-reference/classes/anomaly-insights/methods/add_notification_integration)
- [ANOMALY\_INSIGHTS!GET\_ACCOUNT\_ANOMALIES\_IN\_CREDITS](/sql-reference/classes/anomaly-insights/methods/get_account_anomalies_in_credits)
- [ANOMALY\_INSIGHTS!GET\_ACCOUNT\_NOTIFICATION\_EMAILS](/sql-reference/classes/anomaly-insights/methods/get_account_notification_emails)
- [ANOMALY\_INSIGHTS!GET\_DAILY\_CONSUMPTION\_ANOMALY\_DATA](/sql-reference/classes/anomaly-insights/methods/get_daily_consumption_anomaly_data)
- [ANOMALY\_INSIGHTS!GET\_HOURLY\_CONSUMPTION\_BY\_SERVICE\_TYPE](/sql-reference/classes/anomaly-insights/methods/get_hourly_consumption_by_service_type)
- [ANOMALY\_INSIGHTS!GET\_HOURLY\_SPEND\_FOR\_ANOMALY](/sql-reference/classes/anomaly-insights/methods/get_hourly_spend_for_anomaly)
- [ANOMALY\_INSIGHTS!GET\_NOTIFICATION\_INTEGRATIONS](/sql-reference/classes/anomaly-insights/methods/get_notification_integrations)
- [ANOMALY\_INSIGHTS!GET\_ORG\_NOTIFICATION\_EMAILS](/sql-reference/classes/anomaly-insights/methods/get_org_notification_emails)
- [ANOMALY\_INSIGHTS!GET\_TOP\_ACCOUNTS\_BY\_CONSUMPTION](/sql-reference/classes/anomaly-insights/methods/get_top_accounts_by_consumption)
- [ANOMALY\_INSIGHTS!GET\_TOP\_QUERIES\_FROM\_WAREHOUSE](/sql-reference/classes/anomaly-insights/methods/get_top_queries_from_warehouse)
- [ANOMALY\_INSIGHTS!GET\_TOP\_WAREHOUSES\_ON\_DATE](/sql-reference/classes/anomaly-insights/methods/get_top_warehouses_on_date)
- [ANOMALY\_INSIGHTS!REMOVE\_NOTIFICATION\_INTEGRATION](/sql-reference/classes/anomaly-insights/methods/remove_notification_integration)
- [ANOMALY\_INSIGHTS!SET\_ACCOUNT\_NOTIFICATION\_EMAILS](/sql-reference/classes/anomaly-insights/methods/set_account_notification_emails)
- [ANOMALY\_INSIGHTS!SET\_ORG\_NOTIFICATION\_EMAILS](/sql-reference/classes/anomaly-insights/methods/set_org_notification_emails)

## Anomaly monitor methods

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

- [ANOMALY\_INSIGHTS!ADHOC\_CALCULATE\_ANOMALIES\_FROM\_CONFIG](/sql-reference/classes/anomaly-insights/methods/adhoc_calculate_anomalies_from_config)
- [ANOMALY\_INSIGHTS!CREATE\_MONITOR](/sql-reference/classes/anomaly-insights/methods/create_monitor)
- [ANOMALY\_INSIGHTS!DROP\_MONITOR](/sql-reference/classes/anomaly-insights/methods/drop_monitor)
- [ANOMALY\_INSIGHTS!GET\_MONITOR\_ANOMALIES](/sql-reference/classes/anomaly-insights/methods/get_monitor_anomalies)
- [ANOMALY\_INSIGHTS!GET\_MONITOR\_CONFIG](/sql-reference/classes/anomaly-insights/methods/get_monitor_config)
- [ANOMALY\_INSIGHTS!GET\_MONITOR\_NOTIFICATION\_EMAILS](/sql-reference/classes/anomaly-insights/methods/get_monitor_notification_emails)
- [ANOMALY\_INSIGHTS!GET\_MONITOR\_NOTIFICATION\_LOG](/sql-reference/classes/anomaly-insights/methods/get_monitor_notification_log)
- [ANOMALY\_INSIGHTS!LIST\_MONITORS](/sql-reference/classes/anomaly-insights/methods/list_monitors)
- [ANOMALY\_INSIGHTS!RECALCULATE\_ANOMALIES](/sql-reference/classes/anomaly-insights/methods/recalculate_anomalies)
- [ANOMALY\_INSIGHTS!RENAME\_MONITOR](/sql-reference/classes/anomaly-insights/methods/rename_monitor)
- [ANOMALY\_INSIGHTS!SET\_MONITOR\_NOTIFICATION\_EMAILS](/sql-reference/classes/anomaly-insights/methods/set_monitor_notification_emails)
- [ANOMALY\_INSIGHTS!UPDATE\_MONITOR\_CONFIG](/sql-reference/classes/anomaly-insights/methods/update_monitor_config)
