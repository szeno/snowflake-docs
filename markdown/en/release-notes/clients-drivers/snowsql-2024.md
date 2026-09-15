# SnowSQL release notes for 2024

This article contains the release notes for the SnowSQL, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Note

For release note information for versions released prior to January 2022, see the [Client Release History](https://community.snowflake.com/s/article/client-release-history).

See [SnowSQL (CLI client)](/user-guide/snowsql) for documentation.

## Version 1.3.2 (August 12, 2024)

### New features and updates

None.

### Bug fixes

- Fixed an issue with the `snowsql --version` command failing when automatic upgrades are disabled (`noup=False`).

## Version 1.3.1 (June 28, 2024)

### New features and updates

- Added Linux aarch64 binaries.

### Bug fixes

- None

## Version 1.3.0 (May 03, 2024)

### BCR (Behavior Change Release) changes

- The SnowSQL 1.3.0 release disabled automatic upgrades. To use this version, please [download and reinstall](/user-guide/snowsql-install-config) SnowSQL 1.3.0. Going forward, you must manually install new versions of SnowSQL.

### New features and updates

- None.

### Bug fixes

- Disabled automatic updates to fix an issue where expired S3 licenses caused SnowSQL to fail.
- Fixed an issue where the lack of permission to create log directory aborted SnowSQL.
- Fixed an issue that endpoint is not created correctly when connecting to China deployment.

## Version 1.2.32 (March 05, 2024)

### New features and updates

- Bumped the `keyring` dependency to 23.1.0 to address a security vulnerability.

### Bug fixes

- None.
