# Ingest Java SDK release notes for 2024

This article contains the release notes for the Ingest Java SDK, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Ingest Java SDK updates.

## Version 3.0.1 (December 4, 2024)

### Bug fixes

- Fixed an issue with schema evolution for structured data type.
- Fixed an issue with loading files greater than 16 MB using the MD5 hash.
- Upgraded io.netty to fix a security vulnerability.

## Version 3.0.0 (November 12, 2024)

### New features and updates

- With this release, [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview) can ingest data into Snowflake-managed [Apache Iceberg](/user-guide/tables-iceberg) tables.

### Bug fixes

- Fixed dependency issues and error messages in the SDK.

## Version 2.3.0 (October 11, 2024)

### BCR (Behavior Change Release) changes

- Beginning with release 2.3.0, numeric values preserve their format. The numeric values will not be converted to and from scientific notation.

### New features and updates

- Made updates to support a new table format.

### Bug fixes

- Fixed vulnerable dependencies.
- Upgraded Hadoop to fix vulnerability issues.
- Removed unnecessary dependencies to reduce JAR size.

## Version 2.2.2 (September 12, 2024)

### Bug fixes

- Fixed a critical issue by updating the location for the file name in metadata.

## Version 2.2.1 (September 05, 2024)

### New features and updates

- Added `ExternalVolumeManager` to support multiple stages for a new table format.
- Upgraded dependency versions.
- Updated parameters to support a new table format.

## Version 2.2.0 (August 09, 2024)

### New features and updates

- Improved code logic to support different storage volumes.

### Bug fixes

- Fixed a critical issue that could potentially cause conflicts when `change_tracking` is enabled for streams and dynamic tables.

Note

For all Snowpipe Streaming usage, Snowflake recommends using the Ingest Java SDK version 2.2.0 or later.

## Version 2.1.2 (July 29, 2024)

### New features and updates

- Improved `InsertRows` performance.
- Added or improved various logs for better observability.
- Fine-tuned channel and chunk sizes.

### Bug fixes

- Fixed an issue with failover across deployments.

## Version 2.1.1 (May 09, 2024)

### New features and updates

- Returned more detailed error messages for the `INVALID_CHANNEL` error.
- Added support for external OAuth 2.0.

### Bug fixes

- Upgraded several dependencies, including vulnerability fixes.
- Fixed an issue where HTTP connections are leaked due to error responses.
- Relaxed the file size constraints to deal with issues where longer client flush lags produce larger files.

## Version 2.1.0 (February 28, 2024)

### BCR (Behavior Change Release) changes

- Set Zstandard as the default compression algorithm.

### New features and updates

- Allowed clients to drop channels.
- Upgraded JDBC to 3.14.5.
- Implemented a change for sending the start and end offset tokens for a channel.
- Implemented a change for sending the column ordinal data to the server side for cross-checking table schema changes.
- Added support to pass verification logic for a user-defined offset token as part of channel creation.

### Bug fixes

- Fixed an overflow issue that caused silent data issue.

## Version 2.0.5 (January 22, 2024)

### New features and updates

- Added an optional offset token parameter for `openChannel`.
- Added support for specifying compression algorithm to be used for BDEC Parquet files.
- Updated to support customized URL and added Snowflake account name in request header.
- Implemented a change to send `spansMixedTables` flag in blob registration requests.
- Deprecated BUFFER\_FLUSH\_INTERVAL\_IN\_MILLIS parameter, instead use the MAX\_CLIENT\_LAG parameter.
- Implemented the refresh of downscoped GCS tokens.

### Bug fixes

- Reverted one change that updated public API for internal use case.
- Fixed the end-to-end JAR test so it can run on all cloud platforms.
