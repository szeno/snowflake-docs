# Snowflake Connector for Kafka release notes for 2025

This article contains the release notes for the Snowflake Connector for Kafka, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Kafka updates.

See [Snowflake Connector for Kafka](/user-guide/kafka-connector/index) for documentation.

## Version 3.5.0 (Dec 15, 2025)

### New features

- The connector now automatically handles client redirect during failover, thus eliminating the need to manually restart the connector after a primary deployment change.
- Added automatic failover support for Snowpipe Streaming.
- Added granular logging for schema evolution to improve troubleshooting.
- Upgraded Snowflake Ingest SDK to version 4.4.0.

## Version 3.4.0 (November 5, 2025)

### Behavior changes

- Changed default value of `enable.streaming.channel.offset.migration` property to `false`.
  This property was used only when the Snowflake Streaming channel was first used after migrating from
  Kafka Connector version 2.1.0 or 2.1.1: it enabled migration of offsets from channels created
  by those versions (which included the connector name in the channel name:
  `[connectorName]_[topic]_[partition]`) to the channel name format used by all other
  versions (`[topic]_[partition]`).

### New features

- Added `snowflake.streaming.channel.name.include.connector.name` property. When set to
  `true`, this includes the connector name in Snowpipe Streaming channel names
  (`[connectorName]_[topic]_[partition]`). Setting this property to `true` requires
  `enable.streaming.channel.offset.migration` to be set to `false`. This allows users
  of Kafka Connector versions 2.1.0 and 2.1.1 to upgrade without data loss.

  Warning

  Users upgrading from versions other than 2.1.0 and 2.1.1 who set
  `snowflake.streaming.channel.name.include.connector.name` to `true` will
  experience data duplication; there is no offset migration logic for other versions.
- Upgraded Snowflake Ingest SDK to version 4.3.2.

### Bug fixes

Not applicable.

## Version 3.3.1 (Oct 23, 2025)

### New features

- Upgraded Snowflake JDBC driver to version 3.26.1.

### Bug fixes

- OAuth URLs now support dots and hyphens.

## Version 3.3.0 (Aug 26, 2025)

### Behavior changes

Not applicable

### New features

- The Snowflake Connector for Kafka now supports `long` type with `timestamp` logical type in Apache Iceberg™ tables.
  For a complete list of support types see [Data types for Apache Iceberg™ tables](/user-guide/tables-iceberg-data-types).

### Bug fixes

Not applicable.

## Version 3.2.4 (Jul 31, 2025)

Internal updates only.

## Version 3.2.3 (Jul 14, 2025)

Internal updates only.

## Version 3.2.2 (Jun 26, 2025)

### Behavior changes

Not applicable

### New features

- Uses Confluent version 7.9.2 packages.

### Bug fixes

Not applicable

## Version 3.2.1 (Jun 2, 2025)

### Behavior changes

Not applicable

### New features

- Uses [JDBC](/release-notes/clients-drivers/jdbc-2025) version 3.24.2.

### Bug fixes

Not applicable

## Version 3.2.0 (Apr 28, 2025)

### Behavior changes

Not applicable

### New features

- Removed support for double buffered version for SNOWPIPE\_STREAMING ingestion type.

  Setting *snowflake.streaming.enable.single.buffer* has no effect.

### Bug fixes

- The connector no longer drops table rows with missing offsets.
- During schema evolution, on schema change, certain single records are no longer dropped.

## Version 3.1.3 (Apr 7, 2025)

### Behavior changes

- Snowpipe Streaming with double buffer is now deprecated. Only single buffer will be supported in future releases.

### New features and improvements

- Updated connector to use Kafka version 3.9.0.
- Updated connector to use slf4j-api version 2.0.17.
- Supports [JDBC](/release-notes/clients-drivers/jdbc-2025) version 3.23.2.

### Bug fixes

- snowflake-jdbc no longer throws NullPointerException in certain situations.

## Version 3.1.2 (Mar 18, 2025)

### Behavior changes

Not applicable

### New features

- Supports using `-Infinity` values in a [floating-point number](/sql-reference/data-types-numeric#label-data-type-float).
- Updated connector to use Confluent version 7.9.0 packages.
- Supports [JDBC](/release-notes/clients-drivers/jdbc-2025) version 3.21.1.

### Bug fixes

Not applicable.

## Version 3.1.1 (Feb 26, 2025)

### Behavior changes

- [max\_client\_lag in Snowpipe Streaming](/user-guide/snowpipe-streaming/snowpipe-streaming-classic-configuration) default value changed from *120s* to *30s*.

### New features

Not applicable

### Bug fixes

Not applicable.

## Version 3.1.0 (Jan 21, 2025)

Important

If the `snowflake.topic2table.map` parameter is configured, Snowflake recommends using this version.
We strongly recommend upgrading the connector if you are on earlier versions 2.x, 1.9.x, and 1.8.x.

### Behavior changes

Not applicable

### New features

- The Snowflake Connector for Kafka now supports external OAuth authentication.
- The Snowflake Connector for Kafka now uses Confluent version 7.8.0.

### Bug fixes

- The connector no longer throws the `IndexOutOfBoundException` when offsets are not continuous during schema evolution.
- For the Snowpipe ingestion method, when the `snowflake.topic2table.map` parameter is configured
  to map multiple topics to a single table, the connector adds the topic’s salt `hashCode` to the stage file prefixes to
  avoid file collision and load data from all specified topics.
