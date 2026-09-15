# snow app teardown

Drops the Application Service and cleans up associated objects (stage or
workspace files). Use `--force` to skip the confirmation prompt.

## Syntax

Copy code

```
snow app teardown
  --force
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

`--force`
:   Skip the confirmation prompt and immediately drop the Application Service. Default: False.

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

This command is destructive. Unless you pass `--force`, the CLI prompts you to
confirm before it drops anything. It drops the following objects:

- The Application Service (or plain service) named
  `<database>.<schema>.<app>`.
- Code storage, based on the backend in `app.yml`:
  - **Workspace backend (`code_workspace`)**: Only this app’s subdirectory is
    cleared. The workspace itself is kept, because it can be shared across apps
    (for example, the default `SNOWFLAKE_APPS` workspace).
  - **Stage backend (`code_stage`, or the `<app>_CODE` fallback)**: The stage is
    dropped.

The command does not drop the artifact repository or previously built package
versions. If you need to redeploy later, run
[`snow app deploy`](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/deploy) again.

The app’s database and schema come from `app.yml`. For those fields, see the
[app.yml reference](/developer-guide/snowflake-app-runtime/app-yml).

## Examples

Tear down the app (with confirmation prompt):

Copy code

```
snow app teardown
```

Tear down without confirmation:

Copy code

```
snow app teardown --force
```
