# Openflow telemetry

Feature — Generally Available

Openflow Snowflake Deployments are available to all accounts in AWS, Azure, and GCP [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow BYOC deployments are available to all accounts in AWS [Commercial regions](/user-guide/intro-regions#label-na-general-regions).

Openflow writes logs and metrics to the event table that you configured when you set up Openflow
([BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc#label-openflow-event-table) | [Snowflake deployment](/user-guide/data-integration/openflow/setup-openflow-spcs-deployment#label-openflow-spcs-event-table)).
This topic describes that telemetry and how to query it.

For setting up predefined alerts, see [Set up alerts for Openflow](/user-guide/data-integration/openflow/alerts).

For pre-built metrics visualization, see [Monitor connectors using the Openflow Connectors Dashboard](/user-guide/data-integration/openflow/connectors-dashboard).

For metrics specific to a given connector type, see [Connector-specific metrics](#label-openflow-connector-specific-metrics).

For legacy runtime metrics, see [Runtime metrics: Event table (deprecated)](/user-guide/data-integration/openflow/monitor-legacy-event-table) and
[Runtime metrics: Export (deprecated)](/user-guide/data-integration/openflow/monitor-legacy-export).

## Metrics

### Connector metrics

The following metrics are emitted every 60 seconds only for connectors that are running.

| Metric | Description |
| --- | --- |
| connector.bytes.received | Bytes the connector received from external sources. |
| connector.bytes.sent | Bytes the connector sent to external destinations, such as Snowflake. |
| connector.time.processing | Time, in nanoseconds, that all components of the connector spent processing data. |

Expand

Show lessSee more

Connector metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| connector.id | Unique identifier of the connector in Openflow. |
| connector.name | Name of the connector. |
| connector.type | Type of the connector. |
| connector.version | Version of the connector. |

Expand

Show lessSee more

### Component metrics

The following metrics are emitted every 60 seconds only for processors that are running.

| Metric | Description |
| --- | --- |
| component.bytes.sent | Bytes a processor sent to an external destination, such as Snowflake. Reported only for processors that sent data in a given reporting interval. |

Expand

Show lessSee more

Component metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| component.id | Unique identifier of the processor. |
| component.name | Name of the processor. |
| component.type | Type of the processor, for example *PutSnowpipeStreaming*. |
| process.group.id.path | Slash-delimited path of process group identifiers of the processor. |
| process.group.name.path | Slash-delimited path of process group names of the processor. |
| connector.id | Unique identifier of the connector. Set only for components of connectors. |
| connector.name | Name of the connector. Set only for components of connectors. |
| connector.type | Type of the connector. Set only for components of connectors. |
| connector.version | Version of the connector. Set only for components of connectors. |

Expand

Show lessSee more

### Connection metrics

The following metrics are emitted every 60 seconds only for connections for which FlowFiles entered or left the queue in a given
reporting interval. If there was no activity on a given queue, no value is emitted.

| Metric | Description |
| --- | --- |
| connection.flowfiles.queued | Number of FlowFiles queued in the connection. |
| connection.bytes.queued | Size, in bytes, of the FlowFiles queued in the connection. |
| connection.backpressure.flowfiles.threshold | Number of queued FlowFiles at which the connection applies back pressure. |
| connection.backpressure.bytes.threshold | Size, in bytes, of queued FlowFiles at which the connection applies back pressure. |

Expand

Show lessSee more

Connection metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| component.id | Unique identifier of the connection. |
| component.name | Name of the connection. |
| component.type | The fixed value *Connection*. |
| process.group.id.path | Slash-delimited path of process group identifiers of the connection. |
| process.group.name.path | Slash-delimited path of process group names of the connection. |
| connector.id | Unique identifier of the connector. Set only for components of connectors. |
| connector.name | Name of the connector. Set only for components of connectors. |
| connector.type | Type of the connector. Set only for components of connectors. |
| connector.version | Version of the connector. Set only for components of connectors. |

Expand

Show lessSee more

### Storage metrics

The following metrics are emitted every 60 seconds.

| Metric | Description |
| --- | --- |
| storage.free | Free disk space, in bytes, on the disk that holds the repository. |
| storage.used | Used disk space, in bytes, on the disk that holds the repository. |

Expand

Show lessSee more

Storage metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| id | Identifier of the repository. |
| name | Name of the repository. |
| storage.type | One of: `flowfile`, `content`, `provenance`, or `configuration_resources`. |

Expand

Show lessSee more

### CPU metrics

The following metrics are emitted every 60 seconds.

| Metric | Description |
| --- | --- |
| cores.available | Number of processors available to the runtime node. |
| cores.load | System load average for the last minute, for example *3.2*. *-1* if the load average isn’t available. |

Expand

Show lessSee more

CPU metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| id | The fixed value *cpu*. |
| name | Name of the operating system. |
| architecture | Architecture of the operating system. |
| version | Version of the operating system. |

Expand

Show lessSee more

### JVM metrics

The following metrics are emitted every 60 seconds.

| Metric | Description |
| --- | --- |
| jvm.memory.heap.used | Heap memory used, in bytes. |
| jvm.memory.heap.committed | Heap memory committed, in bytes. |
| jvm.memory.heap.max | Maximum heap memory, in bytes. |
| jvm.memory.heap.init | Initial heap memory, in bytes. |
| jvm.memory.heap.usage | Heap memory used divided by maximum heap memory, from 0 to 1. *-1* if the maximum is undefined. |
| jvm.memory.non-heap.usage | Non-heap memory used divided by maximum non-heap memory, from 0 to 1. *-1* if the maximum is undefined. |
| jvm.memory.total.used | Heap and non-heap memory used, in bytes. |
| jvm.memory.total.committed | Heap and non-heap memory committed, in bytes. |
| jvm.memory.total.max | Maximum heap and non-heap memory, in bytes. |
| jvm.memory.total.init | Initial heap and non-heap memory, in bytes. |
| jvm.threads.count | Number of live threads. |
| jvm.threads.daemon.count | Number of live daemon threads. |
| jvm.threads.deadlocks | Number of deadlocked threads. |
| jvm.gc.<collector>.runs | Number of garbage collections since the JVM started, for each garbage collector. Spaces in the collector name are replaced with hyphens, for example *jvm.gc.G1-Young-Generation.runs*. |
| jvm.gc.<collector>.time | Time, in milliseconds, spent in garbage collection since the JVM started, for each garbage collector. |

Expand

Show lessSee more

JVM metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| jvm.vendor | Vendor of the JVM. |
| jvm.version | Version of the JVM. |

Expand

Show lessSee more

### Container metrics

The following metrics are emitted every 60 seconds.

| Metric | Description |
| --- | --- |
| container.cpu.usage | CPU used by the container, in cores. |
| container.memory.usage | Memory used by the container, in bytes. |
| container.memory.available | Memory available to the container, in bytes. |

Expand

Show lessSee more

For more information about container metrics, see the OpenTelemetry [Kubelet Stats Receiver documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/kubeletstatsreceiver/documentation.md).

### Connector-specific metrics

Some connectors report custom metrics. For these metrics, see the monitoring page of the connector:

- [Openflow Connector for MongoDB](/user-guide/data-integration/openflow/connectors/mongodb/monitor)
- [Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/monitor)
- [Openflow Connector for Oracle](/user-guide/data-integration/openflow/connectors/oracle/monitor)
- [Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/monitor)
- [Openflow Connector for Salesforce Bulk API](/user-guide/data-integration/openflow/connectors/salesforce-bulk-api/monitor)
- [Openflow Connector for SQL Server](/user-guide/data-integration/openflow/connectors/sql-server/monitor)
- [Openflow Connector for SQL Server (CDC)](/user-guide/data-integration/openflow/connectors/sql-server-cdc/monitor)

### Metric resource attributes

All metrics, including connector-specific metrics, have the following resource attributes:

| Attribute | Description |
| --- | --- |
| application | The fixed value *openflow*. |
| cloud.service.provider | For Snowflake deployments: *snowflake*. For BYOC AWS deployments: *aws*. |
| deployment.version | Version of the deployment. |
| k8s.pod.uid | Uniquely identifies the runtime node that is emitting the metrics. |
| openflow.dataplane.id | Unique identifier of the deployment, shown as *ID* in the deployment details in Openflow. |
| openflow.runtime.id | Unique identifier of the runtime. |
| service.version | Version of the runtime. |

Expand

Show lessSee more

Container metrics are the exception. Their resource attributes include standard kubernetes attributes instead.

## Logs

### Log format

Openflow runtimes emit logs as JSON. To break the `VALUE` column into the following structured fields, apply [TRY\_PARSE\_JSON](/sql-reference/functions/try_parse_json) to it:

| Name | Type | Description |
| --- | --- | --- |
| formattedMessage | String | Contents of the log message. |
| level | String | One of: `ERROR`, `WARN`, `INFO`, `DEBUG`, or `TRACE`. |
| loggerName | String | The fully qualified class name for the logger. |
| nanoseconds | Integer | Nanoseconds elapsed within the second in which this log message was created. Use it with `timestamp` for sub-millisecond precision. |
| threadName | String | Name of the thread handling this call. |
| throwable | JSON Object | Stack trace information for logs at `ERROR` level. |
| timestamp | Integer | Time that this log message was created, represented as milliseconds since the UNIX epoch. |
| mdc | JSON Object | Additional context for the log entry. See [Log context fields](#label-openflow-log-mdc). |

Expand

Show lessSee more

### Log context fields

The `mdc` object contains the following fields. `service.version` and `openflow.runtime.id` are present on all
runtime log entries. The other fields are present only for log entries produced by flow components, and only
when they apply to that component.

| Field | Description |
| --- | --- |
| processGroupId | Unique identifier of the process group that contains the component. |
| processGroupName | Name of the process group that contains the component. |
| processGroupIdPath | Slash-delimited path of process group identifiers, starting at the root process group. |
| processGroupNamePath | Slash-delimited path of process group names, starting at the root process group. |
| registeredFlowIdentifier | Identifier of the versioned flow that contains the component. Present for all versioned flows, including Openflow connectors. |
| registeredFlowVersion | Version of the versioned flow that contains the component. |
| registeredFlowIdentifierPath | Slash-delimited path of the versioned flows that contain the component, starting at the root process group. Each versioned flow is shown as *identifier:version*. |
| snowOpenflowConnectorId | Unique identifier of the connector in Snowflake. Set only for [gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations) connectors. |
| connectorId | Unique identifier of the connector in Openflow. |
| connectorName | Name of the connector. |
| connectorDefinitionId | Type of the connector. |
| connectorBundleVersion | Version of the connector. |
| service.version | Version of the Openflow runtime. |
| openflow.runtime.id | Unique identifier of the Openflow runtime. |

Expand

Show lessSee more

### Log levels

Openflow processors (`com.snowflake.openflow.runtime.processors.*`) default to the `WARN` log level. To change the
log level for a processor, update the bulletin level in the processor configuration on the canvas.

### Log resource attributes

Logs have the following resource attributes:

| Attribute | Description |
| --- | --- |
| application | The fixed value *openflow*. |
| cloud.service.provider | One of: `snowflake` or `aws`. |
| deployment.version | Version of the deployment. |
| openflow.dataplane.id | Unique identifier of the deployment. |

Expand

Show lessSee more

## Example queries

The following queries are examples to get you started with Openflow telemetry.

All queries assume that Openflow is configured to send telemetry to the default event table, `SNOWFLAKE.TELEMETRY.EVENTS`. If your account or Openflow deployment is configured with a different event table, substitute that table name where you see `SNOWFLAKE.TELEMETRY.EVENTS`.

For queries about connector-specific metrics, see [Connector-specific metrics](#label-openflow-connector-specific-metrics).

### Find connections close to back pressure

Copy code

```
SELECT
  resource_attributes:"openflow.dataplane.id" AS deployment_id,
  resource_attributes:"openflow.runtime.id" AS runtime_id,
  record_attributes:"connector.name" AS connector_name,
  record_attributes:"component.name" AS connection_name,
  record_attributes:"component.id" AS connection_id,
  MAX(IFF(record:metric:name = 'connection.flowfiles.queued', value::NUMBER, NULL)) AS flowfiles_queued,
  MAX(IFF(record:metric:name = 'connection.backpressure.flowfiles.threshold', value::NUMBER, NULL)) AS flowfiles_threshold,
  MAX(IFF(record:metric:name = 'connection.bytes.queued', value::NUMBER, NULL)) AS bytes_queued,
  MAX(IFF(record:metric:name = 'connection.backpressure.bytes.threshold', value::NUMBER, NULL)) AS bytes_threshold
FROM snowflake.telemetry.events
WHERE true
  AND timestamp > DATEADD(minute, -10, SYSDATE())
  AND record_type = 'METRIC'
  AND record:metric:name IN (
    'connection.flowfiles.queued',
    'connection.backpressure.flowfiles.threshold',
    'connection.bytes.queued',
    'connection.backpressure.bytes.threshold')
GROUP BY 1, 2, 3, 4, 5
HAVING flowfiles_queued >= 0.8 * flowfiles_threshold
  OR bytes_queued >= 0.8 * bytes_threshold
ORDER BY flowfiles_queued DESC;
```

### Find error logs for Openflow runtimes

Copy code

```
SELECT
  timestamp,
  resource_attributes:"openflow.dataplane.id" AS deployment_id,
  TRY_PARSE_JSON(value):mdc:"openflow.runtime.id" AS runtime_id,
  TRY_PARSE_JSON(value):loggerName AS logger,
  TRY_PARSE_JSON(value):formattedMessage AS message,
  TRY_PARSE_JSON(value) AS parsed_log
FROM snowflake.telemetry.events
WHERE true
  AND timestamp > DATEADD(minute, -30, SYSDATE())
  AND record_type = 'LOG'
  AND record:severity_text = 'ERROR'
  AND runtime_id IS NOT NULL
ORDER BY timestamp DESC;
```

### Find the amount of data ingested by each connector

Copy code

```
SELECT
  DATE_TRUNC('hour', timestamp) AS hour,
  resource_attributes:"openflow.runtime.id" AS runtime_id,
  record_attributes:"connector.name" AS connector_name,
  SUM(value::NUMBER) AS bytes_sent
FROM snowflake.telemetry.events
WHERE true
  AND timestamp > DATEADD(day, -1, SYSDATE())
  AND record_type = 'METRIC'
  AND record:metric:name = 'connector.bytes.sent'
GROUP BY 1, 2, 3
ORDER BY 1 DESC, bytes_sent DESC;
```

### Find high JVM heap usage for Openflow runtimes

Copy code

```
SELECT
  resource_attributes:"openflow.dataplane.id" AS deployment_id,
  resource_attributes:"openflow.runtime.id" AS runtime_id,
  resource_attributes:"k8s.pod.uid" AS node_id,
  MAX(value::FLOAT) * 100 AS max_heap_usage_percentage
FROM snowflake.telemetry.events
WHERE true
  AND timestamp > DATEADD(minute, -30, SYSDATE())
  AND record_type = 'METRIC'
  AND record:metric:name = 'jvm.memory.heap.usage'
GROUP BY 1, 2, 3
HAVING max_heap_usage_percentage > 85
ORDER BY max_heap_usage_percentage DESC;
```

### Find high CPU usage for Openflow runtimes

Copy code

```
SELECT
  DATE_TRUNC('minute', timestamp) AS minute,
  resource_attributes:"openflow.dataplane.id" AS deployment_id,
  resource_attributes:"openflow.runtime.id" AS runtime_id,
  resource_attributes:"k8s.pod.uid" AS node_id,
  MAX(IFF(record:metric:name = 'cores.load', value::FLOAT, NULL)) AS max_load,
  MAX(IFF(record:metric:name = 'cores.available', value::NUMBER, NULL)) AS cores_available,
  max_load / cores_available * 100 AS load_percentage
FROM snowflake.telemetry.events
WHERE true
  AND timestamp > DATEADD(minute, -30, SYSDATE())
  AND record_type = 'METRIC'
  AND record:metric:name IN ('cores.load', 'cores.available')
  AND value::FLOAT >= 0
GROUP BY 1, 2, 3, 4
ORDER BY minute DESC, load_percentage DESC;
```
