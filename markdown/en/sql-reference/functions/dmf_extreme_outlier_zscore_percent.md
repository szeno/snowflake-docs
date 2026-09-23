Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# EXTREME\_OUTLIER\_ZSCORE\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of a column’s values whose Z-score exceeds 4.5.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.EXTREME_OUTLIER_ZSCORE_PERCENT(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects a single column.

## Allowed data types

The column projected by the `query` must have one of the following data types:

- FLOAT
- NUMBER

## Returns

The function returns a scalar value with a FLOAT data type.

## Usage notes

- When you call a system DMF manually, you don’t need to specify whichever allowed data type you are using. You only need to specify
  the query for the column that you want to measure. Snowflake matches the allowed data type for the function with the data type for
  the column.
- The function computes the mean and standard deviation of the non-NULL, non-NaN values, then measures the percentage of values
  whose absolute difference from the mean is more than 4.5 standard deviations (a Z-score greater than 4.5). This is a wider
  threshold than [OUTLIER\_ZSCORE\_PERCENT](/sql-reference/functions/dmf_outlier_zscore_percent) uses, so it flags only the most
  extreme values.
- The denominator for the percentage includes all rows in the table, including rows where the projected column is NULL or NaN.
- The function returns 0 if the column has fewer than 100 non-NULL, non-NaN values, if the mean or standard deviation isn’t finite,
  or if the standard deviation is 0.
- This function is optimized for tables with up to approximately 10 billion rows. Beyond that range, evaluation latency
  increases, and the metric might not complete within the DMF scheduling window.
- Because evaluating this function scans the column and computes the mean and standard deviation over it, the serverless
  compute consumed (and therefore its cost) scales with table size. For information about how DMF evaluation is billed, see
  [Cost considerations](/user-guide/data-quality-intro#label-data-quality-cost).

## Example

Measure the percentage of extreme outlier values for the sensor\_reading column in an IoT table:

Copy code

```
SELECT SNOWFLAKE.CORE.EXTREME_OUTLIER_ZSCORE_PERCENT(
  SELECT
    sensor_reading
  FROM iot.public.readings
);
```

```
+-----------------------------------------------------------------------------------------------+
| SNOWFLAKE.CORE.EXTREME_OUTLIER_ZSCORE_PERCENT(SELECT sensor_reading FROM iot.public.readings) |
+-----------------------------------------------------------------------------------------------+
| 0.012                                                                                         |
+-----------------------------------------------------------------------------------------------+
```
