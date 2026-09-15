# Best practices for Snowpipe Streaming with classic architecture

## Cost optimization

As a best practice, we recommend calling the API with fewer Snowpipe Streaming clients that write more data per second. Use a Java or Scala application to aggregate data from multiple sources, such as IoT devices or sensors, and then use the Snowflake Ingest SDK to call the API to load data at higher flow rates. The API efficiently aggregates data across multiple target tables in an account.

A single Snowpipe Streaming client can open multiple channels to send data, but the client cost is only charged per active client. The number of channels does not affect the client cost. Therefore, we recommend using multiple channels per client for performance and cost optimization.

When you use the same tables for both batch and streaming ingestion, you can also reduce Snowpipe Streaming compute costs because of pre-empted file migration operations.

Snowpipe Streaming handles and bills all file-migration compute costs for tables with [Automatic Clustering](/user-guide/tables-auto-reclustering) enabled, where Snowpipe Streaming is inserting data. This process optimizes and migrates data within the same transaction, incorporating costs previously associated with Automatic Clustering.

## Performance recommendations

For optimal performance in high-throughput deployments, we recommend the following actions:

- If you are loading multiple rows, using `insertRows` is more efficient and cost effective than calling `insertRow` multiple times because less time is spent on locks.

  - Keep the size of each row batch passed to `insertRows` below 16 MB compressed.
  - The optimal size of row batches is between 10-16 MB.
- Pass values for the TIME, DATE, and all TIMESTAMP columns as one of the [supported types](/user-guide/snowpipe-streaming/snowpipe-streaming-table-support#label-snowpipe-streaming-supported-java-data-types) from the `java.time` package.
- When you create a channel using `OpenChannelRequest.builder`, set the `OnErrorOption` to `OnErrorOption.CONTINUE`, and manually check the return value from `insertRows` for potential ingestion errors. This approach currently leads to a better performance than relying on exceptions thrown when `OnErrorOption.ABORT` is used.
- When you set the default log level to DEBUG, make sure that the following loggers keep logging on INFO: their DEBUG output is very verbose, which can lead to a significant performance degradation.

  - `net.snowflake.ingest.internal.apache.parquet`
  - `org.apache.parquet`
- Channels should be long lived when a client is actively inserting data and should be reused because offset token information is retained. Don’t close channels after inserting data because data inside the channels is automatically flushed based on the time configured in `MAX_CLIENT_LAG`.

## Latency recommendations

When you use Snowpipe Streaming, latency refers to how quickly data written to a channel becomes available for querying in Snowflake. Snowpipe Streaming automatically flushes data within channels every one second, meaning you don’t need to explicitly close a channel for data to be flushed.

**Configuring latency with MAX\_CLIENT\_LAG**
With Snowflake Ingest SDK versions 2.0.4 and later, you can fine-tune data flush latency by using the `MAX_CLIENT_LAG` option:

- Standard Snowflake Tables (non-Iceberg): The default MAX\_CLIENT\_LAG is 1 second. You can override this to set your desired flush latency anywhere from 1 second up to a maximum of 10 minutes.
- Snowflake-managed Iceberg Tables: Supported by Snowflake Ingest SDK versions 3.0.0 and later, the default `MAX_CLIENT_LAG` is 30 seconds. This default helps ensure that optimized Parquet files are created, which is beneficial for query performance. While you can set a lower value, it’s generally not recommended unless you have exceptionally high throughput.

**Latency recommendations for optimal performance**
Setting `MAX_CLIENT_LAG` effectively can significantly impact query performance and the internal migration process (where Snowflake compacts small partitions).

For low-throughput scenarios, where you might only be sending a small amount of data (for example,e.g., 1 row or 1 KB) every second, frequent flushes can lead to numerous small partitions. This can increase query compilation time as Snowflake has to resolve many tiny partitions, especially if queries run before the migration process can compact them.

Therefore, you should set MAX\_CLIENT\_LAG as high as your target latency requirements allow. Buffering inserted rows for a longer duration allows Snowpipe Streaming to create better-sized partitions, which improves query performance and reduces migration overhead.
For example, if you have a task that runs every minute to merge or transform your streamed data, an optimal `MAX_CLIENT_LAG` might be between 50 and 55 seconds. This ensures data is flushed in larger chunks just before your downstream process runs.

**Kafka connector for Snowpipe Streaming**
It’s important to note that the Kafka connector for Snowpipe Streaming has its own internal buffer. Whenthe Kafka buffer flush time is reached, data is then sent to Snowflake with the standard one-second latency through Snowpipe Streaming. For more information, see [buffer.flush.time setting](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-kafka#label-snowpipe-streaming-kafka-buffer)

## Exactly-once delivery best practices

Achieving exactly-once delivery can be challenging, and adherence to the following principles in your custom code is critical:

> - To ensure appropriate recovery from exceptions, failures, or crashes, you must always reopen the channel and restart ingestion using the latest committed offset token.
> - Although your application may maintain its own offset, it’s crucial to use the latest committed offset token provided by Snowflake as the source of truth and reset your own offset accordingly.
> - The only instance in which your own offset should be treated as the source of truth is when the offset token from Snowflake is set or reset to NULL. A NULL offset token usually means one of the following:
>
>   - This is a new channel, so no offset token has been set.
>   - The target table was dropped and recreated, so the channel is considered new.
>   - There was no ingestion activity through the channel for 30 days, so the channel was automatically cleaned up, and the offset token information was lost.
> - If necessary, you can periodically purge the source data that has already been committed based on the latest committed offset token, and advance your own offset.
> - If the table schema is modified when Snowpipe Streaming channels are active, the channel must be reopened. The Snowflake Kafka connector handles this scenario automatically, but if you use Snowflake Ingest SDK directly, you must reopen the channel yourself.

For more information about how the Kafka connector with Snowpipe Streaming achieves exactly-once delivery, see
[Exactly-once semantics](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-kafka#label-snowpipe-streaming-kafka-exactly-once).
