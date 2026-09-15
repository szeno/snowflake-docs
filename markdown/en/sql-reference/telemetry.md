# TELEMETRY schema

In the SNOWFLAKE database, the TELEMETRY schema contains tables, views, and stored procedures to support collecting telemetry data.

## TELEMETRY tables

The SNOWFLAKE.TELEMETRY.EVENTS table is the [default event table](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default) for telemetry data collection.
If you haven’t [set up an event table](/developer-guide/logging-tracing/event-table-setting-up), Snowflake uses the EVENTS table by
default to collect telemetry data.

For reference information about columns in SNOWFLAKE.TELEMETRY.EVENTS, see [Event table columns](/developer-guide/logging-tracing/event-table-columns).

For more about telemetry in Snowflake, see [Logging, tracing, and metrics](/developer-guide/logging-tracing/logging-tracing-overview).

| View | Notes |
| --- | --- |
| EVENTS | Displays rows for log messages, trace events, and metrics measurements collected in the default event table. |

Expand

Show lessSee more

## TELEMETRY views

The TELEMETRY schema provides the following view on the default event table, SNOWFLAKE.TELEMETRY.EVENTS.

| View | Notes |
| --- | --- |
| [EVENTS\_VIEW](/sql-reference/telemetry/events_view) | Displays a row for log messages, trace events, and metrics measurements collected in the default event table. |

Expand

Show lessSee more

### Accessing views in the TELEMETRY schema

The EVENTS\_VIEWER or EVENTS\_ADMIN roles can execute SELECT operations on the EVENTS\_VIEW view. For more information, see
[Roles for access to the default event table and EVENTS\_VIEW](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default-roles).

### General usage notes

- The Snowflake-specific views are subject to change. Avoid selecting all columns from these views. Instead, select the columns that you want.
  For example, if you want the `name` column, use `SELECT name`, rather than `SELECT *`.
- The rows returned in a query of a view depend on the privileges granted to the user’s current role. When you query a view in
  the EVENTS\_VIEW view, only objects for which the current role has been granted access privileges are returned.

## TELEMETRY stored procedures

The TELEMETRY schema provides the following stored procedures you can use to manage access to rows selected from the EVENTS\_VIEW view.

| View | Notes |
| --- | --- |
| [ADD\_ROW\_ACCESS\_POLICY\_ON\_EVENTS\_VIEW(VARCHAR, ARRAY)](/sql-reference/stored-procedures/snowflake_telemetry_add_row_access_policy_on_events_view) | Binds a row access policy to the [EVENTS\_VIEW](/sql-reference/telemetry/events_view) by specifying an array of the table’s columns. |
| [DROP\_ROW\_ACCESS\_POLICY\_ON\_EVENTS\_VIEW(VARCHAR)](/sql-reference/stored-procedures/snowflake_telemetry_drop_row_access_policy_on_events_view) | Deletes the specified row access policy bound to the [EVENTS\_VIEW](/sql-reference/telemetry/events_view). |

Expand

Show lessSee more
