# Gateway monitoring & A/B testing

When you want to update a production model or run an experiment, you can route real-time inference traffic through a [Snowflake Gateway](/developer-guide/snowflake-ml/inference/stable-endpoints-api-reference) to compare inference services behind it. Gateway
model monitors allow you to track the behavior of those services using [auto-captured inference logs](/developer-guide/snowflake-ml/inference/auto-capture-inference-logs) across dimensions such as drift and, when you configure a ground truth table, performance.

Additionally, you can compare services in A/B tests by splitting live traffic between a baseline and a challenger,
or run shadow tests in which a gateway mirrors requests to a challenger while the baseline service handles production responses.

Currently, gateway model monitors support binary classification, regression, and multi-class classification.

## A/B testing workflow

Deploy inference services from the [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview) behind a [Snowflake Gateway](/developer-guide/snowflake-ml/inference/stable-endpoints-api-reference) so production clients send requests through the gateway rather than to individual service endpoints.
You must explicitly create a gateway model monitor for each model, gateway, and inference function name combination you want to observe. The monitor automatically refreshes aggregated metrics when auto-captured inference logs or the ground truth table change, and updates monitoring reports based on the combined data.

The typical workflow:

1. Deploy inference services with [Auto Capture](/developer-guide/snowflake-ml/inference/auto-capture-inference-logs).
2. Route traffic through a [traffic split or shadow traffic gateway](/developer-guide/snowflake-ml/inference/stable-endpoints-api-reference).
3. (Optional) [Prepare late ground truth](#label-gateway-monitor-ground-truth) for performance metrics.
4. [Create a gateway model monitor](#label-gateway-monitor-create).
5. [Evaluate the A/B test in Snowsight](#label-gateway-monitor-view-reports) or [query monitoring results](#label-gateway-monitor-query-metrics).

Each gateway model monitor encapsulates the following information:

- The model to monitor across inference services behind the gateway.
- The gateway whose inference services are observed.
- The function invoked on inference requests (for example, `predict`).
- The refresh interval at which the monitor refreshes aggregated metrics.
- The aggregation window (minimum 1 hour) over which metrics are computed.
- An optional ground truth table and ID columns for performance metrics.
- An optional comment that describes the monitor.

## Gateway configuration for A/B tests

For A/B tests, route live traffic between baseline and challenger services using a `traffic_split` gateway.

Alternatively, use a `shadow_traffic` gateway. The primary service receives all requests and handles production responses. The gateway mirrors the percentage of requests specified by each shadow target’s `weight` to that target, but doesn’t return shadow responses to clients.

For specifications, examples, and upgrade workflows, see [Stable Endpoints & API Reference](/developer-guide/snowflake-ml/inference/stable-endpoints-api-reference) and [CREATE GATEWAY](/sql-reference/sql/create-gateway).

## Late ground truth join

In online inference, labels are often available only after the prediction is made, so you can create the monitor with an empty or partially populated ground truth table and load labels over time. Snowflake joins late-arriving labels to auto-captured inference logs on the ID columns you specify.

Use [`extra_columns`](/developer-guide/snowflake-ml/inference/stable-endpoints-api-reference#label-extra-columns) in inference requests so ID values in auto-captured logs match the ground truth table.

## Creating a gateway model monitor

Create a gateway model monitor using the [CREATE MODEL MONITOR](/sql-reference/sql/create-model-monitor) command. You must have the CREATE MODEL MONITOR privilege on the schema where the monitor is created. You must also have OWNERSHIP on the model and USAGE on the gateway. To compute performance metrics, specify a ground truth table and ID columns at creation time. Omit both for drift-only monitoring. You can create a maximum of 250 model monitors per account.

At creation time, Snowflake selects a representative service from the gateway and tries to infer the model task and prediction columns from auto-captured inference logs. When you specify a ground truth table, Snowflake also tries to infer actual columns from that table.

For online inference, gateway model monitors support hourly aggregated metrics for fine-grained monitoring. You can set the refresh interval as low as 1 minute to refresh metrics frequently as new inference data and labels arrive.
Data from up to 2 weeks before the monitor creation time can be monitored.

See [CREATE MODEL MONITOR](/sql-reference/sql/create-model-monitor) for more details on the CREATE MODEL MONITOR command.

Tip

For details on other SQL commands that you can use with model monitors, see [MODEL MONITOR SQL reference](/sql-reference/commands-model-monitor).

## Temporarily stopping and resuming monitoring

You can suspend (temporarily stop) a gateway model monitor using [ALTER MODEL MONITOR … SUSPEND](/sql-reference/sql/alter-model-monitor). To resume monitoring, issue [ALTER MODEL MONITOR … RESUME](/sql-reference/sql/alter-model-monitor).

### Automatic suspension on refresh failure

Model monitors automatically suspend refreshes when they encounter five consecutive refresh failures related to the underlying data. You can view the status and cause of refresh suspension using the [DESCRIBE MODEL MONITOR](/sql-reference/sql/desc-model-monitor) command. The output includes the following columns, among others:

- `aggregation_status`: The value in this column is a JSON object. One or more of the values in this object will be SUSPENDED if the model monitor is suspended.
- `aggregation_last_error`: The value in this column is a JSON object that contains the specific SQL error that caused the suspension.

After resolving the root cause of the refresh failure, resume the monitor by issuing [ALTER MODEL MONITOR … RESUME](/sql-reference/sql/alter-model-monitor).

## Evaluating A/B tests in Snowsight

Use Snowsight to review gateway model monitor metrics while an A/B test runs and decide whether to shift traffic toward the challenger or roll back.

In Snowsight, select **AI & ML** » **Models**, then open the **Gateways** tab. The gateways list shows a **Monitoring** column with the number of monitors on each gateway. Select a gateway to open its details page.

On the gateway details page:

- **Overview** — Review services behind the gateway and each service’s traffic percentage. Use **Edit Gateway** to change the traffic split during the test.
- **Metrics** — View gateway-level operational and system metrics for inference services behind the gateway: request count, error rate, latency (p50, p90, and p99), and resource utilization (CPU, memory, and GPU when available). Select a service, method, and time range to compare services on the same gateway, and cross-check those results against drift and performance metrics on the **Monitoring** tab for the same period.
- **Monitoring** — View gateway model monitors for that gateway. Select a monitor to open its dashboard. Use **Create gateway monitor** to open a dialog and create a monitor from the UI.

On the monitor dashboard:

- **Metrics overview** — A table of services with their latest drift and performance metrics. Use **Set as baseline** to designate the control service; drift metrics for challenger services are computed relative to that baseline. When a confidence interval is available, it appears under the metric value. For supported metrics and `CI_VALUE` details, see [MODEL\_MONITOR\_DRIFT\_METRIC](/sql-reference/functions/model-monitor-drift-metric) and [MODEL\_MONITOR\_PERFORMANCE\_METRIC](/sql-reference/functions/model-monitor-performance-metric).
- **Charts** — Time-series charts for the selected metrics and services.
- **Control bar** — Filter by **Metrics** and **Services**, change the time range, and refresh data. Open **Monitor details** to view monitor metadata (description, status, refresh interval, aggregation window, warehouse, and ground truth table). Suspend, resume, edit (refresh interval, warehouse, and comment), or drop the monitor from the control bar and actions menu.

Gateway model monitors are not shown on a model’s **Monitoring** tab; that view is for [model version monitors](/developer-guide/snowflake-ml/model-registry/model-observability). For general Model Registry UI tasks, see [Using the Snowflake Model Registry in Snowsight](/developer-guide/snowflake-ml/model-registry/snowsight-ui).

## Querying monitoring results

Each gateway model monitor that you create has the following metrics:

- **Drift metrics**: Distribution changes or data shifts for inference services behind the gateway
- **Performance metrics**: Accuracy and related metrics when ground truth is configured
- **Stat metrics**: Counts of records and null values for prediction and actual columns

To query the metrics computed by the monitor, use the [monitor metric functions](/sql-reference/functions-model-monitors). Use [MODEL\_MONITOR\_DRIFT\_METRIC](/sql-reference/functions/model-monitor-drift-metric), [MODEL\_MONITOR\_PERFORMANCE\_METRIC](/sql-reference/functions/model-monitor-performance-metric), and [MODEL\_MONITOR\_STAT\_METRIC](/sql-reference/functions/model-monitor-stat-metric) to read aggregated results. Performance and drift results can include a `CI_VALUE` column with a confidence interval when one can be computed for the selected metric. You can use the results from the metric functions to create custom dashboards in Streamlit or other centralized monitoring tools.

Important

You must have the following privileges to work with gateway model monitor objects:

| Command | Required privileges |
| --- | --- |
| CREATE MODEL MONITOR | - CREATE MODEL MONITOR privilege on the schema where you want to create the monitor - OWNERSHIP on the model - USAGE on the gateway - SELECT on the ground truth table (if `GROUND_TRUTH` is specified) - USAGE on the database, schema, and warehouse |
| SHOW MODEL MONITORS | Any privilege on the model monitor |
| SHOW MODEL MONITORS IN GATEWAY | USAGE on the gateway |
| DESCRIBE MODEL MONITOR | Any privilege on the model monitor |
| ALTER MODEL MONITOR | MODIFY on the model monitor |
| DROP MODEL MONITOR | OWNERSHIP on the model monitor |

Expand

Show lessSee more

For A/B tests, pass named arguments to select inference services:

- `SERVICE` (required): The service whose metrics you want (for example, the challenger).
- `BASE_SERVICE` (required for drift): The baseline or control service to compare against `SERVICE`.

For syntax, arguments, return columns, and gateway examples, see [MODEL\_MONITOR\_DRIFT\_METRIC](/sql-reference/functions/model-monitor-drift-metric), [MODEL\_MONITOR\_PERFORMANCE\_METRIC](/sql-reference/functions/model-monitor-performance-metric), and [MODEL\_MONITOR\_STAT\_METRIC](/sql-reference/functions/model-monitor-stat-metric).

## Known limitations

The following limitations apply to gateway monitoring and A/B testing.

- Only single-output binary classification, regression, and multi-class classification models are supported.
- At least one active inference service that backs the model must be on the gateway.
- Every inference service you want to monitor must have [Auto Capture](/developer-guide/snowflake-ml/inference/auto-capture-inference-logs) enabled.
- A representative service from the gateway will be selected to infer the model task; every service behind the gateway must use the same output feature name for the monitored function.
- Performance metrics require ground truth and ID columns to be set; without them, you must drop the monitor and create it again.
- A column may be specified only once across all parameters (for example, an ID column cannot also be a prediction column).
- Up to 250 monitors can be created per account.
- Invalid data (nulls, NaNs, out-of-range scores, and similar values) can cause refresh failures and automatic suspension.

## Cost considerations

Virtual warehouse compute:

> - Gateway model monitors use a virtual warehouse, incurring costs during creation and each refresh.
> - Loading the Snowsight dashboard also uses a virtual warehouse, incurring additional charges.

Storage:

> - Monitors materialize aggregated data from inference logs in your account.

Cloud services compute:

> - Gateway model monitors use cloud services compute to trigger refreshes when an underlying base object has changed. Cloud services compute cost is only billed if the daily cloud services cost is greater than 10% of the daily warehouse cost for the account.
