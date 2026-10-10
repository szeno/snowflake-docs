# snow dbt deploy

Note

Some features described on this page require a dbt project object that uses the mutable `live` version. To get a live-version object, opt in to the 2026\_06 behavior change bundle or ask your Snowflake account representative to enable the separate single live version feature. Then create or replace the object, or migrate an existing versioned object with `SYSTEM$MIGRATE_DBT_PROJECT`. For details, see [dbt Projects on Snowflake: dbt project objects migrate to a single mutable live version](/release-notes/bcr-bundles/2026_06/bcr-2362).

Upload local dbt project files and create or update a dbt project object on Snowflake.

## Syntax

Copy code

```
snow dbt deploy
  <name>
  --source <source>
  --profiles-dir <profiles_dir>
  --env-file-dir <env_file_dir>
  --force / --no-force
  --default-target <default_target>
  --unset-default-target
  --default-env <default_env>
  --unset-default-env
  --external-access-integration <external_access_integrations>
  --install-local-deps
  --dbt-version <dbt_version>
  --default-writeback / --no-default-writeback
  --auto-compile / --no-auto-compile
  --git-commit <git_commit>
  --git-branch <git_branch>
  --git-url <git_url>
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

`name`
:   *Required*

    Identifier of the DBT Project; for example: my\_pipeline.

## Options

`--source TEXT`
:   Path to directory containing dbt files to deploy. Defaults to current working directory.

`--profiles-dir TEXT`
:   Path to directory containing profiles.yml or dbt\_projects\_profiles.yml (the latter takes precedence and is staged under its own name). Defaults to directory provided in –source or current working directory.

`--env-file-dir TEXT`
:   Path to directory containing env.yml. If provided, the file is injected into the deployed project root, overwriting any env.yml present in –source.

`--force / --no-force`
:   Recreates the dbt project object with CREATE OR REPLACE DBT PROJECT. This removes all existing versions and run history. Default: False.

`--default-target TEXT`
:   Default target for the dbt project. Mutually exclusive with –unset-default-target.

`--unset-default-target`
:   Unset the default target for the dbt project. Mutually exclusive with –default-target. Default: False.

`--default-env TEXT`
:   Default environment for the dbt project. Selects the environment block from env.yml that the project compiles and executes with by default. Mutually exclusive with –unset-default-env.

`--unset-default-env`
:   Unset the default environment for the dbt project. Mutually exclusive with –default-env. Default: False.

`--external-access-integration TEXT`
:   External access integration to be used by the dbt object.

`--install-local-deps`
:   Sets EXTERNAL\_ACCESS\_INTEGRATIONS = () on the dbt project. Snowflake still runs dbt deps at compile; Hub or Git packages in packages.yml still need network access. Default: False.

`--dbt-version TEXT`
:   dbt Core version to use for the project, for example ’1.10.15’. Full list of supported versions can be found at <https://docs.snowflake.com/en/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions>.

`--default-writeback / --no-default-writeback`
:   Set the writeback default persisted on the dbt project. Omit to leave the existing setting unchanged.

`--auto-compile / --no-auto-compile`
:   Set whether the dbt project is compiled on deploy; persisted on the project and applied to subsequent deploys until changed. Omit to leave the existing setting unchanged.

`--git-commit TEXT`
:   Git commit hash to record in last\_deployed\_from metadata when deploying from a plain stage (e.g. SnowCLI temp stage). In GitHub Actions it is auto-detected when not provided.

`--git-branch TEXT`
:   Git branch name to record in last\_deployed\_from metadata when deploying from a plain stage (e.g. SnowCLI temp stage). In GitHub Actions it is auto-detected when not provided.

`--git-url TEXT`
:   Git repository URL to record in last\_deployed\_from metadata when deploying from a plain stage (e.g. SnowCLI temp stage). In GitHub Actions it is auto-detected from GITHUB\_SERVER\_URL and GITHUB\_REPOSITORY when not provided.

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
:   Specifies the output format. [env var: SNOWFLAKE\_CLI\_OUTPUT\_FORMAT | config: cli.output\_format]. Default: TABLE.

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

The `snow dbt deploy` command uploads local files to a temporary stage and either creates a new object or replaces the existing object’s live version in a single operation. A valid dbt project object must contain `dbt_project.yml` and one of the supported profile files:

- `dbt_project.yml`: A standard dbt configuration file that specifies the profile to use.
- [dbt\_projects\_profiles.yml](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml`: A dbt connection profile definition referenced in `dbt_project.yml`. The selected profile file must define the database, role, schema, and type. If both files are present, Snowflake uses `dbt_projects_profiles.yml` and ignores `profiles.yml` during deployment, compilation, and subsequent commands.
- By default, dbt Projects on Snowflake uses your target schema (`target.schema`) specified from your dbt environment or profile. When you execute a dbt project object, dbt attempts to create the target schema specified in the profile file if it doesn’t already exist. For more information, see [Understand schema generation and customization](/user-guide/data-engineering/dbt-projects-on-snowflake-schema-customization).

A profile defines `target`, `outputs`, and per-output fields such as `database`, `role`, `schema`, `warehouse`, and `type: snowflake`.

When `snow dbt deploy` runs in GitHub Actions, Snowflake CLI automatically captures the commit and branch. For other CI runners, explicitly pass `--git-commit` and `--git-branch` to preserve this source metadata.

Warning

Don’t use `--force` unless you intentionally want to recreate the dbt project object. In `snow dbt deploy`, `--force` runs `CREATE OR REPLACE DBT PROJECT`, which may remove run history.

## Examples

- Deploy a dbt project named `jaffle_shop`:

  Copy code

  ```
  snow dbt deploy jaffle_shop
  ```
- Deploy a project with automatic compilation disabled. Useful for [optimizing Slim CI workflows](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod):

  Copy code

  ```
  snow dbt deploy jaffle_shop --no-auto-compile
  ```
- Deploy from a CI runner and record the source commit and branch. Snowflake CLI captures this information automatically when deploying from GitHub Actions:

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
