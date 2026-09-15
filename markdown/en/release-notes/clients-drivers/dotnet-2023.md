# .NET Driver release notes for 2023

This article contains the release notes for the .NET Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for .NET Driver updates.

See [.NET Driver](/developer-guide/dotnet/dotnet-driver) for documentation.

## Version 2.1.5 (December 18, 2023)

### New features and updates

- None

### Bug fixes

- Fixed an issue with enabling certificate revocation checks.

## Version 2.1.4 (December 05, 2023)

### New features and updates

- Added documentation on how to enable Arrow format.

### Bug fixes

- Implemented the validation of the account name format in connection parameters.
- Added synchronization of accessing query context cache.

## Version 2.1.3 (November 15, 2023)

### New features and updates

- Added support for managing the frequency of retries for unsuccessful connection requests:

  - Added the `RETRY_TIMEOUT` parameter with a default value of 300 seconds.
  - Updated how the driver uses the `CONNECTION_TIMEOUT` and `maxHttpRetries` connection parameters and changed the default value of `CONNECTION_TIMEOUT` to 300 seconds.
- Arrow format is now available as a [preview feature](/release-notes/preview-features) (will be enabled by default in the future)

### Bug fixes

- Fixed an issue relating to failures with unexpected exceptions with HTAP metadata optimization.
- Fixed an issue with HTAP that could occur when changing databases or schemas.
- Implemented asynchronous cleanup while destroying a pool to avoid potential deadlocks.
- Removed confusing error information for PUT commands for GCP.
- Fixed incorrect `SnowflakeDbConnection.Dispose` behavior.

## Version 2.1.2 (September 27, 2023)

### New features and updates

- Added support for hybrid transactional and analytical processing:

  - Added retry context in retries for query requests.
  - Added query context caching.
- Added the `GetQueryId()` method to `SnowflakeDbCommand` to retrieve the query ID of the most
  recent executed query to match the existing functionality in `SnowflakeDbDataReader`.

### Bug fixes

- Fixed an issue where PUT/GET commands could fail with internal stages on Azure government cloud accounts.
- Decreased memory usage in PUT/GET operations.
- Fixed an issue that could occur while uploading and downloading data when source files differed from destination files,
  such as might occur due to automatic file compression.

## Version 2.1.1 (August 22, 2023)

### New features and updates

- None.

### Bug fixes

- Fixed an issue where test connections were not reused when created successfully.
- Fixed an issue where the `*` and `?` wildcards did not work correctly in file paths.
- Fixed an issue where the driver incorrectly required a username and password for external browser authentication.

## Version 2.1.0 (July 27, 2023)

### BCR (Behavior Change Release) change

Fixed an issue where, under certain conditions, the .NET driver could retry HTTP requests indefinitely.
Previously, during an outage the .NET driver would retry the failed HTTP call continuously until the request
succeeds or until someone force kills the operation.

With this change, disables infinite HTTP retries originating from execute and executeQuery calls. Now, the .NET driver
limits HTTP retries to seven, by default. Customers can set the `MAXHTTPRETRIES` connection parameter to
customize the maximum number of retries. Customers can set `MAXHTTPRETRIES=0` to remove the retry limit,
but doing so runs the risk of the .NET driver infinitely retrying failed HTTP calls.

### New features and updates

- Improved handling of remote paths containing a subdirectory in a GET command.

### Bug fixes

- Fixed an issue with connection pools that could occur when a dirty connection is closed and the
  `BeginTransaction` method is called explicitly.
- Fixed an issue with `UseProxy` in `HTTPClientHandler`.
- Added the `BROWSER_RESPONSE_TIMEOUT` connection parameter to fix an issue with authentication in an external browser.
  The default is 120 seconds.
- Fixed an issue with connection pool timeouts during daylight saving time transitions.

## Version 2.0.25 (June 16, 2023)

### New features and updates

- None

### Bug fixes

- Fixed an issue where the proxy password could be visible in the Snowflake log file.
- Fixed an issue where `SnowflakeDbDataReader.HasRows()` always returned true for some query types (e.g. SELECT)
  regardless whether there are valid rows in query result.
- Fixed an intermittent “Authentication token has expired” or “Session no longer exists” issue when connection pooling
  enabled.
- Removed use of `WinHttpHandler`.
- Fixed an issue where retries on chunk downloading would occasionally fail, such as when a network error occurred
  after the data was partially downloaded.
- Fixed problem in chunk retry downloading process and improved testing of those retries.

## Version 2.0.24 (May 23, 2023)

### New features and updates

- Added session ID logging to get better tracking of the activity for each session in cases where multiple connections are used in parallel.

### Bug fixes

- Fixed an issue where a .NET application throw an unauthorized error when connection pooling was enabled.
- Fixed an issue with 401 errors caused by empty session tokens.

## Version 2.0.23 (April 19, 2023)

### New features and updates

- Changed the legacy supported version to version 4.7.1.

### Bug fixes

- Fixed an issue where a .NET application would terminate for an unhandled exception
  when `client_session_keep_alive=true`.
- Fixed an issue where a COMMIT could be interrupted by an unnecessary rollback.
- Fixed an issue where a connection could not terminate a session when connection pooling is enabled.
- Fixed an issue where calling `Close()` before `Dispose()` resulted in duplication connections in a pool.
- Fixed an issue where errors were thrown then a mandatory USER property was not provided.
- Fixed the WinHttpHandler `PlatformNotSupportedException`; the .NET driver now uses WinHttpHandler only
  for .NET framework applications.
- Fixed an issue where an error incorrectly occurred when passing an empty USER property in the connection
  string for SSO logins.
- Fixed an issue where database names that contained spaces that were enclosed in double quotes (e.g. “My DB”)
  were not treated properly.

## Version 2.0.22 (March 22, 2023)

### New features and updates

- None.

### Bug fixes

- Fixed an issue that caused applications that set `CLIENT_SESSION_KEEP_ALIVE=true` to hang when it closed the connection.
- Fixed an issue where query execution would intermittently fail after a timeout occurred.
- Fixed an issue where the .NET driver would fail to execute PUT commands in an FIPS-enabled deployment.
- Fixed the .NET connector throwing error: “System.Net.Http.WinHttpException (80072EE2, 12002): Error 12002 calling WINHTTP\_CALLBACK\_STATUS\_REQUEST\_ERROR”.
- Started adding the **https:** prefix to AWS endpoints that do not include the prefix.
- Updated the **Specify an unencrypted private key (read from a file)** example in the `README.md` file
  to remove the `Replace()` function call.

## Version 2.0.21 (February 22, 2023)

### New features and updates

- Added support for using GCS access tokens for PUT and GET queries (#585).

### Bug fixes

- Improved exception handling to preserve stack traces.

## Version 2.0.20 (January 24, 2023)

### New features and updates

- Added support for the new Okta OIE.
- Improved error logging for JSON parsing by including the `queryid` in the log message.

### Bug fixes

- Fixed issue with PUT/GET not determining the correct compression type of files to be uploaded.
- Fixed issue with PUT/GET result values not being mapped to the appropriate field.
- Fixed an out of bounds issue when trimming SQL queries that contained a closing comment.
- Fixed an issue where using Okta authentication failed when receiving an HTTP 429 error.
- Fixed an issue with session timeouts by adding the `DEFAULT_TIMEOUT_IN_SECOND` session parameter.
