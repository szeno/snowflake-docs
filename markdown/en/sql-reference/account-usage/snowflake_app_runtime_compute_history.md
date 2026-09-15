Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# SNOWFLAKE\_APP\_RUNTIME\_COMPUTE\_HISTORY view

The SNOWFLAKE\_APP\_RUNTIME\_COMPUTE\_HISTORY view in the ACCOUNT\_USAGE schema returns
the hourly compute credit usage for
[Snowflake App Runtime](/developer-guide/snowflake-app-runtime/about-snowflake-app-runtime)
in an account within the last 365 days (1 year).

All App Runtime apps in an account share Snowflake-managed compute, and the
view reports credit usage at the account level. Per-app cost attribution isn’t
available.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the usage took place. |
| COMPUTE\_POOL\_NAME | VARCHAR | Name of the Snowflake-managed compute pool that served the usage. Currently always `SNOWFLAKE_APP_RUNTIME_COMPUTE`. |
| CREDITS\_USED | NUMBER | Number of credits used by Snowflake App Runtime in the hour. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- Credit usage reported here is also included in
  [METERING\_HISTORY](/sql-reference/account-usage/metering_history) and
  [METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history)
  under the `SNOWFLAKE_APP_RUNTIME` service type.

## Examples

Return daily Snowflake App Runtime credit usage for the last 30 days:

Copy code

```
SELECT
    DATE(start_time) AS usage_date,
    SUM(credits_used) AS credits_used
FROM snowflake.account_usage.snowflake_app_runtime_compute_history
WHERE start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY usage_date
ORDER BY usage_date DESC;
```
