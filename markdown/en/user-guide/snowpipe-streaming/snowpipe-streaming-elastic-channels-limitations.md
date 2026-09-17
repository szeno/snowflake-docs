# Elastic Channels limitations and considerations

This topic covers the limits and considerations that apply specifically to Elastic Channels. For Named Channel limits, general SDK limits, and service-level limits, see [Limitations and considerations for Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-limitations).

## SDK version requirement

Elastic Channels require SDK version **1.8.0 or later** for Java, Python, and Node.js. Earlier SDK versions do not include the GA Elastic Channels API.

## Delivery and ordering

- **At-least-once delivery**: Elastic Channels do not guarantee exactly-once delivery. Retrying after an ambiguous failure (timeout, network error, or 5xx) can produce duplicate rows in the target table.
- **No ordering guarantee**: Rows appended concurrently by multiple producers, or in successive appends from a single producer, are not guaranteed to appear in the target table in the order they were submitted.
- **No offset tokens**: Elastic Channels do not use offset tokens, continuation tokens, committed-offset queries, or server-side deduplication.

Use [Named Channels](/user-guide/snowpipe-streaming/snowpipe-streaming-channels#label-replication-snowpipe-channels) when your workload requires ordered ingestion or exactly-once delivery.

## Append tokens

- Append tokens are identifiers returned in callbacks to match outcomes to submitted messages.
- They are not sent to Snowflake and do not provide server-side deduplication, replay, or ordering.
- Tokens are retained in SDK memory until the append is acknowledged. Keep tokens small (compact event or append IDs). Large tokens increase producer memory footprint.

## REST payload limit

Each Elastic REST request can contain up to **4 MB** of payload data (the payload size sent over the network, after compression if used). Use ZSTD or Gzip compression to reduce request size and fit more rows per request.

Named Channel REST requests have the same 4 MB limit on the payload sent over the network, after compression if used.

## Request and rate limits

- Snowflake can return HTTP 429 when request or byte-rate limits are exceeded.
- Direct REST clients should retry 429 responses using exponential backoff with random variation in retry delays (jitter). SDK users should let internal retries handle accepted appends and pause intake if local backpressure rejects new appends.
- Do not assume a fixed reserved request rate.

## Channel lifecycle

- The Elastic Channel lifecycle is tied to the client. There is no separate close or drop operation for the Elastic Channel.
- `getElasticChannel()` (or the language-equivalent method) returns the same channel instance on repeated calls.
- Closing the client closes the Elastic Channel. Any subsequent appends raise a synchronous closed-client error.

## Client-side buffer durability

- The SDK automatically batches rows using time and size thresholds and retries transient failures while the client process remains alive.
- Buffered rows and SDK recovery state aren’t persisted across a process crash, node loss, or forced shutdown.
- Pausing intake bounds outstanding work but doesn’t make memory-only events crash-durable.
- For loss-intolerant data that can’t be regenerated or replayed, persist events before accepting responsibility for them and retain them until durable acknowledgement. Application-managed durable storage can provide retention without requiring Kafka; local storage has capacity and host-loss limits.

This limitation applies before acknowledgement. After the durable acknowledgement, Snowflake has durably buffered the append. For deployment choices, see [Protect unacknowledged data](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-best-practices#protect-unacknowledged-data).

## Unsupported Named Channel operations

The following Named Channel operations do not apply to Elastic Channels:

- Opening or closing a channel by name
- Dropping a channel
- Offset tokens and `getLatestCommittedOffsetToken`
- Continuation tokens
- Channel sequencer operations
- `waitForCommit` or equivalent offset-commit wait

## Supported targets

- Standard Snowflake tables
- Snowflake-managed Iceberg v2 and v3 tables, including partitioned tables

For Iceberg details, see [Snowpipe Streaming high-performance architecture with Apache Iceberg™ tables](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-iceberg).

## Schema evolution

Schema evolution is asynchronous and can complete after the append is durably acknowledged. Supported inferred types differ between standard tables and managed Iceberg versions. For the complete constraints, see [Schema evolution](/user-guide/snowpipe-streaming/snowpipe-streaming-table-support#label-streaming-schema-evolution).

## General service limits

For table-level throughput limits, pipe limits, and SDK architectural constraints (supported architectures, glibc version, timezone, authentication), see [Limitations and considerations for Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-limitations).
