# ANOMALY\_INSIGHTS!GET\_HOURLY\_CONSUMPTION\_BY\_SERVICE\_TYPE

Returns the hourly consumption in the current account on a specific day, broken down by service type. You can optionally limit the results
to the service types that are consuming the most credits on that day.

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_HOURLY_CONSUMPTION_BY_SERVICE_TYPE(
  '<date>',
  <number_of_types> )
```

## Arguments

`'date'`
:   Specifies the day for which you want to return consumption data.

    Data type: DATE

`number_of_types`
:   Specifies the number of service types to return, ranked by total consumption on the specified day.

    To return all service types that consumed credits on the specified day, specify `NULL`.

    Data type: NUMBER

## Output

Returns a table with the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| HOUR | NUMBER | A number between 0 and 23 (inclusive) that specifies the hour of the day during which consumption occurred. |
| SERVICE\_TYPE | VARCHAR | The service type that consumed the credits (for example, `AI_SERVICES`). |
| CREDITS | NUMBER | The number of credits consumed by the service type during the specified hour. |

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
- The top service types are determined by total consumption across the entire day. After the top service types are identified, the
  method returns the hourly consumption for each of those service types.

## Examples

Return the two service types that consumed the most credits on January 15, 2026. The output includes the hourly consumption for each service
type.

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_HOURLY_CONSUMPTION_BY_SERVICE_TYPE(
  '2026-01-15', 2);
```

Return the hourly consumption on January 15, 2026, for all service types that had consumption on that day:

Copy code

```
CALL SNOWFLAKE.LOCAL.ANOMALY_INSIGHTS!GET_HOURLY_CONSUMPTION_BY_SERVICE_TYPE(
  '2026-01-15',
  NULL);
```
