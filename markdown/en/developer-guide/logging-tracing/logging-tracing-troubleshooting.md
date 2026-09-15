# Troubleshooting telemetry data collection

## Logging, metrics, or tracing data is not visible

For example, you might see **No Metrics Data** on the **Related Metrics** panel under **Query History > Query Telemetry**. Or your
event table queries for data return no results. There’s a good chance this is due to telemetry not being fully enabled. To learn more, see
[Enabling telemetry collection](/developer-guide/logging-tracing/logging-tracing-enabling).

To troubleshoot, confirm the following:

- Your account has an active event table and that the table is the one you’re checking for data.

  For more information, see [Event table overview](/developer-guide/logging-tracing/event-table-setting-up).
- The default level for the data you’re looking for (logging, metrics, or tracing) is set to a value that allows data to be recorded.

  For more information, see [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).
- You are setting the levels for logs, traces, and metrics high enough at runtime.

  For example, although you might have set the level for each when you [enabled telemetry collection](/developer-guide/logging-tracing/logging-tracing-enabling),
  you might be overriding those levels for individual objects. For more information on setting and overriding levels, see
  [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).
- You have installed the telemetry package you need for your handler language. These packages should be added to the PACKAGES statement of
  your UDF or stored procedure, or added to your Streamlit with the **Packages** dropdown.

  - For Java and Scala: `com.snowflake.telemetry`
- The type of object from which you want to collect data supports emitting telemetry data. For information about language support for
  types of telemetry data, see the following topics on supported languages:

  - [For logging](/developer-guide/logging-tracing/logging#label-logging-supported-languages)
  - [For metrics](/developer-guide/logging-tracing/metrics#label-metrics-supported-languages)
  - [For tracing](/developer-guide/logging-tracing/tracing#label-tracing-supported-languages)
- The event table has not been truncated.

  For more information, see [TRUNCATE TABLE](/sql-reference/sql/truncate-table).
- You have raw data in the event table.

  - If your queries of the event table return data but you don’t see the data in Snowsight, ensure that you’ve chosen a warehouse
    in Snowsight.
  - **Metrics:** If your queries of the event table return no data, ensure that the duration of the procedure or UDF execution for which you
    want to collect data is longer than the metrics collection interval. Short-running jobs may not emit any metrics data.

    For information about the role time plays in metrics data collection, see [Metrics limitations](/developer-guide/logging-tracing/metrics-limitations).
  - Remember that the data might not yet be in the event table.

    For example, it might take longer due to latency. It can take up to 5 minutes for the metrics data to be available in the event table
    and in Snowsight.

  You can query the event table for raw data as described in the following topics:

  - [Query the event table for log entries](/developer-guide/logging-tracing/logging-accessing-messages#label-logging-viewing-query-event-table)
  - [Query the event table for trace entries](/developer-guide/logging-tracing/tracing-accessing-events#label-tracing-viewing-query-event-table)
