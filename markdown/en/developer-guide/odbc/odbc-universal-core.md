# Snowflake ODBC Driver built on the Universal Core

Preview Feature

This feature is in public preview. Inputs and behavior may change between releases.

The Snowflake ODBC Driver 4.x is built on the Universal Core. This is the next version of the driver you already use, not a new product.

The Universal Core (`sf_core`) is a shared Rust library that implements the networking, authentication, result-set fetching, and stage-transfer logic that every Snowflake driver needs. Each driver wraps that core in a thin, language-specific layer that exposes the interface its ecosystem expects; the Rust layer is not visible to application code.

Snowflake previously maintained a separate implementation of this logic in each driver, so a security fix or protocol change had to be applied separately to every one. Because the core is shared, a change to it reaches every driver built on it in that driver’s next release.

The ODBC Driver wraps that core with a thin C layer. It is not a parallel install: installing ODBC 4.x on a machine replaces the 3.x driver there. Validate it on a dedicated host, VM, or container against a non-production account.

The ODBC Driver 4.x implements the same ODBC API surface and accepts the same connection-string keywords as the 3.x driver. The existing ODBC documentation applies except where this page notes differences. See [ODBC Driver](/developer-guide/odbc/odbc), [Configuration and connection parameters](/developer-guide/odbc/odbc-parameters), and [Using the ODBC Driver](/developer-guide/odbc/odbc-using).

This version is in public preview. Validate it against a non-production account. Preview versions are not covered by the client support policy described in [Client versions & support policy](/release-notes/requirements), and the recommended and minimum supported versions listed there refer to the generally available drivers.

For the terms that apply to preview features, see [Preview features](/release-notes/preview-features).

This page covers:

- [What’s improved](#label-odbc-universal-core-improvements)
- [Ecosystem compatibility](#label-odbc-universal-core-ecosystem)
- [Installing the preview driver](#label-odbc-universal-core-install)
- [Configuration differences](#label-odbc-universal-core-config)
- [Limitations and behavior changes worth validating](#label-odbc-universal-core-limitations)
- [Migrating from the 3.x ODBC driver](#label-odbc-universal-core-migration)
- [Behavior differences](#label-odbc-universal-core-behavior-differences)
- [Known issues](#label-odbc-universal-core-known-issues)

## What’s improved

- **Improved stage transfers:** PUT and GET operations, including multipart upload, chunk-level retry, and cloud-provider-specific signing (S3, Azure Blob Storage, Google Cloud Storage), are handled by the Universal Core. GET now auto-creates missing destination directories and uses atomic `.part` file writes to avoid corrupt partial downloads.
- **Richer diagnostics:** The connection diagnostic service (controlled by `ENABLE_CONNECTION_DIAG` in the connection string) runs inside the Universal Core and produces a structured connectivity report. Troubleshooting logs can be captured without any code change by setting `SNOWFLAKE_TROUBLESHOOTING_ENABLED=true`.
- **Smaller surface for bugs:** The ODBC wrapper itself contains no protocol logic, which reduces the places where driver-specific bugs can be introduced and simplifies maintenance.
- **Open sourced code:** The driver and Universal Core source are available in the [Snowflake drivers repository](https://github.com/snowflakedb/drivers) on GitHub, so you can inspect the implementation, file issues, and contribute.

**Unified security model:** TLS, certificate revocation checking, token refresh, and OAuth flows are implemented once in the Universal Core and behave the same way across every driver built on it. A fix in any of these areas reaches all of those drivers rather than being reimplemented per language.

**Consistent cross-driver behavior:** Because networking, authentication, and stage-transfer logic live in the Universal Core, the same query, the same authentication flow, and the same error condition produce the same outcome across drivers built on it.

## Ecosystem compatibility

The following tools and frameworks are validated against the Snowflake ODBC Driver 4.x:

| Tool / framework | Status |
| --- | --- |
| Datometry | Validated |

Expand

Show lessSee more

Note

Validated minimum versions are added to this table as validation completes. Contact your Snowflake account team for the latest validation status.

## Installing the preview driver

Important

Installing ODBC 4.x replaces the 3.x driver on that machine. Install it on a dedicated host, VM, or container.

### Download

Download the installer from the [Snowflake drivers releases](https://github.com/snowflakedb/drivers/releases) page on GitHub. Preview builds of this driver are tagged `snowflake-odbc/<version>`, and the current version is `4.0.0-rc4`. Each release publishes an installer for every supported platform:

- Windows: an `.msi` for `x86_64`, `x86_32`, and `aarch64`.
- macOS: a single universal `.dmg` covering both Intel and Apple silicon.
- Linux: a `.deb`, `.rpm`, or `.tar.gz` for `x86_64` and `aarch64`.

### Windows (MSI)

Run the MSI installer for your architecture. The installer registers the driver under the name **Snowflake ODBC** in the Windows ODBC Data Source Administrator and installs files under:

Copy code

```
%ProgramFiles%\Snowflake ODBC Driver\
```

To confirm the driver is registered correctly, open the ODBC Data Source Administrator and verify that **Snowflake ODBC** appears in the **Drivers** tab.

### macOS (dmg)

Install from the universal `.dmg`. The driver is installed to:

Copy code

```
/opt/snowflake/snowflakeodbc/
```

The installer places a default `sf.odbc.ini` at that location with `DriverManagerEncoding=UTF-32`, which matches macOS’s stock iODBC. To override logging or encoding settings, create a user-level file at `~/.snowflake/sf.odbc.ini` (see [Configuration](#label-odbc-universal-core-config)).

### Linux (RPM, deb, or tar.gz)

Install using the package manager or extract the tar.gz archive. The driver library is placed at:

Copy code

```
/usr/lib64/snowflake/odbc/lib/libsfodbc.so
```

After installation, the post-install script registers the driver as **Snowflake ODBC** through `odbcinst`. To verify:

Copy code

```
odbcinst -q -d -n "Snowflake ODBC"
```

### Creating a DSN

Use your driver manager or data source name (DSN) editor to point a data source at the **Snowflake ODBC** driver. Because 4.x replaces 3.x on the machine, existing DSNs that name **SnowflakeDSIIDriver** no longer resolve there and must be repointed.

Example `odbc.ini` entry on Linux:

Copy code

```
[my_snowflake]
Driver    = Snowflake ODBC
SERVER    = myaccount.snowflakecomputing.com
UID       = myuser
```

### Confirming the driver version

After connecting, call `SQLGetInfo(SQL_DRIVER_VER)` to confirm you are on 4.x. The version string uses the zero-padded `MM.mm.bbbb` format, for example `04.00.0000`. You can also call `SQLGetInfo(SQL_DRIVER_NAME)` to verify the installed driver file path.

## Configuration differences

Most connection parameters and DSN keywords are shared with the 3.x ODBC driver. The items below are specific to or behave differently in ODBC 4.x.

### sf.odbc.ini (new; replaces simba.snowflake.ini)

Process-wide logging for ODBC 4.x is configured in `sf.odbc.ini`, not `simba.snowflake.ini`. The driver searches the following locations and uses the first existing file:

1. `$SF_ODBC_INI` (explicit override)
2. `~/.config/snowflake/sf.odbc.ini` (Linux) / `~/Library/Application Support/snowflake/sf.odbc.ini` (macOS)
3. `~/.snowflake/sf.odbc.ini`
4. `/opt/snowflake/snowflakeodbc/sf.odbc.ini` (macOS only, installer default)

On Unix the file must be `chmod 600`; the driver logs a warning and falls back to defaults if permissions are looser.

On Windows, the ODBC setup dialog no longer exposes a per-DSN `Tracing(0-6)` field. Configure logging only through `sf.odbc.ini` or the troubleshooting environment variables below. Legacy `TRACING` values in a DSN or connection string are ignored. *(BD#144)*

Recognized keys (all case-insensitive):

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `LogEnabled` | bool | `true` | Master switch for the driver log file. |
| `LogLevel` | enum | `INFO` | `OFF`, `ERROR`, `WARN`, `INFO`, `DEBUG`, `TRACE`. |
| `LogPath` | path | None | Directory for the rolling log file. |
| `LogFile` | string | `snowflake_odbc.log` | Log file name. |
| `LogRotation` | enum | `NEVER` | `NEVER`, `DAILY`, `HOURLY`, `MINUTELY`. |
| `LogMaxCount` | integer | None | Number of rotated files to retain. |
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

Drivers built on the Universal Core do not support OCSP-based certificate revocation checking. Starting with the public preview versions, revocation checking is available only through CRLs (certificate revocation lists), and it is off by default.

This aligns with the broader move away from OCSP, which has been a frequent cause of production outages and offers little real security in its default fail-open mode.

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

ODBC 4.x supports `connections.toml` profiles for setting connection parameters outside the DSN or connection string. The file lives at `~/.snowflake/connections.toml` (overridable with `$SNOWFLAKE_HOME`).

## Limitations and behavior changes worth validating

Snowflake ODBC 4.x is a breaking change release. To verify the compatibility, review [Behavior differences](#label-odbc-universal-core-behavior-differences), for the curated summary of behavior differences that are most likely to affect existing applications.

## Migrating from the 3.x ODBC driver

Most applications require no code changes to run against ODBC 4.x. Use the steps below to validate your application against a non-production account. When 4.x reaches general availability, the same validation covers your production cutover.

### Step 1: Install on a test host and point a DSN at it

Install ODBC 4.x driver (see [Installing the preview driver](#label-odbc-universal-core-install)). Create a new DSN entry pointing to **Snowflake ODBC** with the same account, role, warehouse, and credentials as your existing DSN.

### Step 2: Run your test suite against the new DSN

Point your application or test suite at the new DSN against a non-production account. Watch for the items listed in [Behavior differences](#label-odbc-universal-core-behavior-differences), especially:

- Key pair authentication using a raw `EVP_PKEY*` pointer: migrate to `PRIV_KEY_CONTENT` or `PRIV_KEY_BASE64`.
- Vendor prefix from `SQLGetDiagRec` messages.
- OAuth flows using `http://` token or authorization endpoints: switch to `https://`.

### Step 3: Switch error handling for diagnostic messages

If your application catches specific vendor strings or error-trace content from `SQLGetDiagRec`, update it to handle the new `[Snowflake][Snowflake ODBC Driver]` prefix and the appended internal trace, or set `ErrorTraceEnabled=false` in `sf.odbc.ini` to suppress the trace.

## Behavior differences

Every behavior difference between the generally available driver and the version built on the Universal Core is catalogued in the driver source repository, as a machine-readable file listing each entry’s previous behavior, new behavior, classification, and whether it is a breaking change. Read it in full before you upgrade an application you cannot easily roll back:

- [Snowflake ODBC Driver 4.x behavior-difference catalog](https://github.com/snowflakedb/drivers/blob/main/odbc_tests/BehaviorDifferences.yaml)

The sections above summarize the entries most likely to affect an existing application. The catalog is the complete list.

The following curated list summarizes breaking behavior differences between the ODBC 3.x and ODBC 4.x drivers.

### ODBC API compliance

- **Fixed truncation of DECIMAL/`SQL_C_CHAR`.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `22003` (numeric value out of range) when whole digits do not fit; ODBC 3.x truncated with `SQL_SUCCESS_WITH_INFO`. *(BD#11)*
- **Improved error handling for undersized `SQL_C_BINARY` buffers for DECIMAL/NUMERIC/DECFLOAT.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `22003` (numeric value out of range) when the buffer is smaller than `sizeof(SQL_NUMERIC_STRUCT)`; ODBC 3.x ignored `BufferLength` that could cause buffer overflow. *(BD#12)*
- **Fixed conversion of ‘NaN’ from FLOAT/DOUBLE to integer or `SQL_C_BIT`.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `22003` (numeric value out of range); ODBC 3.x wrote `0` with `SQL_SUCCESS_WITH_INFO` which could produce data inconsistency. *(BD#16)*
- **Improved single-field precision handling, by respecting the default setting and explicit user override.** ODBC 4.x enforces the default precision of two and returns `SQL_ERROR` with SQLSTATE `22015` (interval field overflow) for values of 100 or greater; ODBC 3.x did not enforce it and did not respect the SQL\_DESC\_DATETIME\_INTERVAL\_PRECISION parameter. *(BD#18)*
- **Improved handling of null `RowCountPtr` during `SQLRowCount` call.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `HY009` (invalid use of null pointer); ODBC 3.x returned `SQL_SUCCESS`. A null out-pointer is not a meaningful call. *(BD#25)*
- **Fixed handling of negative `DecimalDigits` on `SQLBindParameter`.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `HY104` (invalid precision or scale value); ODBC 3.x accepted negative scale silently. Negative scale is invalid. *(BD#26)*
- **Fixed extreme exponent conversion from DECFLOAT to `SQL_C_BINARY`.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `22003` (numeric value out of range); ODBC 3.x could succeed with a clamped value. Prevents data loss for extreme exponents. *(BD#29)*
- **Fixed scale handling during the conversion from `SQL_C_NUMERIC` to `VARCHAR`.** ODBC 4.x applies the scale from `SQL_NUMERIC_STRUCT`, for example magnitude `12345` with scale `2` becomes `"123.45"`; ODBC 3.x ignored scale. New driver now honors the explicitly set scale by the user. *(BD#33)*
- **Fixed binding of subnormal doubles near `DBL_MIN`.** ODBC 4.x preserves the value; ODBC 3.x could store `0.0`. Prevents data loss for very small floating-point values. *(BD#36)*
- **Improved conversion from TIME `SQL_C_CHAR` / `SQL_C_WCHAR`.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `22003` (numeric value out of range) when the buffer is too small for the base time (HH:MM:SS), and `SQL_SUCCESS_WITH_INFO` with SQLSTATE `01004` (string data, right truncated) when only fractional seconds are truncated; ODBC 3.x returned error when buffer was undersized to hold the full time. *(BD#38)*
- **Fixed conversion from DATE to `SQL_C_BINARY` with an undersized buffer.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `22003` (numeric value out of range); ODBC 3.x could return `SQL_SUCCESS` with truncated data. Prevents data inconsistency. *(BD#44)*
- **Fixed the export of `SQLGetFunctions` for `SQL_API_SQLCANCELHANDLE`.** ODBC 4.x reports the function as supported; ODBC 3.x reported `SQL_FALSE` even though the export worked at runtime. *(BD#45, to be verified)*
- **Tightened conversion from VARCHAR to `SQL_C_INTERVAL_*` types.** ODBC 4.x follows the ODBC [Appendix D data-type conversion rules](https://learn.microsoft.com/en-us/sql/odbc/reference/appendixes/appendix-d-data-types) more strictly, including `SQL_SUCCESS_WITH_INFO` with SQLSTATE `01S07` truncation and `SQL_ERROR` with SQLSTATE `22015` (interval field overflow); ODBC 3.x was inconsistent. *(BD#55, to be verified)*
- **Fixed `SQL_C_INTERVAL_SECOND` with fractional seconds bindings to exact-numeric SQL types.** ODBC 4.x truncates the fraction and succeeds with `SQL_SUCCESS`; ODBC 3.x rejected the bind with `SQL_ERROR` with SQLSTATE `22015` (interval field overflow). *(BD#60)*
- **Changed binding of exact-numeric C types to single-field `SQL_INTERVAL_*` parameters.** ODBC 4.x follows ODBC [Appendix D data-type conversion rules](https://learn.microsoft.com/en-us/sql/odbc/reference/appendixes/appendix-d-data-types); approximate-numeric C types bound to any interval target are rejected with `SQL_ERROR` with SQLSTATE `07006` (restricted data type attribute violation). Aligns the API with the ODBC spec. *(BD#72)*
- **Fixed data-at-execution cleanup after `SQLCancel` call.** ODBC 4.x discards all accumulated `SQLPutData` so a re-entered sequence starts fresh; ODBC 3.x could concatenate previously accumulated chunks with new data leading to data inconsistency. *(BD#86)*
- **Disallowed setting `SQL_ATTR_LOGIN_TIMEOUT` after connect.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `HY011` (attribute cannot be set now); ODBC 3.x returned `SQL_SUCCESS` for a no-op. Avoids silently accepting a value that has no effect. *(BD#94)*
- **Tightened support of `SQL_ATTR_CURSOR_TYPE` values.** ODBC 4.x substitutes any unsupported cursor types with `SQL_CURSOR_FORWARD_ONLY` and returns `SQL_SUCCESS_WITH_INFO` with SQLSTATE `01S02` (option value changed); ODBC 3.x accepted non-forward-only types silently. Snowflake supports only forward-only cursors. *(BD#96)*
- **Changed the diagnostic vendor prefix.** ODBC 4.x uses `[Snowflake][Snowflake ODBC Driver]`; ODBC 3.x used `[Snowflake][Support]`. Matches the ODBC requirement for `[vendor][ODBC-component-identifier]`. *(BD#110)*
- **Fixed handling of invalid `SQLCancelHandle(SQL_HANDLE_DBC)` call during async or data-at-execution.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `HY010` (function sequence error); ODBC 3.x returned a no-op `SQL_SUCCESS`. *(BD#111)*
- **Changed when `SQLCancel` returns.** ODBC 4.x cancels through the core operation handle and `SQLCancel` returns as soon as the cancel is signaled; the cancelled statement still reports `HY008` and does not return until the abort has been issued. ODBC 3.x issued a separate server-side cancel call.
- **Changed `SQLSetStmtAttr(SQL_ROWSET_SIZE, 0)`.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `HY024`; when the Driver Manager forwards the value (iODBC and Windows), ODBC 3.x returned `SQL_SUCCESS` and stored `0`. unixODBC already rejects `0` before the driver is called. *(BD#102)*
- **Implemented `SQLFreeConnect` and `SQLFreeEnv`.** ODBC 4.x exports both as wrappers around `SQLFreeHandle` so direct-link and ODBC 2.x applications that bypass the Driver Manager can free connections and environments. Under iODBC, `SQLGetFunctions` reports both as supported; ODBC 3.x omitted them from the ODBC 3 bitmap. *(BD#127)*

### Catalog functions

- **Fixed `SQLColumns` / `SQLProcedureColumns` `BUFFER_LENGTH` for `NUMBER`/`DECIMAL`.** ODBC 4.x returns precision + 2 (ODBC transfer octet length); ODBC 3.x returned the Snowflake storage width from the precision ladder (for example `16` for `NUMBER(38,0)`). Query-result `SQLColAttribute` octet/display size for `NUMBER` remains 136. *(BD#122)*
- **Fixed `SQLColumns` `COLUMN_SIZE` and `BUFFER_LENGTH` for `VARIANT`/`OBJECT`/`ARRAY`.** ODBC 4.x follows `VARCHAR_AND_BINARY_MAX_SIZE_IN_RESULT`; ODBC 3.x hardcoded 128 MB from `SHOW COLUMNS`. *(BD#130)*
- **Fixed `SQLColumns` `COLUMN_SIZE`, `BUFFER_LENGTH`, and `CHAR_OCTET_LENGTH` for `GEOGRAPHY`/`GEOMETRY`.** ODBC 4.x reports all three as `VARCHAR_AND_BINARY_MAX_SIZE_IN_RESULT` (default `16777216`), so raising the session parameter raises all three; ODBC 3.x reported `134217728` independent of the session setting. Both drivers report `SQL_VARCHAR` as `DATA_TYPE`. *(BD#146)*
- **Fixed `SQLProcedureColumns` `TYPE_NAME` for unsupported types such as `GEOGRAPHY`/`GEOMETRY`.** ODBC 4.x reports the Snowflake type name while `DATA_TYPE` remains `SQL_VARCHAR`.
- **Fixed `SQLProcedureColumns` `CHAR_OCTET_LENGTH` for unsupported types such as `GEOGRAPHY`/`GEOMETRY`.** ODBC 4.x reports a byte length instead of `NULL`, matching the `SQL_VARCHAR` they report as `DATA_TYPE`.
- **Fixed `SQLGetTypeInfo` string result columns (`TYPE_NAME`, `LITERAL_PREFIX`/`SUFFIX`, `CREATE_PARAMS`, `LOCAL_TYPE_NAME`).** ODBC 4.x reports `SQL_WVARCHAR` as the IRD concise type, matching `SQLTables`/`SQLColumns`.
- **Fixed `SQLGetTypeInfo` `INTERVAL_PRECISION`.** ODBC 4.x reports `SQL_SMALLINT` as the IRD concise type, matching the ODBC spec; `NUM_PREC_RADIX` remains `SQL_INTEGER`.
- **Fixed `SQLColumns` `BUFFER_LENGTH` for `DATE`/`TIME`.** ODBC 4.x returns `6` (`sizeof(SQL_DATE_STRUCT)` / `sizeof(SQL_TIME_STRUCT)`); ODBC 3.x copied `COLUMN_SIZE` (`10` / `18` for `TIME(9)`). Query-result `SQLColAttribute` octet length for `DATE`/`TIME` remains `6`. *(BD#133)*

### Data type conversion and binding

- **Added `INTERVAL YEAR TO MONTH` and `INTERVAL DAY TO SECOND` result fetch support.** ODBC 4.x returns the canonical ANSI literal for `SQL_C_CHAR`/`SQL_C_WCHAR`, same-family `SQL_C_INTERVAL_*` targets receive the parsed interval struct, and scalar numeric targets receive total months or total whole seconds (reporting `01S07` when sub-second precision is dropped). *(BD#145)*
- **Fixed `FLOAT`/`DOUBLE`/`REAL` fetch as `SQL_C_BINARY`.** ODBC 4.x returns the native 8-byte IEEE 754 value; ODBC 3.x returned the raw 8-byte double. *(BD#14)*
- **Fixed `SQL_BIT` parameter binding from integer and `SQL_C_NUMERIC` sources.** ODBC 4.x accepts only `0` and `1`; ODBC 3.x rejected other magnitudes with `22003`. *(BD#37)*
- **Fixed binding of `"Infinity"`, `"-Infinity"`, and `"NaN"` as `SQL_C_CHAR`/`SQL_C_WCHAR` to `SQL_FLOAT`/`SQL_REAL`/`SQL_DOUBLE`.** ODBC 4.x forwards the non-finite value; ODBC 3.x returned `22018`. *(BD#48)*
- **Fixed DECFLOAT string formatting.** ODBC 4.x returns normalized scientific notation, for example `1.2e200` instead of `12e199`. *(BD#19)*

### PUT/GET behavior

- **Fixed stage array binding thresholds and user-defined array bind support.** ODBC 4.x honors `arrayBindSupported`. `CLIENT_STAGE_ARRAY_BINDING_THRESHOLD` is aligned across the driver suite; ODBC 3.x ignored server-provided value of `arrayBindSupported`. *(BD#78)*
- **Changed PUT and GET retry limits.** ODBC 4.x uses one shared `PUT_GET_MAX_ATTEMPTS` budget (default 6 total attempts) for both operations; ODBC 3.x honors independent `PUT_MAXRETRIES` and `GET_MAXRETRIES` values in `[0, 100]` and silently resets out-of-range values to 5. ODBC 4.x still accepts the 3.x spellings as aliases and posts `01000` on connect. *(BD#141)*
- **Changed PUT and GET to transfer several files in parallel**, bounded by the statement `PARALLEL` value; result rows keep their original file order.
- **Improved GET to warn** when a downloaded batch contains multiple files that resolve to the same local filename. *(BD#135)*

### Authentication and security

- **Changed private-key connection attributes.** ODBC 4.x removed support for `SQL_SF_CONN_ATTR_PRIV_KEY` (raw `EVP_PKEY*`); use `PRIV_KEY_CONTENT`, `PRIV_KEY_BASE64`, or `PRIV_KEY_FILE`. Raw OpenSSL structs cannot safely cross the Rust ODBC boundary. *(BD#10)*
- **Changed client-local rejection of invalid non-credential connection parameters.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `HY000`; ODBC 3.x returned `28000` (native error `20032`) for cases such as an invalid `PORT` or an unparseable connection string. *(BD#1)*
- **Changed native error codes on client-local authentication failures.** ODBC 4.x returns SQLSTATE `28000` with native error `0` for a missing authentication parameter; ODBC 3.x returns `28000` with native error `20032`. The message text also differs. *(BD#1)*
- **Added native AKS Workload Identity support for Azure.** When the Azure Workload Identity webhook injects `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and `AZURE_FEDERATED_TOKEN_FILE` into a pod and the projected token file exists on disk, `WORKLOAD_IDENTITY_PROVIDER=AZURE` exchanges that federated token for an Entra ID access token directly. `WORKLOAD_IDENTITY_IMPERSONATION_PATH` is not supported in this environment.
- **Added the `WORKLOAD_IDENTITY_AWS_USE_OUTBOUND_TOKEN` connection parameter** for AWS Workload Identity Federation. When set to `true`, attestation uses outbound STS `GetWebIdentityToken` instead of the default pre-signed `GetCallerIdentity` token; the connection parameter takes precedence over `SNOWFLAKE_ENABLE_AWS_WIF_OUTBOUND_TOKEN`.
- **Tightened OAuth endpoint URL scheme requirements.** ODBC 4.x requires HTTPS for token and authorization endpoints (loopback `http://` allowed); ODBC 3.x accepted plaintext endpoints. Security hardening aligned with OAuth requirements. *(BD#81)*
- **Refined SQLSTATE for OAuth IdP token-exchange rejection.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `28000` (invalid authorization specification); ODBC 3.x surfaced generic `HY000` (general error). Classifies IdP credential rejection as an authentication failure. *(BD#83)*
- **Hardened workload identity federation (WIF) parameter validation.** ODBC 4.x rejects WIF-only parameters unless `authenticator` is set in `WORKLOAD_IDENTITY`; ODBC 3.x silently ignored them with another authenticator. Hardened validation. *(BD#108)*
- **Hardened `workload_identity_impersonation_path` with provider `OIDC`.** ODBC 4.x rejects the combination; ODBC 3.x silently ignored it. The path is unused for OIDC attestation, so silent ignore was misleading. *(BD#109)*
- **Removed OCSP support in favor of CRLs.** ODBC 4.x does not provide OCSP certificate verification method in favor of CRL verification; ODBC 3.x provided both: OCSP and CRL verification depending on the settings. *(BD#124)*

### Snowflake extensions and diagnostics

- **Extended Snowflake statement attributes: `SQL_SF_STMT_ATTR_LAST_QUERY_ID`, `SQL_SF_STMT_ATTR_MULTI_STATEMENT_COUNT`.** ODBC 4.x: `SQL_SF_STMT_ATTR_LAST_QUERY_ID` is read-only and properly populated in all cases; `SQL_SF_STMT_ATTR_MULTI_STATEMENT_COUNT` defaults to `-1` (auto-detect) and supports get/set. ODBC 3.x: `SQL_SF_STMT_ATTR_LAST_QUERY_ID` is not populated in all use cases. Set on `SQL_SF_STMT_ATTR_LAST_QUERY_ID` succeeds with a no-op. `SQL_SF_STMT_ATTR_MULTI_STATEMENT_COUNT` is not implemented. Extends multi-statement control and tightens query-ID behavior. *(BD#56)*
- **Changed diagnostic message text.** ODBC 4.x appends an internal error trace by default (`ErrorTraceEnabled` in `sf.odbc.ini`, default `true`); ODBC 3.x returned message text only. Improves error visibility; can be disabled. *(BD#77)*
- **Changed failed-login diagnostic message framing.** ODBC 4.x leads with `Failed to login: Login error: <server text>, code: <code>` and may append an error trace; ODBC 3.x returned the server sentence alone on the first line. SQLSTATE and native error code are unchanged. *(BD#140)*
- **Added `INCLUDE_RETRY_REASON` (default `true`)** so retried query requests send `retryReason` (the HTTP status that triggered the retry, or `0` for transport failures) alongside `retryCount`.

### iODBC-specific behavior

- **Fixed success codes and diagnostics under iODBC.** ODBC 4.x matches the ODBC spec, for example `SQL_NO_DATA` for zero-row DML, `SQL_SUCCESS` for length-only queries, and required diagnostics on `SUCCESS_WITH_INFO`; ODBC 3.x took iODBC-only shortcuts. Spec compliance. *(BD#61)*
- **Fixed orphaned statement handle release under iODBC.** ODBC 4.x returns `SQL_INVALID_HANDLE` after `SQLDisconnect` or `SQLFreeStmt(SQL_DROP)`; ODBC 3.x could return `SQL_SUCCESS` and leave the handle in the driver manager’s alloc table. Prevents handle leaks. *(BD#68)*
- **Fixed error handling when calling descriptors (`SQLGetDescField`, `SQLSetDescField`) during `SQL_NEED_DATA` state.** ODBC 4.x returns `SQL_ERROR` with SQLSTATE `HY010` (function sequence error); ODBC 3.x returns `SQL_SUCCESS`. *(BD#69)*
- **Fixed ODBC 3.x SQLSTATEs under iODBC.** ODBC 4.x returns states such as `HY090`, `HY010`, `HY017`, `HY092`, `07009`, and `HY008`; ODBC 3.x often exposed vendor `HY000` or ODBC 2.x aliases. Driver-side pre-validation yields a single spec-correct diagnostic. *(BD#70)*
- **Fixed `SQL_C_WCHAR` fetch encoding under iODBC.** ODBC 4.x uses uniform UTF-32 driven by `DriverManagerEncoding` in `sf.odbc.ini` (indicator is always character count × 4); ODBC 3.x varied code-unit width by Snowflake source column type. *(BD#79)*

### Resolved during preview

These items were preview regressions. ODBC 4.x now matches ODBC 3.x, so they are not differences you need to prepare for when migrating from 3.x.

- **PUT result compression tokens.** Both drivers return lowercase tokens such as `gzip`. *(BD#2)*
- **Gzip-compressed PUT uploads.** When `AUTO_COMPRESS=TRUE`, both drivers omit `FNAME` from the gzip header and zero gzip `mtime`, so identical content produces the same bytes. *(BD#5)*
- **Character hex literals bound to `SQL_BINARY`.** Both drivers hex-decode the value, for example `"DEADBEEF"` becomes 4 bytes, drop a leftover nibble on an odd-length string, and return `22018` for non-hex input. *(BD#49)*
- **`SQLDescribeParam` for Snowflake vendor `TIMESTAMP` type codes (`2000` / `2001` / `2002`).** Both drivers return those codes as bound. *(BD#50)*
- **OAuth Authorization Code token caching.** Both drivers default `CLIENT_STORE_TEMPORARY_CREDENTIAL` to `true` when the caller has not set it. *(BD#85)*
- **Unreadable or empty `TOKEN_FILE_PATH`.** Both drivers report SQLSTATE `28000`.
- **`SQLBrowseConnect` under iODBC.** Both drivers return `SQL_NEED_DATA` for an incomplete connection string and keep the handle available for further browse calls. *(BD#63)*
- **`SQLForeignKeys` with `SQL_ATTR_METADATA_ID=TRUE`.** Both drivers return `SQL_ERROR` with SQLSTATE `HY009` for a `NULL` catalog, schema, or table pointer on either side. *(BD#89)*
- **NULL `CatalogName` substitution on catalog functions.** Both drivers leave `CatalogName` unconstrained when it is NULL unless `UseCurrentCatalog=true` or `CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX` is enabled. *(BD#88)*
- **Unrecognized connection-string keywords.** Both drivers post a local `01S00` warning when `SQLDriverConnect` sees an unknown keyword and still open the connection. *(BD#106)*

## Known issues

The following list describes the known issues that are subject to change.

- **iODBC driver-manager might return different codes or SQLSTATEs as capability advertisement for the drivers differ.** ODBC 4.x and 3.x advertise different capabilities, so iODBC might return different codes or SQLSTATEs for identical calls, for example DSN-name lookup, catalog/privilege calls, or out-of-range `SQLGetFunctions`. *(BD#62)*
