# ANOMALY\_INSIGHTS!GET\_ACCOUNT\_ANOMALIES\_IN\_CREDITS

Returns daily consumption for the current account, and identifies whether that consumption is considered a
[cost anomaly](/user-guide/cost-anomalies).

Note

This method returns consumption with credits as the unit of measure. If you want to return consumption in a currency instead, see
[ANOMALY\_INSIGHTS!GET\_DAILY\_CONSUMPTION\_ANOMALY\_DATA](/sql-reference/classes/anomaly-insights/methods/get_daily_consumption_anomaly_data).

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_ACCOUNT_ANOMALIES_IN_CREDITS(
  '<start_date>',
  '<end_date>' )
```

## Arguments

`'start_date'`
:   Specifies the beginning of the time period for which consumption data is returned.

    Data type: DATE

`'end_date'`
:   Specifies the end of the time period for which consumption data is returned.

    Data type: DATE

## Output

Returns a table with the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| USAGE\_DATE | DATE | Day in Coordinated Universal Time (UTC) when the consumption occurred. |
| CONSUMPTION | NUMBER (38,2) | Amount of consumption, measured in credits. |
| FORECASTED\_CONSUMPTION | NUMBER (38,2) | Predicted consumption based on the anomaly-detecting algorithm, measured in credits. |
| UPPER\_BOUND | NUMBER (38,2) | Predicted highest level of consumption based on the anomaly-detecting algorithm, measured in credits. Consumption levels above this value are considered an anomaly. |
| LOWER\_BOUND | NUMBER (38,2) | Predicted lowest level of consumption based on the anomaly-detecting algorithm, measured in credits. Consumption levels below this value are considered an anomaly. |
| IS\_ANOMALY | BOOLEAN | If `TRUE`, consumption was identified as a cost anomaly because it has gone outside the range of the upper and lower bound. |
| CURRENCY\_TYPE | VARCHAR | Unit of measure for the consumption, which is always `CREDITS`. |
| ANOMALY\_ID | VARCHAR | System-generated identifier. |

Expand

Show lessSee more

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role
- SNOWFLAKE.APP\_USAGE\_VIEWER application role

## Example

The following example identifies anomalies in the current account based on consumption between January 1, 2024, and March 31, 2024:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_ACCOUNT_ANOMALIES_IN_CREDITS(
  '2024-01-01', '2024-03-31');
```
