# Elastic Channels overview

Stream events directly from applications and devices into Snowflake tables or Snowflake-managed Iceberg tables. Elastic Channels let you stream directly into Snowflake without introducing Kafka or another intermediary solely for ingestion. Elastic Channels manage ingestion scaling and channel lifecycle, while the SDK automatically batches appends and retries transient failures. They are the recommended starting point for most new Snowpipe Streaming applications.

Use Elastic Channels when your application doesn’t need ordered ingestion or exactly-once recovery. Use [Named Channels](/user-guide/snowpipe-streaming/snowpipe-streaming-channels#label-replication-snowpipe-channels) when your application requires these guarantees. Exactly-once recovery requires records retained in the source or durable application-managed storage for replay.

## How Elastic Channels work

A streaming pipe has one implicit `ELASTIC` channel. Many producers can append to the same Elastic Channel concurrently. Snowflake distributes the appends across server-managed resources without requiring the application to create, name, open, close, or recover the channel.

The end-to-end path:

1. SDK users obtain a handle with `getElasticChannel` (Python: `get_elastic_channel`) and append rows as they arrive. The SDK automatically batches appends internally. Direct REST callers send batches to an Elastic REST endpoint using newline-delimited JSON (NDJSON), with one JSON object per line.
2. Snowflake durably buffers the append and returns a **durable acknowledgement**: an SDK append Future or Promise completes successfully, a registered success handler reports the outcome, or a direct REST request returns HTTP 200. Data isn’t yet ready for querying at this point.
3. The pipe processes the rows server-side: validates the schema, applies configured transformations or pre-clustering, and commits to the target table.
4. The target table receives the committed rows, which become queryable after table processing completes.

Once Snowflake acknowledges an append, your producer can release its retained copy. The data is durable in Snowflake; processing and query availability follow. Row-level processing errors are persisted to the [error table](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables) when error logging is enabled.

Keep unacknowledged events available according to your delivery requirements. During an outage, pause intake or retain incoming events in durable storage to keep collecting. The SDK’s in-memory buffer doesn’t survive a process crash. See [Protect unacknowledged data](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-best-practices#protect-unacknowledged-data) for retention and recovery patterns.

## Delivery semantics

Elastic Channels provide **at-least-once delivery**. Ordering is not guaranteed. If a producer retries an append after a timeout, process restart, or another ambiguous failure, an earlier attempt might already have been accepted and the target table can contain duplicate rows. Include a stable event identifier in your data model when duplicates matter, and reconcile or deduplicate downstream.

## Supported targets

Elastic Channels can write to:

- Standard Snowflake tables
- Snowflake-managed Iceberg v2 and v3 tables, including partitioned tables

For details on Iceberg support, see [Snowpipe Streaming high-performance architecture with Apache Iceberg™ tables](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-iceberg).

For supported data types and automatic schema evolution, see [Table support and schema](/user-guide/snowpipe-streaming/snowpipe-streaming-table-support).

## Append tokens

An append token helps you identify which messages Snowflake has durably acknowledged. You supply an identifier when you append rows, and the SDK returns it to your success or error handler so you can match the result to the messages you sent.

Use an event ID for a single row, or an identifier for a group of rows submitted in one append. A success handler reports that the append is durable, so you can release your retained copy of those messages. An error handler identifies the append that failed so your application can handle it.

For example, the Java API accepts `appendRow(Map<String, Object> row, Object appendToken)`. Register handlers before sending the row, then pass `"event-123"` as its token:

Copy code

```
channel.setSuccessHandler(detail ->
    System.out.println("Acknowledged: " + detail.getAppendTokens()));
channel.setErrorHandler(detail ->
    System.err.println("Failed: " + detail.getAppendTokens() + " cause: " + detail.getError()));
channel.appendRow(row, "event-123");
```

When Snowflake durably acknowledges this row, the success handler receives `event-123` in `detail.getAppendTokens()`. If the append fails, the error handler receives the token and the error. A callback can report several append tokens together.

If you use an append API that returns a Future, such as Java’s `appendRowWithWait(row, appendToken)`, you can track completion through the returned Future instead. The SDK tutorial shows [Java, Python, and Node.js examples](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-getting-started).

Keep tokens small: the SDK holds them in memory while tracking the append and doesn’t send them to Snowflake. A token is a label for tracking the result, not a deduplication key or a saved recovery position. Supply `null` or `None` if you don’t need callback reporting for that append.

### Tracking direct REST requests

Direct REST callers don’t use SDK append tokens. Set `requestId` and `retryCount` as URL query parameters:

```
POST /v2/streaming/data/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/rows?requestId={requestUuid}&retryCount=0
```

Generate a new request UUID for each distinct rowset (batch of rows). When retrying that rowset, reuse the UUID and increment `retryCount` to `1`, `2`, and so on. These parameters support request correlation; they aren’t deduplication keys. For details, see the [Elastic REST reference](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-rest-api#elastic-channel-rest-api).

## Success and error callbacks

Register `setSuccessHandler` and `setErrorHandler` to receive asynchronous append outcomes. Callbacks receive the append tokens grouped by a common acknowledgement or failure event.

Keep callbacks quick so they don’t delay other acknowledgements. Handle retries and longer-running work outside the callback. For implementation guidance, see [Keep callbacks short](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-best-practices#keep-callbacks-short).

## Get started

- SDK path: [Tutorial: Get started with Elastic Channels (SDK)](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-getting-started)
- REST path: [Tutorial: Get started with Elastic Channels (REST API)](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-rest-getting-started)
- Costs: [Snowpipe Streaming high-performance architecture: Understand your costs](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-cost)
- Limits: [Elastic Channels limitations and considerations](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-limitations)
