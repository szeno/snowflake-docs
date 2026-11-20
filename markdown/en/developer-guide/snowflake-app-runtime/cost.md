# Cost and credit usage

This topic describes how Snowflake bills compute used by
[Snowflake App Runtime](/developer-guide/snowflake-app-runtime/about-snowflake-app-runtime)
and where to track that usage.

## How App Runtime compute is billed

Snowflake App Runtime usage appears in
[METERING\_HISTORY](/sql-reference/account-usage/metering_history) and
[METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history)
under these service types:

| Service type | Description |
| --- | --- |
| `SNOWFLAKE_APP_RUNTIME` | Compute used to build and host Snowflake App Runtime services on managed compute. |
| `SNOWFLAKE_APP_RUNTIME_SERVERLESS` | Compute used to run Snowflake App Runtime services on serverless compute (`compute_resource: SERVERLESS`). |
| `SNOWFLAKE_APP_RUNTIME_PREVIEW` | Compute used to preview Snowflake App Runtime apps in Snowsight Workspaces. |

Expand

Show lessSee more

How credits are attributed depends on the app’s compute resource:

- **Managed compute.** All apps in an account share
  Snowflake-managed compute. Snowflake bills credit usage at the account level
  under the `SNOWFLAKE_APP_RUNTIME` service type, separate from your warehouses
  and other compute. You can’t see credits for individual apps.
- **Serverless compute.** Snowflake reports credits for each Application
  Service under the `SNOWFLAKE_APP_RUNTIME_SERVERLESS` service type, so you can see
  what each app costs. See [Find credit usage for each app](#label-snowflake-app-runtime-cost-per-app).
- **Workspaces preview.** Snowflake reports credits for the user who ran
  the preview under the `SNOWFLAKE_APP_RUNTIME_PREVIEW` service type. See
  [Find credit usage for Workspaces preview](#label-snowflake-app-runtime-cost-workspaces).

### Credit rate

Managed compute credits are charged per compute-hour at the rate listed in the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
under “Serverless Feature Credit Table” for the `SNOWFLAKE_APP_RUNTIME` service
type. Managed compute uses `CPU_X64_S` nodes (3 vCPU, 13 GiB RAM).
This rate reflects a discount relative to the equivalent self-managed SPCS
compute pool node rate.

You aren’t billed per request or per concurrent user. Cost depends on how
long the underlying compute nodes run, regardless of whether your app is
handling traffic.

You pay for nodes, not instances. App Runtime packs multiple instances onto
a node when resource requests allow it, so a new node is added only when
existing ones are full.

### Billing lifecycle

On managed compute, App Runtime billing follows the same lifecycle as SPCS compute pools. For
details on how costs accrue in each state (ACTIVE, IDLE, SUSPENDED), see
[Compute pool cost](/developer-guide/snowpark-container-services/accounts-orgs-usage-views#label-compute-pool-cost).

Apps left running while idle still accrue credits. To stop an app you don’t
need, see [Start, stop, and scale a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/scale-and-suspend).

On serverless compute, an app accrues credits only while it runs. Snowflake
starts the app on the first request and stops it after the idle period set by
`auto_suspend_secs`, so an app with no traffic doesn’t consume compute.

## Find App Runtime usage in metering views

App Runtime credits appear in the same metering views that report other
Snowflake compute usage:

- [METERING\_HISTORY](/sql-reference/account-usage/metering_history): hourly
  credit usage for the last 365 days.
- [METERING\_DAILY\_HISTORY](/sql-reference/account-usage/metering_daily_history):
  daily credit usage rolled up by service type.

For cross-account roll-ups, use organization-level metering views such as
[USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily).

The following query returns hourly App Runtime credit usage for the last 30
days. Filter `service_type` to one value to see a single compute type:

Copy code

```
SELECT
    start_time,
    end_time,
    service_type,
    credits_used_compute
FROM snowflake.account_usage.metering_history
WHERE service_type IN (
    'SNOWFLAKE_APP_RUNTIME',
    'SNOWFLAKE_APP_RUNTIME_SERVERLESS',
    'SNOWFLAKE_APP_RUNTIME_PREVIEW')
  AND start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
```

## Find credit usage for each app

Snowflake reports managed compute credits at the account level, so you can’t
break them down by app. Apps on serverless compute (Public Preview) report
credits for each app.

In [METERING\_HISTORY](/sql-reference/account-usage/metering_history), each
serverless row has `SERVICE_TYPE` set to `SNOWFLAKE_APP_RUNTIME_SERVERLESS`,
`ENTITY_TYPE` set to `APPLICATION SERVICE`, and `ENTITY_ID` set to the
service’s unique ID. `DATABASE_NAME`, `SCHEMA_NAME`, and `NAME` identify the
Application Service.

You can also query
[SNOWFLAKE\_APP\_RUNTIME\_COMPUTE\_HISTORY](/sql-reference/account-usage/snowflake_app_runtime_compute_history)
for hourly serverless credits for each app:

Copy code

```
SELECT
  start_time,
  end_time,
  application_service_name,
  credits_used
FROM snowflake.account_usage.snowflake_app_runtime_compute_history
WHERE compute_type = 'SERVERLESS'
  AND start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
```

In METERING\_HISTORY, group by `ENTITY_ID` rather than by name. A service that you drop and recreate
under the same name gets a new ID, so it counts as a separate app.

To total credits for each app:

Copy code

```
SELECT
  entity_id,
  database_name,
  schema_name,
  name AS application_service_name,
  SUM(credits_used) AS credits_used
FROM snowflake.account_usage.metering_history
WHERE service_type = 'SNOWFLAKE_APP_RUNTIME_SERVERLESS'
  AND entity_type = 'APPLICATION SERVICE'
GROUP BY 1, 2, 3, 4
ORDER BY credits_used DESC;
```

To see daily credit usage for one app over the last 30 days:

Copy code

```
SELECT
  DATE_TRUNC('day', start_time) AS usage_date,
  SUM(credits_used) AS credits_used
FROM snowflake.account_usage.metering_history
WHERE service_type = 'SNOWFLAKE_APP_RUNTIME_SERVERLESS'
  AND entity_type = 'APPLICATION SERVICE'
  AND database_name = 'MY_DB'
  AND schema_name = 'MY_SCHEMA'
  AND name = 'MY_APP'
  AND start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY 1
ORDER BY 1;
```

Per-app credits cover serverless compute only. Usage on the managed compute
pool isn’t broken down by app, so per-app totals don’t add up to the account’s
total App Runtime usage when you use both compute resources.

To query METERING\_HISTORY, your role needs access to the `SNOWFLAKE.ACCOUNT_USAGE`
schema, for example through the `USAGE_VIEWER` database role or `IMPORTED PRIVILEGES`
on the `SNOWFLAKE` database. See [Account Usage](/sql-reference/account-usage).

Usage can take up to three hours to appear in Account Usage views.

## Find credit usage for Workspaces preview

[![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

When you preview an app in a Snowsight workspace, usage appears in metering
views with the service type `SNOWFLAKE_APP_RUNTIME_PREVIEW`. Each row is
attributed to the user who ran the preview, not to an Application Service. See
[Develop Snowflake App Runtime apps in Snowsight Workspaces](/developer-guide/snowflake-app-runtime/workspaces).

To see hourly preview credit usage for the last 30 days:

Copy code

```
SELECT
  start_time,
  end_time,
  credits_used
FROM snowflake.account_usage.metering_history
WHERE service_type = 'SNOWFLAKE_APP_RUNTIME_PREVIEW'
  AND start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
```

To total preview credits for each user, query
[SNOWFLAKE\_APP\_RUNTIME\_COMPUTE\_HISTORY](/sql-reference/account-usage/snowflake_app_runtime_compute_history)
where `compute_type` is `PREVIEW`:

Copy code

```
SELECT
  user_id,
  SUM(credits_used) AS credits_used
FROM snowflake.account_usage.snowflake_app_runtime_compute_history
WHERE compute_type = 'PREVIEW'
GROUP BY user_id;
```

To stop a preview before it suspends on its own, select **Shutdown** from the
Preview pane’s menu. Closing the pane leaves the dev server running until it
goes idle.

## Inspect App Runtime credit usage

For a focused view of App Runtime credit usage, query
[SNOWFLAKE\_APP\_RUNTIME\_COMPUTE\_HISTORY](/sql-reference/account-usage/snowflake_app_runtime_compute_history).
The view returns hourly credit usage for each compute type over the last 365
days. Use `compute_type` to tell the rows apart:

- `MANAGED COMPUTE POOL`: one row per account per hour.
- `SERVERLESS`: one row per Application Service per hour.
- `PREVIEW`: one row per user per hour for Workspaces previews.

Copy code

```
SELECT
    start_time,
    end_time,
    compute_type,
    credits_used
FROM snowflake.account_usage.snowflake_app_runtime_compute_history
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
```

## Reduce App Runtime cost

On managed compute, an app runs until you suspend or drop it, so a deployed
app that nobody uses still consumes compute. To control cost:

- **Migrate to serverless compute** for apps with intermittent traffic.
  Serverless apps stop when idle and report credits for each app. See
  [Move an existing app to serverless compute](/developer-guide/snowflake-app-runtime/serverless#label-snowflake-app-runtime-serverless-switch).
- **Drop unused apps.** Use
  [`DROP APPLICATION SERVICE`](/sql-reference/sql/drop-application-service)
  to permanently remove apps you no longer need.
- **Monitor app state.** Use
  [Monitor a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/observability)
  to find apps stuck in unexpected states that may still be consuming compute.

## Next steps

- Set how long a serverless app stays idle before it stops: [Set the idle timeout](/developer-guide/snowflake-app-runtime/scale-and-suspend#label-snowflake-app-runtime-scale-idle-timeout).
- Query hourly App Runtime credit usage: [SNOWFLAKE\_APP\_RUNTIME\_COMPUTE\_HISTORY view](/sql-reference/account-usage/snowflake_app_runtime_compute_history).
