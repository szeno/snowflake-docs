# Data validation

The Data Validation feature provides a fault-tolerant, scalable way to verify that data in Snowflake matches the data in the original source system. For most sources it runs on the same infrastructure used by Data Migration, so you can migrate and validate with the same Orchestrator and Workers. Snowflake-to-Snowflake validation is an exception: it runs in-warehouse on the Orchestrator and doesn’t need Workers.

AIM DMV data validation is designed for migration and copy scenarios where you need confidence that data is correct before cutting over. Supported source platforms are **SQL Server**, **Azure Synapse Analytics**, **Amazon Redshift**, **Teradata**, **Oracle**, **PostgreSQL**, and **Snowflake** (Snowflake-to-Snowflake).

For shared architecture, deployment options, prerequisites, and Worker tuning, see [Data Migration & Validation overview](./overview).

## Validation levels

AIM DMV performs comparisons at three increasingly detailed levels:

### Schema validation (L1)

Confirms that table structure is preserved: table name, column names, ordinal position, data types, character length, numeric precision and scale, nullability, and row count.

### Metrics validation (L2)

Compares aggregate statistics: row count, min, max, sum, average, null count, distinct count, standard deviation, and variance (metrics vary by column type).

### Row validation (L3)

Performs row-level comparison. When `row_validation` is enabled, most source platforms fingerprint each partition with MD5 row hashes, then drill into individual cells on mismatches. Snowflake-to-Snowflake validation compares rows with SQL set-difference inside Snowflake instead of MD5 hashing on Workers. See [Validating Data from Snowflake](./validate-snowflake).

Row validation is disabled by default and is typically applied only where needed because it’s the most resource-intensive level.

## Prerequisites

Before you use data validation, make sure the following are in place:

- **[Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/intro)**: Use the agent’s **`data-validation`** skill for guided validation. Workers that run validation tasks receive the validation runtime through the same install path.
- **Snowflake access**: A connection for the Orchestrator (and Workers, when you use a non-Snowflake source) using a role that can create and administer `SNOWCONVERT_AI` and its objects.
- **Source connectivity**: Platform-specific drivers on Workers for non-Snowflake sources. See the per-platform pages below. Snowflake-to-Snowflake validation uses the Orchestrator’s Snowflake connection only.
- **Target data available**: Tables to validate must already exist in Snowflake. Don’t alter migrated data between migration and validation.

## Supported source platforms

Each platform page covers prerequisites (including platform-specific UDF or driver requirements), connectivity, validation behavior, data type mappings, and suggestions:

- [Validating Data from Amazon Redshift](./validate-redshift)
- [Validating Data from SQL Server](./validate-sql-server)
- [Validating Data from Azure Synapse Analytics](./validate-synapse)
- [Validating Data from Teradata](./validate-teradata)
- [Validating Data from Oracle](./validate-oracle)
- [Validating Data from PostgreSQL](./validate-postgresql)
- [Validating Data from Snowflake](./validate-snowflake)

For workflow and Worker field definitions, see [Data validation configuration reference](../manual-migration/data-validation-configuration-reference).

## Usage

To validate migrated data, complete the following high-level steps:

1. Start the Orchestrator.
2. Start the Workers (skip this step for Snowflake-to-Snowflake validation).
3. Create a data validation workflow.
4. Monitor the validation workflow until completion.

If you’ve already set up an Orchestrator and Workers for migration, you can reuse them for validation from a non-Snowflake source.

Ask the Snowflake AIM Agent for Data Warehouses for validation:

Copy code

```
Run cloud data validation for my project
```

For SnowConvert AI CLI commands, see [Manual Migration with SnowConvert AI CLI: Data validation](../manual-migration/data-validation).

## Validation results

Workflow lifecycle stages: **Pending**, **Executing**, **Completed**.

Result codes vary by validation level:

| Level | Result codes | Notes |
| --- | --- | --- |
| **L1 schema** | `SUCCESS`, `WARNING`, `FAILURE` | `WARNING` is treated as a pass (for example source numeric precision lower than target). |
| **L2 metrics** | `SUCCESS`, `WARNING`, `FAILURE` | Numeric metrics honor `comparisonConfiguration.tolerance` (default `0.001`). |
| **L3 row/cell** | `MISMATCH`, `POSSIBLE_MISMATCH`, `NOT_FOUND_SOURCE`, `NOT_FOUND_TARGET`, `DUPLICATE_SOURCE`, `DUPLICATE_TARGET`, `DUPLICATE_BOTH_SIDES` | `MISMATCH` means values differ. `POSSIBLE_MISMATCH` is provisional pending [accepted-transformation](#accepted-transformations) reconcile. |

Expand

Show lessSee more

For the precise meaning of each L3 code (including which side a row is missing from or duplicated on), see [Validation levels and result codes](../manual-migration/data-validation-configuration-reference#validation-levels-and-result-codes) in the configuration reference.

Task-level failures appear in `DATA_VALIDATION_ERROR` (distinct from row-level `MISMATCH` results).

Monitor workflows in `SNOWCONVERT_AI.DATA_VALIDATION` or the `DATA_VALIDATION_DASHBOARD` Streamlit app. See [The SNOWCONVERT\_AI database](./snowconvert-ai-database) for views and sample queries filtered by `WORKFLOW_ID`.

### Cancel, pause, resume, or retry a workflow

Prefer asking the Snowflake AIM Agent for Data Warehouses in natural language (for example, “Pause my last validation workflow” or “Cancel the sales validation run”). You can also use the SnowConvert AI CLI (`scai data validate pause|resume|cancel`) or call the workflow management stored procedures directly.

Canceling a workflow fails active tasks with a cancellation message. You can also pause, resume, retry, or cancel a single source table inside a workflow.

See [Managing workflow lifecycle](./snowconvert-ai-database#workflow-management-procedures) in [The SNOWCONVERT\_AI database](./snowconvert-ai-database).

Copy code

```
CALL SNOWCONVERT_AI.DATA_MIGRATION.CANCEL_WORKFLOW(<workflow_id>);
```

### Re-validating what failed

When a validation workflow finishes with failures, you don’t have to re-run the whole thing. **Re-validation** creates a child workflow that repeats only the failed partitions and levels from a parent run.

**Prompt:**

Copy code

```
The sales validation run finished with failures. Re-validate just the parts that failed.
```

The CLI equivalent takes the parent workflow name:

Copy code

```
scai data validate revalidate <WORKFLOW_NAME>
```

The parent workflow must have **finished**. Re-validation scope depends on what failed: an L1 failure regenerates the full set of queries for that table, while an L2 or L3 failure re-runs only the affected partitions and reuses the parent’s partition metadata. The shared Orchestrator and Worker must still be running.

There’s no workflow configuration property that controls re-validation scope. It’s derived from the parent workflow’s results.

AIM DMV retries at three different layers, and it’s worth keeping them apart:

| Layer | Trigger | Scope |
| --- | --- | --- |
| Task retry | Automatic, inside a single run | An individual task that failed or whose lease expired, up to a fixed retry limit |
| `RETRY_WORKFLOW` | You call the procedure | Failed and abandoned tasks in an existing workflow |
| Re-validation | You run `revalidate` after the parent finishes | A new child workflow covering only the failed partitions and levels |

Expand

Show lessSee more

Re-validation is also distinct from [incremental validation](./data-validation-advanced-configuration#re-validating-only-what-changed): re-validation retries **failed** work from one run, while incremental validation skips **unchanged** partitions on later scheduled runs.

## Considerations and recommendations

For more scenarios (validating views, customizable normalization for row-hashing and cell comparison, partition and index keys, INTERVAL handling, and more) with example prompts, see [Data validation advanced configuration](./data-validation-advanced-configuration).

### Initial testing

Start with a small subset of tables, keep L3 disabled on the first run, use `sourceWhereClause` and `targetWhereClause` to limit rows on both sides, and use small partition sizes. Enable row validation only on tables where you need it.

### Early stopping

When L3 validation runs across many partitions, processing every partition can be expensive. **Early stopping** lets AIM DMV skip remaining L3 partition work once enough mismatches have been found, so you don’t keep scanning a table that already clearly fails validation.

During L3, the Orchestrator periodically checks how many mismatch rows have been ingested into the results tables. When the count reaches **`max_failed_rows_number`**, pending partition tasks for that stage are skipped.

Configure early stopping in **`validation_configuration`** (globally or per table):

| Option | Default | Purpose |
| --- | --- | --- |
| `max_failed_rows_number` | `1000` | Mismatch threshold that triggers early stop; also caps reported mismatches per partition |
| `early_stopping_for_row_hashing` | `false` | Stop remaining row-hash partitions once the threshold is reached |
| `early_stopping_for_cell_by_cell_comparison` | `true` | Stop remaining cell drill-down partitions once the threshold is reached |
| `early_stop_check_interval_minutes` | `5` (when early stopping is enabled) | How often the Orchestrator rechecks the mismatch count |
| `early_stop_check_interval_seconds` | unset | Alternative to minutes (mutually exclusive) |

Expand

Show lessSee more

Row-hash and cell drill-down early stopping are independent. Per-table values override global settings. See [Validation configuration](../manual-migration/data-validation-configuration-reference#validation-configuration) in the configuration reference.

### Numeric precision and scale

When source numeric precision or scale exceeds the Snowflake target, validation surfaces the difference at each level:

- **L1**: `WARNING` when the target is wider than the source (pass); `FAILURE` when the source is wider than the target.
- **L2**: aggregate metrics honor `tolerance` (default `0.001`).
- **L3**: values are compared using scale-aligned canonical text. Truncation that changes a stored value causes a `MISMATCH`.

Deploy converted DDL before migration so target types match your expectations. See [Numeric precision and scale](./data-migration#numeric-precision-and-scale) on the Data migration page.

### Query tagging

The Orchestrator and Worker set Snowflake [`QUERY_TAG`](/sql-reference/parameters#query-tag) on every query. Filter in `QUERY_HISTORY` with `TRY_PARSE_JSON(query_tag):DMVF_WORKFLOW_ID`.

### Normalization and metrics customization

Built-in normalization and L2 metric templates apply per platform and data type. Override them at the workflow root with `validationCustomNormalizations` and `validationCustomMetrics`. See [Customizing normalization and metrics](../manual-migration/data-validation-configuration-reference#customizing-normalization-and-metrics) in the configuration reference.

### Accepted transformations

Accepted transformations declare source-to-target value pairs that migration legitimately changes (encoding, NULL-to-empty-string coercion, status-code remapping, and similar). AIM DMV does not report matching diffs as mismatches. This is an advanced option used when you already know specific column diffs are expected.

Accepted transformations apply only when **L3 row validation is enabled**. Tables without rules write `MISMATCH` directly from row hashing. Tables with rules use a provisional **`POSSIBLE_MISMATCH`** path until cell drill-down and reconcile complete.

Add an `acceptedTransformations` array to the validation workflow file. Rules merge from the workflow root, global `validation_configuration`, and per-table entries.

For configuration examples, the full property reference, and how to query provisional results, see [Accepted transformations](../manual-migration/data-validation-configuration-reference#accepted-transformations) and [The SNOWCONVERT\_AI database](./snowconvert-ai-database#provisional-mismatches-accepted-transformations).

Warning

For accurate validation and to avoid false negatives, don’t alter the migrated data during the validation process.

## Related content

- [Data Migration & Validation overview](./overview)
- [Data validation configuration reference](../manual-migration/data-validation-configuration-reference)
- [Data validation advanced configuration](./data-validation-advanced-configuration)
- [Data migration](./data-migration)
- [The SNOWCONVERT\_AI database](./snowconvert-ai-database)
- [Glossary](./glossary)
- [Manual Migration with SnowConvert AI CLI: Data validation](../manual-migration/data-validation)
