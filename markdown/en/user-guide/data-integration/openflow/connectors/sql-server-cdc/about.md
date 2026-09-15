# About Openflow Connector for SQL Server (CDC)

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes the basic concepts, workflow, and limitations of the Openflow Connector for SQL Server (CDC).

## About the Openflow Connector for SQL Server (CDC)

The Openflow Connector for SQL Server (CDC) connects a SQL Server database instance to Snowflake and replicates data from selected tables in near real-time or on a schedule.
The connector uses SQL Server
[Change Data Capture](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-data-capture-sql-server)
(CDC) to detect and apply changes to replicated tables. Change data is recorded in change tables alongside the
current state of the replicated tables.

## Use cases

Use this connector if you’re looking to do the following:

- Synchronize SQL Server data with Snowflake for comprehensive, centralized reporting.
- Capture every individual row-level change from the source database, including intermediate states between polling intervals.

## Supported SQL Server versions

The following SQL Server database versions and platforms are supported:

- Microsoft SQL Server 2025
- [Microsoft SQL Server 2022](https://www.microsoft.com/sql-server)
- Microsoft SQL Server 2019
- Microsoft SQL Server 2017
- Microsoft SQL Server 2016 (SP1 or later, Enterprise / Standard / Developer edition)
- [Azure SQL Database](https://learn.microsoft.com/azure/azure-sql/database/?view=azuresql)
- [Azure SQL Managed Instance](https://learn.microsoft.com/azure/azure-sql/managed-instance/?view=azuresql)
- [AWS RDS for SQL Server](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_SQLServer.html)
- Google Cloud SQL for SQL Server

Note

The connector requires SQL Server Change Data Capture to be enabled on the source databases
and tables. CDC isn’t available on SQL Server Express or SQL Server Web editions (including
the Web edition on AWS RDS). SQL Server 2017 and later support CDC on the Enterprise,
Standard, and Developer editions. On SQL Server 2016, CDC on the Standard edition requires
SP1 or later; builds before 2016 SP1 require the Enterprise or Developer edition.

## Openflow requirements

- Choose the runtime size based on the sustained replication workload. For sizing guidance and how to run multiple connectors on one runtime, see [Runtime sizing](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup#label-sql-server-cdc-runtime-sizing).
- The connector doesn’t support multi-node Openflow runtimes. Configure the runtime for this connector
  with **Min nodes** and **Max nodes** set to `1`.

## Limitations

- The connector supports only username and password authentication with SQL Server.
- Each replicated table must have a primary key, a qualifying unique constraint, a qualifying
  unique index, or a user-declared logical key. For more information, see
  [How the connector chooses a replication key](#label-sqlserver-cdc-replication-key-selection).
- The connector doesn’t update existing records in the Snowflake database when a new NOT NULL column with
  a default value is added to one of the source databases.
- The connector doesn’t update existing records in the Snowflake database when a new column is added to
  the included list in the Column Filter JSON.
- The connector supports common source table schema changes during replication, such as adding and dropping columns. See [Schema changes](#label-sql-server-cdc-schema-changes) for the full list and a few unsupported change types.
- The connector doesn’t detect at runtime when you drop or modify the primary key, unique constraint,
  or unique index that it uses as the replication key, or when you alter or drop a logical-key column
  after the CDC capture instance exists. After any such change, restart replication for the affected
  table: see [Restart table replication](/user-guide/data-integration/openflow/connectors/sql-server-cdc/maintenance#label-of-sql-server-cdc-restart-table-replication).
- When a new column is added to a source table and an update changes only that newly added column,
  SQL Server Change Data Capture doesn’t record those updates in the change table, so
  the connector can’t replicate them as individual change events. This is a SQL Server CDC
  limitation: a change is captured only when an update modifies at least one column that the table’s
  capture instance already tracks. The connector still reflects the latest value of the new column in
  the destination table after the connector switches to the new capture instance.
- The connector doesn’t support the truncate table operation. `TRUNCATE` statements on the source are ignored, and the corresponding row deletions are not applied to the destination table.

Note

You can bypass limitations affecting certain table columns by excluding these specific columns from replication.

## Workflow

The following workflow outlines the steps to set up and run the Openflow Connector for SQL Server (CDC):

1. A SQL Server database administrator performs the following tasks:

   1. Enables Change Data Capture on each database using `sys.sp_cdc_enable_db`, then creates a
      capture instance for each table to be replicated using `sys.sp_cdc_enable_table`.
   2. Creates credentials for the connector.
   3. Deploys the Openflow CDC wrapper procedures so the connector can rotate capture instances during supported schema changes. If permissions or internal policy blocks deployment, see [When the wrapper procedures aren’t deployed](#label-sql-server-cdc-wrapper-procedures-missing).
   4. (Optional) Provides the SSL certificate to connect to the SQL Server instance over SSL.
2. A Snowflake account administrator performs the following tasks:

   1. Creates a service user for the connector, a destination database to store replicated data,
      and a warehouse for the connector.
   2. Installs the connector.
   3. Specifies the required parameters for the connector flow definition.
   4. Runs the flow.

The connector does the following when run in Openflow:

1. Creates the schemas and destination tables matching the source tables configured for replication.
2. Begins replication according to the table replication lifecycle.

   For more information, see [How tables are replicated](#label-of-sql-server-cdc-how-tables-are-replicated).

## How the connector works

The following sections describe how the connector works in various scenarios, including replication, snapshots of partitioned tables, changes in schema, and data retention.

### Change Data Capture behavior

The connector uses SQL Server
[Change Data Capture](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-data-capture-sql-server)
(CDC) to detect changes in the source tables. CDC captures row-level insert, update, and delete
activity from the SQL Server transaction log into dedicated change tables.

Because CDC preserves every individual change, the connector is suitable for both
**data synchronization** use cases and **audit or history** use cases where every change to
a row must be captured. For a comparison with the Openflow Connector for SQL Server, which uses Change Tracking
instead, see [Comparison of Openflow connectors for SQL Server](/user-guide/data-integration/openflow/connectors/sql-server-cdc/compare-change-tracking-cdc).

### Data replication

The connector supports replicating tables from multiple SQL Server databases in a single SQL Server instance. The connector creates replicated tables from different databases in separate schemas in the destination Snowflake database.

Reference replicated tables by combining the source database name, the source schema name, and the
table name in the following format:

`<database_name>.<schema_name>.<table_name>`

For each schema in each source database being replicated, the connector creates a separate schema in the destination Snowflake database.
The name of the destination schema is a combination of the source database name and the source schema name, separated by an underscore character (`_`) as shown in the following example:

`<source_database_name>_<source_schema_name>`

The connector creates tables in the destination schema with the same name as the source table name as shown in the following example:

`<destination_database>.<destination_schema_name>.<source_table_name>`

### How tables are replicated

The connector replicates tables in the following stages:

1. Schema introspection: The connector discovers the columns in the source table, including the column
   names and types, then validates them against Snowflake’s and the connector’s limitations. Validation
   failures cause this stage to fail, and the cycle completes. After successful completion of this stage,
   the connector creates an empty destination table.
2. Snapshot load: The connector copies all data available in the source table into the destination table.
   If this stage fails, the connector stops replicating data. After successful completion, the data from the
   source table is available in the destination table. For how large partitioned tables are handled, see
   [Snapshot of partitioned tables](#label-sql-server-cdc-partitioned-snapshot).
3. Incremental load: The connector reads new entries from the CDC change tables and applies those changes to the
   destination table. This process continues until the table is removed from replication. Failure at this
   stage stops replication of the source table until the issue is resolved.

For information on bypassing snapshot load and using the incremental load process, see [Incremental replication](/user-guide/data-integration/openflow/connectors/sql-server-cdc/incremental-replication).

### Snapshot of partitioned tables

During snapshot load, the connector pages through each source table in primary key order. For a large table that is [physically partitioned](https://learn.microsoft.com/en-us/sql/relational-databases/partitions/partitioned-tables-and-indexes) on the source, this ordering can force SQL Server to sort the whole table on every batch when no index delivers rows in the required order, which makes the snapshot extremely slow or prevents it from completing.

To avoid this, the connector snapshots a physically partitioned table one partition at a time. Reading a single partition lets SQL Server stream rows in index order without a sort, so each batch finishes quickly. This behavior is automatic: the connector detects partitioned tables and requires no configuration change. Non-partitioned tables are unaffected and continue to be read as a whole. This per-partition optimization applies only to the snapshot phase. Incremental load reads from the CDC change tables and isn’t affected.

### How the connector chooses a replication key

The connector uses one column or set of columns from each source table as the
replication key. The replication key uniquely identifies a row, drives the MERGE
operation that applies CDC changes to the destination, and orders rows during the
snapshot load.

For each table, the connector resolves the replication key in this order:

1. **User-declared logical key.** If the connector’s **Table Key Configuration JSON**
   parameter lists the table, the connector uses those columns as the
   replication key, overriding any primary key, unique constraint, or unique index on the table.
   For more information, see [Specify a logical key for a table](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup#label-sqlserver-cdc-logical-key).
2. **Primary key.** The columns of the table’s enabled primary key constraint.
3. **Unique constraint or unique index.** If the table has no primary key, the
   connector looks for a qualifying unique constraint or unique index, as described
   in [Qualifying unique constraints and unique indexes](#label-sqlserver-cdc-replication-key-uk-criteria).
4. **None.** If no qualifying key is found, the connector can’t replicate the
   table. To resolve this, either add a primary key to the table, modify an existing
   constraint or index so it qualifies (see the following criteria), or declare a logical
   key on columns that uniquely identify rows.

#### Qualifying unique constraints and unique indexes

The connector evaluates a unique constraint or unique index as a candidate replication key only when:

- It’s unique and isn’t the primary key.
- It’s enabled (not disabled).
- It’s a standard B-tree index. Filtered indexes (those with a `WHERE` clause) are excluded.
- All columns covered by the constraint or index are `NOT NULL`.

Note

SQL Server `text`, `image`, and `varbinary(max)` columns can’t appear in unique constraints
or unique indexes, so they never qualify as replication-key columns.

#### Tiebreakers

When more than one candidate qualifies, the connector picks one deterministically using
the following preferences, in order:

1. Among all candidates, a unique constraint is preferred over a unique index.
2. Among candidates of the same type, the candidate with the fewest columns is preferred.
3. Among candidates with the same column count, the candidate with the most numeric
   columns is preferred. The connector counts the following SQL Server types as numeric:
   `INT`, `BIGINT`, `SMALLINT`, `TINYINT`, `DECIMAL`, `NUMERIC`, `MONEY`, `SMALLMONEY`,
   `FLOAT`, `REAL`.
4. If a tie remains, the candidate with the lowest constraint or index name in
   alphabetical order is selected.

If you want a specific column set used regardless of the tiebreaker outcome, declare it
as a logical key. For more information, see
[Specify a logical key for a table](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup#label-sqlserver-cdc-logical-key).

#### Replication key example

The following table has no primary key but has a unique constraint on a `NOT NULL`
column. The constraint qualifies, and the connector replicates the table using the
constraint as the replication key:

Copy code

```
CREATE TABLE customers (
    email      NVARCHAR(255) NOT NULL,
    name       NVARCHAR(100),
    created_at DATETIME2 DEFAULT SYSUTCDATETIME(),
    CONSTRAINT uq_customers_email UNIQUE (email)
);
```

### Schema changes

During incremental replication, the connector detects many source table schema changes and applies them automatically through SQL Server capture instance rotation, without stopping replication or requiring a manual re-snapshot of the table. Unsupported changes stop replication for the affected table until you restart it. To manage capture instances, the connector uses the wrapper procedures deployed during setup. For more information, see [Deploy the Openflow CDC wrapper procedures](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup#label-sql-server-cdc-wrapper-procedures).

#### Supported changes

The connector supports the following schema changes:

- **Add column.** The connector adds the column to the destination table and replicates values for new and updated rows. Existing rows aren’t backfilled; the new column is NULL for rows that existed before the change.
- **Drop column.** The connector renames the destination column with a `__SNOWFLAKE_DELETED` suffix to preserve historical values. For details, see [Dropped columns](#dropped-columns).
- **Compatible type change.** The connector transitions to a new capture instance that reflects the updated column definition when you change a column to a source type that maps to the same Snowflake data type (for example, `INT` to `BIGINT`, both mapped to `NUMBER`).
- **Re-add a previously dropped column.** The connector adds the column as a new destination column alongside the existing soft-deleted column (for example, `A` and `A__SNOWFLAKE_DELETED`).
- **Numeric precision or scale change.** For example, widening `DECIMAL(7,2)` to `DECIMAL(12,4)`. The connector transitions to a new capture instance that reflects the updated column definition.
- **Character column length change.** The connector transitions to a new capture instance that reflects the updated column definition; for example, widening `VARCHAR(50)` to `VARCHAR(200)`.

If you drop a column that was previously dropped and soft-deleted, replication for the affected table fails because the soft-deleted column name is already taken.

#### Unsupported changes

The connector doesn’t support the following schema changes. When one occurs, replication stops for the affected table:

- **Primary key definition change.** Adding or removing primary key columns, or changing which columns form the primary key.
- **Incompatible type change.** When the new source type maps to a different Snowflake data type (for example, `INT` to `VARCHAR`, mapped to `NUMBER` and `TEXT` respectively).
- **Rename column.** SQL Server doesn’t allow renaming a column that belongs to an active CDC capture instance. This is a source-side restriction that SQL Server enforces itself, not a limitation of the connector: the rename statement fails on the source database before any change reaches the connector.

#### When the wrapper procedures aren’t deployed

The connector expects `dbo.sf_openflow_cdc_enable_table` and `dbo.sf_openflow_cdc_disable_table` from [Deploy the Openflow CDC wrapper procedures](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup#label-sql-server-cdc-wrapper-procedures). Only use replication without them when permissions or internal policy blocks deployment. Treat that as a last resort, not the normal path. Replication still works until a supported schema change occurs; then a DBA must run manual capture-instance SQL for that change.

Look for a WARN bulletin on the **MultiDatabaseCaptureChangeCdcSqlServer** processor whose message starts with `Schema-change replication` (Openflow bulletins or runtime logs). The bulletin includes the SQL to run. Use that script to unblock the table, or deploy the procedures and grants from [Deploy the Openflow CDC wrapper procedures](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup#label-sql-server-cdc-wrapper-procedures) so later schema changes don’t need manual steps. After the fix, the connector continues on the next run without restarting the flow or re-adding the table.

#### How the schema transition works

A SQL Server capture instance records changes against a fixed set of columns that’s frozen when the
capture instance is created. When the schema of a source table changes, the connector can’t keep
using the same capture instance, so it transitions to a new capture instance that reflects the
updated schema. This transition happens in the following stages:

1. **Schema change detection.** The connector detects DDL changes through a polling mechanism: it
   periodically queries SQL Server’s
   [`cdc.ddl_history`](https://learn.microsoft.com/en-us/sql/relational-databases/system-tables/cdc-ddl-history-transact-sql)
   table for the tables it replicates. The polling interval is configurable and defaults to 30
   seconds, so a schema change is picked up shortly after it occurs rather than in the same cycle.
2. **New capture instance creation.** When the connector detects a schema change, it creates a new
   capture instance that reflects the post-change column set. The new capture instance starts
   recording changes from the point at which it’s created.
3. **Draining the old capture instance.** The connector keeps reading from the old capture instance
   up to the point where the schema changed, so that no change committed under the old schema is
   lost. These changes are emitted using the old column set. All changes committed under the old
   schema are delivered to the destination before any changes recorded under the new schema, so the
   destination always receives changes in schema-consistent commit order.
4. **Mini-snapshot.** A gap exists between the point where the schema changed and the point where
   the new capture instance started recording. To fill this gap, the connector replays the changes in that
   gap from the old capture instance, joining them against the live source table so that newly
   added columns carry their current values. This mini-snapshot brings the destination table up to
   date with the new schema without a full re-snapshot of the whole table.
5. **Switching to the new capture instance.** After the mini-snapshot completes, the connector
   retires (drops) the old capture instance and resumes normal replication from the new one.

#### Replaying already-sent changes

When the connector detects a schema change, it might need to rewind and replay change records that
it already sent. For example, records sent before a new column was detected don’t include a value
for that column, so the connector replays the affected rows to populate the new column. Because the
connector applies changes idempotently by replication key, replaying these records doesn’t create
duplicate rows in the destination table.

#### A schema change during a schema transition

A second schema change can occur while the connector is still transitioning to a new capture
instance because of an earlier change. The connector detects the follow-up change, provisions a
newer capture instance that reflects the latest schema, and continues the transition against that
newer instance, rewinding as needed so the affected changes are replayed under the most recent
schema. No data is lost, and the transition completes against the most recent schema.

### Oversized values

By default, the connector replicates individual values up to **16 MB**. When the connector encounters a larger value, it marks the associated table as permanently failed and stops replicating it. To change how the connector handles oversized values (for example, to replace them with `NULL` instead), modify the **Oversized Value Strategy** destination parameter.

If your Snowflake account has the `ENABLE_OPENFLOW_CDC_BASED_SQLSERVER_SSV2` parameter set to `true`, the per-value limit can be raised from 16 MB to **128 MB**.

For details and instructions on enabling the 128 MB per-value limit, see [Increase the oversized value limit](/user-guide/data-integration/openflow/connectors/sql-server-cdc/maintenance#label-of-sql-server-cdc-increase-oversized-value-limit).

### Always On Availability Groups and source failover

The connector supports SQL Server [Always On Availability Groups](https://learn.microsoft.com/sql/database-engine/availability-groups/windows/overview-of-always-on-availability-groups-sql-server). The connector tolerates planned and unplanned failover without requiring you to restart replication or remove tables from the connector configuration.

During failover, source databases can be briefly offline while SQL Server moves the primary role to another replica. When a source database is temporarily unavailable, replicated tables keep their current status in the Table State Store. The connector retries on the next polling cycle and resumes incremental replication from the last recorded position once the database is online again. Transient connection errors and temporary source unavailability do not move tables to `FAILED`.

Note

This behavior is distinct from permanent failures such as unsupported schema changes or other source-side conditions that permanently stop change capture for a table. Those conditions still move affected tables to `FAILED` until you resolve the underlying problem and restart replication for the table.

For connection settings, see [Always On Availability Groups](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup#label-sql-server-availability-groups).

### Source database locking behavior

During the snapshot phase, the connector reads directly from the source tables to perform the
initial full copy. Under SQL Server’s default READ COMMITTED isolation level, these read
operations acquire shared locks on the source tables, which can lead to deadlocks if other
database clients hold conflicting locks at the same time.

During incremental replication, the connector reads changes from dedicated CDC change tables, not from the
source tables, so it doesn’t take shared locks on the source tables and isn’t subject to the deadlocks
described here.

To avoid deadlocks during the snapshot phase without affecting the isolation level that other applications use,
configure the connector to read under [SNAPSHOT isolation](https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/sql/snapshot-isolation-in-sql-server).
SNAPSHOT isolation reads from row versions instead of acquiring shared locks, so the connector’s snapshot
queries no longer contend with concurrent writes on the source tables.

Because this approach makes SNAPSHOT isolation available only to the connector’s own sessions, it doesn’t
change the default READ COMMITTED isolation level that other applications rely on. Avoid using
Read Committed Snapshot Isolation (RCSI) for this purpose, because RCSI redefines the default isolation level
for every connection to the database.

For the steps to enable SNAPSHOT isolation for the connector, see
[Read the source under SNAPSHOT isolation](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup#label-sql-server-cdc-snapshot-isolation).

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

Review [Set up the Openflow Connector for SQL Server (CDC)](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup) to set up the connector.
