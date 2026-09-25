# Elastic Channels operations

This topic covers durable acknowledgements, flush, shutdown, ingestion validation, and monitoring for Elastic Channels. For access privileges, see [Access control](/user-guide/snowpipe-streaming/snowpipe-streaming-access-control).

## Track durable acknowledgements with the SDK

Append events as they arrive and let the SDK batch internally. With appends that return a Future or Promise, retain a bounded set of Futures or Promises and periodically wait for all events in an application checkpoint to succeed. With appends tracked through callbacks, use non-null tokens and success and error handlers to track the same set of outcomes. A checkpoint tracks already submitted events, not a batch awaiting submission.

Use outstanding-event and byte limits to bound memory, and an elapsed-time trigger to checkpoint low-volume streams. Also checkpoint when intake pauses or ends. Keep the client open after a checkpoint so ingestion can resume without rebuilding it. Don’t advance a checkpoint past an unresolved event, even if later events have been acknowledged.

`waitForFlush` (Python: `wait_for_flush`) triggers a flush and waits for data submitted before the call to reach Snowflake. It doesn’t establish target-table visibility or replace inspecting append failures. Frequent explicit flushes can reduce the SDK’s ability to combine appends, so don’t flush after every row. If a wait times out, retain the unresolved events and original acknowledgement handles; see [Caller wait timeouts](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-error-handling#label-elastic-caller-timeouts).

Waiting for Elastic Channel acknowledgements is different from tracking Named Channel committed offsets. Elastic Channels have no `waitForCommit` operation or last-committed offset to query.

## Flush and graceful shutdown

Before shutting down a producer, flush pending data and wait for in-flight appends to complete. This reduces the risk of losing data that was submitted but not yet acknowledged.

JavaPythonNode.js

Copy code

```
// Stop accepting new source work, then initiate flush
channel.initiateFlush();

// Wait for all pending data to be flushed (with timeout)
CompletableFuture<Void> flush = channel.waitForFlush(Duration.ofMinutes(2));
flush.get();  // blocks until flush completes or throws on timeout/error

// Closing the client also closes the Elastic Channel
client.close();
```

Copy code

```
# Stop accepting new source work
channel.initiate_flush()

# Wait for pending data to flush
channel.wait_for_flush(timeout_seconds=120)

client.close()
```

Copy code

```
// Stop accepting new source work
channel.initiateFlush();

// Wait for pending data to flush
await channel.waitForFlush({ timeoutMs: 120000 });

await client.close();
```

Closing the client closes the Elastic Channel. Once the client is closed, any subsequent append calls raise an error immediately (synchronous closed-client failure, not an asynchronous callback).

For REST producers, ensure that all in-flight requests have received a successful HTTP response before stopping the process.

## Channel status

You can query the channel status to check the health of the Elastic Channel. The Elastic Channel name is always `ELASTIC`.

JavaPythonNode.js

Copy code

```
ChannelStatus status = channel.getChannelStatus();
System.out.println("Status: " + status.getStatusCode());
```

Copy code

```
status = channel.get_channel_status()
print("Status:", status.status_code)
```

Copy code

```
const status = await channel.getChannelStatus();
console.log("Status:", status.statusCode);
```

For historical channel activity, see [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY view](/sql-reference/account-usage/snowpipe_streaming_channel_history).

## Validate ingestion

After running your producer, verify data reached the target table. Materialization can follow the durable acknowledgement by several seconds.

Copy code

```
SELECT COUNT(*) FROM MY_DATABASE.MY_SCHEMA.MY_TABLE;
SELECT * FROM MY_DATABASE.MY_SCHEMA.MY_TABLE LIMIT 10;
```

### Check the error table

If rows are missing from the target after a durable acknowledgement, check the error table for row-level processing failures:

Copy code

```
SELECT * FROM MY_DATABASE.MY_SCHEMA.MY_TABLE__ERRORS
ORDER BY _SNOWFLAKE_INGEST_TIME DESC
LIMIT 20;
```

Turn on error logging on the target table to capture failed rows. For details, see [Error logging in Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).

### Check ingestion history

The [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY](/sql-reference/account-usage/snowpipe_streaming_channel_history) view provides a historical record of channel activity for monitoring and troubleshooting.

Copy code

```
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.SNOWPIPE_STREAMING_CHANNEL_HISTORY
WHERE DATABASE_NAME = 'MY_DATABASE'
  AND SCHEMA_NAME = 'MY_SCHEMA'
  AND TABLE_NAME = 'MY_TABLE'
ORDER BY START_TIME DESC
LIMIT 20;
```

## Prometheus metrics

For metrics setup, Prometheus configuration, and client logging, see [Monitor SDK clients with Prometheus and logs](/user-guide/snowpipe-streaming/snowpipe-streaming-event-table-telemetry#label-snowpipe-streaming-client-monitoring).
