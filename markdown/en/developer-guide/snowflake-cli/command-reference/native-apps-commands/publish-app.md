# snow app publish

Adds the version to the release channel and updates the release directive with the new version and patch.

## Syntax

Copy code

```
snow app publish
  --version <version>
  --patch <patch>
  --channel <channel>
  --directive <directive>
  --interactive / --no-interactive
  --force
  --create-version
  --from-stage
  --label <label>
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

None

## Options

`--version TEXT`
:   The version to publish to the provided release channel and release directive. Version is required to exist unless *–create-version* flag is used.

`--patch INTEGER`
:   The patch number under the given version. This will be used when setting the release directive. Patch is required to exist unless *–create-version* flag is used.

`--channel TEXT`
:   The name of the release channel to publish to. If not provided, the default release channel is used. Default: DEFAULT.

`--directive TEXT`
:   The name of the release directive to update with the specified version and patch. If not provided, the default release directive is used. Default: DEFAULT.

`--interactive / --no-interactive`
:   When enabled, this option displays prompts even if the standard input and output are not terminal devices. Defaults to True in an interactive shell environment, and False otherwise.

`--force`
:   When enabled, this option causes the command to implicitly approve any prompts that arise. You should enable this option if interactive mode is not specified and if you want perform potentially destructive actions. Defaults to unset. Default: False.

`--create-version`
:   Create a new version or patch based on the provided *–version* and *–patch* values. Fallback to the manifest values if not provided. Default: False.

`--from-stage`
:   When enabled, the Snowflake CLI creates a version from the current application package stage without syncing to the stage first. Can only be used with *–create-version* flag. Default: False.

`--label TEXT`
:   A label for the version that is displayed to consumers. Can only be used with *–create-version* flag.

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

The `snow app publish` command lets you add Snowflake Native App versions to a release channel and then sets the selected release directive to use the provided version and patch.

For more information on release channels and release directives, see [Publishing a Snowflake Native App to customers](/developer-guide/snowflake-cli/native-apps/publish-app).

Note

The release channels feature might not be available in all regions. Please contact Snowflake Support for more information.

If the release channel feature is not available, you can ignore the `--channel` parameter of this command.

This command adds the specified version to the release channel. If the release channel has reached its maximum number of versions, the oldest version not referenced by any release directive is removed from the release channel.
After the version is added to the release channel, the release directive within the release channel is updated to use the provided version and patch.

If release channels are not enabled for the application package, only the release directive is updated to use the provided version and patch.
When a release channel is not provided, or when using the default release channel, you can use the same commands whether release channels are enabled or not.

This command assumes that the version and patch already exist in the application package. If the version and patch do not exist, the command fails.

To create a new version or patch when using this command, use the `--create-version` option. By using this option, you can use options like `--from-stage` or `--label`. For more information, also see the [snow app version create](/developer-guide/snowflake-cli/command-reference/native-apps-commands/version/app-version-create) command.

The rules for creating a new version are the same rules as for the [snow app version create](/developer-guide/snowflake-cli/command-reference/native-apps-commands/version/app-version-create) command. In other words, Snowflake CLI uses the same fallback logic to the manifest file if the version field is missing.

## Examples

- Publish version v1 and patch 2 to the default release directive of the default release channel or to the default release directive in the package. In this example, release channels are not enabled:

  Copy code

  ```
  snow app publish --version v1 --patch 2
  ```
- Publish version v1 and patch 2 to the `customers_group_1` release directive of the ALPHA release channel:

  Copy code

  ```
  snow app publish --version v1 --patch 2 --channel ALPHA --directive customers_group_1
  ```
- Publish version v1 and patch 2 to the default release directive of the QA release channel:

  Copy code

  ```
  snow app publish --version v1 --patch 2 --channel QA
  ```
- Create a new version and publish it to the custom `early_adopters` release directive of the default release channel:

  Copy code

  ```
  snow app publish --version v2 --create-version --directive early_adopters
  ```
- Add a patch to an existing version and publish it to the default release directive of the default release channel. You must use `--create-version` and either provide the patch number or omit it to use the next available patch number:

  Copy code

  ```
  snow app publish --version v2 --create-version
  ```
- Create a new patch from the content of the stage without syncing files to the stage first, and publish it to the default release directive of the default release channel:

  Copy code

  ```
  snow app publish --version v2 --patch 11 --create-version --from-stage
  ```
