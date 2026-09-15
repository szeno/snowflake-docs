# Monitor a native app

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how providers can monitor a Snowflake Native App across all consumer accounts. It covers application
health, performance, lifecycle and upgrade state, container health (for apps with containers), telemetry costs, and
usage and engagement patterns.

## Monitor application health

Providers can centrally monitor application health using the
[APPLICATION\_STATE view](/sql-reference/data-sharing-usage/application-state-view) in the
`SNOWFLAKE.DATA_SHARING_USAGE` schema of the provider account. Unlike event-table telemetry (which is
emitted per region and is only centralized if the provider builds an ETL or uses a third-party tool),
`APPLICATION_STATE` aggregates health and upgrade state across every region your listing is published to via
Cross-Cloud Auto-Fulfillment, without requiring consumer opt-in.

This view delivers:

- Centralized health across all consumer regions, with no per-region login required.
- Automatic health reporting that does not require consumers to enable event sharing.
- A minimal data footprint: only health and upgrade state columns are replicated, which keeps replication cost low
  and prevents data exfiltration.

Note

`APPLICATION_STATE` centralizes health and upgrade state only. Log, trace, metric, and lifecycle event data
stay in each consumer’s event table and (if shared) replicate to the provider’s event account in the same
region. To route shared events from multiple regions to a central location, see
[Configure centralized event sharing for an app](/developer-guide/native-apps/event-central).

### Set up health reporting

Each application instance reports its health using
[SYSTEM$REPORT\_HEALTH\_STATUS](/sql-reference/functions/system_report_health_status) with a status of
`OK`, `FAILED`, or `PAUSED`. The function returns `true` on success and `false` if the call is
rate-limited.

Health status can only be updated once every 55 minutes. If a report is attempted sooner, the function returns
`false` and the stored value isn’t changed. `PAUSED` can override this limit. The 55-minute cadence is the
built-in sampling for health: there is no separate sampling control. To adjust the volume of log, trace, and metric
telemetry, set `log_level`, `trace_level`, and `metric_level` (at app, schema, or object scope) and use
[event definitions](/developer-guide/native-apps/event-definition) to filter what is shared.

### Query health status

CoCo prompt: “Show me the latest health status for every consumer instance of my native app and sort by most
recent update.”

The following query returns the latest health status for every consumer instance of an app:

Copy code

```
SELECT
    CONSUMER_ORGANIZATION_NAME,
    CONSUMER_ACCOUNT_NAME,
    LAST_HEALTH_STATUS,
    LAST_HEALTH_STATUS_UPDATED_ON
FROM
    SNOWFLAKE.DATA_SHARING_USAGE.APPLICATION_STATE
WHERE
    PROVIDER_ACCOUNT_NAME = '<your_provider_account_name>'
    AND PACKAGE_NAME = '<your_application_package_name>'
ORDER BY
    LAST_HEALTH_STATUS_UPDATED_ON DESC;
```

The preceding query may return results similar to the following:

```
CONSUMER_ORGANIZATION_NAME    CONSUMER_ACCOUNT_NAME    LAST_HEALTH_STATUS    LAST_HEALTH_STATUS_UPDATED_ON
--------------------------    ---------------------    ------------------    -----------------------------
consumer_org_1                consumer_account_1       OK                    2026-04-15 10:30:00.000
consumer_org_2                consumer_account_2       FAILED                2026-04-15 09:45:00.000
consumer_org_3                consumer_account_3       PAUSED                2026-04-14 16:20:00.000
```

### Detect and respond to issues

Look for instances with the `FAILED` status, or instances with no recent update within the expected interval.
When an issue is detected, query the provider’s event table to read shared lifecycle events, log messages, and
trace events from the consumer’s instance to diagnose the root cause.

For the full column reference, including `UPGRADE_STATE`, `DISABLEMENT_REASONS`, and the
[BCR bundle 2026\_02](/release-notes/bcr-bundles/2026_02/bcr-2231) additions `UPGRADE_DEADLINE`,
`MAINTENANCE_STATE`, and `MAINTAIN_AFTER`, see the
[APPLICATION\_STATE view](/sql-reference/data-sharing-usage/application-state-view).

## Monitor application lifecycle events

Snowflake emits *application lifecycle events* (records with `RECORD_TYPE = 'EVENT'`) that complement the
`APPLICATION_STATE` view. While `APPLICATION_STATE` shows the current snapshot of every consumer instance,
lifecycle events give you the full per-instance event stream so you can replay history, build alerts, and
correlate state changes.

Supported lifecycle events:

- `upgrade_state` changes: every version transition across all instances, including `QUEUED`, `UPGRADING`,
  `COMPLETE`, `QUEUED_RETRY`, `FAILED`, `DISABLED`, and `QUEUED_DELAYED`.
- `health_status` updates: when an instance reports `OK`, `FAILED`, or `PAUSED` via
  [SYSTEM$REPORT\_HEALTH\_STATUS](/sql-reference/functions/system_report_health_status).
- `auto_grant` changes: when consumers grant or revoke privileges (for example, `CREATE COMPUTE POOL`,
  `CREATE WAREHOUSE`) to the app.

Common use cases:

- **Catch failing upgrades early.** Watch for `upgrade_state` transitions to `FAILED` or `QUEUED_RETRY` and
  alert on the failure reason before consumers open a support case.
- **Detect health regressions across the fleet.** Stream `health_status` transitions from `OK` to `FAILED`
  into your alerting tool to triage instance-by-instance.
- **Audit privilege changes.** When a consumer revokes `CREATE COMPUTE POOL` or another privilege, the
  `auto_grant` event lands in your event table within seconds; use it to tell support what changed.
- **Reconstruct an incident timeline.** Lifecycle events are timestamped, so you can correlate an upgrade attempt
  with a subsequent health failure and a consumer privilege revocation.

Example `VALUE` for an `auto_grant` event:

Copy code

```
VALUE = {
  "action": "REVOKED",
  "privileges": ["CREATE COMPUTE POOL", "CREATE WAREHOUSE"]
}
```

By default, lifecycle events are not logged. With
[BCR bundle 2026\_02](/release-notes/bcr-bundles/2026_02/bcr-2232) enabled, set
[LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) in the manifest to control which severity of lifecycle events is
recorded (`TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`, or `OFF`). Each level includes records
from all lower levels. If the BCR bundle is disabled, the `log_level` property controls which lifecycle events
are recorded instead.

CoCo prompt: “From my native app event table, show every upgrade\_state, health\_status, and auto\_grant change in
the last 7 days, grouped by consumer account.”

The following query returns lifecycle events for a specific app recorded in the past hour:

Copy code

```
SELECT TIMESTAMP, RESOURCE_ATTRIBUTES, RECORD, VALUE
  FROM <your_event_table>
  WHERE TIMESTAMP > DATEADD(hour, -1, CURRENT_TIMESTAMP())
    AND RESOURCE_ATTRIBUTES:"snow.application.name" = '<your_app_name>'
    AND RECORD_TYPE = 'EVENT'
    AND SCOPE:"name" = 'snow.application.lifecycle'
  ORDER BY TIMESTAMP DESC
  LIMIT 10;
```

## Monitor application performance

Snowflake Native Apps auto-instrument every stored procedure and UDF call with a SPAN that captures start time, duration,
error status, and error message. Python, Java, and Scala stored procedures and UDFs additionally emit METRIC
records for CPU and memory usage. SQL and JavaScript handlers emit SPANs only.

The following matrix summarizes the auto-instrumented telemetry by handler language:

| Handler language | Span (duration, status) | Metric (CPU, memory) |
| --- | --- | --- |
| SQL stored procedure or UDF | Yes | No |
| JavaScript stored procedure or UDF | Yes | No |
| Python stored procedure or UDF | Yes | Yes |
| Java stored procedure or UDF | Yes | Yes |
| Scala stored procedure | Yes | Yes |

Expand

Show lessSee more

For details, see [Trace events for functions and procedures](/developer-guide/logging-tracing/tracing) and
[Collecting metrics data](/developer-guide/logging-tracing/metrics).

CoCo prompt: “From my native app event table, show execution counts, average duration, error count, and success
rate for each auto-instrumented function and procedure over the last 24 hours.”

The following query returns execution counts, average duration, error counts, and success rate for each
auto-instrumented function and procedure in your event table:

Copy code

```
SELECT
    RESOURCE_ATTRIBUTES:"snow.executable.name"::string AS function_name,
    RESOURCE_ATTRIBUTES:"snow.executable.type"::string AS function_type,
    COUNT(*) AS total_executions,
    AVG(TIMESTAMPDIFF('millisecond', START_TIMESTAMP, TIMESTAMP)) AS avg_duration_ms,
    COUNT(CASE WHEN RECORD:"status":"code" = 'STATUS_CODE_ERROR' THEN 1 END) AS error_count,
    ROUND(1 - (error_count / NULLIF(total_executions, 0)), 3) AS success_rate
FROM <your_event_table>
WHERE RECORD_TYPE = 'SPAN'
  AND RECORD:"name" = 'snow.auto_instrumented'
GROUP BY function_name, function_type
ORDER BY total_executions DESC;
```

## Monitor SPCS containers

For Snowflake Native Apps with Snowpark Container Services, Snowflake emits platform events to the event table for service, service instance, and
container status changes. For containers, these include startup and readiness, image pull failures, resource
constraints (OOM kills), restarts, and error conditions. Events are written with
seconds-scale delay; Snowflake does not publish a platform-event latency SLA at this time.

For the full list of telemetry types available in containers (application logs, application metrics, application
traces, platform event logs, and platform metrics, with their preview status), see
[Snowpark Container Services: Monitoring Services](/developer-guide/snowpark-container-services/monitoring-services).

Configure platform metric collection in your service specification:

Copy code

```
platformMonitor:
  metricConfig:
    groups:
      - system
      - storage
      - network
      - status
```

Snowflake exports the selected metric groups to the event table. You can also scrape metrics directly from
compute pool nodes via the Prometheus-compatible endpoint for real-time monitoring or custom integrations. See
[Snowpark Container Services: Monitoring Services](/developer-guide/snowpark-container-services/monitoring-services) for the endpoint reference and metric
schema.

CoCo prompt: “Show SPCS platform events from the event table for my container service in the last 24 hours,
ordered by most recent.”

The following query returns SPCS platform events from the event table:

Copy code

```
SELECT *
FROM <your_event_table>
WHERE SCOPE:"name" = 'snow.spcs.platform'
ORDER BY TIMESTAMP DESC;
```

## Monitor application upgrades

The [APPLICATION\_STATE view](/sql-reference/data-sharing-usage/application-state-view) exposes upgrade
lifecycle columns: `UPGRADE_STATE`, `CURRENT_VERSION`, `TARGET_UPGRADE_VERSION`, `UPGRADE_FAILURE_REASON`,
`UPGRADE_ATTEMPT`, `UPGRADE_STARTED_ON`, and `UPGRADE_ATTEMPTED_ON`.

[BCR bundle 2026\_02](/release-notes/bcr-bundles/2026_02/bcr-2231) adds the following columns:

- `UPGRADE_DEADLINE`: the deadline by which an upgrade must be completed.
- `MAINTENANCE_STATE`: the current state of the application’s maintenance process. Possible values are
  `COMPLETED`, `QUEUED`, `INITIALIZING`, `IN_PROGRESS`.
- `MAINTAIN_AFTER`: the earliest time the system will begin maintenance.

To find instances with in-progress, queued, or failed upgrades, including the failure reason:

CoCo prompt: “Show every consumer instance of my native app whose upgrade is not in COMPLETE or DISABLED state,
including the failure reason and current version.”

Copy code

```
SELECT CONSUMER_ACCOUNT_NAME, CURRENT_VERSION, TARGET_UPGRADE_VERSION, UPGRADE_STATE, UPGRADE_FAILURE_REASON
FROM SNOWFLAKE.DATA_SHARING_USAGE.APPLICATION_STATE
WHERE UPGRADE_STATE NOT IN ('COMPLETE', 'DISABLED');
```

To find instances that successfully completed upgrades to the latest target version:

Copy code

```
SELECT CONSUMER_ACCOUNT_NAME, CURRENT_VERSION, TARGET_UPGRADE_VERSION, UPGRADE_STATE
FROM SNOWFLAKE.DATA_SHARING_USAGE.APPLICATION_STATE
WHERE UPGRADE_STATE = 'COMPLETE'
  AND CURRENT_VERSION = TARGET_UPGRADE_VERSION;
```

To find instances still finalizing the previous version due to active queries:

Copy code

```
SELECT CONSUMER_ACCOUNT_NAME, PREVIOUS_VERSION_STATE, PREVIOUS_VERSION
FROM SNOWFLAKE.DATA_SHARING_USAGE.APPLICATION_STATE
WHERE PREVIOUS_VERSION_STATE = 'FINALIZING';
```

Once an application is uninstalled, `APPLICATION_STATE` no longer includes that instance. For listings published
through Cross-Cloud Auto-Fulfillment, the view aggregates data across all regions.

## Manage telemetry costs

Telemetry costs scale with the volume of data emitted. For pricing details, see
[Costs of telemetry data collection](/developer-guide/logging-tracing/logging-tracing-billing).

Track overall telemetry credits and bytes ingested using
[EVENT\_USAGE\_HISTORY](/sql-reference/account-usage/event_usage_history):

CoCo prompt: “Show daily telemetry credits used and bytes ingested for my native app over the last 30 days.”

Copy code

```
SELECT DATE(START_TIME) AS usage_date,
       SUM(CREDITS_USED) AS credits_used,
       SUM(BYTES_INGESTED) AS bytes_ingested
FROM SNOWFLAKE.ACCOUNT_USAGE.EVENT_USAGE_HISTORY
GROUP BY usage_date
ORDER BY usage_date DESC;
```

Track per-app credits and storage in test environments using
[APPLICATION\_DAILY\_USAGE\_HISTORY](/sql-reference/account-usage/application_daily_usage_history):

Copy code

```
SELECT APPLICATION_NAME,
       USAGE_DATE,
       ROUND(CREDITS_USED, 3) AS daily_credits,
       ROUND(STORAGE_BYTES / POW(1024, 3), 2) AS storage_gb
FROM SNOWFLAKE.ACCOUNT_USAGE.APPLICATION_DAILY_USAGE_HISTORY
WHERE USAGE_DATE >= DATEADD(DAY, -7, CURRENT_DATE())
ORDER BY USAGE_DATE DESC;
```

Break down compute by service type:

Copy code

```
SELECT APPLICATION_NAME,
       f.value:serviceType::string AS service_type,
       ROUND(SUM(f.value:credits::float), 3) AS total_credits
FROM SNOWFLAKE.ACCOUNT_USAGE.APPLICATION_DAILY_USAGE_HISTORY,
     TABLE(FLATTEN(input => CREDITS_USED_BREAKDOWN)) f
GROUP BY APPLICATION_NAME, service_type
ORDER BY total_credits DESC;
```

To control telemetry volume, set `log_level`, `trace_level`, and `metric_level` at the most specific scope
that meets your monitoring needs (procedure or UDF, schema, or app), use
[event definitions](/developer-guide/native-apps/event-definition) to filter the records shared with the
provider, and configure regional event tables only in regions where the app has active usage.

## Understand app usage patterns

Use [LISTING\_ACCESS\_HISTORY](/sql-reference/data-sharing-usage/listing-access-history) to track daily query
volume and active consumer accounts by version and patch:

CoCo prompt: “For my native app, show daily query volume and active consumer accounts broken down by version and
patch.”

Copy code

```
SELECT APPLICATION_PACKAGE_NAME,
       APPLICATION_VERSION,
       APPLICATION_PATCH_ID,
       DATE(QUERY_DATE) AS usage_date,
       COUNT(DISTINCT QUERY_TOKEN) AS total_queries,
       COUNT(DISTINCT CONSUMER_ACCOUNT_NAME) AS active_accounts
FROM SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY
WHERE IS_APPLICATION = TRUE
GROUP BY APPLICATION_PACKAGE_NAME, APPLICATION_VERSION, APPLICATION_PATCH_ID, usage_date
ORDER BY usage_date DESC;
```

Flatten `APPLICATION_OBJECTS_ACCESSED` to see which procedures, functions, tables, or views are accessed most
often:

CoCo prompt: “For my native app, which procedures, functions, tables, or views are accessed most, and by how
many distinct consumer accounts?”

Copy code

```
SELECT APPLICATION_PACKAGE_NAME,
       f.value:"objectName"::string AS object_name,
       f.value:"objectDomain"::string AS object_type,
       COUNT(DISTINCT QUERY_TOKEN) AS access_count,
       COUNT(DISTINCT CONSUMER_ACCOUNT_NAME) AS user_count
FROM SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY,
     LATERAL FLATTEN(input => APPLICATION_OBJECTS_ACCESSED) f
WHERE IS_APPLICATION = TRUE
GROUP BY APPLICATION_PACKAGE_NAME, object_name, object_type
ORDER BY access_count DESC;
```

## Monitor consumer engagement

Use [LISTING\_CONSUMPTION\_DAILY](/sql-reference/data-sharing-usage/listing-consumption-daily) to track weekly
and monthly usage trends, regional adoption patterns, and engaged customers. Data has up to a 2-day latency and is
retained for 365 days.

## Monitor app acquisition funnel

Use [LISTING\_TELEMETRY\_DAILY](/sql-reference/data-sharing-usage/listing-telemetry-daily) and
[LISTING\_EVENTS\_DAILY](/sql-reference/data-sharing-usage/listing-events-daily) to track:

- Discovery: unique account views by region and viewing trends.
- Conversion: view-to-get rate, get-to-install rate, overall funnel conversion.
- Retention: uninstall trends by region and paid listing cancellations.

Uninstall events are currently available for paid listings. Support for trial and free listings is not yet available.
