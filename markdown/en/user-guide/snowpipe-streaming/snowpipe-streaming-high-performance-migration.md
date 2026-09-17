# Snowpipe Streaming migration guide

This guide describes how to migrate from the classic Snowpipe Java SDK to the high-performance Snowpipe Streaming SDK. The architectural changes and API updates discussed here also apply to migrations to the Python and Node.js SDKs, because the high-performance architecture is available in all three languages. Although the code examples in this document are in Java, the core migration principles remain consistent across languages.

This guide uses Named Channels because they preserve the ordered, offset-token recovery model used by Snowpipe Streaming Classic applications. For new workloads that don’t require these guarantees, evaluate [Elastic Channels](/user-guide/snowpipe-streaming/snowpipe-streaming-elastic-channels-overview) separately.

## Key architectural changes

The following table summarizes the most important architectural changes in the high-performance Snowpipe Streaming SDK. For a detailed comparison of the SDKs, see [Comparison between Named Channel and classic SDKs](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-comparison).

| Area | Classic (snowflake-ingest-java) | High-Performance (snowpipe-streaming SDK) |
| --- | --- | --- |
| Entry point | Data is ingested directly into tables. | Data is ingested through PIPE objects, which support transforms and schema enforcement. |
| SDK / Core | Java SDK only. | SDK in multiple languages (Java, Python, and Node.js) with a shared Rust core. |
| API names | `insertRow`/`insertRows`, `openChannel(request)` | `appendRow`/`appendRows`, `openChannel(channelName, offsetToken)` |
| Error handling | Client-side validation is performed. | Server-side validation with richer error feedback is provided. |
| Backpressure handling | Puts the thread to sleep, leading to a blocked/unresponsive state. | Returns an error, allowing the caller to implement a backoff/retry strategy. |
| Client-to-table mapping | A single client object could open channels to any table. | A single client object is now exclusively tied to one pipe object. |
| Billing | Based on compute and client count. | Flat, per-GB ingested. |
| Schema / transforms | Managed on the client side. | Managed on the server side through the PIPE definition. |

Expand

Show lessSee more

## Migration process

To migrate your application to the high-performance SDK, complete the following high-level steps:

1. For each target table, [create a PIPE](/sql-reference/sql/create-pipe).

   Copy code

   ```
   CREATE PIPE my_pipe
   AS COPY INTO my_table
     FROM TABLE (DATA_SOURCE(TYPE => 'STREAMING'))
     MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
     [CLUSTER_AT_INGEST_TIME = TRUE];
   ```
2. Stop ingestion from all classic clients.
3. For each channel in the classic client, confirm the last committed offsets. To retrieve these offsets, use the `getLatestCommittedOffsetTokens()` method from the classic SDK. Verify that these offsets align with your client-side records.
4. Update your application code.

   - Switch your project dependencies to the high-performance SDK (Java, Python, or Node.js).
   - Update your API calls as detailed in the following  section.
   - Initialize one client per table/PIPE by using the last committed offset from Snowflake.
5. After your new client is configured and stable, resume ingestion.

## API and configuration changes

The following changes must be made to your API calls and configuration settings during migration:

### Client initialization

- Classic: `builder(name)`
- High-performance: `builder(name, db, schema, pipeName)`

### Channels

- Classic: `openChannel(OpenChannelRequest)`
- High-performance: `openChannel(channelName, offsetToken)` returns both channel and status

### Ingestion methods

- Classic: `insertRow/insertRows(...)`
- High-performance: `appendRow/appendRows(...)`

### Offset tracking

- The classic SDK’s `getLatestCommittedOffsetTokens(channels)` method offers limited visibility and lacks error context.
- The high-performance SDK still supports `getLatestCommittedOffsetTokens(...)`, but for robust monitoring, we recommend that you use `getChannelStatuses(...)`. This method performs the following tasks:
  - Confirms that offsets are advancing as expected.
  - Returns error counts and detailed error information per channel.
  - Enables proactive monitoring and troubleshooting of your data pipelines.

### Handling semi-structured data

When migrating to the high-performance SDK, review how your application provides data for ARRAY and VARIANT columns to avoid data being stored as literal strings.

#### Behavioral change

Passing a serialized string literal — for example, “[1, 2, 3]” — to an ARRAY column in v2 results in a single-element array containing that string literal. To maintain the classic architecture behavior, select one of the following options:

#### Option 1: Pass native objects (Recommended)

Update your client application to deserialize JSON strings into native objects before calling *appendRow*.

- **Java**: Use `java.util.List` for arrays and `java.util.Map` for objects.
- **Python**: Use native `list` and `dict` types.
- **Node.js**: Use native `Array` and `Object` types.

**Benefit**: Compatible with the default pipe and automatic schema evolution.

#### Option 2: Pipe-side transformation

Explicitly define the *Pipe* object with transformation logic by using the `PARSE_JSON` function.

**Example SQL**

Copy code

```
CREATE PIPE my_pipe AS
COPY INTO my_table (my_array_col)
FROM (SELECT PARSE_JSON($1:my_array_col) FROM TABLE(DATA_SOURCE(TYPE => 'STREAMING')));
```

Note

This method is incompatible with the default pipe and the automatic schema evolution features.
