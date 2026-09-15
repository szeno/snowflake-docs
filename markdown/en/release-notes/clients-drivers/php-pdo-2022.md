# PHP PDO Driver for Snowflake release notes for 2022

This article contains the release notes for the PHP PDO Driver for Snowflake, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Note

For release note information for versions released prior to January 2022, see the [Client Release History](https://community.snowflake.com/s/article/client-release-history).

See [PHP PDO Driver for Snowflake](/developer-guide/php-pdo/php-pdo-driver) for documentation.

## Version 1.2.5 (October 26, 2022)

### New features

- Added new `proxy` and `no_proxy` connection settings.

### Bug fixes

- Fixed an issue with key pair authentication.

## Version 1.2.4 (August 23, 2022)

### New features

- Added support for key-pair authentication.

## Version 1.2.3 (July 08, 2022)

### Bug fixes

- Fixed an issue that caused `autocommit` to turn over when creating a connection with options.

Version 1.2.2 (May 24, 2022)

### Bug fixes

- Fixed an issue related to loading the PHP driver with php-fpm.
- Upgraded libsnowflakeclient to version 0.6.12.

## Version 1.2.1 (Mar 16, 2022)

### New features

- Added support for PHP 8.1.
- Updated documentation to update the supported PHP versions.
