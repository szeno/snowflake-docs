Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# EXTREME\_OUTLIER\_IQR\_PERCENT (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the percentage of a column’s values that fall outside the extreme Tukey fences (3 times the interquartile range) for the
column.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view so it
runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.EXTREME_OUTLIER_IQR_PERCENT(<query>)
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
- The function computes the first and third quartiles (Q1, Q3) of the non-NULL, non-NaN values and the interquartile range
  `IQR = Q3 - Q1`, then measures the percentage of values less than `Q1 - 3 * IQR` or greater than `Q3 + 3 * IQR`. This is a wider
  fence than [OUTLIER\_IQR\_PERCENT](/sql-reference/functions/dmf_outlier_iqr_percent) uses, so it flags only the most extreme values.
- The denominator for the percentage includes all rows in the table, including rows where the projected column is NULL or NaN.
- The function returns 0 if the column has fewer than 100 non-NULL, non-NaN values, or if the required quartiles aren’t finite.
- This function is optimized for tables with up to approximately 10 billion rows. Beyond that range, evaluation latency
  increases, and the metric might not complete within the DMF scheduling window.
- Because evaluating this function scans the column and computes quartiles over it, the serverless compute consumed (and
  therefore its cost) scales with table size. For information about how DMF evaluation is billed, see
  [Cost considerations](/user-guide/data-quality-intro#label-data-quality-cost).

## Example

Measure the percentage of extreme outlier values for the transaction\_amount column in a finance table:

Copy code

```
SELECT SNOWFLAKE.CORE.EXTREME_OUTLIER_IQR_PERCENT(
  SELECT
    transaction_amount
  FROM finance.public.transactions
);
```

```
+--------------------------------------------------------------------------------------------------------+
| SNOWFLAKE.CORE.EXTREME_OUTLIER_IQR_PERCENT(SELECT transaction_amount FROM finance.public.transactions) |
+--------------------------------------------------------------------------------------------------------+
| 0.082                                                                                                  |
+--------------------------------------------------------------------------------------------------------+
```
