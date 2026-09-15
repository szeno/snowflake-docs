# ANOMALY\_INSIGHTS!RECALCULATE\_ANOMALIES

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Recomputes the full history of an [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors) and returns the new results.

Snowflake recomputes each monitor daily from the current state of your tags, but it can’t detect changes to which resources carry a tag.
Call this method after you tag or untag resources and want the monitor’s history refreshed immediately.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!RECALCULATE_ANOMALIES(
  '<alias>' )
```

## Arguments

`'alias'`
:   Name of the monitor. The name isn’t case-sensitive.

    Data type: VARCHAR

## Output

Returns a table with one row per day in the monitor’s history, with the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| USAGE\_DATE | DATE | Day in UTC when the consumption occurred. |
| CONSUMPTION | NUMBER | Amount of consumption attributed to the monitor on this day. |
| FORECASTED\_CONSUMPTION | NUMBER | Predicted consumption based on the anomaly-detecting algorithm. |
| CURRENCY\_TYPE | VARCHAR | Unit of measure for the consumption, which corresponds to the monitor’s credit family. |
| LOWER\_BOUND | NUMBER | Predicted lowest level of consumption based on the anomaly-detecting algorithm. Consumption levels below this value are considered anomalies. |
| UPPER\_BOUND | NUMBER | Predicted highest level of consumption based on the anomaly-detecting algorithm. Consumption levels above this value are considered anomalies. |
| IS\_ANOMALY | BOOLEAN | If `TRUE`, consumption fell outside the range defined by the lower and upper bounds, so Snowflake identified it as a cost anomaly. |
| ANOMALY\_ID | VARCHAR | System-generated identifier for the anomaly. Empty when `IS_ANOMALY` is `FALSE`. |
| LAST\_REFRESHED\_AT | TIMESTAMP | Time when Snowflake last finished computing results for the monitor. This value is the same for every row. |

Expand

Show lessSee more

The method doesn’t accept a date range.

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role
- SNOWFLAKE.APP\_USAGE\_VIEWER application role

## Usage notes

- The method fails if no monitor with the specified name exists in the account, or if the recomputation fails for any reason, such as a
  tag that can no longer be resolved.
- The call is synchronous and regenerates the full consumption time series and calculates any anomalies, so it takes longer to return than
  [ANOMALY\_INSIGHTS!GET\_MONITOR\_ANOMALIES](/sql-reference/classes/anomaly-insights/methods/get_monitor_anomalies).
- The recomputed results are saved, so later calls to
  [ANOMALY\_INSIGHTS!GET\_MONITOR\_ANOMALIES](/sql-reference/classes/anomaly-insights/methods/get_monitor_anomalies) return the refreshed values.
- Recalculating a monitor doesn’t send notifications.

## Example

Recompute the results for the monitor named `Eng-Platform`:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!RECALCULATE_ANOMALIES('Eng-Platform');
```
