# Configure a connector with the setup wizard

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The Openflow connector setup wizard provides a guided, step-by-step experience for configuring
gen 2 connectors. The wizard validates your inputs at each step so
you can identify and fix configuration issues before completing the setup.

This topic applies to gen 2 connectors only. For gen 1 catalog connectors, see
[Openflow connectors](/user-guide/data-integration/openflow/connectors/about-openflow-connectors).
For an overview of gen 1 vs gen 2, see
[Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations).

## Supported connectors

The following **gen 2** connectors are available in the catalog:

- PostgreSQL CDC
- MySQL and MariaDB CDC

## Prerequisites

Before you start the setup wizard, make sure the following requirements are met:

- You have a **gen 2** Openflow deployment (BYOC or Openflow - Snowflake Deployment) with at least one gen 2 runtime.
  The wizard configures gen 2 connectors, which run on gen 2 runtimes only. To create deployment and runtime resources,
  see [Quickstart: gen 2 Openflow](/user-guide/data-integration/openflow/gen2/quickstart). For BYOC cloud installation, Snowflake deployment
  networking, deployment setup, and runtime parameters, see [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc),
  [Set up Openflow - Snowflake Deployment - Task overview](/user-guide/data-integration/openflow/setup-openflow-spcs), or
  [Set up Openflow - Snowflake Deployment: Create runtime](/user-guide/data-integration/openflow/setup-openflow-spcs-create-runtime) as applicable. If
  you are unsure whether your resources are gen 1 or gen 2, see
  [Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations).
- For Openflow - Snowflake Deployments, your PostgreSQL database must be reachable through an
  [external access integration](/developer-guide/external-network-access/external-network-access-overview) (EAI)
  that references a [network rule](/sql-reference/sql/create-network-rule) permitting egress to your
  PostgreSQL hostname and port (the connector uses a customer-specific endpoint; see
  [PostgreSQL](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list#label-openflow-domains-used-by-openflow-connectors-postgresql)).
  Grant `USAGE` on the EAI to the runtime’s `EXECUTE_AS_ROLE` (see
  [Create an execute-as role](/user-guide/data-integration/openflow/gen2/quickstart#label-openflow-gen2-quickstart-execute-as-role)).
  For setup steps, see
  [Configure external access](/user-guide/data-integration/openflow/gen2/quickstart#label-openflow-gen2-quickstart-eai) in the gen 2
  quickstart or [Set up Openflow - Snowflake Deployment: Configure allowed domains for Openflow connectors](/user-guide/data-integration/openflow/setup-openflow-spcs-sf-allow-list).
  If you use Openflow BYOC, configure outbound connectivity in your cloud environment so the runtime can reach
  PostgreSQL; Snowflake EAIs are not used in that deployment model.
- Any required secrets (for example, database passwords or API keys) are created as
  [Snowflake secrets](/sql-reference/sql/create-secret) and accessible to the runtime’s
  `EXECUTE_AS_ROLE` (see
  [Create an execute-as role](/user-guide/data-integration/openflow/gen2/quickstart#label-openflow-gen2-quickstart-execute-as-role)).
  You can also source secret values from an
  [external secret provider](/user-guide/data-integration/openflow/security/external-secret-providers).
- You have `CREATE OPENFLOW CONNECTOR` on the schema that the runtime is in, `USAGE` on the
  runtime, and `USAGE` on the runtime’s database and schema.
- You have the required permissions for the connector you want to install, and have
  completed any connector-specific source database prerequisites:
  [PostgreSQL CDC](/user-guide/data-integration/openflow/connectors/postgres/setup#source-database-setup) |
  [MySQL and MariaDB CDC](/user-guide/data-integration/openflow/connectors/mysql/setup#source-database-setup).
  For Snowflake account setup (destination database, warehouse, and secrets), follow the
  [Snowflake account setup](/user-guide/data-integration/openflow/connectors/postgres/setup#snowflake-account-setup)
  on those pages.

## Create and configure a connector

1. In the navigation menu, select **Ingestion** » **Openflow**.
2. Select **Launch Openflow**.
3. Navigate to the **Connector library** tab.
4. Find a **gen 2** connector in the catalog.
5. Select a runtime to install the connector to. The list is filtered based on the
   runtime size requirements needed to run the connector.
6. Select **Install**.
7. Complete the wizard steps. The specific steps vary depending on the connector you selected.
   Documentation for every step is present within the wizard.
8. Upon completion, select **Create Connector**.
9. You’re redirected to the **Installed Connectors** page. Once the connector has finished
   installing, select **Start** from the menu for your connector to start moving data.

At any point during the wizard, you can select **Save and Close** to preserve your configuration
changes without applying them to the connector. To apply your saved changes later, select **Edit**
from the menu for that connector on the **Installed Connectors** tab, step through the wizard to
the end, and select **Apply**.

To create and configure the same connector types with SQL instead of the wizard, see
[Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql).

## Edit an existing connector

To edit a connector that you’ve already created, go to the **Installed Connectors** tab and
select **Edit** from the menu for that connector. This reopens the setup wizard with your
existing configuration.

## Input validation

The wizard provides a button that allows you to validate your input at each step. Validation checks include:

- **Connection tests**: The wizard attempts to connect to your data source using the provided
  credentials and displays the result.
- **Permission checks**: The wizard verifies that the specified Snowflake user has the required
  privileges on the target database, schema, and table.
- **Format validation**: The wizard checks that values such as hostnames, ports, and database
  names are in the expected format.

If a validation check fails, the wizard highlights the field and displays a message explaining
the issue. You can move to the next step even when intermediate validation fails; only the final
validation before **Create Connector** (or **Apply**) must pass.

## Troubleshooting

When you select **Verify** and validation fails, the wizard displays troubleshooting information
directly in the UI explaining what went wrong and how to fix it. The panel on the right side of the wizard also contains detailed information about what is required for each property.

## Verify ingestion (dashboard, destination database, read-only canvas)

After you **Start** the connector, confirm that data is flowing:

- Use the [Openflow Connectors Dashboard](/user-guide/data-integration/openflow/connectors-dashboard)
  (**Ingestion** » **Openflow** » **Connector Observability**) for health, throughput, and errors.
- In **Snowflake**, query the **destination database** (the tables or schemas the connector writes to) to
  verify that new rows or changes are arriving as you expect.
- Open the **runtime canvas** to inspect processors, queues, FlowFiles, and bulletins for your connector’s
  process group—a **read-only** operational view. From the dashboard, select **Go to canvas** for that
  connector; or open the canvas from **Runtimes** in Openflow. You **cannot** configure the connector on
  the canvas for setup wizard connector types; use **Installed Connectors** » **Edit** or the
  connector API for any configuration changes.

For starting and stopping ingestion, removal actions, and how the canvas compares to catalog-installed
connectors, see [Manage the gen 2 Openflow connector lifecycle](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle).

## Next steps

After you configure a connector with the wizard, you can:

- [Manage the gen 2 connector lifecycle (start, stop, removal)](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle)
- [Monitor connector health and performance](/user-guide/data-integration/openflow/connectors-dashboard)
- [Manage your Openflow deployment](/user-guide/data-integration/openflow/manage)
- [Troubleshoot Openflow issues](/user-guide/data-integration/openflow/troubleshoot)
