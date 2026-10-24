# Validation and error handling

This topic describes how the Snowflake Connector for Kafka validates data and handles errors during ingestion.

## Validation modes

The connector supports two validation modes, controlled by the `snowflake.validation` configuration property.

### Server-side validation (default)

Copy code

```
snowflake.validation=server_side
```

With server-side validation, data is sent to Snowflake without client-side type checking.
The Snowflake backend performs validation and schema evolution, aligned with the behavior of
COPY and Snowpipe.

- Invalid records are captured in the [Snowflake Error Table](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-error-handling) associated with the target table.
- The DLQ isn’t used for ingestion validation errors in this mode. Use Error Tables instead.
  However, records that fail to be deserialized by the Kafka converters (before reaching Snowflake)
  are still routed to the DLQ if configured.
- Delivers maximum throughput by offloading validation from the connector.
- Supports both default pipe and user-defined pipe modes.

Important

With server-side validation, the connector infers column types after serializing each record to JSON. As a result:

- Schema registry information about numerical precision might be lost.
- Binary data results in [VARCHAR](/sql-reference/data-types-text#varchar) columns being created, with the data ingested as base64-encoded strings.

To preserve declared types from a schema registry, use client-side validation (`snowflake.validation=client_side`), or pre-create the table columns with the intended types before ingestion.

**When to use server-side validation:**

- You want maximum throughput.
- You can manage error tables in Snowflake.
- You’re using user-defined pipes for in-flight transformations.

### Client-side validation

Copy code

```
snowflake.validation=client_side
```

With client-side validation, the connector validates data types and schema compatibility before
sending rows to Snowflake.

- Invalid records are handled according to the `errors.tolerance` setting (see below).
- Schema evolution DDL is executed by the connector when new fields are detected.
- Supports Dead Letter Queue (DLQ) for routing invalid records.
- Only works with the default pipe (`{tableName}-STREAMING`). If a user-created pipe
  exists and client-side validation is enabled, the connector fails with `ERROR_5030`.

Note

Client-side schema evolution isn’t supported for [Apache Iceberg tables](/user-guide/tables-iceberg). To ingest into Iceberg tables, use server-side validation (`snowflake.validation=server_side`, the default). Because server-side validation infers column types from values rather than from a schema registry, pre-create the Iceberg table columns with the intended types to avoid type downgrades.

**When to use client-side validation:**

- You need a Dead Letter Queue for error handling.
- You’re migrating from v3 and want familiar behavior.
- You need the connector to control validation.

## Error handling

### Error tolerance

The `errors.tolerance` property controls how the connector responds to errors:

`errors.tolerance=none` (default)
:   The connector task fails on the first error. If a DLQ is configured, the failing record is
    still sent to the DLQ before the task aborts.

`errors.tolerance=all`
:   The connector continues ingesting data. Invalid records are routed to the DLQ (if configured)
    or silently dropped.

    Warning

    Setting `errors.tolerance=all` without configuring a DLQ topic causes invalid records to be
    silently dropped. This is an unsafe configuration that can cause data loss.

### Dead Letter Queue (DLQ)

To configure a DLQ:

Copy code

```
errors.deadletterqueue.topic.name=my_topic_dlq
errors.log.enable=true
```

The following records are routed to the DLQ (if configured):

- **Converter errors** (both validation modes): Records that fail to be deserialized by the
  Kafka converters are sent to the DLQ regardless of the validation mode. This applies with
  both `errors.tolerance=none` (record pushed to DLQ, then task fails) and
  `errors.tolerance=all` (record pushed to DLQ, task continues).
- **Client-side validation errors**: Records that fail client-side data conversion or schema
  validation are sent to the DLQ when `snowflake.validation=client_side`.

Records that fail Snowflake server-side ingestion aren’t routed to the DLQ. Use
[Error Tables](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-error-handling)
instead.

Note

The connector provides **at most once** delivery for records encountering validation errors.
This means a record might not reach the DLQ under certain failure conditions.

### Error tables (server-side validation)

When using `snowflake.validation=server_side`, records that fail server-side ingestion
(type mismatches, constraint violations) are logged in the Error Table for inspection and replay.

Note

Tables that are auto-created by the connector have Error Tables enabled by default.

For more information about Error Tables and error handling with Snowpipe Streaming, see
[Error handling in Snowpipe Streaming high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-error-handling).

## Channel status inspection (server-side validation)

When using server-side validation, the connector inspects the Snowpipe Streaming channel status
before committing Kafka offsets. If the channel reports an increasing `rows_error_count`:

- With `errors.tolerance=none`: The connector raises a fatal error (`ERROR_5030`) and the task fails.
- With `errors.tolerance=all`: The connector continues, logging the error count. Records after the
  invalid row can still be ingested. If Error Tables are enabled, the invalid records are stored there.

With client-side validation, the connector detects invalid records before sending them to Snowflake.
Invalid records either cause an immediate task failure (`errors.tolerance=none`) or are routed to
the DLQ (`errors.tolerance=all`).

To investigate broken records with server-side validation, review the channel history and use the
gap-finding technique described in [Detect and recover from errors using metadata offsets](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-best-practices#label-detect-and-recover-from-errors-using-metadata-offsets).
Kafka offset information needed for this technique is available in the `RECORD_METADATA` column.
