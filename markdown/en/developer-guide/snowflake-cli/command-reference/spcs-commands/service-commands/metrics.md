# snow spcs service metrics

Note

You can use Snowpark Container Services from Snowflake CLI only if you have the necessary permissions to use Snowpark Container Services.

Retrieve platform metrics for a service container.

## Syntax

Copy code

```
snow spcs service metrics
  <name>
  --container-name <container_name>
  --instance-id <instance_id>
  --since <since>
  --until <until>
  --all
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
:   Identifier of the service; for example: my\_service.

## Options

`--container-name TEXT`
:   Name of the container.

`--instance-id TEXT`
:   ID of the service instance, starting with 0.

`--since TEXT`
:   Fetch events that are newer than this time ago, in Snowflake interval syntax.

`--until TEXT`
:   Fetch events that are older than this time ago, in Snowflake interval syntax.

`--all`
:   Fetch all columns. Default: False.

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

- The following parameters are required:

  - `name`
  - `--container-name <name>`
  - `--instance-id <ID>`
- You can use the `--since` and `--until` time-based filters to return metrics for a specified period of time. You can specify the time as a relative time, such as `1h` (hour) or `2d` (days).

## Examples

- Retrieve metrics for a specific service:

  Copy code

  ```
  snow spcs service metrics LOG_EVENT --container-name log-printer --instance-id 0
  ```
- Retrieve a subset of metrics for a specific service:

  Copy code

  ```
   snow spcs service metrics LOG_EVENT --container-name log-printer --instance-id 0
  snow spcs service metrics LOG_EVENT --container-name log-printer --instance-id 0
  ```
- Fetch metrics older than the last two hours:

  Copy code

  ```
  snow spcs service metrics LOG_EVENT --container-name log-printer --instance-id 0 --until '2 hours'
  ```
- Fetch metrics newer than one hour:

  Copy code

  ```
  snow spcs service metrics LOG_EVENT --container-name log-printer --instance-id 0 --since '1hour'
  ```
- Retrieve metrics with all columns:

  Copy code

  ```
  snow spcs service metrics LOG_EVENT --container-name log-printer --instance-id 0 --all
  ```

  Copy code

  ```
  | TIMESTAMP                  | DATABASE NAME | SCHEMA NAME | SERVICE NAME | INSTANCE NAME | CONTAINER NAME | METRIC NAME                | METRIC VALUE          |
  |----------------------------|---------------|-------------|--------------|---------------|----------------|----------------------------|-----------------------|
  | 2024-12-18 18:10:25.202000 | TESTDB        | PUBLIC      | LOG_EVENT    | 0             | log-printer    | container.cpu.limit        | 1                     |
  | 2024-12-18 18:10:25.202000 | TESTDB        | PUBLIC      | LOG_EVENT    | 0             | log-printer    | container.memory.requested | 536870912             |
  | 2024-12-18 18:10:25.202000 | TESTDB        | PUBLIC      | LOG_EVENT    | 0             | log-printer    | container.memory.limit     | 6442450944            |
  | 2024-12-18 18:10:25.202000 | TESTDB        | PUBLIC      | LOG_EVENT    | 0             | log-printer    | container.cpu.requested    | 0.5                   |
  | 2024-12-18 18:10:08.957000 | TESTDB        | PUBLIC      | LOG_EVENT    | 0             | log-printer    | container.cpu.usage        | 0.0004400012665396536 |
  | 2024-12-18 18:10:08.957000 | TESTDB        | PUBLIC      | LOG_EVENT    | 0             | log-printer    | container.memory.usage     | 1323008               |
  ```
- Retrieve metrics formatted for JSON output:

  Copy code

  ```
  snow spcs service metrics LOG_EVENT --container-name log-printer --instance-id 0 --format json
  ```

  ```
  [
   {
       "TIMESTAMP": "2024-12-14T22:27:25.420489",
       "SERVICE NAME": "LOG_EVENT",
       "INSTANCE NAME": "0",
       "CONTAINER NAME": "log-printer",
       "METRIC TYPE": "CPU_UTILIZATION",
       "VALUE": "75.4"
   }
  ]
  ```
