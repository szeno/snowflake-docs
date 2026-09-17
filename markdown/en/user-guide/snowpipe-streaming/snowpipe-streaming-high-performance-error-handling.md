# Error handling in Snowpipe Streaming high-performance architecture

This topic explains Named Channel error handling for Snowpipe Streaming with high-performance architecture. For Elastic Channel error handling, see [Error handling for Elastic Channels](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-error-handling).

## Named Channel error handling

### Key error handling features

- Enhanced channel status endpoint: This edition extends the channel status endpoint to provide more comprehensive error information.
- Granular error details: The high-performance edition provides more detailed error information to help identify where it occurred and find the root causes of ingestion issues.
- Improved client experience: The high-performance edition simplifies error handling for clients, reducing the complexity of error reasoning and recovery.
- The channel history view: [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY view](/sql-reference/account-usage/snowpipe_streaming_channel_history) provides a historical record of channel activity to monitor and locate errors. This feature lets you track error trends and proactively address potential issues.

### Channel status endpoint details

The high-performance architecture includes a channel status endpoint to provide more detailed, point-in-time information about a channel.

In addition to the channel status information for the classic architecture, which is `statusCode`, `persistedOffsetToken`, the high-performance architecture includes the following information:

- `channel_status_code`: Represents the current operational status of the streaming channel. This code provides a high-level indication of the channel’s health and ability to ingest data. For more information about the channel status codes, see [Client-side error handling and required actions](#client-side-error-handling-and-required-actions).
- `last_commited_offset_token`: Indicates the offset token of the last row set that was successfully committed to the target table by Snowflake. This is crucial for tracking progress and ensuring data delivery.
- `created_on_ms`: The timestamp, in milliseconds, that indicates when the streaming channel was initially created within Snowflake.
- `database_name`: The name of the database to which the streaming channel is configured to ingest data.
- `schema_name`: The name of the schema within the specified database where the target table for the streaming channel resides.
- `pipe_name`: The name of the Snowpipe object that is configured to use this Snowpipe Streaming channel for data ingestion into a specific target table.
- `channel_name`: A user-created name for the specific Snowpipe Streaming channel instance.
- `rows_inserted`: A count of the total number of data rows that have been successfully inserted into the target table through this streaming channel since its creation.
- `rows_parsed`: A count of the total number of data rows that have been processed and parsed by the Snowpipe Streaming service for this channel. (but not necessarily inserted, for example, due to errors).
- `rows_error_count`: A count of the total number of data rows that encountered errors during processing and were therefore rejected by the Snowpipe Streaming service for this channel.
- `last_error_offset_upper_bound`: The upper bound of the offset token range of the last rowset (batch of rows) that contained errors. This helps in identifying the approximate location of the most recent errors within the data stream.
- `last_error_message`: A human-readable message corresponding to the latest error code.
- `last_error_timestamp`: The timestamp indicating when the most recent error occurred on this streaming channel.
- `snowflake_avg_processing_latency_ms`: The average latency, in milliseconds, observed by the Snowflake service in processing rowsets received by this channel. This metric provides insight into the performance of the ingestion pipeline within Snowflake.

### Error-handling flow

- Client sends data: The client application uses the Snowpipe Streaming SDK to send data to Snowflake through the `appendRow(s)` API.
- Server processing: The Snowflake service processes the data. This involves:

  - Buffering the data.
  - Parsing and validating the data.
  - Committing the data to the table.
- Error detection: Errors can occur during any of the server-side processing stages.
- Error recording: Snowflake records detailed information about the last error that occurred, including the following information:

  - The upper bound of the offset token range of the last rowset that contained errors. This helps in identifying the approximate location of the most recent errors within the data stream.
  - An error message.
  - A timestamp.
- Error reporting:

  - The enhanced channel status endpoint provides access to the recorded error information.
  - Clients can query this endpoint to retrieve details about the last error that occurred.
  - [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY view](/sql-reference/account-usage/snowpipe_streaming_channel_history) provides a historical record of errors and their offsets.
- Client action: The client application uses the error information to perform the following actions:

  - Identify the cause of the error.
  - Implement appropriate error handling logic, such as the following actions:
    - Retrying the failed operation.
    - Logging the error.
    - Alerting an administrator.
    - Moving the erroneous data to a dead-letter queue.
    - Reopening channels.

### Client-side error handling and required actions

The Snowpipe Streaming SDK simplifies error handling by implementing internal retry logic for transient errors. However, for fatal channel errors and persistent authorization issues, you are required to take manual action.

#### SDK retry logic for transient errors

The SDK automatically retries the request to send unflushed data in the channel to the server for the following HTTP status codes, as they typically indicate a temporary or transient service issue:

- 5XX (Server errors)
- 429 (Too many requests)
- 408 (Request timeout)

#### Channel errors that require a manual reopen

The Snowpipe Streaming SDK doesn’t automatically reopen the channel. When a channel enters a state that isn’t valid, you must explicitly close and reopen the channel to continue ingestion.

A channel is considered invalid — and requires client action — if the `channel_status_code` in the channel status response is anything other than `SUCCESS`.

The following table shows persisted error codes that indicate a fatal channel state and require the channel to be reopened:

| Error code | Context | Required client action |
| --- | --- | --- |
| ERR\_PIPE\_DOES\_NOT\_EXIST\_OR\_NOT\_AUTHORIZED | The target pipe is missing or inaccessible. | Fix the pipe issue. Reopen channel. |
| ERR\_TABLE\_DOES\_NOT\_EXIST\_NOT\_AUTHORIZED | The target table is missing or inaccessible. | Fix the table issue. Reopen channel. |
| ERR\_CHANNEL\_HAS\_INVALID\_ROW\_SEQUENCER | Row sequencing state isn’t valid. | Reopen channel. |
| ERR\_CHANNEL\_HAS\_INVALID\_CLIENT\_SEQUENCER | Channel sequencing state isn’t valid. | Reopen channel. |
| ERR\_CHANNEL\_MUST\_BE\_REOPENED | A general error indicating the channel is unusable. | Reopen channel. |
| ERR\_CHANNEL\_MUST\_BE\_REOPENED\_DUE\_TO\_ROW\_SEQ\_GAP | A gap in the row sequence was detected. | Reopen channel. |

Expand

Show lessSee more

#### Schema evolution failure and channel invalidation

When you use the Snowpipe Streaming high-performance architecture, it is important for you to understand a specific exception to the general `ON_ERROR=CONTINUE` behavior regarding schema evolution.

##### Channel invalidation on schema errors

Even if the `ON_ERROR=CONTINUE` option is configured for the load, the channel is invalidated if it encounters a schema evolution failure caused by user errors.

The following list includes common user errors that trigger channel invalidation:

- Submitting data with invalid column names that can’t be mapped.
- Attempting to add more columns than allowed by the configured column limit in a single batch. When columns are added across multiple batches, there is no limit.

This channel invalidation prevents the pipe from continuing to accept data that would cause persistent, non-recoverable schema issues. You can verify the invalidation status and reason for the channel failure by calling the `getChannelStatus()` method. For more information about the channel status fields, see [Channel status endpoint details](#channel-status-endpoint-details).

#### Authorization errors that require a configuration fix

When an ingestion attempt results in an HTTP authorization error, you must correct the underlying permission or credential issue. Don’t reopen the channel for these errors because the new channel immediately encounters the same problem.

- 401 (Unauthorized)
- 403 (Forbidden)

For these errors, stop the ingestion, and then fix the client application’s security configuration — for example, pipe permissions, user role, authentication credentials — before you resume ingestion. After you fix the authorization issue, you can reopen the client to continue ingestion.

### Handling SDK exceptions and HTTP status codes

When you use the Java SDK, methods such as `insertRows`, `getLatestCommittedOffsetToken`, and `getChannelStatus` might throw an `SFException`. To ensure resilient ingestion, applications must catch these exceptions, and then inspect `getHttpStatusCode()` to determine the required recovery action.

The following table describes common HTTP status codes, their error conditions, and the required actions:

| Status code | Error condition | Required action |
| --- | --- | --- |
| 409 | Channel invalidated | The channel is no longer valid; for example, superseded by another client. Close the current channel, call `openChannel` to create a new instance, and then resume from the last committed offset. |
| 429 | Throttling | The client is sending data too quickly. Implement an exponential back-off and retry strategy. |
| 500 / 503 | Service error | Transient network or server-side issues. These errors are typically retryable after a short delay. |
| 401 | Unauthorized | Authentication failed. Verify credentials, JWT configuration, or role permissions. |

Expand

Show lessSee more

#### Understanding invalidation levels

It is critical to distinguish between a channel invalidation and a client invalidation:

- **InvalidChannelException (HTTP 409)**: Only the specific channel is affected. Reopening the channel is sufficient.
- **InvalidClientException**: The entire `SnowflakeStreamingIngestClient` is compromised. You must close the existing client, initialize a new one using the factory, and then reopen all associated channels.

### Row-level error logging

For row-level error debugging, turn on **error logging** on your target table. When turned on, rows that fail
during server-side processing are automatically captured in a dedicated error table.

For more information, see [Error logging in Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).
