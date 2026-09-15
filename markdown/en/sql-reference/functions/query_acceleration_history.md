Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# QUERY\_ACCELERATION\_HISTORY

[Enterprise Edition Feature](/user-guide/intro-editions)

The [query acceleration service](/user-guide/query-acceleration-service) requires Enterprise Edition (or higher).
To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

The QUERY\_ACCELERATION\_HISTORY function is used for querying the [query acceleration service](/user-guide/query-acceleration-service)
history within a specified date range. The information returned includes the credits used for the query acceleration service at the
warehouse level for a given time frame.

Note

This function is generally deprecated in favor of the
[ACCOUNT\_USAGE.QUERY\_ACCELERATION\_HISTORY view](/sql-reference/account-usage/query_acceleration_history),
which provides a more complete data set and supports longer date ranges.

## Syntax

Copy code

```
QUERY_ACCELERATION_HISTORY(
      [ DATE_RANGE_START => <constant_expr> ]
      [ , DATE_RANGE_END => <constant_expr> ]
      [ , WAREHOUSE_NAME => '<string>' ] )
```

## Parameters

All the arguments are optional.

`DATE_RANGE_START => constant_expr` , `DATE_RANGE_END => constant_expr`
:   The date/time range to display the query acceleration history.

    For example, if you specify that the start date is 2019-05-03 and the end date 2019-05-05, you will get data for May 3, May 4, and May 5.
    (The endpoints are included.)

    - If neither a start date nor an end date is specified, the default will be the last 12 hours.
    - If an end date is not specified, but a start date is specified, then [CURRENT\_DATE](/sql-reference/functions/current_date)
      at midnight is used as the end of the range.
    - If a start date is not specified, but an end date is specified, then the range starts 12 hours prior to the start
      of `DATE_RANGE_END`.

`WAREHOUSE_NAME => string`
:   Warehouse name. If specified, only shows the history for the specified warehouse.

    If a warehouse name is not specified, then the results will include history for each warehouse using the query acceleration service.

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range in which the service was in use. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range in which the service was in use. |
| CREDITS\_USED | NUMBER | Number of credits used by the service. |
| WAREHOUSE\_NAME | TEXT | Name of the warehouse where usage occurred. |
| NUM\_FILES\_SCANNED | NUMBER | Number of files scanned by the service. |
| NUM\_BYTES\_SCANNED | NUMBER | Number of bytes scanned by the service. |

Expand

Show lessSee more

## Usage notes

- Returns results only for the ACCOUNTADMIN role or any role that has been explicitly granted the MONITOR USAGE global privilege.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name
  must be fully-qualified. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).
