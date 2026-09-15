Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions), [Table functions](/sql-reference/functions-table)

# AUTOMATIC\_CLUSTERING\_HISTORY

This table function is used for querying the [Automatic Clustering](/user-guide/tables-auto-reclustering) history for given tables within a specified date range. The information returned by the function includes the
credits consumed, bytes updated, and rows updated each time a table is reclustered.

Note

This function does not include Optima Clustering data and is deprecated in favor of the
[ACCOUNT\_USAGE.AUTOMATIC\_CLUSTERING\_HISTORY view](/sql-reference/account-usage/automatic_clustering_history),
which provides a more complete data set and supports longer date ranges.

## Syntax

Copy code

```
AUTOMATIC_CLUSTERING_HISTORY(
      [ DATE_RANGE_START => <constant_expr> ]
      [ , DATE_RANGE_END => <constant_expr> ]
      [ , TABLE_NAME => '<string>' ] )
```

## Arguments

All the arguments are optional.

`DATE_RANGE_START => constant_expr` , `DATE_RANGE_END => constant_expr`
:   The date/time range to display the Automatic Clustering history.
    For example, if you specify that the start date is 2019-04-03 and the end date is 2019-04-05, then you get data for
    April 3, April 4, and April 5. (The endpoints are included.)

    - If neither a start date nor an end date is specified, the default is the last 12 hours.
    - If an end date is not specified, but a start date is specified, then [CURRENT\_DATE](/sql-reference/functions/current_date)
      at midnight is used as the end of the range.
    - If a start date is not specified, but an end date is specified, then the range starts 12 hours prior to the start
      of `DATE_RANGE_END`.

`TABLE_NAME => string`
:   Table name. If specified, only shows the history for the specified table.
    The table name can include the schema name and the database name.

    If a table name is not specified, then the results include history for each table maintained by the
    Automatic Clustering Service within the specified time range.

## Usage notes

- Returns results only for the ACCOUNTADMIN role or any role that has been explicitly granted the MONITOR USAGE global privilege.

  Note

  A role with the MONITOR USAGE privilege can view per-object credit usage, but not object names. The role must also be granted SELECT on an object in order for its name to be returned by this function. If the role does not have sufficient privileges to see the object name, the object name might be displayed with a substitute name such as “unknown\_#”, where “#” represents one or more digits.
- When calling an Information Schema table function, the session must have an INFORMATION\_SCHEMA schema in use or the function name must be fully qualified. For more details, see
  [Snowflake Information Schema](/sql-reference/info-schema).
- The history is displayed in increments of 1 hour.
- A row might be clustered multiple times, depending on data skew, clustering key distribution, and reordering required for micro-partitions. A large table with poor initial clustering might need multiple passes to reach an optimally clustered state. Therefore, the NUM\_ROWS\_RECLUSTERED value for a table could be as high as the total number of rows in the table or even higher.

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | Start of the specified time range. |
| END\_TIME | TIMESTAMP\_LTZ | End of the specified time range. |
| TABLE\_NAME | TEXT | Name of the table. Displays NULL if no table name is specified in the function, in which case each row includes the totals for all tables in use within the time range. |
| CREDITS\_USED | NUMBER | Number of credits billed for automatic clustering during the START\_TIME and END\_TIME window. |
| NUM\_BYTES\_RECLUSTERED | NUMBER | Number of bytes reclustered during the START\_TIME and END\_TIME window. |
| NUM\_ROWS\_RECLUSTERED | NUMBER | Number of rows reclustered during the START\_TIME and END\_TIME window. |

Expand

Show lessSee more

## Examples

Retrieve the automatic clustering history for a one-hour range for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.automatic_clustering_history(
>     date_range_start=>'2018-04-10 13:00:00.000 -0700',
>     date_range_end=>'2018-04-10 14:00:00.000 -0700'));
> ```

Retrieve the automatic clustering history for the last 12 hours, in 1 hour periods, for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.automatic_clustering_history(
>     date_range_start=>dateadd(H, -12, current_timestamp)));
> ```

Retrieve the automatic clustering history for the past week for your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.automatic_clustering_history(
>     date_range_start=>dateadd(D, -7, current_date),
>     date_range_end=>current_date));
> ```

Retrieve the automatic clustering history for the past week for a specified table in your account:

> Copy code
>
> ```
> select *
>   from table(information_schema.automatic_clustering_history(
>     date_range_start=>dateadd(D, -7, current_date),
>     date_range_end=>current_date,
>     table_name=>'mydb.myschema.mytable'));
> ```
