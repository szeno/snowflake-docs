# Snowflake Connector for Spark release notes for 2026

This article contains the release notes for the Snowflake Connector for Spark, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Spark updates.

See [Snowflake Connector for Spark](/user-guide/spark-connector) for documentation.

## Version 3.2.2 (September 1, 2026)

### Bug fixes

- Fixed Parquet writes to Snowflake on Spark 3.5 that failed with a `NoSuchMethodError` because `parquet-avro` 1.15.2 was incompatible with Spark 3.5’s Parquet 1.13.1 runtime. The Spark 3.5 build now pins `parquet-avro` 1.13.1, while Spark 4.0 and later continue to use `parquet-avro` 1.15.2.

## Version 3.2.1 (July 8, 2026)

### Bug fixes

- Restricted the fallback catalog to merge only immutable Spark configuration, so runtime and session settings can no longer override trusted catalog connection options.
- Registered the connector’s sensitive DataSource options with Spark’s log redaction, so they are masked in logs, plan output, and the Spark UI.
- Fixed identifier quoting to escape embedded quote characters.
- Fixed `CREATE STAGE` construction to escape SQL metacharacters in interpolated values.
- Added validation of the OAuth token request URL’s scheme and host.

## Version 3.2.0 (June 23, 2026)

### Behavior changes

- The Snowflake Connector for Spark now requires Snowflake JDBC driver version 4.0.2 or later at runtime. If your environment pins a specific Snowflake JDBC driver version, upgrade it to 4.0.2 or later. The AWS SDK and Azure Storage SDK are now bundled (relocated) inside the connector JAR and are no longer pulled in as transitive dependencies.

### New features

- Added support for Apache Spark 4.0 and 4.1 (Scala 2.13, JDK 17).
- Added a Scala 2.13 cross-build for Spark 3.5.
- Added `VariantType` support for reading and writing Snowflake `VARIANT` columns under Spark 4.x, including the Parquet write path.

## Version 3.1.9 (May 13, 2026)

### New features

- Added support for OAuth client credentials authentication.

### Bug fixes

- Prevented silent data loss that could occur when speculative tasks are killed during a stage upload.
- Added missing `TimestampNTZType` support in the Parquet write path.

## Version 3.1.8 (March 13, 2026)

### New features

- None

### Bug fixes

- Fixed the `UnsupportedOperationException: Unexpected type: NullType` error that was raised when writing DataFrames with structured columns (StructType) containing all null values via the Parquet write path.
