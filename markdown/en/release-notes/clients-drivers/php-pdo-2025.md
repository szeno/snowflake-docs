# PHP PDO Driver for Snowflake release notes for 2025

This article contains the release notes for the PHP PDO Driver for Snowflake, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for PHP PDO Driver for Snowflake updates.

See [PHP PDO Driver for Snowflake](/developer-guide/php-pdo/php-pdo-driver) for documentation.

## Version 3.4.0 (Dec 03, 2025)

### New features and updates

- Added native OKTA authentication support.
- Implemented a new CRL (Certificate Revocation List) checking mechanism.

  Enabling CRLs improves security by checking for revoked certificates during the TLS handshake process. For more information, see the [Replacing OCSP with CRL as the method of certificate revocation checking](https://community.snowflake.com/s/article/Replacing-OCSP-with-CRL-as-the-method-of-certificate-revocation-checking) Knowledge Base article.

  This feature is disabled by default. Snowflake recommend you test this feature in advisory mode before enabling it in production.

### Bug fixes

- Fixed the aarch64 build on MacOS.

## Version 3.3.0 (Aug 27, 2025)

### New features and updates

- Added ARM64 support for Linux.
- Added support for the Easy Logging feature in a configuration file.

### Bug fixes

- None.

## Version 3.2.0 (May 20, 2025)

### New features and updates

- Added support mult-factor authentication (MFA).

### Bug fixes

- Fixed a memory leak that occurred when fetching results.
- Fixed an OCSP configuration issue.

## Version 3.1.0 (January 29, 2025)

### New features and updates

- Added support for Visual Studio 2022 (VS17).
- Added support for PHP 8.4.

### Bug fixes

- Fixed an issue with executing unsupported queries like PUT or GET on stages causes a signed-to-unsigned conversion error that crashes the application using the driver. For more information, see [CVE-2025-24792](https://github.com/snowflakedb/pdo_snowflake/security/advisories/GHSA-f8q2-7fv5-cg93).
