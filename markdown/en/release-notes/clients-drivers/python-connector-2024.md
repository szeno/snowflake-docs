# Snowflake Connector for Python release notes for 2024

This article contains the release notes for the Snowflake Connector for Python, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Python updates.

See [Snowflake Connector for Python](/developer-guide/python-connector/python-connector) for documentation.

## Version 3.12.4 (December 03, 2024)

### New features and updates

- Bumped the pyOpenSSL dependency from >=16.2.0,<25.0.0 to >=22.0.0,<25.0.0.

### Bug fixes

- Fixed a bug where multi-part uploads to Azure were missing their MD5 hashes.
- Fixed a bug where `OpenTelemetry` header injection would sometimes cause Exceptions to be thrown.
- Fixed a bug where OCSP checks would throw `TypeError` and make mainly GCP blob storage unreachable.

## Version 3.12.3 (October 24, 2024)

### Security fixes

- Addressed issues raised by CVE-2024-49750. For more information, see advisory [GHSA-5vvg-pvhp-hv2m](https://github.com/snowflakedb/snowflake-connector-python/security/advisories/GHSA-5vvg-pvhp-hv2m).

### New features and updates

- Improved the error message for SSL-related issues to provide clearer resolution guidance.
- Improved the error message for SQL execution cancellations caused by a timeout.

### Bug fixes

- None.

## Version 3.12.2 (September 11, 2024)

### New features and updates

- None.

### Bug fixes

- Improved error handling for asynchronous queries, providing more detailed and informative error messages when an async query fails.
- Improved inference of top-level domains for accounts specifying a region in China, now defaulting to `snowflakecomputing.cn`.
- Improved implementation of `snowflake.connector.util_text.random_string` to reduce the likelihood of collisions.
- Updated the log level for OCSP fail-open warning messages from ERROR to WARNING.

## Version 3.12.1 (August 20, 2024)

### New features and updates

- None.

### Bug fixes

- Fixed a bug that logged the session token when renewing a session.
- Fixed a bug where disabling client telemetry did not work.
- Fixed a bug where passing `login_timeout` as a string raised a `TypeError` during the login retry step.
- Updated the connector to use `pathlib` instead of `os` for resolving the default configuration file location.
- Removed the upper `cryptography` version pin.
- Removed references to the `snowflake-export-certs` script, as its backing module was removed in a previous version.
- Enhanced the retry mechanism for handling transient network failures during query result polling when no server response is received.

## Version 3.12.0 (July 26, 2024)

### New features and updates

- Set the default connection timeout to 10 seconds and the socket read time to 10 minutes for HTTP calls in file transfers.
- Added the ability to connect to multiple domains.
- Optimized `to_pandas()` performance by using fully-parallel downloading logic.
- Bumped the keyring dependency from g>=23.1.0,<25.0.0 to g>=23.1.0,<26.0.0.

### Bug fixes

- Fixed a bug where specifying `client_session_keep_alive_heartbeat_frequency` in `snowflake-sqlalchemy` could make the connector unresponsive.
- Fixed an incorrect `private_key` connection parameter type hint.

## Version 3.11.0 (June 18, 2024)

### New features and updates

- Added support for the `token_file_path` connection parameter to read an OAuth token from a file when connecting to Snowflake.
- Added support for the `debug_arrow_chunk` connection parameter to allow debugging raw arrow data in cases of arrow data parsing failures.
- Added support for the `disable_saml_url_check` connection parameter to disable SAML URL checks in OKTA authentication.

### Bug fixes

- Fixed a bug where OCSP certificates signed using SHA384 algorithm cannot be verified.
- Fixed a bug where the status code showed as uploaded when a PUT command failed with a 400 error.
- Fixed a bug where a `PermissionError` was raised when the current user does not have the right permission on parent directory of configuration file path.
- Fixed a bug where an OCSP GET URL is not encoded correctly when it contains a slash.
- Fixed a bug where an SSO URL didn’t accept `:` in a query parameter, such as in `https://sso.abc.com/idp/startSSO.ping?PartnerSpId=https://xyz.snowflakecomputing.com/`.

## Version 3.10.1 (May 21, 2024)

### New features and updates

- None.

### Bug fixes

- Removed an incorrect error log message that could occur during arrow data conversion.

## Version 3.10.0 (April 29, 2024)

### New features and updates

- Added support for structured types to `fetch_pandas_all`.

### Bug fixes

- Fixed an issue relating to incorrectly formed China S3 endpoints.

## Version 3.9.1 (April 22, 2024)

### New features and updates

- Fixed an issue that caused a HTTP 400 error when connecting to a China endpoint.

### Bug fixes

- None.

## Version 3.9.0 (April 18, 2024)

### New features and updates

- Added support for log settings in a [logging configuration file](/developer-guide/python-connector/python-connector-example#label-python-easy-logging).
- Improved S3 acceleration logic when connecting to a China endpoint.

### Bug fixes

- None.

## Version 3.8.1 (April 09, 2024)

### New features and updates

- Improved `externalbrowser` authentication in containerized environments:

  - Instructs the browser to not fetch `/favicon` on a success page.
  - Uses a simple retry strategy for an empty `socket.recv` call.
  - Adds a `SNOWFLAKE_AUTH_SOCKET_REUSE_PORT` flag (`SNOWFLAKE_AUTH_SOCKET_REUSE_PORT=true`) to set the underlying socket’s `SO_REUSEPORT` flag (as described in the [socket man page](https://man7.org/linux/man-pages/man7/socket.7.html)).

    - Setting this flag can be useful when the randomized port used in the localhost callback url is being followed before the container engine completes port forwarding to host.
    - You can then statically map a port between your host and container and allow that port to be reused in rapid succession with a command similar to the following:

      Copy code

      ```
      SF_AUTH_SOCKET_PORT=3037 SNOWFLAKE_AUTH_SOCKET_REUSE_PORT=true poetry run python somescript.py
      ```
  - Adds a `SNOWFLAKE_AUTH_SOCKET_MSG_DONTWAIT` flag (`SNOWFLAKE_AUTH_SOCKET_MSG_DONTWAIT=true`) to make a non-blocking `socket.recv` call and retry on an error.
- Added support for parsing structured type information in schema queries.
- Bumped `platformdirs` from >=2.6.0,<4.0.0 to >=2.6.0,<5.0.0.
- Updated diagnostics to use `system$allowlist` instead of `system$whitelist`.
- Improved the cleanup logic so connections now rely on an interpreter shutdown instead of the `__del__` method.
- Updated the logging level from INFO to DEBUG when logging the executed query using `SnowflakeCursor.execute`.

### Bug fixes

- Fixed a bug that the truncated password in log is not masked.

## Version 3.7.1 (February 22, 2024)

### New features and updates

- Bumped the following dependencies:

  - pandas from version >=1.0.0,<2.2.0 to >=1.0.0,<3.0.0
  - cryptography from version <42.0.0,>=3.1.0 to >=3.1.0,<43.0.0
  - pyOpenSSL from version >=16.2.0,<24.0.0 to >=16.2.0,<25.0.0
- Bumped the keyring dependency lower bound to version 23.1.0 to address a security vulnerability.

### Bug fixes

- Fixed a memory leak in decimal data conversion.
- Fixed a bug where `write_pandas` wasn’t truncating the target table.

## Version 3.7.0 (January 26, 2024)

### New features and updates

- Added support for Python 3.12.
- Added a new Boolean `force_return_table` parameter to `SnowflakeCursor.fetch_arrow_all` to force returning `pyarrow.Table` in case of zero rows.
- Cleanup some C++ code warnings and performance issues.
- Made local testing more robust against implicit assumptions.
- Added support for connecting using an existing connection via the session and master token.
- Added support for connecting to Snowflake by authenticating with multiple SAML IDP using an external browser.
- Improved configuration permissions warning message.

### Bug fixes

- Fixed an issue with PyArrow Table type hinting.
- Fixed a compilation issue due to a missing `cstdint` header on gcc13.
