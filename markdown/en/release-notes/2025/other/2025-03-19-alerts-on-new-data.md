# Mar 19, 2025: Alerts on new data (*Preview*)

You can now use alerts on new data to monitor dynamic table refreshes and task completions.

An [alert on new data](/user-guide/alerts#label-alerts-type-streaming) is executed when new rows are added to a specified table or view.
Snowflake evaluates the condition against the new rows.

You can set up an alert on new data to notify you when new rows for error messages are inserted into the
[event table](/developer-guide/logging-tracing/event-table-setting-up) for your account. Because dynamic table refreshes
and task executions log events to the event table, you can set up an alert on new data to:

- [Monitor dynamic table refreshes](/user-guide/dynamic-tables/monitoring#label-dynamic-tables-streaming-alerts).
- [Monitor task executions](/user-guide/tasks-events).

For more information, see [Alerts on new data](/user-guide/alerts#label-alerts-type-streaming).
