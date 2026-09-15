# snow app deploy

Uploads your project source to Snowflake, builds it remotely, and creates or
alters the Application Service. This is the primary command for shipping
changes to a Snowflake App Runtime project. By default it runs three phases in
order: upload, build, and deploy.

When the project has an `app.yml`, `snow app deploy` runs the Snowflake App
Runtime flow (upload, build, deploy). When `snowflake.yml` contains a Native
App entity, the command runs the Native App flow instead. Older App Runtime
projects that still use `snowflake.yml` are covered in
[Migrate from snowflake.yml to app.yml](/developer-guide/snowflake-app-runtime/migrate-to-app-yml).

## Syntax

Copy code

```
snow app deploy
  --upload-only
  --build-only
  --promote-only
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

`--upload-only`
:   Re-upload source files without rebuilding or redeploying. Only one of `--upload-only`, `--build-only`, or `--promote-only` can be used at a time. Default: False.

`--build-only`
:   Re-trigger the remote build without re-uploading or redeploying. Only one of `--upload-only`, `--build-only`, or `--promote-only` can be used at a time. Default: False.

`--promote-only`
:   Create or alter the Application Service without re-uploading or rebuilding. Only one of `--upload-only`, `--build-only`, or `--promote-only` can be used at a time. Default: False.

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
:   Database to use. Overrides the value specified for the connection. This
    doesn’t change the Application Service destination in `app.yml`.

`--schema, --schemaname TEXT`
:   Database schema to use. Overrides the value specified for the connection. This
    doesn’t change the Application Service destination in `app.yml`.

`--role, --rolename TEXT`
:   Role to use. Overrides the value specified for the connection.

`--warehouse TEXT`
:   Warehouse to use. Overrides the value specified for the connection. This
    doesn’t change `query_warehouse` in `app.yml`.

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

Running `snow app deploy` with no phase flags performs the full pipeline:

1. **Upload phase**: Syncs local source files to an internal stage or workspace.
2. **Build phase**: Runs the [build phase](/developer-guide/snowflake-app-runtime/deploy#label-deploy-build-phase)
   that produces an immutable package version in the application’s artifact
   repository.
3. **Deploy phase**: Creates or alters the Application Service from that
   package (typically the `LATEST` version). The command converges the service
   to the `app.yml` specification.

The command name covers all three phases. **Deploy phase** means publishing the
built package to a running service, not a separate CLI command.

We recommend
[account administrator setup](/developer-guide/snowflake-app-runtime/account-admin-setup)
before team deploys to shared account defaults (for example `SNOWFLAKE_APPS`). If
account defaults aren’t configured,
[`snow app setup`](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/setup)
may resolve to a [personal database](/user-guide/personal-databases) instead; see
[Getting started with Snowflake App Runtime](/developer-guide/snowflake-app-runtime/getting-started).

Run `snow app setup` to generate `app.yml` for your deploy destination.
With named targets, pass `--target` or set `default_target` in `app.yml`.

If a deploy fails partway through, retry just the failed phase:

- `snow app deploy --upload-only`: Re-upload source files without rebuilding or redeploying.
- `snow app deploy --build-only`: Re-trigger the build without re-uploading or redeploying.
- `snow app deploy --promote-only`: Create or alter the service without re-uploading or rebuilding.

Only one phase flag can be used at a time.

`snow app deploy` isn’t idempotent. Running it again restarts the selected
phase sequence. If upload and build have already succeeded, use
`--promote-only` instead of rerunning the full pipeline.

For operating and debugging after deployment:

- Check service state with
  [DESCRIBE APPLICATION SERVICE](/sql-reference/sql/desc-application-service).
- List services with
  [SHOW APPLICATION SERVICES](/sql-reference/sql/show-application-services).
- Read logs with
  [snow app events](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/events)
  or
  [SYSTEM$GET\_APPLICATION\_SERVICE\_LOGS](/sql-reference/functions/system_get_application_service_logs).

## Troubleshooting deploy and build failures

### Build runs too long or is canceled

Remote builds have a maximum running time measured from when the builder pod
becomes ready (containers running), not from when the build job is submitted.
Queueing, scheduling, image pull, and container startup don’t count toward the
limit. The default maximum is about 12 hours. If a build exceeds the limit,
Snowflake can cancel the job and `snow app deploy` fails. Retry with
`--build-only` after you fix long-running install or build steps in your project,
or split work so each build finishes within the limit.

### Invalid `app.yml` during build

When your uploaded source includes
[`app.yml`](/developer-guide/snowflake-app-runtime/app-yml), Snowflake validates
the manifest during the build phase. Syntax errors, invalid `icon`
paths, or other manifest problems fail the build with an error similar to:

`Application service manifest (app.yaml) cannot be parsed. '<details>'.`

Fix the manifest locally, then rerun `snow app deploy --build-only` (or the full
deploy if upload also changed).

## Examples

Deploy the full pipeline (upload, build, deploy):

Copy code

```
snow app deploy
```

Re-trigger only the build after fixing a build error:

Copy code

```
snow app deploy --build-only
```
