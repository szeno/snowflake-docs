# PHP PDO Driver for Snowflake release notes for 2024

This article contains the release notes for the PHP PDO Driver for Snowflake, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for PHP PDO Driver for Snowflake updates.

See [PHP PDO Driver for Snowflake](/developer-guide/php-pdo/php-pdo-driver) for documentation.

## Version 3.0.3 (October 30, 2024)

### New features and updates

- Upgraded libsnowflakeclient to version 1.1.0.
- Upgraded openssl to version 3.0.15.
- Upgraded curl to version 8.10.1.

### Bug fixes

- None.

## Version 3.0.2 (August 29, 2024)

### New features and updates

- Increased the maximum allowable large object (LOB) size.

### Bug fixes

- None.

## Version 3.0.1 (July 24, 2024)

### New features and updates

- Removed the hardcoded top-level domain.

### Bug fixes

- Fixed an issue with Microsoft Windows not honoring proxy settings in environment variables.

## Version 3.0.0 (June 18, 2024)

### BCR (Behavior Change Release) changes

- PHP 8.0 is no longer supported.
- The minimum gcc compiler version for Linux changed from version 5.2 to 8.3.
- The default `loglevel` changed from TRACE to FATAL.

### New features and updates

- Added support for PHP version 8.3.
- Improved performance for connection reuse.

### Bug fixes

- Fixed an issue where the driver always created a log folder whether or not logging is actually needed.

## Version 2.0.3 (April 29, 2024)

### New features and updates

- None.

### Bug fixes

- Fixed an issue where timeout values in connection parameters weren’t honored.

## Version 2.0.2 (February 22, 2024)

### New features and updates

- Updated the following libraries:
  - curl from version 8.4.0 to 8.6.0
  - openssl from version 3.0.11 to 3.0.13
  - zlib from version 1.2.13 to 1.3.1

### Bug fixes

- Fixed an issue related to segmentation faults when the log level is set to DEBUG.
- Fixed an issue where the dependency libraries couldn’t be downloaded when building the driver with Visual Studio 2019.
