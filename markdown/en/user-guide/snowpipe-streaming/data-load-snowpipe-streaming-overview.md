# Snowpipe Streaming

Snowpipe Streaming is Snowflake’s real-time ingestion service built on our latest high-performance architecture. It enables applications to stream rows directly from devices, applications, and services into Snowflake tables or Snowflake-managed [Apache Iceberg](/user-guide/tables-iceberg) tables. This direct path can remove staging files, intermediate object storage, message buses, and connector services that the workload doesn’t otherwise need.

Snowpipe Streaming supports two ingestion modes. In both modes, a channel is a logical path that carries rows through a pipe to a target table:

- **Elastic Channels** are the recommended starting point for most new applications. Producers write directly without creating or coordinating channels; Snowflake manages them and scales ingestion as traffic changes. An acknowledgement confirms that Snowflake has durably buffered the append, so the producer can release its retained copy; table processing and query visibility follow. Elastic Channels provide at-least-once delivery without an ordering guarantee. Producers retain unacknowledged events according to their delivery requirements.
- **Named Channels** provide ordered, exactly-once ingestion within each channel by using offset tokens. Use Named Channels when reading from a source that requires strict ordering semantics, such as Kafka partitions or Change Data Capture (CDC).

Snowpipe Streaming delivers:

- Up to **20 GB/s** throughput per table
- **As low as 5 seconds** ingest-to-queryable latency
- **Direct ingestion without application-managed channels** through Elastic Channels
- **Ordered, exactly-once ingestion** through Named Channels and offset tokens
- Streaming into Snowflake-managed [Apache Iceberg](/user-guide/tables-iceberg) tables

The results you observe depend on workload shape and configuration, including row size, table width (number of columns), SDK buffering or REST request batching, concurrency, table type, transformations, and clustering.

## Why use Snowpipe Streaming

- **Simpler direct ingestion**: Elastic Channels let producers stream rows directly from devices and services into Snowflake, reducing pipeline hops without requiring you to create channels or coordinate ingestion across producers. Snowflake scales the ingest path as producers and traffic change.
- **Exactly-once and ordered ingestion when required**: Named Channels use offset tokens to track committed progress and preserve row order within each channel. They map naturally to source partitions and make strict exactly-once recovery straightforward.
- **High throughput, low latency**: Designed to support ingest speeds of up to 20 GB/s per table, with ingest-to-queryable latency as low as 5 seconds. Results depend on workload shape and configuration.
- **In-flight transformations**: Cleanse, reshape, and transform data during ingestion by using COPY command syntax within the PIPE object. Reorder columns, cast types, and apply expressions before data is committed to the target table, with no separate ETL step needed.
- **Pre-clustering at ingest time**: Sort data during ingestion for optimized query performance on tables with clustering keys.
- **Apache Iceberg table support**: Stream data into Snowflake-managed Iceberg tables, including both Iceberg v2 and [Iceberg v3](/user-guide/tables-iceberg-v3-specification-support) tables. For more information, see [Snowpipe Streaming high-performance architecture with Apache Iceberg™ tables](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-iceberg).
- **Schema evolution**: Automatically adapt table schemas to changing data structures. Snowflake can add new columns detected in the incoming stream without manual DDL changes.
- **Monitoring and error investigation**: Query [event table telemetry](/user-guide/snowpipe-streaming/snowpipe-streaming-event-table-telemetry) to track ingestion progress, processing time, and errors. Enable [error logging](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables) to inspect or reprocess rejected-row data.
- **Simplified pipelines**: With Elastic Channels, producers write rows directly into Snowflake tables or Iceberg tables without staging files or intermediate message-bus infrastructure that the workload doesn’t otherwise need.
- **Serverless and scalable**: Compute resources scale automatically based on ingestion load. No infrastructure to manage.
- **Transparent pricing**: Throughput-based billing calculated by credits per uncompressed GB of data ingested. For more information, see [Snowpipe Streaming high-performance architecture: Understand your costs](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-cost).

## How to connect

Snowpipe Streaming supports multiple ingestion paths to fit different workloads:

| Integration | Best for |
| --- | --- |
| [Java SDK](https://central.sonatype.com/artifact/com.snowflake/snowpipe-streaming) ([Java API reference](https://docs.snowflake.com/user-guide/snowpipe-streaming-sdk/reference/java/com/snowflake/ingest/streaming/package-summary.html)) | High-throughput custom applications. Requires Java 11 or later. |
| [Python SDK](https://pypi.org/project/snowpipe-streaming/) ([Python API reference](https://docs.snowflake.com/en/user-guide/snowpipe-streaming-sdk-python/reference/latest/index)) | Data engineering and Python-native workflows. Requires Python 3.9 or later. |
| [Node.js SDK](https://www.npmjs.com/package/snowpipe-streaming) ([Node.js API reference](https://docs.snowflake.com/user-guide/snowpipe-streaming-sdk/reference/nodejs/index.html)) | JavaScript and TypeScript applications. Requires Node.js 20 or later. |
| [REST API](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-rest-api) | Lightweight workloads, IoT devices, and edge deployments. |
| [Snowflake Connector for Kafka](/user-guide/kafka-connector/index) | Apache Kafka topic ingestion. |

Expand

Show lessSee more

The Java, Python, and Node.js SDKs use a shared Rust-based client core. Append rows as they arrive: the SDK automatically buffers and batches appends using time and size thresholds, and handles compression and sending data to Snowflake. Direct REST clients instead group rows into newline-delimited JSON (NDJSON), with one JSON object per line, and handle compression themselves.

Note

Where possible, use the Snowpipe Streaming SDK instead of the REST API to benefit from automatic batching and simpler integration. Use direct REST when an SDK isn’t suitable for your environment.

To get started, choose [Elastic Channels](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-overview) or [Named Channels](/user-guide/snowpipe-streaming/snowpipe-streaming-channels), then follow the SDK or REST tutorial in that section.

For a side-by-side comparison and use-case guidance, see [Choosing a channel type](/user-guide/snowpipe-streaming/snowpipe-streaming-choosing-channel-type).

For technical details about the PIPE object, channels, offset tokens, and supported data types, see [Key concepts](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview).

## Recommended for

- High-volume streaming workloads with per-table throughput needs of up to 20 GB/s
- Real-time analytics and dashboards with ingest-to-queryable latency as low as 5 seconds
- IoT, telemetry, and distributed applications using Elastic Channels through an SDK or the REST API
- CDC pipelines using Named Channels with exactly-once delivery guarantees
- Apache Kafka topic ingestion using the [Snowflake Connector for Kafka](/user-guide/kafka-connector/index)
- Streaming into [Apache Iceberg](/user-guide/tables-iceberg) tables for open table format analytics

Note

Looking for SQL-native streaming? See [Dynamic Tables](/user-guide/dynamic-tables/overview) and [Streams](/user-guide/streams-intro) with [Tasks](/user-guide/tasks-intro) for declarative streaming pipelines.

## Snowpipe Streaming versus Snowpipe

Snowpipe Streaming and [Snowpipe](/user-guide/data-load-snowpipe-intro) complement each other. Use Snowpipe Streaming when data arrives as rows from applications, devices, or services and you need low-latency data availability. Use Snowpipe when your pipeline already produces files in cloud storage and batch-oriented, higher-latency loading is acceptable.
