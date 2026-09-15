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
| `preflight` | `Boolean` |  | When `true`, caps each table to a single partition and writes to a transient `PREFLIGHT_<workflowId>` schema instead of the configured target. Defaults to `false`. See [Preflight: a bounded dry run](#preflight-bounded-dry-run). |
| `preflightKeepSchema` | `Boolean` |  | When `preflight` is `true`, skips cleanup so the transient schema survives for inspection. Defaults to `false`. |
| `cleanUpTransientResources` | `String` (`"never"`, `"on-success"`, `"always"`) |  | When to delete this workflow’s intermediate stage files. Defaults to `"on-success"`. See [Cleaning up transient resources](#cleaning-up-transient-resources). |

Expand

Show lessSee more

When `defaultTableConfiguration` is present, each object in `tables` is merged with those defaults: shared fields apply to every table unless the same field is set again on a specific table entry.

### Preflight: a bounded dry run

Setting `preflight: true` runs the migration as a bounded smoke test. Each table is capped at **one partition**, and the data lands in a transient `PREFLIGHT_<workflowId>` schema rather than your configured target schema. It exercises the whole pipeline (connectivity, extraction, staging, type mapping, and load) without touching production tables.

Copy code

```
preflight: true
preflightKeepSchema: false # true leaves PREFLIGHT_<workflowId> in place for inspection
```

Run it the same way you run any other workflow. AIM DMV drops the transient schema when the workflow ends unless `preflightKeepSchema` is `true`.

Three related things are easy to confuse:

| Mechanism | What it does |
| --- | --- |
| `preflight: true` | Bounded dry run: one partition per table, into a transient schema |
| `whereClauseCriteria` | A row-limited but otherwise real migration, into the actual target |
| `scai data doctor` | Infrastructure and configuration health check before anything starts. A failure blocks a local start |

Expand

Show lessSee more

Use preflight when you want to prove the pipeline works end to end. Use `whereClauseCriteria` when you want a real sample of rows in the real target.

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
| `externalVolume` | `String` | For `catalog` `SNOWFLAKE` | Snowflake external volume for Iceberg data and metadata. |
| `baseLocationPrefix` | `String` |  | Optional path prefix for `BASE_LOCATION`. |
| `catalogTableName` | `String` | For external `catalog` | Fully qualified name in the external catalog. |
| `catalogSync` | `String` |  | Optional catalog integration to sync Snowflake-managed metadata back to an external catalog. |
| `sourceDataStage` | `String` |  | Stage path starting with `@` pointing at existing Parquet files. |
| `migrationStrategy` | `String` |  | One of `catalog_link`, `convert_to_managed`, or `copy_files`. |

Expand

Show lessSee more

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

Automatic key selection applies to tables. Views don’t expose the catalog metadata needed for inference, so you must set `columnNamesToPartitionBy` explicitly when migrating a view.

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
| `externalStage` | `String` | See description | Required when `strategy` is `"unload"`, `"write_nos"`, `"dbms_cloud"`, `"cet_as"`, or `"cloud_direct"`. Snowflake external stage whose URL matches the bucket or container that receives the extracted files. |
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
| `"cloud_direct"` | Supported ODBC sources | Worker streams cursor results directly to S3 or Azure Blob and Snowflake loads from the external stage. |
| `"tpt"` | Teradata only | Worker runs TPT EXPORT via `tbuild`. `externalStage` is not required. |

Expand

Show lessSee more

See [Extraction strategies](#extraction-strategies) for YAML examples and platform prerequisites.

### SynchronizationStrategy model

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `strategy` | `String` (`"none"`, `"checksum"`, `"watermark"`) |  | Synchronization method. `"none"` (default) re-extracts fully on every run. |
| `checksumExpression` | `String` |  | `checksum` only. Custom SQL aggregate expression that returns a single value per partition (for example a row-version column or `MAX(last_modified)`). Only partitions whose value changed since the last run are cleared and re-extracted. When omitted, the default per-column hash is used. May reference pseudo-columns or system columns (for example `MAX(ORA_ROWSCN)` on Oracle). |
| `watermarkColumn` | `String` | `watermark` only | Monotonically increasing column name. May be a **pseudo-column or system column** not present in the migrated schema (for example Oracle `ORA_ROWSCN`). AIM DMV projects it into the extract for change detection but does not migrate it to the target. |
| `trackModifications` | `Boolean` |  | `watermark` only. If `true`, uses the primary key to deduplicate modified rows after `COPY INTO`. Requires `primaryKeyColumns`. |
| `trackDeletions` | `Boolean` |  | `watermark` only. If `true`, extracts a full primary-key snapshot of each source partition on every incremental run and deletes target rows absent from the snapshot before loading new rows. Requires `primaryKeyColumns`. Independent of `trackModifications`; the two can be combined. |

Expand

Show lessSee more

Both incremental strategies carry a cost and a coverage caveat:

- **`checksum`** recomputes a checksum on the source for **every partition on every run**, so the detection pass itself has a fixed cost proportional to table size. A custom `checksumExpression` over an indexed row-version or SCN column is usually much cheaper than the default per-column hash.
- **`watermark`** only reads the watermark column, but it can’t see rows that changed without the watermark advancing.

### Changes a checksum may not detect

The default partition checksum hashes a **normalized subset** of columns. Some types are skipped outright. A row whose only change falls into one of the categories below won’t be detected, so its partition won’t be re-extracted.

This applies to `synchronization.strategy: checksum` during migration and to [incremental validation](./data-validation-configuration-reference#incremental-validation) probes, which use the same hashing.

| Category | Where it applies | Effect |
| --- | --- | --- |
| Skipped legacy large objects | SQL Server `TEXT`, `NTEXT`, `IMAGE`; Oracle LOBs, `LONG`, `XMLTYPE`, `VECTOR` | The column is excluded from the checksum input, so changes confined to it are invisible |
| Spatial values as text | SQL Server, Redshift, and Oracle `SDO_GEOMETRY` | Compared as Well-Known Text with spacing normalized, so binary geometry detail is lost |
| A custom `checksumExpression` | Any platform | Only that expression drives detection — whether a change is detected depends entirely on what the expression evaluates |

Expand

Show lessSee more

If one of these applies to a column you need to track:

- Truncate the target table and run a full re-migration (`strategy: none`) to reconcile.
- Switch to `watermark` if the table has a reliable monotonic column.
- Use row-level validation to detect the difference after the fact.

### Affinity

Affinity routes workflow tasks to specific Workers. Use it when you run more than one Worker pool and need each workflow to land on the right pool, for example SPCS Workers for one source and on-premises Workers for another, or separate pools per team.

Set `affinity` on the workflow YAML and the same value (or a matching wildcard) on the Worker:

- Workflow: top-level `affinity` in the migration or validation YAML
- Worker TOML: `[application].affinity`
- SPCS service: `AGENT_AFFINITY` in the container environment

The string format is yours to define. Examples of valid values: `sql-server`, `DEV_SERVER`, `onprem-redshift`, `::blue::`.

Matching rules:

- A task without affinity is picked up by any Worker.
- A Worker without affinity picks up any task.
- A task with a given affinity is not picked up by a Worker with a different affinity.
- A Worker affinity may include `*` wildcards. For example, Worker affinity `team-*` matches workflow affinities `team-blue` and `team-red`.

Validation workflows use the same `affinity` field and the same matching rules as migration.

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

Each table can set **`extraction.strategy`** (or inherit from **`defaultTableConfiguration.extraction`**). Worker TOML holds connection and platform-specific options (UNLOAD credentials, WRITE\_NOS location, TPT tuning).

| Strategy | Platforms | When to use |
| --- | --- | --- |
| **`unload`** | Redshift only | **Recommended default** when S3 and a Snowflake external stage are available. Redshift writes Parquet to S3; Snowflake loads from the external stage. Use for all tables from the source. See [Migrating Data from Amazon Redshift](../data-migration-validation/migrate-redshift). |
| **`write_nos`** | Teradata only | **Recommended default** when Teradata NOS and a Snowflake external stage are available. Server-side export to S3, Azure Blob, or GCS. Use for all tables from the source. See [Migrating Data from Teradata](../data-migration-validation/migrate-teradata). |
| **`dbms_cloud`** | Oracle only | **Recommended default** when object storage and a Snowflake external stage are available. Server-side export via `DBMS_CLOUD.EXPORT_DATA`. Use for all tables from the source. See [Migrating Data from Oracle](../data-migration-validation/migrate-oracle). |
| **`cet_as`** | SQL Server and Azure Synapse | Source-side CETAS export to Azure Blob. See [Migrating Data from SQL Server](../data-migration-validation/migrate-sql-server#using-cetas-extraction) and [Migrating Data from Azure Synapse Analytics](../data-migration-validation/migrate-synapse#using-cetas-extraction). |
| **`cloud_direct`** | Supported ODBC sources | Worker streams query results directly to S3 or Azure Blob, skipping local disk and re-upload. |
| **`regular`** (default) | All | Worker pulls data over the source connection, then uploads to the Snowflake internal stage. Use when volume is genuinely small, or when server-side export prerequisites aren’t in place yet. |
| **`tpt`** | Teradata only | Worker-side bulk export via Teradata Parallel Transporter when WRITE\_NOS isn’t available. See [Migrating Data from Teradata](../data-migration-validation/migrate-teradata). |

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

**Cloud direct:**

Copy code

```
defaultTableConfiguration:
  extraction:
    strategy: cloud_direct
    externalStage: TARGET_DB.DATA_MIGRATION.CLOUD_LANDING
```

**Teradata tpt:**

Copy code

```
    extraction:
      strategy: tpt
```

## Worker configuration

The Worker configuration file uses [TOML](https://toml.io/) format. For cloud data migration, set `selected_task_source` to `"snowflake_stored_procedure"` and provide a matching **`[task_source.snowflake_stored_procedure]`** section.

| Section | Property | Type | Description |
| --- | --- | --- | --- |
| Top level | `selected_task_source` | `String` | Required. Use `"snowflake_stored_procedure"`. |
| `[task_source.snowflake_stored_procedure]` | `connection_name` | `String` | Snowflake connection name for task-queue stored procedures, or `"@SPCS_CONNECTION"` on SPCS. |
| `[application]` | `max_parallel_tasks` | `Integer` | Maximum parallel tasks (threads). |
| `[application]` | `task_fetch_interval` | `Integer` | Seconds between idle polls for new tasks. |
| `[application]` | `lease_refresh_interval` | `Integer` | Optional. Seconds between task lease renewals (default `120`). |
| `[application]` | `affinity` | `String` | Optional. Worker affinity for task routing. May include `*` wildcards. See [Affinity](#affinity). |
| `[application]` | `snowflake_database_for_metadata` | `String` | Optional. Database holding the migration and validation metadata procedures (default `SNOWCONVERT_AI`). Must match the Orchestrator’s `CUSTOM_SNOWFLAKE_DATABASE_FOR_METADATA`. |
| `[application]` | `snowflake_schema_for_data_migration_metadata` | `String` | Optional. Schema holding the migration task-queue procedures (default `DATA_MIGRATION`). Must match the Orchestrator’s `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_MIGRATION_METADATA`. |
| `[application]` | `snowflake_schema_for_data_validation_metadata` | `String` | Optional. Schema holding validation-specific objects such as the results stage and file format (default `DATA_VALIDATION`). Must match the Orchestrator’s `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_VALIDATION_METADATA`. |
| `[application]` | `local_results_directory` | `String` | Optional. Base directory for exported Parquet/CSV before upload. |
| `[connections.source.*]` | (per engine) | `Object` | Source database connection. Typically one active source section. |
| `[connections.source.*]` | `plugin_class` | `String` | Optional. Fully qualified class name of a custom extraction plugin that replaces the built-in extractor for this source connection. See [Preparing a custom extraction plugin](../data-migration-validation/data-migration-advanced-configuration#preparing-a-custom-extraction-plugin). |
| `[connections.source.sqlserver]` | `prefer_native_driver` | `Boolean` | Optional. Defaults to `true`. Set to `false` to force the ODBC fallback. |
| `[connections.source.sqlserver]` | `set_context_info` | `Boolean` | Optional. Defaults to `true`. Set to `false` to prevent the native driver from tagging the SQL Server session with `SET CONTEXT_INFO`. |
| `[connections.target.s3]` | (S3 storage settings) | `Object` | S3 target for `cloud_direct`. Requires `bucket_name`; optional fields include `profile_name`, `region_name`, and `prefix`. |
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

SPCS and container entrypoints may copy Orchestrator environment values into the Worker TOML when the container starts, which is why an SPCS Worker can appear to honor the environment variables directly.

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

### Environment variables

Most configuration lives in the workflow YAML and Worker TOML. These environment variables cover the settings that don’t:

**Orchestrator:**

| Variable | Default | Purpose |
| --- | --- | --- |
| `SNOWFLAKE_CONNECTION_NAME` |  | Required. Name of the Snowflake connection the Orchestrator uses, matching an entry in your connections file. |
| `CUSTOM_SNOWFLAKE_DATABASE_FOR_METADATA` | `SNOWCONVERT_AI` | Metadata database. See [Matching metadata locations](#matching-metadata-locations). |
| `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_MIGRATION_METADATA` | `DATA_MIGRATION` | Migration metadata schema. |
| `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_VALIDATION_METADATA` | `DATA_VALIDATION` | Validation metadata schema. |
| `CUSTOM_SNOWFLAKE_SCHEMA_FOR_COMMON_METADATA` | `COMMON` | Shared metadata schema. |
| `CUSTOM_SNOWFLAKE_SCHEMA_FOR_TEMP_METADATA` | `TEMP` | Schema for transient Snowpipe stage and pipe objects. |
| `SNOWFLAKE_METADATA_STORAGE_MODE` | Probed at startup | `HYBRID`, `STANDARD`, or `ICEBERG`. See [Metadata storage mode](#metadata-storage-mode). |
| `SNOWFLAKE_METADATA_EXTERNAL_VOLUME` | Unset | Required when the storage mode is `ICEBERG`. There’s no fallback if it’s missing. |
| `DM_IDLE_SHUTDOWN_MINUTES` | `60` | How long the Orchestrator stays up with no work before shutting itself down. |

Expand

Show lessSee more

**Worker:**

| Variable | Default | Purpose |
| --- | --- | --- |
| `SECRET_MANAGERS_*` |  | External secret resolution. See [Resolving credentials from an external secret manager](#external-secret-manager). |

Expand

Show lessSee more

Note

The storage mode is resolved once and cached for the life of the process. **Restart the Orchestrator** after changing `SNOWFLAKE_METADATA_STORAGE_MODE`.

On SPCS, Snowflake injects service identity variables such as `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_HOST`, and `SNOWFLAKE_WAREHOUSE` automatically. Don’t set them yourself.

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
| `AFFINITY` | Optional. Restricts the rule to one Worker affinity. `NULL` matches any. |
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
