# Test observability for an app

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how providers can validate that observability is set up correctly for a Snowflake Native App before
publishing. It covers cross-account validation against a test consumer, same-account validation in preview, and a
validation checklist to run before each release.

## Cross-account validation

Before publishing a new version of your app, validate end-to-end event collection from a test consumer account
into your event account.

1. **Set up a test consumer account.** Use a dedicated Snowflake account for installation testing. See
   [Install and test an app locally](/developer-guide/native-apps/installing-testing-application).
2. **Configure a test event table** in the test consumer account using
   [CREATE EVENT TABLE](/sql-reference/sql/create-event-table) and
   [ALTER ACCOUNT … SET EVENT\_TABLE](/sql-reference/sql/alter-account).
3. **Enable event sharing** for the installed app following
   [Set up event tracing for an app](/developer-guide/native-apps/ui-consumer-enable-logging).
4. **Emit a known set of events** from the app (for example, a stored procedure that calls `SYSTEM$LOG` at each
   severity level and reports health via `SYSTEM$REPORT_HEALTH_STATUS`).
5. **Validate end-to-end delivery** by querying the provider event account’s event table and confirming that the
   expected records are present with the expected `RECORD_TYPE` and `SCOPE`. Confirm that masked fields are
   hashed and that omitted fields are absent.

If your app ships in multiple regions, repeat this validation in every region you ship to, or use
[Configure centralized event sharing for an app](/developer-guide/native-apps/event-central) to validate against a single consolidated event account.

## Same-account validation (preview)

Same-account event sharing (sharing events from an installed app back to the same account that owns the
application package) is currently in preview. It lets providers validate event sharing during local development
without provisioning a separate consumer account.

When same-account event sharing is enabled, the same field categorization and SHA-1 masking apply: events leave
the application’s logical boundary and are written into the event account just as they would be from a real
consumer.

For the current preview limitations, see
[Install and test an app locally](/developer-guide/native-apps/installing-testing-application). Notable limitations include: same-account event
sharing is intended for development and validation, not production telemetry collection, and certain enterprise
features (such as cross-region routing) are not yet available in this mode.

## Validation checklist

Run through this checklist before publishing a new version, patch, or change to event definitions:

- **Event collection working:** the app emits the expected log, trace, and metric records to the consumer event
  table, and the records arrive in the provider event account when sharing is enabled.
- **Privacy masks applied correctly:** `snow.database.hash` and `snow.query.hash` are populated; the omitted
  fields listed in [Set up and manage an event table in the provider account](/developer-guide/native-apps/event-manage-provider) are absent. For apps with SPCS
  containers, also confirm that compute pool name/ID, service UUID, and other SPCS environment fields are
  omitted per the categorization in [Set up and manage an event table in the provider account](/developer-guide/native-apps/event-manage-provider).
- **Regional setup functioning:** the provider has an active event table in every region where the app is
  installed, or [centralized event sharing](/developer-guide/native-apps/event-central) is configured.
- **Cost monitoring in place:** the
  [EVENT\_USAGE\_HISTORY view](/sql-reference/account-usage/event_usage_history) and the
  [APPLICATION\_DAILY\_USAGE\_HISTORY view](/sql-reference/account-usage/application_daily_usage_history) are
  queryable and a baseline daily volume has been recorded.
- **Health reporting working:** `SYSTEM$REPORT_HEALTH_STATUS` returns `true` for the test instance and the
  status appears in
  [APPLICATION\_STATE](/sql-reference/data-sharing-usage/application-state-view) within the 55-minute report
  window.
- **Lifecycle events emitted:** with `LOG_EVENT_LEVEL` set to `INFO` (or stricter), upgrade and health events
  show up in the event table with `SCOPE.name = 'snow.application.lifecycle'`.

For a deeper end-to-end monitoring workflow once the app is in production, see
[Monitor a native app](/developer-guide/native-apps/monitoring).
