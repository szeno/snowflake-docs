# Anomaly Detection (Snowflake ML Functions)

## Overview

Anomaly detection is the process of identifying outliers in data. The anomaly detection function lets you train a model
to detect outliers in your time-series data. Outliers, which are data points that deviate from the expected range, can
have an outsized impact on statistics and models derived from your data. Spotting and removing outliers can therefore
help improve the quality of your results.

Note

Anomaly Detection is part of Snowflake’s suite of business analysis tools powered by machine learning.

Detecting outliers can also be useful in pinpointing the origin of problems or deviations in processes when there is no
obvious cause. For example:

- Determining when a problem started to occur with your logging pipeline.
- Identifying the days when your Snowflake compute costs are higher than expected.

Anomaly detection works with either single-series or multi-series data. Multi-series data represents multiple
independent threads of events. For example, if you have sales data for multiple stores, each store’s sales can be
checked separately by a single model based on the store identifier.

The data must include:

- A timestamp column.
- A target column representing some quantity of interest at each timestamp.

Note

Ideally, the training data for an Anomaly Detection model has time steps at equally spaced intervals (for example,
daily). However, model training can handle real-world data that has missing, duplicate, or misaligned time steps.
For more information, see [Dealing with real-world data in Time-Series Forecasting](/user-guide/ml-functions/preprocessing).

To detect outliers in time-series data, use the Snowflake built-in class [ANOMALY\_DETECTION (SNOWFLAKE.ML)](/sql-reference/classes/anomaly_detection),
and follow these steps:

1. [Create an anomaly detection object](/sql-reference/classes/anomaly-detection/commands/create-anomaly-detection#label-class-anomaly-detection-create),
   passing in a reference to the training data.

   This object fits a model to the training data that you provide. The model is a schema-level object.
2. Using this anomaly detection model object, call the [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies) method to
   detect anomalies, passing in a reference to the data to analyze.

   The method uses the model to identify outliers in the data.

Anomaly detection is closely related to [Forecasting](/user-guide/ml-functions/forecasting). An anomaly detection model
produces a forecast for the same time period as the data you’re checking for anomalies, then compares the actual data to
the forecast to identify outliers.

## About the Algorithm for Anomaly Detection

The anomaly detection algorithm is powered by a [gradient boosting machine](https://en.wikipedia.org/wiki/Gradient_boosting)
(GBM). Like an [ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average) model, it uses a
differencing transformation to model data with a non-stationary trend and uses auto-regressive lags of the historical
target data as model variables.

Additionally, the algorithm uses rolling averages of historical target data to help predict trends, and automatically
produces cyclic calendar variables (such as day of week and week of year) from timestamp data.

You can fit models with only historical target and timestamp data, or you may include exogenous data (variables) that
might have influenced the target value. Exogenous variables can be numerical or categorical and may be NULL (rows
containing NULLs for exogenous variables are not dropped).

The algorithm does not rely on one-hot encoding when training on categorical variables, so you can use categorical data
with many dimensions (high cardinality).

If your model incorporates exogenous variables, you must provide values for those variables at timestamps in the future
when detecting anomalies. Appropriate exogenous variables could include weather data (temperature, rainfall),
company-specific information (historic and planned company holidays, advertisement campaigns, event schedules), or any
other external factors you believe may help predict your target variable.

Optionally, individual historical rows can be labeled as anomalous or non-anomalous by using a separate Boolean column.

A *prediction interval* is an estimated range of values within an upper bound and a lower bound in which a certain
percentage of data is likely to fall. For example, a 0.99 value means that 99% of the data likely appears within the
interval. The anomaly detection model identifies any data that falls outside of the prediction interval as an anomaly. You can
specify a prediction interval or use the default, which is 0.99. You may want to set this value to be very close
to 1.0; 0.9999 or even closer.

Important

From time to time, Snowflake may refine the anomaly detection algorithm. Such improvements roll out
through the regular Snowflake release process. You cannot revert to a previous version of the feature, but models you
created with a previous version continue to use that version for anomaly detection.

### Limitations

- You cannot choose or adjust the anomaly detection algorithm. In particular, the algorithm does not provide parameters
  to override trend, seasonality, or seasonal amplitudes; these are inferred from the data.
- The minimum number of rows for the main anomaly detection algorithm is 12 per time series. For time series with
  between 2 and 11 observations, anomaly detection produces a “naive” result in which all predicted values are equal to
  the last observed target value. For the labeled anomaly detection case, the number of observations used is the number
  of rows where the label column is false.
- The minimum acceptable granularity of data is one second. (Timestamps must not be less than one second apart.)
- The minimum granularity of seasonal components is one minute. (The function cannot detect cyclic patterns at smaller
  time deltas.)
- The “season length” of autoregressive features is tied to the input frequency (24 for hourly data, 7 for daily data,
  and so on).
- Anomaly detection models, once trained, are immutable. You cannot update existing models with new data; you must train
  an entirely new model. Models do not support versioning. Generally, you should retrain models on a regular cadence,
  such as once a day, once a week, or once a month, depending on how frequently you receive new data, to help the model
  keep up with changing trends.
- This feature only detects anomalies in the test data; it cannot detect anomalies in the training data. Furthermore,
  timestamps in the test data must all be greater than timestamps in the training data. Ensure that the training data
  covers a typical period free of actual outliers, or label known outliers in a Boolean column.
- You cannot clone models or share models across roles or accounts. When cloning a schema or database, model objects are skipped.
- You cannot [replicate](/user-guide/account-replication-intro) an instance of the ANOMALY\_DETECTION
  class.

## Preparing for Anomaly Detection

Before you can use anomaly detection, you must:

- [Select a virtual warehouse](#label-analysis-anomaly-detection-selecting-warehouse)
  in which to train and run your models.
- [Grant the privileges to create anomaly detection objects](#label-analysis-anomaly-detection-privileges).

You might also want to [modify your search path](/sql-reference/snowflake-db-classes#label-update-search-path) to include
SNOWFLAKE.ML.

### Selecting a Virtual Warehouse

A Snowflake [virtual warehouse](/user-guide/warehouses) provides the compute resources for training and using your
machine learning models for this feature. This section provides general guidance on selecting the best size and type of
warehouse for this purpose, focusing on the training step (the most time-consuming and memory-intensive part of
the process).

#### Training on Single-Series Data

For models trained on single-series data, you should choose the warehouse type based on the size of your training data.
Standard warehouses are subject to a lower [Snowpark memory limit](/developer-guide/udf/python/udf-python-troubleshooting),
and are more appropriate for training jobs with fewer rows or exogenous features.
If your training data does not contain any exogenous features, you can train on a standard warehouse if the dataset has 5 million rows or less.
If your training data uses 5 or more exogenous features, then the maximum row count is lower.
Otherwise, Snowflake suggests using a [Snowpark-optimized warehouse](/user-guide/warehouses-snowpark-optimized) for larger training jobs.

In general, for single-series data, a larger warehouse size does not result in a faster training time or higher memory limits.
As a rough rule of thumb, training time is proportional to the number of rows in your time series. For example, on a XS
standard warehouse, with evaluation turned off (`CONFIG_OBJECT => {'evaluate': False}`), training on a
100,000-row dataset takes about 60 seconds, while training on a 1,000,000-row dataset takes about 125 seconds. With
evaluation turned on, training time increases roughly linearly by the number of splits used.

For best performance, Snowflake recommends using a dedicated warehouse without other concurrent workloads to train your model.

#### Training on Multi-Series Data

As with single-series data, choose the warehouse type based on the number of rows in your largest time series. If your
largest time series contains more than 5 million rows, the training job is likely to exceed memory limits on a standard
warehouse.

Unlike single-series data, multi-series data trains considerably faster on larger warehouse sizes.
The following data points can guide you in your selection. Once again, all these times are done with evaluation turned
off.

| Warehouse type and size | Number of time series | Number of rows per time series | Training time (seconds) |
| --- | --- | --- | --- |
| Standard XS | 1 | 100,000 | 60 seconds |
| Standard XS | 10 | 100,000 | 204 seconds |
| Standard XS | 100 | 100,000 | 720 seconds |
| Standard XL | 10 | 100,000 | 104 seconds |
| Standard XL | 100 | 100,000 | 211 seconds |
| Standard XL | 1000 | 100,000 | 840 seconds |
| Snowpark-optimized XL | 10 | 100,000 | 65 seconds |
| Snowpark-optimized XL | 100 | 100,000 | 293 seconds |
| Snowpark-optimized XL | 1000 | 100,000 | 831 seconds |

Expand

Show lessSee more

#### Detecting Anomalies

The inference step takes approximately 1 second to process 100 rows in the input dataset, regardless of warehouse size.

### Granting Privileges to Create Anomaly Detection Objects

Training an anomaly detection model results in a schema-level object. Therefore, the role you use to create models must
have the CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION privilege on the schema where the model is created, which allows the
model to be stored there. This privilege is similar to other schema privileges like CREATE TABLE or CREATE VIEW.

Snowflake recommends that you create a role named `analyst` to be used by people who need to detect anomalies.

In the following example, the `admin` role is the owner of the schema `admin_db.admin_schema`. The
`analyst` role needs to create models in this schema.

Copy code

```
USE ROLE admin;
GRANT USAGE ON DATABASE admin_db TO ROLE analyst;
GRANT USAGE ON SCHEMA admin_schema TO ROLE analyst;
GRANT CREATE SNOWFLAKE.ML.ANOMALY_DETECTION ON SCHEMA admin_db.admin_schema TO ROLE analyst;
```

To use this schema, a user assumes the role `analyst`:

Copy code

```
USE ROLE analyst;
USE SCHEMA admin_db.admin_schema;
```

If the `analyst` role has CREATE SCHEMA privileges in database `analyst_db`, the role can create a new schema
`analyst_db.analyst_schema` and create anomaly detection models in that schema:

Copy code

```
USE ROLE analyst;
CREATE SCHEMA analyst_db.analyst_schema;
USE SCHEMA analyst_db.analyst_schema;
```

To revoke a role’s model creation privilege on the schema, use [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege):

Copy code

```
REVOKE CREATE SNOWFLAKE.ML.ANOMALY_DETECTION ON SCHEMA admin_db.admin_schema FROM ROLE analyst;
```

## Setting Up the Data for the Examples

The examples in the following sections use a sample dataset that contains daily sales for items in different stores along with
daily weather data (humidity and temperature). The dataset also contains a column that indicates whether the day is a holiday.

1. Execute the following statements to create a table named `historical_sales_data` that contains the training data for the model:

> Copy code
>
> ```
> CREATE OR REPLACE TABLE historical_sales_data (
>   store_id NUMBER, item VARCHAR, date TIMESTAMP_NTZ, sales FLOAT, label BOOLEAN,
>   temperature NUMBER, humidity FLOAT, holiday VARCHAR);
>
> INSERT INTO historical_sales_data VALUES
>   (1, 'jacket', to_timestamp_ntz('2020-01-01'), 2.0, false, 50, 0.3, 'new year'),
>   (1, 'jacket', to_timestamp_ntz('2020-01-02'), 3.0, false, 52, 0.3, null),
>   (1, 'jacket', to_timestamp_ntz('2020-01-03'), 5.0, false, 54, 0.2, null),
>   (1, 'jacket', to_timestamp_ntz('2020-01-04'), 30.0, true, 54, 0.3, null),
>   (1, 'jacket', to_timestamp_ntz('2020-01-05'), 8.0, false, 55, 0.2, null),
>   (1, 'jacket', to_timestamp_ntz('2020-01-06'), 6.0, false, 55, 0.2, null),
>   (1, 'jacket', to_timestamp_ntz('2020-01-07'), 4.6, false, 55, 0.2, null),
>   (1, 'jacket', to_timestamp_ntz('2020-01-08'), 2.7, false, 55, 0.2, null),
>   (1, 'jacket', to_timestamp_ntz('2020-01-09'), 8.6, false, 55, 0.2, null),
>   (1, 'jacket', to_timestamp_ntz('2020-01-10'), 9.2, false, 55, 0.2, null),
>   (1, 'jacket', to_timestamp_ntz('2020-01-11'), 4.6, false, 55, 0.2, null),
>   (1, 'jacket', to_timestamp_ntz('2020-01-12'), 7.0, false, 55, 0.2, null),
>   (1, 'jacket', to_timestamp_ntz('2020-01-13'), 3.6, false, 55, 0.2, null),
>   (1, 'jacket', to_timestamp_ntz('2020-01-14'), 8.0, false, 55, 0.2, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-01'), 3.4, false, 50, 0.3, 'new year'),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-02'), 5.0, false, 52, 0.3, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-03'), 4.0, false, 54, 0.2, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-04'), 5.4, false, 54, 0.3, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-05'), 3.7, false, 55, 0.2, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-06'), 3.2, false, 55, 0.2, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-07'), 3.2, false, 55, 0.2, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-08'), 5.6, false, 55, 0.2, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-09'), 7.3, false, 55, 0.2, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-10'), 8.2, false, 55, 0.2, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-11'), 3.7, false, 55, 0.2, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-12'), 5.7, false, 55, 0.2, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-13'), 6.3, false, 55, 0.2, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-14'), 2.9, false, 55, 0.2, null);
> ```

1. Execute the following statements to create a table named `new_sales_data` that contains the data to analyze:

> Copy code
>
> ```
> CREATE OR REPLACE TABLE new_sales_data (
>   store_id NUMBER, item VARCHAR, date TIMESTAMP_NTZ, sales FLOAT,
>   temperature NUMBER, humidity FLOAT, holiday VARCHAR);
>
> INSERT INTO new_sales_data VALUES
>   (1, 'jacket', to_timestamp_ntz('2020-01-16'), 6.0, 52, 0.3, null),
>   (1, 'jacket', to_timestamp_ntz('2020-01-17'), 20.0, 53, 0.3, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-16'), 3.0, 52, 0.3, null),
>   (2, 'umbrella', to_timestamp_ntz('2020-01-17'), 70.0, 53, 0.3, null);
> ```

## Training, Using, Viewing, Deleting, and Updating Models

Use [CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/create-anomaly-detection#label-class-anomaly-detection-create) to create and train a model. The model is trained on the dataset you
provide.

Copy code

```
CREATE SNOWFLAKE.ML.ANOMALY_DETECTION mydetector(...);
```

See [ANOMALY\_DETECTION (SNOWFLAKE.ML)](/sql-reference/classes/anomaly_detection) for complete details about the SNOWFLAKE.ML.ANOMALY\_DETECTION
constructor. For examples of creating a model, see [Detecting Anomalies](#label-analysis-anomaly-detection-examples).

Note

SNOWFLAKE.ML.ANOMALY\_DETECTION runs using limited privileges, so by default it does not have access to your data. You must
therefore pass tables and views as [references](/developer-guide/stored-procedure/stored-procedures-calling-references), which pass along the
caller’s privileges. You can also provide a [query reference](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-query-references) instead of a
reference to a table or a view.

To create this reference, you can use the [TABLE keyword](/sql-reference/snowflake-db-classes#label-class-select-from-methods) with the table name, view name,
or query, or you can call the [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) or
[SYSTEM$QUERY\_REFERENCE](/sql-reference/functions/system_query_reference) function.

To detect anomalies, call the model’s [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies) method:

Copy code

```
CALL mydetector!DETECT_ANOMALIES(...);
```

To select columns from the tabular output of the method, you can
[call the method in the FROM clause](/sql-reference/snowflake-db-classes#label-class-select-from-methods):

Copy code

```
SELECT ts, forecast FROM TABLE(mydetector!DETECT_ANOMALIES(...));
```

To view a list of your models, use the [SHOW SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/show-anomaly-detection#label-class-anomaly-detection-show) command:

Copy code

```
SHOW SNOWFLAKE.ML.ANOMALY_DETECTION;
```

To remove a model, use the [DROP SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/drop-anomaly-detection#label-class-anomaly-detection-drop) command:

Copy code

```
DROP SNOWFLAKE.ML.ANOMALY_DETECTION <name>;
```

To update a model, delete it and train a new one. Models are immutable and cannot be updated in place.

## Detecting Anomalies

The following sections demonstrate how to use anomaly detection to detect outliers. These sections provide examples of
detecting anomalies for a single time series, for multiple time series, with and without exogenous variables, with a
user-defined prediction interval, and with a supervised (labeled) approach.

- [Detecting Anomalies for a Single Time Series (Unsupervised)](#label-analysis-anomaly-detection-single-series)
- [Training an Anomaly Detection Model with Labeled Data](#label-analysis-anomaly-detection-single-series-labeled)
- [Specifying the Prediction Interval For Anomaly Detection](#label-analysis-anomaly-detection-single-series-interval)
- [Including Additional Columns for Analysis](#label-analysis-anomaly-detection-single-series-add-columns)
- [Detecting Anomalies in Multiple Series](#label-analysis-anomaly-detection-multiple-series)

### Detecting Anomalies for a Single Time Series (Unsupervised)

To detect anomalies in your data:

1. Train an anomaly detection model using historical data.
2. Use the trained anomaly detection model to detect anomalies in historical or projected data. The timestamps in the test data
   must chronologically follow the timestamps in the training data. You need at least 2 data points to train a model, at least
   12 for non-naive results, and at least 60 for non-linear results.

See [ANOMALY\_DETECTION (SNOWFLAKE.ML)](/sql-reference/classes/anomaly_detection) for information on the parameters used in creating and using a model.

#### Training an Anomaly Detection Model

To create an anomaly detection model object, execute the [CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/create-anomaly-detection#label-class-anomaly-detection-create) command.

For example, suppose that you want to analyze the sales for jackets in the store with the `store_id` of 1:

1. Create a view or design a query that returns the data for training the model for anomaly detection.

   For this example, execute the [CREATE VIEW](/sql-reference/sql/create-view) command to create a view named `view_with_training_data`
   that contains the date and sales information:

   Copy code

   ```
   CREATE OR REPLACE VIEW view_with_training_data
     AS SELECT date, sales FROM historical_sales_data
    WHERE store_id=1 AND item='jacket';
   ```
2. Create an anomaly detection object, and train its model on the data in that view.

   For this example, execute the [CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/create-anomaly-detection#label-class-anomaly-detection-create) command to create an anomaly detection object named
   `basic_model`. Pass in the following arguments:

   Copy code

   ```
   CREATE OR REPLACE SNOWFLAKE.ML.ANOMALY_DETECTION basic_model(
     INPUT_DATA => TABLE(view_with_training_data),
     TIMESTAMP_COLNAME => 'date',
     TARGET_COLNAME => 'sales',
     LABEL_COLNAME => '');
   ```

   This example passes in a reference to a view as the INPUT\_DATA argument. The example
   [uses the TABLE keyword to create the reference](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-table-keyword). As an alternative, you can call
   [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) to create the reference.

   The purpose of the label column is to tell the model which rows are known anomalies. Because this example uses
   unsupervised training, you do not need to use the label column. Pass an empty string as the name of the label column.

   Tip

   If you don’t want to create a view for the INPUT\_DATA argument, you can pass in a
   [reference to a query](/developer-guide/stored-procedure/stored-procedures-calling-references#label-reference-object-query-references) that uses a SELECT statement that serves as an inline
   view.

   You can use the TABLE keyword to create this query reference. For example:

   Copy code

   ```
   CREATE OR REPLACE SNOWFLAKE.ML.ANOMALY_DETECTION basic_model(
     INPUT_DATA =>
    TABLE(SELECT date, sales FROM historical_sales_data WHERE store_id=1 AND item='jacket'),
     TIMESTAMP_COLNAME => 'date',
     TARGET_COLNAME => 'sales',
     LABEL_COLNAME => '');
   ```

   Escape any single quotes and other special characters with a backslash.

   As an alternative to using the TABLE keyword, you can call [SYSTEM$QUERY\_REFERENCE](/sql-reference/functions/system_query_reference) to create
   the query reference.

> If the command is executed successfully, a message indicates that your anomaly detection instance was created
> successfully:
>
> ```
> +--------------------------------------------+
> |                 status                     |
> +--------------------------------------------+
> | Instance basic_model successfully created. |
> +--------------------------------------------+
> ```

#### Using an Anomaly Detection Model to Detect Anomalies

Creating the anomaly detection object trains the model and stores it in the schema. To use the anomaly detection object
to detect anomalies, call the [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies) method of the object. For example:

1. Create a view or design a query that returns the data for analysis.

   For this example, execute the [CREATE VIEW](/sql-reference/sql/create-view) command to create a view named
   `view_with_data_to_analyze` that contains the date and sales information:

   Copy code

   ```
   CREATE OR REPLACE VIEW view_with_data_to_analyze
     AS SELECT date, sales FROM new_sales_data
    WHERE store_id=1 and item='jacket';
   ```
2. Using the object for the anomaly detection model (in this example, `basic_model`, which
   [you created earlier](#label-analysis-anomaly-detection-single-series)),
   call the [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies) method:

   Copy code

   ```
   CALL basic_model!DETECT_ANOMALIES(
     INPUT_DATA => TABLE(view_with_data_to_analyze),
     TIMESTAMP_COLNAME =>'date',
     TARGET_COLNAME => 'sales'
   );
   ```

   The method returns a table that includes rows for the data currently in the view `view_with_data_to_analyze` along with the
   prediction of the detector. For a description of the columns in this table, see [Returns](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies-output).

**Output**

The results have been rounded for readability.

```
+--------+-------------------------+----+----------+--------------+--------------+------------+--------------+--------------+
| SERIES | TS                      |  Y | FORECAST |  LOWER_BOUND |  UPPER_BOUND | IS_ANOMALY |   PERCENTILE |     DISTANCE |
+--------|-------------------------+----+----------+--------------+--------------+------------+--------------+--------------|
| NULL   | 2020-01-16 00:00:00.000 |  6 |      4.6 | -7.185885251 | 16.385885251 | False      | 0.6201873452 | 0.3059728606 |
| NULL   | 2020-01-17 00:00:00.000 | 20 |      9   | -2.785885251 | 20.785885251 | False      | 0.9918932208 | 2.404072476  |
+--------+-------------------------+----+----------+--------------+--------------+------------+--------------+--------------|
```

To save your results directly to a table, use [CREATE TABLE … AS SELECT …](/sql-reference/sql/create-table#label-ctas-syntax) and
[call the DETECT\_ANOMALIES method in the FROM clause](/sql-reference/snowflake-db-classes#label-class-select-from-methods):

Copy code

```
CREATE TABLE my_anomalies AS
  SELECT * FROM TABLE(basic_model!DETECT_ANOMALIES(
    INPUT_DATA => TABLE(view_with_data_to_analyze),
    TIMESTAMP_COLNAME =>'date',
    TARGET_COLNAME => 'sales'
  ));
```

As shown in the example above, when calling the method, omit the [CALL](/sql-reference/sql/call) command. Instead, put the call
in parentheses, preceded by the TABLE keyword.

### Training an Anomaly Detection Model with Labeled Data

In the previous example, the result of the model appears to be inaccurate. This is probably because:

- The anomaly detection model was trained on very little input data.
- A larger number of jackets (30) were sold on 2020-01-03. This skewed the predictions upward and increased the size of
  the prediction interval.

To improve the accuracy of the anomaly detection model, you can either include more training data or label the training data
(supervised training). Labeled training data has an additional Boolean column that indicates whether each row is a known
anomaly. Labeling can help the anomaly detection model to avoid overfitting to known anomalies in the training data.

To include labeled data in the training data, specify the column containing the label in the LABEL\_COLNAME constructor argument
of the [CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/create-anomaly-detection#label-class-anomaly-detection-create) command. For example:

1. Create a view or design a query that returns the labels with the training data.

   For this example, execute the [CREATE VIEW](/sql-reference/sql/create-view) command to create a view named
   `view_with_labeled_data` that contains the labels in a column named `label`:

   Copy code

   ```
   CREATE OR REPLACE VIEW view_with_labeled_data_for_training
     AS SELECT date, sales, label FROM historical_sales_data
    WHERE store_id=1 and item='jacket';
   ```
2. Create an object for the anomaly detection model, and train the model on the data in that view.

   For this example, execute the [CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/create-anomaly-detection#label-class-anomaly-detection-create) command to create an anomaly detection object named
   `model_trained_with_labeled_data`. The following statement creates the anomaly detection object:

   Copy code

   ```
   CREATE OR REPLACE SNOWFLAKE.ML.ANOMALY_DETECTION model_trained_with_labeled_data(
     INPUT_DATA => TABLE(view_with_labeled_data_for_training),
     TIMESTAMP_COLNAME => 'date',
     TARGET_COLNAME => 'sales',
     LABEL_COLNAME => 'label'
   );
   ```
3. Using this new anomaly detection model, call the [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies) method,
   passing in the same arguments that you used in [Detecting Anomalies for a Single Time Series (Unsupervised)](#label-analysis-anomaly-detection-single-series):

   Copy code

   ```
   CALL model_trained_with_labeled_data!DETECT_ANOMALIES(
     INPUT_DATA => TABLE(view_with_data_to_analyze),
     TIMESTAMP_COLNAME =>'date',
     TARGET_COLNAME => 'sales'
   );
   ```

   The method returns a table that includes rows for the data currently in the view `view_with_data_to_analyze` along with the
   prediction of the detector. For a description of the columns in this table, see [Returns](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies-output).

**Output**

The results have been rounded for readability.

> ```
> +--------+-------------------------+----+----------+---------------+--------------+------------+--------------+------------+
> | SERIES | TS                      |  Y | FORECAST |   LOWER_BOUND |  UPPER_BOUND | IS_ANOMALY |   PERCENTILE |   DISTANCE |
> +--------|-------------------------+----+----------+---------------+--------------+------------+--------------+------------|
> | NULL   | 2020-01-16 00:00:00.000 |  6 |        6 |  0.82         | 11.18        | False      | 0.5          | 0          |
> | NULL   | 2020-01-17 00:00:00.000 | 20 |        6 | -0.39         | 12.33        | True       | 0.99         | 5.70       |
> +--------+-------------------------+----+----------+---------------+--------------+------------+--------------+------------+
> ```

### Specifying the Prediction Interval For Anomaly Detection

You can detect anomalies with varying levels of sensitivity. To specify the percentage of observations to classify as
anomalies, create an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) that contains configuration settings for [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies), and set the
`prediction_interval` key to the percentage of the observations that should be marked as anomalies.

To construct this object, you can use either an [object constant](/sql-reference/data-types-semistructured#label-object-constant) or the
[OBJECT\_CONSTRUCT](/sql-reference/functions/object_construct) function.

Then, when calling the [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies) method, pass in this object as the CONFIG\_OBJECT argument.

By default, the value associated with the prediction\_interval key is set to 0.99, which means that roughly 1% of the data is
marked as anomalies. You can specify a value between 0 and 1:

- To mark fewer observations as anomalies, specify a higher value for `prediction_interval`.
- To mark more observations as anomalies, reduce the `prediction_interval` value.

The following example configures anomaly detection to be more strict by setting the `prediction_interval` to 0.995. The example also
uses the model trained on labeled data (that you set up in [Training an Anomaly Detection Model with Labeled Data](#label-analysis-anomaly-detection-single-series-labeled)) with the view
that contains the data to analyze (that you set up in [Detecting Anomalies for a Single Time Series (Unsupervised)](#label-analysis-anomaly-detection-single-series)).

Copy code

```
CALL model_trained_with_labeled_data!DETECT_ANOMALIES(
  INPUT_DATA => TABLE(view_with_data_to_analyze),
  TIMESTAMP_COLNAME => 'date',
  TARGET_COLNAME => 'sales',
  CONFIG_OBJECT => {'prediction_interval':0.995}
);
```

This statement produces a table that includes rows for the data currently in the view `view_with_data_to_analyze`. Each row
includes a column with the prediction of the detector. You can see that the result
of this model is more accurate than the unlabeled example.

**Output**

The results have been rounded for readability.

```
+--------+-------------------------+----+----------+---------------+--------------+------------+--------------+------------+
| SERIES | TS                      |  Y | FORECAST |   LOWER_BOUND |  UPPER_BOUND | IS_ANOMALY |   PERCENTILE |   DISTANCE |
+--------|-------------------------+----+----------+---------------+--------------+------------+--------------+------------|
| NULL   | 2020-01-16 00:00:00.000 |  6 |        6 |  0.36         | 11.64        | False      | 0.5          | 0          |
| NULL   | 2020-01-17 00:00:00.000 | 20 |        6 | -0.90         | 12.90        | True       | 0.99         | 5.70       |
+--------+-------------------------+----+----------+---------------+--------------+------------+--------------+------------+
```

### Including Additional Columns for Analysis

You can include additional columns in the data (for example, `temperature`, `weather`, `is_black_friday`) in the data for training
and analysis, if these columns can help you improve the identification of true anomalies.

To include new columns for analysis:

1. For the training data, create a view or design a query that includes the new columns, and create a new anomaly detection object,
   passing in a reference to that view or query.
2. For the data to analyze, create a view or design a query that includes the new columns, and pass a reference to that
   view or query to the [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies) method.

The anomaly detection model detects and uses the additional columns automatically.

Note

You must provide a view or query with the same set of additional columns when executing the [CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/create-anomaly-detection#label-class-anomaly-detection-create)
command and when calling the [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies) method. If there is a mismatch between the columns in the training data
passed to the command and the columns in the data for analysis passed to the function, an error occurs.

For example, suppose that you want to add the columns `temperature`, `humidity`, and `holiday`:

1. Create a view or design a query that returns the training data with these additional columns.

   For this example, execute the [CREATE VIEW](/sql-reference/sql/create-view) command to create a view named
   `view_with_training_data_extra_columns`:

   Copy code

   ```
   CREATE OR REPLACE VIEW view_with_training_data_extra_columns
     AS SELECT date, sales, label, temperature, humidity, holiday
    FROM historical_sales_data
    WHERE store_id=1 AND item='jacket';
   ```
2. Create an object for the anomaly detection model, and train the model on the data in that view.

   For this example, execute the [CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/create-anomaly-detection#label-class-anomaly-detection-create) command to create an anomaly detection object named
   `model_with_additional_columns`, passing in a reference to the new view:

   Copy code

   ```
   CREATE OR REPLACE SNOWFLAKE.ML.ANOMALY_DETECTION model_with_additional_columns(
     INPUT_DATA => TABLE(view_with_training_data_extra_columns),
     TIMESTAMP_COLNAME => 'date',
     TARGET_COLNAME => 'sales',
     LABEL_COLNAME => 'label'
   );
   ```
3. Create a view or design a query that returns the data to analyze with these additional columns.

   For this example, execute the [CREATE VIEW](/sql-reference/sql/create-view) command to create a view named
   `view_with_data_for_analysis_extra_columns`:

   Copy code

   ```
   CREATE OR REPLACE VIEW view_with_data_for_analysis_extra_columns
     AS SELECT date, sales, temperature, humidity, holiday
    FROM new_sales_data
    WHERE store_id=1 AND item='jacket';
   ```
4. Using this new anomaly detection object, call the [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies) method, passing in the new view:

   Copy code

   ```
   CALL model_with_additional_columns!DETECT_ANOMALIES(
     INPUT_DATA => TABLE(view_with_data_for_analysis_extra_columns),
     TIMESTAMP_COLNAME => 'date',
     TARGET_COLNAME => 'sales',
     CONFIG_OBJECT => {'prediction_interval':0.93}
   );
   ```

   This statement produces a table that includes rows for the data currently in the view
   `view_with_data_for_analysis_extra_columns` along with the prediction of the detector. The format of the output
   is the same as the format of the output shown for the commands that you ran earlier.

**Output**

The results have been rounded for readability.

> ```
> +--------+-------------------------+----+----------+-------------+--------------+------------+--------------+------------+
> | SERIES | TS                      |  Y | FORECAST | LOWER_BOUND |  UPPER_BOUND | IS_ANOMALY |   PERCENTILE |   DISTANCE |
> +--------|-------------------------+----+----------+-------------+--------------+------------+--------------+------------|
> | NULL   | 2020-01-16 00:00:00.000 |  6 |        6 | 2.34        |  9.64        | False      | 0.5          | 0          |
> | NULL   | 2020-01-17 00:00:00.000 | 20 |        6 | 1.56        | 10.451       | True       | 0.99         | 5.70       |
> +--------+-------------------------+----+----------+-------------+--------------+------------+--------------+------------+
> ```

### Detecting Anomalies in Multiple Series

The previous sections provided examples of detecting anomalies for a single series. These examples flagged anomalies for
the sale of one type of item (jackets) in one store (store ID 1). To detect anomalies for multiple time series at the
same time (for example, for multiple combinations of items and stores):

1. For the training data, create a view or design a query that includes a column that identifies the series, and create
   a new anomaly detection object, passing in a reference to that view or query and specifying the name of the series
   column for the SERIES\_COLNAME argument.
2. For the data to analyze, create a view or design a query that includes the column that identifies the series. Call
   the [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies) method, passing in a reference to that view or query and
   specifying the name of the series column for the SERIES\_COLNAME argument.

For example, suppose that you want to use the combination of the `store_id` and `item` columns to identify the series:

1. Create a view or design a query that returns the training data with the column for the series.

   For this example, execute the [CREATE VIEW](/sql-reference/sql/create-view) command to create a view named
   `view_with_training_data_multiple_series` that contains a column named `store_item` that identifies the series as
   a combination of store ID and item:

   Copy code

   ```
   CREATE OR REPLACE VIEW view_with_training_data_multiple_series
     AS SELECT
    [store_id, item] AS store_item,
    date,
    sales,
    label,
    temperature,
    humidity,
    holiday
     FROM historical_sales_data;
   ```
2. Create an object for the anomaly detection, and train the model on the data in that view.

   For this example, execute the [CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION](/sql-reference/classes/anomaly-detection/commands/create-anomaly-detection#label-class-anomaly-detection-create) command to create an anomaly detection object named
   `model_for_multiple_series`, passing in a reference to the new view and specifying `store_item` for the SERIES\_COLNAME
   argument:

   Copy code

   ```
   CREATE OR REPLACE SNOWFLAKE.ML.ANOMALY_DETECTION model_for_multiple_series(
     INPUT_DATA => TABLE(view_with_training_data_multiple_series),
     SERIES_COLNAME => 'store_item',
     TIMESTAMP_COLNAME => 'date',
     TARGET_COLNAME => 'sales',
     LABEL_COLNAME => 'label'
   );
   ```
3. Create a view or design a query that returns the data to analyze with the series column.

   For this example, execute the [CREATE VIEW](/sql-reference/sql/create-view) command to create a view named
   `view_with_data_for_analysis_multiple_series` that contains a column named `store_item` for the series:

   Copy code

   ```
   CREATE OR REPLACE VIEW view_with_data_for_analysis_multiple_series
     AS SELECT
    [store_id, item] AS store_item,
    date,
    sales,
    temperature,
    humidity,
    holiday
     FROM new_sales_data;
   ```
4. Using this new anomaly detection object, call the [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies) method, passing in the new view and specifying
   `store_item` for the SERIES\_COLNAME argument:

   Copy code

   ```
   CALL model_for_multiple_series!DETECT_ANOMALIES(
     INPUT_DATA => TABLE(view_with_data_for_analysis_multiple_series),
     SERIES_COLNAME => 'store_item',
     TIMESTAMP_COLNAME => 'date',
     TARGET_COLNAME => 'sales',
     CONFIG_OBJECT => {'prediction_interval':0.995}
   );
   ```

   This statement produces a table that includes rows for the data currently in the view
   `view_with_data_for_analysis_multiple_series` along with the prediction of the detector. The output includes the column that
   identifies the series.

**Output**

The results have been rounded for readability.

> ```
> +--------------+-------------------------+----+----------+---------------+--------------+------------+---------------+--------------+
> | SERIES       | TS                      |  Y | FORECAST |   LOWER_BOUND |  UPPER_BOUND | IS_ANOMALY |    PERCENTILE |     DISTANCE |
> |--------------+-------------------------+----+----------+---------------+--------------+------------+---------------+--------------|
> | [            | 2020-01-16 00:00:00.000 |  3 |      6.3 |  2.07         | 10.53        | False      | 0.01          | -2.19         |
> |   2,         |                         |    |          |               |              |            |               |              |
> |   "umbrella" |                         |    |          |               |              |            |               |              |
> | ]            |                         |    |          |               |              |            |               |              |
> | [            | 2020-01-17 00:00:00.000 | 70 |      2.9 | -1.33         |  7.13        | True       | 1             | 44.54         |
> |   2,         |                         |    |          |               |              |            |               |              |
> |   "umbrella" |                         |    |          |               |              |            |               |              |
> | ]            |                         |    |          |               |              |            |               |              |
> | [            | 2020-01-16 00:00:00.000 |  6 |      6   |  0.36         | 11.64        | False      | 0.5           |  0           |
> |   1,         |                         |    |          |               |              |            |               |              |
> |   "jacket"   |                         |    |          |               |              |            |               |              |
> | ]            |                         |    |          |               |              |            |               |              |
> | [            | 2020-01-17 00:00:00.000 | 20 |      6   | -0.90         | 12.90        | True       | 0.99          |  5.70         |
> |   1,         |                         |    |          |               |              |            |               |              |
> |   "jacket"   |                         |    |          |               |              |            |               |              |
> | ]            |                         |    |          |               |              |            |               |              |
> +--------------+-------------------------+----+----------+---------------+--------------+------------+---------------+--------------+
> ```

## Visualizing Anomalies and Interpreting the Results

Use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to review and visualize the results of anomaly detection. In Snowsight, when
you call the [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies) method, the results are displayed in a table under the worksheet.

![Results from DETECT_ANOMALIES method displayed in a table](/static/images/screens/anomaly-detection-table.png)

To visualize the results, you can use the chart feature in Snowsight.

1. After calling the [<model\_name>!DETECT\_ANOMALIES](/sql-reference/classes/anomaly-detection/methods/detect_anomalies#label-class-anomaly-detection-detect-anomalies) method, select **Charts** above the results table.
2. In the **Data** section on the right side of the chart:

   1. Select the **Y** column, and under **Aggregation**, select **None**.
   2. Select the **TS** column, and under **Bucketing**, select **None**.
3. Add the **LOWER\_BOUND** and **UPPER\_BOUND** columns, and under **Aggregation**, select **None**.
4. To display the initial visualization, select **Chart**.

   ![Results from DETECT_ANOMALIES method displayed in a chart](/static/images/screens/anomaly-detection-chart.png)
5. Select **Add Column** on the right side of the page, and select the columns you want to visualize:

   - **LOWER\_BOUND**
   - **UPPER\_BOUND**
   - **IS\_ANOMALY**

   Results:

   ![Anomaly displayed in a chart](/static/images/screens/anomaly-detection-anomaly.png)
6. Hover over the high spike to see that Y lies outside of the upper bound and is tagged with a 1 in the **IS\_ANOMALY** field.

Tip

To better understand your results, try [Top Insights](/user-guide/ml-functions/top-insights).

## Automate Anomaly Detection with Snowflake Tasks and Alerts

You can create an automated anomaly detection pipeline, both for retraining the model and for monitoring your data for anomalies, by using Anomaly Detection functions within Snowflake Tasks or Alerts.

- [Recurring Training with a Snowflake Task](#label-analysis-anomaly-detection-periodic-retraining-tasks)
- [Monitoring with a Snowflake Task](#label-analysis-anomaly-detection-monitoring-tasks)
- [Monitoring with a Snowflake Alert](#label-analysis-anomaly-detection-monitoring-alerts)

### Recurring Training with a Snowflake Task

You can update your model to reflect the most up-to-date data using [Snowflake Tasks](/user-guide/tasks-intro).

To create a task that refreshes the anomaly detection object every hour, run following statement, replacing `your_warehouse_name` with your warehouse name:

Copy code

```
CREATE OR REPLACE TASK ad_model_retrain_task
WAREHOUSE = <your_warehouse_name>
SCHEDULE = '60 MINUTE'
AS
EXECUTE IMMEDIATE
$$
BEGIN
  CREATE OR REPLACE SNOWFLAKE.ML.ANOMALY_DETECTION model_trained_with_labeled_data(
    INPUT_DATA => TABLE(view_with_labeled_data_for_training),
    TIMESTAMP_COLNAME => 'date',
    TARGET_COLNAME => 'sales',
    LABEL_COLNAME => 'label'
  );
END;
$$;
```

By default, newly created tasks are suspended.

To resume the task, execute the [ALTER TASK … RESUME](/sql-reference/sql/alter-task) command:

Copy code

```
ALTER TASK ad_model_retrain_task RESUME;
```

To pause the task, execute the [ALTER TASK … SUSPEND](/sql-reference/sql/alter-task) command:

Copy code

```
ALTER TASK ad_model_retrain_task SUSPEND;
```

### Monitoring with a Snowflake Task

You can also use Snowflake Tasks to monitor your data at a given frequency.

First, create a table to hold the results
of anomaly detection:

Copy code

```
CREATE OR REPLACE TABLE anomaly_res_table (
  ts TIMESTAMP_NTZ, y FLOAT, forecast FLOAT, lower_bound FLOAT, upper_bound FLOAT,
  is_anomaly BOOLEAN, percentile FLOAT, distance FLOAT);
```

Create a task to store the results of a recurring anomaly detection operation in the table.
This example sets the `WAREHOUSE` parameter to `snowhouse`. You can replace that with
your own warehouse:

Copy code

```
CREATE OR REPLACE TASK ad_model_monitoring_task
WAREHOUSE = snowhouse
SCHEDULE = '1 minute'
AS
EXECUTE IMMEDIATE
$$
BEGIN
  INSERT INTO anomaly_res_table (ts, y, forecast, lower_bound, upper_bound, is_anomaly, percentile, distance)
    SELECT * FROM TABLE(
      model_trained_with_labeled_data!DETECT_ANOMALIES(
        INPUT_DATA => TABLE(view_with_data_to_analyze),
        TIMESTAMP_COLNAME => 'date',
        TARGET_COLNAME => 'sales',
        CONFIG_OBJECT => {'prediction_interval':0.99}
    )
  );
END;
$$;
```

To resume the task, execute the [ALTER TASK … RESUME](/sql-reference/sql/alter-task) command:

Copy code

```
ALTER TASK ad_model_monitoring_task RESUME;
```

`anomaly_res_table` then contains all the results for each task run.

To pause the task, execute the [ALTER TASK … SUSPEND](/sql-reference/sql/alter-task) command:

Copy code

```
ALTER TASK ad_model_monitoring_task SUSPEND;
```

### Monitoring with a Snowflake Alert

You can also use [Snowflake Alerts](/user-guide/alerts) to monitor your data at a given frequency and send you
email with detected anomalies. The following statements create an alert that detects anomalies every minute. First you
define a [stored procedure](/developer-guide/stored-procedure/stored-procedures-overview) to detect anomalies, then create an alert
that uses that stored procedure.

Note

You must set up email integration to send mail from a stored procedure; see [Notifications in Snowflake](/user-guide/notifications/about-notifications).

Copy code

```
CREATE OR REPLACE PROCEDURE extract_anomalies()
  RETURNS TABLE()
  LANGUAGE SQL
  AS
  $$
    BEGIN
      let res RESULTSET := (SELECT * FROM TABLE(
        model_trained_with_labeled_data!DETECT_ANOMALIES(
          INPUT_DATA => TABLE(view_with_data_to_analyze),
          TIMESTAMP_COLNAME => 'date',
          TARGET_COLNAME => 'sales',
          CONFIG_OBJECT => {'prediction_interval':0.99}
        ))
        WHERE is_anomaly = TRUE
      );
      RETURN TABLE(res);
    END;
  $$
  ;

CREATE OR REPLACE ALERT sample_sales_alert
WAREHOUSE = <your_warehouse_name>
SCHEDULE = '1 MINUTE'
IF (EXISTS (CALL extract_anomalies()))
THEN
CALL SYSTEM$SEND_EMAIL(
  'sales_email_alert',
  'your_email@snowflake.com',
  'Anomalous Sales Data Detected in data stream',
  CONCAT(
    'Anomalous Sales Data Detected in data stream \n',
    'Value outside of prediction interval detected in the most recent run at ',
    current_timestamp(1)
  ));
```

To start or resume the alert, execute the [ALTER ALERT … RESUME](/sql-reference/sql/alter-alert) command:

Copy code

```
ALTER ALERT sample_sales_alert RESUME;
```

To pause the alert, execute the [ALTER ALERT … SUSPEND](/sql-reference/sql/alter-alert) command:

Copy code

```
ALTER ALERT sample_sales_alert SUSPEND;
```

## Understanding Feature Importance

An anomaly detection model can explain the relative importance of all features used in your model, including any exogenous
variables that you choose, automatically generated time features (such as day of week or week of year), and
transformations of your target variable (such as rolling averages and auto-regressive lags). This information is useful
in understanding what factors are really influencing your data.

The [<model\_name>!EXPLAIN\_FEATURE\_IMPORTANCE](/sql-reference/classes/anomaly-detection/methods/explain_feature_importance#label-class-anomaly-detection-explain-feature-importance) method counts the number of times the
model’s trees used each feature to make a decision. These feature importance scores are then normalized to values
between 0 and 1 so that their sum is 1. The resulting scores represent an approximate ranking of the features in your
trained model.

Features that are close in score have similar importance. For extremely simple series (for example, when the target
column has a constant value), all feature importance scores may be zero.

Using multiple features that are very similar to each other may result in reduced importance scores for those features.
For example, if one feature is *quantity of items sold* and another is *quantity of items in inventory*, the values may be
correlated because you can’t sell more than you have and because you try to manage inventory so you won’t have more in
stock than you will sell. If two features are identical, the model may treat them as interchangeable when making
decisions, resulting in feature importance scores that are half of what those scores would be if only one of the
features were included.

Feature importance also reports *lag features.* During training, the model infers the frequency (hourly, daily, or weekly)
of your training data. The feature `lagx` (e.g. `lag24`) is the value of the target variable *x* time units ago.
For example, if your data is inferred to be hourly, `lag24` represents your target variable 24 hours ago.

All other transformations of your target variable (rolling averages, etc.) are summarized as
`aggregated_endogenous_features` in the results table.

### Limitations

- You cannot choose the technique used to calculate feature importance.
- Feature importance scores can be helpful for gaining intuition about which features are important to your model’s
  accuracy, but the actual values should be considered estimates.

### Example

To understand the relative importance of your features to your model, train a model, and then call
[<model\_name>!EXPLAIN\_FEATURE\_IMPORTANCE](/sql-reference/classes/anomaly-detection/methods/explain_feature_importance#label-class-anomaly-detection-explain-feature-importance). In this example, you first create random data with
two exogenous variables: one that is random and therefore unlikely to be very important to your model, and one that
is a copy of your target and therefore likely to be more important to your model.

Execute the following statements to generate the data, train a model on it, and get the importance of the features:

Copy code

```
CREATE OR REPLACE VIEW v_random_data AS SELECT
  DATEADD('minute', ROW_NUMBER() over (ORDER BY 1), '2023-12-01')::TIMESTAMP_NTZ ts,
  MOD(SEQ1(),10) y,
  UNIFORM(1, 100, RANDOM(0)) exog_a
FROM TABLE(GENERATOR(ROWCOUNT => 500));

CREATE OR REPLACE VIEW v_feature_importance_demo AS SELECT
  ts,
  y,
  exog_a
FROM v_random_data;

SELECT * FROM v_feature_importance_demo;

CREATE OR REPLACE SNOWFLAKE.ML.ANOMALY_DETECTION anomaly_model_feature_importance_demo(
  INPUT_DATA => TABLE(v_feature_importance_demo),
  TIMESTAMP_COLNAME => 'ts',
  TARGET_COLNAME => 'y',
  LABEL_COLNAME => ''
);

CALL anomaly_model_feature_importance_demo!EXPLAIN_FEATURE_IMPORTANCE();
```

**Output**

Because this example uses random data, do not expect your output to match this exactly.

```
+--------+------+--------------------------------------+-------+-------------------------+
| SERIES | RANK | FEATURE_NAME                         | SCORE | FEATURE_TYPE            |
+--------+------+--------------------------------------+-------+-------------------------+
| NULL   |    1 | aggregated_endogenous_trend_features |  0.36 | derived_from_endogenous |
| NULL   |    2 | exog_a                               |  0.22 | user_provided           |
| NULL   |    3 | epoch_time                           |  0.15 | derived_from_timestamp  |
| NULL   |    4 | minute                               |  0.13 | derived_from_timestamp  |
| NULL   |    5 | lag60                                |  0.07 | derived_from_endogenous |
| NULL   |    6 | lag120                               |  0.06 | derived_from_endogenous |
| NULL   |    7 | hour                                 |  0.01 | derived_from_timestamp  |
+--------+------+--------------------------------------+-------+-------------------------+
```

## Inspecting Training Logs

When you train multiple series with `CONFIG_OBJECT => {'ON_ERROR': 'SKIP'}`, individual time series models can
fail to train without the overall training process failing. To understand which time series failed and why, call
`<model_instance>!SHOW_TRAINING_LOGS`.

### Example

Copy code

```
CREATE TABLE t_error(date TIMESTAMP_NTZ, sales FLOAT, series VARCHAR);
INSERT INTO t_error VALUES
  (TO_TIMESTAMP_NTZ('2019-12-20'), 1.0, 'A'),
  (TO_TIMESTAMP_NTZ('2019-12-21'), 2.0, 'A'),
  (TO_TIMESTAMP_NTZ('2019-12-22'), 3.0, 'A'),
  (TO_TIMESTAMP_NTZ('2019-12-23'), 2.0, 'A'),
  (TO_TIMESTAMP_NTZ('2019-12-24'), 1.0, 'A'),
  (TO_TIMESTAMP_NTZ('2019-12-25'), 2.0, 'A'),
  (TO_TIMESTAMP_NTZ('2019-12-26'), 3.0, 'A'),
  (TO_TIMESTAMP_NTZ('2019-12-27'), 2.0, 'A'),
  (TO_TIMESTAMP_NTZ('2019-12-28'), 1.0, 'A'),
  (TO_TIMESTAMP_NTZ('2019-12-29'), 2.0, 'A'),
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

CREATE SNOWFLAKE.ML.ANOMALY_DETECTION model(
  INPUT_DATA => TABLE(SELECT date, sales, series FROM t_error),
  SERIES_COLNAME => 'series',
  TIMESTAMP_COLNAME => 'date',
  TARGET_COLNAME => 'sales',
  LABEL_COLNAME => '',
  CONFIG_OBJECT => {'ON_ERROR': 'SKIP'}
);

CALL model!SHOW_TRAINING_LOGS();
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

## Cost Considerations

For details on costs for using ML functions, see [Cost Considerations](/guides-overview-ml-functions#label-ml-functions-costs) in the ML functions overview.
