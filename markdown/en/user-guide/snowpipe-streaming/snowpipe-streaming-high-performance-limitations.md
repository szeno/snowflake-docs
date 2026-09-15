# Limitations and considerations for Snowpipe Streaming with high-performance architecture

This document outlines the known limitations and key considerations for Snowpipe Streaming with high-performance architecture.

## General and service-level limitations

- The service is available in all Amazon Web Services (AWS), Microsoft Azure, and Google Cloud regions except for government-specific regions.

## Table limits

- Maximum throughput: A table can achieve an aggregate throughput of 10 GB/s uncompressed.

## Pipe limits

- Channels per pipe: By default, a single pipe can have up to 2,000 active channels. Contact Snowflake Support if you require more channels for your use case.
- Pipes for Snowpipe Streaming: The maximum number of PIPE objects configured for Snowpipe Streaming is limited to 10,000 per account and 10 per table. If you require more pipes, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Channel limits

Each channel has the following soft limits. If your application requires higher throughput per channel, contact Snowflake Support to discuss increasing these limits.

- Channel throughput: 20 MB/s (uncompressed).
- REST payload limit: 4 MB per request (observed size). To ingest more data per request, use compression (Gzip or ZSTD). This lets you fit a larger uncompressed data volume into the 4 MB limit.
- Request rate: 10 requests per second (RPS).

## Ingestion and data-specific limitations

- The ON\_ERROR option in Snowpipe Streaming with high-performance architecture only supports CONTINUE. To capture
  failed rows for debugging and recovery, turn on error logging on your target table. For more information, see [Error logging in Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables).
- Sudden spikes in data throughput might experience brief increases in end-to-end latency because the service is elastically scaling to support the new throughput level.
- Partitioned Iceberg tables aren’t supported. Non-partitioned Snowflake-managed Iceberg tables are supported. For more information, see [Snowpipe Streaming high-performance architecture with Apache Iceberg™ tables](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-iceberg).
- Time functions (CURRENT\_DATE, CURRENT\_TIME, CURRENT\_TIMESTAMP, GETDATE, LOCALTIME, LOCALTIMESTAMP, SYSDATE, and SYSTIMESTAMP) are evaluated when the pipe’s copy statement is compiled rather than when each row is committed, so rows ingested hours apart can share the same value. This applies both to functions called in the copy statement and to column DEFAULT values. To record when each row was committed, enable [row timestamps](/user-guide/data-engineering/row-timestamps) on the target table and query `METADATA$ROW_LAST_COMMIT_TIME`.

## SDK and architectural limitations

- Supported architectures (Rust Core): ARM64 Mac, Windows, ARM64-Linux, and x86\_64-Linux.
- Linux requirements: If you use the SDK on Linux, your system must have glibc version 2.26 or later.
- Timezone: The SDK automatically uses UTC, and this setting can’t be changed by the user.
- Authentication: The SDK supports RSA key-pair (JWT), OAuth, and personal access token (PAT) authentication. OAuth and PAT require SDK version 1.4.0 or later.
- Snowpark Container Services (SPCS): SDK version 1.5.0 and later supports running inside SPCS services with workload-identity authentication. For more information, see [Run the Snowpipe Streaming SDK in Snowpark Container Services](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-spcs).
