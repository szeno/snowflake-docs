# Openflow Connector for SQL Server: Maintenance

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

This topic describes maintenance considerations and best practices for the Openflow Connector for SQL Server, such as reinstalling the connector or setting the change tracking starting position.

These operations are often used in conjunction with [Incremental replication without snapshots](/user-guide/data-integration/openflow/connectors/sql-server/incremental-replication).

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

If a permanent failure prevents table replication, remove the table from replication. After you address the problem that caused the failure, you can add the table back to replication. For more information, see [Restart table replication](#label-of-sql-server-restart-table-replication).

## Restart table replication

Note

This procedure re-snapshots the table in place. It requires connector version `0.53.0` or later, and runtime-extensions `2026.9.3.12` or later. On earlier versions, re-snapshotting a table that already exists in Snowflake fails instead of reloading in place. Upgrade the connector before you use this procedure.

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

By default, the connector replicates individual values up to 16 MB and marks any table that contains a larger value as permanently failed. If your Snowflake account has the `ENABLE_OPENFLOW_CDC_SQLSERVER_SSV2` parameter set to `true`, the per-value limit can be raised from 16 MB to **128 MB**.

Important

The 128 MB limit applies in two ways: it’s both the maximum size of a single value and the maximum total size of a row. The connector adds metadata columns to every replicated row (`_SNOWFLAKE_UPDATED_AT`, `_SNOWFLAKE_INSERTED_AT`, `_SNOWFLAKE_DELETED`) that count toward the per-row limit, along with all other columns in the row. As a result, a single value can’t reach the full 128 MB in practice when the row includes other data.

The increased limit doesn’t apply equally to all column types.

Note

In Snowflake, the maximum size for `BINARY` is **64 MB** (`BINARY(67108864)`), even when the increased size limits are enabled. Only `VARCHAR`, `VARIANT`, `ARRAY`, and `OBJECT` columns can hold up to 128 MB.

### Check whether the 128 MB limit is available

You may not be able to verify the `ENABLE_OPENFLOW_CDC_SQLSERVER_SSV2` parameter value by querying it. To check if it is enabled, see if the FlowFiles flow through the **Upload Rows via Snowpipe Streaming 2** processor (not through **Upload Rows via Snowpipe Streaming**).

### Configure the processors

Update the **Oversized Value Limit** property to `128 MB` on the following processors:

- **Fetch Table Rows** (in the **Snapshot Load** group): used for non-partitioned tables
- **MultiDatabaseFetchTableSnapshot** (in the **Snapshot Load** group): used for partitioned tables
- **Read SQLServer Change Tracking tables** (in the **Incremental Load** group)

For each processor:

1. Locate the processor in the flow. On the connector canvas, you can use the search box in the top-right corner to find processors by name.
2. Right-click the processor and select **Configure**.
3. Open the **Properties** tab.
4. Set **Oversized Value Limit** to `128 MB`.
5. Apply the change.

For tables that are already being replicated and have destination columns narrower than `VARCHAR(134217728)` or `BINARY(67108864)`, see [Migrate existing tables](#label-of-sql-server-migrate-oversized-value-tables).

### Migrate existing tables

The steps in [Increase the oversized value limit](#label-of-sql-server-increase-oversized-value-limit) raise the limit for newly created destination tables. If a table is already being replicated and its destination column type is **not** `VARCHAR(134217728)` or `BINARY(67108864)`, but you now want to load values larger than the original 16 MB limit, you must manually widen the column type on **both** the journal and destination tables.

Before you migrate, check the current destination column type, because it can vary depending on when the snapshot replication was performed.

Warning

You must stop replication for the affected table before altering its journal or destination tables. Altering these tables while replication is active can corrupt in-flight data.

To migrate a table:

1. Stop replication for the affected table by stopping the topmost processors of the **Snapshot Load** and **Incremental Load** groups until all queues are empty. For the equivalent stop procedure, see the substeps in [Reinstall the connector](#label-sql-server-reinstall-connector).
2. Widen the column on both the journal table and the destination table, according to the column type:
   1. For **VARCHAR** columns, run `ALTER TABLE ... ALTER COLUMN ... SET DATA TYPE VARCHAR(134217728)` on the journal table and on the destination table (one statement per table).
   2. For **BINARY** columns, Snowflake doesn’t allow widening `BINARY` in place, so do the following on both the journal and destination tables:
      1. Add a new column of type `BINARY(67108864)`.
      2. Copy data from the original column into the new column.
      3. Drop the original column and rename the new column to the original name.
3. Restart replication by re-enabling the processors.

### Performance considerations

Raising the per-value limit increases the amount of data that the connector loads into memory and moves through the flow, which raises the load on both the runtime and the warehouse. Size the runtime and warehouse accordingly.

When **Oversized Value Strategy** is set to **Set Null**, the connector still loads each oversized value into memory before it can replace it with `NULL`. If your tables contain multi-gigabyte LOB columns, exclude those columns from replication.

During both snapshot and incremental replication, the queue in front of the **Upload Rows via Snowpipe Streaming 2** processor can fill with FlowFiles and trigger back pressure, which consumes a large amount of runtime disk space. For larger tables, use a Large runtime to provide additional storage. For guidance on choosing a size, see [Runtime sizing](/user-guide/data-integration/openflow/connectors/sql-server/setup#label-sql-server-runtime-sizing).

#### Snapshot replication

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

When the source produces frequent changes to rows that contain large values, you might need a Large warehouse. High-frequency merges of many moderately large rows (for example, many 8 MB values) can require a large single merge operation, and smaller warehouses can run out of memory. By contrast, fewer very large rows (for example, 128 MB values) are streamed file by file through the **Upload Rows via Snowpipe Streaming 2** processor, and each file is merged incrementally, which typically completes without warehouse errors even on smaller warehouses.

## Enable error logging on an existing schema

When you set the **Error Handling Strategy** parameter to **Log Errors and Continue**, the connector enables error logging automatically only on tables that it creates afterward. Tables that the connector created earlier don’t capture rejected rows until you turn on error logging for them. For more information about the error-handling strategies, see [Error handling for invalid rows](/user-guide/data-integration/openflow/connectors/sql-server/about#label-sql-server-error-handling).

Because the connector stores journal tables in the same schema as the destination tables, you can turn on error logging for a whole destination schema at once. Run the following stored procedure once per destination schema. Replace `my_database` with your destination database and `my_schema` with the destination schema.

Note

The schema name is passed as a quoted identifier (for example, `'"my_schema"'`) so it matches the exact, case-sensitive name that the connector created. For more information about how the connector names destination schemas, see [SQLServer Destination Parameters](/user-guide/data-integration/openflow/connectors/sql-server/setup#label-of-sqlserver-destination-parameters).

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

## Reinstall the connector

This section provides instructions on how to reinstall the connector, and continue replicating data for
the same tables without having to snapshot them again.
It covers situations where the new connector is installed in the same runtime, as well as when it’s moved to a new runtime.

### Prerequisites

Review and note connector parameter context values.
If you reinstall the connector in the same runtime, you can reuse the existing context.
If the new instance is located in a different runtime, you must re-enter all parameters.

1. Finish processing all in-flight FlowFiles in the existing connector, then stop the connector.

   1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
   2. In the navigation menu, select **Ingestion** » **Openflow**.
   3. Select **Launch Openflow**.
   4. In the **Openflow** pane select the **Runtimes** tab.
   5. Select the runtime containing the connector.
   6. Select the connector.
   7. Stop the topmost processor **Set Tables for Replication** in the **Snapshot Load** group.
   8. Stop the topmost processor **Read SQLServer Change Tracking tables** in the **Incremental Load** group.
   9. If you changed the value of the **Merge Task Schedule CRON** parameter, return it to `* * * * * ?`; otherwise, queues won’t be emptied until the next scheduled run.

      Wait until all FlowFiles in the connector have been processed, and all queues are empty.
      When all FlowFiles have been processed, the **Queued** value on the connector’s processor group becomes zero.
      If there are any items left in the original connector’s queues, there may be data gaps when the new connector starts.
   10. Stop all processors and controller services in the connector.

   Caution

   The existing connector can remain in the runtime and doesn’t interfere with the new instance, as long as it remains stopped.
2. If you’re moving the connector to a new runtime, download the flow definition from the existing connector so that you can recreate the connector with its current state instead of configuring it from scratch. Downloading a flow definition requires Openflow Runtime Server version 2026.6.4.18 or later.

   1. Right-click the connector’s process group, then select **Download flow definition**.
   2. Select both of the following options, then download the flow definition:
      - **Export with External Services**: includes the controller services that the connector references from parent process groups.
      - **Export with Components State**: includes component state, such as change tracking positions and incremental replication state, so that replication continues from where it left off.
3. Create the connector in the target runtime:

   - If you downloaded the flow definition, import it into the new runtime. Importing the flow definition preserves the component state captured during the export, so the connector resumes incremental replication from its previous positions.
   - Otherwise, create a new instance of the connector. If you use the same runtime as the original connector, you can choose to keep the existing parameter contexts and reuse the settings.
4. If you install into a different runtime or you deleted the previous parameter contexts, enter the configuration settings into the new parameter contexts,
   including the table names and patterns as described in [Set up the Openflow Connector for SQL Server](/user-guide/data-integration/openflow/connectors/sql-server/setup). A downloaded flow definition doesn’t include sensitive values (such as passwords) or uploaded files (such as the Microsoft JDBC driver), so you must re-enter and re-upload them.
5. Navigate to the `SQLServer Ingestion Parameters` context, and set the following parameters:

   - Set the `Ingestion Type` parameter to `incremental`. For information, see [Enable incremental replication without snapshots](/user-guide/data-integration/openflow/connectors/sql-server/incremental-replication#label-sql-server-incremental-replication).
   - Set the `Starting Change Tracking Position` parameter to `Earliest`.
     For information, see [Specify load from change tracking table position](#label-sql-server-connector-start-restart-incremental-load-from-earliest-available-change-tracking-position).

   Note

   If you imported the flow definition with **Export with Components State** selected, the connector retains its previous change tracking positions. In this case, leave `Starting Change Tracking Position` set to `Latest` to continue replication from where it stopped.
6. Start the new connector.

### Usage notes

The new connector uses the existing destination tables created by the original connector, but creates new journal tables.

## Specify load from change tracking table position

The Openflow Connector for SQL Server connector lets you select the starting position where change tracking tables are read.
By default, the connector reads from the latest available position. Alternatively, you can choose the earliest position available on the source instance.
Choosing to start from the earliest position is common when reinstalling the connector.
This allows the new instance to catch up and continue replicating existing tables without having to snapshot each again.

Switching a running connector from latest to earliest position causes the contents of change tracking tables to be re-read, re-processed, and re-applied to the destination table.

Warning

While the change tracking tables are being re-read, the data in affected destination tables
can become out of sync with their sources until all events have been re-processed and merged.

The following parameters are available in the `Ingestion Parameters` context:

| Parameter | Description |
| --- | --- |
| Starting Change Tracking Position | - `Latest` (default): change tracking table reading starts at the latest available position and continues from there. - `Earliest`: Switches the incremental load to start, or restart reading from the earliest available   change tracking table positions. |
| Re-read Tables in State | - `New` (default):   Only new tables, added after the starting position was switched to `Earliest`, will have their change   tracking tables read from the earliest available positions. Tables that started replication before the   configuration change will continue reading from their last positions. - `Any active`: Re-read and re-process changes from any table currently in replication. |

Expand

Show lessSee more

To determine whether the connector finished re-reading the change tracking tables:

1. Navigate to the Openflow canvas.
2. Open the **Incremental Load** process group.
3. Right-click the topmost processor named **Read SQLServer Change Tracking tables**, then select **View state**.
4. Check the state entries for every table with keys starting with `position.`. If a value is `0/0` then the connector has not yet finished re-reading the changes for this table.

### Usage notes

- After you switch a running connector to read from the earliest positions and start it,
  you can’t reconfigure or cancel the process, and it will continue until the currently read positions reach the latest values.
- Switching to the earliest position on a running connector will, for any tables being re-processed,
  finish their existing journals, and create new journal tables.
