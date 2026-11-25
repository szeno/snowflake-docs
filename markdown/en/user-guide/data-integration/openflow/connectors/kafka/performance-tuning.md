# Performance Tuning of the Openflow Connector for Kafka

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

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

If the schema often changes between messages, ConsumeKafka starts a new flowfile for each distinct schema. Those flowfiles are small, and each one is processed on its own, so throughput drops and latency goes up even when the topic itself is busy. Set the **Schema Conflict Resolution** property of ConsumeKafka to **Continue with Merged Schema** so records with different schemas stay in one flowfile and the file size can stay in the 1-10 MB range above. This uses more memory, because ConsumeKafka holds each whole batch until it can merge the schemas. See [Schema conflict resolution and memory usage](#label-openflow-kafka-schema-conflict-resolution) before you enable it.

If you observe small flowfiles with high throughput for any other reason, contact [Snowflake Support](/user-guide/contacting-support) for assistance.

#### Schema conflict resolution and memory usage

When the **Schema Conflict Resolution** property of ConsumeKafka is set to **Continue with Merged Schema**, ConsumeKafka keeps each whole batch of Kafka records in memory so that it can merge their schemas before it writes the flowfile. This significantly increases memory usage.

If you use **Continue with Merged Schema**:

- Use it only when the default setting produces small flowfiles because messages have varying structures.
- Keep the number of ConsumeKafka concurrent tasks low, within the limit in [Concurrent tasks with multiple connectors on one runtime](#label-openflow-kafka-multiple-connectors).
- Monitor JVM heap usage and garbage collection time, especially while the connector catches up on consumer lag.
- If you observe memory pressure, lower the number of ConsumeKafka concurrent tasks first, within the limit in [Concurrent tasks with multiple connectors on one runtime](#label-openflow-kafka-multiple-connectors). Change Kafka consumer properties only if that is not enough. See [Advanced: limit the Kafka fetch size](#label-openflow-kafka-advanced-fetch-size).

##### Advanced: limit the Kafka fetch size

Set concurrent tasks before you change fetch sizes. If memory pressure remains while **Continue with Merged Schema** is enabled, lower **Max Partition Fetch Size** on the Kafka connection controller service that ConsumeKafka uses. This property is the Kafka `max.partition.fetch.bytes` setting. It limits how much data one fetch returns for each partition. The default is 1 MB. 256 KB was tested with merged schemas while the connector was catching up on lag. The limit only takes effect when consumers fall behind, because polls are smaller than the limit while the connector keeps up. A record batch larger than the limit is still returned, so the consumer can make progress.

**Max Fetch Size** on the same service is the Kafka `fetch.max.bytes` setting. The default is 50 MB. It caps one fetch across all partitions, and it applies only when the per-partition limits of the partitions fetched from one broker add up to more than this value. It has little effect when each consumer reads only a few partitions, because the per-partition limit is reached first.

Set **Max Partition Fetch Size** and **Max Fetch Size** on the Kafka connection service. Do not add `max.partition.fetch.bytes` or `fetch.max.bytes` as dynamic properties. A service that already has those dynamic properties moves their values to these properties when the runtime is upgraded.

To change **Max Partition Fetch Size**, stop the ConsumeKafka processor and disable the Kafka connection controller service. Set **Max Partition Fetch Size**, enable the controller service, and then start ConsumeKafka.

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

These values apply when a single connector uses the full capacity of each node.

#### Concurrent tasks with multiple connectors on one runtime

All connectors on a runtime share the CPU and memory of each runtime node, and the **Concurrent tasks** setting applies to each runtime node. Don’t apply the recommended values from the previous table to every connector. Instead, size each connector separately:

- **Size by partitions:** One ConsumeKafka task can usually handle six to seven high-throughput partitions. Use at most one task on each node for every six partitions that the connector reads. For example, a connector that reads 20 partitions on a runtime with 2 nodes needs at most 2 tasks on each node. Two tasks on each of 2 nodes are 4 consumers, so each consumer reads about 5 partitions.
- **Low-throughput topics:** Start with one task.
- **Number of connectors:** The combined throughput of all connectors on the runtime must fit within what its nodes can process. For node capacity, see [Network and infrastructure](#label-openflow-kafka-network-infrastructure).
- **Busy ConsumeKafka tasks on each node:** Count the ConsumeKafka tasks of all connectors that read continuously, because their topics have high throughput or the connector is catching up on consumer lag. A Large node can usually handle about 8 to 10 such tasks in total, and smaller nodes proportionally fewer. ConsumeKafka tasks of low-throughput connectors are idle most of the time, so a runtime with many low-throughput connectors can run more of them in total.
- **Consumer lag:** Check the CPU and memory usage of the runtime first. Above one task for every six partitions, more tasks usually don’t help. If CPU or memory is saturated, add nodes to the runtime or use a larger node type tier.

#### Important considerations

Memory usage
:   Each concurrent task consumes additional memory. Monitor JVM heap usage when increasing concurrent tasks. With **Continue with Merged Schema**, each task can hold a full poll of parsed records in memory. See [Schema conflict resolution and memory usage](#label-openflow-kafka-schema-conflict-resolution).

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

1. Reduce the number of concurrent tasks for the ConsumeKafka processor. When several connectors share the runtime, check the concurrent tasks of every connector. See [Concurrent tasks with multiple connectors on one runtime](#label-openflow-kafka-multiple-connectors).
2. If ConsumeKafka uses **Continue with Merged Schema**, lower **Max Partition Fetch Size** on the Kafka connection service, as described in [Advanced: limit the Kafka fetch size](#label-openflow-kafka-advanced-fetch-size). If your messages don’t vary in structure, switch to **Create New FlowFile**.
3. Reduce Kafka message batch sizes to lower the memory footprint.
4. Move some connectors to another runtime, or upgrade to a bigger node type.

##### Network latency issues

If experiencing high latency:

1. Verify network configuration between Openflow and external systems.
2. Consider deploying Openflow closer to your Kafka cluster.
3. If working with low throughput, consider lowering **Max Uncommitted Time** in the ConsumeKafka processor.
