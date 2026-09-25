# Node.js Driver release notes for 2026

This article contains the release notes for the Node.js Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Node.js Driver updates.

See [Node.js Driver](/developer-guide/node-js/nodejs-driver) for documentation.

## Version 3.3.0 (September 3, 2026)

### Security fixes

- Restricted the `WORKLOAD_IDENTITY` authenticator to recognized Snowflake hosts (`*.snowflakecomputing.com`, `*.snowflakecomputing.cn`, and `*.snowflakecomputing.mil`). To extend the list of allowed hosts, use the `SNOWFLAKE_WIF_ALLOWED_HOST_SUFFIXES` environment variable.
- Improved OCSP response validation so that a response must correspond to the certificate being checked. Verification now selects the matching single response from the OCSP message instead of using the first one, and fails with `ERR_OCSP_RESPONSE_CERT_MISMATCH` when none matches. This applies to both live checks and cached responses.
- Fixed PrivateLink host detection using a substring match that could misclassify a host as a PrivateLink host.
- Changed cloud storage response logs to list header names instead of full header objects, which keeps header values out of the logs. Query strings are also trimmed from cloud storage URLs before they reach debug logs.
- Corrected the SAS token masking rule in debug logs and extended masking to cover the `X-Amz-Credential` and `X-Amz-Security-Token` URL parameters and the S3 SSE-C customer-key header.

## Version 3.2.0 (August 18, 2026)

### Deprecations

- Marked `RowStatement.fetchRows()` as deprecated. This method will be removed in the next major version. Use `streamRows()` instead.
- Removed the `getRowValue()` and `getRowValueAsString()` methods from the `Column` interface. These methods required an internal row representation that is never exposed publicly, so calling them on user-visible rows always threw a runtime error.

### New features and updates

- Improved CRL signature verification performance by about 100 times, from roughly 635 ms to roughly 6 ms per certificate revocation list in upstream testing. The driver now caches the raw CRL bytes and verifies the signature directly against them, instead of re-encoding the certificate list from the decoded CRL on every check. This is only on the connection path when certificate revocation checking is enabled.

### Bug fixes

- Fixed the TypeScript typing for `connection.fetchResult()`, which incorrectly required `sqlText` and omitted `queryId`.
- Fixed Azure PUT and GET file transfers failing on non-commercial Azure clouds.
- Fixed `compressFileWithGZIP` crashing the Node.js process with an unhandled stream `'error'` event when the source file for a `PUT` can’t be read.
- Fixed token cache key collisions in multi-account and multi-role scenarios.

## Version 3.1.0 (July 9, 2026)

### New features and updates

- Added the `workloadIdentityAwsUseOutboundToken` connection option (default `false`) that switches AWS workload identity attestation to STS `GetWebIdentityToken` JWTs. Snowflake recommends this method and might make it the default in a future release.
- Added a `customLogger` option to `snowflake.configure()` to route the driver’s log messages through your own logger (for example, winston, pino, or OpenTelemetry) instead of the built-in file or console logging.

### Bug fixes

- Reverted the unintentional breaking change from the [3.0.0 release](#label-nodejs-rn-3-0-0) that switched AWS workload identity attestation from SigV4 `GetCallerIdentity` to STS `GetWebIdentityToken`. AWS workload identity again defaults to `GetCallerIdentity`, and the new method is now opt-in with the `workloadIdentityAwsUseOutboundToken` connection option.
- Fixed Private Link OCSP proxy requests failing with `HTTP 405 Method Not Allowed` for certificates whose AIA OCSP URI contains a path component (for example, `oneocsp.microsoft.com/ocsp`).
- Fixed Node.js 24 compatibility by removing usage of the deprecated `util.isString` method, and added logging where this previously caused a silent failure.
- Fixed CRL validation failing with a `crl.tbsCertList.revokedCertificates is not iterable` error for CRLs that contain no revoked certificates.
- Fixed an unnecessary second PUT (stage re-resolution) per file during GCS uploads when the server scopes upload credentials with an access token.
- Fixed key-pair authentication ignoring `privateKeyPass` for an inline `privateKey`, so encrypted private keys can now be passed directly, just like with `privateKeyPath`.

## Version 3.0.0 (June 17, 2026)

### BCR (Behavior Change Release) changes

Beginning with version 3.0.0, the Node.js driver introduced the following breaking change:

- Dropped official support for Node.js version 18. The minimum supported Node.js version is now 20, and `engines.node` is set to `>=20`. This release might still run on Node.js 18 for now, but Snowflake no longer tests against it and won’t investigate or fix Node 18-only issues. Treat Node 18 as unsupported and migrate to a current Node.js LTS version.

### New features and updates

- Added the `browserResponseRenderer` connection option to customize the HTML response shown in the browser after `EXTERNALBROWSER` and `OAUTH_AUTHORIZATION_CODE` callbacks.
- Added the `tokenFilePath` connection option that reads the authentication token from a file when no `token` is provided.
- Added the `serverSessionKeepAlive` connection option that keeps the session alive on the server side when `connection.destroy()` is called. This option is useful when you want to close the local connection while keeping async queries running on the server.

### Bug fixes

- Fixed global URL detection incorrectly truncating account names that contain “global” (for example, `myorg-global`).
- Fixed the `noProxy` connection option and the `NO_PROXY` environment variable not bypassing the proxy for Private Link connections.
- Fixed interrupted streaming HTTP responses being treated as successful empty responses instead of errors, which could cause `streamRows()` to hang silently on large result sets.
- Fixed `LOCAL_FS` stage downloads writing to the wrong path by using the destination file’s base name, consistent with cloud stages.
- Fixed the `OAUTH_AUTHORIZATION_CODE` cold-connect lockout caused by a cached invalid refresh token. The bad token is now evicted and the full browser flow restarts.

## Version 2.4.3 (May 26, 2026)

### New features and updates

- Bumped `@aws-sdk/*` dependencies to version 3.1051.0 to address `fast-xml-builder` security vulnerabilities.

### Bug fixes

- Fixed the platform-detection probe not aborting within 200 ms on Bun.

## Version 2.4.2 (May 19, 2026)

### Bug fixes

- Destroyed S3 clients after use in `s3_util.js` (`getFileHeader`, `uploadFileStream`, `nativeDownloadFile`) to prevent keep-alive socket accumulation and memory leaks on long-lived pods.
- Fixed `deserializeConnection()` not deriving `accessUrl` or `host` from `account`, which caused it to fail with a missing `accessUrl` error when only `account` was provided.
- Fixed the `OAUTH_AUTHORIZATION_CODE` browser-popup loop caused by reauthentication opening a new browser window on every failed server response. This bug was a regression introduced in 2.4.1.

## Version 2.4.1 (May 12, 2026)

### New features and updates

- Reduced peak memory usage when streaming large result sets by reordering the chunk lifecycle to free the previous chunk before parsing the next one.
- Bumped axios to version 1.15.1 to address the deprecated `url.parse()` warning in Node.js 22+ and a set of security issues, including CVE-2025-62718.
- Pinned all `@aws-sdk/*` dependencies to their latest minor (patch floats only) to avoid breaking changes for supported Node.js versions (Node 18+).
- Removed the `browser-request` dependency and related dead code.
- Dropped the `uuid` dependency in favor of the Node.js built-in `crypto.randomUUID()`.

### Bug fixes

- Fixed file name pattern matching to not match dot-prefixed files or directories by default, aligning with standard glob behavior and the `dot: false` default. This bug was introduced in v2.3.3.
- Fixed the `OAUTH_AUTHORIZATION_CODE` cache not evicting entries on server `390303` errors.

## Version 2.4.0 (Apr 7, 2026)

### New features and updates

- Added the `browserRedirectPort` connection option to customize the port of the local server that receives the EXTERNALBROWSER authentication callback.
- Bumped `@aws-sdk/*` dependencies to address a `fast-xml-parser` vulnerability.
- Improved keep-alive HTTP agents with a 30-second idle socket timeout that proactively discards stale connections before the server closes them, preventing socket hang up and ECONNRESET errors.

### Bug fixes

- Fixed connection pools re-prompting browser authentication for every pooled connection when using EXTERNALBROWSER or OAUTH\_AUTHORIZATION\_CODE authenticators. The first connection now completes auth and caches tokens before subsequent pool connections start.
- Fixed session token renewal failing due to a malformed request, which caused long-running connections to disconnect instead of refreshing their expired session token.
- Fixed query context cache not being updated on failed queries, which could cause a stale cache when subsequent queries land on a different GS node.

## Version 2.3.6 (Mar 25, 2026)

### New features and updates

- Added support for every authenticator type (including external browser and Okta) in `connect()`, matching `connectAsync()`.
- Removed the `@google-cloud/storage` dependency. GCS transfers now use the JSON API directly. The `forceGCPUseDownscopedCredential` connection option has been removed as it is no longer needed.
- Updated the default `jsonColumnVariantParser` to fall back to eval-based parsing for non-JSON-compliant variant values (such as `undefined`, `NaN`, and `Infinity`), restoring pre-2.3.5 behavior while keeping `JSON.parse` as the primary parser.

### Bug fixes

- Fixed the `OAUTH_AUTHORIZATION_CODE` authenticator not honoring the `openExternalBrowserCallback` connection option.
- Fixed `createConnection()` and `createPool()` types to accept no arguments, matching the runtime behavior of loading configuration from `connections.toml`.
- Fixed the `account` field in the `ConnectionOptions` type to be optional, since it can be derived from `accessUrl` or `host`.
- Fixed external browser SSO authentication crashing when the SSO URL request returns a server-side error.

## Version 2.3.5 (Mar 17, 2026)

### New features and updates

- Added the ability to skip token file permission checks by using the `SF_SKIP_TOKEN_FILE_PERMISSIONS_VERIFICATION` environment variable.
- Added Node 18+ to engines, which is the minimum officially supported version since the 2.x release.
- Added the `PLATFORM` field to `login-request` telemetry.
- Added request retries to previously uncovered query execution paths.
- Added the `rowStreamHighWaterMark` connection option to control how many rows are buffered when streaming query results through `statement.streamRows()`.
- Added a warning when converting query results to JavaScript numbers with precision loss.
- Added snake\_case key support when loading `connections.toml` through `createConnection()` with no arguments.
- Exported the `normalizeConnectionOptions()` utility to convert snake\_case connection keys to camelCase, with key aliases and acronym overrides.
- Added the `LIBC_FAMILY` and `LIBC_VERSION` fields to `login-request` telemetry.
- Added the `crlDownloadMaxSize` configuration option to enforce a maximum response size limit when downloading CRL files.
- Added RSASSA-PSS signature verification support for CRL validation.
- Improved error details when OAuth fails.
- Changed the default `jsonColumnVariantParser` to `JSON.parse`.
- Updated Linux GNU minicore binaries to target glibc 2.18 for broader compatibility with older Linux distributions.

### Bug fixes

- Fixed OAuth crashing when using bundlers.
- Fixed `Binds` typing to allow readonly arrays.
- Fixed the `connectAsync()` method resolving before the connection is completed.
- Fixed incorrect handling of a callback argument that should be optional in `connect()` and `connectAsync()`.
- Fixed a bug where an invalid JWT was generated if a user accidentally set both the account and the host in the configuration.
- Fixed a bug where parsing the JSON media type failed when it included an optional parameter from Microsoft Identity Platform v2.0 tokens, causing the OAuth Client Credentials flow to fail.
- Fixed `disableSamlUrlCheck` typing to use the correct casing: `disableSamlURLCheck`.
- Fixed `getDefaultCacheDir()` crashing in environments where no user home directory is configured by falling back to `os.tmpdir()`.
- Fixed `SF_OCSP_RESPONSE_CACHE_DIR` not being used directly as the OCSP cache directory.
- Fixed bugs in `noProxy` and `NO_PROXY` handling:

  - The `.domain.com` wildcard format was not correctly matching the destination host.
  - `.` was incorrectly matching as any character instead of a literal dot.
  - Partial strings were incorrectly matching instead of requiring a full destination match.
- Fixed CRL ADVISORY mode to log failures at the warn level instead of debug.
- Fixed OAuth Authorization Code reauthentication not using the refreshed access token when the cached access token is expired.
- Fixed OAuth Authorization Code refresh token being removed from cache when the IdP does not return a new one.
- Fixed an unhandled promise rejection when the server returns malformed query responses.

## Version 2.3.4 (Feb 9, 2026)

### New features and updates

- Reduced memory usage during PUT operations.
- Added `APPLICATION_PATH` to `login-request` telemetry.
- Added Linux distribution details parsed from `/etc/os-release` to `login-request` telemetry.
- Bumped axios to version 1.13.4 to address a bug in axios interceptors.
- Bumped other dependencies to their latest minor versions.

### Bug fixes

- Fixed inconsistent retry behavior across HTTP requests and ensured all recoverable failures are properly retried.
- Fixed invalid OAuth scope when `role` and `oauthScope` are missing from the connection configuration.
- Fixed `APPLICATION` field not being passed from the connection configuration to `login-request` telemetry.
- Fixed build errors in bundlers caused by the `minicore` module.
