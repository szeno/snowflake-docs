# Jul 16, 2025: Data governance release notes

## Automatic tag propagation: Event table to monitor conflicts (*General availability*)

Use an event table to collect telemetry data related to automatic tag propagation, especially data related to conflicts encountered during
propagation and how they were resolved. After Snowflake starts collecting data in the event table, you can query the table, create a stream
to track changes, or set alerts to send notifications when certain events occur.

For more information, see [Using an event table to monitor tag propagation](/user-guide/object-tagging/propagation#label-tag-propagation-event-table).
