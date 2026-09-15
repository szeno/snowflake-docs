Categories:
:   [Model monitor functions](/sql-reference/functions-model-monitors)

# MODEL\_MONITOR\_PERFORMANCE\_METRIC

Gets performance metrics from a model monitor. Each model monitor monitors one machine learning model. See [ML Observability](/developer-guide/snowflake-ml/model-registry/model-observability) for model version monitors and [Gateway Monitoring & A/B Testing](/developer-guide/snowflake-ml/inference/gateway-monitor-and-ab-testing) for gateway model monitors.

## Syntax

### Model version monitor

Copy code

```
MODEL_MONITOR_PERFORMANCE_METRIC(<model_monitor_name>, <performance_metric_name>,
    [, <granularity> [, <start_time> [, <end_time> [, <extra_args> ] ] ] ] )
```

### Gateway model monitor

Copy code

```
MODEL_MONITOR_PERFORMANCE_METRIC(
  <model_monitor_name>, <performance_metric_name>
  [, <granularity> [, <start_time> [, <end_time> ] ] ],
  SERVICE => <service_name>
)
```

## Required arguments

### All monitor types

`model_monitor_name`
:   Name of the model monitor used to compute the metric.

    Valid values:

    A string that’s the name of the model monitor. It can be a simple or fully qualified name.

`performance_metric_name`
:   Name of the performance metric.

    Valid values if the model monitor is attached to a regression model:

    > - `'RMSE'`
    > - `'MAE'`
    > - `'MAPE'`
    > - `'MSE'`

    Valid values if the model monitor is attached to a binary classification model:

    > - `'ROC_AUC'`
    > - `'CLASSIFICATION_ACCURACY'`
    > - `'PRECISION'`
    > - `'RECALL'`
    > - `'F1_SCORE'`

    Valid values if the model monitor is attached to a multi-class classification model:

    > - `'CLASSIFICATION_ACCURACY'`
    > - `'MACRO_AVERAGE_PRECISION'`
    > - `'MACRO_AVERAGE_RECALL'`
    > - `'MICRO_AVERAGE_PRECISION'`
    > - `'MICRO_AVERAGE_RECALL'`

### Gateway model monitor

`SERVICE => service_name`
:   Name of the inference service whose performance metrics you are measuring.

    Valid values: A simple or fully qualified inference service identifier.

## Optional arguments

`granularity`
:   Granularity of the time range being queried. Default value is *1 DAY* for model version monitors and `AGGREGATION_WINDOW` for gateway model monitors.

    Valid values:

    > - `'<num> HOUR'` (valid for gateway model monitors only)
    > - `'<num> DAY'`
    > - `'<num> WEEK'`
    > - `'<num> MONTH'`
    > - `'<num> QUARTER'`
    > - `'<num> YEAR'`
    > - `'ALL'`
    > - `NULL`

`start_time`
:   Start of the time range used to compute the metric. The default value is 60 days before the current time for model version monitors, and 1 day before the current time for gateway model monitors. The default value is calculated each time you call the function.

    Valid values:

    > A timestamp expression or `NULL`.

`end_time`
:   End of the time range used to compute the metric. The default value is the current time, and is calculated each time you call the function.

    Valid values:

    > A timestamp expression or `NULL`.

`extra_args`
:   Additional arguments for segment-specific queries. This parameter is optional: if not provided, the query returns metrics for all data (non-segment query). The segment queries are not supported for gateway model monitors.

    Valid values: A string in JSON format specifying segment column and value pairs: `'{"SEGMENTS": [{"column": "<segment_column_name>", "value": "<segment_value>"}]}'`

    Note

    Currently, segment queries support only 1 segment column:value pair per query. You cannot query multiple segments
    simultaneously in a single function call.

    For more information about segments, see [ML Observability: Monitoring model behavior over time](/developer-guide/snowflake-ml/model-registry/model-observability).

## Returns

### Columns returned for all monitor types

| Column | Description | Example values |
| --- | --- | --- |
| `EVENT_TIMESTAMP` | Timestamp at the start of the time range. | `2024-01-01 00:00:00.000` |
| `METRIC_VALUE` | Value of the metric within the specified time range. | `0.5` |
| `COUNT_USED` | Number of records used to compute the metric. | `100` |
| `COUNT_UNUSED` | Number of records excluded from the metric computation. | `10` |
| `METRIC_NAME` | Name of the metric that has been computed. | `ROC_AUC` |
| `SEGMENT_COLUMN` | Name of the segment column for which the metric is computed (or NULL for non-segment queries). | `CUSTOMER_TIER` |
| `SEGMENT_VALUE` | Segment value for which the metric is computed (or NULL for non-segment queries). | `PREMIUM` |

Expand

Show lessSee more

### Additional columns for gateway model monitor

| Column | Description | Example values |
| --- | --- | --- |
| `SERVICE` | Name of the inference service for the metric. | `challenger_service` |
| `CI_VALUE` | 95% confidence interval with `lower` and `upper` bounds. Wilson CI for `CLASSIFICATION_ACCURACY`, `PRECISION`, `RECALL`, `F1_SCORE`, `MICRO_AVERAGE_PRECISION`, and `MICRO_AVERAGE_RECALL`; Wald CI for `MSE`, `RMSE`, and `MAE`. Returns `NULL` for other performance metrics. | `{"lower": 0.85, "upper": 0.92}` |

Expand

Show lessSee more

## Usage notes

If the value you’ve specified for `model_monitor_name` is case-sensitive or contains special characters or spaces, enclose it in double quotes.
You must enclose the double quotes within single quotes. For example, `'"<example_model_monitor_name>"'`.

If you don’t use double-quotes, the `model_monitor_name` is assumed to be case-insensitive.

To minimize potential impact from schema changes, update your queries to explicitly select only the necessary columns instead of using a wildcard (\*).

### General requirements

- The model monitor must be associated with a model that supports the requested metric type.
- The model monitor must contain the necessary data for each metric type, as described below.

### Metric requirements

The following are the required columns to get regression metrics:

- RMSE: Requires the `prediction_score` and `actual_score` columns
- MAE: Requires the `prediction_score` and `actual_score` columns
- MAPE: Requires the `prediction_score` and `actual_score` columns

The following are the required columns to get binary classification metrics:

- ROC\_AUC: Requires the `prediction_score` and `actual_class` columns
- CLASSIFICATION\_ACCURACY: Requires the `prediction_class` and `actual_class` columns
- PRECISION: Requires the `prediction_class` and `actual_class` columns
- RECALL: Requires the `prediction_class` and `actual_class` columns
- F1\_SCORE: Requires the `prediction_class` and `actual_class` columns

The following are the required columns to get multiclass classification metrics:

- CLASSIFICATION\_ACCURACY: Requires the `prediction_class` and `actual_class` columns
- MACRO\_AVERAGE\_PRECISION: Requires the `prediction_class` and `actual_class` columns
- MACRO\_AVERAGE\_RECALL: Requires the `prediction_class` and `actual_class` columns
- MICRO\_AVERAGE\_PRECISION: Requires the `prediction_class` and `actual_class` columns
- MICRO\_AVERAGE\_RECALL: Requires the `prediction_class` and `actual_class` columns

Note

For binary classification, you can use micro-average precision and recall metrics similarly to how you use classification accuracy in multi-class classification.

### Error cases

You might run into errors if you do the following:

- Request an accuracy metric when the monitor lacks the corresponding prediction or actual column (gateway model monitors infer omitted columns at creation when possible).
- Fail to provide data in the `actual_score` or `actual_class` column.
- Pass `extra_args` for segment metrics on a gateway model monitor.

## Examples

### Model version monitor

The following example gets the Root Mean Square Error (RMSE) over a one-day period from the model monitor.

Copy code

```
SELECT * FROM TABLE(MODEL_MONITOR_PERFORMANCE_METRIC(
'MY_MONITOR', 'RMSE', '1 DAY', TO_TIMESTAMP_TZ('2024-01-01'), TO_TIMESTAMP_TZ('2024-01-02'))
)
```

The following example gets the Root Mean Square Error (RMSE) over the last 30 days from the model monitor:

Copy code

```
SELECT * FROM TABLE(MODEL_MONITOR_PERFORMANCE_METRIC(
'MY_MONITOR', 'RMSE', '1 DAY', DATEADD('DAY', -30, CURRENT_DATE()), CURRENT_DATE())
)
```

### Gateway model monitor

The following example gets the Precision for `MY_GATEWAY_MONITOR` over a one-day period:

Copy code

```
SELECT * FROM TABLE(MODEL_MONITOR_PERFORMANCE_METRIC(
'MY_GATEWAY_MONITOR', 'PRECISION', '1 DAY', TO_TIMESTAMP_TZ('2024-01-01'), TO_TIMESTAMP_TZ('2024-01-02'), SERVICE => mydb.myschema.challenger_service)
)
```
