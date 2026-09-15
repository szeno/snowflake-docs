# Snowflake Connector for Kafka release notes for 2023

This article contains the release notes for the Snowflake Connector for Kafka, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Kafka updates.

See [Snowflake Connector for Kafka](/user-guide/kafka-connector/index) for documentation.

## Version 2.1.2 (December 04, 2023)

### New features and updates

- Enabled Java Management Extensions (JMX) metrics for Snowpipe Streaming.
- Enabled tombstone ingestion for Snowpipe Streaming.
- Enabled Snowflake OAuth for Kafka connector with Snowpipe Streaming.
- Enabled schematization columns with special or reserved keywords.

### Bug fixes

- Fixed an issue that the one-client configuration option is not enabled by default. The one-client configuration option `enable.streaming.client.optimization` is now `TRUE` by default.
- Fixed an issue with channel naming.

## Version 2.0.1 (August 25, 2023)

### New features and updates

- Improved performance for schematization permission checks when rebalancing.

### Bug fixes

- Fixed a bug that caused missing data in tables due to issues with internal cache clearing during rebalancing.

## Version 2.0.0 (July 31, 2023)

### New features and updates

- Snowpipe Streaming with Kafka Connector is now Generally Available.

### Bug fixes

- None.

## Version 1.9.4 (July 13, 2023)

### New features and updates

- One client configuration:

  - Introduced the `enable.streaming.client.optimization` option, which is enabled by default.
  - With this client optimization, only one client is created for multiple topic partitions per Kafka connector. This feature can reduce client runtime and lower migration cost by creating larger files.
  - Note that in a high throughput scenario (for example, 50 MB/s per connector), we recommend that you disable this property if you see an increase in latency or costs.
- Permissions and security:

  - Unified Snowflake role and user for Snowpipe Streaming for table creation and insertion.
  - Upgraded guava dependency to 32.0.1.
  - Upgraded Snowpipe Streaming SDK dependency to 2.0.1.

### Bug fixes

- Fixed a wrong result issue that offsets are skipped when schematization is enabled.
- Snowpipe Streaming Channels are not closed on rebalance.

## Version 1.9.3 (May 22, 2023)

### New features and updates

- Added the ability to use one Streaming Ingest client (Default to false).
- Started using the MDC context logger.
- Upgraded to the following versions:
  - Ingest SDK version 1.1.4
  - JDBC version 3.13.30

### Bug fixes

- Fixed an issue related to using the GET command when using the downscoped token on GCP.
- Fixed Snowpipe-based KC’s commit offset behavior.
