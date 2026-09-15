# Node.js Driver release notes for 2024

This article contains the release notes for the Node.js Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Node.js Driver updates.

See [Node.js Driver](/developer-guide/node-js/nodejs-driver) for documentation.

## Version 2.0.1 (December 13, 2024)

### New features and updates

- None.

### Bug fixes

- Fixed an issue related to missing proxy ports during configuration processing.

## Version 2.0.0 (December 11, 2024)

### BCR (Behavior Change Release) changes

Beginning with version 2.0.0, the Node.js driver introduced the following breaking changes:

- Removed support for the Node.js library 14, 16, and 17 versions in the Node.js driver. Node.js no longer officially supports versions lower than 18 of its library. Snowflake encourages everyone using Node.js versions lower than 18 to upgrade to Node.js version 22 (LTS).
- Changed the name of the `insecureConnect` configuration flag that allows skipping OCSP verification to `disableOCSPChecks`.
- The Node.js driver considers all types and methods described in the typings file to be part of the driver’s public API; other components are treated as internal.

### New features and updates

- Extended logging at the transport layer.
- Improved URL data sanitation.
- Added support for GCS region-specific endpoints.
- Implemented GCM encryption algorithms.
- Bumped axios to version 1.7.7.
- Replaced aws-sdk with smithy in version 3.2.5.

### Bug fixes

- Fixed nonempty logs when the log level is set to `OFF`.

## Version 1.15.0 (November 07, 2024)

### New features and updates

- Added support for Node.js version 22.
- Added checks for the `PROXY*` (such as `proxyHost`) and the `noProxy` environment variables when creating an httpAgent.
- Added support for the `describeOnly` configuration parameter.
- Improved logging at the connection layer.

### Bug fixes

- Fixed an issue where the driver did not handle the `rejected` state of the `Promise` object in the `heartbeat` method.

## Version 1.14.0 (October 02, 2024)

### New features and updates

- Added support for structured types.
- Extended logs for the configuration layer.

### Bug fixes

- Fixed a callback parameter heartbeat issue.
- Fixed SSO token authentication.
- Extended log levels and added new methods in the driver types definition.

## Version 1.13.1 (September 04, 2024)

### New features and updates

- None.

### Bug fixes

- Fixed a compilation error with the types file.

## Version 1.13.0 (September 03, 2024)

### New features and updates

- Added support for the `passcode` and `passcodeInPassword` parameters in the MFA authentication process.

### Bug fixes

- Fixed an issue that exposed query IDs to users on failed requests.
- Added `axios` error and response sanitization.
- Fixed error handling issues in the `getResultsFromQueryId` method.
- Fixed an issue related to re-authentication for JWT and SAML authentication.
- Fixed an issue with returned types for `async` methods in the driver types definition.

## Version 1.12.0 (August 05, 2024)

### New features and updates

- Added SSO and MFA token caching to the Node.js driver.
- Picked a top-level domain for Snowflake hosts.
- Added support for reading the connection information from a file.
- Added the `cwd` (current working directory) parameter to use for GET/PUT execution when it differs from the connector directory.
- Added support for AES 256 encryption/decryption.

### Bug fixes

- Fixed a bug related to reusing the jwt token for login retries.
- Fixed azure-storage-blob version compatibility with node version 14.
- Fixed an issue that caused enum type errors when the `isolatedModule` option is set.
- Fixed an issue with the type definitions, by adding the missing `cancel` method and setting the `complete` field in `StatementOption` as optional in driver types.
- Fixed an issue with regex expressions in account name validation.

## Version 1.11.0 (May 28, 2024)

### New features and updates

- Added the `disableSamlURLCheck` parameter to disable SAML URL checks.
- Added the `representNullAsStringNull` configuration parameter to specify how the `fetchAsString` method returns null values. When disabled, `fetchAsString` returns null values as `NULL` instead of as the string, “NULL”.
- Released Snowflake’s official `d.ts` type declaration file to support TypeScript users.
- Removed the following unused dependencies:
  - agent-base
  - debug
  - extend

### Bug fixes

- Fixed an issue with millisecond precision.
- Fixed an issue with creating paths on Windows when using the PUT command.

## Version 1.10.1 (April 08, 2024)

### New features and updates

- None.

### Bug fixes

- Fixed unhandled promise rejections on keypair authorization.
- Fixed an issue with reading a `timestamp` type with high precision.
- Fixed external browser authentication.
- Fixed an issue with native Okta URL validation.
- Fixed the data format in bulk upload `.csv` files.
- Fixed validation for short account names.
- Bumped axios to version 1.6.8.

## Version 1.10.0 (February 27, 2024)

### New features and updates

- Added support for setting the log level in a logging configuration file.
- Added the `forceGCPUseDownscopedCredential` flag to force sending a custom HTTP request instead of the one from the GCP library. Default: `false`.
- Added proxy support for files operations on AWS S3.
- Updated google-cloud version to 7.7.0.

### Bug fixes

- Fixed an issue where an error was thrown when getting a query status.
- Fixed an issue where OKTA authentication failed when receiving an HTTP 429 error.

## Version 1.9.3 (January 17, 2024)

### New features and updates

- Added the `host` configuration parameter.
- Added support for multiple SAML integrations.
- Added logging for mapping resultset columns.
- Updated the following libraries:
  - axios to version 1.6.5.
  - Removed the `tmp` module.

### Bug fixes

- Fixed an issue with the SESSION\_TOKEN\_EXPIRED error when destroying connections.
