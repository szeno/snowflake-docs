Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# SKEW (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the sample skewness of the values in the specified column in a table.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.SKEW(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- `FLOAT`
- `NUMBER`

## Returns

The function returns a `FLOAT` value. `NULL` values are ignored. The function returns `NULL` if the column contains fewer than
three
non-`NULL` values, or if all of its values are the same.

## Usage notes

- The function uses the same sample formula as the [SKEW](/sql-reference/functions/skew) aggregate function. A symmetric
  distribution has a skewness of 0.

## Example

Measure the skewness in the `order_total` column:

Copy code

```
SELECT SNOWFLAKE.CORE.SKEW(
  SELECT
    order_total
  FROM sales.tables.orders
);
```
