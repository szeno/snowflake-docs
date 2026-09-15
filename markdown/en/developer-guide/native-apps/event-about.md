# Use logging and event tracing for an app

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how providers can configure a Snowflake Native App to record log messages and trace events.

This guide covers both provider and consumer responsibilities. Provider topics cover how to emit, share, and centrally
monitor telemetry from apps installed in consumer accounts. Consumer topics cover how to set up an event table,
control what is shared back to the provider, and understand the cost model. Section headings are labeled accordingly.

## About log messages and trace events in an app

The Snowflake Native App Framework supports using the Snowflake [logging and tracing](/developer-guide/logging-tracing/logging-tracing-overview)
functionality to gather information about an app. Providers can configure an app to record and analyze the following:

- [Log messages](/developer-guide/logging-tracing/logging): independent, detailed messages with information about
  the state of a specific piece of app code.
- [Trace events](/developer-guide/logging-tracing/tracing): structured data that providers can use to get
  information spanning and grouping multiple parts of your code. Trace events allow an app to emit information
  related to its performance and behavior.
- [Metrics](/developer-guide/logging-tracing/metrics): information about stored procedure and UDF resource
  consumption based on the CPU and memory metrics that Snowflake generates.

App telemetry is written to the active [event table](/developer-guide/logging-tracing/event-table-setting-up)
in the consumer account. The default `SNOWFLAKE.TELEMETRY.EVENTS` table is active in every account out of the
box. Customers can also create a custom event table and set it as the active table to isolate app telemetry from
other account events. Snowflake ships two default database roles for access control: `EVENTS_ADMIN` (manage
row-access policies and delete data) and `EVENTS_VIEWER` (read-only access to the masked
`SNOWFLAKE.TELEMETRY.EVENTS_VIEW`). For containerized apps, container telemetry types are listed in
[Snowpark Container Services: Monitoring Services](/developer-guide/snowpark-container-services/monitoring-services).

To configure an app to emit log messages and trace events, providers set the log and trace levels in the manifest file.
See [Set the log and trace levels for an app](/developer-guide/native-apps/event-definition#label-nativeapps-provider-logging-configure).

Providers can also configure an app to use event sharing to allow the consumer to share the log messages
and trace events with the provider. See [About event sharing](#label-nativeapps-provider-logging-about-events) for
more information.

## About event sharing

Event sharing allows the provider to collect information about an app’s performance and behavior.
A provider can configure an app to request that the consumers share the log messages
and trace events with the provider. Event sharing requires that the provider and consumer configure an
event table in their account to store the log messages and trace events emitted by the app.

When event sharing is enabled, the log messages and trace events that are inserted into the event table in the
consumer account are also inserted into the event table in the provider account.

Providers can also use [centralized event sharing](/developer-guide/native-apps/event-central) to route
telemetry from multiple regions to a central location.

Note

The only events with a `RECORD_TYPE` of `EVENT` that support event
sharing are Snowflake Native Apps application lifecycle events and Snowpark Container Services platform events.

## Considerations when using event sharing

Before configuring logging and event sharing for an app, providers must consider the following:

- Providers are responsible for all costs associated with event sharing on the provider side, including data
  ingestion and storage.
- Providers must have [an account to store shared events](/developer-guide/native-apps/event-manage-provider#label-nativeapps-provider-logging-configure-event-account)
  in each region where you want to support event sharing.
- Providers must define the default log level and trace level for an app in the manifest file.

## Considerations when migrating from the previous event sharing functionality

When migrating from the existing event sharing functionality to use event definitions, providers
should consider the following.

- The previous event sharing functionality is equivalent to the OPTIONAL ALL event definition.
- Published versions and patches of an app that used the previous functionality will have the
  OPTIONAL ALL event definition by default. Providers do not need to add this event definition
  to the manifest file.

To begin using event definitions, providers can add supported event definitions to the manifest
file. This is applicable to new apps as well as new versions and patches of existing apps.

Note

To being begin requesting more granular log and event sharing, providers only have to add
event definitions to the manifest file. No other actions are required for providers.

## Workflow - Set up event sharing for an app

Event sharing allows consumers to share log messages and trace events with the provider.

The following workflow shows how to set up and enable event sharing for an app:

1. The provider [sets the log and trace levels](/developer-guide/native-apps/event-definition#label-nativeapps-provider-logging-configure)
   for the app.
2. The provider [adds event definitions](/developer-guide/native-apps/event-definition#label-nativeapps-event-definitions-add) to the manifest file.

   Event definitions act as filters on the log messages and trace events emitted by the app.
   Providers can configure event definitions to be required or optional.
3. The provider [sets up an event table](/developer-guide/native-apps/event-manage-provider#label-nativeapps-provider-logging-configure-event-account)
   in their organization.
4. The provider publishes the app.

When a consumer installs an app, they can set up an event table and enable event sharing.
See [Enable logging and event sharing for an app](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging)
for more information on the consumer requirements for event sharing.

## Monitor consumer application health

For centralized health monitoring across all consumer accounts, see
[Monitor a native app](/developer-guide/native-apps/monitoring).
