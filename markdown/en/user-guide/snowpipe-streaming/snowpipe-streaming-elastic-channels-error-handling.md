# Error handling for Elastic Channels

This topic explains synchronous and asynchronous error handling for Elastic Channel appends.

## Synchronous failures

The following failures are raised synchronously by the append call itself:

- Validation errors (missing required fields, unsupported types)
- Serialization errors
- Closed-client errors (the client has already been closed)
- Immediate backpressure (the SDK’s local buffer is full)

Retain the row or batch data at the call site so you can log, retry, or route the data elsewhere. These failures do not invoke the asynchronous error callback.

On local backpressure, pause intake and retain the event whose append was rejected. Let pending appends drain and retry the rejected event with backoff. Don’t resubmit previously accepted appends just because a later append encountered backpressure.

For REST requests, HTTP 400 (Bad Request) errors are synchronous and indicate that the request was rejected before being accepted. Correct the request payload before retrying.

## Asynchronous outcomes

### Appends tracked through callbacks

`appendRow` and `appendRows` return as soon as the data is accepted locally. Outcomes are reported through callbacks when the append token is non-null:

- **Success callback** (`setSuccessHandler`): invoked after the durable acknowledgement.
- **Error callback** (`setErrorHandler`): invoked after an asynchronous failure.

An append with a `null` or `None` token reports outcomes to neither callback. There is also no future to check for `appendRow` or `appendRows` calls, so the outcome is not reported when the token is null.

### Appends that return a Future or Promise

`appendRowWithWait` and `appendRowsWithWait` return a `CompletableFuture<Void>` (Java), `Future` (Python), or `Promise` (Node.js) that completes successfully after the durable acknowledgement or reports an error if the append fails.

JavaPythonNode.js

Copy code

```
CompletableFuture<Void> ack = channel.appendRowWithWait(row, "batch-1");
try {
    ack.get();
    // durable acknowledgement received
} catch (ExecutionException e) {
    // asynchronous failure: log, buffer for retry, or raise
    System.err.println("Append failed: " + e.getCause());
}
```

Copy code

```
future = channel.append_row_with_wait(row, "batch-1")
try:
    future.result()
    # durable acknowledgement received
except Exception as e:
    # asynchronous failure: log, buffer for retry, or raise
    print("Append failed:", e)
```

Copy code

```
try {
    await channel.appendRowWithWait(row, "batch-1");
    // durable acknowledgement received
} catch (err) {
    // asynchronous failure: log, buffer for retry, or raise
    console.error("Append failed:", err);
}
```

These single-append examples illustrate outcome handling, not a production loop that waits after every row. For throughput, append events as they arrive and retain a bounded set of Futures or Promises, then wait for all pending appends to be durably acknowledged. The SDK batches internally.

### Caller wait timeouts

A caller’s deadline for waiting is separate from the outcome of the SDK append. Java `Future.get(timeout, unit)` and Python `Future.result(timeout=...)` can time out while the original append is still pending. In Node.js, a separate timeout observer can stop waiting without settling the original Promise.

Retain the original Future or Promise and the unresolved event, pause intake if necessary, and continue observing the original acknowledgement. Don’t immediately resubmit, cancel the handle, or recreate an otherwise valid client just because the caller stopped waiting. In Java, avoid applying `orTimeout` directly to the SDK’s `CompletableFuture` when you need to preserve its eventual acknowledgement, because it completes that same future exceptionally.

Advance an application checkpoint only after every relevant event succeeds. If the SDK reports a terminal error or invalidation, follow the recovery guidance below. If a process is lost or an unresolved append must be replayed, treat its outcome as ambiguous and use stable event IDs to reconcile possible duplicates.

## Durable acknowledgement semantics

A durable acknowledgement confirms that Snowflake has durably buffered the append. It does not mean:

- The rows are queryable in the target table. Materialization follows and can take several seconds.
- Rows are free of processing errors. Rows can still fail during table processing after acknowledgement. When error logging is enabled, Snowflake records these failures in the [error table](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables) for diagnosis and recovery.

## At-least-once delivery and duplicates

Elastic Channels provide at-least-once delivery. If a producer retries after an ambiguous outcome (network timeout, no response, or 5xx), Snowflake may already have accepted the original request and the target table can contain duplicate rows.

For SDK appends tracked through callbacks, the success and error callback details expose `requestId` and `retryCount`. A `retryCount` greater than `0` is a conservative signal that the SDK resent a rowset (batch of rows) and duplicates are possible. It does not prove that a duplicate occurred. For an error callback, interpret `retryCount` only when `requestId` is non-null. A null request ID indicates that the failure wasn’t associated with one identifiable server request, so the fields don’t determine whether the rows reached Snowflake.

For REST requests, supply `requestId` and `retryCount` as query parameters. Reuse the request ID when retrying the same rowset and increment the retry count for each attempt.

Include a stable event identifier in your data model and reconcile or deduplicate downstream when duplicates matter. Append tokens are application-side values and do not prevent server-side duplicates.

## Retry guidance

The SDK buffers appends and retries transient network and service failures internally while the client process is running. Don’t start a second retry loop for an append whose acknowledgement is still pending. These retries don’t provide crash recovery: buffered rows and recovery state aren’t persisted across process or node failure.

If the SDK reports a terminal append failure, retain the unresolved event and inspect the error before retrying. Recreate an invalidated client as described below. Correct validation, serialization, and persistent authorization errors rather than retrying unchanged input or configuration.

Direct REST clients own request retries:

- HTTP 429 (Too Many Requests) and transient 5xx responses: use exponential backoff with random variation in retry delays (jitter).
- Network timeout or no response: the request might already have been accepted. If retrying, reuse the same `requestId`, increment `retryCount`, and reconcile possible duplicates.
- HTTP 400 (Bad Request): correct the request payload before retrying.
- HTTP 401 / 403: fix authentication or permissions if the failure persists; don’t retry indefinitely with unchanged credentials.

## Client invalidation

If the client is invalidated (`InvalidClientException` in Java, similar in other SDKs), the entire client is affected. Close the existing client, initialize a new one, and get a new Elastic Channel. Before re-ingesting, identify which appends did not receive a durable acknowledgement and reingest only those rows. Do not reingest rows that already received a durable acknowledgement.

## Recover after a client or node failure

Classify events by their last known outcome:

- **Acknowledged**: Snowflake has durably buffered the append. Don’t replay it solely because the producer restarted.
- **Not acknowledged and known not to have been sent**: Replay from the source or durable application buffer.
- **No acknowledgement with an unknown outcome**: The append might have reached Snowflake. Replay if necessary, but treat the rows as possibly duplicated and reconcile by stable event identifier.

For loss-intolerant workloads, retain unacknowledged data in a replayable source or producer-side durable store before accepting responsibility for it. The SDK’s in-process buffer isn’t a write-ahead log and can’t recover rows after the process is lost. This doesn’t require Kafka or an external queue for every producer. For deployment choices and local-storage limits, see [Protect unacknowledged data](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-best-practices#protect-unacknowledged-data).

## Row-level errors

Turn on error logging on the target table to capture row-level processing failures in a dedicated error table. Rows that fail schema validation or type coercion are persisted to the error table with an error message.

For more information, see [Error logging in Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).

## Troubleshooting acknowledged rows not visible in the target table

1. Wait a few seconds for materialization to complete and query the target table again.
2. Check the error table for row-level processing failures.
3. Verify the pipe is active and the target table exists.
4. Check the [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY](/sql-reference/account-usage/snowpipe_streaming_channel_history) view for channel-level error details.
