# Aug 28, 2025: Monitoring events for Snowpipe

You can now configure Snowflake to record detailed events, providing valuable insights into the status and progress of your data pipelines
and tables. This new capability helps you monitor your data ingestion processes more effectively.

## Snowpipe: data ingestion events

Snowpipe now records events that provide detailed information about the status of your pipes. These events are captured in the active event
table associated with the pipe. By monitoring these events, you can gain insights into the following areas:

- Pipe status changes: Track the operational state of your Snowpipes.
- File processing progress: Understand the journey of files through the Snowpipe system.
- Periodic, aggregated, ingestion statistics digest: Get summarized statistics on data ingestion.

For more information, see [Monitor events for Snowpipe](/user-guide/data-load-snowpipe-monitor-events).

## Externally managed Apache Iceberg™ tables: automated refresh events

As part of the Snowpipe event monitoring feature, Snowflake now records events that provide information about the status of automated
refresh for externally managed Iceberg tables. These events, which are a component of the new Snowpipe events, can help you gain insights
into automated refresh progress and aggregated statistics. Note that this feature does not support events for manual refreshes.

For more information, see [Monitor automated refresh events](/user-guide/tables-iceberg-auto-refresh#label-tables-iceberg-auto-refresh-events).
