# Node.js Driver release notes for 2023

This article contains the release notes for the Node.js Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Node.js Driver updates.

See [Node.js Driver](/developer-guide/node-js/nodejs-driver) for documentation.

## Version 1.9.2 (December 07, 2023)

### New features and updates

- Enhanced observability for generic and proxy use cases.
- Updated the following libraries:
  - glob to version 9.0.0.
  - https-proxy-agent to version 7.0.2.

### Bug fixes

- None.

## Version 1.9.1 (November 14, 2023)

### New features and updates

- Added support for Node.js version 20.
- Connections are now considered valid if they are in either renewing or connecting state.
- Added support for executing asynchronous queries.
- Added the `retryTimeout`, `sfRetryStartingSleepTime`, and `sfRetryMaxLoginRetries` connection parameters to manage the frequency of retries for unsuccessful connection requests. The default for `retryTimeout` is 300.
- Added `account` parameter validation.
- Updated the following libraries:
  :   - Updated axios version to 1.6.0
      - Updated mocha version to 10.2.0
      - Updated bignumber.js version to 9.1.2
      - Added asn1.js to `peerDependency` and updated @techteamer/ocsp version to 1.0.1

### Bug fixes

- Fixed an issue where `sqlText` was overwritten when specified by a user.
- Fixed an issue with caching all types of HTTPS agents.
- Fixed an issue related to using an axios httpclient for Okta authentication.
- Fixed an issue with external browser SSO authentication with proxy.
- Fixed response handling for Okta authentication.

## Version 1.9.0 (September 28, 2023)

### BCR (Behavior Change Release) Change

- Removed support for the Node.js library version 12 in the Node.js driver. Node.js no longer officially supports version 12 of its library. Snowflake encourages everyone using the Node.js version 12 environment to upgrade to Node.js version 18.

### New features and updates

- Added support for hybrid transactional and analytical processing:

  - Added retry context in retries for query requests.
  - Added query context caching.
- Updated the following libraries:

  - Replaced the `urlib2` library with `axios`.
  - Upgraded `aws-sdk` to version v3.
  - Upgraded `uuid` to version 8.

### Bug fixes

- The default JSON parser now returns the result from a new `Function` object.

## Version 1.8.0 (August 29, 2023)

### New features and updates

- Added support for Node.js version 18.
- Added a new `rowMode` configuration option to specify how to return results sets that contain duplicate column names,
  including as an:

  - `array`
  - `object`
  - `object_with_renamed_duplicate_columns`

  For more information, see [Returning Result Sets that Contain Duplicate Column Names](/developer-guide/node-js/nodejs-driver-consume#label-nodejs-duplicate-column-names).
- Upgraded a minor `urllib` version and deleted the vm2 exclusion.

### Bug fixes

- Fixed an issue where the `moment.js` library incorrectly populated the millisecond position for times in the log messages.
- Fixed an issue with getting files from stages in Windows and Azure environments.
- Fixed an issue where external browser authentication incorrectly required a username and password.

## Version 1.7.0 (July 28, 2023)

### New features and updates

- Added the `connection.isValidAsync()` function to determine whether a connection is up and usable.

### Bug fixes

- Fixed an issue where some stage files were not downloaded correctly during a multi-file download.
- Modified the `fetchAsString` error message to include “Buffer” as an accepted type.
- Fixed a performance issue with stage bindings.
- Fixed issue that where `connection.execute()` did not return a Statement in bind mode.
- Fixed the `connection.heartbeatAsync()` to use the same endpoint as `connection.heartbeat()`
  function is using instead of querying with SELECT 1.

## Version 1.6.23 (June 14, 2023)

### New features and updates

- Added support for initializing the JSON parser and XmlParser with a custom configuration.

### Bug fixes

- Excluded a vulnerable vm2 transitive dependency.
- Added the `browserActionTimeout` connection parameter to fix an issue with authentication in an external browser.
- Fixed an issue with private keys that contained new lines at the end of the key.
- Fixed an issue related to importing a `uuid` library.
- Removed an unused qs dependency.
- Fixed a retry issue in a `LargeResultSet`.
- Replaced the better-eval package with vm.
- Removed requirement for a username for OAuth connections.

## Version 1.6.22 (May 24, 2023)

### New features and updates

- None.

### Bug fixes

- Added the missing bn and `https-proxy-agent` dependencies.
- Fixed an issue where `econnreset` and `etimedout` error codes would not retry the connection.
- Fixed the error message that was returned when calling `connection.execute()` with a requestId failed.
- Fixed the error message that was returned for calling `connect()` failed when using OKTA or an external browser authenticator.
- Fixed the `maskedtxt` variable undefined error.
- Fixed an issue that occurred for multiple connections when using a OAuth authenticator.
- Fixed an issue where calling `connection.execute()` with extra whitespace in `sqltext` caused errors.
- Fixed an issue where retrying a connection failed due to using the wrong value in the sleep timer.

## Version 1.6.21 (April 18, 2023)

### New Features and Updates

- Added support for GCS access token for PUT/GET.
- Added support for Okta Identity Engine (OIE) logins.
- Improved security when parsing JSON strings with the `eval` function.

### Bug Fixes

- Fixed a parsing issue with XML data loaded from VARIANT columns.
- Fixed an issue where the OCSP cache was not refreshed when it expired.
- Fixed an issue where using a full table path on array binding could crash the application.
- To resolve a deprecation warning issue related to the `Buffer()` deprecation, please reinstall snowflake-sdk.
  Reinstalling updates the `formstream` library to the latest version, such as `formstream 1.2.0`, and resolves the issue.

## Version 1.6.20 (March 23, 2023)

### New Features and Updates

- None.

### Bug Fixes

- The Node.js driver now supports retrying on an HTTP 429 error code.
- Fixed an issue where the Node.js driver would not sent OCSP requests through proxies.
- Fixed an issue where errors occurred when the amount of data submitted using array binding exceeded the array
  binding threshold. The driver now produces output for ingest instead of failing the SQL statement.
- Fixed an issue that incorrectly generated “Bind variable ? not set” error messages after upgrading from
  version 1.6.13 to a higher version.

## Version 1.6.19 (February 27, 2023)

### New Features and Updates

- None.

### Bug Fixes

- Fixed an issue where an insert query failed intermittently when trying to insert large amounts of data with
  array binding.

## Version 1.6.18 (January 31, 2023)

### New Features and Updates

- Added the ability to execute a batch of SQL statements (multi-statement support).
- Updated the `jsonwebtoken` library to version 9.0.0.

### Bug Fixes

- Improved performance by sending heartbeat messages instead of select calls to verify endpoint connections.
- Added error details to the log messages for OCSP open failures and changed the log level from info to warning.
- Added a check to verify that the OCSP cache is initialized before setting the cache entry.
