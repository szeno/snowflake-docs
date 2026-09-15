# Configure event definitions for an app

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to define event definitions in the manifest file of an app. Event definitions
define which log messages and trace events are shared with a provider.

## About event definitions

Event definitions specify how an app shares log messages and trace events with the provider.
Event definitions act as filters on the log message and trace event levels set by the provider.
A provider specifies the event definitions for an app when a new app version or patch is published.

Event definitions are filters that act on the log messages and trace events. They determine what
information is inserted in the provider event table when event sharing is enabled.

Event definitions are optional. If a provider does not specify event definitions for an app,
consumers can only enable or disable event sharing for all events when the provider enables event tracing.

Caution

Event definitions differ from the log and tracing levels set by the provider. Log and
tracing levels determine the information that is inserted into the consumer event table. If neither
the log nor tracing levels are set, then the app does not emit any events.

The log and trace levels for an app can change based on the event definitions enabled by the consumer.
Snowflake uses the most verbose log and trace levels allowed by the event definitions
the consumer has enabled.

## Mandatory and optional event definitions

Providers can set an event definition to be required or optional:

- Required event definitions are enabled automatically when the app is installed.

  After installing an app with required event definitions, consumers cannot disable event sharing or
  the required event definitions. When an app is being upgraded, providers can use system functions or
  the Python Permission SDK to check if the consumer has enabled all required event definitions.
- Optional event definitions can be enabled or disabled by the consumer as necessary.

## Supported event definitions

The following table lists currently supported event definitions.

| Type | Name | Description | Filter |
| --- | --- | --- | --- |
| **All** | SNOWFLAKE$ALL | Shares all log messages and trace events that the app emits. | `*` |
| **Events** | SNOWFLAKE$ALL\_EVENTS | Shares all events from the application. | `RECORD_TYPE='EVENT'` |
| **Errors and warnings** | SNOWFLAKE$ERRORS\_AND\_WARNINGS | Shares logs related to errors, warnings, and fatal events. | `RECORD_TYPE = ‘LOG’ AND RECORD:severity_text in (‘FATAL’, ‘ERROR’, ‘WARN’)` |
| **Traces** | SNOWFLAKE$TRACES | Shares detailed traces of user activities and journeys in the application. | `RECORD_TYPE in (‘SPAN’, ‘SPAN_EVENT’)` |
| **Usage logs** | SNOWFLAKE$USAGE\_LOGS | Shares high-level logs related to user actions and app events. | `RECORD_TYPE = LOG AND RECORD:severity_text = ‘INFO’` |
| **Debug logs** | SNOWFLAKE$DEBUG\_LOGS | Shares technical logs used to troubleshoot the app. | `RECORD_TYPE = ‘LOG’ AND RECORD:severity_text in (‘DEBUG’, ‘TRACE’)` |
| **Metrics** | SNOWFLAKE$METRICS | Enable consumers to share metrics with providers. | `RECORD_TYPE in (‘METRIC’)` |

Expand

Show lessSee more

Note

Snowsight only displays the all event **All** type to the consumer if the provider has not configured the app to
use event definitions.

## Limitations of event definitions in apps with containers

Snowflake Native Apps with Snowpark Container Services currently only support the `SNOWFLAKE$ALL` event definition. Granular event definitions for
containerized apps will be added in a future release. Container telemetry levels are configured in the
service specification rather than the manifest file. The manifest `log_level` does not propagate into containers.

## Set the log and trace levels for an app

To allow an app to use event tracing, a provider must configure the log and trace levels
in the manifest file.

To set the log and trace levels for an app, add a `configuration` block in the manifest file as shown in the following example:

Copy code

```
configuration:
  ...
  log_level: INFO
  trace_level: ALWAYS
  metric_level: ALL
  log_event_level: INFO
  ...
```

This example sets the log and trace levels for the app as follows:

- The `log_level` property is set to `INFO`.
- The `trace_level` property is set to `ALWAYS`.
- The `metric_level` property is set to `ALL`.
- The `log_event_level` property is set to `INFO`.

See [LOG\_LEVEL](/sql-reference/parameters#label-log-level), [TRACE\_LEVEL](/sql-reference/parameters#label-trace-level), [METRIC\_LEVEL](/sql-reference/parameters#label-metric-level), and
[LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) for information on the valid values for these parameters.

[LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) was introduced in
[BCR bundle 2026\_02](/release-notes/bcr-bundles/2026_02/bcr-2232) and controls which application lifecycle
events (RECORD\_TYPE=EVENT) are recorded, separately from log messages controlled by `log_level`. Supported
severity values are `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`, and `OFF`.

Caution

After you publish an app, the log and trace levels cannot be changed. If the log and trace levels
are not set in the manifest file, the app does not emit any information.

When the log and trace levels are set for an app, consumers must set up an event table in their account
to see the log messages and trace events that the app emits.

To allow the provider to see the log messages and trace events that an app generates, consumers must
enable event sharing. See [Enable event sharing for an app](/developer-guide/native-apps/event-about#label-nativeapps-provider-event-enable)
for more information.

## Add an event definition to the manifest file

To specify an event definition, a provider adds an entry to the
`configuration.telemetry_event_definitions` block of the manifest file as shown in the
following example:

Copy code

```
configuration:
  telemetry_event_definitions:
    - type: ERRORS_AND_WARNINGS
      sharing: MANDATORY
    - type: DEBUG_LOGS
      sharing: OPTIONAL
```

This example specifies the following event definitions:

- A required event definition with type `ERRORS_AND_WARNINGS`.
- An optional event definition with type `DEBUG_LOGS`.

See [Supported event definitions](#label-nativeapps-provider-logging-available-events) for more information.

After a consumer installs an app, the event definitions appears in the **Events and logs** tab on the
**Security** page of the app. See
[Enable logging and event sharing for an app](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging)
for more information.

## Set the log, trace, and metric levels for specific objects

Providers may fine-tune the log, trace, and metric levels for specific objects within an app. This
gives providers more control over the telemetry data emitted by the app.

Providers can set the log, trace, and metric levels for the following objects within an app:

- Schemas
- Versioned schemas
- Stored procedures
- User-defined functions

The following table lists the SQL commands used to set the log, trace, and event levels for
these objects:

| Object | Command |
| --- | --- |
| Schemas | [ALTER SCHEMA](/sql-reference/sql/alter-schema) |
| Versioned schema | [CREATE OR ALTER VERSIONED SCHEMA](/sql-reference/sql/create-versioned-schema) |
| Stored procedures | [ALTER PROCEDURE](/sql-reference/sql/alter-procedure) |
| User-defined functions | [ALTER FUNCTION](/sql-reference/sql/alter-function) |

Expand

Show lessSee more

For schemas, stored procedures, and user-defined functions, providers can use the `SET` clause
of the ALTER commands to set the following properties:

- LOG\_LEVEL
- TRACE\_LEVEL
- METRIC\_LEVEL

For versioned schemas providers can set these properties using
[CREATE OR ALTER VERSIONED SCHEMA](/sql-reference/sql/create-versioned-schema) in the setup script.

## Order of precedence for log, trace, and metric levels

Within an app, the log, trace, and metric levels can be configured in different ways
for components of the app. To determine the events that are emitted, the Snowflake Native App Framework uses the
following order of precedence:

- Stored procedures and user-defined functions

  If an override is set for the specific stored procedure or user-defined function,
  it takes precedence.
- Schemas and version schemas

  If no overrides are set for stored procedures or user-defined functions, overrides
  for schemas and versioned schemas take precedence.
- App-level settings

  If no object-level overrides are found, the app-level telemetry configuration, typically defined
  in the manifest file, is used.
