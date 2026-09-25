# Best practices for Snowpipe Streaming with high-performance architecture

This guide outlines key best practices to design and implement robust data ingestion pipelines by using Snowpipe Streaming with high-performance architecture. By following these best practices, you ensure that your pipelines are durable, reliable, and have efficient error handling.

## Let the SDK batch automatically

Append rows as they arrive. The Java, Python, and Node.js SDKs buffer and combine appends internally using time and size thresholds, and handle compression and sending data to Snowflake. Use multi-row append APIs when your source already supplies multiple rows together, not as a prerequisite for throughput.

For each Named Channel, submit rows serially in source order without waiting for each row to commit. Bound outstanding work and retained bytes, and periodically wait for the committed offset to reach or pass your source checkpoint. Advance the source checkpoint only after that commit. An application checkpoint tracks committed progress, not how the SDK groups rows for sending. See [Open and use a Named Channel](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-getting-started#get-started-with-named-channels). For Elastic acknowledgements without offset tokens, see [Elastic Channels best practices](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-best-practices#label-elastic-bound-acknowledgements).

## Manage Named Channels strategically

Apply the following channel-management strategies for performance and long-term stability:

- **Use long-lived channels**: To minimize overhead, open a channel once, and then keep it active for the duration of the ingestion task. Avoid repeatedly opening and closing channels.
- **Use deterministic channel names**: Apply a consistent, predictable naming convention — for example, `source-env-region-client-id` — to simplify troubleshooting and facilitate automated recovery processes.
- **Scale out with multiple channels**: To increase throughput, open multiple channels. These channels can point to a single target pipe or to multiple pipes, depending on service limits and your throughput requirements.
- **Monitor channel status**: Regularly use the `getChannelStatus` method to monitor the health of your ingestion channels.
  - Track the `last_committed_offset_token` to verify that data is being ingested successfully and that the pipeline is making progress.
  - Monitor the `row_error_count` to detect bad records or other ingestion issues early.

## Validate the schema consistently

Ensure that incoming data conforms to the expected table schema to prevent ingestion failures and maintain data integrity:

- **Client-side validation**: Implement schema validation on the client side to provide immediate feedback and reduce server-side errors. Although full row-by-row validation offers maximum safety, a method that performs better might involve selective validation; for example, at batch boundaries or by sampling rows.
- **Server-side validation**: The high-performance architecture can offload schema validation to the server. Errors and their counts are reported through `getChannelStatus` if schema mismatches occur during ingestion into the target pipe and table.

## Add client-side metadata columns

To enable robust error detection and recovery, you must carry ingestion metadata as part of the row payload. This requires planning your data shape and PIPE definition in advance.

Add the following columns to your row payload before ingestion:

- `CHANNEL_ID`; for example, a compact INTEGER
- `STREAM_OFFSET`; a BIGINT that is monotonically increasing per channel, such as a Kafka partition offset

Together, these columns uniquely identify records per channel and enable you to trace the data’s origin.

Optionally, add a `PIPE_ID` column if multiple pipes ingest into the same target table. With this column, you can trace rows back to their ingestion pipeline. You can store descriptive pipe names in a separate lookup table, mapping them to compact integers to reduce storage costs.

## Detect and recover from errors using metadata offsets

Combine channel monitoring with your metadata columns to detect and recover from issues:

- **Monitor status**: Regularly check `getChannelStatus`. An increasing `row_error_count` is a strong indicator of a potential problem.
- **Detect missing records**: If errors are detected, use a SQL query to identify missing or out-of-order records by checking for gaps in your `STREAM_OFFSET` sequence.

Copy code

```
SELECT
  PIPE_ID,
  CHANNEL_ID,
  STREAM_OFFSET,
  LAG(STREAM_OFFSET) OVER (
    PARTITION BY PIPE_ID, CHANNEL_ID
    ORDER BY STREAM_OFFSET
  ) AS previous_offset,
  (LAG(STREAM_OFFSET) OVER (
    PARTITION BY PIPE_ID, CHANNEL_ID
    ORDER BY STREAM_OFFSET
  ) + 1) AS expected_next
FROM my_table
QUALIFY STREAM_OFFSET != previous_offset + 1;
```

## Batch rows and use compression for REST API requests

Direct REST clients must group and send rows themselves. Combine rows into requests using newline-delimited JSON (NDJSON), with one JSON object per line, and use compression to reduce network overhead. Bound request size and send partial batches based on elapsed time so low-volume streams don’t wait indefinitely for a full batch.

Named Channel REST requests have a 4 MB limit on the payload sent over the network, after compression if used. By using compression, you can fit a larger uncompressed data volume into each request, enabling higher throughput and reducing the number of API calls required.

Snowflake recommends using ZSTD as the high-performance compression algorithm, although Gzip is also supported.

For Snowflake-side tracing and duplicate detection, include a `requestId` UUID query parameter with each REST request. Use the same `requestId` for all retry attempts on the same rowset (batch of rows). Snowflake logs the request ID and can use it to correlate retried requests and identify potential duplicates. See [Limitations and considerations](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-limitations) for per-request payload limits.

## Optimize ingestion performance and cost with MATCH\_BY\_COLUMN\_NAME

Configure your pipe to map the necessary columns from your source data instead of ingesting all data into a single VARIANT column. To do this, use `MATCH_BY_COLUMN_NAME = CASE_SENSITIVE` or apply transformations in your pipe definition. This best practice not only optimizes your ingestion costs but also enhances the overall performance of your streaming data pipeline.

This best practice has the following important advantages:

- By using `MATCH_BY_COLUMN_NAME = CASE_SENSITIVE`, you’re only billed for the data values that are ingested into your target table. In contrast, ingesting data into a single VARIANT column bills you for all JSON bytes, including both the keys and the values. For data with verbose or numerous JSON keys, this can lead to a significant and unnecessary increase in your ingestion costs.
- Snowflake’s processing engine is more computationally efficient. Instead of parsing the entire JSON object into a VARIANT, and then extracting the required columns, this method directly extracts the necessary values.

## Use native data types for semi-structured data

For optimal performance and data integrity, provide semi-structured data by using native language objects rather than serialized strings.

- **Performance**: With native objects, the SDK can handle data more efficiently without requiring additional parsing steps on the Snowflake server.
- **Type Safety**: The high-performance architecture treats string literals as literal text. By using native objects, you ensure that your data is stored as structured JSON rather than escaped string values.

JavaPythonNode.js

Copy code

```
// Preferred: SDK converts the List to a structured ARRAY
row.put("tags", Arrays.asList("electronics", "sale"));
```

Copy code

```
# Preferred: SDK converts the dict to a structured VARIANT
row["payload"] = {"event_id": 101, "status": "active"}
```

Copy code

```
// Preferred: use a native Array for ARRAY columns
const row = {
  tags: ["electronics", "sale"],
  payload: { event_id: 101, status: "active" },
};
await channel.appendRow(row, "1");
```

## Get Prometheus metrics

For metrics setup, Prometheus configuration, and client logging, see [Monitor SDK clients with Prometheus and logs](/user-guide/snowpipe-streaming/snowpipe-streaming-event-table-telemetry#label-snowpipe-streaming-client-monitoring).

## Memory management on Linux and macOS

Beginning with SDK version 1.5.0, the Snowpipe Streaming SDK uses the [jemalloc](https://jemalloc.net/) memory allocator on Linux and macOS to keep memory usage stable under sustained high-throughput streaming workloads. This change applies to the Java, Python, and Node.js SDKs and is enabled automatically. You don’t need to update your application or set any configuration.

What this means for your application:

- More predictable memory usage in long-running ingest processes that hold many channels open or run at high throughput.
- Reduced memory fragmentation compared to the default system allocator on Linux.
- No change to the SDK’s public API or to existing configuration.

Windows builds continue to use the system allocator and aren’t covered by this change. If you run the SDK on Windows under sustained high throughput and observe steadily increasing memory usage, consider running the workload on Linux or macOS, or contact [Snowflake Support](/user-guide/contacting-support).

### Configure JVM heap size for Java deployments

The SDK includes a native Rust component that allocates memory outside the JVM heap. When you use the Java wrapper, limit the JVM heap to approximately 50% of available memory to leave room for the SDK’s native allocations.

For example, for a host with 8 GB of RAM, set `-Xmx4g`:

Mavenjava command

Copy code

```
MAVEN_OPTS="-Xmx4g" mvn exec:java -Dexec.mainClass="com.example.Main"
```

Copy code

```
java -Xmx4g -jar your-app.jar
```

## Designing for resiliency

### Wrap ingestion in try-catch blocks

Don’t assume that an append call always succeeds. Synchronous validation, serialization, closed-client, and immediate backpressure failures are raised directly by the append call. Catch the SDK error (for example, `StreamingIngestError` in Python), and then retry or otherwise handle it. Never ignore or drop the returned error. Interpret the HTTP status codes, specifically 409 for Named Channel invalidations and 429 for throttling.

Some errors surface asynchronously, after rows are buffered rather than at the append call. Monitor Named Channel status (for example, `getChannelStatus` or `row_error_count`) to detect failures that appear later.

### Implement exponential back-off

For retryable errors (429, 500, 503), don’t retry immediately. Use an exponential back-off strategy —– increasing the wait time between each retry —– to allow the system to recover.

### Verify progress with offset tokens

Periodically call `getLatestCommittedOffsetToken` to track which data was successfully persisted. If a 409 error occurs, use this token to identify the exact point from which to replay data after reopening the channel.

### Monitor channel status

Regularly check `getChannelStatus()`. If the status code is anything other than `SUCCESS`, trigger your error-handling logic to reset the channel or client connection.
