# Logging and tracing limitations

## General limitations

There is a 1MB limit for log and trace event payloads. If the payload is over the 1MB threshold, the record in the event table will be
incomplete and only contain values for the following columns: TIMESTAMP, RECORD\_TYPE, and RESOURCE\_ATTRIBUTES. Currently there is no
additional indication that the threshold was exceeded.

## Event tables associated with databases

- When you use [event tables associated with databases](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-object), the Snowsight trace explorer
  currently won’t show the entire span for traces with spans across multiple event tables. Instead, you can see the partial trace with
  the spans in the currently selected event table from the drop-down.
- Snowflake does not support collecting events for Snowpark Container Services when the event table is associated with a database.
