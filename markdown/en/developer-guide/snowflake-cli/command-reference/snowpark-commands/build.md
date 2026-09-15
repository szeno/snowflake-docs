# snow snowpark build

Builds artifacts required for the Snowpark project. The artifacts can be used by `deploy` command. For each directory in artifacts a .zip file is created. All non-anaconda dependencies are packaged in dependencies.zip file.

## Syntax

Copy code

```
snow snowpark build
  --ignore-anaconda
  --allow-shared-libraries
  --index-url <index_url>
  --skip-version-check
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

`--ignore-anaconda`
:   Does not lookup packages on Snowflake Anaconda channel. Default: False.

`--allow-shared-libraries`
:   Allows shared (.so) libraries, when using packages installed through PIP. Default: False.

`--index-url TEXT`
:   Base URL of the Python Package Index to use for package lookup. This should point to a repository compliant with PEP 503 (the simple repository API) or a local directory laid out in the same format.

`--skip-version-check`
:   Skip comparing versions of dependencies between requirements and Anaconda. Default: False.

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

- The `app.zip` contains everything needed to run the functions and procedures in the project, apart from packages available through [Snowflake Anaconda channel](https://repo.anaconda.com/pkgs/snowflake/), which you can call directly from Snowflake.-
- The command parses `requirements.txt` for packages available on Conda channel. This process creates the `requirements.snowflake.txt` file that contains project dependencies available on the Conda channel, which is later used by the `snow snowpark deploy` command.
- By default, the command looks for the `snowflake.yml` file in the current directory. Alternatively, you can specify a different path with the `--project` option.
- This command automatically downloads dependencies and adds them to a file called `app.zip`, together with project source code (specified by the `src` field in the `snowflake.yml` file.
- To use different Python Package Index than PyPi, specify one using the `--index-url` option.
- You can use `--skip-version-check` option to skip version requirements between project dependencies and the Anaconda Channel.
- You can use the `--ignore-anaconda` option to include all the required dependencies in the `app.zip` file, even those available in Snowflake Anaconda channel. The dependencies aren’t downloaded from Anaconda, but from PyPi.
- The `--allow-shared-libraries` option checks whether any of the packages downloaded from PyPi are using native dependencies, which can cause problems as Snowpark currently supports only native dependencies for packages taken from Conda channel

## Examples

- Build a project located in the current directory:

  Copy code

  ```
  snow snowpark build
  ```

  ```
  Resolving dependencies from requirements.txt
    No external dependencies.
  Preparing artifacts for source code
    Creating: app.zip
  Build done.
  ```
- Build a project located in a different directory:

  Copy code

  ```
  ls
  ```

  ```
  project_dir    some_other_dir    some_file.txt
  ```

  Copy code

  ```
  snow snowpark build -p project_dir
  ```

  ```
  Resolving dependencies from requirements.txt
    No external dependencies.
  Preparing artifacts for source code
    Creating: app.zip
  Build done.
  ```
- Build a project in a directory with no `snowflake.yml` project definition:

  Copy code

  ```
  ls
  ```

  ```
  project_dir    some_other_dir    some_file.txt
  ```

  Copy code

  ```
  snow snowpark build
  ```

  ```
  ╭─ Error ──────────────────────────────────────────────────────────╮
    Cannot find project definition (snowflake.yml). Please provide
    a path to the project or run this command in a valid
    project directory.
  ╰──────────────────────────────────────────────────────────────────╯
  ```
- Build a project with native libraries:

  Copy code

  ```
  snow snowpark build --ignore-anaconda --allow-shared-libraries
  ```

  ```
  2024-04-16 16:05:52 ERROR Following dependencies utilise shared libraries, not supported by Conda:
  2024-04-16 16:05:52 ERROR contourpy
  pillow
  numpy
  kiwisolver
  fonttools
  matplotlib
  2024-04-16 16:05:52 ERROR You may still try to create your package with --allow-shared-libraries, but the might not work.
  2024-04-16 16:05:52 ERROR You may also request adding the package to Snowflake Conda channel
  2024-04-16 16:05:52 ERROR at https://support.anaconda.com/
  Build done. Artifact path: /Path/to/current/dir/project_dir/app.zip
  ```
- Build a project and include all dependencies:

  Copy code

  ```
  snow snowpark build --ignore-anaconda
  ```

  ```
  Resolving dependencies from requirements.txt
    No external dependencies.
  Preparing artifacts for source code
    Creating: app.zip
  Build done.
  ```
