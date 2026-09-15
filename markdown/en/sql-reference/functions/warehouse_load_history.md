Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# WAREHOUSE\_LOAD\_HISTORY

This table function can be used to query the activity history (defined as the “query load”) for a single warehouse within a specified date range.

Note

This function returns warehouse activity within the last 14 days.

Note

Specifying a date value that is within one minute of the current timestamp can produce inaccurate results.

See also:
:   [WAREHOUSE\_METERING\_HISTORY](/sql-reference/functions/warehouse_metering_history)

## Syntax

Copy code

```
WAREHOUSE_LOAD_HISTORY(
      [ DATE_RANGE_START => <constant_expr> ]
      [, DATE_RANGE_END => <constant_expr> ]
      [, WAREHOUSE_NAME => '<string>' ] )
```

## Arguments

All the arguments are optional.

`DATE_RANGE_START => constant_expr` , `DATE_RANGE_END => constant_expr`
:   The date range, within the last 14 days, for which to retrieve warehouse load history data:

    - If an end date is not specified, then [CURRENT\_DATE](/sql-reference/functions/current_date) is used as the end of the range.
    - If a start date is not specified, then the range starts 10 minutes prior to the start of `DATE_RANGE_END` (i.e. the default is to show the previous 10 minutes of load history). For example,
      if `DATE_RANGE_END` is [CURRENT\_DATE](/sql-reference/functions/current_date), then the default `DATE_RANGE_START` is 11:50 PM on the previous day.

    If the range falls outside the last 15 days, an error is returned.

    Note

    If the selected period is less than 8 hours, load is shown in 5-second intervals; otherwise, 5-minute intervals are used.

`WAREHOUSE_NAME => 'string'`
:   The name of the warehouse to retrieve usage load history for. Note that the warehouse name must be enclosed in single quotes. Also, if the warehouse name contains any spaces, mixed-case characters,
    or special characters, the name must be double-quoted within the single quotes (e.g. `'"My Warehouse"'` vs `'mywarehouse'`).

    Default: [CURRENT\_WAREHOUSE](/sql-reference/functions/current_warehouse)

## Usage notes

- To get results from this function, one of the following roles or privileges are required:

  - The ACCOUNTADMIN role can get results from this function as it has all of the global account permissions.
  - A role with the MONITOR USAGE global privilege on the ACCOUNT can query this function for any warehouses in the account.
  - A role with the MONITOR privilege on the WAREHOUSE can query this function for the warehouse it has permissions on.
  - A role with the OWNERSHIP privilege on the WAREHOUSE has all permissions on the warehouse including MONITOR.

  For more details, see [Access control privileges](/user-guide/security-access-control-privileges).
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).

## Output

Note

For the output columns of this function, the query load value is the ratio of the total execution time (in seconds) of all queries in a specific state in an interval by the total time (in seconds) for that interval.

For example, if 276 seconds was the total time for 4 queries in a 5 minute (300 second) interval, then the query load value is 276 / 300 = 0.92.

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The start of the specified time range (in the UTC time zone) in which the warehouse usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The end of the specified time range (in the UTC time zone) in which the warehouse usage took place. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse. |
| AVG\_RUNNING | NUMBER(38,2) | Query load value for queries executed. |
| AVG\_QUEUED\_LOAD | NUMBER(38,2) | Query load value for queries queued because the warehouse was overloaded. |
| AVG\_QUEUED\_PROVISIONING | NUMBER(38,2) | Query load value for queries queued because the warehouse was being provisioned. |
| AVG\_BLOCKED | NUMBER(38,2) | Query load value for queries blocked by a transaction lock. |

Expand

Show lessSee more

## Examples

Retrieve the load history for the last hour, in 5-second intervals, for the warehouse currently in use for your session:

> Copy code
>
> ```
> use warehouse mywarehouse;
>
> select *
> from table(information_schema.warehouse_load_history(date_range_start=>dateadd('hour',-1,current_timestamp())));
> ```

Retrieve the load history for the last 14 days, in 5-minute intervals, for the warehouse currently in use for your session:

> Copy code
>
> ```
> use warehouse mywarehouse;
>
> select *
> from table(information_schema.warehouse_load_history(date_range_start=>dateadd('day',-14,current_date()), date_range_end=>current_date()));
> ```
