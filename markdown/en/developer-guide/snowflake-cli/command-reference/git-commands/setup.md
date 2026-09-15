# snow git setup

Sets up a git repository object.

## Syntax

Copy code

```
snow git setup
  <repository_name>
  --connection <connection>
  --host <host>
  --port <port>
  --account <account>
  --user <user>
  --password <password>
  --authenticator <authenticator>
  --workload-identity-provider <workload_identity_provider>
  --private-key-file <private_key_file>
  --token <token>
  --token-file-path <token_file_path>
  --database <database>
  --schema <schema>
  --role <role>
  --warehouse <warehouse>
  --temporary-connection
  --mfa-passcode <mfa_passcode>
  --enable-diag
  --diag-log-path <diag_log_path>
  --diag-allowlist-path <diag_allowlist_path>
  --oauth-client-id <oauth_client_id>
  --oauth-client-secret <oauth_client_secret>
  --oauth-authorization-url <oauth_authorization_url>
  --oauth-token-request-url <oauth_token_request_url>
  --oauth-redirect-uri <oauth_redirect_uri>
  --oauth-scope <oauth_scope>
  --oauth-disable-pkce
  --oauth-enable-refresh-tokens
  --oauth-enable-single-use-refresh-tokens
  --client-store-temporary-credential
  --format <format>
  --verbose
  --debug
  --silent
  --enhanced-exit-codes
  --decimal-precision <decimal_precision>
```

## Arguments

`repository_name`
:   Identifier of the git repository; for example: my\_repo.

## Options

`--connection, -c, --environment TEXT`
:   Name of the connection, as defined in your *config.toml* file. Default: *default*.

`--host TEXT`
:   Host address for the connection. Overrides the value specified for the connection.

`--port INTEGER`
:   Port for the connection. Overrides the value specified for the connection.

`--account, --accountname TEXT`
:   Name assigned to your Snowflake account. Overrides the value specified for the connection.

`--user, --username TEXT`
:   Username to connect to Snowflake. Overrides the value specified for the connection.

`--password TEXT`
:   Snowflake password. Overrides the value specified for the connection.

`--authenticator TEXT`
:   Snowflake authenticator. Overrides the value specified for the connection.

`--workload-identity-provider TEXT`
:   Workload identity provider (AWS, AZURE, GCP, OIDC). Overrides the value specified for the connection.

`--private-key-file, --private-key-path TEXT`
:   Snowflake private key file path. Overrides the value specified for the connection.

`--token TEXT`
:   OAuth token to use when connecting to Snowflake.

`--token-file-path TEXT`
:   Path to file with an OAuth token to use when connecting to Snowflake.

`--database, --dbname TEXT`
:   Database to use. Overrides the value specified for the connection.

`--schema, --schemaname TEXT`
:   Database schema to use. Overrides the value specified for the connection.

`--role, --rolename TEXT`
:   Role to use. Overrides the value specified for the connection.

`--warehouse TEXT`
:   Warehouse to use. Overrides the value specified for the connection.

`--temporary-connection, -x`
:   Uses a connection defined with command-line parameters, instead of one defined in config. Default: False.

`--mfa-passcode TEXT`
:   Token to use for multi-factor authentication (MFA).

`--enable-diag`
:   Whether to generate a connection diagnostic report. Default: False.

`--diag-log-path TEXT`
:   Path for the generated report. Defaults to system temporary directory. Default: <system\_temporary\_directory>.

`--diag-allowlist-path TEXT`
:   Path to a JSON file that contains allowlist parameters.

`--oauth-client-id TEXT`
:   Value of client id provided by the Identity Provider for Snowflake integration.

`--oauth-client-secret TEXT`
:   Value of the client secret provided by the Identity Provider for Snowflake integration.

`--oauth-authorization-url TEXT`
:   Identity Provider endpoint supplying the authorization code to the driver.

`--oauth-token-request-url TEXT`
:   Identity Provider endpoint supplying the access tokens to the driver.

`--oauth-redirect-uri TEXT`
:   URI to use for authorization code redirection.

`--oauth-scope TEXT`
:   Scope requested in the Identity Provider authorization request.

`--oauth-disable-pkce`
:   Disables Proof Key for Code Exchange (PKCE). Default: *False*.

`--oauth-enable-refresh-tokens`
:   Enables a silent re-authentication when the actual access token becomes outdated. Default: *False*.

`--oauth-enable-single-use-refresh-tokens`
:   Whether to opt-in to single-use refresh token semantics. Default: *False*.

`--client-store-temporary-credential`
:   Store the temporary credential.

`--format [TABLE%JSON%JSON_EXT|CSV]`
:   Specifies the output format. Default: TABLE.

`--verbose, -v`
:   Displays log entries for log levels *info* and higher. Default: False.

`--debug`
:   Displays log entries for log levels *debug* and higher; debug logs contain additional information. Default: False.

`--silent`
:   Turns off intermediate output to console. Default: False.

`--enhanced-exit-codes`
:   Differentiate exit error codes based on failure type. Default: False.

`--decimal-precision INTEGER`
:   Number of decimal places to display for decimal values. Uses Python’s default precision if not specified. [env var: SNOWFLAKE\_DECIMAL\_PRECISION].

`--help`
:   Displays the help text for this command.

## Usage notes

The `snow git setup` command prompts for the following information:

- **URL**: address of repository to use for `git clone` operation.
- **Secret**: Snowflake secret containing authentication credentials. Not needed if origin repository does not require authentication for read-only operations, such as clone and fetch.
- **API integration**: object allowing Snowflake to interact with a Git repository.

If the role or user specified in your [connection](/developer-guide/snowflake-cli/connecting/configure-connections) has not been granted, executing this command generates an error similar to the following:

```
003001 (42501): 01b2f095-0508-c66d-0001-c1be009a66ee: SQL access control error: Insufficient privileges to operate on account XXX
```

In this situation, you should check your connection configuration or ask your account administrator to give you the necessary privileges or to create the integration for you. For more information, see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up).

## Examples

- Create a repository that requires a secret and credentials:

  Copy code

  ```
  $ snow git setup snowcli_git
  Origin url: https://github.com/snowflakedb/snowflake-cli.git
  Use secret for authentication? [y/N]: y
  Secret identifier (will be created if not exists) [snowcli_git_secret]: new_secret
  Secret 'new_secret' will be created
  username: john_doe
  password/token: ****
  API integration identifier (will be created if not exists) [snowcli_git_api_integration]:
  ```

  ```
  Secret 'new_secret' successfully created.
  API integration snowcli_git_api_integration successfully created.
  +------------------------------------------------------+
  | status                                               |
  |------------------------------------------------------|
  | Git Repository SNOWCLI_GIT was successfully created. |
  +------------------------------------------------------+
  ```
- Create a repository without a secret and an existing API integration ID:

  Copy code

  ```
  $ snow git setup snowcli_git
  Origin url: https://github.com/snowflakedb/snowflake-cli.git
  Use secret for authentication [y/N]: n
  API integration identifier (will be created if not exists) [snowcli_git_api_integration]: EXISTING_INTEGRATION
  ```

  ```
  Using existing API integration 'EXISTING_INTEGRATION'.
  +------------------------------------------------------+
  | status                                               |
  |------------------------------------------------------|
  | Git Repository SNOWCLI_GIT was successfully created. |
  +------------------------------------------------------+
  ```
