# Best practices and scenarios for native app observability

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic collects best practices and reusable patterns for observability in Snowflake Native Apps. Use it once you have
the basics in place (event sharing configured, manifest set, and `APPLICATION_STATE` in your daily monitoring
rhythm).

## Best practices

### Maintenance

Audit your telemetry configuration and volume regularly. Event tables themselves are reliable; the common gotcha
is an app version upgrade that inherits a more verbose log or trace level, or a new library that emits more
records than expected. A weekly check against
[EVENT\_USAGE\_HISTORY](/sql-reference/account-usage/event_usage_history) catches cost spikes early.

Review retention policies based on your organization’s needs. Remove or archive old data periodically to manage
storage costs.

As your app expands to new regions, make sure each region has either an active event account (with an event
table) or routes through [centralized event sharing](/developer-guide/native-apps/event-central).

### Security

Routinely review access policies for your event tables so only authorized roles can view or modify telemetry data.
Use the `EVENTS_ADMIN` and `EVENTS_VIEWER` database roles or apply custom row-access and masking policies on
custom event tables.

Do not emit confidential or consumer-identifying data in log messages, trace events, or metrics. Snowflake masks
or omits known consumer identifiers, but it cannot redact data your app puts into the message body or attributes.

## Centralizing across regions

Events only share within the same region. To centralize across regions and clouds, choose one of:

- [Configure centralized event sharing for an app](/developer-guide/native-apps/event-central) (recommended): the Snowflake Native App Framework’s built-in centralized event sharing.
  Define routing rules per region and route to a single destination account, without operating per-region event
  accounts yourself.
- A provider-managed ETL: build a job that reads each per-region event account and writes into a consolidated
  table. Best for cases where you need transformations or enrichment that don’t fit a routing rule.
- A third-party observability tool that reads event tables across regions. See
  [Route telemetry to third-party observability tools](/developer-guide/native-apps/native-apps-third-party-observability).

## Per-instance log and trace levels via data shares

Providers can configure instance-specific telemetry without rebuilding the manifest by sharing a small mapping
table from the provider account to installed apps:

1. Create a table in the provider account with columns such as `account_id`, `log_level`, `trace_level`,
   `metric_level`.
2. Share the table to consumer accounts using a regular Secure Data Share or Cross-Cloud Auto-Fulfillment.
3. In the app’s setup script or runtime code, query the shared table and call
   [ALTER SCHEMA](/sql-reference/sql/alter-schema),
   [ALTER PROCEDURE](/sql-reference/sql/alter-procedure), or
   [ALTER FUNCTION](/sql-reference/sql/alter-function) to apply the mapped levels at object scope.

Note

Object-scope `ALTER` statements do not survive an app upgrade if the setup script re-creates those objects.
Re-apply the mapped levels from a post-upgrade callback (or from the setup script after object creation) so
the configuration persists across versions.

Keep the schema simple. Standardize across customer tiers (for example, “trial”, “premium”, “enterprise”) rather
than maintaining a unique configuration per consumer account, otherwise the matrix becomes hard to operate.

## In-app telemetry store for customer-facing diagnostics

In addition to Snowflake’s event table, providers can maintain a custom table inside the app to power in-product
monitoring and support experiences. Writing core health metrics, version deployments, and critical state changes
to this dedicated table lets you build dashboards or status pages directly into the app for consumers to
self-serve troubleshooting.

This is **not** a Snowflake event table. Snowflake’s logging, trace, and metric APIs do not write to a custom app
table; they write to the consumer’s active event table. To populate an in-app telemetry store, the app code must
capture and `INSERT` records itself, typically inside the handler that catches an error or at the end of a
procedure.

Use this pattern when you want the data visible inside the consumer’s app UI and under your own retention and
schema policies.

## Simplify monitoring with Snowflake Trail

Once telemetry is enabled, Snowflake Trail provides built-in dashboards for app performance and resource usage.
You can:

- Query the event table directly for custom monitoring.
- Use Snowsight’s built-in observability dashboards.
- Integrate with Observe, Datadog, or PagerDuty for alerting and downstream tooling.

For an overview of Snowflake’s logging and tracing experience, see
[Logging, tracing, and metrics](/developer-guide/logging-tracing/logging-tracing-overview).
