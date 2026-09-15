Categories:
:   [Information Schema](/sql-reference/info-schema#label-info-schema-functions) , [Table functions](/sql-reference/functions-table)

# DATABASE\_STORAGE\_USAGE\_HISTORY

This table function can be used to query the average daily storage usage, in bytes, for a single database (or all the databases in your account) within a specified date range. The results include:

- All data stored in tables and materialized views in the database(s).
- All historical data maintained in Fail-safe for the database(s).

Note

This function returns storage usage within the last 6 months.

Note

This function is generally deprecated in favor of the
[ACCOUNT\_USAGE.DATABASE\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/database_storage_usage_history),
which provides a more complete data set and supports longer date ranges.

See also:
:   [STAGE\_STORAGE\_USAGE\_HISTORY](/sql-reference/functions/stage_storage_usage_history) , [WAREHOUSE\_METERING\_HISTORY](/sql-reference/functions/warehouse_metering_history)

## Syntax

Copy code

```
DATABASE_STORAGE_USAGE_HISTORY(
      [ DATE_RANGE_START => <constant_expr> ]
      [, DATE_RANGE_END => <constant_expr> ]
      [, DATABASE_NAME => '<string>' ] )
```

## Arguments

All the arguments are optional.

`DATE_RANGE_START => constant_expr` , `DATE_RANGE_END => constant_expr`
:   The date range, within the last 6 months, for which to retrieve database storage usage:

    - If an end date is not specified, [CURRENT\_DATE](/sql-reference/functions/current_date) is used as the end of the range.
    - If a start date is not specified, `DATE_RANGE_END` is used as the start of the range (that is, the default is one day of storage usage).

    If the range falls outside the last 6 months, an error is returned.

`DATABASE_NAME => 'string'`
:   The name of the database to retrieve storage usage history for. Note that the database name must be enclosed in single quotes. Also, if the database name contains any spaces, mixed-case characters,
    or special characters, the name must be double-quoted within the single quotes (for example, `'"My DB"'` vs `'mydb'`).

    If no database is specified, data is returned for all the databases in your account.

## Usage notes

- Returns results only for the ACCOUNTADMIN role or any role that has been explicitly granted the MONITOR USAGE global privilege.
- To call an Information Schema table function, your session must have an INFORMATION\_SCHEMA schema in use *or* the function name must be fully-qualified. For more details, see [Snowflake Information Schema](/sql-reference/info-schema).

## Output

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| USAGE\_DATE | DATE | Date of this storage usage record. |
| DATABASE\_NAME | TEXT | Name of the database. |
| AVERAGE\_DATABASE\_BYTES | NUMBER | Number of bytes of database storage used, including bytes currently in Time Travel. |
| AVERAGE\_FAILSAFE\_BYTES | NUMBER | Number of bytes of Fail-safe storage used. |

Expand

Show lessSee more

If a database has been dropped and its data retention period has passed (that is, the database cannot be recovered using Time Travel), then the database name is reported as `DROPPED_id`, where `id` is an internally-generated identifier. This ID can be used to match entries across rows returned by the table function.

## Examples

Retrieve average daily storage usage for the past 10 days, per database, for all databases in your account:

Copy code

```
SELECT *
  FROM TABLE(INFORMATION_SCHEMA.DATABASE_STORAGE_USAGE_HISTORY(DATEADD('days',-10,CURRENT_DATE()),CURRENT_DATE()));
```
