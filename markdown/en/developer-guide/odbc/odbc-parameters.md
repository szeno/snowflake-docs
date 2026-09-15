# ODBC configuration and connection parameters

The Snowflake ODBC driver utilizes both configuration and connection parameters. The methods for setting the parameters are different depending on the environment in which the driver is installed.

Note

You cannot set the [SEARCH\_PATH](/sql-reference/parameters#label-search-path) parameter within an ODBC client connection string. You must
establish a session before setting a search path.

## Setting parameters in Windows

In Windows:

- [Configuration parameters](#label-odbc-configuration-parameters) are set in the Windows registry using **regedit**
  and the following registry path:

  Copy code

  ```
  [HKEY_LOCAL_MACHINE\SOFTWARE\Snowflake\Driver]
  ```
- [Connection parameters](#label-odbc-connection-parameters) are set in Data Source Names (DSNs):

  - DSNs are typically created and edited using the Windows **Data Source Administration** tool.
  - If you wish, the registry keys for DSNs can be edited directly in the Windows registry using **regedit**. The registry path to the keys is different depending on whether you’re using 64-bit and
    32-bit Windows and whether you’re editing a user or system DSN:

    - 64-bit Windows:

      Copy code

      ```
      [HKEY_CURRENT_USER\SOFTWARE\ODBC\ODBC.INI\<DSN_NAME>]

      [HKEY_LOCAL_MACHINE\SOFTWARE\ODBC\ODBC.INI\<DSN_NAME>]
      ```
    - 32-bit Windows:

      Copy code

      ```
      [HKEY_CURRENT_USER\SOFTWARE\WOW6432NODE\ODBC\ODBC.INI\<DSN_NAME>]

      [HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432NODE\ODBC\ODBC.INI\<DSN_NAME>]
      ```

    To add a connection parameter using **regedit**, add a new **String Value**, double-click on the value you created, then enter the ODBC parameter as the **Value name** and the parameter value
    as the **Value data**.

## Setting parameters in macOS or Linux

In macOS or Linux:

- [Configuration parameters](#label-odbc-configuration-parameters) are set in the configuration file
  (`simba.snowflake.ini`).
- [Connection parameters](#label-odbc-connection-parameters) are set in the data source name (DSN) file (`odbc.ini`).

## Configuration parameters

`CABundleFile`
:   Set the location of the Certificate Authority (CA) bundle file. Must reference a file that includes a valid list of CA certificates.

    For Linux, the RPM and DEB installers automatically copy the file and set this parameter.

    For Mac, the PKG installer copies the file and sets this parameter.

    For Windows, the MSI installer copies the file and sets this parameter.

    A manual installation requires you to download the file from <https://curl.haxx.se/docs/caextract.html> and set the location of the file.

`client_config_file`
:   Specifies the path of a [logging configuration file](#label-configuring-odbc-logging-config) that you can use to define the logging level and directory for saving log files.

`CURLVerboseMode`
:   Set to `true` to enable cURL verbose logging. The log file `snowflake_odbc_curl.dmp` is created and updated. The Snowflake ODBC driver uses cURL as the HTTP and TLS library. This parameter
    is useful for diagnosing network issues.

`DisableOCSPCheck`
:   Set to `true` to disable the TLS certificate revocation status check by the Online Certificate Status Protocol (OCSP). In normal circumstances, this flag should not set. But if the OCSP
    availability problem persists, the application might temporarily set this parameter in order to unblock connectivity issues and remove it when the OCSP availability problem is addressed.

`DisableTelemetry`
:   Specifies whether toggling the in-band telemetry handler is enabled or not. If this driver configuration setting is set to `true`, the telemetry handler is not created in the driver.

`DriverManagerOverride`
:   By default, the driver auto-detects which driver manager to use. However, if your specific situation calls for it, starting from ODBC driver version 3.9.0, you can override this auto-detection and manually specify which driver manager to use.

    Possible values are: UnixODBC and iODBC.

    If `DriverManagerOverride` is not specified, the driver uses auto-detection for the driver manage (call backtrace()) to get driver manager information. This is the default behavior.

    The parameter works only on Linux and MacOS.

`EnableAutoIpdByDefault`
:   Set to `false` to configure the ODBC Driver to set SQL\_ATTR\_ENABLE\_AUTO\_IPD to `false` (which is the default value in the
    ODBC standard).

    Otherwise, by default, the ODBC Driver sets SQL\_ATTR\_ENABLE\_AUTO\_IPD to true for compatibility with third-party tools.

    This parameter was introduced in version 2.22.0 of the ODBC Driver.

`EnablePidLogFileNames`
:   Set to `true` to include the process ID in the name of the log file. For example, if the process ID is 7394, the log files
    will be named:

    - `snowflake_odbc_connection_7394_0.log`
    - `snowflake_odbc_generic7394_0.log`
    - `snowflake_odbc_curl_7394.dmp`

    You can set this parameter to prevent different processes from overwriting the same log files. Each process will generate its
    own set of log files.

    By default, the value of this parameter is `false`.

    This parameter was introduced in version 2.22.2 of the ODBC Driver.

`get_size_threshold`
:   Specifies the minimum file size, in megabytes (MB), to break files into smaller parts when downloading files with the [GET](/sql-reference/sql/get) command.
    Files with sizes smaller than this threshold will not use multi-part downloading.

    Default is **5** (MB).

    Note

    You can override this value for specific cases by setting the corresponding [get\_size\_threshold](/developer-guide/odbc/odbc-parameters#label-odbc-additional-connection-parameters-get-size-threshold) connection parameter.

`KeepLeadingTrailingZeros`
:   Determines how leading or trailing zeros in numbers formatted as string values are handled. By default, the parameter is set to `true`,
    which means the driver retains any leading or trailing zeros. Set the parameter to `false` to remove leading or trailing zeros, for example:

    - `0.23` is changed to `.23`
    - `7.00` is changed to `7`

`LogFileCount`
:   Sets the maximum number of log files to keep before rotating older files to make room for new log files.

`LogFileSize`
:   Specifies the maximum size, in bytes, of a log file. When a log file reaches the specified size,
    the ODBC driver automatically creates a new log file.

    Default is **20971520**.

`LogLevel`
:   Specifies the level of detail logged for clients that use the ODBC driver:

    - 0 = Off
    - 1 = Fatal
    - 2 = Error
    - 3 = Warning
    - 4 = Info
    - 5 = Debug
    - 6 = Trace

`LogPath`
:   Specifies the location of the Snowflake log files for clients that use the ODBC
    driver.

`MapToLongVarchar`
:   Specifies the length of a string at which to begin mapping string values to an ODBC `SQL_LONGVARCHAR` data type
    instead of the default ODBC `SQL_CHAR` or `SQL_VARCHAR` data types.

    - < 0 (or unset): Maps string values in their default ODBC data types. Default = **-1**.
    - >= 0: Specifies the maximum number of string characters to map to default ODBC string data types.
      All strings larger than this value are mapped to `SQL_LONGVARCHAR`.

    You can also specify this parameter as a connection parameter. (See the instructions for setting the
    parameters [in Windows](#label-odbc-setting-parameters-windows),
    [macOS and Linux](#label-odbc-setting-parameters-macos-linux).)
    If set both as a connection parameter and
    a configuration parameter, the connection parameter in the DSN (or connection string) takes precedence.

    This parameter was introduced in version 2.24.3 of the ODBC Driver.

`NoExecuteInSQLPrepare`
:   Set to `true` to configure the ODBC Driver to use the standard ODBC behavior when passing DDL statements (such as
    CREATE and DROP) to `SQLPrepare()` and `SQLExecute()`.

    In Snowflake, by default, when you pass a DDL statement to `SQLPrepare()`, the ODBC Driver sends the statement to the
    data source for execution (not preparation). When you pass a DDL statement to `SQLExecute()`, the ODBC Driver does not
    send the statement to the data source.

    If you set `NoExecuteInSQLPrepare` to `true`, the ODBC Driver follows the standard ODBC behavior. Calling
    `SQLPrepare()` sends the statement to the data source for preparation (not execution). Calling `SQLExecute()`
    sends the statement to the data source for execution.

    This parameter was introduced in version 2.21.6 of the ODBC Driver.

`NoProxy`
:   Specifies the hostname patterns to bypass the proxy server (e.g. `.amazonaws.com` to bypass Amazon S3 access).

    Note

    The Snowflake ODBC driver passes the `NoProxy` value to the curl option `CURLOPT_NOPROXY`.

    The format of the `NoProxy` value can be found [CURLOPT\_NOPROXY explained”](https://curl.haxx.se/libcurl/c/CURLOPT_NOPROXY.html).

`Proxy`
:   Specifies a proxy server in the form of `<host>:<port>` for clients that use the ODBC driver.

    Note

    In Windows, entries for `LogLevel` and `LogPath` are created and populated with default values when the ODBC
    driver is installed; however, an entry for `Proxy` is not created during install. To specify a proxy to use with the driver,
    you must manually add the entry to the driver registry key.

    To bypass the proxy for one or more IP addresses or URLs, add the [NoProxy](/developer-guide/odbc/odbc-parameters#label-odbc-configuration-parameters-noproxy) parameter.

`SSLVersion`
:   Specifies the minimum SSL/TLS version to use when initiating TLS handshake. The values correspond to libcurl’s capabilities. For more information, see `CURL_SSLVERSION_*` entries in [CURLOPT\_SSLVERSION explained](https://curl.se/libcurl/c/CURLOPT_SSLVERSION.html).

    Possible values: one of TLSv1, SSLv2, SSLv3, TLSv1\_0, TLSv1\_1, TLSv1\_2, TLSv1\_3 (default: TLSv1\_2).

    Snowflake recommends leaving this setting at its default when you don’t have a very specific need to change it.

`SSLVersionMax`
:   Specifies the maximum SSL/TLS version to use when initiating TLS handshake. The values correspond to libcurl’s capabilities. For more information, see `CURL_SSLVERSION_MAX_*` entries in [CURLOPT\_SSLVERSION explained](https://curl.se/libcurl/c/CURLOPT_SSLVERSION.html).

    Possible values: one of TLSv1\_0, TLSv1\_1, TLSv1\_2, TLSv1\_3 (default: TLSv1\_3).

    Snowflake recommends leaving this setting at its default when you don’t have a very specific need to change it.

## Connection parameters

Important

Beginning with Snowflake version 8.24, network administrators have the option to require multi-factor authentication (MFA) for all connections to Snowflake. If your administrator decides to enable this feature, you must configure your client or driver to use MFA when connecting to Snowflake. For more information, see the following resources:

- [8.24 release notes](/release-notes/2024/8_24#label-authentication-policies-new-multi-factor-authentication-parameters)
- [Multi-factor authentication (MFA)](/user-guide/security-mfa)
- [Troubleshooting service users authentication issues with Snowflake MFA](https://community.snowflake.com/s/article/Troubleshooting-service-users-authentication-issues-with-Snowflake-MFA) Knowledge Base article

### Required connection parameters

`<name>` (Data Source)
:   Specifies the name of your DSN.

`port` (Port)
:   Specifies the port on which the driver listens for Snowflake communication.

    Note

    You do not need to change the default `Port` value of `443`.

`pwd` (Password)
:   A password is required to connect to Snowflake; however, for security and authentication reasons, Snowflake strongly discourages storing password credentials directly within any DSN definition.

    Typically, the credentials are passed to the driver programmatically by the client application that is attempting to connect to Snowflake.

    Note

    In Windows, the ODBC driver displays a **Password** field in the **Data Source Administration** tool; however, the driver does not store any values entered in the field. Instead, the driver
    requires login credentials to be provided at connection time.

`server` (Server)
:   Specifies the *hostname* for your account in the following format:

    `account_identifier.snowflakecomputing.com`

    To determine the account identifier to use, see [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).

`uid` (User)
:   Specifies the login name of the Snowflake user to authenticate.

### Optional connection parameters

`BROWSER_RESPONSE_TIMEOUT`
:   Specifies the number of seconds to wait for an authentication response in an external browser.

    Default is 120.

`CLIENT_OUT_OF_BAND_TELEMETRY_ENABLED=<Boolean>`
:   Specifies whether to enable out-of-band telemetry.

    Default is `true`

`CLIENT_SESSION_KEEP_ALIVE=<Boolean>`
:   Specifies whether to keep the current session active after a period of inactivity or to force the user to log in again.
    If the value is `true`, Snowflake keeps the session active indefinitely,
    even if there is no activity from the user. If the value is `false`, the user must log in again after four hours of inactivity.

    Default is `false`.

`CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY`
:   Specifies the number of seconds between heartbeats sent by the driver to keep the session alive when [CLIENT\_SESSION\_KEEP\_ALIVE](/developer-guide/odbc/odbc-parameters#label-odbc-keep-alive) is `true`. For more information, see [CLIENT\_SESSION\_KEEP\_ALIVE\_HEARTBEAT\_FREQUENCY](/sql-reference/parameters#label-client-session-keep-alive-heartbeat-frequency).

    Valid values are integers between `900` and `3600`.

    Default is `3600`.

`database` (Database)
:   Specifies the default database to use for sessions initiated by the driver.

`disableSamlUrlCheck`
:   Specifies whether to disable verification for SAML URLs. By default, the driver verifies SAML URLs.

    Default is `false`.

`maxHttpRetries` (Database)
:   Specifies the maximum number of HTTP retries for queries with failed HTTP requests before returning an error. Setting `maxHttpRetries=0` removes the retry limit, but doing so runs the risk of the driver infinitely retrying failed HTTP calls.

    Default value is 7.

`role` (Role)
:   Specifies the default role to use for sessions initiated by the driver. The specified role should be a role that has been assigned to the specified user for the driver. If the specified role does not
    match any of the roles assigned to the user, sessions initiated by the driver have no role initially; however, a role can always be specified from within the session.

`schema` (Schema)
:   Specifies the default schema to use for sessions initiated by the driver.

    Default is `public`.

`SecondaryRoles` (Role)
:   Specifies the secondary roles to use for sessions initiated by the driver.
    The roles must already be granted to the specified user for the driver.
    Secondary roles can also be activated from within a user session using the `USE SECONDARY ROLES` command.

    Possible values include:

    - **All**: All roles granted to the user.
    - **None**: No roles allowed (disables secondary roles).

`token_file_path` (Token File Path)
:   Specifies the path to the file that contains the SPCS token to use when logging in to an SPCS container.

`tracing` (Tracing)
:   The level of detail to be logged in the driver trace files:

    - 0 = Disable tracing
    - 1 = Fatal only error tracing
    - 2 = Error tracing
    - 3 = Warning tracing
    - 4 = Info tracing
    - 5 = Debug tracing
    - 6 = Detailed tracing

`warehouse` (Warehouse)
:   Specifies the default warehouse to use for sessions initiated by the driver.

### Certificate revocation list (CRL) options

These options are available in driver versions 3.13.0 and later.

`CRL_CHECK`
:   Specifies whether to enable or disable CRL checking. When set to `true`, the driver checks the CRL to verify the server certificate has not been revoked. The connection fails if the server’s certificate is revoked or another revocation check issue (such as downloading or parsing) occurs.

    Default is `false`.

`CRL_ADVISORY`
:   Modifies the CRL connection checking to fail only when the certificate is revoked explicitly. When any other problem (such as parsing errors or download errors) is present, the connection is allowed.

    Default is `false`.

`CRL_ALLOW_NO_CRL`
:   Specifies whether to allow connections when no CRL is found. When set to `true`, the driver allows connections when no CRL is found.

    Default is `false`.

`CRL_DISK_CACHING`
:   Specifies whether to enable or disable disk caching of CRLs. When set to `true`, the driver caches CRLs on disk, which reduces the time spent re-downloading the certificate distribution lists.

    The driver stores the cached CRLs in the following directories:

    - MacOS: `$HOME/Library/Caches/Snowflake/crls`
    - Linux: `$HOME/.cache/snowflake/crls`
    - Windows: `%LOCALAPPDATA%SnowflakeCachescrls`

    Default is `true`.

    You can override the default disk cache location by setting the `SF_CRL_RESPONSE_CACHE_DIR` environment variable.

`CRL_MEMORY_CACHING`
:   Specifies whether to enable or disable memory caching of CRLs. When set to `true`, the driver caches CRLs in memory.

    Default is `true`.

`CRL_DOWNLOAD_TIMEOUT`
:   Specifies the timeout, in seconds, for downloading CRLs. If the download does not complete within the specified time, the connection fails.

    Default is **120** (seconds).

The driver also supports the following environment variables for CRL caching in long-lived processes. They apply to different parts of the cache and don’t override each other.

`SF_CRL_CACHE_CLEANUP_INTERVAL`
:   Time, in seconds, between runs of the background thread that removes stale CRLs from the in-memory and on-disk caches. Default is **3600** (1 hour). Set to **0** to disable cleanup.

`SF_CRL_CACHE_VALIDITY_TIME`
:   Time, in seconds, that a CRL remains valid in the in-memory cache after it is downloaded. After this interval, or sooner if the CRL itself has expired, the next cleanup run evicts it from memory. Default is **86400** (1 day). This value doesn’t control how long the on-disk file is kept.

`SF_CRL_ON_DISK_CACHE_REMOVAL_DELAY`
:   Time, in seconds, after a CRL’s next-update time before the on-disk cache file is deleted. Default is **604800** (1 week). Because this delay is measured from the CRL expiration, not from download time, an on-disk file can outlive the in-memory validity window. After memory eviction, the driver can still reload the CRL from disk until this delay elapses.

### Additional connection parameters

Note

In Windows, these additional connection parameters can be set in the Windows Registry (by using **regedit**).

In macOS or Linux, they are set in the `odbc.ini` file, similar to the rest of the connection parameters.

`allowEmptyProxy`
:   Specifies whether to allow empty values for the [proxy](/developer-guide/odbc/odbc-parameters#label-odbc-additional-connection-parameters-proxy)
    and [no\_proxy](/developer-guide/odbc/odbc-parameters#label-odbc-additional-connection-parameters-no-proxy) connection parameters, as described in the following sections:

    - [Using connection parameters](#using-connection-parameters)
    - [Using configuration parameters](#using-configuration-parameters)
    - [Using environment variables](#using-environment-variables)

    Setting this value produces the following effects:

    > - `true`: The driver treats empty proxy values as valid proxy settings and overrides any existing settings or environment variable.
    > - `false`: The driver ignores empty proxy values and uses the specified configuration parameters or environment variable.

    Default is `true`.

`application`
:   Snowflake partner use only: Specifies the name of a partner application to connect through ODBC.

    This parameter can also be set by calling the `SQLSetConnectAttr()` function. For more details, see
    [Snowflake-specific behavior of the SQLSetConnectAttr function](/developer-guide/odbc/odbc-api#label-odbc-api-sqlsetconnectattr-specific-behavior).

`authenticator`
:   Specifies the authenticator to use for verifying user login credentials:

    > - `snowflake` (Default) to use the internal Snowflake authenticator.
    > - `externalbrowser` to [use your web browser](/user-guide/admin-security-fed-auth-use#label-browser-based-sso) to authenticate with Okta, AD FS, or any other
    >   SAML 2.0-compliant identity provider (IdP) that has been defined for your account.
    >
    >   Note
    >
    >   The Snowflake ODBC driver does not support `externalbrowser` authentication using Microsoft Excel with MacOS.
    > - `https://<okta_account_name>.okta.com` (i.e. the URL endpoint for your Okta account) to [authenticate through native Okta](/user-guide/admin-security-fed-auth-use#label-native-sso-okta) (only supported if your IdP is Okta).
    > - `oauth` to authenticate using OAuth. When OAuth is specified as the authenticator, you must also set the `token` parameter to specify the OAuth token ([see below](/developer-guide/odbc/odbc-parameters#label-odbc-additional-connection-parameters-token)).
    > - `username_password_mfa` to authenticate with MFA token caching. For more details, see [Using Multi-Factor Authentication](#using-multi-factor-authentication) (in this topic).
    > - `oauth_authorization_code` Manually authenticate using an OAuth authorization code with your web browser and a chosen identity provider (including Snowflake as an IdP). For more information, see [Using the OAuth 2.0 Authorization Code flow](#label-odbc-oauth-code-flow).
    > - `oauth_client_credentials` Automatically authenticate using OAuth client credentials with your chosen identity provider (Snowflake as an IdP doesn’t support the client credentials flow). For more information, see [Using the OAuth 2.0 Client Credentials flow](#label-odbc-oauth-client-flow).
    > - `programmatic_access_token` to authenticate with a programmatic access token (PAT).
    > - `workload_identity` to authenticate with the [workload identity federation (WIF)](/user-guide/workload-identity-federation) authenticator.

    Default is `snowflake`.

    On Windows, you can use the [ODBC Data Source Administration Tool](/developer-guide/odbc/odbc-windows#label-odbc-windows-configure-dsn) to set this parameter.

    For more information on authentication, see [Managing/Using federated authentication](/user-guide/admin-security-fed-auth-use) and [Clients, drivers, and connectors](/user-guide/oauth-intro#label-oauth-intro-clients-drivers-conns).

`singleAuthenticationPrompt`
:   Specifies whether to prompt for authentication when a single authentication is required. When enabled, concurrent connections wait for the initial authentication process to complete and reuse the retrieved token instead of prompting for authentication again.

    Default: `true`.

`disablePlatformDetection`
:   Specifies whether to disable cloud platform detection performed by the driver during the login flow. Platform detection identifies the cloud environment (for example, AWS, Azure, or GCP) where the client is running and reports it as part of the connection telemetry.

    Default: `false`.

`platformDetectionTimeoutMs`
:   Specifies the timeout, in milliseconds, for the cloud platform detection probes performed during the login flow.

    Default: `200`.

`LOG_QUERY_TEXT`
:   Specifies whether to include the SQL query text in the driver debug logs. This option is intended for diagnostic purposes only.

    Warning

    Enabling this option causes query text to be written to the driver log files. Only enable it when needed for troubleshooting and ensure the log files are stored securely.

    Default: `false`.

`LOG_QUERY_PARAMETERS`
:   Specifies whether to include bind parameter values in the driver debug logs. This option is intended for diagnostic purposes only.

    Warning

    Enabling this option causes bind parameter values to be written to the driver log files. Only enable it when needed for troubleshooting and ensure the log files are stored securely.

    Default: `false`.

`default_binary_size`, `default_varchar_size`
:   Specifies the default size, in bytes, that the driver uses when retrieving and converting values from BINARY or VARCHAR columns of
    undetermined sizes. Set this when retrieving values from these types of columns.

    By default, the driver uses `67108864` (for BINARY columns) and `134217728` (for VARCHAR columns) as the default sizes when
    allocating memory for retrieving the value of a column of undetermined size.

    To reduce the amount of memory allocated for these values, you can set `default_binary_size` and
    `default_varchar_size` to the maximum size of the values in these types of columns.

    Note

    Setting these values only changes the `SQL_DESC_LENGTH` field in Implementation Row Descriptor (IRD) and the
    corresponding values returned from `SQLDescribeCol/SQLColAttribute/SQLColAttributes`. The driver still returns the
    entire data even when it’s length exceeds the setting.

    However, an application could allocate a data buffer based on the length
    specified in these parameters that could truncate the data because of insufficient space in the buffer. As the best practice,
    Snowflake recommends setting the default size larger than the maximum size of the typical data (for example, 4000 or 8000 bytes)
    to reduce the memory usage significantly from the original default values of 134217728/67108864 bytes and to minimize
    the chance of data truncation.

    You can also use these settings to avoid the following error, which can occur when using the Microsoft OLE DB
    provider (MSDASQL) with a Snowflake database:

    Copy code

    ```
    Requested conversion is not supported
    Cannot get the current row value of column
    ```

    You can specify these parameters as connection
    [configuration parameters](#label-odbc-setting-parameters-windows) (for example, in the `simba.snowflake.ini` on
    [macOS and Linux](#label-odbc-setting-parameters-macos-linux)). If this is set as both a connection parameter and
    a configuration parameter, the connection parameter in the DSN (or connection string) takes precedence.

    These parameters were introduced in version 2.23.2 of the ODBC Driver.

`get_size_threshold`
:   Specifies the minimum file size, in megabytes (MB), to break files into smaller parts when downloading files with the [GET](/sql-reference/sql/get) command.
    Files with sizes smaller than this threshold will not use multi-part downloading.

    Default is **5** (MB).

    Note

    Setting this value as a connection parameter overrides the value of the corresponding [get\_size\_threshold](/developer-guide/odbc/odbc-parameters#label-odbc-additional-configuration-parameters-get-size-threshold) configuration parameter.

`login_timeout`
:   Specifies how long, in seconds, to wait for a response when connecting to the Snowflake service before returning a login failure error.

    Default is **300** (seconds).

`network_timeout`
:   Specifies how long, in seconds, to wait for a response when interacting with the Snowflake service before returning an error. Zero (0) indicates no network timeout is set.

    Default is **0** (seconds).

`retryTimeout`
:   Specifies how long, in seconds, to wait before returning an error for HTTP retries from queries with failed HTTP requests. Zero (0) indicates no retry timeout is set.

    Default is **300** (seconds).

`no_proxy`
:   Specifies which hostname endings should be allowed to bypass the proxy server (e.g. `no_proxy=.amazonaws.com` means that Amazon S3 access does not need to go through the proxy).

    This parameter does not support wildcards. Each value specified should be one of the following:

    - The end of a hostname (or a complete hostname), for example:

      - .amazonaws.com
      - myorganization-myaccount.snowflakecomputing.com
    - An IP address, for example:

      - 192.196.1.15

    If more than one value is specified, values should be separated by commas, for example:

    Copy code

    ```
    no_proxy=localhost,.example.com,myorganization-myaccount.snowflakecomputing.com,192.168.1.15,192.168.1.16
    ```

    Note

    This parameter is applied to the process. If another connection shares the same process, the proxy setting must be identical or the behavior is not predictable.

`odbc_use_standard_timestamp_columnsize`
:   This boolean parameter affects the column size (in characters) returned for SQL\_TYPE\_TIMESTAMP.
    When this parameter is set to true, the driver returns 29, following the ODBC standard. When this parameter is set
    to `false`, the driver returns 35, which allows room for the timezone offset (e.g. “-08:00”).

    This value can be set via not only the odbc.ini file (Linux or macOS) or the Microsoft Windows registry, but also
    the connection string.

    Default is `false`.

`passcode`
:   Specifies the passcode to use for multi-factor authentication.

    For more information about multi-factor authentication, see [Multi-factor authentication (MFA)](/user-guide/security-mfa).

`passcodeInPassword`
:   Specifies whether the passcode for multi-factor authentication is appended to the password:

    - `on` (or `true`) specifies the passcode is appended.
    - `off` (or `false`) or any other value specifies the passcode is not appended.

    The default value is `off`.

`proxy`
:   Specifies the proxy server URL in the format `http://<hostname>:<port>/` or `<hostname>:<port_number>` so that all communications from ODBC use the proxy server.

    Note

    This parameter is applied to the process. If another connection shares the same process, the proxy setting must be identical or the behavior is not predictable.

`put_compresslv`
:   Specifies the compression rate the ODBC driver uses when transferring data with the [PUT](/sql-reference/sql/put) command. This parameter overrides the default gzip
    compression level. If you do not specify `put_compresslv` the ODBC driver uses the default
    compression level.

    Valid values are `-1` to `9`. The default value is `-1` and specifies the default
    `Z_DEFAULT_COMPRESSION`.

    Values `0` through `9` specify a custom compression rate. `0` causes the ODBC driver to use a lower
    compression rate and `9` uses a higher compression rate. Using a higher compression rate results in slower data
    transfer speeds.

    You can also specify this parameter as a
    [configuration parameter](#label-odbc-setting-parameters-windows) (for example, in the `simba.snowflake.ini` on
    [macOS and Linux](#label-odbc-setting-parameters-macos-linux)). If this is set as both a connection parameter and
    a configuration parameter, the connection parameter in the DSN (or connection string) takes precedence.

    This parameter was introduced in version 2.23.3 of the ODBC Driver.

`put_fastfail`
:   If you are using wildcard characters with the [PUT](/sql-reference/sql/put) command to upload multiple files at once and you
    want the driver to stop uploading the files when an error occurs, set this parameter to `true`.

    The default value is `false`, which means that if an error occurs with one file, the driver continues uploading the rest
    of the files.

    This parameter was introduced in version 2.22.3 of the ODBC Driver.

    As of version 2.22.5 of the ODBC Driver, you can also specify this parameter as a
    [configuration parameter](#label-odbc-setting-parameters-windows) (for example, in the `simba.snowflake.ini` on
    [macOS and Linux](#label-odbc-setting-parameters-macos-linux)). If this is set as both a connection parameter and
    a configuration parameter, the connection parameter in the DSN (or connection string) takes precedence.

`put_maxretries`
:   Specifies the number of times that the driver should retry the [PUT](/sql-reference/sql/put) command if the command fails.

    The default value is **5**.

    The valid range of values for this parameter is `0` to `100`. If you specify a value outside this range, the driver
    uses the default value of `5`.

    This parameter was introduced in version 2.22.3 of the ODBC Driver.

    As of version 2.22.5 of the ODBC Driver, you can also specify this parameter as a
    [configuration parameter](#label-odbc-setting-parameters-windows) (for example, in the `simba.snowflake.ini` on
    [macOS and Linux](#label-odbc-setting-parameters-macos-linux)). If this is set as both a connection parameter and
    a configuration parameter, the connection parameter in the DSN (or connection string) takes precedence.

`put_tempdir`
:   Specifies the temporary directory to use for [PUT](/sql-reference/sql/put) command requests. The driver uses this temporary
    directory to create temporary compressed files before uploading those files to Snowflake.

    If this parameter is not set, the driver creates and uses the temporary directory `/tmp/snowflakeTmp_username`, where
    `username` is the username of the current user in the operating system.

    You can also specify this parameter as a
    [configuration parameter](#label-odbc-setting-parameters-windows) (for example, in the `simba.snowflake.ini` on
    [macOS and Linux](#label-odbc-setting-parameters-macos-linux)). If this is set as both a connection parameter and
    a configuration parameter, the connection parameter in the DSN (or connection string) takes precedence.

    This parameter was introduced in version 2.23.1 of the ODBC Driver.

`token=<string>`
:   Specifies the token for OAuth or PAT authentication, where `<string>` is the token. This parameter is required only when the `authenticator=oauth` or `authenticator=programmatic_access_token` parameter is set.

    Default is none.

`query_timeout`
:   Specifies how long, in seconds, to wait for a query to complete before returning an error. Zero (0) indicates to wait indefinitely.

    Default is **0** (seconds).

`validateSessionParam`
:   Specifies how to respond when any of the following
    [session connection parameters](#label-odbc-optional-connection-parameters) are invalid:

`enable_connection_diag`
:   Specifies whether the connector generates a connectivity diagnostic report.

    Default is `false`.

`connection_diag_log_path`
:   Specifies the absolute path where the connectivity report is stored.

    Valid only when `enable_connection_diag` is `true`.

    Example: `connection_diag_log_path=C:\\reports`

`connection_diag_allowlist_path`
:   Specifies the absolute path to a JSON file containing the output of `SYSTEM$ALLOWLIST()`
    or `SYSTEM$ALLOWLIST_PRIVATELINK()`.

    Valid only when `enable_connection_diag` is `true`.

    Example: `connection_diag_log_path=C:\\allowlist.json`

`OAUTH_CLIENT_ID`
:   Value of the `client id` provided by the identity provider for Snowflake integration (Snowflake security integration metadata).

    Default: `LOCAL_APPLICATION`.

`OAUTH_CLIENT_SECRET`
:   Value of the `client secret` provided by the identity provider for Snowflake integration (Snowflake security integration metadata).

    Default: `LOCAL_APPLICATION`.

`OAUTH_AUTHORIZATION_URL`
:   Identity provider endpoint supplying the authorization code to the driver. When Snowflake is used as an identity provider, this value is derived from the `server` or `account` parameters.

`OAUTH_TOKEN_REQUEST_URL`
:   Identity provider endpoint supplying the access tokens to the driver. When using Snowflake as an identity provider, this value is derived from the `server` or `account` parameters.

`OAUTH_SCOPE`
:   Scope requested in the identity provider authorization request. By default, it is derived from the role. When multiple scopes are required, the value should be a space-separated list of multiple scopes.

`OAUTH_REDIRECT_URI`
:   URI to use for authorization code redirection (Snowflake security integration metadata). Default: `http://127.0.0.1:{randomAvailablePort}`.

`WORKLOAD_IDENTITY_PROVIDER`
:   Platform of the workload identity provider. Possible values include: `AWS`, `AZURE`, `GCP`, and `OIDC`.

`WORKLOAD_IDENTITY_IMPERSONATION_PATH`
:   An array of strings that provides an identity chain to use when connecting to Snowflake. Array elements are either a full service account address or a service account’s unique ID.

    Impersonation works by following each array entry to obtain a token that allows authorization of the next service account. Each account in the identity chain needs permissions to impersonate the next account only. The final account in the list obtains your Snowflake connection token and is used to connect to Snowflake.

    This argument is supported for AWS and Google Cloud workloads and only applies when `authenticator=WORKLOAD_IDENTITY`.

`wif_host`
:   Overrides the STS/IAM endpoint used for Workload Identity Federation. You can specify either a bare hostname (for example, `sts.us-gov-east-1.amazonaws.com`) or a full base URL (for example, `https://iamcredentials.privategoogleapis.com/v1`). The driver normalizes the value to the format required by the configured provider. This parameter only applies when `authenticator=WORKLOAD_IDENTITY`.

`PRIV_KEY_BASE64`
:   Base64-encoded private key.

`PRIV_KEY_PWD`
:   Base64-encoded private key password.

## Connecting using the `connections.toml` file

The ODBC driver lets you add connection definitions to a `connections.toml` configuration file.
A connection definition refers to a collection of connection-related parameters. The driver currently supports TOML version 1.0.0.

For more information about `toml` file formats, see [TOML (Tom’s Obvious Minimal Language)](https://toml.io/en/).

The connection string containing only the `Driver` parameter tells the driver to look for the connection configuration within the predefined (default) files.
The ODBC driver looks for the `connections.toml` file in the following locations, in order:

- The location specified by the `SNOWFLAKE_HOME` environment variable.
- The `~/.snowflake/connections.toml` file, if the `~/.snowflake` directory exists.

You can generate the basic settings for the TOML configuration file in Snowsight. For information, see
[Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).

If you want to switch between multiple existing connections, you can configure them in the `connections.toml` file. The default key is `default`, but you change the name of the default connection by setting the `SNOWFLAKE_DEFAULT_CONNECTION_NAME` shell environment variable.

The following sample `connections.toml` files defines two connections:

Copy code

```
[default]
account = 'my_organization-my_account'
user = 'test_user'
password = '******'
warehouse = 'testw'
database = 'test_db'
schema = 'test_odbc'
protocol = 'https'
port = '443'

[aws-oauth-file]
account = 'my_organization-my_account'
user = 'test_user'
password = '******'
warehouse = 'testw'
database = 'test_db'
schema = 'test_odbc'
protocol = 'https'
port = '443'
authenticator = 'oauth'
token_file_path = '/Users/test/.snowflake/token'
```

## Specifying parameters in a connection string

You can specify [connection parameters](#label-odbc-connection-parameters) as name-value pairs in a connection string, using
an equals sign (`=`) between each parameter and value, and using a semicolon (`;`) between parameters. For example:

Copy code

```
driver={SnowflakeDSIIDriver};server=myorganization-myaccount.snowflakecomputing.com;uid=myloginname;pwd=mypassword;database=mydatabase;schema=myschema;warehouse=mywarehouse;role=myrole;...
```

You can generate the basic connection string in Snowsight. For information, see [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).

## Verifying the network connection to Snowflake with SnowCD

After configuring your driver, you can evaluate and troubleshoot your network connectivity to Snowflake using [SnowCD](/user-guide/snowcd).

You can use SnowCD during the initial configuration process and on-demand at any time to evaluate and troubleshoot your network connection to Snowflake.

## Connecting through a proxy server

The instructions for configuring a proxy server connection depend on your operating system and driver version:

| Operating System | Driver Version | Supported Instructions |
| --- | --- | --- |
| Linux | 2.16.0 (released May 3, 2018) or higher | - [Using Connection Parameters](#using-connection-parameters) - [Using Environment Variables](#using-environment-variables) |
| 2.13.18 (released February 7, 2018) - 2.15.0 (released April 30, 2018) | [Using Environment Variables](#using-environment-variables) |  |
| 2.13.17 or lower | [Using Configuration Parameters](#using-configuration-parameters) |  |
| macOS | 2.16.0 (released May 3, 2018) or higher | - [Using Connection Parameters](#using-connection-parameters) - [Using Environment Variables](#using-environment-variables) |
| 2.14.0 (released March 28, 2018) - 2.15.0 (released April 30, 2018) | [Using Environment Variables](#using-environment-variables) |  |
| 2.13.21 or lower | [Using Configuration Parameters](#using-configuration-parameters) |  |
| Windows | 2.16.0 (released May 3, 2018) or higher | - [Using Connection Parameters](#using-connection-parameters) - [Using Environment Variables](#using-environment-variables) |
| 2.15.0 (released April 30, 2018) | [Using Environment Variables](#using-environment-variables) |  |
| 2.14.0 or lower | [Using Configuration Parameters](#using-configuration-parameters) |  |

Expand

Show lessSee more

Note

The latest versions of ODBC driver, indicated above, support any of the listed configuration options. The options are listed
in the order of precedence. If more than one option is defined, the setting with the highest precedence is applied.

### Using connection parameters

To connect through a proxy server, add the following connection parameters to the DSN:

- `proxy`
- `no_proxy`

For example:

> Copy code
>
> ```
> [connection]
> Description = SnowflakeDB
> Driver      = SnowflakeDSIIDriver
> Locale      = en-US
> server      = myorganization-myaccount.snowflakecomputing.com
> proxy       = http://proxyserver.company:80
> no_proxy    = .amazonaws.com
> ```

See [Connection Parameters](#connection-parameters) for parameter descriptions.

### Using configuration parameters

To connect through a proxy server, add the following configuration parameters:

- `Proxy`
- `NoProxy`

See [Configuration Parameters](#configuration-parameters) for parameter descriptions.

### Using environment variables

To connect through a proxy server, configure the following environment variables:

- `http_proxy`
- `https_proxy`
- `no_proxy`

Note

These environment variables are case-sensitive for Linux and macOS, and must be set in lowercase. For Windows, the environment variables are case-insensitive.

For example:

- Linux or macOS:

  Copy code

  ```
  export http_proxy=http://proxyserver.example.com:80
  export https_proxy=http://proxyserver.example.com:80
  ```

  If the proxy server requires a user name and password, include the credentials, for example:

  Copy code

  ```
  export https_proxy=http://username:password@proxyserver.example.com:80
  ```
- Windows:

  Copy code

  ```
  set http_proxy=http://proxyserver.example.com:80
  set https_proxy=http://proxyserver.example.com:80
  ```

  If the proxy server requires a user name and password, include the credentials, for example:

  Copy code

  ```
  set https_proxy=http://username:password@proxyserver.example.com:80
  ```

Optional: To bypass the proxy for specific communications, set `no_proxy` (for example, to bypass Amazon S3 access , use `no_proxy=.amazonaws.com`).

When using a the `SPCS_TOKEN` service identifier token for SPCS containers, you can set the `SKIP_TOKEN_FILE_PERMISSIONS_VERIFICATION` parameter to `true` to bypass the permission verification for the token file.

## Using single sign-on (SSO) for authentication

If you have [configured Snowflake to use single sign-on (SSO)](/user-guide/admin-security-fed-auth-overview), you can configure
your client application to use SSO for authentication. See [Using SSO with client applications that connect to Snowflake](/user-guide/admin-security-fed-auth-use#label-sso-with-command-line-clients) for details.

## Using multi-factor authentication

Snowflake supports caching MFA tokens, including combining MFA token caching with SSO.

For more information, see [Using MFA token caching to minimize the number of prompts during authentication — \*optional\*](/user-guide/security-mfa#label-mfa-token-caching).

## Using key-pair authentication

The ODBC driver supports key pair authentication and key rotation.

1. To start, complete the initial configuration for key pair authentication as shown in [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).
2. Modify the data source name (DSN) entries for the driver. For information about the DSN entries, see the appropriate topic for your operating system:

   - [Installing and configuring the ODBC Driver for Linux](/developer-guide/odbc/odbc-linux)
   - [Installing and configuring the ODBC Driver for Windows](/developer-guide/odbc/odbc-windows)

   Add the following (case-sensitive) parameters: - `AUTHENTICATOR = SNOWFLAKE_JWT`

   Specifies to authenticate the Snowflake connection using key pair authentication with JSON Web Token (JWT).

   - `JWT_TIME_OUT = integer`

     Optional. Specifies the length of time Snowflake waits to receive the JWT (in seconds) before timing out. If that happens, authentication fails and the driver returns an `Invalid JWT token` error. To resolve repeated occurrences of the error, increase the parameter value. Default: `30`
   - `PRIV_KEY_FILE = path/rsa_key.p8`

     Specifies the local path to the private key file you created (i.e. `rsa_key.p8`).

     The value set in DSN can be overridden by calling the `SQLSetConnectAttr()` function. For more details, see
     [Snowflake-specific behavior of the SQLSetConnectAttr function](/developer-guide/odbc/odbc-api#label-odbc-api-sqlsetconnectattr-specific-behavior).
   - `PRIV_KEY_FILE_PWD = <password>`

     Specifies the passcode to decode the private key file.

     This parameter should be set only if the parameter PRIV\_KEY\_FILE is also set.

     The value set in DSN can be overridden by calling the `SQLSetConnectAttr()` function. For more details, see
     [Snowflake-specific behavior of the SQLSetConnectAttr function](/developer-guide/odbc/odbc-api#label-odbc-api-sqlsetconnectattr-specific-behavior).
3. Save the settings.

## Using the OAuth 2.0 Authorization Code flow

The OAuth 2.0 Authorization Code flow is a secure method for a client application to obtain an access token from an authorization server on behalf of a user, without revealing the user’s credentials.

To enable the OAuth 2.0 Authorization Code flow:

1. Set the `authenticator` connection parameter to `oauth_authorization_code`.
2. Set the following OAuth connection parameters:
   - `OAUTH_CLIENT_ID`: Value of the `client id` provided by the identity provider for Snowflake integration (Snowflake security integration metadata).
   - `OAUTH_CLIENT_SECRET`: Value of the `client secret` provided by the identity provider for Snowflake integration (Snowflake security integration metadata).
   - `OAUTH_AUTHORIZATION_URL`: Identity provider endpoint supplying the authorization code to the driver. When Snowflake is used as an identity provider, this value is derived from the `server` or `account` parameters.
   - `OAUTH_TOKEN_REQUEST_URL`: Identity provider endpoint supplying the access tokens to the driver. When Snowflake is used as an identity provider, this value is derived from the `server` or `account` parameters.
   - `OAUTH_SCOPE`: Scope requested in the identity provider authorization request. By default, it is derived from the role. When multiple scopes are required, the value should be a space-separated list of multiple scopes.
   - `OAUTH_REDIRECT_URI`: URI to use for authorization code redirection (Snowflake security integration metadata). Default: `http://127.0.0.1:{randomAvailablePort}`.

## Using the OAuth 2.0 Client Credentials flow

The OAuth 2.0 Client Credentials flow provides a secure way for machine-to-machine (M2M) authentication, such as the Snowflake Connector for Python connecting to a backend service. Unlike the OAuth 2.0 Authorization Code flow, this method does not rely on any user-specific data.

To enable the OAuth 2.0 Client Credentials flow:

1. Set the `authenticator` connection parameter to `oauth_client_credentials`.
2. Set the following OAuth connection parameters:
   - `OAUTH_CLIENT_ID`: Value of the `client id` provided by the identity provider for Snowflake integration (Snowflake security integration metadata).
   - `OAUTH_CLIENT_SECRET`: Value of the `client secret` provided by the identity provider for Snowflake integration (Snowflake security integration metadata)
   - `OAUTH_TOKEN_REQUEST_URL`: Identity provider endpoint supplying the access tokens to the driver. When Snowflake is used as an identity provider, this value is derived from the `server` or `account` parameters.
   - `OAUTH_SCOPE`: Scope requested in the identity provider authorization request. By default, it is derived from the role. When multiple scopes are required, the value should be a space-separated list of multiple scopes.

## Authenticating with a programmatic access token (PAT)

Programmatic access token (PAT) is a Snowflake-specific authentication method. The feature must be enabled for the account before usage (see the [Prerequisites](/user-guide/programmatic-access-tokens#label-pat-prerequisites) for more information). Authentication with PAT doesn’t involve any human interaction.

## Authenticating with workload identity federation (WIF)

[Workload identity federation](/user-guide/workload-identity-federation) provides a service-to-service authentication method for Snowflake. This method enables applications, services, or containers to authenticate with Snowflake by leveraging their cloud provider’s native identity system, such as AWS IAM, Microsoft Entra ID, or Google Cloud service accounts. This approach eliminates the need for managing long-lived credentials and simplifies credential acquisition compared to other methods like External OAuth. Snowflake connectors are designed to automatically obtain short-lived credentials from the platform’s identity provider.

To enable the workload identity federation authenticator, do the following:

1. Set the `authenticator` connection parameter to `WORKLOAD_IDENTITY`.
2. Set the `workload_identity_provider` connection parameter to `AWS`, `AZURE`, `GCP`, or `OIDC`, based on your platform.
3. For OpenID Connect (OIDC), specify the `token` connection parameter.

## Managing log files

To help you to track issues that might arise, you can enable logging in the ODBC driver.
The ODBC driver provides the following configuration options that you can use to set up logging and manage log files:

- [EnablePidLogFileNames](/developer-guide/odbc/odbc-parameters#label-odbc-enablepidlogfilenames): Adds the process ID to the name of a log file.
- [LogFileCount](/developer-guide/odbc/odbc-parameters#label-odbc-logfilecount): Sets the maximum number of saved log files.
- [LogFileSize](/developer-guide/odbc/odbc-parameters#label-odbc-logfilesize): Specifies the maximum size of a log file.
- [LogLevel](/developer-guide/odbc/odbc-parameters#label-odbc-loglevel): Specifies the types of information to log.
- [LogPath](/developer-guide/odbc/odbc-parameters#label-odbc-logpath): Sets the location for log files.

You can use these parameters to manage how you name, store, and rotate log files. You can specify how large and how many log files you want to keep
before replacing them with newly-created log files. The following example appends the process ID to file names to ensure uniqueness,
sets the maximum file size to 30MB, and keeps the 100 most recent log files.

Copy code

```
EnablePidLogFileNames = true  # Appends the process ID to each log file
LogFileSize = 30,145,728      # Sets log files size to 30MB
LogFileCount = 100            # Saves the 100 most recent log files
```

### Logging configuration file

Alternatively, you can easily specify the log level and
the directory in which to save log files in the `sf_client_config.json` configuration file.

Note

This logging configuration file feature supports only the following log levels:

> - `DEBUG`
> - `ERROR`
> - `INFO`
> - `OFF`
> - `TRACE`
> - `WARNING`
> - `FATAL`

This configuration file uses JSON to define the `log_level` and `log_path` logging parameters, as follows:

Copy code

```
{
  "common": {
    "log_level": "DEBUG",
    "log_path": "/home/user/logs"
  }
}
```

The driver looks for the location of the configuration file in the following order:

- `client_config_file` containing the full path to the configuration file.
- `SF_CLIENT_CONFIG_FILE` environment variable, containing the full path to the configuration file.
- ODBC driver installation directory, where the file must be named `sf_client_config.json`.
- User’s home directory, where the file must be named `sf_client_config.json`.

Note

- The values of the `LogLevel` and `LogPath` take precedence over values defined in the `sf_client_config.json` file.
- If a configuration file specified in either the `client_config_file` connection parameter or
  `SF_CLIENT_CONFIG_FILE` environment variable cannot be found or read, the driver throws an error message.

## Verifying the OCSP connector or driver version

Snowflake uses OCSP to evaluate the certificate chain when making a connection to Snowflake. The driver or connector version and its configuration both determine the OCSP behavior. For more information about the driver or connector version, their configuration, and OCSP behavior, see [OCSP Configuration](/user-guide/ocsp).

## OCSP response cache server

Note

The OCSP response cache server is currently supported by the Snowflake ODBC Driver 2.15.0 and higher.

Snowflake clients initiate every connection to a Snowflake service endpoint with a “handshake” that establishes a secure connection before actually transferring data. As part of the handshake, a
client authenticates the TLS certificate for the service endpoint. The revocation status of the certificate is checked by sending a client certificate request to one of the OCSP
(Online Certificate Status Protocol) servers for the CA (certificate authority).

A connection failure occurs when the response from the OCSP server is delayed beyond a reasonable time. The following caches persist the revocation status, helping alleviate these issues:

- Memory cache, which persists for the life of the process.
- File cache, which persists until the cache directory (e.g. `~/.cache/snowflake` or `~/.snowsql/ocsp_response_cache`) is purged.
- Snowflake OCSP response cache server, which fetches OCSP responses from the CA’s OCSP servers hourly and stores them for 24 hours. Clients can then request the validation status of a given Snowflake
  certificate from this server cache.

  Important

  If your server policy denies access to most or all external IP addresses and web sites, you must allowlist the cache server
  address to allow normal service operation. The cache server hostname is `ocsp*.snowflakecomputing.com:80`.

  If you need to disable the cache server for any reason, set the `SF_OCSP_RESPONSE_CACHE_SERVER_ENABLED` environment variable to `false`. Note that the value is case-sensitive and must
  be in lowercase.

If none of the cache layers contain the OCSP response, the client then attempts to fetch the validation status directly from the OCSP server for the CA.
