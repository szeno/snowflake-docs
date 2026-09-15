# Limitations and considerations for Snowpipe Streaming with classic architecture

For Snowpipe Streaming classic, be aware of the following limitations:

- Snowpipe Streaming classic doesn’t support the increased maximum size limits for database objects – 128 MB for VARCHAR, VARIANT, ARRAY, and OBJECT, and 64 MB for BINARY, GEOGRAPHY, and GEOMETRY — that are part of the 2025\_03 behavior change bundle.
- Fail-safe doesn’t support tables that contain data ingested by Snowpipe Streaming classic. For such tables, you can’t use fail-safe for recovery because fail-safe operations on these tables fail completely.
- Snowpipe Streaming only supports using 256-bit AES keys for data encryption.
- If [Automatic Clustering](/user-guide/tables-auto-reclustering) is also enabled on the same table that Snowpipe Streaming is inserting into, compute costs for file migration might be reduced. For more information, see [Best practices for Snowpipe Streaming with classic architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-recommendation).
- The following objects or types aren’t supported or have limitations:

  - GEOGRAPHY and GEOMETRY data types
  - Columns with collations
  - TEMPORARY tables
  - Transient Iceberg tables that use [Snowflake storage](/user-guide/tables-iceberg-internal-storage)
  - Structured data types (like OBJECT, MAP, ARRAY) are only supported for ingestion to iceberg tables.
- The total number of channels per table can’t exceed 10,000. We recommend reusing channels when you need them. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) if you need to open more than 10,000 channels per table.
