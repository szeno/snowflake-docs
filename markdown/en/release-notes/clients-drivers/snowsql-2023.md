# SnowSQL release notes for 2023

This article contains the release notes for the SnowSQL, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Note

For release note information for versions released prior to January 2022, see the [Client Release History](https://community.snowflake.com/s/article/client-release-history).

See [SnowSQL (CLI client)](/user-guide/snowsql) for documentation.

## Version 1.2.31 (December 13, 2023)

### New features and updates

- Added a new `--include_connector_version` command-line option to display the version of the Snowflake Connector for Python software that is packaged in the SnowSQL binary.
- Stopped removing whitespace from SnowSQL variables.

### Bug fixes

- None.

## Version 1.2.30 (November 13, 2023)

### New features and updates

- Updated the `snowflake-connector-python` dependency to 3.4.1.
- Removed the `oscrypto` dependency, while maintaining the `pycryptodomex` dependency.

### Bug fixes

- Updated `isAuthorizedToRun` in `CallCtx` to fix an issue that prevented the [VALIDATE\_PIPE\_LOAD](/sql-reference/functions/validate_pipe_load) function from accessing the pipe inside an app when the app is created from listing.

## Version 1.2.29 (October 10, 2023)

### New features and updates

- Updated the cryptography dependency to version 41.0.3.

### Bug fixes

- None.

## Version 1.2.28 (August 07, 2023)

### New features and updates

- Added support for Mac ARM64 binaries.

### Bug fixes

- None.

## Version 1.2.27 (June 15, 2023)

### New features and updates

- Added the `json_result_force_utf8_decoding` option to force result data to be decoded in UTF-8.
  By default, `json_result_force_utf8_decoding` is set to `false` for compatibility with legacy data. Snowflake
  recommends setting the value to true.

### Bug fixes

- Fixed a bug where default logging settings referenced parent directory and the level was set to debug by default.

## Version 1.2.26 (April, 2023)

Note

Version 1.2.25 was removed shortly after release. Version 1.2.26 includes the features and fixes initially
included in version 1.2.25.

### New features

- Added the recursion\_limit option to limit the Python recursion depth.
- Added the QUERY\_TAG CLI argument to specify query tags for running queries in SnowSQL. By default, QUERY\_TAG
  reads the value of the `SNOWSQL_QUERY_TAG` environment variable.

### Bug fixes

- Fixed a bug where SnowSQL used an incorrect version of LD\_LIBRARY\_PATH to open web browsers.
- Fixed an issue where SnowSQL warned of failure to import ArrowResult.
