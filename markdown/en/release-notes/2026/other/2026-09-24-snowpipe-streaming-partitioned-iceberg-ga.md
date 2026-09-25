# Sep 24, 2026: Snowpipe Streaming: Partitioned Apache Iceberg™ tables (*General availability*)

With this release, we’re pleased to announce the general availability of Snowpipe Streaming support for partitioned Snowflake-managed Iceberg tables. You can now ingest data into both partitioned and non-partitioned Snowflake-managed Iceberg tables, including Iceberg v2 and Iceberg v3 tables.

Snowpipe Streaming writes new data by using the table’s current partition specification. Elastic Channels and Named Channels are both supported. Snowpipe Streaming Classic and externally managed Iceberg tables aren’t included in this release.

For more information, see [Snowpipe Streaming with Apache Iceberg™ tables](/user-guide/snowpipe-streaming/snowpipe-streaming-high-performance-iceberg).
