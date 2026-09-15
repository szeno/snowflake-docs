Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# FRESHNESS (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns how much time in seconds has elapsed since a table was last modified.

When a column argument is specified, the time period is calculated by comparing the current run of the function with the maximum value of a
timestamp column. If the scheduled time to run the function is different than the time it actually ran, then the scheduled time is used for
the comparison.

When no column is specified, the time period is calculated by comparing the current run of the function with the last time a
[DML command](/sql-reference/sql-dml) acted on the table. If the scheduled time to run the function is different than the time it
actually ran, then the scheduled time is used for the comparison.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.FRESHNESS( [ <query> ] )
```

## Arguments

`query`
:   If specified, the query must project a single timestamp column.

    If you don’t want to specify a column, you must [associate the function with a table](/user-guide/data-quality-working#label-dmf-associate) rather than call
    it directly.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- DATE
- TIMESTAMP\_LTZ
- TIMESTAMP\_TZ

## Returns

The function returns a scalar value with a NUMBER data type.

## Usage notes

- You must specify a column argument if you want to associate this function with a view or external table.
- This function can be called directly only if you specify a query that projects a timestamp column. If you want to associate the function
  with a table or view so it runs at regular intervals with or without a column argument, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Example

Associate the function with the table `t1` to determine how long it’s been since the last DML operation on the table:

Copy code

```
ALTER TABLE t1
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.FRESHNESS on ();
```

Call the function directly to determine the freshness of the data, 300 seconds or 5 minutes, in the table by measuring the
`TIMESTAMP` column:

Copy code

```
SELECT SNOWFLAKE.CORE.FRESHNESS(
  SELECT
    timestamp
  FROM hr.tables.empl_info
) < 300;
```

```
+---------------------------------------------------------------------+
| SNOWFLAKE.CORE.FRESHNESS(SELECT timestamp FROM hr.tables.empl_info) |
+---------------------------------------------------------------------+
| True                                                                |
+---------------------------------------------------------------------+
```
