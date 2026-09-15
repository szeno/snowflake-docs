Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# REPLICATION\_GROUP\_USAGE\_HISTORY

[Standard & Business Critical Feature](/user-guide/intro-editions)

- Database and share replication are available to all accounts.
- Replication of other account objects & failover/failback require Business Critical Edition (or higher).
  To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the replication usage history for secondary replication or failover groups within the last 14 days.

Note

This function is generally deprecated in favor of the
[ACCOUNT\_USAGE.REPLICATION\_GROUP\_USAGE\_HISTORY view](/sql-reference/account-usage/replication_group_usage_history),
which provides a more complete data set and supports longer date ranges.

## Syntax

Copy code

```
REPLICATION_GROUP_USAGE_HISTORY(
   [ DATE_RANGE_START => <constant_expr> ]
   [, DATE_RANGE_END => <constant_expr> ]
   [, REPLICATION_GROUP_NAME => '<string>' ] )
```

## Arguments

All the arguments are optional.

`DATE_RANGE_START => constant_expr` , `DATE_RANGE_END => constant_expr`
:   The date/time range, within the last 2 weeks, for which to retrieve the data load history:

    - If an end date is not specified, then [CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp) is used as the end of the range.
    - If a start date is not specified, then the range starts 12 hours prior to the `DATE_RANGE_END`

`REPLICATION_GROUP_NAME => string`
:   A string specifying a replication or failover group. Only replication operations for the specified group are returned.

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range. |
| REPLICATION\_GROUP\_NAME | TEXT | Name of the replication group. |
| CREDITS\_USED | TEXT | Number of credits billed for replication during the START\_TIME and END\_TIME window. |
| BYTES\_TRANSFERRED | NUMBER | Number of bytes transferred for replication during the START\_TIME and END\_TIME window. |

Expand

Show lessSee more

## Usage notes

- Returns results only for the ACCOUNTADMIN role or any role that has been explicitly granted the MONITOR USAGE global privilege.
- Returns results only for a secondary replication or failover group in the current account.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name
  must be fully-qualified. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

Retrieve the replication usage history for the last 7 days:

> Copy code
>
> ```
> SELECT START_TIME, END_TIME, REPLICATION_GROUP_NAME, CREDITS_USED, BYTES_TRANSFERRED
>   FROM TABLE(information_schema.replication_group_usage_history(date_range_start=>dateadd('day', -7, current_date())));
> ```

Retrieve the replication usage history for the last 7 days for replication group `myrg`:

> Copy code
>
> ```
> SELECT START_TIME, END_TIME, REPLICATION_GROUP_NAME, CREDITS_USED, BYTES_TRANSFERRED
>   FROM TABLE(information_schema.replication_group_usage_history(
>     date_range_start => dateadd('day', -7, current_date()),
>     replication_group_name => 'myrg'
> ));
> ```
