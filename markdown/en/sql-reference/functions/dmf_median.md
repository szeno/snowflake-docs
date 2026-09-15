Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# MEDIAN (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the median value for the specified column in a table. The median is more robust than the average for columns with skewed
distributions.

The MEDIAN system data metric function is optimized to calculate the median for a single column and provides greater performance when
compared to calling the [MEDIAN](/sql-reference/functions/median) function.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.MEDIAN(<query>)
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

Measure the median value of the `salary` column:

Copy code

```
SELECT SNOWFLAKE.CORE.MEDIAN(
  SELECT
    salary
  FROM hr.tables.empl_info
);
```
