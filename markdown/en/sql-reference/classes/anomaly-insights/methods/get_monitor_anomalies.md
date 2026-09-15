# ANOMALY\_INSIGHTS!GET\_MONITOR\_ANOMALIES

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Returns the saved results for an [anomaly monitor](/user-guide/cost-anomalies#label-cost-anomaly-monitors), and identifies which days are cost anomalies.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_MONITOR_ANOMALIES(
  '<alias>',
  '<start_date>',
  '<end_date>' )
```

## Arguments

`'alias'`
:   Name of the monitor. The name isn’t case-sensitive.

    Data type: VARCHAR

`'start_date'`
:   Specifies the beginning of the time period for which consumption data is returned.

    Data type: DATE

`'end_date'`
:   Specifies the end of the time period for which consumption data is returned.

    Data type: DATE

## Output

Returns a table with one row per day in the time period, with the following columns:

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

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role
- SNOWFLAKE.APP\_USAGE\_VIEWER application role

## Usage notes

- The method fails if no monitor with the specified name exists in the account, or if `end_date` is earlier than `start_date`.
- The range between `start_date` and `end_date` can’t exceed 366 days. To retrieve a longer history, call the method more than once with
  consecutive ranges.
- The method reads saved results. It doesn’t recompute them. To force a recomputation, use
  [ANOMALY\_INSIGHTS!RECALCULATE\_ANOMALIES](/sql-reference/classes/anomaly-insights/methods/recalculate_anomalies).

## Example

Return the results for the monitor `Eng-Platform` between January 1, 2026, and March 31, 2026:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_MONITOR_ANOMALIES(
  'Eng-Platform', '2026-01-01', '2026-03-31');
```

To use the output to identify the cost anomalies, look for the days where the value of the `IS_ANOMALY` column is `TRUE`.
