# Migrating from JDBC Driver 4.x to 5.x

[Preview Feature](/release-notes/preview-features) — Open

JDBC Driver 5.x is in public preview and available to all accounts. Validate it against a non-production account. Preview builds are not covered by the client support policy in [Client versions & support policy](/release-notes/requirements). The pages under [JDBC Driver](/developer-guide/jdbc/jdbc) describe JDBC Driver 4.x. Use of this preview is subject to [Snowflake’s Preview Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/preview-terms-of-service/).

Version 5.x of the Snowflake JDBC Driver is built on the [Universal Core](/developer-guide/universal-core/universal-core). The `jdbc:snowflake:` URL and the JDBC API stay the same, except where this page notes differences. `net.snowflake.client.jdbc.SnowflakeDriver` still loads. It is deprecated in favor of `net.snowflake.client.api.driver.SnowflakeDriver`, which is the class registered with `java.sql.Driver`.

Migrating from JDBC Driver 3.x to 5.x requires the 4.x API migration first. See [Migrating from JDBC Driver 3.x to JDBC Driver 4.x](/developer-guide/jdbc/jdbc-migration). This page starts from that API.

The Universal Core (`sf_core`) is a shared Rust library that implements the networking, authentication, result-set fetching, and stage-transfer logic that every Snowflake driver needs. Each driver wraps that core in a thin, language-specific layer that exposes the interface its ecosystem expects; the Rust layer is not visible to application code.

Snowflake previously maintained a separate implementation of this logic in each driver, so a security fix or protocol change had to be applied separately to every one. Because the core is shared, a change to it reaches every driver built on it in that driver’s next release.

Replace `snowflake-jdbc` or `snowflake-jdbc-thin` with one 5.x artifact. Do not leave a 4.x jar on the same classpath: both drivers register `jdbc:snowflake:`, and `DriverManager` uses whichever it finds first. Most applications that are already on the 4.x API need no code changes. Validate on a non-production application before you change the production dependency.

## Install

Important

The driver loads a native library with JNI. It runs only on a JVM that permits JNI and native library loading.

The driver runs only when all of the following are true:

- A 64-bit JVM, Java 8 or later.
- Linux x86\_64 or aarch64, macOS x86\_64 or aarch64, or Windows x86\_64. On Linux the driver selects the glibc or musl library. When it cannot detect the C library, it selects glibc. Set `-Djdbc.libc=musl` on a musl host in that case.
- `net.snowflake:snowflake-jdbc-native:5.0.0-RC1` with a platform classifier, or `net.snowflake:snowflake-jdbc-native-all:5.0.0-RC1`.
- A writable `java.io.tmpdir`. The driver copies the native library from the jar there and loads it with JNI.
- No `snowflake-jdbc`, `snowflake-jdbc-fips`, or `snowflake-jdbc-thin` jar on the classpath.

Choose one package. `snowflake-jdbc-native` is the smaller one: the native library for a single platform, with its other libraries downloaded alongside it. `snowflake-jdbc-native-all` is one larger jar that contains every platform and those libraries. Use it when the same jar has to run on more than one platform.

A FIPS-compliant 5.x package is not available yet. JNA is not required.

After connecting, `DatabaseMetaData.getDriverVersion()` returns `5.0.0-RC1`.

### `snowflake-jdbc-native`

Set the classifier to the platform where the application runs: `linux-x86_64`, `linux-aarch_64`, `osx-x86_64`, `osx-aarch_64`, or `windows-x86_64`. The examples use Linux x86\_64. With no classifier, the jar contains no native library and the driver does not run.

Maven:

Copy code

```
<dependency>
  <groupId>net.snowflake</groupId>
  <artifactId>snowflake-jdbc-native</artifactId>
  <version>5.0.0-RC1</version>
  <classifier>linux-x86_64</classifier>
</dependency>
```

Gradle:

Copy code

```
implementation "net.snowflake:snowflake-jdbc-native:5.0.0-RC1:linux-x86_64"
```

### `snowflake-jdbc-native-all`

This jar bundles a native library for every supported architecture and selects the one for the host at runtime.

Maven:

Copy code

```
<dependency>
  <groupId>net.snowflake</groupId>
  <artifactId>snowflake-jdbc-native-all</artifactId>
  <version>5.0.0-RC1</version>
</dependency>
```

Gradle:

Copy code

```
implementation "net.snowflake:snowflake-jdbc-native-all:5.0.0-RC1"
```

### Set the classifier from the build machine

Maven and Gradle do not detect the platform. To use the machine that runs the build, add the plugin below and use its property as the classifier in the `snowflake-jdbc-native` dependency above, in place of `linux-x86_64`. `snowflake-jdbc-native-all` does not use a classifier.

The [os-maven-plugin](https://github.com/trustin/os-maven-plugin) extension sets `${os.detected.classifier}`:

Copy code

```
<build>
  <extensions>
    <extension>
      <groupId>kr.motd.maven</groupId>
      <artifactId>os-maven-plugin</artifactId>
      <version>1.7.1</version>
    </extension>
  </extensions>
</build>
```

The [osdetector](https://github.com/google/osdetector-gradle-plugin) plugin sets `osdetector.classifier`:

Copy code

```
plugins {
    id 'com.google.osdetector' version '1.7.3'
}
```

## Native library and JVM settings

The JDBC classes stay in the JVM. Login, query execution, authentication, TLS, HTTP, and PUT and GET run in the Universal Core native library, loaded with JNI from the jar. JDBC Driver 4.x uses JNA for its credential cache. This driver does not. Do not add the JNA jars.

Result data and network buffers live off the JVM heap, so `-Xmx` does not limit them. `CLIENT_MEMORY_LIMIT` limits buffered result chunks, in megabytes. The default is 1536. A value of 0 removes that limit. Values the application reads, such as strings, still occupy the JVM heap.

Snowflake traffic does not use JSSE or the Apache HTTP client. These settings do not apply:

- `javax.net.ssl.trustStore`, `javax.net.ssl.trustStorePassword`, `javax.net.ssl.trustStoreType`. Set `extra_root_store_path` to a PEM file to add those certificates to the default root store, or `custom_root_store_path` to a PEM file that replaces it. `custom_root_store_path` wins, and `extra_root_store_path` is then ignored.
- `jdk.tls.client.protocols`, `jdk.tls.disabledAlgorithms`. Set `min_tls_version` and `max_tls_version` to `tls12` or `tls13`. Any other spelling, `TLSv1.2` included, is rejected.
- A default `SSLSocketFactory` or `HostnameVerifier` on `HttpsURLConnection`.
- `net.snowflake.jdbc.ocspFailOpen`, `net.snowflake.jdbc.ocspResponseCacheDir`. *(BD#46)*
- `net.snowflake.jdbc.enableBouncyCastle`, `net.snowflake.jdbc.useBundledBouncyCastleForPrivateKeyDecryption`. `privateKey`, `private_key_file`, and `private_key_base64` still work.
- `net.snowflake.jdbc.max_connections`, `net.snowflake.jdbc.max_connections_per_route`.
- `net.snowflake.jdbc.http_client_connection_timeout_in_ms`, `net.snowflake.jdbc.http_client_socket_timeout_in_ms`. The connection properties `HTTP_CLIENT_CONNECTION_TIMEOUT`, `HTTP_CLIENT_SOCKET_TIMEOUT`, and `networkTimeout` take milliseconds and apply in whole seconds, rounded up. Each HTTP attempt uses a 300-second wall-clock timeout, measured from the start of the attempt to the end of the response body, so arriving bytes do not extend it and a response that takes longer than five minutes fails. Result-chunk downloads are outside that limit and have no read timeout of their own. `networkTimeout` does not bound retries of query requests. *(BD#77, BD#78)*

## Proxy

Set an HTTP or HTTPS proxy with `useProxy`, `proxyHost`, and `proxyPort`, or with `-Dhttp.useProxy=true` plus `http.proxyHost` or `https.proxyHost` and the matching port. The JVM properties apply when the connection does not set a proxy, and both a host and its port must be set. `http.nonProxyHosts` is included, and the `NO_PROXY` environment variable is merged into it.

`-DsocksProxyHost`, `-DsocksProxyPort`, and `java.net.useSystemProxies` do not apply. `disableSocksProxy` does not change routing. *(BD#64)*

`nonProxyHosts=foo.com` bypasses `foo.com` and its subdomains. JDBC 4.x bypasses only the exact host. `*` bypasses domains and not IP addresses. `10.0.0.0/8` is a CIDR. `192.168.*` is not. Matching is case-sensitive. *(BD#65)*

## Logging

Driver messages and native-library messages are delivered to the application logger. Native-library messages use `net.snowflake.client.CoreLogger`. DEBUG is the finest level.

SLF4J is recommended. The driver includes the SLF4J API. Add a binding such as Logback:

```
-Dnet.snowflake.jdbc.loggerImpl=net.snowflake.client.log.SLF4JLogger
```

Set the level on `net.snowflake.client` and `net.snowflake.client.CoreLogger`.

When `net.snowflake.jdbc.loggerImpl` is unset, delivery uses `java.util.logging` (`net.snowflake.client.log.JDK14Logger`). With that logger, a `tracing` connection property writes `%h/snowflake_jdbc%u.log` unless `java.util.logging.config.file` is set.

`SNOWFLAKE_TROUBLESHOOTING_ENABLED=true`, set before the process starts, writes `sf_driver_troubleshooting.log`. `SNOWFLAKE_TROUBLESHOOTING_REPORT_PATH` selects the directory. Otherwise the file is written in the current directory.

## Configuration differences

Camel-case names such as `proxyHost`, `loginTimeout`, `putGetMaxRetries`, and `oauthClientId` are mapped to the names the Universal Core uses. `browser_response_timeout` is mapped to `authentication_timeout`.

| 4.x name or call | 5.x |
| --- | --- |
| `clientRequestMfaToken`, `setEnableClientRequestMfaToken` | Ignored, with a log warning. Use `clientStoreTemporaryCredential`. *(BD#5)* |
| `setEnableClientStoreTemporaryCredential` | Removed. Use `setClientStoreTemporaryCredential`. *(BD#31)* |
| `setOcspFailOpen`, `disableOCSPChecks`, `insecureMode` | No OCSP. Set `crl_check_mode` to `ENABLED` (fail-close) or `ADVISORY` (fail-open). The default is `DISABLED`. *(BD#46)* |
| `ocspFailOpen` | Still accepted, but it is no longer a TLS setting: it is forwarded as a login session parameter and checks no certificate. *(BD#46)* |
| `setHttpHeadersCustomizers` | Removed. *(BD#43)* |
| `setClientConfigFile` | Removed. Configure logging on the application logger. *(BD#31)* |
| `SnowflakeDataSource.setNetworkTimeout` | Absent. `Connection.setNetworkTimeout` does not store the value, and `getNetworkTimeout` returns `0`. *(BD#31, BD#41)* |
| `setEnablePutGet` | Absent. The connection property `enablePutGet` still applies. *(BD#31)* |
| `setStringsQuotedForColumnDef` | Absent. The connection property `STRINGS_QUOTED_FOR_COLUMN_DEF` still applies. *(BD#31)* |
| `setDisableGcsDefaultCredentials`, `disableGcsDefaultCredentials` | Not read. *(BD#31)* |
| `ownerOnlyStageFilePermissionsEnabled` | Not read. A GET writes mode `0600` on Unix. Set `unsafe_file_write` to `true` to restore the process umask. *(BD#56)* |
| `putGetMaxRetries` unset | PUT and GET retry 6 times. JDBC 4.x retries 25. A zero or negative value also gives 6. A positive value is used as given. *(BD#79)* |
| `disableQueryContextCache`, `private_key_pwd`, `PRIVATE_KEY_PWD`, `PRIVATE_KEY_BASE64`, `wifHost`, `workloadIdentityHost` | No longer applied in a `connections.toml` or `config.toml` profile, and the setting is lost without an error. `disable_query_context_cache`, `PRIVATE_KEY_FILE_PWD`, and `workload_identity_host` still apply. *(BD#71)* |
| `/snowflake/session/token`, `SKIP_TOKEN_FILE_PERMISSIONS_VERIFICATION` | Not read. Supply the token file path explicitly. `SNOWFLAKE_HOME` is used only when that directory exists; otherwise the platform config directory is used. *(BD#71)* |

Expand

Show lessSee more

Drivers built on the Universal Core do not support OCSP-based certificate revocation checking. Revocation checking is available only through CRLs (certificate revocation lists), and it is off by default.

If you require revocation checking, enable CRL checking and evaluate it in a non-production environment under a realistic workload. Confirm that your network allows outbound access to the CRL distribution points named in Snowflake’s certificate chain: a driver that cannot reach a distribution point cannot complete a revocation check.

## Behavior differences

### Authentication

- **`clientRequestMfaToken=false` does not turn caching off.** Set `clientStoreTemporaryCredential=false`. That one property covers MFA, browser, and OAuth token caching. Both default to `true`. *(BD#5)*
- **OAuth token and authorization URLs must use HTTPS.** A non-loopback `http://` value is rejected at connect. *(BD#10)*
- **Remove workload-identity settings unless `authenticator=WORKLOAD_IDENTITY`.** A non-empty provider, Entra resource, Azure client id, impersonation path, or `wif_host`, or `workloadIdentityAwsUseOutboundToken=true`, fails the connection. JDBC 4.x ignored those settings on other authenticators. *(BD#48)*
- **Remove `workloadIdentityImpersonationPath` when the provider is `OIDC`.** JDBC 4.x ignored the path and logged in as the original identity. *(BD#49)*
- **Remove `workloadIdentityAwsExternalId`.** With AWS workload identity a non-empty value fails the connection. The value is not sent on `AssumeRole`. *(BD#73)*
- **Local workload-identity failures have no SQLSTATE or vendor code.** `getSQLState()` is null and `getErrorCode()` is `0`. JDBC 4.x used `08000` and `200071`. *(BD#75)*
- **A missing OAuth client id, secret, or token URL is one error** naming every missing `oauth_client_id`, `oauth_client_secret`, and `oauth_token_request_url`. JDBC 4.x reports the first gap as vendor code `200001`. *(BD#6)*

Password, key-pair, and external-browser login keep the same authenticator names.

### Statements and batches

- **`Statement.getQueryID()` after a synchronous multi-statement execute returns the parent id.** JDBC 4.x returns the first child’s id. *(BD#24)*
- **`getUpdateCount()` after a result-set statement returns `-1`**, including `SELECT`, PUT, GET, and REMOVE. *(BD#58)*
- **`executeBatch()` with an update count above `Integer.MAX_VALUE` returns `SUCCESS_NO_INFO` (`-2`).** JDBC 4.x throws `BatchUpdateException` vendor code `200058`. *(BD#2)*
- **`getBatchQueryIDs()` keeps one slot per statement**, including a failed statement. An array bind records one id. JDBC 4.x records none. *(BD#3)*
- **`getUpdateCount()` after `executeBatch()` returns `-1`.** JDBC 4.x returns the last count. *(BD#4)*
- **`addBatch()` rejects a later row that omits a placeholder bound on the first row.** *(BD#11)*
- **A failed array-bind `executeBatch()` throws `BatchUpdateException`.** `catch (SnowflakeSQLException)` does not see it. *(BD#72)*

### Results

- **`JDBC_ARROW_TREAT_DECIMAL_AS_INT` applies to JSON results.** With `JDBC_QUERY_RESULT_FORMAT=JSON`, `JDBC_TREAT_DECIMAL_AS_INT=false`, and `JDBC_ARROW_TREAT_DECIMAL_AS_INT` left at its default `true`, `getObject()` returns `Long` for a scale-0 number. JDBC 4.x returns `BigDecimal`. Metadata still follows `JDBC_TREAT_DECIMAL_AS_INT`, so the SQL type can be `DECIMAL` while `getObject()` returns `Long`. A connection that leaves both properties at `true` sees no change. *(BD#60)*
- **A `GEOGRAPHY` or `GEOMETRY` column in `WKB` or `EWKB` output reports `VARCHAR`.** `getColumnType()` is `VARCHAR` and `getColumnClassName()` is `java.lang.String`, while `getObject()` and `getBytes()` still return the bytes. JDBC 4.x reports `BINARY`. Code that reads the column type and then treats the value as text can mangle the bytes. `GeoJSON` and `WKT` output is `VARCHAR` on both drivers. *(BD#53)*
- **`isLast()` and `isAfterLast()` on a `DatabaseMetaData` result set return a boolean.** JDBC 4.x throws a `SQLFeatureNotSupportedException` subclass from the query-backed metadata calls, so a `catch` around those two methods no longer runs. *(BD#21)*

### DataSource

- **`DataSource.getProperties()` returns a copy.** Configure the DataSource with its setters: editing the returned map no longer changes later connections. A user and password passed to `getConnection(username, password)` apply to that call only and no longer appear in a later `getProperties()`. *(BD#44)*
- **`DataSource.getConnection()` no longer rejects a missing username up front.** A programmatic-access-token, `OAUTH_AUTHORIZATION_CODE`, or `OAUTH_CLIENT_CREDENTIALS` login, and OAuth or workload identity set outside `setAuthenticator`, connect with no username. Password, key-pair, external-browser, Okta, and MFA login still fail, but at connect and with the message `Missing required parameter: user`, so code matching on `Cannot create connection because username is missing in DataSource properties.` has to change. An empty-string username counts as missing. *(BD#45)*
- **`PooledConnection.getConnection()` invalidates the handle it returned last.** Code still holding the older handle gets vendor code `200052` and SQLSTATE `08003` from `createStatement()` and the other calls that need a live connection, and `isClosed()` returns `true`. JDBC 4.x leaves both handles working against the same session. *(BD#36)*
- **A closed logical handle no longer reaches the physical connection.** `setClientInfo`, both `getClientInfo` methods, `unwrap`, and `isWrapperFor` throw vendor code `200052` and SQLSTATE `08003`. `unwrap(Connection.class)` returns the closed handle itself. *(BD#29, BD#33)*
- **`PooledConnection.getConnection()` after `close()`, and `abort()` on a borrowed handle, throw a checked `SQLException`.** JDBC 4.x throws `NullPointerException` from the first and leaves `isClosed()` false after the second, so a `catch (NullPointerException)` there no longer runs. *(BD#27, BD#40)*
- **`connectionErrorOccurred` no longer fires for caller mistakes.** A `SQLFeatureNotSupportedException`, a rejected client-info property, and an `unwrap` to an unsupported type reach the caller without the event, so a pool no longer evicts a healthy connection over them. Any other `SQLException` still fires it. *(BD#26, BD#32, BD#35)*
- **A listener that throws no longer stops dispatch**, and a listener handling `connectionClosed` observes `isClosed()` as `true`. *(BD#28, BD#30)*

### Driver

- **`Driver.getPropertyInfo` asks for `user` and `password`** when `authenticator` is empty or `USERNAME_PASSWORD_MFA`. *(BD#68, BD#69)*
- **`Driver.getPropertyInfo` does not include a malformed URL.** SQLSTATE stays `08000` and vendor code stays `200059`. *(BD#66)*
- **`Driver.getPropertyInfo` rejects a non-String `proxy_host`, `proxy_port`, `proxyHost`, or `proxyPort`** with SQLSTATE `22023` and vendor code `200033`. `connect` applies no such check, so an integer `proxy_port` still connects. Only a `Properties.put` of a non-`String` reaches this; a URL query value is always a string. *(BD#67)*
- **`Driver.getPropertyInfo` parses a `jdbc:snowflake:auto` URL the same way `connect` does.** A malformed auto URL reports `INVALID_PARAMETER_VALUE` rather than `INVALID_CONNECTION_STRING`, so code matching the latter has to accept it. *(BD#71)*

### Connection

- **`jdbc:snowflake:auto` also reads `[connections.<name>]` from `config.toml`.** `connections.toml` wins when both files define the name. Profile selection falls back through `SNOWFLAKE_DEFAULT_CONNECTION_NAME`, `default_connection_name` in `config.toml`, and then `default`. *(BD#71)*
- **`jdbc:snowflake:auto` validates strictly.** A malformed query, a URL fragment, a duplicate alias, and a non-String selector in `Properties` report `INVALID_PARAMETER_VALUE`. Two aliases with equal values are accepted, where JDBC 4.x rejected them. *(BD#71)*
- **A missing profile carries SQLSTATE `22023` and vendor code `200047`.** The message is unchanged, so it can be classified instead of string-matched. JDBC 4.x reported no SQLSTATE and vendor code `0`. *(BD#71)*
- **`Properties` override URL options, and `connectionName` and `connection_name` are matched case-insensitively.** JDBC 4.x matched the exact, case-sensitive `connectionName` URL key. A `url` entry in `Properties` supplies the auto URL when the JDBC URL argument is blank. *(BD#71)*

### Clob

- **`setAsciiStream` writes characters.** `'a'` then `'b'` yields `"ab"`. JDBC 4.x yields `"98"`. *(BD#14)*
- **`free()` invalidates the handle.** JDBC 4.x leaves an empty Clob that still accepts calls. *(BD#15)*
- **`position` searches forward from 1.** `position("world", 1)` on `"hello world"` returns `7`. *(BD#16)*
- **`setString(pos, str, offset, len)` copies `len` characters.** `setString(1, "XXhelloYY", 2, 5)` writes `"hello"`. JDBC 4.x writes `"hel"`. *(BD#17)*
- **`setString` overwrites.** `"hello world"` plus `setString(1, "HELLO")` is `"HELLO world"`. JDBC 4.x yields `"HELLOhello world"`. *(BD#13)*

### PUT and GET

- **PUT canonicalizes every source path**, including `..` and a symlink. A symlinked file is uploaded under the target’s base name. *(BD#57)*
- **An auto-compressed PUT does not store `Content-Encoding: gzip`.** GET and COPY still use the compression recorded with the file. *(BD#76)*
- **The size columns are `BIGINT`, not `DECIMAL`.** Under the default `JDBC_TREAT_DECIMAL_AS_INT=true`, PUT `source_size` and `target_size` and GET `size` report `BIGINT`, type name `NUMBER`, precision 64, and `getObject()` returns `Long`, so a cast of `getObject()` to `BigDecimal` throws `ClassCastException`. `getLong`, `getString`, and `getBigDecimal` are unaffected. `status` and `message` are `VARCHAR` with declared length 10000 rather than 20480. *(BD#54)*
- **A GET writes mode `0600` on Unix** rather than following the process umask. A second local account or group that could read downloaded stage files loses access unless the deployment sets `unsafe_file_write` to `true`. Windows is unaffected. *(BD#56)*
- **A failed GET leaves an existing destination file intact.** The download is staged as `<dst>.part` and renamed on success, so cleanup code that deleted a truncated destination is no longer needed. A hard process kill can leave a `.part` file behind. *(BD#25)*
- **A GET whose files collapse to one local basename logs a `WARNING`** naming every colliding basename. The result status and the surviving file are unchanged. *(BD#61)*

Every behavior difference between the generally available driver and the version built on the Universal Core is catalogued in the driver source repository, as a machine-readable file listing each entry’s previous behavior, new behavior, classification, and whether it is a breaking change. Read it in full before you upgrade an application you cannot easily roll back:

- [Snowflake JDBC Driver 5.x behavior-difference catalog](https://github.com/snowflakedb/drivers/tree/main/jdbc/behavior_differences)

The sections above summarize the entries most likely to affect an existing application. The catalog is the complete list.

## Differences removed during preview

Earlier preview builds differed from JDBC Driver 4.x on these items. Those behavior differences have been removed:

- A programmatic-access-token login with a token and no password connects. *(BD#1)*
- Binding a `DATE` when `DATE_OUTPUT_FORMAT` contains `MON` succeeds. *(BD#7)*
- `getTransactionIsolation()` returns the value last set. The default is `TRANSACTION_NONE`. *(BD#18)*
- A query-context cache entry is displaced when a new id arrives at the same priority. *(BD#59)*
- An Okta authenticator rejection includes the Snowflake message. *(BD#63)*
