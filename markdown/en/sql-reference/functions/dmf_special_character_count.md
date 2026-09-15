Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# SPECIAL\_CHARACTER\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-NULL column values that contain characters outside the alphanumeric range (not `A`-`Z`, `a`-`z`,
or `0`-`9`). Spaces, punctuation, and Unicode characters are all counted as special. Use this function to validate columns
that should be alphanumeric only (identifiers, codes).

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.SPECIAL_CHARACTER_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a NUMBER value. NULL values are excluded from the count.

## Example

Measure the number of values in the `product_code` column containing special characters:

Copy code

```
SELECT SNOWFLAKE.CORE.SPECIAL_CHARACTER_COUNT(
  SELECT
    product_code
  FROM inventory.tables.products
);
```
