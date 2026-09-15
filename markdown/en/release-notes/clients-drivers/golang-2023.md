# Go Snowflake Driver release notes for 2023

This article contains the release notes for the Go Snowflake Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Go Snowflake Driver updates.

See [Go Snowflake Driver](/developer-guide/golang/go-driver) for documentation.

## Version 1.7.1 (December 07, 2023)

### New features and updates

- Upgraded the `crypto` and `net` libraries.
- Added support to run S3 clients on the new AWS SDK library while preserving compatibility with the previous library version.
- Improved the OCSP response cache performance by changing the key from an `x509.Certificate` to a string.
- Implemented separate retry strategies for authentication endpoints and other types of endpoints.

### Bug fixes

- The driver now retries `getQueryStatus` queries that fail when backend errors occur.
- The driver now provides a `QueryId` for failed queries invoked by statements.

## Version 1.7.0 (November 15, 2023)

### BCR (Behavior Change Release) change

- Changed the default PUT behavior for the `OVERWRITE` parameter. Previously, the default was `OVERWRITE=true`. With this change, the default is `OVERWRITE=false`, so you must explicitly enable overwrite PUT behavior.

### New features and updates

- Added the `IncludeRetryReason` configuration parameter to enable or disable whether to send the HTTP status code for query retry requests.
- Added a new `WithOriginalTimestamp` context to allow arrow batches to use nanosecond precision in the full year range supported by Snowflake.
- Added support for setting the log level in a configuration file.
- Improved performance by caching parsed OCSP responses.

### Bug fixes

- Fixed an issue related to concurrent access to an HTAP query context cache.
- Fixed an issue related to improper connection handling in the asynchronous demo example.

## Version 1.6.25 (September 26, 2023)

### New features and updates

- Added support for hybrid transactional and analytical processing.
- Implemented the `GetQueryId` function on the statement level, which allows you to get the last query id on this statement.
- Added the retry reason to query requests.
- Updated the `cacert` bundle used for SSL connections.

### Bug fixes

- Fixed an issue with OCSP fallback requests in PrivateLink environments.
- Removed QueryID from the snowflakeConn struct to address some race conditions when the same connection was reused among threads.
- Fixed an issue where the driver showed an error for successful queries.

## Version 1.6.24 (August 22, 2023)

### New features and updates

- Added support specifying a temporary directory for encryption and compression.
- Improved performance by checking location data once per query instead of for each row and column separately.
- Added support specifying a custom context when fetching an arrow batch.

### Bug fixes

- None.

## Version 1.6.23 (July 25, 2023)

### New features and updates

- Added support for binding named parameters.
- Added support for `sql.Null` types for query bind mapping.
- Allowed setting separate authentication timeout for key pair authentication.
- Added sample application providing example of distributed fetch feature.
- Added external browser timeout.
- Provided easier way to configure Snowflake connection (see `/cmd` examples).
- Upgraded arrow library to better handle 32bit systems.
- Provided sample app demonstrating how to use Arrow batches.

### Bug fixes

- Fixed error messages from race conditions with multiple threads.
- Fixed an issue with retry async requests if a query is still in progress.
- Added null checks before accessing connection config during chunk downloading.
- Fixed an issue with handling JSON result sets returned from server when driver expected Arrow.
- Recreate new JWT token (with new expiration) on key pair authentication retry.
- Added timeout for authentication in external browser to prevent infinite waiting when user closed browser tab.
- Fixed driver panic when temporary file system is in readonly mode.
- Fixed an authentication issue by requiring username and password only for authentication modes in which it is required.

## Version 1.6.22 (June 14, 2023)

### New features and updates

- Added a sample app, `async.go,` within the cmd folder to demonstrate how to use asynchronous API calls within
  the Golang driver.
- Added a sample app, `multistatement.go`, within the cmd folder to demonstrate how to send multiple statements
  within the Golang driver.

### Bug fixes

- Fixed an issue where `Commit()` and `Rollback()` did not use the same context set
  in `BeginTx()`, which could cause locks to occur.

## Version 1.6.21 (May 23, 2023)

### New features and updates

- Added to check to see whether the context deadline was exceeded when retrying in the `snowflakeChunkDownloader`.
- Upgraded the arrow library to version v12.
- Added the ability to expose the direct arrow IPC streams from the Snowflake Go driver.
- Included the Arrow Database Connectivity (ADBC) version 0.4.0 release, which uses the updated Snowflake library
  to provide a Snowflake ADBC driver that can be consumed by anything that access a C interface, in
  addition to the native Go bindings.

### Bug fixes

- Fixed an int64 overflow issue with large or small `datetime` values.

## Version 1.6.20 (April 18, 2023)

### New features and updates

- Added support for Okta Identity Engine (OIE) logins.
- Improved memory usage by cleaning up the first data chunk before reading the next data chunk.

### Bug fixes

- Fixed the interface conversion panic when the context has been cancelled while monitoring an asynchronous
  query and passing a cancelable context to `WithFetchResultByID`.
- Updated log messages for OCSP file lock errors.
- Now logs an error when a single file upload fails.

## Version 1.6.19 (March 21, 2023)

### New features and updates

- Added support for Go version 1.20 and dropped support for Go version 1.18.
- Migrated from azure-storage-blob-go v0.15.0 to azure-sdk-for-go v1.0.0.
- The Go driver now supports retrying on an HTTP 429 error code.
- Upgraded the Arrow library to version v10.

### Bug fixes

- Fixed an issue where the Go driver failed to validate an SSO URL before executing it. Now, the driver uses the URLValidator and URLEncoder utilities to validate and encode the URL.
- Fixed the Pointer datatype `*time.Time` returns `<nil>` value from version GO Driver 1.6.13.

## Version 1.6.18 (February 22, 2023)

### New features and updates

- None.

### Bug fixes

- Added support for disabling connection caching for multi-factor authentication and external browsers, which
  are enabled by default, but setting either of the following configuration parameters.
  - `ClientStoreTemporaryCredential=ConfigBoolFalse`
  - `ClientRequestMfaToken=ConfigBoolFalse`

## Version 1.6.17 (January 26, 2023)

### New features and updates

- Updated `golang.org/x/net/http2` to version 0.5.0.

### Bug fixes

- Improved performance of multi-statement queries by skipping queries that return no update count.
- Fixed connection caching for MFA and external browser authentication.
- Added a mutex lock to the configuration parameters map to avoid concurrent read/writes when using multiple go routines.
