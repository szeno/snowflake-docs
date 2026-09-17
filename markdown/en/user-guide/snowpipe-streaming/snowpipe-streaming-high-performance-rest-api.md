# Snowpipe Streaming REST API endpoints

Note

Where possible, use the Snowpipe Streaming SDK instead of the REST API to benefit from automatic batching and simpler integration. Use direct REST when an SDK isn’t suitable for your environment.

The Snowpipe Streaming REST API is designed for lightweight workloads and provides a flexible way to integrate with external applications without using a Snowpipe Streaming SDK.

This reference documents both ingestion modes:

- [Elastic Channel endpoints](#elastic-channel-rest-api) for at-least-once ingestion without channel lifecycle or offset-token management.
- [Named Channel endpoints](#named-channel-rest-api) for ordered, exactly-once ingestion.

## Request headers

The following request headers apply to all the endpoints for the Snowpipe Streaming REST API:

| Header | Description |
| --- | --- |
| `Authorization` | Authentication token |
| `X-Snowflake-Authorization-Token-Type` (optional) | JWT/OAuth |
| `Content-Encoding` (optional) | Specifies the compression format of the payload. Supported: `gzip`, `zstd`. |
| `User-Agent` (optional) | Identifies the client application. Recommended format: `SnowpipeStreamingSDK/{version} ({platform}) {LANGUAGE}/{language_version} (app={partner-name})`. Example: `SnowpipeStreamingSDK/1.0.0 (Linux amd64) PYTHON/3.11.0 (app=MyPartnerApp)`. |

Expand

Show lessSee more

Direct REST clients must group rows into newline-delimited JSON (NDJSON), with one JSON object per line, and handle compression themselves. Both Elastic and Named Channel append requests have a 4 MB payload limit (the payload size sent over the network, after compression if used). Batch rows and use ZSTD or Gzip compression to reduce request overhead; bound batch size and elapsed time before sending.

## Get Hostname

The `Get Hostname` returns the hostname used to interact with the Snowpipe Streaming REST API. Each account has a unique hostname.

Note

For private connectivity (AWS PrivateLink, Azure Private Link, or Google Cloud Private Service Connect), call this endpoint through your private account URL, and configure private DNS for the returned ingest hostname before you use it for the scoped-token exchange and streaming operations. For complete steps, see [Discover and configure the ingest host](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-rest-tutorial) in the REST API tutorial.

```
GET /v2/streaming/hostname
```

Response:

Copy code

```
{
  "hostname": "string"
}
```

Description of response fields:

| Field | Type | Description |
| --- | --- | --- |
| Hostname | String | The hostname of the account. |

Expand

Show lessSee more

## Exchange Scoped Token

The `Exchange Scoped Token` returns a security token that can be used to access only the Snowpipe Streaming API-related service. This provides security protection for the customer.

```
POST /oauth/token
```

Request:

| Attribute | Required | Component | Description |
| --- | --- | --- | --- |
| content\_type | Yes | Header | “application/x-www-form-urlencoded” |
| grant\_type | Yes | Payload | “<urn:ietf:params:oauth:grant-type:jwt-bearer>” |
| scope | Yes | Payload | The hostname of the account. |

Expand

Show lessSee more

Response:

Copy code

```
{
  "token": "string"
}
```

Description of response fields:

| Field | Type | Description |
| --- | --- | --- |
| Token | String | The scoped token. |

Expand

Show lessSee more

## Elastic Channel endpoints

Elastic Channels don’t require a separate open-channel operation. Send a batch of NDJSON rows directly to a table or to the implicit `ELASTIC` channel of a pipe:

```
POST /v2/streaming/data/databases/{databaseName}/schemas/{schemaName}/tables/{tableName}/rows
POST /v2/streaming/data/databases/{databaseName}/schemas/{schemaName}/pipes/{pipeName}/channels/ELASTIC/rows
```

The table endpoint is only for Elastic Channels. On the first request, Snowflake creates or resolves the managed default pipe named `<tableName>-STREAMING`. Each streaming pipe includes an implicit `ELASTIC` channel, which the request uses without a separate open-channel operation. Use the pipe endpoint for an Elastic Channel on a custom pipe with in-flight transformations or pre-clustering.

### Elastic request attributes

| Attribute | Required | Component | Description |
| --- | --- | --- | --- |
| `databaseName` | Yes | URI | Database name, case-insensitive. |
| `schemaName` | Yes | URI | Schema name, case-insensitive. |
| `tableName` or `pipeName` | Yes | URI | The target table for the default pipe, or the custom pipe name. |
| `rows` | Yes | Body | NDJSON rows. The maximum Elastic request payload is 4 MB (the payload size sent over the network, after compression if used). |
| `requestId` | No | Query parameter | A UUID that tracks the request. Use the same value on every retry of the same rowset (batch of rows), and generate a new UUID for each distinct rowset. |
| `retryCount` | No | Query parameter | The retry attempt number, starting at `0`. Increment it for each retry. A value greater than `0` signals that duplicate rows are possible; it doesn’t prove that a duplicate occurred. |

Expand

Show lessSee more

Elastic requests must not include `offsetToken`, `startOffsetToken`, `endOffsetToken`, or `continuationToken`.

### Elastic response and delivery semantics

A successful HTTP 200 response is the durable acknowledgement: Snowflake has durably buffered the request payload. It doesn’t mean that rows are immediately queryable in the target table. Row-level processing errors are persisted to the [error table](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables) when error logging is enabled.

Copy code

```
{
  "message": "OK"
}
```

Elastic Channels provide at-least-once delivery without an ordering guarantee. Retrying after an ambiguous response can produce duplicate rows. Include a stable event identifier in the row payload and reconcile or deduplicate downstream when duplicates matter.

### Elastic append example

Copy code

```
export REQUEST_ID=$(uuidgen)

curl -sS -X POST \
  -H "Authorization: Bearer $SCOPED_TOKEN" \
  -H "Content-Type: application/x-ndjson" \
  "https://${INGEST_HOST}/v2/streaming/data/databases/$DB/schemas/$SCHEMA/tables/$TABLE/rows?requestId=$REQUEST_ID&retryCount=0" \
  --data-binary @rows.ndjson | jq .
```

For a retry of this rowset, reuse `REQUEST_ID` and increment `retryCount`. To use a custom pipe, replace the table path with `/pipes/$PIPE/channels/ELASTIC/rows`.

## Named Channel endpoints

Named Channels require explicit channel lifecycle, continuation tokens, and source offset tokens. The following operations support ordered, exactly-once ingestion.

The following diagram shows the Named Channel request flow:

> ![Snowpipe Streaming named-channel REST API flow](/static/images/data-load-snowpipe-streaming-rest-api.png)

### Open a Named Channel

The `Open Channel` operation creates or opens a new channel against a pipe or table. If the channel already exists, Snowflake bumps the client sequencer of the channel and returns the last committed offset token.

```
PUT /v2/streaming/databases/{databaseName}/schemas/{schemaName}/pipes/{pipeName}/channels/{channelName}
```

Request:

| Attribute | Required | Component | Description |
| --- | --- | --- | --- |
| databaseName | Yes | URI | Database name, case-insensitive. |
| schemaName | Yes | URI | Schema name, case-insensitive. |
| pipeName | Yes | URI | Pipe name, case-insensitive. |
| channelName | Yes | URI | The name of the channel that you create or re-open, case-insensitive. |
| offset\_token | No | Payload | String used to set an offset token when opening a channel. |
| fail\_on\_uncommitted\_rows | No | Payload | Boolean. When `true`, the server rejects the request with HTTP `409 Conflict` (`ERR_CHANNEL_HAS_UNCOMMITTED_DATA`) if the channel has uncommitted in-flight data. Otherwise, in-flight data is silently discarded and can slow co-located channels on the pipe (default: `false`). |
| requestId | No | Query parameter | A universally unique identifier (UUID) used to track requests through the system. |

Expand

Show lessSee more

Response:

Copy code

```
{
  "next_continuation_token": "string",
  "channel_status": {
    "database_name": "string",
    "schema_name": "string",
    "pipe_name": "string",
    "channel_name": "string",
    "channel_status_code": "string",
    "last_committed_offset_token": "string",
    "created_on_ms": "long",
    "rows_inserted": "int",
    "rows_parsed": "int",
    "rows_error_count": "int",
    "last_error_offset_upper_bound": "string",
    "last_error_message": "string",
    "last_error_timestamp": "timestamp_utc",
    "snowflake_avg_processing_latency_ms": "int"
  }
}
```

Description of response fields:

| Field | Type | Description |
| --- | --- | --- |
| next\_continuation\_token | String | An API-managed token that must be used in the subsequent Append Rows request. The token links a series of calls, ensuring a contiguous, in-order stream of data and maintaining the session state for exactly once delivery. |
| channel\_status | Object | A nested object with the following detailed information about the channel:   - database\_name (String): The name of the database where the pipe is located. - schema\_name (String): The name of the schema where the pipe is located. - pipe\_name (String): The name of the specific pipe being used. - channel\_name (String): The name of the streaming channel. - channel\_status\_code (String): A code that indicates the current status of the channel; for example, “ACTIVE”. - last\_committed\_offset\_token (String): The token that represents the last successfully committed offset. - created\_on\_ms (Long): The timestamp, in milliseconds, when the channel was created. - rows\_inserted (Int): The total number of rows successfully inserted. - rows\_parsed (Int): The total number of rows parsed. - rows\_error\_count (Int): The total number of rows that encountered an error. - last\_error\_offset\_upper\_bound (String): A token that indicates the upper bound of the offset where the last error occurred. - last\_error\_message (String): The message of the last error that occurred. - last\_error\_timestamp (Long): The timestamp, in milliseconds, of the last error. - snowflake\_avg\_processing\_latency\_ms (Int): The average processing latency of Snowflake in milliseconds. |

Expand

Show lessSee more

### Append rows to a Named Channel

The `Append Rows` operation inserts a batch of rows to the given channel.

```
POST /v2/streaming/data/databases/{databaseName}/schemas/{schemaName}/pipes/{pipeName}/channels/{channelName}/rows
```

Request:

| Attribute | Required | Component | Description |
| --- | --- | --- | --- |
| databaseName | Yes | URI | Database name, case-insensitive. |
| schemaName | Yes | URI | Schema name, case-insensitive. |
| pipeName | Yes | URI | Pipe, case-insensitive. |
| channelName | Yes | URI | Channel name, case-insensitive. |
| continuationToken | Yes | Query parameter | Continuation token from Snowflake, encapsulates both client and row sequencers. |
| startOffsetToken | No | Query parameter | Offset token for the first row in the batch. |
| endOffsetToken | No | Query parameter | Offset token for the last row in the batch. |
| rows | Yes | Payload | The actual data payload to be ingested in NDJSON format. The maximum allowed size for this attribute is 4 MB. |
| requestId | No | Query parameter | A UUID used to track requests through the system. |

Expand

Show lessSee more

Note

The JSON text within the NDJSON payload must strictly conform to the `RFC 8259` standard. Each JSON text must be followed by a newline character `\n` (`0x0A`). You can also insert a carriage return `\r` (`0x0D`) before the newline character.

Response:

Copy code

```
{
  "next_continuation_token": "string"
}
```

Description of response fields:

| Field | Type | Description |
| --- | --- | --- |
| next\_continuation\_token | string | The next continuation token from Snowflake, which encapsulates both client and row sequencers. It should be used for inserting the next batch. |

Expand

Show lessSee more

### Drop a Named Channel

The `Drop Channel` operation drops a channel at server side along with its metadata.

```
DELETE /v2/streaming/databases/{databaseName}/schemas/{schemaName}/pipes/{pipeName}/channels/{channelName}
```

Request:

| Attribute | Required | Component | Description |
| --- | --- | --- | --- |
| databaseName | Yes | URI | Database name, case-insensitive |
| schemaName | Yes | URI | Schema name, case-insensitive |
| pipeOrTableName | Yes | URI | Pipe or table name, case-insensitive |
| channelName | Yes | URI | Channel name, case-insensitive |
| fail\_on\_uncommitted\_rows | No | Payload | Boolean. When `true`, the server rejects the request with HTTP `409 Conflict` (`ERR_CHANNEL_HAS_UNCOMMITTED_DATA`) if the channel has uncommitted in-flight data. Otherwise, in-flight data is silently discarded and can slow co-located channels on the pipe (default: `false`). |
| requestId | No | Query parameter | A UUID used to track requests through the system |

Expand

Show lessSee more

Response:

This operation returns a payload with no specific successful response other than the HTTP status code.

### Get Named Channel status in bulk

The `Bulk Get Channel Status` operation returns the status of a channel for a specific client sequencer.

```
POST /v2/streaming/databases/{databaseName}/schemas/{schemaName}/pipes/{pipeName}:bulk-channel-status
```

Request:

| Attribute | Required | Component | Description |
| --- | --- | --- | --- |
| databaseName | Yes | URI | Database name, case-insensitive |
| schemaName | Yes | URI | Schema name, case-insensitive |
| pipeName | Yes | URI | Pipe name, case-insensitive |
| channel\_names | Yes | Payload | An array of String channel names that the customer wants to get status for; the names are case-sensitive. For example, `{"channel_names":["channel1", "channel2"]}`. |

Expand

Show lessSee more

Response:

Copy code

```
{
  "channel_statuses": {
    "channel1": {
      "channel_status_code": "String",
      "last_committed_offset_token": "String",
      "database_name": "String",
      "schema_name": "String",
      "pipe_name": "String",
      "channel_name": "String",
      "rows_inserted": "int",
      "rows_parsed": "int",
      "rows_errors": "int",
      "last_error_offset_upper_bound": "String",
      "last_error_message": "String",
      "last_error_timestamp": "timestamp_utc",
      "snowflake_avg_processing_latency_ms": "int"
    },
    "channel2": {
      "comment": "same structure as channel1"
    }
    "comment": "potentially other channels"
  }
}
```

Note

If no requested channel is found in the service, the response payload doesn’t have an entry for that channel within the `channel_statuses` object.

Description of `channel_statuses` fields for each channel:

| Field | Type | Description |
| --- | --- | --- |
| channel\_status\_code | String | Indicates the status of the channel. |
| last\_committed\_offset\_token | String | Latest committed offset token. |
| database\_name | String | The name of the database that the channel belongs to. |
| schema\_name | String | The name of the schema that the channel belongs to. |
| pipe\_name | String | The name of the pipe that the channel belongs to. |
| channel\_name | String | The name of the channel. |
| rows\_inserted | int | A count of all rows inserted into this channel. |
| rows\_parsed | int | A count of all rows parsed, but not necessarily inserted into this channel. |
| rows\_errors | int | A count of all rows that experienced errors when inserted into this channel and were therefore rejected. |
| last\_error\_offset\_upper\_bound | String | The upper bound for an ingestion error. The error will be located at or before this committed offset token. |
| last\_error\_message | String | A human readable message corresponding to the latest error code for that channel, with sensitive customer data redacted. |
| last\_error\_timestamp | timestamp\_utc | Timestamp at the time when the last error occurred. |
| snowflake\_avg\_processing\_latency\_ms | int | Average end-to-end processing time for this channel. |

Expand

Show lessSee more

## Error response structure

The Snowpipe Streaming REST APIs return a JSON payload for error responses. This structure provides actionable information for both automated error handling and human analysis.

The response payload has the following structure:

Copy code

```
{
  "code": "...",
  "message": "..."
}
```

### Response fields

| Field | Type | Description |
| --- | --- | --- |
| Code | String | A stable, programmatic error code. This value can be used for automated error handling and logging. For example, an application’s logic can check for a specific code to trigger a predefined action. |
| Message | String | A human-readable message that describes the error. This message is subject to change and shouldn’t be used for automated parsing. |

Expand

Show lessSee more

### Example

The following example shows an error response you might receive:

Copy code

```
{
  "code": "STALE_CONTINUATION_TOKEN_SEQUENCER",
  "message": "Channel sequencer in the continuation token is stale. Please reopen the channel"
}
```

This example shows the response for an attempt to use a continuation token with a stale channel sequencer. The code provides a clear, machine-readable identifier for the error, and the message offers a helpful, descriptive text for a user.
