Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# SUM (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the sum of the values for the specified column in a table. Use this function to detect unexpected changes in totals, such as
during financial reconciliation.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.SUM(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- FLOAT
- NUMBER

## Returns

The function returns a NUMBER value for a NUMBER column and a FLOAT value for a FLOAT column. NULL values are ignored. The function
returns NULL if the column contains no non-NULL values.

## Example

Measure the sum of the `amount` column:

Copy code

```
SELECT SNOWFLAKE.CORE.SUM(
  SELECT
    amount
  FROM sales.tables.orders
);
```
