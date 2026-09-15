# .NET Driver release notes for 2025

This article contains the release notes for the .NET Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for .NET Driver updates.

See [.NET Driver](/developer-guide/dotnet/dotnet-driver) for documentation.

## Version 5.2.1 (December 10, 2025)

### New features and improvements

- None.

### Bug fixes

- Fixed the extremely rare case where intermittent network issues during uploads to Azure Blob Storage prevented metadata updates.

## Version 5.2.0 (December 03, 2025)

### New features and improvements

- Added multi-targeting support. NuGet now selects the appropriate build based on the target framework and OS.
- Added support for native Arrow structured types.

### Bug fixes

- Fixed CRL validation to reject newly downloaded CRLs when their `NextUpdate` value has expired.
- Added exception handling to the session heartbeat to prevent network errors from disrupting background heartbeat checks.
- Added retry support for HTTP 307/308 status codes.
- Added the ability to specify non-string values in TOML configuration files. For example, `port` can now be specified as an integer.

## Version 5.1.0 (November 04, 2025)

### New features and improvements

- Added the `APPLICATION_PATH` to the `CLIENT_ENVIRONMENT` sent during authentication to identify the application connecting to Snowflake.
- AWS WIF (Workload Identity Federation) now also checks the application configuration and AWS profile credentials store when determining the current AWS region.
- Added ability for users to configure the maximum number of connections by setting the `SERVICE_POINT_CONNECTION_LIMIT` property.
- Added the `CRLDOWNLOADMAXSIZE` connection parameter to limit the maximum size of CRL (certificate revocation list) files downloaded during certificate revocation checks.

### Bug fixes

- Renew idle sessions in the pool if keep alive is enabled.

## Version 5.0.0 (October 16, 2025)

### BCR (Behavior Change Release) changes

- Removed the `log4net` dependency and enabled delegated logging.
- Upgraded the AWS SDK library to v4.
- Removed some internal classes from the public API.

### New features and improvements

- Implemented a new CRL (Certificate Revocation List) checking mechanism.

  Enabling CRLs improves security by checking for revoked certificates during the TLS handshake process. For more information, see the [Replacing OCSP with CRL as the method of certificate revocation checking](https://community.snowflake.com/s/article/Replacing-OCSP-with-CRL-as-the-method-of-certificate-revocation-checking) Knowledge Base article.

  This feature is disabled by default. For information on enabling this feature, see [Switching on/off certificate revocation checks (CRL)](https://github.com/snowflakedb/snowflake-connector-net/blob/master/doc/CertficateValidation.md#switching-onoff-certificate-revocation-checks-crl). We recommend you test this feature in advisory mode before enabling it in production.
- Added support for TLS 1.3. The default negotiated version of TLS is either TLS 1.2 or TLS 1.3, and the server decides which one to establish.
- Removed noisy log messages.

### Bug fixes

- None.

## Version 4.8.0 (August 13, 2025)

### New features and updates

- Added support for workload identity federation in the AWS, Azure, Google Cloud, and Kubernetes platforms.

  - Added the `WORKLOAD_IDENTITY_PROVIDER` connection parameter.
  - Added `WORKLOAD_IDENTITY` to the values for the `authenticator` connection parameter.
- Added support of single use refresh tokens during the OAuth flow.

### Bug fixes

- Removed trailing slash from the default `RedirectUri` within the OAuth Authorization process.
- Fixed a problem with ignoring *endpoint* override in AWS FIPS deployments.

## Version 4.7.0 (July 01, 2025)

### Private Preview (PrPr) features

Added support for workload identity federation in the AWS, Azure, GCP, and Kubernetes platforms.

Disclaimer:

- This feature can only be accessed by setting the `SF_ENABLE_EXPERIMENTAL_AUTHENTICATION` environment variable to `true`.
- You should use this feature only with non-production data.
- This PrPr feature is not covered by Support. However, the Product and Engineering teams are available during the PrPr phase.
- Please contact your account team for participation and documentation.

### New features and improvements

- None.

### Bug fixes

- Set `ConfigureAwait(false)` for asynchronous Programmatic Access Token authentications.
- Fixed an issue with the missing `OAuthClientSecret` parameter provided externally to a connection string when creating sessions that use the `MinPoolSize` feature.

## Version 4.6.0 (June 18, 2025)

### New features and improvements

- Added support for virtual style domains in Google Cloud Storage (GCS).
- Added a time duration to the logs for HTTPS calls.
- Added a cleaning query context cache before pooling a connection.

### Bug fixes

- Enabled returning result sets for DML operations.
- Added refreshing of expired sessions when fetching operation results.

## Version 4.5.0 (May 09, 2025)

### New features and improvements

- Added OAuth 2.0 Authorization Code flow authentication:

  - Added the `oauth_authorization_code` authenticator.
  - Added the `oauthScope`, `oauthClientId`, `oauthClientSecret`, `oauthAuthorizationUrl`, `oauthTokenRequestUrl`, and `oauthRedirectUri` connection parameters to configure the authentication.
  - Added the ability to provide `oauthClientSecret` by setting the `SnowflakeDbConnection.OAuthClientSecret` property instead of providing it in a connection string.
  - Added a cache for OAuth 2.0 tokens.
- Added OAuth 2.0 Client Credential flow authentication:

  - Added the `oauth_client_credentials` authenticator.
  - Added `oauthScope`, `oauthClientId`, `oauthClientSecret`, and `oauthTokenRequestUrl` connection parameters to configure the authentication.
  - Added the ability to provide `oauthClientSecret` by setting the `SnowflakeDbConnection.OAuthClientSecret` property instead of providing it in a connection string.
- Added Programmatic Access Token authentication:

  - Added the `programmatic_access_token` authenticator.
  - Added the ability to specify the `token` parameter either in a connection string or by setting the `SnowflakeDbConnection.Token` property.
- Added validations for the `scheme`, `port`, and `host` connection properties.
- Added the ability to provide tokens by setting the `SnowflakeDbConnection.Token` property instead of providing them in a connection string.

### Bug fixes

- None.

## Version 4.4.1 (April 28, 2025)

### New features and improvements

- None.

### Bug fixes

- Fixed a Time-of-check Time-of-use (TOCTOU) race condition when checking access to Easy Logging configuration file. For more information, see [CVE-2025-46326](https://github.com/snowflakedb/snowflake-connector-net/security/advisories/GHSA-c82r-c9f7-f5mj).
- Fixed an issue with cancelling connecting with *CancellationTokenSource.CancelAsync()* that did not decrease the pool usage counter.

## Version 4.4.0 (April 10, 2025)

### New features and improvements

- Added an SSO token cache for external browser authentication and the `client_store_temporary_credential` parameter to indicate whether to use the SSO cache.
- Implemented and improved the file-based credentials cache for Linux, including enhanced token caching.

### Bug fixes

- Fixed case insensitivity for authenticators. Before the fix, the logic for `username_password_mfa` and `oauth` was not properly applied if authenticators used uppercase characters.
- Fixed an issue with passing null into a query parameter.
- Fixed an issue with reading tokens from the Windows Credential Manager, which was used for `username_password_mfa` authenticator. In some cases the value read from the credential manager could be too long.
- Made some small changes to credential manager implementations, such as changing some log levels and issuing a warning for too permissive cache directory permissions on Unix instead of changing the permissions automatically.
- Fixed the binding of `AnsiString` parameters to the `TEXT` type.
- Fixed loading structured or semi-structured data to a `DataTable`.

## Version 4.3.0 (January 29, 2025)

### New features and improvements

- Added support for configuring connection parameters in TOML files.
- Added an MFA token cache.
- Added support for GCP region-specific endpoints.
- Made encryption headers for files downloaded by GET be case insensitive.
- The driver was tested with .net9 framework.
- Extended documentation for checking CRL endpoints for Windows users.

### Bug fixes

- Improved security of intermediary files placed in OS temporary directories, which makes the files no longer world-readable. For more information, see [CVE-2025-24788](https://github.com/snowflakedb/snowflake-connector-net/security/advisories/GHSA-2mqw-rq5m-8hc8).
- Fixed an issue with handling null data in failed responses.
- Fixed an issue with logging diagnostic information.
- Fixed an issue with handling of spaces in the file path for PUT command with GCS (Google Cloud Storage).
- Fixed an issue with handling GCS endpoints without `https://` prefix.
- Fixed an issue with downloading files with a GET operation that don’t have the `SFC_DIGEST` property in their metadata.
- Fixed the ability to use `STDOUT` as the log path in Easy Logging feature.
