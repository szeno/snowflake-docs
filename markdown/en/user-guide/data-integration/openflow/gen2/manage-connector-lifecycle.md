# Manage the gen 2 Openflow connector lifecycle

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

This topic describes how to manage the **gen 2** Openflow connector lifecycle: **start and stop**
ingestion and **remove** a gen 2 connector after it is created. To monitor connector health,
throughput, and ingestion status, use the
[Openflow Connectors Dashboard](/user-guide/data-integration/openflow/connectors-dashboard).
For gen 1 connectors, follow the lifecycle guidance in each connector’s public setup topic. See
[Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations) for how to tell gen 1 resources from gen 2.

These tasks apply no matter how the gen 2 connector was created: using the
[Configure a connector with the setup wizard](/user-guide/data-integration/openflow/gen2/setup-connector-wizard), [Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql),
or other supported SQL/API automation.

## Start and stop data movement

After a gen 2 connector is installed on a runtime, start it to begin reading from the source and
writing to Snowflake. Use **Start** from the connector’s menu on the **Installed Connectors** tab.

Use **Stop** when you need to pause ingestion—for example before maintenance, upgrades described in your
connector’s documentation, or before removal. Stopping leaves the connector installed but idle.

Tip

Some connectors retain external resources while stopped (for example, database replication slots).
Do not leave connectors stopped for long periods on busy sources unless you understand the impact; see
your connector’s setup or maintenance topic.

For **gen 2** connectors, use **Start** and **Stop** from the connector menu on
**Installed Connectors**, or run `ALTER OPENFLOW CONNECTOR ... START` or `STOP` with SQL. Do
not use the canvas for configuration or processor-level start/stop. See
[ALTER OPENFLOW CONNECTOR](/sql-reference/sql/alter-openflow-connector) for syntax and wait functions.

## Remove a connector

Gen 2 connector removal follows **stop** → **terminate** → **drop**. **`TERMINATE` drains**
in-flight data before removal. Complete each step before starting the next.

In UI-driven workflows, wait for each step to finish before starting the next. In scripts, call
`SYSTEM$WAIT_FOR_STABLE_OPENFLOW_CONNECTORS` after asynchronous `ALTER` commands. See
[SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_CONNECTORS](/sql-reference/functions/system_wait_for_stable_openflow_connectors).

### Remove a connector (UI)

1. From the **Installed Connectors** tab, open the connector **menu** and select **Stop**.
2. From the connector **menu** on **Installed Connectors**, select **Delete** (terminates the
   connector and drains in-flight data).
3. From the same menu, select **Drop**.

### Remove a connector (SQL)

**Delete** in the UI corresponds to `ALTER OPENFLOW CONNECTOR ... TERMINATE`; **Drop** corresponds
to `DROP OPENFLOW CONNECTOR`. `DROP` requires `OWNERSHIP` on the connector.

Copy code

```
ALTER OPENFLOW CONNECTOR my_db.my_schema.my_connector STOP;
SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_CONNECTORS(600, 'my_db.my_schema.my_connector');

ALTER OPENFLOW CONNECTOR my_db.my_schema.my_connector TERMINATE;
SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_CONNECTORS(600, 'my_db.my_schema.my_connector');

DROP OPENFLOW CONNECTOR my_db.my_schema.my_connector;
```

For full command syntax, privileges, and additional `ALTER` options, see
[ALTER OPENFLOW CONNECTOR](/sql-reference/sql/alter-openflow-connector).

Caution

**Delete**, **Drop**, `TERMINATE`, and `DROP OPENFLOW CONNECTOR` are irreversible for Openflow
entities. Snowflake does not support undrop for these objects. These steps do not remove destination
tables or external resources (such as PostgreSQL replication slots). Read confirmation dialogs
carefully.

For source-specific cleanup after removal (for example PostgreSQL replication slots), see **Stop or delete
the connector** in [Set up the Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/setup) and analogous
sections for other connectors.
