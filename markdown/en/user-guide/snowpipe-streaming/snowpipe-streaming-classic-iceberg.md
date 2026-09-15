# Snowpipe Streaming Classic with Apache Iceberg™ tables

With Snowflake Ingest SDK versions 3.0.0 and later, Snowpipe Streaming can ingest data into Snowflake-managed [Apache Iceberg](/user-guide/tables-iceberg) tables. The Snowpipe Streaming Ingest Java SDK supports loading into both standard Snowflake tables (non-Iceberg) and Iceberg tables.

> ![Snowpipe Streaming with Iceberg tables](/static/images/data-load-snowpipe-streaming-iceberg.png)

Data sent through the Snowpipe Streaming API ingests rows through one or more channels, which are automatically flushed according to the specified `MAX_CLIENT_LAG`.

The `MAX_CLIENT_LAG` property controls the latency of streaming ingestion:

- For standard Snowflake tables (non-Iceberg), the default `MAX_CLIENT_LAG` is 1 second.
- For Iceberg tables, the default `MAX_CLIENT_LAG` is 30 seconds.

Snowflake connects to your storage location using an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def), and Snowpipe Streaming flushes the data to create Iceberg-compatible Parquet data files with corresponding Iceberg metadata. These Parquet data and metadata files are uploaded to your configured external cloud storage location and made available as Snowflake-managed Iceberg tables registered with Snowflake as the Iceberg catalog.

## Configurations

Create your [Snowflake-managed Iceberg table with your configured external volume](/sql-reference/sql/create-iceberg-table-snowflake) and specify the Iceberg table name in your open [channel](/user-guide/snowpipe-streaming/snowpipe-streaming-channels#label-replication-snowpipe-channels) request.

To enable Snowpipe Streaming with the Snowflake-managed Iceberg table, you need to set the following property `ENABLE_ICEBERG_STREAMING=true` in the `profile.json` file.

## Supported data types

- The Snowflake Ingest SDK supports most of the Iceberg data types, the same as what Snowflake currently supports. For more information, see [Data types for Apache Iceberg™ tables](/user-guide/tables-iceberg-data-types).
- The Snowflake Ingest SDK supports ingestion into the three [structured data types](/sql-reference/data-types-structured): Structured ARRAY, Structured OBJECT, Structured MAP.

## Usage notes

- The default `MAX_CLIENT_LAG` for streaming to Snowflake-managed Iceberg tables is 30 seconds to ensure optimized Parquet files. You can set the property to a lower value, but we recommend *not* doing this unless there is a significantly high throughput.
- The Ingest SDK supports automatic serverless compaction of small Parquet files asynchronously.
- The same client application cannot be used for Iceberg and non-Iceberg tables simultaneously.
- Snowflake-managed Iceberg tables do not support client-side encryption.
- The Iceberg compatible Parquet files are created based on the [STORAGE\_SERIALIZATION\_POLICY](/sql-reference/parameters#label-storage-serialization-policy) specified on the Iceberg table.
- Snowpipe Streaming only supports Snowflake as the Iceberg catalog, but it also supports [syncing with Snowflake Open Catalog](/user-guide/tables-iceberg-open-catalog-sync).
- Snowflake connects to your storage location using an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def). You are responsible for [data storage](/user-guide/tables-iceberg#label-tables-iceberg-data-storage) for Iceberg tables.
- Only Iceberg v2 tables are supported. [Iceberg v3 tables](/user-guide/tables-iceberg-v3-specification-support) aren’t supported. To use Snowpipe Streaming with Iceberg v3 tables, you must use
  [Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-iceberg).

## Limitations

The [Snowpipe Streaming limitations](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-limitations#label-snowpipe-streaming-limitations) and [Iceberg tables limitations](/user-guide/tables-iceberg#label-tables-iceberg-considerations) also apply to Snowpipe Streaming with Iceberg tables.
