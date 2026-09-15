Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# HYBRID\_TABLE\_USAGE\_HISTORY view

Feature — Generally Available

Available to accounts in AWS and Microsoft Azure commercial regions only. For more information, see [Clouds and regions](/user-guide/tables-hybrid-limitations#label-hybrid-tables-limitations-regions).

Note

As of March 1, 2026, Snowflake no longer bills customers for hybrid table requests,
and metering was disabled soon after this pricing change took effect. Any new data
in the view as of March 1, 2026, will not be billed to customers, and you can still
query the historical data in the view.

This Account Usage view displays consumption of hybrid table requests
(serverless compute resources), in terms of credits billed for
your entire Snowflake account, within the last 365 days (1 year).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| OBJECT\_TYPE | TEXT | Type of object referenced for scope of consumption: `ACCOUNT` for hybrid tables in your account. |
| OBJECT\_ID | NUMBER | Internal identifier of object referenced for scope of consumption: `NULL` because scope of consumption for hybrid tables is tracked at the account level. |
| OBJECT\_NAME | TEXT | Name of object referenced for scope of consumption: `NULL` because scope of consumption for hybrid tables is tracked at the account level. |
| START\_TIME | TIMESTAMP\_LTZ | Date and start time (in the local time zone) when usage of hybrid tables occurred. |
| END\_TIME | TIMESTAMP\_LTZ | Date and end time (in the local time zone) when usage of hybrid tables occurred. |
| CREDITS\_USED | NUMBER | Number of credits used for hybrid table requests between the values for `START_TIME` and `END_TIME`. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).
- This view may return usage data that is slightly inconsistent with metrics
  returned in [METERING\_DAILY\_HISTORY view](/sql-reference/account-usage/metering_daily_history) and
  [METERING\_HISTORY view](/sql-reference/account-usage/metering_history). The discrepancy in the
  calculation of credits used is due to rounding during division.

## Examples

The following queries return the total number of credits used by hybrid tables in your
account over specific periods of time.

The first query returns credits used for all time (the past year):

Copy code

```
SELECT SUM(credits_used) AS total_credits
  FROM SNOWFLAKE.ACCOUNT_USAGE.HYBRID_TABLE_USAGE_HISTORY;
```

The second query returns credits used over the past 5 days. Alternatively, you could specify some number
of weeks or months:

Copy code

```
SELECT SUM(credits_used) AS total_credits
  FROM SNOWFLAKE.ACCOUNT_USAGE.HYBRID_TABLE_USAGE_HISTORY
  WHERE start_time >= DATEADD(day, -5, CURRENT_TIMESTAMP());
```
