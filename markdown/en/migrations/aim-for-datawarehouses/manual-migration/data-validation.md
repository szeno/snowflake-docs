# SnowConvert AI CLI - Data validation

Tip

This page covers **SnowConvert AI CLI (`scai`) commands** for cloud data validation. For validation levels, architecture, and platform guidance using the Snowflake AIM Agent for Data Warehouses, see [Data validation](/migrations/aim-for-datawarehouses/data-migration-validation/data-validation). For workflow and Worker field definitions, see [Data validation configuration reference](/migrations/aim-for-datawarehouses/manual-migration/data-validation-configuration-reference).

Use this page when you run data validation from the CLI instead of Snowflake CoCo. Cloud validation commands mirror the data migration commands under `scai data validate …`, sharing `scai data worker …` and `scai data orchestrator …`.

Supported source platforms: **SQL Server**, **Amazon Redshift**, **Teradata**, **Oracle**, **PostgreSQL**, and **Snowflake** (Snowflake-to-Snowflake). Platform-specific prerequisites (for example Teradata **HASH\_MD5** for L3), Worker TOML, and data type mappings live on the AIM pages:

- [Validating Data from Amazon Redshift](/migrations/aim-for-datawarehouses/data-migration-validation/validate-redshift)
- [Validating Data from SQL Server](/migrations/aim-for-datawarehouses/data-migration-validation/validate-sql-server)
- [Validating Data from Teradata](/migrations/aim-for-datawarehouses/data-migration-validation/validate-teradata)
- [Validating Data from Oracle](/migrations/aim-for-datawarehouses/data-migration-validation/validate-oracle)
- [Validating Data from PostgreSQL](/migrations/aim-for-datawarehouses/data-migration-validation/validate-postgresql)
- [Validating Data from Snowflake](/migrations/aim-for-datawarehouses/data-migration-validation/validate-snowflake)

## Prerequisites

Before you run CLI commands, make sure the following are in place:

- **SCAI CLI** installed and a SnowConvert AI project on disk.
- **Snowflake connection** with a role that can create and administer `SNOWCONVERT_AI`.
- **Source connection** on Workers (same TOML as data migration) for non-Snowflake sources. Generate with `scai data worker generate-config`. Snowflake-to-Snowflake validation doesn’t need a Worker or a source TOML section.
- **Target tables in Snowflake** already loaded. Don’t alter migrated data between migration and validation.
- **Validation runtime** on Workers that execute validation tasks for non-Snowflake sources (the CLI installs this when you use `scai data validate start` or `--start-worker` paths locally).

## Install orchestrator and workers

Reuse the same Orchestrator and Workers as data migration when possible:

Copy code

```
scai data worker generate-config .scai/settings/DataExchangeWorkerConfig.toml

# SPCS (first time):
scai data orchestrator setup --compute-pool MY_COMPUTE_POOL --connection my-snowflake
scai data worker setup --compute-pool MY_COMPUTE_POOL --connection my-snowflake

# Local Worker:
scai data worker start --local .scai/settings/DataExchangeWorkerConfig.toml
```

Worker TOML reference: [Data validation configuration reference](/migrations/aim-for-datawarehouses/manual-migration/data-validation-configuration-reference#worker-configuration) (same format as migration).

## Run a validation workflow

### Generate validation config

Copy code

```
scai data validate generate-config
scai data validate generate-config --where "source.schema = 'public'"
scai data validate generate-config -o .scai/config/data-validation-config.yaml
scai data validate generate-config --affinity my-team
scai data validate generate-config --help
```

Default output: `.scai/config/data-validation-config.yaml`. The `source_platform` field must match your project dialect. For Snowflake-to-Snowflake, set `source_platform: snowflake`. Full workflow schema: [Data validation configuration reference](/migrations/aim-for-datawarehouses/manual-migration/data-validation-configuration-reference). Use `--affinity` when you need to route the workflow to a specific Worker pool; see [Affinity](/migrations/aim-for-datawarehouses/manual-migration/data-migration-configuration-reference#affinity).

### Submit and monitor workflows

Copy code

```
# Local all-in-one (generates config if missing, starts local orchestrator + worker, watches):
scai data validate start --connection my-snowflake
scai data validate start --config .scai/config/data-validation-config.yaml --connection my-snowflake

# Snowflake-to-Snowflake (in-warehouse; Workers aren't required):
scai data validate create-workflow --config .scai/config/data-validation-config.yaml --connection my-snowflake

# Submit only:
scai data validate create-workflow --config my-validation.yaml --connection my-snowflake
scai data validate create-workflow --config my-validation.yaml --connection my-snowflake --watch

# Status and listing:
scai data validate status DATA_VALIDATION_WORKFLOW_xx_yy_zz --watch
scai data validate list --status running --limit 20

# Re-run only the failed partitions and levels of a finished workflow:
scai data validate revalidate DATA_VALIDATION_WORKFLOW_xx_yy_zz
```

Migrate data first with [Data migration (CLI)](./data-migration) if targets aren’t loaded yet.

## Command reference

| Command | Purpose |
| --- | --- |
| `scai data validate generate-config` | Generate validation workflow YAML from the project |
| `scai data validate generate-config -o <path>` | Write config to a custom path |
| `scai data validate start` | Local all-in-one validation run |
| `scai data validate create-workflow --config <path>` | Submit a validation workflow |
| `scai data validate status <WORKFLOW_NAME>` | Show or watch workflow status |
| `scai data validate list` | List validation workflows |
| `scai data validate pause <WORKFLOW_NAME>` | Pause a running workflow |
| `scai data validate resume <WORKFLOW_NAME>` | Resume a paused workflow |
| `scai data validate cancel <WORKFLOW_NAME>` | Cancel a workflow |
| `scai data validate revalidate <WORKFLOW_NAME>` | Create a child workflow that re-runs only the failed partitions and levels of a finished workflow. See [Re-validating what failed](/migrations/aim-for-datawarehouses/data-migration-validation/data-validation#re-validating-what-failed) |
| `scai data worker generate-config <path>` | Generate shared Worker TOML |
| `scai data worker start --local <config.toml>` | Run a local Worker |
| `scai data orchestrator setup --compute-pool <POOL>` | Deploy Orchestrator on SPCS |
| `scai data orchestrator stop` | Suspend Orchestrator SPCS service |
| `scai connection test -l <dialect> -s <profile> --json` | Verify source connectivity |

Expand

Show lessSee more

Monitor progress in `SNOWCONVERT_AI.DATA_VALIDATION` (`TABLE_PROGRESS`, `TABLE_PROGRESS_DETAIL`, `DATA_VALIDATION_ERROR`, `DATA_VALIDATION_WARNING`) and the `DATA_VALIDATION_DASHBOARD` Streamlit app. See [Data validation](/migrations/aim-for-datawarehouses/data-migration-validation/data-validation#monitoring-a-cloud-data-validation-workflow) for outcome categories and query tagging.

## Related content

- [Data validation](/migrations/aim-for-datawarehouses/data-migration-validation/data-validation)
- [Data validation configuration reference](/migrations/aim-for-datawarehouses/manual-migration/data-validation-configuration-reference)
- [Data migration (CLI)](./data-migration)
- [SCAI Command Reference](./SCAI_Command_Reference)
