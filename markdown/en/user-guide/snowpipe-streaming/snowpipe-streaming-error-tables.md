# Error logging in Snowpipe Streaming with high-performance architecture

Error logging for Snowpipe Streaming builds on Snowflake’s [DML error logging](/user-guide/data-load-overview#label-data-load-overview-dml-error-logging)
feature to provide a robust way to manage and recover from data ingestion errors. This feature prevents silent data loss
and increases visibility into faulty data rows. When error logging is turned on, error-free data continues to load into your
target table, while rows that fail processing are automatically routed to a dedicated error table for review and recovery.

Important

The data stored in error tables is the original payload sent to the API or SDK before any pipe transformations
are applied. Even if your pipe drops or transforms fields, the full original payload is persisted in the error table.

## Overview

When using the Snowpipe Streaming high-performance architecture, data processing happens server-side in Snowflake.
The high-performance architecture implicitly operates in `ON_ERROR = CONTINUE` mode, meaning valid rows are ingested while
problematic rows are skipped.

### Error handling options

You can monitor and handle ingestion errors in the following ways:

**Without error tables:**

- Use [getChannelStatus()](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-error-handling)
  to monitor aggregated error counts, last error message, and last error timestamp.
- Query the [SNOWPIPE\_STREAMING\_CHANNEL\_HISTORY](/sql-reference/account-usage/snowpipe_streaming_channel_history)
  view for historical error trends and patterns.

These methods tell you *that* errors occurred and *how many*, but not *which rows* failed or their payloads.

**With error tables:**

- Rows that fail processing are automatically captured in a dedicated error table.
- Each error row includes the full original payload and detailed error metadata.
- You can query, analyze, and reprocess failed rows using standard SQL.

Error tables complete the picture by showing you exactly which rows failed and why, enabling full debugging and recovery.

## Turn on error logging

To turn on error logging for Snowpipe Streaming, set the `ERROR_LOGGING` property on the target table.
For complete details on turning on and configuring error logging, see
[Configure DML error logging for a table](/user-guide/data-load-overview#label-data-load-overview-dml-error-logging).

Copy code

```
-- For a new table:
CREATE TABLE my_streaming_table (...) ERROR_LOGGING = TRUE;

-- For an existing table:
ALTER TABLE my_streaming_table SET ERROR_LOGGING = TRUE;
```

When error logging is turned on, the same error table captures errors from both DML statements and Snowpipe Streaming
ingestion workloads.

## Query error tables

To query the error table for a base table, use the `ERROR_TABLE` table function. For complete details on
error table schema, access control, and supported operations, see
[Error logging and error tables](/user-guide/data-load-overview#label-data-load-overview-dml-error-logging).

Copy code

```
SELECT * FROM ERROR_TABLE(my_streaming_table) ORDER BY timestamp;
```

The result contains a row for every erroneous row in the ingestion stream.

## Snowpipe Streaming error fields

Snowpipe Streaming errors are stored in the same
[error table columns](/user-guide/data-load-overview#label-data-load-overview-dml-error-logging) as DML errors (`timestamp`,
`query_id`, `error_code`, `error_metadata`, `error_data`). The `error_metadata` and `error_data`
objects include additional fields for Snowpipe Streaming, described in the following sections.

### Identify Snowpipe Streaming errors

The `error_metadata:service` field is populated with `snowpipe_streaming` for errors from Snowpipe Streaming.
Use this field to filter errors by source:

Copy code

```
SELECT * FROM ERROR_TABLE(my_streaming_table)
WHERE error_metadata:service = 'snowpipe_streaming';
```

### Error metadata details

For Snowpipe Streaming errors, the `error_metadata:details` object contains the following additional fields:

| Field | Description |
| --- | --- |
| `pipe_name` | Name of the pipe used to ingest the erroneous row. |
| `channel_name` | Name of the channel used to ingest the erroneous row. |
| `offset_token_lower_bound` | Lower bound offset token containing the erroneous row. The row appears in the payload at this offset token or later. Requires SDK version 1.4.0 or later. |
| `offset_token_upper_bound` | Upper bound offset token containing the erroneous row. The row appears in the payload with this offset token or earlier. |
| `error_data_truncated` | Indicates whether the raw payload was truncated to fit into the error table (maximum 128 MB). |
| `error_data_content_type` | Indicates the type of content stored in the `error_data` column. See [Error data content types](#label-ssv2-error-data-content-types). |

Expand

Show lessSee more

### Error data format

For Snowpipe Streaming errors, the `error_data:$1` field contains the raw payload representing the erroneous row.

If the payload contains invalid UTF-8 characters, the raw payload is stored as a base64-encoded binary string.

### Error data content types

The `error_data_content_type` field indicates the type of error encountered and suggests remediation steps.

#### json

The erroneous row is a syntactically valid JSON string, but a logical error occurred while ingesting the data
into the target table.

Common logical errors include:

- **Missing non-nullable columns**: A required column with a NOT NULL constraint was not provided in the payload.
- **Type conversion errors**: The JSON data type can’t be cast to the target column type. For example, a string
  value `"abc"` can’t be converted to a NUMBER column.
- **Transformation errors**: An error occurred while evaluating a pipe transformation expression, such as
  division by zero.

To resolve, inspect the error message in `error_metadata:error_message` and the column name in
`error_metadata:error_source` that caused the ingestion error. Parse the payload with
`PARSE_JSON(error_data:$1)`, correct the data, and reinsert it into the target table.

#### json-invalid

A syntactically invalid JSON object was ingested.

To resolve, inspect the error message in `error_metadata:error_message`, which contains details about
the syntax error. Correct the payload stored in `error_data:$1`, and reinsert it into the target table.

#### binary-base64

Invalid UTF-8 data was ingested. The error payload is stored in the error table as a base64-encoded binary string.

This error type typically indicates a format mismatch or encoding error in the upstream data source.

To resolve, examine the data source and the data formats and encodings it produces. Decode the payload stored
in `error_data:$1` with the [BASE64\_DECODE\_STRING](/sql-reference/functions/base64_decode_string)
function to inspect the raw bytes and identify incorrect UTF-8 sequences.

## Error recovery workflow

The following example demonstrates how to query errors, analyze them, and reinsert corrected data.

### Query recent errors

Copy code

```
SELECT
    timestamp,
    error_code,
    error_metadata:error_message::STRING AS error_message,
    error_metadata:details:channel_name::STRING AS channel,
    error_metadata:details:pipe_name::STRING AS pipe,
    error_metadata:details:error_data_content_type::STRING AS content_type,
    error_data:"$1"::STRING AS raw_payload
FROM ERROR_TABLE(my_streaming_table)
WHERE error_metadata:service = 'snowpipe_streaming'
  AND timestamp >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
ORDER BY timestamp DESC;
```

### Analyze error distribution

Copy code

```
SELECT
    error_code,
    error_metadata:error_message::STRING AS error_message,
    COUNT(*) AS error_count
FROM ERROR_TABLE(my_streaming_table)
WHERE error_metadata:service = 'snowpipe_streaming'
  AND timestamp >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
GROUP BY 1, 2
ORDER BY error_count DESC;
```

### Fix and reinsert recoverable errors

For errors with valid JSON payloads, you can parse, correct, and reinsert the data:

Copy code

```
INSERT INTO my_streaming_table (col1, col2, col3)
SELECT
    TRY_CAST(PARSE_JSON(error_data:"$1"):col1 AS NUMBER),
    PARSE_JSON(error_data:"$1"):col2::STRING,
    TRY_CAST(PARSE_JSON(error_data:"$1"):col3 AS TIMESTAMP)
FROM ERROR_TABLE(my_streaming_table)
WHERE error_metadata:service = 'snowpipe_streaming'
  AND error_metadata:details:error_data_content_type = 'json'
  AND timestamp >= DATEADD(hour, -24, CURRENT_TIMESTAMP());
```

After successfully reprocessing errors, you can truncate the error table:

Copy code

```
TRUNCATE ERROR_TABLE(my_streaming_table);
```

## Billing

Snowpipe Streaming ingestion is billed at the standard Snowpipe Streaming rate. Turning on error logging
doesn’t change your ingestion costs. There are no additional ingestion charges for routing failed rows to the
error table.

Snowflake charges for data stored in the error table at the standard storage rate, the same as any other table.
The error table stores the raw payload and error metadata for each failed row.

For more information about Snowpipe Streaming costs, see
[Snowpipe Streaming high-performance architecture: Understand your costs](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-cost).

## Limitations

- Error tables capture errors that occur during server-side data processing (parsing and transformation).
  Errors from other stages (SDK validation, API failures, and other server-side asynchronous errors) aren’t captured in error tables.
  Monitor server-side asynchronous errors using [getChannelStatus()](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-error-handling).
- A high failure rate of incoming rows can increase processing latency due to overhead of storing error information.
- Payloads larger than 128 MB are truncated. The `error_data_truncated` field indicates when truncation occurred.
- Error tables are available only for the Snowpipe Streaming high-performance architecture. For the classic
  architecture, error handling is managed client-side through the SDK.
