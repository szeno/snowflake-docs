# Performance Tuning of the Openflow Connector for Kafka

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic provides guidance for optimizing the performance of the [Snowflake Openflow Connector for Kafka](/user-guide/data-integration/openflow/connectors/kafka/about)
to achieve optimal throughput and minimize latency when ingesting data into Snowflake.

## Performance considerations

When configuring the Openflow Connector for Kafka for optimal performance, consider the following key factors that impact ingestion throughput and latency:

### Kafka configuration

#### Partition count

More partitions allow for higher parallelism but require careful coordination with consumer configuration. Excessive partitions can cause several issues: increased memory usage, slower leader elections during failures, and significant metadata management overhead on brokers.

#### Compression

Message compression can reduce network bandwidth but increases CPU overhead.

### Flowfile optimization

#### Flowfile size

For optimal performance, flowfiles should be in the range 1-10 MB rather than containing individual small messages. Larger flowfiles reduce processing overhead and improve throughput by minimizing the number of individual file operations. Default settings should yield flowfiles in an acceptable size range. Small flowfiles are expected when throughput is low.

If you observe small flowfiles with high throughput, contact [Snowflake Support](/user-guide/contacting-support) for assistance.

### Network and infrastructure

#### Network latency

Lower latency between Kafka brokers and Openflow improves overall performance. Snowflake recommends deploying Kafka brokers and Openflow in the same CSP region.

#### Node size recommendations

The following table provides configuration recommendations based on expected workload characteristics:

| Node Size | Recommended For | Message Rate Capacity |
| --- | --- | --- |
| Small (S) | Low to moderate throughput scenarios | Up to 18 MB/s per node |
| Medium (M) | Moderate to high throughput scenarios | Up to 145 MB/s per node |
| Large (L) | High throughput scenarios | Up to 250 MB/s per node |

Expand

Show lessSee more

### Performance optimization best practices

#### Adjusting processor concurrent tasks

To optimize processor performance, you can adjust the number of concurrent tasks for both
[ConsumeKafka](/user-guide/data-integration/openflow/processors/consumekafka) and PublishSnowpipeStreaming processors. Concurrent tasks allow processors to run multiple threads simultaneously, improving throughput for high-volume scenarios.

To adjust concurrent tasks for a processor, perform the following tasks:

1. Right-click on the processor in the Openflow canvas.
2. Select Configure from the context menu.
3. Navigate to the Scheduling tab.
4. In the Concurrent tasks field, enter the preferred number of concurrent tasks.
5. Select Apply to save the configuration.

#### Recommended concurrent task settings

The following table provides recommended concurrent task settings for different node sizes:

| Node Size | ConsumeKafka Tasks | PublishSnowpipeStreaming Tasks |
| --- | --- | --- |
| Small (S) | 1 | 1 |
| Medium (M) | 4 | 2 |
| Large (L) | 8 | 2 |

Expand

Show lessSee more

#### Important considerations

Memory usage
:   Each concurrent task consumes additional memory. Monitor JVM heap usage when increasing concurrent tasks.

Kafka partitions
:   For ConsumeKafka, the number of concurrent tasks multiplied by the number of runtime nodes should not exceed the number of total Kafka partitions from all topics.

Start conservatively
:   Begin with lower values and gradually increase while monitoring performance metrics.

#### Troubleshooting performance issues: Common performance bottlenecks

##### High consumer lag or Snowflake ingestion bottlenecks

If Kafka consumer lag is increasing or Snowflake ingestion is slow, then perform the following tasks:

1. Verify network connectivity and bandwidth between Openflow and Kafka brokers.
2. Observe if the queue in front of the PublishSnowpipeStreaming processor increases.

   1. If yes, consider adding more concurrent tasks for the PublishSnowpipeStreaming processor in the range limitations provided in [Recommended concurrent task settings](#label-openflow-kafka-adjust-concurrent-tasks).
   2. If not, consider adding more concurrent tasks for the ConsumeKafka processor in the range limitations provided in [Recommended concurrent task settings](#label-openflow-kafka-adjust-concurrent-tasks).
3. Consider using a bigger node type.
4. Consider increasing the max number of nodes for the runtime.

##### Memory pressure

If experiencing memory-related issues:

1. Reduce the batch sizes to lower the memory footprint.
2. Reduce the number of concurrent tasks for the ConsumeKafka processor.
3. Consider upgrading to a bigger node type.

##### Network latency issues

If experiencing high latency:

1. Verify network configuration between Openflow and external systems.
2. Consider deploying Openflow closer to your Kafka cluster.
3. If working with low throughput, consider lowering the Client Lag settings in the PublishSnowpipeStreaming processor and Max Uncommitted Time in the ConsumeKafka processor.
