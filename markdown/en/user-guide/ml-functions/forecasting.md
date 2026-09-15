# Time-Series Forecasting (Snowflake ML Functions)

Forecasting uses a machine learning algorithm that predicts future numeric data from historical time series data.
A common use case is to forecast sales by item for the next two weeks.

## Quickstart to forecasting

This section gives the quickest way to get started with forecasting.

### Prerequisites

To get started you must do the following:

- Select a database, schema and virtual warehouse.
- Confirm that you own your schema or have CREATE SNOWFLAKE.ML.FORECAST privileges in the schema you’ve chosen.
- Have a table or view with at least two columns: one timestamp column and one numeric column. Be sure your timestamp column has
  timestamps at a fixed interval and isn’t missing too many timestamps. The following example shows a dataset with timestamp intervals
  of one day:

  Copy code

  ```
  ('2020-01-01 00:00:00.000', 2.0),
  ('2020-01-02 00:00:00.000', 3.0),
  ('2020-01-03 00:00:00.000', 4.0);
  ```

### Create forecasts

Once you have the prerequisites, you can use the AI & ML Studio in Snowsight to guide you through setup or you can use the
following SQL commands to train a model and start creating forecasts:

Copy code

```
-- Train your model
CREATE SNOWFLAKE.ML.FORECAST my_model(
  INPUT_DATA => TABLE(my_view),
  TIMESTAMP_COLNAME => 'my_timestamps',
  TARGET_COLNAME => 'my_metric'
);

-- Generate forecasts using your model
SELECT * FROM TABLE(my_model!FORECAST(FORECASTING_PERIODS => 7));
```

For more details on syntax and available methods, see the [FORECAST (SNOWFLAKE.ML)](/sql-reference/classes/forecast) reference.

## Dive deeper into forecasting

The forecasting function is built to predict any numeric time series data into the future. In addition to the simple case presented in the
[Quickstart to forecasting](#label-quick-guide-forecasting) section, you can do the following:

- Predict for multiple series at once. For example, you can predict the sales of multiple items for the next two weeks.
- Train and predict using features. Features are additional factors that you believe influence the metric you want to forecast.
- Assess your model’s accuracy.
- Understand the relative importance of the features the model was trained on.
- Debug training errors.

The following sections provide examples of these scenarios and additional details on how forecasting works.

## Examples

This section provide examples of how to set up your data for forecasting and how to create a forecasting model based on your time-series
data.

Note

Ideally, the training data for a Forecasting model has time steps at equally spaced intervals (for example, daily).
However, model training can handle real-world data that has missing, duplicate, or misaligned time steps. For more
information, see [Dealing with real-world data in Time-Series Forecasting](/user-guide/ml-functions/preprocessing).

### Set up example data

The example below creates two tables. Views of these tables are included in the [examples](#label-analysis-forecasting-examples) later in this topic.

The `sales_data` table contains sales data. Each sale includes a store ID, an item identifier, a timestamp, and
the sales amount. Additional columns, which are additional features (temperature, humidity, and holiday) are also included.

The `future_features` table contains future values of the feature columns, which are necessary when forecasting
using features as part of your prediction process.

Copy code

```
CREATE OR REPLACE TABLE sales_data (store_id NUMBER, item VARCHAR, date TIMESTAMP_NTZ,
  sales FLOAT, temperature NUMBER, humidity FLOAT, holiday VARCHAR);

INSERT INTO sales_data VALUES
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-01'), 2.0, 50, 0.3, 'new year'),
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-02'), 3.0, 52, 0.3, NULL),
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-03'), 4.0, 54, 0.2, NULL),
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-04'), 5.0, 54, 0.3, NULL),
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-05'), 6.0, 55, 0.2, NULL),
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-06'), 7.0, 55, 0.2, NULL),
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-07'), 8.0, 55, 0.2, NULL),
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-08'), 9.0, 55, 0.2, NULL),
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-09'), 10.0, 55, 0.2, NULL),
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-10'), 11.0, 55, 0.2, NULL),
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-11'), 12.0, 55, 0.2, NULL),
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-12'), 13.0, 55, 0.2, NULL),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-01'), 2.0, 50, 0.3, 'new year'),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-02'), 3.0, 52, 0.3, NULL),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-03'), 4.0, 54, 0.2, NULL),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-04'), 5.0, 54, 0.3, NULL),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-05'), 6.0, 55, 0.2, NULL),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-06'), 7.0, 55, 0.2, NULL),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-07'), 8.0, 55, 0.2, NULL),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-08'), 9.0, 55, 0.2, NULL),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-09'), 10.0, 55, 0.2, NULL),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-10'), 11.0, 55, 0.2, NULL),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-11'), 12.0, 55, 0.2, NULL),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-12'), 13.0, 55, 0.2, NULL);

-- Future values for additional columns (features)
CREATE OR REPLACE TABLE future_features (store_id NUMBER, item VARCHAR,
  date TIMESTAMP_NTZ, temperature NUMBER, humidity FLOAT, holiday VARCHAR);

INSERT INTO future_features VALUES
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-13'), 52, 0.3, NULL),
  (1, 'jacket', TO_TIMESTAMP_NTZ('2020-01-14'), 53, 0.3, NULL),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-13'), 52, 0.3, NULL),
  (2, 'umbrella', TO_TIMESTAMP_NTZ('2020-01-14'), 53, 0.3, NULL);
```

### Forecasting on a single series

This example uses a single time series (that is, all the rows are part of a single series) that has two columns, a
timestamp column and a target value column, without additional features.

First, prepare the example dataset to train the model:

Copy code

```
CREATE OR REPLACE VIEW v1 AS SELECT date, sales
  FROM sales_data WHERE store_id=1 AND item='jacket';
SELECT * FROM v1;
```

The SELECT statement returns:

```
+-------------------------+-------+
| DATE                    | SALES |
+-------------------------+-------+
| 2020-01-01 00:00:00.000 | 2     |
| 2020-01-02 00:00:00.000 | 3     |
| 2020-01-03 00:00:00.000 | 4     |
| 2020-01-04 00:00:00.000 | 5     |
| 2020-01-05 00:00:00.000 | 6     |
+-------------------------+-------+
```

Now, train a forecasting model using this view:

Copy code

```
CREATE SNOWFLAKE.ML.FORECAST model1(
  INPUT_DATA => TABLE(v1),
  TIMESTAMP_COLNAME => 'date',
  TARGET_COLNAME => 'sales'
);
```

The following message appears after the model is trained:

```
Instance MODEL1 successfully created.
```

Next, use the forecasting model to forecast the next three timestamps:

Copy code

```
call model1!FORECAST(FORECASTING_PERIODS => 3);
```

**Output**

Note that the model has inferred the interval between timestamps from the training data.

```
+--------+-------------------------+-----------+--------------+--------------+
| SERIES | TS                      | FORECAST  | LOWER_BOUND  | UPPER_BOUND  |
+--------+-------------------------+-----------+--------------+--------------+
| NULL   | 2020-01-13 00:00:00.000 | 14        | 14           | 14           |
| NULL   | 2020-01-14 00:00:00.000 | 15        | 15           | 15           |
| NULL   | 2020-01-15 00:00:00.000 | 16        | 16           | 16           |
+--------+-------------------------+-----------+--------------+--------------+
```

In this example, because the forecast yields a perfectly linear prediction that has zero errors compared to the actual
values, the prediction interval (LOWER\_BOUND, UPPER\_BOUND) is the same as the FORECAST value.

To customize the size of the prediction interval, pass `prediction_interval` as part of a configuration object:

Copy code

```
CALL model1!FORECAST(FORECASTING_PERIODS => 3, CONFIG_OBJECT => {'prediction_interval': 0.8});
```

To save your results directly to a table, use [CREATE TABLE … AS SELECT …](/sql-reference/sql/create-table#label-ctas-syntax) and
[call the FORECAST method in the FROM clause](/sql-reference/snowflake-db-classes#label-class-select-from-methods):

Copy code

```
CREATE TABLE my_forecasts AS
  SELECT * FROM TABLE(model1!FORECAST(FORECASTING_PERIODS => 3));
```

As shown in the example above, when calling the method, omit the [CALL](/sql-reference/sql/call) command. Instead, put the call
in parentheses, preceded by the TABLE keyword.

### Forecast on multiple series

To create a forecasting model for multiple series at once, use the `series_colname` parameter.

In this example, the data contains `store_id` and `item` columns. To forecast sales separately for every store/item
combination in the dataset, create a new column that combines these values, and specify that as the series
column.

The following query creates a new view combining `store_id` and `item` into a new column named
`store_item`:

Copy code

```
CREATE OR REPLACE VIEW v3 AS SELECT [store_id, item] AS store_item, date, sales FROM sales_data;
SELECT * FROM v3;
```

**Output**

The first five rows for each series for the resulting dataset are:

```
+-------------------+-------------------------+-------+
| STORE_ITEM        | DATE                    | SALES |
+-------------------+-------------------------+-------+
| [ 1, "jacket" ]   | 2020-01-01 00:00:00.000 | 2     |
| [ 1, "jacket" ]   | 2020-01-02 00:00:00.000 | 3     |
| [ 1, "jacket" ]   | 2020-01-03 00:00:00.000 | 4     |
| [ 1, "jacket" ]   | 2020-01-04 00:00:00.000 | 5     |
| [ 1, "jacket" ]   | 2020-01-05 00:00:00.000 | 6     |
| [ 2, "umbrella" ] | 2020-01-01 00:00:00.000 | 2     |
| [ 2, "umbrella" ] | 2020-01-02 00:00:00.000 | 3     |
| [ 2, "umbrella" ] | 2020-01-03 00:00:00.000 | 4     |
| [ 2, "umbrella" ] | 2020-01-04 00:00:00.000 | 5     |
| [ 2, "umbrella" ] | 2020-01-05 00:00:00.000 | 6     |
+-------------------+-------------------------+-------+
```

Now use the forecasting function to train a model for each series, all in one step. Note that the `series_colname` parameter is set
to `store_item`:

Copy code

```
CREATE SNOWFLAKE.ML.FORECAST model2(
  INPUT_DATA => TABLE(v3),
  SERIES_COLNAME => 'store_item',
  TIMESTAMP_COLNAME => 'date',
  TARGET_COLNAME => 'sales'
);
```

Next, use that model to forecast the next two timestamps for all series:

Copy code

```
CALL model2!FORECAST(FORECASTING_PERIODS => 2);
```

**Output**

```
+-------------------+------------------------+----------+-------------+-------------+
| SERIES            | TS                     | FORECAST | LOWER_BOUND | UPPER_BOUND |
+-------------------+------------------------+----------+-------------+-------------+
| [ 1, "jacket" ]   | 2020-01-13 00:00:00.000 | 14      | 14          | 14          |
| [ 1, "jacket" ]   | 2020-01-14 00:00:00.000 | 15      | 15          | 15          |
| [ 2, "umbrella" ] | 2020-01-13 00:00:00.000 | 14      | 14          | 14          |
| [ 2, "umbrella" ] | 2020-01-14 00:00:00.000 | 15      | 15          | 15          |
+-------------------+-------------------------+---------+-------------+-------------+
```

You can also forecast a specific series with:

Copy code

```
CALL model2!FORECAST(SERIES_VALUE => [2,'umbrella'], FORECASTING_PERIODS => 2);
```

**Output**

The result shows only the next two steps for store 2’s sales of umbrellas.

```
+-------------------+------------ ------------+-----------+-------------+-------------+
| SERIES            | TS                      | FORECAST  | LOWER_BOUND | UPPER_BOUND |
+-------------------+---------- --------------+-----------+-------------+-------------+
| [ 2, "umbrella" ] | 2020-01-13 00:00:00.000 | 14        | 14          | 14          |
| [ 2, "umbrella" ] | 2020-01-14 00:00:00.000 | 15        | 15          | 15          |
+-------------------+-------------------------+-----------+-------------+-------------+
```

Tip

Specifying one series with the FORECAST method is more efficient than filtering the results of a multi-series
forecast to include only the series you’re interested in, because only one series’ forecast is generated.

### Forecasting with features

If you want additional features (for example, holidays or weather) to influence your forecasts, you must include these features
in your training data. Here you create a view containing those fields from the `sales_data` table:

Copy code

```
CREATE OR REPLACE VIEW v2 AS SELECT date, sales, temperature, humidity, holiday
  FROM sales_data WHERE store_id=1 AND item='jacket';
SELECT * FROM v2;
```

**Output**

This is the first five rows of the result of the SELECT query.

```
+-------------------------+--------+-------------+----------+----------+
| DATE                    | SALES  | TEMPERATURE | HUMIDITY | HOLIDAY  |
+-------------------------+--------+-------------+----------+----------+
| 2020-01-01 00:00:00.000 | 2      | 50          | 0.3      | new year |
| 2020-01-02 00:00:00.000 | 3      | 52          | 0.3      | null     |
| 2020-01-03 00:00:00.000 | 4      | 54          | 0.2      | null     |
| 2020-01-04 00:00:00.000 | 5      | 54          | 0.3      | null     |
| 2020-01-05 00:00:00.000 | 6      | 55          | 0.2      | null     |
+-------------------------+--------+-------------+----------+----------+
```

Now you can use this view to train a model. You are only required to specify the timestamp and target column names;
additional columns in the input data are assumed to be features for use in training.

Copy code

```
CREATE SNOWFLAKE.ML.FORECAST model3(
  INPUT_DATA => TABLE(v2),
  TIMESTAMP_COLNAME => 'date',
  TARGET_COLNAME => 'sales'
);
```

To generate forecasts with this model, you must provide future values for the features to the model: in this case, `TEMPERATURE`,
`HUMIDITY` and `HOLIDAY`. This allows the model to adjust its sales forecasts based on temperature, humidity, and holiday
forecasts.

Now create a view from the `future_features` table containing this data for future timestamps:

Copy code

```
CREATE OR REPLACE VIEW v2_forecast AS select date, temperature, humidity, holiday
  FROM future_features WHERE store_id=1 AND item='jacket';
SELECT * FROM v2_forecast;
```

**Output**

```
+-------------------------+-------------+----------+---------+
| DATE                    | TEMPERATURE | HUMIDITY | HOLIDAY |
+-------------------------+-------------+----------+---------+
| 2020-01-13 00:00:00.000 | 52          | 0.3      | null    |
| 2020-01-14 00:00:00.000 | 53          | 0.3      | null    |
+-------------------------+-------------+----------+---------+
```

Now you can generate a forecast using this data:

Copy code

```
CALL model3!FORECAST(
  INPUT_DATA => TABLE(v2_forecast),
  TIMESTAMP_COLNAME =>'date'
);
```

In this variation of the FORECAST method, you do not specify the number of timestamps to predict. Instead, the timestamps
of the forecast come from the `v2_forecast` view.

```
+--------+-------------------------+-----------+--------------+--------------+
| SERIES | TS                      | FORECAST  | LOWER_BOUND  | UPPER_BOUND  |
+--------+-------------------------+-----------+--------------+--------------+
| NULL   | 2020-01-13 00:00:00.000 | 14        | 14           | 14           |
| NULL   | 2020-01-14 00:00:00.000 | 15        | 15           | 15           |
+--------+-------------------------+-----------+--------------+--------------+
```

## Troubleshooting and model assessment

You can use the following helper functions to assess your model performance, understand which features are most impactful to your model,
and to help you debug the training process if any error occurred:

- [model!SHOW\_EVALUATION\_METRICS()](/sql-reference/classes/forecast/methods/show_evaluation_metrics);
- [model!EXPLAIN\_FEATURE\_IMPORTANCE()](/sql-reference/classes/forecast/methods/explain_feature_importance);
- [model!SHOW\_TRAINING\_LOGS()](/sql-reference/classes/forecast/methods/show_training_logs);

### Evaluation metrics

To get the evaluation metrics for your model, call the [<model\_name>!SHOW\_EVALUATION\_METRICS](/sql-reference/classes/forecast/methods/show_evaluation_metrics) method.
By default, the forecasting function evaluates all models it trains using a method called
[cross-validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics)). This means that under the hood,
in addition to training the final model on all of the training data you provide, the function also trains models on subsets of your
training data. Those models are then used to predict your target metric on the withheld data, allowing the function to compare those
predictions to actual values in your historical data.

If you don’t need these evaluation metrics, you can set `evaluate` to FALSE. If you want to control the way cross-validation is run,
you can use the following parameters:

- **n\_splits**: Represents the number of splits in your data for cross validation. Default is 1.
- **max\_train\_size**: Represents the maximum number of rows for a single training set.
- **test\_size**: Limits number of rows included in each test set.
- **gap**: Represents the gap between the end of each training set and the start of the test set.

For complete details on evaluation parameters, see [Evaluation configuration](/sql-reference/classes/forecast/commands/create-forecast#label-forecast-evaluation-config).

Note

Small datasets may not have enough data to perform evaluation. The total number of training rows must be equal to or greater
than (n\_splits \* test\_size) + gap. If not enough data is available to train an evaluation model, no evaluation metrics are available
even when `evaluate` is set to TRUE.

When **n\_splits** is 1 (the default), the standard deviation for evaluation metric values is NULL, as only a validation dataset is used.

#### Example

Copy code

```
CREATE OR REPLACE VIEW v_random_data AS SELECT
  DATEADD('minute', ROW_NUMBER() over (ORDER BY 1), '2023-12-01')::TIMESTAMP_NTZ ts,
  UNIFORM(1, 100, RANDOM(0)) exog_a,
  UNIFORM(1, 100, RANDOM(0)) exog_b,
  (MOD(SEQ1(),10) + exog_a) y
FROM TABLE(GENERATOR(ROWCOUNT => 500));

CREATE OR REPLACE SNOWFLAKE.ML.FORECAST model(
  INPUT_DATA => TABLE(v_random_data),
  TIMESTAMP_COLNAME => 'ts',
  TARGET_COLNAME => 'y'
);

CALL model!SHOW_EVALUATION_METRICS();
```

**Output**

Copy code

```
+--------+--------------------------+--------------+--------------------+------+
| SERIES | ERROR_METRIC             | METRIC_VALUE | STANDARD_DEVIATION | LOGS |
+--------+--------------------------+--------------+--------------------+------+
| NULL   | "MAE"                    |         2.49 |                NaN | NULL |
| NULL   | "MAPE"                   |        0.084 |                NaN | NULL |
| NULL   | "MDA"                    |         0.99 |                NaN | NULL |
| NULL   | "MSE"                    |        8.088 |                NaN | NULL |
| NULL   | "SMAPE"                  |        0.077 |                NaN | NULL |
| NULL   | "WINKLER_ALPHA=0.05"     |       12.101 |                NaN | NULL |
| NULL   | "COVERAGE_INTERVAL=0.95" |            1 |                NaN | NULL |
+--------+--------------------------+--------------+--------------------+------+
```

### Feature importance

To understand the relative importance of the features used in your model, use the [<model\_name>!EXPLAIN\_FEATURE\_IMPORTANCE](/sql-reference/classes/forecast/methods/explain_feature_importance#label-class-forecast-explain-feature-importance)
method.

When you train a forecasting model, your model uses provided data, such as timestamps, your target metric, additional columns
you provide (features), and features that are automatically generated to improve the performance of your forecasts, to learn patterns
in your data. Training detects how important each of these is to making accurate predictions than others. Understanding the
relative importance of these features on a scale of 0 to 1 is the purpose of this helper function.

Under the hood, this helper function counts the number of times the model used each feature to make a decision. These feature importance
scores are then normalized to values between 0 and 1 so that their sum is 1. The resulting scores represent an approximate ranking of the
features in your trained model.

#### Key considerations for this feature

- Features that are close in score have similar importance.
- For extremely simple series (for example, when the target column has a constant value), all feature importance scores may be zero.
- Using multiple features that are very similar to each other may result in reduced importance scores for those features. For example,
  if two features are exactly identical, the model may treat them as interchangeable when making decisions, resulting in feature
  importance scores that are half of what those scores would be if only one of the identical features were included.

#### Example

This example uses the data from the [evaluation example](#label-analysis-forecasting-evaluation-metrics) and calls the feature
importance method. You can see that the `exog_a` variable that was created is the second most important feature - behind all rolling
averages, which are aggregated under the `aggregated_endogenous_trend_features` feature name.

Execute the following statements to get the importance of the features:

Copy code

```
CALL model!EXPLAIN_FEATURE_IMPORTANCE();
```

**Output**

```
+--------+------+--------------+---------------+---------------+
| SERIES | RANK | FEATURE_NAME | SCORE         | FEATURE_TYPE  |
+--------+------+--------------+---------------+---------------+
| NULL   |    1 | exog_a       |  31.414947903 | user_provided |
| NULL   |    2 | exog_b       |             0 | user_provided |
+--------+------+--------------+---------------+---------------+
```

### Troubleshooting

When you train multiple series with `CONFIG_OBJECT => {'ON_ERROR': 'SKIP'}`, individual time series models can
fail to train without the overall training process failing. To understand which time series failed and why, call the
[<model\_name>!SHOW\_TRAINING\_LOGS](/sql-reference/classes/forecast/methods/show_training_logs) method.

### Example

Copy code

```
CREATE TABLE t_error(date TIMESTAMP_NTZ, sales FLOAT, series VARCHAR);
INSERT INTO t_error VALUES
  (TO_TIMESTAMP_NTZ('2019-12-30'), 3.0, 'A'),
  (TO_TIMESTAMP_NTZ('2019-12-31'), 2.0, 'A'),
  (TO_TIMESTAMP_NTZ('2020-01-01'), 2.0, 'A'),
  (TO_TIMESTAMP_NTZ('2020-01-02'), 3.0, 'A'),
  (TO_TIMESTAMP_NTZ('2020-01-03'), 3.0, 'A'),
  (TO_TIMESTAMP_NTZ('2020-01-04'), 7.0, 'A'),
  (TO_TIMESTAMP_NTZ('2020-01-06'), 10.0, 'B'), -- the same timestamp used again and again
  (TO_TIMESTAMP_NTZ('2020-01-06'), 13.0, 'B'),
  (TO_TIMESTAMP_NTZ('2020-01-06'), 12.0, 'B'),
  (TO_TIMESTAMP_NTZ('2020-01-06'), 15.0, 'B'),
  (TO_TIMESTAMP_NTZ('2020-01-06'), 14.0, 'B'),
  (TO_TIMESTAMP_NTZ('2020-01-06'), 18.0, 'B'),
  (TO_TIMESTAMP_NTZ('2020-01-06'), 12.0, 'B');

CREATE SNOWFLAKE.ML.FORECAST error_model(
  INPUT_DATA => TABLE(SELECT date, sales, series FROM t_error),
  SERIES_COLNAME => 'series',
  TIMESTAMP_COLNAME => 'date',
  TARGET_COLNAME => 'sales',
  CONFIG_OBJECT => {'ON_ERROR': 'SKIP'}
);

CALL error_model!SHOW_TRAINING_LOGS();
```

**Output**

```
+--------+--------------------------------------------------------------------------+
| SERIES | LOGS                                                                     |
+--------+--------------------------------------------------------------------------+
| "B"    | {   "Errors": [     "At least two unique timestamps are required."   ] } |
| "A"    | NULL                                                                     |
+--------+--------------------------------------------------------------------------+
```

## Model management

To view a list of your models, use the [SHOW SNOWFLAKE.ML.FORECAST](/sql-reference/classes/forecast/commands/show-forecast) command:

Copy code

```
SHOW SNOWFLAKE.ML.FORECAST;
```

To delete a model, use the [DROP SNOWFLAKE.ML.FORECAST](/sql-reference/classes/forecast/commands/drop-forecast) command:

Copy code

```
DROP SNOWFLAKE.ML.FORECAST my_model;
```

Models are immutable and cannot be updated in place. Train a new model instead.

## Warehouse selection

A Snowflake [virtual warehouse](/user-guide/warehouses) provides the compute resources for training and using the
machine learning models for this feature. This section provides general guidance on selecting the best type and size of
warehouse for this purpose, focusing on the training step, the most time-consuming and memory-intensive part of
the process.

There are two key factors to keep in mind when choosing a warehouse:

1. The number of rows and columns your data contains.
2. The number of distinct series your data contains.

You can use the following rules of thumb to choose your warehouse:

1. If you are training on a longer time series (> 5 million rows) or on many columns (many features), consider upgrading to
   [Snowpark-optimized warehouses](/user-guide/warehouses-snowpark-optimized).
2. If you are training on many series, size up. The forecasting function distributes model training across all available nodes in your
   warehouse when you are training for multiple series at once.

The following table provides this same guidance:

| Series type | < 5 million rows | > 5 million rows and ≤ 100 million rows | > 100 million rows |
| --- | --- | --- | --- |
| One series | Standard warehouse; XS | Snowpark optimized warehouse; XS | Consider aggregating to a less frequent timestamp interval (e.g., hourly to daily) |
| Multiple series | Standard warehouse; Size up | Snowpark optimized warehouse; Size up | Consider batching training by series into multiple jobs |

Expand

Show lessSee more

As a rough estimate, training time is proportional to the number of rows in your time series. For example, on a XS standard warehouse,
with evaluation turned off (`CONFIG_OBJECT => {'evaluate': False}`), training on a 100,000-row dataset takes about
400 seconds. Training on a 1,000,000-row dataset takes about 850 seconds. With
evaluation turned on, training time increases roughly linearly by the number of splits used.

## Algorithm details

The forecasting algorithm used is specified by the (`CONFIG_OBJECT => {'method': '<method>'}`) config object
parameter. This parameter defaults to (`'method': 'best'`). When the method is set to `'best'`, the
algorithm used is an ensemble of multiple models, including [Prophet](https://facebook.github.io/prophet/),
[ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average) ,
[Exponential Smoothing](https://en.wikipedia.org/wiki/Exponential_smoothing) , and a
[gradient boosting machine](https://en.wikipedia.org/wiki/Gradient_boosting) (described further below).

When the method is set to `fast`, the algorithm used is a gradient boosting machine (GBM). Like an ARIMA model,
it uses a differencing transformation to model data with a non-stationary trend and uses auto-regressive lags of the
historical target data as model variables. Additionally, the algorithm uses rolling averages of historical target data
to help predict trends, and automatically produces cyclic calendar variables (such as day of week and week of year) from
timestamp data.

You can fit models with only historical target and timestamp data, or you may include features (extra columns) that
might have influenced the target value. Exogenous variables can be numerical or categorical and may be NULL (rows
containing NULLs for exogenous variables are not dropped).

The algorithm does not rely on one-hot encoding when training on categorical variables, so you can use categorical data
with many dimensions (high cardinality).

If your model incorporates features, when generating a forecast you must provide values for those features
at every timestamp of the full forecast horizon. Appropriate features could include weather data
(temperature, rainfall), company-specific information (historic and planned company holidays, advertisement campaigns,
event schedules), or any other external factors you believe may help predict your target variable.

The algorithm also generates prediction intervals, in addition to forecasts. A prediction interval is an estimated range
of values within an upper bound and a lower bound in which a certain percentage of data is likely to fall. For example,
a 0.95 value means that 95% of the data likely appears within the interval. You may specify a prediction interval
percentage, or use the default, which is 0.95. Lower and upper bounds of the prediction interval are returned as part of
the forecast output.

Important

From time to time, Snowflake may refine the forecasting algorithm. Such improvements roll out through
the regular Snowflake release process. You cannot revert to a previous version of the feature, but models you
created with a previous version continue to use that version for predictions until deprecation through the Behavior Change Release process.

### Current Limitations

The current release has the following limitations:

- You cannot choose or adjust the forecasting algorithm.
- The minimum number of rows for the main forecasting algorithm is 12 per time series. For time series with between 2 and 11
  observations, forecasting produces a “naive” forecast where all forecasted values are equal to the last observed target
  value.
- The forecasting function does not provide parameters to override trend, seasonality, or seasonal amplitudes; these are
  inferred from the data.
- The minimum acceptable granularity of data is one second. (Timestamps must not be less than one second apart.)
- The minimum granularity of seasonal components is one minute. (The function cannot detect cyclic patterns at
  smaller time deltas.)
- The “season length” of autoregressive features is tied to the input frequency (24 for hourly data, 7 for daily data,
  and so on).
- Forecast models, once trained, are immutable. You cannot update existing models with new data; you must train an
  entirely new model.
- Models do not support versioning. Snowflake recommends retraining a model on a regular cadence,
  perhaps daily, weekly, or monthly, depending on how frequently you receive new data, allowing the model to adjust
  to changing patterns and trends.
- You cannot clone models or share models across roles or accounts. When cloning a schema or database, model objects are skipped.
- You cannot [replicate](/user-guide/account-replication-intro) an instance of the FORECAST class.

## Granting privileges to create forecast objects

Training a forecasting model results in a schema-level object. Therefore, the role you use to create models must
have the CREATE SNOWFLAKE.ML.FORECAST privilege on the schema where the model is created, allowing the
model to be stored there. This privilege is similar to other schema privileges like CREATE TABLE or CREATE VIEW.

Snowflake recommends that you create a role named `analyst` to be used by people who need to create forecasts.

In the following example, the `admin` role is the owner of the schema `admin_db.admin_schema`. The
`analyst` role needs to create models in this schema.

Copy code

```
USE ROLE admin;
GRANT USAGE ON DATABASE admin_db TO ROLE analyst;
GRANT USAGE ON SCHEMA admin_schema TO ROLE analyst;
GRANT CREATE SNOWFLAKE.ML.FORECAST ON SCHEMA admin_db.admin_schema TO ROLE analyst;
```

To use this schema, a user assumes the role `analyst`:

Copy code

```
USE ROLE analyst;
USE SCHEMA admin_db.admin_schema;
```

If the `analyst` role has CREATE SCHEMA privileges in database `analyst_db`, the role can create a new schema
`analyst_db.analyst_schema` and create forecast models in that schema:

Copy code

```
USE ROLE analyst;
CREATE SCHEMA analyst_db.analyst_schema;
USE SCHEMA analyst_db.analyst_schema;
```

To revoke a role’s forecast model creation privilege on the schema, use [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege):

Copy code

```
REVOKE CREATE SNOWFLAKE.ML.FORECAST ON SCHEMA admin_db.admin_schema FROM ROLE analyst;
```

## Cost considerations

For details on costs for using ML functions, see [Cost Considerations](/guides-overview-ml-functions#label-ml-functions-costs) in the ML functions overview.
