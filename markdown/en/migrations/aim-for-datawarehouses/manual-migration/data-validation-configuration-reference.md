# Data validation configuration reference

This page documents the **validation workflow YAML** and shared **Worker TOML** settings for AIM DMV data validation. For platform-specific prerequisites, connectivity, and data type mappings, see the per-platform pages linked from [Data validation](../data-migration-validation/data-validation).

Tip

If you use the Snowflake AIM Agent for Data Warehouses instead of hand-editing these files, see [Data validation advanced configuration](../data-migration-validation/data-validation-advanced-configuration) for common scenarios and the prompts that generate and adjust this configuration for you.

For SnowConvert AI CLI commands that generate and submit validation workflows, see [Data validation](./data-validation).

## Validation workflow file overview

Validation is driven by a single YAML workflow file. Key sections:

| Section | Purpose |
| --- | --- |
| `source_platform` / `target_platform` | Source dialect and target (defaults to Snowflake) |
| `validation_configuration` | Global L1/L2/L3 toggles, thresholds, early stopping, accepted transformations |
| `comparison_configuration` | Numeric `tolerance` and optional type mapping file |
| `acceptedTransformations` | Global rules for expected source-to-target value pairs (optional) |
| `database_mappings` / `schema_mappings` | Source-to-target name maps |
| `tables` | Tables to validate, with optional per-table overrides |
| `views` | Same shape as `tables`, for view validation |
| `objects` | Same shape as `tables`, with optional `objectType`; omitting the type triggers runtime detection |

Expand

Show lessSee more

## Top-level object

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `source_platform` | `String` | Yes | Source dialect: `sqlserver`, `redshift`, `teradata`, `oracle`, `postgresql`, or `snowflake`. |
| `target_platform` | `String` |  | Defaults to `Snowflake`. |
| `target_database` | `String` |  | Default target database for tables that don’t specify one. |
| `affinity` | `String` |  | Optional affinity tag that routes this workflow’s tasks to matching Workers. Same matching rules as migration; see [Affinity](./data-migration-configuration-reference#affinity). |
| `validation_configuration` | `Object` |  | Global validation levels and options. |
| `comparison_configuration` | `Object` |  | Numeric tolerance and optional type mapping file. |
| `acceptedTransformations` | `Array` |  | Global accepted-transformation rules. Merged with per-table rules. |
| `database_mappings` | `Object` |  | Map of source database names to Snowflake database names. |
| `schema_mappings` | `Object` |  | Map of source schema names to Snowflake schema names. |
| `tables` | `Array` | See note | Table entries to validate (each tagged `object_type = "TABLE"`). |
| `views` | `Array` | See note | View entries using the same shape as `tables` (each tagged `object_type = "VIEW"`). |
| `objects` | `Array` | See note | Entries using the same shape as `tables`, plus an optional `objectType` (`TABLE` or `VIEW`). Omitting `objectType` resolves the type at runtime against the target Snowflake catalog. See [Objects with runtime type detection](#objects-with-runtime-type-detection). |
| `target_partition_size_rows` | `Integer` |  | Desired rows per partition. Mutually exclusive with `target_partition_size_mb`. |
| `target_partition_size_mb` | `Integer` |  | Desired MB per partition. Default is 200 MB when both are omitted. |
| `use_snowpipe_for_results` | `Boolean` |  | When `true` (default), L2/L3 results from Worker-based workflows are ingested via Snowpipe. Snowflake-to-Snowflake workflows ignore this flag and never use Snowpipe. |
| `queryModifiers` | `QueryModifiers` |  | Optional SQL hints for source queries. Default is unset (no hints). See [Anti-locking and query modifiers](#anti-locking-and-query-modifiers). |
| `intervalHandling` | `String` (`"interval"`, `"varchar"`) |  | How `INTERVAL` columns are compared. Defaults to `"interval"`, matching the target’s native interval type. See [INTERVAL data type handling](#interval-data-type-handling). |
| `validationCustomNormalizationRules` | `Array` |  | Preferred, granular normalization overrides by data type, column, or column pattern. See [Customizing normalization and metrics](#customizing-normalization-and-metrics). |
| `validationCustomNormalizations` | `Object` |  | Legacy, workflow-wide overrides for L2/L3 normalization SQL templates, keyed only by data type. See [Customizing normalization and metrics](#customizing-normalization-and-metrics). |
| `validationCustomMetrics` | `Object` |  | Workflow-wide overrides for L2 metric definitions. See [Customizing normalization and metrics](#customizing-normalization-and-metrics). |
| `validationCustomTypes` | `Object` |  | Workflow-wide overrides for L1 source data type name mapping. See [Customizing normalization and metrics](#customizing-normalization-and-metrics). |
| `validationCustomTypeRules` | `Array` |  | Per-column L1 type overrides, for columns deliberately migrated to a different type. See [Per-column L1 type overrides](#per-column-l1-type-overrides). |
| `defaultTableConfiguration` | `Object` |  | Shared defaults inherited by every table, view, and object entry. Per-entry properties override them, and a nested `synchronization` block is merged field by field. See [Incremental validation](#incremental-validation). |
| `synchronization` | `SynchronizationStrategy` |  | Enables incremental validation, which re-validates only changed partitions. Usually set once under `defaultTableConfiguration`. See [Incremental validation](#incremental-validation). |
| `cleanUpTransientResources` | `String` (`"never"`, `"on-success"`, `"always"`) |  | When to delete this workflow’s intermediate stage files under the validation `TASK_RESULTS` stage. Defaults to `"on-success"`. Underscores are accepted, so `on_success` also works. Set `"never"` to keep the files while debugging. See [Cleaning up transient resources](./data-migration-configuration-reference#cleaning-up-transient-resources). |

Expand

Show lessSee more

`tables`, `views`, and `objects` are each individually optional, but the workflow must define **at least one** entry across the three.

### Objects with runtime type detection

The top-level `objects` array is an alternative to `tables` and `views` that lets you list objects without committing to a type. Each entry uses the same shape as a `tables` or `views` entry, plus an optional `objectType`:

- When `objectType` is `TABLE` or `VIEW`, the entry behaves exactly like the corresponding `tables` or `views` entry.
- When `objectType` is omitted, AIM DMV resolves the type at runtime against the target Snowflake catalog. Only `TABLE` and `VIEW` are supported. If a detected type is something else (for example a materialized view) or the object doesn’t exist on the target, only that object’s check fails; other objects continue.

`tables`, `views`, and `objects` can be combined freely in the same workflow.

## Validation configuration

When `validation_configuration` is omitted, defaults are: schema validation and metrics validation **enabled**; row validation **disabled**; when L3 is enabled, Worker-based workflows fingerprint each partition with MD5 row hashes and drill into individual cells on mismatches (Snowflake-to-Snowflake L3 uses SQL set-difference instead; see [Validating Data from Snowflake](../data-migration-validation/validate-snowflake)); `max_failed_rows_number` defaults to **1000**; `early_stopping_for_cell_by_cell_comparison` defaults to **`true`**; `early_stopping_for_row_hashing` defaults to **`false`**.

| Property | Type | Description |
| --- | --- | --- |
| `schema_validation` | `Boolean` | Level 1: schema and column consistency checks. |
| `metrics_validation` | `Boolean` | Level 2: statistical metrics comparison. |
| `row_validation` | `Boolean` | Level 3: row fingerprinting and cell drill-down on mismatches. |
| `continue_on_failure` | `Boolean` | Whether to continue to the next validation level after a failure. |
| `max_failed_rows_number` | `Integer` | Cap on failed rows reported for L3 per partition and early-stop threshold (default **1000**). |
| `exclude_metrics` | `Boolean` | When `true`, skips overflow-prone L2 aggregates: `avg`, `sum`, and `stddev` (default `false`). |
| `apply_metric_column_modifier` | `Boolean` | When `true` (default), applies a platform overflow guard to aggregate metrics such as `sum` and `avg`. |
| `early_stopping_for_row_hashing` | `Boolean` | When `true`, stops remaining row-hash partitions once `max_failed_rows_number` mismatches are ingested (default `false`). |
| `early_stopping_for_cell_by_cell_comparison` | `Boolean` | When `true`, stops remaining cell drill-down partitions once `max_failed_rows_number` mismatches are ingested (default `true`). |
| `early_stop_check_interval_minutes` | `Integer` | Poll interval when either early-stop flag is enabled (default **5**). |
| `early_stop_check_interval_seconds` | `Integer` | Alternative poll interval in seconds. Mutually exclusive with `early_stop_check_interval_minutes`. |
| `text_comparison_mode` | `String` (`"logical"`, `"raw"`) | Teradata only. `"logical"` (default) normalizes text before comparing; `"raw"` compares source and target text byte-exact. |
| `acceptedTransformations` | `Array` | Rules merged with workflow-root and per-table rules. |

Expand

Show lessSee more

### Validation levels and result codes

**Schema validation (L1)** compares table name, column names, ordinal position, data types, character length, numeric precision and scale, nullability, and row count. Results use `SUCCESS`, `WARNING` (treated as a pass), or `FAILURE`.

**Metrics validation (L2)** compares row count, min, max, sum, average, null count, distinct count, standard deviation, and variance (metrics vary by column type). Numeric comparisons honor `comparison_configuration.tolerance` (default `0.001`). Results use `SUCCESS`, `WARNING`, or `FAILURE`.

**Row validation (L3)** on Worker-based (non-Snowflake) workflows fingerprints each partition with MD5 row hashes, then drills into individual cells on mismatches. Snowflake-to-Snowflake L3 compares rows with SQL set-difference in the warehouse. Row-level `RESULT` values include:

| Result | Meaning |
| --- | --- |
| `MISMATCH` | The row matches on the index columns on both sides, but one or more compared values differ. |
| `POSSIBLE_MISMATCH` | A provisional `MISMATCH` recorded while the table has [accepted transformations](#accepted-transformations) configured. Reconciled before the workflow completes: rows matching an accepted rule are cleared, and the rest become `MISMATCH`. |
| `NOT_FOUND_TARGET` | The row exists on the **source** but has no matching row on the **target** (missing from the target). |
| `NOT_FOUND_SOURCE` | The row exists on the **target** but has no matching row on the **source** (extra row on the target). |
| `DUPLICATE_SOURCE` | The index-column key appears more than once on the **source** side. |
| `DUPLICATE_TARGET` | The index-column key appears more than once on the **target** side. |
| `DUPLICATE_BOTH_SIDES` | The index-column key is duplicated on **both** the source and the target. |

Expand

Show lessSee more

Task-level failures are recorded in `DATA_VALIDATION_ERROR`, distinct from row-level `MISMATCH` results.

## Comparison configuration

| Property | Type | Description |
| --- | --- | --- |
| `tolerance` | `Number` | Relative tolerance for L2 metric comparisons (default `0.001`, or 0.1%). |
| `type_mapping_file_path` | `String` | Optional path to a custom type mapping file. |

Expand

Show lessSee more

## Accepted transformations

Accepted transformations allowlist specific source-to-target value pairs so AIM DMV does not report them as L3 mismatches. See [Accepted transformations](../data-migration-validation/data-validation#accepted-transformations) for the end-to-end flow and `POSSIBLE_MISMATCH` lifecycle.

Rules can appear at three levels (unioned per table):

1. Workflow root (`acceptedTransformations`)
2. Global `validation_configuration.acceptedTransformations`
3. Per-table `acceptedTransformations` or nested `validation_configuration.acceptedTransformations`

Each rule object:

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `column` | `String` | One of `column` or `columnPattern` | Exact source column name (case-insensitive). |
| `columnPattern` | `String` | One of `column` or `columnPattern` | Regex tested against the source column name. |
| `sourceValue` | `String` or `null` | Yes | Expected source value. Use `null` to represent SQL NULL. |
| `targetValue` | `String` or `null` | Yes | Expected target value after migration. |

Expand

Show lessSee more

Example:

Copy code

```
validation_configuration:
  row_validation: true
acceptedTransformations:
  - column: status
    sourceValue: "ACTIVE"
    targetValue: "1"
  - columnPattern: "^flag_"
    sourceValue: null
    targetValue: "false"
tables:
  - fully_qualified_name: MYDB.MYSCHEMA.MYTABLE
    acceptedTransformations:
      - column: code
        sourceValue: "Y"
        targetValue: "YES"
```

## Per-table and per-view entry

### Property naming and aliases

Some per-entry properties accept more than one spelling. Use the documented camelCase name in new workflows; the other spellings are kept for compatibility with existing files.

| Concept | Documented name | Also accepted |
| --- | --- | --- |
| Source row filter | `sourceWhereClause` | `whereClause` (legacy), `source_where_clause`, `where_clause` |
| Target row filter | `targetWhereClause` | `target_where_clause` |
| L3 index columns (source) | `indexColumnList` | `index_column_list` |
| L3 index columns (target) | `targetIndexColumnList` | `target_index_column_list` |

Expand

Show lessSee more

Three rules apply:

- **Set both WHERE clauses or neither.** Filtering one side only means you’re comparing different row subsets on source and target, which almost always reports mismatches.
- **Don’t combine `sourceWhereClause` with the legacy `whereClause`** on the same entry. The workflow is rejected when it loads.
- **camelCase wins** if an entry supplies both camelCase and snake\_case spellings for the index column lists.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `fully_qualified_name` | `String` | Yes | Source object name (format depends on platform). |
| `use_column_selection_as_exclude_list` | `Boolean` |  | Default `false`. |
| `column_selection_list` | `String[]` |  | Columns to include or exclude (literals and/or Python regex). |
| `target_name` | `String` |  | Target object name override. |
| `target_database` | `String` |  | Per-table target database override. |
| `target_schema` | `String` |  | Per-table target schema override. |
| `sourceWhereClause` | `String` |  | Filter applied to **source** rows, in the source dialect. Pair it with `targetWhereClause`. See [Property naming and aliases](#property-naming-and-aliases) and [Filtering compared rows](#filtering-compared-rows). |
| `targetWhereClause` | `String` |  | Filter applied to **target** rows, in Snowflake SQL. Pair it with `sourceWhereClause`. |
| `indexColumnList` | `String[]` |  | Columns used to align rows on the source (required for L3). Can be omitted and inferred automatically. See [Automatic partition and index key selection](#automatic-partition-and-index-key-selection). |
| `targetIndexColumnList` | `String[]` |  | Columns used to align rows on the target. |
| `column_mappings` | `Object` |  | Map of source column name to target column name. |
| `is_case_sensitive` | `Boolean` |  | Case sensitivity for identifiers and column filtering (default `false`). |
| `object_type` | `String` |  | `TABLE` (default) or `VIEW`. Set to `VIEW` to validate a view from a flat `tables` list instead of the `views` array. |
| `column_names_to_partition_by` | `String[]` |  | Columns for range-based partitioning during L2/L3. Can be omitted and inferred automatically. See [Automatic partition and index key selection](#automatic-partition-and-index-key-selection). |
| `target_partition_size_rows` | `Integer` |  | Per-table rows per partition override. |
| `target_partition_size_mb` | `Integer` |  | Per-table MB per partition override. |
| `max_failed_rows_number` | `Integer` |  | Overrides the global L3 cap for this object. |
| `acceptedTransformations` | `Array` |  | Per-table accepted-transformation rules. |
| `validation_configuration` | `Object` |  | Nested overrides for this object only. |
| `queryModifiers` | `QueryModifiers` |  | Optional SQL hints for source queries on this object. Default is unset (no hints). See [Anti-locking and query modifiers](#anti-locking-and-query-modifiers). |
| `excludeMetrics` | `Boolean` |  | Per-table override for `exclude_metrics`. |
| `applyMetricColumnModifier` | `Boolean` |  | Per-table override for `apply_metric_column_modifier`. |
| `intervalHandling` | `String` (`"interval"`, `"varchar"`) |  | Per-table override of the workflow-level `intervalHandling` setting. See [INTERVAL data type handling](#interval-data-type-handling). |
| `validationCustomNormalizationRules` | `Array` |  | Per-table normalization overrides. Take precedence over workflow-level rules for matching columns. See [Customizing normalization and metrics](#customizing-normalization-and-metrics). |
| `synchronization` | `SynchronizationStrategy` |  | Per-table incremental validation strategy. Overrides `defaultTableConfiguration.synchronization` field by field. See [Incremental validation](#incremental-validation). |

Expand

Show lessSee more

### Filtering compared rows

`sourceWhereClause` and `targetWhereClause` limit which rows take part in validation. Each filter is stored per side and **AND-composed** with the partition range predicate when L2 and L3 run, so a filter never widens a partition’s scope. Source-side SQL is written in the source dialect, while target-side SQL goes through column mapping and identifier folding before it runs on Snowflake.

Copy code

```
tables:
  - fully_qualified_name: MYDB.dbo.ORDERS
    target_name: ORDERS
    sourceWhereClause: "STATUS = 'ACTIVE'"
    targetWhereClause: "STATUS = 'ACTIVE'"
    indexColumnList:
      - ORDER_ID
```

A `targetWhereClause` that filters out every row is **not** treated as an empty target table: partition sizing continues against the filtered count. A genuinely empty target behaves differently, running L1 if enabled and skipping L2 and L3 with an explanatory failure row.

When a table uses [incremental validation](#incremental-validation), neither filter is applied while detecting change. Change probes read partition boundaries only. The filters apply when L2 and L3 run on a partition that changed.

### Column filtering with regex patterns

Each entry in `column_selection_list` is matched against every column name:

- **Literal** — plain string (for example `LOAD_DATE`), case-insensitive unless `is_case_sensitive: true`
- **Regex** — entry wrapped in single quotes with `r"..."` inside (for example `'r".*_TS"'`)

| `use_column_selection_as_exclude_list` | Behavior |
| --- | --- |
| `false` (default) | **Include mode** — only matched columns are validated |
| `true` | **Exclude mode** — all columns except matched ones are validated |

Expand

Show lessSee more

## Partitioning

When `column_names_to_partition_by` is set, the Orchestrator splits the table into range-based partitions:

1. Compute target rows-per-partition from `target_partition_size_rows` or `target_partition_size_mb` (default 200 MB).
2. Apply internal caps for safe infrastructure bounds.
3. Derive partition count as `ceil(row_count / effective_rows_per_partition)`.

### Automatic partition and index key selection

When `column_names_to_partition_by` or `indexColumnList` is omitted for a table that needs metrics or row validation, AIM DMV infers keys automatically from source catalog metadata:

- **Partition key**: clustered, sort, or distribution key columns when available, otherwise a unique index, otherwise the first non-boolean schema column as a last resort.
- **Index key** (for L3 row alignment): the declared primary key, otherwise the first unique index as a fallback.

Inferred keys are cached per source table and reused by later workflows. A manually specified `column_names_to_partition_by` or `indexColumnList` always takes precedence. Views can’t be inferred; set these explicitly when validating a view, and prefer a partition key that matches the underlying tables plus a `sourceWhereClause` to limit the scan. See [Validating views](../data-migration-validation/data-validation-advanced-configuration#validating-views).

Each partition key must be a **real, physical column name**. Persisted computed columns (SQL Server) and virtual columns (Oracle) qualify. Bare SQL expressions, pseudo-columns (for example Oracle `ROWID`, `ROWNUM`, or `ORA_ROWSCN`), and hidden system columns are **not** valid: AIM DMV quotes partition key names as identifiers, so those values won’t resolve. To partition on a derived value, add a persisted or virtual computed column on the source and reference that column name.

Index keys deserve particular attention when you enable L3. They’re what lets AIM DMV pair a source row with its target row, so they need to identify rows uniquely: a non-unique index key produces `DUPLICATE_SOURCE` and `DUPLICATE_TARGET` results rather than useful comparisons. Set `targetIndexColumnList` as well whenever the target column names differ from the source, for example after a `columnNameMappings` rename during migration.

## Incremental validation

By default, every validation run compares every partition of every table. **Incremental validation** detects which partitions changed since the last run and re-validates only those, which cuts cost and runtime on scheduled re-validation of large tables.

Incremental validation uses the same `synchronization` block as [incremental sync](./data-migration-configuration-reference#synchronizationstrategy-model) in data migration, but it’s **read-only**: nothing is written to the target, and no rows are moved or reconciled.

### SynchronizationStrategy model

| Property | Type | Description |
| --- | --- | --- |
| `strategy` | `String` (`"none"`, `"watermark"`, `"checksum"`) | `none` (default) validates every partition on every run. `watermark` and `checksum` enable incremental validation. |
| `watermarkColumn` | `String` | Required when `strategy` is `watermark`. AIM DMV compares `MAX(column)` per partition against the stored baseline, so the column must be monotonically increasing. |
| `checksumExpression` | `String` | Optional when `strategy` is `checksum`. A SQL aggregate that replaces the default per-partition hash, for example `MAX(ORA_ROWSCN)`. Must not contain a semicolon. |

Expand

Show lessSee more

Note

`trackModifications` and `trackDeletions` are not supported for Data Validation.

### Prerequisites

- The table must be **partitioned**. Set `column_names_to_partition_by`, or let AIM DMV infer it. Change detection works per partition, so an unpartitioned table has nothing to skip.
- At least one **prior full validation** must have completed, to establish baseline metadata in `PARTITION_METADATA.SYNCHRONIZATION_DATA`. The first run with `synchronization` configured still validates everything.

### What happens on each run

| Run | Behavior |
| --- | --- |
| First run | Full pipeline: L1, partition discovery, then L2 and L3 at the levels you enabled. Baselines are stored per partition. |
| Later runs | L1 is skipped and its column metadata is reused. A change-detection task per partition compares the current probe against the baseline. Unchanged partitions skip L2 and L3; changed partitions are validated at the currently enabled levels. |

Expand

Show lessSee more

Unchanged partitions report **Not validated** rather than a pass. That’s expected on an incremental run, not a failure.

Warning

An incremental run needs the **same L1, L2, and L3 toggles** as the run that established the baseline. If you change which levels are enabled, run a full validation (`strategy: none`) once to re-establish baseline metadata before returning to incremental runs.

Change-detection probes read partition boundaries only. `sourceWhereClause` and `targetWhereClause` aren’t applied while detecting change; they’re applied when L2 and L3 run on a partition that was found to have changed.

Because change detection relies on the same hashing as migration checksums, review [Changes a checksum may not detect](./data-migration-configuration-reference#changes-a-checksum-may-not-detect) before using `strategy: checksum`. Columns excluded from the hash won’t trigger re-validation of their partition.

### Example

Copy code

```
source_platform: sqlserver
target_database: MY_DB
defaultTableConfiguration:
  column_names_to_partition_by:
    - ID
  synchronization:
    strategy: checksum
tables:
  # Inherits the checksum strategy and the partition column.
  - fully_qualified_name: MYDB.dbo.CUSTOMERS
  # Overrides both: partition on ORDER_ID, detect change by watermark.
  - fully_qualified_name: MYDB.dbo.ORDERS
    column_names_to_partition_by:
      - ORDER_ID
    synchronization:
      strategy: watermark
      watermarkColumn: UPDATED_AT
  # Opts out: always validate in full, despite the global default.
  - fully_qualified_name: MYDB.dbo.LOOKUP_CODES
    synchronization:
      strategy: none
```

## Anti-locking and query modifiers

Anti-locking hints are **off by default** and work the same way as in migration: they apply to source queries only and are set with `queryModifiers` at the workflow root or per table. See [Anti-locking and query modifiers](./data-migration-configuration-reference#anti-locking-and-query-modifiers) for per-platform behavior and configuration.

The validation-specific consideration: `WITH (NOLOCK)` and similar read-uncommitted hints allow dirty reads that can produce false `MISMATCH` results. The impact is usually stronger at row-level validation (byte-exact hashing) than at metrics validation (aggregates compared within tolerance). Enable these hints only when source locking is actually blocking your workflow, ideally against a low-write window.

## INTERVAL data type handling

`intervalHandling` controls how `INTERVAL` columns are compared, and should match the value used for the same table during migration. Neither setting is universally better: `"interval"` compares as a native Snowflake `INTERVAL` (on PostgreSQL, mixed year-month and day-time values were already folded into `INTERVAL DAY TO SECOND` during migration), and `"varchar"` compares as text when migration preserved the original interval text. See [INTERVAL columns and intervalHandling](../data-migration-validation/migrate-postgresql#interval-columns-and-intervalhandling) for the PostgreSQL tradeoff.

| Value | Behavior |
| --- | --- |
| `"interval"` (default) | Compare the column as a native Snowflake `INTERVAL` value against the normalized source interval text. |
| `"varchar"` | Compare the column as text, matching a table migrated with `intervalHandling: "varchar"`. |

Expand

Show lessSee more

Set `intervalHandling` at the workflow root or on a per-table entry. See [INTERVAL data type handling](./data-migration-configuration-reference#interval-data-type-handling) in the Data migration configuration reference for how values are extracted and cast during migration.

Note

Comparing an `INTERVAL` column with the wrong `intervalHandling` value (mismatched with how it was migrated) produces false `MISMATCH` results, because the two sides are normalized differently.

## Customizing normalization and metrics

AIM DMV ships built-in normalization and metric templates per platform and data type. The keys below override those defaults so benign formatting differences (for example float precision, or a platform-specific type such as Teradata `PERIOD`) don’t show up as L3 mismatches. Set these in the validation workflow file, not in Worker TOML.

### Custom normalization rules (`validationCustomNormalizationRules`)

`validationCustomNormalizationRules` is the preferred way to override normalization. Unlike the legacy `validationCustomNormalizations` key (still supported, see below), rules can target a specific **column** or **column name pattern**, not only a data type, and can be scoped to the workflow root or to an individual table.

Each rule:

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `dataType` | `String` | Exactly one of `dataType`, `column`, `columnPattern` | Applies the rule to every column of this data type. |
| `column` | `String` | Exactly one of `dataType`, `column`, `columnPattern` | Applies the rule to one exact column name. |
| `columnPattern` | `String` | Exactly one of `dataType`, `column`, `columnPattern` | Applies the rule to column names matching this regex. |
| `sourceExpression` | `String` | At least one of `sourceExpression`, `targetExpression` | SQL template in the **source** dialect. Use the `{{ col_name }}` placeholder for the column reference. |
| `targetExpression` | `String` | At least one of `sourceExpression`, `targetExpression` | SQL template in **Snowflake** SQL. Use the `{{ col_name }}` placeholder for the column reference. |

Expand

Show lessSee more

When more than one rule could match the same column, AIM DMV applies the most specific one, in this order: table-level `column` match, table-level `columnPattern` match, table-level `dataType` match, workflow-level `column` match, workflow-level `columnPattern` match, workflow-level `dataType` match, then the built-in template for that platform and type.

Copy code

```
validationCustomNormalizationRules:
  - dataType: FLOAT
    sourceExpression: "TRIM(CAST({{ col_name }} AS VARCHAR(100)))"
    targetExpression: "TRIM(TO_VARCHAR({{ col_name }}))"
  - column: AMT
    sourceExpression: "TRIM(CAST({{ col_name }} AS VARCHAR(50)))"
  - columnPattern: "^GEO_"
    sourceExpression: "ST_AsText({{ col_name }})"
    targetExpression: "TO_VARCHAR({{ col_name }})"
tables:
  - fully_qualified_name: MYDB.MYSCHEMA.MYTABLE
    validationCustomNormalizationRules:
      - column: LEGACY_FLAG
        sourceExpression: "TRIM(CAST({{ col_name }} AS VARCHAR(10)))"
        targetExpression: "TRIM(TO_VARCHAR({{ col_name }}))"
```

Use custom normalization rules when a benign, predictable formatting difference (not a real data problem) would otherwise show up as an L3 mismatch, and you want the fix scoped to one column, one naming pattern, or one table rather than every column of a data type.

### Custom normalization (`validationCustomNormalizations`, legacy)

Normalization is the SQL AIM DMV wraps around each column so source and target values compare in a canonical form (consistent date, number, or string formatting) for L2 metrics and L3 hashing. This key is global-only and keyed by data type; prefer [`validationCustomNormalizationRules`](#custom-normalization-rules) for new workflows, especially when you need per-column or per-table control. When both are present for the same column, the granular rule wins.

| Property | Type | Description |
| --- | --- | --- |
| `source` | `Array` | Overrides applied on the source platform side. |
| `target` | `Array` | Overrides applied on the Snowflake target side. |

Expand

Show lessSee more

Each array entry is a single-key map of **data type → SQL template**. Keys are data types (uppercased), not column names. Use the `"{{ col_name }}"` placeholder for the column reference.

An override for a data type **replaces** the built-in template for that type; other types are unchanged.

Copy code

```
validationCustomNormalizations:
  source:
    - BIGINT: "TRIM(TO_CHAR(\"{{ col_name }}\", '999990.000000000000000000'))"
    - DECIMAL: "TRIM(TO_CHAR(\"{{ col_name }}\", '999990.000000000000000000'))"
  target:
    - NUMBER: "TO_CHAR(\"{{ col_name }}\", 'FM999990.000000000000000000')"
```

### Custom metrics (`validationCustomMetrics`)

L2 metrics are chosen by column data type. A `DEFAULT` set applies to types without a specific entry.

| Property | Type | Description |
| --- | --- | --- |
| `source` | `Array` | Metric overrides on the source platform side. |
| `target` | `Array` | Metric overrides on the Snowflake target side. |

Expand

Show lessSee more

Each array entry:

| Field | Type | Description |
| --- | --- | --- |
| `datatype` | `String` | Source or target data type (uppercased). |
| `metrics` | `Array` | Metric definitions for that type. |
| `replace_all` | `Boolean` | When `true`, removes all built-in metrics for the type before applying the listed metrics (default `false`). |

Expand

Show lessSee more

Each metric definition:

| Field | Type | Description |
| --- | --- | --- |
| `name` | `String` | Metric name (for example `count`, `sum`, `min`, `max`, `stddev`). |
| `metric_query` | `String` | SQL aggregate using `"{{ col_name }}"`. A null or empty value **removes** that metric from the built-in set. |
| `metric_return_datatype` | `String` | Data type used to normalize the metric result. |
| `metric_column_modifier` | `String` | Optional overflow guard override for this metric. |

Expand

Show lessSee more

Control which metrics run with these related settings:

| Setting | Default | Purpose |
| --- | --- | --- |
| `metrics_validation` | `true` | Enable or disable L2 entirely (global or per table). |
| `exclude_metrics` / `excludeMetrics` | `false` | Skip overflow-prone aggregates: `avg`, `sum`, `stddev`. |
| `apply_metric_column_modifier` / `applyMetricColumnModifier` | `true` | Apply platform overflow guards to aggregate metrics. |
| `comparison_configuration.tolerance` | `0.001` | Relative threshold for **numeric** L2 metric comparison only. |

Expand

Show lessSee more

Example:

Copy code

```
validationCustomMetrics:
  source:
    - datatype: BIT
      replace_all: false
      metrics:
        - name: sum
          metric_query: "SUM(\"{{ col_name }}\")"
          metric_return_datatype: NUMBER
        - name: stddev_pop
          metric_query: "STDDEV_POP(\"{{ col_name }}\")"
          metric_return_datatype: FLOAT
  target: []
```

### L1 type mapping overrides (`validationCustomTypes`)

`validationCustomTypes` overrides how source data type names map for **L1 schema comparison**. This is distinct from normalization (L2/L3).

| Property | Type | Description |
| --- | --- | --- |
| `source` | `Array` | List of single-key maps, each from an original source type name to the normalized type name. |

Expand

Show lessSee more

Example:

Copy code

```
validationCustomTypes:
  source:
    - "PERIOD(DATE)": "VARCHAR(40)"
```

### Per-column L1 type overrides (`validationCustomTypeRules`)

Where `validationCustomTypes` remaps a type name everywhere it appears, `validationCustomTypeRules` overrides the **expected target type for one column**. Use it when a single column was deliberately migrated to a different type than the default mapping would produce.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `column` | `String` | Yes | Source column name. |
| `sourceType` | `String` | Yes | Type on the source. |
| `targetType` | `String` | Yes | Type expected on the target. |

Expand

Show lessSee more

Copy code

```
validationCustomTypeRules:
  - column: GEO_COL
    sourceType: GEOGRAPHY
    targetType: VARIANT
```

A rule affects only the L1 **`DATA_TYPE`** criterion. The other L1 criteria (`CHARACTER_MAXIMUM_LENGTH`, `NUMERIC_PRECISION`, and `NUMERIC_SCALE`) still report the genuine metadata difference, because a type rule doesn’t claim those match.

A type rule also doesn’t change how values compare. When the two sides hold the same information in different types, pair the rule with a [custom normalization rule](#custom-normalization-rules) so L3 sees equal values.

Note

L3 row validation requires schema validation. The workflow is rejected if you set `schema_validation: false` while relying on them.

Set these rules at the workflow root or on an individual table entry. Per-table rules win for matching columns.

## Worker configuration

Workers reuse the same TOML format as Data Migration. See [Data migration configuration reference](./data-migration-configuration-reference#worker-configuration) for the full property list, including custom extraction plugin setup, [external secret managers](./data-migration-configuration-reference#external-secret-manager), and [environment variables](./data-migration-configuration-reference#environment-variables).

Validation objects such as the results stage and file format live in the validation metadata schema. When you override its name, the Worker’s `[application].snowflake_schema_for_data_validation_metadata` key must match the Orchestrator’s `CUSTOM_SNOWFLAKE_SCHEMA_FOR_DATA_VALIDATION_METADATA`. See [Matching metadata locations between the Orchestrator and Workers](./data-migration-configuration-reference#matching-metadata-locations).

Workers that execute validation tasks must have the validation runtime available. The `[connections.source.*]` section matches the source platform documented on each [Validating Data from …](../data-migration-validation/data-validation) page.

## Observability

Validation metadata lives under `SNOWCONVERT_AI.DATA_VALIDATION` by default. Filter queries by `WORKFLOW_ID`. See [The SNOWCONVERT\_AI database](../data-migration-validation/snowconvert-ai-database) for tables, views, workflow management procedures, and sample queries.

## Related content

- [Data validation](../data-migration-validation/data-validation)
- [Data validation advanced configuration](../data-migration-validation/data-validation-advanced-configuration)
- [Data migration configuration reference](./data-migration-configuration-reference)
- [The SNOWCONVERT\_AI database](../data-migration-validation/snowconvert-ai-database)
- [Data validation (CLI)](./data-validation)
