# Monitor Snowpipe Streaming

Monitor your Snowpipe Streaming pipelines to check that data is arriving, identify processing delays, and investigate ingestion failures. Snowflake provides two complementary ways to see what is happening:

- [Monitor ingestion with event tables](#label-snowpipe-streaming-event-monitoring) to track processing inside Snowflake.
- [Monitor SDK clients with Prometheus and logs](#label-snowpipe-streaming-client-monitoring) to investigate the software development kit (SDK) running in your application.

## Monitor ingestion with event tables

Use event tables to monitor processing across your streaming pipelines from within Snowflake. Once you enable collection, Snowflake records ingestion activity in your configured event table. Query it with SQL to compare pipelines, investigate problems, and build dashboards or alerts without collecting these server-side events in your application. You can monitor:

- **Latency:** Time from when Snowflake receives the data to when it commits the data to the target table. For retried requests, measurement starts from the most recent receipt.
- **Throughput and progress:** How many rows are ingested over time and, for Named Channels, which offset tokens are reported with commits.
- **Errors:** Rejected-row counts, error details, and channel failures.
- **Channel activity:** Channel open and drop operations.

### Prerequisites

Before you query Snowpipe Streaming telemetry, ensure that you have the following:

- A Snowpipe Streaming pipeline that uses the high-performance architecture.
- An [active event table](/developer-guide/logging-tracing/event-table-setting-up), which is the destination configured to receive telemetry. The Snowflake-managed default is `SNOWFLAKE.TELEMETRY.EVENTS`.
- A role with permission to query that table or its view. For the default table, the `SNOWFLAKE.EVENTS_VIEWER` application role provides access to `SNOWFLAKE.TELEMETRY.EVENTS_VIEW`, not the underlying table. Use the view in the examples if you have viewer access. For other access options, see [Event table access control](/developer-guide/logging-tracing/event-table-setting-up).

### Enable event collection

The `LOG_EVENT_LEVEL` parameter controls which events Snowflake records. Set it to `INFO` on the schema that contains your target tables:

Copy code

```
ALTER SCHEMA <database_name>.<schema_name> SET LOG_EVENT_LEVEL = INFO;
```

If the schema doesn’t set a level, it inherits the database setting, which in turn inherits the account setting. The resulting setting determines which events are collected:

- `INFO`: Records all five event types described on this page.
- `ERROR`: Records row and channel errors only.
- `OFF`: Records no Snowpipe Streaming events. Ingestion continues normally.

Changes might not take effect immediately. For more information, see [Set telemetry levels](/developer-guide/logging-tracing/telemetry-levels).

### Query Snowpipe Streaming events

Each event has a name and severity (informational or error) in `RECORD`, object names in `RESOURCE_ATTRIBUTES`, and event-specific fields in `VALUE`. The `SCOPE` column identifies the service that produced the event. To select Snowpipe Streaming events, use both of these filters:

- `SCOPE:"name" = 'snow.snowpipe.streaming'`
- `RECORD_TYPE = 'EVENT'`

The following query returns events from the last 15 minutes for one target table. In every example on this page, replace `<event_table>` with the event table or view name in `database.schema.object` form. Replace the database, schema, and table placeholders with the exact names stored in Snowflake, including capitalization:

Copy code

```
SELECT
  timestamp,
  record:"name"::STRING AS event_name,
  record:"severity_text"::STRING AS severity,
  resource_attributes:"snow.database.name"::STRING AS database_name,
  resource_attributes:"snow.schema.name"::STRING AS schema_name,
  resource_attributes:"snow.table.name"::STRING AS table_name,
  value:"channel_name"::STRING AS channel_name,
  value
FROM <event_table>
WHERE scope:"name"::STRING = 'snow.snowpipe.streaming'
  AND record_type = 'EVENT'
  AND resource_attributes:"snow.database.name"::STRING = '<database_name>'
  AND resource_attributes:"snow.schema.name"::STRING = '<schema_name>'
  AND resource_attributes:"snow.table.name"::STRING = '<table_name>'
  AND timestamp > DATEADD('minute', -15, CURRENT_TIMESTAMP())
ORDER BY timestamp DESC;
```

The fields in `RESOURCE_ATTRIBUTES` identify the affected objects:

- `snow.executable.type`: Service identifier, set to `SNOWPIPE_STREAMING`.
- `snow.database.name`: Database that contains the target table.
- `snow.schema.name`: Schema that contains the target table.
- `snow.table.name`: Target table name.
- `snow.pipe.name`: Streaming pipe name, when available. Because this field can be absent, the examples filter by database, schema, and table instead. The channel name is in `VALUE:"channel_name"`.

### Event types

Choose an event type based on what you want to monitor. Severity identifies informational events (`INFO`) and errors (`ERROR`):

| Event name | Severity | Purpose |
| --- | --- | --- |
| `commit` | `INFO` | Reports row counts and available offset tokens when Snowflake commits processed data to the target table. |
| `latency` | `INFO` | Reports the time Snowflake takes to process data for a channel. |
| `row_error` | `ERROR` | Provides details about rows that failed processing. |
| `channel_lifecycle` | `INFO` | Records successful channel `OPEN` and `DROP` operations. |
| `channel_error` | `ERROR` | Reports a failure when operating on a channel or committing its data. |

Expand

Show lessSee more

#### Track ingestion progress with commit events

The `VALUE` column for a `commit` event contains these fields:

- `channel_name`: Channel associated with the commit.
- `row_count`: Number of rows successfully ingested.
- `rows_parsed`: Number of rows read during parsing, including rows that were rejected.
- `error_count`: Number of rows rejected during validation or parsing.
- `uncompressed_bytes`: Uncompressed bytes associated with the commit request. If a request includes multiple channels, the same byte count can appear in each channel’s event. Summing this field can double-count data, so don’t use it for exact ingestion or billing totals.
- `offset_start` and `offset_end`: Offset tokens reported with the commit, when available. These are strings defined by the application that sends the data, not counters that Snowflake orders numerically or alphabetically.

Row counts describe each event, not running totals. For Named Channels, use [channel status](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-error-handling) to determine where to resume ingestion after an interruption, rather than relying on the order of telemetry events.

The following query aggregates rows and errors by target table and channel. The error rate is the number of rejected rows divided by parsed rows in the selected events; it is `NULL` when no rows were parsed:

Copy code

```
SELECT
  resource_attributes:"snow.table.name"::STRING AS table_name,
  value:"channel_name"::STRING AS channel_name,
  SUM(value:"row_count"::NUMBER) AS rows_ingested,
  SUM(value:"rows_parsed"::NUMBER) AS rows_parsed,
  SUM(value:"error_count"::NUMBER) AS rows_with_errors,
  SUM(value:"error_count"::NUMBER)
    / NULLIF(SUM(value:"rows_parsed"::NUMBER), 0) AS row_error_rate
FROM <event_table>
WHERE scope:"name"::STRING = 'snow.snowpipe.streaming'
  AND record_type = 'EVENT'
  AND record:"name"::STRING = 'commit'
  AND resource_attributes:"snow.database.name"::STRING = '<database_name>'
  AND resource_attributes:"snow.schema.name"::STRING = '<schema_name>'
  AND resource_attributes:"snow.table.name"::STRING = '<table_name>'
  AND timestamp > DATEADD('minute', -15, CURRENT_TIMESTAMP())
GROUP BY 1, 2
ORDER BY rows_with_errors DESC, rows_ingested DESC;
```

For Named Channels, the following query returns `offset_end` from the latest event that contains an offset for each channel. If multiple events share the latest timestamp, the query returns all of them. This identifies the latest recorded events, not the order of records in the source. For background, see [Offset tokens and exactly-once delivery](/user-guide/snowpipe-streaming/snowpipe-streaming-channels#label-replication-snowpipe-offset-tokens):

Copy code

```
SELECT
  timestamp,
  resource_attributes:"snow.table.name"::STRING AS table_name,
  value:"channel_name"::STRING AS channel_name,
  value:"offset_end"::STRING AS offset_end
FROM <event_table>
WHERE scope:"name"::STRING = 'snow.snowpipe.streaming'
  AND record_type = 'EVENT'
  AND record:"name"::STRING = 'commit'
  AND resource_attributes:"snow.database.name"::STRING = '<database_name>'
  AND resource_attributes:"snow.schema.name"::STRING = '<schema_name>'
  AND resource_attributes:"snow.table.name"::STRING = '<table_name>'
  AND value:"offset_end"::STRING IS NOT NULL
  AND timestamp > DATEADD('minute', -15, CURRENT_TIMESTAMP())
QUALIFY RANK() OVER (
  PARTITION BY resource_attributes:"snow.table.name"::STRING,
    value:"channel_name"::STRING
  ORDER BY timestamp DESC
) = 1
ORDER BY channel_name;
```

#### Measure processing time with latency events

A `latency` event includes `channel_name` and, when a measurement is available, `total_latency_ms`: the processing time in milliseconds. Measurement starts when the data reaches Snowflake’s ingestion endpoint and ends when Snowflake commits the data to the target table. For retried requests, the start time is the most recent receipt at that endpoint, not the first attempt.

Snowflake uses the recorded request-start timestamp when request timing is enabled and available. Otherwise, the measurement starts when Snowflake buffers the data for processing.

This measurement doesn’t include time before the request reaches Snowflake. It isn’t the total time from creating a record in the source to querying it in Snowflake.

The following query groups measurements into one-minute intervals by table and channel. It returns the average, approximate 95th percentile (p95), maximum, and number of measurements. The p95 value is the time at or below which approximately 95% of measurements fall:

Copy code

```
SELECT
  DATE_TRUNC('minute', timestamp) AS minute,
  resource_attributes:"snow.table.name"::STRING AS table_name,
  value:"channel_name"::STRING AS channel_name,
  AVG(value:"total_latency_ms"::NUMBER) AS avg_latency_ms,
  APPROX_PERCENTILE(value:"total_latency_ms"::NUMBER, 0.95) AS p95_latency_ms,
  MAX(value:"total_latency_ms"::NUMBER) AS max_latency_ms,
  COUNT(value:"total_latency_ms"::NUMBER) AS measured_samples
FROM <event_table>
WHERE scope:"name"::STRING = 'snow.snowpipe.streaming'
  AND record_type = 'EVENT'
  AND record:"name"::STRING = 'latency'
  AND resource_attributes:"snow.database.name"::STRING = '<database_name>'
  AND resource_attributes:"snow.schema.name"::STRING = '<schema_name>'
  AND resource_attributes:"snow.table.name"::STRING = '<table_name>'
  AND timestamp > DATEADD('minute', -15, CURRENT_TIMESTAMP())
GROUP BY 1, 2, 3
ORDER BY minute DESC, p95_latency_ms DESC;
```

#### Investigate row and channel errors

A `row_error` event can include the following fields:

- `channel_name`: Channel where the error occurred.
- `error_code` and `error_message`: Error identifier and description.
- `error_col_name`: Column associated with the error.
- `error_line_number` and `error_char_pos`: Line number and character position reported for the error.
- `error_offset`: Offset token associated with the error, when available.

A `channel_error` event includes the channel name, error code, error message, and `error_type` classification. Failures during a commit have `error_type` set to `SYSTEM` and can include `uncompressed_bytes`. Other channel-operation failures are classified as `USER` or `SYSTEM`. Use the error code and message to decide what action to take; the classification alone doesn’t establish the cause.

There isn’t necessarily a `row_error` event for every rejected row. Use `error_count` from commit events for totals, and use row-error events to investigate individual failures.

The following query returns recent row and channel errors:

Copy code

```
SELECT
  timestamp,
  record:"name"::STRING AS event_name,
  resource_attributes:"snow.table.name"::STRING AS table_name,
  value:"channel_name"::STRING AS channel_name,
  value:"error_type"::STRING AS error_type,
  value:"error_code"::STRING AS error_code,
  value:"error_message"::STRING AS error_message,
  value:"error_offset"::STRING AS error_offset,
  value:"error_col_name"::STRING AS error_column
FROM <event_table>
WHERE scope:"name"::STRING = 'snow.snowpipe.streaming'
  AND record_type = 'EVENT'
  AND record:"name"::STRING IN ('row_error', 'channel_error')
  AND resource_attributes:"snow.database.name"::STRING = '<database_name>'
  AND resource_attributes:"snow.schema.name"::STRING = '<schema_name>'
  AND resource_attributes:"snow.table.name"::STRING = '<table_name>'
  AND timestamp > DATEADD('minute', -15, CURRENT_TIMESTAMP())
ORDER BY timestamp DESC;
```

An event might lack object names if Snowflake couldn’t identify the affected objects. The example’s object-name filters exclude those events. If an expected error is missing, remove those filters while keeping the time and event-type filters. Your role’s access controls still apply. Events don’t capture every client authentication or connection failure.

#### Inspect channel activity with lifecycle events

A `channel_lifecycle` event records a successful `OPEN` or `DROP` operation. Its `VALUE` fields identify the channel (`channel_name`), its mode (`channel_mode`), and the operation (`event_type`). When supplied by the client, `tracking_label` and `client_version` provide additional information about the client that performed the operation.

The following query returns recent channel operations:

Copy code

```
SELECT
  timestamp,
  resource_attributes:"snow.table.name"::STRING AS table_name,
  value:"channel_name"::STRING AS channel_name,
  value:"channel_mode"::STRING AS channel_mode,
  value:"event_type"::STRING AS event_type,
  value:"tracking_label"::STRING AS tracking_label,
  value:"client_version"::STRING AS client_version
FROM <event_table>
WHERE scope:"name"::STRING = 'snow.snowpipe.streaming'
  AND record_type = 'EVENT'
  AND record:"name"::STRING = 'channel_lifecycle'
  AND resource_attributes:"snow.database.name"::STRING = '<database_name>'
  AND resource_attributes:"snow.schema.name"::STRING = '<schema_name>'
  AND resource_attributes:"snow.table.name"::STRING = '<table_name>'
  AND timestamp > DATEADD('minute', -15, CURRENT_TIMESTAMP())
ORDER BY timestamp DESC;
```

### Snowflake alert templates

Alert templates provide predefined monitoring conditions that you can configure for your workload. Snowpipe Streaming templates include:

- `SNOWPIPE_STREAMING_ROW_ERROR_RATE`: Monitors the ratio of rejected rows to parsed rows. You can require a minimum number of parsed rows before evaluating the rate.
- `SNOWPIPE_STREAMING_AUTH_FAILURE`: Detects selected permission, object-access, and encryption-key errors reported during commit. It doesn’t cover every login or authentication-token failure.
- `SNOWPIPE_STREAMING_CHANNEL_LIMIT`: Detects when a pipe exceeds its channel limit (`ERR_CHANNEL_LIMIT_EXCEEDED_FOR_PIPE`). It doesn’t detect rate limiting when data is sent too quickly.

You can monitor an account, database, schema, or table. Available templates and settings can vary by account. Use [SYSTEM$LIST\_ALERT\_TEMPLATES](/sql-reference/functions/system_list_alert_templates) to find available templates, then [SYSTEM$GET\_ALERT\_TEMPLATE](/sql-reference/functions/system_get_alert_template) to inspect their settings. Create an alert with [CREATE ALERT … FROM TEMPLATE](/sql-reference/sql/create-alert). For more information, see [Snowflake alerts](/user-guide/alerts).

### Troubleshooting

Use the [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY view](/sql-reference/account-usage/snowpipe_streaming_channel_history) for historical channel activity. To retain rejected-row data for inspection or reprocessing, use [error tables](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables), subject to their capture and size limits.

- **No events appear:** Check the active event table, query permissions, and `LOG_EVENT_LEVEL` setting. Verify that the time range and object names in your query match the ingestion you want to inspect.
- **Data isn’t arriving:** Look for recent `commit` events with a positive `row_count` and check for `channel_error` events. For Named Channels, confirm progress with channel status.
- **Rows are rejected:** Compare `error_count` with `rows_parsed` in commit events, then inspect `row_error` events for details.
- **Processing is slow:** Compare latency measurements with row counts and errors for the same table, channel, and time interval.

### Collection behavior and costs

- Changes to object names might not appear in events immediately because Snowflake briefly caches this information.
- Keep object and time filters narrow, especially for event tables with many records. For collection, storage, and query charges, see [Costs of telemetry data collection](/developer-guide/logging-tracing/logging-tracing-billing).

## Monitor SDK clients with Prometheus and logs

The SDK provides performance metrics and logs for the application sending data. These are separate from event table records: enabling `LOG_EVENT_LEVEL` in Snowflake doesn’t enable SDK metrics or change the SDK’s log level.

### Enable and verify Prometheus metrics

Prometheus collects metrics by periodically reading an HTTP endpoint, a process called scraping. The SDK includes a metrics server that exposes this endpoint on the host running your application.

1. Set `SS_ENABLE_METRICS` to `true` in the application’s environment before starting it:

   Copy code

   ```
   export SS_ENABLE_METRICS=true
   ```
2. Start your ingestion application from that environment. By default, the metrics server listens on `127.0.0.1:50000` and serves metrics at `/metrics`.
3. While the application is running, verify the endpoint from another terminal on the same host:

   Copy code

   ```
   curl http://127.0.0.1:50000/metrics
   ```

The response contains metrics in Prometheus text format. The `SS_METRICS_IP` and `SS_METRICS_PORT` environment variables control the listening address and port. For their defaults and other settings, see [Environment variables](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-configurations#environment-variables).

### Configure Prometheus collection

Add the SDK endpoint to your Prometheus configuration. This example assumes Prometheus runs on the same host and can reach the SDK’s default endpoint:

Copy code

```
scrape_configs:
  - job_name: snowpipe_streaming_hp
    metrics_path: /metrics
    static_configs:
      - targets: ['127.0.0.1:50000']
```

If Prometheus runs on a different host or in a separate container, `127.0.0.1` refers to that host or container, not your ingestion application. Configure the SDK’s listening address and the Prometheus target so they can communicate. Restrict access to the metrics endpoint to your monitoring infrastructure; don’t expose it publicly.

### Configure client logs

Set `SS_LOG_LEVEL` before initializing the client to control its log output. Supported values are `info`, `warn`, and `error`; the default is `info`. Logging and metrics settings apply to all SDK clients in the same process. For the configuration reference, see [Environment variables](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-configurations#environment-variables).

### Investigate client issues

Compare client metrics and logs with event table records for the same time period and ingestion target. For channel-specific status and recovery, see [Named Channel operations](/user-guide/snowpipe-streaming/snowpipe-streaming-operations) or [Elastic Channel operations](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-operations).

- **No metrics are available:** Confirm that `SS_ENABLE_METRICS` was set before the application started and that the application is still running.
- **The local endpoint works but Prometheus can’t collect metrics:** Check the configured target, listening address, port, and network access between Prometheus and the application.
- **Client logs don’t explain an ingestion error:** Check event table records for errors during processing inside Snowflake. Client logs and server-side events cover different parts of ingestion.
