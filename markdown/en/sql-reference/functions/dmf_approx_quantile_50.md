Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# APPROX\_QUANTILE\_50 (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the approximate 50th percentile (P50, also known as the approximate median) value for the specified column in a table. For
large datasets, this function is faster than exact median calculation.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.APPROX_QUANTILE_50(<query>)
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

Measure the approximate median of the `latency_ms` column:

Copy code

```
SELECT SNOWFLAKE.CORE.APPROX_QUANTILE_50(
  SELECT
    latency_ms
  FROM metrics.tables.requests
);
```
