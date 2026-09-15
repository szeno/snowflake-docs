# snow dbt copy

Copies files between local directories, stages, or a dbt project object’s live version. This command behaves exactly like `snow stage copy`; it’s provided as a convenience when working with dbt project files.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

## Syntax

Copy code

```
snow dbt copy
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
  --protocol <protocol>
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
  --secondary-roles <secondary_roles>
  --server-session-keep-alive
  --format <format>
  --verbose
  --debug
  --silent
  --enhanced-exit-codes
  --decimal-precision <decimal_precision>
```

## Arguments

`source_path`
:   *Required*

    Source path for the copy operation. Can be a local path, a stage path, or a `snow://dbt/.../versions/live` path. You can use a glob pattern for local files, but the pattern must be enclosed in quotes.

`destination_path`
:   *Required*

    Target directory path for the copy operation. Can be a local path, a stage path, or a `snow://dbt/.../versions/live` path.

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
:   Specifies whether `ALTER STAGE {name} REFRESH` should be executed after uploading. Default: False.

`--connection, -c, --environment TEXT`
:   Name of the connection, as defined in your `config.toml` file. Default: `default`.

`--host TEXT`
:   Host address for the connection. Overrides the value specified for the connection.

`--port INTEGER`
:   Port for the connection. Overrides the value specified for the connection.

`--protocol TEXT`
:   Protocol to use for the connection, for example `https`. Overrides the value specified for the connection.

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
:   Disables Proof Key for Code Exchange (PKCE). Default: `False`.

`--oauth-enable-refresh-tokens`
:   Enables a silent re-authentication when the actual access token becomes outdated. Default: `False`.

`--oauth-enable-single-use-refresh-tokens`
:   Whether to opt-in to single-use refresh token semantics. Default: `False`.

`--client-store-temporary-credential`
:   Store the temporary credential.

`--secondary-roles TEXT`
:   Secondary roles mode applied when the session starts. Supported values are `ALL` and `NONE`; pass `NONE` to run the session only with the primary role.

`--server-session-keep-alive`
:   Keep the session active indefinitely, even if there is no activity from the user.

`--format [TABLE|JSON|JSON_EXT|CSV]`
:   Specifies the output format. Default: TABLE.

`--verbose, -v`
:   Displays log entries for log levels `info` and higher. Default: False.

`--debug`
:   Displays log entries for log levels `debug` and higher; debug logs contain additional information. Default: False.

`--silent`
:   Turns off intermediate output to console. Default: False.

`--enhanced-exit-codes`
:   Differentiate exit error codes based on failure type. Default: False.

`--decimal-precision INTEGER`
:   Number of decimal places to display for decimal values. Uses Python’s default precision if not specified. [env var: SNOWFLAKE\_DECIMAL\_PRECISION].

`--help`
:   Displays the help text for this command.

## Usage notes

Use the `versions/live` path to copy files into, out of, or between dbt project objects. A dbt project object path has the following form:

```
snow://dbt/<database>.<schema>.<dbt_project>/versions/live/<path>
```

`snow dbt copy` moves files between locations. It can persist files in the live version when that path is the destination. In contrast, repeatable `snow dbt execute --import` options mount files under `./imports/<alias>` only for an execution. For more information, see [snow dbt execute commands](/developer-guide/snowflake-cli/command-reference/dbt-commands/execute/overview).

## Examples

- Copy local dbt project files to a stage:

  Copy code

  ```
  snow dbt copy ./models/ @MY_DB.MY_SCHEMA.MY_STAGE/dbt/models/
  ```
- Copy from one stage to another:

  Copy code

  ```
  snow dbt copy @SOURCE_STAGE/dbt/ @DEST_STAGE/dbt/
  ```
- Copy a directory recursively, overwriting existing files:

  Copy code

  ```
  snow dbt copy ./project/ @MY_STAGE/dbt/ --recursive --overwrite
  ```
- Copy local model files into a dbt project object’s live version:

  Copy code

  ```
  snow dbt copy ./models/ \
    snow://dbt/MY_DB.MY_SCHEMA.MY_DBT_PROJECT/versions/live/models/ \
    --recursive \
    --overwrite
  ```
- Copy the live target artifacts to a local directory:

  Copy code

  ```
  snow dbt copy \
    snow://dbt/MY_DB.MY_SCHEMA.MY_DBT_PROJECT/versions/live/target/ \
    ./target/ \
    --recursive
  ```
- Copy files from one dbt project object’s live version into another:

  Copy code

  ```
  snow dbt copy \
    snow://dbt/MY_DB.MY_SCHEMA.SOURCE_PROJECT/versions/live/ \
    snow://dbt/MY_DB.MY_SCHEMA.DESTINATION_PROJECT/versions/live/imported/
  ```
- Copy target artifacts to another location in the same dbt project object’s live version:

  Copy code

  ```
  snow dbt copy \
    snow://dbt/MY_DB.MY_SCHEMA.MY_DBT_PROJECT/versions/live/target/ \
    snow://dbt/MY_DB.MY_SCHEMA.MY_DBT_PROJECT/versions/live/previous_target/
  ```
