# Named Channel operations

This topic covers lifecycle, monitoring, and recovery operations for Named Channels. For channel concepts and exactly-once delivery, see [Named Channels and exactly-once delivery](/user-guide/snowpipe-streaming/snowpipe-streaming-channels). For access privileges, see [Access control](/user-guide/snowpipe-streaming/snowpipe-streaming-access-control).

## Channel lifecycle

Open a Named Channel with `openChannel(channelName, offsetToken)`, append rows, and keep the channel open for the life of the ingestion task; avoid repeatedly opening and closing channels. For setup and code samples, see [Tutorial: Get started with the SDK](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-getting-started).

- List the channels you have access to with `SHOW CHANNELS`. For syntax, see [SHOW CHANNELS](/sql-reference/sql/show-channels).
- Drop a channel you no longer need with `dropChannel`. Flush pending data first unless you intend to discard it. For details, see [Named Channels and exactly-once delivery](/user-guide/snowpipe-streaming/snowpipe-streaming-channels).
- Inactive channels, along with their offset tokens, are deleted automatically after 30 days.

## Flush and graceful shutdown

Before shutting down a producer, flush pending data and wait for in-flight appends to complete.

JavaPythonNode.js

Copy code

```
channel.initiateFlush();
channel.waitForFlush(Duration.ofMinutes(2)).get();
channel.close();
```

Copy code

```
channel.initiate_flush()
channel.wait_for_flush(timeout_seconds=120)
channel.close()
```

Copy code

```
channel.initiateFlush();
await channel.waitForFlush({ timeoutMs: 120000 });
await channel.close();
```

The client exposes the same `initiateFlush` and `waitForFlush` methods. Its close options can also wait for all open channels to flush before shutdown.

The SDK batches appends automatically during normal ingestion. Use explicit flushes for checkpoints or shutdown, not after every row. A completed flush isn’t a committed-offset checkpoint: wait for the relevant offset to commit before advancing a replayable source. If a commit wait times out, retain the source position and check committed progress again rather than treating the timeout alone as a channel invalidation or replay instruction. See the [Named Channel SDK tutorial](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-getting-started#get-started-with-named-channels).

## Channel and offset status

Check a single channel’s status with `getChannelStatus()`, or check many at once with the client’s bulk `getChannelStatus(channelNames)` (SDK) or the [Bulk Get Channel Status](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-rest-api#bulk-get-channel-status) REST endpoint. Track `last_committed_offset_token` and `row_error_count` to confirm progress and catch bad records early. For the full field list, see [Channel status endpoint details](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-error-handling#channel-status-endpoint-details).

To find the last committed position and resume a source from there, call `getLatestCommittedOffsetToken` for a single channel or `getLatestCommittedOffsetTokens` for many channels. For the full recovery pattern, see [Offset tokens and exactly-once delivery](/user-guide/snowpipe-streaming/snowpipe-streaming-channels#label-replication-snowpipe-offset-tokens).

## Row errors

Turn on error logging on the target table to capture row-level processing failures in a dedicated error table, and monitor `row_error_count` on the channel status to detect them early. For setup and query examples, see [Error logging and error tables](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).

## Channel history

The [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY](/sql-reference/account-usage/snowpipe_streaming_channel_history) view provides a historical record of channel activity for monitoring and troubleshooting:

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

## Recovery from invalidation

A channel is invalid whenever `channel_status_code` isn’t `SUCCESS`. An invalid channel can surface to the client as an HTTP `409` response. Close and reopen the channel, then resume from the last committed offset token. Authorization errors (`401`, `403`) require a configuration fix instead of a reopen. For the full list of invalidating error codes and required client actions, see [Client-side error handling and required actions](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-error-handling#client-side-error-handling-and-required-actions).

## Prometheus metrics and logging

Enable Prometheus metrics on the SDK by setting the environment variable `SS_ENABLE_METRICS=true` before starting your application. The default endpoint is `/metrics` on port `50000`.

Copy code

```
export SS_ENABLE_METRICS=true
curl http://127.0.0.1:50000/metrics
```

For Prometheus scrape configuration and JVM heap-sizing guidance, see [Get Prometheus metrics](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-best-practices#get-prometheus-metrics).

## Migrating from the classic architecture

Classic applications generally migrate to Named Channels because both models use channel identities and offset tokens for recovery. See the [Migration guide](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-migration), [SDK comparison](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-comparison), and [Notice of planned deprecation](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-deprecation).
