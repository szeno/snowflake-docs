Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# APPROX\_QUANTILE\_99 (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the approximate 99th percentile (P99) value for the specified column in a table. Use this function to detect outliers and
monitor tail behavior. Commonly used for SLO monitoring on latency metrics.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.APPROX_QUANTILE_99(<query>)
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

Measure the approximate P99 of the `latency_ms` column:

Copy code

```
SELECT SNOWFLAKE.CORE.APPROX_QUANTILE_99(
  SELECT
    latency_ms
  FROM metrics.tables.requests
);
```
