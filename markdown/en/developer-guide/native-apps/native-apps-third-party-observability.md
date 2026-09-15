# Route telemetry to third-party observability tools

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how providers can route Snowflake Native App telemetry from their event account to a third-party
observability tool. Snowflake event tables are OpenTelemetry-compatible, so any OTel-aware backend can read them.

## Observe (Snowflake)

Observe is part of Snowflake. It is the first-party path for AI-powered observability on top of Snowflake event
tables. Observe natively reads native app log messages, trace events, and metrics, and centralizes them across
regions and consumer accounts. Use Observe when you want a managed observability experience without operating an
ETL pipeline yourself.

For background on the acquisition and what it unlocks for native apps, see
[Snowflake completes Observe acquisition](https://www.snowflake.com/en/blog/observe-acquisition-ai-powered-observability/).

## Datadog

Datadog’s Snowflake integration reads event tables so you can consolidate log messages and trace events from
multiple deployments, accounts, and regions into a single Datadog dashboard. Use Datadog if you already standardize
your operational monitoring on Datadog.

For configuration details, see
[Monitor Snowflake Snowpark with Datadog](https://www.datadoghq.com/blog/snowpark-monitoring-datadog/).

## Other OpenTelemetry-compatible backends

Because event tables are OpenTelemetry-compatible, you can forward records to other backends such as Grafana,
Elastic, or Splunk by:

- Building a Snowflake-side ETL job that reads the event table and pushes records to the destination.
- Routing events through your provider event account using
  [centralized event sharing](/developer-guide/native-apps/event-central) and exporting from there.
- Using [COPY INTO](/sql-reference/sql/copy-into-location) with an external stage to batch-export event
  records to cloud storage (S3, Azure Blob, GCS), where any downstream tool can ingest them. This is often the
  simplest path for smaller providers.

## Choosing between approaches

- If centralizing across regions is the primary goal, prefer
  [Configure centralized event sharing for an app](/developer-guide/native-apps/event-central) over a custom solution.
- For smaller deployments, an in-house ETL job that reads the event table and pushes to your existing tooling is
  often the lowest-cost option.
- For larger deployments, or when AI-driven analysis is a requirement, Observe or Datadog typically pays for
  itself in operator time.

Whichever path you choose, validate the end-to-end pipeline using the checklist in
[Test observability for an app](/developer-guide/native-apps/native-apps-observability-testing).
