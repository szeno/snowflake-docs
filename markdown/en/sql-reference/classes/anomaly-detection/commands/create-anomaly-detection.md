# CREATE SNOWFLAKE.ML.ANOMALY\_DETECTION

Creates a new anomaly detection model or replaces an existing one using
the training data you provide.

## Syntax

Copy code

```
CREATE [ OR REPLACE ] SNOWFLAKE.ML.ANOMALY_DETECTION <model_name>(
  INPUT_DATA => <reference_to_training_data>,
  [ SERIES_COLNAME => '<series_column_name>', ]
  TIMESTAMP_COLNAME => '<timestamp_column_name>',
  TARGET_COLNAME => '<target_column_name>',
  LABEL_COLNAME => '<label_column_name>',
  [ CONFIG_OBJECT => <config_object> ]
)
[ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
[ COMMENT = '<string_literal>' ]
```

## Parameters

`model_name`
:   Specifies the identifier (*model\_name*) for the anomaly detector object; must be unique for the schema in which the object is
    created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive. For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Constructor arguments

**Required:**

`INPUT_DATA => reference_to_training_data`
:   Specifies a [reference](/developer-guide/stored-procedure/stored-procedures-calling-references) to the table, view, or query that returns
    the training data for the model.

    To create this reference, you can use the [TABLE keyword](/sql-reference/snowflake-db-classes#label-class-select-from-methods) with the table name, view name,
    or query, or you can call the [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) or
    [SYSTEM$QUERY\_REFERENCE](/sql-reference/functions/system_query_reference) function.

`TIMESTAMP_COLNAME => 'timestamp_column_name'`
:   Specifies the name of the column containing the timestamps (TIMESTAMP\_NTZ) in the time series data.

`TARGET_COLNAME => 'target_column_name'`
:   Specifies the name of the column containing the data (NUMERIC or FLOAT) to analyze.

`LABEL_COLNAME => 'label_column_name'`
:   Specifies the name of the column containing the labels for the data. Labels are Boolean (true/false) values indicating
    whether a given row is a known anomaly. If you do not have labeled data, pass an empty string (`''`) for this argument.

**Optional:**

`SERIES_COLNAME => 'series_column_name'`
:   Name of the column containing the identifier for the series (for multi-series data). This column should be a
    VARIANT because it can be any kind of value or a combination of values from more than one column in an array.

`CONFIG_OBJECT => config_object`
:   An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) containing key-value pairs used to configure the model training job.

    | Key | Type | Default | Description |
    | --- | --- | --- | --- |
    | `aggregation_categorical` | [STRING](/sql-reference/data-types-text#label-character-datatypes) | `'MODE'` | The aggregation method for categorical features. Supported values are:   - `'MODE'`: The most frequent value. - `'FIRST'`: The earliest value. - `'LAST'`: The latest value. |
    | `aggregation_numeric` | [STRING](/sql-reference/data-types-text#label-character-datatypes) | `'MEAN'` | The aggregation method for numeric features. Supported values are:   - `'MEAN'`: The average of the values. - `'MEDIAN'`: The middle value. - `MODE`: The most frequent value. - `'MIN'`: The smallest value. - `'MAX'`: The largest value. - `'SUM'`: The total of the values. - `'FIRST'`: The earliest value. - `'LAST'`: The latest value. |
    | `aggregation_target` | [STRING](/sql-reference/data-types-text#label-character-datatypes) | Same as `aggregation_numeric`, or `'MEAN'` if not specified | The aggregation method for the target value. Supported values are:   - `'MEAN'`: The average of the values. - `'MEDIAN'`: The middle value. - `MODE`: The most frequent value. - `'MIN'`: The smallest value. - `'MAX'`: The largest value. - `'SUM'`: The total of the values. - `'FIRST'`: The earliest value. - `'LAST'`: The latest value. |
    | `evaluate` | [BOOLEAN](/sql-reference/data-types-logical#label-data-type-boolean) | TRUE | Whether evaluation metrics should be generated. If TRUE, additional models are trained for cross-validation using the parameters in the `evaluation_config`. |
    | `evaluation_config` | [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) | See [Evaluation configuration](#label-anomaly-detection-evaluation-config). | An optional config object to specify how out-of-sample evaluation metrics should be generated. See next section. |
    | `frequency` | [STRING](/sql-reference/data-types-text#label-character-datatypes) | n/a | The frequency of the time series. If not specified, the model infers the frequency. The value must be a string representing a time period, such as `'1 day'`. Supported units include seconds, minutes, hours, days, weeks, months, quarters, and years. You may use singular (“hour”) or plural (“hours”) for the interval name, but may not abbreviate. |
    | `lower_bound` | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) or NULL | NULL | The lower bound for the target value. If specified, the model will not predict values below this threshold. |
    | `upper_bound` | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) or NULL | NULL | The upper bound for the target value. If specified, the model will not predict values above this threshold. |
    | `on_error` | [STRING](/sql-reference/data-types-text#label-character-datatypes) | `'ABORT'` | String (constant) that specifies the error handling method for training. This is most useful when training multiple series. Supported values are:   - `'abort'`: Abort training if an error is encountered in any time series. - `'skip'`: Skip any time series where training encounters an error. This allows training to succeed for other time series.   To see which series failed during model training, call the model’s [<model\_name>!SHOW\_TRAINING\_LOGS](/sql-reference/classes/anomaly-detection/methods/show_training_logs#label-class-anomaly-show-training-logs) method. |

    Expand

    Show lessSee more

## Evaluation configuration

The `evaluation_config` object contains key-value pairs that configure cross-validation. These parameters are from the scikit-learn
[TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)
cross-validator.

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `n_splits` | [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer) | 5 | Number of splits. |
| `max_train_size` | [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer) or NULL (no maximum). | NULL | Maximum size for a single training set. |
| `test_size` | [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer) or NULL. | NULL | Used to limit the size of the test set. |
| `gap` | [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer) | 0 | Number of samples to exclude from the end of each training set before the test set. |
| `prediction_interval` | [FLOAT](/sql-reference/data-types-numeric#label-data-type-float) | 0.95 | The prediction interval used in calculating interval metrics. |

Expand

Show lessSee more

## Usage notes

- If the column names specified by the TIMESTAMP\_COLNAME, TARGET\_COLNAME, or LABEL\_COLNAME arguments do not exist in the table,
  view, or query specified by the INPUT\_DATA argument, an error occurs.
- [Replication](/user-guide/account-replication-intro) is supported only for instances
  of the [CUSTOM\_CLASSIFIER](/sql-reference/classes/custom_classifier) class.

## Examples

For a representative example, see the [anomaly detection example](/user-guide/ml-functions/anomaly-detection#label-analysis-anomaly-detection-ddl-examples).
