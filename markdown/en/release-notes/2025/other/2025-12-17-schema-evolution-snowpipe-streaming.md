# Dec 17, 2025: Schema evolution support for Snowpipe Streaming with high-performance architecture

Snowflake announces support for automatic table schema evolution within the Snowpipe Streaming high-performance architecture. This feature lets your streaming pipelines seamlessly adapt to schema drift in near real-time, which eliminates the need for manual DDL intervention when new data attributes are introduced at the source.

To enable this feature, set `ENABLE_SCHEMA_EVOLUTION = TRUE` on your target table.

Key Features:

- Automatic column addition: New fields detected in the incoming stream are automatically added to the target table.
- Constraint management: Automatically drops NOT NULL constraints if incoming records are missing specific values.
- Seamless ingestion: Reduces pipeline failures caused by schema mismatches, ensuring continuous data availability.

Limitations:

- Table type: Support is limited to standard (native) Snowflake tables. External tables and Iceberg tables aren’t supported.
- Column modifications: Automatic column widening — increasing the precision, scale, or text length — isn’t supported.
- Data types: Schema evolution isn’t currently supported for structured types, which are structured OBJECT, ARRAY, or MAP columns. However, new columns that contain structured types are inferred as VARIANT, which enables JSON objects and arrays to be supported.

For more information, see:

- [Table schema evolution](/user-guide/data-load-schema-evolution)
- [Snowpipe Streaming with high-performance architecture](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-overview)
