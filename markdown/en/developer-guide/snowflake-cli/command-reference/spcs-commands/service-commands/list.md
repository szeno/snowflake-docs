# snow spcs service list

Note

You can use Snowpark Container Services from Snowflake CLI only if you have the necessary permissions to use Snowpark Container Services.

Lists all available services.

## Syntax

Copy code

```
snow spcs service list
  --like <like>
  --in <scope>
  --in-account
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

`--like, -l TEXT`
:   SQL LIKE pattern for filtering objects by name. For example, *list –like “my%”* lists all services that begin with “my”.. Default: %%.

`--in {<TEXT TEXT>...}`
:   Specifies the scope of this command using ‘–in <scope> <name>’, for example *list –in compute-pool my\_pool*. Default: (None, None).

`--in-account`
:   Lists objects across the entire account.

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

None.

## Examples

The following command lists the services and their statuses:

Copy code

```
snow spcs service list
```

```
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|        |        |        |        |        |        |        |        |        |        |        |         | extern |         |        |         |        |         |        |        |         |        |         |        |
|        |        |        |        |        |        |        |        |        |        |        |         | al_acc |         |        |         |        |         |        |        |         |        | managin | managi |
|        |        | databa |        |        |        |        | curren | target | min_in | max_in |         | ess_in |         |        |         |        | owner_r | query_ |        |         |        | g_objec | ng_obj |
|        |        | se_nam | schema |        | comput | dns_na | t_inst | _insta | stance | stance | auto_re | tegrat | created | update | resumed | commen | ole_typ | wareho |        | spec_di | is_upg | t_domai | ect_na |
| name   | status | e      | _name  | owner  | e_pool | me     | ances  | nces   | s      | s      | sume    | ions   | _on     | d_on   | _on     | t      | e       | use    | is_job | gest    | rading | n       | me     |
|--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+---------+--------+---------+--------+---------+--------+---------+--------+--------+---------+--------+---------+--------|
| ECHO_S | RUNNIN | TEST00 | TEST_S | SYSADM | TUTORI | echo-s | 1      | 1      | 1      | 1      | true    | None   | 2024-10 | 2024-1 | None    | This   | ROLE    | COMPUT | false  | 52e62d1 | false  | None    | None   |
| ERVICE | G      | _DB    | CHEMA  | IN     | AL_COM | ervice |        |        |        |        |         |        | -16     | 0-16   |         | is a   |         | E_WH   |        | f19c720 |        |         |        |
|        |        |        |        |        | PUTE_P | .imhd. |        |        |        |        |         |        | 15:09:3 | 15:09: |         | test   |         |        |        | 6b5f4ef |        |         |        |
|        |        |        |        |        | OOL    | svc.sp |        |        |        |        |         |        | 0.49300 | 31.905 |         | servic |         |        |        | c069557 |        |         |        |
|        |        |        |        |        |        | cs.int |        |        |        |        |         |        | 0-07:00 | 000-07 |         | e      |         |        |        | 8b6c2b3 |        |         |        |
|        |        |        |        |        |        | ernal  |        |        |        |        |         |        |         | :00    |         |        |         |        |        | 806ad76 |        |         |        |
|        |        |        |        |        |        |        |        |        |        |        |         |        |         |        |         |        |         |        |        | 67d78cc |        |         |        |
|        |        |        |        |        |        |        |        |        |        |        |         |        |         |        |         |        |         |        |        | ce8b6ed |        |         |        |
|        |        |        |        |        |        |        |        |        |        |        |         |        |         |        |         |        |         |        |        | 6501a8a |        |         |        |
|        |        |        |        |        |        |        |        |        |        |        |         |        |         |        |         |        |         |        |        | 3       |        |         |        |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```
