Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# SEARCH\_OPTIMIZATION\_HISTORY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This table function is used for querying maintenance history for indexes maintained by the
[search optimization service](/user-guide/search-optimization-service) for a specified table within a specified date range. The
information returned by the function includes the index, the base table, and the credits consumed each time a maintenance
operation occurred.

Note

This function is generally deprecated in favor of the
[ACCOUNT\_USAGE.SEARCH\_OPTIMIZATION\_HISTORY view](/sql-reference/account-usage/search_optimization_history),
which provides a more complete data set and supports longer date ranges.

The `INDEX_ID`, `INDEX_NAME`, `INDEX_TYPE`, `BASE_TABLE_ID`, and `BASE_TABLE_NAME` columns replace `TABLE_NAME` when
[SEARCH\_OPTIMIZATION\_HISTORY views: New columns and column changes (Pending)](/release-notes/bcr-bundles/2026_06/bcr-2384) is enabled. If you have scripts that query `TABLE_NAME`, update them to use the new
column names.

## Syntax

Copy code

```
SEARCH_OPTIMIZATION_HISTORY(
      [ DATE_RANGE_START => <constant_expr> ]
      [ , DATE_RANGE_END => <constant_expr> ]
      [ , TABLE_NAME => '<string>' ] )
```

## Arguments

All the arguments are optional.

`DATE_RANGE_START => constant_expr` , `DATE_RANGE_END => constant_expr`
:   The date/time range for which to display the history.
    For example, if you specify that the start date is 2019-04-03 and the end date is 2019-04-05, then you get data for
    April 3, April 4, and April 5. (The endpoints are included.)

    - If neither a start date nor an end date is specified, the default is the last 12 hours.
    - If an end date is not specified, but a start date is specified, then [CURRENT\_DATE](/sql-reference/functions/current_date)
      at midnight is used as the end of the range.
    - If a start date is not specified, but an end date is specified, then the range starts 12 hours prior to the start
      of `DATE_RANGE_END`.

`TABLE_NAME => string`
:   The table name. If specified, only shows the history for the specified table. The name can include the schema name and the database
    name.

    If a name is not specified, then the results include the data for each table that has a search optimization service
    index for which maintenance occurred within the specified time range.

## Usage notes

- Returns results only for the ACCOUNTADMIN role or any role that has been explicitly granted the MONITOR USAGE
  global privilege.

  Note

  A role with the MONITOR USAGE privilege can view per-object credit usage, but not object names. The role must
  also be granted SELECT on an object in order for the object’s name to be returned by this function. If the role
  does not have sufficient privileges to see the object name, the object name might be displayed with a substitute
  name such as “unknown\_#”, where “#” represents one or more digits.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be
  fully-qualified. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).
- The history is displayed in increments of 1 hour.

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range. |
| CREDITS\_USED | TEXT | Number of credits billed for search optimization service index maintenance during the START\_TIME and END\_TIME window. |
| INDEX\_ID | NUMBER | Internal/system-generated identifier for the index. Replaces `TABLE_ID`. |
| INDEX\_NAME | TEXT | Name of the index. Replaces `TABLE_NAME`. For a search optimization index, this is a system-generated alias of the form `SEARCH OPTIMIZATION ON: <base_table_id>`. For a search optimization secondary index, this is the customer-defined index name. |
| INDEX\_TYPE | TEXT | Type of index maintained by the search optimization service. Possible values are `Search Optimization Index` and `Secondary Index`. `Secondary Index` is not a [hybrid table secondary index](/user-guide/tables-hybrid-index). |
| BASE\_TABLE\_ID | NUMBER | Internal/system-generated identifier for the base table. |
| BASE\_TABLE\_NAME | TEXT | Name of the base table. |

Expand

Show lessSee more

## Examples

Retrieve the history for a one-hour range for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.search_optimization_history(
>     date_range_start=>'2019-05-22 19:00:00.000',
>     date_range_end=>'2019-05-22 20:00:00.000'));
> ```
>
> Here is sample output:
>
> ```
> +-------------------------------+-------------------------------+--------------+---------+------------------------------+---------------------------+---------------+-----------------+
> | START_TIME                    | END_TIME                      | CREDITS_USED | INDEX_ID | INDEX_NAME                   | INDEX_TYPE                | BASE_TABLE_ID | BASE_TABLE_NAME |
> |-------------------------------+-------------------------------+--------------+---------+------------------------------+---------------------------+---------------+-----------------|
> | 2019-05-22 19:00:00.000 -0700 | 2019-05-22 20:00:00.000 -0700 |  0.223276651 |      42 | SEARCH OPTIMIZATION ON: 1200 | Search Optimization Index |          1200 | TEST_TABLE_1    |
> +-------------------------------+-------------------------------+--------------+---------+------------------------------+---------------------------+---------------+-----------------+
> ```

Retrieve the history for the last 12 hours for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.search_optimization_history(
>     date_range_start=>dateadd(H, -12, current_timestamp)));
> ```

Retrieve the history for the past week for a specified table:

> Copy code
>
> ```
> select *
>   from table(information_schema.search_optimization_history(
>     date_range_start=>dateadd(D, -7, current_date),
>     date_range_end=>current_date,
>     table_name=>'mydb.myschema.my_table')
>     );
> ```

Retrieve the maintenance history for the past week for all tables in your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.search_optimization_history(
>     date_range_start=>dateadd(D, -7, current_date),
>     date_range_end=>current_date)
>     );
> ```
