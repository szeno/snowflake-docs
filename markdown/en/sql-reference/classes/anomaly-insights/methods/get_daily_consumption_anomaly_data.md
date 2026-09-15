# ANOMALY\_INSIGHTS!GET\_DAILY\_CONSUMPTION\_ANOMALY\_DATA

Returns daily consumption for a specific account or the entire organization, and identifies whether that consumption is considered a
[cost anomaly](/user-guide/cost-anomalies).

Note

This method returns consumption with a currency as the unit of measure. If you want to return consumption in credits instead, see
[ANOMALY\_INSIGHTS!GET\_ACCOUNT\_ANOMALIES\_IN\_CREDITS](/sql-reference/classes/anomaly-insights/methods/get_account_anomalies_in_credits).

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_DAILY_CONSUMPTION_ANOMALY_DATA(
  '<start_date>',
  '<end_date>',
  <account_name> )
```

## Arguments

`'start_date'`
:   Specifies the beginning of the time period for which consumption data is returned.

    Data type: DATE

`'end_date'`
:   Specifies the end of the time period for which consumption data is returned.

    Data type: DATE

`account_name`
:   Specifies an expression that determines the account(s) for which consumption data is returned. You can specify the following values:

    - `'account_name'`: Returns data for the specified account. You must specify the account name, not the account locator.
    - `CURRENT_ACCOUNT_NAME()`: Returns data for the current account.
    - `NULL`: Returns data for the entire organization, not a specific account.

## Output

Returns a table with the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| USAGE\_DATE | DATE | Day in UTC when the consumption occurred. |
| CONSUMPTION | NUMBER (38,2) | Amount of consumption measured in CURRENCY\_TYPE. |
| FORECASTED\_CONSUMPTION | NUMBER (38,2) | Predicted consumption based on the anomaly-detecting algorithm, measured in CURRENCY\_TYPE. |
| UPPER\_BOUND | NUMBER (38,2) | Predicted highest level of consumption based on the anomaly-detecting algorithm, measured in CURRENCY\_TYPE. Consumption levels above this value are considered an anomaly. |
| LOWER\_BOUND | NUMBER (38,2) | Predicted lowest level of consumption based on the anomaly-detecting algorithm, measured in CURRENCY\_TYPE. Consumption levels below this value are considered an anomaly. |
| IS\_ANOMALY | BOOLEAN | If true, consumption has been identified as a cost anomaly because it has gone outside the range of the upper and lower bound. |
| CURRENCY\_TYPE | VARCHAR | Unit of measure for the consumption. For information about why the unit of measure is credits or a currency, see [Unit of measure for cost data](/user-guide/cost-anomalies#label-cost-anomaly-currency). |
| ANOMALY\_ID | VARCHAR | System-generated identifier. |

Expand

Show lessSee more

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- ORGANIZATION\_BILLING\_VIEWER application role in the organization account
- SNOWFLAKE.APP\_ORGANIZATION\_BILLING\_VIEWER application role in an ORGADMIN-enabled account

## Usage notes

To return data for a different account or the entire organization, you must execute this method from the
[organization account](/user-guide/organization-accounts) or an
[ORGADMIN-enabled account](/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account).

## Example

Identify organization-level anomalies based on consumption between January 1, 2024, and March 31, 2024:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_DAILY_CONSUMPTION_ANOMALY_DATA(
  '2024-01-01', '2024-03-31', NULL);
```

Identify anomalies in the current account based on consumption between January 1, 2024, and March 31, 2024:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_DAILY_CONSUMPTION_ANOMALY_DATA(
  '2024-01-01', '2024-03-31', current_account_name());
```

Identify anomalies in the account `prod_acct1` based on consumption between January 1, 2024, and March 31, 2024:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_DAILY_CONSUMPTION_ANOMALY_DATA(
  '2024-01-01', '2024-03-31', 'prod_acct1');
```
