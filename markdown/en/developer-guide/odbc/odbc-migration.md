# Migrating from ODBC Driver 3.x to 4.x

Version 4.x of the Snowflake ODBC Driver is built on the [Universal Core](/developer-guide/universal-core/universal-core). It is the next version of the driver you already use, not a new product. Installing 4.x on a machine replaces the 3.x driver.

The Universal Core (`sf_core`) is a shared Rust library that implements the networking, authentication, result-set fetching, and stage-transfer logic that every Snowflake driver needs. Each driver wraps that core in a thin, language-specific layer that exposes the interface its ecosystem expects; the Rust layer is not visible to application code.

Snowflake previously maintained a separate implementation of this logic in each driver, so a security fix or protocol change had to be applied separately to every one. Because the core is shared, a change to it reaches every driver built on it in that driver’s next release.

The driver implements the same ODBC API surface and accepts the same connection-string keywords as the 3.x driver, except where this page notes differences. Use the explicitly versioned installation guides for your target driver.

Most applications need no code changes. The steps in [Migration steps](#label-odbc-migration-steps) help you find the applications that do.

## What’s improved

- **Improved stage transfers:** PUT and GET operations, including multipart upload, chunk-level retry, and cloud-provider-specific signing (S3, Azure Blob Storage, Google Cloud Storage), are handled by the Universal Core. GET now auto-creates missing destination directories and uses atomic `.part` file writes to avoid corrupt partial downloads.
- **Richer diagnostics:** The connection diagnostic service (controlled by `ENABLE_CONNECTION_DIAG` in the connection string) runs inside the Universal Core and produces a structured connectivity report. Troubleshooting logs can be captured without any code change by setting `SNOWFLAKE_TROUBLESHOOTING_ENABLED=true`.
- **Smaller surface for bugs:** The ODBC wrapper itself contains no protocol logic, which reduces the places where driver-specific bugs can be introduced and simplifies maintenance.
- **Open sourced code:** The driver and Universal Core source are available in the [Snowflake drivers repository](https://github.com/snowflakedb/drivers) on GitHub, so you can inspect the implementation, file issues, and contribute.

**Unified security model:** TLS, certificate revocation checking, token refresh, and OAuth flows are implemented once in the Universal Core and behave the same way across every driver built on it. A fix in any of these areas reaches all of those drivers rather than being reimplemented per language.

**Consistent cross-driver behavior:** Because networking, authentication, and stage-transfer logic live in the Universal Core, the same query, the same authentication flow, and the same error condition produce the same outcome across drivers built on it.

## Migration steps

Before changing a production host, save its current installer, DSN settings, and driver configuration.
Keep the original 3.x environment available while you validate 4.x separately, and agree on a recovery plan
with your application owner before cutover. Installing 3.x again alone does not restore changed configuration.

### Step 1: Install on a test host and point a DSN at it

Installing ODBC 4.x replaces the 3.x driver on that machine. See [Downloading the ODBC Driver 4.x](/developer-guide/odbc/odbc-download).

Create a new DSN entry pointing to **Snowflake ODBC** with the same account, role, warehouse, and credentials as your existing DSN. Because 4.x replaces 3.x on the machine, existing DSNs that name **SnowflakeDSIIDriver** no longer resolve there and must be repointed.

After connecting, call `SQLGetInfo(SQL_DRIVER_VER)` to confirm you are on 4.x. The version string uses the zero-padded `MM.mm.bbbb` format, for example `04.00.0000`.

### Step 2: Run your test suite against the new DSN

Point your application or test suite at the new DSN. Watch for the items listed in [Behavior differences](#label-odbc-migration-behavior-differences), especially:

- Key pair authentication using a raw `EVP_PKEY*` pointer: use `SQLSetConnectAttr` with `SQL_SF_CONN_ATTR_PRIV_KEY_CONTENT` or `SQL_SF_CONN_ATTR_PRIV_KEY_BASE64`, or set `PRIV_KEY_FILE` in the DSN or connection string.
- Vendor prefix from `SQLGetDiagRec` messages.
- OAuth flows using `http://` token or authorization endpoints: switch to `https://`.
- Proxy configuration that relied on `HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY` being read automatically: set `USE_PROXY_ENV=true`.
- Catalog calls that pass a NULL `CatalogName` and expect the current database: set `UseCurrentCatalog=true` or enable `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX`.
- Applications that catch SQLSTATE `HY000` for an unsupported `SQL_GUID` parameter type: 4.x returns `07006`.
- Applications that catch the server SQLSTATE `42601` for skipped parameter numbers on `SQLExecDirect`: 4.x rejects the call locally with `HY000`.

### Step 3: Switch error handling for diagnostic messages

If your application catches specific vendor strings or error-trace content from `SQLGetDiagRec`, update it to handle the new `[Snowflake][Snowflake ODBC Driver]` prefix and the appended internal trace, or set `ErrorTraceEnabled=false` in `sf.odbc.ini` to suppress the trace.

### Step 4: Re-check certificate revocation checking

Version 4.x does not implement OCSP. Revocation checking is available only through certificate revocation lists (CRLs), and it is off by default. The `DisableOCSPCheck` and `OCSP_FAIL_OPEN` connection parameters are accepted but ignored, with a deprecation warning. Keeping an OCSP fail-close setting in your connection string does not enable revocation checking in 4.x.

If you require fail-close revocation checking, set `CRL_MODE=ENABLED` and evaluate it in a non-production environment under a realistic workload. Confirm that your network allows outbound access to the CRL distribution points named in Snowflake’s certificate chain. See [ODBC 4.x](/developer-guide/odbc/odbc-parameters#label-odbc-crl-4x).

### Step 5: Re-check OAuth, proxy, and token-cache configuration

- If you use `OAUTH_TOKEN_REQUEST_URL` or `OAUTH_AUTHORIZATION_URL` with a plaintext `http://` endpoint (other than a loopback address), switch it to `https://`.
- If you rely on `HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY` environment variables being picked up automatically, set `USE_PROXY_ENV=true` on the connection.
- Tokens cached by ODBC 3.x are stored in `credential_cache_v1.json`. Version 4.x reads `credential_cache_v2.json`, so expect one extra authentication after upgrading.

### Step 6: Validate before cutover

Confirm that authentication, representative queries, metadata calls, and any file transfers used by your application
work on the test host. Apply the tested configuration to production only after these checks pass. If validation fails,
keep the application on its original 3.x environment while you investigate.

## Installation changes by operating system

Installing 4.x replaces 3.x on that machine. Validate the migration on a dedicated host, VM, or container first.
The tables below show only installation differences. Use the linked version-specific guides for complete instructions.

### Linux

[Install ODBC 4.x on Linux](/developer-guide/odbc/odbc-linux) · [Install ODBC 3.x on Linux](/developer-guide/odbc/odbc-linux-3x)

| What changes | 3.x | 4.x |
| --- | --- | --- |
| Driver name | `SnowflakeDSIIDriver` | `Snowflake ODBC` |
| Library | `libSnowflake.so` | `libsfodbc.so` |
| Configuration file | `simba.snowflake.ini` | `sf.odbc.ini` |
| Archive | `.tgz`, with setup scripts | `.tar.gz`, manual registration |

Expand

Show lessSee more

After extracting a 4.x archive, register the library from `usr/lib64/snowflake/odbc/lib/` under **Snowflake ODBC**.
The archive does not include `unixodbc_setup.sh` or `iodbc_setup.sh`. RPM and DEB installations register the driver
through their installer; both use `/usr/lib64/snowflake/odbc/` in 4.x. The 3.x DEB directory was `/usr/lib/snowflake/odbc/`.

Update DSNs that use the old registration name or library path. For unixODBC, check registration with:

Copy code

```
odbcinst -q -d -n "Snowflake ODBC"
```

Create a user-level `sf.odbc.ini` for logging and driver-manager encoding. Do not copy the 3.x INI file unchanged.
See [configuration differences](#label-odbc-migration-config) and [Linux configuration](/developer-guide/odbc/odbc-linux#label-odbc-configure-driver).

### macOS

[Install ODBC 4.x on macOS](/developer-guide/odbc/odbc-mac) · [Install ODBC 3.x on macOS](/developer-guide/odbc/odbc-mac-3x)

| What changes | 3.x | 4.x |
| --- | --- | --- |
| DSN driver reference | Legacy library path | `Snowflake ODBC` |
| Library | `libSnowflake.dylib` | `libsfodbc.dylib` |
| Configuration file | `simba.snowflake.ini` | `sf.odbc.ini` |
| Disk image | Legacy `.dmg` naming | Universal `.dmg` naming |

Expand

Show lessSee more

Use the exact filenames in [4.x downloads](/developer-guide/odbc/odbc-download) or
[3.x macOS installation](/developer-guide/odbc/odbc-mac-3x). Update each DSN’s driver reference before testing.
The 4.x installer sets `DriverManagerEncoding=UTF-32` for iODBC. If you use unixODBC, set `UTF-16` in a user-level
`sf.odbc.ini`; see [macOS installation](/developer-guide/odbc/odbc-mac).

### Windows

[Install ODBC 4.x on Windows](/developer-guide/odbc/odbc-windows) · [Install ODBC 3.x on Windows](/developer-guide/odbc/odbc-windows-3x)

| What changes | 3.x | 4.x |
| --- | --- | --- |
| Driver name | `SnowflakeDSIIDriver` | `Snowflake ODBC` |
| Library | `SnowflakeDSIIDriver.dll` | `sfodbc.dll` |
| Logging controls | Legacy tracing controls | `sf.odbc.ini` |
| MSI architectures | 32-bit or 64-bit | 32-bit, 64-bit, or ARM64 |

Expand

Show lessSee more

Choose an MSI that matches the application architecture. The 4.x installation directory is
`%ProgramFiles%\Snowflake ODBC Driver\`. Repoint DSNs that still name **SnowflakeDSIIDriver** to **Snowflake ODBC**.
Configure logging in `sf.odbc.ini` instead of the former `Tracing(0-6)` field; see
[configuration differences](#label-odbc-migration-config).

## Configuration differences

Most connection parameters and DSN keywords are shared with the 3.x ODBC driver. The items below are specific to or behave differently in ODBC 4.x.

### sf.odbc.ini (replaces simba.snowflake.ini)

Process-wide logging for ODBC 4.x is configured in `sf.odbc.ini`, not `simba.snowflake.ini`. The driver searches the following locations and uses the first existing file:

1. `$SF_ODBC_INI` (explicit override)
2. The platform configuration directory:
   - Linux: `$XDG_CONFIG_HOME/snowflake/sf.odbc.ini`, or `~/.config/snowflake/sf.odbc.ini` if `XDG_CONFIG_HOME` is unset.
   - macOS: `~/Library/Application Support/snowflake/sf.odbc.ini`
   - Windows: `%APPDATA%\snowflake\sf.odbc.ini` (Roaming AppData)
3. `~/.snowflake/sf.odbc.ini` (on Windows, `%USERPROFILE%\.snowflake\sf.odbc.ini`)
4. `/opt/snowflake/snowflakeodbc/sf.odbc.ini` (macOS only, installer default)

On Unix the file must be `chmod 600`; the driver logs a warning and falls back to defaults if permissions are looser.

Recognized keys (all case-insensitive):

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `LogEnabled` | bool | `true` | Master switch for the driver log file. |
| `LogLevel` | enum | `INFO` | `OFF`, `ERROR`, `WARN`, `INFO`, `DEBUG`, `TRACE`. |
| `LogPath` | path | None | Directory for the rolling log file. |
| `LogFile` | string | `snowflake_odbc.log` | Log file name. |
| `LogRotation` | enum | `NEVER` | `NEVER`, `DAILY`, `HOURLY`, `MINUTELY`. |
| `LogMaxCount` | integer | None | Number of rotated files to retain. |
| `LogMaxSize` | bytes | None | Accepted but ignored. Size-based log rotation is not implemented. |
| `LogQueryText` | bool | `false` | Log SQL text of executed statements (sensitive). |
| `LogQueryParameters` | bool | `false` | Log bound parameter values (sensitive). |
| `ErrorTraceEnabled` | bool | `true` | Append an internal error trace to `SQLGetDiagRec` messages. Set to `false` to restore 3.x-driver-shaped error messages. |

Expand

Show lessSee more

### DriverManagerEncoding

The `DriverManagerEncoding` key in `sf.odbc.ini` selects the wide-character encoding the driver uses to communicate with the driver manager:

| Value | Use when |
| --- | --- |
| `UTF-16` (default) | unixODBC, Windows DM, or any driver manager where `SQLWCHAR` is 2 bytes. |
| `UTF-32` | iODBC with `SQLWCHAR` as `wchar_t` (4 bytes on Linux/macOS). |

Expand

Show lessSee more

The macOS installer sets `UTF-32` in the bundled `sf.odbc.ini` to match macOS’s stock iODBC. If you use unixODBC on macOS, create a user-level `sf.odbc.ini` and set `DriverManagerEncoding=UTF-16`.

### Certificate revocation checking

Drivers built on the Universal Core do not support OCSP-based certificate revocation checking. Revocation checking is available only through CRLs (certificate revocation lists), and it is off by default.

If you require revocation checking, enable CRL checking and evaluate it in a non-production environment under a realistic workload. Confirm that your network allows outbound access to the CRL distribution points named in Snowflake’s certificate chain: a driver that cannot reach a distribution point cannot complete a revocation check.

### Troubleshooting logs

To capture all driver log events at any level with no code change, set these environment variables before starting the ODBC application:

Copy code

```
export SNOWFLAKE_TROUBLESHOOTING_ENABLED=true
export SNOWFLAKE_TROUBLESHOOTING_REPORT_PATH=/tmp/sfodbc
isql -v my_snowflake
```

Collect `/tmp/sfodbc/sf_driver_troubleshooting.log` and include it in support tickets.

### Connection diagnostics

To run a connectivity probe (DNS, TLS, CRL, proxy, stage allowlist) add these keywords to the connection string:

Copy code

```
ENABLE_CONNECTION_DIAG=true;CONNECTION_DIAG_LOG_PATH=/tmp/sfdiag
```

The probe writes `SnowflakeConnectionTestReport.txt` to the specified directory.

### connections.toml profiles

ODBC 4.x supports `connections.toml` profiles for setting connection parameters outside the DSN or connection string.
It selects the directory for `connections.toml` as follows:

1. Use the directory specified by `SNOWFLAKE_HOME`, or `~/.snowflake` if the variable is unset, when that directory exists.
2. If that directory does not exist, use the platform configuration directory:
   - Linux: `$XDG_CONFIG_HOME/snowflake/connections.toml`, or `~/.config/snowflake/connections.toml` if `XDG_CONFIG_HOME` is unset.
   - Windows: `%USERPROFILE%\AppData\Local\snowflake\connections.toml`
   - macOS: `~/Library/Application Support/snowflake/connections.toml`

The fallback depends on whether the directory exists, not whether it contains `connections.toml`.
See [Connecting using the connections.toml file](/developer-guide/odbc/odbc-parameters#label-odbc-connection-toml).

### Renamed or replaced parameters

| Previous name (3.x) | 4.x name or replacement |
| --- | --- |
| `simba.snowflake.ini` | `sf.odbc.ini` |
| `SnowflakeDSIIDriver` | `Snowflake ODBC` |
| `SQL_SF_CONN_ATTR_PRIV_KEY` | Set `SQL_SF_CONN_ATTR_PRIV_KEY_CONTENT` or `SQL_SF_CONN_ATTR_PRIV_KEY_BASE64` with `SQLSetConnectAttr`, or use the `PRIV_KEY_FILE` DSN/connection-string keyword. |
| `BROWSER_RESPONSE_TIMEOUT` | `AUTHENTICATION_TIMEOUT` |
| `PUT_MAXRETRIES` / `GET_MAXRETRIES` | `PUT_GET_MAX_ATTEMPTS` (aliases still accepted, with an `01000` warning) |
| `TRACING` | Ignored. Configure `LogLevel` and `LogPath` in `sf.odbc.ini`. |
| `DisableOCSPCheck` / `OCSP_FAIL_OPEN` | Accepted but ignored, with a deprecation warning. Configure [4.x CRL options](/developer-guide/odbc/odbc-parameters#label-odbc-crl-4x) instead. |

Expand

Show lessSee more

## Behavior differences

Every behavior difference between the generally available driver and the version built on the Universal Core is catalogued in the driver source repository, as a machine-readable file listing each entry’s previous behavior, new behavior, classification, and whether it is a breaking change. Read it in full before you upgrade an application you cannot easily roll back:

- [Snowflake ODBC Driver 4.x behavior-difference catalog](https://github.com/snowflakedb/drivers/blob/main/odbc_tests/BehaviorDifferences.yaml)

The sections above summarize the entries most likely to affect an existing application. The catalog is the complete list.

The following curated list summarizes accepted breaking behavior differences between the ODBC 3.x and ODBC 4.x drivers. Entries marked `fixed` in the catalog were preview regressions and are not differences you need to prepare for when migrating from 3.x.

### ODBC API compliance

- **Fixed truncation of DECIMAL/`SQL_C_CHAR`.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `22003` when whole digits do not fit; ODBC 3.x truncated with `SQL_SUCCESS_WITH_INFO`. *(BD#11)*
- **Improved error handling for undersized `SQL_C_BINARY` buffers for DECIMAL/NUMERIC/DECFLOAT.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `22003` when the buffer is smaller than `sizeof(SQL_NUMERIC_STRUCT)`; ODBC 3.x ignored `BufferLength`. *(BD#12)*
- **Fixed conversion of `NaN` from FLOAT/DOUBLE to integer or `SQL_C_BIT`.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `22003`; ODBC 3.x wrote `0` with `SQL_SUCCESS_WITH_INFO`. *(BD#16)*
- **Improved single-field interval precision handling.** ODBC 4.x enforces the default precision of two and returns `SQL_ERROR` with SQLSTATE `22015` for values of 100 or greater; ODBC 3.x did not enforce it. *(BD#18)*
- **Improved handling of a null `RowCountPtr` during `SQLRowCount`.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `HY009`; ODBC 3.x returned `SQL_SUCCESS`. *(BD#25)*
- **Fixed handling of negative `DecimalDigits` on `SQLBindParameter`.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `HY104`; ODBC 3.x accepted negative scale silently. *(BD#26)*
- **Fixed extreme exponent conversion from DECFLOAT to `SQL_C_BINARY`.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `22003`; ODBC 3.x could succeed with a clamped value. *(BD#29)*
- **Fixed scale handling during conversion from `SQL_C_NUMERIC` to `VARCHAR`.** ODBC 4.x applies the scale from `SQL_NUMERIC_STRUCT`; ODBC 3.x ignored scale. *(BD#33)*
- **Fixed binding of subnormal doubles near `DBL_MIN`.** ODBC 4.x preserves the value; ODBC 3.x could store `0.0`. *(BD#36)*
- **Improved conversion from TIME to `SQL_C_CHAR` / `SQL_C_WCHAR`.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `22003` when the buffer is too small for the base time, and `SQL_SUCCESS_WITH_INFO` with SQLSTATE `01004` when only fractional seconds are truncated. *(BD#38)*
- **Tightened conversion from VARCHAR to `SQL_C_INTERVAL_*` types.** ODBC 4.x follows the ODBC Appendix D conversion rules more strictly. *(BD#55)*
- **Fixed `SQL_C_INTERVAL_SECOND` with fractional seconds bound to exact-numeric SQL types.** ODBC 4.x truncates the fraction and succeeds; ODBC 3.x rejected the bind with SQLSTATE `22015`. *(BD#60)*
- **Changed binding of exact-numeric C types to single-field `SQL_INTERVAL_*` parameters.** Approximate-numeric C types bound to any interval target are rejected with SQLSTATE `07006`. *(BD#72)*
- **Changed `SQL_GUID` parameter binding.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `07006` when `SQL_GUID` is used as the parameter type. Version 3.x returned `HY000`. Neither driver supports binding `SQL_GUID`. *(BD#158)*
- **Changed non-contiguous `SQLExecDirect` parameter bindings.** ODBC 4.x rejects the call locally with SQLSTATE `HY000` when bound parameters are not contiguous and do not start at 1. Version 3.x submitted the statement and returned the server SQLSTATE `42601`. *(BD#159)*
- **Changed binding of unbindable Snowflake vendor type codes.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `HYC00` from `SQLBindParameter` for `SQL_SF_ARRAY`, `SQL_SF_OBJECT`, `SQL_SF_VARIANT`, and VECTOR (`2006`), which `SQLGetTypeInfo` publishes but neither driver can bind. A vendor code that `SQLGetTypeInfo` doesn’t publish, such as `2007`, still returns `HY004`. ODBC 3.x accepted the bind and failed later during execution with `HY000`. To insert a semi-structured value, bind it as `SQL_VARCHAR` and convert it in the statement with `PARSE_JSON(?)`, `TO_ARRAY(?)`, or `TO_OBJECT(?)`. *(BD#167)*
- **Fixed data-at-execution cleanup after `SQLCancel`.** ODBC 4.x discards all accumulated `SQLPutData` so a re-entered sequence starts fresh. *(BD#86)*
- **Disallowed setting `SQL_ATTR_LOGIN_TIMEOUT` after connect.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `HY011`; ODBC 3.x returned `SQL_SUCCESS` for a no-op. *(BD#94)*
- **Tightened support of `SQL_ATTR_CURSOR_TYPE` values.** ODBC 4.x substitutes unsupported cursor types with `SQL_CURSOR_FORWARD_ONLY` and returns `SQL_SUCCESS_WITH_INFO` with SQLSTATE `01S02`. *(BD#96)*
- **Changed the diagnostic vendor prefix.** ODBC 4.x uses `[Snowflake][Snowflake ODBC Driver]`; ODBC 3.x used `[Snowflake][Support]`. *(BD#110)*
- **Fixed invalid `SQLCancelHandle(SQL_HANDLE_DBC)` during async or data-at-execution.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `HY010`; ODBC 3.x returned a no-op `SQL_SUCCESS`. *(BD#111)*
- **Changed when `SQLCancel` returns.** ODBC 4.x returns as soon as the cancel is signaled; the cancelled statement still reports `HY008`.
- **Changed `SQLSetStmtAttr(SQL_ROWSET_SIZE, 0)`.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `HY024`.
- **Implemented `SQLFreeConnect` and `SQLFreeEnv`.** ODBC 4.x exports both as wrappers around `SQLFreeHandle`.

### Catalog functions

- **Fixed `SQLColumns` / `SQLProcedureColumns` `BUFFER_LENGTH` for `NUMBER`/`DECIMAL`.** ODBC 4.x returns precision + 2; ODBC 3.x returned the Snowflake storage width. *(BD#122)*
- **Changed catalog `REMARKS` and `COLUMN_DEF`.** ODBC 4.x returns `SQL_NULL_DATA` when absent instead of an empty string. *(BD#121)*
- **Added native `INTERVAL` result types.** ODBC 4.x reports `INTERVAL YEAR TO MONTH` and `INTERVAL DAY TO SECOND` as native `SQL_INTERVAL_*` types with ANSI literals. *(BD#145)*
- **Fixed unquoted identifier case-folding in identifier mode.** When `SQL_ATTR_METADATA_ID` is `SQL_TRUE`, ODBC 4.x folds unquoted catalog, schema, table, procedure, and column identifiers to uppercase before the lookup, so a lowercase identifier matches the stored name. ODBC 3.x compared case-sensitively and returned an empty result set. Double-quoted identifiers stay case-sensitive, and the default pattern mode is case-sensitive in both versions. *(BD#87, BD#91, BD#113)*
- **Changed `SQLForeignKeys` side selection for an empty table name.** ODBC 4.x treats an empty string table name the same as an omitted one, so an empty `PKTableName` with a populated `FKTableName` resolves to `SHOW IMPORTED KEYS` and returns the relationship. ODBC 3.x returned an empty result set. *(BD#90)*

### PUT/GET behavior

- **Fixed stage array binding thresholds.** ODBC 4.x honors `arrayBindSupported` and `CLIENT_STAGE_ARRAY_BINDING_THRESHOLD`. *(BD#78)*
- **Changed PUT and GET to transfer several files in parallel**, bounded by the statement `PARALLEL` value.
- **Mapped `PUT_MAXRETRIES` and `GET_MAXRETRIES`** to a shared `PUT_GET_MAX_ATTEMPTS` count. *(BD#141)*

### Authentication and security

- **Changed private-key connection attributes.** ODBC 4.x removed support for `SQL_SF_CONN_ATTR_PRIV_KEY`. Set `SQL_SF_CONN_ATTR_PRIV_KEY_CONTENT` or `SQL_SF_CONN_ATTR_PRIV_KEY_BASE64` with `SQLSetConnectAttr`, or use the `PRIV_KEY_FILE` DSN/connection-string keyword. *(BD#10)*
- **Tightened OAuth endpoint URL scheme requirements.** ODBC 4.x requires HTTPS for token and authorization endpoints (loopback `http://` allowed). *(BD#81)*
- **Refined SQLSTATE for OAuth IdP token-exchange rejection.** ODBC 4.x returns SQLSTATE `28000`; ODBC 3.x surfaced generic `HY000`. *(BD#83)*
- **Hardened workload identity federation parameter validation.** ODBC 4.x rejects WIF-only parameters unless `authenticator` is `WORKLOAD_IDENTITY`. *(BD#108)*
- **Hardened `workload_identity_impersonation_path` with provider `OIDC`.** ODBC 4.x rejects the combination. *(BD#109)*
- **Removed OCSP support in favor of CRLs.** *(BD#124)*
- **Renamed `BROWSER_RESPONSE_TIMEOUT` to `AUTHENTICATION_TIMEOUT`.** *(BD#138)*

### Snowflake extensions and diagnostics

- **Tightened Snowflake statement attributes.** `SQL_SF_STMT_ATTR_LAST_QUERY_ID` is read-only and populated in all cases. `SQL_SF_STMT_ATTR_MULTI_STATEMENT_COUNT` keeps its `-1` default, but ODBC 4.x now validates the range and returns the value through `SQLGetStmtAttr`. *(BD#56)*
- **Changed diagnostic message text.** ODBC 4.x appends an internal error trace by default (`ErrorTraceEnabled` in `sf.odbc.ini`). *(BD#77)*
- **Fixed DECFLOAT string formatting.** ODBC 4.x returns normalized scientific notation, for example `1.2e200` instead of `12e199`. *(BD#19)*

### iODBC-specific behavior

- **Fixed success codes and diagnostics under iODBC** to match the ODBC specification. *(BD#61)*
- **Fixed orphaned statement handle release under iODBC.** *(BD#68)*
- **Fixed descriptor calls during `SQL_NEED_DATA`** to return `SQL_ERROR` with SQLSTATE `HY010`. *(BD#69)*
- **Fixed ODBC 3.x SQLSTATEs under iODBC.** *(BD#70)*
- **Fixed `SQL_C_WCHAR` fetch encoding under iODBC** to use uniform UTF-32 driven by `DriverManagerEncoding`. *(BD#79)*
- **iODBC might return different codes or SQLSTATEs** because ODBC 4.x and 3.x advertise different capabilities. *(BD#62)*

## Additional reviewed behavior differences

The following entries are reviewed and allowed in `BehaviorDifferences.yaml`. Validate applications that depend on these behaviors when migrating from 3.x.

- **`SQLColumns` `SQL_DATA_TYPE` for DATE/TIME/TIMESTAMP** returns verbose `SQL_DATETIME` (`9`) with the subtype in `SQL_DATETIME_SUB`. *(BD#125)*
- **A second `SQLFreeHandle` on an already-freed statement** returns `SQL_INVALID_HANDLE` under iODBC. *(BD#126)*
- **`SQLColumns` `TIMESTAMP` `COLUMN_SIZE`** is `20` + scale (`19` when scale is `0`), not a fixed `35`. *(BD#128)*
- **`SQLColumns` `TIMESTAMP` `BUFFER_LENGTH`** is `16`, not `35`. *(BD#129)*
- **`SQLColumns` `VARIANT`/`OBJECT`/`ARRAY` size** follows `VARCHAR_AND_BINARY_MAX_SIZE_IN_RESULT`. *(BD#130)*
- **`SQLColumns` `DATE`/`TIME` `BUFFER_LENGTH`** is `6`. *(BD#133)*
- **`CLIENT_REQUEST_MFA_TOKEN` replaced by `CLIENT_STORE_TEMPORARY_CREDENTIAL` for MFA caching.** If you previously set `CLIENT_REQUEST_MFA_TOKEN=false`, set `CLIENT_STORE_TEMPORARY_CREDENTIAL=false` to keep MFA caching disabled. *(BD#137)*
- **`SQLColumns` `GEOGRAPHY`/`GEOMETRY` sizes** follow the session VARCHAR maximum. *(BD#146)*
- **`MaxHttpRetries` maps to `retry_max_attempts`** with different default, floor, and zero semantics. *(BD#148)*
- **`MAX_CON_RETRY_ATTEMPTS` is not recognized.** *(BD#149)*
- **`RetryOn403` is not recognized**; 403 retry is opt-in via `retry_extra_status_codes`. *(BD#150)*
- **`SQLGetTypeInfo` `TIMESTAMP` `COLUMN_SIZE` is `29`**; `ODBC_USE_STANDARD_TIMESTAMP_COLUMNSIZE` is not accepted. *(BD#151)*
- **`SQLDriverConnect` fails with SQLSTATE `28000` and native error `0`** for an invalid WIF provider, missing OIDC token, or malformed JWT. *(BD#155)*

## Resolved during preview

These items were preview regressions. ODBC 4.x now matches ODBC 3.x, so they are not differences you need to prepare for when migrating from 3.x.

- PUT result compression tokens are lowercase. *(BD#2)*
- Gzip-compressed PUT uploads omit `FNAME` from the gzip header. *(BD#5)*
- `SQL_C_BINARY` fetch of `FLOAT`/`DOUBLE`/`REAL` returns the native 8-byte IEEE 754 value. *(BD#14)*
- `SQL_BIT` parameter binding from integer and `SQL_C_NUMERIC` sources accepts only `0` and `1`. *(BD#37)*
- Binding of `"Infinity"`, `"-Infinity"`, and `"NaN"` as `SQL_C_CHAR`/`SQL_C_WCHAR` to float SQL types forwards the non-finite value. *(BD#48)*
- Character hex literals bound to `SQL_BINARY` hex-decode the value. *(BD#49)*
- `SQLDescribeParam` preserves Snowflake vendor `TIMESTAMP` type codes (`2000` / `2001` / `2002`). *(BD#50)*
- `SQLBrowseConnect` under iODBC returns `SQL_NEED_DATA` for an incomplete connection string. *(BD#63)*
- OAuth Authorization Code token caching defaults `CLIENT_STORE_TEMPORARY_CREDENTIAL` to `true`. *(BD#85)*
- `SQLForeignKeys` with `SQL_ATTR_METADATA_ID=TRUE` returns `SQL_ERROR` (`HY009`) for a `NULL` catalog, schema, or table pointer. *(BD#89)*
