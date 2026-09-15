# snow app release-directive set

Sets a release directive. target\_accounts cannot be specified for default release directives. target\_accounts field is required when creating a new non-default release directive.

## Syntax

Copy code

```
snow app release-directive set
  <directive>
  --channel <channel>
  --target-accounts <target_accounts>
  --version <version>
  --patch <patch>
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

`directive`
:   Name of the release directive to set.

## Options

`--channel TEXT`
:   Name of the release channel to use. Default: DEFAULT.

`--target-accounts TEXT`
:   List of the accounts to apply the release directive to. Format must be *org1.account1,org2.account2*.

`--version TEXT`
:   Version of the application package to use.

`--patch INTEGER`
:   Patch number to use for the selected version.

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

The `snow app release-directive set` command sets the release directive for an application package.
There are two types of release directives: default and custom.

- When you set the default release directive, target accounts are not accepted.
- When you set a new custom release directive, the target accounts are required.
- When you update an existing custom release directive, the target accounts are optional.

Target accounts are provided in the format ORGANIZATION\_NAME.ACCOUNT\_NAME, separated by commas.

When release channels are enabled in the application package, the release directive is scoped to the specified release channel; otherwise, it is scoped to the application package.

Snowflake recommends using the [snow app publish](/developer-guide/snowflake-cli/command-reference/native-apps-commands/publish-app) command to publish the application package and using the `snow app release-directive set` command for creating custom release directives.
See [Publishing a Snowflake Native App to customers](/developer-guide/snowflake-cli/native-apps/publish-app) for more information.`

## Examples

- Set the default release directive for an application package:

  Copy code

  ```
  snow app release-directive set DEFAULT --version v1 --patch 1
  ```
- Set a custom release directive for an application package:

  Copy code

  ```
  snow app release-directive set CUSTOM_DIR --version v1 --patch 1 --target-accounts ORG1.ACCT1,ORG2.ACCT2
  ```
- Update an existing custom release directive for an application package:

  Copy code

  ```
  snow app release-directive set CUSTOM_DIR --version v1 --patch 2
  ```
- Set the default release directive of a release channel when the application package has release channels enabled:

  Copy code

  ```
  snow app release-directive set DEFAULT --version v1 --patch 1 --channel ALPHA
  ```
