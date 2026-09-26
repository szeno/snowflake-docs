# snow spcs service remote-build

Note

You can use Snowpark Container Services from Snowflake CLI only if you have the necessary permissions to use Snowpark Container Services.

Builds an image or app artifact with Snowflake’s remote build REST API, instead of `snow spcs service build-image` (which runs `EXECUTE JOB SERVICE`).

Use `--build-type image` (the default) to build an OCI container image and push it to an image repository. Use `--build-type app` to build an application tarball and upload it to an artifact repository; `--location` is required for that type.

## Syntax

Copy code

```
snow spcs service remote-build
  --build-context-dir <build_context_dir>
  --location <location>
  --name <name>
  --image-tag <image_tag>
  --project-type <project_type>
  --compute-pool <compute_pool>
  --stage <stage>
  --build-type <build_type>
  --validation-profile <validation_profile>
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

None

## Options

`--build-context-dir DIRECTORY`
:   Directory to use as build context. Must contain a Dockerfile (image) or project root (app).

`--location TEXT`
:   Target repository for the build output. For image builds: IMAGE REPOSITORY in [db.][schema.]repo format (optional, account default used when omitted). For app builds: ARTIFACT REPOSITORY in db.schema.repo format (required).

`--name TEXT`
:   Output name. For image builds: short image name without a tag. For app builds: artifact package name. Auto-generated when omitted.

`--image-tag TEXT`
:   Tag for the built image. Applies to image builds only. Defaults to ‘latest’ when omitted.

`--project-type TEXT`
:   Project type hint for app builds (e.g. ‘node’, ‘python’). Ignored for image builds.

`--compute-pool TEXT`
:   Compute pool to run the build job on. Uses the platform default when omitted.

`--stage TEXT`
:   Stage to store build context files. Format: [db.][schema.]stage\_name. If not provided, a temporary stage will be created and dropped automatically.

`--build-type TEXT`
:   Type of build to execute: ‘image’ (default) or ‘app’. Default: image.

`--validation-profile TEXT`
:   Validation profile for image builds (e.g. ML\_JOB, NOTEBOOK). Selects the pre-baked ruleset the image builder runs before publish. Ignored for –build-type app. When omitted, no image validation is requested.

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
