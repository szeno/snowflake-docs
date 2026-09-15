# Sep 23, 2025: Snowpipe Streaming with high-performance architecture (*General availability*)

The high-performance architecture for Snowpipe Streaming is now generally available for all accounts on AWS. This new architecture is designed from the ground up for large-scale, real-time data ingestion with high throughput and low latency.

## Key features and benefits

**High performance and low latency:** Ingest data at up to 10 GB per second per table, with ingest-to-query latencies typically under 10 seconds.

**Multi-language client support:** Use the new, high-performance Java and Python SDKs, built on a shared Rust core for efficiency. A REST API is also available for lightweight and serverless ingestion workloads.

**Simplified data pipelines:** Centralize your ingestion logic using the PIPE object. The new architecture moves schema validation to the server side and supports in-flight data transformations using familiar COPY command syntax, reducing client-side complexity.

**Improved cost-efficiency:** Benefit from a new throughput-based pricing model that provides predictable costs.

## Key difference from classic architecture

This new architecture requires the use of the new SDKs or REST API. All ingestion configuration, including transformations and schema validation, is now managed through the server-side PIPE object, which acts as the entry point for all streaming data into a table.

## Recommended use cases

This architecture is recommended for consistent, high-volume streaming workloads, such as powering real-time analytics dashboards, log and event analysis, and integrating data from IoT devices.

For more information, see [Snowpipe Streaming: High-Performance Architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview).
