Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# SPECIAL\_CHARACTER\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of non-NULL column values that contain characters outside the alphanumeric range (not `A`-`Z`,
`a`-`z`, or `0`-`9`). The percentage is computed over the total row count, including NULL values in the denominator.
Spaces, punctuation, and Unicode characters are all counted as special.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.SPECIAL_CHARACTER_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a FLOAT value.

## Example

Measure the percentage of values in the `product_code` column containing special characters:

Copy code

```
SELECT SNOWFLAKE.CORE.SPECIAL_CHARACTER_PERCENT(
  SELECT
    product_code
  FROM inventory.tables.products
);
```
