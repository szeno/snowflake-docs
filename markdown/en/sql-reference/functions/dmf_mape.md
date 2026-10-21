Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# MAPE (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the mean absolute percentage error (MAPE) between a column of predicted values and a column of actual values. MAPE is
the average size of an error, expressed as a percentage of the actual value.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.MAPE(<query>)
```

## Arguments

`query`
:   Specifies a SQL query that projects two columns. The first column contains the predicted values, and the second column contains
    the actual values.

## Allowed data types

The two columns projected by the `query` must have the same data type, which must be one of
the following:

- `FLOAT`
- `NUMBER`

## Returns

The function returns a `FLOAT` value that is greater than or equal to 0. A value of 0 means that every prediction matches the
actual value. The value has no upper bound: a prediction that is three times the actual value contributes an error of 200 percent.

The function returns `NULL` if no row has both a predicted value and a non-zero actual value.

## Usage notes

- The function computes `100 * AVG(ABS((actual - predicted) / actual))`.
- The order of the columns matters. The first column is the predicted value and the second is the actual value. When you
  associate the function with a table or view, specify the columns in the same order:
  `ON (predicted_column, actual_column)`.
- Rows in which either value is `NULL` are ignored.
- You can’t mix data types. For example, you can’t use the function on a `NUMBER` column of predictions and a `FLOAT` column of
  actual values.
- Rows in which the actual value is 0 are ignored, because the percentage error is undefined for them. If many actual values
  are 0 or close to 0, use [MAE](/sql-reference/functions/dmf_mae) or [RMSE](/sql-reference/functions/dmf_rmse) instead.

## Examples

The examples use the following table of demand forecasts. The prediction in the last row is missing, so the function ignores
that row:

Copy code

```
CREATE TABLE sales.forecasts.store_demand (
  forecast_units FLOAT,
  actual_units FLOAT);

INSERT INTO sales.forecasts.store_demand VALUES
  (110, 100),
  (95, 100),
  (130, 120),
  (80, 90),
  (NULL, 50);
```

Measure the mean absolute percentage error of the forecasts:

Copy code

```
SELECT SNOWFLAKE.CORE.MAPE(
  SELECT
    forecast_units,
    actual_units
  FROM sales.forecasts.store_demand
) AS mape;
```

```
+-------------+
| MAPE        |
+-------------+
| 8.611111111 |
+-------------+
```

Associate the function with the table, and define an expectation that is violated when the average error reaches 10 percent:

Copy code

```
ALTER TABLE sales.forecasts.store_demand
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.MAPE
    ON (forecast_units, actual_units)
    EXPECTATION mape_under_10 (VALUE < 10);
```
