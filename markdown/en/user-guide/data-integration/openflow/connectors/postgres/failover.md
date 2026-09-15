# Openflow Connector for PostgreSQL: PostgreSQL 17+ failover slot support

Feature — Generally Available

Snowflake connectors are supported in every region where Snowflake Openflow is available.

[Openflow Snowflake deployments](/user-guide/data-integration/openflow/about-spcs) are available to all accounts in AWS, Azure, and GCP Commercial Regions.

[Snowflake Openflow on BYOC deployments](/user-guide/data-integration/openflow/about-byoc) are available to all accounts in AWS Commercial Regions only ([Commercial regions](/user-guide/intro-regions#label-na-general-regions)).

Note

This connector is subject to the [Snowflake Connector Terms](https://www.snowflake.com/legal/snowflake-connector-terms/).

Important

Requires runtime-extensions 2026.7.16.14 or later. Applies to PostgreSQL 17 and later only.

On PostgreSQL 17 and later, the connector creates its logical replication slot with `failover=true`.
The slot is synchronized to standbys by PostgreSQL and survives:

- A primary failover: replication resumes from the new primary.
- A major-version upgrade through `pg_upgrade` (for example, 17 → 18), provided the slot is caught up and not conflicting or invalidated at upgrade time.

The connector must be pointed at the primary to get failover protection.
PostgreSQL does not allow `failover=true` on slots created against a standby.
If the JDBC URL resolves to a read replica, the slot on that node will not have failover protection.

Version is auto-detected. No new connector property is required.

## Limitations

- PostgreSQL 16 and earlier versions are unchanged. Failover protection is not available on those versions as this is a native PostgreSQL feature that does not exist before PostgreSQL 17.
- Upgrading the connector alone does not retrofit failover onto an existing slot. The connector only sets `failover=true` at slot creation time. To gain failover protection on an existing deployment, see [Retrofit failover protection on an existing deployment](#label-retrofit-failover-protection-on-an-existing-deployment).
- Delivery is at-least-once across a failover. The connector de-duplicates on reconnect.
- The connector does not validate the PostgreSQL configuration described in this topic. If it is missing, `failover=true` is inert and the slot will not survive a failover.

## Required PostgreSQL configuration

The following configuration must be set by the user. The connector can’t set these.

- Point the JDBC URL at the primary’s writer endpoint so the connector reconnects to the new primary after a failover.
  To confirm the connector is connected to the primary, run the following against the connected database.
  The result must be `false` (false = primary, true = standby):

  Copy code

  ```
  SELECT pg_is_in_recovery();
  ```
- On the primary, set `synchronized_standby_slots` to list the physical replication slot names of the failover-candidate standbys.
  Without it, the failover slot may advance faster than the standby receives WAL:

  Copy code

  ```
  synchronized_standby_slots = '<physical_slot_name>'
  ```
- On each failover-candidate standby, set the following:

  - `wal_level = logical` (already required on the primary): set this on standbys so it takes effect on promotion.
  - `sync_replication_slots = on`
  - `hot_standby_feedback = on`
  - `primary_conninfo` must include `dbname=<database>` (PostgreSQL 17 requirement).
  - `primary_slot_name` must reference a physical slot listed in `synchronized_standby_slots` on the primary.

## Retrofit failover protection on an existing deployment

To gain failover protection on an existing deployment, there are two paths available: with re-snapshot or without re-snapshot. Follow the procedure for the path you choose.

### Retrofit failover protection without re-snapshotting

Warning

Process all existing FlowFiles in the existing connector before you start the new one. The existing connector should have no FlowFiles in queue and should have all processors stopped. Any writes between stopping the existing connector and starting the new connector will not be delivered to Snowflake. Once a slot is dropped, PostgreSQL can’t replay old WAL. If you can’t guarantee a write-free window, use [Retrofit failover protection with re-snapshot](#label-retrofit-with-re-snapshot) instead.

Important

Do not add new tables while the connector is in incremental mode. New tables will not be snapshotted.

1. Ensure the connector is fully caught up before proceeding. The `confirmed_flush_lsn` should match `pg_current_wal_lsn()`:

   Copy code

   ```
   SELECT slot_name, confirmed_flush_lsn, pg_current_wal_lsn() FROM pg_replication_slots;
   ```
2. Pause writes on the source tables by running the following against your PostgreSQL source database. Replace `<schema>` and `<app_role>` with your values:

   Copy code

   ```
   REVOKE INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA <schema> FROM <app_role>;
   ```
3. Wait until all queues in the connector are empty.
4. Stop the connector and disable all Controller Services.
5. Drop the replication slot. The slot name is in the `CaptureChangePostgreSQL` processor state under `replication.slot.name`, or in `pg_replication_slots`:

   Copy code

   ```
   SELECT pg_drop_replication_slot('<slot_name>');
   ```
6. In the parameter context, set **Ingestion Type** to `incremental`. To set this, go to **Ingestion Parameters** → **Ingestion Type** → edit the value to `incremental`.
7. Install a new connector. In the top menu, drag down **Import from registry**. Select **postgresql** from **Flow**, select **Keep existing Parameter contexts** to reuse the same parameter context as the existing connector, then click **Import**.
8. Start the connector fully, including all Processors and Controller Services.
9. Verify the new slot was created with `failover=true` by running the following against your PostgreSQL source database:

   Copy code

   ```
   SELECT slot_name, failover FROM pg_replication_slots;
   ```
10. Resume writes:

    Copy code

    ```
    GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA <schema> TO <app_role>;
    ```
11. Optionally, delete the existing connector to prevent accidentally resuming it.

Note

Once all existing tables are in **Incremental Replication**, change **Ingestion Type** from `incremental` to `full`. To verify, in Snowsight go to **Ingestion** → **Openflow** → **Connector Observability**, select your connector, and confirm all tables show **Incremental Replication** in the **Replication Phase** column.

### Retrofit failover protection with re-snapshot

Note

Individual change events that occur on the source between dropping the slot and completing the re-snapshot are not delivered as CDC events. They are absorbed into the snapshot’s final row values.

1. In the connector, remove all tables from replication by clearing the **Included Table Names** and **Included Table Regex** parameters.
2. Wait until all queues in the connector are empty.
3. Stop the connector, including all Processors and Controller Services.
4. Drop the replication slot. The slot name is in the `CaptureChangePostgreSQL` processor state under `replication.slot.name`, or in `pg_replication_slots`:

   Copy code

   ```
   SELECT pg_drop_replication_slot('<slot_name>');
   ```
5. Install a new connector. In the top menu, drag down **Import from registry**. Select **postgresql** from **Flow**, select **Keep existing Parameter contexts** to reuse the same parameter context as the existing connector, then click **Import**.
6. Re-add tables to **Included Table Names**.
7. Start the new connector fully, including all Processors and Controller Services. The connector creates a new replication slot with `failover=true` and snapshots the tables fresh.

Verify the new slot has `failover=true`:

Copy code

```
SELECT slot_name, failover FROM pg_replication_slots;
```

## Additional step when running pg\_upgrade

This step is only needed during a major-version upgrade. It is not part of the general setup.

Ensure the connector is caught up and the slot is not conflicting or invalidated before starting `pg_upgrade`:

Copy code

```
SELECT slot_name, conflicting, invalidation_reason FROM pg_replication_slots;
```
