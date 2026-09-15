# Snowflake Connector for Python release notes for 2023

This article contains the release notes for the Snowflake Connector for Python, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Python updates.

See [Snowflake Connector for Python](/developer-guide/python-connector/python-connector) for documentation.

## Version 3.6.0 (December 07, 2023)

### New features and updates

- Added support for vector types.
- Added support for the `private_key_file` and `private_key_file_pwd` connection parameters.
- Added the new `expired` flag to the `SnowflakeConnection` class that tracks whether the connection’s master token has expired.
- Changed the urllib3 version pin to affect only Python versions lower than 3.10.

### Bug fixes

- Fixed a bug where date insertion failed when the date format is set and qmark-style binding is used.

## Version 3.5.0 (November 13, 2023)

### New features and updates

- Snowflake Connector for Python is now built solely on the apache arrow-nanoarrow project:

  - Reduced the wheel size to ~1MB and the installation size to ~5MB.
  - Removed a hard dependency on a specific version of pyarrow.
- Deprecated the following in support of the nanoarrow converter:

  - `snowflake.connector.cursor.NanoarrowUsage` class.
  - `NANOARROW_USAGE` environment variable.
  - `snowflake.connector.cursor.NANOARROW_USAGE` module variable.

### Bug fixes

- None.

## Version 3.4.1 (November 09, 2023)

### New features and updates

- Updated the following libraries:
  - Updated the vendored `urllib3` to version 1.26.18.
  - Updated the vendored `requests` to version 2.31.0.

### Bug fixes

- None.

## Version 3.4.0 (November 03, 2023)

### New features and updates

- Added support for `use_logical_type` in `write_pandas`.
- Added the `backoff_policy` argument to `snowflake.connector.connect` allowing for configurable backoff policy between retries of failed requests. See available implementations in the `backoff_policies` module.
- Added the `socket_timeout` argument to `snowflake.connector.connect` specifying socket read and connect timeout.
- Removed dependencies on pycryptodomex and oscrypto. All connections now go through OpenSSL via the cryptography library, which was already a dependency.

### Bug fixes

- Fixed `login_timeout` and `network_timeout` behavior. Retries of login and network requests are now properly halted after these timeouts expire.
- Fixed bug for issue [urllib3/urllib3#1878](https://github.com/urllib3/urllib3/issues/1878) in vendored `urllib`.
- Fixed issue with ingesting files over 80 GB to S3.

## Version 3.3.1 (October 18, 2023)

### New features and updates

- For non-Windows platforms, added command suggestions (`chown` or `chmod`) for insufficient file permissions of config files.

### Bug fixes

- Fixed an issue where connection diagnostics failed to complete certificate checks.
- Fixed an issue where the arrow iterator caused `ImportError` when the C extensions were not compiled.

## Version 3.3.0 (October 12, 2023)

### New features and updates

- Updated to Apache arrow-nanoarrow project for result arrow data conversion.
- Introduced the `NANOARROW_USAGE` environment variable to allow switching between the nanoarrow converter and the
  arrow converter. Valid values include:

  - `FOLLOW_SESSION_PARAMETER`, which uses the converter configured in the server.
  - `DISABLE_NANOARROW`, which uses the arrow converter, overriding the server setting.
  - `ENABLE_NANOARROW`, which uses the nanoarrow converter, overriding the server setting.
- Introduced the `snowflake.connector.cursor.NanoarrowUsage` enum, whose members include:

  - `NanoarrowUsage.FOLLOW_SESSION_PARAMETER`, which uses the converter configured in the server.
  - `NanoarrowUsage.DISABLE_NANOARROW`, which uses the arrow converter, overriding the server setting.
  - `NanoarrowUsage.ENABLE_NANOARROW`, which uses the nanoarrow converter, overriding the server setting.
- Introduced the `snowflake.connector.cursor.NANOARROW_USAGE` module variable to allow switching between the nanoarrow converter and the
  arrow converter. It works in conjunction with the `snowflake.connector.cursor.NanoarrowUsage` enum.

Note

The newly-introduced environment variable, enum, and module variable are temporary. They will be removed in a
future release when switch from arrow to nanoarrow for data conversion is complete.

### Bug fixes

- None.

## Version 3.2.1 (October 3, 2023)

### New features and updates

- Added thread safety in telemetry when instantiating multiple connections concurrently.
- Improved robustness in handling authentication changes.
- Removed the `urllib3.contrib.pyopenssl` deprecation warning from `urllib3` library.
- Updated the `platformdirs` dependency to versions 2.6.0 through 4.0.0 from versions 2.6.0 through 3.9.0.

### Bug fixes

- Fixed a bug where URL, port, and path were ignored in AWS PrivateLink OCSP retry attempts.

## Version 3.2.0 (September 7, 2023)

### New features and updates

- Made the `parser -> manager` renaming more consistent in `snowflake.connector.config_manager` module.
- Added support for default values for `ConfigOptions`.
- Added `default_connection_name` to `config.toml` file.

### Bug fixes

- None.

## Version 3.1.1 (August 28, 2023)

### New features and updates

- Added support for RSAPublicKey when constructing `AuthByKeyPair` in addition to raw bytes.

### Bug fixes

- Fixed a bug in retry logic for OKTA authentication to refresh token.
- Fixed a bug where the attribute `proxy_header` is missing in `SOCKSProxyManager` when connecting through SOCKS5 proxy.

## Version 3.1.0 (July 31, 2023)

### New features and updates

- Added a feature that lets you add connection definitions to the `connections.toml` configuration file.
  A connection definition refers to a collection of connection parameters, for example, if you wanted to define a
  connection named “prod”:

  Copy code

  ```
  [prod]
  account = "my_account"
  user = "my_user"
  password = "my_password"
  ```

  By default, we look for the `connections.toml` file in the location specified in the `SNOWFLAKE_HOME` environment
  variable (default: `~/.snowflake`). If this folder does not exist, the Python connector looks for the file in
  the `platformdirs` location, as follows:

  - On Linux: `~/.config/snowflake/`, but follows XDG settings
  - On Mac: `~/Library/Application Support/snowflake/`
  - On Windows: `%USERPROFILE%\AppData\Local\snowflake\`

  You can determine which file is used by running the following command:

  Copy code

  ```
  python -c "from snowflake.connector.constants import CONNECTIONS_FILE; print(str(CONNECTIONS_FILE))"
  ```
- Bumped cryptography dependency from <41.0.0,>=3.1.0 to >=3.1.0,<42.0.0.
- Improved OCSP response caching to remove tmp cache files on Windows
- Improved OCSP response caching to reduce the times of disk writing.
- Added a parameter `server_session_keep_alive` in `SnowflakeConnection` that skips session deletion when client connection closes.
- Tightened our pinning of `platformdirs`, to prevent their new releases breaking new versions of the connector.
- Allowed you to pass `type_mapper` to `fetch_pandas_batches()` and `fetch_pandas_all()`.
- Improved retry logic for okta authentication to refresh token if authentication gets throttled.
- Added retry reasons for queries that are retried by the client.
- Remove Python 3.7 support.
- Improved error handling of connection reset error.

### Bug fixes

- Fixed a bug where `SFPlatformDirs` would incorrectly append application\_name/version to its path.
- Fixed a bug where `write_pandas` fails when user does not have the privilege to create stage or file format in the target schema, but has the right privilege for the current schema.
- Worked around a segfault which sometimes occurred during cache serialization in multi-threaded scenarios.
- Fixed a bug about deleting the temporary files happened when running PUT command.
- Fixed a bug where `pickle.dump` segfaults during cache serialization in multi-threaded scenarios.

## Version 3.0.4 (May 25, 2023)

### New features and updates

- Added the `json_result_force_utf8_decoding` connection parameter to force decoding JSON content in utf-8 when the
  result format is JSON.
- Bumped vendored library urllib3 to 1.26.15
- Bumped vendored library requests to 2.29.0
- Bumped pandas dependency from <1.6.0,>=1.0.0 to >=1.0.0,<2.1.0
- Add support for Geometry types.

### Bug fixes

- Fixed a bug in which `cursor.execute()` could modify the argument `statement_params` dictionary object when executing a multi-statement query.
- Fixed a bug prevented calling `SnowflakeCursor.nextset` before fetching the result of the first query if the cursor runs an async multi-statement query.
- Fixed a bug when `_prefetch_hook()` was not called before yielding results of `execute_async()`.
- Fixed a bug where some `ResultMetadata` fields were marked as required when they were optional.
- Fixed a bug where bulk insert converts date incorrectly.

## Version 3.0.3 (April 20, 2023)

### New features and updates

- Added a parameter that allows users to skip file uploads to stage if file exists on stage and contents of the file match.
- Improved type hint of `SnowflakeCursor.execute` method.
- Improved GET logging to warn when downloading multiple files with the same name.

### Bug fixes

- Fixed a bug that prints error in logs for GET command on GCS.
- Added a parameter that allows users to skip file uploads to stage if file exists on stage and contents of the file match.
- Fixed a bug that occurred when writing a Pandas DataFrame with column names containing double quotes in `snowflake.connector.pandas_tool.write_pandas`.
- Fixed a bug that occurred when writing a Pandas DataFrame with binary data in `snowflake.connector.pandas_tool.write_pandas`.

## Version 3.0.2 (March 23, 2023)

### New features and updates

- None.

### Bug fixes

- Fixed a bug of incorrect type hints of `SnowflakeCursor.fetch_arrow_all` and `SnowflakeCursor.fetchall`.
- Improved logging to mask tokens in case of errors.
- Fixed a bug where `snowflake.connector.util_text.split_statements` swallowed the final line break in the case when there are no space between lines.
- Fixed a memory leak in the logging module of the Cython extension.
- Fixed a bug where the `put` command on AWS raised an `AttributeError` when uploading a file composed of multiple parts.
- Fixed a bug where the `put` command on AWS raised an `AttributeError` for file sizes larger than 200MB.

## Version 3.0.1 (March 01, 2023)

### New features and updates

- Improved the robustness of OCSP response caching to handle errors in cases of serialization and deserialization.
- Replaced the dependency on `setuptools` in favor of packaging.
- Updated `async_executes` method’s doc-string.
- Errors raised now have a query field that contains the SQL query that caused them when available.

### Bug fixes

- Fixed a bug where `AuthByKeyPair.handle_timeout` should pass keyword arguments instead of positional arguments
  when calling `AuthByKeyPair.prepare`.
- Fixed a bug where MFA token caching would refuse to work until restarted instead of re-authenticating.

## Version 3.0.0 (January 27, 2023)

### BCR (Behavior Change Release) change

- Fixed a bug where write\_pandas did not use user-specified schemas and databases to create intermediate objects.

  Previously, the write\_pandas function created temporary objects in the currently-used database and schema and only put
  the final table (that was created or appended) in the user-specified database and schema. With this version,
  if the database or schema parameters for `write_pandas` are different than the currently-selected one, you need to
  make sure that the user who is executing `write_pandas` has access to create/drop temporary stages, file formats,
  and tables with the schema referenced by the `write_pandas` function.

  Snowflake recommends that you test any new driver version in pre-production environments before deploying to
  production environments. With this behavior change, you should give special attention to the scenario(s)
  listed above (i.e. `write_pandas` with database or schemas parameters that differ from the current context).

### New features and updates

- Bumped pyarrow dependency from >=8.0.0,<8.1.0 to >=10.0.1,<10.1.0
- Bumped pyOpenSSL dependency from <23.0.0 to <24.0.0
- During browser-based authentication, the SSO url is now printed before opening it in the browser
- Increased the level of a log for when ArrowResult cannot be imported
- Added a minimum MacOS version check when compiling C-extensions

### Bug fixes

- Fixed a bug where `write_pandas` did not use user-specified schema and database to create intermediate objects
- Fixed a bug where HTTP response code of 429 were not retried
- Fixed a bug where MFA token caching was not working
