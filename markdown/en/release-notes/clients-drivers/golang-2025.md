# Go Snowflake Driver release notes for 2025

This article contains the release notes for the Go Snowflake Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Go Snowflake Driver updates.

See [Go Snowflake Driver](/developer-guide/golang/go-driver) for documentation.

## Version 1.18.1 (Dec 15, 2025)

### New features and updates

- Included a shared library to collect telemetry to identify and prepare testing platforms for native Rust extensions.

### Bug fixes

- Handled HTTP 307 and 308 responses in drivers to achieve better resiliency to backend errors.
- Created a temporary directory only if needed during file transfers.
- Fixed unnecessary user expansion for file paths during file transfers.

## Version 1.18.0 (Nov 20, 2025)

### New features and updates

- Added validation of CRL `NextUpdate` for freshly downloaded CRLs.
- Added logging of query text and parameters.

### Bug fixes

- Fixed a data race error in tests caused by the platform detection `init()` function.
- Made secrets detector initialization thread safe and more maintainable.

## Version 1.17.1 (Nov 4, 2025)

### New features and updates

- Added telemetry for login requests to supported platforms (such as EC2, Lambda, Azure function, and so on). You can disable the telemetry by setting the `SNOWFLAKE_DISABLE_PLATFORM_DETECTION` environment variable (`SNOWFLAKE_DISABLE_PLATFORM_DETECTION=true`).
- Exposed `QueryStatus` from `SnowflakeResult` and `SnowflakeRows` in the `GetStatus()` function.
- Added the `CrlDownloadMaxSize` parameter to limit the size of CRL downloads.
- Added official support for RHEL9 (Red Hat Enterprise Linux 9).
- Improved log messages.
- Deprecated several configuration options and functions. For more information, see the [Upcoming Gosnowflake v2 changes](https://github.com/snowflakedb/gosnowflake/issues/1586).

### Bug fixes

- Fixed a bug where GCP PUT/GET operations would fail when the connection context was canceled.
- Fixed unsafe reflection of `nil` pointers on `DECFLOAT` function in the bind uploader.
- Added temporary download files cleanup.
- Added a small clarification in the `oauth.go` example on token escaping.
- Ensured proper permissions for CRL cache directory.
- Bypassed proxy settings for WIF metadata requests.
- Fixed `nil` pointer dereferences while calling long-running queries.
- Moved the keyring-based secure storage manager into a separate file to avoid the need to initialize keyring on Linux.

## Version 1.17.0 (Sep 29, 2025)

### New features and updates

- Added support for Go 1.25, dropped support for Go 1.22.
- Added ability to configure OCSP for each individual connection.
- Added `DECFLOAT` support. See the [gosnowflake documentation](https://pkg.go.dev/github.com/snowflakedb/gosnowflake) for details.
- Added proxy options to connection parameters.
- Added `client_session_keep_alive_heartbeat_frequency` connection paramameter.
- Added support for multi-part downloads for S3, Azure and Google Cloud.
- Added `Config.singleAuthenticationPrompt` to control authentication flow. When `true`, only one authentication is performed at a time, allowing for manual interactions such as MFA or OAuth. Default is `true`.

### Bug fixes

- Fixed missing `DisableTelemetry` option in `Config`.
- Fixed multistatements in large result sets.
- Fixed unnecessary retries when a context is cancelled.
- Fixed a regression in loading TOML connection files.
- Fixed race conditions in stage downloads.

## Version 1.16.0 (Aug 14, 2025)

### New features and updates

- Added support for workload identity federation in the AWS, Azure, Google Cloud, and Kubernetes platforms.

  - Added the `WorkloadIdentityProvider` connection parameter.
  - Added `AuthTypeWorkloadIdentityFederation` to the values for the `authenticator` connection parameter.
- Implemented a new CRL (Certificate Revocation List) checking mechanism.

  Enabling CRLs improves security by checking for revoked certificates during the TLS handshake process. For more information, see the [Replacing OCSP with CRL as the method of certificate revocation checking](https://community.snowflake.com/s/article/Replacing-OCSP-with-CRL-as-the-method-of-certificate-revocation-checking) Knowledge Base article.

  This feature is disabled by default. For information on enabling this feature, see [CertRevocationCheckMode](https://pkg.go.dev/github.com/snowflakedb/gosnowflake#CertRevocationCheckMode). We recommend you test this feature in advisory mode before enabling it in production.
- Added support for opt-in single-use refresh tokens in the OAuth flow.
- Implemented a connectivity diagnostic tool.
- Added a session ID to logs produced by the connection and heartbeat modules.
- Added the `RegisterTLSConfig` function that lets you pass your own `TLSConfig` for the driver to use. Please use this function instead of modifying `SnowflakeTransport` directly.
- Removed the dependency to static list of root CAs for OCSP checking. Now, the default list of root CAs is used.

### Bug fixes

- Fixed an issue where error messages were not displayed while reading in structured types.
- Fixed a memory leak in the arrow batches example.
- Fixed issues with query cancellation.
- Removed the trailing slash from the default `RedirectUri` within the OAuth Authorization process.
- Fixed an issue with ignoring the maximum retry count when the timeout is not set.

## Version 1.15.0 (Jul 01, 2025)

### Private Preview (PrPr) features

Added support for workload identity federation in the AWS, Azure, GCP, and Kubernetes platforms.

Disclaimer:

- This feature can only be accessed by setting the `SF_ENABLE_EXPERIMENTAL_AUTHENTICATION` environment variable to `true`.
- You should use this feature only with non-production data.
- This PrPr feature is not covered by Support. However, the Product and Engineering teams are available during the PrPr phase.
- Please contact your account team for participation and documentation.

### New features and updates

- Added support for snake-case connection parameters.
- Optimized memory consumption during execution of PUT commands.

### Bug fixes

- Fixed an issue with permission handling for the `configuration.toml` file.

## Version 1.14.1 (May 28, 2025)

### New features and updates

- Added support for propagating OpenTelemetry contexts to GS.
- Added support for default client credentials in the OAuth authorization code flow.
- Moved OCSP initialization to the first HTTPS call.

### Bug fixes

- Aligned scan types and actually returned types for NUMBERs.
- Fixed an issue with `nil` dereferencing when an internal timeout happened (for instance for cloud provider call) when the original context was still valid.
- Fixed an issue with `nil` dereferencing during time out or canceling context race.
- Fixed encryption bugs where errors were never returned.
- Fixed downcast `smkId` to `int`, which caused decryption problems for very large stages.
- Fixed support for virtual style domains on GCP.
- Fixed the validation of the owner of the secure storage lock directory.

## Version 1.14.0 (Apr 30, 2025)

### New features and updates

- Implemented support for OAuth2 authorization code and client credential flows.
- Added support for PAT (programmatic access token):

  - Added the PROGRAMMATIC\_ACCESS\_TOKEN parameter for the parameter authenticator.
- Added support for virtual endpoints for GCP stages.

### Bug fixes

- Fixed the scan type for NUMBER columns when higher precision was enabled.

## Version 1.13.3 (Apr 28, 2025)

### Private Preview (PrPr) features

- Implemented support for OAuth2 authorization code and client credential flows.

Disclaimer:

- These features can only be accessed by setting `SF_ENABLE_EXPERIMENTAL_AUTHENTICATION` environment variable to `true`.
- You should use these features only with non-production data.
- These PrPr features are not covered by Support. However, the Product and Engineering teams are available during the PrPr phase.
- Please contact your account team for participation and documentation.

### New features and updates

- None.

### Bug fixes

- Fixed an issue with re-encrypting files for each request retry.
- Fixed Time-of-check Time-of-use (TOCTOU) race condition when checking access to Easy Logging configuration file. For more information, see [CVE-2025-46327](https://github.com/snowflakedb/gosnowflake/security/advisories/GHSA-6jgm-j7h2-2fqg).

## Version 1.13.2 (Mar 31, 2025)

### New features and updates

- Bumped the JWT library version from 5.2.1 to 5.2.2.
- Implemented and improved the file-based credentials cache for Linux, including enhanced token caching.

### Bug fixes

- Fixed PUT/GET handling when the query begins with a newline.
- Added more logging to certificate chain verification.
- Falling back to OCSP GET request only if the response for POST request was malformed.
- Fixed a memory leak related to not clearing OCSP cache.

## Version 1.13.1 (Mar 05, 2025)

### Private Preview (PrPr) features

Added support for PAT (programmatic access token) in Private Preview.

- Added the `PROGRAMMATIC_ACCESS_TOKEN` parameter for the parameter authenticator.

Disclaimer:

- This feature can only be accessed by setting `SF_ENABLE_EXPERIMENTAL_AUTHENTICATION` environment variable to `true`.
- You should use these features only with non-production data.
- These PrPr features are not covered by Support. However, the Product and Engineering teams are available during the PrPr phase.
- Please contact your account team for participation and documentation.

### New features and updates

- Dropped support for Go 1.21 and added support for Go 1.24.
- Upgraded Arrow to v18.
- Added a log for JWT claims.

### Bug fixes

- Fixed error messages for HTTP retries.

## Version 1.13.0 (Jan 29, 2025)

### New features and updates

- The driver now handles UUID as varchars.
- The driver honors `driver.Valuer/fmt.Stringer` interfaces when binding parameters.
- The driver detects when a response is JSON-based and runs a regular chunk downloader when Arrow batches mode is enabled to allow fetching response as rows.
- Added a timeout configuration for cloud providers calls.
- Added support for GCS region-specific endpoints.
- Fixed minor documentation formatting.
- Added retry when calling HEAD requests to GCP.
- Bumped the x/crypto library to version v0.31.0.

### Bug fixes

- Fixed a memory leak in handling Arrow responses that caused leakage of 64 bytes of memory.
- Fixed an issue with ignoring the region when us-west-2 is used.
- Added a check for empty private key before trying to generate JWT from it.
- The driver uses the correct transport for cloud providers calls.
- The driver no longer performs OCSP calls for cloud providers when OCSP is disabled.
