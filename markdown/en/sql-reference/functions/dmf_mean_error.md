Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# MEAN\_ERROR (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the mean signed error between a column of predicted values and a column of actual values, where each error is the actual
value minus the predicted value. Use this function to detect bias, that is, whether predictions are consistently too high or too low.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.MEAN_ERROR(<query>)
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

The function returns a `FLOAT` value:

- A positive value means that, on average, the predictions are lower than the actual values.
- A negative value means that, on average, the predictions are higher than the actual values.
- A value of 0 means that the errors cancel out. It doesn’t mean that every prediction is correct.

The function returns `NULL` if no row has both a predicted and an actual value.

## Usage notes

- The function computes `AVG(actual - predicted)`.
- The order of the columns matters. The first column is the predicted value and the second is the actual value. When you
  associate the function with a table or view, specify the columns in the same order:
  `ON (predicted_column, actual_column)`.
- Rows in which either value is `NULL` are ignored.
- You can’t mix data types. For example, you can’t use the function on a `NUMBER` column of predictions and a `FLOAT` column of
  actual values.
- Errors in opposite directions cancel each other out. To measure the size of the errors, use
  [MAE](/sql-reference/functions/dmf_mae) or [RMSE](/sql-reference/functions/dmf_rmse).

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

Measure the bias of the forecasts:

Copy code

```
SELECT SNOWFLAKE.CORE.MEAN_ERROR(
  SELECT
    forecast_units,
    actual_units
  FROM sales.forecasts.store_demand
) AS mean_error;
```

```
+------------+
| MEAN_ERROR |
+------------+
| -1.25      |
+------------+
```

Associate the function with the table, and define an expectation that is violated when forecasts are, on average, more than 5 units
too high or too low:

Copy code

```
ALTER TABLE sales.forecasts.store_demand
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.MEAN_ERROR
    ON (forecast_units, actual_units)
    EXPECTATION low_bias (VALUE BETWEEN -5 AND 5);
```
