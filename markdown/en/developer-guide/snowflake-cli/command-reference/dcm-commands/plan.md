# snow dcm plan

Shows what objects would be created, altered, or dropped by the `deploy` command, without applying any changes.

## Syntax

Copy code

```
snow dcm plan
  <identifier>
  --from <from_location>
  --delta
  --variable <variables>
  --target <target>
  --save-output
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

`identifier`
:   Identifier of DCM Project. Example: MY\_DB.MY\_SCHEMA.MY\_PROJECT. Supports fully qualified (recommended) or simple names. If unqualified, it defaults to the connection’s database and schema. Optional if *–target* or *default\_target* is defined in the manifest.

## Options

`--from PATH`
:   Local directory path containing DCM project files. Omit to use current directory.

`--delta`
:   Only evaluates definitions that changed since the last deployment, and any downstream definitions that depend on
    them, instead of comparing all definitions against the current account state. Default: False.

`--variable, -D TEXT`
:   Variables for the execution context; for example: *-D “<key>=<value>”*.

`--target TEXT`
:   Target profile from *manifest.yml* to use. Uses *default\_target* if not specified.

`--save-output`
:   Save command response and artifacts to local ‘out/’ directory. Default: False.

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

`--format [TABLE|JSON|JSON_EXT|CSV]`
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

The `snow dcm plan` command validates a DCM project object and simulates what would happen if the `deploy` command were executed, printing the computed changeset as a result. No Snowflake objects are created, altered, or dropped when you run this command.

Note

This command automatically uploads local source SQL files to a temporary stage in Snowflake so their content impacts the final result of the operation.

Use the `--save-output` option to save the plan results to a local `out/plan.json` file.

Use `--delta` during active development to get faster feedback on incremental changes. Because it skips unchanged
definitions, it doesn’t detect changes that happened outside of DCM Projects on your account since the last deployment.
Always run a full `snow dcm plan` before deploying.

## Examples

- Plan a DCM project object with the default options, where the project name is specified in the target identified by the `default_target` property in the manifest:

  Copy code

  ```
  snow dcm plan
  ```
- Plan a DCM project project where the project name is specified in the `DEV` target in the manifest:

  Copy code

  ```
  snow dcm plan --target DEV
  ```
- Plan a DCM project object with an explicit fully qualified name:

  Copy code

  ```
  snow dcm plan MY_DB.MY_SCHEMA.MY_PROJECT
  ```
- Plan a DCM project project using local files, where the project name is specified in the `DEV` target in the manifest, set the value for the `db_name` variable, and set the deployment alias to `v3`:

  Copy code

  ```
  snow dcm plan --target DEV --variable db_name=jdoe --alias v3
  ```
- Plan a DCM project object and save the plan output locally:

  Copy code

  ```
  snow dcm plan --save-output
  ```
- Plan only the definitions that changed since the last deployment:

  Copy code

  ```
  snow dcm plan --delta
  ```
