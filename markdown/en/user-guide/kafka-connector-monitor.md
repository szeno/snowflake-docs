Important

- Advance notice: The classic Kafka connector (v3 and earlier) is fully supported today,
  but it is planned for future deprecation.
- Action: No immediate changes are required. Your current workloads are safe
  and continue to be fully supported.
- Timeline: Snowflake plans to issue a formal deprecation announcement in mid-2026.
  After the announcement, an 18-month migration window begins before end-of-life.
- Recommendation: Use the
  [Snowflake Connector for Kafka (v4)](/user-guide/kafka-connector/index)
  for all new implementations.

For migration guidance, see [Migrate from v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4).

# Monitoring the Kafka connector using Java Management Extensions (JMX)

This topic describes how to use Java Management Extensions (JMX) to monitor the Snowflake Connector for
Kafka. Kafka Connect provides pre-configured JMX metrics that provide information about the Kafka connector.
The Snowflake Connector for Kafka provides multiple Managed Beans (MBeans) that you can use to ingest metrics
about the Kafka environment. You can load this information into 3rd-party tools, including Prometheus and
Grafana.

The JMX feature is enabled in the connector by default. To disable JMX, set the `jmx` property to `false`.

Important

[Snowpipe](/user-guide/data-load-snowpipe-intro) supports the Kafka connector version 1.6.0 and later.

[Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) supports the Kafka connector version 2.1.2 and later.

## Configuring JMX in the Kafka connector

JMX is enabled by default in the Snowflake Kafka connector. To enable JMX in Kafka, perform the following:

1. Enable JMX to connect to your Kafka installation:

   - To make JMX connections to a Kafka installation running on a remote server, set the `KAFKA_JMX_OPTS` environment variable in your Kafka Connect startup script:

     Copy code

     ```
     export KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote=true
         -Dcom.sun.management.jmxremote.authenticate=false
         -Dcom.sun.management.jmxremote.ssl=false
         -Djava.rmi.server.hostname=<ip_address>
         -Dcom.sun.management.jmxremote.port=<jmx_port>"
     ```

     Where:

     - `ip_address`: specifies the IP address of your Kafka Connect installation.
     - `jmx_port`: specifies the JMX port where Kafka Connect listens for JMX connections.
   - To make JMX connections to Kafka running on the same server, set the `JMX_PORT` environment variable in your Kafka startup script:

     Copy code

     ```
     export JMX_PORT=<port_number>
     ```

     Where `port_number` is the JMX port of your Kafka installation.
2. Restart the Kafka connector.

## Using the Snowflake Kafka connector managed beans (MBeans)

JMX uses MBeans to represent objects within Kafka that it can monitor (e.g. thread count, cpu load, etc.). The Snowflake Kafka connector provides MBeans for accessing objects managed by the connector. You can use these MBeans to create monitoring dashboards.

The general format of the Kafka Connector MBean object name is:

`snowflake.kafka.connector:connector=connector_name,pipe=pipe_name,category=category_name,name=metric_name`

Where:

- `connector=connector_name` specifies the name of the connector defined in the Kafka configuration file.
- `pipe=pipe_name` specifies the Snowpipe object used to ingest data. The Kafka connector defines Snowpipe objects for each partition.
- `category=category_name` specifies the category of the MBean. Each category contains a set of metrics.
- `name=metric_name` specifies the name of the metric.

The following sections list the names of the categories and metrics provided by the Snowflake Kafka connector.

### Category: `file-counts`

This category of metrics only applies to Snowpipe-based Kafka connector and does not apply to Snowpipe Streaming.

| Metric Name | Data Type | Description |
| --- | --- | --- |
| `file-count-on-stage` | long | The number of files currently on an internal stage. This value is decremented after the process of purging the files has started. This property provides an estimate of how many files are currently on an internal stage. |
| `file-count-on-ingestion` | long | The number of files in Snowpipe determined by calling the `insertFiles` REST API. There is currently a limitation of 5k for files that are being sent via a single REST API request. There is not a one to one relation between the number of files and the number of REST API calls. The number of calls to the `insertFiles` REST API can be larger than this value. The value of this property is `0` if there are no more files to be ingested. |
| `file-count-table-stage-ingestion-fail` | long | The number of files on the table stage that failed ingestion. |
| `file-count-table-stage-broken-record` | long | The number of files present on the table stage that corresponds to a broken offset. |
| `file-count-purged` | long | The number of files purged from the internal stage after the ingestion status was determined. |

Expand

Show lessSee more

### Category: `offsets`

The `offsetPersistedInSnowflake` and `latestConsumerOffset` metrics apply to Snowpipe Streaming-based Kafka connector. The rest of this category only applies to Snowpipe-based Kafka connector.

| Metric Name | Data Type | Description |
| --- | --- | --- |
| `processed-offset` | long | An offset referring to the most recent record sent to the in-memory buffer. |
| `flushed-offset` | long | An offset referring to a record that is being flushed on an internal stage after the buffer threshold was reached. The buffer can reach its threshold by time, number of records, or size. |
| `committed-offset` | long | An offset referring to a record that has had the precommit API called and has called the Snowpipe `insertFiles` REST API called. |
| `purged-offset` | long | An offset referring to a record that is being purged from the internal stage. This number is the value of the highest recent offset that was purged from the internal stage. |
| `offsetPersistedInSnowflake` | long | An offset that refers to a record that has the latest persisted data in Snowflake. The offset is determined by the `insertRows` API call. |
| `latestConsumerOffset` | long | An offset that refers to the most recent record sent to the in-memory buffer. It is only used to resend the offset when the channel offset token is `NULL`. |

Expand

Show lessSee more

### Category: `buffer`

This category of metrics is only available to Snowpipe-based Kafka connector.

| Metric Name | Data Type | Description |
| --- | --- | --- |
| `buffer-size-bytes` | long | Based on buffer thresholds, returns the buffer size (in bytes) before it is flushed to an internal stage. This value may not be same as the file size since files are compressed when being loaded to an internal stage. |
| `buffer-record-count` | long | Based on buffer thresholds, returns the number of Kafka records buffered into memory before the buffer is flushed to an internal stage. |

Expand

Show lessSee more

### Category: `latencies`

This category of metrics is only available to Snowpipe-based Kafka connector.

| Metric Name | Data Type | Description |
| --- | --- | --- |
| `kafka-lag` | long | The difference (in seconds) between the time the record is put into Kafka and the time the record is fetched into Kafka Connect. Note that this value can be null if the value was not set inside a record. |
| `commit-lag` | long | The difference (in seconds) between the time the file is uploaded to an internal stage and the time the `insertFiles` REST API is called. |
| `ingestion-lag` | long | The difference (in seconds) between the time a file is uploaded to an internal stage and the time the file ingestion status is reported through the `insertReport` or `loadHistoryScan` API. |

Expand

Show lessSee more
