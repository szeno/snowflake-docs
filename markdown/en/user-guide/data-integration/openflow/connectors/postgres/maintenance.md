# Openflow Connector for PostgreSQL Maintenance

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes important maintenance considerations and best practices for
maintaining the Openflow Connector for PostgreSQL when making changes to the source PostgreSQL database.
In addition, this topic describes how to restart table replication and reinstall the connector.

## Check the replication status of a table

Interim failures, such as connection errors or temporary source unavailability during a high-availability failover, do not prevent table replication. Replicated tables keep their current status and the connector retries on the next polling cycle. However, permanent failures, such as unsupported data types, prevent table replication.

To troubleshoot replication issues or verify that a table has been successfully removed from the replication flow, check the Table State Store:

1. In the Openflow runtime canvas, right-click a processor group and choose **Controller Services**. A table listing controller services displays.
2. Locate the row labeled **Table State Store**, click the **More** [![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) button on the right side of the row, and then choose **View State**.

A list of tables and their current states displays. Type in the search box to filter the list by table name. The possible states are:

- **NEW**: The table is scheduled for replication but replication hasn’t started.
- **SNAPSHOT\_REPLICATION**: The connector is copying existing data. This status displays until all records are stored in the destination table.
- **INCREMENTAL\_REPLICATION**: The connector is actively replicating changes. This status displays after snapshot replication ends and continues to display indefinitely until a table is either removed from replication or replication fails.
- **FAILED**: Replication has permanently stopped due to an error.

Note

The Openflow runtime canvas doesn’t display table status changes — only the current table status. However, table status changes are recorded in logs when they occur. Look for the following log message:

```
Replication state for table <database_name>.<schema_name>.<table_name> changed from <old_state> to <new_state>
```

If a permanent failure prevents table replication, remove the table from replication. After you address the problem that caused the failure, you can add the table back to replication. For more information, see [Restart table replication](#label-of-postgres-restart-table-replication).

## Restart table replication

Note

This procedure re-snapshots the table in place. It requires Runtime Extensions version `2026.6.18.9` or later and connector version `0.55.0` or later. On earlier versions, re-snapshotting a table that already exists in Snowflake fails instead of reloading in place. Upgrade Runtime Extensions first, and then upgrade the connector flow before you use this procedure.

A table in a FAILED state (for example, due to a missing primary key or an unsupported schema change) does not restart automatically. If a table enters a FAILED state or you need to restart replication from scratch, use the following procedure to remove and re-add the table to replication.

Note

If the failure was caused by an issue in the source table such as a missing primary key, resolve that issue in the source database before continuing.

1. Remove the table from replication, using one of the following methods:

   - Add the table to the **Re-snapshot Table Exclusions** parameter to temporarily exclude it from replication. This approach is convenient when the table is matched by an **Included Table Regex** that you don’t want to change.
   - In the **Ingestion Parameters** context, either remove the table from **Included Table Names** or modify the **Included Table Regex** so the table is no longer matched.
2. Verify the table has been removed:

   1. In the Openflow runtime canvas, right-click a processor group and choose **Controller Services**.
   2. In the table listing controller services, locate the **Table State Store** row, click the three vertical dots on the right side of the row, then choose **View State**.

   Important

   You must wait until the table’s state is fully removed from this list before proceeding. Don’t continue until this configuration change has completed.
3. Wait until all queues in the connector are empty before you re-add the table. When all FlowFiles have been processed, the **Queued** value on the connector’s processor group becomes zero.

   Warning

   Don’t re-add the table while change events that were captured before you removed it are still queued. When you re-add a table, the connector loads the new snapshot in append-only mode, so any leftover change event that merges into the table after the re-snapshot might create duplicate rows in the destination table.
4. Re-add the table by reversing the change you made in the first step: either remove the table from **Re-snapshot Table Exclusions**, or add it back to **Included Table Names** or **Included Table Regex**.

   You do not need to drop the destination table first. The connector re-snapshots the table in place: it makes a zero-copy [clone](/sql-reference/sql/create-clone) of the current destination table to an archive table named `<destination_table>_ARCHIVE_<timestamp>`, clears the destination table, and then loads the fresh snapshot into the same destination table. Because the destination table object is preserved, dependent objects such as streams remain attached and continue to work.

   The archive table retains a copy of the destination table’s contents from immediately before the reload, as a safeguard. The connector does not read from or write to it again, so you can drop it at any time once the backup is no longer needed, typically after you confirm that the re-snapshot completed and the destination data is correct.
5. Verify the restart: Check the **Table State Store** using the instructions given previously. The state of the table should appear with the status NEW, then transition to SNAPSHOT\_REPLICATION, and finally to INCREMENTAL\_REPLICATION.

## Increase the oversized value limit

By default, the connector replicates individual values up to 16 MB and marks any table that contains a larger value as permanently failed. If your Snowflake account has the `ENABLE_OPENFLOW_CDC_POSTGRES_SSV2` parameter set to `true`, the per-value limit can be raised from 16 MB to **128 MB**.

Important

The 128 MB limit applies in two ways: it’s both the maximum size of a single value and the maximum total size of a row. The connector adds metadata columns to every replicated row (`_SNOWFLAKE_UPDATED_AT`, `_SNOWFLAKE_INSERTED_AT`, `_SNOWFLAKE_DELETED`) that count toward the per-row limit, along with all other columns in the row. As a result, a single value can’t reach the full 128 MB in practice when the row includes other data.

The increased limit doesn’t apply equally to all column types.

Note

In Snowflake, the maximum size for `BINARY` is **64 MB** (`BINARY(67108864)`), even when the increased size limits are enabled. Only `VARCHAR`, `VARIANT`, `ARRAY` and `OBJECT` columns can hold up to 128 MB.

### Check whether the 128 MB limit is available

You may not be able to verify the `ENABLE_OPENFLOW_CDC_POSTGRES_SSV2` parameter value by querying it. To check if it is enabled, see if the FlowFiles flow through **Upload Rows via Snowpipe Streaming 2** processor (not through **Upload Rows via Snowpipe Streaming**).

### Configure the processors

Update the **Oversized Value Limit** property to `128 MB` on both of the following processors:

- **Fetch Table Rows** (in the **Snapshot Load** group)
- **Read PostgreSQL CDC Stream** (in the **Incremental Load** group)

For each processor:

1. Locate the processor in the flow. On the connector canvas, you can use the search box in the top-right corner to find processors by name.
2. Right-click the processor and select **Configure**.
3. Open the **Properties** tab.
4. Set **Oversized Value Limit** to `128 MB`.
5. Apply the change.

For tables that are already being replicated and have destination columns narrower than `VARCHAR(134217728)` or `BINARY(67108864)`, see [Migrate existing tables](#label-of-postgres-migrate-oversized-value-tables).

### Migrate existing tables

The steps in [Increase the oversized value limit](#label-of-postgres-increase-oversized-value-limit) raise the limit for newly created destination tables. If a table is already being replicated and its destination column type is **not** `VARCHAR(134217728)` or `BINARY(67108864)`, but you now want to load values larger than the original 16 MB limit, you must manually widen the column type on **both** the journal and destination tables.

Before you migrate, check the current destination column type, because it can vary depending on when the snapshot replication was performed.

Warning

You must stop replication for the affected table before altering its journal or destination tables. Altering these tables while replication is active can corrupt in-flight data.

To migrate a table:

1. Stop replication for the affected table by stopping the topmost processors of the **Snapshot Load** and **Incremental Load** groups until all queues are empty. For the equivalent stop procedure, see the substeps in [Reclaim journal table storage](#label-postgres-reinstall-connector).
2. Widen the column on both the journal table and the destination table, according to the column type:
   1. For **VARCHAR** columns, run a single `ALTER TABLE ... ALTER COLUMN ... SET DATA TYPE VARCHAR(134217728)` on both the journal and destination tables.
   2. For **BINARY** columns, Snowflake doesn’t allow widening `BINARY` in place, so do the following on both the journal and destination tables:
      1. Add a new column of type `BINARY(67108864)`.
      2. Copy data from the original column into the new column.
      3. Drop the original column and rename the new column to the original name.
3. Restart replication by re-enabling the processors.

### Performance considerations

Raising the per-value limit increases the amount of data that the connector loads into memory and moves through the flow, which raises the load on both the runtime and the warehouse. Size the runtime and warehouse accordingly.

During both snapshot and incremental replication, the queue in front of the **Upload Rows via Snowpipe Streaming 2** processor can fill with FlowFiles and trigger back pressure, which consumes a large amount of runtime disk space. For larger tables, use a Large runtime to provide additional storage. For guidance on choosing a size, see [Runtime sizing](/user-guide/data-integration/openflow/connectors/cdc-runtime-sizing#label-openflow-cdc-runtime-sizing).

#### Snapshot replication

During snapshot replication, the product of `fetchSize * rowSize * concurrentQueries` can’t exceed the heap size of the NiFi runtime, where:

- `fetchSize` is the number of rows fetched per query, set on the **Fetch Table Rows** processor (default: 100).
- `rowSize` is the size of a single row being fetched.
- `concurrentQueries` is the number of concurrent queries, set on the **Fetch Table Rows** processor (default: 2).

This memory requirement applies even when **Oversized Value Strategy** is set to **Set Null**, because the connector must load each oversized value into memory before it can replace the value with `NULL`.

If the source database contains many densely packed oversized values, consider excluding the affected column from replication before you start the snapshot. For example, if a column contains 1 GB values, loading even nine rows (~9 GB) can exhaust the heap and cause an out-of-memory error on a Medium runtime.

To speed up snapshot replication, you can increase the number of channels that the **Upload Rows via Snowpipe Streaming 2** processor uses. The number of channels is set by the processor’s **Channel Group** property, which defaults to `${chunk.index:isEmpty():ifElse('1', ${chunk.index:mod(8)})}`.

To increase the number of channels:

1. Locate the **Upload Rows via Snowpipe Streaming 2** processor in the flow.
2. Stop the processor. You must stop the processor before you can change its properties.
3. Right-click the processor and select **Configure**.
4. Open the **Properties** tab.
5. In the **Channel Group** property, increase the value `8` in the expression. For example, change `8` to `16` to double the number of channels.
6. Apply the change.
7. Start the processor.

Warning

While a snapshot replication is in progress, only increase the number of channels. Decreasing the number of channels during an active snapshot can cause data loss.

#### Incremental replication

When the source produces frequent changes to rows that contain large values, you might need a Large warehouse. With smaller warehouses, replicating many 8 MB rows can cause an out-of-memory error. By contrast, replicating 128 MB rows with continuous merges completes without warehouse errors, because the connector streams the data file by file through the **Upload Rows via Snowpipe Streaming 2** processor and the merge processes it gradually.

## Enable error logging on an existing schema

When you set the **Error Handling Strategy** parameter to **Log Errors and Continue**, the connector enables error logging automatically only on tables that it creates afterward. Tables that the connector created earlier don’t capture rejected rows until you turn on error logging for them. For more information about the error-handling strategies, see [Error handling for invalid rows](/user-guide/data-integration/openflow/connectors/postgres/about#label-postgres-error-handling).

Because the connector stores journal tables in the same schema as the destination tables, you can turn on error logging for a whole destination schema at once. Run the following stored procedure once per destination schema. Replace `my_database` with your destination database and `my_schema` with the destination schema.

Note

The schema name is passed as a quoted identifier (for example, `'"my_schema"'`) so it matches the exact, case-sensitive name that the connector created. For more information about how the connector names destination schemas, see [PostgreSQL Destination Parameters](/user-guide/data-integration/openflow/connectors/postgres/setup#label-of-postgres-destination-parameters).

Copy code

```
USE DATABASE my_database;

WITH enable_error_logging AS PROCEDURE (schema_name STRING)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
  tables RESULTSET;
  table_count NUMBER DEFAULT 0;
BEGIN
  SHOW TABLES IN SCHEMA IDENTIFIER(:schema_name);

  -- Assign AFTER SHOW TABLES so LAST_QUERY_ID() refers to that result
  tables := (
    SELECT "database_name", "schema_name", "name"
    FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
    WHERE "kind" = 'TABLE'
  );

  FOR t IN tables DO
    -- Double-quote each identifier so names with special characters are handled safely
    EXECUTE IMMEDIATE
      'ALTER TABLE "' || REPLACE(t."database_name", '"', '""') || '".' ||
      '"'             || REPLACE(t."schema_name",   '"', '""') || '".' ||
      '"'             || REPLACE(t."name",          '"', '""') || '" ' ||
      'SET ERROR_LOGGING = TRUE';

    table_count := table_count + 1;
  END FOR;

  RETURN 'Enabled ERROR_LOGGING on ' || table_count || ' table(s) in schema ' || :schema_name;
END;
$$
CALL enable_error_logging('"my_schema"');
```

### Verify that error logging is enabled

To confirm that error logging is enabled on every table in a schema, run the following procedure. It reports how many tables have error logging enabled and how many don’t.

Copy code

```
USE DATABASE my_database;

WITH verify_error_logging AS PROCEDURE (schema_name STRING)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
  tables RESULTSET;
  probe RESULTSET;
  total_tables          NUMBER DEFAULT 0;
  logging_enabled       NUMBER DEFAULT 0;
  disabled_or_invisible NUMBER DEFAULT 0;
BEGIN
  SHOW TABLES IN SCHEMA IDENTIFIER(:schema_name);

  -- Assign AFTER SHOW TABLES so LAST_QUERY_ID() refers to that result
  tables := (
    SELECT "database_name", "schema_name", "name"
    FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
    WHERE "kind" = 'TABLE'
  );

  FOR t IN tables DO
    total_tables := total_tables + 1;

    -- Probe ERROR_TABLE(): it succeeds only when error logging is enabled and visible
    BEGIN
      probe := (
        EXECUTE IMMEDIATE
          'SELECT 1 FROM ERROR_TABLE(' ||
          '"' || REPLACE(t."database_name", '"', '""') || '".' ||
          '"' || REPLACE(t."schema_name",   '"', '""') || '".' ||
          '"' || REPLACE(t."name",          '"', '""') || '"' ||
          ') LIMIT 1'
      );
      logging_enabled := logging_enabled + 1;
    EXCEPTION
      WHEN STATEMENT_ERROR THEN
        disabled_or_invisible := disabled_or_invisible + 1;
    END;
  END FOR;

  RETURN 'schema='                                  || :schema_name ||
         ', total_tables='                          || total_tables ||
         ', error_logging_enabled='                 || logging_enabled ||
         ', error_logging_disabled_or_not_visible=' || disabled_or_invisible;
END;
$$
CALL verify_error_logging('"my_schema"');
```

## Upgrading PostgreSQL

Upgrading the connector requires a different approach depending on whether PostgreSQL is being upgraded to the next minor or major version.

Minor version upgrades

- Are data-safe.
- Require no special treatment.
- Require stopping the connector for the duration of the upgrade to avoid reporting connectivity issues.
- Continue replicating, after the upgrade, with no data loss.

Major version upgrades

- Require the PostgreSQL server to drop replication slots, including any used by the connector.
- Cannot preserve or migrate replication slots to the new version. See also [PostgreSQL 17 and later versions upgrades](#label-postgres-upgrade-note).
- Require restarting replication of all tables from the snapshot phase, unless you can stop all writes to the source database for the duration of the upgrade. In that case, you can keep the replicated data and resume with incremental replication only. For more information, see [Upgrade without re-snapshotting tables](#label-postgres-upgrade-incremental-only).

To perform a minor version upgrade, do the following:

1. Stop the connector, including all Processors and Controller Services.
2. Upgrade PostgreSQL.
3. Restart the connector.

To perform a major version upgrade, do the following:

1. Remove all tables from replication in the connector by clearing the **Included Table Names** and **Included Table Regex** parameters.
2. Wait until all queues in the connector are empty, so that every captured change is merged into the destination tables.
3. Stop the connector, including all Processors and Controller Services.
4. Open the **Incremental Load** group in the connector.
5. Clear the state of the CDC processor:
   1. Open the **Incremental Load** group in the connector.
   2. Right-click the top Processor in the group, **Read PostgreSQL CDC Stream**, and select **View state**.
   3. Click **Clear state**.
   4. Click **Close**.
6. Upgrade PostgreSQL.
7. Restart the connector. A new replication slot will be created.
8. Re-add all tables to the **Included Table Names** or **Included Table Regex** parameters.

You don’t need to drop or rename the destination tables before you re-add the tables. The connector re-snapshots each table in place, which preserves the destination table object along with dependent objects such as streams. Before it loads the fresh snapshot, the connector saves a copy of the previous contents in an archive table named `<destination_table>_ARCHIVE_<timestamp>`, which you can drop once you’ve confirmed that the re-snapshot completed. For more information, see [Restart table replication](#label-of-postgres-restart-table-replication).

### Upgrade without re-snapshotting tables

When an upgrade drops the replication slot, you can avoid re-snapshotting every table if you can stop all writes to the source database while you upgrade. This applies to major version upgrades and to any upgrade to PostgreSQL 17.0 from version 16 or earlier. The connector keeps the data it already replicated and continues with incremental replication only.

Warning

No writes of any kind, whether DML or DDL, can reach the replicated database from the moment you stop the connector until all tables are back in incremental replication. The new replication slot starts at the current write-ahead log position, so any change made during that window is lost and there’s no way to recover it without a new snapshot.

To upgrade without re-snapshotting tables, do the following:

1. Remove all tables from replication in the connector by clearing the **Included Table Names** and **Included Table Regex** parameters.
2. Wait until all queues in the connector are empty, so that every captured change is merged into the destination tables.
3. Stop the connector, including all Processors and Controller Services.
4. Stop all writes to the source database, and keep them stopped for the rest of this procedure.
5. Clear the state of the CDC processor:
   1. Open the **Incremental Load** group in the connector.
   2. Right-click the top Processor in the group, **Read PostgreSQL CDC Stream**, and select **View state**.
   3. Click **Clear state**.
   4. Click **Close**.
6. Upgrade PostgreSQL.
7. In the `PostgreSQL Ingestion Parameters` context, set the `Ingestion Type` parameter to `incremental`. For more information, see [Openflow Connector for PostgreSQL: Set up incremental replication without snapshots](/user-guide/data-integration/openflow/connectors/postgres/incremental-replication).
8. Restart the connector. A new replication slot is created.
9. Re-add all tables to the **Included Table Names** or **Included Table Regex** parameters. The tables bypass the snapshot phase and replicate incrementally into the existing destination tables.
10. Confirm that every table reaches the status INCREMENTAL\_REPLICATION in the **Table State Store** controller service. For instructions on viewing table state, see [Check the replication status of a table](#label-of-postgres-check-table-replication-status).
11. Resume writes to the source database.
12. Set the `Ingestion Type` parameter back to `full`, so that tables you add later still get a snapshot.

### PostgreSQL 17 and later versions upgrades

PostgreSQL 17 improved upgrading such that it no longer requires dropping replication slots when upgrading to later versions such as 17.1 » 18.0.
Upgrading to PostgreSQL 17.0 or later from prior versions (16 and earlier) drops replication slots and should be treated as a major upgrade.
Future versions of PostgreSQL may also improve the upgrade process further.

If the connector is using failover slot support, ensure the slot is caught up and not conflicting before starting the upgrade. See [Additional step when running pg\_upgrade](/user-guide/data-integration/openflow/connectors/postgres/failover#label-postgres-failover-pg-upgrade).

## Reclaim journal table storage

Journal tables hold every change to a replicated table. The connector never drops them, but it only
reads the latest journal for each replicated source table, using append-only streams on top of the
journals. To reclaim storage, you can:

- Truncate all journal tables at any time.
- Drop the journal tables related to source tables that were removed from replication.
- Drop all but the latest generation journal tables for actively replicated tables.

For example, if your connector is set to actively replicate source table `orders`, and you have
earlier removed table `customers` from replication, you may have the following journal tables. In
this case you can drop all of them *except* `orders_5678_2`.

```
customers_1234_1
customers_1234_2
orders_5678_1
orders_5678_2
```

## Stop or delete the connector

When stopping or removing the connector, you have to consider the [replication slot](https://www.postgresql.org/docs/current/warm-standby.html#STREAMING-REPLICATION-SLOTS) that the connector uses.

The connector creates its own replication slot with a name starting with
`snowflake_connector_` followed by a random suffix. As the connector reads the replication stream,
it advances the slot, so that PostgreSQL can trim its WAL log and free up disk space.

When the connector is paused, the slot isn’t advanced, and changes to the source database keep increasing the WAL
log size. You should not keep the connector paused for extended periods of time, especially on high-traffic databases.

When the connector is removed, whether by dropping it with `DROP OPENFLOW CONNECTOR` (gen 2), deleting it from the Openflow canvas,
or any other means, such as deleting the whole Openflow instance, the replication slot remains in place, and must be dropped manually.

If you have multiple connector instances replicating from the same PostgreSQL database,
each instance will create its own uniquely named replication slot. When dropping a replication slot manually, make sure
it’s the right one. You can see which replication slot is used by a given connector instance by checking the state of the `CaptureChangePostgreSQL` processor.

## Reinstall the connector

This section describes how to reinstall the connector.
It covers situations where the new connector is installed in the same runtime, or where it is moved to a new runtime.
Reinstall is often used in conjunction with [Incremental replication without snapshots](/user-guide/data-integration/openflow/connectors/postgres/incremental-replication).

Warning

For the connector to be able to continue replicating from the same CDC stream position where it stopped before reinstallation,
the source database must retain the WAL long enough to cover the time between when the old connector stops and the new connector starts.
Ensure the `max_wal_size` parameter of the PostgreSQL server is high enough, depending on your traffic, and keep the reinstallation time to a minimum.

### Prerequisites

Review and note connector parameter context values.
If you’re reinstalling the connector in the same runtime, you can reuse the existing context.
If the new instance will be located in a different runtime, you will have to re-enter all parameters.

To reinstall the connector:

1. Finish processing all in-flight FlowFiles in the existing connector, and then stop the connector.

   1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
   2. In the navigation menu, select **Ingestion** » **Openflow**.
   3. Select **Launch Openflow**.
   4. In the **Openflow** pane select the **Runtimes** tab.
   5. Select the runtime containing the connector.
   6. Select the connector.
   7. Stop the topmost processor **Set Tables for Replication** in the **Snapshot Load** group.
   8. Stop the topmost processor **Read PostgreSQL CDC Stream** in the **Incremental Load** group.
   9. If you changed the value of the **Merge Task Schedule CRON** parameter, return it to `* * * * * ?`. Otherwise, queues won’t be emptied until the next scheduled run.

      Wait until all FlowFiles in the connector have been processed, and all queues are empty.
      When all FlowFiles have been processed, the **Queued** value on the connector’s processor group becomes zero.
      If there are any items left in the original connector’s queues, there may be data gaps when the new connector starts.
   10. Stop all Processors and Controller Services in the connector.
2. Find and copy the name of the replication slot used by the original connector,
   by viewing the state of the topmost processor in the `Incremental Load` group with name `Read PostgreSQL CDC Stream`.
   The replication slot name is stored under the key `replication.slot.name`.
   Copy the value of the key to a text editor.
3. Create a new instance of the connector. If you’re using the same runtime as the original connector, you can choose to keep the existing parameter contexts, and reuse the settings.

   Caution

   The existing connector can remain in the runtime and doesn’t interfere with the new instance, as long as it remains stopped.
4. If you’re installing into a different runtime, or you deleted the previous parameter contexts, enter all the configuration settings into the new parameter contexts,
   including the table names and patterns as described in [Set up the Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/setup).
5. Open the `PostgreSQL Ingestion Parameters` context, and set `Ingestion Type` parameter to `incremental`.
   For more information, see [Enable incremental replication without snapshots](/user-guide/data-integration/openflow/connectors/postgres/incremental-replication#label-postgres-incremental-replication).
6. Open the `PostgreSQL Source Parameters` context, and set the `Replication Slot Name` parameter to the value you copied earlier.
7. Start the new connector.

### Usage notes

The new connector will use the same existing destination tables that were created by the original connector, but will create new journal tables.
