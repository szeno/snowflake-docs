# Use row timestamps to measure latency in your pipelines

Row timestamps provide a precise, chronological record of when each row in a table was last updated. Rows modified in the
same transaction share the exact same timestamp and rows modified in different transactions are ordered by when they were
committed.

Key use cases include the following:

- **Pipeline observability:** Measure end-to-end latency and data freshness for streaming ingest, CDC, and ETL workloads
  with higher accuracy than client-side timestamps.
- **Reliable incremental processing:** Capture delayed or backfilled records that event timestamps might skip by using
  definitive commit times.
- **Definitive audit trails:** Establish a chronological order of events for regulatory compliance or SCD2-style
  milestoning.

To set row timestamps on your tables, choose one of the following options:

- **Set row timestamps on a table or dynamic table:** Using a role that has the OWNERSHIP privilege on the table, set the ROW\_TIMESTAMP
  property to TRUE when executing the [CREATE TABLE](/sql-reference/sql/create-table), [ALTER TABLE](/sql-reference/sql/alter-table),
  [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table), or [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table) command.

  For example, `CREATE TABLE … ROW_TIMESTAMP = TRUE`, `ALTER TABLE … SET ROW_TIMESTAMP = TRUE`, or
  `ALTER DYNAMIC TABLE … SET ROW_TIMESTAMP = TRUE`.
- **Set row timestamps by default for new tables in a container:** Set the ROW\_TIMESTAMP\_DEFAULT property to TRUE on the container.

  For example, `ALTER SCHEMA … SET ROW_TIMESTAMP_DEFAULT = TRUE` means that every new table created in the schema after setting the
  parameter will have row timestamps on by default.
- **Bulk enable row timestamps on existing tables:** Use the system function SELECT SYSTEM$SET\_ROW\_TIMESTAMP\_ON\_ALL\_SUPPORTED\_TABLES.

  For example, `SELECT SYSTEM$SET_ROW_TIMESTAMP_ON_ALL_SUPPORTED_TABLES('schema', '{my_db}.my_schema')`.

  - The first argument is level: one of `schema`, `database`, or `account`.
  - The second argument is the fully qualified name of the container.

  This function adds the row timestamp column to all existing eligible tables within the container and ensures newly created tables automatically
  have row timestamp enabled.

  To successfully execute the function, you need MODIFY privileges on the container you’re invoking the function on.

After row timestamps are enabled, tables expose the METADATA$ROW\_LAST\_COMMIT\_TIME column, which returns the timestamp when each row was last
modified. This enables change tracking, incremental processing, and time-travel queries based on row modification time.

Note

In a data sharing scenario, consumers can’t select METADATA$ROW\_LAST\_COMMIT\_TIME even if the producer table has row timestamp enabled. Producers
must create a view that selects METADATA$ROW\_LAST\_COMMIT\_TIME and then share the view if they want to share row timestamps with consumers.

The following statements demonstrate how to create a table that supports row timestamps. The statements insert data into the table and retrieve
the timestamp of each row.

Copy code

```
CREATE OR REPLACE TABLE table1(value1 STRING)
  ROW_TIMESTAMP = TRUE;

INSERT INTO table1 VALUES('some-value-a');

INSERT INTO table1 VALUES('some-value-b');

SELECT METADATA$ROW_LAST_COMMIT_TIME AS row_timestamp, *
  FROM table1
  ORDER BY 1;
```

## Primary use cases

The METADATA$ROW\_LAST\_COMMIT\_TIME metadata column helps track latency. For example, if you aim for a five-second total latency, this column
helps you determine Snowflake’s contribution to that latency.

Key use cases include:

- **Measuring ingestion latency**: Track the time between when a row is created on the client and when it becomes visible in Snowflake,
  allowing users to calculate data ingestion time.
- **Measuring end-to-end latency**: Combine ingestion latency and pipeline latency to measure the total time from data generation to its
  final state.
- **Measuring pipeline latency**: Tracks timestamps as data moves through a pipeline. By comparing the timestamp of the initial table to the
  final table, users can measure how long the pipeline takes to process data.
  - Supported for pipelines based on streams, dynamic tables, and tasks.

### Example: measure ingestion latency

To measure ingestion latency using the METADATA$ROW\_LAST\_COMMIT\_TIME metadata column, do the following:

1. Create an ingestion pipeline that sends data to Snowflake using one of the following methods:

   - [Snowpipe Streaming Ingest SDK](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview). For a simple example that shows how the client
     SDK could be used to build a Snowpipe Streaming application, see
     [this Java file](https://github.com/snowflakedb/snowflake-ingest-java/blob/master/src/main/java/net/snowflake/ingest/streaming/example/SnowflakeStreamingIngestExample.java) (GitHub).
   - [Snowpipe](/user-guide/data-load-snowpipe-intro)
   - [COPY INTO <table>](/sql-reference/sql/copy-into-table) command
2. Execute the following:

   Copy code

   ```
   ALTER SESSION SET TIMESTAMP_TZ_OUTPUT_FORMAT = 'YYYY-MM-DDTHH:MI:SS.FF3 TZH';

   ALTER SESSION SET TIMEZONE = 'UTC';

   CREATE OR REPLACE DATABASE mydb;

   CREATE OR ALTER SCHEMA myschema;

   CREATE OR REPLACE TABLE table1(record_id STRING, client_timestamp TIMESTAMP_LTZ);

   -- The rows inserted from server-side-insert-1 up to this point will not have a valid METADATA$ROW_LAST_COMMIT_TIME timestamp.
   INSERT INTO table1 VALUES('server-side-insert-1', current_timestamp());
   ```
3. Modify the table to enable the METADATA$ROW\_LAST\_COMMIT\_TIME feature.

   Copy code

   ```
   ALTER TABLE table1 SET ROW_TIMESTAMP = TRUE;
   ```
4. Ingest data that includes the `record_id` and `client_timestamp` columns to your Snowflake table using the ingestion pipeline defined in Step 1.
5. Insert a new row as an immediate example if not using an ingestion pipeline. Unlike the insert in Step 2, this insert will have a valid METADATA$ROW\_LAST\_COMMIT\_TIME timestamp because the table property is enabled.

   Copy code

   ```
   INSERT INTO table1 VALUES('server-side-insert-2', current_timestamp());
   ```
6. Run your client-side program again, and then do the following:

   Copy code

   ```
   SELECT *, METADATA$ROW_LAST_COMMIT_TIME AS ROW_TIMESTAMP, TIMESTAMPDIFF(ms, CLIENT_TIMESTAMP, ROW_TIMESTAMP)
     AS INGEST_LATENCY FROM table1 ORDER BY 2;
   ```

### Example: measure pipeline latency with dynamic tables

Row timestamps are supported on dynamic tables. By enabling ROW\_TIMESTAMP on both a source table and a dynamic table, you can
measure pipeline latency — the time it takes for data to flow from the source table through to the dynamic table.

The following example creates a source table, inserts data, creates a dynamic table that materializes the source row timestamp,
refreshes the dynamic table, and then queries it to compute pipeline latency.

1. Create a source table with row timestamps enabled and insert data:

   Copy code

   ```
   CREATE OR REPLACE TABLE raw_events (
     event_id INT,
     event_type STRING,
     event_data STRING
   ) ROW_TIMESTAMP = TRUE;

   INSERT INTO raw_events VALUES
     (1, 'click', '{"page":"home"}'),
     (2, 'view',  '{"page":"product"}');
   ```
2. Create a dynamic table that materializes the source table’s `METADATA$ROW_LAST_COMMIT_TIME` as a column. Enable
   ROW\_TIMESTAMP on the dynamic table as well so it has its own `METADATA$ROW_LAST_COMMIT_TIME`:

   Copy code

   ```
   CREATE OR REPLACE DYNAMIC TABLE processed_events
     TARGET_LAG = '1 minute'
     WAREHOUSE = my_warehouse
     REFRESH_MODE = INCREMENTAL
     ROW_TIMESTAMP = TRUE
   AS
   SELECT
     event_id,
     event_type,
     event_data,
     METADATA$ROW_LAST_COMMIT_TIME AS source_last_commit_time
   FROM raw_events;
   ```
3. Refresh the dynamic table to process the inserted rows:

   Copy code

   ```
   ALTER DYNAMIC TABLE processed_events REFRESH;
   ```
4. Query the dynamic table to measure pipeline latency. The `source_last_commit_time` column captures when each row was
   committed in the source table, while the dynamic table’s own `METADATA$ROW_LAST_COMMIT_TIME` records when the dynamic
   table refresh committed that row:

   Copy code

   ```
   SELECT
     event_id,
     event_type,
     source_last_commit_time,
     METADATA$ROW_LAST_COMMIT_TIME AS dt_last_commit_time,
     TIMESTAMPDIFF('second', source_last_commit_time, METADATA$ROW_LAST_COMMIT_TIME) AS pipeline_latency_seconds
   FROM processed_events
   ORDER BY event_id;
   ```

### Example: expire or archive rows based on commit time

Because [storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies) can evaluate
METADATA$ROW\_LAST\_COMMIT\_TIME, you can retain rows by commit time without maintaining your own timestamp column.

The following example archives rows to COOL storage 90 days after they were last committed, then expires them
from archive after a further 365 days. For an expiration-only policy, omit ARCHIVE\_TIER and ARCHIVE\_FOR\_DAYS.

Copy code

```
CREATE OR REPLACE STORAGE LIFECYCLE POLICY retain_by_commit_time
  AS (commit_time TIMESTAMP)
  RETURNS BOOLEAN ->
    TO_DATE(commit_time) < TO_DATE(DATEADD(DAY, -90, CURRENT_TIMESTAMP()))
  ARCHIVE_TIER = COOL
  ARCHIVE_FOR_DAYS = 365;

ALTER TABLE events ADD STORAGE LIFECYCLE POLICY retain_by_commit_time
  ON (METADATA$ROW_LAST_COMMIT_TIME);
```

## Secondary use cases

Row timestamps can also be used in the following cases:

- **Data retention**: Attach a [storage lifecycle policy](/user-guide/storage-management/storage-lifecycle-policies)
  on METADATA$ROW\_LAST\_COMMIT\_TIME to automatically expire or archive old rows and save on storage costs, without
  maintaining your own last-modified column.
- **Event ordering and change tracking**: You can use row timestamps to track changes. The row with the largest timestamp represents the
  latest change.
- **Append-only data**: If rows are only appended, row timestamps can help filter for table states from specific points in time, enabling
  you to use [Time Travel](/user-guide/data-time-travel) regardless of data retention policy.

## Limitations and considerations

- Row timestamps are only guaranteed to maintain chronological order within the same table, except in the event of failover where ordering
  isn’t guaranteed. Ordering across tables, different regions, or other time sources isn’t guaranteed. You shouldn’t compare row timestamps
  across tables or other sources because doing so can lead to inconsistencies.
- Row timestamps reflect the last updated time, not the creation time. For instance, if the data row is updated after it has been committed,
  the row timestamp reflects the last updated time, not the creation time of the data.
- Timestamps on rows created before the row timestamps were enabled for a table are set to NULL.
- Row timestamps are stored as long as the rows are stored.
- Setting the ROW\_TIMESTAMP property to FALSE permanently deletes all stored METADATA$ROW\_LAST\_COMMIT\_TIME values. Re-enabling
  it will not restore them and Time Travel queries will return nothing.
- Row timestamps are not supported for Apache Iceberg™ tables, external tables, hybrid tables, streams, or views.
- The metadata column METADATA$ROW\_LAST\_COMMIT\_TIME can’t be referenced in the following:

  - [CHANGES](/sql-reference/constructs/changes) clause
  - Row access policies and column access (masking) policies
  - Constraints
  - CLUSTER BY expressions
- [Storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies) can reference
  METADATA$ROW\_LAST\_COMMIT\_TIME. Both expiration and archival policies are supported, so you can expire or
  archive rows based on when they were last committed instead of maintaining your own timestamp column. This
  isn’t supported for [dynamic tables](/user-guide/dynamic-tables/storage-lifecycle-policies): attaching a
  policy that references METADATA$ROW\_LAST\_COMMIT\_TIME to a dynamic table returns an unsupported feature error.
- Row timestamps can’t be restored by archive table restore. As a workaround, you can materialize METADATA$ROW\_LAST\_COMMIT\_TIME as a persisted
  column of another table to use in archive restore.

### Cloning considerations for row timestamps

Cloning a table preserves row timestamps exactly. Operations that create a physical copy of data, such as CREATE TABLE AS SELECT (CTAS) and
INSERT INTO … SELECT, assign fresh row timestamps reflecting when the copy was made. The original row timestamps from the source table aren’t
preserved. If you would like to keep a record of them, then select them explicitly into a persisted column, as shown in the
following example:

Copy code

```
CREATE TABLE my_archive AS
 SELECT *, METADATA$ROW_LAST_COMMIT_TIME AS original_commit_time
 FROM my_source_table;
```
