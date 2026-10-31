# Parquet Direct

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

## Overview

Parquet Direct lets you create a read-only [Apache Iceberg™ table](/user-guide/tables-iceberg) in Snowflake from
Apache Parquet™ files that you manage in object storage. Snowflake registers your existing Parquet files in place, so you
can query your data lake without copying the data or rewriting it into another table format.

Parquet Direct is one type of [Direct Iceberg table](/user-guide/tables-iceberg-direct). Use it when your data lake contains
plain Parquet files, with or without Hive-style partitioning, that aren’t managed by a table format such as Iceberg or
Delta Lake.

Parquet Direct offers the following benefits:

- **Performance**: Queries use Snowflake’s Iceberg table engine, which delivers better performance than
  [external tables](/user-guide/tables-external-intro).
- **Cost**: Snowflake queries Parquet files in-place without any additional storage costs.
- **Seamless syncing**: Snowflake can automatically refresh tables to reflect files that are added, changed, or deleted
  in storage, including schema changes.
- **Hive-style partitioning**: Snowflake can automatically infer partition columns from Hive-style `key=value` paths to simplify table creation.

Note

Parquet Direct tables are read-only. You can’t perform DML operations (INSERT, UPDATE, DELETE) on these tables in
Snowflake. Instead, use other engines to modify the files in cloud storage, and refresh the table to pick up the changes.
For all limitations, see [Considerations and limitations](#label-tables-iceberg-parquet-direct-limitations).

## How Parquet Direct works

A Parquet Direct table uses three objects:

- An [external volume](/user-guide/tables-iceberg-storage) that gives Snowflake read access to the storage location that
  contains your Parquet files.
- A [catalog integration](/sql-reference/sql/create-catalog-integration-object-storage) with
  `CATALOG_SOURCE = OBJECT_STORE` and a `TABLE_FORMAT` of `NONE` or `HIVE`. The table format tells Snowflake how to
  interpret your directory layout.
- An Iceberg table, created with [CREATE ICEBERG TABLE (Parquet files in object storage)](/sql-reference/sql/create-iceberg-table-parquet), that points to a base location
  on the external volume.

When you create the table and each time you refresh it, Snowflake lists the Parquet files under the base location and
registers new, changed, and deleted files in the table’s metadata. Queries read the registered files directly from your
storage.

## Partitioning

To improve query performance, Snowflake strongly recommends that you partition tables created from Parquet files.
Query response time is faster when Snowflake processes only a small part of the data instead of scanning the entire
dataset. To partition a table, your data must be organized using logical paths.

How partition columns work depends on the `TABLE_FORMAT` of the catalog integration:

- **`TABLE_FORMAT = HIVE`**: Snowflake infers partition column names and values from Hive-style `key=value` directory names
  in your file paths (for example, `year=2024/month=01/`). You don’t write partition expressions, and you can’t define
  explicit partition columns.
- **`TABLE_FORMAT = NONE`**: Use when your paths aren’t Hive-style. You define partition columns explicitly by using
  expressions that parse the `METADATA$FILENAME` pseudocolumn; for example, a regular expression that extracts a date or
  identifier from the path. For an example, see [Define a partition column with an expression](/sql-reference/sql/create-iceberg-table-parquet#label-sql-create-iceberg-table-parquet-example-partition).

In both cases, Snowflake computes partitions when the table is refreshed.

If your data lake has Hive-style partition keys with inconsistent casing (for example, some files under `Year=2024/` and
others under `year=2024/`), set `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` on the table so that Snowflake resolves all
casing variants to the same partition column.

## Create a Parquet Direct table

To create a Parquet Direct table, complete the following steps. For complete, end-to-end instructions that also set up
auto-refresh, see the [tutorials](#label-tables-iceberg-parquet-direct-auto-refresh).

### Step 1: Create an external volume

To create an external volume, complete the instructions for your cloud storage service:

- [Amazon S3](/user-guide/tables-iceberg-configure-external-volume-s3)
- [Google Cloud Storage](/user-guide/tables-iceberg-configure-external-volume-gcs)
- [Azure Storage](/user-guide/tables-iceberg-configure-external-volume-azure)

### Step 2: Create a catalog integration

Create a catalog integration by using the [CREATE CATALOG INTEGRATION (Object storage)](/sql-reference/sql/create-catalog-integration-object-storage) command with
`CATALOG_SOURCE = OBJECT_STORE`. Choose the table format that matches your file layout:

Copy code

```
-- Hive-style partitioned data (for example, year=2024/month=01/data.parquet)
CREATE CATALOG INTEGRATION hive_catalog_int
  CATALOG_SOURCE = OBJECT_STORE
  TABLE_FORMAT = HIVE
  ENABLED = TRUE;

-- Custom directory layouts, or partition columns that you define with expressions
CREATE CATALOG INTEGRATION parquet_catalog_int
  CATALOG_SOURCE = OBJECT_STORE
  TABLE_FORMAT = NONE
  ENABLED = TRUE;
```

### Step 3: Create an Iceberg table

Create a table by using the [CREATE ICEBERG TABLE (Parquet files in object storage)](/sql-reference/sql/create-iceberg-table-parquet) command. The following example lets
Snowflake infer the schema and partition columns, and evolve the schema on later refreshes:

Copy code

```
CREATE ICEBERG TABLE sales_data
  EXTERNAL_VOLUME = 'my_ext_vol'
  CATALOG = 'hive_catalog_int'
  BASE_LOCATION = 'sales/'
  ENABLE_SCHEMA_EVOLUTION = TRUE;
```

Schema evolution is disabled by default, and you can’t enable it after you create the table, so include
`ENABLE_SCHEMA_EVOLUTION = TRUE` in the CREATE ICEBERG TABLE statement.

For more examples, including explicit column definitions and partition expressions, see
[Examples](/sql-reference/sql/create-iceberg-table-parquet#label-sql-create-iceberg-table-parquet-examples).

## Refresh a Parquet Direct table

Refreshing a table registers the latest changes to your Parquet files in object storage. You can
[refresh the table automatically](#label-tables-iceberg-parquet-direct-auto-refresh) when Snowflake receives event
notifications from your cloud storage, or [refresh it manually](#label-tables-iceberg-parquet-direct-manual-refresh).
Snowflake recommends auto-refresh.

### Auto-refresh

Parquet Direct supports event-driven auto-refresh for all three major cloud storage providers. Auto-refresh is serverless:
Snowflake processes event notifications for new, changed, and deleted files as they arrive, without a warehouse.

To set up auto-refresh, follow the tutorial for your cloud storage provider:

- [Tutorial: Auto-refresh a Parquet Direct table from Amazon S3](/user-guide/tutorials/parquet-direct-auto-refresh-s3)
- [Tutorial: Auto-refresh a Parquet Direct table from Azure Blob Storage](/user-guide/tutorials/parquet-direct-auto-refresh-azure)
- [Tutorial: Auto-refresh a Parquet Direct table from Google Cloud Storage](/user-guide/tutorials/parquet-direct-auto-refresh-gcs)

When you enable auto-refresh on a table that previously had auto-refresh disabled, Snowflake queues notifications for
files that were added while auto-refresh was off and processes a full backfill refresh asynchronously.

### Manual refresh

To manually refresh a table, use [ALTER ICEBERG TABLE … REFRESH](/sql-reference/sql/alter-iceberg-table-refresh). You can
refresh the entire base location, or specify a path relative to the base location to refresh a directory, a partition, or a
single file:

Copy code

```
-- Refresh all files under the table's BASE_LOCATION
ALTER ICEBERG TABLE my_table REFRESH;

-- Refresh a directory or partition
ALTER ICEBERG TABLE my_table REFRESH '/year=2024/month=01/';

-- Refresh a single file
ALTER ICEBERG TABLE my_table REFRESH '/year=2024/month=01/part-00001.parquet';
```

Note

- Snowflake matches the path as a prefix. For example, `'/year=2024/month=1'` refreshes both `month=1` and `month=10`
  through `month=12`. To refresh only one directory, end the path with a slash, as in `'/year=2024/month=1/'`. For more
  examples, see [ALTER ICEBERG TABLE … REFRESH](/sql-reference/sql/alter-iceberg-table-refresh).
- If you specify a path that doesn’t exist, the refresh proceeds as if you didn’t specify a path.
- You can’t manually refresh a table that has auto-refresh enabled. To manually refresh the table, set
  `AUTO_REFRESH = FALSE` first.

### Schema evolution

With `ENABLE_SCHEMA_EVOLUTION = TRUE`, a refresh synchronizes the table with the following schema changes in your Parquet
files:

- New columns
- Type widening, as defined by the Apache Iceberg specification, for the following types:

| Original type | Widened type | Notes |
| --- | --- | --- |
| int | long | NUMBER(10,0) to NUMBER(19,0) |
| float | double | Both map to Snowflake FLOAT |
| decimal(p1, s) | decimal(p2, s) | Precision can increase; for example, decimal(5,2) to decimal(7,2) |

Expand

Show lessSee more

Type widening also applies recursively to struct fields, array elements, and map keys and values. For example:

```
struct<p1:int, p2:float, p3:decimal(5,2)>  →  struct<p1:long, p2:double, p3:decimal(8,2)>
array<int>                                 →  array<long>
map<int, string>                           →  map<long, string>
map<string, float>                         →  map<string, double>
```

Schema evolution is disabled by default, even when Snowflake infers the schema at creation time. You can only enable
schema evolution when you create the table:

Copy code

```
CREATE ICEBERG TABLE my_table
  EXTERNAL_VOLUME = 'my_ext_vol'
  CATALOG = 'my_parquet_cat_int'
  BASE_LOCATION = 'my/relative/path/'
  ENABLE_SCHEMA_EVOLUTION = TRUE;
```

After you create the table, you can disable schema evolution, but you can’t enable it again:

Copy code

```
ALTER ICEBERG TABLE my_table SET ENABLE_SCHEMA_EVOLUTION = FALSE;
```

Without schema evolution, you can’t change a Parquet Direct table’s schema. To pick up schema changes in an existing table
that was created without schema evolution, re-create the table with `ENABLE_SCHEMA_EVOLUTION = TRUE`.

## Best practices

### Use schema inference and schema evolution

Let Snowflake infer the table schema and evolve it over time:

- Schema inference reads your Parquet files and chooses the most appropriate Snowflake data type for each column.
- Schema evolution ensures that new columns and type widening in your files aren’t silently missed on refresh.

When you omit the column list in CREATE ICEBERG TABLE, Snowflake enables schema inference by default, but not schema
evolution. Set `ENABLE_SCHEMA_EVOLUTION = TRUE` when you create the table, because you can’t enable schema evolution
later.

### Use Hive partition inference

If your files use Hive-style `key=value` paths, create the catalog integration with `TABLE_FORMAT = HIVE` so that
Snowflake infers partition columns automatically, instead of writing and maintaining partition expressions.

### Use auto-refresh

Auto-refresh is event-driven and serverless. Compared with scheduled manual refreshes, it’s usually less expensive and picks up
incremental changes much faster, because Snowflake processes only the files named in event notifications instead of listing
the entire base location.

### Use auto-refresh when creating large tables

By default, CREATE ICEBERG TABLE registers all existing files before it completes, which can take a long time for a large
table. You can use auto-refresh to register the existing files instead. Create the table with both
`REFRESH_ON_CREATE = FALSE` and `AUTO_REFRESH = FALSE`, then turn on auto-refresh:

Copy code

```
CREATE ICEBERG TABLE my_large_table
  EXTERNAL_VOLUME = 'my_ext_vol'
  CATALOG = 'parquet_catalog_int'
  BASE_LOCATION = 'data-lake/'
  ENABLE_SCHEMA_EVOLUTION = TRUE
  REFRESH_ON_CREATE = FALSE
  AUTO_REFRESH = FALSE;

ALTER ICEBERG TABLE my_large_table SET AUTO_REFRESH = TRUE;
```

Snowflake then registers the existing files in the background. Instead of blocking until every file is registered, the table
is queryable immediately and returns more results as files are registered.

Note

When you use `REFRESH_ON_CREATE = FALSE`, you must define the table’s columns explicitly, because schema inference requires
files at creation time.

### Register only the files you need from cold storage

If your Parquet files are in a cold or archive storage tier, avoid registering every file in the base location, because
registration reads each file and requires it to be in a hot tier. Instead, create the table with
`REFRESH_ON_CREATE = FALSE`, then [manually refresh](#label-tables-iceberg-parquet-direct-manual-refresh) only the paths
that your queries need. Snowflake reads only the files under those paths, so you only need to move those files to a hot
tier:

Copy code

```
CREATE ICEBERG TABLE archived_orders 
  EXTERNAL_VOLUME = 'my_ext_vol'
  CATALOG = 'parquet_catalog_int'
  BASE_LOCATION = 'archive/orders/'
  ENABLE_SCHEMA_EVOLUTION = TRUE
  REFRESH_ON_CREATE = FALSE;

ALTER ICEBERG TABLE archived_orders REFRESH '2026/09/';
```

Snowflake doesn’t register files when you query the table. Queries return data only from the files that you registered.

### Give each table its own storage folder

Keep each table’s files in their own folder, and don’t point one table’s `BASE_LOCATION` inside another table’s base
location. Disjoint folders keep each table’s contents unambiguous, and ensure that any storage credentials scoped to a
table, such as with future credential vending, aren’t over-scoped to the files of other tables.

The following layout is recommended. Each table has its own folder:

```
s3://analytics-lake/
├── inbound/
│   ├── orders/                       ← table ORDERS
│   │   ├── year=2024/
│   │   │   ├── month=01/
│   │   │   │   ├── part-0000.parquet
│   │   │   │   └── part-0001.parquet
│   │   │   └── month=02/
│   │   │       └── part-0000.parquet
│   │   └── year=2025/
│   │       └── month=01/
│   │           └── part-0000.parquet
│   │
│   └── returns/                      ← table RETURNS
│       ├── year=2024/
│       │   └── month=01/
│       │       └── part-0000.parquet
│       └── year=2025/
│           └── month=01/
│               └── part-0000.parquet
│
└── curated/
    └── sales/                        ← table SALES
        └── year=2024/month=01/…
```

Avoid the following layout. The RETURNS table’s folder is nested inside the folder for the ORDERS table, so ORDERS also
picks up the RETURNS files:

```
s3://analytics-lake/inbound/orders/         ← ORDERS owns this whole tree
├── year=2024/month=01/part-0000.parquet
└── returns/                                ← RETURNS pointed here  ✗
    └── year=2024/month=01/part-0000.parquet
```

## Monitor refresh

Snowflake provides the following tools to monitor Parquet Direct tables:

| Tool | Best used for |
| --- | --- |
| [Event tables](#label-tables-iceberg-parquet-direct-monitoring-events) | Debugging auto-refresh at the file level, and building real-time alerts and notifications. |
| [SYSTEM$PARQUET\_DIRECT\_AUTO\_REFRESH\_STATUS](#label-tables-iceberg-parquet-direct-monitoring-status) | A current snapshot of auto-refresh health for a table. |
| [ICEBERG\_TABLE\_FILE\_REGISTRATION\_HISTORY](#label-tables-iceberg-parquet-direct-monitoring-files) and [ICEBERG\_TABLE\_FILES](#label-tables-iceberg-parquet-direct-monitoring-files) | Which files were registered, when, and which files the table currently contains. |
| [PIPE\_USAGE\_HISTORY view](#label-tables-iceberg-parquet-direct-monitoring-pipe-usage) | Auto-refresh history and compute costs over time. |

Expand

Show lessSee more

### Monitor auto-refresh with an event table

Snowflake can record auto-refresh events for Parquet Direct tables in your [active event table](/developer-guide/logging-tracing/event-table-setting-up).
Events are emitted for auto-refresh only; manual refreshes and table creation don’t emit events.

Note

To use an event table to monitor Parquet Direct auto-refresh, contact [Snowflake Support](/user-guide/contacting-support)
to request access.

#### Log levels

To capture events, set the [LOG\_EVENT\_LEVEL](/sql-reference/parameters#label-log-event-level) parameter on the table, or on its schema, database, or
account. Snowflake captures events at the level you set and at more severe levels:

| Level | Event name | What it captures |
| --- | --- | --- |
| `ERROR` | `parquet_direct_file_ingestion_failure` | One event for each file that auto-refresh failed to register. Body fields: `file_path`, `error_message`. |
| `INFO` | `parquet_direct_auto_refresh_batch_success` | One event for each successfully committed batch of files. Body fields: `add_count`, `delete_count`, `skip_count`, `ingested_size` (bytes), `total_latency`, `processing_latency`. |
| `DEBUG` | `parquet_direct_file_lifecycle` | One event for each file that auto-refresh registered or removed. Body fields: `file_path`, `state` (`INGESTED` or `DELETED`). |

Expand

Show lessSee more

Latency fields are in milliseconds. Parquet Direct tables don’t emit WARN events.

Events use the scope `snow.ingest.parquet_direct`. The `resource_attributes` column includes the database, schema, and table
name.

For most tables, set `LOG_EVENT_LEVEL = ERROR` to capture failures, or `INFO` to also track successful refreshes. Use `DEBUG`
only while you troubleshoot specific files, because it records an event for every file.

Copy code

```
ALTER ICEBERG TABLE my_parquet_table SET LOG_EVENT_LEVEL = INFO;
```

#### Query auto-refresh events

The following example retrieves recent auto-refresh events for a table:

The event body fields are in the `VALUE` column.

Copy code

```
SELECT timestamp,
       record:"name"::STRING AS event_name,
       record:"severity_text"::STRING AS log_level,
       resource_attributes:"snow.table.name"::STRING AS table_name,
       PARSE_JSON(value) AS event_body
  FROM my_active_event_table
  WHERE record_type = 'EVENT'
    AND scope:"name" = 'snow.ingest.parquet_direct'
    AND resource_attributes:"snow.table.name" = 'MY_PARQUET_TABLE'
  ORDER BY timestamp DESC
  LIMIT 100;
```

The following example summarizes files added, deleted, and bytes registered by auto-refresh per hour:

Copy code

```
SELECT DATE_TRUNC('hour', timestamp) AS hour,
       resource_attributes:"snow.table.name"::STRING AS table_name,
       SUM(PARSE_JSON(value):add_count::NUMBER) AS files_added,
       SUM(PARSE_JSON(value):delete_count::NUMBER) AS files_deleted,
       SUM(PARSE_JSON(value):ingested_size::NUMBER) AS bytes_registered
  FROM my_active_event_table
  WHERE record_type = 'EVENT'
    AND record:"name" = 'parquet_direct_auto_refresh_batch_success'
  GROUP BY ALL
  ORDER BY hour DESC;
```

The following example lists files that failed to register in the last day:

Copy code

```
SELECT timestamp,
       resource_attributes:"snow.table.name"::STRING AS table_name,
       PARSE_JSON(value):file_path::STRING AS file_path,
       PARSE_JSON(value):error_message::STRING AS error_message
  FROM my_active_event_table
  WHERE record_type = 'EVENT'
    AND record:"name" = 'parquet_direct_file_ingestion_failure'
    AND timestamp > DATEADD(day, -1, CURRENT_TIMESTAMP())
  ORDER BY timestamp DESC;
```

#### Alert on auto-refresh failures

You can create an [alert](/user-guide/alerts) that notifies you when auto-refresh fails to register files. The following
example checks for failure events every 10 minutes and sends an email by using an existing
[email notification integration](/user-guide/notifications/email-notifications):

Copy code

```
CREATE ALERT parquet_direct_failure_alert
  WAREHOUSE = my_alert_wh
  SCHEDULE = '10 MINUTE'
  IF (EXISTS (
    SELECT 1
      FROM my_active_event_table
      WHERE record_type = 'EVENT'
        AND record:"name" = 'parquet_direct_file_ingestion_failure'
        AND timestamp BETWEEN SNOWFLAKE.ALERT.LAST_SUCCESSFUL_SCHEDULED_TIME()
                          AND SNOWFLAKE.ALERT.SCHEDULED_TIME()
  ))
  THEN
    CALL SYSTEM$SEND_EMAIL(
      'my_email_int',
      'data-team@example.com',
      'Parquet Direct auto-refresh failures',
      'One or more Parquet files failed to register. Check the event table for details.'
    );

ALTER ALERT parquet_direct_failure_alert RESUME;
```

You can integrate Snowflake notifications with external systems such as Slack, Microsoft Teams, PagerDuty, Jira, and ServiceNow by using the [webhooks](/user-guide/notifications/webhook-notifications).

### Check auto-refresh status

Use [SYSTEM$PARQUET\_DIRECT\_AUTO\_REFRESH\_STATUS](/sql-reference/functions/system_parquet_direct_auto_refresh_status) to get a current snapshot of auto-refresh for a
table, including its execution state, the number of files waiting to be processed, and the most recent notification and
error from the notification channel:

Copy code

```
SELECT SYSTEM$PARQUET_DIRECT_AUTO_REFRESH_STATUS('my_db.my_schema.my_parquet_table');
```

To extract individual fields, parse the result:

Copy code

```
SELECT status:executionState::STRING AS execution_state,
       status:pendingFileCount::NUMBER AS pending_files,
       status:lastReceivedMessageTimestamp::TIMESTAMP_LTZ AS last_notification,
       status:channelErrorMessage::STRING AS channel_error
  FROM (
    SELECT PARSE_JSON(SYSTEM$PARQUET_DIRECT_AUTO_REFRESH_STATUS('my_db.my_schema.my_parquet_table')) AS status
  );
```

An `executionState` of `RUNNING` means auto-refresh is healthy. `STALLED` means Snowflake encountered an error and is
attempting to recover, and `STOPPED` means auto-refresh stopped and requires action; see
[Refresh fails](#label-tables-iceberg-parquet-direct-troubleshoot-refresh-fails).

### Check registered files

Use the following Information Schema table functions to see which Parquet files Snowflake registered for a table:

- [ICEBERG\_TABLE\_FILE\_REGISTRATION\_HISTORY](/sql-reference/functions/iceberg_table_file_registration_history) returns the history of file registration operations,
  including failures and the reason for each failure.
- [ICEBERG\_TABLE\_FILES](/sql-reference/functions/iceberg_table_files) returns the files that the table currently contains.

Copy code

```
-- Recent registration activity, including failures
SELECT *
  FROM TABLE(my_db.INFORMATION_SCHEMA.ICEBERG_TABLE_FILE_REGISTRATION_HISTORY(
    TABLE_NAME => 'my_db.my_schema.my_parquet_table',
    START_TIME => DATEADD(day, -1, CURRENT_TIMESTAMP())))
  ORDER BY operation_time DESC;

-- Files currently registered in the table
SELECT file_name, registered_on, file_size, row_count
  FROM TABLE(my_db.INFORMATION_SCHEMA.ICEBERG_TABLE_FILES(
    TABLE_NAME => 'my_db.my_schema.my_parquet_table'))
  ORDER BY registered_on DESC;
```

### Track auto-refresh history and compute costs

Auto-refresh credits appear in the [PIPE\_USAGE\_HISTORY view](/sql-reference/account-usage/pipe_usage_history) view.

Note

To query Parquet Direct tables in the PIPE\_USAGE\_HISTORY view, contact [Snowflake Support](/user-guide/contacting-support)
to request access.

The following example shows daily auto-refresh credits and bytes for a Parquet Direct table over the last 30 days:

Copy code

```
SELECT pipe_name AS table_name,
       DATE_TRUNC('day', start_time) AS usage_date,
       SUM(credits_used) AS credits_used,
       SUM(bytes_inserted) AS bytes_inserted,
       SUM(files_inserted) AS files_inserted
  FROM SNOWFLAKE.ACCOUNT_USAGE.PIPE_USAGE_HISTORY
  WHERE pipe_name = 'MY_PARQUET_TABLE'
    AND start_time > DATEADD(day, -30, CURRENT_TIMESTAMP())
  GROUP BY ALL
  ORDER BY usage_date DESC;
```

For Parquet Direct tables, the `PIPE_NAME` column contains the table name, without the database or schema name.

## Troubleshooting

### Refresh succeeds but data is missing

If a refresh succeeds but some data doesn’t appear in query results, complete the following steps:

1. Check whether the table’s `PATTERN` excludes the missing files. Use [DESCRIBE ICEBERG TABLE](/sql-reference/sql/desc-iceberg-table) or
   [GET\_DDL](/sql-reference/functions/get_ddl) to see the table definition, and verify that the missing file paths match the
   regular expression.
2. Check whether Snowflake registered the files, and whether any registration failed:

   Copy code

   ```
   SELECT operation_time, file_name, operation_status, message
     FROM TABLE(INFORMATION_SCHEMA.ICEBERG_TABLE_FILE_REGISTRATION_HISTORY(
       TABLE_NAME => 'my_parquet_table'))
     ORDER BY operation_time DESC;
   ```

   To see every file that the table currently contains, query [ICEBERG\_TABLE\_FILES](/sql-reference/functions/iceberg_table_files).
3. If the table uses auto-refresh, check when Snowflake last received a notification from your cloud storage:

   Copy code

   ```
   SELECT SYSTEM$PARQUET_DIRECT_AUTO_REFRESH_STATUS('my_parquet_table');
   ```

   If `lastReceivedMessageTimestamp` is older than the time you added the files and `pendingFileCount` = 0, Snowflake didn’t receive notifications for
   them. This could be because of a misconfiguration either between your bucket and queue, or your queue and Snowflake account. Verify your cloud storage event notification configuration; see the tutorial for your
   [cloud storage provider](#label-tables-iceberg-parquet-direct-auto-refresh).

### Refresh fails

1. Find the most recent failure:

   - For auto-refresh, call [SYSTEM$PARQUET\_DIRECT\_AUTO\_REFRESH\_STATUS](/sql-reference/functions/system_parquet_direct_auto_refresh_status) and check the
     `executionState`, `invalidExecutionStateReason`, and `channelErrorMessage` fields. If you set up an
     [event table](#label-tables-iceberg-parquet-direct-monitoring-events), query it for
     `parquet_direct_file_ingestion_failure` events.
   - For a manual refresh, look up the refresh statement by its query ID in [QUERY\_HISTORY , QUERY\_HISTORY\_BY\_\*](/sql-reference/functions/query_history)
     and check the error message:

     Copy code

     ```
     SELECT query_id, query_text, error_code, error_message
       FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
       WHERE query_id = '<query_id>';
     ```
2. If auto-refresh is failing, fix the underlying issue, then reset auto-refresh by running a manual refresh:

   1. Disable auto-refresh on the table:

      Copy code

      ```
      ALTER ICEBERG TABLE my_parquet_table SET AUTO_REFRESH = FALSE;
      ```
   2. Manually refresh the table:

      Copy code

      ```
      ALTER ICEBERG TABLE my_parquet_table REFRESH;
      ```
   3. Re-enable auto-refresh:

      Copy code

      ```
      ALTER ICEBERG TABLE my_parquet_table SET AUTO_REFRESH = TRUE;
      ```

### Refresh fails with a schema error

If a refresh fails because a file’s schema doesn’t match the table, compare the file’s schema with the table definition:

1. Run [INFER\_SCHEMA](/sql-reference/functions/infer_schema) on the failing file:

   Copy code

   ```
   SELECT *
     FROM TABLE(
       INFER_SCHEMA(
         LOCATION => '@my_stage/folder/my_single_file.parquet',
         FILE_FORMAT => 'my_parquet_format'));
   ```

   This step requires a [stage](/sql-reference/sql/create-stage) that points to the same storage location and a
   [Parquet file format](/sql-reference/sql/create-file-format).
2. Get the table definition with [GET\_DDL](/sql-reference/functions/get_ddl), and compare the column names and types:

   Copy code

   ```
   SELECT GET_DDL('ICEBERG_TABLE', 'my_parquet_table');
   ```

If the file adds columns or widens types and the table was created without
[schema evolution](#label-tables-iceberg-parquet-direct-schema-evolution), re-create the table with
`ENABLE_SCHEMA_EVOLUTION = TRUE`.
If the file changes a column type in a way that schema evolution doesn’t support, fix the file or create a new table.

### Initial table creation takes a long time

By default, CREATE ICEBERG TABLE registers all existing files in the base location before it completes. For a large table, use one of the following approaches instead:

- Create the table with `REFRESH_ON_CREATE = FALSE` to skip the initial registration, then register older files
  gradually by [manually refreshing specific paths](#label-tables-iceberg-parquet-direct-manual-refresh).
- [Create the table with auto-refresh](#label-tables-iceberg-parquet-direct-best-practices-create) so the table is
  queryable immediately and returns more results as files are registered.

With `REFRESH_ON_CREATE = FALSE`, Snowflake doesn’t register files when you query the table. The table returns no rows
until you refresh it or auto-refresh registers files.

### You can’t change the table schema

Without schema evolution, you can’t modify a Parquet Direct table’s schema, and you can’t enable schema evolution on an
existing table. To let the table pick up new columns and widened types from your files, re-create the table with
`ENABLE_SCHEMA_EVOLUTION = TRUE`. For more information, see [Schema evolution](#label-tables-iceberg-parquet-direct-schema-evolution).

## Billing

Parquet Direct costs have the following components:

| Component | What you pay for |
| --- | --- |
| Table creation and manual refresh | Compute used for registering Parquet files during table creation and refresh. |
| Auto-refresh | Serverless compute to process event notifications and register files, plus data registration for the bytes added. Auto-refresh compute appears in the [PIPE\_USAGE\_HISTORY](/sql-reference/account-usage/pipe_usage_history) view. |
| Data registration | 0.35 credits per terabyte of Parquet data added to a table, for every creation, manual refresh, and auto-refresh. Files that are deleted or unchanged aren’t charged. |

Expand

Show lessSee more

Important

Billing for data registration takes effect on December 1, 2026. Data registration
before that date isn’t billed.

For more information about the credits charged for each service, see the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

### Query Parquet Direct costs

The following example returns auto-refresh compute credits for each table over the last 30 days. To query Parquet Direct
tables in the PIPE\_USAGE\_HISTORY view, contact [Snowflake Support](/user-guide/contacting-support) to request access.

Copy code

```
SELECT pipe_name AS table_name,
       SUM(credits_used) AS credits
  FROM SNOWFLAKE.ACCOUNT_USAGE.PIPE_USAGE_HISTORY
  WHERE start_time > DATEADD(day, -30, CURRENT_TIMESTAMP())
  GROUP BY ALL
  ORDER BY credits DESC;
```

## Data types

For how Parquet data types map to Snowflake data types, see [Parquet data types](/user-guide/tables-iceberg-data-types#label-tables-iceberg-parquet-direct-data-types).

## Supported features

Parquet Direct tables support the following Snowflake features:

- **Queries:** Query Parquet Direct tables with SQL like any other Iceberg table, and use them as the source for
  CREATE TABLE … AS SELECT (CTAS) and CREATE TABLE … LIKE.
- **[Materialized views](/user-guide/views-materialized):** Create materialized views on Parquet Direct tables.
- **[Secure views](/user-guide/views-secure):** Create secure views on Parquet Direct tables.
- **[Insert-only streams](/user-guide/streams-intro):** Track files that are added to a Parquet Direct table. Standard and
  append-only streams aren’t supported.
- **[Tasks](/user-guide/tasks-intro):** Use Parquet Direct tables in scheduled and triggered tasks.
- **Access control and data protection:** Control access with [role-based access control](/user-guide/security-access-control-overview),
  including [organization users and groups](/user-guide/organization-users), and protect data with
  [masking policies](/user-guide/security-column-intro) and [row access policies](/user-guide/security-row-intro).
- **Performance:** Use the [search optimization service](/user-guide/search-optimization-service) and the
  [query acceleration service](/user-guide/query-acceleration-service) with Parquet Direct tables.
- **Data sharing:** [Share](/user-guide/data-sharing-intro) Parquet Direct tables, including local sharing, cross-region
  sharing, and listings that use [Cross-Cloud Auto-Fulfillment](/collaboration/provider-listings-auto-fulfillment).
- **Data types:** Use [semi-structured data types](/sql-reference/data-types-semistructured), including VARIANT, and
  [geospatial data types](/sql-reference/data-types-geospatial). For how Parquet types map to Snowflake types, see
  [Parquet data types](/user-guide/tables-iceberg-data-types#label-tables-iceberg-parquet-direct-data-types).

Parquet Direct tables also support the following capabilities for working with Parquet files:

- **Schema inference and schema evolution:** Snowflake can infer column definitions from your files when you create the
  table, and evolve the schema on later refreshes. For more information, see
  [Schema evolution](#label-tables-iceberg-parquet-direct-schema-evolution).
- **Partitioning:** Snowflake infers partition columns from Hive-style `key=value` paths when you use a catalog
  integration with `TABLE_FORMAT = HIVE`, or derives them from expressions that you define with `TABLE_FORMAT = NONE`. For
  more information, see [Partitioning](#label-tables-iceberg-parquet-direct-partitioning).
- **Case-insensitive column matching:** Files that use different casings for a column name populate the same table
  column. For more information, see the `MATCH_BY_COLUMN_NAME` parameter of
  [CREATE ICEBERG TABLE (Parquet files in object storage)](/sql-reference/sql/create-iceberg-table-parquet).
- **Refresh:** Keep tables in sync with your files by using [auto-refresh](#label-tables-iceberg-parquet-direct-auto-refresh)
  with Amazon S3, Azure Blob Storage, or Google Cloud Storage, or by
  [refreshing manually](#label-tables-iceberg-parquet-direct-manual-refresh), optionally for a specific path.
- **Monitoring:** Monitor auto-refresh with event tables, SYSTEM$PARQUET\_DIRECT\_AUTO\_REFRESH\_STATUS, and
  ICEBERG\_TABLE\_FILE\_REGISTRATION\_HISTORY. For more information, see [Monitor refresh](#label-tables-iceberg-parquet-direct-monitoring).

For features that aren’t supported, see [Considerations and limitations](#label-tables-iceberg-parquet-direct-limitations).

## Considerations and limitations

- Parquet files that use any of the following features or data types aren’t supported:

  - Invalid or duplicate field IDs. Files with valid field IDs are supported; Snowflake matches columns by name, not by
    field ID.
  - The DECIMAL data type with precision higher than 38.
  - LIST or MAP types with one-level or two-level representation.
  - Unsigned integer types (`INT(signed=false)`).
  - The FLOAT16 data type.
- Snowflake currently only supports creating Parquet Direct tables with an [object storage-based catalog integration](/sql-reference/sql/create-catalog-integration-object-storage). Other catalog integration types are not supported.
- When auto-refresh is enabled on a table, you can’t manually refresh the table. To manually refresh the table, disable
  auto-refresh first.
- Parquet Direct tables are read-only:

  - You can’t perform DML operations (INSERT, UPDATE, DELETE, MERGE) on these tables in Snowflake. Use other engines to
    modify the files in your cloud storage.
  - You can’t convert these tables to Snowflake-managed Iceberg tables.
  - You can’t perform table maintenance on these tables.
- The following Snowflake features aren’t supported for Parquet Direct tables:

  - Cloning
  - Clustering (`CLUSTER BY`)
  - Replication
  - Standard streams and append-only streams (insert-only streams are supported)
  - Dynamic tables
  - Native Apps
- You can’t create a Parquet Direct table by using CREATE TABLE … AS SELECT (CTAS) or CREATE TABLE … LIKE.
  You can use a Parquet Direct table as the source for either statement.
- You can’t undrop a Parquet Direct table. After you drop a Parquet Direct table, re-create it to register the files
  again.
- You can’t set the `DATA_RETENTION_TIME_IN_DAYS` parameter on a Parquet Direct table.
- You can’t enable schema evolution on an existing Parquet Direct table. To use schema evolution, set
  `ENABLE_SCHEMA_EVOLUTION = TRUE` when you create the table.
- Data sharing is supported for Parquet Direct tables, including local sharing, cross-region sharing, and listings that use
  Cross-Cloud Auto-Fulfillment.
