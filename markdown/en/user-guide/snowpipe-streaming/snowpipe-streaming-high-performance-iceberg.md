# Snowpipe Streaming high-performance architecture with Apache Iceberg™ tables

Snowpipe Streaming with high-performance architecture supports ingesting data into Snowflake-managed [Apache Iceberg](/user-guide/tables-iceberg) tables, including both Iceberg v2 and [Iceberg v3](/user-guide/tables-iceberg-v3-specification-support) tables. This enables near real-time streaming of data into Iceberg tables with all the performance benefits of the high-performance architecture.

Note

The classic architecture supports Iceberg v2 tables only. If you need Iceberg v3 support, you must use the high-performance architecture. For more information about Iceberg support in the classic architecture, see [Snowpipe Streaming Classic with Apache Iceberg™ tables](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-iceberg).

## How it works

Snowpipe Streaming ingests data through the PIPE object into your target Iceberg table. Snowflake creates Iceberg-compatible Apache Parquet data files with corresponding Iceberg metadata, and the data is made available as a Snowflake-managed Iceberg table registered with Snowflake as the Iceberg catalog.

The Iceberg table can use either of the following storage options:

- [Snowflake storage](/user-guide/tables-iceberg-internal-storage): Snowflake stores and manages the Iceberg table files for you, so you don’t need to configure or grant access to external cloud storage.
- External cloud storage that you manage. Snowflake connects to your storage location using an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def).

## Get started

This section provides a step-by-step example of how to set up Snowpipe Streaming with high-performance architecture to ingest data into an Iceberg table.

### Step 1: Create an external volume

If you plan to use [Snowflake storage](/user-guide/tables-iceberg-internal-storage), skip this step and continue to Step 2. You don’t need to create an external volume; Snowflake provides the storage.

To use your own cloud storage, create an [external volume](/user-guide/tables-iceberg-configure-external-volume) that specifies a storage location for your Iceberg table data, then grant the streaming role USAGE on the volume:

Copy code

```
GRANT USAGE ON EXTERNAL VOLUME my_external_volume TO ROLE my_streaming_role;
```

### Step 2: Create a Snowflake-managed Iceberg table

Create a [Snowflake-managed Iceberg table](/sql-reference/sql/create-iceberg-table-snowflake) using one of the following examples.

To use [Snowflake storage](/user-guide/tables-iceberg-internal-storage), set `EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'` and omit `BASE_LOCATION`:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
    event_id NUMBER,
    event_type STRING,
    event_data VARIANT,
    event_timestamp TIMESTAMP_NTZ
)
    CATALOG = 'SNOWFLAKE'
    EXTERNAL_VOLUME = 'SNOWFLAKE_MANAGED'
    ICEBERG_VERSION = 3;
```

To use your own external volume, set `EXTERNAL_VOLUME` to the volume you created in Step 1 and provide a `BASE_LOCATION`:

Copy code

```
CREATE OR REPLACE ICEBERG TABLE my_iceberg_table (
    event_id NUMBER,
    event_type STRING,
    event_data VARIANT,
    event_timestamp TIMESTAMP_NTZ
)
    CATALOG = 'SNOWFLAKE'
    EXTERNAL_VOLUME = 'my_external_volume'
    BASE_LOCATION = 'my_iceberg_table/'
    ICEBERG_VERSION = 3;
```

Note

If you omit the `ICEBERG_VERSION` parameter, the table defaults to Iceberg v2.

### Step 3: Create a pipe for ingestion

Create a pipe that targets the Iceberg table. You can use the default pipe (automatically created) or create a custom pipe:

Copy code

```
-- Option 1: Use the default pipe.
-- The default pipe is automatically created when you open a channel
-- against the table using the SDK. The default pipe name follows the
-- convention: <TABLE_NAME>-STREAMING (for example, MY_ICEBERG_TABLE-STREAMING).

-- Option 2: Create a custom pipe with explicit column mapping.
CREATE OR REPLACE PIPE my_iceberg_pipe AS
    COPY INTO my_iceberg_table (event_id, event_type, event_data, event_timestamp)
    FROM (SELECT $1:event_id, $1:event_type, $1:event_data, $1:event_timestamp);
```

### Step 4: Stream data using the SDK

Configure the SDK to stream data into your Iceberg table through the pipe. Use the same SDK setup as described in [Tutorial: Get started with Snowpipe Streaming high-performance architecture SDK](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-getting-started), specifying your Iceberg table’s pipe in the client configuration.

## Supported Iceberg versions

The high-performance architecture supports both Iceberg v2 and [Iceberg v3](/user-guide/tables-iceberg-v3-specification-support) tables.

The [classic architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-iceberg) supports only Iceberg v2 tables.

## Supported data types

The Snowflake Ingest SDK supports most of the Iceberg data types that Snowflake currently supports. For more information, see [Data types for Apache Iceberg™ tables](/user-guide/tables-iceberg-data-types).

The SDK also supports ingestion into the three [structured data types](/sql-reference/data-types-structured): Structured ARRAY, Structured OBJECT, and Structured MAP.

## Usage notes

- Snowpipe Streaming only supports **Snowflake as the Iceberg catalog**. Externally managed Iceberg tables that use external catalogs (such as AWS Glue or Hive Metastore) aren’t supported. However, you can [sync your Snowflake-managed Iceberg tables with Snowflake Open Catalog](/user-guide/tables-iceberg-open-catalog-sync).
- For Iceberg tables that use an external volume, Snowflake connects to your storage location using the [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def), and you’re responsible for [data storage](/user-guide/tables-iceberg#label-tables-iceberg-data-storage). For Iceberg tables that use [Snowflake storage](/user-guide/tables-iceberg-internal-storage), Snowflake stores and manages the table files.
- The Iceberg-compatible Parquet files are created based on the [STORAGE\_SERIALIZATION\_POLICY](/sql-reference/parameters#label-storage-serialization-policy) specified on the Iceberg table.
- Server-side schema evolution is supported for Iceberg tables that have `ENABLE_SCHEMA_EVOLUTION = TRUE`, the same way it’s supported for standard tables. For more information, see [Table schema evolution](/user-guide/data-load-schema-evolution).

## Limitations

The following limitations apply to Snowpipe Streaming with high-performance architecture and Iceberg tables:

- Partitioned Iceberg tables aren’t supported.
- Length-constrained VARCHAR columns (for example, `VARCHAR(100)`) aren’t supported for Iceberg tables. Use STRING or VARCHAR without a length constraint.

The [Snowpipe Streaming high-performance architecture limitations](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-limitations#label-snowpipe-streaming-high-performance-limitations) and [Iceberg tables limitations](/user-guide/tables-iceberg#label-tables-iceberg-considerations) also apply.
