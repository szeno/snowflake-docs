# snow spcs service events

Note

You can use Snowpark Container Services from Snowflake CLI only if you have the necessary permissions to use Snowpark Container Services.

Retrieve platform events for a service.

## Syntax

Copy code

```
snow spcs service events
  <name>
  --container-name <container_name>
  --instance-id <instance_id>
  --since <since>
  --until <until>
  --first <first>
  --last <last>
  --all
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
:   Identifier of the service; for example: my\_service.

## Options

`--container-name TEXT`
:   Narrow events to this container. Requires `--instance-id`.

`--instance-id TEXT`
:   Narrow events to this service instance, starting with 0.

`--since TEXT`
:   Fetch events that are newer than this time ago, in Snowflake interval syntax.

`--until TEXT`
:   Fetch events that are older than this time ago, in Snowflake interval syntax.

`--first INTEGER`
:   Fetch only the first N events. Cannot be used with `--last`.

`--last INTEGER`
:   Fetch only the last N events. Cannot be used with `--first`.

`--all`
:   Fetch all columns. Default: False.

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
:   Specifies the output format. Default: TABLE.

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

- Only the `name` argument is required. By default, the command returns all platform events for the service.
- Use the scope filters to narrow the results:
  - `--instance-id <ID>` returns events for a single service instance.
  - `--container-name <name>` returns events for a single container. This option requires `--instance-id`.
- You can use the `--since` and `--until` time-based filters to return events for a specified period of time. You can specify the time as a relative time, such as `1h` (hour) or `2d` (days).
- You can use the `--first` and `--last` options to return only a specified number of events. Note that these options are mutually exclusive.

## Examples

- Retrieve all events for a service (service, service instance, and container events):

  Copy code

  ```
  snow spcs service events LOG_EVENT
  ```

  ```
  +----------------------------+---------------+-------------+--------------+-------------+----------------+----------+--------------------------------+---------------------------------------------------------------+
  | TIMESTAMP                  | DATABASE NAME | SCHEMA NAME | SERVICE NAME | INSTANCE ID | CONTAINER NAME | SEVERITY | EVENT NAME                     | EVENT VALUE                                                   |
  +----------------------------+---------------+-------------+--------------+-------------+----------------+----------+--------------------------------+---------------------------------------------------------------+
  | 2024-12-14 22:27:25.420489 | TESTDB        | PUBLIC      | LOG_EVENT    | N/A         | N/A            | INFO     | SERVICE.STATUS_CHANGE          | {"message": "Service is ready", "status": "RUNNING"}          |
  | 2024-12-14 22:27:25.630550 | TESTDB        | PUBLIC      | LOG_EVENT    | 0           | N/A            | INFO     | SERVICE_INSTANCE.STATUS_CHANGE | {"message": "Service instance is running", "status": "READY"} |
  | 2024-12-14 22:27:26.100000 | TESTDB        | PUBLIC      | LOG_EVENT    | 0           | log-printer    | INFO     | CONTAINER.STATUS_CHANGE        | {"message": "Running", "status": "READY"}                     |
  +----------------------------+---------------+-------------+--------------+-------------+----------------+----------+--------------------------------+---------------------------------------------------------------+
  ```
- Retrieve events for a single service instance:

  Copy code

  ```
  snow spcs service events LOG_EVENT --instance-id 0
  ```
- Retrieve events for a single container:

  Copy code

  ```
  snow spcs service events LOG_EVENT --instance-id 0 --container-name log-printer
  ```
- Retrieve only the first or last N events:

  Copy code

  ```
  snow spcs service events LOG_EVENT --first 5
  snow spcs service events LOG_EVENT --last 5
  ```
- Fetch events newer than the last five minutes:

  Copy code

  ```
  snow spcs service events LOG_EVENT --since '5 minutes'
  ```
- Fetch events older than one hour:

  Copy code

  ```
  snow spcs service events LOG_EVENT --until '1 hour'
  ```
- Retrieve the raw event-table columns (`RESOURCE_ATTRIBUTES`, `SCOPE`, `RECORD`, `VALUE`, and so on) instead of the summarized columns:

  Copy code

  ```
  snow spcs service events LOG_EVENT --all
  ```

  ```
  +----------------------+-----------------+----------------------+-------+----------+----------------------+---------------------+------------------+-------------+----------------------+-------------------+---------------------+-----------+
  | TIMESTAMP            | START_TIMESTAMP | OBSERVED_TIMESTAMP   | TRACE | RESOURCE | RESOURCE_ATTRIBUTES  | SCOPE               | SCOPE_ATTRIBUTES | RECORD_TYPE | RECORD               | RECORD_ATTRIBUTES | VALUE               | EXEMPLARS |
  +----------------------+-----------------+----------------------+-------+----------+----------------------+---------------------+------------------+-------------+----------------------+-------------------+---------------------+-----------+
  | 2024-12-14           | None            | 2024-12-14           | None  | None     | {                    | {                   | None             | EVENT       | {                    | None              | {                   | None      |
  | 22:27:26.100000      |                 | 22:27:26.100000      |       |          |                      |   "name":           |                  |             |   "name":            |                   |   "message":        |           |
  |                      |                 |                      |       |          | "snow.compute_pool.i | "snow.spcs.platform |                  |             | "CONTAINER.STATUS_CH |                   | "Running",          |           |
  |                      |                 |                      |       |          | d": 48,              | "                   |                  |             | ANGE",               |                   |   "status": "READY" |           |
  |                      |                 |                      |       |          |                      | }                   |                  |             |                      |                   | }                   |           |
  |                      |                 |                      |       |          | "snow.compute_pool.n |                     |                  |             | "severity_number":   |                   |                     |           |
  |                      |                 |                      |       |          | ame": "MYPOOL",      |                     |                  |             | 9,                   |                   |                     |           |
  |                      |                 |                      |       |          |                      |                     |                  |             |   "severity_text":   |                   |                     |           |
  |                      |                 |                      |       |          | "snow.database.id":  |                     |                  |             | "INFO"               |                   |                     |           |
  |                      |                 |                      |       |          | 161,                 |                     |                  |             | }                    |                   |                     |           |
  |                      |                 |                      |       |          |                      |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | "snow.database.name" |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | : "TESTDB",          |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          |   "snow.schema.id":  |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | 12441,               |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          |                      |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | "snow.schema.name":  |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | "PUBLIC",            |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          |                      |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | "snow.service.contai |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | ner.name":           |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | "log-printer",       |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          |                      |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | "snow.service.id":   |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | 2143,                |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          |                      |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | "snow.service.instan |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | ce": "0",            |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          |                      |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | "snow.service.name": |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          |  "LOG_EVENT",        |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          |                      |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | "snow.service.type": |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          |  "SERVICE"           |                     |                  |             |                      |                   |                     |           |
  |                      |                 |                      |       |          | }                    |                     |                  |             |                      |                   |                     |           |
  +----------------------+-----------------+----------------------+-------+----------+----------------------+---------------------+------------------+-------------+----------------------+-------------------+---------------------+-----------+
  ```
- Retrieve events formatted for JSON output:

  Copy code

  ```
  snow spcs service events LOG_EVENT --last 1 --format json
  ```

  ```
  [
      {
          "TIMESTAMP": "2024-12-14T22:27:25.420489",
          "DATABASE NAME": "TESTDB",
          "SCHEMA NAME": "PUBLIC",
          "SERVICE NAME": "LOG_EVENT",
          "INSTANCE ID": "N/A",
          "CONTAINER NAME": "N/A",
          "SEVERITY": "INFO",
          "EVENT NAME": "SERVICE.STATUS_CHANGE",
          "EVENT VALUE": "{\n  \"message\": \"Service is ready\",\n  \"status\": \"RUNNING\"\n}"
      }
  ]
  ```
