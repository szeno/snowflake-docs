# <budget\_name>!GET\_SERVICE\_TYPE\_USAGE

View the credit usage for a [budget](/user-guide/budgets) by service type.

Important

This method has been deprecated. Use [<budget\_name>!GET\_SERVICE\_TYPE\_USAGE\_V2](/sql-reference/classes/budget/methods/get_service_type_usage_v2) instead.

## Syntax

Copy code

```
<budget_name>!GET_SERVICE_TYPE_USAGE( SERVICE_TYPE => '<service_type>' ,
                                      TIME_DEPART => '<time_interval>' ,
                                      USER_TIMEZONE => '<timezone>' ,
                                      TIME_LOWER_BOUND => <constant_expr> ,
                                      TIME_UPPER_BOUND => <constant_expr>
                                    )
```

## Arguments

`SERVICE_TYPE => service_type`
:   The service type used to limit results.

    Valid values:

    > [Type of service](/user-guide/budgets#label-budgets-supported-serverless-features) that is consuming credits, which can be one of the following:
    >
    > - `AUTO_CLUSTERING`
    > - `DATA_QUALITY_MONITORING`
    > - `HYBRID_TABLE_REQUESTS`
    > - `MATERIALIZED_VIEW`
    > - `PIPE`
    > - `QUERY_ACCELERATION`
    > - `SEARCH_OPTIMIZATION`
    > - `SERVERLESS_ALERTS`
    > - `SERVERLESS_TASK`
    > - `SNOWPIPE_STREAMING`
    > - `WAREHOUSE_METERING`
    > - `WAREHOUSE_METERING_READER`

`TIME_DEPART => time_interval`
:   Time interval used to delineate usage records. Each row displays service usage by the specified time interval.

    Valid values:

    - HOUR, hour
    - DAY, day
    - WEEK, week

`USER_TIMEZONE => timezone`
:   String specifying the user’s timezone. Budget metering is based on the UTC timezone.

`TIME_LOWER_BOUND => constant_expr`
:   The start of the time range during which the spending occurred.

`TIME_UPPER_BOUND => constant_expr`
:   The end of the time range during which the spending occurred.

## Returns

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_TZ | Date and time the usage occurred. |
| ENTITY\_ID | NUMBER | Internal identifier for the object in the budget. |
| NAME | VARCHAR | Name of the metered object. |
| CREDITS\_USED | FLOAT | Number of credits used. This is the sum of CREDITS\_COMPUTE and CREDITS\_CLOUD. |
| CREDITS\_COMPUTE | FLOAT | Number of compute credits used. |
| CREDITS\_CLOUD | FLOAT | Number of cloud service credits used. |

Expand

Show lessSee more

## Access control requirements

- The following minimum privileges and roles are required to view results for *custom budgets*:

  - Any [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
  - USAGE privilege on the database and schema that contains the budget instance.
  - [Snowflake database role](/sql-reference/snowflake-db-roles) USAGE\_VIEWER.
- The following role is required to view results for the *account budget*:

  - Any [application role](/user-guide/budgets#label-budgets-application-roles) for the account budget.
  - [Snowflake database role](/sql-reference/snowflake-db-roles) USAGE\_VIEWER.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- For `timezone`, you can specify a [time zone name](https://data.iana.org/time-zones/tzdb-2025b/zone1970.tab) or a [link name](https://data.iana.org/time-zones/tzdb-2025b/backward) from release
  2025b of the [IANA Time Zone Database](https://www.iana.org/time-zones) (e.g. `America/Los_Angeles`, `Europe/London`, `UTC`,
  `Etc/GMT`, etc.).

  Note

  - Time zone names are case-sensitive and must be enclosed in single quotes (e.g. `'UTC'`).
  - Snowflake does not support the majority of timezone [abbreviations](https://en.wikipedia.org/wiki/List_of_time_zone_abbreviations) (e.g. `PDT`, `EST`, etc.) because a
    given abbreviation might refer to one of several different time zones. For example, `CST` might refer to Central
    Standard Time in North America (UTC-6), Cuba Standard Time (UTC-5), and China Standard Time (UTC+8).
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Examples

View the daily credits spent for each warehouse in the past week for the account budget:

Copy code

```
CALL snowflake.local.account_root_budget!GET_SERVICE_TYPE_USAGE(
   SERVICE_TYPE => 'WAREHOUSE_METERING',
   TIME_DEPART => 'day',
   USER_TIMEZONE => 'UTC',
   TIME_LOWER_BOUND => dateadd('day', -7, current_timestamp()),
   TIME_UPPER_BOUND => current_timestamp()
);
```

## Error messages

To troubleshoot issues that can occur when you call this method, see [You can’t successfully call the GET\_SERVICE\_TYPE\_USAGE method](/user-guide/budgets/troubleshoot#label-troubleshooting-budgets-get-service-type-usage).
