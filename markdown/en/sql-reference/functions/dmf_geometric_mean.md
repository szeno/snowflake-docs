Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# GEOMETRIC\_MEAN (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the geometric mean of the positive values for the specified column in a table. Zero and negative values are excluded,
because their logarithm is undefined.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.GEOMETRIC_MEAN(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- FLOAT
- NUMBER

## Returns

The function returns a FLOAT value. The function returns NULL if the column contains no positive values.

## Example

Measure the geometric mean of the `growth_rate` column:

Copy code

```
SELECT SNOWFLAKE.CORE.GEOMETRIC_MEAN(
  SELECT
    growth_rate
  FROM finance.tables.returns
);
```
