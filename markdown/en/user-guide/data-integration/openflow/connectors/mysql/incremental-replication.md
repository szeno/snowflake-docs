# Openflow Connector for MySQL: Set up incremental replication without snapshots

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

You can configure the Openflow Connector for MySQL connector to immediately replicate incremental changes for newly added tables, bypassing snapshots. Use incremental load to continue replication without snapshotting every table again when you reinstall the connector over previously replicated data.

To enable incremental replication in a new connector instance:

1. Set up the connector as described in [Set up the Openflow Connector for MySQL](/user-guide/data-integration/openflow/connectors/mysql/setup).
2. In the `MySQL Ingestion Parameters` context, set the `Ingestion Type` parameter to `incremental`.

## Enable incremental replication without snapshots

To enable incremental replication on an existing connector:

1. sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. in the navigation menu, select **Ingestion** » **Openflow**.
3. In the **Openflow** pane select the **Runtimes** tab.
4. Select the runtime containing the connector.
5. Select the connector.
6. In the `Ingestion Parameters` context, specify `Ingestion Type` = `incremental`.
7. Add new replication tables. These tables immediately switch to their incremental load.

Note

To return to replicating tables with the snapshot load, change **Ingestion Type** from `incremental` to `full`.

# Usage notes

- Changing the value of **Ingestion Type** does not impact any tables that have begun replicating data.
  Tables currently in the snapshot phase continue until the snapshot load is complete.
- While **Ingestion Type** is set to `incremental`, new tables added to the list of replicated tables bypass the snapshot phase.
  This includes new tables added to the source database that match the `Included Table Regex` parameter.
  Ensure that the ingestion type is set to `incremental` to bypass the snapshot phase.

  Note

  Connectors should only remain in `incremental` mode as long as required as it bypasses snapshots.
  Once customer needs for incremental updates have been satisfied the connector should be returned to `full` mode.
- For tables that bypass snapshot load, the connector creates a destination table in Snowflake,
  by executing `CREATE TABLE IF NOT EXISTS`, only if no destination table already exists.
  Tables going through the snapshot require that no destination table exist.

## Recover a table using incremental-only mode

If a table’s snapshot completed successfully but incremental replication later failed, you don’t need to remove the table and snapshot it again. Instead, you can recover the table by replaying the changes that are still available in the source binary logs (binlog) and merging them onto the existing destination table.

Incremental replication can fail for several reasons, for example:

- A record in the source database can’t be read because it has an incorrect or unsupported format.
- A row exceeds the maximum supported size.
- A merge operation can’t complete.
- A transient error persists through so many retries that the table enters the FAILED state.

To recover the table without a new snapshot, remove it from replication, switch the connector to incremental-only mode reading from the earliest available position, and add the table back. The connector reads all available changes from the oldest available binary log position, then replays and reapplies them to the destination table.

Important

Before you recover the table, address the underlying cause of the failure. Otherwise, the connector encounters the same error again when it replays the changes. For example, raise the per-value limit (see [Increase the oversized value limit](/user-guide/data-integration/openflow/connectors/mysql/maintenance#label-of-mysql-increase-oversized-value-limit)) or fix the problematic record in the source database.

To recover the table:

1. Remove the table from replication. In the `Ingestion Parameters` context, remove the table from **Included Table Names**, or modify **Included Table Regex** so the table is no longer matched. Wait until the table’s state is fully removed from the **Table State Store** controller service before you continue.

   Important

   Don’t drop the destination table. This procedure reuses the existing destination table and replays incremental changes onto it.
2. Stop the connector’s process group so that you can change its configuration. On the connector canvas, right-click the connector’s process group and select **Stop**.
3. In the `Ingestion Parameters` context, set the `Ingestion Type` parameter to `incremental`.
4. Set the `Starting Binlog Position` parameter to `Earliest`. The connector reads all available changes again from the oldest available binary log position, then replays and reapplies them to the destination table. For more information, see [Specify load from binary log position](/user-guide/data-integration/openflow/connectors/mysql/maintenance#label-mysql-connector-start-restart-incremental-load-from-earliest-available-binary-log-position).

   Leave `Re-read Tables in State` at its default value, `New`, so that only the table you add back reads from the earliest position. Tables already in replication continue from their last positions.
5. Add the table back to replication by reversing the change you made in step 1.
6. Start the connector’s process group. Right-click the connector’s process group and select **Start**.
7. Wait until the table returns to incremental replication. In the **Table State Store** controller service state, the table transitions to INCREMENTAL\_REPLICATION when recovery completes.
8. Revert the changes you made in steps 3 and 4: set `Ingestion Type` and `Starting Binlog Position` back to their previous values.

Warning

This procedure recovers only the changes still retained in the source binary logs. If the binary log retention period expired and some changes were purged, the recovered table can have gaps. In that case, you must take a new snapshot to fully resynchronize the table.
