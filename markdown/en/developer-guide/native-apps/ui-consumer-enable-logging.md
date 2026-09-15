# Set up event tracing for an app

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how to use event tracing to capture the log messages and trace events
emitted by an app. It also describes how to enable event sharing to share log messages and trace events
with providers.

## About event tracing in the Snowflake Native App Framework

Event tracing allows an app to emit information related to its performance and behavior. The Snowflake Native App Framework
supports using the Snowflake
[logging and tracing](/developer-guide/logging-tracing/logging-tracing-overview).
functionality to gather this information. An app can emit the following:

- Log messages that are independent, detailed messages with information about the state of a specific
  feature within the app.
- Trace events with structured data you can use to get information spanning and grouping multiple
  parts of an app.
- Metrics data that includes the CPU and memory metrics that Snowflake generates.

### View the log messages, trace events, and metrics for an app

To view the log messages and trace events emitted by the app, consumers must set up an event table in
their account to collect this information. See
[Set up an event table](#label-nativeapps-consumer-logging-setting-up) for more information.

## About event sharing

Consumers can also enable event sharing to share event data with providers. When a provider enables
event sharing, the log messages and trace events that are inserted into the event table in
the consumer account are also inserted into an event table in provider account.

Event sharing allows the provider to collect information about the app’s performance and behavior. See
[About event sharing for an app](#label-nativeapps-consumer-logging-enabling) for more information.

### About event definitions

Event definitions specify how an app shares log messages and trace events with the provider.
Event definitions act as filters on the log message and trace event levels set by the provider.
A provider specifies the event definitions for an app when a new version or patch is published.

Note

Event definitions are not required. If a provider does not specify event definitions for an app
consumers can enable or disable event sharing as required.

Providers can set an event definition to be required or optional:

- Required event definitions are enabled automatically when the app is installed. To collect the
  event definitions emitted by an app, a consumer should create an event table and set it as
  the active event table for their account.
- Optional event definitions can be enabled or disabled by the consumer as necessary. Optional event
  definitions require an active event table, but they are not required to install or use the app.

Caution

Event definitions are not the same as the log and tracing levels set by the provider. The log and
tracing levels determine the information that is inserted into the consumer event table.

Event definitions are filters that act on the log messages and trace events. They determine what
information is inserted in the provider event table when event sharing is enabled.

### Supported event definitions

The following table lists the event definitions that are currently supported:

> | Type | Name | Description | Filter |
> | --- | --- | --- | --- |
> | **All** | SNOWFLAKE$ALL | Shares all log messages and trace events that the app emits. | `*` |
> | **Events** | SNOWFLAKE$ALL\_EVENTS | Shares all events from the application. | `RECORD_TYPE='EVENT'` |
> | **Errors and warnings** | SNOWFLAKE$ERRORS\_AND\_WARNINGS | Shares logs related to errors, warnings, and fatal events. | `RECORD_TYPE = ‘LOG’ AND RECORD:severity_text in (‘FATAL’, ‘ERROR’, ‘WARN’)` |
> | **Metrics** | SNOWFLAKE$METRICS | Shares the CPU and memory metrics that Snowflake generates. | `RECORD_TYPE = in ('METRIC')` |
> | **Traces** | SNOWFLAKE$TRACES | Shares detailed traces of user activities and journeys in the application. | `RECORD_TYPE in (‘SPAN’, ‘SPAN_EVENT’)` |
> | **Usage logs** | SNOWFLAKE$USAGE\_LOGS | Shares high-level logs related to user actions and app events. | `RECORD_TYPE = LOG AND RECORD:severity_text = ‘INFO’` |
> | **Debug logs** | SNOWFLAKE$DEBUG\_LOGS | Shares technical logs used to troubleshoot the app. | `RECORD_TYPE = ‘LOG’ AND RECORD:severity_text in (‘DEBUG’, ‘TRACE’)` |
>
> Expand
>
> Show lessSee more

Note

If a provider does not configure the app to use event definitions, Snowsight displays only the
**All** type.

### Considerations for consumers when using event definitions

Consumers can continue to use the existing SHARE\_EVENTS\_WITH\_PROVIDER property, however there
are limitations:

- If an app only uses the OPTIONAL ALL event definition, setting the SHARE\_EVENTS\_WITH\_PROVIDER property
  to `true` enables event sharing and setting it to `false` disables event sharing.

  This is applicable when a provider explicitly adds the OPTIONAL ALL event definition to the manifest
  file or an app was migrated from the existing event sharing functionality.
- If a provider adds mandatory and optional event definitions to the manifest file, setting the
  SHARE\_EVENTS\_WITH\_PROVIDER property to `true` enables all event definitions. In contrast, the
  SHARE\_EVENTS\_WITH\_PROVIDER property can only be set to `false` if the provider adds only
  optional event definitions.

  SHARE\_EVENTS\_WITH\_PROVIDER is TRUE only when all event definitions are enabled, otherwise it is FALSE.

## Workflow to set up event tracing for an app

The following workflow describes how to set up event tracing for an app:

1. [Review the considerations for using logging and event tracing](#label-nativeapps-consumer-logging-considerations).
2. [Set up an event table](#label-nativeapps-consumer-logging-setting-up).
3. [View the logging and trace event levels configured for the app](#label-nativeapps-consumer-logging-view-log-level).
4. [View the events in the event table](#label-nativeapps-consumer-logging-view-events).
5. [Enable event sharing on an app](#label-nativeapps-consumer-logging-enabling).

## Considerations when using event tracing

Before setting up event tracing for an app, you must consider the following:

- This feature requires you to [set up an event table](#label-nativeapps-consumer-logging-setting-up) in
  your account.
- After you [enable event sharing](#label-nativeapps-consumer-logging-enabling), a masked and redacted
  copy of the trace events and log messages is automatically inserted in the event table of the designated
  provider account.
- Snowflake does not charge you to enable event sharing. However, you are responsible for the
  cost of ingesting trace events and log messages in the event table as well as storage
  costs for the event table.
- After enabling event sharing with a provider, you cannot revoke access to shared
  trace events and log messages.
- You cannot share historical events using event sharing.
- Snowflake sends the shared events to a designated provider account within the same region as your account.
  This feature does not share data across different regions.
- You cannot change the logging or tracing levels for an app. The app provider sets these levels
  when publishing the app.
- Snowflake recommends reviewing the trace events and log messages in the event table before enabling
  event sharing.
- Snowflake recommends disabling event sharing if you do not need to troubleshoot the app.

## Set up an event table

To collect the log messages and trace events emitted by the app, consumers must create an event table to
store the information.

Note

If a provider includes required event definitions in the app, they are enabled by default during
installation. However, if the consumer does not have an active event table, the log messages and
trace events emitted by the app are discarded.

An account can have multiple event tables, but only one of them can be set as the active event table in a
Snowflake account at a time. Without an active event table, log messages and trace events that the app emits
are not captured. This is true even if the functions and procedures in an app call the logging and trace
event APIs directly.

To create an event table, run the [CREATE EVENT TABLE](/sql-reference/sql/create-event-table) command as shown in the following example:

Copy code

```
CREATE EVENT TABLE event_db.event_schema.my_event_table;
```

Note that this command specifies the database and schema that contain the event table.

After creating the event table, use the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command to
specify that the event table is the active table for the account:

Copy code

```
ALTER ACCOUNT SET EVENT_TABLE=event_db.event_schema.my_event_table;
```

## Enable event sharing for an app

The Snowflake Native App Framework supports sharing log messages and trace events stored in the consumer event table with the
app provider. To share logs and event information with a provider, the consumer must enable event
sharing for an app.

### Prerequisites for enabling event sharing for an app

The following prerequisites must be met to enable event sharing for an app instance:

- Use a role with the MANAGE EVENT SHARING global privilege. The ACCOUNTADMIN role has this privilege by
  default and can grant it to other roles.
- [Set up an event table in the consumer account](#label-nativeapps-consumer-logging-setting-up).

### Enable event sharing using Snowsight

Note

If the provider includes required
[event definitions](#label-nativeapps-consumer-logging-available-events)
in the app, event sharing and the required event definitions are enabled during installation and
cannot be disabled later.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select the app.
4. Select the **Settings** icon in the toolbar.
5. Select the **Events and logs** tab.
6. Under the **Events and logs sharing** area, move the slider for the events you want to capture.
7. If the provider has defined event definitions for the app:

   1. Use the slider to enable optional event definitions. By default, all event types are enabled.
   2. Select **Save**.
8. If no event table is currently selected, select the event table from the list
   under **Event table location**.

   Caution

   Use caution when changing the event table in Snowsight. Each Snowflake account
   uses a single event table for all events generated within the account. Changing the event
   table causes all events generated in the account to be stored in the new location.

### Enable event sharing by using SQL

1. Use the
   [SHOW TELEMETRY EVENT DEFINITIONS](/sql-reference/sql/show-telemetry-event-definitions)
   command to determine the event definitions for the app:

   Copy code

   ```
   SHOW TELEMETRY EVENT DEFINITIONS IN APPLICATION hello_snowflake;
   ```

   If the provider did not configure the app to use event definitions, the `type` column
   displays `ALL`. Otherwise, this command lists the optional event definitions specified
   for the app.
2. If the app contains required event definitions, use the
   [ALTER APPLICATION](/sql-reference/sql/alter-application) command to
   enable them:

   Copy code

   ```
   ALTER APPLICATION hello_snowflake SET AUTHORIZE_TELEMETRY_EVENT_SHARING=true
   ```

   This command enables all of the required event definitions, but does not enable optional event
   definitions.

   Note

   After enabling the required event definitions for an app, event sharing cannot be disabled.
3. If the app contains optional event definitions, use the
   [ALTER APPLICATION](/sql-reference/sql/alter-application)
   to enable them as shown in the following example:

   Copy code

   ```
   ALTER APPLICATION hello_snowflake SET SHARED TELEMETRY EVENTS ('SNOWFLAKE$TRACES', 'SNOWFLAKE$DEBUG_LOGS');
   ```

   This example enables the `SNOWFLAKE$TRACES` and `SNOWFLAKE$DEBUG_LOGS` based on the output of the
   [SHOW TELEMETRY EVENT DEFINITIONS](/sql-reference/sql/show-telemetry-event-definitions)
   command.
4. To verify that event tracing and logging is enabled, use the [DESCRIBE APPLICATION](/sql-reference/sql/desc-application)
   command:

   Copy code

   ```
   DESC APPLICATION hello_snowflake;
   ```

   The `authorize_telemetry_event_sharing` and `share_events_with_provider` rows of the output
   indicate if event sharing is enabled.

### Enable event sharing using SQL (deprecated functionality)

Caution

The method of enabling event sharing using SQL described in this section will be deprecated
in a future release. Snowflake recommends using the method described in
[Enable log and event sharing using SQL](#label-nativeapps-consumer-logging-enabling-sql)
to enable event sharing using SQL.

To enable event sharing for an app, run the
[ALTER APPLICATION](/sql-reference/sql/alter-application) command to set
SHARE\_EVENTS\_WITH\_PROVIDER to `TRUE`. For example:

Copy code

```
ALTER APPLICATION HelloSnowflake SET SHARE_EVENTS_WITH_PROVIDER = TRUE;
```

To show the event sharing status for an app, use the [DESCRIBE APPLICATION](/sql-reference/sql/desc-application) command as shown in the following example:

Copy code

```
DESC APPLICATION HelloSnowflake;
```

`SHARE_EVENTS_WITH_PROVIDER` shows the status of event sharing for the app.

## Enable event definitions during upgrades

During upgrades, event definitions behave as follows:

> | Change to event definition | Behavior during upgrade |
> | --- | --- |
> | No change to an event definition | The event definition retains the same status as the previous version or patch. |
> | A new event definition | Not enabled automatically. This is true for both required and optional event definitions. The consumer must manually enable new event definitions. |
> | Changes from required to optional or optional to required | The event definition retains the same status as the previous version or patch. |
> | Deleted event definition | Event sharing stops after upgrade for log messages or trace events filter in the previous version or patch. |
>
> Expand
>
> Show lessSee more

During upgrade, consumers are prompted to review the changes to event definitions from the previous patch or
version.

## View the log messages and trace events in the event table

When an event table is enabled, consumers can query the event table to see the log messages and
trace events emitted by the app.

### View the event log messages and trace events by using Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps**.
3. Select the app.
4. In the toolbar, select **Settings**.
5. Select the **App events** tab.
6. In the **Event logging** section, select **View logs**.

This opens a new worksheet with a pre-populated
[SELECT](/sql-reference/sql/select) statement that displays the log messages
and trace events for the app.

### View the event log messages and trace events by using SQL

Use the [SELECT](/sql-reference/sql/select) command to query the
event log messages and trace events, as shown in the following example:

Copy code

```
SELECT
  TIMESTAMP as time,
  RESOURCE_ATTRIBUTES['snow.executable.name'] as executable,
  RECORD['severity_text'] as severity,
  VALUE as message
FROM
  "EVENT_LOG"."PUBLIC"."CONSUMER_EVENT_TABLE"
WHERE RESOURCE_ATTRIBUTES['snow.application.name'] = 'YOUR_APP_NAME'
```

This command returns all of the log messages and trace events stored in the event table `CONSUMER_EVENT_TABLE`
for an app named `YOUR_APP_NAME`.

### Determine if a log message or trace event is shared with the provider

The RECORD\_ATTRIBUTES column contains the `snow.application.shared` field. If the value of
this field is TRUE, the log message or trace event is shared with the provider. Otherwise,
the log message or event is not shared.

## View the log and trace levels for an app

The log and trace levels of an app are defined by the provider before publishing an app.
Consumers cannot change the log and trace levels for an app.

However, before setting up event tracing or enabling event sharing for an app, Snowflake
recommends verifying the log level to understand the type of information that collected
and shared with the provider.

To view the log and trace level of an app, run the following command:

Copy code

```
DESC APPLICATION HelloSnowflake;
```

This command displays information about the `HelloSnowflake` app, including the following information
about the log and trace level set for the app:

- log\_level: The log level set by the provider.
- trace\_level: The trace level set by the provider.
- metric\_level: The metric data level set by the provider.
- log\_event\_level: The log event level set by the provider.
- effective\_log\_level: The log level set for the app.
- effective\_trace\_level: The trace level enabled for the app.

The effective log and trace levels are determined by the event definitions the consumer enables for the app.

For example, if the provider defines the log level as OFF, but consumer enables the ERROR\_AND\_WARNING event
definition, the app dynamically changes log level to WARN so that ERROR\_AND\_WARNING events can be collected. The app
emits events that are less or equally as verbose as WARN and shares those error and warning events with the provider.
The value of `log_level` would be OFF and the value of `effective_log_level` would be WARN.

In contrast, if the provider defines the log level as TRACE, but the consumer enables the ERROR\_AND\_WARNING
event definition, the app emits events that are less or equally as verbose as trace, but only error and warning
messages are shared with the provider. The value of both log\_level and effective\_log\_level would be TRACE.

## Privacy and masking

Telemetry is filtered and transformed before it leaves your account. Fields fall into three categories:

- Shared: general app and organizational context essential for support (for example,
  `APPLICATION_PROVIDER_ORG`, `LISTING_NAME`).
- Masked: sensitive identifiers hashed so providers can correlate events without seeing raw values (for example,
  `snow.database.hash`, `snow.query.hash`, `snow.application.hash`). Application name and application
  instance name are not shared in clear text; they are hashed.
- Omitted: fields that never leave the consumer account (for example, `snow.user.name`, `snow.warehouse.name`,
  `snow.session.id`).

Hashing today uses SHA-1, exposed via
[SYSTEM$GET\_HASH\_FOR\_APPLICATION](/sql-reference/functions/system_get_hash_for_application) so consumers
can derive the same hash for support interactions.

For the authoritative categorized list of shared, masked, and omitted fields (including SPCS identifiers), see
the field categorization table in
[Set up and manage an event table in the provider account](/developer-guide/native-apps/event-manage-provider).

## Cost ownership

As a consumer, you own the cost of your event table:

- You pay for event storage in your account; you do not pay for sharing telemetry to the provider’s event account.
- You cannot revoke events that have already been shared. To stop sharing future events, disable event sharing
  for the application.
- Historical events are not backfilled when sharing is enabled.
- Events only share within the same region. Cross-region centralization is the provider’s responsibility.

To control your event-table cost, scope event sharing to the event definitions you actually need (for example,
`ERRORS_AND_WARNINGS` and `METRICS` may be sufficient for most apps; reserve `DEBUG_LOGS` and `TRACES`
for active troubleshooting).
