# snow logs

Retrieves logs for a given object.

## Syntax

Copy code

```
snow logs
  <object_type>
  <object_name>
  --from <from_>
  --to <to>
  --refresh <refresh_time>
  --table <event_table>
  --log-level <log_level>
  --partial
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

`object_type`
:   Type of object. For example table, database, compute-pool.

`object_name`
:   Name of the object.

## Options

`--from TEXT`
:   The start time of the logs to retrieve. Accepts all ISO 8601 formats.

`--to TEXT`
:   The end time of the logs to retrieve. Accepts all ISO 8601 formats.

`--refresh INTEGER`
:   If set, the logs will be streamed with the given refresh time in seconds.

`--table TEXT`
:   The table to query for logs. If not provided, the default table will be used.

`--log-level TEXT`
:   The log level to filter by. If not provided, INFO will be used. Default: INFO.

`--partial`
:   Enable partial, case-insensitive matching for object names. Default: False.

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

The `snow logs` command accesses an event table and retrieves [logs](/developer-guide/logging-tracing/logging) for a specified entity. By default, the command looks for
the logs in the default event table, which is SNOWFLAKE.TELEMETRY.EVENTS; however, you can select a different table with the
`--table` option. For more information about event tables and default values, see [Create an event table](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-custom-create).

You can use the `--from` and `-to` options to filter the period during which to retrieve the logs.
You can use one or both of these option, but if you use both, the `--from` time must be earlier than the `--to` time.
The values for times you provide must comply with the [ISO 8601 standard](https://www.iso.org/iso-8601-date-and-time-format.html).
For more information, you can also check the Python [datetime.fromisoformat()](https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat) method documentation.

The `--log-level` option lets you filter message by [severity level](/developer-guide/logging-tracing/event-table-columns#label-event-table-schema).
Some logs do not include a severity level. In those cases, messages are display for all `--log-level` values.

The `--partial` option lets you retrieve logs that contain a specific string using a case-insensitive match. For example, if you searched for logs containing *myDb* with this option, the results would include logs for databases named *mydb*, *MYDB*, and *MyDb*. Without this option, it would return only logs for databases named exactly *myDb*.

If you want continuous updates for the logs, you can use the `--refresh` option and provide the number of seconds between retrievals.
You cannot use both the `--refresh` and `--to` options together.
To stop streaming the logs, use your system’s default `Keyboardinterrupt` key, such as `CTRL-c` in a Mac Terminal.

## Examples

- Display the compute pool logs for a period from a specified starting time to now:

  Copy code

  ```
  snow logs compute_pool MY_COMPUTE_POOL --from '2025-04-01 09:00:31'
  ```

  ```
  10.12.71.201 - - [01/Apr/2025 09:46:07] "GET /healthcheck HTTP/1.1" 200 -
  10.12.71.201 - - [01/Apr/2025 09:46:09] "GET /healthcheck HTTP/1.1" 200 -
  10.12.71.201 - - [01/Apr/2025 09:46:14] "GET /healthcheck HTTP/1.1" 200 -
  10.12.71.201 - - [01/Apr/2025 09:46:19] "GET /healthcheck HTTP/1.1" 200 -
  10.12.71.201 - - [01/Apr/2025 09:46:24] "GET /healthcheck HTTP/1.1" 200 -
  10.12.71.201 - - [01/Apr/2025 09:46:29] "GET /healthcheck HTTP/1.1" 200 -
  10.12.71.201 - - [01/Apr/2025 09:46:34] "GET /healthcheck HTTP/1.1" 200 -
  ```
- Display the logs for a specific event table:

  Copy code

  ```
  snow logs compute_pool SNOWCLI_COMPUTE_POOL --table "my_db.my_schema.my_events"
  ```
- Display the logs for all databases that contain `myDb` using a case-insensitive partial match:

  Copy code

  ```
  snow logs database myDb --partial
  ```
- Display the logs for a time range where the from time is later than the to time, which causes an error:

  Copy code

  ```
  snow logs compute_pool SNOWCLI_COMPUTE_POOL --from '2025-03-24 12:00:31' --to "2024-01-03 00:00:00"
  ```

  ```
  ╭─ Error ─────────────────────────────────────────────────────────
  │ From_time cannot be later than to_time. Please check the values
  ╰─────────────────────────────────────────────────────────────────
  ```
