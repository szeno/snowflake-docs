# PHP PDO Driver for Snowflake release notes for 2026

This article contains the release notes for the PHP PDO Driver for Snowflake, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for PHP PDO Driver for Snowflake updates.

See [PHP PDO Driver for Snowflake](/developer-guide/php-pdo/php-pdo-driver) for documentation.

## Version 4.2.0 (Sep 3, 2026)

### New features and updates

- Added the `workload_identity_aws_use_outbound_token` connection parameter (default `false`) to opt into AWS Workload Identity Federation attestation using STS `GetWebIdentityToken` (JWT) instead of the default SigV4 `GetCallerIdentity` method.
- Added the `wif_host` connection parameter to override the STS/IAM endpoint domain used for AWS and GCP Workload Identity Federation.
- Added CRL cache cleanup so expired CRLs no longer accumulate in long-lived processes. New environment variables control cleanup behavior:
  - `SF_CRL_CACHE_CLEANUP_INTERVAL` (default 3600 seconds; set to 0 to disable)
  - `SF_CRL_CACHE_VALIDITY_TIME` (default 86400 seconds)
  - `SF_CRL_ON_DISK_CACHE_REMOVAL_DELAY` (default 604800 seconds)
- Migrated Azure storage from azure-storage-cpplite to Azure SDK for C++ (azure-storage-blobs 12.18.0).
- Removed the `wif_audience` connection parameter.
- Updated Curl to v8.21.0.
- Upgraded libsnowflakeclient to version 2.10.0.

### Bug fixes

- Restored SigV4 `GetCallerIdentity` as the default AWS Workload Identity Federation attestation method. The STS `GetWebIdentityToken` (JWT) flow introduced in version 4.0.0 is now opt-in via the `workload_identity_aws_use_outbound_token` connection parameter.
- Restricted `WORKLOAD_IDENTITY` authentication to recognized Snowflake hosts before fetching ambient cloud credentials. The `SNOWFLAKE_WIF_ALLOWED_HOST_SUFFIXES` environment variable can add extra trusted suffixes.
- Fixed credentials appearing in diagnostic trace output.
- Fixed the HTTP retry path so the request buffer is reset correctly.
- Fixed a delay in the AWS identity detector.
- Tightened string copy bounds checking after the Azure SDK migration to prevent a buffer overflow.

## Version 4.1.0 (Jul 23, 2026)

### New features and updates

- Added support for TOML configuration file connections. When `config.toml` or `connections.toml` is present, you can connect with an empty DSN and no username/password: `new PDO("snowflake:", null, null)`. Connection parameters in the TOML file are equivalent to specifying them in the DSN. See [Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections).
- Updated OpenSSL to v3.5.7.
- Upgraded libsnowflakeclient to version 2.9.2.

### Bug fixes

- Fixed memory handling in the named-parameter binding path when parameters are rebound or cleared during statement teardown.
- Calling `PDO::quote()` now returns SQLSTATE IM001 with a clear message that quoting is not supported. Applications using prepared statements with bound parameters are unaffected.
- Private key passphrases are now masked in DEBUG-level connection log output, consistent with other sensitive connection parameters.
- Improved validation of account, region, host, protocol, and port connection attributes used in request URLs.
- Improved OCSP cache reliability under concurrent access.
- Fixed a resource handling issue that could affect DNS resolution when address lookup fails.

## Version 4.0.0 (Jun 16, 2026)

### BCR (Behavior Change Release) changes

- PHP 8.1 is no longer supported.

### New features and updates

- Added support for PHP 8.5.
- Added support for forwarding the Snowpark Container Services session token in the login request. When the `SNOWFLAKE_RUNNING_INSIDE_SPCS` environment variable is set to `true`, the driver reads the token from `/snowflake/session/spcs_token` and attaches it as `SPCS_TOKEN` on the login payload.
- Added the `SF_SKIP_TOKEN_FILE_PERMISSIONS_VERIFICATION` environment variable as the namespaced replacement for `SKIP_TOKEN_FILE_PERMISSIONS_VERIFICATION` when reading JSON token files. The unprefixed variable still works but is now logged as deprecated.
- Changed AWS workload identity federation attestation from a base64-encoded signed STS `GetCallerIdentity` request to a JWT obtained from STS `GetWebIdentityToken`.
- Updated Curl to v8.20.0.
- Updated OpenSSL to v3.0.21.
- Updated AWS SDK for C++ to v1.11.806.
- Upgraded libsnowflakeclient to version 2.9.1.

### Bug fixes

- Fixed an infinite JWT renewal loop during login when `renew_timeout` elapses repeatedly (for example, behind a bad proxy or slow network). Renewal is now bound by the configured login retry count and overall login timeout.
- Fixed misleading error message when building the driver on Windows.

## Version 3.7.0 (Apr 22, 2026)

### New features and updates

- Added the `log_query_text` and `log_query_parameters` connection parameters to allow the logging of the SQL text and bound parameter values, respectively. Both parameters default to `false`.
- Added the `crl_download_max_size` connection parameter to control the maximum size (in bytes) of a CRL file downloaded during TLS certificate revocation checks. The default value is 20 MB.
- Updated Curl to v8.19.0.
- Updated OpenSSL to v3.0.20.

### Bug fixes

- None.

## Version 3.6.0 (Mar 05, 2026)

### New features and updates

- Implemented richer `client_environment` telemetry information to include on which environment the driver runs (such as Lambda, EC2, GCP, Azure VM, and so on) and whether the managed identity is enabled.
- Added support for workload identity federation authentication, including the following new connection parameters:

  - `workload_identity_provider` - Platform of the workload identity provider. Possible values include: AWS, AZURE, GCP, and OIDC.
  - `workload_identity_azure_resource` - If the AZURE `workload_identity_provider` is used, this parameter sets the resource that the driver should use to identify itself.
  - `workload_identity_impersonation_path` - An array of strings that provides an identity chain to use when connecting to Snowflake. Array elements are either a full service account address or a service account’s unique ID.

    Impersonation works by following each array entry to obtain a token that allows authorization of the next service account. Each account in the identity chain needs permissions to impersonate the next account only. The final account in the list obtains your Snowflake connection token and uses it to connect to Snowflake.

    This parameter is supported for AWS and Google Cloud workloads and only applies when `authenticator=WORKLOAD_IDENTITY`.
- Updated OpenSSL to 3.0.19.
- Added support for multistatement queries.

### Bug fixes

- None.

## Version 3.5.0 (Feb 03, 2026)

### New features and updates

- Added support for Red Hat Enterprise Linux (RHEL) 9.
- Deprecated CentOS 7 builds. Rocky 8/RHEL8 is now the minimum system version.
- Added a warning for HTTP usage in OAuth authentication flows.
- Set `LOCAL_APPLICATION` as a default for the `client_id` and `client_secret` for the OAuth Authorization code flow.
- Updated Curl to 8.16.0.
- Removed the workload identity federation (WIF) auto-detection mechanism.
- Added auto-detection of the application path and included it in the `CLIENT_ENVIRONMENT` variable.
- Updated OpenSSL to 3.0.18

### Bug fixes

- Fixed the expired file lock on Linux for the Secure Storage.
- Removed the username requirement for the WIF authentication.
