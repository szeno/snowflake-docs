Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# INVALID\_NUMERIC\_TYPE\_CAST\_COUNT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the count of non-NULL column values that cannot be parsed as numeric. Use this function to detect non-numeric data in
columns that are expected to contain numbers (for example, after CSV imports or user input).

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.INVALID_NUMERIC_TYPE_CAST_COUNT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have the VARCHAR data type.

## Returns

The function returns a NUMBER value. NULL values are excluded from the count.

## Example

Measure the number of values in the `quantity_str` column that cannot be cast to a number:

Copy code

```
SELECT SNOWFLAKE.CORE.INVALID_NUMERIC_TYPE_CAST_COUNT(
  SELECT
    quantity_str
  FROM staging.tables.csv_imports
);
```
