Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# AUTO\_REFRESH\_REGISTRATION\_HISTORY

This table function can be used to query the history of data files registered in the metadata for a specified external table
or directory table and the credits billed
for these operations. The table function returns the billing history for a specified range
within the last 14 days for your entire Snowflake account.

Note

To retrieve refresh history information for an Apache Iceberg™ table,
see [ICEBERG\_TABLE\_SNAPSHOT\_REFRESH\_HISTORY](/sql-reference/functions/iceberg_table_snapshot_refresh_history) instead.

Note

This function is generally deprecated in favor of the
[ACCOUNT\_USAGE.CATALOG\_LINKED\_DATABASE\_USAGE\_HISTORY view](/sql-reference/account-usage/catalog_linked_database_usage_history),
which provides a more complete data set and supports longer date ranges.

## Syntax

Copy code

```
AUTO_REFRESH_REGISTRATION_HISTORY(
      [ DATE_RANGE_START => <constant_expr> ]
      [, DATE_RANGE_END => <constant_expr> ]
      [, OBJECT_TYPE => '<string>' [, OBJECT_NAME => '<string>'] ])
```

## Arguments

All of the arguments are optional.

`DATE_RANGE_START => constant_expr` , `DATE_RANGE_END => constant_expr`
:   The date/time range of the billing window:

    - If an end date is not specified, then [CURRENT\_DATE](/sql-reference/functions/current_date) is used as the end of the range.
    - If a start date is not specified, then the range starts 10 minutes prior to the start of `DATE_RANGE_END` (i.e. the default is to
      show the previous 10 minutes of the billing history). For example, if `DATE_RANGE_END` is [CURRENT\_DATE](/sql-reference/functions/current_date), then the default
      `DATE_RANGE_START` is 11:50 PM on the previous day.

    History is displayed in increments of 5 minutes, 1 hour, or 24 hours (depending on the length of the specified range).

`OBJECT_TYPE => string`
:   Type of object for which credits are billed. The following value is supported:

    `DIRECTORY_TABLE`
    :   Directory tables that are configured for automatic metadata refreshes.

    `EXTERNAL_TABLE`
    :   External tables that are configured for automatic metadata refreshes.

`OBJECT_NAME => string`
:   A string specifying the name of the external table or directory table for which credits are billed.

## Usage notes

- Returns results only for the ACCOUNTADMIN role or any role that has been explicitly granted the MONITOR USAGE global privilege.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name
  must be fully-qualified. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified billing window. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified billing window. |
| OBJECT\_NAME | TEXT | Name of the object for which credits are billed. |
| OBJECT\_TYPE | TEXT | Type of object for which credits are billed. |
| CREDITS\_USED | TEXT | Number of credits billed for data files registered in the metadata of the specified object or object type during the START\_TIME and END\_TIME window. |
| FILES\_REGISTERED | NUMBER | Number of files registered during the START\_TIME and END\_TIME window. |

Expand

Show lessSee more

## Examples

Note that all of the examples in this topic reference external table metadata. To retrieve similar history records for
other object types, edit the `OBJECT_TYPE => string` value in the query.

Retrieve the billing history for all external tables in your account that are configured for automatic metadata refreshes. The query retrieves
the history for a 30 minute range, in 5 minute periods:

> Copy code
>
> ```
> select *
>   from table(information_schema.auto_refresh_registration_history(
>     date_range_start=>to_timestamp_tz('2021-06-17 12:00:00.000 -0700'),
>     date_range_end=>to_timestamp_tz('2021-06-17 12:30:00.000 -0700'),
>     object_type=>'external_table'));
> ```

Same as the previous example, but retrieves the billing history for the last 14 days, in 1 day periods:

> Copy code
>
> ```
> select *
>   from table(information_schema.auto_refresh_registration_history(
>     date_range_start=>dateadd('day',-14,current_date()),
>     date_range_end=>current_date(),
>     object_type=>'external_table'));
> ```

Same as the first example, but retrieves the billing history for the last 14 days, in 1 day periods:

> Copy code
>
> ```
> select *
>   from table(information_schema.auto_refresh_registration_history(
>     date_range_start=>dateadd('day',-14,current_date()),
>     date_range_end=>current_date(),
>     object_type=>'external_table'));
> ```

Retrieve the billing history for an external table named `myexttable` in the active schema in the session for the last 12 hours, in 1
hour periods:

> Copy code
>
> ```
> select *
>   from table(information_schema.auto_refresh_registration_history(
>     date_range_start=>dateadd('hour',-12,current_timestamp()),
>     object_type=>'external_table',
>     object_name=>'myexttable'));
> ```

Retrieve the billing history for an external table named `myexttable` in the `mydb.myschema` schema for the last 12 hours, in 1 hour
periods:

> Copy code
>
> ```
> select *
>   from table(information_schema.auto_refresh_registration_history(
>     date_range_start=>dateadd('hour',-12,current_timestamp()),
>     object_type=>'external_table',
>     object_name=>'mydb.myschema.myexttable'));
> ```
