# Ingest Java SDK release notes for 2025

This article contains the release notes for the Ingest Java SDK, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Ingest Java SDK updates.

## Version 4.4.0 (November 19, 2025)

### New features and updates

- Data ingestion reliability update: To prevent failed data ingestion after system infrastructure changes, Snowflake updated the client to be more responsive to deployment mismatches. If the client detects that the primary deployment URL, storage location, or encryption key has changed, it now automatically closes the connection. This immediately forces you to recreate your client, ensuring that you use the correct, updated deployment credentials and location, thereby guaranteeing successful and reliable data ingestion.

### Bug fixes

- Security: Upgraded the Bouncy Castle FIPS (bc-fips) dependency to v2.1.1 to resolve potential security vulnerabilities.

## Version 4.3.2 (November 03, 2025)

### Bug fixes

- Fixed an issue that blocked Iceberg table ingestion when the external volume encryption is set to `NONE`.

## Version 4.3.1 (October 08, 2025)

### New features and updates

- Enhanced cloud security: Snowpipe Streaming now fully supports server-side encryption with Amazon Web Services (AWS) Key Management Service (SSE-KMS) configured on your external AWS S3 and Google Cloud Storage volumes. This enhancement ensures that data uploaded during ingestion uses your required, higher-grade KMS encryption policy, moving beyond the previously hardcoded default encryption.

### Bug fixes

- Fixed vulnerable dependencies and cleaned up internal dependency workarounds.

## Version 4.3.0 (August 21, 2025)

### Bug fixes

- Fixed vulnerable dependencies.

## Version 4.2.0 (August 18, 2025)

### New features and updates

- Improved the reliability of streaming ingest into Iceberg tables, ensuring that your data is consistently uploaded to the correct location.
- Improved how the SDK manages table keys, which ensures that our system stays in sync and helps maintain the stability and security of your tables.
- Improved system stability for high-volume data by allowing connections to retry for up to five minutes, preventing immediate closures.

## Version 4.1.0 (June 11, 2025)

### BCR (Behavior Change Release) changes

- Beginning with release 4.1.0, the Ingest Java SDK includes a behavior change to JSON handling to improve data integrity and performance. See the following list for details:
  - Added robust validation to detect and prevent duplicate JSON object fields, including those with trailing null terminators.
  - All JSON keys and values are now strictly enforced to be valid UTF-8, which improves data integrity and compatibility.
  - Optimized the JSON serialization process to directly convert objects into JSON strings, bypassing an intermediate conversion step. This results in improved performance and reduced memory usage.

## Version 4.0.1 (June 06, 2025)

### New features and updates

- Upgraded the JDBC version to 3.24.2.

## Version 4.0.0 (April 14, 2025)

### BCR (Behavior Change Release) changes

- Beginning with release 4.0.0, the Ingest Java SDK now uses the Snowflake JDBC thin JAR instead of the fat JAR.

### New features and updates

- Updated dependencies and imports for Snowflake JDBC thin JAR.
- Removed unnecessary dependencies.
- Enhanced Channel Invalidation Handling. The `channel` object now automatically invalidates itself upon receiving a response from the server indicating an invalid channel state. This improvement enhances error handling and resource management within the SDK.

## Version 3.1.2 (March 17, 2025)

### Bug fixes

- Fixed issues with the filename mismatch for Iceberg ingestion.

## Version 3.1.1 (February 27, 2025)

### New features and updates

- Made updates to silence the exception log in the JDBC driver.

### Bug fixes

- Fixed issues with the Jenkins job to push artifacts to Maven.
- Fixed the proxy settings for the OAuth HTTP client.
- Fixed a Java formatter script and its dependencies.

## Version 3.1.0 (February 24, 2025)

### BCR (Behavior Change Release) changes

- Beginning with release 3.1.0, any duplicate keys in variant columns result in client-side errors with the `INVALID_VALUE_ROW` error code.

### New features and updates

- Upgraded the JDBC version to 3.22.0.
- Upgraded the Netty version to 4.1.118.
