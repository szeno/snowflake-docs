Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# NOT\_TODAY\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-`NULL` column values that are not on the date of the scheduled evaluation time.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.NOT_TODAY_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- `DATE`
- `TIMESTAMP_LTZ`
- `TIMESTAMP_TZ`

## Returns

The function returns a `NUMBER` value. `NULL` values are not counted.

## Usage notes

- The function compares the date of each value with the date of the scheduled evaluation time. Values on earlier and later
  dates are
  both counted.
- For a `TIMESTAMP_TZ` value, the value is converted to `TIMESTAMP_LTZ`, so its date is determined in the session time zone
  (the same time zone used for the scheduled evaluation time), not from its own offset.
- When you call the function directly, the current timestamp is used as the scheduled evaluation time.

## Example

Measure the number of values that are not from the scheduled date in the `load_date` column:

Copy code

```
SELECT SNOWFLAKE.CORE.NOT_TODAY_COUNT(
  SELECT
    load_date
  FROM etl.tables.daily_snapshot
);
```
