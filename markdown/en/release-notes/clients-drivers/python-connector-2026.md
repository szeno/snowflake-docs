# Snowflake Connector for Python release notes for 2026

This article contains the release notes for the Snowflake Connector for Python, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Python updates.

See [Snowflake Connector for Python](/developer-guide/python-connector/python-connector) for documentation.

## Version 5.0.0rc3 (Sep 10, 2026)

Third release candidate of the connector built on the Universal Core. See [Snowflake Connector for Python built on the Universal Core](/developer-guide/python-connector/python-connector-universal-core) for installation instructions, the curated list of behavior differences, and migration guidance.

### New features and updates

- Dropped support for Python 3.10. The minimum supported Python version is now 3.11. Prebuilt wheels are published for CPython 3.11, 3.12, 3.13, and 3.14.
- Added type codes for structured `MAP`, `FILE`, `INTERVAL_YEAR_MONTH`, and `INTERVAL_DAY_TIME` columns in `cursor.description`, matching the 4.x connector. These columns previously reported as `TEXT`.
- Mapped `DECFLOAT` columns to the `FIXED` type code so they are reported as decimal rather than text.
- Added nested column metadata on `ResultMetadataV2.fields` for VECTOR and structured types.

### Bug fixes

- Fixed `file_stream` PUT uploads that could silently send zero bytes when the stream wasn’t positioned at the start.
- Fixed binding of non-finite floats (`inf`, `-inf`, `nan`) so the server’s `REAL`/`DOUBLE` parser accepts them.
- Fixed `cursor.execute_async()` (sync and asyncio) ignoring `num_statements`, which caused multi-statement async queries to fail with a statement-count mismatch.
- Fixed `Error.msg` appending `sfqid` and `request_id`. The `.msg` attribute now holds only the server error text; `str(err)` still includes both identifiers.
- Fixed structured `MAP` and `FILE` columns raising `Unsupported column type` (and, for JSON `MAP` results, a process abort) instead of describing and fetching the column.
- Fixed GET downloads of multiple files that share a destination basename silently overwriting each other; GET now warns when that collision occurs.
- Fixed Windows wheels shipping `snowflake/__init__.py`, which broke the PEP 420 `snowflake` namespace and conflicted with other `snowflake.*` packages.
- Fixed fetching an out-of-range nanosecond timestamp through `fetch_pandas_all()` or `fetch_arrow_all()` aborting the process. These values now raise `InterfaceError`.
- Fixed the file-based token cache rewriting and then using a cache file whose mode isn’t `0600`. Such a file is now reported and left unused.

## Version 5.0.0rc2 (Sep 4, 2026)

Second release candidate of the connector built on the Universal Core. See [Snowflake Connector for Python built on the Universal Core](/developer-guide/python-connector/python-connector-universal-core) for installation instructions, the curated list of behavior differences, and migration guidance.

### New features and updates

- Added the `token_file_path` connection parameter, which loads a programmatic access token (PAT), legacy OAuth, or OIDC bearer token from a file (including from `connections.toml`). If both `token` and `token_file_path` are set, the file contents are used.
- Added native Azure Kubernetes Service (AKS) workload identity support: on an AKS pod configured with the Azure Workload Identity webhook, `workload_identity_provider="AZURE"` now authenticates directly using the injected federated token, without requiring the projected-volume/OIDC workaround. Falls back to the existing Azure Functions/IMDS flow if the AKS environment isn’t detected.
- Restored the `workload_identity_aws_use_outbound_token` connection parameter for AWS Workload Identity Federation. When set to `true`, attestation uses outbound STS `GetWebIdentityToken` instead of the default pre-signed `GetCallerIdentity` token; the connection parameter takes precedence over the `SNOWFLAKE_ENABLE_AWS_WIF_OUTBOUND_TOKEN` environment variable.
- Restored automatic `application` detection from the `SF_PARTNER` environment variable and from imported Streamlit, Jupyter, and Snowflake Notebook modules when `application` isn’t passed to `connect()`.

### Changes

- `PUT` now resolves relative local source paths to an absolute, canonical form (resolving `..` segments and symlinks) before upload, matching the legacy connector’s behavior.
- Binding a value of an unsupported Python type in `cursor.execute()` now raises `ProgrammingError` instead of silently sending a `str()`-coerced value, matching the legacy connector.
- Removed the `Connection.disable_request_pooling` property. Passing `disable_request_pooling` to `connect()` is still accepted for compatibility but has no effect and emits a `DeprecationWarning`.
- `ReauthenticationRequest` can no longer be imported from `snowflake.connector.network`; import it from `snowflake.connector` or `snowflake.connector.errors` instead.
- Removed the `snowflake.connector.options` backward-compatibility module; accessing `MissingPandas` (now in `snowflake.connector.constants`) emits a `DeprecationWarning`.

### Deprecated features

- Restored the bare `DESC`/`DESCRIBE <table>` shorthand (rewritten client-side to `DESCRIBE TABLE <table>`), which previously failed with a SQL syntax error. This shorthand now emits a `DeprecationWarning` and will be removed in a future release; use `DESC TABLE <table>` instead.
- Restored the authenticator-type constants (for example, `WORKLOAD_IDENTITY_AUTHENTICATOR`) in `snowflake.connector.network`, needed by tools such as dbt-adapters that import them directly. These constants are deprecated and emit a `DeprecationWarning` on first use; use the new `snowflake.connector.constants.AuthenticatorType` enum instead.

### Bug fixes

- Fixed reading a session parameter with `.get(name, default)` raising `AttributeError`.
- Fixed a crash when connecting with non-string values (for example, a boolean) in `session_parameters`; those values are now sent as strings instead of failing at connect time.
- Fixed `cursor.executemany()` returning `None`; it now returns the cursor (matching `execute()` and the legacy connector), so query IDs are accessible after a batch.
- Fixed multi-statement connection helpers (`execute_string()`, `execute_stream()`) not applying caller-provided keyword arguments to every executed statement.
- Fixed result partitions from `cursor.get_result_batches()` returning standard Python values instead of NumPy values when the connection was opened with `numpy=True`, on both the synchronous and asynchronous connectors.
- Fixed login failures (including key-pair/JWT authentication) to report the server’s own error code instead of a generic one, and to use SQLSTATE `28000` for credential-rejection failures.
- Fixed `internal_size` on `cursor.description` to report the character count (matching the legacy connector) instead of the UTF-8 byte count.
- Fixed a negative sub-second timestamp decoding bug on the JSON result-format path that could shift instants just before 1970-01-01 a full second into the future.
- Fixed exception classification for query failures, timeouts, and stage-binding errors so they consistently raise `ProgrammingError` or `OperationalError` instead of a generic internal error; `get_query_status()` for a valid query ID with no server-side status now returns `NO_DATA` instead of raising an internal error.

## Version 4.7.3 (Sep 3, 2026)

### Security fixes

Note

Improved the robustness and correctness of OCSP revocation checking. `SF_OCSP_RESPONSE_CACHE_SERVER_URL` now takes precedence over connector-derived cache URLs, including for PrivateLink hosts, and PrivateLink OCSP cache URLs are derived only for valid hosts that contain a `.privatelink.` label and end in a recognized Snowflake domain. Other hosts use the public default cache URL.

Warning

This also means that if you’re using [Snowflake internal stages over PrivateLink](/user-guide/private-connectivity-inbound#label-private-connect-internal-stages), and also want OCSP to be performed over the PrivateLink OCSP host, in version 4.7.3 and later 4.x versions of the Snowflake Connector for Python, you now need to actively configure `SF_OCSP_RESPONSE_CACHE_SERVER_URL` and define the PrivateLink OCSP host. See [`SYSTEM$ALLOWLIST_PRIVATELINK()`](/sql-reference/functions/system_allowlist_privatelink) for details on hostnames.

Without this, the OCSP for the internal stage will be performed **over public link** which might be blocked by default in your private network.

- Restricted the `WORKLOAD_IDENTITY` authentication flow to recognized Snowflake hosts ending in `snowflakecomputing.com`, `snowflakecomputing.cn`, or `snowflakecomputing.mil`. You can add recognized host suffixes with the `SNOWFLAKE_WIF_ALLOWED_HOST_SUFFIXES` environment variable.
- Applied secret masking by default to the `snowflake.connector` loggers and to the third-party loggers used by the connector: `botocore`, `boto3`, `aiohttp`, `aiobotocore`, `aioboto3`, and vendored `urllib3`. Set `SNOWFLAKE_DISABLE_LOG_SECRET_MASKING=true` to opt out.
- Extended masking to cover additional connection token formats, OAuth access and refresh tokens, one-time passcodes, OAuth client identifiers and secrets, and `Authorization` headers in error logs. The asynchronous path copies request headers before modifying them.
- Masked SQL text before it is written to DEBUG logs. Masking is deferred until a handler emits the log record to avoid unnecessary processing when DEBUG logging is disabled.
- Removed query result master key (`qrmk`) values, chunk-header values, and malformed response contents from result batch logs. Logs instead report whether a key is present and include structural metadata useful for debugging.

### New features and updates

- Published experimental wheels for Python 3.14t (free-threaded CPython). These wheels are not intended for production use.

### Bug fixes

- Fixed TLS hostname verification rejecting a matching certificate subject alternative name when a Snowflake account locator contains an underscore.
- Fixed a significant `connect()` slowdown on deep call stacks. The connector now walks frame references directly instead of reading and parsing the source file for every frame.
- Fixed `split_statements` truncating unquoted URLs containing `://` by interpreting the `//` as a line comment. URL schemes are now recognized in both line-comment and block-comment parsing.
- Corrected the invalid account identifier error message to state that periods are allowed as label separators.
- Fixed the on-disk OCSP response validation cache failing when written from a forked child process. The cache file lock is now re-created when the owning process changes.

## Version 5.0.0rc1 (Aug 19, 2026)

Initial public preview release of the connector built on the Universal Core. This is a new version line, published under the existing `snowflake-connector-python` package name as a release candidate. Because pre-release versions are not installed by default, `pip install --pre snowflake-connector-python` is required. See [Snowflake Connector for Python built on the Universal Core](/developer-guide/python-connector/python-connector-universal-core) for installation instructions, the curated list of behavior differences, and migration guidance.

### New features and updates

- Rebuilt the connector on the Universal Core, a shared Rust library that implements networking, authentication, result-set fetching, and stage transfers for every Snowflake driver, replacing the pure-Python implementation.
- Published the connector and Universal Core source in the [Snowflake drivers repository](https://github.com/snowflakedb/drivers) on GitHub.
- Added the `snowflake.connector.aio` module, which exposes the PEP 249 `Connection` and `Cursor` objects as asyncio coroutines.
- Published wheels for CPython 3.11, 3.12, 3.13, and 3.14. Python 3.10 installs from the source distribution and compiles the Rust extension locally.

### Changes

- Only one version of the package can be installed in a given environment, so install this version into a separate virtual environment rather than upgrading in place.
- Certificate revocation checking uses CRLs rather than OCSP, and is off by default. OCSP-specific connection parameters are not accepted. See [Configuration differences](/developer-guide/python-connector/python-connector-universal-core#label-python-universal-core-config).
- Snowflake’s Python libraries currently declare a dependency on a connector version below 5.0.0 and cannot be installed alongside this version. See [Ecosystem compatibility](/developer-guide/python-connector/python-connector-universal-core#label-python-universal-core-ecosystem).
- This release contains breaking behavior changes relative to the 4.x connector. The most significant are summarized in [Behavior differences](/developer-guide/python-connector/python-connector-universal-core#label-python-universal-core-behavior-differences), and the complete catalog is published as [`BehaviorDifferences.yaml`](https://github.com/snowflakedb/drivers/blob/main/python/BehaviorDifferences.yaml).

## Version 4.7.2 (Aug 7, 2026)

### New features and updates

- None.

### Bug fixes

- Fixed a thread leak in the file transfer agent by properly shutting down thread pool executors after `PUT` and `GET` transfers.
- Fixed `split_statements` treating `//` as SQL instead of a line comment, which could merge multiple statements when a `//` comment contained an apostrophe.
- Fixed large-file `PUT` uploads to internal Azure stages failing against the Azure limit of 50,000 blocks per blob. The connector now increases the multipart chunk size for very large files, and the default Azure chunk size increased from 4 MB to 8 MB.
- Fixed connections using cached OAuth credentials failing when the cached access token was invalid. The connector now reauthenticates silently using a refresh token when available, or a browser otherwise. A new process that has only a cached refresh token also attempts a silent refresh before opening a browser.
- Fixed Okta SAML authentication reporting an opaque negative connect timeout error after `login_timeout` expired. A timed-out login now reports error `250006` with a message that identifies `login_timeout`.
- Fixed the OAuth authorization code flow failing for accounts with uppercase letters in the account name.
- Fixed JWT key-pair authentication errors always reporting the generic error code `250001`. Authentication failures now preserve the server’s specific error code and use SQLSTATE `28000`.

## Version 4.7.1 (July 15, 2026)

### New features and updates

- Added support for Python 3.14t (free-threaded).
  - **Note:** Python 3.14t is not supported on `win_arm64` because `cryptography` wheels are not yet available for that platform and architecture combination.
- Improved URL validation reliability by replacing the hand-rolled regex in `is_valid_url()` with `urllib.parse.urlparse`.
- Removed the pandas upper bound dependency constraint on the `[pandas]` extra to allow installation of pandas 3.0.0 and later.
- Added native AKS (Azure Kubernetes Service) workload identity support. When running on AKS with workload identity configured, the connector automatically uses `WorkloadIdentityCredential` to authenticate using the injected service account credentials. OIDC backward compatibility is also supported.
- Added the `workload_identity_aws_use_outbound_token` connection option (default `false`) to opt into AWS WIF JWT attestation using the STS `GetWebIdentityToken` action instead of the default SigV4 `GetCallerIdentity` method. This connection option supersedes the `SNOWFLAKE_ENABLE_AWS_WIF_OUTBOUND_TOKEN` environment variable introduced in version 4.5.0, which will be removed in a future release.

### Bug fixes

- Improved verification of TLS connections.
- Fixed `python-connector.log` not rotating on Windows, and every record being logged twice, when easy logging is enabled using `config.toml`.
  - **Note:** As part of this fix, easy logging no longer calls `logging.basicConfig()` and therefore no longer configures the root logger. `python-connector.log` now captures only the `snowflake.connector`, `botocore`, and `boto3` loggers.
- Fixed an OAuth infinite loop when tokens expire by ensuring `reauthenticate()` calls `_request_tokens()` directly instead of looping through `prepare()`. The token cache is now read exactly once per connection, and `_store_tokens()` preserves the macOS Keychain ACL by never calling `remove()`. The async OAuth `reauthenticate()` now runs the synchronous OAuth flow on a worker thread instead of blocking the event loop.
- Fixed OAuth scope handling for Snowflake custom OAuth: when refresh tokens are enabled, the connector no longer appends the OIDC `offline_access` scope for token endpoints on `*.snowflakecomputing.com` or `*.snowflakecomputing.cn`, which caused `invalid_scope` errors. Snowflake custom OAuth expects `refresh_token` in the scope instead. External IdP behavior is unchanged.
- Fixed input validation for the `scale` metadata in Arrow result set processing for `TIME`, `TIMESTAMP_NTZ`, `TIMESTAMP_LTZ`, and `TIMESTAMP_TZ` columns.
- Fixed the S3 storage client to correctly handle 307/308 (method-preserving) and 301/302 (GET/HEAD only) redirects by disabling automatic redirect following and re-signing each request with AWS SigV4 credentials for the redirect target. The region is updated from the `x-amz-bucket-region` response header on each redirect. Redirects are capped at 5 hops.
- Fixed a bug where a fully-qualified DDL statement (for example, `CREATE VIEW db.schema.obj`) on a session with no current schema would populate the connector’s cached schema and database from the referenced object’s namespace. This made `get_current_schema()` diverge from the server’s `CURRENT_SCHEMA()` and mis-qualified Snowpark temporary objects.

## Version 3.18.1 (July 15, 2026)

### New features and updates

- None.

### Bug fixes

- Improved verification of TLS connections.

## Version 4.6.0 (May 28, 2026)

### New features and updates

- Bumped vendored `urllib3` to version 2.7.0.
- Added one in-band telemetry record per successful login describing which connection-identifier fields the user supplied (`account_provided`, `account_with_region`, `account_org_provided`, `region_provided`, `host_provided`). No hostname or account value is included.
- The telemetry is gated by the existing server-side `CLIENT_TELEMETRY_ENABLED` parameter and can additionally be disabled locally by setting `SF_TELEMETRY_DISABLE_CONNECTION_SHAPE=true`. Collection is time-boxed and will be removed in a future release.

### Deprecated features

- Dropped support for Python 3.9. The minimum supported Python version is now 3.10.

### Bug fixes

- Fixed sdist to only install the minicore binary matching the current platform. Previous 4.x releases copied every platform’s minicore `.so`/`.dylib`/`.dll` into the install prefix, which broke downstream packagers (for example, Homebrew) whose audits reject foreign-architecture binaries.

## Version 4.5.0 (May 12, 2026)

### New features and updates

- Added ECDSA key support (ES256, ES384, ES512) for key-pair authentication.
- Added HTTP 307/308 redirect status codes to the retryable set as defense-in-depth, with redirect-aware logging in both sync and async paths.
- Consolidated keyring token cache to use a single service name with hashed account keys, reducing macOS Keychain password prompts. Legacy entries are auto-migrated on first read.
- Added support for AWS outbound JWT token attestation for Workload Identity Federation (WIF). This can be enabled by setting the `SNOWFLAKE_ENABLE_AWS_WIF_OUTBOUND_TOKEN` environment variable to `true`. This environment variable will be removed in a future release.
- Removed dynamic class deserialization from the OCSP response validation cache to prevent arbitrary code execution via crafted cache files. The `SNOWFLAKE_ENABLE_CUSTOM_REVOCATION_ERRORS` environment variable is now a no-op.
- Updated SPCS token injection to gate on the `SNOWFLAKE_RUNNING_INSIDE_SPCS` environment variable, trim whitespace, and remove the configurable token path.
- GCP WIF attestation now uses hostname `metadata.google.internal` instead of the IPv4 link-local address, so it works on IPv6-only GCP VMs.
- Added validation of the `account` connection parameter so malformed identifiers (for example path-like values or labels outside letters, digits, `_`, and `-`) are rejected with `ProgrammingError` before login.
- Added support for Azure Workload Identity Federation impersonation, allowing a managed identity to authenticate as a service principal.

### Bug fixes

- Fixed `write_pandas` temp stage name collisions. The old PRNG could produce identical name sequences in forked processes (for example, Notebook kernels), causing `CREATE TEMPORARY STAGE` to fail with “Object already exists”.
- Fixed a security bug in Okta SAML authentication where `_is_prefix_equal()` compared `url1`’s port against itself instead of `url2`’s port, allowing an attacker to redirect credentials to a different port on the same hostname. Also fixed the default port fallback to use `int` instead of `str` for correct comparison when one URL omits the port.
- Fixed `executemany` with `paramstyle="pyformat"` to correctly locate the VALUES clause using a balanced-parentheses parser instead of a greedy regex. This fixes incorrect behavior with nested function calls such as SQLAlchemy `@compiles VARIANT` patterns (for example, `PARSE_JSON(%(col)s)`) and subquery-form INSERTs.
- Fixed a bug where `write_pandas()` with `auto_create_table=False` and `overwrite=True` would execute `CREATE TABLE IF NOT EXISTS`, which required unnecessary `OWNERSHIP` privilege on the table. Now only `TRUNCATE TABLE` is executed in this case.

## Version 4.4.0 (Mar 25, 2026)

### New features and updates

- Bumped the lower boundary of the `cryptography` package to 46.0.5 to address CVE-2026-26007.
- Added support for Python 3.14.
- Removed the upper bound dependency constraint on `pyOpenSSL` to allow installation of `pyOpenSSL` 26.0.0+, which includes a fix for GHSA-vp96-hxj8-p424.

### Deprecated features

- Renamed the environment variable for skipping config file permission warnings from `SF_SKIP_WARNING_FOR_READ_PERMISSIONS_ON_CONFIG_FILE` to `SF_SKIP_TOKEN_FILE_PERMISSIONS_VERIFICATION`. The old variable is still supported but emits a deprecation warning.

### Bug fixes

- Fixed the Azure IMDS `Metadata` header to use lowercase `"true"` instead of `"True"`, which caused 400 errors during Azure Workload Identity Federation authentication.
- Fixed the default `crl_download_max_size` to be 20 MB instead of 200 MB to prevent potential out-of-memory issues.
- Fixed a bug where Azure GET commands would incorrectly set the file status to `UPLOADED` instead of preserving the `DOWNLOADED` status during metadata retrieval.
- Fixed the `unsafe_skip_file_permissions_check` flag not being respected when reading `connections.toml`.
- Fixed a `JSONDecodeError` in `result_batch._load()` when fetching large result sets.

## Version 4.3.0 (Feb 12, 2026)

### Deprecated features

- Deprecated support for custom revocation error classes in OCSP response cache deserialization.
  By default, only `RevocationCheckError` exceptions are deserialized from OCSP cache. Custom exception classes can be temporarily enabled by setting the `SNOWFLAKE_ENABLE_CUSTOM_REVOCATION_ERRORS` environment variable to `true` or `1`, but this support will be removed in a future release.

### New features and updates

- Bumped vendored `urllib3` to version 2.6.3.
- Added `force_microseconds_precision` to `cursor.fetch_arrow_all` and `cursor.fetch_pandas_all` to avoid PyArrow schema inconsistencies between batches.
- Added a warning when using HTTP protocol for OAuth URLs.
- Updated the `server_session_keep_alive` parameter in `SnowflakeConnection` to skip checking for pending asynchronous queries, providing faster connection close times, especially when many asynchronous queries are executed.

### Bug fixes

- Fixed the string representation of `INTERVAL YEAR` and `INTERVAL MONTH` types.
- Ensured proper list conversions; the converter now runs `to_snowflake` on all list items.

## Version 4.2.0 (Jan 07, 2026)

### New features and updates

- Added the `SnowflakeCursor.stats` property to expose granular DML statistics (rows inserted, deleted, updated, and duplicates) for operations like CTAS where `rowcount` is insufficient.
- Added support for injecting Snowpark Container Services (SPCS) service identifier tokens (`SPCS_TOKEN`) into login requests when present in SPCS containers.
- Introduced a shared library for extended telemetry to identify and prepare testing platforms for native Rust extensions.

### Bug fixes

- None.
