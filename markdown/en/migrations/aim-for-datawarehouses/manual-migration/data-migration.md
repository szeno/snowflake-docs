# SnowConvert AI CLI - Data migration

Tip

This page covers **SnowConvert AI CLI (`scai`) commands** for data migration. For architecture, prerequisites, and platform guidance using the Snowflake AIM Agent for Data Warehouses, see [Data migration](/migrations/aim-for-datawarehouses/data-migration-validation/data-migration). For workflow and Worker field definitions, see [Data migration configuration reference](/migrations/aim-for-datawarehouses/manual-migration/data-migration-configuration-reference).

Use this page when you run data migration from the CLI instead of Snowflake CoCo. Cloud data commands are grouped under `scai data migrate …`, `scai data worker …`, and `scai data orchestrator …`.

Supported source platforms: **SQL Server**, **Amazon Redshift**, **Teradata**, **Oracle**, and **PostgreSQL**. Platform-specific auth, extraction strategies, Worker TOML, and data type mappings live on the AIM pages:

- [Migrating Data from Amazon Redshift](/migrations/aim-for-datawarehouses/data-migration-validation/migrate-redshift)
- [Migrating Data from SQL Server](/migrations/aim-for-datawarehouses/data-migration-validation/migrate-sql-server)
- [Migrating Data from Teradata](/migrations/aim-for-datawarehouses/data-migration-validation/migrate-teradata)
- [Migrating Data from Oracle](/migrations/aim-for-datawarehouses/data-migration-validation/migrate-oracle)
- [Migrating Data from PostgreSQL](/migrations/aim-for-datawarehouses/data-migration-validation/migrate-postgresql)

## Prerequisites

Before you run CLI commands, make sure the following are in place:

- **SCAI CLI** installed and a SnowConvert AI project on disk (`scai init …`).
- **Snowflake connection** in `~/.snowflake/config.toml` or `connections.toml` with a role that can create and administer `SNOWCONVERT_AI`.
- **Source connection** registered for your dialect (`scai connection add-*`). See the platform pages above for Worker TOML shape.
- **SPCS (optional)**: Required only for `scai data orchestrator setup` and `scai data worker setup` on Snowflake compute.

## Project and connection setup

Initialize a project and register source connections from your project directory:

Copy code

```
# Example: SQL Server project
scai init my-project -l Sqlserver -c my-snowflake
scai connection add-sqlserver --source-connection prod-sql --auth standard \
  --host db.example.com --database mydb --user scai --password '***'
scai connection set-default -l sqlserver -s prod-sql

# Verify connectivity
scai connection test -l sqlserver -s prod-sql --json
```

Use `scai connection add-oracle`, `scai connection add-postgresql`, `scai connection add-redshift`, or Teradata equivalents for other dialects. See [SCAI Command Reference](./SCAI_Command_Reference) for all connection options.

After code conversion, extract and deploy before migrating:

Copy code

```
scai code extract
scai code convert
scai code deploy
```

## Install orchestrator and workers

Generate Worker TOML from your project, then deploy on SPCS or run locally:

Copy code

```
# Generate Worker TOML (recommended):
scai data worker generate-config .scai/settings/DataExchangeWorkerConfig.toml
scai data worker generate-config .scai/settings/DataExchangeWorkerConfig.toml --affinity my-team -y

# SPCS (first time):
scai data orchestrator setup --compute-pool MY_COMPUTE_POOL --connection my-snowflake
scai data worker setup --compute-pool MY_COMPUTE_POOL --connection my-snowflake

# Local Worker (customer environment):
scai data worker start --local .scai/settings/DataExchangeWorkerConfig.toml
```

Edit the generated TOML using examples on your platform page. Full Worker property reference: [Data migration configuration reference](/migrations/aim-for-datawarehouses/manual-migration/data-migration-configuration-reference#worker-configuration). To route workflows to a specific Worker pool, set matching affinity on the Worker and the workflow; see [Affinity](/migrations/aim-for-datawarehouses/manual-migration/data-migration-configuration-reference#affinity).

## Run a migration workflow

### Generate workflow config

Copy code

```
scai data migrate generate-config
scai data migrate generate-config --where "source.schema = 'public'"
scai data migrate generate-config \
  -o artifacts/data_migration/workflows/sales.yaml \
  --where "source.schema = 'sales'"
scai data migrate generate-config --affinity my-team
scai data migrate generate-config --help
```

Workflow files are **YAML** (`.yaml` or `.yml`). See [Data migration configuration reference](/migrations/aim-for-datawarehouses/manual-migration/data-migration-configuration-reference) for the object model. Use `--affinity` when you need to route the workflow to a specific Worker pool; see [Affinity](/migrations/aim-for-datawarehouses/manual-migration/data-migration-configuration-reference#affinity).

Note

To migrate a fixed set of tables, prefer an exact registry filter with `IN (...)`:

`scai data migrate generate-config --where "source.objectType = 'table' AND source.canonicalName IN ('dbo.orders', 'dbo.order_items')"`

Avoid substring patterns such as `source.canonicalName ILIKE '%orders%'`, which can pull in similarly named tables (for example, `ORDERS_ARCHIVE` or `ORDERS_SWTCH`). SnowConvert AI uses the exact `canonicalName` filter you provide; it doesn’t auto-include partition SWITCH or staging tables. After you generate the config, review the `tables:` list before you start the migration.

### Start orchestrator and workers

Copy code

```
# Resume SPCS orchestrator:
scai data orchestrator start

# Resume SPCS worker service:
scai data worker start

# Stop when idle:
scai data orchestrator stop
scai data worker stop
```

### Submit and monitor workflows

Copy code

```
# Local all-in-one (generates config if missing, starts local orchestrator + worker, watches):
scai data migrate start --connection my-snowflake
scai data migrate start --config my-data-migration-config.yaml --connection my-snowflake

# Submit only (SPCS or existing orchestrator/workers):
scai data migrate create-workflow --config my-data-migration-config.yaml --connection my-snowflake
scai data migrate create-workflow --config my-data-migration-config.yaml --connection my-snowflake --watch

# Start SPCS service, then create workflow:
scai data migrate create-workflow --config my-data-migration-config.yaml \
  --start-service --compute-pool MY_COMPUTE_POOL --connection my-snowflake

# Status and listing:
scai data migrate status DATA_MIGRATION_WORKFLOW_xx_yy_zz --watch
scai data migrate list --status running --limit 20
```

Global options such as `--json`, `--log-debug`, `-c` / `--connection`, `--warehouse`, and `--role` apply where the CLI exposes them. Run `scai data migrate --help` for the full surface.

## Command reference

| Command | Purpose |
| --- | --- |
| `scai data worker generate-config <path>` | Generate Worker TOML from the project |
| `scai data worker start --local <config.toml>` | Run a local Worker |
| `scai data worker start --auto-config [PATH]` | Emit a Worker TOML template |
| `scai data orchestrator setup --compute-pool <POOL>` | Create or resume Orchestrator on SPCS |
| `scai data orchestrator stop` | Suspend Orchestrator SPCS service |
| `scai data worker setup --compute-pool <POOL>` | Create Worker SPCS service |
| `scai data worker stop` | Suspend Worker SPCS service |
| `scai data migrate generate-config` | Generate workflow YAML from the project |
| `scai data migrate create-workflow --config <path>` | Submit a migration workflow |
| `scai data migrate start` | Local all-in-one run from the project |
| `scai data migrate status <WORKFLOW_ID>` | Show or watch workflow status |
| `scai data migrate list` | List recent workflows |
| `scai connection test -l <dialect> -s <profile> --json` | Verify source connectivity |

Expand

Show lessSee more

Monitor progress in Snowflake with `SNOWCONVERT_AI.DATA_MIGRATION.WORKFLOW`, `TABLE_PROGRESS_WITH_EXAMPLE_ERROR`, and the `DATA_MIGRATION_DASHBOARD` Streamlit app. See [Data migration](/migrations/aim-for-datawarehouses/data-migration-validation/data-migration#usage) for observability details.

## Related content

- [Data migration](/migrations/aim-for-datawarehouses/data-migration-validation/data-migration)
- [Data migration configuration reference](/migrations/aim-for-datawarehouses/manual-migration/data-migration-configuration-reference)
- [Data validation (CLI)](./data-validation)
- [SCAI Command Reference](./SCAI_Command_Reference)
