Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# STRING\_LENGTH\_STDDEV (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the sample standard deviation of the string length of non-`NULL` values for the specified column in a table.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.STRING_LENGTH_STDDEV(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `FLOAT` value. `NULL` values are ignored. The function returns `NULL` if the column contains fewer than
two
non-`NULL` values.

## Example

Measure the standard deviation of string lengths in the `product_code` column:

Copy code

```
SELECT SNOWFLAKE.CORE.STRING_LENGTH_STDDEV(
  SELECT
    product_code
  FROM sales.tables.products
);
```
