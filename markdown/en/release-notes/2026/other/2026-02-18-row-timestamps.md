# Feb 18, 2026: Row timestamps for pipeline latency and event tracking (*General availability*)

Row timestamps provide a precise, chronological record of when each row in a table was last updated. Rows modified in the
same transaction share the exact same timestamp and rows modified in different transactions are ordered by when they were
committed.

This feature eliminates the need to rely on unpredictable client-side timestamps, empowering data teams to accurately
measure data latency, manage incremental processing without missing out of order events, and establish an audit trail of
changes.

Key use cases include the following:

- **Pipeline observability:** Measure end-to-end latency and data freshness for streaming ingest, CDC, and ETL workloads
  with higher accuracy than client-side timestamps.
- **Reliable incremental processing:** Capture delayed or backfilled records that event timestamps might skip by using
  definitive commit times.
- **Definitive audit trails:** Establish a chronological order of events for regulatory compliance or SCD2-style
  milestoning.

You can enable row timestamps for individual tables, set it as a default at the account/database/schema level, or use a
system function to bulk-enable it for existing tables.

For more information, see [Use row timestamps to measure latency in your pipelines](/user-guide/data-engineering/row-timestamps).
