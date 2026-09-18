# .NET Driver release notes for 2026

This article contains the release notes for the .NET Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for .NET Driver updates.

See [.NET Driver](/developer-guide/dotnet/dotnet-driver) for documentation.

## Version 6.2.0 (September 17, 2026)

### New features and improvements

- Added `ExecuteDbDataReaderWithMemoryStream` method on `SnowflakeDbCommand` for uploading data from an in-memory `MemoryStream` via PUT without writing to disk. When `AUTO_COMPRESS=TRUE`, compression is performed in-memory by default; set `SF_PUT_DISABLE_IN_MEMORY_COMPRESS=true` to use temporary files instead.
- `FILE_TRANSFER_MEMORY_THRESHOLD` connection parameter now also controls the in-memory buffer limit during PUT encryption. When the encrypted payload exceeds this threshold, the driver spills to a temporary file. Set to `-1` to keep encryption entirely in memory (no disk spill). Defaults to 1 MB when not specified.
- Added the opt-in `WORKLOAD_IDENTITY_HOST` connection property, overriding the AWS STS endpoint used by `WORKLOAD_IDENTITY` authentication. It accepts a bare host or a full URL and applies no partition or domain-suffix mapping; the value is normalized (the scheme defaults to `https`, a default port and trailing slashes are dropped) and applies to every AWS attestation flow. When unset - the default - the regional endpoint is used exactly as before. It is rejected for non-AWS workload identity providers.

### Bug fixes

- Fixed `ExecuteReader(CommandBehavior.SchemaOnly)` to send `describeOnly=true` to the server, returning column metadata without executing the query. Previously the `CommandBehavior` parameter was ignored.

## Version 6.1.0 (September 3, 2026)

### New features and improvements

- Extended log secret-masking to cover additional cloud-storage URL query parameters, and routed the telemetry loggers through the shared masking pipeline.
- Restricted the `WORKLOAD_IDENTITY` authenticator to recognized Snowflake hosts (`*.snowflakecomputing.com`/`.cn`/`.mil`), normalizing the host before a suffix-anchored match. The `SNOWFLAKE_WIF_ALLOWED_HOST_SUFFIXES` environment variable additively extends the recognized-host list.
- Performance improvements in parsing query status for given result set.
- NuGet package now publishes `.snupkg` symbol packages, enabling source-link debugging for consumers.
- Added configurable timeouts for chunk download stream reads. `SF_CHUNK_DOWNLOAD_IDLE_TIMEOUT` (default 180s) detects stalled connections between reads; `SF_CHUNK_DOWNLOAD_READ_TIMEOUT` (default disabled) sets a per-read deadline. Both are configured in seconds; set to `0` to disable.

### Bug fixes

- Token cache file on Linux/macOS is now written as UTF-8 without a BOM for cross-driver compatibility.
- Fixed `TIMESTAMP_TZ` sub-hour timezone offsets (e.g. +05:30) being truncated to whole hours in JSON result format.

## Version 6.0.0 (August 10, 2026)

### Breaking Changes

- Surface-level connection exceptions occurring in `OpenAsync` and `CloseAsync` are now thrown directly, without wrapping inside `AggregateException`.
- A fault that occurs while closing a connection now leaves it in the `Broken` state instead of `Closed`.
- A fault that occurs while opening a connection with `OpenAsync` no longer leaves the connection stuck in the `Connecting` state. Retry patterns on such failures are now possible without recreating the connection object.

### New features and improvements

- Added `CancellationToken` support to chunk download and parsing pipeline. Query result fetching now respects cancellation during both JSON and Arrow chunk parsing.
- Reduced synchronization context capture in the library, minimizing the risk of deadlocks across different code execution paths.
- Replaced NUnit tests with Xunit to modernize and stabilize existing CI/CD setup.
- Improved handling of certificate serial number matching and performance of CRL checking.
- AWS Workload Identity Federation attestation now defaults to a SigV4-presigned `GetCallerIdentity` request and attestation through the STS `GetWebIdentityToken` path (returning a signed JWT) is available as an opt-in by setting the `SNOWFLAKE_ENABLE_AWS_WIF_OUTBOUND_TOKEN=true` environment variable.
- `OpenAsync` method of `SnowflakeDbConnection` now throws the original exception on failure instead of wrapping it in an `AggregateException`.
- `CloseAsync` now throws the original exception on failure instead of wrapping it in an `AggregateException`.
- Upgraded `AWSSDK.S3` dependency. Now getting the object header invokes a HEAD S3 call instead of GET.
- Added `AllowNumberOverflowAsString` connection property. When set to `true`, numeric values that exceed the range of `System.Decimal` (or a narrower integer type) are returned as strings from `GetValue()` instead of throwing `OverflowException`.

### Bug fixes

- Fixed non-Windows builds with added NativeLibrary items in their transitively built projects that were no longer available to copy to the output directory.
- `OpenAsync` method of `SnowflakeDbConnection` now resets its state to `Closed` on failures.
- `CloseAsync` method of `SnowflakeDbConnection` now resets its state to `Closed` on cancellation and `Broken` on failures.
- Fixed session creation token leak when `GetSessionAsync` is cancelled.
- Fixed incorrect DateTime conversion for timestamps preceding Unix epoch (1970-01-01) when fractional seconds are present.
- Fixed an unnecessary second PUT (stage re-resolution) per file during GCS uploads when the server scopes upload credentials with an access token.

## Version 5.7.0 (June 12, 2026)

### New features and improvements

- Improved input handling in `ChangeDatabase` by using parameterized queries.
- Improved input validation in `QueryResultsAwaiter` with stricter UUID format checks.

### Bug fixes

- Fixed `OverflowException` when converting REST response with master token validity more than approximately 9.1 hours.
- Added path traversal protection for file downloads: destination paths are now validated against the target base directory before writing.
- Replaced use of `System.Random` with a cryptographically secure random number generator in the authenticator challenge/proof key generation and file transfer encryption key/IV generation.

## Version 5.6.0 (May 20, 2026)

### New features and improvements

- Added .NET 10 support. Changed `LangVersion` to C# 13.
- Added client-side telemetry instrumentation using `System.Diagnostics.Activity` (OpenTelemetry-compatible). When `CLIENT_TELEMETRY_ENABLED=true` (the default), the driver automatically instruments all command executions and their async variants, and sends telemetry data to Snowflake’s `/telemetry/send` endpoint. Activities are enriched with session context (warehouse, role, database, session ID) and report success or error status with exception details.
- Added the public `StartActivity` extension method on `SnowflakeDbCommand` for creating custom client-defined telemetry activities. Custom activities use a separate activity source (`Client_custom_activity`).
- Added `DbType.AnsiStringFixedLength` to the set of types mapped to Snowflake `TEXT`, matching existing support for `AnsiString`, `String`, and `StringFixedLength`.
- Extended login-request telemetry with libc detection (`LIBC_FAMILY`, `LIBC_VERSION`). On Linux, the driver now reports whether the runtime uses glibc and includes the library version.
- Reduced the default maximum CRL download size from 200 MB to 20 MB, aligning with other Snowflake drivers.

### Bug fixes

- Fixed handling of transient server issues that resulted in sending a truncated JSON response.
- Fixed an issue where connections with sessions that no longer existed on the server were reused from the pool, which previously caused repeated failures until the connection expired on its own. These connections are now detected and removed from the pool.

## Version 5.5.0 (April 13, 2026)

### New features and improvements

- The driver now includes `SPCS_TOKEN` in login requests when running inside a Snowpark Container Services (SPCS) container (detected via the `SNOWFLAKE_RUNNING_INSIDE_SPCS` environment variable).
- Extended login-request telemetry with cloud platform and environment detection (AWS Lambda, EC2, Azure VM/Functions, GCE/Cloud Run, GitHub Actions). Detection runs once at startup in the background within a 200ms timeout. You can disable this feature by setting the `SNOWFLAKE_DISABLE_PLATFORM_DETECTION` environment variable.
- Added the `workloadIdentityImpersonationPath` connection parameter for `authenticator=WORKLOAD_IDENTITY`, which allows workloads to authenticate as a different identity through transitive service account impersonation.
- Added the `HonorSessionTimezone` connection parameter (default: `false`). When set to `true`, `TIMESTAMP_LTZ` values honor the session TIMEZONE parameter (set using ALTER SESSION SET TIMEZONE) instead of the local machine timezone. This will become the default behavior in a future major release.

### Bug fixes

- Fixed an issue where idle sessions were not evicted from the connection pool when closing them fails.
- Fixed an issue where sessions that receive HTTP 401 during query execution were returned to the connection pool.
- Fixed `GetResultsFromQueryIdAsync` not aborting queries on the server when a `CancellationToken` is cancelled. Previously, only client-side polling stopped while queries continued running on Snowflake.
- Fixed Azure GET (download) operations incorrectly reporting an `UPLOADED` result status instead of `DOWNLOADED` when the server returns presigned URLs for an encrypted stage.
- Fixed query context cache not being updated when the server returns `queryContext` in a failed query response.
- Improved CRL issuer validation: issuer names are now compared using DER encoding (avoiding string-form mismatches such as `S=` vs `ST=`), and the CRL’s Authority Key Identifier is verified against the issuing CA’s Subject Key Identifier when both extensions are present.

## Version 5.4.1 (February 17, 2026)

### New features and improvements

- Extended login-request telemetry with Linux distribution details parsed from `/etc/os-release`.

### Bug fixes

- Fixed `IndexOutOfRangeException` in Arrow result chunk processing by adding retry state cleanup, batch integrity validation, and defensive bounds checking in `ExtractCell()`.
- Fixed `IndexOutOfRangeException` when reading `NUMBER`/`DECIMAL` columns with scale greater than 9 in Arrow result format.

## Version 5.4.0 (February 05, 2026)

### New features and improvements

- Added support for Red Hat Enterprise Linux (RHEL) 9.
- Added support for the [DECFLOAT](/sql-reference/data-types-numeric#label-data-type-decfloat) data type (returned as string to preserve full precision).

### Bug fixes

- Fixed `IndexOutOfRangeException` in Arrow result processing when empty batches are returned by the Snowflake backend.

## Version 5.3.0 (January 07, 2026)

### New features and improvements

- Introduced a shared library for extended telemetry to identify and prepare the testing platform for native Rust extensions.

### Bug fixes

- None.
