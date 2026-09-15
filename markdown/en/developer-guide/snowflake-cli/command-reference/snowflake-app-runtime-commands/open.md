# snow app open

Opens the deployed Application Service URL in your default browser. Use this
command after a successful deploy to view your running app.

## Syntax

Copy code

```
snow app open
  --print-only
  --settings
  --watch
  --target <target>
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
  --format <format>
  --verbose
  --debug
  --silent
  --enhanced-exit-codes
```

## Arguments

None

## Options

`--print-only`
:   Print the URL without opening a browser. Default: False.

`--settings`
:   Open the app settings page in Snowsight instead of the live service URL. Default: False.

`--watch`
:   Poll until the app service is created and its endpoint is ready before opening (or printing) the URL, instead of failing immediately when the service doesn’t exist yet. Default: False.

`--target TEXT`
:   (Snowflake App Runtime only) Name of the target (environment) declared in the `targets` block of `app.yml`. If you omit `--target`, the CLI uses the top-level `default_target`. Required when `targets` are declared and `default_target` is unset.

`--connection, -c, --environment TEXT`
:   Name of the connection, as defined in your `config.toml` file. Default: `default`.

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

`--help`
:   Displays the help text for this command.

## Usage notes

If `snow app open` can’t resolve an endpoint URL, deploy first with
[`snow app deploy`](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/deploy).

## Examples

Open the deployed app in the default browser:

Copy code

```
snow app open
```

Print the URL without launching a browser:

Copy code

```
snow app open --print-only
```

Open the app’s settings page in Snowsight:

Copy code

```
snow app open --settings
```

Wait for the app service to be ready, then open it:

Copy code

```
snow app open --watch
```
