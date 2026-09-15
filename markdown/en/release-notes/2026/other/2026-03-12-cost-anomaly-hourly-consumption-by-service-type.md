# Mar 12, 2026: Investigate cost anomalies using hourly consumption by service type

When investigating a cost anomaly, you can now view hourly consumption broken down by service type. This enhancement lets you
see which service types (for example, `AI_SERVICES`) are contributing to your consumption during each hour of the day, making
it easier to identify the root cause of a cost anomaly.

You can investigate hourly consumption by service type using Snowsight or SQL.

- **Snowsight web interface:** When you investigate an account-level anomaly, the **Top consumption drivers** section now shows
  consumption broken down by the top service types for each hour.

  For more information, see [Identify and investigate cost anomalies with Snowsight](/user-guide/cost-anomalies-ui#label-cost-anomaly-identify-ui).
- **ANOMALY\_INSIGHTS class:** A new [GET\_HOURLY\_CONSUMPTION\_BY\_SERVICE\_TYPE](/sql-reference/classes/anomaly-insights/methods/get_hourly_consumption_by_service_type)
  method returns the hourly consumption for a given day, broken down by the top service types.

  For more information, see [Hourly consumption by service type](/user-guide/cost-anomalies-class#label-cost-anomaly-investigate-hourly-service-type-class).
