Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# NOT\_YESTERDAY\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are not on the day before the date of the scheduled evaluation time. The
percentage is
computed over the total row count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.NOT_YESTERDAY_PERCENT(<query>)
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

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- The function compares the date of each value with the day before the date of the scheduled evaluation time. Values on any
  other
  date, earlier or later, are counted.
- For a `TIMESTAMP_TZ` value, the value is converted to `TIMESTAMP_LTZ`, so its date is determined in the session time zone
  (the same time zone used for the scheduled evaluation time), not from its own offset.
- When you call the function directly, the current timestamp is used as the scheduled evaluation time.

## Example

Measure the percentage of values that are not from the previous day in the `business_date` column:

Copy code

```
SELECT SNOWFLAKE.CORE.NOT_YESTERDAY_PERCENT(
  SELECT
    business_date
  FROM finance.tables.daily_positions
);
```
