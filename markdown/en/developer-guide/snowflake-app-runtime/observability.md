# Observability for Snowflake App Runtime

This topic describes how to inspect the state of a running Application
Service and how to read its container logs. In [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli)
or [Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop/building-apps), you can
ask the agent to check status, show logs, or diagnose deployment issues. For example:
`Show me the logs for my warehouse-monitor app`.

## Check service status

Use [SHOW APPLICATION SERVICES](/sql-reference/sql/show-application-services) to list services you can see, along with
their current state, deployed package, and version:

Copy code

```
SHOW APPLICATION SERVICES;
```

Use [DESCRIBE APPLICATION SERVICE](/sql-reference/sql/desc-application-service) to inspect a single service in more
detail:

Copy code

```
DESCRIBE APPLICATION SERVICE my_db.my_schema.my_app;
```

A service can be in one of the following states:

- `PENDING`: the service is starting up.
- `RUNNING`: the service is running and can accept requests.
- `SUSPENDING`: a suspend is in progress.
- `SUSPENDED`: the service is stopped and not consuming compute.
- `FAILED`: a container in the service encountered an unrecoverable error.
- `FAILING`: the service is transitioning to a failed state.
- `DONE`: the service ran to completion (job-style runs only).
- `CANCELLED`: a job-style run was cancelled.
- `CANCELLING`: a cancel is in progress.
- `DELETING`: a drop is in progress.
- `DELETED`: the service has been dropped.
- `INTERNAL_ERROR`: the service is in an unexpected internal state.

## Read container logs and telemetry

The fastest way to read container logs is with the Snowflake CLI:

Copy code

```
snow app events
snow app events --last 1000
```

By default, the command returns the 500 most recent log lines for the
Application Service defined in your `app.yml` (`--type log`). Pass `--target`
when the manifest defines named targets. Output is
capped at 100 KB.

Use `--type` to select another observability stream:

Copy code

```
# Historical logs from the event table (works after suspend; short ingestion lag)
snow app events --type log --since 6h

# CPU / memory / network metrics from the event table
snow app events --type metric --metric cpu --since 1h

# Service and container lifecycle events
snow app events --type lifecycle --since 2d
```

`--since` and `--until` accept relative shorthand such as `30m`, `6h`, or `2d`,
or an absolute UTC timestamp. Metric and lifecycle streams are historical and
default to the last hour when you don’t pass a time window. With `--type metric`, use `--metric cpu`, `memory`, or `network`, and `--raw` for
unconverted values.

You can also read live container logs with SQL using
[SYSTEM$GET\_APPLICATION\_SERVICE\_LOGS](/sql-reference/functions/system_get_application_service_logs).
The second argument limits the number of lines returned (default: 500). For a
multi-instance service, pass a third argument to choose the instance by its
number, starting from 0:

Copy code

```
SELECT SYSTEM$GET_APPLICATION_SERVICE_LOGS('my_db.my_schema.my_app');
SELECT SYSTEM$GET_APPLICATION_SERVICE_LOGS('my_db.my_schema.my_app', 1000);
SELECT SYSTEM$GET_APPLICATION_SERVICE_LOGS('my_db.my_schema.my_app', 500, 1);
```

The role that reads logs needs the MONITOR privilege on the service.

## Quick troubleshooting runbook

Use this sequence when a deploy or running app looks unhealthy:

1. Check service health:

   Copy code

   ```
   DESCRIBE APPLICATION SERVICE my_db.my_schema.my_app;
   ```
2. Confirm the service appears in inventory:

   Copy code

   ```
   SHOW APPLICATION SERVICES IN SCHEMA my_db.my_schema;
   ```
3. Pull recent logs quickly:

   Copy code

   ```
   snow app events --last 500
   ```
4. Pull logs with SQL for scripts and worksheets:

   Copy code

   ```
   SELECT SYSTEM$GET_APPLICATION_SERVICE_LOGS('my_db.my_schema.my_app', 500);
   ```
5. If `ALTER APPLICATION SERVICE ... RESUME` fails with a blocked runtime
   image error, upgrade to a new package version before resuming. See
   [Usage notes](/sql-reference/sql/alter-application-service#label-alter-application-service-usage-notes).

If the service endpoint is not available, run
[`snow app open --print-only`](/developer-guide/snowflake-cli/command-reference/snowflake-app-runtime-commands/open)
to check whether the URL is resolvable from the current deployment state.

## Use an event table for structured logs

For persistent, queryable logs, configure an active event table on your
account and emit structured logs from your application code. The event table
receives logs, metrics, and traces emitted by your containers and by
Snowflake. For more information, see
[Logging, tracing, and metrics](/developer-guide/logging-tracing/logging-tracing-overview). Treat event table
access as sensitive: anyone with `SELECT` on it can read logs from every
Application Service. Don’t log query results, tokens, or secrets. See
[Avoid logging sensitive data](/developer-guide/snowflake-app-runtime/secure-development#label-snowflake-app-runtime-secure-development-logging)
and
[Governing log access](/developer-guide/snowflake-app-runtime/security#label-snowflake-app-runtime-security-observability).

## See also

- [Cost and credit usage for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/cost): credit usage and cost monitoring for App Runtime.
- [SNOWFLAKE\_APP\_RUNTIME\_COMPUTE\_HISTORY view](/sql-reference/account-usage/snowflake_app_runtime_compute_history): hourly App Runtime credit usage view.
