# Node.js Driver release notes for 2026

This article contains the release notes for the Node.js Driver, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Snowflake uses semantic versioning for Node.js Driver updates.

See [Node.js Driver](/developer-guide/node-js/nodejs-driver) for documentation.

## Version 4.0.0-beta.0 (November 12, 2026)

Initial public preview release of the Node.js Driver built on the [Universal Core](/developer-guide/universal-core/universal-core). This is a new major version line, published under the existing `snowflake-sdk` package name with the npm `beta` tag. The npm `latest` tag still points to version 3.x, so install this version explicitly with `npm install snowflake-sdk@beta`. Version 3.x remains the version recommended for production.

### New architecture and installation

Version 4 is a full rewrite. Most of the driver is now written in Rust and compiled into a native `.node` addon, which makes the driver much faster, uses less disk space, and reduces the driver’s other npm dependencies to two. The driver and Universal Core source are published in the [Snowflake drivers repository](https://github.com/snowflakedb/drivers) on GitHub.

The public API is the same, except for the breaking changes listed in this release note. Because this is a new codebase, expect some small differences in behavior, including different error messages and codes. If your code checks error text, test it before you upgrade.

npm installs the prebuilt addon for your platform as the optional dependency `@snowflake/sdk-core-<platform>`. Prebuilt addons are available for the following platforms:

- macOS: arm64 and x64
- Linux: arm64 and x64 (glibc and musl)
- Windows: arm64, x64, and x86

You might need to adjust your setup in the following cases:

- If you install with `--omit=optional`, the addon isn’t installed.
- If you run `npm install` on one platform and deploy to another, for example, from macOS to a Linux container or AWS Lambda, run `npm install` on the target platform instead.
- If you bundle your app with webpack, esbuild, or a similar tool, mark `snowflake-sdk` as external.
- If you use a platform that isn’t listed, you must build the addon from source with Rust.

### Known issues

The following areas are still in progress, so their behavior might change in later beta releases before the 4.x general availability release:

- FIPS mode is still in progress. The native library can be built for FIPS, but the published prebuilt addons aren’t FIPS builds, so `snowflake.getFipsStatus()` returns `{ isFips: false }` for them. The way to set up FIPS mode in 4.x isn’t decided yet. Node.js FIPS settings, such as the `--enable-fips` and `--force-fips` flags or `crypto.setFips()`, have no effect on the driver, because the driver performs cryptography in its native library instead of the built-in `crypto` module.
- Errors are still a work in progress. Error classes, `code` values, and messages might change, and some errors don’t have a `code` yet. Avoid relying on the exact error text.
- TypeScript types and their JSDoc aren’t final. Some methods and options have short or missing descriptions, and some types might still change.
- Some behavior still differs from 3.x and is being reviewed, mainly in the following areas:
  - Query cancellation and long-running queries
  - Reading large results
  - Timeouts and retries
  - External browser, Okta, OAuth, and workload identity authentication
  - Proxy settings
  - Token caching and custom credential managers
- Performance is still being tuned. The driver is already faster than 3.x in most cases, and more improvements are planned.
- Some features have gaps in test coverage. These gaps are being reviewed, and tests are being added in upcoming beta releases.

### Breaking changes

Note

This list of breaking changes isn’t final. Entries might be added or removed based on feedback from the beta.

#### General changes

- Changed the minimum supported Node.js version from 20 to 22, because Node.js 20 has reached end of life. Upgrade to Node.js 22 or later before you update the driver.
- Changed queries to fail when a `VARIANT`, `OBJECT`, `ARRAY`, or `MAP` value contains `NaN`, `Infinity`, or `undefined`, which aren’t valid JSON. Snowflake returns these values by default, when the [STRICT\_JSON\_OUTPUT](/sql-reference/parameters#label-strict-json-output) parameter is `FALSE`. For example, `OBJECT_CONSTRUCT('a', 'NaN'::FLOAT)` returns `{"a": NaN}`, and `ARRAY_CONSTRUCT(1, NULL, 2)` returns `[1, undefined, 2]`. The driver now parses these values only with `JSON.parse()`. Previously, it evaluated values that weren’t valid JSON as JavaScript code. This evaluation was removed as a safety precaution and because `JSON.parse()` is much faster. To read such values, do one of the following:
  - Set `STRICT_JSON_OUTPUT` to `TRUE`. Snowflake then returns `null` instead of `undefined`, and the strings `"NaN"` and `"Infinity"`.
  - Pass your own `jsonColumnVariantParser` to `snowflake.configure()`.
- Changed the driver to no longer honor most Node.js runtime flags, environment variables, and global settings of the Node.js `tls`, `https`, `dns`, and `crypto` modules, because the driver doesn’t use these modules. For example, flags such as `--use-openssl-ca`, `--openssl-config`, `--tls-min-v1.3`, `--tls-cipher-list`, and `--dns-result-order`, and code such as `tls.DEFAULT_MIN_VERSION = 'TLSv1.3'` or `dns.setDefaultResultOrder('ipv4first')`, have no effect on the driver. Only two Node.js environment variables still work:
  - `NODE_TLS_REJECT_UNAUTHORIZED=0` turns off TLS certificate checks.
  - `NODE_EXTRA_CA_CERTS` adds the certificates from the specified file to the list of trusted certificates.

#### Removed APIs and options

- Removed OCSP checks. Snowflake drivers now check for revoked certificates with certificate revocation lists (CRLs), because OCSP often caused connection failures and many certificate authorities are dropping OCSP support. CRL checks are off by default, matching the OCSP default since version 3.4.0. To turn them on, set the [`certRevocationCheckMode`](/developer-guide/node-js/nodejs-driver-options#label-nodejs-crl-validation-options) connection option to `ENABLED` (replaces OCSP fail-closed mode) or `ADVISORY` (replaces OCSP fail-open mode). The following APIs were removed:
  - The `disableOCSPChecks` and `ocspFailOpen` options of `snowflake.configure()`.
  - The `useConnectionConfigProxyForOCSP` connection option.
  - The `connection.setupOcspPrivateLink()` method.
  - The `snowflake.ocspModes` export and the `OcspModes` type.
- Removed the undocumented `toStringSf()` and `getFormat()` methods from the `Buffer` returned for `BINARY` columns, which is now a plain `Buffer`. To get the value as text, use `buffer.toString('hex').toUpperCase()` or `buffer.toString('base64')`.
- Removed the undocumented `BR` value of `SOURCE_COMPRESSION` in `PUT`. To upload Brotli-compressed files, use the documented `BROTLI` value instead.
- Removed the following connection options:
  - `clientRequestMFAToken`. MFA token caching is now controlled by `clientStoreTemporaryCredential`.
  - `disableConsoleLogin`. This option isn’t needed because Snowflake already chooses the right login page. External browser authentication always opens the URL that Snowflake returns, as it did with the default value `true`. If the account has the `ENABLE_IDENTIFIER_FIRST_LOGIN` parameter turned on, Snowflake returns its login page, where the user selects one of the account’s identity providers. Otherwise, the account can have only one identity provider, and the browser goes directly to it.
  - `region`, which was deprecated. Set `host` to the full host name of your account, or set `accessUrl`, instead.
  - `clientConfigFile`, and the easy logging feature that it configured. The driver no longer reads `sf_client_config.json`, whether its path comes from this option or the `SF_CLIENT_CONFIG_FILE` environment variable, or the file is in the driver or home directory. If you used this file, the driver no longer writes those logs. To set the log level and log file, use the `logLevel` and `logFilePath` options of `snowflake.configure()`.
  - `oauthHttpAllowed`, which was deprecated and intended only for tests. `oauthTokenRequestUrl` must still use `https://`, but `http://` is now accepted without any option when the host is `localhost`, `127.0.0.1`, or `::1`, for example, for a local mock server.
  - `serviceName`. The service name is an internal session value that applications shouldn’t set.
  - `includeRetryReason`. Retried requests always include the HTTP status code that caused the retry, as they did by default, because Snowflake uses this status code to find out why requests are retried.
  - `validateDefaultParameters`. TypeScript already reports a misspelled option name at compile time, and the driver now always logs a warning for an unknown option and ignores it.
  - `forceStageBindError`. This option made array binds fail on purpose and was intended only for the driver’s own tests.
  - `gcsUseDownscopedCredential`. Snowflake already uses downscoped credentials for `PUT` and `GET` on Google Cloud Storage by default, so this option had no effect.
- Removed the experimental `enableExperimentalMultipartUploads` option of `snowflake.configure()`. `PUT` and `GET` now always transfer large files in parts on Amazon S3 and Azure stages. For details, see the multipart transfer entry under New features and updates.
- Removed the following methods:
  - `connection.getServiceName()`. The service name is an internal session value that applications shouldn’t depend on.
  - `statement.getStatementId()`, which was deprecated. This method returned the same query ID as `statement.getQueryId()`, so call `getQueryId()` instead.
  - `statement.fetchRows()`, which was deprecated. Use `statement.streamRows()` instead, which returns the same rows as a `Readable` stream. Read the stream with `for await (const row of statement.streamRows())`, or replace the `each` callback with the `'data'` event and the `end` callback with the `'end'` and `'error'` events.
- Removed the following types and type members:
  - The `FileAndStageBindStatement` type. Its `hasNext()` and `NextResult()` methods moved to `RowStatement`, which every query returns. These methods step through the results of a multi-statement query and aren’t related to files or stages, so declaring them only on `FileAndStageBindStatement` was a mistake in the types. For a single statement, `hasNext()` returns `false`. If your code uses `FileAndStageBindStatement`, replace it with `RowStatement`.
  - The options that apply only to `connection.execute()` from `connection.fetchResult()` and `connection.getResultsFromQueryId()`. Their options were typed as `{ queryId: string } & Partial<StatementOption>`, but most of these options, such as `binds`, `parameters`, `requestId`, and `asyncExec`, had no effect. They’re now typed as the new `FetchResultOptions` type, with only `queryId`, `complete`, `streamResult`, `rowMode`, and `fetchAsString`. If your TypeScript code passes other options, remove them. The `sqlText` option was also removed. If you need the SQL text, keep it in your own code.
  - The `excludeGuid` and `queryId` fields of the `StatementOption` type. `connection.execute()` never used them, so setting them had no effect. If your TypeScript code sets them, remove them. To get the result of an earlier query by its ID, use `connection.getResultsFromQueryId({ queryId })`.
- Removed the following undocumented APIs, which were never intended to be public and weren’t part of the TypeScript types:
  - The `snowflake.STRING`, `snowflake.BOOLEAN`, `snowflake.NUMBER`, `snowflake.DATE`, `snowflake.OBJECT`, `snowflake.ARRAY`, `snowflake.MAP`, and `snowflake.JSON` constants. No public API used them.
  - The `connection.isTokenValid()` method.
  - The `connection.heartbeat()` and `connection.heartbeatAsync()` methods. To check that a connection still works, use `await connection.isValidAsync()`, which sends the same heartbeat request. To keep a session alive, set the `clientSessionKeepAlive` connection option.
  - The `getFileMetadata()` method on the statement returned for a `PUT` or `GET` command. This method returned the raw response that Snowflake sent for the command. To see what happened to each file, read the result rows, for example, in the `complete` callback.
  - The `getCurrentDatabaseProvider()` method on the object returned by `statement.getSessionState()`. This method always returned `null`.
  - The `sessionToken`, `masterToken`, `sessionTokenExpirationTime`, and `masterTokenExpirationTime` options of `snowflake.createConnection()`. These options weren’t part of `ConnectionOptions`. To reuse a session, use `connection.serialize()` and `snowflake.deserializeConnection()`.

#### Data type changes

- Changed `TIMESTAMP_TZ`, `TIMESTAMP_LTZ`, and `TIME` values with a zero UTC offset to show the offset as `Z` instead of `+0000`, `+00:00`, or `+00` when they’re returned as text, for example, `2024-01-15 10:30:00.000 Z`. This format matches the text that Snowflake returns for `TO_CHAR` and `::VARCHAR`. For timestamps, this change applies to `fetchAsString: ['Date']` and `toJSON()`, and therefore also to `JSON.stringify()` of rows. `TIME` values are always returned as text, so for them, this change applies whenever `TIME_OUTPUT_FORMAT` contains `TZH`. `new Date()` reads both forms the same way. If your code checks the offset text with a regular expression or a strict format, also accept `Z`.
- Changed integer columns to return a native JavaScript `BigInt` instead of a `big-integer` object when the `jsTreatIntegerAsBigInt` connection option or the [JS\_TREAT\_INTEGER\_AS\_BIGINT](/sql-reference/parameters#label-js-treat-integer-as-bigint) session parameter is enabled. `BigInt` is built into JavaScript and doesn’t need an extra package. Both types hold the same values and work mostly the same way, but `big-integer` adds its own helper methods. If you use these methods, for example, `.equals()`, `.add()`, or `BigInteger.isInstance()`, switch to `BigInt` operators such as `===` and `+`, and to `typeof value === 'bigint'`.
- Changed `VECTOR` columns to return an array of numbers, such as `[1.5, 2.5, 3.5]`, instead of the text sent by the server, such as `'[1.500000,2.500000,3.500000]'`. If your code parses that text, use the array directly. To get a string instead, add `'Number'` to `fetchAsString`. The array is then returned as JSON text, such as `'[1.5,2.5,3.5]'`, and a NULL value as `'NULL'`, the same as for other numbers.

#### Connection changes

- Changed login tokens to be cached by default. The `clientStoreTemporaryCredential` connection option now defaults to `true` and also controls MFA token caching, replacing the removed `clientRequestMFAToken` option. External browser, OAuth authorization code, and MFA authentication now reuse a cached token, so users are asked to log in less often. MFA tokens are cached only when your account allows it.
  - Tokens are stored in the system keyring when one is available, such as the macOS Keychain, Windows Credential Manager, or a Linux keyring.
  - Without a keyring, for example, on headless Linux or in CI, tokens are stored in a JSON file in the `SF_TEMPORARY_CREDENTIAL_CACHE_DIR` directory. When `SF_TEMPORARY_CREDENTIAL_CACHE_DIR` isn’t set, the file is stored in `$XDG_CACHE_HOME/snowflake` or `~/.cache/snowflake`.
  - If none of these directories can be used, the driver logs a warning and logs in without caching.
  - To turn off caching, set `clientStoreTemporaryCredential: false`.
- Changed `snowflake.createConnection()` to no longer check the values of connection options. A missing or invalid option now fails `connection.connect()` or `connection.connectAsync()` instead. Connecting is the step that reads the connection profile and key files and logs in, so all errors about your settings come from one place. If you wrap `createConnection()` in `try`/`catch` to handle missing or invalid options, handle these errors when you connect instead: in the `connect()` callback, or with `try`/`catch` around `await connection.connectAsync()`.
- Changed `connection.connectAsync()` to report every error by rejecting the returned promise, and removed its callback parameter. Previously, the promise rejected only for some setup errors. Login errors, such as a wrong password, went only to the callback, and the promise still resolved. A callback passed to `connectAsync()` is now never called, so handle errors with `try`/`catch` around `await connection.connectAsync()` or with `.catch()`.
- Changed the `resultPrefetch` connection option to be an alias for the `CLIENT_PREFETCH_THREADS` session parameter, which sets the number of result chunks that the driver downloads at the same time. Snowflake now validates the value. Without this option, the session uses its own `CLIENT_PREFETCH_THREADS` value, which is 4 unless it’s set on the user or account. Previously, the driver validated the value itself and downloaded up to `resultPrefetch + 1` chunks at once, 3 by default.
- Changed connecting to fail with an `InvalidParameterError` when `authenticator` isn’t a supported value, for example, because of a typo. Previously, the driver logged a warning and fell back to password authentication, so the typo could go unnoticed when a `password` was also set.
- Changed connecting to fail with an `InvalidParameterError` when `workloadIdentityProvider`, `workloadIdentityAzureEntraIdResource`, `workloadIdentityImpersonationPath`, or `workloadIdentityAwsUseOutboundToken` is set but `authenticator` isn’t `WORKLOAD_IDENTITY`. Previously, the driver ignored these options and logged in with the other authenticator, which hid a mistake in the connection settings. Remove these options, or set `authenticator` to `WORKLOAD_IDENTITY`.
- Changed `connection.isUp()` to return `false` only when the session has ended: the login expired, or Snowflake reports that the session is closed or no longer exists. Previously, it also returned `false` when Snowflake refused to renew the session for any other reason, for example, because the account no longer allows the client’s IP address. `isUp()` doesn’t contact Snowflake. To check whether a connection can still run queries, use `await connection.isValidAsync()`, which sends a request to Snowflake and also returns `false` in these cases.

#### Query execution changes

- Changed `connection.execute()` to fail with a `ClientError` with code `407001` when it’s called while the connection is still logging in. Previously, the driver held such queries and ran them after the login finished. The new driver doesn’t hold queries. Wait until the connection is established before you run queries, for example, with `await connection.connectAsync()` or inside the `connect()` callback.
- Changed the TypeScript types of `statement.getQueryId()`, `getRequestId()`, `getSqlText()`, `getNumRows()`, and `getColumn()` to include `undefined`, because these methods return `undefined` in some cases, as they did before: for example, while the query is running, after it fails, or for a column that doesn’t exist. They’re now typed as `getQueryId(): string | undefined`, `getRequestId(): string | undefined`, `getSqlText(): string | undefined`, `getNumRows(): number | undefined`, and `getColumn(columnIdentifier: string | number): Column | undefined`, and their descriptions say when they return `undefined`. The returned values didn’t change, so where TypeScript now reports an error but your code knows that the value is set, for example, in the `complete` callback of a successful query, check for `undefined` or add `!`.
- Changed the `complete` callback of `connection.execute()` to receive `undefined` as its `rows` argument when `asyncExec` is `true`. Previously, the driver incorrectly put a `{ queryId }` object in `rows`: `rows` is typed as an array of rows or `undefined`, and an async query has no rows yet. The query ID has always been available from `statement.getQueryId()`, so use that method instead.
- Changed `connection.execute()` with `describeOnly: true` to fail for a multi-statement query. Previously, it succeeded but returned only one placeholder column named `multiple statement execution` instead of the columns of your statements, because Snowflake doesn’t describe the statements of a multi-statement query. To get column metadata, run `describeOnly` on each statement separately.
- Changed `GET` to fail when no file in the stage matches the path or `PATTERN`. Previously, it returned an empty result and downloaded nothing, which also hid a wrong path. If a `GET` in your code can match no files, catch the error, or run `LIST` with the same path and `PATTERN` first.
- Changed `connection.getQueryStatus()` and `connection.getQueryStatusThrowIfError()` to return `'NO_DATA'` instead of the undocumented `'NO_QUERY_DATA'` when Snowflake has no status for the query ID. Snowflake returns no status both for a query that hasn’t started yet and for a query ID that doesn’t exist, so the driver can’t tell these cases apart. `'NO_DATA'` counts as still running, so a loop that waits while `connection.isStillRunning(status)` is `true` keeps waiting for a query ID that doesn’t exist. If your code can pass such an ID, limit how long it waits.

#### Error and configuration changes

- Changed the errors that the driver reports for missing or invalid connection options to be an `InvalidParameterError` without a `code`. The 3.x driver checked each option in its own way, so its errors weren’t consistent: most were an `InvalidParameterError` or a `MissingParameterError` with a code such as `404008`, but some were a plain `Error` with no code. The new driver checks all options in one shared step, so it can no longer give each problem its own code. Instead, the error `message` names every option that’s missing or invalid. If your code checks `error.code` or `MissingParameterError`, check `error.name === 'InvalidParameterError'` instead.
- Changed the type of the `xmlParserConfig` option of `snowflake.configure()` to `X2jOptions` from `fast-xml-parser`. `attributesGroupName: null` no longer compiles in TypeScript. Use `attributesGroupName: false` instead, which works the same way.

### New features and updates

- Added support for connection profiles in the [`config.toml` file](/developer-guide/snowflake-cli/connecting/configure-cli), the configuration file that other Snowflake tools also use. Profiles go under `[connections.<name>]`, and the `default_connection_name` key sets the profile that’s used when `createConnection()` gets no options.
- Added the `connectionName` connection option, which selects a connection profile by name. You can pass other connection options with it. The driver starts from the profile and replaces only the options that you pass, for example, to use a different `warehouse` than the profile sets. Without this option, a profile is read only when `createConnection()` gets no options, as before.
- Added the `proxy` connection option, which sets the proxy as one URL, for example, `http://user:password@proxy.example.com:8080`. The scheme can be `http` or `https` and defaults to `http`. Percent-encode special characters in the user name or password, for example, `@` as `%40`. When `proxyHost`, `proxyPort`, `proxyProtocol`, `proxyUser`, or `proxyPassword` is also set, it replaces the matching part of the URL.
- Added the `protocol` and `port` options to `ConnectionOptions`. These options set the scheme and port used with `host`, and now apply to every request, including external browser and Okta authentication, which previously always used `https` on the default port.
- Added support for a base64-encoded DER key in the `privateKey` connection option. Previously, only a PEM string was accepted.
- Added support for `workloadIdentityImpersonationPath` with the `AZURE` workload identity provider. The path must contain exactly one service principal client ID.
- Added `sqlState` `'28000'` to errors for logins that Snowflake rejects because of wrong credentials, such as a wrong password or an invalid key-pair token.
- Added `isDecfloat()`, `isIntervalYearMonth()`, `isIntervalDayTime()`, and `isVector()` to `Column`, for data types that had no such check.
- Added the `SnowflakeDate` export, the class of the values returned for `DATE` and `TIMESTAMP` columns. It extends `Date` and adds `getEpochSeconds()`, `getNanoSeconds()`, `getScale()`, `getTimezone()`, and `getFormat()`. These methods existed before but had no types, so TypeScript code can now use them after a `value instanceof SnowflakeDate` check instead of a hand-written type.
- Added the `SessionState` type. `statement.getSessionState()` now returns `SessionState | undefined` instead of `object | undefined`, so TypeScript code can call `getCurrentDatabase()`, `getCurrentSchema()`, `getCurrentWarehouse()`, and `getCurrentRole()` without a cast. Each method returns `string | null`.
- Added the `CustomCredentialManager` type. The `customCredentialManager` option of `snowflake.configure()` is now typed as `CustomCredentialManager` instead of `object`. This type declares the `read`, `write`, and `remove` methods that the driver already required, so TypeScript reports a manager without them at compile time, instead of `configure()` throwing an error at runtime.
- Added `snowflake.getFipsStatus()` and the `FipsStatus` type. The method is typed as `getFipsStatus(): FipsStatus`, where `FipsStatus` is `{ isFips: boolean }`, and reports whether the driver’s native library is compiled for FIPS.
- Added support for all `fast-xml-parser` options in the `xmlParserConfig` option of `snowflake.configure()`. Previously, the driver used only `ignoreAttributes`, `alwaysCreateTextNode`, `attributeNamePrefix`, and `attributesGroupName`, and ignored any other option.
- Added multipart uploads to `PUT` and multipart downloads to `GET` on Amazon S3 and Azure stages. Large files now transfer faster, and when a request fails, the driver repeats only that part instead of the whole file. This behavior is always on, so the experimental `enableExperimentalMultipartUploads` option of `snowflake.configure()` was removed. Multipart transfers work as follows:
  - A file is split into parts when its size, after compression and encryption, is at least the limit that Snowflake sends for each `PUT` and `GET` command. This limit is currently 200 MiB. Smaller files are still sent in one request.
  - Each part is 8 MiB. For very large files, the parts are bigger, so the file stays within the limit on the number of parts: 10,000 on Amazon S3 and 50,000 on Azure.
  - Parts are sent in parallel. The `PARALLEL` option of `PUT` and `GET` sets how many requests run at once for the whole command. A single file uses at most 16 requests at once. The driver reads the file one part at a time, so it never holds the whole file in memory.
  - When an upload part fails, for example, because the stage credentials expired, the driver retries only that part. If an Amazon S3 upload still fails, the driver cancels it, which deletes the parts already sent.
  - On Google Cloud Storage, `PUT` intentionally sends each file in one request, because one request is much faster than a multipart upload on Google Cloud Storage.
  - In version 3.x, with `enableExperimentalMultipartUploads` turned on, uploads were split starting at 64 MiB, parts were sent one at a time, and Google Cloud Storage uploads were also split into parts.

### Changes

- Changed the format of the string returned by `connection.serialize()`. As documented, the format can change between driver versions, so pass the string to `snowflake.deserializeConnection()` only on the same driver version. If several processes share serialized connections, upgrade them all at the same time.
- Removed the client-side length check for the `queryTag` connection option. Snowflake still checks the value when you connect, so an invalid `queryTag` can still fail when `connect()` or `connectAsync()` is called.
- Removed the format check for the `application` connection option. Any string is now accepted, because Snowflake doesn’t check this value.
- Changed how `ISA` is reported in telemetry to be consistent with other drivers.
- Changed when `PLATFORM` is reported in telemetry, so it no longer blocks the first connection request.

### Bug fixes

#### Bug fixes that might affect your code

The following fixes change a value, error, or type that the driver returns. If your code works around the old behavior, update it.

- Fixed `fetchAsString: ['JSON']` returning only `VARIANT` columns as strings. It now also covers `OBJECT`, `ARRAY`, and `MAP` columns. This includes `FILE` columns, and `GEOGRAPHY` and `GEOMETRY` columns in the default GeoJSON format, because their `getType()` is `'object'`. Their values are returned as the JSON text sent by Snowflake, such as `'{\n "key": "value"\n}'`, and NULL values as `'NULL'` unless `representNullAsStringNull` is `false`. If your code reads these columns as objects, parse them with `JSON.parse()`.
- Fixed `TIME` columns returning the string `'NULL'` instead of `null` for NULL values. All other types already returned `null`. If your code checks a `TIME` value for `'NULL'`, check for `null` instead.
- Fixed `FLOAT` columns returning `NaN` for the values `inf` and `-inf`. They now return `Infinity` and `-Infinity`, so they can be distinguished from a real `NaN`. If your code finds these values with `Number.isNaN()`, use `!Number.isFinite()` instead.
- Fixed the `BLOCKED` query status being treated as a failure. A blocked query hasn’t finished and can still succeed, so `isStillRunning('BLOCKED')` now returns `true` and `isAnError('BLOCKED')` returns `false`. `getQueryStatusThrowIfError()` no longer throws an error for this status, and `getResultsFromQueryId()` waits for the query to finish instead of failing. If your code handles `BLOCKED` as a failure, remove that handling.
- Fixed `statement.getNumUpdatedRows()` returning `-1` for `COPY INTO <table>`. It now returns the number of rows loaded. If your code checks for `-1` after `COPY INTO`, use the returned number instead.
- Fixed `Column.isObject()` and `Column.isArray()` returning `false` for `OBJECT` and `ARRAY` columns, even though `getType()` returned `'object'` or `'array'`. Code that branches on these methods now takes the `OBJECT` or `ARRAY` branch for these columns.
- Fixed `connection.getQueryStatusThrowIfError()` rejecting with code `-1` when the query failed on the server. The error now has the query’s Snowflake error code, for example, `'002003'`. If your code checks for code `-1`, check the Snowflake error code instead.
- Fixed `pool.acquire()` and `pool.use()` rejecting with a plain `Error` when a pooled connection fails to connect. They now reject with the original connection error, including its `name`, `code`, and `sqlState`. If your code checks the message of that error, check its `name` or `code` instead.
- Fixed `targetSize` in `PUT` results not matching the size of the file stored in the stage. On stages with client-side encryption, it was the size before encryption. It’s now the size after encryption, which is slightly larger.
- Fixed `Column.getScale()` and `Column.getPrecision()` being typed to return `number`. They return `null` for columns that have no scale or precision, such as `TEXT` columns. They’re now typed as `getScale(): number | null` and `getPrecision(): number | null`, so TypeScript might ask you to handle `null` where you use these values.

#### Other bug fixes

- Fixed `representNullAsStringNull` set on one connection also applying to every other connection in the same process.
- Fixed the missing `status` argument in the `connection.isAnError()` types. The method is now typed as `isAnError(status: QueryStatus): boolean`.
- Fixed `connection.getQueryStatus()` and `connection.getQueryStatusThrowIfError()` being typed to return `Promise<string>`, which meant that TypeScript code had to cast the result before passing it to `isStillRunning()` or `isAnError()`. They’re now typed as `getQueryStatus(queryId: string): Promise<QueryStatus>` and `getQueryStatusThrowIfError(queryId: string): Promise<QueryStatus>`.
- Fixed the `Bind` type missing `Date`. The driver has always accepted `Date` values in `binds`, but the type didn’t list it.
- Fixed a `QUERY_TAG` passed in the `parameters` option of `connection.execute()` being replaced by the `queryTag` connection option. The statement’s `QUERY_TAG` now applies to that query, and later queries still use the connection’s `queryTag`.
- Fixed `ALTER SESSION SET CLIENT_STAGE_ARRAY_BINDING_THRESHOLD` having no effect when the `arrayBindingThreshold` connection option is set. The option now sets only the starting value of the session parameter, so the value that’s set last decides when binds are uploaded to a stage.
- Fixed the `options` argument of `snowflake.configure()` being typed as optional. A call without arguments always threw a `TypeError`. The method is now typed as `configure(options: ConfigureOptions): void`, so TypeScript reports this mistake at compile time.
- Fixed `snowflake.configure()` dropping an earlier `customLogger` or `additionalLogToConsole` value when a later call sets another logging option, such as `logLevel`. Logging options now keep their earlier values, like every other `configure()` option, and a call that sets only `additionalLogToConsole` now takes effect.
- Fixed `snowflake.deserializeConnection()` ignoring the `clientSessionKeepAlive` option.
- Fixed `PUT` failing with a `TypeError` when `SOURCE_COMPRESSION` is `BROTLI`, `AUTO_DETECT`, or `NONE`.
- Fixed `sourceCompression` in `PUT` results always being `null`. It now shows the compression type of the source file, such as `'NONE'` or `'GZIP'`.
- Fixed `PUT` failing when the source path starts with `~` or contains the `?` wildcard. `~` now means your home directory, and `?` matches any single character.

## Version 3.4.1 (October 26, 2026)

### New features and updates

- Added the HTTP status of the failed storage request, such as `(HTTP 502)`, to `PUT` and `GET` errors from S3, Azure, and Google Cloud Storage stages. The HTTP status helps you diagnose failures when the storage response can’t be read, such as an S3 `Deserialization error` caused by a proxy that returns a plain-text error.

### Bug fixes

- Fixed concurrent S3 file transfers through a proxy failing with `socket hang up` because finishing one transfer closed the proxy connections that other transfers were still using.
- Fixed `GET` from S3 and Azure stages failing with `TypeError: Cannot read properties of null (reading 'encryptionMetadata')` when the file metadata request failed but the download itself succeeded (for example, when an HTTPS proxy rejected the TLS handshake). The `GET` now fails with the underlying error before decrypting the file.
- Fixed a failed `GET` of an encrypted file leaving the still-encrypted download in the local directory when the file metadata request failed or the file couldn’t be decrypted. When the metadata request fails, the error now includes its HTTP status.
- Fixed `PUT` failing with `Unknown error during PUT of file` after the file was uploaded, when the follow-up request that checks whether the file is on the stage failed.
- Fixed `GET` from Google Cloud Storage stages hanging indefinitely when the connection broke during the download. The driver now retries the download.
- Fixed queries failing with `Unable to perform operation using terminated connection.` (`407002`) when the expired session couldn’t be renewed. These queries now fail with the server error that explains the cause, for example, `390114` when the authentication token expired after the connection was idle for too long.
- Fixed a late session-expired response starting another session renewal on a connection that a failed renewal had already closed.

## Version 3.4.0 (September 30, 2026)

### Security fixes

- Hardened `EXTERNALBROWSER` authentication by binding the local callback listener to `127.0.0.1` and rejecting requests whose `Origin` header doesn’t match the connected Snowflake account. The listener now ignores incomplete or unrelated requests instead of ending the login.

### New features and updates

- Added the `workloadIdentityHost` connection option that overrides the STS host used by AWS workload identity flows, so AWS partitions unknown to the driver can be reached. When this option isn’t set, the STS host is derived from the AWS region.
- Bumped the `toml` dependency to version 5.0.0.

### Changes

- Turned OCSP off by default and marked OCSP support as deprecated. OCSP support will be removed in the next major release. Use CRL validation (`certRevocationCheckMode`) instead.
  - To keep using OCSP, call `snowflake.configure({ disableOCSPChecks: false })`, `snowflake.configure({ ocspFailOpen: true })` for fail-open, or `snowflake.configure({ ocspFailOpen: false })` for fail-closed. If both options are provided in the same call, `disableOCSPChecks: true` turns OCSP off regardless of `ocspFailOpen`. CRL still takes precedence when `certRevocationCheckMode` is enabled.
  - Deprecated APIs: OCSP options (`disableOCSPChecks`, `ocspFailOpen`, `useConnectionConfigProxyForOCSP`), `connection.setupOcspPrivateLink()`, `ocspModes`, and OCSP error codes.

### Bug fixes

- Fixed failed `PUT` operations reporting `Unknown Error in uploading a file` instead of the underlying storage error.

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
