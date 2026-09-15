Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# STRING\_LENGTH\_MAX (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the maximum string length of non-NULL values for the specified column in a table. Use this function to detect overflow or
unexpectedly long values.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.STRING_LENGTH_MAX(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a NUMBER value. If all values in the column are NULL, the function returns NULL.

## Example

Measure the maximum string length for the `code` column:

Copy code

```
SELECT SNOWFLAKE.CORE.STRING_LENGTH_MAX(
  SELECT
    code
  FROM inventory.tables.products
);
```
