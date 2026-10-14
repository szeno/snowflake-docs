Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_PERCENTAGE\_RANGE\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-`NULL` column values that are outside the range for a percentage, 0 to 100 inclusive.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_PERCENTAGE_RANGE_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- `FLOAT`
- `NUMBER`

## Returns

The function returns a `NUMBER` value. `NULL` values are not counted.

## Usage notes

- The values 0 and 100 are in range.
- NaN values are counted as out of range.
- For percentages stored as a fraction from 0 to 1, use
  [INVALID\_PROBABILITY\_RANGE\_COUNT](/sql-reference/functions/dmf_invalid_probability_range_count).

## Example

Measure the number of out-of-range percentages in the `discount_pct` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_PERCENTAGE_RANGE_COUNT(
  SELECT
    discount_pct
  FROM sales.tables.orders
);
```
