# Choosing a channel type

Snowpipe Streaming uses channels to carry rows from producers through a pipe to a target table. Choose Named Channels when your application requires ordered ingestion or exactly-once delivery. If you don’t need these guarantees, choose Elastic Channels.

## What is a channel?

A channel is a logical ingestion path, not a separate table or a message queue. Producers append rows through a channel; the pipe defines how Snowflake processes those rows before loading them into the target table, including transformations and column mapping.

Both modes use Snowflake’s serverless ingestion service. The choice depends on whether your application needs ordering and exactly-once delivery, not on who manages the server infrastructure.

Both channel types use pipes and can load Snowflake tables or Snowflake-managed Iceberg tables. Choosing a channel type is separate from choosing a default or custom pipe.

## Compare channel types

| Consideration | Elastic Channels | Named Channels |
| --- | --- | --- |
| When to choose | You don’t need ordering or exactly-once delivery from your producer to the table. | You need per-channel ordering or exactly-once delivery from your producer to the table. |
| Channel management | Each streaming pipe has one implicit Elastic Channel, identified as `ELASTIC` in the REST API. Snowflake manages its lifecycle and scaling. | Your application opens and reuses Named Channels with explicit names, typically mapping each source partition to a channel. |
| Concurrent producers | Many producers can append to the same Elastic Channel concurrently. | Submit in source order within each channel. Use separate channels for independent source partitions or streams. |
| Delivery and recovery | At-least-once delivery. Retrying an ambiguously acknowledged append can produce duplicates. No source-offset cursor or server-side deduplication is provided. | Offset tokens track committed progress. On recovery, replay retained records after the last committed offset, using the source or durable application-managed storage. |
| Ordering | No ordering guarantee. | Ordering is preserved within a channel, not across channels. |
| Progress tracking | Use per-append durable acknowledgements to determine which retained events can be released. | Use committed offset tokens to determine when to advance source checkpoints. |
| Representative use cases | IoT device events, application telemetry, and logs where ordering is unnecessary and duplicates can be tolerated or reconciled downstream. | CDC, billing, and inventory updates that require ordering or exactly-once delivery, including ingestion from Kafka partitions. |

Expand

Show lessSee more

Choose based on delivery requirements, not just the use-case name. For example, logs can use Elastic Channels when duplicates are acceptable, or Named Channels when ordering or exactly-once delivery is required.

Exactly-once recovery requires retaining records so they can be replayed from the last committed offset, either from the source or from durable application-managed storage. Keep the records associated with their original offsets and replay them in order.

Neither mode makes unsubmitted or memory-only producer data crash-durable. Retain events or source records until the relevant acknowledgement or committed checkpoint confirms progress. Durable ingestion progress is separate from target-table query visibility.

## Explore each mode

- [Elastic Channels](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-overview): Learn how Elastic Channels scale ingestion for concurrent producers and high-throughput workloads, then follow the SDK or REST tutorial.
- [Named Channels](/user-guide/snowpipe-streaming/snowpipe-streaming-channels): Learn how channel ordering and offset tokens work, then follow the SDK or REST tutorial for source-offset-based ingestion.
