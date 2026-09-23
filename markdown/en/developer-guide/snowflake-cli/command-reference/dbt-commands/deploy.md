# snow dbt deploy

Upload local dbt project files and create or update a dbt project object on Snowflake.

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

## Syntax

Copy code

```
snow dbt deploy
  <name>
  --source <source>
  --profiles-dir <profiles_dir>
  --auto-compile / --no-auto-compile
  --default-writeback / --no-default-writeback
  --git-commit <git_commit>
  --git-branch <git_branch>
  --force / --no-force
  --default-target <default_target>
  --unset-default-target
  --external-access-integration <external_access_integrations>
  --env-file-dir <env_file_dir>
  --default-env <default_env>
  --install-local-deps
  --dbt-version <dbt_version>
  --git-commit <git_commit>
  --git-branch <git_branch>
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

`name`
:   Identifier of the dbt project; for example: my\_pipeline.

## Options

`--source TEXT`
:   Path to directory containing dbt files to deploy. Defaults to current working directory.

`--profiles-dir TEXT`
:   Path to a directory containing [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml`. The CLI looks for `dbt_projects_profiles.yml` first and uses `profiles.yml` only if `dbt_projects_profiles.yml` isn’t present. The CLI copies the file into the root of the deployed dbt project object with the same filename, overwriting a file with the same name. If you don’t specify `--profiles-dir`, the CLI looks in the `--source` directory. If you don’t specify either option, the CLI looks in the current working directory.

`--auto-compile / --no-auto-compile`
:   Sets whether Snowflake automatically compiles the project during deployment. With `--auto-compile`, Snowflake runs `dbt compile`. If an
    external access integration is configured, Snowflake first runs `dbt deps`, then `dbt compile`. Use `--no-auto-compile` to skip both commands.
    The setting persists on the dbt project object and applies to later deployments until you change it. Default: True.

`--default-writeback / --no-default-writeback`
:   Sets whether executions write generated target and log files back to the live version by default. The setting persists on the dbt project
    object and applies to later executions, but an individual execution can override it. Omit the option to leave the existing setting unchanged.
    Snowflake stores the per-query result artifacts and archive regardless of this setting.
    For retrieval instructions, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).
    Default: True.

`--git-commit TEXT`
:   Git commit identifier to record in the dbt project object’s deployment metadata.

    Snowflake CLI captures the commit and branch automatically when `snow dbt deploy` runs in GitHub Actions. For other CI
    runners, specify `--git-commit` and `--git-branch`.

`--git-branch TEXT`
:   Git branch name to record in the dbt project object’s deployment metadata.

`--force / --no-force`
:   Recreates the dbt project object with `CREATE OR REPLACE DBT PROJECT`. This replaces the live version and removes run history. Default: False.

`--default-target TEXT`
:   Default target for the dbt project. Mutually exclusive with `--unset-default-target`.

`--unset-default-target`
:   Unset the default target for the dbt project. Mutually exclusive with `--default-target`. Default: False.

`--external-access-integration TEXT`
:   External access integration to be used by the dbt object.

`--env-file-dir TEXT`
:   Path to a directory containing an `env.yml` file. The CLI pulls this file into the deployed dbt project object, overwriting the object’s root `env.yml` if one already exists. Requires Snowflake CLI 3.21 or later. For more information, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

`--default-env TEXT`
:   Sets or changes the default environment (defined in the project’s `env.yml` file) used for compilation and subsequent executions of the dbt project object. You can override this per run with the `ENVIRONMENT` argument on the [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project) command. Use the reserved name `NO_ENV` to run without any environment by default. Requires Snowflake CLI 3.21 or later.

`--install-local-deps`
:   Installs local dependencies from project that don’t require external access. Default: False.

`--dbt-version TEXT`
:   dbt version to use for the project, for example ’1.11.11’. Full list of supported versions can be found at <https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions>.

`--git-commit TEXT`
:   Git commit hash to record in last\_deployed\_from metadata when deploying from a plain stage (e.g. SnowCLI temp stage). In GitHub Actions it is auto-detected when not provided.

`--git-branch TEXT`
:   Git branch name to record in last\_deployed\_from metadata when deploying from a plain stage (e.g. SnowCLI temp stage). In GitHub Actions it is auto-detected when not provided.

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
:   Enables a silent re-authentication when the current access token becomes outdated. Default: *False*.

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

The `snow dbt deploy` command uploads local files to a temporary stage and either creates a new object or replaces the existing object’s live version in a single operation. A valid dbt project object must contain `dbt_project.yml` and one of the supported profile files:

- `dbt_project.yml`: A standard dbt configuration file that specifies the profile to use.
- [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml`: A dbt connection profile definition referenced in `dbt_project.yml`. The selected profile file must define the database, role, schema, and type. If both files are present, Snowflake uses `dbt_projects_profiles.yml` and ignores `profiles.yml` during deployment, compilation, and subsequent commands.

  - By default, dbt Projects on Snowflake uses your target schema (`target.schema`) specified from your dbt environment or profile. When you execute a dbt project object, dbt attempts to create the target schema specified in the profile file if it doesn’t already exist. For more information, see [Understand schema generation and customization](/user-guide/data-engineering/dbt-projects-on-snowflake-schema-customization).

  Copy code

  ```
  <profile_name>:
    target: dev
    outputs:
      dev:
        database: <database_name>
        role: <role_name>
        schema: <schema_name>
        warehouse: <warehouse_name>
        type: snowflake
  ```

When `snow dbt deploy` runs in GitHub Actions, Snowflake CLI automatically captures the commit and branch. For other CI runners, explicitly pass `--git-commit` and `--git-branch` to preserve this source metadata.

Warning

Don’t use `--force` unless you intentionally want to recreate the dbt project object. In `snow dbt deploy`, `--force` runs `CREATE OR REPLACE DBT PROJECT`, which may remove run history.

## Examples

- Deploy a dbt project named `jaffle_shop`:

  Copy code

  ```
  snow dbt deploy jaffle_shop
  ```
- Deploy a project with automatic compilation disabled. Useful for
  [optimizing Slim CI workflows](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod):

  Copy code

  ```
  snow dbt deploy jaffle_shop --no-auto-compile
  ```
- Deploy from a CI runner and record the source commit and branch. Snowflake CLI captures this information automatically when
  deploying from GitHub Actions:

  Copy code

  ```
  snow dbt deploy jaffle_shop \
    --git-commit "<commit_sha>" \
    --git-branch "<branch_name>"
  ```
- Deploy a project named `jaffle_shop` from a specified directory, using a profile file from a separate directory:

  Copy code

  ```
  snow dbt deploy jaffle_shop --source /path/to/dbt/directory --profiles-dir ~/my_profiles/
  ```
- Deploy a project named `jaffle_shop` from a specified directory, supplying a profile file from outside the project, setting a default target, and enabling [external access integrations](/developer-guide/external-network-access/creating-using-external-network-access):

  Copy code

  ```
  snow dbt deploy jaffle_shop --source /path/to/dbt/directory \
    --profiles-dir ~/my_profiles/ \
    --default-target dev \
    --external-access-integration dbthub-integration \
    --external-access-integration github-integration
  ```
- Deploy a project named `jaffle_shop` and set a specific dbt runtime version:

  Copy code

  ```
  snow dbt deploy jaffle_shop --dbt-version '1.11.11'
  ```
- Deploy a project named `jaffle_shop`, pull in an `env.yml` file from a separate directory, and set the default environment for compilation and later executions:

  Copy code

  ```
  snow dbt deploy jaffle_shop --source /path/to/dbt/directory \
    --env-file-dir /path/to/env/directory \
    --default-env prod
  ```
