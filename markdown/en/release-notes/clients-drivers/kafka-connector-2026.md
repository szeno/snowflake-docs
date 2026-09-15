# Snowflake Connector for Kafka release notes for 2026

This article contains the release notes for the Snowflake Connector for Kafka, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Kafka updates.

See [Snowflake Connector for Kafka](/user-guide/kafka-connector/index) for documentation.

## Version 4.1.0 (Jul 22, 2026)

Note

Apache Iceberg™ table schema evolution isn’t supported when using client-side validation. Server-side
schema evolution is being rolled out and will be fully available within a few weeks of this release.

### New features

- Added OAuth authentication support.
- Added managed Apache Iceberg™ table auto-creation and ingestion through the
  `snowflake.autocreate.table.type` property.
- Added support for recreating the Snowpipe Streaming client when the client becomes invalid.
- Added optional regex group substitution for `snowflake.topic2table.map` through the
  `snowflake.topic2table.map.regex.replacement` property.
- Added typed Kafka record header support through the `snowflake.feature.structured.headers`
  property.
- Improved telemetry and local observability.
- Updated dependencies.

### Bug fixes

- Normalized TIME values that include a UTC offset for compatibility with version 3 of the
  connector.
- Structural validation error messages now include the target table name.
- Fixed detection of whether error logging is enabled on the target table.

## Version 4.0.2 (Jun 25, 2026)

### New features

- Upgraded the Snowpipe Streaming SDK to version 1.6.0.
- Added version attribution for Snowpipe Streaming high-performance traffic.

### Bug fixes

- Recovered an invalid SDK client during offset fetch.
- The connector no longer rewinds unassigned partitions.
- Added validation for decimal precision and scale.
- Removed a misleading warning message.

## Version 4.0.1 (Jun 2, 2026)

Important

Snowflake strongly recommends using this version or newer instead of 4.0.0. Version 4.0.1 contains
a critical fix for an issue introduced in 4.0.0-rc9 that can cause certain rows to be dropped or
missed during ingestion.

### New features

- Upgraded the Snowpipe Streaming SDK to version 1.4.0.
- Updated kafka-clients and other dependencies.

### Bug fixes

- The connector now recreates the streaming client when the SDK reports a pipe failover (HTTP 410).
- Made offset rewinds thread-safe during channel recreation.

## Version 3.5.4 (May 28, 2026)

### Bug fixes

- Updated Apache Kafka to version 3.9.2 and Jackson to version 2.18.6 to address security findings.

## Version 4.0.0 (Apr 17, 2026)

Warning

Snowflake strongly recommends upgrading to version 4.0.1 or newer. Version 4.0.1 contains a
critical fix for an issue introduced in 4.0.0-rc9 that can cause certain rows to be dropped or
missed during ingestion.

### New features

Version 4.0.0 introduces the high-performance Kafka connector built on Snowpipe Streaming. For a
full overview, see
[Apr 20, 2026: Snowflake Connector for Kafka version 4.0 (General availability)](/release-notes/2026/other/2026-04-20-kafka-connector-v4-ga). For migration
guidance, see [Migrate from Kafka connector v3 to v4](/user-guide/kafka-connector/migrate-v3-to-v4).

- Added error table support for high-throughput mode.
- Added migration of offset tokens from Snowpipe Streaming Classic channels to High-Performance
  Architecture channels on startup.
- Added validation for compatibility-mode configuration settings.
- Improved channel usage telemetry, including SDK channel status fields, backpressure retry and
  append-row fallback counts, and schema evolution failure counts.

### Bug fixes

- Fixed `RECORD_CONTENT` serialization.
- Timestamp validation now accepts Integer and Long epoch values.

## Version 3.5.3 (Jan 27, 2026)

### Bug fixes

- Improved performance in schema type resolution for ConnectSchema.

## Version 3.5.2 (Jan 13, 2026)

### Bug fixes

- Fixed security vulnerabilities CVE-2025-58056 and CVE-2025-58057 in Netty dependencies.

## Version 3.5.1 (Jan 8, 2026)

### New features

- Upgraded Snowflake Ingest SDK to version 4.4.1.

### Bug fixes

- Fixed a `NullPointerException` in `SnowflakeSinkTask#precommit()`.
