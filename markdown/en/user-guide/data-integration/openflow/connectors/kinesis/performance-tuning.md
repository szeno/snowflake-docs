# Performance tuning of the Openflow Connector for Amazon Kinesis Data Streams

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

When configuring the Openflow Connector for Kinesis for optimal performance, consider the following key factors that impact ingestion throughput and latency.

## Flowfile size

For optimal performance, flowfiles should be in the range 1-10 MB rather than containing individual small messages. Larger flowfiles reduce processing overhead and improve throughput by minimizing the number of individual file operations. Default settings should yield flowfiles in an acceptable size range. Small flowfiles are expected when throughput is low.

If you observe small flowfiles with high throughput, contact [Snowflake Support](/user-guide/contacting-support) for assistance.

## Network and infrastructure

### Network latency

Lower latency between Kinesis and Openflow improves overall performance. It’s highly advised that your Kinesis stream and Openflow are located in the same cloud service provider (CSP) region.

### Node size recommendations

The following table provides configuration recommendations based on expected workload characteristics. Throughput values are relative and depend heavily on the source system configuration, topic and stream sizes, data format, and other factors.

| Node Size | Recommended For | Message Rate Capacity |
| --- | --- | --- |
| Small (S) | Low to moderate throughput scenarios | Up to 27 MB/s per node |
| Medium (M) | Moderate to high throughput scenarios | Up to 135 MB/s per node |
| Large (L) | High throughput scenarios | Exceeding 135 MB/s per node. Up to 310 MB/s per node. |

Expand

Show lessSee more

## Performance optimization best practices

### Tuning Max Records Per Request

When the ConsumeKinesis processor uses the **SHARED\_THROUGHPUT** consumer type, the **Max Records Per Request** property controls the maximum number of records that the processor retrieves from Kinesis in a single request. If ingestion throughput is low and you don’t see an obvious bottleneck in Openflow, Snowflake, or the network, this value might be too low for your workload.

For most workloads, start by setting **Max Records Per Request** so that each request retrieves about 1 MB of data. Estimate the value by dividing 1 MB by your average Kinesis record size.

The following table shows example starting values for common average record sizes:

| Average record size | Approximate calculation | Max Records Per Request |
| --- | --- | --- |
| 1 KB | 1 MB / 1 KB | 1000 |
| 200 bytes | 1 MB / 200 bytes | 5000 |
| 5 KB | 1 MB / 5 KB | 200 |

Expand

Show lessSee more

After changing the value, monitor consumer lag, throughput, and runtime resource usage. Increase the value gradually if Kinesis consumption remains the bottleneck.

### Adjusting processor concurrent tasks

To optimize processor performance, you can adjust the number of concurrent tasks for both ConsumeKinesis and PublishSnowpipeStreaming processors. Concurrent tasks allow processors to run multiple threads simultaneously, improving throughput for high-volume scenarios.

To adjust concurrent tasks for a processor, perform the following tasks:

1. Right-click on the processor in the Openflow canvas.
2. Select **Configure** from the context menu.
3. Navigate to the **Scheduling** tab.
4. In the **Concurrent tasks** field, enter the preferred number of concurrent tasks.
5. Select **Apply** to save the configuration.

#### Recommended concurrent task settings

| Node Size | ConsumeKinesis Tasks | PublishSnowpipeStreaming Tasks |
| --- | --- | --- |
| Small (S) | 2 | 1 |
| Medium (M) | 4 | 2 |
| Large (L) | 6 | 3 |

Expand

Show lessSee more

#### Important considerations

- **Memory usage**: Each concurrent task consumes additional memory. Monitor JVM heap usage when increasing concurrent tasks.
- **Start conservatively**: Begin with lower values and gradually increase while monitoring performance metrics.

## Troubleshoot common performance bottlenecks

### High consumer lag or Snowflake ingestion bottlenecks

If Kinesis consumer lag is increasing or Snowflake ingestion is slow, then perform the following tasks:

1. Verify network connectivity and bandwidth between Openflow and Kinesis.
2. Observe if the queue in front of the PublishSnowpipeStreaming processor increases.

   1. If yes, consider adding more concurrent tasks for the PublishSnowpipeStreaming processor in the range limitations provided in [Adjusting processor concurrent tasks](#adjusting-processor-concurrent-tasks).
   2. If not, consider adding more concurrent tasks for the ConsumeKinesis processor in the range limitations provided in [Adjusting processor concurrent tasks](#adjusting-processor-concurrent-tasks).
3. Consider using a bigger node type.
4. Consider increasing the number of nodes for the runtime. This can be done by stopping the connectors in the runtime. Changing node min and max size numbers and starting the connectors again..

### Memory pressure

If experiencing memory-related issues:

1. Reduce the batch sizes to lower the memory footprint. This can be done by changing the File Fragment Size and File Fragment Count parameters in the PublishSnowpipeStreaming processor.
2. Reduce the number of concurrent tasks for the ConsumeKinesis processor.
3. Consider using a bigger node type.

### Network latency issues

If experiencing high latency:

1. Verify network configuration between Openflow and external systems.
2. Consider deploying Openflow in the same region as your Kinesis stream.
3. If working with low throughput, consider lowering the Client Lag settings in the PublishSnowpipeStreaming processor and Max Uncommitted Time in the ConsumeKinesis processor.
