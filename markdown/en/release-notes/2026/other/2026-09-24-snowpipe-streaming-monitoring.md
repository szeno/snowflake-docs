# Sep 24, 2026: Snowpipe Streaming: Event table monitoring

You can now monitor Snowpipe Streaming ingestion with event tables to check that data is arriving, identify processing delays, and investigate failures across your pipelines. Query ingestion events with SQL to track row counts, server-side latency, row and channel errors, and channel activity. Use these records to build dashboards and configure alerts.

Snowflake provides a default event table, so you don’t need to create one. To collect monitoring events, set `LOG_EVENT_LEVEL` to `INFO` on the schema containing your target tables, unless an inherited setting already enables collection. Your role must have access to query the active event table or its view.

For setup instructions, query examples, and complementary SDK client monitoring with Prometheus and logs, see [Monitor Snowpipe Streaming](/user-guide/snowpipe-streaming/snowpipe-streaming-event-table-telemetry).
