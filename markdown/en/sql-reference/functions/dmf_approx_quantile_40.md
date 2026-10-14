Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# APPROX\_QUANTILE\_40 (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the approximate 40th percentile (P40) value for the specified column in a table.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.APPROX_QUANTILE_40(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- `FLOAT`
- `NUMBER`

## Returns

The function returns a `FLOAT` value. `NULL` values are ignored. The function returns `NULL` if the column contains no
non-`NULL` values.

## Usage notes

- The function uses [APPROX\_PERCENTILE](/sql-reference/functions/approx_percentile), so the result is an estimate, and values
  between data points are interpolated linearly.

## Example

Measure the approximate 40th percentile in the `latency_ms` column:

Copy code

```
SELECT SNOWFLAKE.CORE.APPROX_QUANTILE_40(
  SELECT
    latency_ms
  FROM metrics.tables.requests
);
```
