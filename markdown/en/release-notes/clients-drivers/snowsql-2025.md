# SnowSQL release notes for 2025

This article contains the release notes for the SnowSQL, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Note

For release note information for versions released prior to January 2022, see the [Client Release History](https://community.snowflake.com/s/article/client-release-history).

See [SnowSQL (CLI client)](/user-guide/snowsql) for documentation.

## Version 1.4.5 (Aug 13, 2025)

### New features and updates

- Added support for workload identity federation in the AWS, Azure, Google Cloud, and Kubernetes platforms.
  - Added the `workload_identity_provider` connection parameter.
  - Added `WORKLOAD_IDENTITY` to the values for the authenticator connection parameter.

### Bug fixes

- None

## Version 1.4.4 (Jul 30, 2025)

### New features and updates

- Updated openssl to version 3 for Windows.

### Bug fixes

- None

## Version 1.4.3 (Jul 10, 2025)

### New features and updates

- None

### Bug fixes

- Updated `!system` command library cleanup. Removed deprecation warning for setuptools.

## Version 1.4.2 (Jun 24, 2025)

### New features and updates

- None

### Bug fixes

- Removed SnowSQL \_internals from LD\_LIBRARY\_PATH for subprocess on linux.

## Version 1.4.1 (May 29, 2025)

### New features and updates

- Upgraded `snowflake-connector-python` to 3.15.0.

### Bug fixes

- None.

## Version 1.4.0 (May 22, 2025)

### New features and updates

- Added support for OAuth 2.0 Authorization Code Flow and OAuth 2.0 Client Credentials Flow.
- Upgraded openssl to version 3.5.0, cryptography <= 44.0.3.
- Updated how Windows binaries sign internally upgradable components.

### Bug fixes

- Fixed an issue with the `snowsql --version` command failing when automatic upgrades are disabled (`noup=False`).

## Version 1.3.3 (February 05, 2025)

### New features and updates

- Improved inference of top-level domains for accounts specifying a region in China, now defaulting to `snowflakecomputing.cn` with new `snowflake-connector-python` 3.13.2.
- Bumped `pycryptodomex` to version 3.21.0.
- Updated the build system with latest openssl 1.1.1w version.

### Bug fixes

- Fixed an issue with the `snowsql --version` command failing when automatic upgrades are disabled (`noup=False`).
