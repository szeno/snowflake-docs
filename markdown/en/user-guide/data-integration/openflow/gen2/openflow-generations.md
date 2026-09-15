# Openflow gen 1 and gen 2

Gen 2 deployment and runtime SQL objects are generally available on AWS, Azure, and GCP. Gen 2
connector configuration remains in Public Preview (see [Connectors](/user-guide/data-integration/openflow/gen2/openflow-generations#label-openflow-generations-connectors)).

Enabled accounts can use gen 1 and gen 2 Openflow resources:

- **First generation (gen 1)** — Runtimes are created from the Openflow UI on an existing gen 1
  deployment. New gen 1 deployments can no longer be created. Connectors are Apache NiFi process
  groups installed from the connector catalog with **Install** (Openflow UI) and configured on
  the runtime canvas.
- **Second generation (gen 2)** — Deployments, runtimes, and connectors are first-class Snowflake objects
  created with SQL commands (`CREATE OPENFLOW DEPLOYMENT`, `CREATE OPENFLOW RUNTIME`,
  `CREATE OPENFLOW CONNECTOR`) or by installing from the connector catalog in the Openflow UI.
  Gen 2 connectors are [File Based Entities (FBEs)](/user-guide/data-integration/openflow/gen2/connector-versioning) with versioned
  configuration and can use the setup wizard.

Any newly created Openflow deployment is gen 2. Existing gen 1 deployments stay gen 1 until you
migrate them, and new runtimes on a gen 1 deployment are gen 1. Gen 2 runtimes support both gen 1
and gen 2 connectors — you do not need to wait for a gen 2 version of a connector to use it on a
gen 2 runtime. This topic explains how gen 1 and gen 2 differ and which documentation to follow
for each.

## Overview

Gen 1 and gen 2 resources share the same Openflow platform concepts—BYOC and Openflow - Snowflake Deployment deployment
types, NiFi-based data movement, and Snowflake as a destination—but they differ in how objects are
created, secured, and managed.

Gen 2 is the long-term Openflow management model: SQL-accessible objects, granular
privileges, and connectors with committed configuration versions. Gen 1 resources
you already have continue to work unchanged. New gen 2 resources are created separately and follow
Gen 2 lifecycle rules.

## Why migrate to gen 2?

**Manage everything with SQL**

Gen 2 deployments, runtimes, and connectors are first-class Snowflake objects. Create, configure,
start, stop, and remove them with SQL commands (`CREATE OPENFLOW DEPLOYMENT`, `ALTER OPENFLOW CONNECTOR ... START`, and so on) or the Openflow UI. Because these are standard SQL operations, you
can programmatically schedule runtime suspends during off-hours to reduce total cost of ownership.

**CI/CD and infrastructure as code**

Gen 2 connectors store configuration as versioned files
([File Based Entities](/user-guide/data-integration/openflow/gen2/connector-versioning)). Draft changes, commit
them, and roll back to a previous version. Reuse validated configs across environments through Git
workflows, promote configurations from dev to production without click-ops, and integrate connector
management into CI/CD pipelines. Gen 2 objects are also supported by the Snowflake Terraform
provider for infrastructure-as-code workflows.

**Setup wizard for guided installation**

Gen 2 connectors can be installed through a step-by-step setup wizard that validates connectivity
and configuration before starting. Gen 1 connector installation requires manual configuration of
processors, controller services, and parameter contexts on the canvas.

**Granular access control**

Gen 2 runtimes and connectors are schema-scoped objects with standard Snowflake RBAC. Control who
can see deployments, operate runtimes, or manage connectors using `GRANT USAGE` and `GRANT OPERATE`.

**To get started:** Migration from gen 1 to gen 2 is available in Private Preview. Contact your
Snowflake account representative to be included.

## Comparison by resource type

### Deployments

|  | gen 1 | gen 2 |
| --- | --- | --- |
| **Creation** | Not available — new gen 1 deployments can’t be created | `CREATE OPENFLOW DEPLOYMENT` (UI or SQL) |
| **Required privilege** | N/A | `CREATE OPENFLOW DEPLOYMENT` on the account |
| **Documentation** | [Set up Openflow - BYOC](/user-guide/data-integration/openflow/setup-openflow-byoc), [Set up Openflow - Snowflake Deployment - Task overview](/user-guide/data-integration/openflow/setup-openflow-spcs) | [Quickstart: gen 2 Openflow](/user-guide/data-integration/openflow/gen2/quickstart), [Second generation Openflow objects and interfaces](/user-guide/data-integration/openflow/gen2/index) |
| **Event table** | Set on the data plane integration (`ALTER OPENFLOW DATA PLANE INTEGRATION ... SET EVENT_TABLE`). Value stored on the integration at creation. View with `DESCRIBE OPENFLOW DATA PLANE INTEGRATION`. [[Optional] Configure an Openflow-specific event table](/user-guide/data-integration/openflow/setup-openflow-spcs-deployment#label-openflow-spcs-event-table) | Optional `EVENT_TABLE` on the deployment object. When unset, inherits the account-level event table. View with `SHOW PARAMETERS LIKE 'EVENT_TABLE' IN OPENFLOW DEPLOYMENT <name>`. [CREATE OPENFLOW DEPLOYMENT](/sql-reference/sql/create-openflow-deployment) |
| **Availability** | Existing gen 1 deployments continue to work unchanged. New gen 1 deployments can’t be created. | All new deployments are gen 2, created with `CREATE OPENFLOW DEPLOYMENT`. |

Expand

Show lessSee more

Note

**Snowflake deployment limit:** Each account supports up to three Snowflake Openflow
deployments. Gen 1 and gen 2 deployments share this limit; `CREATE OPENFLOW DEPLOYMENT WITH DEPLOYMENT_TYPE = SNOWFLAKE` fails when the account already has three Snowflake deployments,
regardless of generation.

### Runtimes

|  | gen 1 | gen 2 |
| --- | --- | --- |
| **Creation** | `CREATE OPENFLOW RUNTIME INTEGRATION` (UI or SQL) | `CREATE OPENFLOW RUNTIME ... IN DEPLOYMENT ...` (UI or SQL) |
| **Account- or schema-level object** | Account-level `OPENFLOW RUNTIME INTEGRATION` object | Schema-level object; fully qualified name `<database>.<schema>.<runtime_name>`. Read and write access during connector execution is dictated by the runtime’s `EXECUTE_AS_ROLE`, not by the schema where the runtime object lives. |
| **Required privilege** | `CREATE OPENFLOW RUNTIME INTEGRATION` on the account | `CREATE OPENFLOW RUNTIME` on the target schema, `USAGE` on the containing database, and `USAGE` on the deployment (schema owners can create without the explicit `CREATE OPENFLOW RUNTIME` grant) |
| **Runtime object privileges** | `USAGE`, `OPERATE`, or `MONITOR` on the `OPENFLOW RUNTIME INTEGRATION` object | `USAGE`, `OPERATE`, or `MONITOR` on the runtime, and `USAGE` on its database and schema |
| **Deletion** | Suspend, then delete from the UI (see [Runtime deletion workflow](#label-openflow-generations-runtime-deletion)) | **UI:** **Suspend** → **Delete** → **Drop** from the runtime menu on the **Runtimes** tab (see [Runtime deletion workflow](#label-openflow-generations-runtime-deletion)). **SQL:** `ALTER OPENFLOW RUNTIME ... SUSPEND` → `TERMINATE` → `DROP` |
| **Documentation** | [Set up Openflow - Snowflake Deployment: Create runtime](/user-guide/data-integration/openflow/setup-openflow-spcs-create-runtime), [Manage Openflow](/user-guide/data-integration/openflow/manage) | [Quickstart: gen 2 Openflow](/user-guide/data-integration/openflow/gen2/quickstart), [Second generation Openflow objects and interfaces](/user-guide/data-integration/openflow/gen2/index) |
| **Generation** | Determined by the parent deployment. All runtimes added to a gen 1 deployment are gen 1. | Determined by the parent deployment. All runtimes added to a gen 2 deployment are gen 2. |

Expand

Show lessSee more

### Connectors (Public Preview)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

|  | gen 1 | gen 2 |
| --- | --- | --- |
| **Creation** | Install from connector catalog with **Install** (Openflow UI), or import from the registry on the runtime canvas (see [Coexistence](#label-openflow-generations-coexistence)) | **Openflow UI:** install from connector catalog (**gen 2** entries; setup wizard). **SQL:** `CREATE OPENFLOW CONNECTOR ... FROM DEFINITION` (see [Quickstart: gen 2 Openflow](/user-guide/data-integration/openflow/gen2/quickstart), [Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql)). To reuse a validated configuration, see [Create from a known configuration](/user-guide/data-integration/openflow/gen2/connector-versioning#label-openflow-fbe-git-create) in [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning). |
| **Object type** | NiFi process group on the runtime canvas (not a separate Snowflake object) | Schema-level `OPENFLOW CONNECTOR` [File Based Entity (FBE)](/user-guide/data-integration/openflow/gen2/connector-versioning) with versioned stage configuration |
| **Configuration** | Runtime canvas: parameter contexts, controller services, processors | Setup wizard, **Installed Connectors** » **Edit**, or SQL/stage commands (`PUT`/`COMMIT` on the connector’s live version). See [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning). |
| **Canvas** | Full read/write configuration surface | Read-only for gen 2 connectors; use **Installed Connectors** » **Edit** or SQL/API for configuration changes |
| **Lifecycle** | Start/stop processors on the canvas; remove via canvas and UI steps documented per connector | **UI:** **Start** / **Stop** from **Installed Connectors**; remove with **Stop** → **Delete** → **Drop** (see [Manage the gen 2 Openflow connector lifecycle](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle)). **SQL:** `ALTER OPENFLOW CONNECTOR ... START|STOP|TERMINATE`; `DROP` after terminate. |
| **Documentation** | [Openflow connectors](/user-guide/data-integration/openflow/connectors/about-openflow-connectors) and connector-specific setup topics | [Configure a connector with the setup wizard](/user-guide/data-integration/openflow/gen2/setup-connector-wizard), [Manage the gen 2 Openflow connector lifecycle](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle), [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning) |

Expand

Show lessSee more

## Authorization differences

### USAGE on a deployment does not grant visibility on runtimes

In gen 1, users with `USAGE` on a deployment can see its runtimes.

In gen 2, `USAGE` on a deployment does **not** grant access to runtimes in that deployment. To
access or manage a runtime, the user must have `USAGE`, `OPERATE`, or `MONITOR` granted
**directly on the runtime**, and `USAGE` on the runtime’s database and schema.

### Users must have a privilege on a deployment to see it

In gen 1, all users can see all deployments in the account.

In gen 2, a user must hold a role with a qualifying privilege on the deployment to see it in
listings. If secondary roles are enabled, secondary roles are considered when determining deployment
visibility.

### Runtime object privileges

Gen 1 runtimes are represented by account-level `OPENFLOW RUNTIME INTEGRATION` objects. Required
privileges on that integration object are `USAGE`, `OPERATE`, or `MONITOR`.

Gen 2 runtimes are schema-level objects. Required privileges are:

- `USAGE`, `OPERATE`, or `MONITOR` on the runtime object itself, **and**
- `USAGE` on the runtime’s database and schema

### Connector privileges (Public Preview)

Most connector operations derive privileges from the parent runtime. If you have `USAGE` on the
runtime, you can start, stop, configure, and terminate connectors in that runtime. `OWNERSHIP` on
the connector object itself is required for metadata changes, rename, and `DROP`.

### Transferring OWNERSHIP

`GRANT OWNERSHIP` on gen 2 Openflow deployments, runtimes, or connectors can break underlying
functionality today (for example, deployment agent credentials or runtime control-plane bindings).
The command is accepted in SQL, but **avoid transferring ownership** until an upcoming update
addresses this behavior.

## Behavior differences

### Runtime deletion workflow

Before you delete a runtime in either generation, stop the connectors in that runtime.

Gen 1 runtimes follow this workflow:

Copy code

```
ACTIVE → (stop connectors) → (suspend) → SUSPENDED → (delete from UI) → removed
```

Gen 2 runtimes follow this workflow:

Copy code

```
ACTIVE → (stop connectors) → (suspend) → SUSPENDED → (terminate) → TERMINATED → (drop) → removed
```

`ALTER OPENFLOW RUNTIME ... TERMINATE` drains in-flight connector data before removal. Use
`TERMINATE FORCE` to purge queues instead of draining when you accept possible data loss.

From the UI:

1. Stop connectors in the runtime.
2. Select **Launch Openflow**, open the **Runtimes** tab, and open the runtime **menu**.
3. Select **Suspend**.
4. From the same menu, select **Delete** (terminates the runtime).
5. From the same menu, select **Drop**.

From SQL:

Copy code

```
ALTER OPENFLOW RUNTIME my_db.my_schema.my_runtime SUSPEND;
SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_RUNTIMES(600, 'my_db.my_schema.my_runtime');

ALTER OPENFLOW RUNTIME my_db.my_schema.my_runtime TERMINATE;
SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_RUNTIMES(600, 'my_db.my_schema.my_runtime');

DROP OPENFLOW RUNTIME my_db.my_schema.my_runtime;
```

In UI-driven workflows, wait for each step to finish before starting the next. In scripts, call
`SYSTEM$WAIT_FOR_STABLE_OPENFLOW_*` after asynchronous `ALTER` commands. See
[SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_DEPLOYMENTS](/sql-reference/functions/system_wait_for_stable_openflow_deployments), [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_RUNTIMES](/sql-reference/functions/system_wait_for_stable_openflow_runtimes), [SYSTEM$WAIT\_FOR\_STABLE\_OPENFLOW\_CONNECTORS](/sql-reference/functions/system_wait_for_stable_openflow_connectors).

### Connector deletion workflow (Public Preview)

**gen 1** connectors are NiFi process groups on the runtime canvas. They are not `OPENFLOW CONNECTOR`
objects and cannot be removed with `ALTER OPENFLOW CONNECTOR` or `DROP OPENFLOW CONNECTOR`. Stop
ingestion and remove the process group using connector-specific steps on the canvas and in that
connector’s public setup or maintenance topic.

**gen 2** connectors are first-class Snowflake objects removed with **stop** → **terminate** →
**drop**. Use **Start** / **Stop** on **Installed Connectors** or
`ALTER OPENFLOW CONNECTOR ... START|STOP` for day-to-day control; use **Delete** / **Drop** or
`TERMINATE` / `DROP OPENFLOW CONNECTOR` for removal. UI **Delete** maps to `TERMINATE`; UI
**Drop** maps to `DROP OPENFLOW CONNECTOR`. **`TERMINATE`** drains in-flight data before removal.

For full UI and SQL removal steps, wait functions, and cleanup guidance, see
[Manage the gen 2 Openflow connector lifecycle](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle).

### Gen 2 connector configuration (Public Preview)

Gen 1 connectors are configured on the runtime canvas: parameter contexts, controller services, and
processors, following that connector’s public setup documentation.

Gen 2 connectors use versioned configuration (see [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning)). A connector in
**Draft** state must be committed before it can start. The UI shows **Edits not applied** when a live
version exists alongside a committed default version.

For gen 2 connectors, the runtime canvas is read-only for configuration. Use
**Installed Connectors** » **Edit**, the setup wizard, or SQL/API commands to change settings.

## How to identify gen 1 and gen 2 resources

Use the following checks when you are unsure whether a resource is gen 1 or gen 2.

### In the Openflow UI

The fastest check is the **gen 2** label in Openflow:

- **Deployments** and **runtimes** — gen 2 resources show a **gen 2** tag in the Openflow UI.
  Gen 1 resources do not.

### Deployments and runtimes in SQL

Gen 1 and gen 2 objects use different `SHOW` commands. These are Openflow-specific listings—not
the generic `SHOW INTEGRATIONS` command.

**gen 2 deployments** — Listed by `SHOW OPENFLOW DEPLOYMENTS`. You must hold a qualifying
privilege on the deployment to see it.

**gen 1 deployments** — Listed by `SHOW OPENFLOW DATA PLANE INTEGRATIONS`. They do not appear
in `SHOW OPENFLOW DEPLOYMENTS`.

**gen 2 runtimes** — Listed by `SHOW OPENFLOW RUNTIMES IN ACCOUNT`. Each row includes
`database_name` and `schema_name` columns; the fully qualified name is
`<database>.<schema>.<runtime_name>`.

**gen 1 runtimes** — Listed by `SHOW OPENFLOW RUNTIME INTEGRATIONS`. Runtime names are not
schema-qualified and do not appear in `SHOW OPENFLOW RUNTIMES`.

If `SHOW OPENFLOW DEPLOYMENTS` returns a SQL error (not an empty result), the account does not
support gen 2 SQL objects. Use the gen 1 `SHOW OPENFLOW ... INTEGRATIONS` commands and the
public gen 1 documentation instead.

### Connectors (Public Preview)

Gen 2 connectors are first-class Snowflake objects. Gen 1 connectors are NiFi process groups on the
runtime canvas only—they are not separate Snowflake objects.

**You have a gen 2 connector if any of the following is true:**

- The connector shows a **gen 2** label in the catalog or on **Installed Connectors**.
- The connector appears on the **Installed Connectors** tab for its runtime.
- `SHOW OPENFLOW CONNECTORS` or `DESCRIBE OPENFLOW CONNECTOR` returns the connector (when you
  have access).

**You have a gen 1 connector if any of the following is true:**

- The connector is visible on the runtime canvas but does **not** appear on **Installed Connectors**.
- The connector was installed on the canvas (for example, **Install** from the catalog on a gen 1
  runtime, or **Import from Registry** on a gen 2 runtime—see [Gen 1 and gen 2 coexistence](#label-openflow-generations-coexistence)).

**Using SQL to tell gen 1 from gen 2**

- If `SHOW OPENFLOW CONNECTORS` or `DESCRIBE OPENFLOW CONNECTOR` returns the connector, it is
  gen 2 (when you have the required privileges).
- If those commands return no row, the connector might be gen 1 **or** you might lack `USAGE` on
  the parent runtime (or another required privilege). Use the UI checks above—especially whether the
  connector appears on **Installed Connectors**—before assuming it is gen 1.

If you see a process group on the canvas that is missing from **Installed Connectors** and you
have confirmed you have access to the runtime, treat it as gen 1 and follow that connector’s public
setup documentation.

## Coexistence

Gen 1 and gen 2 resources can exist in the same account, with these
rules:

- **New deployments are gen 2 only.** You can no longer create new gen 1 deployments (BYOC or
  Snowflake) — all new deployments use `CREATE OPENFLOW DEPLOYMENT`. Existing gen 1 deployments
  continue to work unchanged and can be migrated. Migration from gen 1 to gen 2 is available in
  Private Preview; contact your Snowflake account representative to be included.
- **Gen 2 runtimes** — Support both gen 1 and gen 2 connectors; both types can coexist on the
  same runtime. Install gen 2 connectors from the connector catalog in the Openflow UI (using the
  setup wizard).

  Tip

  If a gen 2 catalog entry isn’t available for your source yet, or if you prefer the gen 1
  connector, install it from the connector catalog — it runs on the same gen 2 runtime and follows
  that connector’s public setup documentation.
- **Gen 1 runtimes** — Support gen 1 connectors only. Don’t install gen 2 connectors on a gen 1
  runtime.
- **Snowflake deployment limit** — Each account supports up to three Snowflake Openflow
  deployments. Gen 1 and gen 2 deployments share this limit; `CREATE OPENFLOW DEPLOYMENT WITH DEPLOYMENT_TYPE = SNOWFLAKE` fails when the account already has three Snowflake deployments,
  regardless of generation.
- **Shared source setup** — Source preparation (database permissions, network access, secrets) often
  follows the same public connector setup documentation for gen 1 and gen 2. Gen 2 topics link to
  those instructions where applicable.

Migration from gen 1 to gen 2 is available in Private Preview. Contact your Snowflake account
representative to be included.

## Which documentation to follow

Use this decision guide to choose the right topic:

| You want to… | Follow… |
| --- | --- |
| Understand gen 1 vs gen 2 (this page) | [Openflow gen 1 and gen 2](/user-guide/data-integration/openflow/gen2/openflow-generations) |
| Get started with gen 2 (privileges, first gen 2 resources) | [Second generation Openflow objects and interfaces](/user-guide/data-integration/openflow/gen2/index), [Quickstart: gen 2 Openflow](/user-guide/data-integration/openflow/gen2/quickstart) |
| Manage an existing **gen 1** deployment, or create a gen 1 runtime | Public Openflow setup and [Manage Openflow](/user-guide/data-integration/openflow/manage) topics |
| Install a **gen 1** catalog connector (**Install** or **Import from Registry** on the canvas) | [Openflow connectors](/user-guide/data-integration/openflow/connectors/about-openflow-connectors) and the connector’s setup topic |
| Install a **gen 2** connector with the setup wizard | [Configure a connector with the setup wizard](/user-guide/data-integration/openflow/gen2/setup-connector-wizard) |
| Configure a **gen 2** connector with SQL | [Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql) |
| Start, stop, or remove a **gen 2** connector | [Manage the gen 2 Openflow connector lifecycle](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle) |
| Manage gen 2 connector configuration versions (draft, commit, abort) | [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning) |
| SQL reference for gen 2 deployments, runtimes, and connectors | [Second generation Openflow SQL command reference](/sql-reference/commands-openflow-gen2) |
| Prepare a data source (for example, PostgreSQL CDC) | The connector’s public setup topic; return to gen 2 docs for connector creation |

Expand

Show lessSee more
