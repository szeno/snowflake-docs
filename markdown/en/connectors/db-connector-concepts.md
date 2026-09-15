# Database connector concepts

## Connector components

The Snowflake Database connectors consist of a Snowflake Native App, installed from the Marketplace into your Snowflake account,
and an **Agent** application running inside your infrastructure, either on-premise, or in the cloud.

- **Agents** connect directly to your source databases, track updates on tables that you chose to replicate, and upload changes into your Snowflake account.
  Agents requires one-time configuration for connecting to Snowflake and the data sources, and afterwards only upgrading when new versions are released.
  Beyond that, it’s entirely controlled and configured via the Native App.
- **Native Apps** control the process of replicating data. They instruct the agents on which tables to track, receive the changes,
  and merge them into your destination databases. Most of your interaction will be with the Native App. It is upgraded automatically, when a new version becomes available.

This model in which an agent runs locally is necessary so that the connector can securely access source databases in networks that are closed to external connections.

One Agent instance always connects to a single Native App instance, and one Native App always works with one Agent.
If you need to run multiple Agent instances, perhaps to replicate source databases from disconnected networks,
you will need to install and configure multiple instances of the Native App. For assistance, [contact Snowflake Support](/user-guide/contacting-support).

Note

For optimal performance, keep the Agent at the same version as the Native App, and upgrade it regularly.
Currently Snowflake ensures compatibility between all publicly available Agent versions and the Native App.

Internally, the connector relies on an asynchronous, event-driven exchange of commands.
The Native App must also communicate and coordinate with the Agent. This is why you can notice a delay between the execution of a command, and seeing the effect of that command.

## Data sources, tables, journals and destinations

When talking about the data flow through the connector, we distinguish the following stages:

Data Source
:   The database that holds the tables that the connector is replicating. Depending on the database engine,
    this can either be the whole database *server* or one of the databases hosted *inside* the server.

    A single connector instance can replicate from multiple Data Sources, as long as the Agent can directly connect to all of them.

Source Table
:   A specific table in the source database that is tracked by the connector for changes which are then replicated into Snowflake.
    Each Data Source may contain multiple Source Tables that are replicated simultaneously by the same connector instance.

    The immediate parent of the Source Table in the Data Source becomes the schema of the corresponding Destination Table in Snowflake.

Journal
:   A Snowflake table, owned and managed by the connector’s Native App, that receives and stores every change applied to the Source Table:
    inserts, updates, and deletes. It’s a de-facto changelog of the Source Table’s data, and
    its structure reflects how database engines typically broadcast changes to their replicas.

    Every Source Table has a separate Journal table.

Destination Table
:   The Snowflake table in your account where the connector replicates data into.
    There’s a separate Destination Table for every Source Table.
    Its column names reflect the names in the Source Table, and their types are corresponding Snowflake types for the source columns.

    Each Destination Table also includes columns with replication information:
    `_SNOWFLAKE_INSERTED_AT`, `_SNOWFLAKE_UPDATED_AT`, `_SNOWFLAKE_DELETED`,
    holding the timestamps of the original insertion, last update, and deletion of the given row, respectively.

    The Destination Table has change tracking pre-enabled to allow for creating streams. The connector’s Native App keeps the `OWNERSHIP` grant on the table.

## Snapshot and incremental load

Replicating data from a newly added table begins with a **Snapshot Load**.
The Agent performs a single `SELECT <columns>` statement on the source table, t
hen streams all the records into an interim table in Snowflake, and afterwards copies them into the destination table.
This operation can be resource-intensive on the source database, and will typically take a long time for large tables.
You may need to wait until you see first records appear in the destination table.

A Snapshot Load can also be repeated, replacing previously-replicated data, to synchronize the source table with the destination, in the following scenarios:

- When the table’s replication fails permanently, due to unsupported data types, sizes, connector bugs, or other issues.
- When replication was paused, and after resuming, the source database’s changelog no longer contains entries since the last time the table was replicated.

After the initial snapshot is complete, the table’s replication turns to **Incremental Load**.
The Agent tracks the source database’s changelog, and streams these changes into the corresponding journal table,
from where they are later merged into the destination table. This cycle of reading, streaming, and merging can either be performed
continuously, or on a schedule. For more information about these modes,
see [Next steps](/connectors/postgres6/configure-replication#label-postgres-connector-configure-scheduled-replication) and [Next steps](/connectors/postgres6/configure-replication#label-postgres-connector-configure-scheduled-replication).

## Table replication lifecycle

A newly added source table’s replication cycle starts with **Schema Introspection**.
This is where the connector discovers the columns in the source table, their names, types,
then validates them against Snowflake’s and the connector’s limitations. Validation failures will cause this stage to fail,
and the cycle completes. After successful completion of Schema Introspection, the connector creates an empty destination table.

The second stage is **Snapshot Load** where the connector copies all data available in the source table into the destination table.
Failure of this stage will also finish the cycle, and no more data will be replicated. After successful completion,
the whole set of data from the source table will be available in the destination table.

Finally, the table moves on to **Incremental Load**, where the connector keeps tracking changes in the source table, and copying them into the destination table.
This continues until the table is removed from replication. Failure at this stage will permanently stop replication of the source table, until the issue is removed.

For instructions on how to determine which replication phase your tables are currently in, see [Monitoring the Snowflake Connector for MySQL](/connectors/mysql6/monitor) and [Monitoring the Snowflake Connector for PostgreSQL](/connectors/postgres6/monitor).

Note

To resume replication for a failed table, once the issue that caused failure is fixed, remove the table from replication, and then add it again.
For more information, see [Configuring replication for the Snowflake Connector for MySQL](/connectors/mysql6/configure-replication) and [Monitoring the Snowflake Connector for PostgreSQL](/connectors/postgres6/monitor).

## Flow of data from source to destination

The connector moves data differently from the source table into the destination,
depending on whether the its performing a Snapshot or Incremental Load.
For more information see [Snapshot and incremental load](#label-connector-snapshot-incremental-load).

### Snapshot load flow

1. The Agent performs a `SELECT <columns> FROM <source table>` on the source table, and inserts those records,
   using Snowflake’s Snowpipe Streaming, into an interim table called the Snapshot Table, stored inside the connector’s Native App.
2. Once all of the available rows are present in the Snapshot Table, the Native App runs a task that copies them into the
   destination table via `INSERT INTO <destination table> (SELECT <columns> FROM <snapshot table>)`.
3. After all the rows were copied into the destination table, the Snapshot Table is dropped.
   The replicated table is ready to move on to Incremental Load.

### Incremental load flow

1. The source database publishes changes on the source table into its changelog.
   The specific mechanism depends on the type of source database, but generally these list inserts, updates and deletes row by row.
2. The agent reads these changelogs in real time, and inserts these row-by-row changes into the corresponding journal tables.
3. A merge task detects the new entries in the journal in real time, and merges them into the destination table: inserting new records,
   updating or soft-deleting existing records. The merge task also adds timestamps for these changes into columns
   described in [Data sources, tables, journals and destinations](#label-connector-data-sources-tables-journals-destinations).

In Scheduled replication mode, the reading of the source database’s changelog, moving these changes into Snowflake,
and merging them into the source database are *not* performed continuously,
but on a fixed schedule instead. See [Continuous vs. scheduled replication](#label-connector-continuous-scheduled-replication) for details.

## Continuous vs. scheduled replication

The default replication mode for newly added data sources is **Continuous**. In this mode, the connector aims to replicate data changes as quickly as possible.
It’s the optimal mode for data sources that change often, where you need that data to be available in Snowflake at low latencies.

You can change the data source to replicate in **Scheduled** mode, where data is copied from the source and into destination tables in batches,
on a fixed schedule. This is the optimal mode for data sources that change infrequently, or when you intend to reduce credit consumption, and don’t require the data to be available in Snowflake at low latencies.

Note

The replication mode can be set *per data source*, and will uniformly affect all tables configured for that data source. Setting a different mode or schedule per table is not supported.

When running Continuous replication, incremental load will never be reported as “completed”.
In Scheduled mode, incremental load is reported as completed after every batch of data is merged into the destination table.
A “batch” in Scheduled mode consists of all the changelog entries between the previous scheduled run, and the moment the next scheduled run is started.

## Warehouse types

Connectors requires two warehouses to operate:

- An **Operational Warehouse**, sometimes referred to as an Ops Warehouse, is used to execute the connector’s command & control operations.
  This warehouse is automatically created by the setup wizard, and its optimal size is XS.
- A **Compute Warehouse** is used to execute the merge tasks that move data from journals into destination tables.
  This warehouse may be created by the setup wizard, or manually. Its optimal size and type depend on the scale of your replication.

The above distinction is required to ensure that operational queries are executed in a timely fashion,
without being queued together with the queries that move large quantities of data.
This also means that the Operational Warehouse *cannot* be reused between connector instances, and should not be shared with other workloads in the account.

The Compute Warehouse, in turn, *can* be shared with other connector instances, and workloads.
Keep in mind, though, that sharing this warehouse may cause delays in data appearing in your destination tables.

Important

The Operational Warehouse will *never* suspend when working in continuous mode which will cause it to consume credits even if no data is being replicated.
To enable auto-suspend, change the replication mode for *all* data sources to scheduled. See [Continuous vs. scheduled replication](#label-connector-continuous-scheduled-replication) for details.
