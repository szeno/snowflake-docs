# snow package create

Creates a Python package as a zip file that can be uploaded to a stage and imported for a Snowpark Python app.

## Syntax

Copy code

```
snow snowpark package create
  <name>
  --ignore-anaconda
  --index-url <index_url>
  --skip-version-check
  --allow-shared-libraries
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
:   Name of the package to create.

## Options

`--ignore-anaconda`
:   Does not lookup packages on Snowflake Anaconda channel. Default: False.

`--index-url TEXT`
:   Base URL of the Python Package Index to use for package lookup. This should point to a repository compliant with PEP 503 (the simple repository API) or a local directory laid out in the same format.

`--skip-version-check`
:   Skip comparing versions of dependencies between requirements and Anaconda. Default: False.

`--allow-shared-libraries`
:   Allows shared (.so) libraries, when using packages installed through PIP. Default: False.

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

The `snowpark package create` command does the following:

- Creates an artifact ready to upload to a stage.
- Checks for native libraries and asks if you want to continue. If the native libraries are present in the downloaded packages, this command works the same as the `snowpark package build` command.

## Examples

- This example creates a Python package as a zip file that can be uploaded to a stage and later imported by a Snowpark Python app. Dependencies for the “july” package are found on the Anaconda channel, so they were excluded from the `.zip` file. The command displays the packages you would need to include in *requirements.txt* of your Snowpark project.

  Copy code

  ```
  snow snowpark package create july==0.1
  ```

  ```
  Package july.zip created. You can now upload it to a stage using
  snow snowpark package upload -f july.zip -s <stage-name>`
  and reference it in your procedure or function.
  Remember to add it to imports in the procedure or function definition.

  The package july is successfully created, but depends on the following
  Anaconda libraries. They need to be included in project requirements,
  as their are not included in .zip.
  matplotlib
  contourpy >=1.0.1
  numpy>=1.20
  bokeh
  selenium
  mypy==1.8.0
  Pillow
  pytest-xdist
  wurlitzer
  cycler >=0.10
  fonttools >=4.22.0
  kiwisolver >=1.3.1
  pyparsing >=2.3.1
  jinja2
  python-dateutil >=2.7
  six >=1.5
  importlib-resources >=3.2.0
  ```
- This example creates the `july.zip` package that you can use in your Snowpark project without needing to add any dependencies to the `requirements.txt` file. The error messages indicate that some packages contain shared libraries, which might not work, such as when creating a package using Windows.

  Copy code

  ```
  snow snowpark package create july==0.1 --ignore-anaconda --allow-shared-libraries
  ```

  ```
  2024-04-11 16:24:56 ERROR Following dependencies utilise shared libraries, not supported by Conda:
  2024-04-11 16:24:56 ERROR numpy
  contourpy
  fonttools
  kiwisolver
  matplotlib
  pillow
  2024-04-11 16:24:56 ERROR You may still try to create your package with --allow-shared-libraries, but the might not work.
  2024-04-11 16:24:56 ERROR You may also request adding the package to Snowflake Conda channel
  2024-04-11 16:24:56 ERROR at https://support.anaconda.com/

  Package july.zip created. You can now upload it to a stage using
  snow snowpark package upload -f july.zip -s <stage-name>`
  and reference it in your procedure or function.
  Remember to add it to imports in the procedure or function definition.
  ```
- This example fails to create the package because it already exists. You can still forcibly create the package by using the `--ignore-anaconda` option.

  Copy code

  ```
  snow snowpark package create matplotlib
  ```

  ```
  Package matplotlib is already available in Snowflake Anaconda Channel.
  ```
