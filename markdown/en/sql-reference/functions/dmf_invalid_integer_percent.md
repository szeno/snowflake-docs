Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_INTEGER\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of column values that are not an integer: an optional sign followed by digits. The percentage is
computed over the total row count, including `NULL` values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_INTEGER_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the `VARCHAR` data type.

## Returns

The function returns a `FLOAT` value. The function returns `NULL` if the table or view has no rows.

## Usage notes

- The value must be an optional `+` or `-` sign followed by one or more digits. Leading zeros are allowed.
- Decimals such as `3.7`, exponent notation such as `1e5`, thousands separators, surrounding whitespace, and the empty string
  are
  counted.
- The function checks the format only; it does not check whether the value fits in a `NUMBER` column. To check whether values
  can be
  cast to a number, use [INVALID\_NUMERIC\_TYPE\_CAST\_PERCENT](/sql-reference/functions/dmf_invalid_numeric_type_cast_percent).

## Example

Measure the percentage of values that are not whole integers in the `quantity` column:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_INTEGER_PERCENT(
  SELECT
    quantity
  FROM sales.tables.order_lines
);
```
