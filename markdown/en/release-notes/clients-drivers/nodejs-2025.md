# Node.js Driver release notes for 2025

This article contains the release notes for the Node.js Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Node.js Driver updates.

See [Node.js Driver](/developer-guide/node-js/nodejs-driver) for documentation.

## Version 2.3.3 (December 11, 2025)

### New features and updates

- None.

### Bug fixes

- Replaced the `glob` dependency used in PUT queries with a custom wildcard matching implementation to address security issues.
- Fixed misleading debug messages during login requests.
- Fixed a bug in the build script that failed to include minicore binaries in the `dist` folder.

## Version 2.3.2 (December 08, 2025)

### New features and updates

- Added support for Red Hat Enterprise Linux (RHEL) 9.
- Added support for Node.js version 24.
- Included a shared library to collect telemetry to identify and prepare testing platforms for native node addons.

### Bug fixes

- Fixed the TypeScript definition for `getResultsFromQueryId` where `queryId` should be required and `sqlText` should be optional.
- Bumped the dependency `glob` to address [CVE-2025-64756](https://nvd.nist.gov/vuln/detail/CVE-2025-64756).
- Fixed a regression introduced in version 2.3.1 where `SnowflakeHttpsProxyAgent` was instantiated without the `new` keyword, breaking the driver when both OCSP was enabled and the `HTTP_PROXY` environment variable was used to set the proxy. This bug did not affect `HTTPS_PROXY`.

## Version 2.3.1 (October 09, 2025)

### New features and updates

- Added the `workloadIdentityAzureClientId` configuration option, allowing you to customize the Azure Client for `WORKLOAD_IDENTITY` authentication.
- Added the `workloadIdentityImpersonationPath` configuration option for `authenticator=WORKLOAD_IDENTITY`, allowing workloads to use service account impersonation.

### Bug fixes

- Fixed a regression causing PUT operations to encrypt files with the wrong `smkId`.

## Version 2.3.0 (September 30, 2025)

Warning

This release contained a serious regression, and was unpublished. Update to version 2.3.1 or later.

### New features and updates

- Implemented a new CRL (Certificate Revocation List) checking mechanism.

  Enabling CRLs improves security by checking for revoked certificates during the TLS handshake process. For more information, see the [Replacing OCSP with CRL as the method of certificate revocation checking](https://community.snowflake.com/s/article/Replacing-OCSP-with-CRL-as-the-method-of-certificate-revocation-checking) Knowledge Base article.

  This feature is disabled by default. For information on enabling this feature, see [Certificate revocation list (CRL) options](/developer-guide/node-js/nodejs-driver-options#label-nodejs-crl-validation-options). We recommend you test this feature in advisory mode before enabling it in production.

### Bug fixes

- Improved debug logs when downloading query result chunks.
- Fixed missing error handling in `getResultsFromQueryId()`.
- Fixed invalid transformation of `null` values to `""` when using stage binds.
- Extended typing of `Bind`.

## Version 2.2.0 (August 13, 2025)

### New features and updates

- Added support for Workload Identity Federation in the AWS, Azure, Google Cloud, and Kubernetes platforms.

  - Added the `workloadIdentityProvider` connection parameter.
  - Added `WORKLOAD_IDENTITY` to the values for the `authenticator` connection parameter.
- Added the `queryTag` connection parameter to set the `QUERY_TAG` session parameter.

### Bug fixes

- Fixed a network error when connecting with an expired OAuth access token.
- Fixed the OAuth Authorization Code’s default value for redirect URI by removing a trailing / (slash) to be compliant with RFC 6749 Section 3.1.2.
- Improved errors for GET commands.

## Version 2.1.3 (July 21, 2025)

### New features and updates

- None.

### Bug fixes

- Fixed an issue with using the Google Cloud Platform (GCP) XML API when `useVirtualUrl=true`.
- Fixed a permission check for `.toml` configuration files.
- Fixed unhandled resources after creating a connection to prevent the process from terminating when using external browser authentication.
- Fixed an issue with `oauthEnableSingleUseRefreshTokens` in the authorization code flow.

## Version 2.1.2 (July 10, 2025)

### New features and updates

- None.

### Bug fixes

- Fixed a TypeScript error that was introduced in version 2.1.1.

## Version 2.1.1 (July 03, 2025)

### Private Preview (PrPr) features

Added support for Workload Identity Federation in the AWS, Azure, GCP, and Kubernetes platforms.

Disclaimer:

- This feature can only be accessed by setting the `SF_ENABLE_EXPERIMENTAL_AUTHENTICATION` environment variable to `true`.
- You should use this feature only with non-production data.
- This PrPr feature is not covered by Support. However, the Product and Engineering teams are available during the PrPr phase.
- Please contact your account team for participation and documentation.

### New features and updates

- Removed token caching for Client Credentials authentication.

### Bug fixes

- Corrected an issue where `Util.getProxyFromEnv` incorrectly assumed HTTPS, causing `HTTP_PROXY` values to be ignored for HTTP traffic (port 80).
- Improved `extractQueryStatus` to handle cases where `getQueryResponse` returns a null response, preventing occasional breaks.
- Added `ErrorCode` to the core instance.

### Additional notes

- This release introduces TypeScript for development. The npm package contains compiled JavaScript code that contains no anticipated breaking changes for driver users.

## Version 2.1.0 (May 11, 2025)

### New features and updates

- Added support for OAuth 2.0 Authorization Code Flow and OAuth 2.0 Client Credentials Flow.

  - For OAuth 2.0 Authorization Code Flow:

    - Added the `oauthClientId`, `oauthClientSecret`, `oauthAuthorizationUrl`, `oauthTokenRequestUrl`, and `oauthScope` parameters.
    - Added the `OAUTH_AUTHORIZATION_CODE` parameter for the parameter authenticator.
  - For OAuth 2.0 Client Credentials Flow:

    - Added the `oauthClientId`, `oauthClientSecret`, `oauthTokenRequestUrl`, and `oauthScope` parameters.
    - Added the `OAUTH_CLIENT_CREDENTIALS` parameter for the parameter authenticator.
- Added support for virtual-style domains.
- Implemented and improved the file-based credentials cache for Linux, including enhanced token caching.

### Bug fixes

- None

## Version 2.0.4 (April 28, 2025)

### Private Preview (PrPr) features

- Implemented support for Programmatic Access Tokens authentication.

Disclaimer:

- These features can only be accessed by setting `SF_ENABLE_EXPERIMENTAL_AUTHENTICATION` environment variable to `true`.
- You should use these features only with non-production data.
- These PrPr features are not covered by Support. However, the Product and Engineering teams are available during the PrPr phase.
- Please contact your account team for participation and documentation.

### New features and updates

- Upgraded axios to version 1.8.2+.

### Bug fixes

- Fixed a Time-of-check Time-of-use (TOCTOU) race condition when checking access to the Easy Logging configuration file. For more information, see [CVE-2025-46328](https://github.com/snowflakedb/snowflake-connector-nodejs/security/advisories/GHSA-wmjq-jrm2-9wfr).
- Fixed OCSP response cache entries not being refreshed properly.

## Version 2.0.3 (March 13, 2025)

### New features and updates

- None

### Bug fixes

- Fixed an issue with promise rejection for file upload errors.

## Version 2.0.2 (January 29, 2025)

### New features and updates

- Added support for regional Google Cloud Storage endpoints.
- Added support for endpoints without protocols for GCS.
- Updated the following dependencies:
  - azure/storage-blob to version 12.26.x,
  - aws-sdk/client-s3 to version 3.726.0,
  - smithy/node-http-handler to version 4.0.1

### Bug fixes

- Fixed the verification of the token caching file permissions and its owner when authentication is set to `EXTERNALBROWSER` or `USERNAME_PASSWORD_MFA`. For more information, see [CVE-2025-24791](https://github.com/snowflakedb/snowflake-connector-nodejs/security/advisories/GHSA-xfhv-wqj6-rx99).
- Fixed the `FileAndStageBindStatement` type in the typings file.
- Fixed an issue with aborting requests and inconsistent request methods in `HttpClient`.
- Fixed an issue with the proxy configuration settings used for sending requests to a GCS bucket.
