# snow stage copy

Copies all files from source path to target directory. This works for uploading to and downloading files from the stage, and copying between named stages.

## Syntax

Copy code

```
snow stage copy
  <source_path>
  <destination_path>
  --overwrite / --no-overwrite
  --parallel <parallel>
  --recursive / --no-recursive
  --auto-compress / --no-auto-compress
  --refresh / --no-refresh
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

`source_path`
:   Source path for copy operation. Can be either stage path or local. You can use a glob pattern for local files but the pattern has to be enclosed in quotes.

`destination_path`
:   Target directory path for copy operation.

## Options

`--overwrite / --no-overwrite`
:   Overwrites existing files in the target path. Default: False.

`--parallel INTEGER`
:   Number of parallel threads to use when uploading files. Default: 4.

`--recursive / --no-recursive`
:   Copy files recursively with directory structure. Default: False.

`--auto-compress / --no-auto-compress`
:   Specifies whether Snowflake uses gzip to compress files during upload. Ignored when downloading. Default: False.

`--refresh / --no-refresh`
:   Specifies whether ALTER STAGE {name} REFRESH should be executed after uploading. Default: False.

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

- One of `SOURCE_PATH` or `DESTINATION_PATH` must be a local directory, while the other should be a directory in the Snowflake stage. The stage path must start with “@”. For example:

  - `snow stage copy @my_stage dir/` - copies files from `my_stage` stage to the local `dir` directory.
  - `snow stage copy dir/ @my_stage` - copies files from the local `dir` directory to `my_stage`.
- You can specify multiple files matching a regular expression by using a glob pattern for the `source_path` argument. You must enclose the glob pattern in single or double quotes.

## Examples

- To copy files from the local machine to a stage, use a command similar to the following:

  Copy code

  ```
  snow stage copy local_example_app @example_app_stage/app
  ```

  ```
  put file:///.../local_example_app/* @example_app_stage/app4 auto_compress=false parallel=4 overwrite=False
  +--------------------------------------------------------------------------------------
  | source           | target           | source_size | target_size | source_compression...
  |------------------+------------------+-------------+-------------+--------------------
  | environment.yml  | environment.yml  | 62          | 0           | NONE             ...
  | snowflake.yml    | snowflake.yml    | 252         | 0           | NONE             ...
  | streamlit_app.py | streamlit_app.py | 109         | 0           | NONE             ...
  +--------------------------------------------------------------------------------------
  ```
- To download files from a stage to a local directory, use a command similar to the following:

  Copy code

  ```
  mkdir local_app_backup
  snow stage copy @example_app_stage/app local_app_backup
  ```

  ```
  get @example_app_stage/app file:///.../local_app_backup/ parallel=4
  +------------------------------------------------+
  | file             | size | status     | message |
  |------------------+------+------------+---------|
  | environment.yml  | 62   | DOWNLOADED |         |
  | snowflake.yml    | 252  | DOWNLOADED |         |
  | streamlit_app.py | 109  | DOWNLOADED |         |
  +------------------------------------------------+
  ```
- The following example copies all `.txt` files in a directory to a stage.

  Copy code

  ```
  snow stage copy "testdir/*.txt" @TEST_STAGE_3
  ```

  ```
  put file:///.../testdir/*.txt @TEST_STAGE_3 auto_compress=false parallel=4 overwrite=False
  +------------------------------------------------------------------------------------------------------------+
  | source | target | source_size | target_size | source_compression | target_compression | status   | message |
  |--------+--------+-------------+-------------+--------------------+--------------------+----------+---------|
  | b1.txt | b1.txt | 3           | 16          | NONE               | NONE               | UPLOADED |         |
  | b2.txt | b2.txt | 3           | 16          | NONE               | NONE               | UPLOADED |         |
  +------------------------------------------------------------------------------------------------------------+
  ```
