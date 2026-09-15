# snow app version create

Adds a new patch to the provided version defined in your application package. If the version does not exist, creates a version with patch 0.

## Syntax

Copy code

```
snow app version create
  <version>
  --patch <patch>
  --label <label>
  --skip-git-check
  --from-stage
  --interactive / --no-interactive
  --force
  --package-entity-id <package_entity_id>
  --app-entity-id <app_entity_id>
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

`version`
:   Version to define in your application package. If the version already exists, an auto-incremented patch is added to the version instead. Defaults to the version specified in the *manifest.yml* file.

## Options

`--patch INTEGER`
:   The patch number you want to create for an existing version. Defaults to undefined if it is not set, which means the Snowflake CLI either uses the patch specified in the *manifest.yml* file or automatically generates a new patch number.

`--label TEXT`
:   A label for the version that is displayed to consumers. If unset, the version label specified in *manifest.yml* file is used.

`--skip-git-check`
:   When enabled, the Snowflake CLI skips checking if your project has any untracked or stages files in git. Default: unset. Default: False.

`--from-stage`
:   When enabled, the Snowflake CLI creates a version from the current application package stage without syncing to the stage first. Default: False.

`--interactive / --no-interactive`
:   When enabled, this option displays prompts even if the standard input and output are not terminal devices. Defaults to True in an interactive shell environment, and False otherwise.

`--force`
:   When enabled, this option causes the command to implicitly approve any prompts that arise. You should enable this option if interactive mode is not specified and if you want perform potentially destructive actions. Defaults to unset. Default: False.

`--package-entity-id TEXT`
:   The ID of the package entity on which to operate when the definition\_version is 2 or higher.

`--app-entity-id TEXT`
:   The ID of the application entity on which to operate when the definition\_version is 2 or higher.

`-p, --project TEXT`
:   Path where the Snowflake project is stored. Defaults to the current working directory.

`--env TEXT`
:   String in the format key=value. Overrides variables from the env section used for templates. Default: [].

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

Note

This command does not accept a role or warehouse overrides to your `config.toml` file. Please add them to the native app definition in the `snowflake.yml` or `snowflake.local.yml` instead.

This command creates an application package (if it does not exist) with a version and an optional patch.

- If you do not provide a version, the command uses the version specified in the `manifest.yml` file. If the version is not present in the `manifest.yml` file, the command throws an error.
- If you provide both the version argument and the `--patch` option, and the application package does not already exist, the command throws an error. You should only provide the version argument to create a new application package with the required version.
- If you provide both the version argument and the `--patch` option, and the version does not already exist, the command throws an error. You should only provide the version argument to create a new version with a predetermined patch 0.
- If you are working in a Git repository and execute this command, the command checks for local changes to your working copy. If it finds local changes, it prompts you to confirm whether it is safe to proceed. You can skip this check using `--skip-git-check` option.
- If the application package does not exist, a new one is created by the Snowflake CLI is tagged with a special comment `GENERATED_BY_SNOWCLI`. It also runs any post-deploy hooks and uploads code files to the stage.
- If the application package already exists and its distribution property is `INTERNAL`, the command checks if the package was created by the Snowflake CLI. If it was not, the command throws an error. If the distribution of the application package is `EXTERNAL`, no such check is performed.
- The command warns you if the application package you are working with has a different value for distribution than is set in your resolved project definition, but continues execution.
- If the version is referenced in a release directive for the application package, the command prompts you to confirm whether you want to create a patch on this version.
- If the version already exists and you do not provide a `--patch` option, the Native Apps Framework automatically increments the patch number for this existing version. Else, it creates a custom patch under the version provided by you.
- The `--label` option sets a label for the version or patch created with this command. If specified, this value overrides the label specified for the `version` defined in the application’s `manifest.yml` file.
- If you specify a named version, such as `snow app version create my_version`, the `version` field in the `manifest.yml` file is ignored.

## Examples

These examples assume you have made the necessary changes to your code files and added them to your `snowflake.yml` or `snowflake.local.yml` files.

If you want to create an application package and add a version **V1** to it, use the following command:

Copy code

```
snow app version create V1 --connection="dev"
```

You can also use the command above to create a version **V1** on an existing application package.

If you want to add a patch to version **V1** using the auto-increment functionality and invoke the interactive mode, use the following command:

Copy code

```
snow app version create V1 --interactive --connection="dev"
```

If you want to add a custom patch number to version `V1` and bypass the interactive mode, even if you are in an interactive shell, use the following command:

Copy code

```
snow app version create V1 --patch 42 --force --connection="dev"
```

To create a new version from the current content of the stage without syncing files to the stage first, use the following command:

Copy code

```
snow app version create V1 --from-stage --connection="dev"
```
