# SnowSQL release notes for 2026

This article contains the release notes for the SnowSQL, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Note

For release note information for versions released prior to January 2022, see the [Client Release History](https://community.snowflake.com/s/article/client-release-history).

See [SnowSQL (CLI client)](/user-guide/snowsql) for documentation.

## Version 1.5.5 (Nov 9, 2026)

### New features and updates

- Upgraded the bundled `certifi` package to 2026.10.23.
- Upgraded the bundled `botocore` library to 1.43.117.

### Bug fixes

- Restored the `boto3` and `botocore` libraries in the SnowSQL installation bundle. This fixes workload identity federation authentication on AWS, which failed with `module 'boto3' has no attribute 'session'` or `module 'botocore' has no attribute 'session'`.

## Version 1.5.4 (Oct 22, 2026)

### New features and updates

- Upgraded the bundled `certifi` package to 2026.10.19.

### Bug fixes

- Improved signature validation of auto-upgrade downloads.

## Version 1.5.3 (Oct 20, 2026)

### New features and updates

- Upgraded `snowflake-connector-python` to 4.8.0.
- Upgraded the bundled Python version to 3.12 for Linux and macOS.

### Bug fixes

- None.

## Version 1.5.2 (Sep 10, 2026)

### New features and updates

- Upgraded `snowflake-connector-python` to 4.7.3.
- Removed the SQLite dependency from the SnowSQL installation bundle.

### Bug fixes

- None.

## Version 1.5.1 (Jul 17, 2026)

### New features and updates

- Upgraded `snowflake-connector-python` to 4.7.1.

### Bug fixes

- None.

## Version 1.5.0 (Apr 16, 2026)

### New features and updates

- Upgraded `snowflake-connector-python` to 4.4.0.
- Upgraded OpenSSL to 3.5.5 to address CVE-2025-9230.

### Bug fixes

- None.

## Version 1.4.7 (Nov 6, 2026)

### New features and updates

- Upgraded the bundled `certifi` package to 2026.10.23.
- Upgraded the bundled `botocore` library to 1.43.117.

### Bug fixes

- Restored the `boto3` and `botocore` libraries in the SnowSQL installation bundle. This fixes workload identity federation authentication on AWS, which failed with `module 'boto3' has no attribute 'session'` or `module 'botocore' has no attribute 'session'`.

## Version 1.4.6 (Oct 29, 2026)

### New features and updates

- Upgraded `snowflake-connector-python`.
- Upgraded the bundled `certifi` package.
- Upgraded the bundled Python version for Linux and macOS.

### Bug fixes

- None.
