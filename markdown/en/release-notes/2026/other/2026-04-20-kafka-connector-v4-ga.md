# Apr 20, 2026: Snowflake Connector for Kafka version 4.0 (*General availability*)

The Snowflake Connector for Kafka version 4.0 is now generally available. Version 4.0 is a ground-up rewrite
built on Snowflake’s high-performance Snowpipe Streaming architecture, delivering up to
10 GB/s throughput per table with 5 to 10 second end-to-end latency, and exactly-once
and ordered delivery semantics.

Key capabilities in the GA release:

- **Flat, throughput-based pricing** based on the volume of data ingested (GB).
- **Server-side validation and schema evolution** through PIPE objects, reducing connector
  resource usage and aligning with COPY and Snowpipe behavior.
- **In-flight transformations** using COPY command syntax within user-defined PIPE objects.
- **Pre-clustering** during ingestion when the target table has clustering keys defined.
- **Error Tables** for capturing and inspecting invalid records with server-side validation.
- **Dead Letter Queue (DLQ)** support for converter and client-side validation errors.
- **Iceberg table** ingestion (auto-detected, no special configuration required).

Migration and compatibility features for upgrading from version 3.x:

- **Seamless migration** from both Snowpipe mode and Snowpipe Streaming mode without gaps
  or duplicates when configured correctly.
- **Compatibility validator** (`snowflake.streaming.validate.compatibility.with.classic`)
  that checks your configuration at startup and guides you through the required settings.
- **Offset migration** from version 3.x Snowpipe Streaming channels
  (`snowflake.streaming.classic.offset.migration`).
- **Compatibility flags** for table name sanitization, column identifier normalization,
  and schematization to reproduce version 3.x behavior during migration.
- **Downgrade support** back to version 3.x with deduplication guidance using `RECORD_METADATA`.

For more information, see [Snowflake Connector for Kafka](/user-guide/kafka-connector/index). For migration guidance,
see [Migrate from Kafka connector v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4).
