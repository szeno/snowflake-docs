# About Openflow Connector for SQL Server

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts, workflow, and limitations of the Openflow Connector for SQL Server.

## About the Openflow Connector for SQL Server

The Openflow Connector for SQL Server connects a SQL Server database instance to Snowflake and replicates data from selected tables in near real-time or on a schedule.
The connector uses SQL Server
[Change Tracking](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-tracking-sql-server)
to detect and apply changes to replicated tables. Change data is recorded in journal tables alongside the
current state of the replicated tables.

Snowflake also provides the Openflow Connector for SQL Server (CDC), which uses SQL Server Change Data Capture instead. To choose
between the two connectors, see [Comparison of Openflow connectors for SQL Server](/user-guide/data-integration/openflow/connectors/sql-server-cdc/compare-change-tracking-cdc).

## Use cases

Use this connector if you’re looking to do the following:

- Synchronize SQL Server data with Snowflake for comprehensive, centralized reporting.

## Supported SQL Server versions

The following SQL Server database versions and platforms are supported:

- [Microsoft SQL Server 2022](https://www.microsoft.com/sql-server)
- Microsoft SQL Server 2019
- Microsoft SQL Server 2017
- Microsoft SQL Server 2016
- [Azure SQL Database](https://learn.microsoft.com/azure/azure-sql/database/?view=azuresql)
- [Azure SQL Managed Instance](https://learn.microsoft.com/azure/azure-sql/managed-instance/?view=azuresql)
- [AWS RDS for SQL Server](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_SQLServer.html)
- Google Cloud SQL for SQL Server

Note

The connector relies on SQL Server Change Tracking, which is available starting with SQL Server 2008.
Earlier versions don’t support this feature and are incompatible with the connector.

## Openflow requirements

- Choose the runtime size based on the sustained replication workload. For sizing guidance and how to run multiple connectors on one runtime, see [Runtime sizing](/user-guide/data-integration/openflow/connectors/sql-server/setup#label-sql-server-runtime-sizing).
- The connector doesn’t support multi-node Openflow runtimes. Configure the runtime for this connector
  with **Min nodes** and **Max nodes** set to `1`.

## Limitations

- The connector supports only username and password authentication with SQL Server.
- The connector only replicates database tables that contain primary keys.
- The connector doesn’t update existing records in the Snowflake database when a new NOT NULL column with
  a default value is added to one of the source databases.
- The connector doesn’t update existing records in the Snowflake database when a new column is added to
  the included list in the Column Filter JSON.
- The connector supports common source table schema changes during replication, such as adding, dropping, and renaming columns. See [Schema changes](#label-database-schema-changes) for the full list and a few unsupported change types.
- The connector doesn’t support the truncate table operation. `TRUNCATE` statements on the source are ignored, and the corresponding row deletions are not applied to the destination table.

Note

You can bypass limitations affecting certain table columns by excluding these specific columns from replication.

## Workflow

The following workflow outlines the steps to set up and run the Openflow Connector for SQL Server:

1. A SQL Server database administrator performs the following tasks:

   1. Configures SQL Server replication settings and enables change tracking on the databases and tables
      being replicated.
   2. Creates credentials for the connector.
   3. (Optional) Provides the SSL certificate to connect to the SQL Server instance over SSL.
2. A Snowflake account administrator performs the following tasks:

   1. Creates a service user for the connector, a destination database to store replicated data,
      and a warehouse for the connector.
   2. Installs the connector.
   3. Specifies the required parameters for the connector flow definition.
   4. Runs the flow.

The connector does the following when run in Openflow:

1. Creates the schemas and destination tables matching the source tables configured for replication.
2. Begins replication according to the table replication lifecycle.

   For more information, see [How tables are replicated](#label-of-sql-server-how-tables-are-replicated).

## How the connector works

The following sections describe how the connector works in various scenarios, including replication, snapshots of partitioned tables, changes in schema, and data retention.

### Change tracking behavior

The connector uses SQL Server
[Change Tracking](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-tracking-sql-server)
(CT) to detect changes in the source tables. Change Tracking reports the net effect of changes between
polling intervals. If a row is updated multiple times between two consecutive polls, the connector sees
only the most recent version of that row. Intermediate states aren’t preserved.

This makes the connector suitable for **data synchronization** use cases, where the goal is to keep
the destination table in sync with the source. It isn’t suitable for **audit or history** use cases
where every intermediate change to a row must be captured.

### Data replication

The connector supports replicating tables from multiple SQL Server databases in a single SQL Server instance. The connector creates replicated tables from different databases in separate schemas in the destination Snowflake database.

Reference replicated tables by combining the source database name, the source schema name, and the
table name in the following format:

`<database_name>.<schema_name>.<table_name>`

The name of the destination schema is determined by the `Destination Schema Pattern` parameter. For more information, see [SQLServer Destination Parameters](/user-guide/data-integration/openflow/connectors/sql-server/setup#label-of-sqlserver-destination-parameters). By default, the destination schema name is the source database name and source schema name joined by an underscore, so the fully qualified name of a destination table is:

`<destination_database>.<source_database_name>_<source_schema_name>.<source_table_name>`

### How tables are replicated

The connector replicates tables in the following stages:

1. Schema introspection: The connector discovers the columns in the source table, including the column
   names and types, then validates them against Snowflake’s and the connector’s limitations. Validation
   failures cause this stage to fail, and the cycle completes. After successful completion of this stage,
   the connector creates an empty destination table.
2. Snapshot load: The connector copies all data available in the source table into the destination table.
   If this stage fails, the connector stops replicating data. After successful completion, the data from the
   source table is available in the destination table. For how large partitioned tables are handled, see
   [Snapshot of partitioned tables](#label-sql-server-partitioned-snapshot).
3. Incremental load: The connector tracks changes in the source table and applies those changes to the
   destination table. This process continues until the table is removed from replication. Failure at this
   stage permanently stops replication of the source table, until the issue is resolved.

For information on bypassing snapshot load and using the incremental load process, see [Incremental replication](/user-guide/data-integration/openflow/connectors/sql-server/incremental-replication).

### Snapshot of partitioned tables

During snapshot load, the connector pages through each source table in primary key order. For a large table that is [physically partitioned](https://learn.microsoft.com/en-us/sql/relational-databases/partitions/partitioned-tables-and-indexes) on the source, this ordering can force SQL Server to sort the whole table on every batch when no index delivers rows in the required order, which makes the snapshot extremely slow or prevents it from completing.

To avoid this, the connector snapshots a physically partitioned table one partition at a time. Reading a single partition lets SQL Server stream rows in index order without a sort, so each batch finishes quickly. This behavior is automatic: the connector detects partitioned tables and requires no configuration change. Non-partitioned tables are unaffected and continue to be read as a whole.

### Schema changes

During incremental replication, the connector may detect source table schema changes and update the destination table automatically. For an unsupported change, restart replication for the affected table to recover or to apply the change.

#### Supported changes

The connector supports the following schema changes:

- **Add column.** The connector adds the column to the destination table and replicates values for new and updated rows. Existing rows aren’t backfilled; the new column is NULL for rows that existed before the change.
- **Drop column.** The connector renames the destination column with a `__SNOWFLAKE_DELETED` suffix to preserve historical values. For details, see [Dropped columns](#dropped-columns).
- **Rename column.** The connector treats a rename as dropping the original column and adding a new one. The connector retains the original column under a suffixed name; for example, a column named `A` becomes `A__SNOWFLAKE_DELETED`. For query patterns, see [Renamed columns](#renamed-columns).
- **Compatible type change.** The connector keeps replication running with the destination column type unchanged when you change a column to a source type that maps to the same Snowflake data type (for example, `INT` to `BIGINT`, both mapped to `NUMBER`).
- **Re-add a previously dropped column.** The connector adds the column as a new destination column alongside the existing soft-deleted column (for example, `A` and `A__SNOWFLAKE_DELETED`).

If you drop a column that was previously dropped and soft-deleted, replication for the affected table fails because the soft-deleted column name is already taken.

#### Unsupported changes

The connector doesn’t support the following schema changes. Unless noted otherwise, replication stops for the affected table until you restart it:

- **Primary key definition change.** Adding or removing primary key columns, or changing which columns form the primary key. The connector doesn’t detect this change and keeps replicating with the previous key; replication doesn’t stop on its own. Restart replication for the affected table so the connector picks up the new key.
- **Incompatible type change.** When the new source type maps to a different Snowflake data type (for example, `INT` to `VARCHAR`, mapped to `NUMBER` and `TEXT` respectively).
- **Numeric precision or scale change.** For example, changing `NUMERIC(7,2)` to `NUMERIC(6,3)`.
- **Character column length change.** For example, changing `VARCHAR(50)` to `VARCHAR(100)`.

To recover, restart replication for the affected table: see [Restart table replication](/user-guide/data-integration/openflow/connectors/sql-server/maintenance#label-of-sql-server-restart-table-replication).

The same soft-delete mechanism applies when you change a table’s Column Filter JSON. For details, see [Replicate a subset of columns in a table](/user-guide/data-integration/openflow/connectors/sql-server/setup#label-sqlserver-connector-replication-subset-of-columns).

### Oversized values

By default, the connector replicates individual values up to **16 MB**. When the connector encounters a larger value, it marks the associated table as permanently failed and stops replicating it. To change how the connector handles oversized values (for example, to replace them with `NULL` instead), modify the **Oversized Value Strategy** destination parameter.

If your Snowflake account has the `ENABLE_OPENFLOW_CDC_SQLSERVER_SSV2` parameter set to `true`, the per-value limit can be raised from 16 MB to **128 MB**.

For details and instructions on enabling the 128 MB per-value limit, see [Increase the oversized value limit](/user-guide/data-integration/openflow/connectors/sql-server/maintenance#label-of-sql-server-increase-oversized-value-limit).

### Always On Availability Groups and source failover

The connector supports SQL Server [Always On Availability Groups](https://learn.microsoft.com/sql/database-engine/availability-groups/windows/overview-of-always-on-availability-groups-sql-server). The connector tolerates planned and unplanned failover without requiring you to restart replication or remove tables from the connector configuration.

During failover, source databases can be briefly offline while SQL Server moves the primary role to another replica. When a source database is temporarily unavailable, replicated tables keep their current status in the Table State Store. The connector retries on the next polling cycle and resumes incremental replication from the last recorded position once the database is online again. Transient connection errors and temporary source unavailability do not move tables to `FAILED`.

Note

This behavior is distinct from permanent failures such as unsupported schema changes or other source-side conditions that permanently stop change capture for a table. Those conditions still move affected tables to `FAILED` until you resolve the underlying problem and restart replication for the table.

For connection settings, see [Always On Availability Groups](/user-guide/data-integration/openflow/connectors/sql-server/setup#label-sql-server-availability-groups).

### Error handling for invalid rows

An *invalid row* is a row that Snowflake rejects during ingestion because it can’t be written to the destination table, for example a value that can’t be converted to the destination column’s type, or a missing required column. The **Error Handling Strategy** parameter controls what the connector does when it encounters an invalid row:

- **Fail Table** (default): On the first invalid row, the connector marks the table as permanently failed and stops replicating it, preserving strict, all-or-nothing replication. After you fix the source data, resume replication as described in [Restart table replication](/user-guide/data-integration/openflow/connectors/sql-server/maintenance#label-of-sql-server-restart-table-replication).
- **Log Errors and Continue**: The connector keeps replicating the valid rows and records each rejected row, together with its original payload and error details, in the table’s *error table*. The table isn’t marked as failed.

To change the strategy, set the **Error Handling Strategy** parameter. For more information, see [SQLServer Destination Parameters](/user-guide/data-integration/openflow/connectors/sql-server/setup#label-of-sqlserver-destination-parameters).

#### How rejected rows are captured

The connector loads data with Snowpipe Streaming, so error logging behaves exactly as described in [Error logging in Snowpipe Streaming](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables). When you select **Log Errors and Continue**, the connector creates new destination and journal tables with the [`ERROR_LOGGING`](/user-guide/snowpipe-streaming/snowpipe-streaming-error-tables#turn-on-error-logging) property set to `TRUE`, so rejected rows are captured in a dedicated error table instead of aborting the load. The error table stores the original payload sent to Snowflake before any transformation, along with error details.

Query a table’s error table with the `ERROR_TABLE` table function:

Copy code

```
SELECT * FROM ERROR_TABLE(<destination_database>.<schema>.<table>) ORDER BY timestamp;
```

Where a rejected row lands depends on the replication stage:

- **Snapshot load**: The rejected row is written to the destination table’s error table.
- **Incremental (change tracking) load**: The rejected row is written to the journal table’s error table, because changes are first written to the journal table. For more information about journal tables, see .

The connector enables error logging only on tables that it creates after you select **Log Errors and Continue**. To capture rejected rows for tables that were already being replicated, enable error logging on their existing destination and journal tables with the stored procedure in [Enable error logging on an existing schema](/user-guide/data-integration/openflow/connectors/sql-server/maintenance#label-of-sql-server-enable-error-logging-existing-schema).

Note

When the connector encounters invalid rows, it emits a `WARN` log entry that includes the number of rejected rows. Use these entries to monitor rejected-row activity.

#### Consume rejected rows

To process rejected rows programmatically, create a stream on the error table and consume it like any other Snowflake stream. For more information, see [Streams on error tables](/user-guide/data-load-overview#streams-on-error-tables).

### Source database locking behavior

During snapshot and incremental replication, the connector reads from the source database tables to
retrieve row data and track changes.

Under SQL Server’s default READ COMMITTED isolation level, these read operations acquire shared locks on the
source tables. If other database clients hold conflicting locks on the same tables at the same time, this can
lead to deadlocks, where SQL Server terminates one of the conflicting sessions.

To avoid these deadlocks without affecting the isolation level that other applications use, configure the
connector to read under [SNAPSHOT isolation](https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/sql/snapshot-isolation-in-sql-server).
SNAPSHOT isolation reads from row versions instead of acquiring shared locks, so the connector’s queries no
longer contend with concurrent writes on the source tables.

Because this approach makes SNAPSHOT isolation available only to the connector’s own sessions, it doesn’t
change the default READ COMMITTED isolation level that other applications rely on. Avoid using
Read Committed Snapshot Isolation (RCSI) for this purpose, because RCSI redefines the default isolation level
for every connection to the database.

For the steps to enable SNAPSHOT isolation for the connector, see
[Read the source under SNAPSHOT isolation](/user-guide/data-integration/openflow/connectors/sql-server/setup#label-sql-server-snapshot-isolation).

# Understanding data retention

The connector follows a data retention philosophy where customer data is never automatically deleted.
You maintain full ownership and control over your replicated data, and the connector preserves historical
information rather than permanently removing it.

This approach has the following implications:

- Rows deleted from the source table are soft-deleted in the destination table rather than physically removed.
- Columns dropped from the source table are renamed in the destination table rather than dropped.
- Journal tables are retained indefinitely and are not automatically cleaned up.

## Destination table metadata columns

Each destination table includes the following metadata columns that track replication information:

| Column name | Type | Description |
| --- | --- | --- |
| `_SNOWFLAKE_INSERTED_AT` | TIMESTAMP\_NTZ | The timestamp when the row was originally inserted into the destination table. |
| `_SNOWFLAKE_UPDATED_AT` | TIMESTAMP\_NTZ | The timestamp when the row was last updated in the destination table. |
| `_SNOWFLAKE_DELETED` | BOOLEAN | Indicates whether the row was deleted from the source table. When `true`, the row has been soft-deleted and no longer exists in the source. |

Expand

Show lessSee more

## Soft-deleted rows

When a row is deleted from the source table, the connector does not physically remove it from the
destination table. Instead, the row is marked as deleted by setting the `_SNOWFLAKE_DELETED` metadata
column to `true`.

This approach allows you to:

- Retain historical data for auditing or compliance purposes.
- Query deleted records when needed.
- Decide when and how to permanently remove data based on your requirements.

To query only active (non-deleted) rows, filter on the `_SNOWFLAKE_DELETED` column:

Copy code

```
SELECT * FROM my_table WHERE _SNOWFLAKE_DELETED = FALSE;
```

To query deleted rows:

Copy code

```
SELECT * FROM my_table WHERE _SNOWFLAKE_DELETED = TRUE;
```

## Dropped columns

When a column is dropped from the source table, the connector does not drop the corresponding column
from the destination table. Instead, the column is renamed by appending the `__SNOWFLAKE_DELETED` suffix
to preserve historical values.

For example, if a column named `EMAIL` is dropped from the source table, it is renamed to
`EMAIL__SNOWFLAKE_DELETED` in the destination table. Rows that existed before the column was dropped
retain their original values, while rows added after the drop have `NULL` in this column.

You can still query historical values from the renamed column:

Copy code

```
SELECT EMAIL__SNOWFLAKE_DELETED FROM my_table;
```

## Renamed columns

Due to limitations in CDC (Change Data Capture) mechanisms, the connector cannot distinguish between
a column being renamed and a column being dropped followed by a new column being added. As a result,
when you rename a column in the source table, the connector treats this as two separate operations:
dropping the original column and adding a new column with the new name.

For example, if you rename a column from `A` to `B` in the source table, the destination table
will contain:

- `A__SNOWFLAKE_DELETED`: Contains values from before the rename. Rows added after the rename have
  `NULL` in this column.
- `B`: Contains values from after the rename. Rows that existed before the rename have `NULL`
  in this column.

### Querying renamed columns

To retrieve data from both the original and renamed columns as a single unified column, use a
`COALESCE` or `CASE` expression:

Copy code

```
SELECT
    COALESCE(B, A__SNOWFLAKE_DELETED) AS A_RENAMED_TO_B
FROM my_table;
```

Alternatively, using a `CASE` expression:

Copy code

```
SELECT
    CASE
        WHEN B IS NOT NULL THEN B
        ELSE A__SNOWFLAKE_DELETED
    END AS A_RENAMED_TO_B
FROM my_table;
```

### Creating a view for renamed columns

Rather than manually modifying the destination table, you can create a view that presents the renamed
column as a single unified column. This approach is recommended because it preserves the original data
and avoids potential issues with ongoing replication.

Copy code

```
CREATE VIEW my_table_unified AS
SELECT
    *,
    COALESCE(B, A__SNOWFLAKE_DELETED) AS A_RENAMED_TO_B
FROM my_table;
```

Important

Manually modifying the destination table structure (such as dropping or renaming columns) is not
recommended, as it may interfere with ongoing replication and cause data inconsistencies.

## Journal tables

During incremental replication, changes from the source database are first written to journal tables
before being merged into the destination tables. The connector does not automatically remove data from
journal tables, as this data may be useful for auditing, debugging, or reprocessing purposes.

Journal tables are created in the same schema as their corresponding destination tables and follow
this naming convention:

`<TABLE_NAME>_JOURNAL_<timestamp>_<number>`

Where:

- `<TABLE_NAME>` is the name of the destination table.
- `<timestamp>` is the creation timestamp in Unix epoch format (seconds since January 1, 1970),
  ensuring uniqueness.
- `<number>` starts at 1 and increments whenever the destination table schema changes, either due to
  schema changes in the source table or modifications to column filters.

For example, if your destination table is `SALES.ORDERS`, the journal table might be named
`SALES.ORDERS_JOURNAL_1705320000_1`.

Important

Do not drop journal tables while replication is in progress. Removing an active journal table may
cause data loss or replication failures. Only drop journal tables after the corresponding source
table has been fully removed from replication.

### Managing journal table storage

If you need to manage storage costs by removing old journal data, you can create a Snowflake task
that periodically cleans up journal tables for tables that are no longer being replicated.

Before implementing journal cleanup, verify that:

- The corresponding source tables have been fully removed from replication.
- You no longer need the journal data for auditing or processing purposes.

For information on creating and managing tasks for automated cleanup, see
[Introduction to tasks](/user-guide/tasks-intro).

## Next steps

Review [Openflow connectors for SQL Server: Data mapping](/user-guide/data-integration/openflow/connectors/sql-server/data-mapping) to understand how the connector maps data types to Snowflake data types.

Review [Set up the Openflow Connector for SQL Server](/user-guide/data-integration/openflow/connectors/sql-server/setup) to set up the connector.
