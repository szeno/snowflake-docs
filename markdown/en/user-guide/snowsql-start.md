# Connecting through SnowSQL

Caution

[Snowflake CLI](/developer-guide/snowflake-cli/index) is the preferred command-line client for new installs and new work. SnowSQL is a
legacy command-line client. Snowflake will only add new features and enhancements to Snowflake CLI. Snowflake supports SnowSQL 1.5.x through
April 16, 2028. Earlier minor versions have earlier support end dates.

If you’re starting a new project, [install Snowflake CLI](/developer-guide/snowflake-cli/installation/installation). If you already use
SnowSQL, see [Migrating from SnowSQL to Snowflake CLI](/user-guide/snowsql-migrate).

This topic describes how to connect to Snowflake by entering connection parameters manually. The topic then explains how to configure a default connection for ease of use, as well as one or more
*named connections* to use alternative connection settings or create multiple concurrent sessions.

Important

Beginning with Snowflake version 8.24, network administrators have the option to require multi-factor authentication (MFA) for all connections to Snowflake. If your administrator decides to enable this feature, you must configure your client or driver to use MFA when connecting to Snowflake. For more information, see the following resources:

- [8.24 release notes](/release-notes/2024/8_24#label-authentication-policies-new-multi-factor-authentication-parameters)
- [Multi-factor authentication (MFA)](/user-guide/security-mfa)
- [Troubleshooting service users authentication issues with Snowflake MFA](https://community.snowflake.com/s/article/Troubleshooting-service-users-authentication-issues-with-Snowflake-MFA) Knowledge Base article

To run more than one Snowflake session, use `!connect` to open additional
[named connections](#label-connecting-named-connection) inside a single SnowSQL process rather than starting a
second `snowsql` instance:

Note

Snowflake does not support running multiple instances of SnowSQL simultaneously on the same machine. For example, you cannot open two MacOS terminals or Linux shell applications and run `snowsql` in both at the same time.

## Connection syntax

Copy code

```
$ snowsql <connection_parameters>
```

Where `<connection_parameters>` are one or more of the following. For detailed descriptions of each parameter, see [Connection parameters reference](#label-snowsql-connection-parameters) (in this topic).

| Parameter | Description |
| --- | --- |
| `-a, --accountname TEXT` | Your [account identifier](/user-guide/gen-conn-config). Honors $SNOWSQL\_ACCOUNT. |
| `-u, --username TEXT` | Login name of the user to connect to Snowflake. Honors $SNOWSQL\_USER. |
| `-d, --dbname TEXT` | Database to use. Honors $SNOWSQL\_DATABASE. |
| `-s, --schemaname TEXT` | Schema in the database to use. Honors $SNOWSQL\_SCHEMA. |
| `-r, --rolename TEXT` | Role name to use. Honors $SNOWSQL\_ROLE. |
| `-w, --warehouse TEXT` | Warehouse to use. Honors $SNOWSQL\_WAREHOUSE. |
| `-h, --host TEXT` | Host address for the connection. Honors $SNOWSQL\_HOST. |
| `-p, --port INTEGER` | Port number for the connection. Honors $SNOWSQL\_PORT. |
| `--region TEXT` | Region. Honors $SNOWSQL\_REGION. (Deprecated; use -a or –accountname instead) |
| `-m, --mfa-passcode TEXT` | Token to use for multi-factor authentication (MFA) |
| `--mfa-passcode-in-password` | Appends the MFA passcode to the end of the password. |
| `--abort-detached-query` | Aborts a query if the connection between the client and server is lost. By default, it won’t abort even if the connection is lost. |
| `--probe-connection` | Test connectivity to Snowflake. This option is mainly used to print out the TLS (Transport Layer Security) certificate chain. |
| `--proxy-host TEXT` | (DEPRECATED. Use HTTPS\_PROXY and HTTP\_PROXY environment variables.) Proxy server hostname. Honors $SNOWSQL\_PROXY\_HOST. |
| `--proxy-port INTEGER` | (DEPRECATED. Use HTTPS\_PROXY and HTTP\_PROXY environment variables.) Proxy server port number. Honors $SNOWSQL\_PROXY\_PORT. |
| `--proxy-user TEXT` | (DEPRECATED. Use HTTPS\_PROXY and HTTP\_PROXY environment variables.) Proxy server username. Honors $SNOWSQL\_PROXY\_USER. Set $SNOWSQL\_PROXY\_PWD for the proxy server password. |
| `--authenticator TEXT` | Authenticator: ‘snowflake’, ‘externalbrowser’ (to use any IdP and a web browser), https://<okta\_account\_name>.okta.com (to use Okta natively), ‘workload\_identity’ or ‘oauth’ to authenticate using OAuth. |
| `-v, --version` | Shows the current SnowSQL version, or uses a specific version if provided as a value. |
| `--noup` | Disables auto-upgrade for this run. If no version is specified for -v, the latest version in ~/.snowsql/ is used. |
| `-D, --variable TEXT` | Sets a variable to be referred by &<var>. -D tablename=CENUSTRACKONE or –variable db\_key=$DB\_KEY |
| `-o, --option TEXT` | Set SnowSQL options. See the options reference in the Snowflake documentation. |
| `-f, --filename PATH` | File to execute. |
| `-q, --query TEXT` | Query to execute. |
| `--query_tags TEXT` | Tags to use when running queries. By default, `--query_tag` reads the value of the `SNOWSQL_QUERY_TAG` environment variable. |
| `--config PATH` | Path and name of the SnowSQL configuration file. By default, ~/.snowsql/config. |
| `-P, --prompt` | Forces an [interactive password prompt](#label-snowsql-additional-connection-parameters-prompt) to allow you to specify a password that differs from the one stored in the $SNOWSQL\_PWD environment variable. |
| `-M, --mfa-prompt` | Forces a prompt for the second token for MFA. |
| `-c, --connection TEXT` | Named set of connection parameters to use. |
| `--single-transaction` | Connects with autocommit disabled. Wraps BEGIN/COMMIT around statements to execute them as a single transaction, ensuring all commands complete successfully or no change is applied. |
| `--private-key-path PATH` | Path to private key file. |
| `--oauth-client-id` | Value of client id provided by the identity provider for Snowflake integration. |
| `--oauth-redirect-uri` | URI to use for authorization code redirection. |
| `--oauth-authorization-url` | Identity provider endpoint supplying the authorization code to the driver. |
| `--oauth-token-request-url` | Identity provider endpoint supplying the access tokens to the driver. |
| `--oauth-scope` | Scope requested in the identity provider authorization request. |
| `--oauth-disable-pkce` | Disables Proof Key for Code Exchange (PKCE). Default: `False`. |
| `--oauth-enable-refresh-tokens` | Enables a silent re-authentication when the actual access token becomes outdated. Default: `False`. |
| `--oauth-enable-single-use-refresh-tokens` | Whether to opt-in to single-use refresh token semantics. Default: `False`. |
| `--workload-identity-provider` | workload identity provider [AWSMicrosoft AzureGCP|OIDC]. By default auto discovery is performed. |
| `--disable-request-pooling` | Disables connection pooling. |
| `-U, --upgrade` | Force upgrade of SnowSQL to the latest version. |
| `-K, --client-session-keep-alive` | Keep the session active indefinitely, even if there is no activity from the user. |
| `--include_connector_version` | Display the version of the Snowflake Connector for Python software that is packaged in the SnowSQL binary. |
| `-?, --help` | Show this message and exit. |

Expand

Show lessSee more

### Specifying passwords when connecting

Passwords cannot be passed through connection parameters. Passwords must be specified in one of the following ways:

- Entered via [interactive prompt](#label-snowsql-additional-connection-parameters-prompt) in SnowSQL (applies to passwords only).
- Defined in the SnowSQL configuration file using the `password` option. For details, see [Configuring Default Connection Settings](#configuring-default-connection-settings) (in this topic).
- Specified using the `SNOWSQL_PWD` environment variables. For details, see [Using Environment Variables](#using-environment-variables) (in this topic).

Note

In Windows environments, the Cygwin terminal doesn’t prompt for your account identifier, username, or password. This is because
SnowSQL cannot enable TTY mode in Cygwin terminals.

### Using environment variables

Currently, environment variables can only be used to pre-specify some command-line parameter values such as password, host, and database. Environment variables are not available to use in SnowSQL variable substitution unless they are explicitly specified on the command line when starting SnowSQL, using either the `-D` or `--variable` connection parameter. For example:

Linux/macOS:
:   Copy code

    ```
    $ snowsql ... -D tablename=CENUSTRACKONE --variable db_key=$DB_KEY
    ```

Windows:
:   Copy code

    ```
    $ snowsql ... -D tablename=CENUSTRACKONE --variable db_key=%DB_KEY%
    ```

In the above example, `--variable` sets a Snowflake variable named `db_key` to the `DB_KEY` environment variable.

## Configuring default connection settings

We recommend configuring your default connection parameters to simplify the connection process. Thereafter, when connecting to
Snowflake, you can omit your Snowflake account identifier, username, and any other parameters you have configured as your default
values.

To configure your default settings:

1. Open the [SnowSQL configuration file](/user-guide/snowsql-config) (named `config`) in a text editor. The default
   location of the file is:

   Linux/macOS:
   :   `~/.snowsql/`

   Windows:
   :   `%USERPROFILE%\.snowsql\`

   Note

   You can change the default location by specifying the `--config path` command-line flag when starting SnowSQL.

1. In the `[connections]` section, configure the default connection parameters by removing the comment symbol from any of
   the following parameters and specifying the correct values. For information on these settings, see
   [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).

   Copy code

   ```
   [connections]
   #accountname = <string>   # Account identifier to connect to Snowflake (for example, myorganization-myaccount).
   #username = <string>      # User name in the account. Optional.
   #password = <string>      # User password. Optional.
   #dbname = <string>        # Default database. Optional.
   #schemaname = <string>    # Default schema. Optional.
   #warehousename = <string> # Default warehouse. Optional.
   #rolename = <string>      # Default role. Optional.
   #authenticator = <string> # Authenticator: 'snowflake', 'externalbrowser' (to use any IdP and a web browser),  https://<okta_account_name>.okta.com (to use Okta natively), 'oauth' to authenticate using OAuth.
   ```

   Attention

   - The password is stored in plain text in the `config` file. You must explicitly secure the file to restrict access. For example, in Linux or macOS, you can set the read permissions to you
     alone by running `chmod`:

     Copy code

     ```
     $ chmod 700 ~/.snowsql/config
     ```
   - If your password includes special characters, you must enclose the password in either single quotes or double quotes.

## Verifying the network connection to Snowflake with SnowCD

After configuration, you can evaluate and troubleshoot your network connectivity to Snowflake using [SnowCD](/user-guide/snowcd).

You can use SnowCD during the initial configuration process and on-demand at any time to evaluate and troubleshoot your network connection to Snowflake.

## Using named connections

To make multiple simultaneous connections to Snowflake, or to simply store different sets of connection configurations, you can define one or more *named* connections.

### Defining named connections in the configuration file

1. Open the `config` configuration file in a text editor. By default, the file is located in:

   Linux/macOS:
   :   `~/.snowsql/`

   Windows:
   :   `%USERPROFILE%\.snowsql\`
2. Add a separate `[connections]` section with a unique name for each named connection.

   For example, the following illustrates a connection named `my_example_connection` for a Snowflake account with the
   [account identifier](/user-guide/gen-conn-config) `myorganization-myaccount`:

   Copy code

   ```
   [connections.my_example_connection]
   accountname = myorganization-myaccount
   username = jsmith
   password = xxxxxxxxxxxxxxxxxxxx
   dbname = mydb
   schemaname = public
   warehousename = mywh
   ```

### Connecting to Snowflake using a named connection

Use the `-c <string>` (or `--connection <string>`) connection parameter to specify a named connection, where `<string>` is the name of a connection defined in the
[configuration file](/user-guide/snowsql-config#label-configuring-snowsql).

For example, connect using the `my_example_connection` connection you created in [Defining Named Connections in the Configuration File](#defining-named-connections-in-the-configuration-file) (in this topic):

> Copy code
>
> ```
> $ snowsql -c my_example_connection
> ```

## Using key-pair authentication and key-pair rotation

SnowSQL supports key pair authentication and key rotation. You can use unencrypted or encrypted
key pairs.

Caution

While unencrypted private keys are supported, Snowflake strongly recommends using encrypted private keys
when connecting to Snowflake. Unencrypted private keys have no protection against unauthorized use if any
unauthorized person gains access to them.

The following procedure presumes you use the recommended encrypted key pair authentication:

1. To start, follow the instructions to configure [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).
2. Specify the path to the private key file either in the configuration file or on the command line:

> - In the configuration file:
>
>   - Add the `private_key_path` connection parameter to your connection settings and specify the local path to the private key file you created. The syntax is not OS-specific:
>
>     Supported OS:
>     :   Copy code
>
>         ```
>         private_key_path = <path>/rsa_key.p8
>         ```
>   - Use the `SNOWSQL_PRIVATE_KEY_PASSPHRASE` environment variable to set the passphrase for decrypting the private key file.
>     Note that you do not enclose the passphrase in quotes for Linux or MacOS but must use single or double quotes for Windows:
>
>     Linux/macOS:
>     :   Copy code
>
>         ```
>         export SNOWSQL_PRIVATE_KEY_PASSPHRASE=<passphrase>
>         ```
>
>     Windows:
>     :   Copy code
>
>         ```
>         set SNOWSQL_PRIVATE_KEY_PASSPHRASE=<passphrase>
>         ```
> - On the command line:
>
>   Include the `private-key-path` connection parameter and specify the path to your encrypted private key file:
>
>   Copy code
>
>   ```
>   $ snowsql -a <account_identifier> -u <user> --private-key-path <path>/rsa_key.p8
>   ```
>
>   SnowSQL prompts you for the passphrase. Alternatively, use the `SNOWSQL_PRIVATE_KEY_PASSPHRASE` environment variable to set the passphrase for decrypting the private key file (as described above).

## Using the OAuth 2.0 Authorization Code flow

The OAuth 2.0 Authorization Code flow is a secure method for a client application to obtain an access token from an authorization server on behalf of a user, without revealing the user’s credentials.

The following sample configuration file shows how to use this flow:

Copy code

```
[connections.oauth]
authenticator = "OAUTH_AUTHORIZATION_CODE"
username = "user"
accountname = "account"
oauth_client_id = "client_id"
oauth_client_secret = "client_secret"
oauth_redirect_uri = "http://localhost:8001/snowflake/oauth-redirect"
oauth_scope = "session:role:PUBLIC"
```

## Using the OAuth 2.0 Client Credentials flow

The OAuth 2.0 Client Credentials flow provides a secure way for machine-to-machine (M2M) authentication, such as the Snowflake Connector for Python connecting to a backend service. Unlike the OAuth 2.0 Authorization Code flow, this method does not rely on any user-specific data.

The following sample configuration file shows how to use this flow:

Copy code

```
[connections.oauth]
authenticator = "OAUTH_CLIENT_CREDENTIALS"
username = "user"
accountname = "account"
oauth_client_id = "client_id"
oauth_client_secret = "client_secret"
oauth_token_request_url = "http://identity.provider.com/token"
oauth_scope = "session:role:PUBLIC"
```

## Using a proxy server

To use a proxy server, configure the following environment variables:

- HTTP\_PROXY
- HTTPS\_PROXY
- NO\_PROXY

For example:

Linux/macOS:
:   Copy code

    ```
    export HTTP_PROXY='http://username:password@proxyserver.example.com:80'
    export HTTPS_PROXY='http://username:password@proxyserver.example.com:80'
    ```

Windows:
:   Copy code

    ```
    set HTTP_PROXY=http://username:password@proxyserver.example.com:80
    set HTTPS_PROXY=http://username:password@proxyserver.example.com:80
    ```

Tip

Snowflake does not support configurations involving intercepting HTTPS proxies that present a Transport Layer Security (TLS)
certificate other than the one issued by Snowflake. Avoiding this configuration helps reduce potential security risks
such as a MITM (Man In The Middle) attack through a compromised proxy.

If you must use your TLS proxy, Snowflake strongly recommends that you update the server policy to pass through the
Snowflake certificate such that no certificate is altered in the middle of communications.

Optionally, `NO_PROXY` can be used to bypass the proxy for specific communications. For example, Amazon S3 access can be bypassed by specifying `NO_PROXY=".amazonaws.com"`.

## Using a web browser for federated authentication/SSO

To use [browser-based SSO authentication](/user-guide/admin-security-fed-auth-use#label-browser-based-sso) for SnowSQL, add `--authenticator externalbrowser` to your [SnowSQL connection parameters](#label-snowsql-connection-parameters):

For example:

> Copy code
>
> ```
> $ snowsql -a <account_identifier> -u <username> --authenticator externalbrowser
> ```

For more information about federated authentication/SSO, see [Managing/Using federated authentication](/user-guide/admin-security-fed-auth-use).

## Verifying the OCSP connector or driver version

Snowflake uses OCSP to evaluate the certificate chain when making a connection to Snowflake. The driver or connector version and its configuration both determine the OCSP behavior. For more information about the driver or connector version, their configuration, and OCSP behavior, see [OCSP Configuration](/user-guide/ocsp).

## OCSP response cache server

Note

The OCSP response cache server is currently supported by SnowSQL 1.1.55 and higher.

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

## Connection error handling

`Cannot open self /usr/bin/snowsql or archive /usr/bin/snowsql.pkg` (Linux Only)
:   Due to a limitation in `pyinstaller` (the program that packages SnowSQL into a stand-alone executable from Python source code), `prelink` mistakenly strips parts of the `snowsql`
    executable and causes this error.

    To avoid this issue, the SnowSQL installer attempts to update the `prelink` configuration file in `/etc/prelink.conf.d/snowsql.conf` for the `snowsql` executable such that
    `prelink` does not alter the file. Unfortunately, this configuration update cannot be made by the SnowSQL auto-upgrade process.

    Work with your system administrator to run the following command on your workstation:

    > Copy code
    >
    > ```
    > $ sudo bash -c "echo '-b snowsql' > /etc/prelink.conf.d/snowsql.conf"
    > ```

Note

If you install `snowsql` in your user home directory, this issue is less likely to occur because `prelink` is configured, by default, to scan the shared binary directories (e.g.
`/usr/bin` or `/bin`) and does not alter programs in your home directory.

## Connection parameters reference

### `-a` , `--accountname`

> Description:
> :   Required
>
>     Specifies your [account identifier](/user-guide/gen-conn-config). Specify the account identifier in this form:
>     `organization_name-account_name` (for example, `myorganization-myaccount`).
>
>     For instructions on finding the account identifier, see [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).
>
>     This connection parameter can also be set in the [configuration file](/user-guide/snowsql-config#label-configuring-snowsql).
>
> Value:
> :   String
>
>     Also, the value can be an environment variable:
>
>     Linux/macOS:
>     :   `$SNOWSQL_ACCOUNT`
>
>     Windows:
>     :   `%SNOWSQL_ACCOUNT%`
>
>     For example, in Linux or macOS:
>
>     > Copy code
>     >
>     > ```
>     > $ export SNOWSQL_ACCOUNT=myorganization-myaccount
>     >
>     > $ snowsql -a $SNOWSQL_ACCOUNT
>     > ```
>
> Default:
> :   None

### `-u` , `--username`

> Description:
> :   Specifies the login name of the user with whom you connect to the specified account.
>
>     This connection parameter can also be set in the [configuration file](/user-guide/snowsql-config#label-configuring-snowsql).
>
> Value:
> :   String
>
>     The value can be an environment variable:
>
>     Linux/macOS:
>     :   `$SNOWSQL_USER`
>
>     Windows:
>     :   `%SNOWSQL_USER%`
>
>     For example, in Linux or macOS:
>
>     > Copy code
>     >
>     > ```
>     > $ export SNOWSQL_USER=jdoe
>     >
>     > $ snowsql -u $SNOWSQL_USER
>     > ```
>
> Default:
> :   None

### `-d` , `--dbname`

> Description:
> :   Specifies the database to use by default in the client session (can be changed after login).
>
> Value:
> :   String
>
>     The value can be an environment variable:
>
>     Linux/macOS:
>     :   `$SNOWSQL_DATABASE`
>
>     Windows:
>     :   `%SNOWSQL_DATABASE%`
>
>     This connection parameter can also be set in the [configuration file](/user-guide/snowsql-config#label-configuring-snowsql).
>
> Default:
> :   None

### `-s` , `--schemaname`

> Description:
> :   Specifies the database schema to use by default in the client session (can be changed after login).
>
> Value:
> :   String
>
>     The value can be an environment variable:
>
>     Linux/macOS:
>     :   `$SNOWSQL_SCHEMA`
>
>     Windows:
>     :   `%SNOWSQL_SCHEMA%`
>
>     This connection parameter can also be set in the [configuration file](/user-guide/snowsql-config#label-configuring-snowsql).
>
> Default:
> :   None

### `-r` , `--rolename`

> Description:
> :   Specifies the role to use by default for accessing Snowflake objects in the client session (can be changed after login).
>
>     This connection parameter can also be set in the [configuration file](/user-guide/snowsql-config#label-configuring-snowsql).
>
> Value:
> :   String
>
>     The value can be an environment variable:
>
>     Linux/macOS:
>     :   `$SNOWSQL_ROLE`
>
>     Windows:
>     :   `%SNOWSQL_ROLE%`
>
> Default:
> :   None

### `-w` , `--warehouse`

> Description:
> :   Specifies the virtual warehouse to use by default for queries, loading, etc. in the client session (can be changed after login).
>
>     This connection parameter can also be set in the [configuration file](/user-guide/snowsql-config#label-configuring-snowsql).
>
> Value:
> :   String
>
>     The value can be an environment variable:
>
>     Linux/macOS:
>     :   `$SNOWSQL_WAREHOUSE`
>
>     Windows:
>     :   `%SNOWSQL_WAREHOUSE%`
>
> Default:
> :   None

### `-h` , `--host` — *Deprecated*

> Description:
> :   Provided for backward compatibility/internal use
>
>     Specifies the address of the host to which you connect in Snowflake.
>
>     This parameter is no longer used because the host address is determined automatically by concatenating the account identifier
>     you specified (using either `-a` or `--account`) and the Snowflake domain (`snowflakecomputing.com`).
>
> Value:
> :   String
>
> Default:
> :   None

### `-p` , `--port` — *Deprecated*

> Description:
> :   Provided for backward compatibility/internal use
>
>     Specifies the port number to use for connection.
>
>     This parameter is no longer used because the port number for Snowflake is always `443`.
>
> Value:
> :   String
>
> Default:
> :   None

### `--region` — *Deprecated*

> Description:
> :   Provided for backward compatibility/internal use
>
>     Specifies the ID for the [region](/user-guide/intro-regions) where your account is located.
>
>     This parameter is no longer used. For more details, see [Connection parameters reference](#label-account-param-snowsql) (in this topic).
>
> Value:
> :   N/A
>
> Default:
> :   N/A

### `-m` , `--mfa-passcode`

> Description:
> :   Specifies the second token for MFA (multi-factor authentication) if you pass in the passcode in the command line.
>
> Value:
> :   String
>
> Default:
> :   None

### `--mfa-passcode-in-password`

> Description:
> :   Appends the MFA passcode to the end of the password.
>
>     You can force the password prompt and type the password followed by the MFA passcode. For example if the MFA token was `123456` and the password was `PASSWORD`:
>
>     > Copy code
>     >
>     > ```
>     > $ snowsql ... -P ...
>     >
>     > Password: PASSWORD123456
>     > ```
>
> Value:
> :   N/A (parameter doesn’t take a value)
>
> Default:
> :   N/A

### `--abort-detached-query`

> Description:
> :   Aborts a query if the connection between the client and server is lost.
>
> Value:
> :   Boolean
>
> Default:
> :   False (i.e. an active query does not abort if the connection is lost)

### `--probe-connection`

> Description:
> :   Test connectivity to Snowflake and report the results. Note that this is an experimental option used mainly to print out the TLS certificate chain.
>
> Value:
> :   N/A (parameter doesn’t take a value)
>
> Default:
> :   N/A

### `--authenticator`

> Description:
> :   Specifies the authenticator to use for verifying user login credentials.
>
> Value:
> :   String (Constant):
>
>     > - `snowflake` uses the internal Snowflake authenticator.
>     > - `externalbrowser` [uses your web browser](/user-guide/admin-security-fed-auth-use#label-browser-based-sso) to authenticate with Okta, AD FS, or any other SAML 2.0-compliant identity provider (IdP) that has been defined for your account.
>     > - `https://<okta_account_name>.okta.com` (i.e. the URL endpoint for Okta) [authenticates through native Okta](/user-guide/admin-security-fed-auth-use#label-native-sso-okta) (only supported if your IdP is Okta).
>     > - `oauth` authenticates using OAuth. When OAuth is specified as the authenticator, you must also set the `--token` parameter to specify the OAuth token ([see below](/user-guide/snowsql-start#label-snowsql-additional-connection-parameters-token)).
>
>     For more information, see [Managing/Using federated authentication](/user-guide/admin-security-fed-auth-use) and [Clients, drivers, and connectors](/user-guide/oauth-intro#label-oauth-intro-clients-drivers-conns).
>
> Default:
> :   `snowflake`
>
> Note
>
> The `externalbrowser` authenticator is only supported in terminal windows that have web browser access. For example, a terminal window on a remote machine accessed through a SSH (Secure Shell)
> session may require additional setup to open a web browser.
>
> If you don’t have access to a web browser, but your IdP is Okta, you can use native Okta (i.e. set the authenticator to `https://<okta_account_name>.okta.com`).

### `--token`

> Description:
> :   Specifies the OAuth token to use for authentication.
>     This parameter is required only when you specify `--authenticator=oauth`.
>
> Value:
> :   String
>
> Default:
> :   None

### `-v` , `--version`

> Description:
> :   Use the specified SnowSQL version or, if no version is specified, display the latest SnowSQL version installed.
>
> Value:
> :   String
>
> Default:
> :   None

### `--versions`

> Description:
> :   Lists all available versions of SnowSQL that can be installed and run. To install an earlier SnowSQL version from the list, use the `-v` option and specify the version you want
>     to install.
>
> Value:
> :   N/A (parameter doesn’t take a value)
>
> Default:
> :   N/A

### `--noup`

> Description:
> :   Disables auto-upgrade for this run. If this option is not included and a newer version is available, SnowSQL automatically downloads and installs the new version. The next time you
>     run SnowSQL, the new version is used.
>
> Value:
> :   N/A (parameter doesn’t take a value)
>
> Default:
> :   N/A

### `-D` , `--variable`

> Description:
> :   Defines SnowSQL variables on the command line. This option can be used to set specific variables to use in Snowflake.
>
> Value:
> :   String
>
>     For example:
>
>     > Copy code
>     >
>     > ```
>     > $ snowsql ... -D tablename=CENUSTRACKONE --variable db_key=$DB_KEY ...
>     > ```
>
> Default:
> :   None

### `-o` , `--option`

> Description:
> :   Defines SnowSQL configuration options on the command line. These options override any options that have been set in the SnowSQL configuration file. For descriptions of the options you
>     can set/override, see [SnowSQL configuration options reference](/user-guide/snowsql-config#label-snowsql-options).
>
> Value:
> :   String
>
> Default:
> :   None

### `-f` , `--filename`

> Description:
> :   Specifies a SQL file to execute in batch mode.
>
>     The value can be a file name (including the directory path, if needed) or a URL to the file.
>
> Value:
> :   String
>
> Default:
> :   None

### `-q` , `--query`

> Description:
> :   Specifies a SQL query to execute.
>
>     The value can be a single SQL query or a semicolon-separated list of queries to execute (e.g. `'select current_user(); select current_role()'`).
>
>     You can also specify multiple queries to run asynchronously by separating the queries with `;>`.
>     The following example starts SnowSQL and runs all four queries asynchronously:
>
>     `snowsql -o log_level=DEBUG -q "select * from SNOWSQLTABLE;> insert into table table1 values(2);> select 5;>select count(*) from testtable;"`
>
> Value:
> :   String
>
> Default:
> :   None

### `--query_tag`

> Description:
> :   Specifies the tags to use when running a query.
>
>     The value can be a single tag or a semicolon-separated list of tags.
>
> Value:
> :   String
>
> Default:
> :   Value of the `SNOWSQL_QUERY_TAG` environment variable.

### `--config`

> Description:
> :   Specifies the location (i.e. directory path) for the SnowSQL configuration file. Include this connector parameter if you want to move or copy the configuration file from the default
>     location.
>
> Value:
> :   String
>
> Default:
> :   OS-specific:
>
>     Linux/macOS:
>     :   `~/.snowsql/`
>
>     Windows:
>     :   `%USERPROFILE%\.snowsql\`

### `-P` , `--prompt`

> Description:
> :   Forces an interactive password prompt.
>
>     By default, SnowSQL uses the password stored in the $SNOWSQL\_PWD environment variable. Using this option allows you to override the password defined in $SNOWSQL\_PWD.
>
> Value:
> :   N/A (parameter doesn’t take a value)
>
> Default:
> :   N/A

### `-M`, `--mfa-prompt`

> Description:
> :   Forces a prompt for the second token for MFA. Alternatively use `--mfa-passcode <string>` if you want to pass in to the command line.
>
> Value:
> :   N/A (parameter doesn’t take a value)
>
> Default:
> :   N/A

### `-c` , `--connection`

> Description:
> :   Specifies a connection to use, where the specified string is the name of a connection defined in the SnowSQL configuration file. For more details, see
>     [Using named connections](#label-connecting-named-connection) (in this topic).
>
> Value:
> :   String
>
> Default:
> :   None

### `--single-transaction`

> Description:
> :   Combined with `--filename`, `--query`, or standard input commands, this option wraps BEGIN/COMMIT around the statements to ensure all commands complete successfully or no
>     change is applied.
>
> Value:
> :   N/A (parameter doesn’t take a value)
>
> Default:
> :   N/A
>
> Note
>
> Note that if the input commands use BEGIN, COMMIT, or ROLLBACK, this option will not work correctly. Also, if any command cannot be executed inside a transaction block, this option will cause the command to fail.

### `--private-key-path`

> Description:
> :   Path to private key file.
>
> Caution
>
> > While unencrypted private keys are supported, Snowflake strongly recommends using encrypted private keys
> > when connecting to Snowflake.
>
> For more information, see [Using Key Pair Authentication & Key Pair Rotation](#label-snowsql-key-pair-authn-rotation).
>
> This connection parameter can also be set in the [configuration file](/user-guide/snowsql-config#label-configuring-snowsql).
>
> Value:
> :   String
>
> Default:
> :   None

### `--disable-request-pooling`

> Description:
> :   By default, snowsql uses connection pooling. Connection pooling usually reduces the lag
>     time to make a connection. However, it can slow down client failover to an alternative DNS when a
>     DNS problem occurs. This parameter allows you to turn off connection pooling.
>
>     This parameter applies only to customers who have [replication](/user-guide/account-replication-intro) enabled.
>
> Value:
> :   N/A (parameter doesn’t take a value)
>
> Default:
> :   N/A

### `-U` , `--upgrade`

> Description:
> :   Force upgrade of SnowSQL to the latest version if it is not downloaded in the local directory.
>
> Value:
> :   N/A (parameter doesn’t take a value)
>
> Default:
> :   N/A
>
> Note
>
> Requires the bootstrap executable of SnowSQL 1.1.63 or newer version. Download it from the UI.

### `-K` , `--client-session-keep-alive`

> Description:
> :   Keep the session active indefinitely, even if there is no activity from the user.
>
> Value:
> :   N/A (parameter doesn’t take a value)
>
> Default:
> :   N/A

### `--include_connector_version`

> Description:
> :   Displays the version of the Snowflake Connector for Python software that is packaged in the SnowSQL binary.
>
> Value:
> :   N/A (parameter doesn’t take a value)
>
> Default:
> :   N/A

### `-?` , `--help`

> Description:
> :   Shows the command line quick usage guide.
>
> Value:
> :   N/A (parameter doesn’t take a value)
>
> Default:
> :   N/A
