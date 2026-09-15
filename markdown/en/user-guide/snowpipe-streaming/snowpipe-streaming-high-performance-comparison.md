# Comparison between Snowpipe Streaming high-performance and classic SDKs

This section summarizes the main differences between the classic and high-performance SDKs.

**Client and channel management**

- **OpenClient**: The high-performance SDK requires you to specify the `DB`, `SCHEMA`, and `PIPE`. In the classic SDK, you only need to specify a client `NAME`.
- **OpenChannel**: The high-performance SDK simplifies this by only requiring the channel name. The classic SDK requires you to specify the `DB`, `SCHEMA`, `TABLE`, and an `ERROR_OPTION`. The new SDK also returns an `OpenChannelResult` that contains the channel entity and status, removing the need for a separate RPC call to get the last committed offset token.
- **Support for offsetToken**: The new `openChannel` method now has an optional `offsetToken` parameter, allowing you to open a channel at a specific position. `openChannel(String channelName, (optional) String offsetToken)`.

**Data ingestion**

- **InsertRows renamed**: The `InsertRows` method is now called `AppendRows` in the high-performance SDK.
- **AppendResult removed**: The `appendRow` and `appendRows` methods no longer return an `AppendResult`. Their signatures have changed to `void appendRow(Map<String, Object> row, String offsetToken)` and `void appendRows(Iterable<Map<String, Object>> row, String startOffsetToken, String endOffsetToken)`.

**New asynchronous and utility methods**

- **GetChannelStatus**: This is a new API available on the `Channel` object.
- **waitForFlush**: New `waitForFlush` methods have been added to both the client and channel objects.

  - Client: `void close(boolean waitForFlush, Duration timeoutDuration)`
  - Channel and Client: `void waitForFlush((optional) Duration timeoutDuration)`
- **waitForCommit**: A new method, `CompletableFuture<Boolean> waitForCommit(Predicate<String> tokenChecker, Duration timeoutDuration)`, lets you wait for a commit to be confirmed.
- **initiateFlush**: This new method `void initiateFlush()` asynchronously calls a flush on a channel or client. The method lets you flush data without waiting for the timeout or size limits.

**Data type and parsing**

The high-performance architecture requires native objects for ARRAY and VARIANT columns and doesn’t auto-parse string literals.

| Column Type | Classic | High-performance |
| --- | --- | --- |
| OBJECT | Automatically parses JSON strings. | No change. Automatically parses JSON strings. |
| ARRAY | Implicitly parses strings. For example, “[1,2]” becomes [1,2]. | Type-strict. Treats strings as literals. For example, “[1,2]” becomes [“[1,2]”]. |
| VARIANT | Implicitly parses strings. For example, “true” becomes true. | Type-strict. Treats strings as literals. For example, “true” becomes “true”. |

Expand

Show lessSee more

To ensure semi-structured data is stored correctly in the high-performance architecture, pass native language objects (for example, Java List/Map, Python list/dict, or JavaScript Array/Object) instead of serialized JSON strings.

**Other changes**

- **GetLatestCommittedOffsetTokens**: This API is improved. In the high-performance SDK, it can now fetch offset tokens for channels not opened by the client and allows for partial failures.
- **isValid removed**: The `isValid` method is removed from the high-performance SDK.
- **Schema evolution support**: The high-performance SDK supports [schema evolution](/user-guide/data-load-schema-evolution), a key capability for handling changing data schemas automatically.

The following tables show the API changes from the classic SDK to the high-performance SDK:

## SnowflakeStreamingIngestClientFactory and SnowflakeStreamingIngestClientFactory.Builder

| Classic | High-performance | Notes |
| --- | --- | --- |
| `builder(String name)` | `builder(String clientName, String dbName, String schemaName, String pipeName)` | `name` in the classic version = `clientName` in the high-performance version. |
| N/A | `setExecutorService(ExecutorService executorService)` | A new method. Allows you to specify the `ExecutorService` the SDK will use for its background tasks. |

Expand

Show lessSee more

## SnowflakeStreamingIngestClient

> | Classic | High-performance | Notes |
> | --- | --- | --- |
> | `String getName()` | `String getClientName()` | API name change only; the same information is returned. |
> | N/A | `String getDBName()` | New API. |
> | N/A | `String getPipeName()` | New API. |
> | N/A | `String getSchemaName()` | New API. |
> | `SnowflakeStreamingIngestChannel` *openChannel(OpenChannelRequest request)* | `OpenChannelResult` *openChannel(String channelName, (optional) String offsetToken)* | Different request args and return values. |
> | `Map<String,String> getLatestCommittedOffsetTokens` `(List<SnowflakeStreamingIngestChannel> channels)` | `Map<String, String> getLatestCommittedOffsetTokens` `(List<String> channelNames)` | Different request args. High-performance SDK enables the API to fetch the channel’s status that is opened by other clients and potentially don’t belong to the client. |
> | N/A | `ChannelStatusBatch getChannelStatus(List<String> channelNames)` | New API. |
> | `Void dropChannel(DropChannelRequest request)` | `Void dropChannel(String channelName)` | Different request argument. |
> | `Void setRefreshToken(String refreshToken)` | N/A | Removed. |
> | N/A | `CompletableFuture<Void> close(boolean waitForFlush, Duration timeoutDuration)` | A new client `close` method that has more control over the shutdown process. `waitForFlush`: A Boolean parameter to indicate whether the client should wait for all channels to flush before shutting down. `timeoutDuration`: A `Duration` to specify how long the client should wait for the flush to complete before a forced shutdown. |
> | N/A | `CompletableFuture<Void> waitForFlush((optional) Duration timeoutDuration)` | A new method to wait for the flush to complete. `timeoutDuration`: Specifies how long the client should wait before timing out. |
> | N/A | `void initiateFlush()` | A new method for clients to asynchronously trigger a flush and return immediately. |
>
> Expand
>
> Show lessSee more

## **SnowflakeStreamingIngestChannel**

> | Classic | High-performance | Notes |
> | --- | --- | --- |
> | `getLatestCommittedOffsetToken` | `getLatestCommittedOffsetToken` | This API has been improved. In the high-performance SDK, it can now fetch offset tokens for channels not opened by the client and allows for partial failures. |
> | `isValid` | N/A | Removed. |
> | N/A | `String getDBName()` | New API. |
> | N/A | `String getSchemaName()` | New API. |
> | N/A | `String getPipeName()` | New API. |
> | N/A | `String getFullyQualifiedPipeName()` | New API. |
> | `InsertValidationResponse insertRow(Map<String, Object> row, String offsetToken)` | `void appendRow(Map<String, Object> row, @Nullable String offsetToken)` | API name changed. Response type changed because there is no more validation on the client. |
> | `InsertValidationResponse insertRow(Iterable<Map<String, Object>> row, @Nullable String startOffsetToken, @Nullable String endOffsetToken)` | `void appendRows(Iterable<Map<String, Object>> row, String startOffsetToken, String endOffsetToken)` | API name changed. Response type changed because there is no more validation on the client. |
> | `InsertValidationResponse insertRow(Iterable<Map<String, Object>> row, String offsetToken)` | N/A | Removed. |
> | `String getTableName()` | N/A | Removed. |
> | `String getFullyQualifiedTableName()` | N/A | Removed. |
> | N/A | `String getPipeName()` | New API. |
> | N/A | `String getFullyQualifiedPipeName()` | New API. |
> | `String getName()` | `String getChannelName()` | API name change. |
> | `String getFullyQualifiedName()` | `String getFullyQualifiedChannelName()` | API name change. |
> | `Map<String, ColumnProperties> getTableSchema()` | N/A | Removed. |
> | N/A | `ChannelStatus getChannelStatus()` | New API. |
> | `CompletableFuture<Void> close()` | `Void close()` | The return type is changed, but the behavior is the same. |
> | `CompletableFuture<Void> close(boolean drop)` | `Void close(boolean waitForFlush, Duration timeoutDuration)` | API name is changed, but the behavior is the same. |
> | `Boolean isValid()` | N/A | Removed. |
> | N/A | `CompletableFuture<Void> waitForFlush((optional)Duration timeoutDuration)` | A new method to wait for the flush to complete. `timeoutDuration`: Specifies how long the channel should wait before timing out. |
> | N/A | `void waitForCommit(Predicate<String> tokenChecker, Duration timeoutDuration)` | A new method that asynchronously triggers and waits for the flush of all buffered data within this specific channel to the Snowflake server. This method ensures that all pending data is successfully written and the flush operation is complete before proceeding. |
> | N/A | `void initiateFlush()` | A new method for channels to asynchronously trigger a flush. |
>
> Expand
>
> Show lessSee more
