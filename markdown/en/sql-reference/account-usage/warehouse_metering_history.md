Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views) , [READER\_ACCOUNT\_USAGE](/sql-reference/account-usage#label-reader-account-usage-views)

# WAREHOUSE\_METERING\_HISTORY view

This Account Usage view can be used to return the hourly credit usage for a single warehouse (or all the warehouses in your account) within the last 365 days (1 year).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| READER\_ACCOUNT\_NAME | VARCHAR | Name of the reader account where the warehouse usage took place. Column only included in view in READER\_ACCOUNT\_USAGE schema. |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the warehouse usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the warehouse usage took place. |
| WAREHOUSE\_ID | NUMBER | Internal/system-generated identifier for the warehouse. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse. |
| CREDITS\_USED | NUMBER | Total number of credits used for the warehouse in the hour. This is a sum of CREDITS\_USED\_COMPUTE and CREDITS\_USED\_CLOUD\_SERVICES. This value does not take into account the [adjustment for cloud services](/user-guide/cost-understanding-compute#label-understanding-billing-for-cloud-services-usage), and may therefore be greater than the credits that are billed. To determine how many credits were actually billed, run queries against the [METERING\_DAILY\_HISTORY view](/sql-reference/account-usage/metering_daily_history). |
| CREDITS\_USED\_COMPUTE | NUMBER | Number of credits used for the warehouse in the hour. |
| CREDITS\_USED\_CLOUD\_SERVICES | NUMBER | Number of credits used for cloud services in the hour. |
| CREDITS\_ATTRIBUTED\_COMPUTE\_QUERIES | NUMBER | Number of credits attributed to queries in the hour.     Includes only the credit usage for query execution and doesn’t include warehouse idle time usage. |

Expand

Show lessSee more

## Usage notes

- In the ACCOUNT\_USAGE schema, latency for the view is up to 180 minutes (3 hours), except for the CREDITS\_USED\_CLOUD\_SERVICES column. Latency for
  CREDITS\_USED\_CLOUD\_SERVICES is up to 6 hours.
- In the READER\_ACCOUNT\_USAGE schema, latency for the view is up to 24 hours.
- Warehouse idle time is not included in the CREDITS\_ATTRIBUTED\_COMPUTE\_QUERIES column.

  See [Examples](#examples) for a query that calculates the cost of idle time.

- The `CREDITS_ATTRIBUTED_COMPUTE_QUERIES` column is NULL for [Adaptive Warehouses](/user-guide/warehouses-adaptive).
- If you want to reconcile the data in this view with a corresponding view in the [ORGANIZATION USAGE schema](/sql-reference/organization-usage), you must first set the timezone of the session to UTC. Before querying the Account Usage view, execute:

  > Copy code
  >
  > ```
  > ALTER SESSION SET TIMEZONE = UTC;
  > ```

## Examples

For example, to determine the cost of idle time for each warehouse for the last 10 days, execute the following statement:

Copy code

```
SELECT
  (SUM(credits_used_compute) -
    SUM(credits_attributed_compute_queries)) AS idle_cost,
  warehouse_name
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD('days', -10, CURRENT_DATE())
  AND end_time < CURRENT_DATE()
GROUP BY warehouse_name;
```
