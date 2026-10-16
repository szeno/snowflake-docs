# Upgrading to the Snowflake Connector for Python 5.0.0

Installing the connector replaces the earlier `snowflake-connector-python` package in that environment. The `snowflake.connector` module and the PEP 249 `Connection` and `Cursor` objects stay the same.

Most applications need no code changes beyond the items in [Upgrade steps](#label-python-upgrade-steps). Run your tests with deprecation warnings treated as errors so renamed parameters show up immediately.

## Upgrade steps

Install the connector in a separate virtual environment and keep the previous environment available until validation passes. A failed upgrade is a `pip install` of the previous version in the original environment. It does not restore application code you already edited.

### Step 1: Install the connector and run your tests

The connector requires Python 3.11 or later. See [Installing the Python Connector](/developer-guide/python-connector/python-connector-install).

Before you upgrade a shared environment, check libraries that still require a connector version before 5.0. Installing 5.0.0 there can make `pip` refuse the install, or it can replace a connector those libraries can’t import:

- Snowpark for Python (`snowflake-snowpark-python` 1.55.1) requires `snowflake-connector-python>=3.17.0,<5.0.0`.
- Snowflake ML (`snowflake-ml-python` 2.4.0) requires `snowflake-connector-python[pandas]>=3.17.3,<5`.
- Snowflake SQLAlchemy (`snowflake-sqlalchemy` 1.11.1) requires `snowflake-connector-python<5.0.0`.
- Snowflake CLI (`snowflake-cli` 3.29.0) requires `snowflake-connector-python[secure-local-storage]==4.7.5`.

Install 5.0.0 in a separate virtual environment when any of those libraries are installed.

Copy code

```
pip install --upgrade snowflake-connector-python
python -c "import snowflake.connector; print(snowflake.connector.__version__)"
python -W error::DeprecationWarning -m pytest
```

The printed version should be `5.0.0`. That means this environment is using the connector described here.

`-W error::DeprecationWarning` is a Python command-line option. It turns a `DeprecationWarning` into an error that stops the program. Renamed parameters still connect, and each one emits that warning. With this option, pytest fails at the first old parameter name, so you can see what to change. Use the same option on the command that starts your application, for example `python -W error::DeprecationWarning your_app.py`.

### Step 2: Remove parameters and calls that the connector rejects or ignores

[Parameters and calls that no longer work](#label-python-upgrade-removed) lists parameters that raise an error or that are accepted and then ignored. Replace them before you rely on the old behavior.

In particular:

- Don’t call `Connection.connect()` again. Construct a new connection.

  Note

  Before version 5.0, `connect()` was public, but it was not a working reconnect: the connector cleared secrets after the first login.
- Don’t pass `region`. Pass a fully qualified `account` identifier, such as `myaccount.us-east-1`, or set `host`. Passing `region` warns and forwards the value as a login session parameter named `REGION`. It is not used to build the hostname.
- Don’t pass `converter_class`. Result conversion is not a Python plug-in.
- Don’t pass `password_callback`. Change an expired password outside the connector.
- Don’t pass `backoff_policy`. Set the `retry_backoff_*` parameters.
- If you set `enable_crl_cache=False`, set both `crl_enable_memory_caching=False` and `crl_enable_disk_caching=False`. The old switch has no effect.
- If you passed `create_temp_table=True` to `write_pandas`, pass `table_type='temp'` instead. `create_temp_table` raises `TypeError`.

### Step 3: Re-check certificate revocation

Drivers built on the Universal Core do not support OCSP-based certificate revocation checking. Revocation checking is available only through CRLs (certificate revocation lists), and it is off by default.

If you require revocation checking, enable CRL checking and evaluate it in a non-production environment under a realistic workload. Confirm that your network allows outbound access to the CRL distribution points named in Snowflake’s certificate chain: a driver that cannot reach a distribution point cannot complete a revocation check.

`ocsp_fail_open`, `ocsp_response_cache_filename`, and `insecure_mode` do not configure revocation. `connect()` does not reject them. It warns and forwards each unknown key as a login session parameter. Configure `crl_check_mode` and the CRL cache parameters instead. See [Certificate revocation checking](/developer-guide/python-connector/python-connector-connect#label-python-crl).

Note

Before version 5.0, the connector checked revocation with OCSP, and those parameters controlled that check.

### Step 4: Re-check proxy, OAuth, and token caching

- The connector reads `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` unless you pass `use_proxy_env=False`. Explicit `proxy_host`, `proxy_port`, and the `proxy` URL still win when both are set.

  Note

  Before version 5.0 (since 3.17.0), the connector always read those variables, and they overrode explicit `proxy_host` and `proxy_port`.
- If `oauth_token_request_url` or `oauth_authorization_url` uses `http://` for a host that is not a loopback address, switch it to `https://`.

  Note

  Before version 5.0, an `http://` token URL logged a warning and the request continued.
- `client_store_temporary_credential` defaults to `True` on every platform. An explicit `False` disables ID, OAuth, and MFA token caching, including on macOS and Windows.

  Note

  Before version 5.0, the connection parameter defaulted to `False`. External-browser login on macOS and Windows still cached an ID token when you omitted the flag.
- If you depend on the previous console-login default, set `oauth_disable_console_login` explicitly. The current default is `False`, so omitting it enables console login for external-browser authentication. That default is still being confirmed. The old name still maps to the new one and emits a `DeprecationWarning`.

  Note

  Before version 5.0, `disable_console_login` defaulted to `True`, which asked for the SSO URL instead of the console-login URL.
- Expect one extra authentication after upgrading if you depend on a cached token. Token cache files are not reused unchanged from the previous connector.

### Step 5: Re-check cursor and fetch error handling

Note

Before version 5.0, a closed cursor raised `InterfaceError` only from `execute()`. Other methods raised `TypeError` or `AttributeError`, or had no guard. Fetching before `execute()` raised `TypeError`.

Cursor methods raise `InterfaceError` with errno `252006` when the cursor is closed. `fetchone`, `fetchmany`, `fetchall`, and iteration before any query raise `ProgrammingError` with errno `252009`. Rows already buffered on the cursor stay readable after `connection.close()`.

`executemany()` on an `INSERT` that has no `VALUES` clause raises `ProgrammingError` with errno `252001`.

Note

Before version 5.0, that call raised `InterfaceError` with the same errno.

### Step 6: Validate before you switch

Confirm authentication, representative queries, metadata calls, pandas or Arrow fetches, and any PUT or GET your application uses. Move the tested environment to production only after those checks pass.

### Step 7: Update renamed parameters

The names in [Renamed and deprecated parameters](#label-python-upgrade-renamed) still work. Update call sites to the current name. Rows other than the certificate-revocation aliases emit a `DeprecationWarning`. Those aliases do not warn. Only these time parameters change units: `crl_connection_timeout_ms`, `crl_read_timeout_ms`, `crl_cache_validity_hours`, `crl_cache_removal_delay_days`, and `crl_cache_cleanup_interval_hours`. `cert_revocation_check_mode`, `enable_crl_memory_cache`, `enable_crl_file_cache`, and `allow_certificates_without_crl_url` keep the same values.

## Renamed and deprecated parameters

These current names are what the connector docs describe. The previous name still works unless the row says otherwise.

| Previous name (before 5.0) | Current name | How it worked before 5.0 |
| --- | --- | --- |
| `private_key_file_pwd`, `private_key_passphrase` | `private_key_password` | Passphrase for an encrypted private key file. The old names are accepted and mapped to `private_key_password`, with a `DeprecationWarning`. *(BD#5)* |
| `client_request_mfa_token` | `client_store_temporary_credential` | `client_request_mfa_token=True` enabled MFA token caching. The old name is accepted as an alias and warns. The current parameter also covers ID and OAuth token caching, and it defaults to `True`. *(BD#16, BD#97)* |
| `client_fetch_threads` | `client_prefetch_threads` | Set the chunk-fetch pool size. It defaulted to `client_prefetch_threads`. The old name is a deprecated alias. *(BD#25)* |
| `enable_stage_s3_privatelink_for_us_east_1` | `use_s3_regional_url` | Forced PUT and GET to use the S3 regional endpoint. The `_for_us_east_1` suffix was historical: it applied to every S3 region. The old connection argument is a deprecated alias. The server session parameter `ENABLE_STAGE_S3_PRIVATELINK_FOR_US_EAST_1` is still honored. *(BD#30)* |
| `network_timeout` | `query_timeout` and `request_timeout` | One wall-clock budget for non-login HTTP operations. It defaulted to no cap, and `conn.network_timeout` returned `None` when unset. The value is copied to both new parameters unless you set one of them yourself. `conn.network_timeout` returns `request_timeout` (default 120). Using the old name emits a `DeprecationWarning`. *(BD#52)* |
| `socket_timeout` | `connect_timeout` and `retry_timeout` | Per-attempt read-inactivity timeout. It reset on every received byte, so a slow but active download did not trip it. The value is copied to both new parameters. `retry_timeout` is a hard cap on the whole HTTP attempt, including the body download, so `socket_timeout=30` can abort an active chunk download at 30 seconds. `conn.socket_timeout` returns `retry_timeout` (default `None`). *(BD#52)* |
| `disable_console_login` | `oauth_disable_console_login` | Defaulted to `True`, so external-browser login asked for the SSO URL. The current parameter defaults to `False`, and that default is still being confirmed. Set it explicitly if you depend on the previous behavior. The old name is a deprecated alias. *(BD#99)* |
| `external_browser_timeout` | `authentication_timeout` | Seconds to wait for an external-browser authentication response. The old name is a deprecated alias of `authentication_timeout` (default 120). That budget also covers Okta and OAuth authentication, so setting the old name changes those flows too. |
| `oauth_socket_uri` | `oauth_redirect_uri` | Loopback URI for the OAuth redirect. Before version 5.0, the listener could bind a different host or port from the URI sent to the IdP. The listener binds `oauth_redirect_uri`. The old name is a deprecated alias. |
| `skip_file_permissions_check` | `unsafe_skip_config_file_permissions_check` and `crl_unsafe_skip_file_permissions_check` | One flag skipped permission checks on both configuration files and the CRL cache. The value is copied to both parameters unless you set one of them. |
| `cert_revocation_check_mode` | `crl_check_mode` | Enum (`DISABLED`, `ADVISORY`, `ENABLED`). The old name is a silent alias. `crl_check_mode` is a string with the same values and defaults to `DISABLED`. |
| `enable_crl_memory_cache` | `crl_enable_memory_caching` | In-memory CRL cache switch. The old name is a silent alias. Default is `True`. *(BD#42)* |
| `enable_crl_file_cache` | `crl_enable_disk_caching` | On-disk CRL cache switch. Before version 5.0, it applied only when `enable_crl_cache` was `True`. The old name is a silent alias. Default is `True`. *(BD#42)* |
| `allow_certificates_without_crl_url` | `crl_allow_certificates_without_crl_url` | Allow certificates that have no CRL distribution point. The old name is a silent alias. |
| `crl_connection_timeout_ms` | `crl_connection_timeout` | Connection timeout in milliseconds (default 3000). The current parameter is seconds (default 10). The old name is accepted and converted. |
| `crl_read_timeout_ms` | `crl_http_timeout` | Read timeout in milliseconds (default 3000). The current parameter is seconds (default 10). The old name is accepted and converted. |
| `crl_cache_validity_hours` | `crl_validity_time` | Cache lifetime in hours (default 24). The current parameter is seconds (default 86400). The old name is accepted and converted. |
| `crl_cache_removal_delay_days` | `crl_on_disk_cache_removal_delay` | How long to keep expired CRL files, in days (default 7). The current parameter is seconds (default 604800). The old name is accepted and converted. |
| `crl_cache_cleanup_interval_hours` | `crl_cache_cleanup_interval` | Cleanup interval in hours (default 1). The current parameter is seconds (default 3600). The old name is accepted and converted. |

Expand

Show lessSee more

`login_timeout` keeps its name. The default is 120, and the property returns 120 when unset. *(BD#52)*

Note

Before version 5.0, the connector applied a 120-second budget internally, but `conn.login_timeout` returned `None` when you did not set it.

## Parameters and calls that no longer work

| Previous name or call | What to do | How it worked before 5.0 |
| --- | --- | --- |
| `client_fetch_use_mp` | Remove it. Chunk fetch always uses a thread pool. Passing it warns and has no effect. | `True` switched the chunk-fetch pool from threads to processes. *(BD#25)* |
| `oauth_enable_refresh_tokens` | Remove it. The connector always uses a refresh token when the IdP returns one. Use `client_store_temporary_credential` to control caching. Passing it warns and has no effect. | Default `True`. When `False`, the connector did not use the refresh token to renew an expired access token. *(BD#28)* |
| `enable_crl_cache` | Set `crl_enable_memory_caching` and `crl_enable_disk_caching`. Passing it warns and has no effect. | Master switch for both CRL caches (default `True`). `False` disabled memory and disk caches regardless of `enable_crl_file_cache`. *(BD#42)* |
| `backoff_policy` | Set `retry_backoff_base_ms` (default 250), `retry_backoff_cap_ms` (default 16000), `retry_backoff_factor` (default 2), and `retry_backoff_jitter` (`none`, `full`, or `decorrelated`; default `decorrelated`). Passing `backoff_policy` warns and has no effect. | A generator, such as `exponential_backoff()` or a custom function, computed the delay before each retry. Defaults were a 1-second initial delay and full jitter. The 16-second cap and 2x factor are unchanged. *(BD#58)* |
| `create_temp_table` on `write_pandas` | Pass `table_type='temp'`. Passing `create_temp_table` raises `TypeError`. | `create_temp_table=True` was a deprecated alias for `table_type='temp'` and emitted a `DeprecationWarning`. *(BD#19)* |
| `region` | Pass a fully qualified `account` or set `host`. Passing `region` warns and forwards the value as a login session parameter named `REGION`. It is not used to build the hostname, and `Connection` has no `region` property. | Built the Snowflake hostname. `Connection.region` returned the value and emitted a `PendingDeprecationWarning`. *(BD#24)* |
| `Connection.connect()` | Construct a new `Connection`. There is no public `connect()` method. | Public method called at the end of construction. It was not a usable reconnect, because credentials were cleared after login. *(BD#23)* |
| `converter_class` | Remove it. Passing a class raises `ProgrammingError`. `DefaultConverterClass` does not exist. | Selected a converter, including `SnowflakeNoConverterToPython` to skip native type conversion. *(BD#103)* |
| `password_callback` | Change the expired password outside the connector. Passing it raises `ProgrammingError`. | Called when login returned `PWD_CHANGE`. The return value was sent as `CHOSEN_NEW_PASSWORD`. *(BD#100)* |
| `disable_request_pooling` | Remove it. Passing it warns and has no effect. Reading `Connection.disable_request_pooling` raises `AttributeError`. | `True` stopped reusing HTTP sessions across REST calls. *(BD#88)* |
| `iobound_tpe_limit` | Remove it. Passing it warns and has no effect. `Connection.iobound_tpe_limit` does not exist. | Capped the number of I/O worker threads for PUT and GET. *(BD#101)* |
| `client_session_keep_alive` and `client_session_keep_alive_heartbeat_frequency` setters | Read the properties. Assignment raises `AttributeError`. | Setters existed, but they wrote a private attribute and did not change the live heartbeat thread. *(BD#26)* |
| OCSP parameters (`ocsp_fail_open`, `ocsp_response_cache_filename`, `insecure_mode`, and related settings) | Configure CRL parameters. Passing these names warns and forwards them as login session parameters. They have no effect on revocation checking. | Certificate revocation used OCSP. *(BD#104)* |
| Logging `[log]` configuration (`save_logs`, `path`, `level`) | Set `SNOWFLAKE_TROUBLESHOOTING_ENABLED=true` to capture driver troubleshooting logs. There is no configurable log path or rotation schema. | A logging configuration file configured a rotating file handler. *(BD#80)* |
| `dsn`, `session_id` as a connect argument, `support_negative_year`, `json_result_force_utf8_decoding`, `inject_client_pause`, `probe_connection`, `debug_arrow_chunk`, `snowflake_server_dop_cap_for_file_transfer`, `reraise_error_in_file_transfer_work_function` | Remove them. Each one warns and has no effect. `connection.session_id` after login still returns the server-assigned id. | Accepted connect arguments. *(BD#98)* |
| `log_imported_packages`, `log_imported_packages_in_telemetry` | Remove them. They are ignored with no warning. | Accepted connect arguments. *(BD#98)* |

Expand

Show lessSee more

## Behavior differences

Every behavior difference between the generally available driver and the version built on the Universal Core is catalogued in the driver source repository, as a machine-readable file listing each entry’s previous behavior, new behavior, classification, and whether it is a breaking change. Read it in full before you upgrade an application you cannot easily roll back:

- [Snowflake Connector for Python behavior-difference catalog](https://github.com/snowflakedb/drivers/blob/main/python/BehaviorDifferences.yaml)

The sections above summarize the entries most likely to affect an existing application. The catalog is the complete list.

The following list summarizes breaking differences between versions before 5.0 and the current connector. Where a difference is still being confirmed, the bullet says so. Entries marked `fixed` in the catalog were preview regressions. They are listed under [Resolved during preview](#label-python-upgrade-resolved) and are not differences you need to code around.

### Authentication, proxy, and sessions

- **Proxy environment variables are read unless you opt out.** `use_proxy_env` defaults to `True`. Pass `False` to ignore `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY`. Explicit `proxy_host`, `proxy_port`, `proxy_user`, `proxy_password`, and `no_proxy` still work, and they win over the environment. The legacy `proxy` URL form is also accepted. *(BD#31)*
- **OAuth token and authorization URLs must use HTTPS.** A non-loopback `http://` value is rejected at connect time. `http://` is still accepted for loopback hosts (`127.0.0.0/8`, `::1`, and `localhost`). *(BD#38)*
- **`oauth_credentials_in_body=True` sends the client secret in the body only.** The default remains HTTP Basic. *(BD#29)*

  Note

  Before version 5.0, the connector sent the secret in both the HTTP Basic header and the body.
- **A bad OAuth client secret includes the IdP error slug** in the login failure, for example `invalid_client`. *(BD#35)*

  Note

  Before version 5.0, the message was a generic browser-login error.
- **Session-token login requires `master_token`, and invalid tokens fail in `connect()`.** An invalid token raises `DatabaseError` from `connect()`. Omitting `master_token` raises `ProgrammingError`. *(BD#37)*

  Note

  Before version 5.0, the session token was used as a bearer with no upfront check, and a bad token failed later as `HttpError` (errno 290401).
- **External-browser login does not silently re-authenticate** when the master token expires mid-session. The connector raises `ReauthenticationRequest` instead of opening the browser again and retrying the query. Open a new connection to run the browser flow again. *(BD#82)*

  Note

  Before version 5.0, the connector reran the browser flow and retried the query.
- **`ReauthenticationRequest` is raised for master-token expiry** and is importable from `snowflake.connector.errors` and `snowflake.connector.network`. It subclasses `ProgrammingError` and warns that the base class moves to `OperationalError` in a future major release. *(BD#44)*
- **Interactive prompts for the same user and host are serialized** when `client_store_temporary_credential=True` and `disable_parallel_user_prompt=True` (the default). Set `disable_parallel_user_prompt=False` to show one prompt per concurrent connection. *(BD#33)*

  Note

  Before version 5.0, each connection prompted.
- **A bare `connect()` keeps the auto-detected `application` name** when a default connection profile is also loaded. An explicit `application=` still wins. *(BD#59)*

  Note

  Before version 5.0, loading the default profile discarded `SF_PARTNER` and Streamlit or Jupyter detection.

### Cursors, binding, and results

- **Closed cursors raise `InterfaceError` (errno 252006)** from cursor methods. See [Upgrade steps](#label-python-upgrade-steps). *(BD#21)*
- **Fetching before `execute()` raises `ProgrammingError` (errno 252009).** *(BD#22)*
- **`file_stream` on a statement that is not PUT raises `ProgrammingError`.** *(BD#49)*

  Note

  Before version 5.0, the argument was ignored and the statement ran.
- **`executemany()` asks the server whether array binding is supported.** For current Snowflake SQL the outcome is unchanged. Non-`VALUES` `INSERT` rewrite failures raise `ProgrammingError`. *(BD#34, BD#93)*

  Note

  Before version 5.0, the connector matched `INSERT` with a client-side regular expression, and those rewrite failures raised `InterfaceError`.
- **Session parameters set by one cursor are visible to other cursors** on the same connection without another query. *(BD#15)*

  Note

  Before version 5.0, a cursor that had not executed a query kept its own copy.
- **`fetch_pandas_all`, `fetch_pandas_batches`, and `fetch_arrow_*` accept JSON result sets** such as `SHOW`, `DESCRIBE`, and PUT or GET. *(BD#92)*

  Note

  Before version 5.0, those methods raised `NotSupportedError` unless the server returned Arrow.
- **`JSONResultBatch` and `ArrowResultBatch` are aliases of `ResultBatch`.** `to_arrow()` and `to_pandas()` work on every batch. *(BD#18)*

  Note

  Before version 5.0, calling them on a JSON batch raised `NotSupportedError`.
- **`ResultBatch` has no `session_manager` or `http_config`.** Chunk download is handled inside the core. After unpickling a batch, you can pass a live `Connection`, but you don’t have to. *(BD#20)*
- **`pandas.concat` keyword arguments are not accepted by `fetch_pandas_all` or `fetch_pandas_batches`.** Arguments of `Table.to_pandas` (`split_blocks`, `types_mapper`, and similar) are forwarded. `sort`, `keys`, and `copy` raise `TypeError`. *(BD#51)*

  Note

  Before version 5.0, those arguments were forwarded to `pandas.concat`.
- **An unsupported bind value raises `ProgrammingError` with errno 255001.** `except ProgrammingError` still matches. *(BD#89)*

  Note

  Before version 5.0, the same class was raised with errno 252011 and a different message.
- **`display_size` is set for text columns** to the character length. *(BD#90)*

  Note

  Before version 5.0, it was always `None`.
- **Non-string `session_parameters` values are sent as JSON strings.** `True` is sent as `"true"` and `5` as `"5"`. *(BD#57)*

  Note

  Before version 5.0, booleans and numbers were native JSON literals.

### Files, configuration, and errors

- **A `ConfigManager` created without `file_path` raises `MissingConfigOptionError` when you read an option.** *(BD#14)*

  Note

  Before version 5.0, the same call raised `ConfigManagerError` about the missing path.
- **An empty `connections.toml` no longer hides connections from `config.toml`.** *(BD#13)*

  Note

  Before version 5.0, an empty `connections.toml` replaced those connections with an empty set.
- **A failed GET removes its `.part` staging file.** *(BD#39)*

  Note

  Before version 5.0, an interrupted download could leave `<destination>.part` behind.
- **PUT of a symlinked source uses the target file’s base name** on the stage. A relative path that contains a symlink directory and `..` can also select a different file, because the connector resolves the path on the filesystem. *(BD#81)*

  Note

  Before version 5.0, a relative path was normalized lexically, and a symlinked file was uploaded under the symlink’s own name.
- **The `file` column of a GET result is the local file’s base name**, including when the stage key has more than one directory level. *(BD#102)*

  Note

  Before version 5.0, only the first path segment was removed, so `prefix/subdir/file.csv` was reported as `subdir/file.csv`.
- **An `AUTO_COMPRESS` gzip upload omits the original file name from the gzip header.** The compressed file is smaller than the file produced before version 5.0, and a byte-for-byte comparison with those uploads does not match. *(BD#1)*
- **`SOURCE_COMPRESSION=AUTO_DETECT` recognizes DEFLATE files.** The upload keeps the DEFLATE payload and the original file name. *(BD#2)*

  Note

  Before version 5.0, a DEFLATE file was treated as uncompressed and uploaded again as gzip (`filename.gz`).
- **`SOURCE_COMPRESSION=BROTLI` is supported.** *(BD#3)*

  Note

  Before version 5.0, that option raised error 253007 (`Feature is not supported`).
- **`put_get_max_attempts` is not clamped to an upper bound.** Values of 0 or less fall back to 6. *(BD#95)*

  Note

  Before version 5.0, a large retry count was clamped.
- **Azure Blob PUT does not set `Content-Encoding` or `x-ms-blob-content-encoding`.** Reading those blobs still works. *(BD#32)*

  Note

  Before version 5.0, the connector set `Content-Encoding: utf-8`, which Azure stored on the blob.
- **Azure client-side encryption metadata reports `EncryptionAgent.EncryptionAlgorithm` as `AES_CBC_256`.** `KeyWrappingMetadata.EncryptionLibrary` is `Rust(OpenSSL)`. *(BD#46)*
- **Any Azure HTTP 403 during PUT or GET refreshes the SAS token and retries.** A failed refresh raises a terminal error instead of retrying without a limit. *(BD#40, BD#41)*
- **`Connection.is_valid()` returns true for a live `PAT_WITH_EXTERNAL_SESSION` connection.** *(BD#109)*
- **S3 endpoints in `cn-*` regions are chosen by the AWS SDK** when no regional-URL flag or explicit endpoint is set. This path is not yet verified against a live China-region stage. *(BD#27)*
- **`snowflake.connector.options` is not a module.** Import optional-dependency helpers from `snowflake.connector._common.extras`. *(BD#91)*
- **`snowflake.connector.dbapi` is not a module. Authenticator classes such as `AuthByOkta` are not exported from `snowflake.connector.auth`.** Configure authentication with connection parameters. *(BD#105)*
- **File-transfer constants and type helpers are not exported from `snowflake.connector.constants`.** `QueryStatus` remains. `DownloadMetrics`, `RemoteChunkInfo`, and the SSE-C constants are not exported from `result_batch`. *(BD#107, BD#108)*
- **Legacy HTTP exception classes stay importable from `snowflake.connector.errors` and are not raised.** The first access emits a `DeprecationWarning`. Failures use PEP 249 exception types, so `except HttpError` does not catch them. *(BD#106)*
- **Connection-config validation errors set `Error.parameter` and `Error.validation_code`.** Both are `None` for other errors. *(BD#48)*

  Note

  Before version 5.0, callers had to match the message text.

## Resolved during preview

These items were preview regressions. The connector now matches the previous connector, so they are not differences you need to prepare for.

- `ResultMetadataV2.fields` is populated for VECTOR and structured types, and `vector_dimension` is set. *(BD#54)*
- `internal_size` is the character count. *(BD#55)*

  Note

  Before version 5.0, `internal_size` was also the character count.
- `workload_identity_aws_use_outbound_token` is accepted again. *(BD#94)*
- A native Okta authenticator rejection includes the Snowflake message. *(BD#96)*
- `ReauthenticationRequest` is raised for the master-token codes listed in BD#44. The remaining gap is external-browser auto-reauthentication, covered by BD#82.
