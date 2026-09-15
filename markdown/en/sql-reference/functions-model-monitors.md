# Model monitor functions

Model monitors allow you to track the performance of your machine learning models in production. Snowflake supports two types of monitors. See [ML Observability](/developer-guide/snowflake-ml/model-registry/model-observability) for model version monitors and [Gateway Monitoring & A/B Testing](/developer-guide/snowflake-ml/inference/gateway-monitor-and-ab-testing) for gateway model monitors.

You can use the following functions to retrieve metrics from the model monitors.

> - MODEL\_MONITOR\_DRIFT\_METRIC
> - MODEL\_MONITOR\_PERFORMANCE\_METRIC
> - MODEL\_MONITOR\_STAT\_METRIC

Each function requires the name of a model monitor and the name of a metric to be retrieved from that model.

## List of functions

| Function name | Notes |
| --- | --- |
| [MODEL\_MONITOR\_DRIFT\_METRIC](/sql-reference/functions/model-monitor-drift-metric) |  |
| [MODEL\_MONITOR\_PERFORMANCE\_METRIC](/sql-reference/functions/model-monitor-performance-metric) |  |
| [MODEL\_MONITOR\_STAT\_METRIC](/sql-reference/functions/model-monitor-stat-metric) |  |

Expand

Show lessSee more
