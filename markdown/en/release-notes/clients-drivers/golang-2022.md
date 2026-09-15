# Go Snowflake Driver release notes for 2022

This article contains the release notes for the Go Snowflake Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Go Snowflake Driver updates.

See [Go Snowflake Driver](/developer-guide/golang/go-driver) for documentation.

## Version 1.6.16 (December 14, 2022)

### New features

- Fixed an issue where file decryption was causing a panic.
- Reverted the `go-ieproxy` library back to version 0.0.1.

## Version 1.6.15 (November 16, 2022)

### New features

- Added MultiFactor Authentication mechanism and caching for MFA/Id token.
- Fixed an issue where 405 error is thrown when S3 bucket acceleration is disabled.

## Version 1.6.14 (October 28, 2022)

### New features

- Removed the requirement to provide the original SQL query in addition to the requestId when resubmitting requests.
- Updated mocha to version 10.1.0.

## Version 1.6.14 (September 21, 2022)

### New features

- Removed support for Go 1.7 and added support for Go 1.17.
- Changed the format for float and numeric values when converting arrow types.
- Added the following functions to access data in arrow.Record format directly from queries:

  - `GetArrowBatches()`, which is a blocking call
  - `GetQueryID()`
  - `GetStatus()`
- Updated Go vendors.

## Version 1.6.13 (August 22, 2022)

### New features

- Added an example to show how to use key-pair authentication.
- Added the tracing connection parameter to enable logging in the connection string and DSN.
- Improved logging details for chunk downloads.
- Added support for using interface slice `[]interface{}` to insert NULL values via array binding for
  the time.Time data types.

### Bug fixes

- Fixed the “Failed to decrypt. Check file key and master key” error that occurred when binding large data
  files via array binding.

## Version 1.6.12 (July 29, 2022)

### New features

- Added support for using interface slice `[]interface{}` to insert `NULL` values via array binding.

### Bug fixes

- Fixed an issue where setting `DisableTelemetry` to TRUE did not disable telemetry.
- Fixed an issue with encrypted SAML assertions when authenticating with an external browser.

## Version 1.6.11 (June 23, 2022)

### Bug fixes

- Created a temporary workaround to avoid the “Failed to decrypt. Check file key and master key” error that
  occurred when binding large data files via array binding. Determining the root cause of the issue is currently
  under investigation.

## Version 1.6.10 (May 25, 2022)

### Bug fixes

- Removed redundant calls that impacted performance for `PrepareContext()`.

## Version 1.6.8 (March 15, 2022)

### New features

- Added support for exporting unique universal IDs (UUIDs).

### Bug fixes

- Fixed a default server side error.

## Version 1.6.7 (February 16, 2022)

### Bug fixes

- Fixed an issue where multi-statement queries were missing result IDs.
- Implemented Universally Unique Identifier version 4 (UUIDv4).
- Fixed and issue with `GetQueryStatus`.
- Fixed an issue in PUT Memory Enhancements performance tests.
- Fixed an issue with arrow record result batches.
- Made the port parameter optional.
