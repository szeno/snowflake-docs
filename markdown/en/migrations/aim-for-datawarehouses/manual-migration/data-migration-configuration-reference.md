# Data migration configuration reference

This page documents the **workflow YAML** and **Worker TOML** settings for Data Migration. For platform-specific prerequisites, auth methods, extraction strategies, and data type mappings, see the per-platform pages linked from [Data migration](../data-migration-validation/data-migration).

Tip

If you use the Snowflake AIM Agent for Data Warehouses instead of hand-editing these files, see [Data migration advanced configuration](../data-migration-validation/data-migration-advanced-configuration) for common scenarios and the prompts that generate and adjust this configuration for you.

For SnowConvert AI CLI commands that generate and submit these configs, see [Data migration (CLI)](./data-migration).

## Workflow configuration reference

The Data Migration Workflow configuration file is a YAML file. The CLI and Snowflake AIM Agent for Data Warehouses accept `.yaml` or `.yml` files.

Note

Names that require quoting (or brackets) must be manually quoted. For example: `tableName: "\"MyCaseSensitiveTable\""`.

### Top-level object

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `schemaVersion` | `String` |  | Version of the configuration schema (for example, `"1.0.0"`). Accepts `major`, `major.minor`, or `major.minor.patch`. Defaults to `"1.0.0"` when omitted. |
| `tables` | `TableConfiguration[]` | Yes | An array of table-specific configurations defining which tables to migrate and how. Must contain at least one entry. |
| `defaultTableConfiguration` | `TableConfiguration` |  | Shared settings inherited by all tables in the `tables` array. Table-specific values override these defaults. |
| `affinity` | `String` |  | Optional affinity tag that routes this workflow’s tasks to matching Workers. See [Affinity](#affinity). |
| `intervalHandling` | `String` (`"interval"`, `"varchar"`) |  | Default handling for source `INTERVAL` columns across all tables. Defaults to `"interval"`. See [INTERVAL data type handling](#interval-data-type-handling). |
| `preflight` | `Boolean` |  | When `true`, caps each table to a single partition and loads it into a transient copy of the target table in a `PREFLIGHT_<workflowId>` schema, instead of the configured target. The real target tables must already exist. Defaults to `false`. See [Preflight: a bounded dry run](#preflight-bounded-dry-run). |
| `preflightKeepSchema` | `Boolean` |  | When `preflight` is `true`, skips cleanup so the transient schema survives for inspection. You then drop it yourself. Defaults to `false`. See [Keeping the preflight schema](#keeping-the-preflight-schema). |
| `cleanUpTransientResources` | `String` (`"never"`, `"on-success"`, `"always"`) |  | When to delete this workflow’s intermediate stage files. Defaults to `"on-success"`. See [Cleaning up transient resources](#cleaning-up-transient-resources). |

Expand

Show lessSee more

When `defaultTableConfiguration` is present, each object in `tables` is merged with those defaults: shared fields apply to every table unless the same field is set again on a specific table entry.

### Preflight: a bounded dry run

Setting `preflight: true` runs the migration as a bounded smoke test. Each table is capped at **one partition**, which loads into a transient copy of the target table in a `PREFLIGHT_<workflowId>` schema. Your configured target tables are never written to. Your Orchestrator and Workers send one partition per table along the same path a real load takes: source connection, extraction, staging, and the load into a table with your target’s columns and types.

Copy code

```
preflight: true
preflightKeepSchema: false # true leaves PREFLIGHT_<workflowId> in place for inspection
```

Run it the same way you run any other workflow. AIM DMV drops the transient schema when the workflow ends unless `preflightKeepSchema` is `true`.

#### Before you run a preflight

- **The real target tables must already exist.** AIM DMV creates each transient copy with `CREATE TRANSIENT TABLE IF NOT EXISTS <copy> LIKE <real_target>`, so the copy takes its structure from the real target. A normal migration creates a missing native target from the source schema, but a preflight can’t: if the real target doesn’t exist, that table’s setup task fails. Deploy the converted DDL first. See [CREATE TABLE … LIKE](/sql-reference/sql/create-table#label-create-table-like).
- **The services must be running.** A preflight uses the same Orchestrator, Workers, warehouse, and compute pool as a real load, and it’s billed the same way while it runs. If the services suspended themselves, resume them first. See [Resuming services before the next wave](../data-migration-validation/deploy-workers#resuming-services-before-the-next-wave) and [Controlling cost on SPCS](../data-migration-validation/deploy-workers#controlling-cost-on-spcs).
- **The migration role must be able to create schemas in each target database.** See [Target database privileges](../data-migration-validation/required-privileges#target-database-privileges).

#### What a preflight does

| Step | What happens |
| --- | --- |
| Redirect | Each table’s target becomes `<target_database>.PREFLIGHT_<workflowId>.<copy_name>`. The schema is created in the real target’s database, so a workflow whose targets span several databases creates one `PREFLIGHT_<workflowId>` schema in each. `<copy_name>` is the real target’s `<DATABASE>_<SCHEMA>_<TABLE>` in uppercase, with every character other than `A`–`Z`, `0`–`9`, and `_` replaced by `_`. For example, workflow 42 loads `SALES_DB.PUBLIC.ORDERS` into `SALES_DB.PREFLIGHT_42.SALES_DB_PUBLIC_ORDERS`. If two tables produce the same copy name in one database, the workflow fails when it starts, with a configuration error. |
| Setup | Before a table’s first task, AIM DMV runs `CREATE TRANSIENT SCHEMA IF NOT EXISTS` for the schema and `CREATE TRANSIENT TABLE IF NOT EXISTS ... LIKE` for the copy. |
| Planning | Metadata extraction, schema extraction, and partition planning run against the whole source table, as they do in a real load. |
| Load | One partition per table is extracted, staged, and loaded into the copy. See [Which rows a preflight loads](#which-rows-a-preflight-loads). |
| CHECK constraints | Removed from the copy before the load, as they are from a real target. They’re restored only when `preflightKeepSchema` is `true`. See [CHECK constraints](#check-constraints). |
| Cleanup | Unless `preflightKeepSchema` is `true`, the schema is dropped after every other task finishes. See [Cleaning up after a preflight](#cleaning-up-after-a-preflight). |

Expand

Show lessSee more

#### Which rows a preflight loads

A preflight caps each table at one partition of its partition plan, not at a number of rows:

- **A table that fits in one partition is loaded in full.** With [automatic partition sizing](#partition-size), a small table usually gets a single partition, so the preflight moves the whole table. That isn’t a sample, and it takes as long as a real load of that table.
- **A table with several partitions loads only one.** It’s picked by its position in the plan, not at random, and it can hold few rows or none. A table can complete with no rows loaded.
- **The rest of the table isn’t read.** Values that appear only in other partitions, such as unusually long strings or out-of-range dates, aren’t tested.

#### Reading a preflight result

A preflight that completes shows that, for each table, one partition was extracted, staged, and loaded into a copy of the real target, with the Workers, credentials, extraction strategy, and type mappings in this workflow. Check it as you would any workflow, with `scai data migrate status <WORKFLOW_ID>` or the `TABLE_PROGRESS` view and `PARTITION_METADATA` table described in [SnowConvert AI database objects](../data-migration-validation/snowconvert-ai-database). AIM DMV records only the partition it ran, so those counts describe that partition, not the whole table.

A table that fails shows a problem to fix before the real load, such as a missing target table, source connectivity or credentials, the extraction strategy’s prerequisites, such as its external stage, or a value that doesn’t load into the target’s column type.

A completed preflight doesn’t show:

- **How a full load performs.** Duration, throughput, cost, and load on the source all depend on the partitions it didn’t run.
- **That the rest of the data loads.** Only one partition per table was read.
- **That loads into the real targets succeed.** A preflight never writes to them.
- **That the migrated data is correct.** A preflight doesn’t validate data. After the real load, run [data validation](../data-migration-validation/data-validation).

To look at the rows a preflight loaded, set `preflightKeepSchema: true`. Otherwise the schema is dropped when the workflow ends.

#### When to run a preflight

Run a preflight before the **first** real load of a set of tables, once their DDL is deployed and the Workers are set up. It’s most useful when something in the path is new: the first wave, a new source server, a new extraction strategy, or a new Worker deployment.

Warning

Don’t run a preflight between a full load and later incremental runs of the same tables. A preflight records partition metadata for its tables like any other migration workflow. A later workflow that uses `checksum` or `watermark` [synchronization](#synchronizationstrategy-model) reuses the most recent metadata for each source table, which would be the preflight’s single partition. Run the preflight first, then the full load with the default `strategy: none`, so later incremental runs build on the full load’s partitions.

#### Keeping the preflight schema

With `preflightKeepSchema: true`, AIM DMV doesn’t queue the drop task, and it restores CHECK constraints on the copies after the load so they match the real targets. The schema then stays until you drop it, and its tables keep using storage.

Inspect the copies:

Copy code

```
SHOW TABLES IN SCHEMA SALES_DB.PREFLIGHT_42;
SELECT COUNT(*) FROM SALES_DB.PREFLIGHT_42.SALES_DB_PUBLIC_ORDERS;
```

When you’re done, drop the schema in each target database the workflow used:

Copy code

```
DROP SCHEMA IF EXISTS SALES_DB.PREFLIGHT_42 CASCADE;
```

#### Cleaning up after a preflight

Without `preflightKeepSchema`, the drop is a cleanup task in the workflow. Once every other task has finished, whether it succeeded or failed, the Orchestrator runs `DROP SCHEMA IF EXISTS <target_database>.PREFLIGHT_<workflowId> CASCADE` in each target database. The schema stays until an Orchestrator runs that task.

You’re responsible for dropping:

- Schemas you kept with `preflightKeepSchema: true`.
- Any `PREFLIGHT_<workflowId>` schema left behind, for example when no Orchestrator ran the cleanup task.

The schema drop doesn’t remove staged files. `cleanUpTransientResources` governs those, as for any workflow. See [Cleaning up transient resources](#cleaning-up-transient-resources).

Three related things are easy to confuse:

| Mechanism | What it does |
| --- | --- |
| `preflight: true` | Bounded dry run: one partition per table, into a transient schema |
| `whereClauseCriteria` | A row-limited but otherwise real migration, into the actual target |
| `scai data doctor` | Infrastructure and configuration health check before anything starts. A failure blocks a local start |

Expand

Show lessSee more

Use preflight when you want to check that one partition per table gets through the pipeline without touching the real targets. Use `whereClauseCriteria` when you want a real sample of rows in the real target.

Warning

Turn `preflight` off (or generate a workflow without it) before your production load. A preflight workflow never writes to the configured target schema, so leaving it enabled means your target stays empty.

### TableConfiguration model

Defines the settings for migrating a single table.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `source` | `SourceTargetIdentifier` |  | Identifies the source table. |
| `target` | `SourceTargetIdentifier` |  | Identifies the target table in Snowflake. |
| `columnNamesToPartitionBy` | `String[]` |  | Columns used to partition data during extraction. Can be omitted and inferred automatically. See [Automatic partition key selection](#automatic-partition-key-selection). |
| `extraction` | `ExtractionStrategy` |  | How data is extracted from the source database. |
| `synchronization` | `SynchronizationStrategy` |  | Settings for incremental synchronization. |
| `columnTypeMappings` | `ColumnTypeMapping[]` |  | Source-to-target type overrides applied during extraction and load. See [ColumnTypeMapping and ColumnNameMapping models](#columntypemapping-model). |
| `columnNameMappings` | `ColumnNameMapping[]` |  | Column renaming mappings. See [ColumnTypeMapping and ColumnNameMapping models](#columntypemapping-model). |
| `primaryKeyColumns` | `String[]` |  | Primary key columns. Required for `trackModifications` or `trackDeletions` under the `watermark` synchronization strategy. Can be omitted and inferred automatically at runtime. See [Automatic partition key selection](#automatic-partition-key-selection). |
| `targetPartitionSizeMb` | `Integer` |  | Target partition size in MB. Mutually exclusive with `targetPartitionSizeRows`. Must be greater than 0. When both are omitted, the orchestrator picks sizes automatically. See [Partition size](#partition-size). |
| `targetPartitionSizeRows` | `Integer` |  | Target partition size in rows. Mutually exclusive with `targetPartitionSizeMb`. Must be greater than 0. When both are omitted, the orchestrator picks sizes automatically. See [Partition size](#partition-size). |
| `whereClauseCriteria` | `String` |  | SQL-like filter to select a subset of rows (for example, `"is_deleted = 0"`). |
| `loadSegmentation` | `LoadSegmentation` |  | Splits a single `COPY INTO` into multiple parallel statements, each targeting a subset of staged files. Useful when many files are staged for one partition (common with Redshift UNLOAD). See [Load segmentation](#load-segmentation). |
| `queryModifiers` | `QueryModifiers` |  | Optional SQL hints appended to source queries to reduce locking on busy source tables. Default is unset (no hints). See [Anti-locking and query modifiers](#anti-locking-and-query-modifiers). |
| `intervalHandling` | `String` (`"interval"`, `"varchar"`) |  | Per-table override of the workflow-level `intervalHandling` setting. See [INTERVAL data type handling](#interval-data-type-handling). |

Expand

Show lessSee more

### Views and dynamic tables in migration

Data migration copies source tables into Snowflake tables. Before it extracts an entry, AIM DMV reads the source object’s type with the same catalog classification that validation uses (see [How catalog kinds are classified](./data-validation-configuration-reference#how-catalog-kinds-are-classified)):

- **Table:** the entry is migrated.
- **View, including a materialized view:** the entry fails before extraction with `'<name>' is a VIEW, not a TABLE. Data migration does not support views.` Remove the entry, or migrate the view’s base tables instead.
- **Not found:** the entry fails with a table-not-found error.
- **Unrecognized catalog kind:** the entry is migrated, and the task records a warning that the object type is unrecognized and results may be unexpected.

The target must be a Snowflake table or a [Snowflake-managed Iceberg table](../data-migration-validation/iceberg). AIM DMV loads the target with `COPY INTO`, and incremental synchronization can also run `MERGE` and `DELETE` against it. [Dynamic tables are read-only](/user-guide/dynamic-tables/decision-guide#label-dynamic-tables-limitations), so a dynamic table isn’t a supported migration target. AIM DMV doesn’t detect a dynamic-table target before it loads, so the load fails. To populate a dynamic table, migrate its base tables and let Snowflake refresh it.

Validation is different: it can compare a source view with a Snowflake table, including a dynamic table. See [Source and target object types](./data-validation-configuration-reference#source-and-target-object-types).

### ColumnTypeMapping and ColumnNameMapping models

`columnTypeMappings` overrides the default source-to-target type mapping for a table, and applies to both the extraction query and the `COPY INTO` load. `columnNameMappings` renames columns on the way to the target. Set either on a table entry or on `defaultTableConfiguration`.

**`ColumnTypeMapping`:**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `sourceType` | `String` | Yes | Type name as it appears in the source system. |
| `targetType` | `String` | Yes | Snowflake type to use instead of the default mapping. |

Expand

Show lessSee more

**`ColumnNameMapping`:**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `sourceName` | `String` | Yes | Column name on the source. |
| `targetName` | `String` | Yes | Column name on the target. |

Expand

Show lessSee more

Copy code

```
defaultTableConfiguration:
  columnTypeMappings:
    - sourceType: SUPER
      targetType: VARCHAR
    - sourceType: GEOMETRY
      targetType: VARCHAR
  columnNameMappings:
    - sourceName: CUST_NM
      targetName: CUSTOMER_NAME
```

Apache Iceberg™ targets are the most common reason to need this. Iceberg has no equivalent for Snowflake `VARIANT`, `OBJECT`, `ARRAY`, `GEOGRAPHY`, or `GEOMETRY`, so map any source type that would land on one of those to `VARCHAR` or `STRING`. See [Iceberg configuration](#iceberg-configuration-targeticebergconfig).

### QueryModifiers model

| Property | Type | Description |
| --- | --- | --- |
| `objectModifier` | `String` | Text appended after the source table in the `FROM` clause (for example `" WITH (NOLOCK)"` on SQL Server). |
| `selectModifier` | `String` | Token inserted immediately after `SELECT` (for example an Oracle optimizer hint). Use `"NONE"` to disable Oracle’s automatic parallel hint. |

Expand

Show lessSee more

### SourceTargetIdentifier model

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `databaseName` | `String` |  | Source or target database name. |
| `schemaName` | `String` |  | Schema containing the table. |
| `tableName` | `String` |  | Table to migrate. |

Expand

Show lessSee more

### Additional target properties

The following optional fields apply **only** to the `target` object.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `tableType` | `String` |  | `"native"` for a standard Snowflake table (default) or `"iceberg"` for an Apache Iceberg™ table. |
| `icebergConfig` | `Object` | For Iceberg targets | Required when `tableType` is `"iceberg"`. See [Iceberg configuration](#iceberg-configuration-targeticebergconfig). |

Expand

Show lessSee more

### Iceberg configuration (`target.icebergConfig`)

Used when `target.tableType` is `"iceberg"`. Account setup follows Snowflake’s [Apache Iceberg™ tables](https://docs.snowflake.com/en/user-guide/tables-iceberg) documentation.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `catalog` | `String` |  | Default `SNOWFLAKE` for Snowflake-managed Iceberg. Use a catalog integration name for externally cataloged tables. |
| `externalVolume` | `String` | For `catalog` `SNOWFLAKE` | External volume name, or `SNOWFLAKE_MANAGED` to store the table in Snowflake. `SNOWFLAKE_MANAGED` is supported on AWS and Azure commercial accounts. |
| `baseLocationPrefix` | `String` | For a customer volume on `copy_files` | Path prefix for `BASE_LOCATION` (`{prefix}/{database}/{schema}/{table}`). Required when `externalVolume` is a customer volume. Omit it when `externalVolume` is `SNOWFLAKE_MANAGED`. |
| `catalogTableName` | `String` | For external `catalog` | Fully qualified name in the external catalog. |
| `catalogSync` | `String` |  | Optional catalog integration to sync Snowflake-managed metadata back to an external catalog. |
| `sourceDataStage` | `String` |  | Stage path starting with `@` pointing at existing Parquet files. Do not set this and `extraction.externalStage` on the same table. |
| `migrationStrategy` | `String` |  | One of `catalog_link`, `convert_to_managed`, or `copy_files`. When omitted, `catalog: SNOWFLAKE` resolves to `copy_files`. |
| `icebergSpec` | `String` |  | Logical type profile. `v2` is the default. `v3` is also supported. See [Apache Iceberg™ tables (spec v2 and v3)](../data-migration-validation/iceberg). |
| `storageMode` | `String` |  | `compatible` (default) writes `STORAGE_SERIALIZATION_POLICY = COMPATIBLE`. `native` is spec v3 only and writes `STORAGE_SERIALIZATION_POLICY = OPTIMIZED`. |
| `loadMode` | `String` |  | `ADD_FILES_COPY` (default) registers staged Parquet without rewriting it. `FULL_INGEST` rewrites the staged files and, on spec v3, can coerce temporal and geospatial values into native types. |
| `externalEngineAccess` | `Boolean` |  | `false` (default). Set to `true` when another engine must read the Parquet files. Allowed with `storageMode: compatible`. Rejected with `storageMode: native`. |
| `postLoadOptimize` | `Boolean` |  | When omitted, defaults to `true` for `ADD_FILES_COPY` and `false` for `FULL_INGEST`. When enabled, turns on compaction after the first load. |
| `targetFileSize` | `String` |  | Optional target file size: `AUTO`, `16MB`, `32MB`, `64MB`, or `128MB`. When omitted, `FULL_INGEST` uses `128MB`; `ADD_FILES_COPY` does not set a target size. |

Expand

Show lessSee more

Type mappings, storage choices, and how to validate the same tables are in [Apache Iceberg™ tables (spec v2 and v3)](../data-migration-validation/iceberg). On spec v3 with `FULL_INGEST`, a timestamp with an offset becomes `TIMESTAMP_LTZ(6)`. `TIME WITH TIME ZONE` and `TIMETZ` also become `TIMESTAMP_LTZ(6)`. The staged value has no date, so the load attaches it to `1970-01-01`.

Warning

`TIMESTAMP_LTZ` stores the instant in UTC and shows it in the session time zone.

Note

Iceberg targets don’t support a native `INTERVAL` type. Source `INTERVAL` columns are coerced to `VARCHAR` regardless of `intervalHandling`. See [INTERVAL data type handling](#interval-data-type-handling).

### Partition size

Partition size is controlled at the [TableConfiguration](#tableconfiguration-model) level with two flat, mutually exclusive fields: `targetPartitionSizeMb` and `targetPartitionSizeRows`. When both are omitted, the orchestrator uses **auto** sizing.

| Form | Description |
| --- | --- |
| Both omitted (default) | **Auto**. The orchestrator chooses partition sizes from the source platform, extraction strategy, and table size. |
| `targetPartitionSizeMb: N` | Each partition targets about `N` megabytes of data. Must be greater than 0. |
| `targetPartitionSizeRows: N` | Each partition targets `N` rows, regardless of data size. Must be greater than 0. |

Expand

Show lessSee more

Specify at most one of the two fields; setting both on the same table is a configuration error.

### Automatic partition key selection

When `columnNamesToPartitionBy` (and, for incremental sync, `primaryKeyColumns`) is omitted for a table that needs partitioning, AIM DMV infers a key automatically from source catalog metadata rather than scanning the full table sequentially:

1. **Clustered, sort, or distribution key columns**, when the source platform exposes one.
2. **A unique index**, when no clustering key is available.
3. **The first non-boolean column** in the table’s schema, as a last-resort fallback. Boolean columns are never selected because they don’t provide enough distinct values to split partitions evenly.

Inferred keys are cached per source table and reused by later workflows against the same table, so inference runs only once per table. A **manually specified** `columnNamesToPartitionBy` (or `primaryKeyColumns`) always takes precedence over an inferred key.

Note

Automatic key selection reads table catalog metadata. Data migration doesn’t migrate views; see [Views and dynamic tables in migration](#views-and-dynamic-tables-in-migration).

Set `columnNamesToPartitionBy` explicitly when you know a better partitioning column than the one AIM DMV would infer, or when a fallback selection (such as a non-unique first column) would create unevenly sized partitions.

### What makes a good partition key

A good partition key has **high cardinality** (many distinct values) and distributes rows **roughly evenly** across those values. AIM DMV splits the table by dividing the key’s value range into equal-sized buckets, so a column with few distinct values (for example a status flag with three possible values) or a heavily skewed distribution (most rows sharing one value) produces uneven partitions — some Workers receive far more data than others.

**Composite keys**: when no single column meets both criteria, supply two or more columns in `columnNamesToPartitionBy`. AIM DMV partitions on the combination, which multiplies cardinality and can smooth out skew. For example, if `STATUS` has low cardinality but `(STATUS, REGION)` together produce many well-distributed value pairs, use the composite.

**Numeric and date columns** — especially surrogate keys and timestamps — are the preferred choices: they have high cardinality, sort naturally, and let range predicates use source indexes efficiently. VARCHAR columns can also work, but avoid columns with consistently long text values (over roughly 1,000 characters): range predicates on very wide strings are expensive to evaluate and can slow extraction significantly.

Each configured name must be a **real, physical column** in the source table. Persisted computed columns (SQL Server) and virtual columns (Oracle) qualify. Bare SQL expressions, pseudo-columns (for example Oracle `ROWID`, `ROWNUM`, or `ORA_ROWSCN`), and hidden system columns are **not** valid: AIM DMV quotes partition key names as identifiers in `ORDER BY` and range predicates, so those values won’t resolve. To partition on a derived value, add a persisted or virtual computed column on the source and reference that column name.

Note

Pseudo-columns and system columns can be used as **watermark columns** for incremental sync (for example Oracle `ORA_ROWSCN`), but not as partition keys. See [SynchronizationStrategy model](#synchronizationstrategy-model).

### Load segmentation

When a large number of files are staged for a single partition (common with Redshift UNLOAD), the orchestrator can split the `COPY INTO` into multiple parallel statements, each targeting a subset of files.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `targetSegmentSizeMb` | `Integer` | Yes | Target total file size (in MB) per `COPY INTO` segment. Must be greater than 0. |

Expand

Show lessSee more

When `loadSegmentation` is omitted, a single `COPY INTO` loads all files in the partition (the default). Files larger than the target size get their own segment, and Snowflake’s 1,000-file `FILES` limit is enforced per statement.

Copy code

```
    loadSegmentation:
      targetSegmentSizeMb: 5000
```

### ExtractionStrategy model

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `strategy` | `String` |  | Extraction method. See the table below. Defaults to `"regular"`. |
| `externalStage` | `String` | See description | Required when `strategy` is `"unload"`, `"write_nos"`, `"dbms_cloud"`, `"cet_as"`, `"export_data"`, or `"cloud_direct"`. Snowflake external stage whose URL matches the bucket or container that receives the extracted files. |
| `pluginClass` | `String` |  | Optional. Fully qualified class name of a [custom extraction plugin](../data-migration-validation/data-migration-advanced-configuration#preparing-a-custom-extraction-plugin) to use instead of a built-in strategy. |

Expand

Show lessSee more

**Accepted values for `strategy`:**

| Value | Platform | Description |
| --- | --- | --- |
| `"regular"` (default) | All | Worker pulls data over the source connection and uploads to the Snowflake internal stage. Use when volume is genuinely small or when server-side export prerequisites aren’t in place. |
| `"unload"` | Redshift only | Redshift writes Parquet to S3; Snowflake loads from the external stage. Recommended when S3 and the external stage are available. |
| `"write_nos"` | Teradata only | Teradata WRITE\_NOS exports to S3, Azure Blob, or GCS; Snowflake loads from the external stage. Recommended when NOS and the external stage are available. |
| `"dbms_cloud"` | Oracle only | Oracle `DBMS_CLOUD.EXPORT_DATA` writes Parquet to object storage; Snowflake loads from the external stage. Recommended when the object storage and external stage are available. |
| `"cet_as"` | SQL Server and Azure Synapse | Source-side `CREATE EXTERNAL TABLE AS SELECT` writes Parquet to Azure Blob; Snowflake loads from the external stage. SQL Server support requires Azure SQL Managed Instance, SQL Server 2022 or later, or Azure Synapse. Azure SQL Database isn’t supported. |
| `"export_data"` | BigQuery only | BigQuery `EXPORT DATA` writes Parquet to GCS; Snowflake loads from the external stage. See [Migrating Data from Google BigQuery](../data-migration-validation/migrate-bigquery). |
| `"cloud_direct"` | SQL Server, Azure Synapse, Redshift, Oracle, Teradata, PostgreSQL, and IBM DB2 | Worker streams results directly to S3, GCS, or Azure Blob and Snowflake loads from the external stage. |
| `"tpt"` | Teradata only | Legacy alias for `"regular"`. The Orchestrator treats `tpt` as `"regular"`. The Worker uses Teradata Parallel Transporter only when its own configuration allows it and `tbuild` is installed, which is never the case on SPCS. See [Teradata TPT selection](#teradata-tpt-selection). `externalStage` is not required. |

Expand

Show lessSee more

See [Extraction strategies](#extraction-strategies) for YAML examples and platform prerequisites.

### SynchronizationStrategy model

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `strategy` | `String` (`"none"`, `"full-replace"`, `"checksum"`, `"watermark"`) |  | Synchronization method. `"none"` (default) re-extracts fully on every run and appends the rows. `"full-replace"` re-extracts fully and deletes each partition’s target rows before loading. Rejected for Iceberg targets. |
| `checksumExpression` | `String` |  | `checksum` only. Any other strategy is rejected at configuration validation. Custom SQL aggregate expression that returns a single value per partition (for example a row-version column or `MAX(last_modified)`). Only partitions whose value changed since the last run are cleared and re-extracted. When omitted, the default per-column hash is used. May reference pseudo-columns or system columns (for example `MAX(ORA_ROWSCN)` on Oracle). |
| `watermarkColumn` | `String` | `watermark` only | Monotonically increasing column name. May be a **pseudo-column or system column** not present in the migrated schema (for example Oracle `ORA_ROWSCN`). AIM DMV projects it into the extract for change detection but does not migrate it to the target. |
| `trackModifications` | `Boolean` |  | `watermark` only. If `true`, merges modified rows into the target by primary key after `COPY INTO` (warehouse loading only). Requires `primaryKeyColumns`, configured or inferred. Without a key, the merge doesn’t run and updated rows are appended. With `watermark`, it’s rejected with `loading.strategy: snowpipe`. Other strategies accept the flag but never act on it. |
| `trackDeletions` | `Boolean` |  | `watermark` only. Any other strategy is rejected at configuration validation. If `true`, extracts a full primary-key snapshot of each source partition on every incremental run and deletes target rows absent from the snapshot before loading new rows. Requires `primaryKeyColumns`. Independent of `trackModifications`; the two can be combined. Supported with Snowpipe loading. |

Expand

Show lessSee more

Both `trackModifications` and `trackDeletions` are **off by default**. With the `watermark` strategy, leaving them off changes what an incremental run does to updated and deleted source rows: updated rows are appended as a second version, and deleted rows stay on the target. See [Choosing a synchronization strategy](#choosing-a-synchronization-strategy).

### Choosing a synchronization strategy

The following table compares the strategies by what each one compares, what a run reloads, how it treats updates and deletes, and where it applies. Each strategy has its own subsection after the table.

| Strategy | What it compares | What a run reloads | Updates and deletes | Native targets | Iceberg targets |
| --- | --- | --- | --- | --- | --- |
| `none` (default) | Nothing. Every run extracts every row. | All rows, appended to the target. | Not reflected. A rerun adds a second copy of each row, and deleted rows stay. | Supported | Supported. A second `none` run against an existing table fails. |
| `full-replace` | Nothing. Every run extracts every row. | All rows. Each partition’s target rows are deleted before the partition loads. | Reflected. The partition is rebuilt from the source each run. | Supported | Rejected at configuration validation. |
| `checksum` | One checksum per partition, computed on the source. | Only partitions whose checksum changed, in full. | Reflected in each changed partition, because the partition is rebuilt. | Supported | Supported on a Snowflake-managed table this migration creates. A later run reuses that table after a completed run. |
| `watermark` | The highest stored value of `watermarkColumn`. | Rows above the stored value. | Inserts are appended. Updates and deletes are missed unless `trackModifications` and `trackDeletions` are set. | Supported | Supported on a Snowflake-managed table this migration creates. A later run reuses that table. With `trackModifications` and a primary key, that later run merges changed rows. |

Expand

Show lessSee more

#### none (default)

- **Compares:** Nothing. The run doesn’t read the target or the previous run’s state. The partition stores only the strategy name.
- **Reloads:** Every row in every partition, on every run.
- **Inserts, updates, and deletes:** Every run appends the extracted rows. Source updates and deletes never reach the target. A rerun against a populated target duplicates every row.
- **Required keys or columns:** None.
- **Performance and cost:** One full extract and load per run. Cost grows with table size, and the source does no change detection.
- **Blind spots and failure cases:** Rerunning against a target that already has rows duplicates them. Empty the target, or switch to `full-replace`, before a second load.
- **Native and Iceberg:** Supported on native targets and on Iceberg targets. A second `none` run against an existing Iceberg table fails with `IcebergTargetExistsError` instead of appending.
- **Choose it when:** The table loads once, such as the initial load of a set of tables, or the table is small enough to reload in full.
- **Avoid it when:** The workflow reruns against a populated target without clearing it, or the target must follow later source changes.

#### full-replace

- **Compares:** Nothing. Like `none`, it doesn’t compare the source with the target or with a previous run.
- **Reloads:** Every row in every partition, on every run. Before each partition loads, the target rows for that partition are deleted. An unpartitioned table is cleared with a whole-table delete.
- **Inserts, updates, and deletes:** After a successful run, the target holds the source rows for each partition the run covers. Updates and deletes are reflected because the partition is rebuilt. Any row in the target partition that the source doesn’t supply is deleted, including rows written by other processes.
- **Required keys or columns:** None. It doesn’t need a watermark or a primary key. It rejects `checksumExpression` and `trackDeletions`.
- **Performance and cost:** The same extraction cost as `none`, plus one `DELETE` on the Snowflake target per partition. The first load skips the delete because the target doesn’t exist yet.
- **Blind spots and failure cases:** The delete runs before the load. If the load fails after the delete, the partition has no rows until a later run completes. The next run overwrites any manual change to the target.
- **Native and Iceberg:** Native targets only. An Iceberg target is rejected at configuration validation, with a message that begins “Synchronization strategy ‘full-replace’ is not supported for Iceberg targets”. `scai data migrate create-workflow` accepts `full-replace` for an Iceberg target, and the orchestrator then rejects it. The delete runs on Snowflake, so it works for every supported source platform.
- **Choose it when:** You want a repeatable full reload that matches the source on each run, and the table has no reliable watermark or change signal. Use it to replace rows left by an earlier `none` run.
- **Avoid it when:** The target holds rows the workflow doesn’t own, the table is too large to reload on every run, or the target is an Iceberg table.

#### checksum

- **Compares:** One checksum per partition, computed on the source on every run and compared with the value stored by the last successful run. The default checksum hashes a normalized set of columns. `checksumExpression` replaces the hash with a SQL aggregate over the partition.
- **Reloads:** The checksum of every partition, on every run. A partition whose checksum changed is cleared and reloaded in full. Unchanged partitions aren’t extracted.
- **Inserts, updates, and deletes:** A change that moves a partition’s checksum is reflected for that whole partition, so updated and deleted rows in a changed partition are reflected too. A change the checksum can’t see isn’t reflected. See [Changes a checksum may not detect](#changes-a-checksum-may-not-detect).
- **Required keys or columns:** None. The partition columns set how much data a changed row reloads. `checksumExpression` must not contain `;`.
- **Performance and cost:** The source computes the checksum of every partition on every run, even when nothing changed. Cost grows with table size. An expression over an indexed row-version or SCN column is usually much cheaper than the default hash.
- **Blind spots and failure cases:** The default hash skips or normalizes some column types, so changes confined to them don’t trigger a reload. A custom expression sees only what it measures. A partition whose expression returns `NULL` is treated as unchanged on later runs. The first run always extracts every partition.
- **Native and Iceberg:** Supported on native targets. Supported on a Snowflake-managed Iceberg table this migration creates from a relational extract (`catalog: SNOWFLAKE`, with no `sourceDataStage`). A later run reuses that table when an earlier run of the same table completed, and it clears and reloads a partition whose checksum changed. `scai data migrate create-workflow` rejects `checksum` for an Iceberg target before the workflow starts.
- **Choose it when:** The table has no reliable monotonic column, such as a dimension table, and you need any change detected at partition granularity.
- **Avoid it when:** Reloading one changed partition is too costly for the table, or the checksum misses the columns that change and no expression fixes that.

#### watermark

- **Compares:** The highest value of `watermarkColumn` stored by the last successful run. Before `COPY INTO`, a run reads the maximum from its staged rows and keeps it as a candidate. The candidate becomes the stored maximum only when the partition completes, after `COPY INTO` succeeds.
- **Reloads:** Rows whose watermark value is greater than the stored maximum. With `trackDeletions`, the run also extracts the full primary-key list of each partition.
- **Inserts, updates, and deletes:**
  - Inserts are appended.
  - Updates are appended as a second version unless `trackModifications: true`. With it, changed rows are merged into the target by primary key. This applies to warehouse loading only.
  - Deletes aren’t reflected unless `trackDeletions: true`. With it, target rows whose primary key is missing from the source snapshot are deleted before the new rows load. Deletion tracking runs on incremental runs, not on the initial load.
- **Required keys or columns:** `watermarkColumn` is required and must increase on every change you want to migrate. It can be a pseudo-column or system column that isn’t migrated, such as Oracle `ORA_ROWSCN`. `primaryKeyColumns` is required for `trackDeletions`. `trackModifications` merges only when a primary key is available. Keys can be configured or inferred.
- **Performance and cost:** Each run reads the watermark column of each partition. `trackDeletions` scans the full primary-key set of each partition on every run, which adds load on the source for large partitions. `trackModifications` stages the changed rows in a transient table and runs a `MERGE` on the warehouse.
- **Blind spots and failure cases:**
  - A row updated without advancing `watermarkColumn` is never extracted again.
  - A row whose watermark value isn’t above the stored maximum is never extracted, including late-arriving rows with older values.
  - Deletes aren’t seen without `trackDeletions`.
  - An empty partition has no candidate, so the stored maximum doesn’t change and the next run starts from the same point.
  - If `COPY INTO` succeeds but the partition doesn’t reach completion, the stored maximum doesn’t advance. The next run extracts those rows again and appends them, unless `trackModifications` merges them by primary key.
- **Native and Iceberg:** Supported on native targets. Supported on the same Snowflake-managed Iceberg tables as `checksum`. The first load registers the extracted Parquet with `ADD_FILES_COPY`. A later run with `trackModifications: true` and a primary key merges changed rows into the table. `resetPartitions: enabledWithDedup` is rejected for an Iceberg target. `trackModifications` is rejected with `loading.strategy: snowpipe`. `trackDeletions` works with Snowpipe. `scai data migrate create-workflow` rejects `watermark` for an Iceberg target before the workflow starts.
- **Choose it when:** The table has a reliable column that increases on every change you need to migrate, such as `UPDATED_AT`, and a full reload is too costly. Add `trackModifications` and `trackDeletions` when the source updates or deletes rows.
- **Avoid it when:** No column increases on every change, updates don’t change the column, or the source backfills rows with older values.

#### State and reruns

- A run stores its state per partition in `PARTITION_METADATA.SYNCHRONIZATION_DATA`. `none` and `full-replace` store only their strategy name. `checksum` stores the checksum. `watermark` stores the column and the stored maximum.
- A table with no stored state is extracted in full, whichever strategy you choose. A table that’s empty on the first run has no stored maximum, so the first run after rows appear extracts all of them.
- A preflight records partition metadata like any other run. Don’t run one between a full load and later `checksum` or `watermark` runs of the same tables. See [When to run a preflight](#when-to-run-a-preflight).

### Changes a checksum may not detect

The default partition checksum hashes a **normalized subset** of columns. Some types are skipped outright. A row whose only change falls into one of the categories below won’t be detected, so its partition won’t be re-extracted.

This applies to `synchronization.strategy: checksum` during migration and to [incremental validation](./data-validation-configuration-reference#incremental-validation) probes, which use the same hashing.

| Category | Where it applies | Effect |
| --- | --- | --- |
| Skipped legacy large objects | SQL Server `TEXT`, `NTEXT`, `IMAGE`; Oracle LOBs, `LONG`, `XMLTYPE`, `VECTOR` | The column is excluded from the checksum input, so changes confined to it are invisible |
| Spatial values as text | SQL Server, Redshift, and Oracle `SDO_GEOMETRY` | Compared as Well-Known Text with spacing normalized, so binary geometry detail is lost |
| A custom `checksumExpression` | Any platform | Only that expression drives detection — whether a change is detected depends entirely on what the expression evaluates |
| Fully frozen partitions | PostgreSQL (`checksum` strategy) | The default PostgreSQL checksum fingerprints a partition from each row’s MVCC `xmin`. `VACUUM FREEZE` rewrites every row’s `xmin` to the same frozen value, so a fully frozen partition’s fingerprint depends only on its row count. An update that is frozen again between two consecutive sync runs may go undetected. Use a value-derived `checksumExpression` (for example `MAX(updated_at)`) or the `watermark` strategy. See [Migrating Data from PostgreSQL](../data-migration-validation/migrate-postgresql#incremental-sync-and-vacuum-freeze). |
| Skipped large objects | IBM DB2 `BLOB`, `CLOB`, `DBCLOB`, and `XML` | Checksum skips these types. If every column is one of them, the checksum is the partition row count, so a change that doesn’t change the row count isn’t detected. Use a watermark column. See [Migrating Data from IBM DB2](../data-migration-validation/migrate-db2#incremental-sync). |

Expand

Show lessSee more

If one of these applies to a column you need to track:

- Truncate the target table and run a full re-migration (`strategy: none`) to reconcile.
- Switch to `watermark` if the table has a reliable monotonic column.
- Use row-level validation to detect the difference after the fact.

### Affinity

Affinity routes workflow tasks to specific Workers. Use it when you run more than one Worker group and need each workflow to land on the right group, for example SPCS Workers for one source and on-premises Workers for another, or separate pools per team.

Set `affinity` on the workflow YAML and the same value (or a matching wildcard) on the Worker:

- Workflow: top-level `affinity` in the migration or validation YAML. There’s no per-table affinity: every task that the Orchestrator creates for the workflow carries the workflow’s value.
- Worker TOML: `[application].affinity`
- SPCS service: `AGENT_AFFINITY` in the container environment

The Orchestrator matches workflows by affinity too, through `DATA_MIGRATION_ORCHESTRATOR_AFFINITY`. Leave it unset. See [Orchestrator affinity](#orchestrator-affinity).

The string format is yours to define. Examples of valid values: `sql-server`, `DEV_SERVER`, `onprem-redshift`, `::blue::`.

Matching rules:

- A task without affinity is picked up by any Worker.
- A Worker without affinity picks up any task, including tasks that carry an affinity.
- A Worker with an affinity also picks up tasks without affinity.
- Otherwise, the Worker’s affinity must equal the task’s affinity exactly. The comparison is case-sensitive: `S1` doesn’t match `s1`.
- A Worker affinity can include `*` wildcards. For example, Worker affinity `team-*` matches workflow affinities `team-blue` and `team-red`. Only the Worker (or Orchestrator) value is a pattern; the workflow’s value is always compared as literal text. If a Worker affinity contains `*`, any `%` or `_` in that value also acts as a wildcard, so don’t use those characters there.

Validation workflows use the same `affinity` field and the same matching rules as migration.

#### Project default affinity

Every SnowConvert AI project has a default affinity, so a workflow and a Worker that you create in the same project match even when you never choose a value. The default has the form `<project-name>-<id>`, for example `northwind-3f9a1c2b`: the project name in lowercase with other characters replaced by hyphens, followed by the first eight hexadecimal digits of the project ID. It’s stored as `default_affinity` in `.scai/config/project.yml`, or in `.scai/config/project.local.yml`, which takes precedence. Change it with `scai project defaults set --affinity <value>`.

When you omit `--affinity`, these commands apply the project default:

- `scai data migrate generate-config` and `scai data validate generate-config` write it as the workflow’s `affinity`.
- `scai data worker setup` writes it as the SPCS service’s `AGENT_AFFINITY`.
- `scai data worker generate-config` writes it as `[application].affinity`.

A value that you pass with `--affinity` replaces the default for that command only. This has two consequences when you build Workers or workflows outside these commands:

- A Worker whose affinity you set by hand, for example `AGENT_AFFINITY: s1` in a service specification, doesn’t pick up workflows that carry the project default. Generate those workflows with `--affinity s1`, or set `affinity: s1` in the YAML.
- A workflow that you generate with `--affinity s1` isn’t picked up by Workers that carry the project default. When you submit it, `scai data migrate create-workflow` (or `scai data validate create-workflow`) warns that the workflow’s affinity differs from the project’s default affinity. The warning is expected when you route on purpose; check that a running Worker carries the same value.

#### Orchestrator affinity

The Orchestrator reads its affinity from `DATA_MIGRATION_ORCHESTRATOR_AFFINITY` and claims only the workflows that match it, using the rules above. When the variable is unset, the Orchestrator claims every workflow and creates each workflow’s tasks with that workflow’s affinity, which is what routes them to the right Workers. `scai data orchestrator setup` and `scai data orchestrator start` never set it.

Keep the Orchestrator without an affinity, including when you route work to several Worker groups. One Orchestrator serves every affinity. If you set the variable, workflows whose affinity doesn’t match stay `pending`. The Orchestrator logs its value at startup as `Orchestrator affinity: <value>`, where `None` means unset.

#### Affinity in rate-limit rules

The `AFFINITY` column of a [rate-limit](#rate-limiting) rule is compared with each task’s affinity exactly, without wildcards. Set it to the workflow affinity you want to cap. A rule without `AFFINITY` applies to tasks of every affinity.

### INTERVAL data type handling

AIM DMV migrates source `INTERVAL` columns to a native Snowflake `INTERVAL` target by default, extracting each value as Snowflake-parseable text and loading it with an explicit cast. Set `intervalHandling` at the workflow root, `defaultTableConfiguration`, or on an individual table to control this behavior.

| Value | Behavior |
| --- | --- |
| `"interval"` (default) | Migrate to a native Snowflake `INTERVAL` column. |
| `"varchar"` | Migrate the column as text (`VARCHAR`) instead of a native interval. |

Expand

Show lessSee more

Neither option is universally better. On source platforms whose `interval` type can mix year-month and day-time fields in one value (for example PostgreSQL), `"interval"` maps the column to Snowflake `INTERVAL DAY TO SECOND` and folds the year-month part into day-time (via total seconds on PostgreSQL). That keeps a native interval column but loses calendar-accurate year-month precision. Choose `"varchar"` to preserve the original interval text instead. See [INTERVAL columns and intervalHandling](../data-migration-validation/migrate-postgresql#interval-columns-and-intervalhandling) on the PostgreSQL migration page for the tradeoff.

Copy code

```
tables:
  - source:
      databaseName: MY_DB
      schemaName: sales
      tableName: orders
    target:
      databaseName: TARGET_DB
      schemaName: sales
      tableName: orders
    intervalHandling: interval
  - source:
      databaseName: MY_DB
      schemaName: sales
      tableName: legacy_intervals
    target:
      databaseName: TARGET_DB
      schemaName: sales
      tableName: legacy_intervals
    intervalHandling: varchar
```

Iceberg targets always coerce `INTERVAL` columns to `VARCHAR`, regardless of `intervalHandling`, because Iceberg has no native interval type. See platform-specific notes on the [Migrating Data from …](../data-migration-validation/data-migration) pages for interval support by source platform.

## Extraction strategies

Each table can set **`extraction.strategy`** (or inherit from **`defaultTableConfiguration.extraction`**). Worker TOML holds connection and platform-specific options (UNLOAD credentials, WRITE\_NOS location, BigQuery `EXPORT DATA` bucket).

| Strategy | Platforms | When to use |
| --- | --- | --- |
| **`unload`** | Redshift only | **Recommended default** when S3 and a Snowflake external stage are available. Redshift writes Parquet to S3; Snowflake loads from the external stage. Use for all tables from the source. See [Migrating Data from Amazon Redshift](../data-migration-validation/migrate-redshift). |
| **`write_nos`** | Teradata only | **Recommended default** when Teradata NOS and a Snowflake external stage are available. Server-side export to S3, Azure Blob, or GCS. Use for all tables from the source. See [Migrating Data from Teradata](../data-migration-validation/migrate-teradata). |
| **`dbms_cloud`** | Oracle only | **Recommended default** when object storage and a Snowflake external stage are available. Server-side export via `DBMS_CLOUD.EXPORT_DATA`. Use for all tables from the source. See [Migrating Data from Oracle](../data-migration-validation/migrate-oracle). |
| **`cet_as`** | SQL Server and Azure Synapse | Source-side CETAS export to Azure Blob. See [Migrating Data from SQL Server](../data-migration-validation/migrate-sql-server#using-cetas-extraction) and [Migrating Data from Azure Synapse Analytics](../data-migration-validation/migrate-synapse#using-cetas-extraction). |
| **`export_data`** | BigQuery only | Server-side `EXPORT DATA` writes Parquet to GCS. Snowflake loads from an external stage on the same prefix. See [Migrating Data from Google BigQuery](../data-migration-validation/migrate-bigquery). |
| **`cloud_direct`** | SQL Server, Azure Synapse, Redshift, Oracle, Teradata, PostgreSQL, and IBM DB2 | Worker streams query results directly to S3, GCS, or Azure Blob, skipping local disk and re-upload. On **IBM DB2** this is the preferred extract when an object store and external stage are available. See [Migrating Data from IBM DB2](../data-migration-validation/migrate-db2). |
| **`regular`** (default) | All | Worker pulls data over the source connection, then uploads to the Snowflake internal stage. On **PostgreSQL**, **`regular`** with COPY (`use_copy = true`) is the recommended extract. On **IBM DB2**, **`regular`** is the default when the workflow omits a strategy. |
| **`tpt`** | Teradata only | Legacy alias for **`regular`**. The Orchestrator treats `tpt` as `regular`. A Teradata Worker uses Teradata Parallel Transporter only when its own configuration allows it and `tbuild` is installed, which is never the case on SPCS. Use `write_nos` for a server-side export. See [Teradata TPT selection](#teradata-tpt-selection). |

Expand

Show lessSee more

**Regular (default):**

Copy code

```
tables:
  - source:
      databaseName: MY_DB
      schemaName: sales
      tableName: orders
    target:
      databaseName: TARGET_DB
      schemaName: sales
      tableName: orders
    columnNamesToPartitionBy:
      - order_id
```

**Redshift unload:**

Copy code

```
    extraction:
      strategy: unload
      externalStage: TARGET_DB.PUBLIC.S3_EXTERNAL_STAGE
```

**Teradata write\_nos:**

Copy code

```
    extraction:
      strategy: write_nos
      externalStage: TARGET_DB.SALES.MY_CLOUD_STAGE
```

**Oracle dbms\_cloud:**

Copy code

```
    extraction:
      strategy: dbms_cloud
      externalStage: TARGET_DB.DATA_MIGRATION.ORA_EXPORT_STAGE
```

**SQL Server cet\_as:**

Copy code

```
defaultTableConfiguration:
  extraction:
    strategy: cet_as
    externalStage: TARGET_DB.DATA_MIGRATION.AZURE_LANDING
```

**BigQuery export\_data:**

Copy code

```
defaultTableConfiguration:
  extraction:
    strategy: export_data
    externalStage: TARGET_DB.DATA_MIGRATION.GCS_EXPORT_STAGE
```

**Cloud direct:**

Copy code

```
defaultTableConfiguration:
  extraction:
    strategy: cloud_direct
    externalStage: TARGET_DB.DATA_MIGRATION.CLOUD_LANDING
```

**Teradata tpt (legacy alias for `regular`):**

`tpt` is accepted for compatibility and runs as `regular`.

Copy code

```
    extraction:
      strategy: tpt
```

## Constraints, identity columns, and sequences

AIM DMV data migration moves **table data**. It creates each target table with its columns and data types and loads rows; it does **not** author source **constraints** (CHECK, UNIQUE, PRIMARY KEY, FOREIGN KEY) or **identity columns**, **auto-increment columns**, or **sequences** from the source schema. Convert that DDL with SnowConvert — it translates constraints and identity/sequence definitions into Snowflake equivalents — and apply it as part of schema conversion. During a data load, CHECK constraints and generators are handled differently.

### CHECK constraints

You don’t need to drop or re-create CHECK constraints by hand. When a target table already has CHECK constraints (for example, ones created by SnowConvert), AIM DMV **temporarily removes them before loading the table and restores them after the load completes**. This keeps constraints that would otherwise reject in-flight rows during `COPY INTO` from blocking the migration, and leaves them in place once the load finishes — no manual step is required.

During a [`preflight`](#preflight-bounded-dry-run) dry run the constraints are removed but not restored (the transient preflight schema is discarded anyway), unless you set `preflightKeepSchema: true`.

### Identity columns and sequences

Migration copies the values in an identity/auto-increment column (or a sequence-fed column) as ordinary data, but it does not create or advance the target’s generator. Snowflake fixes a sequence’s or identity column’s starting value **at creation time** and has no runtime “reseed”, so create the target generator with a `START` past the highest migrated value:

Copy code

```
-- 1. Read the loaded maximum.
SELECT MAX(ID) AS max_id FROM TARGET_DB.PUBLIC.ORDERS;

-- 2. Create the sequence starting after it (substitute max_id + 1).
CREATE SEQUENCE IF NOT EXISTS TARGET_DB.PUBLIC.ORDERS_SEQ START = <max_id + 1> INCREMENT = 1;

-- 3. Use it as the column default for new inserts.
ALTER TABLE TARGET_DB.PUBLIC.ORDERS
  ALTER COLUMN ID SET DEFAULT TARGET_DB.PUBLIC.ORDERS_SEQ.NEXTVAL;
```

Do this once the final data load completes. For [incremental sync](#synchronizationstrategy-model), reseed at cutover, when writes move to Snowflake — otherwise later incremental loads would collide with generator values already handed out. SnowConvert emits the sequence/identity DDL during schema conversion; adjust its `START` to clear the migrated range.

## Worker configuration

The Worker configuration file uses [TOML](https://toml.io/) format. For cloud data migration, set `selected_task_source` to `"snowflake_stored_procedure"` and provide a matching **`[task_source.snowflake_stored_procedure]`** section.

| Section | Property | Type | Description |
| --- | --- | --- | --- |
| Top level | `selected_task_source` | `String` | Required. Use `"snowflake_stored_procedure"`. |
| `[task_source.snowflake_stored_procedure]` | `connection_name` | `String` | Snowflake connection name for task-queue stored procedures, or `"@SPCS_CONNECTION"` on SPCS. |
| `[application]` | `max_parallel_tasks` | `Integer` | Maximum parallel tasks (threads). Defaults to `4`. The SPCS Worker image uses `2` unless you set `MAX_PARALLEL_TASKS`. See [Worker container: core settings](#worker-container-core-settings). |
| `[application]` | `task_fetch_interval` | `Integer` | Seconds between idle polls for new tasks. Defaults to `5`. |
| `[application]` | `lease_refresh_interval` | `Integer` | Optional. Seconds between task lease renewals (default `120`). |
| `[application]` | `affinity` | `String` | Optional. Worker affinity for task routing. May include `*` wildcards. See [Affinity](#affinity). |
| `[application]` | `snowflake_database_for_metadata` | `String` | Optional. Database holding the migration and validation metadata procedures (default `SNOWCONVERT_AI`). Must match the Orchestrator’s `CUSTOM_SNOWFLAKE_DATABASE_FOR_METADATA`. |
| `[application]` | `snowflake_schema_for_data_migration_metadata` | `String` | Optional. Schema holding the migration task-queue procedures (default `DATA_MIGRATION`). Must match the Orchestrator’s `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_MIGRATION_METADATA`. |
| `[application]` | `snowflake_schema_for_data_validation_metadata` | `String` | Optional. Schema holding validation-specific objects such as the results stage and file format (default `DATA_VALIDATION`). Must match the Orchestrator’s `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_VALIDATION_METADATA`. |
| `[application]` | `local_results_directory` | `String` | Optional. Base directory for exported Parquet/CSV before upload. |
| `[idle_shutdown]` | `minutes` | `Integer` | Optional. Minutes without work after which the Worker shuts itself down (default `60`). `DM_IDLE_SHUTDOWN_MINUTES` overrides it. See [Idle shutdown settings](#idle-shutdown-settings). |
| `[connections.source.*]` | (per engine) | `Object` | Source database connection. Typically one active source section. |
| `[connections.source.*]` | `plugin_class` | `String` | Optional. Fully qualified class name of a custom extraction plugin that replaces the built-in extractor for this source connection. See [Preparing a custom extraction plugin](../data-migration-validation/data-migration-advanced-configuration#preparing-a-custom-extraction-plugin). |
| `[connections.source.sqlserver]` | `prefer_native_driver` | `Boolean` | Optional. Defaults to `true`. Set to `false` to force the ODBC fallback. |
| `[connections.source.sqlserver]` | `set_context_info` | `Boolean` | Optional. Defaults to `true`. Set to `false` to prevent the native driver from tagging the SQL Server session with `SET CONTEXT_INFO`. |
| `[connections.target.s3]` | (S3 storage settings) | `Object` | S3 target for `cloud_direct`. Requires `bucket_name`; optional fields include `profile_name`, `region_name`, and `prefix`. |
| `[connections.target.gcs]` | (GCS storage settings) | `Object` | GCS target for `cloud_direct`. Requires `bucket_name`; optional fields include `project_id`, `credential_file_path`, and `prefix`. |
| `[connections.target.blob]` | (Azure storage credentials) | `Object` | Azure Blob target for `cloud_direct`. Requires `container_name` and either `connection_string`, or `account_name` with `account_key`, `sas_token`, or `use_default_credential = true`. |
| `[connections.target.snowflake_connection_name]` | `connection_name` | `String` | Snowflake profile for data sessions (loads). |

Expand

Show lessSee more

Example minimal Worker config:

Copy code

```
selected_task_source = "snowflake_stored_procedure"

[task_source.snowflake_stored_procedure]
connection_name = "my-snowflake"

[application]
max_parallel_tasks = 4
task_fetch_interval = 30

[connections.source.sqlserver]
username = "username"
password = "password"
database = "database_name"
host = "127.0.0.1"
port = 1433
prefer_native_driver = true
set_context_info = true

[connections.target.snowflake_connection_name]
connection_name = "my-snowflake"
```

Platform-specific `[connections.source.*]` and cloud target examples live on each [Migrating Data from …](../data-migration-validation/data-migration) page.

### Using a custom extraction plugin

Set `plugin_class` on the source connection to replace the built-in extractor entirely. The Worker imports and runs your class in place of the `regular` (or other built-in) strategy for that connection:

Copy code

```
[connections.source.sqlserver]
plugin_class = "acme_ext.my_extractor.MyExtractor"
username = "my_user"
password = "my_password"
database = "my_database"
host = "db.example.com"
port = 1433
```

See [Preparing a custom extraction plugin](../data-migration-validation/data-migration-advanced-configuration#preparing-a-custom-extraction-plugin) for what the plugin must implement and how to package it.

### Matching metadata locations between the Orchestrator and Workers

If you override where AIM DMV keeps its metadata, the Orchestrator and every Worker have to agree. The Orchestrator reads environment variables; Workers read the matching `[application]` TOML keys.

| Metadata location | Orchestrator environment variable | Worker TOML key | Default |
| --- | --- | --- | --- |
| Metadata database | `CUSTOM_SNOWFLAKE_DATABASE_FOR_METADATA` | `snowflake_database_for_metadata` | `SNOWCONVERT_AI` |
| Migration schema | `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_MIGRATION_METADATA` | `snowflake_schema_for_data_migration_metadata` | `DATA_MIGRATION` |
| Validation schema | `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_VALIDATION_METADATA` | `snowflake_schema_for_data_validation_metadata` | `DATA_VALIDATION` |

Expand

Show lessSee more

The database and migration schema keys are read from **TOML or the CLI only** at Worker runtime. Use the matching `[application]` TOML key on each Worker to match the Orchestrator’s environment variable.

Note

The Worker container image is the exception. Its entrypoint writes `CUSTOM_SNOWFLAKE_DATABASE_FOR_METADATA`, `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_MIGRATION_METADATA`, and `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_VALIDATION_METADATA` into these `[application]` keys at startup, and `scai data worker setup` sets all three in the service specification. See [Orchestrator and Worker settings](#shared-environment-variables).

See [Customizing metadata database and schema names](../data-migration-validation/required-privileges#customizing-metadata-database-and-schema-names) for the privileges these objects need.

### Resolving credentials from an external secret manager

Worker TOML examples show credentials inline for brevity. On a **local or otherwise non-SPCS Worker**, you can instead resolve them at startup from an external secret store, so no plaintext password lives in the file.

Note

SPCS Workers don’t need this. They read source credentials from Snowflake `SECRET` objects bound into the service specification. See [Manual SPCS worker setup](./manual-spcs-worker-setup#network-access-objects).

Register providers in a **separate** TOML file and point the Worker at it with the `SECRET_MANAGERS_CONFIG_FILE` environment variable:

Copy code

```
[secret_managers.providers.vault]
type = "rest"
base_url = "https://vault.example.com/v1/secret/data/dea"
```

Then reference a resolved value in a connection field using the provider scheme, naming the provider, path, and field:

Copy code

```
[connections.source.sqlserver]
username = "my_user"
password = "vault://sqlserver/prod#password"
```

| Environment variable | Default | Purpose |
| --- | --- | --- |
| `SECRET_MANAGERS_CONFIG_FILE` | Unset | Path to the TOML file containing `[secret_managers.providers.*]` blocks. |
| `SECRET_MANAGERS_ALLOW_CMD_SUBSTITUTION` | `false` | Allows `$(...)` command recipes in configuration strings. |
| `SECRET_MANAGERS_CACHE_TTL_SECONDS` | `300` | How long a resolved secret is cached. |
| `SECRET_MANAGERS_RESOLVE_TIMEOUT_SECONDS` | `10` | Per-resolution timeout. |

Expand

Show lessSee more

The `[secret_managers]` configuration goes in its own separate TOML file, not in the Worker TOML. Use `SECRET_MANAGERS_CONFIG_FILE` to point the Worker at it.

AIM DMV can also resolve a field by running a shell command, for example `$( aws secretsmanager get-secret-value --secret-id prod/db )#password`.

Warning

Command substitution executes arbitrary shell commands with the Worker’s own privileges, so treat the configuration file as trusted code. It’s disabled by default: set `SECRET_MANAGERS_ALLOW_CMD_SUBSTITUTION=true` only on hosts where you control who can edit Worker configuration, and prefer a REST provider when one is available.

## Environment variables

Most settings live in the workflow YAML and the Worker TOML. Environment variables matter in three places:

- **The Orchestrator process** reads its Snowflake connection, metadata locations, and tuning settings from its environment.
- **Settings shared by the Orchestrator and Workers**, such as task retries and metadata storage mode, are read by both processes. Set them to the same values on both.
- **The Worker container image** that `scai data worker setup` deploys to SPCS has no Worker TOML of its own. At startup, its entrypoint builds the Worker TOML from environment variables. A Worker that you start from a TOML file on your own host doesn’t run that entrypoint, so the Worker container variables don’t affect it unless a row says otherwise. Set the TOML key listed in each table instead.

The tables in this section use these columns:

- **Required**: whether the process fails, or the strategy doesn’t work, without the variable.
- **Default**: the value used when the variable is unset. “None” means the setting is left out.
- **TOML key** (Worker tables only): the Worker TOML key that the container entrypoint writes, which is also the key to set on a Worker you run from TOML.
- **Set by `scai`**: whether `scai` writes the variable into the SPCS service specification. “No” means you add the variable to the specification yourself.

Values marked **Secret** must come from a Snowflake `SECRET` bound in the specification’s `secrets` section, not from `env`, because `DESCRIBE SERVICE` shows `env` values. See [Passing other secrets to the Worker](./manual-spcs-worker-setup#passing-other-secrets-to-the-worker).

Important

`scai data worker update` keeps variables that you added to the service specification yourself, because it reuses the deployed specification. It re-creates the service with the new image, which returns the service to one instance. `scai data worker setup --yes` drops the service and re-creates it from its own specification, so add your variables again after you run it.

### Orchestrator settings

The Orchestrator reads these variables from its own environment. On SPCS, add the ones that `scai` doesn’t set to the Orchestrator service specification:

| Variable | Required | Default | Description | Set by `scai` |
| --- | --- | --- | --- | --- |
| `SNOWFLAKE_CONNECTION_NAME` | Local Orchestrator, unless you set `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, and `SNOWFLAKE_PASSWORD` | None | Name of a connection in your connections file. On SPCS, the Orchestrator authenticates with the service’s OAuth token and ignores this variable. | Yes, for a local Orchestrator |
| `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD` | Local Orchestrator without `SNOWFLAKE_CONNECTION_NAME` | None | Password authentication when no connection name is set. The Orchestrator stops if any of the three is missing. `SNOWFLAKE_PASSWORD` is **Secret**. | No |
| `CUSTOM_SNOWFLAKE_SCHEMA_FOR_COMMON_METADATA` | No | `COMMON` | Shared metadata schema. | Yes |
| `CUSTOM_SNOWFLAKE_SCHEMA_FOR_TEMP_METADATA` | No | `TEMP` | Schema for transient Snowpipe stage and pipe objects. | Yes |
| `SNOWFLAKE_METADATA_EXTERNAL_VOLUME` | When `SNOWFLAKE_METADATA_STORAGE_MODE` is `ICEBERG` | None | External volume for Iceberg metadata tables. There’s no fallback to native tables if it’s missing. | No |
| `SNOWFLAKE_USE_HYBRID_TABLES` | No | None | Legacy storage-mode selector. `1`, `true`, `yes`, or `on` selects `HYBRID`; `0`, `false`, `no`, or `off` selects `STANDARD`. Prefer `SNOWFLAKE_METADATA_STORAGE_MODE`. Setting both to different modes, or this variable to true with `ICEBERG`, is an error. | No |
| `DM_SPCS_SUSPEND_AGENT_SERVICE` | No | None, so the Orchestrator suspends no Worker | On SPCS, the one Worker service that the Orchestrator suspends at idle shutdown, before it suspends itself. Takes a single fully qualified service name; `scai` qualifies the name that you pass to `--worker-service-name`. Other Worker services suspend only themselves. See [Idle shutdown settings](#idle-shutdown-settings). | Yes: `DATA_EXCHANGE_WORKER_SERVICE` in the migration metadata schema (`SNOWCONVERT_AI.DATA_MIGRATION` by default), or the name from `scai data orchestrator setup --worker-service-name` |
| `DM_SPCS_SUSPEND_ORCHESTRATOR_SERVICE` | No | The Orchestrator’s own service, from the `SNOWFLAKE_SERVICE_NAME` that SPCS sets | On SPCS, the service that the Orchestrator suspends last at idle shutdown, normally its own. | Yes: `DATA_MIGRATION_SERVICE` in the migration metadata schema (`SNOWCONVERT_AI.DATA_MIGRATION` by default) |
| `ORCHESTRATOR_MAX_TASK_WORKERS` | No | `8` | Number of persistent threads the Orchestrator uses to run tasks. Positive integer. An invalid or non-positive value falls back to the default with a warning. | No |
| `ORCHESTRATOR_TASK_PULL_INTERVAL_SECONDS` | No | `20` | Seconds between Orchestrator pulls from the task queue. Positive integer. An invalid or non-positive value falls back to the default with a warning. | No |
| `ORCHESTRATOR_WORKFLOW_CYCLE_INTERVAL_SECONDS` | No | `10` | Seconds between workflow cycles. Non-negative integer; `0` is allowed. An invalid or negative value falls back to the default with a warning. | No |
| `ORCHESTRATOR_SF_CONNECTION_MAX_AGE_SECONDS` | No | `10800` (3 hours) | Age after which the Orchestrator replaces a Snowflake connection at the next safe point. `0` or a negative value turns age-based replacement off. A value that isn’t an integer falls back to the default with a warning. | No |
| `DATA_MIGRATION_ORCHESTRATOR_AFFINITY` | No | None, so the Orchestrator claims every workflow | Orchestrator affinity. Leave it unset. When set, the Orchestrator claims only matching workflows and the rest stay `pending`. See [Orchestrator affinity](#orchestrator-affinity). | No |

Expand

Show lessSee more

### Orchestrator and Worker settings

Both processes read these variables. Set each one to the same value for the Orchestrator and every Worker, except `DM_IDLE_SHUTDOWN_MINUTES`, which each process applies to itself:

| Variable | Required | Default | Description | TOML key | Set by `scai` |
| --- | --- | --- | --- | --- | --- |
| `DM_IDLE_SHUTDOWN_MINUTES` | No | `60` | Minutes without work after which the process shuts itself down. Each process applies its own value. On a Worker, it overrides the TOML key. A value that isn’t a positive integer falls back to `60`, not to the TOML key, with a warning. See [Idle shutdown settings](#idle-shutdown-settings). | `[idle_shutdown]` `minutes` | No |
| `DMVF_TASK_MAX_RETRIES` | No | `3` | Retries a failed task gets after its first attempt, so up to four attempts by default. Tasks that aren’t safe to repeat always get `0`. Non-negative integer; any other value is rejected with an error. | None | No |
| `DMVF_TASK_RETRY_BACKOFF_SECONDS` | No | `30` | Delay before the first retry. Each later retry waits twice as long as the one before. `0` retries immediately. Non-negative integer. | None | No |
| `DMVF_TASK_RETRY_BACKOFF_MAX_SECONDS` | No | `600` | Upper bound on any one retry delay. Non-negative integer. | None | No |
| `SNOWFLAKE_METADATA_STORAGE_MODE` | On Workers, when metadata uses `ICEBERG` | Orchestrator: probed at startup. Worker: native tables. | `HYBRID`, `STANDARD`, or `ICEBERG`, case-insensitive. The Orchestrator uses it to choose how metadata tables are created. See [Metadata storage mode](#metadata-storage-mode). Workers don’t probe: they only check whether the value is `ICEBERG`, and use it to write their events in the form that Iceberg metadata tables expect. | None | No |
| `CUSTOM_SNOWFLAKE_DATABASE_FOR_METADATA` | No | `SNOWCONVERT_AI` | Metadata database. A Worker that you run from TOML reads only the TOML key. See [Matching metadata locations](#matching-metadata-locations). | `[application]` `snowflake_database_for_metadata` | Yes |
| `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_MIGRATION_METADATA` | No | `DATA_MIGRATION` | Migration metadata schema. A Worker that you run from TOML reads only the TOML key. | `[application]` `snowflake_schema_for_data_migration_metadata` | Yes |
| `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_VALIDATION_METADATA` | No | `DATA_VALIDATION` | Validation metadata schema. A Worker that you run from TOML uses the TOML key, and falls back to this variable when the key is unset. | `[application]` `snowflake_schema_for_data_validation_metadata` | Yes |

Expand

Show lessSee more

Note

The Orchestrator resolves the storage mode once and caches it for the life of the process. **Restart the Orchestrator** after you change `SNOWFLAKE_METADATA_STORAGE_MODE`.

A Worker that you run from TOML also reads the `SECRET_MANAGERS_*` variables. See [Resolving credentials from an external secret manager](#external-secret-manager).

### Idle shutdown settings

The Orchestrator and every Worker shut themselves down after a period without work. Idle shutdown is always on, and each process measures its own period:

| Process | Idle when | Period | On SPCS | On your own hosts or in Kubernetes |
| --- | --- | --- | --- | --- |
| Orchestrator | It has no active, pending, or upcoming work. | `DM_IDLE_SHUTDOWN_MINUTES`, default `60` | Suspends the Worker service in `DM_SPCS_SUSPEND_AGENT_SERVICE`, then the service in `DM_SPCS_SUSPEND_ORCHESTRATOR_SERVICE`. | Exits. |
| Worker | It has pulled no tasks and holds none. | `DM_IDLE_SHUTDOWN_MINUTES`, then `[idle_shutdown]` `minutes`, default `60` | Suspends its own service. | Exits. |

Expand

Show lessSee more

- `scai` sets neither `DM_IDLE_SHUTDOWN_MINUTES` nor `[idle_shutdown]` `minutes`, so the services it creates use 60 minutes.
- `DM_SPCS_SUSPEND_AGENT_SERVICE` names one Worker service. Every other Worker service is suspended only by its own idle shutdown.
- If a Worker can’t suspend its own service, it stays up and retries after 1, 2, 4, 8, and 16 minutes, then waits for another full idle period.
- A suspended service stays suspended until you resume it with `scai data orchestrator start` or `scai data worker start`.

For what this means when you run several Workers, and how to resume them before the next wave, see [Idle shutdown with several Workers](../data-migration-validation/deploy-workers#idle-shutdown-with-several-workers).

### Worker container: Core settings

These variables apply to every Worker container, whatever the source platform:

| Variable | Required | Default | Description | TOML key | Set by `scai` |
| --- | --- | --- | --- | --- | --- |
| `DATA_SOURCE_TYPE` | For every source except SQL Server | `sqlserver` | Selects the driver the container installs at startup and the source section it writes. For the platforms in this documentation, use `sqlserver`, `azure_synapse`, `redshift`, `oracle`, `postgresql`, or `teradata`. An unrecognized value stops the container. Leaving it unset for another platform installs the SQL Server driver and writes a SQL Server connection. | Section name, for example `[connections.source.redshift]` | Yes |
| `DATA_SOURCE_HOST` | Yes | None | Source host. For Azure Synapse, the workspace SQL endpoint. | `host` | Yes |
| `DATA_SOURCE_PORT` | For `redshift`, `oracle`, and `postgresql` | `teradata`: `1025`. `azure_synapse`: `1433`. `sqlserver`: `443`. Others: none. | Source port. Without a value for Redshift, Oracle, or PostgreSQL, the Worker can’t parse its configuration and exits. For SQL Server, set it explicitly: the fallback is `443`, not the SQL Server default `1433`. | `port` | Yes |
| `DATA_SOURCE_DATABASE` | Yes | None | Source database. For Oracle, the service name. For Azure Synapse, the dedicated pool name, or `master` for a serverless pool. | `database` | Yes |
| `DATA_SOURCE_USERNAME` | For password authentication | None | Source user. Not used with Azure Synapse `azure_ad` mode. | `username` | Yes, from the `username` key of the source `PASSWORD` secret |
| `DATA_SOURCE_PASSWORD` | For password authentication | None | **Secret.** Source password. Not used with Azure Synapse `azure_ad` mode. | `password` | Yes, from the `password` key of the source `PASSWORD` secret |
| `MAX_PARALLEL_TASKS` | No | `WORKER_COUNT`, which the image sets to `2` | Tasks each Worker instance runs at once. The Worker TOML default is `4`, so a container Worker runs half as many tasks as a TOML Worker unless you set this variable. Size instance resources to match. See [Instance count and resource sizing](./manual-spcs-worker-setup#instance-count-and-resource-sizing). | `[application]` `max_parallel_tasks` | No |
| `WORKER_COUNT` | No | `2` | Older name for `MAX_PARALLEL_TASKS`. Used only when `MAX_PARALLEL_TASKS` is unset. | `[application]` `max_parallel_tasks` | No |
| `AGENT_AFFINITY` | No | None, so the Worker picks up any task. `scai data worker setup` always sets it. | Worker affinity. Can include `*` wildcards. See [Affinity](#affinity). | `[application]` `affinity` | Yes, from `--affinity`, or the [project default affinity](#project-default-affinity) when you omit it |
| `PREFER_NATIVE_DRIVER` | No | None, so the native driver is used | `true` or `false`, case-insensitive. Any other value stops the container. `false` forces the ODBC fallback. | `prefer_native_driver` | No |
| `DATA_SOURCE_SESSION_LABEL` | No | None | Label appended to the reserved `SNOWFLAKE-AIM-DMV/<version>` session identifier: `program_name` on SQL Server and Azure Synapse, `application_name` on Redshift and PostgreSQL. Oracle and Teradata ignore it; use `ORACLE_CLIENT_INFO` or `TERADATA_QUERY_BAND` instead. | `session_label` | No |

Expand

Show lessSee more

The image fixes some TOML values that no environment variable changes: `task_fetch_interval = 5` and `debug_mode = false` for every source, `use_bcp = true` for SQL Server, and `auth_method = "standard"` with `auto_detect_driver = false` for Redshift. To change them, run the Worker from your own TOML.

### Worker container: Snowflake connection

On SPCS, keep the default connection. The Worker then authenticates with the service’s OAuth token and uses the `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_HOST`, `SNOWFLAKE_DATABASE`, and `SNOWFLAKE_SCHEMA` variables that Snowflake sets in every service container. Don’t set those four yourself. Snowflake doesn’t set `SNOWFLAKE_WAREHOUSE`. For more information, see [Snowpark Container Services: SQL execution](/developer-guide/snowpark-container-services/spcs-execute-sql). The following table lists each variable:

| Variable | Required | Default | Description | TOML key | Set by `scai` |
| --- | --- | --- | --- | --- | --- |
| `SNOWFLAKE_CONNECTION_NAME` | No | `@SPCS_CONNECTION` | `@SPCS_CONNECTION` uses the SPCS OAuth token. Outside SPCS, set `MY_SNOWFLAKE_CONNECTION` to use the connection that the container builds from `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, and `SNOWFLAKE_PASSWORD`. | `connection_name` in `[task_source.snowflake_stored_procedure]` and `[connections.target.snowflake_connection_name]` | No |
| `SNOWFLAKE_WAREHOUSE` | On SPCS, unless the service sets `QUERY_WAREHOUSE` | None | Warehouse for the Worker’s Snowflake sessions. When it’s unset, a session on SPCS uses the service’s `QUERY_WAREHOUSE`. If you set both, use the same warehouse. | `warehouse` in the connections file | Yes, from the Snowflake connection’s warehouse or `--warehouse` |
| `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD` | Outside SPCS, for `MY_SNOWFLAKE_CONNECTION` | None | Password authentication for the connection the container builds. `SNOWFLAKE_PASSWORD` is **Secret**. | `account`, `user`, and `password` in the connections file | No |
| `SNOWFLAKE_ROLE` | No | None | Role added to the connection the container builds outside SPCS. | `role` in the connections file | No |

Expand

Show lessSee more

### Worker container: SQL Server and Azure Synapse

These variables apply when `DATA_SOURCE_TYPE` is `sqlserver` or `azure_synapse`. On every start, a SQL Server container installs Microsoft ODBC Driver 18 and the BCP tools, and an Azure Synapse container installs Microsoft ODBC Driver 18, whichever driver the connection uses. `regular` extraction from SQL Server always uses BCP in the container. The `cet_as` variables apply to the `cet_as` strategy; see [Migrating Data from SQL Server](../data-migration-validation/migrate-sql-server#using-cetas-extraction). The following table lists each variable:

| Variable | Required | Default | Description | TOML key | Set by `scai` |
| --- | --- | --- | --- | --- | --- |
| `DATA_SOURCE_ENCRYPT` | No | None, so the driver default applies | Encrypt the connection. `true` or `false`; any other value stops the container. | `encrypt` | Yes, from the source connection |
| `DATA_SOURCE_TRUST_SERVER_CERTIFICATE` | No | None, so the driver default applies | Trust the server certificate. `true` or `false`; any other value stops the container. | `trust_server_certificate` | Yes, from the source connection |
| `DATA_SOURCE_MODE` | No | `sql_auth` | Azure Synapse only. `sql_auth` uses `DATA_SOURCE_USERNAME` and `DATA_SOURCE_PASSWORD`. `azure_ad` uses a service principal from `DATA_SOURCE_CLIENT_ID` and `DATA_SOURCE_CLIENT_SECRET`. | `mode` | Yes, from the source connection |
| `DATA_SOURCE_POOL_TYPE` | No | `dedicated` | Azure Synapse only. `dedicated` or `serverless`. | `pool_type` | Yes, from the source connection |
| `DATA_SOURCE_CLIENT_ID` | For `azure_ad` | None | Azure Synapse only. Service principal client ID. | `client_id` | Yes, from the `username` key of the source secret in `azure_ad` mode |
| `DATA_SOURCE_CLIENT_SECRET` | For `azure_ad` | None | **Secret.** Azure Synapse only. Service principal client secret. | `client_secret` | Yes, from the `password` key of the source secret in `azure_ad` mode |
| `DATA_SOURCE_ODBC_DRIVER` | No | `ODBC Driver 18 for SQL Server` | Azure Synapse only. ODBC driver name. | `odbc_driver` | No |
| `DATA_SOURCE_QUERY_TIMEOUT_SECONDS` | No | None, so queries don’t time out | Azure Synapse only. Integer query timeout in seconds, so a blocked extract fails instead of hanging. | `query_timeout_seconds` | No |
| `DATA_SOURCE_CET_AS_EXTERNAL_DATA_SOURCE` | For `cet_as` | None | `EXTERNAL DATA SOURCE` on the source. The Worker turns CETAS on only when this variable and `DATA_SOURCE_CET_AS_FILE_FORMAT` are both set; with only one, CETAS stays off without an error. | `cet_as_external_data_source` | Yes, from the Worker configuration |
| `DATA_SOURCE_CET_AS_FILE_FORMAT` | For `cet_as` | None | Parquet `EXTERNAL FILE FORMAT` on the source. | `cet_as_file_format` | Yes, from the Worker configuration |
| `DATA_SOURCE_CET_AS_PATH_PREFIX` | No | None, so files land at the container root | Path inside the container. Must match the external stage URL so `COPY INTO` reads the same files. | `cet_as_path_prefix` | Yes, from the Worker configuration |
| `DATA_SOURCE_CET_AS_TABLE_SCHEMA` | No | `dbo` | Schema for the transient external table that CETAS creates. The source user needs `CREATE TABLE` there. | `cet_as_table_schema` | No |

Expand

Show lessSee more

### Worker container: Amazon Redshift

These variables apply when `DATA_SOURCE_TYPE` is `redshift` and a table uses the `unload` strategy. `regular` extraction ignores them. See [Migrating Data from Amazon Redshift](../data-migration-validation/migrate-redshift). The following table lists each variable:

| Variable | Required | Default | Description | TOML key | Set by `scai` |
| --- | --- | --- | --- | --- | --- |
| `UNLOAD_S3_BUCKET` | For `unload` | None | S3 bucket that Redshift unloads to. | `unload_s3_bucket` | Yes, from the Worker configuration |
| `UNLOAD_IAM_ROLE_ARN` | For `unload` | None | IAM role that Redshift assumes to write to the bucket. An identifier, not a credential. | `unload_iam_role_arn` | Yes, from the Worker configuration |
| `UNLOAD_S3_PREFIX` | No | None | Path inside the bucket. Must match the external stage URL. | `unload_s3_prefix` | Yes, from the Worker configuration |
| `UNLOAD_FILE_FORMAT` | No | `parquet` | The Worker also accepts `csv`, but the Redshift migration queries are built for Parquet output, so keep the default. | `unload_file_format` | No |
| `UNLOAD_MAX_FILE_SIZE_MB` | No | `256` | Integer maximum size, in MB, of each unloaded file. | `unload_max_file_size_mb` | No |

Expand

Show lessSee more

### Worker container: Oracle

These variables apply when `DATA_SOURCE_TYPE` is `oracle`. The container uses the `oracledb` thin driver and installs no Oracle client. The `DBMS_CLOUD` variables apply to the `dbms_cloud` strategy; see [Migrating Data from Oracle](../data-migration-validation/migrate-oracle). The following table lists each variable:

| Variable | Required | Default | Description | TOML key | Set by `scai` |
| --- | --- | --- | --- | --- | --- |
| `DBMS_CLOUD_CREDENTIAL_NAME` | For `dbms_cloud` | None | Name of the Oracle `DBMS_CLOUD` credential. The name only, not the credential’s secret. | `dbms_cloud_credential_name` | Yes, from the Worker configuration |
| `DBMS_CLOUD_FILE_URI_PREFIX` | For `dbms_cloud` | None | Object storage URI prefix that Oracle writes to. Must match the external stage URL. | `dbms_cloud_file_uri_prefix` | Yes, from the Worker configuration |
| `ORACLE_CLIENT_INFO` | No | None | Session tag in the form `name=value;name2=value2`, written to the `CLIENT_INFO` slot of `DBMS_APPLICATION_INFO`. `MODULE` and `ACTION` carry the reserved application name and version. | `client_info` | No |
| `ORACLE_WALLET_LOCATION` | No | None | Has no effect. The container writes this value to a key that the Worker’s Oracle connection doesn’t read. For a wallet (mTLS) connection, run the Worker from TOML and set `wallet_directory`. | None | No |
| `TNS_ADMIN` | No | None | Not read by the container entrypoint. The Worker sets `TNS_ADMIN` itself, from the `tns_admin` TOML key, while it opens an Oracle connection. | `tns_admin` | No |

Expand

Show lessSee more

### Worker container: Teradata

These variables apply when `DATA_SOURCE_TYPE` is `teradata`. On every start, the container installs the `teradatasql` driver from PyPI. It includes no Teradata ODBC driver and no `tbuild`. The `WRITE_NOS_*` variables apply to the `write_nos` strategy; see [Migrating Data from Teradata](../data-migration-validation/migrate-teradata). The following table lists each variable:

| Variable | Required | Default | Description | TOML key | Set by `scai` |
| --- | --- | --- | --- | --- | --- |
| `TERADATA_AUTHENTICATION` | No | `TD2` | Logon mechanism, case-insensitive. Common values: `TD2`, `TDNEGO`, `LDAP`, `KRB5`, `JWT`, and `BEARER`. | `authentication` | Yes, from the source connection |
| `TERADATA_JWT_TOKEN` | For `JWT` | None | **Secret.** JWT passed to `teradatasql` when the mechanism is `JWT`. | `jwt_token` | No |
| `TERADATA_BEARER_TOKEN` | For `BEARER` | None | **Secret.** OAuth bearer token passed to `teradatasql` when the mechanism is `BEARER`. | `bearer_token` | No |
| `TERADATA_DBC_NAME` | No | None | DBC name or COP alias override. | `dbc_name` | No |
| `TERADATA_ODBC_DRIVER` | No | None | ODBC driver name for the ODBC fallback. Setting it also turns off driver auto-detection. The container includes no Teradata ODBC driver. | `odbc_driver` | No |
| `TERADATA_QUERY_BAND` | No | None | Query band in the form `name=value;name2=value2`, merged with the reserved `ApplicationName=SNOWFLAKE-AIM-DMV` and `Version` entries, which you can’t override. | `query_band` | No |
| `WRITE_NOS_LOCATION_SCHEME` | For `write_nos` | None | `/s3/`, `/az/`, or `/gs/`. `write_nos` is configured only when this variable and `WRITE_NOS_LOCATION_HOST` are both set. | `write_nos_location_scheme` | Yes, from the Worker configuration |
| `WRITE_NOS_LOCATION_HOST` | For `write_nos` | None | Object storage host, for example `myaccount.blob.core.windows.net`. | `write_nos_location_host` | Yes, from the Worker configuration |
| `WRITE_NOS_LOCATION_CONTAINER` | No | None | Bucket or container, optionally with a path. Must match the external stage URL. | `write_nos_location_container` | Yes, from the Worker configuration |
| `WRITE_NOS_FUNCTION_MAPPING` | One credential mode for `write_nos` | None | Function mapping name. The recommended credential mode. | `write_nos_function_mapping` | Yes, from the Worker configuration |
| `WRITE_NOS_AUTHORIZATION_NAME` | One credential mode for `write_nos` | None | Name of a Teradata authorization object. The name only, not the credential. | `write_nos_authorization_name` | Yes, from the Worker configuration |
| `WRITE_NOS_ACCESS_ID` | One credential mode for `write_nos`, with `WRITE_NOS_ACCESS_KEY` | None | **Secret.** Object storage access ID. | `write_nos_access_id` | No |
| `WRITE_NOS_ACCESS_KEY` | One credential mode for `write_nos`, with `WRITE_NOS_ACCESS_ID` | None | **Secret.** Object storage access key. | `write_nos_access_key` | No |
| `TPT_MAX_SESSIONS` | No | `4` | Integer maximum TPT sessions. Has no effect in the container; see [Teradata TPT selection](#teradata-tpt-selection). | `tpt_max_sessions` | No |
| `TPT_DELIMITER` | No | ASCII file separator (U+001C) | TPT field delimiter. Has no effect in the container. | `tpt_delimiter` | No |
| `TPT_TBUILD_EXECUTABLE` | No | `tbuild` | Path to `tbuild`. Read by the Worker process, not the container entrypoint, so it also applies to a Worker that you run from TOML. | None (environment only) | No |

Expand

Show lessSee more

Choose exactly one `write_nos` credential mode. `scai data worker setup` forwards the location, function mapping, and authorization name, but not `WRITE_NOS_ACCESS_ID` or `WRITE_NOS_ACCESS_KEY`. To use that mode on SPCS, bind both from secrets yourself.

#### Teradata TPT selection

`tpt` in a workflow is a legacy alias for `regular`. The Worker, not the workflow, decides whether a Teradata bulk extract uses Teradata Parallel Transporter (TPT):

- It uses TPT when `use_tpt_for_bulk` is `true` (the default) **and** `tbuild` is found on `PATH` or at `TPT_TBUILD_EXECUTABLE`.
- Otherwise it extracts through `teradatasql`, and `tpt_max_sessions` and `tpt_delimiter` have no effect.

The Worker container image doesn’t include `tbuild`, so **TPT never runs on SPCS** and SPCS Workers always extract through `teradatasql`. To use TPT, run the Worker from TOML on a host with Teradata Tools and Utilities installed. For a server-side export on SPCS, use `write_nos`.

### Worker container: `cloud_direct`

These variables configure the `[connections.target.s3]`, `[connections.target.gcs]`, or `[connections.target.blob]` section that the `cloud_direct` strategy writes to. The container writes no target section unless `CLOUD_DIRECT_OBJECT_STORE` and a bucket or container name are both set. The following table lists each variable:

| Variable | Required | Default | Description | TOML key | Set by `scai` |
| --- | --- | --- | --- | --- | --- |
| `CLOUD_DIRECT_OBJECT_STORE` | For `cloud_direct` | None | `s3`, `gcs`, or `blob`, in lowercase or uppercase. Any other value writes no target section. The `scai` object store value `azure` corresponds to `blob`. | Target section name | Yes, from the Worker configuration |
| `CLOUD_DIRECT_BUCKET_NAME` | For `s3` and `gcs` | None | Bucket name. For `blob`, used as the container name when `CLOUD_DIRECT_CONTAINER_NAME` is unset. | `bucket_name` | Yes, from the Worker configuration |
| `CLOUD_DIRECT_CONTAINER_NAME` | For `blob`, unless `CLOUD_DIRECT_BUCKET_NAME` is set | `CLOUD_DIRECT_BUCKET_NAME` | Azure container name. | `container_name` | Yes, from the Worker configuration |
| `CLOUD_DIRECT_PREFIX` | No | None | Path inside the bucket or container. Must match the external stage URL. | `prefix` | Yes, from the Worker configuration |
| `CLOUD_DIRECT_ACCOUNT_NAME` | For `blob`, unless you use a connection string | None | Azure storage account name. | `account_name` | Yes, from the Worker configuration |
| `CLOUD_DIRECT_USE_DEFAULT_CREDENTIAL` | No | None | `blob` only. `true` or `false`; any other value stops the container. `true` uses the Azure default credential chain. An SPCS service has no Azure managed identity, so on SPCS use a SAS token, account key, or connection string instead. | `use_default_credential` | Yes, from the Worker configuration |
| `CLOUD_DIRECT_SAS_TOKEN` | One `blob` credential | None | **Secret.** Azure SAS token. | `sas_token` | Yes. `scai` stores the value in a `GENERIC_STRING` secret and binds it. |
| `CLOUD_DIRECT_ACCOUNT_KEY` | One `blob` credential | None | **Secret.** Azure storage account key. | `account_key` | Yes. `scai` stores the value in a `GENERIC_STRING` secret and binds it. |
| `CLOUD_DIRECT_CONNECTION_STRING` | One `blob` credential | None | **Secret.** Azure connection string. When it’s set, the Worker uses it and ignores the account name. | `connection_string` | Yes. `scai` stores the value in a `GENERIC_STRING` secret and binds it. |

Expand

Show lessSee more

Important

For `s3` and `gcs` targets, the container writes only the bucket and prefix. Neither the container nor `scai` passes S3 or Google Cloud Storage credentials, so an SPCS Worker can’t authenticate to those targets through AIM DMV configuration. On SPCS, use an Azure Blob target. For S3 or Google Cloud Storage, run the Worker from TOML on a host that has credentials for the store. The Worker also needs egress to the storage account; see [Driver download hosts by platform](./manual-spcs-worker-setup#driver-download-hosts-by-platform).

### Metadata storage mode

AIM DMV keeps its orchestration metadata (the task queue, table metadata, and partition metadata) in Snowflake **Hybrid Tables** when your account supports them. At bootstrap it probes for Hybrid Table support and falls back to standard `TRANSIENT` tables when they’re unavailable, which is common on trial and lower-tier accounts.

Note

This is unrelated to L3 row validation. This setting only affects where orchestration metadata lives, never your target tables.

| Path | Metadata tables | Throughput |
| --- | --- | --- |
| Hybrid (default where supported) | `HYBRID TABLE` with hybrid indexes | Higher; scales well under concurrent task claiming |
| Standard (fallback) | `TRANSIENT` tables | Lower under contention |

Expand

Show lessSee more

Override the probe with `SNOWFLAKE_METADATA_STORAGE_MODE` when the result is ambiguous, for example when the account can’t create Hybrid Tables.

What to expect on the standard path:

- **Correctness holds.** Under heavy concurrent task claiming you may see more internal retries, but retries alone aren’t a sign of corruption.
- **Metadata `TRANSIENT` tables have no Time Travel.** Orchestration state can be rebuilt, but not recovered to a point in time. This doesn’t affect your migrated data.
- **Task-queue throughput is lower.** Each pull takes more round trips, and without hybrid secondary indexes the queue scan does more work. Latency degrades as the pending backlog grows.

Note

[Rate limiting](#rate-limiting) protects a busy source system, but it does nothing for metadata-queue contention. The two problems look similar from the outside and may both need attention.

## Rate limiting

Rate limiting caps how many extraction tasks run concurrently against a source system or any other shared resource. Use it when extraction concurrency is overwhelming the source, and prefer it to lowering `max_parallel_tasks` globally or stopping Workers: Workers stay up and matching tasks simply wait in `pending`.

Rules are rows in the **`RATE_LIMIT`** table in your migration metadata schema, not properties in the workflow file. Each rule limits how many **executing** tasks whose `SCOPE` matches a SQL `LIKE` pattern can run at once. A task scope looks like `Table[MY_DB.SALES.ORDERS]::Loading` or `Table[MY_DB.SALES.ORDERS]::Partition[3]::Extraction`.

| Column | Purpose |
| --- | --- |
| `SCOPE_PATTERN` | `LIKE` pattern matched against the task scope. `%` and `_` wildcards apply. |
| `WORKFLOW_ID` | Optional. Restricts the rule to one workflow. `NULL` matches any. |
| `AFFINITY` | Optional. Restricts the rule to tasks whose affinity equals this value exactly. Wildcards don’t apply, and a rule with a value never matches tasks without an affinity. `NULL` matches any. See [Affinity in rate-limit rules](#affinity-in-rate-limit-rules). |
| `TARGET_CONCURRENT_TASKS` | Target number of concurrently executing matching tasks. |
| `ENABLED` | Set to `FALSE` to turn a rule off without deleting it. |

Expand

Show lessSee more

Copy code

```
-- At most 5 concurrent loading tasks across any table:
INSERT INTO SNOWCONVERT_AI.DATA_MIGRATION.RATE_LIMIT (SCOPE_PATTERN, TARGET_CONCURRENT_TASKS)
  VALUES ('Table[%]::Loading', 5);

-- Cap partition loads for one workflow:
INSERT INTO SNOWCONVERT_AI.DATA_MIGRATION.RATE_LIMIT (SCOPE_PATTERN, WORKFLOW_ID, TARGET_CONCURRENT_TASKS)
  VALUES ('Table[%]::Partition[%]::Loading', 42, 2);

-- Pause every task against one source database:
INSERT INTO SNOWCONVERT_AI.DATA_MIGRATION.RATE_LIMIT (SCOPE_PATTERN, TARGET_CONCURRENT_TASKS)
  VALUES ('Table[MY_DB.%]::%', 0);
```

Remove a rule with `DELETE`, or disable it by setting `ENABLED = FALSE`. An empty `RATE_LIMIT` table means no limiting at all.

Warning

`TARGET_CONCURRENT_TASKS` is a **target, not a hard ceiling**: brief overshoot is possible when several Workers poll at once, so set the target below any hard limit you must respect. A target of `0` reliably pauses every matching scope.

## Cleaning up transient resources

AIM DMV temporarily stages data in Snowflake stages while a workflow runs. `cleanUpTransientResources` controls when those staged files are deleted. It’s a top-level property in both workflow types.

| Value | Behavior |
| --- | --- |
| `"on-success"` (default) | Delete the staged files only when the workflow finished with no failed tasks. |
| `"always"` | Delete the staged files whether or not the workflow had failures. |
| `"never"` | Keep everything, which is what you want while debugging a failing workflow. |

Expand

Show lessSee more

Underscores are accepted, so `on_success` works the same as `on-success`.

Copy code

```
cleanUpTransientResources: on-success
```

Target tables, metadata rows, and anything in the source database are **not** removed, regardless of the setting.

## Anti-locking and query modifiers

User-configured anti-locking hints are **off by default**. Unless you set `queryModifiers`, AIM DMV runs plain source queries. Modifiers apply to **source** queries only, never the Snowflake target.

Source platforms fall into two groups:

- **MVCC / snapshot engines** (Oracle, PostgreSQL, Amazon Redshift, and Snowflake itself): readers don’t block writers, so anti-locking hints aren’t needed.
- **Lock-based engines** (SQL Server and Azure Synapse): shared locks on reads can block or be blocked by production writers. Opt-in hints such as `WITH (NOLOCK)` avoid blocking but use read-uncommitted semantics (**dirty reads**). AIM DMV never auto-applies these hints.

**Teradata** is a special case: AIM DMV prepends `LOCKING ROW FOR ACCESS` on every Teradata source scan automatically. This is Teradata’s native, safe row-access pattern (not a dirty read) and cannot be disabled.

### Per-platform behavior

| Platform | Default behavior | How to customize |
| --- | --- | --- |
| **Teradata** | `LOCKING ROW FOR ACCESS` added automatically on every source scan | Not configurable |
| **SQL Server** | No automatic hint | Set `objectModifier: " WITH (NOLOCK)"` on `defaultTableConfiguration` or per table |
| **Oracle** | Automatic `PARALLEL` optimizer hint on large tables | Override with `selectModifier`, or set `selectModifier: "NONE"` to disable |
| **Amazon Redshift** | No automatic hint | Opt-in pass-through via `queryModifiers` |
| **PostgreSQL** | No automatic hint | Opt-in pass-through via `queryModifiers` |
| **IBM DB2** | No automatic hint | Opt-in pass-through via `queryModifiers` |

Expand

Show lessSee more

### Pros and cons

|  |  |
| --- | --- |
| **Pros** | Source reads no longer block on or wait for locks held by production writers, so migration isn’t stalled by long-running source transactions. On Oracle, the parallel hint can speed large-table scans. |
| **Cons** | `WITH (NOLOCK)` (and equivalent read-uncommitted hints) allow **dirty reads**: scans can see uncommitted rows that later roll back, so migration can copy data that never committed. Many DBAs disallow `NOLOCK`. Custom modifier strings are passed through verbatim, so an invalid hint can cause source query errors. |
| **Recommendation** | Leave hints off unless source locking is actually blocking your workflow. When you do enable them, prefer running against a quiesced or low-write window. |

Expand

Show lessSee more

### Workflow example

Set a default on `defaultTableConfiguration` and override per table when needed:

Copy code

```
defaultTableConfiguration:
  queryModifiers:
    objectModifier: " WITH (NOLOCK)"
tables:
  - source:
      databaseName: MY_DB
      schemaName: sales
      tableName: orders
    target:
      databaseName: TARGET_DB
      schemaName: sales
      tableName: orders
    queryModifiers:
      objectModifier: " WITH (NOLOCK)"
```

### Worker TOML example

You can also set query modifiers in Worker TOML under the source connection:

Copy code

```
[connections.source.sqlserver.query_modifiers]
object_modifier = " WITH (NOLOCK)"
select_modifier = ""
```

## Related content

- [Data migration](../data-migration-validation/data-migration)
- [Data migration advanced configuration](../data-migration-validation/data-migration-advanced-configuration)
- [The SNOWCONVERT\_AI database](../data-migration-validation/snowconvert-ai-database)
- [Data validation configuration reference](./data-validation-configuration-reference)
- [Data migration (CLI)](./data-migration)
