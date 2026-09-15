Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# ZERO\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are equal to zero for the specified column in a table. The percentage is computed
over the total row count, including NULL values in the denominator. NULL values are not counted as zero.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.ZERO_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- FLOAT
- NUMBER

## Returns

The function returns a FLOAT value.

## Example

Measure the percentage of zero values in the `amount` column:

Copy code

```
SELECT SNOWFLAKE.CORE.ZERO_PERCENT(
  SELECT
    amount
  FROM sales.tables.orders
);
```
