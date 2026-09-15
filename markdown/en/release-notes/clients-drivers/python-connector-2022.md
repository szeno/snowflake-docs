# Snowflake Connector for Python release notes for 2022

This article contains the release notes for the Snowflake Connector for Python, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Python updates.

See [Snowflake Connector for Python](/developer-guide/python-connector/python-connector) for documentation.

## Version 2.9.0 (December 14, 2022)

### New features and updates

- Reworked authentication internals to allow users to plug custom key-pair authenticators.
- Multi-statement query execution is now supported through `cursor.execute` and `cursor.executemany`.

  - The Snowflake parameter `MULTI_STATEMENT_COUNT` can be altered at the account, session, or statement level.
    An additional argument, `num_statements`, can be provided to execute to use this parameter at the statement level.
    It must be provided to `executemany` to submit a multi-statement query through the method. Note that bulk
    insert optimizations available through `executemany` are not available when submitting multi-statement queries.
    - By default the parameter is 1, meaning only a single query can be submitted at a time.
    - Set to 0 to submit any number of statements in a multi-statement query.
    - Set to >1 to submit the specified exact number of statements in a multi-statement query.
    - Bindings are accepted in the same way for multi-statements as they are for single statement queries.
- Asynchronous multi-statement query execution is supported. Users should still use `get_results_from_sfqid` to retrieve results.
- To access the results of each query, users can `call SnowflakeCursor.nextset()` as specified in the
  DB 2.0 API (PEP-249), to iterate through each statements results.

  - The first statement’s results are accessible immediately after calling execute (or `get_results_from_sfqid` if asynchronous)
    through the existing `fetch*()` methods.

### Bug fixes

- Fixed a bug where the permission of the file downloaded via GET command is changed.

## Version 2.8.3 (November 28, 2022)

### New features and updates

- Bumped cryptography dependency from <39.0.0 to <41.0.0.

### Bug fixes

- Fixed a bug where an expired OCSP response cache caused infinite recursion during cache loading.

## Version 2.8.2 (November 18, 2022)

### New features and updates

- Improved performance of OCSP response caching.
- No longer resolve target location on the local machine during the execution of GET commands.
- Improved performance of regexes used for PUT/GET SQL statement detection.

## Version 2.8.1 (October 28, 2022)

### New features and updates

- Bumped cryptography dependency from <37.0.0 to <39.0.0.
- When closing a connection, the async query status checking is now parallelized.

### Bug fixes

- Fixed an issue where `write_pandas` wouldn’t write an empty `DataFrame` to Snowflake.

## Version 2.8.0 (September 27, 2022)

### Bug fixes

- Fixed missing `dtypes` when calling `fetch_pandas()` and `fetch_arrow()` on empty results.
- Fixed a bug where `rowcount` was deleted when the cursor was closed.
- Fixed a bug where `extTypeName` was used even when it was empty.
- Updated how telemetry entries are constructed.
- Added telemetry for imported root packages during run-time.
- Added telemetry for using `write_pandas`.
- The `write_pandas` function now supports providing additional arguments to be used by `DataFrame.to_parquet`.
- All optional parameters of `write_pandas` can now be provided to `pd_writer` and `make_pd_writer` to be used with `DataFrame.to_sql`.

## Version 2.7.12 (August 24, 2022)

### New features and updates

- Added in-file caching for OCSP response caching.
- Added support for OKTA Identity Engine.
- The `write_pandas` function now supports transient tables through the new `table_type` argument that supersedes `create_temp_table` argument.

### Bug fixes

- Fixed a bug where timestamps fetched as `pandas.DataFrame` or `pyarrow.Table` would overflow for the sake of
  unnecessary precision. In the case where an overflow cannot be prevented, a clear error is now raised.
- Fixed a bug where calling `fetch_pandas_batches` incorrectly raised `NotSupportedError` after an async query was executed.

## Version 2.7.11 (July 28, 2022)

### Bug fixes

- Added a minimum version pin to `typing_extensions`.

## Version 2.7.10 (July 25, 2022)

### New features and updates

- Added an in-memory cache to OCSP requests.
- Added an overwrite option to `write_pandas`.
- Added the `lastrowid` attribute to `SnowflakeCursor` in compliance with PEP-249.
- Added new connection diagnostics capabilities.
- Updated the following libraries and resources:
  - Supported pyarrow versions to 8.0.X.
  - Vendored library versions requests to 2.28.1 and urllib3 to 1.26.10.
  - Supported numpy dependency versions from 1.23.0 to 1.24.0.

### Bug fixes

- Fixed an issue where gzip-compressed HTTP requests might be garbled by an unflushed buffer.

## Version 2.7.5 (March 18, 2022)

### Behavior change

- Deprecated support for Python 3.6.

### New feature

- Added an option for partners to inject their name through an environmental variable (`SF_PARTNER`).

### Bug fixes

- Fixed a bug where we would not wait for input if a browser window couldn’t be opened for SSO login.
- Exported a type definition for `SnowflakeConnection`.
- Fixed a bug where final Arrow table would contain duplicate index numbers when using `fetch_pandas_all`.

## Version 2.7.3 (January 18, 2022)

### Bug fixes

- Moved package metadata from `setup.py` to `setup.cfg`.
- Added `Timezone` to `Timestamp_TZ`.
- Fixed an error related to storage credentials.
- Fixed an issue where py.typed was not being included in wheels.
- Fix an issue where negative numbers were not correctly converted using `arrow_number_to_decimal`.
- Added file handling for empty files when using GET.
- Fixed the long description rendering for PyPi.
- Added error handling for DUO when SMS is not present.
- Added the ability to auto-create a table when writing a pandas `DataFrame` to a Snowflake table.
- Updated numpy requirement from <1.22.0 to <1.23.0.
- Updated the CODEOWNERS file.
