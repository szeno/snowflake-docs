# Comparison of Openflow connectors for SQL Server

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Snowflake provides two Openflow connectors for SQL Server. They differ primarily
in how they detect source changes:

- The Openflow Connector for SQL Server uses SQL Server Change Tracking to identify rows that changed
  between polls.
- The Openflow Connector for SQL Server (CDC) uses SQL Server Change Data Capture to capture every
  row-level change from the transaction log.

## What the connectors have in common

Aside from how they detect source changes, the two connectors share the same
core behavior and requirements:

- Both replicate selected tables from one or more databases in a single SQL
  Server instance into Snowflake, in near real-time or on a schedule.
- Both require a single-node Openflow runtime (set **Min nodes** and **Max nodes**
  to `1`). Size the runtime from the sustained workload. You can run multiple
  connector instances of the same type on one runtime; see
  [Runtime sizing](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup#label-sql-server-cdc-runtime-sizing).
- Both support only username and password authentication with SQL Server.
- Both replicate only tables that have a primary key.

## How change detection differs

Change Tracking reports only the net effect of changes between consecutive polls.
If a row is updated multiple times between two polls, the Openflow Connector for SQL Server sees only
the final state; intermediate states aren’t preserved.

Change Data Capture preserves every individual DML operation. If a row is
updated multiple times between two consecutive polls, the Openflow Connector for SQL Server (CDC) sees
each intermediate state, in commit order.

In practice, this means the Openflow Connector for SQL Server is a good fit for data-synchronization
use cases where only the current row state matters, and the Openflow Connector for SQL Server (CDC) is a
good fit for audit or history use cases where every change must be captured in
addition to keeping the destination synchronized.

## Source database impact

The two SQL Server features are built around different trade-offs, and the
connectors inherit those trade-offs.

The Openflow Connector for SQL Server adds **per-transaction overhead on every DML operation** on a
tracked table:

- Each insert, update, and delete writes a row to SQL Server’s internal
  change-tracking side tables, within the same transaction. Microsoft designs
  this overhead to be low.
- The cost is paid on every DML operation, whether or not the changes are ever
  read.
- On high-DML workloads, especially with wide primary keys or column tracking
  enabled, the overhead can become measurable.
- The connector’s incremental query joins `CHANGETABLE(CHANGES ...)` against
  the source table at each poll, so polling frequency and table activity add to
  source load.

The Openflow Connector for SQL Server (CDC) adds **no cost to DML transactions**, but shifts the cost
elsewhere on the source:

- DML transactions pay no extra write cost, because SQL Server writes the
  transaction log in any case.
- A SQL Server Agent capture job reads the transaction log in the background
  and populates dedicated change tables. The job consumes CPU and I/O on the
  source.
- The connector reads changes from a dedicated change table without taking row
  locks, so replication neither slows down application traffic nor is slowed
  down by it.
- The transaction log can’t be truncated past the capture job’s position. A
  lagging capture job or a long-running transaction can cause the log to grow.

As a rough guide:

- For databases with low-to-moderate DML volumes where simple setup matters,
  the Openflow Connector for SQL Server tends to be the lighter-weight choice.
- For high-volume OLTP workloads, or when keeping replication reads off the
  live source tables matters, the Openflow Connector for SQL Server (CDC) tends to scale better. The
  trade-off is more source-side setup and more attention to transaction log
  retention.

## Supported SQL Server editions and environments

The two SQL Server features have different availability on the source:

- Change Tracking is available on all editions of SQL Server, including
  Express and Web, as well as Azure SQL Database and Azure SQL Managed
  Instance.
- Change Data Capture requires SQL Server Standard or Enterprise edition. It
  isn’t available on SQL Server Express or Web.

For the specific versions and platforms each connector supports, see
[Supported SQL Server versions](/user-guide/data-integration/openflow/connectors/sql-server/about#label-sql-server-versions)
and [Supported SQL Server versions](/user-guide/data-integration/openflow/connectors/sql-server-cdc/about#label-sql-server-cdc-versions).

## Setup complexity

- The Openflow Connector for SQL Server needs one database-level setting (`CHANGE_TRACKING = ON`)
  plus one table-level setting per replicated table. No SQL Server Agent, no
  capture instances.
- The Openflow Connector for SQL Server (CDC) requires SQL Server Agent to be running on the source.
  Each replicated table needs a capture instance, created through
  `sys.sp_cdc_enable_table`. Ongoing replication depends on the capture job
  staying healthy. If replicated tables contain LOB columns with values larger
  than 64 KB, you must also raise the SQL Server `max text repl size` setting
  on the source instance. For configuration steps by
  platform, see [Raise max text repl size for large LOB columns](/user-guide/data-integration/openflow/connectors/sql-server-cdc/setup#label-sql-server-cdc-max-text-repl-size).

## Schema change handling

Both connectors apply supported source-table schema changes during replication,
without a full re-snapshot of the table. Neither connector supports changing the
precision or scale of a numeric column. Changing a table’s primary key while
change detection is enabled is blocked by SQL Server on the source; to move the
connector to a new replication key, restart replication for the affected table.

- The Openflow Connector for SQL Server picks up schema changes on the next poll. It adds new columns
  to the destination table (without backfilling existing rows) and soft-deletes
  dropped columns by renaming them with a `__SNOWFLAKE_DELETED` suffix to
  preserve existing data.
- The Openflow Connector for SQL Server (CDC) applies schema changes automatically by transitioning to a
  new SQL Server capture instance that reflects the updated schema. This relies
  on the Openflow CDC wrapper procedures deployed during setup, which let the
  connector create and drop capture instances without holding elevated
  privileges.

For details, see [Schema changes](/user-guide/data-integration/openflow/connectors/sql-server-cdc/about#label-sql-server-cdc-schema-changes)
and the **Schema changes** section of [About Openflow Connector for SQL Server](/user-guide/data-integration/openflow/connectors/sql-server/about).

## When to choose each connector

Choose the Openflow Connector for SQL Server if you:

- Only need the current row state in the destination, for example for data
  synchronization or centralized reporting.
- Want the simplest source-side setup.
- Run on an edition or platform where Change Data Capture isn’t available.
- Have low-to-moderate DML volumes and want to minimize moving parts on the
  source.

Choose the Openflow Connector for SQL Server (CDC) if you:

- Need every individual row-level change, including intermediate states
  between polls, for audit or history use cases.
- Run a high-volume OLTP source and want replication reads to stay off the
  live tables.
- Can run on SQL Server Standard or Enterprise and can operate the SQL Server
  Agent capture job.
