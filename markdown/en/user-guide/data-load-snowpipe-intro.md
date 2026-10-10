# Snowpipe

Snowpipe continuously loads data from files into standard tables and Apache Iceberg™ tables as the files arrive in a [stage](/user-guide/data-load-overview). You define the load once in a *pipe*, a schema object that holds a `COPY INTO` statement, and Snowpipe runs that statement for every new file on serverless compute that Snowflake manages. New data is typically available for queries within minutes, and you pay a fixed number of credits for each GB of data that Snowpipe loads.

For example, the following pipe loads JSON files from an external stage into a table as the files arrive:

Copy code

```
CREATE PIPE mydb.myschema.orders_pipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO mydb.myschema.orders
    FROM @mydb.myschema.orders_stage
    FILE_FORMAT = (TYPE = 'JSON')
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

This pipe defines where the files come from (the `orders_stage` external stage), where the data goes (the `orders` table), and how to read the files. `AUTO_INGEST = TRUE` turns on *automated loading* (also called auto-ingest): Snowpipe loads each new file when your cloud storage service reports that the file arrived. To load files from your own application instead, create the pipe without `AUTO_INGEST = TRUE` (the default is `FALSE`), and then call the [Snowpipe REST API](/user-guide/data-load-snowpipe-rest-overview) with the names of the files to load.

Before you create a pipe like this one, you need a stage that points to your files, a target table, and a role with the [required privileges](#label-snowpipe-intro-access-control). For automated loading, you also configure event notifications for your storage location so that Snowpipe learns about new files. The steps and their order depend on your cloud provider. For step-by-step instructions, see [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3), [Automating Snowpipe for Google Cloud Storage](/user-guide/data-load-snowpipe-auto-gcs), or [Automating Snowpipe for Microsoft Azure Blob Storage](/user-guide/data-load-snowpipe-auto-azure). To use the REST API instead, set up key pair authentication or workload identity federation for the user that calls the API. For step-by-step instructions, see [Set up the Snowpipe REST API](/user-guide/data-load-snowpipe-rest-gs).

With automated loading, a new pipe loads only the files that arrive after you set up event notifications. To load files that are already in the stage, see [Load historical or missed files](/user-guide/data-load-snowpipe-manage#label-snowpipe-load-historic-data).

## When to use Snowpipe

Snowpipe is a good fit when:

- **Your data already arrives as files.** For example, your applications write logs or your partners deliver exports to Amazon S3, Google Cloud Storage, Microsoft Azure storage, or a Snowflake internal stage. The storage can be on a different cloud platform from the one that hosts your Snowflake account.
- **You want each file loaded soon after it lands.** Files arrive continuously or at unpredictable times, and you want them loaded as they arrive rather than in scheduled batches.
- **You don’t want to manage compute for loading.** Snowflake provides and scales the compute for every load, so there’s no warehouse to size, start, or suspend, and no load schedule to orchestrate.
- **You load standard tables or Iceberg tables.** The same pipe syntax works for standard tables, Snowflake-managed [Iceberg tables](#label-snowpipe-intro-iceberg), and externally managed Iceberg tables. Snowpipe support for partitioned Iceberg tables is in public preview.

Another option is a better fit when:

- **Your data arrives as rows or events, and you need it within seconds.** Use [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview). To ingest Apache Kafka topics, use the [Snowflake Connector for Kafka](/user-guide/kafka-connector/index), which is built on Snowpipe Streaming.
- **You’re running a large one-time or scheduled batch load.** Use [bulk loading](/user-guide/data-load-overview) with `COPY INTO` and a warehouse. Bulk loading also lets you reload files with `FORCE` and, for standard tables, use `VALIDATION_MODE` to check files for errors before you load them.
- **Your source is a database or SaaS application rather than files.** Use an [Openflow](/user-guide/data-integration/openflow/about) connector to ingest the data directly from the source system.

Neither Snowpipe nor bulk loading can join, aggregate, or filter rows during a load. If you need that logic, use Snowpipe to land the raw data, and then transform it with [dynamic tables](/user-guide/dynamic-tables/overview) or [streams and tasks](/user-guide/streams-intro).

The following table compares Snowpipe with bulk loading and Snowpipe Streaming:

| Characteristic | Bulk loading with `COPY INTO` | Snowpipe | Snowpipe Streaming (high-performance architecture) |
| --- | --- | --- | --- |
| Data source | Files in a stage | Files in a stage | Rows sent by the Snowpipe Streaming SDK or REST API, or by the Snowflake Connector for Kafka |
| How loading starts | When you run `COPY INTO`, either manually or on a schedule, such as from a task | When cloud storage sends an event notification (automated loading), or when your application calls the Snowpipe REST API | Continuously, as your client sends rows |
| Typical latency | Depends on how often you run the load | Typically within a minute after Snowpipe learns about a file | As low as 5 seconds |
| Compute | A virtual warehouse that you size and manage | Serverless | Serverless |
| Billing | Warehouse credits for the time that the warehouse runs | A fixed number of credits per GB loaded: uncompressed size for text files, size in storage for binary files | Credits per uncompressed GB of data ingested |

Expand

Show lessSee more

## How Snowpipe works

Each pipe watches one location: the stage URL plus an optional path in the pipe’s `FROM` clause. That path is called the *pipe path*. The pipe learns about new files in that location and loads them into one target table with serverless compute.

### What happens when a file arrives

When a new file arrives in a pipe’s location, Snowpipe processes it as follows:

1. Snowpipe learns about the file, either from a cloud storage event notification or from a call to the Snowpipe REST API.
2. Snowpipe adds the file to the pipe’s ingest queue.
3. Snowflake-provided compute runs the pipe’s `COPY INTO` statement on the queued files and commits the rows to the target table.
4. Snowpipe records the file in the pipe’s [load metadata](#label-snowpipe-intro-load-metadata), whether the file loaded or failed, so that Snowpipe ignores the file if it’s staged again.

Snowpipe is designed to load new data typically within a minute after it learns about a file. Large files, and files that need significant compute to decompress, decrypt, or transform, take longer. Snowflake doesn’t guarantee load latency, so test with a representative set of files to estimate the latency for your workload.

### How Snowpipe detects new files

With automated loading (`AUTO_INGEST = TRUE`), your cloud storage service sends Snowpipe an event notification when a file arrives. With the Snowpipe REST API, your application tells Snowpipe which files to load. The following table shows the options for each storage location:

| Where your files are | How Snowpipe is notified | Setup guide |
| --- | --- | --- |
| Amazon S3 | Automated loading, with S3 event notifications delivered through Amazon SQS, Amazon SNS, or Amazon EventBridge | [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3) |
| Google Cloud Storage | Automated loading, with Google Cloud Pub/Sub and a notification integration | [Automating Snowpipe for Google Cloud Storage](/user-guide/data-load-snowpipe-auto-gcs) |
| Microsoft Azure Blob Storage, Data Lake Storage Gen2, or general-purpose v2 storage | Automated loading, with Azure Event Grid, a storage queue, and a notification integration | [Automating Snowpipe for Microsoft Azure Blob Storage](/user-guide/data-load-snowpipe-auto-azure) |
| Any supported external stage, a named internal stage, or a table stage | Snowpipe REST API, with a pipe that doesn’t set `AUTO_INGEST = TRUE`. Your application calls the `insertFiles` endpoint and authenticates with a key pair or with workload identity federation. | [Load data with the Snowpipe REST API](/user-guide/data-load-snowpipe-rest-overview) |

Expand

Show lessSee more

Keep the following in mind:

- Automated loading from internal stages is in public preview and is available only for accounts hosted on AWS. For more information, see [CREATE PIPE](/sql-reference/sql/create-pipe).
- To keep automated loading traffic from Microsoft Azure on a private network, see [Private connectivity to external stages and Snowpipe automation for Microsoft Azure](/user-guide/data-load-azure-private).

## Key concepts

The following concepts explain how a pipe is defined, which files it loads, and how it handles errors.

### Pipes

A pipe is a named schema object that holds one `COPY INTO` statement. The statement identifies the source stage, the target table, the file format, and any copy options or transformations. You can’t edit a pipe’s definition. To change it, you recreate the pipe, which drops its load metadata. To find out which changes require a new pipe and how to recreate one without losing or duplicating files, see [Change or recreate a pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-management-recreate-pipes).

### Stages and integrations

A pipe reads from an internal stage, or from an external stage that typically accesses cloud storage through a [storage integration](/sql-reference/sql/create-storage-integration). For automated loading, Snowpipe receives event notifications through a *notification channel*: the cloud messaging queue that delivers them, such as the Amazon SQS queue that’s listed in the [SHOW PIPES](/sql-reference/sql/show-pipes) output. For Google Cloud Storage or Microsoft Azure, the pipe references a [notification integration](/sql-reference/sql/create-notification-integration) that gives Snowflake access to the Pub/Sub subscription or Azure storage queue.

### File formats

Snowpipe loads the same file formats as bulk loading: delimited files such as CSV and TSV, JSON, Avro, ORC, Parquet, and XML. For more information, see [Preparing to load data](/user-guide/data-load-prepare).

### Transformations

A pipe’s `COPY INTO` statement can include a simple `SELECT` statement that reorders, omits, or casts columns, or that loads file metadata through `METADATA$` columns. You can also match columns by name with `MATCH_BY_COLUMN_NAME`, but not in the same statement as a `SELECT` transformation. With `MATCH_BY_COLUMN_NAME`, you can let the table add columns as they appear in the files by using [schema evolution](/user-guide/data-load-schema-evolution). As with bulk loading, `WHERE` clauses, `FLATTEN`, joins, and `GROUP BY` aren’t supported, so load the raw data first and transform it downstream when you need that logic. For examples, see [Transform data during a load](/user-guide/data-load-transform).

### Error handling

By default, Snowpipe doesn’t load any file that contains an error (`ON_ERROR = SKIP_FILE`) and continues to load the other files. Files that aren’t loaded because of errors have the `Load failed` status in the copy history and a `FAILED` state in [Snowpipe events](/user-guide/data-load-snowpipe-monitor-events). Bulk loading, in contrast, stops the load by default when a file contains an error (`ON_ERROR = ABORT_STATEMENT`), an option that pipes don’t support. To find files that failed to load and their errors, use the tools in [Monitoring and management](#label-snowpipe-intro-monitoring).

### Transactions

Snowpipe combines or splits loads into one or more transactions, based on the number and size of the rows in each file. In contrast, each bulk `COPY INTO` statement runs in a single transaction.

### Load metadata

Each pipe keeps load metadata, which is a record of the files that it processed in the last 14 days, including the path and name of each file. Snowpipe ignores any staged file whose path and name match a file in this record, even if the file was modified and has a different ETag. Because Snowpipe also records files that failed to load, it ignores a corrected file that you stage again with the same name. For workarounds, see [Reload a file that Snowpipe already processed](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-reload-files).

After a file’s record expires, Snowpipe loads a file that’s staged again with the same path and name, which can duplicate data. Truncating the target table doesn’t clear the pipe’s load metadata.

Bulk loads keep separate load metadata on the target table for 64 days.

Important

Avoid accidentally loading the same files with both Snowpipe and bulk loading. Each method keeps its own load metadata, so neither one ignores the files that the other one loaded. The exception is `ALTER PIPE ... REFRESH`, which checks both the pipe’s load metadata and the target table’s load metadata. To backfill historical files or reload a corrected file on purpose, follow the procedures in [Manage Snowpipe](/user-guide/data-load-snowpipe-manage).

### Load order

Each pipe has a single queue of files that are waiting to load, but multiple processes pull files from that queue. Snowpipe generally loads older files first, but doesn’t guarantee that files load in the order that they were staged.

## Cost

In all Snowflake editions, Snowpipe charges a fixed number of credits per GB of data loaded, with no charge for warehouse time or for the number of files. Text files, such as CSV and JSON, are billed on their uncompressed size. Binary files, such as Parquet, Avro, and ORC, are billed on their size in storage (observed size), regardless of compression.

For the current rate, a worked cost estimate, queries that show your actual usage, and ways to control spending, see [Snowpipe costs](/user-guide/data-load-snowpipe-billing).

## Monitoring and management

The following table lists the tools that you can use to monitor pipes and the files that they load:

| Task | Tool |
| --- | --- |
| View pipe health and copy history, and pause or resume pipes, without writing SQL | [Manage Snowpipe in Snowsight](/user-guide/data-load-snowpipe-snowsight) |
| Check whether a pipe is running and how many files are waiting to load | [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) function |
| See which files loaded, and why a file failed | [COPY\_HISTORY](/sql-reference/functions/copy_history) table function, [COPY\_HISTORY view](/sql-reference/account-usage/copy_history), or [VALIDATE\_PIPE\_LOAD](/sql-reference/functions/validate_pipe_load) function |
| Find out why files aren’t loading | [Troubleshooting Snowpipe](/user-guide/data-load-snowpipe-ts) |
| Get notified when a load fails | [Error notifications](/user-guide/data-load-snowpipe-errors) through Amazon SNS, Google Cloud Pub/Sub, or Azure Event Grid, or an [alert on Snowpipe events](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-alerts) |
| Record pipe errors and file errors in an event table | [Monitor events for Snowpipe](/user-guide/data-load-snowpipe-monitor-events) |
| List the pipes in your account and their definitions | [PIPES view](/sql-reference/account-usage/pipes), or [SHOW PIPES](/sql-reference/sql/show-pipes) for current results |
| Check the load status of files that your application submitted to the Snowpipe REST API | The `insertReport` and `loadHistoryScan` endpoints of the [Snowpipe REST API](/user-guide/data-load-snowpipe-rest-apis) |

Expand

Show lessSee more

To pause, resume, or recreate a pipe, load files that it missed, reload a corrected file, or clean up loaded files, see [Manage Snowpipe](/user-guide/data-load-snowpipe-manage). For the SQL commands that create and manage pipes, see [Pipe DDL commands](/sql-reference/ddl-stage#label-pipe-management-ddl).

## Access control

The following table lists the minimum privileges for common Snowpipe tasks:

| Object | Create a pipe | Own a pipe | Pause or resume a pipe | Refresh a pipe |
| --- | --- | --- | --- | --- |
| Account | `CREATE INTEGRATION`, only if you also create a storage integration or notification integration | Not applicable | Not applicable | Not applicable |
| Database | `USAGE` | `USAGE` | `USAGE` | `USAGE` |
| Schema | `USAGE`, `CREATE PIPE` | `USAGE` | `USAGE` | `USAGE` |
| Pipe | Not applicable | `OWNERSHIP` | `OPERATE` | `OPERATE` |
| Stage in the pipe definition | `USAGE` for an external stage; `READ` for an internal stage | `USAGE` for an external stage; `READ` for an internal stage | Not applicable | `USAGE` for an external stage; `READ` for an internal stage |
| Named file format in the pipe definition | `USAGE` | `USAGE` | Not applicable | `USAGE` |
| Table in the pipe definition | `SELECT`, `INSERT` | `SELECT`, `INSERT` | Not applicable | `SELECT`, `INSERT` |
| Error notification integration | `USAGE`, only if the pipe sends error notifications | `USAGE`, only if the pipe sends error notifications | Not applicable | Not applicable |

Expand

Show lessSee more

After you create a pipe, the role that owns it must keep the privileges in the **Own a pipe** column, or the pipe can’t load files. The exception is `USAGE` on the error notification integration: without it, the pipe keeps loading files but stops sending error notifications. To check a pipe’s status with [SYSTEM$PIPE\_STATUS](/sql-reference/functions/system_pipe_status) or in Snowsight, a role needs the `MONITOR` or `OWNERSHIP` privilege on the pipe, or the `MONITOR EXECUTION` privilege on the account.

To call the Snowpipe REST API, a role needs the `USAGE` privilege on the database and schema that contain the pipe, the `OPERATE` privilege on the pipe for the `insertFiles` endpoint, and either the `MONITOR` privilege on the pipe or the `MONITOR EXECUTION` privilege on the account for the `insertReport` and `loadHistoryScan` endpoints. The role doesn’t need privileges on the stage or the target table, because Snowpipe loads files with the privileges of the role that owns the pipe. To grant or revoke these privileges, use [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) and [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege).

## Snowpipe with Iceberg tables

Snowpipe loads files into [Iceberg tables](/user-guide/tables-iceberg) with the same pipe syntax that it uses for standard tables. It supports Iceberg v2 and [Iceberg v3](/user-guide/tables-iceberg-v3-specification-support) tables of the following types:

- **Snowflake-managed Iceberg tables**, which use Snowflake as the catalog. Snowpipe loads them with either [load mode](#label-snowpipe-intro-iceberg-load-modes).
- **Externally managed Iceberg tables**, which use an external Iceberg REST catalog that Snowflake can [write to](/user-guide/tables-iceberg-externally-managed-writes). Snowpipe loads them only with `FULL_INGEST` and commits each load to the external catalog. If you specify `LOAD_MODE = ADD_FILES_COPY` for these tables, `CREATE PIPE` fails.

If another engine changes an externally managed table while Snowpipe is committing a load, Snowpipe retries the commit. If the commit still fails, Snowpipe doesn’t record the files as loaded and tries to load them again later.

### Load modes for Iceberg tables

The `LOAD_MODE` copy option controls how Snowpipe writes the data. The following table shows each load mode, the source files and Iceberg tables that it supports, and what it does:

| Load mode | Source files | Supported Iceberg tables | What it does |
| --- | --- | --- | --- |
| `FULL_INGEST` (default) | CSV, JSON, Avro, ORC, Parquet, or XML | Snowflake-managed and externally managed, including partitioned tables. Snowpipe support for partitioned tables is in public preview. | Reads the files and writes the data as new Parquet data files in the table’s location. Supports transformations during the load. |
| `ADD_FILES_COPY` | Iceberg-compatible Parquet only | Snowflake-managed tables that aren’t partitioned | Copies the files into the table’s base location and adds them to the table’s metadata without rewriting them. Requires `MATCH_BY_COLUMN_NAME = CASE_SENSITIVE` and `FILE_FORMAT = (TYPE = PARQUET USE_VECTORIZED_SCANNER = TRUE)`. Doesn’t support transformations, `ON_ERROR = CONTINUE`, or the `SKIP_FILE_<num>` or `'SKIP_FILE_<num>%'` options. |

Expand

Show lessSee more

To register Iceberg-compatible Parquet files without rewriting them, create the table with quoted column names that match the Parquet column names exactly, including case. For all of the requirements, see the [usage notes for loading Iceberg-compatible Parquet files](/sql-reference/sql/copy-into-table#label-copy-into-table-usage-notes-iceberg-parquet). The following example creates a pipe that registers Iceberg-compatible Parquet files with a Snowflake-managed Iceberg table as the files arrive:

Copy code

```
CREATE PIPE mydb.myschema.events_iceberg_pipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO mydb.myschema.events_iceberg
    FROM @mydb.myschema.events_parquet_stage
    FILE_FORMAT = (TYPE = PARQUET USE_VECTORIZED_SCANNER = TRUE)
    MATCH_BY_COLUMN_NAME = CASE_SENSITIVE
    LOAD_MODE = ADD_FILES_COPY;
```

If your Parquet files don’t meet these requirements, omit `LOAD_MODE` so that the pipe uses `FULL_INGEST`.

When you use `ADD_FILES_COPY`, keep the following in mind:

- Pipes don’t support the `PURGE` copy option, so Snowpipe doesn’t delete the source files after it copies them into the table’s base location. To avoid storing the data twice, delete the source files after they load. For more information, see [Delete files after Snowpipe loads them](/user-guide/data-load-snowpipe-manage#label-snowpipe-delete-data-files).
- Don’t use `ADD_FILES_COPY` to register Parquet files that already belong to another Iceberg table. To convert an externally managed Iceberg table to a Snowflake-managed table without rewriting its files, see [ALTER ICEBERG TABLE … CONVERT TO MANAGED](/sql-reference/sql/alter-iceberg-table-convert-to-managed).

### Partitioned Iceberg tables

Both Snowflake-managed and externally managed Iceberg tables can be partitioned. Snowpipe support for partitioned Iceberg tables is in public preview. For the features that Snowflake supports for each type of partitioned table, see the partitioning support matrix in [Iceberg partitioning](/user-guide/tables-iceberg-metadata#label-tables-iceberg-partitioning).

You don’t need to change the pipe to load a partitioned table. Snowpipe writes the rows from each file into data files according to the table’s partition specification and path layout. To partition a table that you create in Snowflake, include a `PARTITION BY` clause. An externally managed table that another engine already partitioned needs no changes. For the partition transforms that you can use, see the partition expression parameters for [CREATE ICEBERG TABLE (Snowflake as the Iceberg catalog)](/sql-reference/sql/create-iceberg-table-snowflake#label-create-iceberg-table-snowflake-partitionexpressions) or [CREATE ICEBERG TABLE (Iceberg REST catalog)](/sql-reference/sql/create-iceberg-table-rest#label-create-iceberg-table-rest-partitionexpressions). For example, the following statements create a Snowflake-managed Iceberg table that’s partitioned by day and region, and a pipe that loads JSON files into it:

Copy code

```
CREATE ICEBERG TABLE mydb.myschema.events_by_day (
  event_id STRING,
  event_time TIMESTAMP_NTZ(6),
  region STRING,
  payload STRING
)
  PARTITION BY (DAY(event_time), region)
  EXTERNAL_VOLUME = 'my_ext_vol'
  CATALOG = 'SNOWFLAKE'
  BASE_LOCATION = 'events_by_day';

CREATE PIPE mydb.myschema.events_by_day_pipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO mydb.myschema.events_by_day
    FROM @mydb.myschema.events_stage
    FILE_FORMAT = (TYPE = 'JSON')
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

Keep the following in mind when you load partitioned Iceberg tables:

- Pipes that load partitioned tables use `FULL_INGEST`, which supports transformations and `MATCH_BY_COLUMN_NAME`. `LOAD_MODE = ADD_FILES_COPY` isn’t supported, so `CREATE PIPE` fails if you specify it.
- If Snowflake can’t compute a partition value for a row, for example because a value overflows a `TRUNCATE` transform, the file fails to load, even if the pipe uses `ON_ERROR = CONTINUE`. Other errors, such as type conversion errors, follow the pipe’s `ON_ERROR` setting.
- For a Snowflake-managed table, if you change the table’s partition specification with [ALTER ICEBERG TABLE … ADD | DROP | REPLACE PARTITION BY](/sql-reference/sql/alter-iceberg-table-partition-evolution), the pipe starts writing with the new specification within about 15 minutes. You don’t need to recreate the pipe. For an externally managed table, Snowpipe writes with the partition specification in the latest table metadata that Snowflake has, including changes that another engine makes.
- Each load writes at least one data file for each partition that the load’s rows fall into. To avoid many small data files, choose partition transforms that produce a moderate number of partitions, and follow the [file sizing recommendations](/user-guide/data-load-considerations-prepare#label-snowpipe-file-size).

## Best practices and limitations

Follow these practices to keep pipes efficient and reliable, and keep the following limitations in mind when you design a pipe.

### Best practices

- **Size files for throughput.** Aim for compressed files of roughly 100 to 250 MB. If your source accumulates data slowly, create a new file about once per minute. Staging smaller files more often doesn’t guarantee lower latency. For more information, see [File sizing for Snowpipe](/user-guide/data-load-considerations-prepare#label-snowpipe-file-size).
- **Filter events at the source.** Snowflake recommends that you enable event filtering in your cloud provider so that Snowpipe receives notifications only for the files that it should load. Event filtering reduces event noise and latency. Use the `PATTERN` copy option in the pipe only when your cloud provider’s event filtering isn’t sufficient. For configuration details, see [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-how-to-filtering.html), [Azure Event Grid](https://learn.microsoft.com/en-us/azure/event-grid/event-filtering), and [Google Cloud Pub/Sub](https://cloud.google.com/pubsub/docs/filtering).
- **End stage URLs and pipe paths with a forward slash.** When the stage URL or the [pipe path](#label-snowpipe-intro-how-it-works) doesn’t end with `/`, the path also matches every folder and file whose name starts with the same characters. For example, a pipe path that ends in `orders` also matches the `orders_archive/` folder, so the pipe loads files that you didn’t intend. If another pipe loads that folder too, both pipes load the same files.
- **Track load times with row timestamps.** Don’t record load times with `CURRENT_TIMESTAMP` or similar functions, such as `SYSDATE`, either in a pipe’s `COPY INTO` statement or as a column default, because their values can be a few hours earlier than when the rows are committed. Instead, enable [row timestamps](/user-guide/data-engineering/row-timestamps) on the target table (`ROW_TIMESTAMP = TRUE`) and query the `METADATA$ROW_LAST_COMMIT_TIME` column. Row timestamps aren’t supported for Iceberg tables. For more information, see [Load times recorded with CURRENT\_TIMESTAMP are earlier than expected](/user-guide/data-load-snowpipe-ts#label-load-times-inserted-snowpipe-ts).
- **Set up error notifications.** [Error notifications](/user-guide/data-load-snowpipe-errors) tell you about failed loads without polling. To get a notification for every file that contains an error, keep the default `ON_ERROR = SKIP_FILE` setting. To also get alerts when a pipe stops, or when Snowflake can’t read a pipe’s notification channel (Google Cloud Storage and Microsoft Azure only), see [Get alerted about Snowpipe problems](/user-guide/data-load-snowpipe-monitor-events#label-snowpipe-events-alerts).
- **Plan for region-wide outages.** To keep loading through a region-wide outage, use a failover group to replicate pipes, their target tables, and their load metadata to another account. For more information, see [Stage, pipe, and load history replication](/user-guide/account-replication-stages-pipes-load-history). Failover groups require Business Critical Edition or higher. To switch to a secondary storage location after a failover without reconfiguring every pipe, see [Multi-Location Resilience for Data Pipelines](/user-guide/multi-location-resilience-data-pipelines).

### Limitations

- A pipe’s `COPY INTO` statement can’t use the `FILES` or `VALIDATION_MODE` parameter, or the `FORCE`, `LOAD_UNCERTAIN_FILES`, `ON_ERROR = ABORT_STATEMENT`, `PURGE`, `RETURN_FAILED_ONLY`, or `SIZE_LIMIT` copy option.
- [ALTER PIPE … REFRESH](/sql-reference/sql/alter-pipe) queues only files that were staged within the last 7 days. To load older files, see [Files staged more than 7 days ago](/user-guide/data-load-snowpipe-manage#label-snowpipe-manage-backfill).
- Snowpipe doesn’t load files from user stages or temporary stages.
- Snowpipe ignores a staged file whose path and name match a file that the pipe processed in the last 14 days, even if the file changed or failed to load. For more information, see [Load metadata](#label-snowpipe-intro-load-metadata).
- While a pipe is paused, files stay in its queue for up to 14 days. A pipe that stays paused longer becomes stale. For more information, see [Resume a stale pipe](/user-guide/data-load-snowpipe-manage#label-snowpipe-resume-stale-pipe).
- Snowpipe doesn’t guarantee load latency or the order in which files load.
- Automated loading doesn’t work between government regions and commercial regions. For more information, see [Automated loading doesn’t work across government and commercial regions](/user-guide/data-load-snowpipe-ts#label-snowpipe-ts-gov-regions).

## What’s next

- To set up automated loading, see [Automating Snowpipe for Amazon S3](/user-guide/data-load-snowpipe-auto-s3), [Automating Snowpipe for Google Cloud Storage](/user-guide/data-load-snowpipe-auto-gcs), or [Automating Snowpipe for Microsoft Azure Blob Storage](/user-guide/data-load-snowpipe-auto-azure).
- To load files from your own application, see [Load data with the Snowpipe REST API](/user-guide/data-load-snowpipe-rest-overview).
- To load data into Iceberg tables, see [Load data into Apache Iceberg™ tables](/user-guide/tables-iceberg-load) and, for externally managed tables, [Write support for externally managed Apache Iceberg™ tables](/user-guide/tables-iceberg-externally-managed-writes).
- To pause, resume, or recreate pipes, see [Manage Snowpipe](/user-guide/data-load-snowpipe-manage).
- To monitor pipes and get notified when loads fail, see [Manage Snowpipe in Snowsight](/user-guide/data-load-snowpipe-snowsight), [Snowpipe error notifications](/user-guide/data-load-snowpipe-errors), and [Monitor events for Snowpipe](/user-guide/data-load-snowpipe-monitor-events).
- To protect pipelines against region-wide outages, see [Multi-Location Resilience for Data Pipelines](/user-guide/multi-location-resilience-data-pipelines).
- To understand and monitor costs, see [Snowpipe costs](/user-guide/data-load-snowpipe-billing).
- To resolve load problems, such as missing files or duplicate data, see [Troubleshooting Snowpipe](/user-guide/data-load-snowpipe-ts).
- For hands-on walkthroughs, see the [Getting Started with Snowpipe](https://www.snowflake.com/en/developers/guides/getting-started-with-snowpipe/) and [AWS CloudTrail Ingestion](https://www.snowflake.com/en/developers/guides/cloudtrail-log-ingestion/) guides.
- If you can’t resolve an issue, contact [Snowflake Support](/user-guide/contacting-support).
