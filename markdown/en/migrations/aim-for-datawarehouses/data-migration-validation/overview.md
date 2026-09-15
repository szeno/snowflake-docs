# Data Migration & Validation

Snowflake AIM **Data Migration and Validation** (AIM DMV) provides a fault-tolerant, scalable way to move data from external sources into Snowflake and verify that migrated data matches the source. Both features share the same Orchestrator and Workers, the same `SNOWCONVERT_AI` metadata database, and the same deployment options.

Use [Data migration](./data-migration) when you are moving data from a system you plan to decommission. Use [Data validation](./data-validation) when you need confidence that migrated data is correct before cutover.

## Architecture overview

AIM DMV uses two main components: an **Orchestrator** and one or more **Workers**.

- The Orchestrator connects to your Snowflake account. It requires privileges to create and operate the `SNOWCONVERT_AI` database, where workflow, task, and result metadata is stored.
- One or more Workers connect to both the source system and Snowflake. For migration, Workers read data from the source, upload files to a Snowflake stage, and the Orchestrator loads them with `COPY INTO`. For validation from a non-Snowflake source, Workers run comparison queries on both sides and write results that the Orchestrator evaluates.
- Snowflake-to-Snowflake validation doesn’t use Workers. The Orchestrator runs comparison SQL in-warehouse on a single Snowflake connection. See [Validating Data from Snowflake](./validate-snowflake).
- Validation results from Worker-based (non-Snowflake) workflows are ingested into shared results tables via Snowpipe by default. Snowflake-to-Snowflake workflows write results directly and don’t use Snowpipe.

Each Worker that executes validation tasks must have the **validation runtime** available. Workers that only run data-migration tasks won’t pick up validation tasks from the queue.

## Deployment options

The Orchestrator and Workers can be deployed in multiple ways:

- Both on [Snowpark Container Services](./deploy-workers) (in the Snowflake account).
- Both in your environment, including custom hardware, virtual machines, or Kubernetes.
- Orchestrator on Snowpark Container Services and Workers in your environment, or the other way around.

See [Deploying workers](./deploy-workers) for deployment scenarios, compute pools, image repositories, and network access setup.

## Prerequisites

Before you use AIM DMV, make sure the following are in place:

- **Snowflake access**: Connections for the Orchestrator and Workers in your Snowflake `config.toml` or `connections.toml`, using a role that can create the `SNOWCONVERT_AI` database and its objects. See [Required privileges](./required-privileges) for the full list of grants that role needs.
- **Source connectivity**: Platform-specific drivers on Workers for non-Snowflake sources. See the per-platform pages under [Data migration](./data-migration) and [Data validation](./data-validation). Snowflake-to-Snowflake validation uses the Orchestrator’s Snowflake connection only.
- **Hybrid Tables**: On bootstrap, AIM DMV probes whether Hybrid Tables are enabled and available in your Snowflake account and region. When they are, `SNOWCONVERT_AI` metadata objects (for example the task queue) are created as Hybrid Tables. When they are not, AIM DMV falls back to standard tables instead. Workflows still run and produce correct results in both cases, but the fallback has real operational consequences: see [Running without Hybrid Tables](#running-without-hybrid-tables).
- **Snowpark Container Services (optional)**: Required only when you deploy the Orchestrator or Workers on Snowflake compute. See the [Snowpark Container Services overview](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/overview).

### Running without Hybrid Tables

AIM DMV falls back to standard `TRANSIENT` metadata tables on accounts without Hybrid Tables. Workflows produce correct results, but the task queue has lower throughput and higher latency. This is unrelated to row-level validation.

See [Metadata storage mode](../manual-migration/data-migration-configuration-reference#metadata-storage-mode) for details on what changes, environment-variable overrides, and in-place conversion constraints.

Background reading: [Hybrid Tables](https://docs.snowflake.com/en/user-guide/tables-hybrid) and [Hybrid Tables limitations](https://docs.snowflake.com/en/user-guide/tables-hybrid-limitations).

## Connecting to Snowflake with a PAT

Use a **programmatic** authentication method for Orchestrator and Worker Snowflake connections. Programmatic Access Tokens (PATs) and key-pair authentication are both suitable. Interactive methods such as browser-based SSO are not recommended: AIM DMV opens and closes many Snowflake connections during a workflow, and interactive auth flows are a poor fit for that pattern.

If you use PATs, you’ll need to establish a network policy or temporarily bypass the requirement from Snowsight. See [Programmatic access tokens](https://docs.snowflake.com/en/user-guide/programmatic-access-tokens).

## Managing Workers

The number of Workers (and threads per Worker) has the greatest impact on completion time. Consider the following:

- Don’t run two Workers on the same machine; increase thread count instead.
- Network bandwidth is shared between threads of a Worker.
- Keep a low Worker count to avoid overloading your source system.
- Consider stopping Workers when the source system is under heavy load.

## Monitoring workflows

Workflow and validation metadata is stored in the `SNOWCONVERT_AI` database. Filter almost every query by `WORKFLOW_ID` to scope results to a single run. See [The SNOWCONVERT\_AI database](./snowconvert-ai-database) for tables, views, workflow management procedures, and sample queries.

## Related content

- [Data migration](./data-migration)
- [Data validation](./data-validation)
- [Required privileges](./required-privileges)
- [The SNOWCONVERT\_AI database](./snowconvert-ai-database)
- [Deploying workers](./deploy-workers)
- [Data migration advanced configuration](./data-migration-advanced-configuration)
- [Data validation advanced configuration](./data-validation-advanced-configuration)
- [Glossary](./glossary)
