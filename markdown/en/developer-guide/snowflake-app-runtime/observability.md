# Monitor an app

This topic describes how to check the state of a running Application
Service, read its logs, metrics, and lifecycle events, and work through common
problems. In [Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli)
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

On [serverless compute](/developer-guide/snowflake-app-runtime/serverless)
(Public Preview), the `compute_resource` column in `SHOW APPLICATION SERVICES`
output shows `SERVERLESS`. A serverless app that stopped after its idle period
shows `SUSPENDED` with `current_instances` at `0`. That’s expected: the next
request starts it again, so you don’t resume it.

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

On managed compute, use `--type` to select another stream. Serverless apps
support only `--type log`; see
[On serverless compute, live logs come from the running instance, so you can](/developer-guide/snowflake-app-runtime/observability#label-snowflake-app-runtime-observability-serverless-logs).

Copy code

```
# Historical logs from the event table (works after the app stops; short ingestion lag)
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

On serverless compute, live logs come from the running instance, so you can
read them only while the app runs. While the app isn’t running, live logs fail
with `Failed to retrieve CNG app logs from the orchestrator.` To see logs from a
stopped app, open the app to start it, or read historical logs from the event
table instead:

Copy code

```
SELECT SYSTEM$GET_APPLICATION_SERVICE_EVENT_TABLE_DATA('<db>.<schema>.<app>', 'LOG');
```

The function returns the log records as a JSON array.

Serverless apps write logs to the event table, but not metrics or lifecycle
events: the `METRIC` and `EVENT` types return no rows, and `snow app events`
doesn’t support `--type metric` or `--type lifecycle` for them. To query the
event table directly, filter on the `snow.app.name` resource attribute.
Serverless rows also carry `snow.database.name`, `snow.schema.name`, and
`snow.service.instance`, but not `snow.application_service.name`. See
[Snowflake App Runtime limitations](/developer-guide/snowflake-app-runtime/limitations).

### Read preview logs in Workspaces

When you preview an app in a Snowsight workspace (Public Preview), the Preview
pane shows the dev server’s live logs, refreshed every few seconds.
Lines tagged `[APP]` come from your app’s standard output and standard error.
Lines tagged `[PREVIEW]` come from the preview itself: sync, install, and status
changes. Until the dev server is up, the pane shows `Container not ready`.
Preview logs don’t go to an event table.
See [Develop Snowflake App Runtime apps in Snowsight Workspaces](/developer-guide/snowflake-app-runtime/workspaces).

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
Snowflake. On serverless compute, the event table receives logs only. For more information, see
[Logging, tracing, and metrics](/developer-guide/logging-tracing/logging-tracing-overview). Treat event table
access as sensitive: anyone with `SELECT` on it can read logs from every
Application Service. Don’t log query results, tokens, or secrets. See
[Avoid logging sensitive data](/developer-guide/snowflake-app-runtime/secure-development#label-snowflake-app-runtime-secure-development-logging)
and
[Governing log access](/developer-guide/snowflake-app-runtime/security#label-snowflake-app-runtime-security-observability).

## Next steps

- Fix common deploy and runtime errors: [Troubleshoot Snowflake App Runtime apps](/developer-guide/snowflake-app-runtime/troubleshooting).
- See what your apps cost: [Cost and credit usage for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/cost).
