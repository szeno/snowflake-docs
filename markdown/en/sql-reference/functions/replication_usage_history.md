Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# REPLICATION\_USAGE\_HISTORY

Deprecated Feature

This function has been deprecated. Use [DATABASE\_REPLICATION\_USAGE\_HISTORY](/sql-reference/functions/database_replication_usage_history) instead.

This table function can be used to query the replication history for a specified database within a specified date range. The information returned by the function includes the database name, credits consumed and bytes transferred for replication.

Note

This function returns replication usage activity within the last 14 days.

## Syntax

Copy code

```
REPLICATION_USAGE_HISTORY(
  [ DATE_RANGE_START => <constant_expr> ]
  [ , DATE_RANGE_END => <constant_expr> ]
  [ , DATABASE_NAME => '<string>' ] )
```

## Arguments

All the arguments are optional.

`DATE_RANGE_START => constant_expr` , `DATE_RANGE_END => constant_expr`
:   The date/time range to display the database replication history:

    - If an end date is not specified, then [CURRENT\_DATE](/sql-reference/functions/current_date) is used as the end of the range.
    - If a start date is not specified, then the range starts 10 minutes prior to the start of `DATE_RANGE_END` (i.e. the default is to show the previous 10 minutes of history).

    For example, if `DATE_RANGE_END` is CURRENT\_DATE, then the default `DATE_RANGE_START` is 11:50 PM on the previous day.

`DATABASE_NAME => 'string'`
:   Database name. If specified, only shows the history for the specified database.

    If a name is not specified, then the results include the data for each database replicated within the specified time range.

## Output

The function returns the following elements in a JSON object:

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range. |
| DATABASE\_NAME | TEXT | Name of the database. |
| CREDITS\_USED | TEXT | Number of credits billed for database replication during the START\_TIME and END\_TIME window. |
| BYTES\_TRANSFERRED | NUMBER | Number of bytes transferred for database replication during the START\_TIME and END\_TIME window. |

Expand

Show lessSee more

## Usage notes

- Returns results only for the ACCOUNTADMIN role or any role that has been explicitly granted the MONITOR USAGE global privilege.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).

## Examples

Retrieve the replication history for a 30 minute range for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.replication_usage_history(
>     date_range_start=>'2019-02-10 12:00:00.000 +0000',
>     date_range_end=>'2019-02-10 12:30:00.000 +0000'));
> ```

Retrieve the history for the last 12 hours for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.replication_usage_history(
>     date_range_start=>dateadd(H, -12, current_timestamp)));
> ```

Retrieve the history for the past week for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.replication_usage_history(
>     date_range_start=>dateadd(d, -7, current_date),
>     date_range_end=>current_date));
> ```

Retrieve the replication history for the past week for a specified database in your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.replication_usage_history(
>     date_range_start=>dateadd(d, -7, current_date),
>     date_range_end=>current_date,
>     database_name=>'mydb'));
> ```
