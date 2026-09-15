# Ingest Java SDK release notes for 2026

This article contains the release notes for the Ingest Java SDK, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Ingest Java SDK updates.

## Version 4.4.5 (August 31, 2026)

### Bug fixes

- Fixed a missing-class error (`FileInputFormat`) that occurred when Parquet read-back verification was enabled with the shaded SDK jar.
- Parquet read-back verification now reports decode failures as an SDK exception instead of a raw Parquet exception, and retries a failed compression check up to three times.

## Version 4.4.4 (August 25, 2026)

### New features and updates

- Added optional Parquet read-back verification. After each file is written and before it is uploaded, the SDK can decompress and re-read the file to catch compression corruption on the client. This check is off by default. To enable it, set `enable_parquet_readback_verification` to `true` in the client profile. Enabling the check increases end-to-end flush time by about 7%.

## Version 4.4.3 (April 29, 2026)

### New features and updates

- The SDK no longer ships Snowflake JDBC as a runtime dependency. Ingestion APIs and behavior are unchanged. Applications that also use JDBC should declare their own JDBC dependency.

### Bug fixes

- Security update: Removed unused Snowflake JDBC runtime dependencies and excluded vulnerable transitive libraries.

## Version 4.4.2 (January 12, 2026)

### Bug fixes

- Security update: Updated core networking libraries to resolve a known vulnerability in the netty-codec-http component.
- System stability: Refreshed several internal dependencies to ensure compatibility and improve overall application reliability.

## Version 4.4.1 (January 06, 2026)

### Bug fixes

- Fixed an issue where ingesting repeated fields (arrays) containing multiple null entries would cause a validation error. The ingestion process now correctly handles these structures, ensuring data flows smoothly without unnecessary failures.
