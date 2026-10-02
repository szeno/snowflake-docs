# Migrate a gen 1 connector to gen 2

Connector migration converts a gen 1 connector (a process group running on a runtime
canvas) into a gen 2 `OPENFLOW CONNECTOR` Snowflake object. After migration, the connector picks
up where it left off and you manage it with SQL commands and the gen 2 Openflow UI instead of the
NiFi canvas.

To migrate a gen 1 connector, create a new gen 2 connector of the same type using the install
wizard. If eligible gen 1 connectors are on the same runtime, the wizard includes an option to
migrate from an existing connector.

Warning

**Reverting local changes is required:** The migration wizard only accepts process groups that match
their version-controlled baseline. If you made local modifications to the process group canvas or
processor configurations that you can’t discard or replicate through gen 2 connector properties,
**do not migrate**. Preparing the connector for migration requires reverting all local edits.

Note

**Supported connectors:** Connector migration is currently available for **PostgreSQL CDC** and
**MySQL/MariaDB CDC** connectors. Other gen 2 connector types don’t support migration yet. For
how a gen 2 connector’s release stage applies after you migrate, see
[Supported connectors and their release stage](/user-guide/data-integration/openflow/gen2/migrate-connector#label-openflow-migrate-connector-availability).

The wizard also requires the source and destination to be on the same runtime.

Note

**Current limitation: same runtime only.** In the current release, connector migration requires
the source gen 1 connector (process group) and the destination gen 2 connector to be on the **same
runtime**. Cross-runtime and cross-deployment migration is planned for a future release.

## Supported connectors and their release stage

Connector migration is currently supported for the **PostgreSQL CDC** and **MySQL/MariaDB CDC**
connectors. Other connector types that have a gen 2 version don’t support migration yet: install
those as new gen 2 connectors instead.

Each gen 2 connector carries its own release stage, and migrating puts your data flow on the stage
of the gen 2 connector you migrate to. A gen 1 connector that’s generally available today can
therefore land on a gen 2 connector that’s still in preview. Check the stage before you migrate: on
the **Connector library** tab, a gen 2 connector card carries a **Gen 2** badge, plus a **Preview**
badge when that gen 2 connector is in preview.

Both gen 2 connectors that support migration today are in Public Preview, so any connector you
migrate now runs as a preview feature. For example, the gen 1 PostgreSQL connector is generally
available and carries no **Preview** badge, while the gen 2 PostgreSQL connector carries both a
**Gen 2** badge and a **Preview** badge. For the support terms that apply, see
[Preview features](/release-notes/preview-features).

## Before you migrate

### You need a gen 2 runtime that hosts your gen 1 connector

The migration wizard can only offer gen 1 connectors that are on the **same runtime** as the
new gen 2 connector instance you’re creating. The standard path is to migrate your deployment
and runtimes first:

1. Complete [Migrate a gen 1 deployment and runtimes to gen 2](/user-guide/data-integration/openflow/gen2/migrate-deployment-runtime).
2. After migration, the gen 2 runtime hosts both your existing process groups (gen 1 connectors) and any
   new gen 2 connectors you create.

If you’ve already created a gen 2 runtime through the quickstart without migrating from gen 1,
proceed to the next section. Connector migration is available on any gen 2 runtime that has
eligible process groups.

### Required privileges

To run the migration wizard and create the new gen 2 connector, your Snowflake role must have:

- `USAGE` on the database and schema where the runtime is located
- `USAGE` on the gen 2 `OPENFLOW RUNTIME` object
- `CREATE OPENFLOW CONNECTOR` on the runtime’s schema

Copy code

```
GRANT USAGE ON DATABASE <runtime_db> TO ROLE <your_role>;
GRANT USAGE ON SCHEMA <runtime_db>.<runtime_schema> TO ROLE <your_role>;
GRANT USAGE ON OPENFLOW RUNTIME <runtime_db>.<runtime_schema>.<runtime_name> TO ROLE <your_role>;
GRANT CREATE OPENFLOW CONNECTOR ON SCHEMA <runtime_db>.<runtime_schema> TO ROLE <your_role>;
```

### Prepare your gen 1 connector for migration

The migration wizard only lists gen 1 process groups that are stopped, drained, have all controller services disabled, and match their version-controlled baseline.

Follow these steps in sequence to prepare your connector:

1. **Stop source ingestion and drain the queues:**
   Stop the topmost source processors while leaving all other processors and controller services running so in-flight data flushes completely to Snowflake:

   - For detailed click-by-click instructions, see step 1 of the maintenance procedure for your connector: [PostgreSQL CDC](/user-guide/data-integration/openflow/connectors/postgres/maintenance#label-postgres-reinstall-connector) or [MySQL CDC](/user-guide/data-integration/openflow/connectors/mysql/maintenance#label-mysql-reinstall-connector).
   - Wait until all FlowFiles have finished processing and the connector process group shows **Queued** count at zero (`0 / 0 bytes`).
   - For troubleshooting and details on avoiding data loss, see [Drain the connector safely](#label-openflow-migrate-connector-prereqs-drain).

   Warning

   **Improper draining causes permanent data loss:** Never empty, purge, or force-clear queues to make a connector appear drained. On CDC connectors, queued FlowFiles represent changes already captured from the source but not yet loaded into Snowflake. Draining must be performed by stopping only source ingestion while keeping downstream processors and controller services active until queues reach zero.

   After the queues reach zero, leave the connector stopped until the gen 2 connector is ready to start.

   Warning

   **Ensure the source can retain change logs while stopped:** The gen 1 connector must remain stopped until the new gen 2 connector is configured, verified, and started. Verify that your source database retains change logs (such as the MySQL binary log retention or PostgreSQL WAL capacity and disk space) long enough to cover the entire downtime window. If change logs expire or are pruned before the new connector starts, the connector can’t resume seamlessly and requires a new snapshot. Plan migration during a low-traffic window to keep downtime to a minimum.
2. **Stop all remaining processors:**
   After queues reach zero, right-click the connector process group on the canvas and select **Stop** to halt all downstream processors.
3. **Disable all controller services:**
   Controller services (such as connection pools and state stores) must be disabled.

   - Right-click the connector process group canvas and select **Disable all controller services**, or open **Controller Services** and disable them.
   - The migration wizard requires both processors stopped and controller services disabled.
4. **Revert any local changes:**
   The process group must match its versioned flow definition with no uncommitted local modifications.

   - Look at the version status icon displayed on the process group card. If local modifications were made, the process group displays an asterisk icon (\*).
   - Right-click the connector process group, select **Version** » **Revert local changes**, and confirm the revert.
   - Once reverted, the asterisk disappears.
5. **Upgrade to the latest connector version:**
   After reverting local changes, the connector must be on the latest version available in the registry.

   - If a red upgrade arrow icon appears next to the process group name, an update is available.
   - Right-click the process group, select **Version** » **Change version**, select the latest available version, and select **Change**.
   - Confirm that the process group now displays a green checkmark indicating it is up to date and clean.

Ineligible process groups don’t appear in the wizard. If your process group isn’t listed, verify that each step above has been completed.

### Drain the connector safely

Draining stops new data from queuing while letting already-queued data finish flushing to
Snowflake. The migration wizard requires this stopped-and-drained state before it lists the
connector as eligible. For the click-by-click stop-and-drain steps, see step 1 of the reinstall
procedure for your connector type: [PostgreSQL CDC](/user-guide/data-integration/openflow/connectors/postgres/maintenance#label-postgres-reinstall-connector)
or [MySQL CDC](/user-guide/data-integration/openflow/connectors/mysql/maintenance#label-mysql-reinstall-connector).

Warning

**Don’t empty or purge a queue to force it to drain** unless you’ve confirmed you don’t need the
data it holds, for example on a development or test connector where losing in-flight records is
acceptable. On a CDC connector, a queued FlowFile represents a change event already captured from
the source but not yet written to Snowflake. Emptying the queue discards those events permanently
and silently, with no way to recover them afterward.

If a queue won’t reach zero, look for a stuck downstream processor, a disabled or misconfigured
controller service, or a bulletin describing an error before assuming the connector is stuck.
Don’t try to work around a stuck queue by rewinding the source read position, for example
resetting to the earliest available binary log position: the queue holds events already captured
from the source, and rewinding doesn’t flush them. For PostgreSQL sources this is actively risky,
because the replication slot has already advanced past the queued events. Restarting capture
resumes after them, and they become unrecoverable without a new snapshot.

If you can’t get a queue to drain, fix the downstream issue causing the backup or contact
Snowflake Support before you continue with migration.

### Have Snowflake Secrets ready for sensitive properties

Sensitive properties (passwords, connection strings, API keys) don’t carry over automatically
from the gen 1 connector. You’ll re-map them in the install wizard. Openflow connectors require
secrets of `TYPE = GENERIC_STRING`. Create them before starting so you can complete the wizard
without interruption:

Copy code

```
CREATE SECRET my_db.my_schema.my_connector_password
  TYPE = GENERIC_STRING
  SECRET_STRING = '<password>';
```

Grant `READ` on the secret (and `USAGE` on its database and schema) to the runtime’s
`EXECUTE_AS_ROLE`. See
[Secrets in configuration](/user-guide/data-integration/openflow/gen2/configure-connector-sql#label-openflow-configure-connector-sql-secrets)
for full details and the `SECRET_REFERENCE` structure used in connector configuration.

## Starting scenarios

Find the scenario that matches your current state.

**You have gen 1 resources and are migrating for the first time.**
Migrate your deployment and runtimes first (see
[Migrate a gen 1 deployment and runtimes to gen 2](/user-guide/data-integration/openflow/gen2/migrate-deployment-runtime)), then return to this page to
migrate connectors.

**Your deployment and runtimes are already gen 2, but your connectors are still gen 1.**
Start directly with [Migrate a connector](#label-openflow-migrate-connector-steps) below.

**You need access to a gen 2 runtime to run the migration wizard but your role can’t see it.**
After a deployment/runtime migration, roles that previously had `MONITOR`, `USAGE`, or `OPERATE`
on a gen 1 runtime may lose access to the gen 2 runtime if they don’t have `USAGE` on the
database and schema the runtime is now scoped to. Have the runtime owner or an account admin
run:

Copy code

```
GRANT USAGE ON DATABASE <db_name> TO ROLE <your_role>;
GRANT USAGE ON SCHEMA <db_name>.<schema_name> TO ROLE <your_role>;
```

See [Migrate a gen 1 deployment and runtimes to gen 2](/user-guide/data-integration/openflow/gen2/migrate-deployment-runtime) for details.

## Migrate a connector

Migration is started by **creating a new gen 2 connector instance**, not from the existing
connector’s menu.

1. In the Openflow UI, navigate to the **Connector library** tab.
2. Click **Install** on the gen 2 version of the connector type that matches your gen 1 connector
   (indicated by a **gen 2** badge in the catalog). For example, if you have a gen 1 PostgreSQL CDC
   connector, install the gen 2 PostgreSQL CDC connector.
3. Complete the connector creation dialog. The new instance is created in `STOPPED` state.
4. The install wizard opens. If eligible gen 1 connectors are found on the same runtime, the
   wizard includes a **Migrate** step.
5. In the **Migrate** step, select your gen 1 connector from the table. The table shows only
   connectors that meet the eligibility requirements listed in
   [Before you migrate](#label-openflow-migrate-connector-prereqs).
6. Start the migration. The wizard:

   - Copies the connector’s component state to the new
     gen 2 connector instance.
   - Copies assets (JDBC drivers, keystores, custom binaries) where they can be located.
   - **Disables** the source gen 1 connector and **renames** it to
     `(Migrated) <original name>`. The source connector is not deleted. It stays on the
     runtime canvas as a safety net.
7. Continue through the remaining wizard steps:

   - **Re-map sensitive properties to Snowflake Secrets.** Properties that used parameter-context
     references in the gen 1 connector are not carried over automatically. Assign the
     corresponding Snowflake Secrets here.
   - **Re-attach any assets** that couldn’t be copied automatically, such as JDBC drivers or
     keystores (this is rare and only occurs if an asset was deleted from the runtime before
     migration).
   - Resolve any other prompts the wizard surfaces.
8. Run the wizard’s **Verify** step to confirm connectivity with the source system.
9. Apply the configuration and select **Start** to start the new gen 2 connector.

Warning

Once the gen 2 connector has started, do not re-enable or start the `(Migrated)` process group.
The gen 2 connector is now ingesting data from the source; restarting the gen 1 process group
creates a conflict and can cause duplicated, missing, or out-of-order data.

You can abandon migration from the wizard without starting the gen 2 connector.

Note

You can select **Skip** in the Migrate step at any time to abandon migration and complete the
wizard as a standard fresh install. Skipping doesn’t affect the source gen 1 connector. To
attempt migration again later, create a new gen 2 connector instance and return to step 1.

## After migration

### Monitor and verify the new connector

After starting the gen 2 connector, monitor it from the
[Openflow Connectors Dashboard](/user-guide/data-integration/openflow/connectors-dashboard)
or the **Installed Connectors** tab. Let it run through at least a few ingestion cycles before
considering the migration complete.

For gen 2 connector management (start, stop, remove), see
[Manage the gen 2 Openflow connector lifecycle](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle).

### Migrate alerts to the gen 2 connector

Alerts from the gen 1 connector aren’t migrated automatically. After the gen 2 connector is
running, open the **Observability** dashboard in the Snowsight UI and migrate those
connector-scoped alerts to the new connector. The install wizard also shows this reminder on the
migration success card, with a **Go to observability** link when it’s available.

### Clean up the gen 1 connector

Once the gen 2 connector is running correctly and you’re confident in it, delete the
`(Migrated)` process group from the runtime canvas:

1. Open the runtime canvas.
2. Find the entry named `(Migrated) <original name>`.
3. Confirm it’s still disabled (all processors stopped).
4. Delete it.

You can keep the `(Migrated)` process group on the canvas until you’re comfortable that the gen 2
connector is healthy. There’s no time limit. Just make sure you **don’t start it**.

## If connector migration fails

The recovery path depends on where in the process the failure occurred.

### The migration request failed before the gen 2 connector started ingesting

The gen 2 connector instance is in a partial state. Check whether the process group was disabled:

- **Source process group is NOT prefixed `(Migrated)`:** The backend didn’t reach the disable step.
  The process group is intact. Drop the gen 2 connector instance, create a new one, and attempt
  migration again.
- **Source process group IS prefixed `(Migrated)`:** The backend disabled the source but something failed
  afterward. Drop the gen 2 connector instance, create a new one, and run the migration wizard
  again. The disabled process group is still available as the migration source.

### The gen 2 connector was created successfully but fails some time after launch

Warning

Do **not** re-enable or start the `(Migrated)` process group. Once the gen 2 connector has been
ingesting data, its stateful processors (for example, CDC offset tracking) are ahead of the
disabled gen 1 process group. Restarting the gen 1 process group creates a conflict over the source state and can
cause data loss or duplication.

Recover the gen 2 connector instead:

- **Transient failure** (network error, temporary source outage): restart the gen 2 connector
  from the **Installed Connectors** tab or with `ALTER OPENFLOW CONNECTOR ... START`.
- **Configuration issue** (wrong credentials, missing secret, expired certificate): fix the
  property or Snowflake Secret and restart.
- **Can’t resolve the issue:** contact Snowflake Support. Do not manually re-enable the gen 1
  process group.

## Troubleshooting

Use this table to diagnose common migration problems:

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| **Migrate** step doesn’t appear in the install wizard | No eligible process groups on the runtime, or migration isn’t supported for this connector type yet | Confirm the process group is stopped, drained, has no local changes, and is on the same runtime. See [Supported connectors and their release stage](/user-guide/data-integration/openflow/gen2/migrate-connector#label-openflow-migrate-connector-availability) for which connector types support migration. |
| A gen 1 connector doesn’t appear in the Migrate step table | The process group is running, has queued data, has uncommitted local changes, or is not on the same runtime as the new gen 2 connector | Stop the process group, wait for all queues to drain, and revert any local changes. If the process group is on a different runtime, you need to create the gen 2 connector on that same runtime. Create a new gen 2 connector instance on the correct runtime and try the migration wizard again. |
| Can’t access or select the target gen 2 runtime | Role lacks `USAGE` on the runtime, or on the runtime’s database and schema | Ask the runtime owner or an account admin to grant `USAGE` on the runtime, its database, and its schema to your role. See the scenario in [Starting scenarios](#label-openflow-migrate-connector-scenarios). |
| Migration request fails with a connectivity error | Temporary cluster node disconnection | Use the wizard’s **Retry** option. If retries continue to fail, create a new gen 2 connector instance and run the wizard again. |
| Sensitive property shows as unresolved after migration | The gen 1 connector used a parameter-context reference that didn’t carry over | Assign a Snowflake Secret for the property in the wizard’s configuration steps. |
| Asset missing after migration | A driver, keystore, or binary was deleted from the runtime before migration ran | Re-upload the asset binary through the per-property upload prompt in the wizard. |
| gen 2 connector fails after starting with source connection errors | Source temporarily unavailable, or credentials changed since the Verify step ran | Check the Connectors Dashboard for the error message. If the source is temporarily down, restart the connector once it’s back. If credentials were rotated, update the Snowflake Secret and restart. Do not re-enable the gen 1 process group. |

Expand

Show lessSee more
