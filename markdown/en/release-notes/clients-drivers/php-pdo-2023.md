# PHP PDO Driver for Snowflake release notes for 2023

This article contains the release notes for the PHP PDO Driver for Snowflake, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for PHP PDO Driver for Snowflake updates.

See [PHP PDO Driver for Snowflake](/developer-guide/php-pdo/php-pdo-driver) for documentation.

## Version 2.0.1 (November 09, 2023)

### Behavior Change Release (BCR) changes

Starting with version 2.0.1 of the PHP PDO driver, PHP versions 7.3 and 7.4 are no longer supported.

### New features and updates

- Updated the following libraries:

  - openssl from 3.0.9 to 3.0.11
  - curl from 8.1.2 to 8.4.0
- Added the `login_timeout`, `retryTimeout`, and `max_login_retries` connection parameters to manage the frequency of retries for
  unsuccessful connection requests.

### Bug fixes

- None.

## Version 2.0.0 (September 29, 2023)

### Behavior Change Release (BCR) changes

Starting with version 2.0.0 of the PHP PDO driver:

- Upgraded from openssl 1.1.1 to openssl 3.0.9. Consequently, private keys generated using the deprecated encryption
  algorithms in previous openssl library versions no longer work. When you update to PHP PDO 2.0.0 you must
  regenerate your private key file used for key pair authentication.

### New features and updates

- Added support for PHP 8.2.
- Added support for Mac ARM64 systems.
- Added specific error messages that are generated when building an application if `cmake` is not installed.
- Added support for getting the driver version programmatically with `PDO::getAttribute()` with `PDO::ATTR_CLIENT_VERSION`.
- Added the `PDO::SNOWFLAKE_ATTR_QUERY_ID` attribute to get query ids through `PDO::getAttribute()` or `PDOStatement::getAttribute()`.
- Added support for hybrid transactional and analytical processing:

  - Added retry context in retries for query requests.
  - Added query context caching.
- Updated the following software libraries:

  - Updated `curl` from version 7.88.1 to 8.1.2.
  - Updated `util-linux` from version 2.36.1 to 2.39.0.
  - Updated the `cacert` bundle used for SSL connections.

### Bug fixes

- Fixed an issue where the driver did not use the entire OCSP URL in the certificate when performing OCSP validation.

## Version 1.2.7 (May 23, 2023)

### New features

None.

### Bug fixes

- Fixed an issue where a connection could fail when using a proxy that doesn’t need a username and password.

## Version 1.2.6 (January 24, 2023)

### New features

None.

### Bug fixes

- Fixed an issue where the driver returned empty strings (“”) instead of NULL values when using PHP 8.1.
