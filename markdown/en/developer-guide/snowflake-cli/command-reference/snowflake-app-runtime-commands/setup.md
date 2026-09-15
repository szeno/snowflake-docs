# snow app setup

Initializes an [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml)
manifest for a Snowflake App Runtime project. Creates an `app.yml`
file in the current directory with deployment fields preconfigured from
command-line flags, then Snowsight account defaults, then your personal
database. This command doesn’t apply to Snowflake Native Apps projects.

## Syntax

Copy code

```
snow app setup
  --app-name <app_name>
  --dry-run
  --build-eai <build_eai>
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
  --format <format>
  --verbose
  --debug
  --silent
  --enhanced-exit-codes
```

## Arguments

None

## Options

`--app-name TEXT`
:   Name of the Snowflake App Runtime application to initialize. Defaults to the current directory name.

`--dry-run`
:   Only print the resolved configuration values without writing `app.yml`. Default: False.

`--build-eai TEXT`
:   External access integration used during the app build. External access
    integrations are account-level objects, so specify the integration name without
    a database or schema qualifier.

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
:   Database to use. In `snow app setup`, this value is written to the generated
    `app.yml` as an explicit override, taking precedence over account
    parameters and connection defaults.

`--schema, --schemaname TEXT`
:   Database schema to use. In `snow app setup`, this value is written to the
    generated `app.yml` as an explicit override, taking precedence over
    account parameters and connection defaults.

`--role, --rolename TEXT`
:   Role to use. Overrides the value specified for the connection.

`--warehouse TEXT`
:   Warehouse to use. In `snow app setup`, this value is written to the generated
    `app.yml` as the `query_warehouse` override, taking precedence over
    account parameters and connection defaults.

`--temporary-connection, -x`
:   Uses a connection defined with command-line parameters, instead of one defined in config. Default: False.

`--mfa-passcode TEXT`
:   Token to use for multi-factor authentication (MFA).

`--enable-diag`
:   Whether to generate a connection diagnostic report. Default: False.

`--diag-log-path TEXT`
:   Path for the generated report. Defaults to system temporary directory.

`--diag-allowlist-path TEXT`
:   Path to a JSON file that contains allowlist parameters.

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

The `snow app setup` command bootstraps a new Snowflake App Runtime project by
generating an [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml)
file with default deployment details. Setup resolves the destination
database, schema, and warehouse in this order: the explicit `--database`,
`--schema`, and `--warehouse` options, then Snowsight account defaults from
[account administrator setup](/developer-guide/snowflake-app-runtime/account-admin-setup),
then your current connection settings. If those aren’t set, setup may target
your personal database. Remote builds use the shared external access
integration from Snowsight setup; you don’t add `build_eai` in `app.yml` for
the usual path.

Existing projects that use a `snowflake.yml` with a `snowflake-app` entity keep
working as before.

We recommend completing
[account administrator setup](/developer-guide/snowflake-app-runtime/account-admin-setup)
before team deploys so setup uses shared account defaults. The managed build
service packages your app when you run
[`snow app deploy`](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/deploy).
After `app.yml` exists, edit it only when you need to override defaults,
then deploy to ship your changes.

If account defaults aren’t configured, setup may target a
[personal database](/user-guide/personal-databases). That path isn’t recommended
for apps you plan to share. See
[Getting started with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/getting-started).

When a value can’t be resolved, setup errors and names the account parameter you
can set. The `database`, `schema`, and `query_warehouse` fields are required and
map to `DEFAULT_SNOWFLAKE_APPS_DESTINATION_DATABASE`,
`DEFAULT_SNOWFLAKE_APPS_DESTINATION_SCHEMA`, and
`DEFAULT_SNOWFLAKE_APPS_QUERY_WAREHOUSE`.

Setup leaves `code_stage` and `code_workspace` out of the generated `app.yml`, so
[`snow app deploy`](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/deploy)
provisions temporary code storage for the build and drops it afterward. Set
`code_stage` or `code_workspace` in `app.yml` to keep a persisted stage or
workspace instead. Personal databases use a workspace.

If `app.yml` already exists in the current directory (and you aren’t using
`--dry-run`), setup prints a message and doesn’t overwrite the file.

If you omit `--app-name`, setup uses the current directory name, converting
spaces and hyphens to underscores and removing any other disallowed characters.
The final name must match `[a-zA-Z0-9_]+` (letters, digits, and underscores) or
the command errors.

For the `app.yml` manifest fields, see
[app.yml manifest for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/app-yml). For the `snowflake.yml`
schema that existing projects use, see the
[snowflake.yml reference](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/snowflake-yml).
For a concrete example after setup, see
[Getting started with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/getting-started).
If the project still uses `snowflake.yml`, see
[Migrate from snowflake.yml to app.yml](/developer-guide/snowflake-app-runtime/migrate-to-app-yml).

## Examples

Initialize `app.yml` for a Snowflake App Runtime project in the current directory:

Copy code

```
snow app setup
```

After running the command, edit `app.yml` to configure your app, then deploy it:

Copy code

```
snow app deploy
```

Show the resolved configuration without writing `app.yml`:

Copy code

```
snow app setup --dry-run
```
