Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# R\_SQUARED (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the coefficient of determination (R²) of a column of predicted values against a column of actual values. R² measures the
share of the variation in the actual values that the predictions explain.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.R_SQUARED(<query>)
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

The function returns a `FLOAT` value that is less than or equal to 1:

- A value of 1 means that every prediction matches the actual value.
- A value of 0 means that the predictions are no better than predicting the average actual value for every row.
- A negative value means that the predictions are worse than predicting the average actual value.

The function returns `NULL` if no row has both a predicted and an actual value, or if all of the actual values are the same.

## Usage notes

- The function computes `1 - SUM(POWER(actual - predicted, 2)) / SUM(POWER(actual - mean_actual, 2))`, where
  `mean_actual` is the average of the actual values in the rows that have both a predicted and an actual value.
- The order of the columns matters. The first column is the predicted value and the second is the actual value. When you
  associate the function with a table or view, specify the columns in the same order:
  `ON (predicted_column, actual_column)`.
- Rows in which either value is `NULL` are ignored.
- You can’t mix data types. For example, you can’t use the function on a `NUMBER` column of predictions and a `FLOAT` column of
  actual values.

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

Measure the coefficient of determination of the forecasts:

Copy code

```
SELECT SNOWFLAKE.CORE.R_SQUARED(
  SELECT
    forecast_units,
    actual_units
  FROM sales.forecasts.store_demand
) AS r_squared;
```

```
+--------------+
| R_SQUARED    |
+--------------+
| 0.3157894737 |
+--------------+
```

Associate the function with the table, and define an expectation that is violated when R² falls below 0.8:

Copy code

```
ALTER TABLE sales.forecasts.store_demand
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.R_SQUARED
    ON (forecast_units, actual_units)
    EXPECTATION r_squared_at_least_0_8 (VALUE >= 0.8);
```
