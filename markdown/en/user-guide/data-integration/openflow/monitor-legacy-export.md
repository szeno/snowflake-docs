# Runtime metrics: Export (deprecated)

Deprecated Feature

The OpenTelemetryReportingTask and the legacy runtime metrics that it exports are deprecated and will be removed
in a future release. A removal date isn’t planned yet, and removal won’t happen in the near future. Don’t use
them for new monitoring. Use the metrics described in [Openflow telemetry](/user-guide/data-integration/openflow/monitor) instead.
To access the telemetry outside of Snowflake, use a tool that integrates with event tables, such as the
[Snowflake data source for Grafana](https://grafana.com/grafana/plugins/grafana-snowflake-datasource/). For more
tools, see [Tools for analysis and visualization](/developer-guide/builders/observability#label-observability-tools-analysis-visualization).
For more information, see [Oct 28, 2026: Openflow legacy runtime metrics deprecated](/release-notes/2026/other/2026-10-28-openflow-legacy-runtime-metrics-deprecation).

The OpenTelemetryReportingTask exports legacy runtime metrics in OpenTelemetry format to an OTLP-compatible
endpoint that you operate, such as an OpenTelemetry Collector. The reporting task exports all legacy metrics
for all flows in the runtime, including connectors. It doesn’t affect the telemetry being written to your event table.

## Before you begin

The runtime must be able to connect to the endpoint. For Snowflake deployments, create a network rule and an
external access integration for the endpoint, and add it to the runtime. See
[Create network rules and external access integrations](/user-guide/data-integration/openflow/setup-openflow-spcs-create-rr#label-create-network-rules-and-external-access-integrations).

## Add the reporting task

1. In the Openflow runtime canvas, open the menu in the upper-right corner and select **Controller Settings**.
2. Select the **Reporting Tasks** tab.
3. Select **+** to add a reporting task.
4. Search for and select **OpenTelemetryReportingTask**, and then select **Add**.
5. Edit the reporting task and configure its [properties](#label-openflow-otel-reporting-task-properties).
6. Start the reporting task.

By default, the reporting task runs every 10 seconds. Each run exports the current values of all included metrics.

## Properties

Required properties are in bold.

| Property | Default value | Allowed values | Description |
| --- | --- | --- | --- |
| **Export Endpoint** | `http://localhost:4317` | URL | The endpoint that receives the exported OTLP data. |
| **Export Protocol** | GRPC | - GRPC - HTTP | The OTLP protocol used to send metrics. Endpoints might support one or both. See [Export protocol](#label-openflow-otel-reporting-task-protocol). |
| **Authentication Strategy** | None | - Basic Authentication - Bearer Token - Client Certificate - None | How the reporting task authenticates to the endpoint. See [Authentication](#label-openflow-otel-reporting-task-authentication). |
| SSL Context Service | - | SSLContextService controller service | Provides TLS configuration and client certificate information for connections to the endpoint. |
| Basic Authentication Username | - | String | User name for the endpoint. Required when **Authentication Strategy** is *Basic Authentication*. |
| Basic Authentication Password | - | String | Password for the endpoint. Sensitive. Required when **Authentication Strategy** is *Basic Authentication*. |
| Bearer Token | - | String | Bearer token for the endpoint. Sensitive. Required when **Authentication Strategy** is *Bearer Token*. |
| **Resource Attributes** | - | String | Comma-separated *key=value* pairs to set as resource attributes of the exported metrics. Supports Expression Language with environment variables. For example, *service.name=openflow, deployment.environment=production*. |
| **Export Retry Cache Size** | 5 | Positive integer | If an export fails, or is blocked by an export that’s still running, the reporting task keeps up to this number of exports in memory and retries them on its next run. When the cache is full, the oldest exports are dropped. |
| **Metrics Included** | All | - All - Selected | Export all metrics, or only the metric groups enabled by the properties that follow. |
| **Export Connection Metrics** | true | true, false | Export [connection metrics](#label-openflow-otel-reporting-task-connection-metrics). Used when **Metrics Included** is *Selected*. |
| **Export JVM Metrics** | true | true, false | Export [JVM metrics](#label-openflow-otel-reporting-task-jvm-metrics). Used when **Metrics Included** is *Selected*. |
| **Export CPU Metrics** | true | true, false | Export [CPU metrics](#label-openflow-otel-reporting-task-cpu-metrics). Used when **Metrics Included** is *Selected*. |
| **Export Port Metrics** | true | true, false | Export [input and output port metrics](#label-openflow-otel-reporting-task-port-metrics). Used when **Metrics Included** is *Selected*. |
| **Export Processor Metrics** | true | true, false | Export [processor metrics](#label-openflow-otel-reporting-task-processor-metrics). Used when **Metrics Included** is *Selected*. |
| **Export Process Group Metrics** | true | true, false | Export [process group metrics](#label-openflow-otel-reporting-task-process-group-metrics). Used when **Metrics Included** is *Selected*. |
| **Export Remote Process Group Metrics** | true | true, false | Export [remote process group metrics](#label-openflow-otel-reporting-task-rpg-metrics). Used when **Metrics Included** is *Selected*. |
| **Export Storage Metrics** | true | true, false | Export [storage metrics](#label-openflow-otel-reporting-task-storage-metrics). Used when **Metrics Included** is *Selected*. |

Expand

Show lessSee more

### Export protocol

Choose *GRPC* or *HTTP*, depending on what the endpoint accepts. Many OpenTelemetry Collectors accept both
protocols on different ports. gRPC typically uses port 4317, and HTTP typically uses port 4318.

### Authentication

Basic Authentication
:   Use when the endpoint accepts an Authorization header with a user name and password. Set the
    **Basic Authentication Username** and **Basic Authentication Password** properties.

Bearer Token
:   Use when the endpoint accepts an Authorization header with a bearer token. Set the **Bearer Token** property.

Client Certificate
:   Use when the endpoint accepts certificate authentication. The reporting task authenticates with the key in the
    keystore of the SSL Context Service, so the **SSL Context Service** property is required.

None
:   No authentication. Use only for endpoints in a private network, such as an OpenTelemetry Collector that runs
    next to the runtime.

## Exported metrics

The reporting task exports the following groups of metrics. Each group lists its metrics, followed by their attributes.

### Connection metrics

| Metric | Description |
| --- | --- |
| connection.input.bytes | Total size, in bytes, of FlowFiles that entered the connection in the last five minutes. |
| connection.input.count | Total number of FlowFiles that entered the connection in the last five minutes. |
| connection.output.bytes | Total size, in bytes, of FlowFiles that left the connection in the last five minutes. |
| connection.output.count | Total number of FlowFiles that left the connection in the last five minutes. |
| connection.queued.bytes | Size, in bytes, of the FlowFiles queued in the connection. |
| connection.queued.count | Number of FlowFiles queued in the connection. |
| connection.queued.duration.total | Sum of the times, in milliseconds, that the queued FlowFiles have been in the connection. |
| connection.queued.duration.max | Longest time, in milliseconds, that a queued FlowFile has been in the connection. |
| connection.backpressure.threshold.bytes | Size, in bytes, of queued FlowFiles at which the connection applies back pressure. |
| connection.backpressure.threshold.object | Number of queued FlowFiles at which the connection applies back pressure. |
| connection.loadbalance.status.load\_balance\_not\_configured | *1* if load balancing isn’t configured for the connection. Otherwise, *0*. |
| connection.loadbalance.status.load\_balance\_active | *1* if the connection is load balancing across the runtime nodes. Otherwise, *0*. |
| connection.loadbalance.status.load\_balance\_inactive | *1* if load balancing is configured but the connection isn’t load balancing. Otherwise, *0*. |

Expand

Show lessSee more

Connection metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| id | Unique identifier of the connection. |
| name | Name of the connection. |
| type | The fixed value *connection*. |
| source.id | Unique identifier of the component that sends FlowFiles to the connection. |
| source.name | Name of the component that sends FlowFiles to the connection. |
| destination.id | Unique identifier of the component that receives FlowFiles from the connection. |
| destination.name | Name of the component that receives FlowFiles from the connection. |
| group.id | Unique identifier of the process group that contains the connection. |
| connectorId | Unique identifier of the connector. Gen 2 connectors only. |
| connectorName | Name of the connector. Gen 2 connectors only. |
| connectorDefinitionId | Type of the connector. Gen 2 connectors only. |
| connectorBundleVersion | Version of the connector. Gen 2 connectors only. |
| snowOpenflowConnectorId | Identifier of the connector as a Snowflake object. Gen 2 connectors only. |

Expand

Show lessSee more

### Input and output port metrics

| Metric | Description |
| --- | --- |
| port.thread.count.active | Number of active threads. |
| port.bytes.received | Total bytes received in the last five minutes. |
| port.bytes.sent | Total bytes sent in the last five minutes. |
| port.flowfiles.received | Total number of FlowFiles received in the last five minutes. |
| port.flowfiles.sent | Total number of FlowFiles sent in the last five minutes. |
| port.input.bytes | Total size, in bytes, of FlowFiles input in the last five minutes. |
| port.input.count | Total number of FlowFiles input in the last five minutes. |
| port.output.bytes | Total size, in bytes, of FlowFiles output in the last five minutes. |
| port.output.count | Total number of FlowFiles output in the last five minutes. |

Expand

Show lessSee more

Input and output port metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| id | Unique identifier of the port. |
| name | Name of the port. |
| type | *port-input* for input ports. *port-output* for output ports. |
| group.id | Unique identifier of the process group that contains the port. |
| connectorId | Unique identifier of the connector. Gen 2 connectors only. |
| connectorName | Name of the connector. Gen 2 connectors only. |
| connectorDefinitionId | Type of the connector. Gen 2 connectors only. |
| connectorBundleVersion | Version of the connector. Gen 2 connectors only. |
| snowOpenflowConnectorId | Identifier of the connector as a Snowflake object. Gen 2 connectors only. |

Expand

Show lessSee more

### Process group metrics

| Metric | Description |
| --- | --- |
| processgroup.thread.count.active | Number of active threads. |
| processgroup.thread.count.stateless | Number of stateless threads. |
| processgroup.thread.count.terminated | Number of terminated threads. |
| processgroup.bytes.read | Total bytes read in the last five minutes. |
| processgroup.bytes.received | Total bytes received from external sources in the last five minutes. |
| processgroup.bytes.transferred | Total bytes transferred in the last five minutes. |
| processgroup.bytes.sent | Total bytes sent to external destinations in the last five minutes. |
| processgroup.bytes.written | Total bytes written in the last five minutes. |
| processgroup.flowfiles.received | Total number of FlowFiles received in the last five minutes. |
| processgroup.flowfiles.sent | Total number of FlowFiles sent in the last five minutes. |
| processgroup.flowfiles.transferred | Total number of FlowFiles transferred in the last five minutes. |
| processgroup.input.count | Total number of FlowFiles input in the last five minutes. |
| processgroup.input.content.size | Total size, in bytes, of FlowFiles input in the last five minutes. |
| processgroup.output.count | Total number of FlowFiles output in the last five minutes. |
| processgroup.output.content.size | Total size, in bytes, of FlowFiles output in the last five minutes. |
| processgroup.queued.count | Number of FlowFiles queued. |
| processgroup.queued.content.size | Size, in bytes, of FlowFiles queued. |
| processgroup.time.processing | Total time, in nanoseconds, spent processing in the last five minutes. |

Expand

Show lessSee more

Process group metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| id | Unique identifier of the process group. |
| name | Name of the process group. |
| type | The fixed value *process-group*. |
| tree.level | Depth of the process group, as a string. *1* for process groups on the root canvas of the runtime. |
| processGroupIdPath | Slash-delimited path of process group identifiers, starting at the root process group. |
| processGroupNamePath | Slash-delimited path of process group names, starting at the root process group. |
| flow.identifier | Identifier of the versioned flow. Versioned process groups only. |
| flow.version | Version of the versioned flow. Versioned process groups only. |
| registry.name | Name of the registry of the versioned flow. Versioned process groups only. |
| connectorId | Unique identifier of the connector. Gen 2 connectors only. |
| connectorName | Name of the connector. Gen 2 connectors only. |
| connectorDefinitionId | Type of the connector. Gen 2 connectors only. |
| connectorBundleVersion | Version of the connector. Gen 2 connectors only. |
| snowOpenflowConnectorId | Identifier of the connector as a Snowflake object. Gen 2 connectors only. |

Expand

Show lessSee more

### Processor metrics

| Metric | Description |
| --- | --- |
| processor.thread.count.active | Number of active threads. |
| processor.thread.count.terminated | Number of terminated threads. |
| processor.time.lineage.average | Average time, in nanoseconds, since the FlowFiles that the processor handled in the last five minutes entered the flow. |
| processor.invocations | Total number of times the processor ran in the last five minutes. |
| processor.bytes.read | Total bytes read in the last five minutes. |
| processor.bytes.received | Total bytes received from external sources in the last five minutes. |
| processor.bytes.sent | Total bytes sent to external destinations in the last five minutes. |
| processor.bytes.written | Total bytes written in the last five minutes. |
| processor.flowfiles.received | Total number of FlowFiles received in the last five minutes. |
| processor.flowfiles.removed | Total number of FlowFiles removed in the last five minutes. |
| processor.flowfiles.sent | Total number of FlowFiles sent in the last five minutes. |
| processor.input.count | Total number of FlowFiles input in the last five minutes. |
| processor.input.content.size | Total size, in bytes, of FlowFiles input in the last five minutes. |
| processor.output.count | Total number of FlowFiles output in the last five minutes. |
| processor.output.content.size | Total size, in bytes, of FlowFiles output in the last five minutes. |
| processor.time.processing | Total time, in nanoseconds, spent processing in the last five minutes. |
| processor.run.status.running | *1* if the processor is running. Otherwise, *0*. |
| processor.run.status.stopped | *1* if the processor is stopped. Otherwise, *0*. |
| processor.run.status.validating | *1* if the processor is validating. Otherwise, *0*. |
| processor.run.status.invalid | *1* if the processor is invalid. Otherwise, *0*. |
| processor.run.status.disabled | *1* if the processor is disabled. Otherwise, *0*. |
| processor.counter | Current value of a processor counter. Each counter is reported separately, identified by the *counter* attribute. |

Expand

Show lessSee more

Processor metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| id | Unique identifier of the processor. |
| name | Name of the processor. |
| component | Type of the processor, for example *PutSnowpipeStreaming*. |
| type | The fixed value *processor*. For `processor.counter`, the fixed value *counter*. |
| counter | Name of the counter. `processor.counter` only. |
| execution.node | Either *ALL* or *PRIMARY*, depending on how the processor is configured to run. |
| group.id | Unique identifier of the process group that contains the processor. |
| processGroupIdPath | Slash-delimited path of process group identifiers, starting at the root process group. |
| processGroupNamePath | Slash-delimited path of process group names, starting at the root process group. |
| connectorId | Unique identifier of the connector. Gen 2 connectors only. |
| connectorName | Name of the connector. Gen 2 connectors only. |
| connectorDefinitionId | Type of the connector. Gen 2 connectors only. |
| connectorBundleVersion | Version of the connector. Gen 2 connectors only. |
| snowOpenflowConnectorId | Identifier of the connector as a Snowflake object. Gen 2 connectors only. |

Expand

Show lessSee more

### Remote process group metrics

| Metric | Description |
| --- | --- |
| remoteprocessgroup.thread.count.active | Number of active threads. |
| remoteprocessgroup.remote.port.count.active | Number of active remote ports. |
| remoteprocessgroup.remote.port.count.inactive | Number of inactive remote ports. |
| remoteprocessgroup.duration.lineage.average | Average time, in nanoseconds, since the FlowFiles that the remote process group handled in the last five minutes entered the flow. |
| remoteprocessgroup.refresh.age | Time, in milliseconds, since the last refresh. |
| remoteprocessgroup.received.count | Total number of FlowFiles received in the last five minutes. |
| remoteprocessgroup.received.content.size | Total size, in bytes, of FlowFiles received in the last five minutes. |
| remoteprocessgroup.sent.count | Total number of FlowFiles sent in the last five minutes. |
| remoteprocessgroup.sent.content.size | Total size, in bytes, of FlowFiles sent in the last five minutes. |
| remoteprocessgroup.transmission.status.transmitting | *1* if the remote process group is transmitting. Otherwise, *0*. |
| remoteprocessgroup.transmission.status.nottransmitting | *1* if the remote process group isn’t transmitting. Otherwise, *0*. |

Expand

Show lessSee more

Remote process group metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| id | Unique identifier of the remote process group. |
| name | Name of the remote process group. |
| type | The fixed value *remote-process-group*. |
| group.id | Unique identifier of the process group that contains the remote process group. |
| authorization.issue | Authorization problem with the remote instance, if any. |
| target.uri | URI of the remote instance. |
| connectorId | Unique identifier of the connector. Gen 2 connectors only. |
| connectorName | Name of the connector. Gen 2 connectors only. |
| connectorDefinitionId | Type of the connector. Gen 2 connectors only. |
| connectorBundleVersion | Version of the connector. Gen 2 connectors only. |
| snowOpenflowConnectorId | Identifier of the connector as a Snowflake object. Gen 2 connectors only. |

Expand

Show lessSee more

### JVM metrics

| Metric | Description |
| --- | --- |
| jvm.memory.heap.used | Heap memory used, in bytes. |
| jvm.memory.heap.committed | Heap memory committed, in bytes. |
| jvm.memory.heap.max | Maximum heap memory, in bytes. |
| jvm.memory.heap.init | Initial heap memory, in bytes. |
| jvm.memory.heap.usage | Heap memory used divided by maximum heap memory, from 0 to 1. |
| jvm.memory.non-heap.usage | Non-heap memory used divided by maximum non-heap memory, from 0 to 1. |
| jvm.memory.total.init | Initial heap and non-heap memory, in bytes. |
| jvm.memory.total.used | Heap and non-heap memory used, in bytes. |
| jvm.memory.total.max | Maximum heap and non-heap memory, in bytes. |
| jvm.memory.total.committed | Heap and non-heap memory committed, in bytes. |
| jvm.threads.count | Number of live threads. |
| jvm.threads.deadlocks | Number of deadlocked threads. |
| jvm.threads.daemon.count | Number of live daemon threads. |
| jvm.uptime | Time, in seconds, since the JVM started. |
| jvm.file.descriptor.usage | Open file descriptors divided by the maximum number of file descriptors, from 0 to 1. |
| jvm.gc.<collector>.runs | Number of garbage collections since the JVM started, for each garbage collector, for example *jvm.gc.G1-Young-Generation.runs*. |
| jvm.gc.<collector>.time | Time, in milliseconds, spent in garbage collection since the JVM started, for each garbage collector. |

Expand

Show lessSee more

### CPU metrics

| Metric | Description |
| --- | --- |
| cores.available | Number of processors available to the runtime node. |
| cores.load | System load average for the last minute. *-1* if the load average isn’t available. |

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

### Storage metrics

| Metric | Description |
| --- | --- |
| storage.free | Free space, in bytes, on the storage that holds the repository. |
| storage.used | Used space, in bytes, on the storage that holds the repository. |

Expand

Show lessSee more

Storage metrics have the following attributes:

| Attribute | Description |
| --- | --- |
| id | Identifier of the repository. |
| name | Name of the repository. |
| storage.type | Type of the repository. One of: `flowfile`, `content`, `provenance`, or `configuration_resources`. |

Expand

Show lessSee more
