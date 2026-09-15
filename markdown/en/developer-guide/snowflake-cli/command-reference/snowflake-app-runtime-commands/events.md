# snow app events

Fetches observability data from the Application Service. Use `--type` to select one of three telemetry streams:

- **log** (default): Live container log tail, sized with `--last` (default 500 lines, capped at 100 KB). Supplying `--since` or `--until` switches to historical logs from the event table, which covers data after a suspend and has a short ingestion lag.
- **metric**: CPU, memory, and network telemetry from the event table. Use `--metric` to filter by a specific metric, and `--raw` to get unconverted values.
- **lifecycle**: Service and container status changes from the event table.

The `metric` and `lifecycle` streams are always historical and default to the last hour when no time window is given.

## Syntax

Copy code

```
snow app events
  --since <since>
  --until <until>
  --type <record_types>
  --scope <scopes>
  --consumer-org <consumer_org>
  --consumer-account <consumer_account>
  --consumer-app-hash <consumer_app_hash>
  --first <first>
  --last <last>
  --follow
  --follow-interval <follow_interval>
  --metric <metric>
  --raw
  --instance <instance>
  --target <target>
  --package-entity-id <package_entity_id>
  --app-entity-id <app_entity_id>
  --entity-id <entity_id>
  --project <project_definition>
  --env <env_overrides>
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

`--since TEXT`
:   Fetch events newer than this time. For Snowflake App Runtime projects: a relative shorthand (30m, 6h, 2d) or an absolute UTC timestamp (for example, `2026-07-16 18:00:00`). Supplying a value switches log output to the historical event table. For Native App projects: a time ago in Snowflake interval syntax.

`--until TEXT`
:   Fetch events older than this time. For Snowflake App Runtime projects: a relative shorthand (30m, 6h, 2d) or an absolute UTC timestamp (for example, `2026-07-16 23:59:59`). For Native App projects: a time ago in Snowflake interval syntax.

`--type [log|span|span_event|metric|lifecycle]`
:   Selects the telemetry stream to return. For Snowflake App Runtime projects: `log` (default), `metric`, or `lifecycle`. For Native App projects: one or more of `log`, `span`, `span_event` (repeatable). Default: [].

`--scope TEXT`
:   (Native App only) Restrict results to a specific scope name. Can be specified multiple times. Default: [].

`--consumer-org TEXT`
:   (Native App only) The name of the consumer organization.

`--consumer-account TEXT`
:   (Native App only) The name of the consumer account in the organization.

`--consumer-app-hash TEXT`
:   (Native App only) The SHA-1 hash of the consumer application name.

`--first INTEGER`
:   (Native App only) Fetch only the first N events. Can’t be used with `--last`. Default: -1.

`--last INTEGER`
:   Maximum number of events to fetch. For Snowflake App Runtime projects: number of log lines to retrieve (default: 500, capped at 100 KB). For Native App projects: can’t be used with `--first`. Default: -1.

`--follow, -f`
:   (Native App only) Continue polling for events. Implies `--last 20` unless overridden or `--since` is used. Default: False.

`--follow-interval INTEGER`
:   (Native App only) Polling interval in seconds when using `--follow`. Default: 10.

`--metric TEXT`
:   (Snowflake App Runtime only) With `--type metric`, return only this metric subset: `cpu`, `memory`, or `network`. Omit to return all metrics.

`--raw`
:   (Snowflake App Runtime only) With `--type metric`, emit raw metric values (bytes, cores) instead of human-readable conversions. Default: False.

`--instance INTEGER`
:   (Snowflake App Runtime only) Zero-based index of the service instance to retrieve logs from. Only valid with `--type log` and no `--since`/`--until`. Defaults to instance 0.

`--target TEXT`
:   (Snowflake App Runtime only) Name of the target (environment) declared in the `targets` block of `app.yml`. If you omit `--target`, the CLI uses the top-level `default_target`. Required when `targets` are declared and `default_target` is unset.

`--package-entity-id TEXT`
:   (Native App only) The ID of the package entity on which to operate when the definition\_version is 2 or higher.

`--app-entity-id TEXT`
:   (Native App only) The ID of the application entity on which to operate when the definition\_version is 2 or higher.

`--entity-id TEXT`
:   (Legacy `snowflake.yml` only) The ID of the snowflake-app entity on which to operate. Required if multiple snowflake-app entities exist. For `app.yml`, use `--target` instead.

`-p, --project TEXT`
:   Path where the Snowflake project is stored. Defaults to the current working directory.

`--env TEXT`
:   String in the format key=value. Overrides variables from the env section used for templates. Default: [].

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
:   Whether to opt in to single-use refresh token semantics. Default: `False`.

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

The active role needs the `MONITOR` privilege on the target Application Service to retrieve logs.

Live log output (`--type log` without `--since`/`--until`) is capped at 100 KB regardless of the `--last` value.

When you supply `--since` or `--until`, log output switches to the historical event table. There’s a short ingestion lag, and historical logs are available even after the service is suspended.

The `metric` and `lifecycle` streams read from the event table only and default to the last hour when no time window is given.

## Examples

- Fetch the default 500 lines of container logs:

  Copy code

  ```
  snow app events
  ```
- Fetch the last 100 lines:

  Copy code

  ```
  snow app events --last 100
  ```
- Fetch logs since a relative time window:

  Copy code

  ```
  snow app events --since 6h
  ```
- Fetch logs between two absolute timestamps:

  Copy code

  ```
  snow app events --since "2026-08-01 00:00:00" --until "2026-08-01 06:00:00"
  ```
- Fetch CPU and memory metrics:

  Copy code

  ```
  snow app events --type metric
  ```
- Fetch only CPU metrics with raw values:

  Copy code

  ```
  snow app events --type metric --metric cpu --raw
  ```
- Fetch lifecycle events from the last 2 days:

  Copy code

  ```
  snow app events --type lifecycle --since 2d
  ```
