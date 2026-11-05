# Oct 28, 2026: Openflow legacy runtime metrics deprecated

The following Openflow runtime telemetry is deprecated and will be removed in a future release. A removal date
isn’t planned yet, and removal won’t happen in the near future:

- **Legacy runtime metrics in the event table**: connection, process group, and processor metrics that Openflow
  writes to the event table. For the list of these metrics, see [Runtime metrics: Event table (deprecated)](/user-guide/data-integration/openflow/monitor-legacy-event-table).
- **OpenTelemetryReportingTask**: the reporting task that exports legacy runtime metrics to an OpenTelemetry
  endpoint. For details, see [Runtime metrics: Export (deprecated)](/user-guide/data-integration/openflow/monitor-legacy-export).

Don’t use the deprecated telemetry for new monitoring, and move existing monitoring to the new metrics. For
details, see [Openflow telemetry](/user-guide/data-integration/openflow/monitor).
