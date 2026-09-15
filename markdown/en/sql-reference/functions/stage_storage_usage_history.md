Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# STAGE\_STORAGE\_USAGE\_HISTORY

This table function can be used to query the average daily data storage usage, in bytes, for all the Snowflake stages in your account within a specified date range. The output will include storage for:

- Named internal stages.
- Default staging areas (for tables and users).

Note

This function returns stage storage usage within the last 6 months.

Note

This function is generally deprecated in favor of the
[ACCOUNT\_USAGE.STAGE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/stage_storage_usage_history),
which provides a more complete data set and supports longer date ranges.

See also:
:   [DATABASE\_STORAGE\_USAGE\_HISTORY](/sql-reference/functions/database_storage_usage_history) , [WAREHOUSE\_METERING\_HISTORY](/sql-reference/functions/warehouse_metering_history)

## Syntax

Copy code

```
STAGE_STORAGE_USAGE_HISTORY(
      [ DATE_RANGE_START => <constant_expr> ]
      [, DATE_RANGE_END => <constant_expr> ] )
```

## Arguments

All the arguments are optional.

`DATE_RANGE_START => constant_expr` , `DATE_RANGE_END => constant_expr`
:   The date range, within the last 6 months, for which to retrieve stage storage usage:

    - If an end date is not specified, then [CURRENT\_DATE](/sql-reference/functions/current_date) is used as the end of the range.
    - If a start date is not specified, then `DATE_RANGE_END` is used as the start of the range (i.e. the default is one day of storage usage).

    If the range falls outside the last 6 months, an error is returned.

## Usage notes

- Returns results only for the ACCOUNTADMIN role or any role that has been explicitly granted the MONITOR USAGE global privilege.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| USAGE\_DATE | DATE | Date (in the UTC time zone) of this storage usage record |
| AVERAGE\_STAGE\_BYTES | NUMBER | Number of bytes of stage storage used |

Expand

Show lessSee more

## Examples

Retrieve average daily storage usage for the past 10 days for all internal stages in your account:

Copy code

```
select *
from table(information_schema.stage_storage_usage_history(dateadd('days',-10,current_date()),current_date()));
```
