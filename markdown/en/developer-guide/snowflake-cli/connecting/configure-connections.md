# Managing Snowflake connections

Before you can use Snowflake CLI, you must define connections, which specify how Snowflake CLI connects to Snowflake. Snowflake CLI uses the following precedence hierarchy to determine which value to use when a connection parameter is defined in multiple locations:

- Command-line parameters
- Environment variables overriding specific `config.toml` parameters, such as `SNOWFLAKE_CONNECTIONS_MYCONNECTION_PASSWORD`
- Connections defined in `config.toml` or `connections.toml`
- Generic environment variables, such as `SNOWFLAKE_USER`.

You can also use the `--temporary-connection` option, which does not require defining it in `config.toml`.

Caution

For improved security, Snowflake strongly recommends using either `SNOWFLAKE_CONNECTIONS_<NAME>_PASSWORD` or `SNOWFLAKE_PASSWORD` environment variables.

## Define connections

Connection definitions are stored in the `[connections]` section of the `config.toml` file, similar to the following block of code:

Copy code

```
[connections.myconnection]
account = "myaccount"
user = "jondoe"
password = "password"
warehouse = "my-wh"
database = "my_db"
schema = "my_schema"
```

Connection definitions support the same configuration options as the [Snowflake Connector for Python](/developer-guide/python-connector/python-connector-api#label-snowflake-connector-methods-connect).
Additionally, you can specify a default connection in the `default_connection_name` variable at the top of the file. You cannot include it
within a connection definition. For example:

Copy code

```
default_connection_name = "myconnection"

[connections.myconnection]
account = "myaccount"
...
```

Note

For macOS and Linux systems, Snowflake CLI requires the `config.toml` file to limit its file permissions to read and write for the file owner only. To set the required file permissions, execute the following commands:

Copy code

```
chown $USER config.toml
chmod 0600 config.toml
```

You can relax this check for files with `0644` permissions (readable by group or others) by setting `SF_SKIP_TOKEN_FILE_PERMISSIONS_VERIFICATION=true` or `SKIP_TOKEN_FILE_PERMISSIONS_VERIFICATION=true`. With either variable set, `config.toml` and `connections.toml` files with `0644` permissions emit a warning instead of a hard error, which aligns with the behavior of `snowflake-connector-python`. Files that are writable by group or others remain a hard error regardless of these environment variables.

### Use `connections.toml` to share connections with other tools

Snowflake CLI and other Snowflake developer tools (VS Code Extension, Cortex Code, SnowConvert) all read `connections.toml`, so connections you define there work across all of them.

Pick the setup that matches your tools:

- **Snowflake CLI only:** keep both connections and CLI settings in `config.toml`. You don’t need `connections.toml`.
- **Multiple Snowflake tools:** put shared connections in `connections.toml` and keep CLI-specific settings (such as `default_connection_name`) in `config.toml`.

Place `connections.toml` in the [same directory](/developer-guide/snowflake-cli/connecting/configure-cli#label-cli-config-locations) as `config.toml`. It should contain only connections, with section names that omit the `connections` prefix: `[connections.myconnection]` becomes `[myconnection]`.

Note

If both `config.toml` and `connections.toml` exist, Snowflake CLI reads connections from `connections.toml` and ignores those in `config.toml`.

## Manage or add your connections to Snowflake with the `snow connection` commands

The `snow connection` commands let you create, manage, and test Snowflake connections.

### Add a connection

Note

If you need to add a connection for Snowflake Open Catalog, see [Create a Snowflake CLI connection for Open Catalog](https://other-docs.snowflake.com/opencatalog/sso-configure-open-catalog#create-a-snowflake-cli-connection-for-open-catalog) in the
Open Catalog documentation. You might need to add this connection for tasks like configuring Open Catalog to use SSO.

To create a new connection and add it to the [configuration file](/developer-guide/snowflake-cli/connecting/configure-cli#label-cli-config-locations), do the following:

1. Execute the `snow connection add` command:

   Copy code

   ```
   snow connection add
   ```
2. When prompted, supply the required connection, account, and username parameters, as well as any other desired optional parameters. Note that additional parameters might be required depending on the authentication method you choose.

   ```
   Enter connection name: <connection_name>
   Enter account: <account>
   Enter user: <user-name>
   Enter password: <password>
   Enter role: <role-name>
   Enter warehouse: <warehouse-name>
   Enter database: <database-name>
   Enter schema: <schema-name>
   Enter host: <host-name>
   Enter port: <port-number>
   Enter region: <region-name>
   Enter authenticator: <authentication-method>
   Enter workload identity provider: <workload-identity-provider>
   Enter private key file: <path-to-private-key-file>
   Enter token file path: <path-to-mfa-token>
   Wrote new connection <connection-name> to config.toml
   ```

You can also add values for specific parameters on the command line, as shown:

Copy code

```
snow --config-file config.toml connection add -n myconnection2 --account myaccount2 --user jdoe2
```

Note

If the command finishes with an error, such as if the `--private-key-file` option references a non-existing file, the connection is not saved in the `config.toml` configuration file.

By default, the `snow connection add` command prompts for optional parameters if they are not specified on the command line. If you want to add connections without specifying some optional parameter, like `account`, and skip the interactive prompts, you can use the `--no-interactive` option, as shown:

Copy code

```
snow connection add -n myconnection2 --user jdoe2 --no-interactive
```

After adding a connection, you can [test the connection](#label-cli-test-connection) to make sure it works correctly.

### List defined connections

To list the available connections, enter the `snow connection list` command, as shown:

Copy code

```
snow connection list
```

```
+-------------------------------------------------------------------------------------------------+
| connection_name | parameters                                                       | is_default |
|-----------------+------------------------------------------------------------------+------------|
| myconnection    | {'account': 'myaccount', 'user': 'jondoe', 'password': '****',   | False      |
|                 | 'database': 'my_db', 'schema': 'my_schema', 'warehouse':         |            |
|                 | 'my-wh'}                                                         |            |
| myconnection2   | {'account': 'myaccount2', 'user': 'jdoe2'}                       | False      |
+-------------------------------------------------------------------------------------------------+
```

### Test and diagnose a connection

To test whether a connection can successfully connect to Snowflake, enter the `snow connection test` command, similar to the following:

Copy code

```
snow connection test -c myconnection2
```

```
+--------------------------------------------------+
| key             | value                          |
|-----------------+--------------------------------|
| Connection name | myconnection2                  |
| Status          | OK                             |
| Host            | example.snowflakecomputing.com |
| Account         | myaccount2                     |
| User            | jdoe2                          |
| Role            | ACCOUNTADMIN                   |
| Database        | not set                        |
| Warehouse       | not set                        |
+--------------------------------------------------+
```

If you encounter connectivity issues, you can run diagnostics directly within Snowflake CLI. Snowflake Support might also request this information to help you with connectivity issues.

The diagnostics collection uses the following `snow connection test` command options:

- `--enable-diag` to generate a diagnostic report.
- `--diag-log-path` to specify the absolute path for the generated report.
- `--diag-allowlist-path` to specify the absolute path to a JSON file containing the output of the SYSTEM$ALLOWLIST() or SYSTEM$ALLOWLIST\_PRIVATELINK() SQL commands. This option is required only if the user defined in the connection does not have permission to run the system allowlist functions or if connecting to the account URL fails.

The following example generates a diagnostic report for the `myconnection2` connection and stores it in the `~/report/SnowflakeConnectionTestReport.txt` file:

Copy code

```
snow connection test -c myconnection2 --enable-diag --diag-log-path $HOME/report
```

```
+----------------------------------------------------------------------------+
| key                  | value                                               |
|----------------------+-----------------------------------------------------|
| Connection name      | myconnection2                                       |
| Status               | OK                                                  |
| Host                 | example.snowflakecomputing.com                      |
| Account              | myaccount2                                          |
| User                 | jdoe2                                               |
| Role                 | ACCOUNTADMIN                                        |
| Database             | not set                                             |
| Warehouse            | not set                                             |
| Diag Report Location | /Users/<username>/SnowflakeConnectionTestReport.txt |
+----------------------------------------------------------------------------+
```

You can review the report for any connectivity issues and discuss them with your network team. You can also provide the report to Snowflake Support for additional assistance.

### Remove a connection

You can use the `snow connection remove` command to delete a specific connection, similar to the following:

Copy code

```
snow connection remove bad_connection
```

```
Removed connection bad_connection from /Users/jdoe/.snowflake/config.toml.
```

### Set the default connection

You can use the `snow connection set-default` command to specify which configuration Snowflake CLI should use as the default, overriding the `default_connection_name`
configuration file and `SNOWFLAKE_DEFAULT_CONNECTION_NAME` variables, if set.

The following example sets the default connection to `myconnection2`:

Copy code

```
snow connection set-default myconnection2
```

```
Default connection set to: myconnection2
```

Note

If both files exist, Snowflake CLI uses only connections from `connections.toml`. Snowflake CLI reads `default_connection_name` from `config.toml` only.

### Use environment variables for Snowflake credentials

You can specify Snowflake credentials in system environment variables instead of
in configuration files. You can use the following generic environment variables only to specify connection parameters:

- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_SCHEMA`
- `SNOWFLAKE_ROLE`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_AUTHENTICATOR`
- `SNOWFLAKE_PRIVATE_KEY_PATH`
- `SNOWFLAKE_PRIVATE_KEY_RAW`
- `SNOWFLAKE_SESSION_TOKEN`
- `SNOWFLAKE_MASTER_TOKEN`
- `SNOWFLAKE_TOKEN`
- `SNOWFLAKE_TOKEN_FILE_PATH`
- `SNOWFLAKE_OAUTH_CLIENT_ID`
- `SNOWFLAKE_OAUTH_CLIENT_SECRET`
- `SNOWFLAKE_OAUTH_AUTHORIZATION_URL`
- `SNOWFLAKE_OAUTH_TOKEN_REQUEST_URL`
- `SNOWFLAKE_OAUTH_REDIRECT_URI`
- `SNOWFLAKE_OAUTH_SCOPE`
- `SNOWFLAKE_OAUTH_DISABLE_PKCE`
- `SNOWFLAKE_OAUTH_ENABLE_REFRESH_TOKENS`
- `SNOWFLAKE_OAUTH_ENABLE_SINGLE_USE_REFRESH_TOKENS`
- `SNOWFLAKE_CLIENT_STORE_TEMPORARY_CREDENTIAL`
- `SNOWFLAKE_WORKLOAD_IDENTITY_PROVIDER`

### Pass connection parameters to the `snow` command

You can pass connection parameters directly in every `snow` command that requires a connection. For a full list of connection configuration parameters, execute the `snow sql --help` command, as shown. Note that the output shows only the section with the connection configuration options.

Copy code

```
snow sql --help
```

```
╭─ Connection configuration ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --connection,--environment             -c      TEXT     Name of the connection, as defined in your config.toml. Default: default.
│ --host                                         TEXT     Host address for the connection. Overrides the value specified for the connection.
│ --port                                         INTEGER  Port for the connection. Overrides the value specified for the connection.
│ --account,--accountname                        TEXT     Name assigned to your Snowflake account. Overrides the value specified for the connection.
│ --user,--username                              TEXT     Username to connect to Snowflake. Overrides the value specified for the connection.
│ --password                                     TEXT     Snowflake password. Overrides the value specified for the connection.
│ --authenticator                                TEXT     Snowflake authenticator. Overrides the value specified for the connection.
│ --private-key-file,--private-key-path          TEXT     Snowflake private key file path. Overrides the value specified for the connection.
│ --token                                        TEXT     OAuth token to use when connecting to Snowflake.
│ --token-file-path                              TEXT     Path to file with an OAuth token that should be used when connecting to Snowflake.
│ --database,--dbname                            TEXT     Database to use. Overrides the value specified for the connection.
│ --schema,--schemaname                          TEXT     Database schema to use. Overrides the value specified for the connection.
│ --role,--rolename                              TEXT     Role to use. Overrides the value specified for the connection.
│ --warehouse                                    TEXT     Warehouse to use. Overrides the value specified for the connection.
│ --temporary-connection                 -x               Uses connection defined with command-line parameters, instead of one defined in config.
│ --mfa-passcode                                 TEXT     Token to use for multi-factor authentication (MFA).
│ --oauth-client-id                              TEXT     Value of the client ID provided by the identity provider for Snowflake integration.
│ --oauth-client-secret                          TEXT     Value of the client secret provided by the identity provider for Snowflake integration.
│ --oauth-authorization-url                      TEXT     Identity provider endpoint supplying the authorization code to the driver.
│ --oauth-token-request-url                      TEXT     Identity provider endpoint supplying the access tokens to the driver.
│ --oauth-redirect-uri                           TEXT     URI to use for the authorization code.
│ --oauth-scope                                  TEXT     Scope requested in the identity provider authorization request.
│ --oauth-disable-pkce                                    Disables Proof Key for Code Exchange (PKCE). Default: False.
│ --oauth-enable-refresh-tokens                           Enables a silent re-authentication when the actual access token becomes outdated. Default: False.
│ --oauth-enable-single-use-refresh-tokens                Whether to opt in to single-use refresh token semantics. Default: False.
│ --client-store-temporary-credential                     Store the temporary credential.
│ --enable-diag                                           Run the python connector diagnostic test.
│ --diag-log-path                                TEXT     Diagnostic report path.
│ --diag-allowlist-path                          TEXT     Diagnostic report path to optional allowlist.
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Caution

For improved security, Snowflake strongly recommends using either `SNOWFLAKE_CONNECTIONS_<NAME>_PASSWORD` or `SNOWFLAKE_PASSWORD` environment variables.

## Import connections from SnowSQL

Snowflake CLI is an open-source command-line tool explicitly designed for developer-centric workloads in addition to SQL operations. Snowflake CLI is a more modern, robust, and efficient CLI client than legacy SnowSQL. In addition to executing SQL commands with Snowflake CLI, you can also execute commands for other Snowflake products like Streamlit in Snowflake, Snowpark Container Services, and Snowflake Native App Framework. Because new features and enhancements will be added only to Snowflake CLI, Snowflake recommends that you begin transitioning from SnowSQL to Snowflake CLI.

To import any existing connections defined in [SnowSQL](/user-guide/snowsql) into your Snowflake CLI `config.toml` configuration file, use the `snow helpers import-snowsql-connections` command.

To import SnowSQL connections, enter the `snow helpers import-snowsql-connections` command similar to the following code block that imports SnowSQL connections from the standard configuration file locations:

Copy code

```
snow helpers import-snowsql-connections
```

As the command processes the SnowSQL configuration files, it shows the progress and prompts for confirmation when a connection with the same name is already defined in the Snowflake CLI `config.toml` file:

```
SnowSQL config file [/etc/snowsql.cnf] does not exist. Skipping.
SnowSQL config file [/etc/snowflake/snowsql.cnf] does not exist. Skipping.
SnowSQL config file [/usr/local/etc/snowsql.cnf] does not exist. Skipping.
Trying to read connections from [/Users/<user>/.snowsql.cnf].
Reading SnowSQL's connection configuration [connections.connection1] from [/Users/<user>/.snowsql.cnf]
Trying to read connections from [/Users/<user>/.snowsql/config].
Reading SnowSQL's default connection configuration from [/Users/<user>/.snowsql/config]
Reading SnowSQL's connection configuration [connections.connection1] from [/Users/<user>/.snowsql/config]
Reading SnowSQL's connection configuration [connections.connection2] from [/Users/<user>/.snowsql/config]
Connection 'connection1' already exists in Snowflake CLI, do you want to use SnowSQL definition and override existing connection in Snowflake CLI? [y/N]: Y
Connection 'connection2' already exists in Snowflake CLI, do you want to use SnowSQL definition and override existing connection in Snowflake CLI? [y/N]: n
Connection 'default' already exists in Snowflake CLI, do you want to use SnowSQL definition and override existing connection in Snowflake CLI? [y/N]: n
Saving [connection1] connection in Snowflake CLI's config.
Connections successfully imported from SnowSQL to Snowflake CLI.
```

For more information about this command, see the [snow helpers import-snowsql-connections](/developer-guide/snowflake-cli/command-reference/helpers-commands/import-snowsql-connections) command reference.

For help with migrating from SnowSQL to Snowflake CLI, see [Migrating from SnowSQL to Snowflake CLI](/user-guide/snowsql-migrate).

## Use a temporary connection

You can also specify connection parameters from the command line using the `--temporary-connection [-x]` option. It ignores all definitions from the `config.toml`, using ones specified by command-line options instead. This approach can be helpful for CI/CD use cases when you don’t want to use a configuration file. When you use a temporary connection, Snowflake CLI ignores any connection variables defined in the `config.toml` file, but does still use any of the following [environment variables](#label-snowcli-environment-creds) you set:

- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_SCHEMA`
- `SNOWFLAKE_ROLE`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_AUTHENTICATOR`
- `SNOWFLAKE_PRIVATE_KEY_FILE`
- `SNOWFLAKE_PRIVATE_KEY_RAW`
- `SNOWFLAKE_PRIVATE_KEY_PATH`
- `SNOWFLAKE_SESSION_TOKEN`
- `SNOWFLAKE_MASTER_TOKEN`
- `SNOWFLAKE_TOKEN_FILE_PATH`
- `WORKLOAD_IDENTITY_PROVIDER`

The following example shows how to create a temporary connection using a username and password. This example assumes you stored the password in the `SNOWFLAKE_PASSWORD` environment variable.

Copy code

```
snow sql -q "select 42;" --temporary-connection \
                           --account myaccount \
                           --user jdoe
```

```
select 42;
+----+
| 42 |
|----|
| 42 |
+----+
```

Caution

For improved security, Snowflake strongly recommends using either `SNOWFLAKE_CONNECTIONS_<NAME>_PASSWORD` or `SNOWFLAKE_PASSWORD` environment variables.

For additional security, you can use a [private key file](#label-snowcli-private-key) and store the path to your private key file in the `SNOWFLAKE_PRIVATE_KEY_FILE` environment variable, as shown:

Copy code

```
SNOWFLAKE_ACCOUNT = "account"
SNOWFLAKE_USER = "user"
SNOWFLAKE_PRIVATE_KEY_FILE = "/path/to/key.p8"
```

You can then create a temporary connection without specifying the options, as shown:

Copy code

```
snow sql -q "select 42" --temporary-connection
```

```
select 42;
+----+
| 42 |
|----|
| 42 |
+----+
```

When using CI/CD pipelines with key pair authentication, you might not be able to access local private key files (`SNOWFLAKE_PRIVATE_KEY_FILE`). In this situation, you can store the private key in the `SNOWFLAKE_PRIVATE_KEY_RAW` environment variable, as shown:

Copy code

```
SNOWFLAKE_ACCOUNT = "account"
SNOWFLAKE_USER = "user"
SNOWFLAKE_PRIVATE_KEY_RAW = "-----BEGIN PRIVATE KEY-----..."
```

You can then create a temporary connection without specifying the options, as shown:

Copy code

```
snow sql -q "select 42" --temporary-connection
```

```
select 42;
+----+
| 42 |
|----|
| 42 |
+----+
```

Note

If you use the `SNOWFLAKE_PRIVATE_KEY_RAW` environment variable, you should not also define `SNOWFLAKE_PRIVATE_KEY_FILE`.

## Additional ways to authenticate your connection

You can also use the following methods to authenticate your connection to Snowflake:

- [Use a private key file for authentication](#label-snowcli-private-key)
- [Use OAuth authentication](#label-snowcli-oauth)
- [Use the OAuth 2.0 Authorization Code flow](#label-snowcli-oauth-code-flow)
- [Use the OAuth 2.0 Client Credentials flow](#label-snowcli-oauth-client-flow)
- [Use multi-factor authentication (MFA)](#label-snowcli-mfa)
- [Use MFA caching](#label-snowcli-mfa-caching)
- [Use SSO (single sign-on)](#label-snowcli-sso)
- [Use an external browser](#label-snowcli-externalbrowser)
- [Use PAT (Programmatic Access Token)](#label-snowcli-pat)
- [Use workload identity federation (WIF)](#label-snowcli-wif)

### Use a private key file for authentication

To use a private key file for authentication, your connection configuration requires you to set the `authenticator`
parameter to `SNOWFLAKE_JWT` and provide the path to the file with your private key similar to the following:

- Specify the `--private-key-file` option in the `snow connection add` command, as shown:

  Copy code

  ```
  snow connection add \
  --connection-name jwt \
  --authenticator SNOWFLAKE_JWT \
  --private-key-file ~/.ssh/sf_private_key.p8
  ```
- Use the configuration file:

  Copy code

  ```
  [connections.jwt]
  account = "my_account"
  user = "jdoe"
  authenticator = "SNOWFLAKE_JWT"
  private_key_file = "~/sf_private_key.p8"
  ```

For more details on configuring key pair authentication, see [Key-pair authentication and key-pair rotation](/user-guide/key-pair-auth).

Snowflake CLI looks for the private key in the connection parameters in the following order:

1. If `private_key_file` is specified, Snowflake CLI reads the key from the specified file path.
2. If `private_key_path` is specified, Snowflake CLI reads the key from the specified file path.
3. If `private_key_file` or `private_key_path` are not specified, Snowflake CLI reads the key directly from the `private_key_raw` parameter.

Caution

If you specify your private key in the `private_key_raw` parameter,
Snowflake recommends using either the `SNOWFLAKE_CONNECTIONS_<NAME>_PRIVATE_KEY_RAW`
or the `SNOWFLAKE_PRIVATE_KEY_RAW` environment variables for improved security.

Note

If your private key is passphrase-protected, set the `PRIVATE_KEY_PASSPHRASE` environment variable to that passphrase.

### Use OAuth authentication

To connect using OAuth, you can do either of the following:

- Specify the `--token-file-path` option in the `snow connection add` command, as shown:

  Copy code

  ```
  snow connection add --token-file-path "my-token.txt"
  ```
- In the `config.toml` file, set `authenticator = "OAUTH"`, and add the `token_file_path` parameter to the connection definition, as shown:

  Copy code

  ```
  [connections.oauth]
  account = "my_account"
  user = "jdoe"
  authenticator = "OAUTH"
  token_file_path = "my-token.txt"
  ```

### Use the OAuth 2.0 Authorization Code flow

The OAuth 2.0 Authorization Code flow is a secure method for a client application to obtain an access token from an authorization server on behalf of a user, without revealing the user’s credentials. For more information about this flow and its parameters, see [Enable the OAuth 2.0 Authorization Code flow](/developer-guide/python-connector/python-connector-connect#label-python-oauth-code-flow) in the Snowflake Connector for Python documentation.

To use the OAuth 2.0 Authorization Code flow, add a connection definition to your `config.toml` file similar to the following:

Copy code

```
[connections.oauth]
authenticator = "OAUTH_AUTHORIZATION_CODE"
user = "user"
account = "account"
oauth_client_id = "client_id"
oauth_client_secret = "client_secret"
oauth_redirect_uri = "http://localhost:8001/snowflake/oauth-redirect"
oauth_scope = "session:role:PUBLIC"
```

### Use the OAuth 2.0 Client Credentials flow

The OAuth 2.0 Client Credentials flow provides a secure way for machine-to-machine (M2M) authentication, such as the Snowflake Connector for Python connecting to a backend service. Unlike the OAuth 2.0 Authorization Code flow, this method does not rely on any user-specific data. For more information about this flow and its parameters, see [Enable the OAuth 2.0 Client Credentials flow](/developer-guide/python-connector/python-connector-connect#label-python-oauth-client-flow) in the Snowflake Connector for Python documentation.

To use the OAuth 2.0 Client Credentials flow, add a connection definition to your `config.toml` file similar to the following:

Copy code

```
[connections.oauth]
authenticator = "OAUTH_CLIENT_CREDENTIALS"
user = "user"
account = "account"
oauth_client_id = "client_id"
oauth_client_secret = "client_secret"
oauth_token_request_url = "http://identity.provider.com/token"
oauth_scope = "session:role:PUBLIC"
```

### Use multi-factor authentication (MFA)

To use MFA:

1. Set up [multi-factor authentication](/user-guide/security-mfa) in Snowflake and set the `authenticator` parameter to `SNOWFLAKE` (which is a default value).
2. If you want to use a Duo-generated passcode instead of the push mechanism, use either the `--mfa-passcode <passcode>` option or set `passcode_in_password = true` in the `config.toml` file and include the passcode in your password as described in [Using MFA with Python](/user-guide/security-mfa#label-security-mfa-python).

   Note

   If you want to use the passcode in the password for authentication, after executing the first `snow` command, you can no longer provide the passcode as long as the token is valid. You must do the following:

   - Remove the passcode from the password.
   - Remove or comment the `passcode_in_password = true` in the `config.toml` file.

### Use MFA caching

MFA caching is a security feature that reduces the frequency of Multi-Factor Authentication (MFA) prompts during logins. Frequent MFA prompts can disrupt workflow and decrease productivity. MFA caching addresses this issue by securely storing MFA session information for a specified period. Using MFA caching lets you authenticate without repeatedly entering MFA codes, as long as they are within the cached session’s timeframe.

To enable MFA caching:

1. For your account, set `ALLOW_CLIENT_MFA_CACHING = true`:

   Copy code

   ```
   ALTER ACCOUNT SET ALLOW_CLIENT_MFA_CACHING = TRUE;
   ```
2. In your `config.toml` file, add `authenticator = "USERNAME_PASSWORD_MFA"` to your connection:

   Copy code

   ```
   [connections.myconnection]
   account = "my_account"
   user = "jdoe"
   password = "my_password"
   authenticator = "USERNAME_PASSWORD_MFA"
   ```

With MFA caching enabled, you approve the MFA prompt once, and subsequent `snow` commands reuse the
cached token until it expires. Without it, every `snow` command that opens a new connection issues a
new MFA prompt.

Note

On Linux, token caching also requires secure credential storage, such as keyring with a Secret
Service backend. Without it, you are prompted on every connection even when the account parameter
and the connection are both configured as described.

For more information, see [Using MFA token caching to minimize the number of prompts during authentication — \*optional\*](/user-guide/security-mfa#label-mfa-token-caching).

### Use SSO (single sign-on)

If you have [configured Snowflake to use single sign-on (SSO)](/user-guide/admin-security-fed-auth-overview), you can configure your client application to use SSO for authentication. See [Using SSO with client applications that connect to Snowflake](/user-guide/admin-security-fed-auth-use#label-sso-with-command-line-clients) for details and configure your connection using the instructions for Python.

### Use an external browser

You can use your browser to authenticate your Snowflake CLI connection with any SAML 2.0 compliant identity provider (IdP), such as Okta or Active Directory Federation Services.

Note

The `externalbrowser` authenticator is only supported in terminal windows that have web browser access. For example, a terminal window on a remote machine accessed through an SSH (Secure Shell) session might require additional setup to open a web browser.

If you don’t have access to a web browser, but your IdP is Okta, you can use native Okta by setting the authenticator to `https://<okta_account_name>.okta.com`.

To use external browser authentication, use one of the following methods:

- Use the `snow connection add --authenticator` command option:

  Copy code

  ```
  snow connection add --authenticator EXTERNALBROWSER
  ```
- Set `authenticator` to `EXTERNALBROWSER` in your `config.toml` file:

  Copy code

  ```
  [connections.externalbrowser]
  account = "my_account"
  user = "jdoe"
  authenticator = "EXTERNALBROWSER"
  ```

### Use PAT (Programmatic Access Token)

Programmatic Access Token (PAT) is a Snowflake-specific authentication method. The feature must be enabled for the account before usage (see the [Prerequisites](/user-guide/programmatic-access-tokens#label-pat-prerequisites) for more information). Authentication with PAT doesn’t involve any human interaction.

To use PAT with the connection, set `authenticator` to `PROGRAMMATIC_ACCESS_TOKEN` and `token_file_path` to point to the file with the token, as shown:

Copy code

```
[connections.externalbrowser]
account = "my_account"
user = "jdoe"
authenticator = "PROGRAMMATIC_ACCESS_TOKEN"
token_file_path = "path-to-pat-token"
```

For more information about PATs, see [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens).

### Use workload identity federation (WIF)

Workload identity federation (WIF) is a feature that allows you to use your CI/CD environment’s identity to authenticate to Snowflake without the need for static credentials. This is particularly useful in automated workloads, where you want to minimize the risk of credential exposure.

For more information, see [Workload identity federation](/user-guide/workload-identity-federation).

#### Set up WIF connections

To set up a WIF connection, you need to create a service account in Snowflake using the following steps:

1. Create a service user in Snowflake with the proper WORKLOAD\_IDENTITY:

> Copy code
>
> ```
> CREATE USER <username>
> WORKLOAD_IDENTITY = (
>   TYPE = <WIF type>
>   // ...
> )
> TYPE = SERVICE
> DEFAULT_ROLE = PUBLIC;
> ```

1. Configure a connection in Snowflake CLI using either of the following methods
   - Add the connection to the `config.toml` file

     Copy code

     ```
     [connections.my_wif_conn]
     account = "my_account"
     authenticator = "WORKLOAD_IDENTITY"
     workload_identity_provider = "<provider type>"
     ```
   - Use the `snow connection add` command:

     Copy code

     ```
     snow connection add \
      --connection-name my_wif_conn \
      --account <account> \
      --authenticator WORKLOAD_IDENTITY \
      --workload-identity-provider <provider type>
     ```

where:

> `<provider type>` is one of the following:
>
> - AWS
> - AZURE
> - GCP
> - OIDC

Note

When using OIDC as a provider, you need to retrieve the token from your environment and provide it to the CLI. You can provide the retrieved token via

- `--token` parameter
- `SNOWFLAKE_TOKEN` environment variable
- `SNOWFLAKE_CONNECTIONS_<connection_name>_TOKEN` environment variable
- `token_file_path` in your `config.toml` file

For more information, see [Snowflake CLI GitHub Action](/developer-guide/snowflake-cli/cicd/github-action).

#### Connect to Snowflake using a temporary WIF connection

To connect to Snowflake using a [temporary connection](#label-snowcli-temporary-connection), you can use the following command:

Copy code

```
snow sql -x \
--authenticator WORKLOAD_IDENTITY \
--workload-identity-provider AWS \
--account <my_account> \
-q 'select current_user()'

select current_user();
+----------------+
| CURRENT_USER() |
|----------------|
| <user name>    |
+----------------+
```
