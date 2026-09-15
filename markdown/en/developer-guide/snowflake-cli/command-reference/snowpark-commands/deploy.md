# snow snowpark deploy

Deploys procedures and functions defined in project. Deploying the project alters all objects defined in it. By default, if any of the objects exist already the commands will fail unless `--replace` flag is provided. Required artifacts are deployed before creating functions or procedures. Dependencies are deployed once to every stage specified in definitions.

## Syntax

Copy code

```
snow snowpark deploy
  --replace
  --force-replace
  --prune / --no-prune
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

`--replace`
:   Replaces procedure or function if there were changes in the definition. It only uploads new and overwrites existing files, but does not remove any files already on the stage. Default: False.

`--force-replace`
:   Replace this object, even if the state didn’t change. Default: False.

`--prune / --no-prune`
:   Remove contents of the stage before uploading artifacts. Default: False.

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

The `snow snowpark deploy` command does the following:

- Checks to see whether the objects listed for deployment already exist. If the objects exist, you must use the `--replace` option.

  Note

  If you want to update objects and files, even if they did not change, you can use the `--force-replace` option.
- Creates a stage in the database specified for your connection. If no stage is defined, the command creates a stage named `deployments`.
- If the `--prune` option was specified, removes existing content from the stage used by defined procedures and function objects.
- Uploads the new artifacts.
- Creates the objects specified then `snowflake.yml` file by executing the SQL CREATE PROCEDURE or CREATE FUNCTION queries.

The command deploys the source code and dependencies from the most recent build. If you modified the code or added any requirements since the last build, you must run the [snow snowpark build](/developer-guide/snowflake-cli/command-reference/snowpark-commands/build) command again before deploying the new version.

> Note
>
> When deploying a Snowpark stored procedure, Snowflake CLI lets you upload artifacts to a folder within a stage. This makes it possible to deploy several procedures to a single stage.
>
> If you are deploying to a different Snowflake account, you must run the [snow snowpark build](/developer-guide/snowflake-cli/command-reference/snowpark-commands/build) command again before deploying.

## Examples

The following example shows how to deploy functions and procedures in the current directory.

Copy code

```
snow snowpark deploy
```

```
+-----------------------------------------------------------------------------------+
| object                                             | type      | status           |
|----------------------------------------------------+-----------+------------------|
| MY_DATABASE.PUBLIC.HELLO_PROCEDURE(name string)    | procedure | packages updated |
| MY_DATABASE.PUBLIC.TEST_PROCEDURE()                | procedure | created          |
| MY_DATABASE.PUBLIC.HELLO_FUNCTION(name string)     | function  | packages updated |
+-----------------------------------------------------------------------------------+
```

The following example shows what happens when objects already exist and you deploy without specifying the `--replace` option.

Copy code

```
snow snowpark deploy
```

```
╭─ Error ──────────────────────────────────────────────────────────╮
│ Following objects already exists. Consider using --replace.      |
│ function: MY_DATABASE.PUBLIC.HELLO_FUNCTION(string)              |
│ procedure: MY_DATABASE.PUBLIC.HELLO_PROCEDURE(string)            |
│ procedure: MY_DATABASE.PUBLIC.TEST_PROCEDURE()                   |
╰──────────────────────────────────────────────────────────────────╯
```
