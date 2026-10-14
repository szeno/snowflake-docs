Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# ROWS\_IN\_PAST\_HOUR\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-`NULL` column values that fall in the hour before the scheduled evaluation time.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.ROWS_IN_PAST_HOUR_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- `TIMESTAMP_LTZ`
- `TIMESTAMP_TZ`

## Returns

The function returns a `NUMBER` value. `NULL` values are not counted.

## Usage notes

- The window starts 1 hour before the scheduled evaluation time and ends at the scheduled evaluation time; both boundaries are
  included. Values later than the scheduled evaluation time are not counted.
- Unlike most system DMFs, this function counts rows that meet the expectation: a value of 0 means that no rows arrived in the
  window.

## Example

Measure the number of rows that arrived in the past hour in the `ingested_at` column:

Copy code

```
SELECT SNOWFLAKE.CORE.ROWS_IN_PAST_HOUR_COUNT(
  SELECT
    ingested_at
  FROM events.tables.activity
);
```
