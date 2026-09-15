# JDBC Driver connection parameter reference

This topic lists the connection parameters that you can use to configure the JDBC driver.
You can set these parameters in the [JDBC connection string](/developer-guide/jdbc/jdbc-configure#label-jdbc-connection-string) or in a Java `Properties`
object.

## Required parameters

This section lists the parameters that you must set in the connection string or in the `Map` of properties.

Note

You must also set the [parameters for authentication](#label-jdbc-connection-parameters-auth-section).

### `user`

> Description:
> :   Specifies the login name of the user for the connection.

## Authentication parameters

### `allowUnderscoresInHost`

> Description:
> :   Specifies whether to allow underscores in account names. The JDBC Driver does not support underscores in URLs,
>     which include the account name, so
>     the JDBC Driver automatically converts underscores to hyphens. The default value is `false`.
>
>     Note
>
>     Beginning with version 3.13.25, the Snowflake JDBC driver changes the default value of the `allowUnderscoresInHost` parameter to `false`.
>     This change impacts PrivateLink customers whose account names contain underscores. In this situation, you must override
>     the default value by setting `allowUnderscoresInHost` to `true`.

### `authenticator`

> Description:
> :   Specifies the authenticator to use for verifying user login credentials. You can set this to one of the following
>     values:
>
>     Version 4.xVersion 3.x
>
>     | Value | Description |
>     | --- | --- |
>     | `snowflake` | Use the internal Snowflake authenticator. |
>     | `externalbrowser` | [Use your web browser](/user-guide/admin-security-fed-auth-use#label-browser-based-sso) to authenticate with Okta, AD FS, or any other SAML 2.0-compliant identity provider (IdP) that has been defined for your account. |
>     | `https://<okta_account_name>.okta.com` | The URL endpoint for your Okta account to [authenticate through native Okta](/user-guide/admin-security-fed-auth-use#label-native-sso-okta) (only supported if your IdP is Okta). |
>     | `oauth` | Authenticate using OAuth. When OAuth is specified as the authenticator, you must also set the `token` parameter to specify the OAuth token ([see below](/developer-guide/jdbc/jdbc-parameters#label-jdbc-additional-connection-parameters-token)). |
>     | `snowflake_jwt` | Authenticate using key pair authentication. For more details about key pair authentication, see [Using key pair authentication and key rotation](/developer-guide/jdbc/jdbc-configure#label-jdbc-using-key-pair-authentication). |
>     | `username_password_mfa` | Authenticate with MFA token caching. For more details, see [Using multi-factor authentication](/developer-guide/jdbc/jdbc-configure#label-jdbc-multi-factor-auth). |
>     | `oauth_authorization_code` | Manually authenticate using an OAuth authorization code with your web browser and a chosen identity provider (including Snowflake as an IdP). For more information, see [Using the OAuth 2.0 Authorization Code flow](/developer-guide/jdbc/jdbc-configure#label-jdbc-oauth-code-flow). |
>     | `oauth_client_credentials` | Automatically authenticate using OAuth client credentials with your chosen identity provider (Snowflake as an IdP doesn’t support the client credentials flow). For more information, see [Using the OAuth 2.0 Client Credentials flow](/developer-guide/jdbc/jdbc-configure#label-jdbc-oauth-client-flow). |
>     | `programmatic_access_token` | Authenticate with a programmatic access token (PAT). For more information, see [Authenticating with a programmatic access token (PAT)](/developer-guide/jdbc/jdbc-configure#label-jdbc-authenticate-pat). |
>     | `WORKLOAD_IDENTITY` | Authenticate with the [workload identity federation (WIF)](/user-guide/workload-identity-federation) authenticator. |
>
>     Expand
>
>     Show lessSee more
>
>     | Value | Description |
>     | --- | --- |
>     | `snowflake` | Use the internal Snowflake authenticator. |
>     | `externalbrowser` | [Use your web browser](/user-guide/admin-security-fed-auth-use#label-browser-based-sso) to authenticate with Okta, AD FS, or any other SAML 2.0-compliant identity provider (IdP) that has been defined for your account. |
>     | `https://<okta_account_name>.okta.com` | The URL endpoint for your Okta account to [authenticate through native Okta](/user-guide/admin-security-fed-auth-use#label-native-sso-okta) (only supported if your IdP is Okta). |
>     | `oauth` | Authenticate using OAuth. When OAuth is specified as the authenticator, you must also set the `token` parameter to specify the OAuth token ([see below](/developer-guide/jdbc/jdbc-parameters#label-jdbc-additional-connection-parameters-token)). |
>     | `snowflake_jwt` | Authenticate using key pair authentication. For more details about key pair authentication, see [Using key pair authentication and key rotation](/developer-guide/jdbc/jdbc-configure#label-jdbc-using-key-pair-authentication). |
>     | `username_password_mfa` | Authenticate with MFA token caching. For more details, see [Using multi-factor authentication](/developer-guide/jdbc/jdbc-configure#label-jdbc-multi-factor-auth). |
>     | `oauth_authorization_code` | Manually authenticate using an OAuth authorization code with your web browser and a chosen identity provider (including Snowflake as an IdP). For more information, see [Using the OAuth 2.0 Authorization Code flow](/developer-guide/jdbc/jdbc-configure#label-jdbc-oauth-code-flow). |
>     | `oauth_client_credentials` | Automatically authenticate using OAuth client credentials with your chosen identity provider (Snowflake as an IdP doesn’t support the client credentials flow). For more information, see [Using the OAuth 2.0 Client Credentials flow](/developer-guide/jdbc/jdbc-configure#label-jdbc-oauth-client-flow). |
>     | `programmatic_access_token` | Authenticate with a programmatic access token (PAT). For more information, see [Authenticating with a programmatic access token (PAT)](/developer-guide/jdbc/jdbc-configure#label-jdbc-authenticate-pat). |
>     | `WORKLOAD_IDENTITY` | Authenticate with the [workload identity federation (WIF)](/user-guide/workload-identity-federation) authenticator. |
>
>     Expand
>
>     Show lessSee more
>
>     If the connection string specifies a key pair and the `authenticator` parameter is unset or is set to ‘snowflake’, then key pair authentication will be used.
>
>     For more information on authentication, see [Managing/Using federated authentication](/user-guide/admin-security-fed-auth-use) and
>     [Clients, drivers, and connectors](/user-guide/oauth-intro#label-oauth-intro-clients-drivers-conns).
>
> Default:
> :   `snowflake`

### `disableGcsDefaultCredentials`

> Description:
> :   Specifies whether use the default credential lookup instead of external application default credentials when using GCP (Google Cloud Platform).
>
>     By default, GCP users can use a variety of options to set up Google Application Default Credentials outside of Snowflake. Occasionally, these authentication methods can interfere with cloud storage operations that originate from the Snowflake JDBC driver. In such cases, you can set the value to `true` to force the driver to ignore GCP credentials from other sources.
>
>     For more information, see [Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc)
>
>     You can also use the `net.snowflake.jdbc.disableGcsDefaultCredentials` Java property to achieve the same effect.
>
> Default:
> :   `true`

### `disableSamlURLCheck`

> Description:
> :   Specifies whether to disable the validation check of a SAML response.
>
> Default:
> :   `false`

### `passcode`

> Description:
> :   Specifies the passcode to use for multi-factor authentication.
>
>     For more information about multi-factor authentication, see [Multi-factor authentication (MFA)](/user-guide/security-mfa).

### `passcodeInPassword`

> Description:
> :   Specifies whether the passcode for multi-factor authentication is appended to the password:
>
>     - `on` (or `true`) specifies the passcode is appended.
>     - `off` (or `false`) or any other value specifies the passcode is not appended.
>
> Default:
> :   `off`

### `password`

> Description:
> :   Specifies the password for the specified user.
>
>     There are two ways to specify the password:
>
>     > - The first way is to pass the user ID and password directly to the `getConnection` method:
>     >
>     >   Copy code
>     >
>     >   ```
>     >   String user = "<user>";          // replace "<user>" with your user name
>     >   String password = "<password>";  // replace "<password>" with your password
>     >   Connection con = DriverManager.getConnection("jdbc:snowflake://<account>.snowflakecomputing.com/", user, password);
>     >   ```
>     > - The second way is to create a `Properties` object, update the object with the password, and pass the object to the
>     >   `getConnection` method:
>     >
>     >   Copy code
>     >
>     >   ```
>     >   String user = "<user>";          // replace "<user>" with your user name
>     >   String password = "<password>";  // replace "<password>" with your password
>     >   Properties props = new Properties();
>     >   props.put("user", user);
>     >   props.put("password", password);
>     >   Connection con = DriverManager.getConnection("jdbc:snowflake://<account>.snowflakecomputing.com/", props);
>     >   ```
>
>     Attention
>
>     We strongly recommend that you do not include the user password directly in the JDBC connection string because the
>     password could be inadvertently exposed by the client application that uses the string to connect to Snowflake. Instead, use
>     the interface(s) provided by the application to specify the user password.

### `privatekey`

> Description:
> :   Specifies the private key for the specified user. See [Using key pair authentication and key rotation](/developer-guide/jdbc/jdbc-configure#label-jdbc-using-key-pair-authentication).

### `private_key_base64`

> Description:
> :   Specifies the base64 encoded private key for the specified user. See
>     [Using key pair authentication and key rotation](/developer-guide/jdbc/jdbc-configure#label-jdbc-using-key-pair-authentication).

### `private_key_file`

> Description:
> :   Specifies the path to the private key file for the specified user. See
>     [Using key pair authentication and key rotation](/developer-guide/jdbc/jdbc-configure#label-jdbc-using-key-pair-authentication).

### `private_key_file_pwd`

> Description:
> :   (Deprecated) Use [private\_key\_pwd](/developer-guide/jdbc/jdbc-parameters#label-jdbc-connection-parameters-private-key-pwd) instead.

### `private_key_pwd`

> Description:
> :   Specifies the passphrase to decrypt the private key file or base64 encoded private key for the specified user. See
>     [Using key pair authentication and key rotation](/developer-guide/jdbc/jdbc-configure#label-jdbc-using-key-pair-authentication).

### `token`

> Description:
> :   Specifies the OAuth token to use for authentication, where `<string>` is the token. This parameter is
>     required only when setting the [authenticator](/developer-guide/jdbc/jdbc-parameters#label-jdbc-connection-parameters-authenticator) parameter to `oauth`, except as noted below.
>
>     Note
>
>     Beginning with version 3.13.24, the Snowflake JDBC Driver lets you send the OAuth token in the connection password
>     in addition to including it in the `token` configuration parameter. If the `token` configuration parameter is not specified,
>     the `Driver.connect()` method expects the token to be stored in the connection password.
>
>     This feature primarily supports using OAuth authentication for connection
>     pools, allowing you to pass refreshed tokens as needed instead of being restricted by an expired token specified in the
>     `token` configuration parameter.
>
>     For example, instead of setting he `token` configuration parameter, you can pass the token as the password
>     in the `getConnection()` method properties, similar to the following:
>
>     Copy code
>
>     ```
>     Properties props = new Properties();
>     props.put("user", "myusername");
>     props.put("authenticator", "oauth");
>     props.put("role", "myrole");
>     props.put("password", "xxxxxxxxxxxxx"); // where xxxxxxxxxxxxx is the token string
>     Connection myconnection = DriverManager.getConnection(url, props);
>     ```
>
> Default:
> :   None

### `oauthClientId`

> Description:
> :   Value of `client id` provided by the identity provider for Snowflake integration (Snowflake security integration metadata).

### `oauthClientSecret`

> Description:
> :   Value of the `client secret` provided by the identity provider for Snowflake integration (Snowflake security integration metadata).

### `oauthAuthorizationUrl`

> Description:
> :   Identity provider endpoint supplying the authorization code to the driver. When Snowflake is used as an identity provider, this value is derived from the `server` or `account` parameters.

### `oauthTokenRequestUrl`

> Description:
> :   Identity Provider endpoint supplying the access tokens to the driver. When using Snowflake as an Identity Provider, this value is derived from the `server` or `account` parameters.

### `oauthScope`

> Description:
> :   Scope requested in the Identity Provider authorization request. By default, it is derived from the role. When multiple scopes are required, the value should be a space-separated list of multiple scopes.

### `oauthRedirectUri`

> Description:
> :   URI to use for authorization code redirection (Snowflake security integration metadata). Default: `http://127.0.0.1:{randomAvailablePort}`.

### `workloadIdentityProvider`

> Description:
> :   Platform of the workload identity provider. Possible values include: `AWS`, `AZURE`, `GCP`, and `OIDC`.

### `workloadImpersonationPath`

> Description:
> :   String containing a list of identities separated with commas that provide an identity chain to use when connecting to Snowflake. Elements are either a full service account address or a service account’s unique ID.
>
>     Impersonation works by following each entry in order to obtain a token that allows authorization of the next service account. Each account in the identity chain needs permissions to impersonate the next account only. The final account in the list obtains your Snowflake connection token and uses it to connect to Snowflake.

## Parameters for the default database, role, schema, and warehouse

### `db`

> Description:
> :   Specifies the default database to use once connected, or specifies an empty string. The specified database should
>     be an existing database for which the specified default role has privileges.
>
>     If you need to use a different database after connecting, execute the [USE DATABASE](/sql-reference/sql/use-database) command.

### `role`

> Description:
> :   Specifies the default access control role to use in the Snowflake session initiated by the driver. The specified
>     role should be an existing role that has already been assigned to the specified user for the driver. If the specified role has
>     not already been assigned to the user, the role is not used when the session is initiated by the driver.
>
>     If you need to use a different role after connecting, execute the [USE ROLE](/sql-reference/sql/use-role) command.
>
>     For more information about roles and access control, see [Overview of Access Control](/user-guide/security-access-control-overview).

### `schema`

> Description:
> :   Specifies the default schema to use for the specified database once connected, or specifies an empty string. The
>     specified schema should be an existing schema for which the specified default role has privileges.
>
>     If you need to use a different schema after connecting, execute the [USE SCHEMA](/sql-reference/sql/use-schema) command.

### `warehouse`

> Description:
> :   Specifies the virtual warehouse to use once connected, or specifies an empty string. The specified warehouse
>     should be an existing warehouse for which the specified default role has privileges.
>
>     If you need to use a different warehouse after connecting, execute the [USE WAREHOUSE](/sql-reference/sql/use-warehouse) command can
>     be executed to set a different warehouse for the session.

## Proxy parameters

### `disableSocksProxy`

> Description:
> :   Specifies whether the driver should ignore the SOCKS proxy configuration specified in the Java system options:
>
>     - `on` (or `true`) specifies to ignore the proxy.
>     - `off` (or `false`) or any other value specifies to use the proxy.
>
>     Note
>
>     Setting this connection parameter alters the behavior for all connections on the same JVM (Java virtual machine).
>
> Default:
> :   `off`

### `nonProxyHosts`

> Description:
> :   Specifies the lists of hosts that the driver should connect to directly, bypassing the proxy server. See
>     [Specifying a proxy server in the JDBC connection string](/developer-guide/jdbc/jdbc-configure#label-java-connecting-using-a-proxy-server-using-connection-string) for details.

### `proxyHost`

> Description:
> :   Specifies the hostname of the proxy server to use. See
>     [Specifying a proxy server in the JDBC connection string](/developer-guide/jdbc/jdbc-configure#label-java-connecting-using-a-proxy-server-using-connection-string) for details.

### `proxyPassword`

> Description:
> :   Specifies the password for authenticating to the proxy server. See
>     [Specifying a proxy server in the JDBC connection string](/developer-guide/jdbc/jdbc-configure#label-java-connecting-using-a-proxy-server-using-connection-string) for details.

### `proxyPort`

> Description:
> :   Specifies the port number of the proxy server to use. See
>     [Specifying a proxy server in the JDBC connection string](/developer-guide/jdbc/jdbc-configure#label-java-connecting-using-a-proxy-server-using-connection-string) for details.

### `proxyProtocol`

> Description:
> :   Specifies the protocol used to connect to the proxy server. See
>     [Specifying a proxy server in the JDBC connection string](/developer-guide/jdbc/jdbc-configure#label-java-connecting-using-a-proxy-server-using-connection-string) for details.
>
> Default:
> :   `http`

### `proxyUser`

> Description:
> :   Specifies the user name for authenticating to the proxy server. See
>     [Specifying a proxy server in the JDBC connection string](/developer-guide/jdbc/jdbc-configure#label-java-connecting-using-a-proxy-server-using-connection-string) for details.

### `useProxy`

> Description:
> :   Specifies whether the driver should use a proxy:
>
>     - `on` (or `true`) specifies that the driver should use a proxy.
>     - `off` (or `false`) or any other value specifies that the driver should not use a proxy. This setting has no effect if JVM proxy arguments are present.
>
>     See [Specifying a proxy server in the JDBC connection string](/developer-guide/jdbc/jdbc-configure#label-java-connecting-using-a-proxy-server-using-connection-string).
>
> Default:
> :   `off`

## Timeout parameters

### `loginTimeout`

> Description:
> :   Specifies the number of seconds to wait for a response when connecting to the Snowflake service before returning a login failure error.
>
> Default:
> :   `60`

### `networkTimeout`

> Description:
> :   Specifies the number of milliseconds to wait for a response when interacting with the Snowflake service before returning an error. `0` (zero) specifies that no network timeout is set.
>
> Default:
> :   `0`

### `net.snowflake.jdbc.http_client_connection_timeout_in_ms`

> Description:
> :   Specifies the maximum time, in milliseconds, to wait on fully establishing a new connection (including TLS negotiation) with the remote host.
>
> You can also set this in the connection string with `${HTTP_CLIENT_CONNECTION_TIMEOUT}`.
>
> Default:
> :   `60000` (1 minute)

### `net.snowflake.jdbc.http_client_socket_timeout_in_ms`

> Description:
> :   Specifies the maximum time, in milliseconds, to wait for data (time of inactivity between two data packets) after a connection is successfully established.
>
> You can also set this in the connection string with `${HTTP_CLIENT_SOCKET_TIMEOUT}`.
>
> Default:
> :   `300000` (5 minutes)

### `queryTimeout`

> Description:
> :   Specifies the number of seconds to wait for a query to complete before returning an error. `0` (zero) specifies
>     that the driver should wait indefinitely.
>
> Default:
> :   `0`

## Certificate revocation list (CRL) options

These options are available in driver versions 3.27.0 and later.

### `CERT_REVOCATION_CHECK_MODE`

> Description:
> :   How to treat certificate revocation. Note that certificate revocation checks with CRLs are resource-heavy tasks, both for memory and CPU. The following values are supported:
>
>     - `ENABLED`: Enables CRLs. Connections are terminated if there are errors related to obtaining and parsing the CRL.
>     - `ADVISORY`: Enables CRLs. Errors are logged but do not block the connection; revocation status is not enforced.
>     - `DISABLED`: Disables CRLs. Certificates can only be revoked manually.
>
> Default:
> :   `DISABLED`

### `ALLOW_CERTIFICATES_WITHOUT_CRL_URL`

> Description:
> :   Whether certificates without an associated CRL are accepted. If false, certificates lacking a CRL distribution point cause the connection to fail. Applies only when `CERT_REVOCATION_CHECK_MODE` is not `DISABLED`.
>
> Default:
> :   `false`

### `ENABLE_CRL_IN_MEMORY_CACHING`

> Description:
> :   Whether to enable in-memory caching of CRLs. If enabled, the driver caches CRLs in memory to improve performance. Applies only when `CERT_REVOCATION_CHECK_MODE` is not `DISABLED`.
>
> Default:
> :   `true`

### `ENABLE_CRL_DISK_CACHING`

> Description:
> :   Whether to enable disk caching of CRLs. If enabled, the driver caches CRLs on disk to improve performance. Applies only when `CERT_REVOCATION_CHECK_MODE` is not `DISABLED`.
>
> Default:
> :   `true`

### `CRL_CACHE_VALIDITY_TIME`

> Description:
> :   Specifies the time, in seconds, that a CRL is considered valid. After this time, the CRL is refreshed from the source.
>
> Default:
> :   `86400` (1 day)

### `CRL_RESPONSE_CACHE_DIR`

> Description:
> :   Specifies the directory where the CRL response cache is stored.
>
> Default:
>
> - Windows: `%USERPROFILE%AppDataLocalSnowflakeCachescrls`
> - Linux: `$HOME/.cache/snowflake/crls`
> - macOS: `$HOME/Library/Caches/Snowflake/crls`

### `CRL_ON_DISK_CACHE_REMOVAL_DELAY`

> Description:
> :   Specifies the time, in seconds, to delay removing the on-disk cache.
>
> Default:
> :   `604800` (1 week)

## Other parameters

### `application`

> Description:
> :   Snowflake partner use only: Specifies the name of a partner application to connect through JDBC.

### `CLEAR_BATCH_ONLY_AFTER_SUCCESSFUL_EXECUTION`

> Description:
> :   Specifies whether to clear batch entries only when a batch updates successfully.
>
>     - `true`: Batch entries are cleared only when the batch updated successfully.
>     - `false`: The `Statement.executeBatch` and `Statement.executeLargeBatch` never clears batch entries after execution, while `PreparedStatement.executeBatch` and `PreparedStatement.executeLargeBatch` always clears batch entries after execution.
>
>     This parameter is available for backward compatibility.
>
> Default:
> :   `false`

### `client_config_file`

> Description:
> :   Specifies the path of a [logging configuration file](/developer-guide/jdbc/jdbc-configure#label-configuring-jdbc-logging-config) that you
>     can use to define the logging level and directory for saving log files. .. :Default: `sf_client_config.json`

### `CLIENT_TELEMETRY_ENABLED`

> Description:
> :   Specifies whether to send in-band telemetry data to Snowflake.
>
> Default:
> :   `true`.

### `CLIENT_TREAT_TIME_AS_WALL_CLOCK_TIME`

> Description:
> :   Specifies whether time values should be processed as literal wall-clock times, thereby avoiding potential discrepancies caused by timezone-sensitive epoch conversions when the parameter is `false`.
>
> : Default: `false`.

### `DIAGNOSTICS_ALLOWLIST_FILE`

> Description:
> :   Full path and filename of the JSON file containing the output of the [SYSTEM$ALLOWLIST](/sql-reference/functions/system_allowlist) or [SYSTEM$ALLOWLIST\_PRIVATELINK](/sql-reference/functions/system_allowlist_privatelink) functions.
>
>     If `ENABLE_DIAGNOSTICS` is `true`, you must provide this parameter.

### `disableOCSPChecks`

> Description:
> :   When `true`, driver does not perform any OCSP checks
>
> Default:
> :   `false`

### `ENABLE_DIAGNOSTICS`

> Description:
> :   When `true` and the calling application invokes the `DriverManager` or `DataSource` `getConnection()` method, the driver runs several connectivity tests and writes the results in a pre-configured log file. The driver also returns the following exception:
>
>     ```
>     net.snowflake.client.jdbc.SnowflakeSQLException: A connection was not created because the driver is running in diagnostics mode. If this is unintended then disable diagnostics check by removing the ENABLE_DIAGNOSTICS connection parameter
>     ```
>
>     If you enable this parameter, you must provide a value for the `DIAGNOSTICS_ALLOWLIST_FILE` parameter.
>
> Default:
> :   `false`

### `ENABLE_EXACT_SCHEMA_SEARCH_ENABLED`

> Description:
> :   Enables or disables exact schema searches in some `DatabaseMetaData` methods.
>
> Default:
> :   `false` (for backward compatibility)

### `enablePatternSearch`

> Description:
> :   Enables or disables pattern search for `getCrossReference`, `getExportedKeys`, `getImportedKeys`, and `getPrimaryKeys` metadata operations that should not use their parameters as patterns.
>
> Default:
> :   `true`

### `ENABLE_WILDCARDS_IN_SHOW_METADATA_COMMANDS`

> Description:
> :   Enables or disables treating wildcards as literals in some `DatabaseMetaData` methods when creating SQL queries. This setting can be useful when a client is not able to escape wildcards in identifiers.
>
> Default:
> :   `true`

### `enablePutGet`

> Description:
> :   Specifies whether to allow PUT and GET commands access to local file systems. Setting the value to
>     `false` disables PUT and GET command execution.
>
> Default:
> :   `true`

### `IMPLICIT_SERVER_SIDE_QUERY_TIMEOUT`

> Description:
> :   Specifies whether to send a timeout in the query sent to Snowflake.
>
>     - `true`: Calling `Statement.setQueryTimeout` sets the timeout on the query sent to Snowflake in addition to the client-side timeout.
>     - `false`: Calling `Statement.setQueryTimeout` sets only client side timeout is set.
>
> Default:
> :   `false`

### `insecureMode`

> Description:
> :   Deprecated. See [disableOCSPChecks](/developer-guide/jdbc/jdbc-parameters#label-jdbc-connection-parameters-disableocspchecks).

### `JAVA_LOGGING_CONSOLE_STD_OUT`

> Description:
> :   Specifies whether to write log message to standard output instead of standard error.
>
> Default:
> :   `false`

### `JAVA_LOGGING_CONSOLE_STD_OUT_THRESHOLD`

> Description:
> :   Specifies the maximum log message level to write to standard output. Higher log levels are written to standard error. Valid only when `JAVA_LOGGING_CONSOLE_STD_OUT` is `true`. Possible values include:
>
>     - `OFF`
>     - `SEVERE`
>     - `WARNING`
>     - `INFO`
>     - `CONFIG`
>     - `FINE`
>     - `FINER`
>     - `FINEST`
>     - `ALL`
>
> Default:
> :   none, which is equivalent to setting the value to `OFF` or `SEVERE`.

### `JDBC_ARROW_TREAT_DECIMAL_AS_INT`

> Description:
> :   Specifies whether to return all numbers in an arrow result set from a `getObject` call as integers. If this value and the JDBC\_TREAT\_DECIMAL\_AS\_INT parameter values are both `false`, all integer numbers in arrow return sets from a `getObject` call are returned as a `BigDecimal` type.
>
> Default:
> :   `true`

### `JDBC_DEFAULT_FORMAT_DATE_WITH_TIMEZONE`

> Description:
> :   Specifies whether to use the previously hardcoded value for the formatter (for backwards compatibility).
>
> Default:
> :   `true`

### `JDBC_GET_DATE_USE_NULL_TIMEZONE`

> Description:
> :   Specifies whether to use the previously null timezone value for the `getDate` method (for backwards compatibility).
>
> Default:
> :   `true`

### `JDBC_QUERY_RESULT_FORMAT`

> Description:
> :   Specifies which result format to use while fetching or processing the results of a query sent to Snowflake. Possible values include:
>
>     - `Arrow`
>     - `JSON`
>
> Default:
> :   `Arrow`

### `maxHttpRetries`

> Description:
> :   Specifies the maximum number of times to retry failed HTTP requests before returning an error.
>
> Default:
> :   7

### `net.snowflake.jdbc.max_connections`

> Description:
> :   Specifies the total maximum connections available in the connection pool.
>
> Default:
> :   `300`

### `net.snowflake.jdbc.max_connections_per_route`

> Description:
> :   Specifies the maximum number of connections allowed for a single port or URL. The value cannot
>     exceed the [net.snowflake.jdbc.max\_connections](/developer-guide/jdbc/jdbc-parameters#label-jdbc-connection-parameters-net-snowflake-jdbc-max-connections) value.
>
> Default:
> :   `300`

### `net.snowflake.jdbc.objectMapper.maxJsonStringLength`

> Description:
> :   Specifies the maximum number of bytes for a string. You can increase the value for this Java property to set a larger buffer for Snowflake response deserialization if you receive error messages similar to the following:
>
>     ```
>     com.fasterxml.jackson.core.exc.StreamConstraintsException: String length (XXXXXXX) exceeds the maximum length (180000000)
>     ```
>
> Default:
> :   `180000000`

### `ocspFailOpen`

> Description:
> :   Specifies that the driver should “fail open” if unable reach the OCSP server to verify the certificate. See
>     [OCSP](/developer-guide/jdbc/jdbc-configure#label-jdbc-ocsp-response-cache-server).

### `OWNER_ONLY_STAGE_FILE_PERMISSIONS_ENABLED`

> Description:
> :   Sets owner-only permissions (0600) on the directory created for stage files.
>
> Default:
> :   `false`

### `putGetMaxRetries`

> Description:
> :   Specifies the maximum number of times to retry PUT/GET exceptions for storage clients.
>
> Default:
> :   25

### `stringsQuotedForColumnDef`

> Description:
> :   If this parameter is set to `true`, then when `DatabaseMetaData.getColumns()` and
>     `DatabaseMetaData.getProcedureColumns()` return a value of type `String` in the COLUMN\_DEF column, that
>     value is embedded in single quotes. (If the data type of the value is not `String`, then the value is not
>     quoted, regardless of the setting of this parameter.)
>
>     - `true` specifies that string values should be embedded in single quotes (the quotes are part of the string, not
>       delimiters). This complies with the JDBC standard.
>     - `false` specifies that string values are not embedded in single quotes.
>
> Default:
> :   `false`

### `MAX_TLS_VERSION`

> Description:
> :   Specifies the maximum SSL/TLS version to use when initiating a TLS handshake. Valid values include:
>
>     - `TLSv1.2`
>     - `TLSv1.3`
>
>     Snowflake recommends leaving this setting at its default when you don’t have a specific need to change it.
>
> Default:
> :   `TLSv1.3`

### `MIN_TLS_VERSION`

> Description:
> :   Specifies the minimum SSL/TLS version to use when initiating a TLS handshake. Valid values include:
>
>     - `TLSv1.2`
>     - `TLSv1.3`
>
>     Snowflake recommends leaving this setting at its default when you don’t have a specific need to change it.
>
> Default:
> :   `TLSv1.2`

### `tracing`

> Description:
> :   Specifies the log level for the driver. The driver uses the standard Java log utility. You can set this parameter
>     to one of the following log levels:
>
>     - `OFF`
>     - `SEVERE`
>     - `WARNING`
>     - `INFO`
>     - `CONFIG`
>     - `FINE`
>     - `FINER`
>     - `FINEST`
>     - `ALL`
>
> Default:
> :   `INFO`
