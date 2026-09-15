# Table support and schema

This topic covers the table types, data types, and schema capabilities supported by Snowpipe Streaming.

## Apache Iceberg™ table support

Snowpipe Streaming supports ingestion into Snowflake-managed Apache Iceberg™ tables, including both Iceberg v2 and [Iceberg v3](/user-guide/tables-iceberg-v3-specification-support) tables. For more information, see [Snowpipe Streaming high-performance architecture with Apache Iceberg™ tables](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-iceberg).

## Schema evolution

Snowpipe Streaming supports automatic table schema evolution. When enabled, Snowflake can automatically add new columns that are detected in the incoming stream and drop NOT NULL constraints to accommodate new data patterns. For more information, see [Table schema evolution](/user-guide/data-load-schema-evolution).

Limitations of schema evolution:

- Supported exclusively for standard Snowflake tables. External tables and Apache Iceberg™ tables aren’t supported.
- The precision, scale, or length of existing columns can’t be increased automatically.
- Schema evolution isn’t supported for structured data types. However, new columns that contain structured types are inferred as VARIANT.

## Insert-only operations

The API is currently limited to inserting rows. To modify, delete, or combine data, write the “raw” records to one or more staging tables. Merge, join, or transform the data by using [continuous data pipelines](/user-guide/data-pipelines-intro) to insert modified data into destination reporting tables.

## Supported Java data types

The following table summarizes which Java data types are supported for ingestion into Snowflake columns:

| Snowflake column type | Allowed Java data type |
| --- | --- |
| - CHAR - VARCHAR | - String - primitive data types (int, boolean, char, …) - BigInteger, BigDecimal |
| - BINARY | - byte[] - String (hex-encoded) |
| - NUMBER | - numeric types (BigInteger, BigDecimal, byte, int, double, …) - String |
| - FLOAT | - numeric types (BigInteger, BigDecimal, byte, int, double, …) - String |
| - BOOLEAN | - boolean - numeric types (BigInteger, BigDecimal, byte, int, double, …) - String   See [boolean conversion details](/sql-reference/data-types-logical#label-boolean-conversion). |
| - TIME | - java.time.LocalTime - java.time.OffsetTime - String   - [Integer-stored time](/sql-reference/date-time-input-output#label-date-time-input-output-auto-detection-integer-stored)   - `HH24:MI:SS.FFTZH:TZM` (for example, `20:57:01.123456789+07:00`)   - `HH24:MI:SS.FF` (for example, `20:57:01.123456789`)   - `HH24:MI:SS` (for example, `20:57:01`)   - `HH24:MI` (for example, `20:57`) |
| - DATE | - java.time.LocalDate - java.time.LocalDateTime - java.time.OffsetDateTime - java.time.ZonedDateTime - java.time.Instant - String   - [Integer-stored date](/sql-reference/date-time-input-output#label-date-time-input-output-auto-detection-integer-stored)   - `YYYY-MM-DD` (for example, `2013-04-28`)   - `YYYY-MM-DDTHH24:MI:SS.FFTZH:TZM` (for example, `2013-04-28T20:57:01.123456789+07:00`)   - `YYYY-MM-DDTHH24:MI:SS.FF` (for example, `2013-04-28T20:57:01.123456`)   - `YYYY-MM-DDTHH24:MI:SS` (for example, `2013-04-28T20:57:01`)   - `YYYY-MM-DDTHH24:MI` (for example, `2013-04-28T20:57`)   - `YYYY-MM-DDTHH24:MI:SSTZH:TZM` (for example, `2013-04-28T20:57:01-07:00`)   - `YYYY-MM-DDTHH24:MITZH:TZM` (for example, `2013-04-28T20:57-07:00`) |
| - TIMESTAMP\_NTZ - TIMESTAMP\_LTZ - TIMESTAMP\_TZ | - java.time.LocalDate - java.time.LocalDateTime - java.time.OffsetDateTime - java.time.ZonedDateTime - java.time.Instant - String   - [Integer-stored timestamp](/sql-reference/date-time-input-output#label-date-time-input-output-auto-detection-integer-stored)   - `YYYY-MM-DD` (for example, `2013-04-28`)   - `YYYY-MM-DDTHH24:MI:SS.FFTZH:TZM` (for example, `2013-04-28T20:57:01.123456789+07:00`)   - `YYYY-MM-DDTHH24:MI:SS.FF` (for example, `2013-04-28T20:57:01.123456`)   - `YYYY-MM-DDTHH24:MI:SS` (for example, `2013-04-28T20:57:01`)   - `YYYY-MM-DDTHH24:MI` (for example, `2013-04-28T20:57`)   - `YYYY-MM-DDTHH24:MI:SSTZH:TZM` (for example, `2013-04-28T20:57:01-07:00`)   - `YYYY-MM-DDTHH24:MITZH:TZM` (for example, `2013-04-28T20:57-07:00`) |
| - VARIANT - ARRAY | - String (must be a valid JSON) - primitive data types and their arrays - BigInteger, BigDecimal - java.time.LocalTime - java.time.OffsetTime - java.time.LocalDate - java.time.LocalDateTime - java.time.OffsetDateTime - java.time.ZonedDateTime - java.util.Map<String, T> where T is a valid VARIANT type - T[] where T is a valid VARIANT type - List<T> where T is a valid VARIANT type |
| - OBJECT | - String (must be a valid JSON object) - Map<String, T> where T is a valid variant type |
| - GEOGRAPHY | - Supported |
| - GEOMETRY | - Supported |

Expand

Show lessSee more
