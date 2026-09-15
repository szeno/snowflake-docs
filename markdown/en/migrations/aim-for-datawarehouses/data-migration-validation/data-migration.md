# Data migration

The Data Migration feature provides a fault-tolerant, scalable solution for moving data from external sources into Snowflake. This feature is specifically designed for cases where you are moving data from a system you plan to decommission.

For shared architecture, deployment options, prerequisites, and Worker tuning, see [Data Migration & Validation overview](./overview).

## Supported source platforms

AIM DMV cloud data migration supports **SQL Server**, **Azure Synapse Analytics**, **Amazon Redshift**, **Teradata**, **Oracle**, and **PostgreSQL**. Each platform page covers prerequisites, auth methods, extraction strategies, data type mappings, and platform-specific suggestions:

- [Migrating Data from Amazon Redshift](./migrate-redshift)
- [Migrating Data from SQL Server](./migrate-sql-server)
- [Migrating Data from Azure Synapse Analytics](./migrate-synapse)
- [Migrating Data from Teradata](./migrate-teradata)
- [Migrating Data from Oracle](./migrate-oracle)
- [Migrating Data from PostgreSQL](./migrate-postgresql)

For workflow and Worker field definitions, see [Data migration configuration reference](../manual-migration/data-migration-configuration-reference).

## Usage

To migrate data using this solution, complete the following high-level steps:

1. Start the Orchestrator.
2. Start the Workers.
3. Create a Data Migration Workflow.
4. Monitor the Data Migration Workflow until completion.

A Data Migration Workflow describes which tables to migrate and how. The Orchestrator breaks workflows into smaller tasks, typically splitting a table into partitions before extracting and loading data to Snowflake.

Ask the Snowflake AIM Agent for Data Warehouses to run cloud data migration:

Copy code

```
Migrate data
```

For SnowConvert AI CLI commands (`scai data migrate …`, Worker TOML generation, and orchestrator setup), see [Manual Migration with SnowConvert AI CLI: Data migration](../manual-migration/data-migration).

Monitor progress in the `SNOWCONVERT_AI` database. See [The SNOWCONVERT\_AI database](./snowconvert-ai-database) for views and sample queries filtered by `WORKFLOW_ID`.

### Cancel, pause, resume, or retry a workflow

Prefer asking the Snowflake AIM Agent for Data Warehouses in natural language (for example, “Pause the ORDERS migration workflow” or “Retry failed tasks on my last run”). You can also use the SnowConvert AI CLI (`scai data migrate pause|resume|cancel`) or call the workflow management stored procedures directly.

Canceling a workflow fails active tasks with a cancellation message. Rows already loaded into Snowflake are not rolled back. You can also pause, resume, retry, or cancel a single source table inside a workflow.

See [Managing workflow lifecycle](./snowconvert-ai-database#workflow-management-procedures) in [The SNOWCONVERT\_AI database](./snowconvert-ai-database).

Copy code

```
CALL SNOWCONVERT_AI.DATA_MIGRATION.CANCEL_WORKFLOW(<workflow_id>);
```

## Considerations and recommendations

For more scenarios (extraction strategy choice, partition keys, INTERVAL handling, custom extraction plugins, Iceberg targets, and more) with example prompts, see [Data migration advanced configuration](./data-migration-advanced-configuration).

### Initial testing

Deploy the DDL for tables you want to migrate before starting data migration so target types match your expectations. You can convert DDL using the code conversion capabilities of the Snowflake AIM Agent for Data Warehouses.

Note

If you don’t deploy the DDL before starting data migration, types will be inferred, which may not be as accurate as required.

For an early test run, use a separate workflow whose `tables` array lists only the tables you want to validate, with `whereClauseCriteria` to limit rows and a small `partitionSize`.

### Numeric precision and scale

Snowflake `NUMBER` columns support at most **38** digits of precision and **37** digits of scale. When source metadata exceeds those limits, AIM DMV creates target columns with Snowflake-safe precision and scale. Values wider than the target column can lose fractional digits or fail to load.

Deploy converted DDL before migration so target types match your expectations, especially for wide Oracle `NUMBER` columns and other high-precision source types. Use `columnTypeMappings` in the workflow when you need explicit overrides.

### Incremental sync

After an initial full load, use **`watermark`** or **`checksum`** synchronization in the workflow configuration for incremental loads. The default strategy, **`none`**, runs full loads only and does not track changes. See [Data migration configuration reference](../manual-migration/data-migration-configuration-reference).

## Related content

- [Data Migration & Validation overview](./overview)
- [Data migration configuration reference](../manual-migration/data-migration-configuration-reference)
- [Data validation](./data-validation)
- [The SNOWCONVERT\_AI database](./snowconvert-ai-database)
- [Deploying workers](./deploy-workers)
- [Data migration advanced configuration](./data-migration-advanced-configuration)
- [Manual Migration with SnowConvert AI CLI: Data migration](../manual-migration/data-migration)
