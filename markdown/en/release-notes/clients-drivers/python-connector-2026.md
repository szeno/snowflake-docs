# Snowflake Connector for Python release notes for 2026

This article contains the release notes for the Snowflake Connector for Python, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Snowflake Connector for Python updates.

See [Snowflake Connector for Python](/developer-guide/python-connector/python-connector) for documentation.

## Version 5.1.0 (Oct 21, 2026)

### New features and updates

- Added support for Python 3.14t (free-threaded CPython). Wheels are published for Linux, macOS, and Windows x64. Windows on ARM does not include a 3.14t wheel. See [Installing the Python Connector](/developer-guide/python-connector/python-connector-install).

### Bug fixes

- Fixed statement-level `TIMEZONE` overrides. Pass `TIMEZONE` in `_statement_params` on `execute()` to send that time zone on the query request without changing the session. See .
- Fixed stage uploads and downloads so a failed system certificate load is retried, instead of failing the storage client or skipping the operating-system trust store.

### Security fixes

- Updated bundled root certificates and distrusted compromised intermediate certificate authority (CA) certificates (RUSTSEC-2026-0382).

### Changes

- Login omits `CLIENT_SESSION_KEEP_ALIVE` and `CLIENT_PREFETCH_THREADS` unless you set `client_session_keep_alive` or `client_prefetch_threads`. A heartbeat frequency you set is sent as `CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY` and clamped to 900–3600 seconds. An explicit `validate_default_parameters` value, `True` or `False`, is sent as `CLIENT_VALIDATE_DEFAULT_PARAMETERS`. Omitting `validate_default_parameters` leaves that parameter off the login request.
- Login sends `TIMEZONE`, `AUTOCOMMIT`, `CLIENT_TIMESTAMP_TYPE_MAPPING`, `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX`, `SERVICE_NAME`, `GCS_USE_DOWNSCOPED_CREDENTIAL`, and `CLIENT_OUT_OF_BAND_TELEMETRY_ENABLED` as session parameters when you set them.
- Removed `disable_console_login` and `oauth_disable_console_login`. Passing either connection parameter warns and has no effect. External browser login always requests the SSO URL from Snowflake. See [Parameters and calls that no longer work](/developer-guide/python-connector/python-connector-upgrade#label-python-upgrade-removed).
- Removed `OCSP_MODE` from the login client environment and from connection diagnostics. The connector does not perform OCSP. Certificate revocation is reported as `CERT_REVOCATION_CHECK_MODE`.
- Changed GCS PUT to omit the `Content-Encoding` header.

## Version 5.0.0 (Oct 15, 2026)

Snowflake Connector for Python 5.0.0 is generally available. It is built on the [Universal Core](/developer-guide/universal-core/universal-core) and is published under the existing `snowflake-connector-python` package name. It requires Python 3.11 or later. Installing it replaces the connector from versions before 5.0 in that environment. See [Upgrading to the Snowflake Connector for Python 5.x](/developer-guide/python-connector/python-connector-upgrade) before you upgrade.

The lists below are the differences from versions before 5.0.

### Breaking changes

- Changed an empty `connections.toml` so connections defined in `config.toml` are kept.
- Changed `ConfigManager` with no `file_path` so reading an option raises `MissingConfigOptionError` instead of `ConfigManagerError`.
- Changed a bare `connect()` so a detected application name takes precedence over `application` in the default connection profile. Detection uses the `SF_PARTNER` environment variable, or an imported Streamlit, Jupyter, or `snowbooks` module.
- Changed `client_session_keep_alive` and `client_session_keep_alive_heartbeat_frequency` to read-only properties. Assigning them raises `AttributeError`.
- Removed the public `Connection.connect()` method. The session opens when the connection is constructed.
- Removed the `region` connection parameter and `Connection.region`. Pass a fully qualified `account`, or set `host`.
- Removed the `backoff_policy` callable. Set retry delays with `retry_backoff_base_ms`, `retry_backoff_cap_ms`, `retry_backoff_factor`, and `retry_backoff_jitter`. The default initial delay is 250 ms (it was 1 second), and the default jitter is decorrelated (it was full).
- Removed `Connection.disable_request_pooling`. Passing `disable_request_pooling` to `connect()` warns and has no effect.
- Removed the `converter_class` connection parameter and `DefaultConverterClass`. Passing `converter_class` raises `ProgrammingError`.
- Changed OAuth login failures for a bad client secret so the exception message includes the identity provider’s error name, such as `invalid_client`.
- Changed session-token login so `master_token` is required. Invalid tokens fail in `connect()` instead of on a later request.
- Changed OAuth token and authorization endpoint URL validation to require HTTPS. `http://` is allowed only for loopback addresses.
- Changed external-browser login so a mid-session master-token expiry raises `ReauthenticationRequest` instead of opening the browser again and retrying the query.
- Removed the `password_callback` connection parameter. Passing it raises `ProgrammingError`. Change an expired password outside the connector.
- Changed cursor session parameters so a change on one cursor is visible to other cursors on the same connection without those cursors running a query.
- Changed methods on a closed cursor to raise `InterfaceError`. `fetchone`, `fetchmany`, `fetchall`, and `reset` still read rows already buffered on an open cursor after `connection.close()`.
- Changed `fetchone`, `fetchmany`, `fetchall`, and cursor iteration before any query to raise `ProgrammingError` instead of `TypeError`.
- Changed `cursor.execute` so passing `file_stream` on a statement that is not a PUT raises `ProgrammingError`.
- Changed `fetch_pandas_all`, `fetch_pandas_batches`, and the `fetch_arrow_*` methods so a JSON result, such as `SHOW` or `DESCRIBE`, returns a DataFrame or Arrow table instead of raising `NotSupportedError`.
- Changed `executemany()` on an `INSERT` without a `VALUES` clause to raise `ProgrammingError` instead of `InterfaceError`.
- Removed the `create_temp_table` argument from `write_pandas`. Pass `table_type='temp'` instead.
- Removed `ResultBatch.session_manager` and `ResultBatch.http_config`.
- Changed result-chunk fetching to always use a thread pool. `client_fetch_use_mp` warns and no longer selects a process pool. `client_fetch_threads` is a deprecated alias of `client_prefetch_threads`.
- Changed PUT so symlinks in a source path are resolved before upload. A symlinked file is stored under the target file’s name, and a relative path that walks through a symlink and `..` can select a different file.
- Removed `iobound_tpe_limit`. Passing it to `connect()` warns and has no effect, and `Connection.iobound_tpe_limit` does not exist.
- Changed proxy selection so an explicit `proxy_host`, `proxy_port`, or `proxy` URL wins when `HTTP_PROXY`, `HTTPS_PROXY`, or `NO_PROXY` is also set. `use_proxy_env` defaults to `True`. Pass `False` to ignore those variables.
- Changed CRL caching so `enable_crl_cache=False` warns and no longer disables caching. Set both `crl_enable_memory_caching` and `crl_enable_disk_caching` to `False`. See [Certificate revocation checking](/developer-guide/python-connector/python-connector-connect#label-python-crl).
- Changed FIPS support so it is available only when the connector is installed from the PyPI source distribution with `SNOWFLAKE_FIPS=1`. See [Installing a FIPS-supporting version](/developer-guide/python-connector/python-connector-install#label-python-connector-install-fips).
- Removed OCSP certificate validation in favor of CRL validation.
- Removed YAML easy-logging configuration. Troubleshooting logs are enabled with the `SNOWFLAKE_TROUBLESHOOTING_ENABLED` environment variable.
- Removed the `snowflake.connector.options` module. Importing it raises `ModuleNotFoundError`.
- Removed `snowflake.connector.dbapi` and the authenticator classes previously exported from `snowflake.connector.auth`.
- Removed file-transfer and type-helper exports from `snowflake.connector.constants`, including `FileTransferType`, `ResultStatus`, cloud filesystem labels, part-size constants, the `get_*_types` and `is_*_type_name` helpers, and the Arrow type helpers. `QueryStatus` remains.
- Removed `DownloadMetrics`, `RemoteChunkInfo`, and the chunk-download constants `DOWNLOAD_TIMEOUT`, `MAX_DOWNLOAD_RETRY`, `SSE_C_AES`, `SSE_C_ALGORITHM`, and `SSE_C_KEY` from `snowflake.connector.result_batch`.

### New features and updates

- Added an asyncio-compatible API under `snowflake.connector.aio`, including nonblocking connection, query, fetch, transaction, Arrow, pandas, and async context-manager operations. See [Using asynchronous I/O with the Python Connector](/developer-guide/python-connector/python-connector-asyncio).
- Added the `use_core_arrow` connection parameter for native Rust conversion of row, Arrow, and pandas fetches in the synchronous and asyncio APIs. This parameter is in public preview. See [{/ preview-transition-waiver: Public preview section for usecorearrow. No…](/developer-guide/python-connector/python-connector-example#label-python-connector-core-arrow).

### Bug fixes

- Fixed PUT `SOURCE_COMPRESSION=AUTO_DETECT` so a `.deflate` file is recognized as `DEFLATE`.
- Fixed GET so a failed download removes the temporary `.part` file.
- Fixed Azure client-side encryption metadata so `EncryptionAgent.EncryptionAlgorithm` is `AES_CBC_256`.
- Fixed the GET result `file` column so a stage path with more than one directory level reports only the file name.
- Fixed `Connection.is_valid()` so a live `PAT_WITH_EXTERNAL_SESSION` connection returns true.

### Changes

- Changed gzip-compressed PUT uploads to omit the original file name from the gzip header.
- Added support for PUT `SOURCE_COMPRESSION=BROTLI`, including auto-detection of `.br` files.
- Changed the private-key password parameter to `private_key_password`. `private_key_file_pwd` is still accepted and warns.
- Changed the MFA token-caching parameter to `client_store_temporary_credential`. `client_request_mfa_token` is still accepted and warns.
- Changed `JSONResultBatch` and `ArrowResultBatch` so `to_arrow()`, `to_pandas()`, and table iteration work on every result batch.
- Changed S3 uploads and downloads in China regions (`cn-*`) to use the AWS SDK’s default endpoint when no regional URL and no custom endpoint are set.
- Changed `oauth_enable_refresh_tokens` so it warns and has no effect. A refresh token is used when the identity provider returns one, and `client_store_temporary_credential` controls whether that token is cached on disk.
- Changed `oauth_credentials_in_body=True` so the client id and secret are sent only in the token-request body.
- Changed the connection parameter for S3 regional URLs to `use_s3_regional_url`. `enable_stage_s3_privatelink_for_us_east_1` is still accepted and warns.
- Changed Azure Blob PUT to omit the `Content-Encoding` and `x-ms-blob-content-encoding` headers.
- Changed concurrent interactive logins for the same user and host to share one prompt when `disable_parallel_user_prompt` and `client_store_temporary_credential` are left at their defaults.
- Changed `executemany` to follow the server’s array-binding flag instead of detecting `INSERT` in the SQL text. A statement the server does not mark as array-bindable still runs one row at a time.
- Changed Azure PUT and GET so any HTTP 403 refreshes the SAS token and retries.
- Changed a failed Azure SAS refresh so it raises a terminal error instead of retrying without a limit. A rejected token is logged as a warning, and a failed refresh is logged as an error.
- Changed client-side encryption metadata so `KeyWrappingMetadata.EncryptionLibrary` is `Rust(OpenSSL)`.
- Added `parameter` and `validation_code` on errors from connection-configuration validation.
- Changed `fetch_pandas_all` and `fetch_pandas_batches` so extra keyword arguments are passed to Arrow’s `to_pandas`. Arguments that only `pandas.concat` accepts, such as `sort`, `keys`, and `copy`, raise `TypeError`.
- Changed `login_timeout`, `network_timeout`, and `socket_timeout`. `login_timeout` returns the login budget (120 seconds when unset; previously `None`). `network_timeout` returns `request_timeout` (120 seconds when unset; previously `None`). `socket_timeout` returns `retry_timeout`. Passing `network_timeout` warns and also sets `query_timeout`. Passing `socket_timeout` warns and also sets `connect_timeout`. `retry_timeout` is a total time limit for the attempt, rather than a per-read inactivity timeout.
- Changed non-string session parameter values so they are sent as JSON strings.
- Changed binding of an unsupported Python type to raise `ProgrammingError` with errno 255001.
- Added `display_size` for text columns, set to the column’s character length.
- Changed `put_get_max_attempts` so any positive integer is used, with no upper limit.
- Changed the default of `client_store_temporary_credential` to true on every platform. An explicit false now disables token caching on macOS and Windows as well.
- Changed the unused connection arguments `dsn`, `session_id`, `support_negative_year`, `json_result_force_utf8_decoding`, `inject_client_pause`, `probe_connection`, `debug_arrow_chunk`, `snowflake_server_dop_cap_for_file_transfer`, and `reraise_error_in_file_transfer_work_function` so they warn and have no effect. `connection.session_id` after login still returns the server-assigned id. `log_imported_packages` and `log_imported_packages_in_telemetry` are ignored without a warning.
- Changed legacy HTTP error classes so they remain importable from `snowflake.connector.errors`, warn on first use, and are no longer raised: `HttpError`, `InternalServerError`, `ServiceUnavailableError`, `GatewayTimeoutError`, `ForbiddenError`, `RequestTimeoutError`, `BadRequest`, `BadGatewayError`, `MethodNotAllowed`, `TooManyRequests`, `OtherHTTPRetryableError`, `RevocationCheckError`, `RefreshTokenError`, `BindUploadError`, `RequestExceedMaxRetryError`, `TokenExpiredError`, and `PresignedUrlExpiredError`.

## Version 5.0.0rc4 (Sep 30, 2026)

### New features and updates

- Added Duo push continuation and MFA callbacks for username and password authentication.
- Added native Arrow conversion for Boolean, numeric, DECFLOAT, text, binary, DATE, TIME, TIMESTAMP, INTERVAL, and VECTOR values, including NumPy scalar output and `DictCursor` rows.
- Added pandas and Arrow fetching for JSON result sets returned by commands such as `SHOW`, `DESCRIBE`, DDL, PUT, and GET.
- Added the `platform_detection_timeout_seconds` connection parameter. The parameter is accepted and ignored. Every cloud-metadata and STS probe uses a fixed timeout of 2 seconds.
- Added the `put_compress_level` and `put_tempdir` connection parameters for PUT auto-compression.
- Added the `proxy_scheme` connection parameter for HTTPS connections to proxies and `extra_root_store_path` for extending the default TLS trust store.
- Added support for generators and other iterators in `executemany()`.
- Added `FILE`, `INTERVAL_YEAR_MONTH`, and `INTERVAL_DAY_TIME` type codes.
- Added Conda packaging for the connector.

### Changes

- Requires Python 3.11 or later, unchanged from version 5.0.0rc3.
- Changed `client_store_temporary_credential` to default to `True`. Set it to `False` explicitly to disable ID, OAuth, and MFA token caching.
- Improved native Arrow fetching by using the result prefetch pipeline for asynchronous rows.
- Improved GCS PUT throughput by streaming each file in one request.
- Improved first-connection latency on non-FIPS builds.
- Restored the `timezone`, `interpolate_empty_sequences`, and `reuse_results` connection parameters, along with legacy aliases for private-key, external-browser timeout, and console-login settings.
- Changed failed-login errors to include the server-provided reason.

### Bug fixes

- Fixed `cursor.description` reporting GEOGRAPHY and GEOMETRY columns as OBJECT.
- Fixed `ALTER SESSION`, `COMMIT`, and other statements rejected by statement preparation so they fall back to direct execution.
- Fixed `ALTER SESSION SET` cache updates with non-ASCII SQL text.
- Fixed `SNOWFLAKE_CONNECTIONS` parsing so Snowpark configuration is read as TOML.
- Fixed `ReauthenticationRequest` so it is importable from `snowflake.connector.network` and exposes its underlying `cause`.
- Fixed asynchronous multi-statement result retrieval returning only the first statement.
- Fixed statement-level parameters being omitted from queries and bind values being omitted from describe-only preparation.
- Fixed Python array binding when the session-scoped bind stage is unavailable by retrying with inline JSON bindings.
- Fixed timestamp and MAP conversion failures that could terminate the Python process.
- Fixed invalid query IDs so they raise a connector error instead of reaching the server.
- Fixed `write_pandas()` quoting for Parquet and Iceberg field and option names.
- Fixed intermittent key-pair authentication failures on Windows and added support for plaintext PEM strings in `private_key`.
- Fixed OAuth refresh-token retention when refresh-token rotation is disabled.
- Fixed token-cache files with unsafe permissions so they are reported and ignored rather than modified and used.
- Fixed native Okta authentication errors so they include the Snowflake rejection reason.
- Fixed external-browser callbacks so their CORS origin must match the connected Snowflake account.
- Fixed Azure GET corruption caused by transparent gzip decompression.
- Fixed encrypted S3 GET downloads for files created by server-side unloads.
- Fixed S3 and GCS upload retries after temporary credential expiration.
- Fixed S3 external-stage operations that don’t provide a session token.
- Fixed GET results from stage subdirectories so the `file` column reports the downloaded file name.

## Version 4.8.0 (Sep 30, 2026)

### Security fixes

- Fixed external-browser (SSO) authentication to validate the `Origin` header on the local callback server, rejecting tokens delivered from unexpected origins. A trailing slash in the origin (for example, `https://account.snowflakecomputing.com/`) is now accepted on par with the bare origin, matching JDBC and other driver behavior. Preconnect probe connections (empty recv) no longer count against the retry budget and no longer abort the login flow.

### New features and updates

- Added the `SNOWFLAKE_TLS_CIPHERS` environment variable to restrict which TLS ciphers the connector offers. It takes a colon-separated list. Names beginning with `TLS_` are applied as TLS 1.3 cipher suites and the remainder as the cipher list for TLS 1.2 and below, so a single variable covers both. Leaving it unset keeps OpenSSL’s defaults unchanged, and an unrecognized cipher name is rejected rather than silently ignored. The restriction covers Snowflake API traffic, cloud-storage (stage) transfers, OCSP/CRL fetches, and IdP requests. Requests issued by the AWS and Azure SDKs, and asynchronous connections, aren’t covered. For TLS 1.3 suites specifically they can’t be, because the Python standard library exposes no API for restricting them.
- Added the `workload_identity_host` connection option that overrides the STS host used by AWS Workload Identity Federation, for endpoints the driver can’t derive from the region (such as an interface VPC endpoint). The default STS host is now resolved via botocore so partitions that don’t use `amazonaws.com`, such as ISO and European Sovereign Cloud, get the correct hostname. A privately routed host can’t be reached by Snowflake on the default GetCallerIdentity path, so a VPC or PrivateLink STS endpoint also requires `workload_identity_aws_use_outbound_token=True`.

### Changes

- OCSP certificate revocation checks are now off unless you opt in. Set `ocsp_fail_open=True` (fail-open) or `ocsp_fail_open=False` (fail-closed) to enable OCSP. The stored default is `None` (unset); only an explicit `True` or `False` opts in, so forwarding `DEFAULT_CONFIGURATION` as keyword arguments doesn’t turn OCSP on. `disable_ocsp_checks=True` (or `insecure_mode=True`) always turns OCSP off, including when `ocsp_fail_open` is also set. `disable_ocsp_checks=False` and `insecure_mode=False` are the stored defaults and aren’t an opt-in. The connection attribute `ocsp_fail_open` is no longer a report of whether OCSP is fail-open; it is the stored preference (`None` = unset, `True` = fail-open, `False` = fail-closed). Use `_ocsp_mode()` or `disable_ocsp_checks` to see whether checks are actually on. `ocsp_response_cache_filename` and `ocsp_root_certs_dict_lock_timeout` don’t turn OCSP on; if they’re set without an OCSP mode parameter they’re ignored and a warning is logged. The `SF_OCSP_FAIL_OPEN` environment variable still only switches fail-open versus fail-closed after OCSP is already on. Login `OCSP_MODE` telemetry now reports `DISABLE_OCSP_CHECKS` by default. The process-global `FEATURE_OCSP_MODE` is updated by each constructed REST client, except that a later default (OCSP off) client doesn’t overwrite a non-default already stored on the process, and a later `FAIL_OPEN` client doesn’t overwrite `FAIL_CLOSED`.
- Raised the minimum `pyOpenSSL` requirement to 25.3.0, the first version providing `set_tls13_ciphersuites`. This doesn’t narrow the set of installable versions in practice: earlier releases cap `cryptography` below 46 and so were already uninstallable alongside the connector’s own `cryptography>=46.0.5` requirement.

### Bug fixes

- Fixed MD5 computation for Azure clouds.

## Version 4.7.5 (Sep 21, 2026)

### New features and updates

- Added the `SNOWFLAKE_MIN_TLS_VERSION` environment variable (`1.2`, `1.3`, `TLSv1.2`, or `TLSv1.3`, defaulting to TLS 1.2) to raise the minimum TLS version on every outbound connection a synchronous connector makes: the Snowflake API, stage transfers, OCSP/CRL fetches, platform detection, IdP requests, AWS SDK requests (workload identity STS calls and the platform-detection identity probe), and Azure AD token requests made by `azure-identity`. An unrecognized value is rejected at connect time. The variable name and accepted values match the Go driver. Asynchronous (`snowflake.connector.aio`) connections aren’t yet covered.

### Bug fixes

- Follow-up to the 4.7.4 incomplete-result fix: when a successful query request has an incomplete inline first chunk, the connector re-fetches the finished query once via GET `/queries/{qid}/result` before building the result set. JSON treats empty or shorter-than-declared inline rowsets as incomplete. Arrow only treats a missing or empty `rowsetBase64` as incomplete so the execute hot path doesn’t decode IPC. If the result GET fails (a transport error or `success: false`), the original payload is kept; if the GET succeeds but is still incomplete, that response is used. In either incomplete case, the existing row count checks still raise `OperationalError` errno `252013` when the result is drained (no silent EOF). On the sync path, a remote result chunk whose body holds fewer rows than its declared `rowCount` is re-downloaded once before that check raises, so a truncated-but-valid chunk download can recover without silent data loss. Asynchronous (`snowflake.connector.aio`) remote-chunk re-download is unchanged.
- Fixed a TLS handshake failure that can’t succeed on retry (a minimum-version mismatch, an untrusted certificate, or a hostname mismatch) being reported by `connect()` as a generic `250001: Could not connect to Snowflake backend after N attempt(s)` with a firewall-troubleshooting hint. The network layer already identified and named such failures, but the authentication layer retried them until the login timeout expired and then replaced the diagnosis. They now surface as `NonRetryableTlsError` (a subclass of `OperationalError` that keeps the same errno, so existing handlers are unaffected) naming the underlying cause, and are no longer retried. Transient handshake faults (`ECONNRESET`, unexpected EOF) remain retryable.

## Version 4.7.4 (Sep 16, 2026)

### New features and updates

- None.

### Bug fixes

- Fixed missing retries on transient HTTP failures when fetching an OAuth access token from the IdP token endpoint (`OAUTH_CLIENT_CREDENTIALS` and `OAUTH_AUTHORIZATION_CODE`). Token requests now retry transport errors, HTTP 408/429, and 5xx responses.
- Fixed a TLS handshake terminated by the peer (`SSLError` containing `SysCallError(-1, 'Unexpected EOF')`) being classified as non-retryable and raised as an `OperationalError`, unlike `ECONNRESET`. Such handshake `Unexpected EOF` errors are now retried on both the sync and async request paths.
- Fixed `fetchone()`, `fetchmany()`, `fetchall()`, and cursor iteration silently returning an incomplete result set. A downloaded result chunk holding fewer rows than the backend reported was treated as a normal end of results, so callers received fewer rows than the query produced with no exception. Such a chunk now raises an `OperationalError` (errno `252013`). Errors raised while iterating a result set are no longer reported as end of results either: `_fetchone()` previously caught every `TypeError` and returned `None`, so a failure anywhere in the download or parse chain was indistinguishable from an exhausted result set. Both the sync and async paths are fixed.

## Version 5.0.0rc3 (Sep 10, 2026)

Third release candidate of the connector built on the Universal Core. See [Upgrading to the Snowflake Connector for Python 5.x](/developer-guide/python-connector/python-connector-upgrade) for installation instructions, the curated list of behavior differences, and migration guidance.

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

Second release candidate of the connector built on the Universal Core. See [Upgrading to the Snowflake Connector for Python 5.x](/developer-guide/python-connector/python-connector-upgrade) for installation instructions, the curated list of behavior differences, and migration guidance.

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

Initial public preview release of the connector built on the Universal Core. This is a new version line, published under the existing `snowflake-connector-python` package name as a release candidate. Because pre-release versions are not installed by default, `pip install --pre snowflake-connector-python` is required. See [Upgrading to the Snowflake Connector for Python 5.x](/developer-guide/python-connector/python-connector-upgrade) for installation instructions, the curated list of behavior differences, and migration guidance.

### New features and updates

- Rebuilt the connector on the Universal Core, a shared Rust library that implements networking, authentication, result-set fetching, and stage transfers for every driver built on it, replacing the pure-Python implementation.
- Published the connector and Universal Core source in the [Snowflake drivers repository](https://github.com/snowflakedb/drivers) on GitHub.
- Added the `snowflake.connector.aio` module, which exposes the PEP 249 `Connection` and `Cursor` objects as asyncio coroutines.
- Published wheels for CPython 3.11, 3.12, 3.13, and 3.14. Python 3.10 installs from the source distribution and compiles the Rust extension locally.

### Changes

- Only one version of the package can be installed in a given environment, so install this version into a separate virtual environment rather than upgrading in place.
- Certificate revocation checking uses CRLs rather than OCSP, and is off by default. OCSP-specific connection parameters are not accepted. See [Certificate revocation checking](/developer-guide/python-connector/python-connector-connect#label-python-crl).
- Snowflake’s Python libraries currently declare a dependency on a connector version below 5.0.0 and cannot be installed alongside this version. See [Upgrade steps](/developer-guide/python-connector/python-connector-upgrade#label-python-upgrade-steps).
- This release contains breaking behavior changes relative to the 4.x connector. The most significant are summarized in [Behavior differences](/developer-guide/python-connector/python-connector-upgrade#label-python-upgrade-behavior), and the complete catalog is published as [`BehaviorDifferences.yaml`](https://github.com/snowflakedb/drivers/blob/main/python/BehaviorDifferences.yaml).

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
