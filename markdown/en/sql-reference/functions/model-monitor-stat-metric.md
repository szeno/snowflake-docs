Categories:
:   [Model monitor functions](/sql-reference/functions-model-monitors)

# MODEL\_MONITOR\_STAT\_METRIC

Gets stat metrics from a model monitor. Each model monitor monitors one machine learning model. See [ML Observability](/developer-guide/snowflake-ml/model-registry/model-observability) for model version monitors and [Gateway Monitoring & A/B Testing](/developer-guide/snowflake-ml/inference/gateway-monitor-and-ab-testing) for gateway model monitors.

## Syntax

### Model version monitor

Copy code

```
MODEL_MONITOR_STAT_METRIC(<model_monitor_name>, <stat_metric_name>, <column_name>
    [, <granularity> [, <start_time> [, <end_time> [, <extra_args> ] ] ] ] )
```

### Gateway model monitor

Copy code

```
MODEL_MONITOR_STAT_METRIC(
  <model_monitor_name>, <stat_metric_name>, <column_name>
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

`stat_metric_name`
:   Name of the metric.

    Valid values:

    > - `'COUNT'`
    > - `'COUNT_NULL'`
    > - `'MIN'`
    > - `'MAX'`
    > - `'AVG'`
    > - `'SUM'`

    `'MIN'`, `'MAX'`, `'AVG'`, and `'SUM'` are supported for numeric columns only. `'COUNT'` and `'COUNT_NULL'` are supported for all column types.

`column_name`
:   Name of the column used to compute the metric.

    Valid values:

    Any string that exists as a feature column, prediction column, or actual column in the model monitor.

### Gateway model monitor

`SERVICE => service_name`
:   Name of the inference service whose stat metrics you are measuring.

    Valid values: A simple or fully qualified inference service identifier.

## Optional arguments

`granularity`
:   Granularity of the time range being queried. The default value is *1 DAY* for model version monitors and `AGGREGATION_WINDOW` for gateway model monitors.

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
:   Additional arguments for segment-specific queries. This parameter is optional: if not provided, the query returns metrics for all data (non-segment query). Segment queries are not supported for gateway model monitors.

    Valid values: A string in JSON format specifying segment column and value pairs: `'{"SEGMENTS": [{"column": "<segment_column_name>", "value": "<segment_value>"}]}'`

    Note

    Currently, segment queries support only 1 segment column:value pair per query. You cannot query multiple segments simultaneously in a single function call.

    For more information about segments, see [ML Observability: Monitoring model behavior over time](/developer-guide/snowflake-ml/model-registry/model-observability).

## Returns

| Column | Description |
| --- | --- |
| `EVENT_TIMESTAMP` | Timestamp at the start of the time range. |
| `METRIC_VALUE` | Value of the metric within the specified time range. |
| `METRIC_NAME` | Name of the metric that has been computed. |
| `COLUMN_NAME` | Name of the column for which the stat metric has been computed. |
| `SEGMENT_COLUMN` | Name of the segment column for which the metric is computed (or NULL for non-segment queries). |
| `SEGMENT_VALUE` | Segment value for which the metric is computed (or NULL for non-segment queries). |

Expand

Show lessSee more

### Additional columns for gateway model monitor

| Column | Description |
| --- | --- |
| `SERVICE` | Name of the inference service for the metric. |

Expand

Show lessSee more

## Usage notes

The model monitor must have the column being used to calculate the metric.

If the values you’ve specified for `column_name` or `model_monitor_name` are case-sensitive or contain special characters or spaces, enclose them in double quotes.
You must enclose the double quotes within single quotes. For example, `'"<example_model_monitor_name>"'`.

If double-quotes are not provided in these two fields, the `column_name` or `model_monitor_name` are assumed to be case-insensitive.

To minimize potential impact from schema changes, update your queries to explicitly select only the necessary columns instead of using a wildcard (\*).

You might run into errors if you use `'MIN'`, `'MAX'`, `'AVG'`, or `'SUM'` on categorical or multiclass columns; these metrics require numeric columns.

## Examples

### Model version monitor

The following example gets count metrics for the specified model monitor and time range:

Copy code

```
SELECT * FROM TABLE(MODEL_MONITOR_STAT_METRIC(
'MY_MONITOR', 'COUNT', 'MODEL_PREDICTION', '1 DAY', TO_TIMESTAMP_TZ('2024-01-01')
, TO_TIMESTAMP_TZ('2024-01-02'))
)
```

The following example gets count metric for `MY_MONITOR` over the last 30 days:

Copy code

```
SELECT * FROM TABLE(MODEL_MONITOR_STAT_METRIC(
'MY_MONITOR', 'COUNT', 'MODEL_PREDICTION', '1 DAY', DATEADD('DAY', -30, CURRENT_DATE()), CURRENT_DATE())
)
```

### Gateway model monitor

The following example gets the count of non-null prediction values for a challenger service over a one-day period:

Copy code

```
SELECT * FROM TABLE(MODEL_MONITOR_STAT_METRIC(
'MY_GATEWAY_MONITOR', 'COUNT', 'MODEL_PREDICTION', '1 DAY', TO_TIMESTAMP_TZ('2024-01-01'), TO_TIMESTAMP_TZ('2024-01-02'), SERVICE => mydb.myschema.challenger_service)
)
```
