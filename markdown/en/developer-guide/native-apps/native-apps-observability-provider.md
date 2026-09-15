# Provider guide: Observability for native apps

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic is the entry point for providers configuring observability for a Snowflake Native App. It covers how to emit
telemetry, share events back to your event account, run cross-region centralized sharing, monitor every consumer
instance, and route telemetry to third-party tools.

For an overview of how telemetry flows through native apps, see
[Use logging and event tracing for an app](/developer-guide/native-apps/event-about).

## What providers do

As a provider, you are responsible for the following observability tasks:

- **Emit telemetry from your app code.** Configure log, trace, metric, and event levels in the manifest, with
  optional object-level overrides for individual schemas, stored procedures, and UDFs. See
  [Configure event definitions for an app](/developer-guide/native-apps/event-definition).
- **Centralize event sharing across regions (recommended).** Use centralized event sharing to route telemetry
  from every region to a single destination account, without operating per-region event accounts. See
  [Configure centralized event sharing for an app](/developer-guide/native-apps/event-central).
- **Set up per-region event sharing (fallback).** When centralized event sharing is not an option, designate an
  event account in every region your listing is published, create an event table, and register the event account
  for that region. See [Set up and manage an event table in the provider account](/developer-guide/native-apps/event-manage-provider).
- **Verify event sharing in consumer accounts.** Use system functions or the Python Permission SDK to gate app
  features on whether the consumer has enabled mandatory event definitions. See
  [Determine information about event sharing in the consumer account](/developer-guide/native-apps/event-develop).
- **Test observability before publishing.** Validate cross-account and same-account telemetry collection. See
  [Test observability for an app](/developer-guide/native-apps/native-apps-observability-testing).
- **Monitor health, performance, lifecycle, upgrades, and cost.** Use `APPLICATION_STATE`, the event table, and
  the data-sharing-usage views. See [Monitor a native app](/developer-guide/native-apps/monitoring).
- **Route telemetry to a third-party observability tool (optional).** Snowflake event tables are
  OpenTelemetry-compatible, so any OTel consumer can read them. First-party path is Observe.
  See [Route telemetry to third-party observability tools](/developer-guide/native-apps/native-apps-third-party-observability).

## Reading order

If you are setting up observability for a new app, work through the topics in this order:

1. [Set up and manage an event table in the provider account](/developer-guide/native-apps/event-manage-provider) - set up the event account and event table.
2. [Configure event definitions for an app](/developer-guide/native-apps/event-definition) - configure the manifest, event definitions, and
   object-level overrides.
3. [Configure centralized event sharing for an app](/developer-guide/native-apps/event-central) - if you ship in more than one region, set up centralized
   event sharing.
4. [Determine information about event sharing in the consumer account](/developer-guide/native-apps/event-develop) - gate app features on event-sharing enablement.
5. [Test observability for an app](/developer-guide/native-apps/native-apps-observability-testing) - validate end-to-end before publishing.
6. [Monitor a native app](/developer-guide/native-apps/monitoring) - daily monitoring of health, performance, upgrades, and cost.
7. [Route telemetry to third-party observability tools](/developer-guide/native-apps/native-apps-third-party-observability) - optionally route to Observe,
   Datadog, or another OTel-compatible backend.

For best practices and reusable patterns (Snowflake Trail, per-instance log levels via data shares, in-app
telemetry stores), see
[Best practices and scenarios for native app observability](/developer-guide/native-apps/native-apps-observability-scenarios).

## Consumer documentation

For the consumer-side workflow (set up an event table, enable event sharing, privacy and masking, cost ownership),
see [Set up event tracing for an app](/developer-guide/native-apps/ui-consumer-enable-logging).
