Categories:
:   [Data metric functions](/sql-reference/functions-data-metric)

# MAE (system data metric function)

[Enterprise Edition Feature](/user-guide/intro-editions)

Data Quality Monitoring requires Enterprise Edition. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Returns the mean absolute error (MAE) between a column of predicted values and a column of actual values. MAE is the average
size of an error, in the same units as the values.

This topic provides the syntax for calling the function directly. To learn how to associate the function with a table or view
so it runs at regular intervals, see [Associate a DMF](/user-guide/data-quality-working#label-dmf-associate).

## Syntax

Copy code

```
SNOWFLAKE.CORE.MAE(<query>)
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
actual value. The function returns `NULL` if no row has both a predicted and an actual value.

## Usage notes

- The function computes `AVG(ABS(predicted - actual))`.
- The order of the columns matters. The first column is the predicted value and the second is the actual value. When you
  associate the function with a table or view, specify the columns in the same order:
  `ON (predicted_column, actual_column)`.
- Rows in which either value is `NULL` are ignored.
- You can’t mix data types. For example, you can’t use the function on a `NUMBER` column of predictions and a `FLOAT` column of
  actual values.
- MAE doesn’t show whether predictions are too high or too low. To measure that, use
  [MEAN\_ERROR](/sql-reference/functions/dmf_mean_error).

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

Measure the mean absolute error of the forecasts:

Copy code

```
SELECT SNOWFLAKE.CORE.MAE(
  SELECT
    forecast_units,
    actual_units
  FROM sales.forecasts.store_demand
) AS mae;
```

```
+------+
| MAE  |
+------+
| 8.75 |
+------+
```

Associate the function with the table, and define an expectation that is violated when the MAE reaches 10 units:

Copy code

```
ALTER TABLE sales.forecasts.store_demand
  ADD DATA METRIC FUNCTION SNOWFLAKE.CORE.MAE
    ON (forecast_units, actual_units)
    EXPECTATION mae_under_10 (VALUE < 10);
```
