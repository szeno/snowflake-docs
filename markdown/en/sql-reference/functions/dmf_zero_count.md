Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# ZERO\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of column values that are equal to zero for the specified column in a table. Use this function to detect missing
or placeholder data in numeric columns.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.ZERO_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- FLOAT
- NUMBER

## Returns

The function returns a NUMBER value. NULL values are not counted as zero.

## Example

Measure the number of zero values in the `amount` column:

Copy code

```
SELECT SNOWFLAKE.CORE.ZERO_COUNT(
  SELECT
    amount
  FROM sales.tables.orders
);
```
