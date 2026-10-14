Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# ROWS\_IN\_PAST\_WEEK\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that fall in the 7 days before the scheduled evaluation time. The percentage is computed
over the total row count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.ROWS_IN_PAST_WEEK_PERCENT(<query>)
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

- For a `TIMESTAMP_LTZ` or `TIMESTAMP_TZ` column, the window starts 7 days before the scheduled evaluation time and ends at
  the scheduled evaluation time; both boundaries are included. Values later than the scheduled evaluation time are not
  counted.
- For a `DATE` column, the window is the 7 calendar days that end on the date of the scheduled evaluation time, including that
  date.
- Unlike most system DMFs, this function measures values that meet the expectation: a value of 0 means that no rows arrived in
  the
  window.
- When you call the function directly, the current timestamp is used as the scheduled evaluation time.

## Example

Measure the percentage of rows that arrived in the past 7 days in the `ingested_at` column:

Copy code

```
SELECT SNOWFLAKE.CORE.ROWS_IN_PAST_WEEK_PERCENT(
  SELECT
    ingested_at
  FROM events.tables.activity
);
```
