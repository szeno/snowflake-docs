Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# DATA\_TRANSFER\_HISTORY

This table function can be used to query the history of data transferred from Snowflake tables into a different cloud storage provider’s network (i.e. from Snowflake on AWS, Google Cloud Platform, or Microsoft Azure into the other cloud provider’s network) and/or geographical region within a specified date range. The function returns the history for your entire Snowflake account.

Note

This function returns data transfer activity within the last 14 days.

Note

This function is generally deprecated in favor of the
[ACCOUNT\_USAGE.DATA\_TRANSFER\_HISTORY view](/sql-reference/account-usage/data_transfer_history),
which provides a more complete data set and supports longer date ranges.

## Syntax

Copy code

```
DATA_TRANSFER_HISTORY(
      [ DATE_RANGE_START => <constant_expr> ]
      [, DATE_RANGE_END => <constant_expr> ] )
```

## Arguments

All the arguments are optional.

`DATE_RANGE_START => constant_expr` , `DATE_RANGE_END => constant_expr`
:   The date/time range, within the last 2 weeks, for which to retrieve the data transfer history:

    - If an end date is not specified, then [CURRENT\_DATE](/sql-reference/functions/current_date) is used as the end of the range.
    - If a start date is not specified, then the range starts 10 minutes prior to the start of `DATE_RANGE_END` (i.e. the default is to show the previous 10 minutes of data transfer history).
      For example, if `DATE_RANGE_END` is [CURRENT\_DATE](/sql-reference/functions/current_date), then the default `DATE_RANGE_START` is 11:50 PM on the previous day.

    History is displayed in increments of 5 minutes, 1 hour, or 24 hours (depending on the length of the specified range).

    If the range falls outside the last 15 days, an error is returned.

## Usage notes

- Returns results only for the ACCOUNTADMIN role or any role that has been explicitly granted the MONITOR USAGE global privilege.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully-qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range in which the data transfer took place. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range in which the data transfer took place. |
| SOURCE\_CLOUD | TEXT | Name of the cloud provider where the data transfer originated: Amazon Web Services, Google Cloud Platform, or Microsoft Azure. |
| SOURCE\_REGION | TEXT | Region where the data transfer originated. |
| TARGET\_CLOUD | TEXT | Name of the cloud provider where the data was sent: AWS, Google Cloud Platform, or Microsoft Azure. |
| TARGET\_REGION | TEXT | Region where the data was sent. |
| BYTES\_TRANSFERRED | NUMBER | Number of bytes transferred during the START\_TIME and END\_TIME window. |
| TRANSFER\_TYPE | VARCHAR | Type of operation that caused transfer. [COPY](/sql-reference/sql/copy-into-location), [EXTERNAL\_ACCESS](/developer-guide/external-network-access/external-network-access-overview), [EXTERNAL\_FUNCTION](/sql-reference/external-functions), [REPLICATION](/user-guide/account-replication-intro). |

Expand

Show lessSee more

## Examples

Retrieve the data transfer history for a 30 minute range, in 5 minute periods, for your account:

> Copy code
>
> ```
> select *
>   from table(mydb.information_schema.data_transfer_history(
>     date_range_start=>to_timestamp_tz('2017-10-24 12:00:00.000 -0700'),
>     date_range_end=>to_timestamp_tz('2017-10-24 12:30:00.000 -0700')));
> ```

Retrieve the data transfer history for the last 12 hours, in 1 hour periods, for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.data_transfer_history(
>     date_range_start=>dateadd('hour',-12,current_timestamp())));
> ```

Retrieve the data transfer history for the last 14 days, in 1 day periods, for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.data_transfer_history(
>     date_range_start=>dateadd('day',-14,current_date()),
>     date_range_end=>current_date()));
> ```
