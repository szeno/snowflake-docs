# snow stage execute

Execute immediate all files from the stage path. Files can be filtered with a glob-like pattern, e.g. `@stage/*.sql`, `@stage/dev/*`. Only files with `.sql` extension will be executed.

## Syntax

Copy code

```
snow stage execute
  <stage_path>
  --on-error <on_error>
  --variable <variables>
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

`stage_path`
:   Stage path with files to be execute. For example \*@stage/dev/\*\*.

## Options

`--on-error [break|continue]`
:   What to do when an error occurs. Defaults to break. Default: break.

`--variable, -D TEXT`
:   Variables for the execution context; for example: *-D “<key>=<value>”*. For SQL files, variables are used to expand the template, and any unknown variable will cause an error (consider embedding quoting in the file).For Python files, variables are used to update the os.environ dictionary. Provided keys are capitalized to adhere to best practices. In case of SQL files string values must be quoted in *‘’* (consider embedding quoting in the file).

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

Note

Snowflake CLI does not support executing Python files for Python versions 3.12 and above.

- The command searches for files with a `.sql` extension in the specified `STAGE_PATH` and executes `EXECUTE IMMEDIATE` on each of them. `STAGE_PATH` can be:
  - Only a stage name, such as `@scripts`, which executes all `.sql` files from the stage.
  - Glob-like pattern, such as `@scripts/dir/*`, which executes `.sql` files from the *dir* directory.
  - Direct file path, such as `@scripts/script.sql`, which executes only the `script.sql` file from the `scripts`.

The `--silent` options hides intermediate messages with file execution results.

When using Jinja templates for the SQL files, you can pass template variables using `-D` (or `--variable`) option, such as `-D "<key>=<value>"`. You must enclose string values in single quotes (`''`).

## Examples

- Specify only a stage name to execute all `.sql` files in the stage:

  Copy code

  ```
  snow stage execute "@scripts"
  ```

  ```
  SUCCESS - scripts/script1.sql
  SUCCESS - scripts/script2.sql
  SUCCESS - scripts/dir/script.sql
  +------------------------------------------+
  | File                   | Status  | Error |
  |------------------------+---------+-------|
  | scripts/script1.sql    | SUCCESS | None  |
  | scripts/script2.sql    | SUCCESS | None  |
  | scripts/dir/script.sql | SUCCESS | None  |
  +------------------------------------------+
  ```
- Specify a glob-like pattern to execute all `.sql` files in the `dir` directory:

  Copy code

  ```
  snow stage execute "@scripts/dir/*"
  ```

  ```
  SUCCESS - scripts/dir/script.sql
  +------------------------------------------+
  | File                   | Status  | Error |
  |------------------------+---------+-------|
  | scripts/dir/script.sql | SUCCESS | None  |
  +------------------------------------------+
  ```
- Specify a glob-like pattern to execute only `.sql` files in the `dir` directory that begin with “script”, followed by one character:

  Copy code

  ```
  snow stage execute "@scripts/script?.sql"
  ```

  ```
  SUCCESS - scripts/script1.sql
  SUCCESS - scripts/script2.sql
  +---------------------------------------+
  | File                | Status  | Error |
  |---------------------+---------+-------|
  | scripts/script1.sql | SUCCESS | None  |
  | scripts/script2.sql | SUCCESS | None  |
  +---------------------------------------+
  ```
- Specify a direct file path with the `--silent` option:

  Copy code

  ```
  snow stage execute "@scripts/script1.sql" --silent
  ```

  ```
  +---------------------------------------+
  | File                | Status  | Error |
  |---------------------+---------+-------|
  | scripts/script1.sql | SUCCESS | None  |
  +---------------------------------------+
  ```
