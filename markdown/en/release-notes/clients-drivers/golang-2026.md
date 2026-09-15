# Go Snowflake Driver release notes for 2026

This article contains the release notes for the Go Snowflake Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Go Snowflake Driver updates.

See [Go Snowflake Driver](/developer-guide/golang/go-driver) for documentation.

## Version 2.2.0 (Sep 03, 2026)

### Security fixes

- Restricted the `WORKLOAD_IDENTITY` authenticator to recognized Snowflake hosts (`*.snowflakecomputing.com`, `*.snowflakecomputing.cn`, and `*.snowflakecomputing.mil`), normalizing the host before matching. The `SNOWFLAKE_WIF_ALLOWED_HOST_SUFFIXES` environment variable can additively extend the list of recognized hosts.
- Azure workload identity federation requests now URL-encode the resource and client ID query parameters, so their values can’t alter the rest of the request URL.
- The Azure `IDENTITY_ENDPOINT` must now resolve to a loopback or link-local address before the driver attaches the `IDENTITY_HEADER` value to the request.
- Account identifier and region values supplied in the DSN are now validated as well-formed URL-authority components before being used to construct driver URLs. OCSP cache-server and retry URLs are now built using Go’s `net/url` package instead of direct string formatting.
- Improved OCSP response validation to correctly distinguish transient network failures from definitive certificate status results, so a definitive result is always honored regardless of the `ocspFailOpen` setting.
- Extended secret masking in debug logs to cover the S3 SSE-C customer-key header and the `X-Amz-Credential` and `X-Amz-Security-Token` URL query parameters.
- HTTP response headers, including the chunk-header debug line, are now logged as header names only, without their values, everywhere the driver previously logged full header collections. This prevents session tokens, storage credentials, and SSE-C customer keys from appearing in debug logs.
- The TOML connection configuration loader now logs only setting names, not their values, when reporting a parsing error.
- Corrected the SAS token masking pattern in debug logs so signed URL query parameters are fully masked.
- Corrected the connection token masking pattern in debug logs to properly match and mask Snowflake session tokens that contain a colon (for example, `ver:1-hint:...`).

### New features and updates

- Added the `WorkloadIdentityAwsUseOutboundToken` configuration option (DSN field `workloadIdentityAwsUseOutboundToken`) to produce the AWS workload identity federation attestation as an STS `GetWebIdentityToken` JWT instead of the default signed `GetCallerIdentity` request envelope.
- Added the `CleanupTimeout` configuration option (DSN field `cleanupTimeout`, in seconds) to bound how long post-cancellation cleanup can run.
- Increased the CRL disk cache removal delay to 7 days.
- Added support for loading a private key from a `connections.toml` file.
- Added support for Go 1.27.
- Dropped support for Go 1.24. The minimum supported Go version is now 1.25.
- Added the `SNOWFLAKE_MIN_TLS_VERSION` environment variable to enforce a minimum TLS version for all connections.

### Bug fixes

- Fixed token cache key collisions that could occur across multiple accounts sharing an identity provider, or across multiple roles, by switching to a versioned, SHA-256-hashed cache key that includes the token type.
- Fixed a nil pointer dereference panic when the driver encountered a corrupt or malformed OCSP cache key, whether from the remote OCSP cache server or the local cache file.
- Fixed `WithFileGetStream` returning corrupt or wrong-file bytes when a `GET` pattern matched more than one file. A multi-file match now returns the new `ErrGetStreamMultipleFiles` error instead of an unpredictable mix of file contents.
- The driver no longer attempts to fetch S3 bucket accelerate configuration for Snowflake-internal stages, since that permission isn’t granted for those stages.
- Fixed gosnowflake creating a `gosnowflake-cgo` directory under the system temp directory at package import time, even when the driver was never used (for example, when imported only as a transitive dependency). Minicore now loads lazily when the driver is first referenced instead of at package initialization.
- Fixed `GET` from a `LOCAL_FS` stage downloading 0 files and returning a `264011: not implemented` error. Downloads from cloud stages were unaffected.
- Fixed `NUMBER` columns with a non-zero scale losing precision when a value needed more significant digits than a binary float’s mantissa could hold. For example, a `NUMBER(20,10)` column holding `1234567890.1234567890` returned `1234567890.1234567889`. The `WithHigherPrecision` option is unaffected and continues to return a 64-bit `*big.Float`.
- Fixed `ArrowBatch.WithContext` being able to unintentionally change the conversion options (timestamp handling, higher precision, UTF-8 validation) applied to an already-created batch. These options are now captured when the batch is created and are no longer re-read from a later `WithContext` call.
- Fixed proxy configuration for a literal IPv6 `ProxyHost`, which previously produced an unparseable proxy URL.
- Fixed the `region` parameter overriding an explicitly provided `host` value (for example, `host=myacct.snowflakecomputing.com` combined with `region=us-east-1` incorrectly became `myacct.us-east-1.snowflakecomputing.com`). An explicit host now takes precedence.

### Internal changes

- Migrated from the deprecated `github.com/aws/aws-sdk-go-v2/feature/s3/manager` package to `github.com/aws/aws-sdk-go-v2/feature/s3/transfermanager`.
- Modernized Go syntax idioms throughout the codebase now that the minimum supported Go version is 1.25.
- Updated AWS SDK dependencies:
  - `github.com/aws/aws-sdk-go-v2` from v1.38.1 to v1.43.0
  - `github.com/aws/aws-sdk-go-v2/config` from v1.27.11 to v1.32.31
  - `github.com/aws/aws-sdk-go-v2/credentials` from v1.17.11 to v1.19.30
  - `github.com/aws/aws-sdk-go-v2/feature/ec2/imds` from v1.16.1 to v1.18.31
  - `github.com/aws/aws-sdk-go-v2/service/s3` from v1.53.1 to v1.106.0
  - `github.com/aws/aws-sdk-go-v2/service/sts` from v1.28.6 to v1.45.0
  - `github.com/aws/smithy-go` from v1.22.5 to v1.27.4

## Version 2.1.0 (Jun 08, 2026)

### New features and updates

- Added the `SF_DISABLE_OCSP_CHECKS` environment variable as an additional option to override the default behavior of OCSP checks, alongside the existing `DisableOCSPChecks` configuration option. The environment variable is explicitly refused when OCSP fail-closed mode is active.
- Added the `ArrowStreamBatch.Reset()` method, which closes any existing stream and clears the cached reader. This method lets callers retry `GetStream` after a mid-stream failure (such as a TCP RST) without re-executing the entire query. Inline (`RowSetBase64`) batches are restored from cached bytes on reset.
- Added one in-band telemetry record per successful login that describes which connection-identifier fields the user supplied (`account_provided`, `account_with_region`, `account_org_provided`, `region_provided`, and `host_provided`). No hostname or account value is included. This record is gated by the existing server-side `CLIENT_TELEMETRY_ENABLED` parameter and can also be disabled locally by setting `SF_TELEMETRY_DISABLE_CONNECTION_SHAPE` to `true`. This telemetry collection is time-boxed and will be removed in a future release.

### Bug fixes

- Fixed a stale OCSP cache `.lck` directory permanently blocking cache writes, which forced online OCSP validation when OCSP is enabled (the default). The driver now uses `os.RemoveAll` instead of `os.Remove` for stale lock recovery.
- Fixed regular chunk downloader reads so that canceling the query context now interrupts stalled chunk downloads and wakes waiting row readers instead of hanging on the HTTP body read.
- Fixed `QueryArrowStream` chunk reads so that canceling the query context now interrupts stalled Arrow stream downloads and reports the cancellation instead of hanging on the HTTP body read.
- Fixed `baseName` silently dropping files whose name ends with a dot (such as `myfile.txt.`), which caused PUT uploads to discard such files without an error.
- Improved the error message when `Host` is incorrectly configured with a URL scheme (such as `https://myorg-myaccount.snowflakecomputing.com`). Previously, this produced a cryptic `260004: failed to parse a port number` error.
- Fixed the minicore build on OpenBSD by skipping the `-ldl` linker flag, because libdl is not a separate library on OpenBSD (`dlopen` and `dlsym` are provided by libc).

### Internal changes

- Introduced the `SKIP_FILE_PERMISSIONS_VERIFICATION` environment variable to allow bypassing file permissions checks for `connections.toml` and the credential cache. This option is useful for environments where strict permissions can’t be set.
- Added support for `SPCS_TOKEN` in the login request. When the driver detects that it’s running inside a Snowpark Container Services workload (using the `SNOWFLAKE_RUNNING_INSIDE_SPCS` environment variable), it reads an opaque service token from `/snowflake/session/spcs_token` on every login and attaches it to the login-request payload as `SPCS_TOKEN`. Read failures are logged at the warn level and don’t affect login.
- Minicore binaries for Windows and macOS are now signed. The content is the same.

## Version 2.0.2 (Apr 28, 2026)

### New features and updates

- Added the `QueryResultFormatProvider` interface, which exposes the server-reported query result format (Arrow or JSON) from `QueryArrowStream`. This interface enables callers to distinguish Arrow IPC from JSON responses before interpreting batch streams.

### Bug fixes

- Fixed an issue where the `Account` field was empty when connecting with programmatic `Config` and `database/sql.Connector`. The driver now derives `Account` from the first DNS label of `Host` when it matches the Snowflake hostname pattern.
- Fixed the PAT (Programmatic Access Token) authenticator to properly require the `Token` or `TokenFilePath` field. Previously, the authenticator would silently accept the `Password` field but never forward it to the authentication service.
- Fixed the logger reporting incorrect source locations when called without `WithContext`.
- Fixed GCP workload identity federation (WIF) attestation to use hostname `metadata.google.internal` instead of the IPv4 link-local address, enabling support for IPv6-only GCP VMs.
- Fixed query failures on large inline results (such as 64 MB LOBs) caused by truncated HTTP response bodies. The driver now retries the query when `json.Decoder` returns `io.ErrUnexpectedEOF`, reusing the same request ID to retrieve the cached result from Snowflake.

## Version 2.0.1 (Apr 08, 2026)

### Bug fixes

- Reduced the default `CrlDownloadMaxSize` setting from 200 MB to 20 MB to prevent potential out-of-memory errors.
- Fixed an issue where parameter values could change across connections in the same connection pool.
- Fixed Azure multi-part file uploads to properly populate the blob content-MD5 property.
- Fixed 403 errors from Google Cloud Storage PUT queries on versioned stages.
- Fixed the query context cache not being updated for failed queries, which could result in stale session data.
- Improved connection handling performance by optimizing parameter synchronization.

### Internal changes

- Moved configuration to a dedicated internal package.
- Modernized Go syntax idioms throughout the codebase.
- Added libc family, version, and dynamic linking marker to client environment telemetry.
- Updated dependencies to address security vulnerabilities:

  - `golang.org/x/crypto` from v0.41.0 to v0.46.0
  - `golang.org/x/net` from v0.43.0 to v0.48.0
  - `golang.org/x/oauth2` from v0.30.0 to v0.34.0
  - `golang.org/x/sys` from v0.35.0 to v0.40.0
  - `golang.org/x/mod` from v0.27.0 to v0.30.0
  - `golang.org/x/sync` from v0.16.0 to v0.19.0
  - `golang.org/x/term` from v0.34.0 to v0.38.0
  - `golang.org/x/text` from v0.28.0 to v0.32.0
  - `golang.org/x/tools` from v0.36.0 to v0.39.0
  - `google.golang.org/grpc` from v1.73.0 to v1.79.3
  - `google.golang.org/protobuf` from v1.36.6 to v1.36.10
  - OpenTelemetry packages from v1.37.0 to v1.40.0
- Removed pointer indirection from query context cache in `snowflakeConn`.

## Version 1.9.1 (Apr 08, 2026)

### New features and updates

- Added support for Go 1.26 and dropped support for Go 1.23.

### Bug fixes

- Fixed minicore crashes (SIGFPE) on fully statically linked Linux binaries by detecting static linking via ELF PT\_INTERP inspection and skipping `dlopen` gracefully.

### Internal changes

- Added libc family, version, and dynamic linking marker to client environment telemetry.

## Version 2.0.0 (Mar 03, 2026)

### BCR (Behavior Change Release) changes

- Removed `RaisePutGetError` from `SnowflakeFileTransferOptions` to ensure errors are raised for PUT/GET operations.
- Removed `GetFileToStream` from `SnowflakeFileTransferOptions`. Use `WithFileGetStream` to automatically enable file streaming for GET operations.
- Removed `WithOriginalTimestamp`. Use `WithArrowBatchesTimestampOption(UseOriginalTimestamp)` instead.
- Removed the `ClientIP` field from the `Config` struct. This field was never used and is not needed for any functionality.
- Removed the `InsecureMode` field from `Config` struct. Use `DisableOCSPChecks` instead.
- Removed the `DisableTelemetry` field from the `Config` struct. Use the `CLIENT_TELEMETRY_ENABLED` session parameter instead.
- Removed the stream chunk downloader. Use the default downloader instead.
- Removed `SnowflakeTransport`. Use `Config.Transporter`, or simply register your own TLS configuration with `RegisterTLSConfig` if you just need a custom root certificates set.
- Renamed `WithFileStream` to `WithFilePutStream` for consistency.
- Renamed the `KeepSessionAlive` field in the `Config` struct to `ServerSessionKeepAlive` for consistency with other drivers.
- The `Array` function now returns an error for unsupported types.
- `WithMultiStatement` no longer returns an error.
- Combined `WithMapValuesNullable` and `WithArrayValuesNullable` into the single `WithEmbeddedValuesNullable` option.
- Hid the streaming chunk downloader. It will be removed completely in a future release.
- The maximum number of chunk download goroutines is now configured with the `CLIENT_PREFETCH_THREADS` session parameter.
- Fixed a typo in the `GOSNOWFLAKE_SKIP_REGISTRATION` environment variable.
- Unexported `MfaToken` and `IdToken`.
- Arrow batches changes:

  - Arrow batches have been extracted to a separate package, which should significantly reduce the compilation size for those who don’t need arrow batches (~34MB -> ~18MB).
  - Removed `GetArrowBatches` from `SnowflakeRows` and `SnowflakeResult`. Use `arrowbatches.GetArrowBatches(rows.(SnowflakeRows))` instead.
  - Migrated the following functions:
    - `sf.WithArrowBatchesTimestampOption` to `arrowbatches.WithTimestampOption`
    - `sf.WithArrowBatchesUtf8Validation` to `arrowbatches.WithUtf8Validation`
    - `sf.ArrowSnowflakeTimestampToTime` to `arrowbatches.ArrowSnowflakeTimestampToTime`
- Logging changes:

  - Removed the Logrus logger and migrated to slog.
  - Simplified the `SFLogger` interface.
  - Added the `SFSlogLogger` interface for setting a custom slog handler.

### New features and updates

- Added support for Go 1.26, and dropped support for Go 1.23.
- Added support for FIPS-only mode.

### Bug fixes

- Added a panic recovery block for stage file upload and download operations.
- Fixed a WIF metadata request from an Azure container that manifested as an HTTP 400 error.
- Fixed a SAML authentication port validation bypass in `isPrefixEqual` where the second URL’s port was never checked.
- Fixed a race condition in the OCSP cache clearer.
- The `context.Context` query is now propagated to cloud storage operations for PUT and GET queries, allowing for better cancellation handling.
- Fixed minicore crashes (SIGFPE) on fully statically linked Linux binaries by detecting static linking via ELF PT\_INTERP inspection and skipping `dlopen` gracefully.

## Version 1.19.0 (Feb 03, 2026)

### New features and updates

- Exposed `tokenFilePath` in the `Config` struct, in addition to the existing DSN option.
- `tokenFilePath` is now read for every new connection, not only once at driver startup.
- Added support for identity impersonation when using workload identity federation.
- Added the ability to disable minicore from loading at compile time using the `-tags minicore_disabled` parameter.

### Bug fixes

- Fixed an issue with getting files from an unencrypted stage.
- Fixed the minicore file name gathering in client environment.
- Fixed path escaping for GCS URLs that manifested in 403 responses from GCS when a file or directory contained spaces.
- Fixed leaking file descriptors when uploading files to stages (especially in GCS).
