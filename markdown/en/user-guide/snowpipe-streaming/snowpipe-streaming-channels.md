# Named Channels and exactly-once delivery

Named Channels provide ordered, exactly-once ingestion for applications that coordinate Snowflake commits with source offsets. Use them for partitioned sources such as Kafka or Change Data Capture (CDC), where each source partition maps to a channel.

## How Named Channels work

A Named Channel is a logical streaming connection to Snowflake for loading data into a table. Named Channels provide two guarantees:

- **Ordered ingestion**: The ordering of rows and their corresponding offset tokens is preserved within a channel.
- **Exactly-once delivery**: Offset tokens enable clients to track committed progress and replay from the last committed position on recovery.

Ordering is preserved within a Named Channel but not across Named Channels that point to the same table.

Named Channels are opened against a pipe. The client SDK can open multiple channels to multiple pipes; however, the SDK can’t open channels across accounts. Named Channels are meant to be long lived when a client is actively inserting data and should be reused across client process restarts because offset token information is retained.

You can permanently drop channels by using the `DropChannelRequest` API when you no longer need the channel and the associated offset metadata. You can drop a channel in two ways:

- Dropping a channel at closing. Data inside the channel is automatically flushed before the channel is dropped.
- Dropping a channel blindly. We don’t recommend this approach because it discards any pending data.

You can run the SHOW CHANNELS command to list the channels for which you have access privileges. For more information, see [SHOW CHANNELS](/sql-reference/sql/show-channels).

Note

Inactive channels, along with their offset tokens, are deleted automatically after 30 days of inactivity.

### Offset tokens and exactly-once delivery

Tip

**How exactly-once works in Snowpipe Streaming**: Your application submits rows with an offset token (for example, a Kafka partition offset). Snowflake persists the token when the data is committed. On recovery, retrieve the last committed offset for the reopened channel and replay retained records starting after that offset. Records can be retained in the source or in durable application-managed storage. Preserve their original offsets and order, and retain them until their offsets commit; offset tokens don’t make the producer’s memory persistent.

An *offset token* is a string that a client includes in row-submission requests to track ingestion progress on a per-channel basis. The specific methods used are `appendRow` or `appendRows` for the SDK and the `Append Rows` endpoint for the REST API.

The token is initialized to NULL on channel creation and is updated when the rows with a provided offset token are committed to Snowflake. Clients can periodically call `getLatestCommittedOffsetToken` to get the latest committed offset token for a channel and use that to reason about ingestion progress.

When a client re-opens a channel, the latest persisted offset token is returned. The client can reset its position in the data source by using the token to avoid sending the same data twice. When a channel re-open event occurs, any uncommitted data buffered in Snowflake is discarded to avoid committing it.

You can use the latest committed offset token to perform the following:

> - Track ingestion progress
> - Check whether a specific offset has been committed by comparing it with the latest committed offset token
> - Advance the source offset and purge the data that has already been committed
> - Enable de-duplication and ensure exactly-once delivery of data

**Example: Kafka connector crash recovery**

The Kafka connector stores the Kafka partition offset as the offset token (for example, `20`). When the connector restarts, it calls `getLatestCommittedOffsetToken` on the reopened channel, retrieves the last committed offset, and resets the Kafka read cursor to the next record (`21`). No duplicate data is ingested.

**Example: Log file ingestion with crash recovery**

An application stores the log file name and line number as the offset token (for example, `messages_1.log:20`). On restart, it calls `getLatestCommittedOffsetToken`, retrieves that token, and resumes reading from line `21` of `messages_1.log` to avoid re-ingesting committed data.

Note

The offset token information can be lost. The offset token is linked to a channel object, and a channel is automatically cleared if no new ingestion is performed using the channel for a period of 30 days. To prevent the loss of the offset token, consider maintaining a separate offset and resetting the channel’s offset token if required.

### Roles of `offsetToken` and `continuationToken`

Both `offsetToken` and `continuationToken` are used to ensure exactly-once data delivery, but they serve different purposes and are managed by different subsystems. The primary distinction is who controls the token’s value and the scope of its use.

- `continuationToken` (only used by direct REST API users):

  Snowflake returns a `next_continuation_token` when you open a Named Channel or append rows through REST. Pass that value as `continuationToken` in the next append request. This lets Snowflake validate the request sequence within the channel. SDK users don’t manage continuation tokens themselves.
- `offsetToken`:

  This token is a user-defined identifier that enables exactly-once delivery from an external source. Snowflake stores this value but doesn’t use it for its own internal operations or to prevent re-ingestion. It is the responsibility of the external system, such as a Kafka connector, to read the offsetToken from Snowflake and use it to track its own ingestion progress and avoid sending duplicate data if the external stream needs to be replayed.
