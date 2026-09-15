# Snowflake Connector for Kafka release notes for 2024

This article contains the release notes for the Snowflake Connector for Kafka, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Kafka updates.

See [Snowflake Connector for Kafka](/user-guide/kafka-connector/index) for documentation.

## Version 3.0.0 (December 10, 2024)

### New features and updates

- With this release, the Snowflake Connector for Kafka can ingest data into a Snowflake-managed [Apache Iceberg™ table](/user-guide/tables-iceberg). For more information, see [Using the Snowflake Connector for Kafka with Apache Iceberg™ tables](/user-guide/kafka-connector/classic/iceberg).

### Bug fixes

- Fixed dependency vulnerabilities.

## Version 2.5.0 (October 31, 2024)

### New features and updates

- Upgraded the Snowflake Ingest Java SDK to version 2.3.
- Closing channels in parallel is now enabled by default. This improves the speed of restarting the connector.

### Bug fixes

- Fixed logging issues.

## Version 2.4.1 (September 19, 2024)

### New features and updates

- Upgraded the Snowflake Ingest Java SDK to version 2.2.2.

### Bug fixes

- Fixed issues with schematization.

## Version 2.4.0 (August 15, 2024)

### New features and updates

- Upgraded the Snowflake Ingest Java SDK to version 2.2.0, which contains a critical fix for potential issues when `change_tracking` is enabled for streams and dynamic tables.
- Upgraded the Snowflake JDBC driver from version 3.14.5 to version 3.18.0.
- Improved the logging experience in various components for improved troubleshooting experience.
- Improved the channel reopening logic.

Note

For all Snowpipe Streaming usage, Snowflake recommends using the Kafka connector version 2.4.0 or later.

### Bug fixes

- Updated dependencies with known vulnerabilities.

## Version 2.3.0 (July 10, 2024)

### New features and updates

- Added support to close Snowpipe Streaming channels in parallel, which significantly reduces time for rebalancing.
- Added a new `SnowflakeConnectorPushTime` property in the metadata that represents the time when the message was pushed by the connector.

### Bug fixes

- Updated dependencies with known vulnerabilities.

## Version 2.2.2 (May 07, 2024)

### Bug fixes

- Fixed an issue where the staged files are not cleaned up properly.

## Version 2.2.1 (March 15, 2024)

### New features and updates

- Added offset verification logic to make sure there is no missing or duplicate data.
- Added client provider overridden map for Snowpipe Streaming. The map uses comma-separated key value pairs as input.
- Upgraded to the following versions:
  - JDBC version to 3.14.5.
  - kafka connect-api version to 3.7.0.
  - jackson-core and jackson-databind to 2.16.1
  - commons-compress to 1.26.0

### Bug fixes

- Cleaned up streaming ingest threads when `SinkTask stop ()` is called.

## Version 2.2.0 (February 06, 2024)

### BCR (Behavior Change Release) changes

- Preserved the old data type that goes into an ARRAY column for schematization.

### New features and updates

- Added support for AVRO logical types.
- Implemented changes to prevent potential data duplication because of a new channel name format.
- Implemented changes to preserve the old data type that goes into an ARRAY column for schematization.
- Implemented changes to make schema evolution add columns idempotent.
- Enabled the Ingest SDK `MAX_CLIENT_LAG` configuration in Kafka connector.

### Bug fixes

- Fixed schema evolution cases that could cause non-exactly once delivery.
- Fixed issues with generating and building Java library.
- Fixed an issue that the Kafka offset is not reset correctly.
