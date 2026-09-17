# Best practices for Elastic Channels

## Let the SDK batch automatically

Append rows as they arrive. The Java, Python, and Node.js SDKs buffer and combine appends internally using time and size thresholds. The SDK also handles compression and sending data to Snowflake. Don’t wait to accumulate rows before submitting them to the SDK.

Use `appendRowWithWait` to submit individual rows and retain the returned Futures or Promises, or use `appendRow` with registered success and error handlers. Both use the same internal batching path. If your source already supplies multiple rows together, the corresponding `appendRows` APIs remain supported; application-side batch building isn’t required for throughput.

## Bound outstanding acknowledgements

Submit rows without waiting for each append to be acknowledged before submitting the next. Bound the number of outstanding acknowledgements and the bytes retained for unacknowledged events. Periodically wait for all pending appends to be durably acknowledged, based on your outstanding-work limits or elapsed time. Also wait when intake pauses or ends. This waits for events already submitted; it does not collect rows for sending.

Advance the application checkpoint only after all relevant events are durably acknowledged. Elastic Channels don’t guarantee acknowledgement order, so a later append’s completion alone doesn’t establish that earlier appends succeeded. For checkpoint and flush behavior, see [Elastic Channels operations](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-operations#label-elastic-durability-checkpoints).

If the SDK rejects new appends because its buffer is full, pause intake and retain the rejected event. Let pending appends complete, then wait before retrying the rejected append.

## Allow time for durable acknowledgements

The SDK retries transient network and service failures automatically, so acknowledgements can take longer during retries or service delays. Avoid aggressive per-append timeouts, such as 10 seconds, that treat a slow acknowledgement as a failed append. If your application needs a bounded wait, retain the original Future or Promise and continue tracking its outcome. Bound outstanding appends and retained bytes, and pause intake when those limits are reached rather than resubmitting pending data. For language-specific guidance, see [Caller wait timeouts](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-error-handling#label-elastic-caller-timeouts).

## Use stable event identifiers

Elastic delivery is at-least-once. If a producer retries after an ambiguous failure (timeout, no response, or 5xx), Snowflake may already have accepted the original request and the target table can contain duplicate rows.

Include a stable event identifier in each row (for example, a UUID generated at the source, or a composite of source system, partition, and offset). Use this identifier for downstream deduplication when duplicates matter.

Copy code

```
-- Example downstream deduplication on a stable event_id
SELECT DISTINCT event_id, * FROM MY_TABLE;
```

Append tokens are identifiers returned in callbacks to match outcomes to submitted messages. They are not sent to Snowflake and do not prevent duplicates.

## Protect unacknowledged data

Once Snowflake acknowledges an append, your producer can release its retained copy. Until then, keep the events available. During an outage, pause intake and retain pending events. If your application needs to keep collecting, retain incoming events in durable storage before submitting them to the SDK.

The primary path remains direct: producer to Snowpipe Streaming SDK to Snowflake. The SDK buffers appends in process memory and retries transient failures, but doesn’t provide durable local storage for recovery. Choose retention according to your delivery requirements:

| Producer requirements | Recommended pattern | Kafka required? |
| --- | --- | --- |
| Can pause intake or regenerate events | Direct SDK ingestion. Pause intake during outages and retain events until they are durably acknowledged. Use source replay if recovery must survive a producer restart. | No |
| Must continue accepting events during outages | Direct SDK ingestion with application-managed durable storage for pending events. | No |
| Already needs a shared messaging system | Keep Kafka for delivery to multiple consumers, replay, or retention, and connect it to Snowflake. | Appropriate for those requirements, not mandatory for ingestion |

Expand

Show lessSee more

Pausing intake bounds additional work; it doesn’t make memory-only events survive a crash. If the source can replay, don’t discard records or advance its checkpoint past unacknowledged events.

If you already use Kafka for multiple consumers, shared replay, or retention, keep it and stream a copy into Snowflake. You don’t need to introduce Kafka solely to stream events into a table.

## Continue collecting during outages

For loss-intolerant collection from a source that can’t replay, persist events in durable storage before accepting responsibility for them. Don’t wait until the SDK buffer is full to begin persisting: a crash before that point could lose accepted events. This producer-side retention can preserve the direct network path to Snowflake without a separate broker or connector fleet.

Remove persisted records only after durable acknowledgement. After a restart, replay unresolved records using stable event IDs because an acknowledgement might have been lost before the producer recorded it.

Bound local storage and define what happens when it fills. Local disk doesn’t protect against host loss, and an ephemeral container filesystem might not survive a restart. If retention must survive host loss, use storage with the required replication and durability guarantees. A producer that can neither pause, replay, nor persist events can’t guarantee lossless collection during an outage.

## Keep callbacks short

Register `setSuccessHandler` and `setErrorHandler` before the first append tracked through callbacks. Callbacks run on the channel’s internal acknowledgement task.

Callbacks must:

- Return quickly
- Do only cheap bookkeeping (for example, recording the acknowledged token in a local counter)
- Hand blocking I/O, network calls, retries, and reconciliation to an application-managed queue or executor

A slow callback delays acknowledgements for all appends on the channel. A thrown callback exception is caught and logged, so one bad handler cannot stop the acknowledgement path.

## Batch rows for throughput with REST

Direct REST clients must group and send rows themselves. Combine rows into requests using newline-delimited JSON (NDJSON), with one JSON object per line, and use ZSTD or Gzip compression to reduce request overhead. Bound request size and flush partial batches based on elapsed time so low-volume sources don’t wait indefinitely for a full batch.

Elastic REST requests have a 4 MB payload limit (the payload size sent over the network, after compression if used). Use ZSTD or Gzip compression to reduce the payload size. These are REST request limits, not targets for application-side SDK batches.

Set the `Content-Encoding` header only when the payload is already compressed in the matching format:

- `Content-Encoding: zstd` for ZSTD
- `Content-Encoding: gzip` for Gzip

## Retry safely

Direct REST clients should retry transient errors (HTTP 429, 500, 503) using exponential backoff with random variation in retry delays (jitter). A network timeout or missing response is ambiguous: the original request might already have been accepted.

For REST requests, use the **same `requestId`** on every retry of the same rowset (batch of rows). Set `retryCount=0` on the first attempt and increment it on each retry. This enables server-side request correlation for support diagnostics. A `retryCount` greater than `0` signals that duplicates are possible; it does not prove that a duplicate occurred.

For SDK appends, let the SDK retry transient failures while the original append remains pending. A timeout imposed by the caller is not a terminal append failure. If the SDK reports a terminal failure, classify it before retrying; fix validation or authorization issues, and recreate an invalidated client. Recover only unresolved events, using stable event IDs for ambiguous outcomes. See [Error handling for Elastic Channels](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-error-handling).

## Graceful shutdown

Before stopping a producer:

1. Stop accepting new source work.
2. Call `initiateFlush()` to push any buffered data.
3. Wait for the flush to complete (`waitForFlush` with a timeout).
4. Close the client.

For REST producers, confirm that all in-flight requests have received a successful HTTP response before stopping the process.

For code examples, see [Elastic Channels operations](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-operations).

## Use MATCH\_BY\_COLUMN\_NAME for efficient ingestion

Configure the streaming pipe with `MATCH_BY_COLUMN_NAME = CASE_SENSITIVE` to map only required columns from the source instead of ingesting all data into a single VARIANT column. This reduces ingestion cost and improves processing efficiency.

## Use native data types for semi-structured data

Pass semi-structured data as native language objects (Java `Map`, Python dict, JavaScript object) rather than serialized JSON strings. The SDK serializes native objects correctly. A raw JSON string is stored as a string literal.

JavaPythonNode.js

Copy code

```
// Preferred: SDK converts the Map to a structured VARIANT
row.put("payload", Map.of("event_id", 101, "status", "active"));
```

Copy code

```
# Preferred: SDK converts the dict to a structured VARIANT
row["payload"] = {"event_id": 101, "status": "active"}
```

Copy code

```
// Preferred: SDK converts the object to a structured VARIANT
const row = {
  payload: { event_id: 101, status: "active" },
};
```

## Configure JVM heap size for Java deployments

The Java SDK includes a native Rust component that allocates memory outside the JVM heap. Limit the JVM heap to approximately 50% of available memory. For a host with 8 GB of RAM, set `-Xmx4g`:

Copy code

```
MAVEN_OPTS="-Xmx4g" mvn exec:java -Dexec.mainClass="com.example.Main"
# or
java -Xmx4g -jar your-app.jar
```
