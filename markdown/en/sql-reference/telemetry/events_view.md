# EVENTS\_VIEW view

This view displays rows for telemetry data collected in the [default event table](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-default),
SNOWFLAKE.TELEMETRY.EVENTS.

You can manage access to this view with row access policies. To manage row access policies you create with this view, use the following stored
procedures:

- [ADD\_ROW\_ACCESS\_POLICY\_ON\_EVENTS\_VIEW](/sql-reference/stored-procedures/snowflake_telemetry_add_row_access_policy_on_events_view)
- [DROP\_ROW\_ACCESS\_POLICY\_ON\_EVENTS\_VIEW](/sql-reference/stored-procedures/snowflake_telemetry_drop_row_access_policy_on_events_view)

## Columns

Columns in this view correspond to columns in an event table you create. For more information, see
[Event table columns](/developer-guide/logging-tracing/event-table-columns).

| Column Name | Data Type | Description |
| --- | --- | --- |
| TIMESTAMP | TIMESTAMP\_NTZ | Timestamp when the event record was added. See [TIMESTAMP column](/developer-guide/logging-tracing/event-table-columns#label-event-table-timestamp-column). |
| START\_TIMESTAMP | TIMESTAMP\_NTZ | Event period starting timestamp for metrics and spans. See [START\_TIMESTAMP column](/developer-guide/logging-tracing/event-table-columns#label-event-table-start-timestamp-column). |
| OBSERVED\_TIMESTAMP | TIMESTAMP\_NTZ | A log’s UTC timestamp. Used when capturing logs that do not have an accompanying timestamp. See [OBSERVED\_TIMESTAMP column](/developer-guide/logging-tracing/event-table-columns#label-event-table-observed-timestamp-column). |
| TRACE | OBJECT | Tracing context. See [TRACE column](/developer-guide/logging-tracing/event-table-columns#label-event-table-trace-column). |
| RESOURCE | OBJECT | For future use. See [RESOURCE column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-column). |
| RESOURCE\_ATTRIBUTES | OBJECT | Attributes that identify the source of an event. See [RESOURCE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-resource-attributes-column). |
| SCOPE | OBJECT | Scope for signals. See [SCOPE column](/developer-guide/logging-tracing/event-table-columns#label-event-table-scope-column). |
| SCOPE\_ATTRIBUTES | OBJECT | For future use. See [SCOPE\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-scope-attributes-column). |
| RECORD\_TYPE | VARCHAR | Type of the value in the RECORD field. See [RECORD\_TYPE column](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-type-column). |
| RECORD | OBJECT | Fixed fields for each signal type. See [RECORD column](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-column). |
| RECORD\_ATTRIBUTES | OBJECT | Variable attributes for each signal type. See [RECORD\_ATTRIBUTES column](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-attributes-column). |
| VALUE | VARIANT | Primary event value. See [VALUE column](/developer-guide/logging-tracing/event-table-columns#label-event-table-value-column). |
| EXEMPLARS | ARRAY | Exemplars for metrics. See [EXEMPLARS column](/developer-guide/logging-tracing/event-table-columns#label-event-table-exemplars-column). |

Expand

Show lessSee more
