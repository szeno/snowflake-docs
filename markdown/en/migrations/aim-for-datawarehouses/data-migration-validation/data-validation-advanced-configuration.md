# Data validation advanced configuration

Validation workflows have a full YAML and TOML configuration surface documented in [Data validation configuration reference](../manual-migration/data-validation-configuration-reference). Most projects don’t need to hand-edit that file: the Snowflake AIM Agent for Data Warehouses generates it for you and walks through the settings that matter for your source platform, then shows you the result before anything runs.

This page describes common situations where you’ll want to go beyond the defaults, the prompt that gets you there, and where to find the exact property if you want to review or edit it yourself.

Tip

After the agent generates a validation workflow, it always shows you the YAML and asks whether you want to change anything before running it. You can request any of the scenarios below at that point, or ask for them up front.

## Choosing how deep to validate

Validation runs at up to three levels: schema (L1), aggregate metrics (L2), and row-level fingerprinting with cell drill-down (L3). L3 is the most resource-intensive and is disabled by default.

**Prompt:**

Copy code

```
Run full row-level validation on the ORDERS and CUSTOMERS tables, but keep the rest at schema and metrics validation only
```

The agent sets `row_validation: true` for the tables you named (globally it stays off). See [Validation levels](./data-validation#validation-levels).

## Choosing an L3 extraction strategy

L3 needs a source-side signature extract before Snowflake can compare row hashes. The optional `validation_configuration.extraction` block uses the **same strategy names as data migration**. When the source has a native export, that export is the recommended L3 extract:

| Source | Recommended strategy |
| --- | --- |
| Amazon Redshift | **UNLOAD** (`unload`) |
| Teradata | **WRITE\_NOS** (`write_nos`) |
| Oracle | **DBMS\_CLOUD** (`dbms_cloud`) |
| SQL Server / Azure Synapse | **CETAS** (`cet_as`) |
| BigQuery | **EXPORT DATA** (`export_data`). See [Validating Data from Google BigQuery](./validate-bigquery). |
| PostgreSQL | **regular** (COPY, `use_copy = true`) |
| IBM DB2 | **`cloud_direct`** when an object store and external stage are available. Otherwise **`regular`**. |

Expand

Show lessSee more

When the native bucket isn’t available, SQL Server, Azure Synapse, Redshift, Oracle, Teradata, and PostgreSQL can use **`cloud_direct`** instead: the Worker writes the signature Parquet to S3, GCS, or Azure Blob behind an external stage. BigQuery doesn’t support `cloud_direct`. Use `regular` when no bucket is available. Azure SQL Database can’t use `cet_as`. Use `cloud_direct` or `regular` there.

**Prompt:**

Copy code

```
Use UNLOAD for L3 signature extraction on this Redshift validation workflow, with the same external stage as migration
```

The agent sets `validation_configuration.extraction.strategy` and `externalStage` (and Worker TOML fields if needed). See [L3 extraction](../manual-migration/data-validation-configuration-reference#l3-extraction) for the property shape, platform gating, and [object storage backends](../manual-migration/data-validation-configuration-reference#l3-extraction-object-storage). Snowflake stage grants and object-store IAM are on [Required privileges](./required-privileges#external-stage-and-storage-integration).

## Re-validating only what changed

Validating a large table again doesn’t have to compare every partition every time. **Incremental validation** detects which partitions changed since the last run and re-validates only those. It’s read-only: nothing is written to the target.

A run is one validation command that you invoke, and incremental validation is that command run again, not a loop inside AIM DMV. A run is incremental only when an earlier run of the table exists, so the first run with `synchronization` set still validates everything. To repeat runs on a timetable, see [Running validation on a schedule](#running-validation-on-a-schedule).

**Prompt:**

Copy code

```
Set up incremental validation for the ORDERS table using the UPDATED_AT column, so nightly runs only re-check partitions that changed
```

The agent sets `synchronization.strategy` to `watermark` or `checksum` under `defaultTableConfiguration` so every table inherits it.

Note

`trackModifications` and `trackDeletions` are not supported for Data Validation.

See [Incremental validation](../manual-migration/data-validation-configuration-reference#incremental-validation) for the property shape, prerequisites, and what “Not validated” means on unchanged partitions. Review [Changes a checksum may not detect](../manual-migration/data-migration-configuration-reference#changes-a-checksum-may-not-detect) before choosing `checksum`.

## Running validation on a schedule

To repeat a validation on a timetable, for example a nightly incremental validation, create a Snowflake task that inserts a new workflow and resumes the SPCS services. [Submitting a validation from a Snowflake task](#submitting-a-validation-from-a-snowflake-task) shows the task. AIM DMV doesn’t create the task or start the next run itself. Each insert is one new workflow. You can also run `scai data validate create-workflow` from a scheduler on a host. That command names the workflow with a timestamp and a unique suffix.

**Prompt:**

Copy code

```
Run the ORDERS validation again
```

The agent submits the same validation configuration again as a new run on the shared Orchestrator and Workers. It doesn’t schedule later runs. If the Orchestrator or a Worker isn’t running, the agent tells you which one and offers to start it. See [Incremental validation](../manual-migration/data-validation-configuration-reference#incremental-validation) for what a later run skips.

On SPCS, each externally scheduled run follows this sequence:

1. **Resume the services.** The Orchestrator and every Worker suspend themselves after `DM_IDLE_SHUTDOWN_MINUTES` without work, 60 minutes by default, so they’re usually suspended when the next run is due. Submitting a workflow doesn’t resume a suspended service: a workflow submitted while they’re suspended is created and stays `pending`. Resume the Orchestrator and every Worker service first, as described in [Resuming services before the next wave](./deploy-workers#resuming-services-before-the-next-wave). A Snowflake-to-Snowflake validation doesn’t use Workers, so resume only the Orchestrator.
2. **Run the workflow and wait for it.** Run `scai data validate create-workflow --watch`, which blocks until the run finishes. Without `--watch`, the command returns as soon as the workflow is submitted, so its exit code doesn’t reflect the run.
3. **Check the result.** With `--watch`, the command exits `0` when the run finishes with every table validated, and `1` when a table fails validation, a table isn’t validated, or the command can’t complete. Use `scai data validate status <WORKFLOW_NAME>` for a run’s progress and errors, and `scai data validate list` to find recent runs. See the [SCAI command reference](../manual-migration/SCAI_Command_Reference).
4. **Re-validate what failed.** To repeat only the failed partitions and levels of a finished run, use `scai data validate revalidate <WORKFLOW_NAME>`, which creates a child workflow. See [Re-validating what failed](./data-validation#re-validating-what-failed).
5. **Let idle shutdown stop the services.** After the run, each service suspends itself once it has been idle for its `DM_IDLE_SHUTDOWN_MINUTES`. See [Idle shutdown](./deploy-workers#idle-shutdown) and [Controlling cost on SPCS](./deploy-workers#controlling-cost-on-spcs).

`scai data validate start` doesn’t use the SPCS services. It runs the Orchestrator, and a Worker when the source needs one, as local processes for as long as the command runs and blocks until the run finishes, so a scheduler on a host that can reach the source can run it without resuming anything.

Don’t start the next run of the same tables until the previous run finishes. When a run starts, it skips each table that another validation workflow is initializing or running, as long as that workflow has sent a heartbeat within the last 15 minutes and both workflows have the same affinity or either has none. Each skipped table is reported as `Skipped '<table>': already being validated by workflow '<name>' (created <time>, affinity '<affinity>') to avoid duplicate data / race conditions.` A workflow that’s still `pending` doesn’t hold its tables. When every table is skipped, the run finishes with exit code `0` and the warning “The validation finished without validating any table: every configured table is already being validated by another active workflow. Re-run once that workflow finishes.” Treat that warning as a run that did nothing.

### Submitting a validation from a Snowflake task

A task you create can do the first two steps of the sequence above. It inserts a pending validation workflow, then resumes the Orchestrator and the Workers. You choose how the task runs: add a `SCHEDULE`, chain it after another task, or execute it yourself. AIM DMV doesn’t create this task.

The task below inserts one table. Put in the JSON only the tables that this run should validate, and build that JSON in the task when the list changes. The object is the workflow configuration. See [Validation configuration](../manual-migration/data-validation-configuration-reference#validation-configuration). When the list is too complex for the task body, a Python procedure can build it and the task can call that procedure.

Give every run its own workflow name. The example builds one from the current UTC time. `STATUS` is omitted, so the new row stays `pending` until the Orchestrator picks it up.

The `WORKFLOW` table is in the migration metadata schema, `SNOWCONVERT_AI.DATA_MIGRATION` by default. `TARGET_CLOUD_STAGE_NAME` is the validation metadata stage, `@SNOWCONVERT_AI.DATA_VALIDATION.TASK_RESULTS` by default. If you customized the metadata database or either schema, use those names in the task.

The `ALTER SERVICE` statements resume the default services in the migration metadata schema. The Orchestrator service is `DATA_MIGRATION_SERVICE`. The Worker service is `DATA_EXCHANGE_WORKER_SERVICE`. Resume every Worker the validation uses. A Worker created with `scai data worker setup --service-name` has that name, not the default. A Snowflake-to-Snowflake validation doesn’t use a Worker, so resume only the Orchestrator. Set `AFFINITY` to the Worker’s affinity when that Worker won’t claim a workflow that has none.

Copy code

```
CREATE OR REPLACE TASK SNOWCONVERT_AI.DATA_MIGRATION.START_DATA_VALIDATION
  WAREHOUSE = <WAREHOUSE>
  COMMENT = 'Insert a pending data-validation workflow and resume the orchestrator and data-exchange services.'
AS
BEGIN
  INSERT INTO SNOWCONVERT_AI.DATA_MIGRATION.WORKFLOW (
      NAME,
      WORKFLOW_TYPE,
      SOURCE_PLATFORM,
      TARGET_CLOUD_TYPE,
      TARGET_CLOUD_STAGE_NAME,
      TARGET_CLOUD_URL,
      SCHEMA_VERSION,
      INITIATOR_ID,
      CONFIGURATION,
      AFFINITY
  )
  SELECT
      'VALIDATION_' || TO_VARCHAR(CONVERT_TIMEZONE('UTC', CURRENT_TIMESTAMP()), 'YYYYMMDDHH24MISS'),
      'data-validation',
      '<SOURCE_PLATFORM>',
      'snowflake:stage',
      '@SNOWCONVERT_AI.DATA_VALIDATION.TASK_RESULTS',
      '',
      '1.0',
      '',
      PARSE_JSON($$
        {
          "sourcePlatform": "<SOURCE_PLATFORM>",
          "targetPlatform": "Snowflake",
          "validationConfiguration": {
            "schemaValidation": true,
            "metricsValidation": true,
            "rowValidation": false
          },
          "tables": [
            {
              "fullyQualifiedName": "<FULLY_QUALIFIED_NAME>"
            }
          ]
        }
      $$),
      NULL;

  ALTER SERVICE IF EXISTS SNOWCONVERT_AI.DATA_MIGRATION.DATA_MIGRATION_SERVICE RESUME;
  ALTER SERVICE IF EXISTS SNOWCONVERT_AI.DATA_MIGRATION.DATA_EXCHANGE_WORKER_SERVICE RESUME;
END;
```

The task returns after the insert and the resume. It doesn’t wait for the validation to finish. Check the run with `scai data validate status` and `scai data validate list`.

After the first run, confirm that the services suspend once the workflow is done. Each service suspends itself after `DM_IDLE_SHUTDOWN_MINUTES` without work, 60 minutes by default. See [Idle shutdown](./deploy-workers#idle-shutdown) and [Controlling cost on SPCS](./deploy-workers#controlling-cost-on-spcs).

## Stopping L3 early when a table is clearly failing

When row-level validation runs across many partitions, finishing every partition can be expensive after a table has already failed. **Early stopping** skips remaining partition work once enough mismatches have been ingested.

**Prompt:**

Copy code

```
Enable early stopping for row hashing on the ORDERS table, and stop after 200 mismatches
```

The agent sets `early_stopping_for_row_hashing: true` and lowers `max_failed_rows_number` on the tables you name (or globally, if you ask for that). See [Validation configuration](../manual-migration/data-validation-configuration-reference#validation-configuration) for all early-stopping options and defaults.

## Declaring expected source-to-target differences (accepted transformations)

Some value changes during migration are intentional (encoding normalization, NULL-to-empty-string coercion, status-code remapping) and shouldn’t be reported as failures. **Accepted transformations** allowlist specific source-to-target value pairs so AIM DMV does not treat matching diffs as L3 mismatches.

Accepted transformations apply only when **L3 row validation is enabled**:

- Tables **without** rules write `MISMATCH` directly from row hashing.
- Tables **with** rules use a provisional **`POSSIBLE_MISMATCH`** path until cell drill-down and reconcile complete. Rows that match an accepted rule are cleared; the rest become `MISMATCH`.

Rules can appear at the workflow root, under global `validation_configuration`, or on an individual table. Matching scopes are unioned. Each rule names either an exact `column` or a `columnPattern` regex, plus the expected `sourceValue` and `targetValue` (use `null` for SQL NULL).

**Prompt:**

Copy code

```
We intentionally remap STATUS = 'ACTIVE' on the source to STATUS = '1' on the target. Don't flag that as a mismatch.
```

The agent adds an `acceptedTransformations` rule at the appropriate scope.

### Caveat: `POSSIBLE_MISMATCH` after the workflow finishes

`POSSIBLE_MISMATCH` is temporary. Reconcile runs after cell drill-down and should leave either:

- no row (the diff matched an accepted transformation), or
- `MISMATCH` (a real problem that did not match any rule).

On a **completed** workflow, `ROW_VALIDATION_RESULTS` should not still contain `POSSIBLE_MISMATCH` for that table. Leftover provisional rows usually mean reconcile did not finish (for example the workflow failed or was canceled before the reconcile task ran). Treat them as incomplete validation, not as accepted diffs. Re-run validation for the affected tables, or investigate task status in the workflow, before deciding the table passed.

For the property shape and examples, see [Accepted transformations](./data-validation#accepted-transformations) and [Accepted transformations (configuration reference)](../manual-migration/data-validation-configuration-reference#accepted-transformations). To query provisional rows while a workflow is still running, see [The SNOWCONVERT\_AI database](./snowconvert-ai-database#provisional-mismatches-accepted-transformations).

## Customizing normalization for row-hashing and cell comparison

Validation wraps each column in a normalization expression before hashing (L3 row fingerprinting) and comparing cell values, so that benign formatting differences (trailing zeros, timezone representation, and similar) don’t show up as mismatches. Built-in templates cover common data types per platform, but you can override them when a specific column, naming pattern, or table needs different handling.

**Prompt:**

Copy code

```
The AMOUNT column keeps showing mismatches that look like formatting differences, not real data problems. Can we normalize it before comparing?
```

The agent proposes a normalization expression for that column (or column pattern, or data type, depending on scope) and adds a `validationCustomNormalizationRules` entry, either at the workflow root or scoped to just the affected table. See [Custom normalization rules](../manual-migration/data-validation-configuration-reference#custom-normalization-rules) for the property shape, matching precedence, and more examples (including geometry and legacy platform-specific types).

Note

An older, data-type-only normalization override (`validationCustomNormalizations`) still works, but new column- or pattern-scoped customizations should use `validationCustomNormalizationRules`. See [Custom normalization](../manual-migration/data-validation-configuration-reference#custom-normalization-validationcustomnormalizations-legacy) for the legacy form.

## Overriding partition and index keys

If you already know the columns to use, set them explicitly rather than relying on inference. Views can’t be inferred — see [Validating views](#validating-views).

**Prompt:**

Copy code

```
Partition LEGACY_ORDERS by ORDER_DATE, and align rows on ORDER_UUID
```

See [Automatic partition and index key selection](../manual-migration/data-validation-configuration-reference#automatic-partition-and-index-key-selection) for inference rules and the constraint that keys must be real physical column names.

## Validating views

Views go through the same L1, L2, and L3 pipeline as tables, but they don’t expose the catalog metadata AIM DMV uses to infer partition and index keys. When you validate a view, set those keys yourself and use a row filter so L2/L3 don’t scan an unbounded result.

**Choose a partition key that matches the underlying tables.** Prefer a column that would also be a good partition key on the base tables the view reads (for example the date or ID column that drives filters and joins in the view definition), not an arbitrary projected column. That keeps partition ranges meaningful and avoids uneven or ineffective chunking. For L3, also set an `indexColumnList` that uniquely identifies rows in the view result.

**Filter with a WHERE clause.** Views often expand to large joins. Use `sourceWhereClause` and `targetWhereClause` to limit the rows under validation, for example to a recent date range or an active subset. Set both sides: filtering only one compares different row subsets and reports mismatches that aren’t real.

**Prompt:**

Copy code

```
Validate the ORDERS_SUMMARY view. Partition by ORDER_DATE (same key as the ORDERS table the view is built on), align rows on ORDER_ID, and only validate the last 30 days
```

The agent sets `column_names_to_partition_by`, `indexColumnList`, `sourceWhereClause`, and `targetWhereClause` on the view entry. See [Automatic partition and index key selection](../manual-migration/data-validation-configuration-reference#automatic-partition-and-index-key-selection) and [Per-table and per-view entry](../manual-migration/data-validation-configuration-reference#per-table-and-per-view-entry).

The same rules apply to source materialized views, which AIM DMV classifies as views. Put a view under `views`, or under `objects` with `objectType: VIEW` or no `objectType`. An `objectType: VIEW` key inside `tables` is ignored, and the entry is validated as a table. See [Source and target object types](../manual-migration/data-validation-configuration-reference#source-and-target-object-types) for every source and target pairing and for which catalog kinds count as tables and views.

## Validating a view against a dynamic table

A source view is sometimes rebuilt in Snowflake as a [dynamic table](/user-guide/dynamic-tables/overview) instead of a view. Snowflake reports a dynamic table as a table, so AIM DMV validates the pair as a source view against a target table:

- L1 records the object type as `WARNING`, with the comment “Source view materialized as a Snowflake table.” A warning doesn’t fail L1, so L2 and L3 run when they’re enabled.
- The source is still a view, so AIM DMV can’t infer its keys. Set `columnNamesToPartitionBy` and `indexColumnList` on the entry, and `targetIndexColumnList` when the dynamic table’s column names differ from the view’s.
- A dynamic table can lag its base tables by up to its [target lag](/user-guide/dynamic-tables/target-lag) (`TARGET_LAG`). Validate only after the dynamic table has refreshed past the latest change to its base tables. Otherwise L2 and L3 compare the current view with an older state of the dynamic table and report mismatches that aren’t real.

**Prompt:**

Copy code

```
Validate the dbo.ORDER_TOTALS view against the ORDER_TOTALS dynamic table in Snowflake. Align rows on ORDER_ID and partition by ORDER_ID
```

The agent adds the view under `views` with `indexColumnList`, `targetIndexColumnList`, and `columnNamesToPartitionBy`, and sets `targetName` when the dynamic table’s name differs from the view’s. Before you start the run, check that the dynamic table’s latest refresh succeeded after your last load into its base tables, for example with [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history), or refresh it manually with [ALTER DYNAMIC TABLE … REFRESH](/sql-reference/sql/alter-dynamic-table).

AIM DMV doesn’t migrate data into a dynamic table. Migrate the data into the dynamic table’s base tables, let Snowflake refresh the dynamic table, and then validate the source view against it. See [Dynamic tables](../manual-migration/data-validation-configuration-reference#dynamic-tables-as-validation-targets) for the validation behavior and [Views and dynamic tables in migration](../manual-migration/data-migration-configuration-reference#views-and-dynamic-tables-in-migration) for the migration limitation.

## Validating INTERVAL columns

Use the same `intervalHandling` value as the matching migration workflow: `"interval"` to compare as a native Snowflake `INTERVAL`, or `"varchar"` to compare as text. Neither option is universally better; the tradeoff is the same as during migration. On platforms such as PostgreSQL, `"interval"` means mixed year-month and day-time values were folded into `INTERVAL DAY TO SECOND` (losing calendar-accurate year-month precision), while `"varchar"` preserves the original interval text.

**Prompt:**

Copy code

```
The EVENTS table was migrated with intervalHandling set to varchar. Use the same setting for validation.
```

The agent sets `intervalHandling` on that table’s validation entry to match migration. A mismatch between migration and validation produces false mismatches, because the two sides are normalized differently. See [INTERVAL data type handling](../manual-migration/data-validation-configuration-reference#interval-data-type-handling).

## Reducing lock contention on the source

If validation reads are blocked by production writers, you can opt in to anti-locking query hints. This trades consistency guarantees (dirty reads) for reduced blocking, so use it only when locking is actually a problem.

On MVCC engines (Oracle, PostgreSQL, Redshift), readers don’t block writers and hints usually aren’t needed. On lock-based engines (SQL Server), `WITH (NOLOCK)` avoids blocking but allows dirty reads that can produce false `MISMATCH` results. The impact is usually **stronger at L3** (byte-exact row hashing) than at **L2** (aggregate metrics within tolerance). Teradata gets `LOCKING ROW FOR ACCESS` automatically (safe, not a dirty read). IBM DB2 gets no automatic hint.

**Prompt:**

Copy code

```
Source reads are getting blocked during validation. Can we reduce locking?
```

The agent explains the platform-specific tradeoff and, if you confirm, sets the appropriate `queryModifiers` (for example `WITH (NOLOCK)` on SQL Server). See [Anti-locking and query modifiers](../manual-migration/data-validation-configuration-reference#anti-locking-and-query-modifiers) for per-platform defaults and the pros and cons.

## Adjusting numeric tolerance for metrics

L2 aggregate comparisons (sum, average, and similar) use a relative tolerance by default, since floating-point and precision differences between platforms are expected.

**Prompt:**

Copy code

```
Our source and target use different floating-point precisions, so metric comparisons are noisy. Can we loosen the tolerance?
```

The agent sets `comparisonConfiguration.tolerance` to a value you agree on. See [Comparison configuration](../manual-migration/data-validation-configuration-reference#comparison-configuration).

## Overriding L2 metrics or L1 type mapping

**Prompt:**

Copy code

```
Add a stddev_pop metric for the BIT columns, and treat the Teradata PERIOD(DATE) type as VARCHAR(40) for schema comparison
```

The agent sets `validationCustomMetrics` and `validationCustomTypes` respectively. See [Custom metrics](../manual-migration/data-validation-configuration-reference#custom-metrics-validationcustommetrics) and [L1 type mapping overrides](../manual-migration/data-validation-configuration-reference#l1-type-mapping-overrides-validationcustomtypes).

To skip one L2 aggregate on a single column (for example length-based `avg` on a VARCHAR primary key) without excluding that column from L1 or L3, ask the agent to use a column-scoped `validationCustomMetrics` entry. See [Column-scoped custom metrics](../manual-migration/data-validation-configuration-reference#column-scoped-custom-metrics).

When only one column needs a different expected type, for example because you deliberately migrated a `GEOGRAPHY` column to `VARIANT`, ask for a per-column rule instead and the agent sets `validationCustomTypeRules`. See [Per-column L1 type overrides](../manual-migration/data-validation-configuration-reference#per-column-l1-type-overrides).

Note

Validation type overrides are separate from migration’s `columnTypeMappings`. If you remapped types during migration, that setting doesn’t carry over: tell the agent what the target types actually are so validation expects them.

## Filtering rows or columns

**Prompt:**

Copy code

```
Only validate active customers, and skip the internal AUDIT_* columns
```

The agent sets `sourceWhereClause` and `targetWhereClause` to filter rows on both sides, and `column_selection_list` (with `use_column_selection_as_exclude_list` for the audit columns) to filter columns. See [Filtering compared rows](../manual-migration/data-validation-configuration-reference#filtering-compared-rows) and [Column filtering with regex patterns](../manual-migration/data-validation-configuration-reference#column-filtering-with-regex-patterns).

## Related content

- [Data validation](./data-validation)
- [Data validation configuration reference](../manual-migration/data-validation-configuration-reference)
- [Data migration advanced configuration](./data-migration-advanced-configuration)
- [The SNOWCONVERT\_AI database](./snowconvert-ai-database)
- [Glossary](./glossary)
