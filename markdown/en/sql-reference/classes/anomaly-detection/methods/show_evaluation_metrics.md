# <model\_name>!SHOW\_EVALUATION\_METRICS

Returns out-of-sample evaluation metrics.

If you need to select specific columns from the data returned by this method, you can call the method in the FROM clause of a
SELECT statement. See [Selecting columns from SQL class instance methods that return tabular data](/sql-reference/snowflake-db-classes#label-class-select-from-methods).

## Syntax

You can call this method to retrieve the cross-validation metrics generated when the model was trained, or you
can call it with additional data that was not available at training time (out-of-sample data) and receive
metrics based on how well the model predicts that data.

**Return time-series cross-validation metrics generated at training time:**

These metrics are available only if `evaluate=TRUE` in the `CONFIG_OBJECT` during model construction
(this is the default).

Copy code

```
<model_name>!SHOW_EVALUATION_METRICS();
```

**Compute cross-validation metrics on additional out-of-sample data:**

Copy code

```
<model_name>!SHOW_EVALUATION_METRICS(
  INPUT_DATA => <input_data>,
  [ SERIES_COLNAME => '<series_colname>', ]
  TIMESTAMP_COLNAME => '<timestamp_colname>',
  TARGET_COLNAME => '<target_colname>',
  LABEL_COLNAME => '<label_column_name>',
  [ CONFIG_OBJECT => <config_object> ]
);
```

## Arguments

The following arguments apply only to the additional out-of-sample data use case.

**Required:**

Not all of the following arguments are required for every use case.

`INPUT_DATA => input_data`
:   A [reference](/developer-guide/stored-procedure/stored-procedures-calling-references) to a table, view, or query
    that contains the future timestamps and values of the target and any exogenous variables used during training. Columns
    are matched between this argument and the original exogenous training data by name.

    To create this reference, you can use the [TABLE keyword](/sql-reference/snowflake-db-classes#label-class-select-from-methods) with the table name, view name,
    or query, or you can call the [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) or
    [SYSTEM$QUERY\_REFERENCE](/sql-reference/functions/system_query_reference) function.

`TIMESTAMP_COLNAME => 'timestamp_colname'`
:   Name of the column containing the timestamps in `input_data`.

`TARGET_COLNAME => 'target_colname'`
:   Name of the column containing the target (dependent value) in `input_data`.

`LABEL_COLNAME => 'label_column_name'`
:   Name of the column containing the labels for the data. Labels are Boolean (true/false) values indicating
    whether a given row is a known anomaly. If you do not have labeled data, pass an empty string (`''`) for this argument.

**Optional:**

`SERIES_COLNAME => 'series_colname'`
:   Name of the column in `input_data` specifying the series.

`CONFIG_OBJECT => config_object`
:   An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) containing key-value pairs used to configure the evaluation job.

    | Key | Type | Default | Description |
    | --- | --- | --- | --- |
    | `prediction_interval` | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | 0.99 | A value greater than or equal to 0.0 and less than 1.0. The default value of 0.95 means 95% of future points are expected to fall within the interval [lower\_bound, upper\_bound] derived from the forecast result. |
    | `on_error` | [STRING](/sql-reference/data-types-text#label-character-datatypes) | `'ABORT'` | String (constant) specifying the error handling method. This is most useful when forecasting multiple series. Supported values are:   - `'abort'`: Abort the model forecasting operation if an error is encountered in any time series. - `'skip'`: Skip any time series where forecasting encounters an error. This allows forecasting   to succeed for other time series. Series that fail are absent from the model output. |

    Expand

    Show lessSee more

## Output

| Column | Type | Description |
| --- | --- | --- |
| SERIES | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | Series value (NULL if model was trained with single time series). |
| ERROR\_METRIC | [VARCHAR](/sql-reference/data-types-text#label-character-datatypes) | The name of the error metric used. The method returns the following metrics:  Point Metrics:  - `MAE`: [Mean Absolute Error](https://en.wikipedia.org/wiki/Mean_absolute_error). - `MAPE`: [Mean Absolute Percentage Error](https://en.wikipedia.org/wiki/Mean_absolute_percentage_error). - `MDA`: [Mean Directional Accuracy](https://en.wikipedia.org/wiki/Mean_directional_accuracy). - `MSE`: [Mean Squared Error](https://en.wikipedia.org/wiki/Mean_squared_error). - `SMAPE`: [Symmetric Mean Absolute Percentage Error](https://en.wikipedia.org/wiki/Symmetric_mean_absolute_percentage_error).  Interval Metrics: These metrics use the `prediction_interval` argument from the [Evaluation configuration](/sql-reference/classes/anomaly-detection/commands/create-anomaly-detection#label-anomaly-detection-evaluation-config).  - `COVERAGE_INTERVAL`: The proportion of actual values that fall within the prediction interval. - `WINKLER_ALPHA`: [Winkler Score](https://otexts.com/fpp3/distaccuracy.html#winkler-score). |
| LOGS | [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) | Contains error or warning messages. |

Expand

Show lessSee more
