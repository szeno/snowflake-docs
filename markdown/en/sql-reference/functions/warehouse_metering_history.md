Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# WAREHOUSE\_METERING\_HISTORY

This table function can be used in queries to return the hourly credit usage for a single warehouse (or all the warehouses in your account) within a specified date range.

Note

This function is generally deprecated in favor of the
[ACCOUNT\_USAGE.WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history),
which provides a more complete data set and supports longer date ranges.

Note

This function does not include credit usage for [Adaptive Warehouses](/user-guide/warehouses-adaptive).
To view Adaptive Warehouse usage, use the
[ACCOUNT\_USAGE.WAREHOUSE\_METERING\_HISTORY view](/sql-reference/account-usage/warehouse_metering_history).

See also:
:   [WAREHOUSE\_LOAD\_HISTORY](/sql-reference/functions/warehouse_load_history)

## Syntax

Copy code

```
WAREHOUSE_METERING_HISTORY(
      DATE_RANGE_START => <constant_expr>
      [ , DATE_RANGE_END => <constant_expr> ]
      [ , WAREHOUSE_NAME => '<string>' ] )
```

## Arguments

**Required:**

`DATE_RANGE_START => constant_expr`
:   The starting date, within the last 6 months, for which warehouse usage is returned.

**Optional:**

`DATE_RANGE_END => constant_expr`
:   The ending date, within the last 6 months, for which warehouse usage is returned.

    Default: [CURRENT\_DATE](/sql-reference/functions/current_date) is used.

`WAREHOUSE_NAME => 'string'`
:   The name of the warehouse to retrieve credit usage for. Note that the warehouse name must be enclosed in single quotes. Also, if the warehouse name any spaces, mixed-case characters,
    or special characters, the name must be double-quoted within the single quotes (e.g. `'"My Warehouse"'` vs `'mywarehouse'`).

    Default: All warehouses that ran during the specified date range.

## Usage notes

- Returns results only for the ACCOUNTADMIN role or any role that has been explicitly granted the MONITOR USAGE global privilege.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).
- The order and structure of the arguments depends on whether the argument keywords (e.g. `DATE_RANGE_START`) are included:
  - The keywords are not required if the arguments are specified in order.
  - If the argument keywords are included, the arguments can be specified in any order.

## Output

The function returns the following columns, ordered by WAREHOUSE\_NAME and START\_TIME:

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The beginning of the hour in which this warehouse usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The end of the hour in which this warehouse usage took place. |
| WAREHOUSE\_NAME | VARCHAR | Name of the warehouse. |
| CREDITS\_USED | NUMBER | Number of credits billed for this warehouse in this hour. |
| CREDITS\_USED\_COMPUTE | NUMBER | Number of credits used for the warehouse in the hour. |
| CREDITS\_USED\_CLOUD\_SERVICES | NUMBER | Number of credits used for cloud services in the hour. |

Expand

Show lessSee more

## Examples

Retrieve hourly warehouse usage over the past 10 days for all warehouses that ran during this time period:

> Copy code
>
> ```
> select *
> from table(information_schema.warehouse_metering_history(dateadd('days',-10,current_date())));
> ```

Retrieve hourly warehouse usage for the `testingwh` warehouse on a specified date:

> Copy code
>
> ```
> select *
> from table(information_schema.warehouse_metering_history('2017-10-23', '2017-10-23', 'testingwh'));
> ```
