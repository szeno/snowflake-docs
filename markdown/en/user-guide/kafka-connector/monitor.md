# Monitor the Snowflake Connector for Kafka

This topic describes how to monitor the Snowflake Connector for Kafka.

## JMX monitoring

The connector exposes metrics through Java Management Extensions (JMX) MBeans. JMX is enabled
by default (`jmx=true`).

To use JMX monitoring, configure your Kafka Connect worker JVM with the following system properties:

Copy code

```
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=<port>
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false
```

You can then use any JMX-compatible monitoring tool (for example, JConsole or Prometheus with a
JMX exporter) to view the connector metrics.

### MBean domain and naming

The connector registers MBeans under the domain `snowflake.kafka.connector` with the following
ObjectName pattern:

Copy code

```
snowflake.kafka.connector:connector=<connectorName>,<scope>=<scopeValue>,category=<category>,name=<metricName>
```

Where `<scope>` is either `task` (task-level metrics) or `channel` (per-partition channel metrics).

### Task-level metrics

These metrics are scoped to a connector task and provide aggregate visibility into throughput
and lifecycle operations.

| Metric | Type | Description |
| --- | --- | --- |
| `put-records` | Meter | Number of records received by the task via `put()`. Use the rate attributes (1-minute, 5-minute, 15-minute) to monitor ingestion throughput. |
| `put-duration` | Timer | Duration of each `put()` call. High values can indicate connector bottlenecks or downstream backpressure. |
| `precommit-duration` | Timer | Duration of pre-commit operations, which include offset verification. |
| `assigned-partitions` | Gauge | Current number of Kafka partitions assigned to this task. Useful for verifying balanced partition distribution across tasks. |
| `channel-open-duration` | Timer | Time to open Snowpipe Streaming channels. Elevated values may indicate connection issues. |
| `channel-open-count` | Counter | Total number of channels opened by this task. |
| `backpressure-rewind-count` | Counter | Number of times the connector had to rewind due to downstream backpressure. Sustained non-zero values indicate the connector is producing faster than Snowflake can ingest. |

Expand

Show lessSee more

### Channel-level metrics

These metrics are scoped to a specific Kafka topic-partition channel and are essential for
monitoring ingestion lag and data durability.

| Metric | Type | Description |
| --- | --- | --- |
| `processed-offset` | Gauge | The most recent offset buffered by the connector. This is the latest record received from Kafka for this partition. |
| `persisted-in-snowflake-offset` | Gauge | The latest offset confirmed as durably committed in Snowflake. Compare this to `processed-offset` to measure ingestion lag. |
| `latest-consumer-offset` | Gauge | The latest offset available from the Kafka consumer for this partition. Compare to `persisted-in-snowflake-offset` to see the full end-to-end lag. |
| `channel-recovery-count` | Gauge | Number of channel recovery events. A high or increasing value indicates instability in the Snowpipe Streaming channel. |

Expand

Show lessSee more

### Key metrics for alerting

For production deployments, consider alerting on the following:

- **Ingestion lag**: `latest-consumer-offset` minus `persisted-in-snowflake-offset`. A growing
  gap indicates the connector is falling behind.
- **Backpressure**: `backpressure-rewind-count` increasing over time.
- **Channel recovery**: `channel-recovery-count` increasing, which may indicate connectivity
  or authentication issues.
- **Put duration**: `put-duration` mean or p99 exceeding your acceptable threshold.

### MDC logging

Enable MDC (Mapped Diagnostic Context) logging to prepend connector context to log messages.
This is useful when running multiple connector instances and you need to correlate log entries:

Copy code

```
enable.mdc.logging=true
```

## Estimating ingestion latency

The `SnowflakeConnectorPushTime` field in `RECORD_METADATA` records the timestamp when the
connector buffered a record for ingestion. You can use this value to estimate end-to-end
ingestion latency by comparing it against the time the record becomes queryable in Snowflake.

For example:

Copy code

```
SELECT
  RECORD_METADATA:topic::STRING AS topic,
  RECORD_METADATA:partition::NUMBER AS partition,
  RECORD_METADATA:offset::NUMBER AS offset,
  TIMESTAMPDIFF('millisecond',
    TO_TIMESTAMP(RECORD_METADATA:SnowflakeConnectorPushTime::BIGINT, 3),
    CONVERT_TIMEZONE('UTC', CURRENT_TIMESTAMP())
  ) AS latency_ms
FROM my_table
ORDER BY latency_ms DESC
LIMIT 10;
```

For more information about monitoring Snowpipe Streaming ingestion, see
[Snowpipe Streaming key concepts](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview).
