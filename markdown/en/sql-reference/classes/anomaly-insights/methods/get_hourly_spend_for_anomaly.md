# ANOMALY\_INSIGHTS!GET\_HOURLY\_SPEND\_FOR\_ANOMALY

Returns the hourly consumption in the current account on a specific day.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_HOURLY_SPEND_FOR_ANOMALY(
  '<date>' )
```

## Arguments

`'date'`
:   Specifies the day for which you want to return consumption data.

    Data type: DATE

## Output

Returns a table with the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| HOUR | INTEGER | Specifies the hour of the day during which consumption occurred. |
| CONSUMPTION | NUMBER | Specifies the amount of consumption during the hour in credits. |

Expand

Show lessSee more

## Access control requirements

Users with any of the following roles can call this method:

- ACCOUNTADMIN system role
- GLOBALORGADMIN system role
- SNOWFLAKE.APP\_USAGE\_ADMIN application role
- SNOWFLAKE.APP\_USAGE\_VIEWER application role

## Usage notes

- A day is defined by a 24-hour period in UTC. This might differ from a user’s local time zone.
- This method returns consumption data for the current account. It cannot be used to return data for other accounts or the entire
  organization.
- This method returns credits consumed for the account (not currency).

## Example

The following example returns the hourly consumption on October 17, 2024.

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_HOURLY_SPEND_FOR_ANOMALY('2024-10-17');
```
