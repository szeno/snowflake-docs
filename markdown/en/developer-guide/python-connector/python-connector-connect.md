# Connecting to Snowflake with the Python Connector

This topic explains the various ways you can connect to Snowflake with the Python connector.

Important

Beginning with Snowflake version 8.24, network administrators have the option to require multi-factor authentication (MFA) for all connections to Snowflake. If your administrator decides to enable this feature, you must configure your client or driver to use MFA when connecting to Snowflake. For more information, see the following resources:

- [8.24 release notes](/release-notes/2024/8_24#label-authentication-policies-new-multi-factor-authentication-parameters)
- [Multi-factor authentication (MFA)](/user-guide/security-mfa)
- [Troubleshooting service users authentication issues with Snowflake MFA](https://community.snowflake.com/s/article/Troubleshooting-service-users-authentication-issues-with-Snowflake-MFA) Knowledge Base article

## Importing the `snowflake.connector` module

To import the `snowflake.connector` module, execute the following command:

Copy code

```
import snowflake.connector
```

You can get login information from environment variables, the command line, a configuration file, or another appropriate
source. For example:

Copy code

```
PASSWORD = os.getenv('SNOWSQL_PWD')
WAREHOUSE = os.getenv('WAREHOUSE')
...
```

For the `user` connection parameter, specify the user’s `LOGIN_NAME` property, not the user object’s `NAME` when the values
differ. If no login name was explicitly set, the user object’s name is the default login name. See [CREATE USER](/sql-reference/sql/create-user).

For the ACCOUNT parameter, use your [account identifier](/user-guide/gen-conn-config). Note that the account identifier
does not include the `snowflakecomputing.com` suffix.

For details and examples, see [Usage notes for the `account` parameter (for the `connect` method)](/developer-guide/python-connector/python-connector-api#label-account-format-info).

Note

The `snowflake.connector.ConnectionConfig` class defines all connector parameters. See that class for parameter descriptions.

If you copy data from your own Amazon S3 bucket, then you need the AWS\_ACCESS\_KEY\_ID and AWS\_SECRET\_ACCESS\_KEY.

Copy code

```
import os

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
```

Note

If your data is stored in a Microsoft Azure container, provide the credentials directly in the COPY statement.

After reading the connection information, connect using either the default authenticator or federated authentication
(if enabled).

## Setting session parameters

You can set session parameters, such as QUERY\_TAG, in multiple ways when using the Python Connector:

- You can set session-level parameters at the time you connect to Snowflake by passing
  the optional connection parameter named `session_parameters`, as follows:

  Copy code

  ```
  con = snowflake.connector.connect(
   user='XXXX',
   password='XXXX',
   account='XXXX',
   session_parameters={
       'QUERY_TAG': 'EndOfMonthFinancials',
   }
  )
  ```

  The `session_parameters` dictionary passed to the [snowflake.connector.connect](/developer-guide/python-connector/python-connector-api#label-snowflake-connector-methods-connect) method can contain one or more session-level parameters.

  Note

  You cannot set the [SEARCH\_PATH](/sql-reference/parameters#label-search-path) parameter within a Python connection. You must establish a session before setting a search path.
- You can also set session parameters by executing the ALTER SESSION SET SQL statement after connecting:

  Copy code

  ```
  con.cursor().execute("ALTER SESSION SET QUERY_TAG = 'EndOfMonthFinancials'")
  ```
- `execute()` can override `TIMEZONE` or `QUERY_TAG` for one statement. Pass them in `_statement_params`. The values are sent with that query and do not change the session.

  Copy code

  ```
  cur.execute(
      "SELECT CURRENT_TIMESTAMP()",
      _statement_params={"TIMEZONE": "America/Los_Angeles"},
  )
  ```

For more information about session parameters, see the descriptions of individual parameters on the general
[Parameters](/sql-reference/parameters) page.

## Connecting using the default authenticator

Connect to Snowflake using the login parameters:

Copy code

```
conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE,
    database=DATABASE,
    schema=SCHEMA
    )
```

You might need to extend this with other information available in the [snowflake.connector.connect](/developer-guide/python-connector/python-connector-api#label-snowflake-connector-methods-connect) method.

## Connecting using the `connections.toml` file

The Python connector lets you add connection definitions to a `connections.toml` configuration file.
A connection definition refers to a collection of connection-related parameters. Snowflake Python libraries currently support TOML version 1.0.0.

For more information about `toml` file formats, see [TOML (Tom’s Obvious Minimal Language)](https://toml.io/en/).

The Python connector looks for the `connections.toml` file in the following locations, in order:

- If a `~/.snowflake` directory exists on your machine, the Python Connector uses the
  `~/.snowflake/connections.toml` file. You can override the default `~/.snowflake` directory by setting the
  location in the `SNOWFLAKE_HOME` environment variable.
- Otherwise, the Python Connector uses the `connections.toml` file in the one of the following locations, based on your operating system:
  - Linux: `~/.config/snowflake/connections.toml`, but you can update it with XDG vars
  - Windows: `%USERPROFILE%\AppData\Local\snowflake\connections.toml`
  - Mac: `~/Library/Application Support/snowflake/connections.toml`

To add credentials in a connections configuration file:

1. In a text editor, open the `connections.toml` file for editing. For example, to open the file in the Linux **vi** editor:

   Copy code

   ```
   $ vi connections.toml
   ```
2. Add a new Snowflake connection definition.

   You can generate the basic settings for the TOML configuration file in Snowsight. For information, see
   [Configuring a client, driver, library, or third-party application to connect to Snowflake](/user-guide/gen-conn-config).

   For example, to add a Snowflake connection called `myconnection` with the account `myaccount`,
   user `johndoe`, and password credentials, as well as database information,
   add the following lines to the configuration file:

   Copy code

   ```
   [myconnection]
   account = "myorganization-myaccount"
   user = "jdoe"
   password = "******"
   warehouse = "my-wh"
   database = "my_db"
   schema = "my_schema"
   ```

   Connection definitions support the same configuration options available in the
   [snowflake.connector.connect](/developer-guide/python-connector/python-connector-api#label-snowflake-connector-methods-connect) method.
3. Optional: Add more connections, as shown:

   Copy code

   ```
   [myconnection_test]
   account = "myorganization-myaccount"
   user = "jdoe-test"
   password = "******"
   warehouse = "my-test_wh"
   database = "my_test_db"
   schema = "my_schema"
   ```
4. Save changes to the file.
5. In your Python code, supply the connection name to `snowflake.connector.connect`, similar to the following:

   Copy code

   ```
   with snowflake.connector.connect(
      connection_name="myconnection",
   ) as conn:
   ```

   You can also override values defined for the connection in the `connections.toml` file, as follows:

   Copy code

   ```
   with snowflake.connector.connect(
      connection_name="myconnection",
      warehouse="test_xl_wh",
      database="testdb_2"
   ) as conn:
   ```

## Setting a default connection

You can set a connection as the default, so you don’t have to specify one every time you call
`snowflake.connector.connect()` to connect to Snowflake. You can define a default connection in any of
the following ways, which are listed in increasing order of precedence:

- Create a connection definition named `default`.

  1. In the `connections.toml` file, create the connection definition and give it the name `default`, as shown:

     Copy code

     ```
     [default]
     account = "myorganization-myaccount"
     user = "jdoe-test"
     password = "******"
     warehouse = "my-test_wh"
     database = "my_test_db"
     schema = "my_schema"
     ```
  2. Save the file.
- Specify a named connection as the default connection in the Snowflake `config.toml` file, in the same directory
  as the `connections.toml` file.

  1. Open the `config.toml` file for editing; then:
  2. Set the `default_connection_name` parameter similar to the following:

     Copy code

     ```
     default_connection_name = "myaccount"
     ```
  3. Save the file.
- Set the `SNOWFLAKE_DEFAULT_CONNECTION_NAME` environment variable.

  Sometimes you might want to override the default connection temporarily, such as trying a test connection, without needing
  to change the normal default connection. You can override the default connection specified in the `connections.toml`
  and `config.toml` files by setting the `SNOWFLAKE_DEFAULT_CONNECTION_NAME` environment variable as follows:

  Copy code

  ```
  SNOWFLAKE_DEFAULT_CONNECTION_NAME = myconnection_test
  ```

To use the default connection, execute Python code similar to the following:

> Copy code
>
> ```
> with snowflake.connector.connect() as conn:
>     with conn.cursor() as cur:
>         print(cur.execute("SELECT 1;").fetchall())
> ```

Note

If you choose to rely on a default connection, you cannot override connection parameters, such as `username`,
`database`, or `schema`.

## Using single sign-on (SSO) for authentication

If you have [configured Snowflake to use single sign-on (SSO)](/user-guide/admin-security-fed-auth-overview), you can configure
your client application to use SSO for authentication. See [Using SSO with client applications that connect to Snowflake](/user-guide/admin-security-fed-auth-use#label-sso-with-command-line-clients) for details.

## Using multi-factor authentication (MFA)

Snowflake supports caching MFA tokens, including combining MFA token caching with SSO.

The following sample code shows how to use MFA with the Python connector using a variety of methods:

- Push notification (Duo Push) - Default behavior when no passcode is provided.
- TOTP (Time-based One-Time Password) passcode - Provide the passcode from your authenticator app
- Passcode in password - Append the passcode to your password.
- MFA token caching - Cache the MFA token to skip prompts on reconnect.

Copy code

```
#!/usr/bin/env python
"""
This sample shows how to use Multi-Factor Authentication (MFA) with the
Snowflake Python Connector.

There are several ways to authenticate with MFA:
1. Push notification (Duo Push) - default behavior when no passcode is provided
2. TOTP passcode - provide the passcode from your authenticator app
3. Passcode in password - append the passcode to your password
4. MFA token caching - cache the MFA token to skip prompts on reconnect

Prerequisites:
- MFA must be enabled for your Snowflake user account
- You need a compatible authenticator app (such as Duo Mobile, Google Authenticator)
"""

import snowflake.connector

# Replace with your own Snowflake credentials
CONNECTION_PARAMETERS = {
    "account": "<account_name>",
    "user": "<user_name>",
    "password": "<password>",
    "database": "<database_name>",
    "schema": "<schema_name>",
    "warehouse": "<warehouse_name>",
}

def connect_with_mfa_push():
    """
    Example 1: MFA with Push Notification (Duo Push)

    When no passcode is provided, Snowflake sends a push notification
    to your registered device. You need to approve it to complete login.
    """
    print("Connecting with MFA push notification...")
    print("Please approve the push notification on your device.")

    with snowflake.connector.connect(
        **CONNECTION_PARAMETERS,
        authenticator="username_password_mfa",
    ) as conn:
        result = conn.cursor().execute("SELECT CURRENT_USER(), CURRENT_ROLE()").fetchone()
        print(f"Connected as: {result[0]}, Role: {result[1]}")

def connect_with_mfa_passcode(passcode: str):
    """
    Example 2: MFA with TOTP Passcode

    Provide the time-based one-time password (TOTP) from your
    authenticator app directly in the connection parameters.

    Args:
        passcode: The 6-digit TOTP code from your authenticator app
    """
    print(f"Connecting with MFA passcode: {passcode[:2]}****")

    with snowflake.connector.connect(
        **CONNECTION_PARAMETERS,
        authenticator="username_password_mfa",
        passcode=passcode,
    ) as conn:
        result = conn.cursor().execute("SELECT CURRENT_USER(), CURRENT_ROLE()").fetchone()
        print(f"Connected as: {result[0]}, Role: {result[1]}")

def connect_with_passcode_in_password(passcode: str):
    """
    Example 3: MFA with Passcode Appended to Password

    Instead of providing the passcode separately, you can append it
    to your password. This is useful for tools that don't support
    separate passcode parameters.

    Args:
        passcode: The 6-digit TOTP code from your authenticator app
    """
    print("Connecting with passcode appended to password...")

    # Create a copy of parameters with modified password
    params = CONNECTION_PARAMETERS.copy()
    params["password"] = params["password"] + passcode

    with snowflake.connector.connect(
        **params,
        authenticator="username_password_mfa",
        passcode_in_password=True,
    ) as conn:
        result = conn.cursor().execute("SELECT CURRENT_USER(), CURRENT_ROLE()").fetchone()
        print(f"Connected as: {result[0]}, Role: {result[1]}")

def connect_with_mfa_callback():
    """
    Example 4: MFA with Callback Function

    You can provide a callback function that gets called while waiting
    for MFA approval. This is useful for providing user feedback.
    """
    print("Connecting with MFA callback...")

    def mfa_callback():
        """Called while waiting for MFA approval."""
        print("  ... waiting for MFA approval ...")
        return None

    with snowflake.connector.connect(
        **CONNECTION_PARAMETERS,
        authenticator="username_password_mfa",
        mfa_callback=mfa_callback,
    ) as conn:
        result = conn.cursor().execute("SELECT CURRENT_USER(), CURRENT_ROLE()").fetchone()
        print(f"Connected as: {result[0]}, Role: {result[1]}")

def connect_with_mfa_token_caching():
    """
    Example 5: MFA with Token Caching

    Enable MFA token caching to skip MFA prompts on subsequent connections.
    The token is securely stored and reused for future connections.

    Note: This feature must also be enabled on the server side.
    client_store_temporary_credential defaults to True.
    """
    print("Connecting with MFA token caching enabled...")
    print("First connection - MFA required. Please approve.")

    # First connection - requires MFA approval
    with snowflake.connector.connect(
        **CONNECTION_PARAMETERS,
        authenticator="username_password_mfa",
        client_store_temporary_credential=True,
    ) as conn:
        result = conn.cursor().execute("SELECT CURRENT_USER()").fetchone()
        print(f"First connection successful as: {result[0]}")

    print("\nSecond connection - using cached MFA token (no prompt expected)...")

    # Second connection - should use cached token
    with snowflake.connector.connect(
        **CONNECTION_PARAMETERS,
        authenticator="username_password_mfa",
        client_store_temporary_credential=True,
    ) as conn:
        result = conn.cursor().execute("SELECT CURRENT_USER()").fetchone()
        print(f"Second connection successful as: {result[0]}")

if __name__ == "__main__":
    import sys

    print("Snowflake MFA Authentication Examples")
    print("=" * 40)

    if len(sys.argv) < 2:
        print(
            """
Usage: python auth_by_mfa.py <example> [passcode]

Examples:
  python auth_by_mfa.py push              # MFA with push notification
  python auth_by_mfa.py passcode 123456   # MFA with TOTP passcode
  python auth_by_mfa.py password 123456   # MFA with passcode in password
  python auth_by_mfa.py callback          # MFA with callback function
  python auth_by_mfa.py cache             # MFA with token caching
"""
        )
        sys.exit(1)

    example = sys.argv[1].lower()

    if example == "push":
        connect_with_mfa_push()
    elif example == "passcode":
        if len(sys.argv) < 3:
            print("Error: Please provide a passcode")
            sys.exit(1)
        connect_with_mfa_passcode(sys.argv[2])
    elif example == "password":
        if len(sys.argv) < 3:
            print("Error: Please provide a passcode")
            sys.exit(1)
        connect_with_passcode_in_password(sys.argv[2])
    elif example == "callback":
        connect_with_mfa_callback()
    elif example == "cache":
        connect_with_mfa_token_caching()
    else:
        print(f"Unknown example: {example}")
        sys.exit(1)
```

`client_store_temporary_credential` defaults to `True`, so MFA, SSO, and OAuth token caching is on unless you set it to `False`. `client_request_mfa_token` is still accepted and mapped to `client_store_temporary_credential`, but it emits a `DeprecationWarning`. See [Renamed and deprecated parameters](/developer-guide/python-connector/python-connector-upgrade#label-python-upgrade-renamed) and [Using MFA token caching to minimize the number of prompts during authentication — \*optional\*](/user-guide/security-mfa#label-mfa-token-caching).

Note

Before version 5.0, MFA caching used `client_request_mfa_token` and defaulted to `False`. On Linux, versions before 5.0 also needed the `secure-local-storage` extra (the keyring package).

## Using key-pair authentication and key-pair rotation

The Python connector supports key pair authentication and key rotation.

For more information on how to configure key pair authentication and key rotation, see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).

1. After completing the key pair authentication configuration, set the `private_key_file` parameter in the `connect` function to the path to the private key file. Also, set the `private_key_password` parameter to the passphrase of the private key file. The connector still accepts `private_key_file_pwd` and maps it to `private_key_password`, but using it emits a `DeprecationWarning`.

   Note

   Before version 5.0, the passphrase parameter was named `private_key_file_pwd`.
2. Modify and execute the sample code, below:

> - Update the security parameters:
>
>   - `path`: Specifies the local path to the private key file you created.
> - Update the connection parameters:
>
>   - `user`: Specifies your Snowflake login name.
>   - `account_identifier`: Specifies your [account identifier](/user-guide/gen-conn-config).
>
>     For more details, see [Usage notes for the `account` parameter (for the `connect` method)](/developer-guide/python-connector/python-connector-api#label-account-format-info).
>
> > **Sample code**
> >
> > Copy code
> >
> > ```
> > import os
> > import snowflake.connector as sc
> >
> > private_key_file = '<path>'
> > private_key_password = '<password>'
> >
> > conn_params = {
> >     'account': '<account_identifier>',
> >     'user': '<user>',
> >     'authenticator': 'SNOWFLAKE_JWT',
> >     'private_key_file': private_key_file,
> >     'private_key_password': private_key_password,
> >     'warehouse': '<warehouse>',
> >     'database': '<database>',
> >     'schema': '<schema>'
> > }
> >
> > ctx = sc.connect(**conn_params)
> > cs = ctx.cursor()
> > ```

## Using a proxy server

Set the proxy on the connection with `proxy_host`, `proxy_port`, `proxy_user`, `proxy_password`, and `no_proxy`. You can also pass a single `proxy` URL of the form `[scheme://][user:pass@]host[:port]`. When both are set, individual fields override the matching part of the URL.

The connector reads `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` unless you pass `use_proxy_env=False`. `use_proxy_env` defaults to `True`. When you also set `proxy_host` or `proxy_port`, the explicit parameters win and the environment variables are ignored.

Note

Before version 5.0 (since connector 3.17.0), the connector always read those environment variables, and a variable set in the environment overrode `proxy_host` and `proxy_port` on the connection.

Set the environment variables. The connector reads them by default:

Linux or macOS:
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

Pass `use_proxy_env=False` to ignore those variables:

Copy code

```
conn = snowflake.connector.connect(
    ...,
    use_proxy_env=False,
)
```

Tip

Snowflake’s security model does not allow Secure Sockets Layer (SSL) proxies (using an HTTPS certificate). Your proxy server must use a publicly-available Certificate Authority (CA), reducing potential security risks such as a MITM (Man In The Middle) attack through a compromised proxy.

If you must use your SSL proxy, we strongly recommend that you update the server policy to pass through the Snowflake certificate such that no certificate is altered in the middle of
communications.

Optionally `NO_PROXY` can be used to bypass the proxy for specific communications. For example, access to Amazon S3 can bypass the proxy server by specifying `NO_PROXY=".amazonaws.com"`.

`NO_PROXY` does not support wildcards. Each value specified should be one of the following:

- The end of a hostname (or a complete hostname), for example:

  - .amazonaws.com
  - myorganization-myaccount.snowflakecomputing.com
- An IP address, for example:

  - 192.196.1.15

If more than one value is specified, values should be separated by commas, for example:

> Copy code
>
> ```
> localhost,.example.com,.snowflakecomputing.com,192.168.1.15,192.168.1.16
> ```

## Connecting with OAuth

To connect using OAuth, the connection string must include the `authenticator` parameter set to `oauth` and the `token` parameter set to the `oauth_access_token`. For more information, see [Clients, drivers, and connectors](/user-guide/oauth-intro#label-oauth-intro-clients-drivers-conns).

Copy code

```
ctx = snowflake.connector.connect(
    user="<username>",
    host="<hostname>",
    account="<account_identifier>",
    authenticator="oauth",
    token="<oauth_access_token>",
    warehouse="test_warehouse",
    database="test_db",
    schema="test_schema"
)
```

### Enable the OAuth 2.0 Authorization Code flow

The OAuth 2.0 Authorization Code flow is a secure method for a client application to obtain an access token from an authorization server on behalf of a user, without revealing the user’s credentials.

To enable the OAuth 2.0 Authorization Code flow:

- Set the `authenticator` connection parameter to `OAUTH_AUTHORIZATION_CODE`.
- Set the following OAuth connection parameters:
  - `oauth_client_id`: Value of `client id` provided by the Identity Provider for Snowflake integration (Snowflake security integration metadata).
  - `oauth_client_secret`: Value of the `client secret` provided by the Identity Provider for Snowflake integration (Snowflake security integration metadata).
  - `oauth_authorization_url`: Identity Provider endpoint supplying the authorization code to the driver. When using Snowflake as an Identity Provider, this value is derived from the `server` or `account` parameters. The URL must use `https://`. `http://` is accepted only for a loopback host (`127.0.0.0/8`, `::1`, or `localhost`).

    Note

    Before version 5.0, the authorization-code flow already required `https://` for this URL and did not allow a loopback exception.
  - `oauth_token_request_url`: Identity Provider endpoint supplying the access tokens to the driver. When using Snowflake as an Identity Provider, this value is derived from the `server` or `account` parameters. The URL must use `https://`, except for a loopback host.

    Note

    Before version 5.0, an `http://` token URL logged a warning and the request continued.
  - `oauth_scope`: Scope requested in the Identity Provider authorization request. By default, it is derived from the role. When multiple scopes are required, the value should be a space-separated list of multiple scopes.
  - `oauth_redirect_uri`: URI to use for authorization code redirection (Snowflake security integration metadata). Default: `http://127.0.0.1:{randomAvailablePort}`.
  - `oauth_disable_pkce:` Disables Proof Key for Code Exchange (PKCE), a security enhancement that ensures that even if malicious attackers intercept an Authorization Code, they won’t be able to change it to a valid access token.
  - `oauth_enable_refresh_tokens`: Accepted for compatibility and ignored. The connector always uses a refresh token when the identity provider returns one, and emits a `DeprecationWarning` if you pass this parameter. Use `client_store_temporary_credential` to control whether that token is cached.

    Note

    Before version 5.0, the parameter defaulted to `True` and, when `False`, the connector did not use the refresh token to renew an expired access token.
  - `oauth_enable_single_use_refresh_tokens:` Whether to opt-in to single-use refresh token semantics.

### Enable the OAuth 2.0 Client Credentials flow

The OAuth 2.0 Client Credentials flow provides a secure way for machine-to-machine (M2M) authentication, such as the Snowflake Connector for Python connecting to a backend service. Unlike the OAuth 2.0 Authorization Code flow, this method does not rely on any user-specific data.

To enable the OAuth 2.0 Client Credentials flow:

- Set the `authenticator` connection parameter to `OAUTH_CLIENT_CREDENTIALS`.
- Set the following OAuth connection parameters:
  - `oauth_client_id`: Value of `client id` provided by the Identity Provider for Snowflake integration (Snowflake security integration metadata).
  - `oauth_client_secret`: Value of the `client secret` provided by the Identity Provider for Snowflake integration (Snowflake security integration metadata)
  - `oauth_token_request_url`: Identity Provider endpoint supplying the access tokens to the driver. When using Snowflake as an Identity Provider, this value is derived from the `server` or `account` parameters.
  - `oauth_scope`: Scope requested in the Identity Provider authorization request. By default, it is derived from the role. When multiple scopes are required, the value should be a space-separated list of multiple scopes.

## Authenticating with workload identity federation (WIF)

[Workload identity federation](/user-guide/workload-identity-federation) provides a service-to-service authentication method for Snowflake. This method enables applications, services, or containers to authenticate with Snowflake by leveraging their cloud provider’s native identity system, such as AWS IAM, Microsoft Entra ID, or Google Cloud service accounts. This approach eliminates the need for managing long-lived credentials and simplifies credential acquisition compared to other methods like External OAuth. Snowflake connectors are designed to automatically obtain short-lived credentials from the platform’s identity provider.

To enable the workload identity federation authenticator, do the following:

1. Set the `authenticator` connection parameter to `WORKLOAD_IDENTITY`.
2. Set the `workload_identity_provider` connection parameter to `AWS`, `AZURE`, `GCP`, or `OIDC`, based on your platform.
3. For OpenID Connect (OIDC), specify the `token` connection parameter.

## Authenticating with a programmatic access token (PAT)

Programmatic Access Token (PAT) is a Snowflake-specific authentication method. The feature must be enabled for the account before usage (see the [Prerequisites](/user-guide/programmatic-access-tokens#label-pat-prerequisites) for more information). Authentication with PAT doesn’t involve any human interaction.

For more information about PATs, see [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens).

## Managing connection timeouts

Calling `snowflake.connector.connect` submits a login request. If a login request fails, the connector can resend the connection request. The following parameters set the time limits:

- `login_timeout`: How long, in seconds, to keep retrying the login. The default is 120. When the budget is exhausted, the connector fails after the current attempt finishes. The property returns `120` when unset.

  Note

  Before version 5.0, the connector also used a 120-second budget, but `conn.login_timeout` returned `None` when you did not set the parameter.
- `query_timeout`: Wall-clock timeout, in seconds, for query execution including retries. The default is `0`, which means no timeout.
- `request_timeout`: Wall-clock timeout, in seconds, for other operations, such as closing the session and heartbeats, including retries. The default is 120. `0` means no timeout.
- `connect_timeout`: Timeout, in seconds, for establishing a single HTTP connection. There is no default cap.
- `retry_timeout`: Hard wall-clock cap, in seconds, on one HTTP attempt, including the response body. There is no default cap. A slow but active download counts against this cap.

`network_timeout` and `socket_timeout` are deprecated names. Passing either one emits a `DeprecationWarning`.

The `network_timeout` value is copied to both `query_timeout` and `request_timeout` unless you set one of those yourself. `conn.network_timeout` returns `request_timeout`. The `socket_timeout` value is copied to both `connect_timeout` and `retry_timeout`. Because `retry_timeout` caps the whole attempt, a value you previously used to detect a stalled socket can now abort an active chunk download.

Note

Before version 5.0, `network_timeout` was a single wall-clock budget for non-login HTTP operations and defaulted to no cap.

Note

Before version 5.0, `socket_timeout` was a per-attempt read-inactivity timeout that reset whenever bytes arrived, so an active download did not trip it.

Copy code

```
conn = snowflake.connector.connect(
    login_timeout=60,
    query_timeout=30,
    request_timeout=30,
    retry_timeout=10,
)
```

## Managing retry backoff

The connector waits between retries using four connection parameters:

- `retry_backoff_base_ms`: Initial delay in milliseconds. The default is 250.

  Note

  Before version 5.0, the default initial delay was 1 second.
- `retry_backoff_factor`: Multiplier applied after each retry. The default is 2.

  Note

  Before version 5.0, the default multiplier was also 2.
- `retry_backoff_cap_ms`: Maximum delay in milliseconds. The default is 16000.

  Note

  Before version 5.0, the default maximum delay was also 16000 milliseconds.
- `retry_backoff_jitter`: `none`, `full`, or `decorrelated`. The default is `decorrelated`.

  Note

  Before version 5.0, the default jitter was full jitter.

`backoff_policy` is not used. Passing it emits a `DeprecationWarning` and has no effect. The typed parameters cannot express an arbitrary generator.

Note

Before version 5.0, you passed a generator such as `exponential_backoff()` or your own generator, and that function computed the delay for every retry loop.

Copy code

```
conn = snowflake.connector.connect(
    retry_backoff_base_ms=250,
    retry_backoff_factor=2,
    retry_backoff_cap_ms=16000,
    retry_backoff_jitter="decorrelated",
)
```

## Certificate revocation checking

The connector does not check certificate revocation with OCSP. Revocation checking uses certificate revocation lists (CRLs), and it is off by default.

Set `crl_check_mode` to `DISABLED` (the default), `ADVISORY`, or `ENABLED`. `ENABLED` requires each certificate to have a valid CRL. `ADVISORY` rejects a certificate only when a CRL says it is revoked. Errors fetching or parsing a CRL do not fail the connection in `ADVISORY` mode.

Cache the lists with `crl_enable_memory_caching` and `crl_enable_disk_caching`. Both default to `True`. `enable_crl_cache` is accepted, emits a `DeprecationWarning`, and has no effect. Set both cache parameters to `False` to disable caching.

Note

Before version 5.0, `enable_crl_cache` (default `True`) was the master switch: `False` turned off both caches, and `enable_crl_file_cache` applied only when the master switch was on.

The names `cert_revocation_check_mode`, `enable_crl_memory_cache`, and `enable_crl_file_cache` are still accepted and mapped to the current names without a warning. Timeouts specified in milliseconds or hours are accepted under the old names and converted to the current second-based parameters. See [Renamed and deprecated parameters](/developer-guide/python-connector/python-connector-upgrade#label-python-upgrade-renamed).

Note

Before version 5.0, those timeouts were specified in milliseconds or hours.

If you enable CRL checking, confirm that the network can reach the CRL distribution points named in Snowflake’s certificate chain.

`connect()` does not reject `ocsp_fail_open` or `ocsp_response_cache_filename`. Both are unknown parameters: the driver warns and forwards the values as login session parameters. Neither value selects an OCSP mode. The OCSP response cache server (`ocsp*.snowflakecomputing.com:80`) is not used.

Note

Before version 5.0, the connector sent each certificate to an OCSP responder. `ocsp_fail_open` selected fail-open or fail-close, and `ocsp_response_cache_filename` set the OCSP response cache file.

## Running connectivity tests and diagnostics

Note

Running diagnostics for a connection requires the following:

- Snowflake Connector for Python version 3.9.1 or newer. The connector includes the same diagnostic parameters.
- Python version 3.11 or newer.

Note

Before version 5.0, the connector required Python 3.9 or newer.

If you encounter connectivity issues, you can run diagnostics directly within the connector. Snowflake Support might also request this information to help you with connectivity issues.

The diagnostics collection uses the following [connection](/developer-guide/python-connector/python-connector-api#label-snowflake-connector-methods-connect) parameters:

- `enable_connection_diag`: Whether to generate a diagnostic report.
- `connection_diag_log_path`: Absolute path for the generated report.
- `connection_diag_allowlist_path`: Absolute path to a JSON file containing the output of `SYSTEM$ALLOWLIST()` or `SYSTEM$ALLOWLIST_PRIVATELINK()`. Required only if the user defined in the connection does not have permission to run the system allowlist functions or if connecting to the account URL fails.

To configure a connection to generate diagnostics:

1. Configure the connection parameters:

   - Set your Snowflake account credential parameters.
   - Set `enable_connection_diag=True` in your `connect` parameters.
   - If desired, change the location for the generated report by setting the `connection_diag_log_path` parameter.

   For example:

   Copy code

   ```
   from snowflake import connector

   ctx = connector.connect(
        user=<user>,
        password=<password>,
        account=<account>,
        enable_connection_diag=True,
        connection_diag_log_path="<HOME>/diag-tests",
        )
   print('connected')
   ```
2. Execute the code snippet.
3. Review the diagnostic test output of the generated `SnowflakeConnectionTestReport.txt` file located in the specified log path.

You can review the report for any connectivity issues and discuss them with your network team. You can also provide the report to Snowflake Support for additional assistance.
