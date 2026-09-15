# Go Snowflake Driver release notes for 2024

This article contains the release notes for the Go Snowflake Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Go Snowflake Driver updates.

See [Go Snowflake Driver](/developer-guide/golang/go-driver) for documentation.

## Version 1.12.1 (December 05, 2024)

### New features and updates

- Introduced `golangci-lint` and fixed some errors found by this tool.
- Introduced S3 logging configuration.
- Changed `RaisePutGetError` to be `true` by default.
- Implemented the `DriverContext` interface to reduce the time for creating new connections and to use context when connections are created using `db.Conn(ctx)`.
- Introduced the `disableOCSPChecks` configuration option, which replaces `insecureMode`. Deprecated `insecureMode`.
- Provided the ability to set custom OCSP cache server URLs.

### Bug fixes

- Propagated context to authentication processes.
- HTTP headers used to communicate with Azure are now case insensitive.
- Use correct length of IV for GCM encryption.

## Version 1.12.0 (October 30, 2024)

### New features and updates

- Added support for Golang 1.23, dropped support for Golang 1.20.
- Added support for configuring connections using `connections.toml`.
- Bumped logrus to version 1.9.3.
- Extended logging when querying with `QueryArrowStream`.

### Bug fixes

- Fixed an issue with duplicate requestIDs and requestGUIDs on session renewal.
- Fixed the proxy configuration for Azure.
- Removed the `*.okta.com` native Okta authenticator URL restriction.
- Fixed the `filestransfer` example that failed with an incorrect file path.

## Version 1.11.2 (October 03, 2024)

### New features and updates

- Changed `GetFileToStream` to an exported member of the `SnowflakeFileTransferOptions` `struct` so GET operations can read files using streams to reduce memory usage.

### Bug fixes

- Fixed error handling while getting accelerated configurations from S3 bucket.

## Version 1.11.1 (August 29, 2024)

### New features and updates

- Added support for downloading files into an in-memory stream when using the GET command.
- Added context propagation to `snowflakeFileTransferAgent` to support cancel for file transfer process.

### Bug fixes

- Removed context propagation in `snowflakeConn`, which is used only for dialing purposes.
- Prevent panic in the `arrayToString` method for Golang slices.
- Prevent panic in the `decodeChunk` method when a download is canceled.

## Version 1.11.0 (July 31, 2024)

### New features and updates

- Added support for Go 1.22 and dropped support for Go 1.19.
- Adjusted driver configuration for China deployments.
- Added the ability to bind structured types in queries.
- Added support for using a passcode with MFA token caching enabled.
- Added support for setting session variables in DSN.
- Provided a simpler solution to define structured objects using tags.
- Provided a mechanism to wrap each goroutine in custom code.

### Bug fixes

- Fixed an issue with handling session expiration when executing long-running queries.
- Fixed an issue OCSP failures when OCSP cache is disabled.
- Fixed an issue with reading arrow batches that contained integer columns whose size is smaller than 64b.

## Version 1.10.1 (May 29, 2024)

### New features and updates

- Upgraded AWS SDK dependencies.
- Added automatic password masking in logs.
- Added the `DisableSamlURLCheck` parameter to disable SAML URL checks.
- Added support for binding semi-structured types.
- Decreased the number of retries to OCSP.
- Added the `OcspMaxRetryCount` and `OcspResponderTimeout` variables to define the OCSP maximum retry count and timeout, respectively.

### Bug fixes

- Fixed an issue with exposed objects in Arrow batches mode.
- Fixed an issue with extracting account names when using key-pair authentication.

## Version 1.10.0 (May 8, 2024)

### New features and updates

- Implemented support for structured types (structured objects, arrays, and maps).
- Added an option to skip driver registration during startup.
- Added the `SECURITY.md` file so customers can review Snowflake’s security policy.
- Added the ability to set custom logger fields.

### Bug fixes

- Fixed an issue with closing the error channel twice when using async mode.
- Fixed a race condition when accessing temporal credentials.

## Version 1.9.0 (March 28, 2024)

### New features and updates

- Upgraded to Arrow version 15.
- Added support for the `WithHigherPrecision` context in Arrow batches mode.
- Added date and time converter from the Snowflake format to the Golang format.
- Added a context that replaces UTF-8 characters in Arrow responses.

### Bug fixes

- Fixed an issue with handling unavailable Amazon S3 accelerated configuration when transferring files.
- Fixed an issue with dividing big numbers in Arrow mode.
- Fixed a data racing issue during logging initialization.
- Fixed an issue where results were not downloaded when the first batch was missing in a response.
- Fixed an issue with the backoff retry period for non-authenticated requests.
- Fixed an issue where zombie DBus processes were not terminated when a program ended.

## Version 1.8.0 (February 21, 2024)

### New features and updates

- Added support for multiple SAML integrations.
- Added support for second, millisecond, and microsecond precision for arrow batch timestamps.

### Bug fixes

- Fixed an issue with `WithFetchResultByID` by checking for the `queryInProgressAsyncCode` response code when fetching results.
- Fixed an issue where OKTA authentication failed when receiving an HTTP 429 error.
- Fixed an issue where the driver incorrectly returned an error for empty arrow batches.

## Version 1.7.2 (January 17, 2024)

### New features and updates

- Added support for Go version 1.21.
- Upgraded the `arrow` library to version v14.
- Updated the `jose2go` and `crypto` dependencies.
- Allow clients to set the QUERY\_TAG parameter via context.
- Standardized using the same `http.Transport` for all cloud providers.
- Added an example showing how to insert data into VARIANT and OBJECT columns using variable binding.

### Bug fixes

- Fixed the following issues relating to error handling:

  - The driver now propagates errors when file upload errors occur.
  - The driver now propagates errors that occur during chunk downloading.
  - The driver does not start chunk downloading when an error occurs with the first chunk download.
- Fixed an issue where the driver tried to read an empty chunk, when `arrow_batches` mode is enabled.
- Removed retry attempts for HTTP 400 and 405 statuses.
- Fixed an issue with unexpected errors that occurred during S3 HEAD calls.
- Fixed the GET example in documentation.
