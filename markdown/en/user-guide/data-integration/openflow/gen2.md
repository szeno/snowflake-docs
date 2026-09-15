# Second generation Openflow objects and interfaces

Gen 2 Openflow is available on AWS, Azure, and GCP. Gen 2 deployment and runtime SQL objects are
generally available. Gen 2 connector configuration (the setup wizard, SQL/stage-based
configuration, and supported connectors) remains in Public Preview.

Second-generation (**gen 2**) Openflow **deployments**, **runtimes**, and **connectors** are
first-class Snowflake objects. You can use the Openflow UI or SQL commands to work with the same
underlying objects.

Gen 1 and gen 2 resources can coexist in the same account:

- **New deployments are gen 2 only.** You can no longer create new gen 1 deployments (BYOC or
  Snowflake). All new deployments must use `CREATE OPENFLOW DEPLOYMENT`.
- **Runtimes inherit the generation of their parent deployment.** New runtimes on a gen 1
  deployment are gen 1; new runtimes on a gen 2 deployment are gen 2.
- **Gen 2 runtimes support both gen 1 and gen 2 connectors.** Both types can coexist on the same
  gen 2 runtime.
- **Gen 1 runtimes support gen 1 connectors only.** Don’t install gen 2 connectors on a gen 1
  runtime.
- **Existing gen 1 resources stay gen 1** and continue to work unchanged. Migration from gen 1 to gen 2 is available in Private Preview; contact your Snowflake account representative to be included.

Gen 2 introduces SQL-first lifecycle management, a revised security model, and connectors managed
as [File Based Entities (FBEs)](/user-guide/data-integration/openflow/gen2/connector-versioning) with versioned
configuration.

## Start here

If you are new to gen 2 Openflow, read these topics in order:

1. [Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations) — Understand gen 1 vs gen 2 for deployments, runtimes, and connectors,
   and which documentation set applies to each.
2. [About Openflow](/user-guide/data-integration/openflow/about) — Review Openflow concepts shared by gen 1 and
   gen 2 (deployment types, architecture, use cases).
3. [Quickstart: gen 2 Openflow](/user-guide/data-integration/openflow/gen2/quickstart) — Set up privileges and create your first gen 2 deployment, runtime, and connector.
4. **Migrating from gen 1?** Migration from gen 1 to gen 2 is available in Private Preview;
   contact your Snowflake account representative to be included.
5. [Configure a connector with the setup wizard](/user-guide/data-integration/openflow/gen2/setup-connector-wizard) — Install and configure a gen 2 connector with
   the setup wizard (Public Preview).
6. [Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql) — Create and configure a gen 2 connector with SQL and stage commands (Public Preview).

## Known limitations

For how gen 2 differs from gen 1 in supported operations and lifecycle, see
[Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations).

**Quotas**

- **BYOC deployments:** At most 20 per account (enforced by Openflow and Snowflake).
- **Snowflake deployments:** At most three per account.
- **Runtimes:** At most 100 per deployment. You can hit other limits before that maximum—for
  example, 50 EC2 nodes per node type on a BYOC deployment, or block storage quota on a Snowflake
  deployment when other applications consume storage.
- A runtime can have at most 50 nodes. This applies to both generations (BYOC node groups and Snowflake
  deployment compute pools).

**Diagnostics**

- Gen 2 runtime diagnostic bundles can be created from SQL or the Openflow UI. Snowflake
  **deployment** diagnostic bundles (not scoped to a single runtime) are also supported from SQL.
  For BYOC troubleshooting, you can also run `./diagnostics.sh` on the deployment agent instance;
  see [Troubleshoot Openflow](/user-guide/data-integration/openflow/troubleshoot).

**Operations shared with gen 1**

- `GRANT OWNERSHIP` on gen 2 deployments, runtimes, or connectors can break underlying
  functionality today. Avoid ownership transfer until an upcoming update; see
  [Transferring OWNERSHIP](/user-guide/data-integration/openflow/gen2/openflow-generations#label-openflow-generations-ownership-transfer) in [Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations).
- For BYOC deployments, installation and upgrade documentation can only be downloaded from the UI;
  upgrades are not automatic. See [Manage Openflow](/user-guide/data-integration/openflow/manage).

**Platform integration**

- Object tagging (`ALTER ... SET TAG`) isn’t supported on gen 2 deployments, runtimes, or connectors.
- Gen 2 deployments, runtimes, and connectors aren’t tracked by `ACCOUNT_USAGE.OBJECT_DEPENDENCIES`,
  `ACCOUNT_USAGE.ACCESS_HISTORY`, or `GET_LINEAGE` (including the Snowsight **Lineage** tab).
- `CREATE ... CLONE` isn’t supported for gen 2 deployments, runtimes, or connectors.
- `CREATE OR REPLACE` and `CREATE OR ALTER` aren’t supported for gen 2 deployments, runtimes, or
  connectors. Use `CREATE ... IF NOT EXISTS` and `ALTER ... IF EXISTS` instead.
- Gen 2 deployments, runtimes, and connectors can’t be added to a share.
- Gen 2 deployments, runtimes, and connectors aren’t supported entity types in Database Change
  Management (DCM) projects.

**Cost management and availability**

- Resource monitors don’t support gen 2 Snowflake deployment compute pools.
- Gen 2 deployments and runtimes can’t be added to a [budget](/user-guide/budgets).
- Gen 2 deployments can’t be added to a replication or failover group. Gen 2 runtimes and
  connectors aren’t supported for database replication either: if their containing database is
  replicated, they’re skipped and won’t exist in the target account after failover. There’s no
  built-in cross-region or cross-cloud disaster recovery for gen 2 objects.

**Dropping gen 2 objects**

- `DROP OPENFLOW DEPLOYMENT` and `DROP OPENFLOW RUNTIME` are irreversible. Snowflake doesn’t
  support undrop for these objects, the same restriction documented for connectors; see
  [Remove a connector](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle#label-openflow-connector-lifecycle-remove).

**Setup wizard (Public Preview)**

- Private link is not supported in the setup wizard flow. Private link for deployments and runtime UI
  access is supported separately; see
  [Set up PrivateLink UI access in Openflow - Snowflake Deployments](/user-guide/data-integration/openflow/setup-openflow-spcs-configure-pr-ui).

## Gen 2 documentation

| Topic | Description |
| --- | --- |
| [Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations) | Compare gen 1 and gen 2 deployments, runtimes, and connectors; authorization and lifecycle differences; how to identify resources and which documentation to follow. |
| [Quickstart: gen 2 Openflow](/user-guide/data-integration/openflow/gen2/quickstart) | Prerequisites, privilege grants, and example commands to create gen 2 resources. |
| [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning) (Public Preview) | Versioned configuration for SQL, Git, and automation (optional background if you use the UI only). Stage access and Git workflow for reusing validated configs. |
| [Configure a connector with the setup wizard](/user-guide/data-integration/openflow/gen2/setup-connector-wizard) (Public Preview) | Step-by-step setup wizard for gen 2 connectors. |
| [Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql) (Public Preview) | Create and configure gen 2 connectors with SQL and stage commands (programmatic setup). |
| [Manage the gen 2 Openflow connector lifecycle](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle) (Public Preview) | Start, stop, and remove gen 2 connectors after installation. |
| [Monitor connectors using the Openflow Connectors Dashboard](/user-guide/data-integration/openflow/connectors-dashboard) | Monitor gen 2 connector health, throughput, and ingestion status. |
| Migrate deployment and runtimes (Private Preview) | Migrate an existing gen 1 deployment and all its runtimes to gen 2 objects. Covers prerequisites, the migration wizard, post-migration access grants, rollback constraints, and troubleshooting. Contact your Snowflake account representative for access. |
| Migrate connectors (Private Preview) | Migrate individual gen 1 connectors to gen 2 connector instances. Covers prerequisites, Snowflake Secrets rewiring, the disabled source connector, and failure recovery. Contact your Snowflake account representative for access. |

Expand

Show lessSee more

## Gen 1 documentation

Gen 1 Openflow resources continue to use the public Openflow documentation. When you work with gen 1
deployments, runtimes, or catalog-installed connectors, follow these topics:

- [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc) and
  [Set up Openflow - Snowflake Deployment - Task overview](/user-guide/data-integration/openflow/setup-openflow-spcs) — Manage gen 1 deployments; create gen 1 runtimes.
- [Set up Openflow - Snowflake Deployment: Create runtime](/user-guide/data-integration/openflow/setup-openflow-spcs-create-runtime) — Create gen 1
  runtimes.
- [Openflow connectors](/user-guide/data-integration/openflow/connectors/about-openflow-connectors) — Install and
  configure gen 1 connectors with **Install** or **Import from Registry** on the runtime canvas.
- [Manage Openflow](/user-guide/data-integration/openflow/manage) — Manage gen 1 deployments and runtimes in the
  UI.

For source-specific setup (for example, preparing PostgreSQL for CDC), use the connector setup topic
in the public docs for gen 1 and gen 2 connectors alike. Gen 2 connector topics link to those
instructions where the source configuration is the same.
