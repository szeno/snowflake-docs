Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_NUMERIC\_TYPE\_CAST\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of non-NULL column values that cannot be parsed as numeric. The percentage is computed over the total row
count, including NULL values in the denominator.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_NUMERIC_TYPE_CAST_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a FLOAT value.

## Example

Measure the percentage of values in the `quantity_str` column that cannot be cast to a number:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_NUMERIC_TYPE_CAST_PERCENT(
  SELECT
    quantity_str
  FROM staging.tables.csv_imports
);
```
