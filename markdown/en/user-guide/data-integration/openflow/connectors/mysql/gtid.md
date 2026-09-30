# Openflow Connector for MySQL: GTID-based replication

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Important

GTID tracking is available for the gen 1 Openflow Connector for MySQL only. It isn’t available for gen 2 connectors:
you turn GTID tracking on by setting a processor property, and the runtime canvas is read-only for
gen 2 connectors. For an overview of the two generations, see
[Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations).

By default, the Openflow Connector for MySQL records its place in the CDC stream as a binary log file name and a byte
offset within that file. You can instead have the connector track its position with MySQL
[Global Transaction Identifiers (GTIDs)](https://dev.mysql.com/doc/refman/8.4/en/replication-gtids.html),
which identify each committed transaction independently of the binary log file it was written to.

GTID tracking offers two advantages:

- **Replication survives a source server failover.** A GTID identifies the same transaction on
  every server in a replication topology, so the connector can resume from the transaction where it
  left off even after it reconnects to a different server. Binary log file names and byte offsets
  are meaningful only on the single server that produced them.
- **Large transactions are supported.** With binary log position tracking, a single transaction has
  to fit into a binary log message of no more than 4 GB. GTID tracking identifies transactions
  directly rather than by their offset in a file, so that limit doesn’t apply.

Switching to GTID tracking changes only how the connector records its position in the CDC stream.
It doesn’t change which tables are replicated, how they’re mapped to Snowflake, or the state of any
destination table.

## Prerequisites

GTID tracking has to be enabled on the MySQL server before the connector can use it. Enabling it is
a multi-step procedure, and the order of the steps matters. Follow
[Enabling GTID Transactions Online](https://dev.mysql.com/doc/refman/8.4/en/replication-mode-change-online-enable-gtids.html)
in the MySQL documentation. It doesn’t require taking the server down.

Warning

Once `gtid_mode` is `ON`, the connector can’t replicate a transaction that has no GTID. Before you
switch the connector to GTID tracking, make sure the source no longer retains any binary logs
written before you enabled GTIDs.

Let the connector finish reading those binary logs while it’s still tracking binary log positions,
then wait for the source to purge them. To confirm none are left, see [Check for transactions without GTIDs](#label-mysql-gtid-check-anonymous).

The connector checks `gtid_mode` on the source when it starts, and its behavior depends on whether
it has already recorded a GTID position:

- If `gtid_mode` isn’t `ON` and the connector hasn’t recorded a GTID position yet, it keeps using
  binary log positions and doesn’t switch to GTID tracking. Enable `gtid_mode` on MySQL, then
  restart the connector.
- If `gtid_mode` is turned off after the connector has already recorded a GTID position, the
  connector keeps GTID tracking and replication stops. The connector never falls back to binary log
  positions on its own. To resume replication, turn `gtid_mode` back on. If you need to move the
  connector back to binary log tracking permanently, see [Revert to binary log tracking](#label-mysql-gtid-revert).

### Check for transactions without GTIDs

Ensure *all* binary logs prior to the GTID setting have rolled. You can verify this by inspecting the
oldest transactions retained by your binary logs.

Transactions written before you enabled GTIDs appear in the binary log as `Anonymous_Gtid` events.
They can only precede the first transaction that has a GTID, so the start of the oldest retained
binary log tells you whether any are left:

1. List the binary logs the source still retains. The first row is the oldest file.

   Copy code

   ```
   SHOW BINARY LOGS;
   ```
2. Show the first events in that file, substituting the name from step 1 for `<binary_log_file>`:

   Copy code

   ```
   SHOW BINLOG EVENTS IN '<binary_log_file>' LIMIT 10;
   ```
3. Read the `Event_type` column, past the `Format_desc` and `Previous_gtids` header events:

   - `Anonymous_Gtid` means the source still retains transactions without GTIDs. Don’t switch the
     connector to GTID tracking yet.
   - `Gtid` means every retained transaction has a GTID.

### Replica sources

If the connector reads from a MySQL server that is itself a replica, that replica has to keep
[replica\_preserve\_commit\_order](https://dev.mysql.com/doc/refman/8.4/en/replication-options-replica.html#sysvar_replica_preserve_commit_order)
set to `ON`, which is the default in MySQL 8.4. The setting makes a multithreaded replica commit
transactions in the order they appear in its relay log, which is what the connector relies on. For
why it matters, see [Limitations](#label-mysql-gtid-limitations).

## Limitations

- GTID tracking is available for MySQL sources only. MariaDB sources always use binary log position
  tracking.
- GTID tracking is available for the gen 1 connector only. See the
  [connector generation requirement](/user-guide/data-integration/openflow/connectors/mysql/gtid#label-mysql-gtid-generation) at the top of this page.
- The connector doesn’t support tagged GTIDs, which MySQL 8.3 and later can produce in the form
  `<uuid>:<tag>:1-5`. Don’t assign tags to transactions on a source that the connector replicates.
- The connector doesn’t support out-of-order transactions. When a multithreaded replica runs with
  `replica_preserve_commit_order` set to `OFF`, it can commit transactions in a different order than
  they appear in its relay log, which MySQL calls gaps in the sequence of executed transactions. The
  connector’s GTID position only moves forward, so a transaction that commits behind the position it
  has already reached isn’t replicated. Keep `replica_preserve_commit_order` set to `ON`.
- Migration from binary log positions to GTIDs is automatic, but the reverse isn’t. Returning to
  binary log tracking requires the manual procedure in [Revert to binary log tracking](#label-mysql-gtid-revert).

## Enable GTID-based replication

GTID tracking is controlled by a property on the **Read MySQL CDC Stream** processor rather than by a
parameter in a parameter context, so you set it on the connector canvas:

1. Confirm that `gtid_mode` is `ON` on the source server, and that the source no longer retains
   binary logs containing transactions without GTIDs. See [Prerequisites](#label-mysql-gtid-prerequisites).
2. Navigate to the Openflow canvas.
3. Open the **Incremental Load** process group.
4. Stop the topmost processor named **Read MySQL CDC Stream**. You have to stop a processor before
   you can change its properties.
5. Right-click the processor and select **Configure**.
6. Open the **Properties** tab.
7. Set **Position Tracking Mode** to `GTID Preferred`.
8. Apply the change.
9. Start the processor.

The connector migrates itself from binary log positions to GTIDs. You don’t need to remove tables
from replication, re-snapshot them, or change any other setting.

Warning

Don’t set the `@@GLOBAL.gtid_purged` variable on MySQL manually. The server maintains it as it purges
binary logs, and the connector relies on it to know which transactions the source still retains. A
manually assigned value misrepresents the contents of the binary log, which can lead the connector to
skip transactions that are still available. Those changes never reach Snowflake, and the connector
has no way to detect that they were missed.

## Verify that the migration finished

The connector doesn’t migrate at the moment you apply the property. It waits for a point in the CDC
stream where it can verify that its current position covers everything MySQL has already purged,
which is typically the next binary log file rotation. Until then it keeps replicating with binary log
positions, so a migration that hasn’t completed yet isn’t a sign of a problem.

To check whether the migration finished:

1. Navigate to the Openflow canvas.
2. Open the **Incremental Load** process group.
3. Right-click the topmost processor named **Read MySQL CDC Stream**, then select **View state**.
4. Look at the state entries:

   - The migration has finished when **gtid.position** is present and the **binlog.position.dml**,
     **binlog.position.ddl**, and **binlog.position.start** entries are gone.
   - The migration is still pending while the **binlog.position** entries are present and
     **gtid.position** is absent.

After the migration, the connector rotates the schema generation of every replicated table, so each
table gets a new journal table on its next DDL event. This is expected. For more information about
journal tables, see
[Track data changes in tables](/user-guide/data-integration/openflow/connectors/mysql/about#label-mysql-track-data-changes-in-tables).

## Revert to binary log tracking

Reverting to binary log tracking is a manual procedure. The tables stay in replication
throughout, so you don’t need to remove them, re-add them, or snapshot them again. Clearing the
processor state is what allows the revert, because it removes the GTID position that otherwise keeps
the connector in GTID tracking. That leaves the connector with no position to resume from, so it
replays the retained binary log for the tables still in replication.

Warning

This procedure re-reads the entire available binary log. While that’s in progress, the columns and
data in the affected destination tables can be out of sync with their sources until all events have
been re-processed and merged. For more information, see
[Specify the starting position of the CDC stream](/user-guide/data-integration/openflow/connectors/mysql/maintenance#label-mysql-connector-start-restart-incremental-load-from-earliest-available-binary-log-position).

1. Stop the connector. Right-click the connector’s process group and select **Stop**.
2. Empty every queue in the connector. Right-click each connection that still shows a **Queued**
   count and select **Empty queue**. The **Queued** value on the connector’s process group has to
   reach zero before you continue.
3. Clear the state of the **Read MySQL CDC Stream** processor. Right-click the processor, select
   **View state**, then select **Clear state**. This removes the GTID position that otherwise keeps
   the connector in GTID tracking.
4. In the **MySQL Ingestion Parameters** context, change `Starting Binlog Position` from `Latest` to
   `Earliest`.
5. In the same context, set `Re-read Tables in State` to `Any active`, so that the re-read isn’t
   restricted to newly added tables.
6. Set **Position Tracking Mode** on the **Read MySQL CDC Stream** processor back to
   `Binlog Position`, following the steps in [Enable GTID-based replication](#label-mysql-gtid-enable).
7. Start the connector. Right-click the connector’s process group and select **Start**.
8. Wait until the connector catches up with the binary log. See
   [Check whether the connector caught up](#label-mysql-gtid-revert-catchup).
9. Set `Re-read Tables in State` back to `New`, and `Starting Binlog Position` back to `Latest`.
   Returning the position to `Latest` is also what clears the re-read bookkeeping, so the connector
   can start another re-read later.

### Check whether the connector caught up

Compare the position the connector has reached against the current position on the source:

1. Navigate to the Openflow canvas.
2. Open the **Incremental Load** process group.
3. Right-click the topmost processor named **Read MySQL CDC Stream**, then select **View state**.
4. Note the value of **binlog.position.dml**, which is formatted as
   `<binary-log-file>/<position>`.
5. On the source server, get the current binary log position. The statement depends on the MySQL
   version:

   Copy code

   ```
   SHOW BINARY LOG STATUS;
   ```

   On MySQL 8.0, run `SHOW MASTER STATUS` instead. MySQL 8.4 removed that statement and replaced it
   with `SHOW BINARY LOG STATUS`. Both report a `File` and a `Position`, and both require the
   `REPLICATION CLIENT` privilege that the connector’s user already holds.
6. Compare the two. The connector has caught up once **binlog.position.dml** reaches the file and
   position that the source reports. Because the source keeps committing while the connector reads,
   expect the two to stay close rather than match exactly.
