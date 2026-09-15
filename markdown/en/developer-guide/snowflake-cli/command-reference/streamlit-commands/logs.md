# snow streamlit logs

Streams live logs from a deployed Streamlit app to your terminal. The command reads the Streamlit app name from the project definition file (`snowflake.yml`) or from the `--name` option, connects to the app’s developer log service, and prints log entries in real time. Press Ctrl+C to stop streaming.

Log streaming requires the SPCSv2 container runtime.

## Syntax

Copy code

```
snow streamlit logs
  <entity_id>
  --name <name>
  --tail <tail>
  --project <project_definition>
  --env <env_overrides>
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

`entity_id`
:   Optional. ID of the Streamlit entity in the project definition file. If omitted, use `--name` to identify the app directly.

## Options

`--name TEXT`
:   Fully qualified name of the Streamlit app (for example, `my_app`, `schema.my_app`, or `db.schema.my_app`). Overrides the project definition when provided.

`--tail, -n INTEGER RANGE`
:   Number of historical log lines to fetch before the live stream begins. Pass `0` for live logs only. Allowed range is `0`–`1000`. Default: `100`.

`-p, --project TEXT`
:   Path where the Snowflake project is stored. Defaults to the current working directory.

`--env TEXT`
:   String in the format `key=value`. Overrides variables from the `env` section used for templates.

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

The `streamlit logs` command attaches to the running container of a deployed Streamlit app and streams log entries until you stop the command with Ctrl+C. Note the following requirements:

- The Streamlit app must already be deployed and running on the SPCSv2 container runtime. If the app uses an earlier runtime, the command exits with an error from the runtime check.
- You must use the same Snowflake connection (or override values) that has access to the app’s database, schema, and role.
- Pair the command with the global `--format` option to convert the live stream to JSON or CSV for downstream piping. For example, `snow streamlit logs my_app --format json | jq ...`.
- Use the `--tail` option to control how many historical log lines are sent before the live stream begins. Pass `--tail 0` to receive only new log entries.

## Examples

- Stream live logs (and the most recent 100 historical lines) for the Streamlit app defined in the current project’s `snowflake.yml`:

  Copy code

  ```
  snow streamlit logs
  ```
- Stream live logs for a specific app by fully qualified name, without a project definition:

  Copy code

  ```
  snow streamlit logs --name my_db.public.my_streamlit_app
  ```
- Stream only live entries (no historical lines) and pipe the JSON-formatted stream to another tool:

  Copy code

  ```
  snow streamlit logs my_streamlit --tail 0 --format json
  ```
- When several Streamlit entities are defined in `snowflake.yml`, target one by entity ID:

  Copy code

  ```
  snow streamlit logs my_streamlit_entity --tail 500
  ```
