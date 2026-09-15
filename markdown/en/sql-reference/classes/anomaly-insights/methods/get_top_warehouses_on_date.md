# ANOMALY\_INSIGHTS!GET\_TOP\_WAREHOUSES\_ON\_DATE

Returns warehouses with the highest change in consumption for a given date, determined by comparing the specified day with the previous day.
Helps investigate account-level and organization-level [cost anomalies](/user-guide/cost-anomalies).

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_TOP_WAREHOUSES_ON_DATE(
  '<date>',
  <number_of_warehouses>,
  <account_name> )
```

## Arguments

`'date'`
:   Specifies the date for which you want to return consumption data.

    Data type: DATE

`number_of_warehouses`
:   Limits the number of warehouses returned by the method. For example, if you specify `5`, the method returns only the top five warehouses
    in terms of change in consumption.

    Data type: NUMBER

`account_name`
:   Specifies an expression that determines the account(s) for which consumption data is returned. You can specify the following values:

    - `'account_name'`: Returns warehouse data for the specified account. You must specify the account name, not the account locator.
    - `CURRENT_ACCOUNT_NAME()`: Returns warehouse data for the current account.
    - `NULL`: Returns warehouse data for the entire organization, not a specific account.

## Output

Returns a table with the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse. |
| WAREHOUSE\_ID | NUMBER | System-generated identifier of the warehouse. |
| CONSUMPTION | NUMBER (38,9) | Amount of consumption on the specified day in credits. |
| COST\_CHANGE | NUMBER (38,9) | Difference between consumption on the specified day and the previous day. |

Expand

Show lessSee more

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role
- SNOWFLAKE.APP\_USAGE\_VIEWER application role

## Usage notes

- To return data for a different account or the entire organization, you must execute this method from the
  [organization account](/user-guide/organization-accounts) or an
  [ORGADMIN-enabled account](/user-guide/organization-administrators#label-enabling-orgadmin-role-for-account).
- You cannot use this method to return a currency as the unit of measure for the consumption.

## Example

Returns the top six warehouses in the organization in terms of change in consumption when comparing August 9, 2024, and August 10, 2024.

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_TOP_WAREHOUSES_ON_DATE('2024-08-10', 6, NULL);
```

Returns the top five warehouses in the current account in terms of change in consumption when comparing December 8, 2024, and December 9,
2024.

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_TOP_WAREHOUSES_ON_DATE(
  '2024-12-09', 5, CURRENT_ACCOUNT_NAME());
```

Returns the top three warehouses in the account `my_acct` in terms of change in consumption when comparing November 8, 2024, and November 9,
2024.

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_TOP_WAREHOUSES_ON_DATE(
  '2024-11-09', 5, 'my_acct');
```
