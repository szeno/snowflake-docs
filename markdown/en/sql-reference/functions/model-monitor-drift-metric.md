Categories:
:   [Model monitor functions](/sql-reference/functions-model-monitors)

# MODEL\_MONITOR\_DRIFT\_METRIC

Gets drift metrics from a model monitor. Each model monitor monitors one machine learning model. See [ML Observability](/developer-guide/snowflake-ml/model-registry/model-observability) for model version monitors and [Gateway Monitoring & A/B Testing](/developer-guide/snowflake-ml/inference/gateway-monitor-and-ab-testing) for gateway model monitors.

## Syntax

### Model version monitor

Copy code

```
MODEL_MONITOR_DRIFT_METRIC(
  <model_monitor_name>, <drift_metric_name>, <column_name>
  [, <granularity> [, <start_time> [, <end_time> [, <extra_args> ] ] ] ]
)
```

### Gateway model monitor

Copy code

```
MODEL_MONITOR_DRIFT_METRIC(
  <model_monitor_name>, <drift_metric_name>, <column_name>
  [, <granularity> [, <start_time> [, <end_time> ] ] ],
  SERVICE => <service_name>,
  BASE_SERVICE => <base_service_name>
)
```

## Required arguments

### All monitor types

`model_monitor_name`
:   Name of the model monitor used to compute the metric.

    Valid values: A string that’s the name of the model monitor. It can be a simple or fully qualified name.

`drift_metric_name`
:   Name of the metric.

    Valid values:

    - `'JENSEN_SHANNON'`
    - `'DIFFERENCE_OF_MEANS'`
    - `'WASSERSTEIN'`
    - `'POPULATION_STABILITY_INDEX'`

`column_name`
:   Name of the column used to compute drift.

    Valid values: For model version monitors, any string that exists as a feature column, prediction column, or actual column. For gateway model monitors, prediction or actual columns only.

### Gateway model monitor

`SERVICE => service_name`
:   Name of the inference service whose distribution drift you are measuring.

    Valid values: A simple or fully qualified inference service identifier. Must be different from `BASE_SERVICE`.

`BASE_SERVICE => base_service_name`
:   Name of the inference service used as the comparison baseline.

    Valid values: A simple or fully qualified inference service identifier. Must be different from `SERVICE`.

## Optional arguments

`granularity`
:   Granularity of the time range being queried. Default value is *1 DAY* for model version monitors and `AGGREGATION_WINDOW` for gateway model monitors.

    Valid values:

    - `'<num> HOUR'` (valid for gateway model monitors only)
    - `'<num> DAY'`
    - `'<num> WEEK'`
    - `'<num> MONTH'`
    - `'<num> QUARTER'`
    - `'<num> YEAR'`
    - `'ALL'`
    - `NULL`

`start_time`
:   Start of the time range used to compute the metric. The default value is 60 days before the current time for model version monitors, and 1 day before the current time for gateway model monitors. The default value is calculated each time you call the function.

    Valid values: A timestamp expression or `NULL`.

`end_time`
:   End of the time range used to compute the metric. The default value is the current time, and is calculated each time you call the function.

    Valid values: A timestamp expression or `NULL`.

`extra_args`
:   Additional arguments for segment-specific queries. This parameter is optional - if not provided, the query returns metrics for all data (non-segment query). The segment queries are not supported for gateway model monitors.

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
| `METRIC_VALUE` | Value of the metric within the specified time range. | `5` |
| `COL_COUNT_USED` | Number of records used to compute the metric. | `100` |
| `COL_COUNT_UNUSED` | Number of records excluded from the metric computation. | `10` |
| `BASELINE_COL_COUNT_USED` | Number of records used to compute the metric. | `10` |
| `BASELINE_COL_COUNT_UNUSED` | Number of records excluded from the metric computation. | `0` |
| `METRIC_NAME` | Name of the drift metric that has been computed. | `DIFFERENCE_OF_MEANS` |
| `COLUMN_NAME` | Name of the column for which the drift metric has been computed. | `FEATURE_NAME` |
| `SEGMENT_COLUMN` | Name of the segment column for which the metric is computed (or NULL for non-segment queries). | `CUSTOMER_TIER` |
| `SEGMENT_VALUE` | Segment value for which the metric is computed (or NULL for non-segment queries). | `PREMIUM` |

Expand

Show lessSee more

### Additional columns for gateway model monitor

| Column | Description | Example values |
| --- | --- | --- |
| `SERVICE` | Name of the inference service for the metric. | `challenger_service` |
| `BASE_SERVICE` | Name of the baseline inference service for drift comparison. | `baseline_service` |
| `CI_VALUE` | 95% Wald confidence interval with `lower` and `upper` bounds. Supported for `DIFFERENCE_OF_MEANS` on binary classification models only. Returns `NULL` for other drift metrics and unsupported model tasks. | `{"lower": -0.05, "upper": 0.03}` |

Expand

Show lessSee more

## Usage Notes

The model version monitor must have a baseline set for the drift metric to be computed. The gateway model monitor must have a base service to query the drift metric instead.

You might run into errors if you:

- Don’t set a baseline for the model version monitor, or don’t provide a base service for the gateway model monitor.
- Request a numerical drift metric for a non-numeric feature.
- Use a drift metric that doesn’t exist in the model monitor.
- Pass `extra_args` for segment metrics on a gateway model monitor.

If values you’ve specified for `column_name` or `model_monitor_name` are case-sensitive, or contain special characters or spaces, enclose them in double quotes.
You must enclose the double quotes within single quotes, such as `'"<model_monitor_name>"'`.

If double-quotes are not provided in these two fields, the `column_name` or `model_monitor_name` will be assumed to be case-insensitive.

To minimize potential impact from schema changes, update your queries to explicitly select only the necessary columns instead of using a wildcard (\*).

## Examples

### Model version monitor

The following example gets the differences of means drift metric for `MY_MONITOR` over a one-day period:

Copy code

```
SELECT * FROM TABLE(MODEL_MONITOR_DRIFT_METRIC(
'MY_MONITOR', 'DIFFERENCE_OF_MEANS', 'MODEL_PREDICTION', '1 DAY', TO_TIMESTAMP_TZ('2024-01-01'), TO_TIMESTAMP_TZ('2024-01-02'))
)
```

The following example gets the Jensen-Shannon drift metric for `MY_MONITOR` over the last 30 days:

Copy code

```
SELECT * FROM TABLE(MODEL_MONITOR_DRIFT_METRIC(
'MY_MONITOR', 'JENSEN_SHANNON', 'MODEL_PREDICTION', '1 DAY', DATEADD('DAY', -30, CURRENT_DATE()), CURRENT_DATE())
)
```

### Gateway model monitor

The following example gets the Wasserstein drift metric for `MY_GATEWAY_MONITOR` over a one-day period:

Copy code

```
SELECT * FROM TABLE(MODEL_MONITOR_DRIFT_METRIC(
'MY_GATEWAY_MONITOR', 'WASSERSTEIN', 'MODEL_PREDICTION', '1 DAY', TO_TIMESTAMP_TZ('2024-01-01'), TO_TIMESTAMP_TZ('2024-01-02'), SERVICE => mydb.myschema.challenger_service, BASE_SERVICE => mydb.myschema.base_service)
)
```
