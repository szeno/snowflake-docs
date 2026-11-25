# The SNOWCONVERT\_AI database

AIM DMV stores workflow definitions, task queue state, migration progress, and validation results in a Snowflake metadata database. By default this database is named **`SNOWCONVERT_AI`**. The Orchestrator creates and updates it on startup.

Use this database to monitor migration and validation workflows, inspect errors and warnings, and manage workflow lifecycle (pause, resume, cancel, retry). You can rename the database and schemas through Orchestrator configuration if your account requires a different name.

## Schemas

| Schema | Purpose |
| --- | --- |
| `DATA_MIGRATION` | Workflows, task queue, migration table and partition metadata, workflow management procedures, and migration monitoring views. Validation workflows also register here; both workflow types share `WORKFLOW` and `TASK_QUEUE`. |
| `DATA_VALIDATION` | Validation table and partition metadata, L1/L2/L3 result tables, and validation monitoring views. |
| `COMMON` | Internal schema migration tracking (not customer-facing workflow data). |
| `TEMP` | Transient Snowpipe stage and pipe objects used during migration. |

Expand

Show lessSee more

## Tables and views

When querying any object below, filter by **`WORKFLOW_ID`** to scope results to a single workflow. Other useful filter columns include `TABLE_METADATA_ID`, `PARTITION_NUMBER`, `RESULT`, and `STATUS`.

### DATA\_MIGRATION schema

#### Tables

| Object | Purpose |
| --- | --- |
| `WORKFLOW` | One row per migration or validation workflow (configuration, status, affinity, lifecycle timestamps). |
| `TASK_QUEUE` | Pending and in-progress tasks for the Orchestrator and Workers. |
| `TABLE_METADATA` | Per-workflow registry of source tables being migrated. |
| `PARTITION_METADATA` | Per-partition migration progress (boundaries, row counts, status). |

Expand

Show lessSee more

#### Views

| Object | Purpose |
| --- | --- |
| `TABLE_PROGRESS` | Per-table partition rollup (extraction, loading, completed, and failed counts). |
| `TABLE_PROGRESS_WITH_EXAMPLE_ERROR` | `TABLE_PROGRESS` plus a sample error or warning message per table. |
| `DATA_MIGRATION_ERROR` | First failed task error per workflow, table, and partition. |
| `DATA_MIGRATION_WARNING` | Non-fatal migration warnings (for example type fallbacks). |
| `DATA_MIGRATION_WORKFLOW` | Filtered view of `WORKFLOW` for data-migration workflows only. |
| `DATA_VALIDATION_WORKFLOW` | Filtered view of `WORKFLOW` for data-validation workflows, with L1/L2/L3 rollups. |

Expand

Show lessSee more

#### Dashboard

| Object | Purpose |
| --- | --- |
| `DATA_MIGRATION_DASHBOARD` | Streamlit app for table-centric migration monitoring (Tables, Errors, Overview tabs). |

Expand

Show lessSee more

### DATA\_VALIDATION schema

#### Tables

| Object | Purpose |
| --- | --- |
| `TABLE_METADATA` | Per-workflow registry of validated tables and views (source and target identifiers, configuration). |
| `PARTITION_METADATA` | Validation partition boundaries and row counts per table. |
| `SCHEMA_VALIDATION_RESULTS` | L1 schema comparison results (column existence, types, ordinals, and similar). |
| `METRICS_VALIDATION_RESULTS` | L2 metrics comparison results per partition. |
| `ROW_VALIDATION_RESULTS` | L3 per-partition row comparison results. The `RESULT` column includes `MISMATCH`, `POSSIBLE_MISMATCH` (provisional, pending accepted-transformation reconcile), `NOT_FOUND_SOURCE`, `NOT_FOUND_TARGET`, `DUPLICATE_SOURCE`, `DUPLICATE_TARGET`, and `DUPLICATE_BOTH_SIDES`. See [Validation levels and result codes](../manual-migration/data-validation-configuration-reference#validation-levels-and-result-codes) for each code’s meaning. |
| `ROW_VALIDATION_SUMMARY` | L3 per-table or per-partition summary (matching vs differing chunks). |
| `CELL_VALIDATION_RESULTS` | L3 cell-level diffs (row index, column, source vs target values). |

Expand

Show lessSee more

#### Views

| Object | Purpose |
| --- | --- |
| `TABLE_PROGRESS` | Per-table validation rollup with L1/L2/L3 pass flags. |
| `TABLE_PROGRESS_DETAIL` | Per-table partition-level L2/L3 status counts. |
| `PARTITION_PROGRESS` | Derived L1/L2/L3 and overall validation status per partition. |
| `DATA_VALIDATION_ERROR` | Failed or abandoned validation **tasks** with error messages (distinct from row-level `MISMATCH` results). The `ERROR_MESSAGE` begins with an [error code](../manual-migration/data-validation-configuration-reference#data-validation-error-codes). |
| `DATA_VALIDATION_WARNING` | Non-fatal validation warnings (unsupported types, metric exclusions). |

Expand

Show lessSee more

#### Dashboard

| Object | Purpose |
| --- | --- |
| `DATA_VALIDATION_DASHBOARD` | Streamlit app for validation monitoring (Tables, Schema, Metrics, Rows, Cell, Errors tabs). |

Expand

Show lessSee more

## Managing workflow lifecycle

You can create workflows from SQL, and pause, resume, retry failed or abandoned tasks, or cancel migration and validation workflows. Prefer asking the Snowflake AIM Agent for Data Warehouses in natural language. Use the SnowConvert AI CLI or the stored procedures below when you want to drive the same actions yourself.

### Prefer the Snowflake AIM Agent for Data Warehouses

Tell the agent what you want done. It resolves the workflow and runs the matching lifecycle action for you.

**Prompts:**

Copy code

```
Pause the ORDERS migration workflow
```

Copy code

```
Resume my last validation workflow
```

Copy code

```
Retry the failed tasks on workflow 42
```

Copy code

```
Cancel the sales validation run
```

You can also ask it to pause or cancel a single table inside a workflow when you don’t want to stop the whole run.

### SnowConvert AI CLI

On the manual CLI path, use `scai data migrate pause|resume|cancel` and `scai data validate pause|resume|cancel` with the workflow name. See [Data migration (CLI)](../manual-migration/data-migration) and [Data validation (CLI)](../manual-migration/data-validation). Retrying failed or abandoned tasks is available through the Snowflake AIM Agent for Data Warehouses or the `RETRY_WORKFLOW` procedure below.

### Creating a workflow from SQL

To start a migration, validation, or re-validation workflow without the SnowConvert AI CLI, call `CREATE_WORKFLOW` from a worksheet or any SQL client. It creates a pending workflow, the same as the CLI does, and returns the new `WORKFLOW_ID`. The Orchestrator picks the workflow up and runs it.

Only `WORKFLOW_TYPE` is required. Pass the other arguments by name, and only the ones you need:

Copy code

```
CALL SNOWCONVERT_AI.DATA_MIGRATION.CREATE_WORKFLOW(
    WORKFLOW_TYPE => '<workflow_type>',
    CONFIGURATION => PARSE_JSON('<configuration_json>'),
    NAME => '<workflow_name>'
);
```

The arguments are declared in the order of the table below, so you can also pass the first ones by position, for example `CALL SNOWCONVERT_AI.DATA_MIGRATION.CREATE_WORKFLOW('data-validation', PARSE_JSON('<configuration_json>'), '<workflow_name>')`.

| Argument | Default | Description |
| --- | --- | --- |
| `WORKFLOW_TYPE` | Required | `data-migration`, `data-validation`, or `data-re-validate`. Not case-sensitive. |
| `CONFIGURATION` | `NULL` | Required for a migration or a validation: the workflow configuration as a JSON object. It uses the same keys as the configuration file, must set `sourcePlatform` (unless you pass `SOURCE_PLATFORM`), and must list at least one table under `tables`. A validation can list its entries under `tables`, `views`, or `objects` instead. For a re-validation, pass `NULL` or `{"revalidationRecheckSchema": true}`. |
| `NAME` | `NULL` | Workflow name. It must not match an existing workflow. When `NULL`, the name is `DATA_MIGRATION_WORKFLOW_` or `DATA_VALIDATION_WORKFLOW_` followed by the UTC time, the same as the CLI, or `REVALIDATION_OF_<parent name>` for a re-validation. |
| `PARENT_WORKFLOW_ID` | `NULL` | Required for a re-validation, and not allowed for other workflow types: the `WORKFLOW_ID` of the finished validation to re-validate. |
| `AFFINITY` | `NULL` | Worker affinity. When `NULL`, the configuration’s `affinity` is used. Leave it `NULL` for a re-validation. |
| `SOURCE_PLATFORM` | `NULL` | Source platform. When `NULL`, the configuration’s `sourcePlatform` is used, in lowercase. Leave it `NULL` for a re-validation. |
| `INITIATOR_ID` | `''` | Who created the workflow. Stored on the workflow row. |
| `SCHEMA_VERSION`, `DRIVER`, `TARGET_STAGE` | `'1.0'`, `NULL`, `NULL` | Used by SnowConvert AI clients. Leave them at their defaults. |

Expand

Show lessSee more

For example, to migrate two Teradata tables:

Copy code

```
CALL SNOWCONVERT_AI.DATA_MIGRATION.CREATE_WORKFLOW(
    WORKFLOW_TYPE => 'data-migration',
    NAME => 'TERADATA_SALES',
    CONFIGURATION => PARSE_JSON($$
    {
      "sourcePlatform": "teradata",
      "tables": [
        {
          "source": { "databaseName": "SALES", "schemaName": "SALES", "tableName": "ORDERS" },
          "target": { "databaseName": "MIGRATED", "schemaName": "SALES", "tableName": "ORDERS" },
          "columnNamesToPartitionBy": ["ORDER_ID"]
        },
        {
          "source": { "databaseName": "SALES", "schemaName": "SALES", "tableName": "CUSTOMERS" },
          "target": { "databaseName": "MIGRATED", "schemaName": "SALES", "tableName": "CUSTOMERS" }
        }
      ]
    }
    $$)
);
```

To validate the same tables:

Copy code

```
CALL SNOWCONVERT_AI.DATA_MIGRATION.CREATE_WORKFLOW(
    WORKFLOW_TYPE => 'data-validation',
    NAME => 'TERADATA_SALES_VALIDATION',
    CONFIGURATION => PARSE_JSON($$
    {
      "sourcePlatform": "teradata",
      "targetPlatform": "Snowflake",
      "targetDatabase": "MIGRATED",
      "validationConfiguration": {
        "schema_validation": true,
        "metrics_validation": true,
        "row_validation": true
      },
      "tables": [
        { "fullyQualifiedName": "SALES.ORDERS", "targetSchema": "SALES" },
        { "fullyQualifiedName": "SALES.CUSTOMERS", "targetSchema": "SALES" }
      ]
    }
    $$)
);
```

To re-validate that validation after it finishes, and re-check the schemas of tables whose schema validation failed:

Copy code

```
CALL SNOWCONVERT_AI.DATA_MIGRATION.CREATE_WORKFLOW(
    WORKFLOW_TYPE => 'data-re-validate',
    PARENT_WORKFLOW_ID => <workflow_id>,
    CONFIGURATION => PARSE_JSON('{"revalidationRecheckSchema": true}')
);
```

A re-validation copies the source platform, configuration, and affinity of its parent, so leave `AFFINITY` and `SOURCE_PLATFORM` `NULL`, and pass `CONFIGURATION` as `NULL` or as `{"revalidationRecheckSchema": true}`. The parent must be a finished `data-validation` or `data-re-validate` workflow. If you already re-validated it, the newest finished re-validation becomes the parent, and the call fails while a re-validation of it is still running.

The procedure checks the arguments above and fails with a message that names the problem. The Orchestrator checks the rest of the configuration when it starts the workflow. If the configuration is invalid, the workflow fails and the error is in the `LAST_ERROR_MESSAGE` column of `WORKFLOW`. To catch configuration errors before you create a workflow, use the SnowConvert AI CLI.

`CREATE_WORKFLOW` runs with the rights of the Orchestrator role, which owns it. To let another role create workflows, grant it `USAGE` on the `SNOWCONVERT_AI` database, the `DATA_MIGRATION` schema, and the procedure:

Copy code

```
GRANT USAGE ON PROCEDURE SNOWCONVERT_AI.DATA_MIGRATION.CREATE_WORKFLOW(VARCHAR, VARIANT, VARCHAR, INTEGER, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR, VARCHAR) TO ROLE <role_name>;
```

The grant is kept when the Orchestrator upgrades the metadata database.

### Stored procedures

These procedures in `SNOWCONVERT_AI.DATA_MIGRATION` apply to both migration and validation workflows. Replace `<workflow_id>` with the integer `WORKFLOW_ID` from the `WORKFLOW` table (see [Find your latest workflow](#find-your-latest-workflow)).

Copy code

```
-- Retry failed or abandoned tasks
CALL SNOWCONVERT_AI.DATA_MIGRATION.RETRY_WORKFLOW(<workflow_id>);

-- Pause all pending and executing tasks
CALL SNOWCONVERT_AI.DATA_MIGRATION.PAUSE_WORKFLOW(<workflow_id>);

-- Pause tasks for one source table
CALL SNOWCONVERT_AI.DATA_MIGRATION.PAUSE_TABLE(<workflow_id>, '<source_identifier>');

-- Resume a paused workflow
CALL SNOWCONVERT_AI.DATA_MIGRATION.RESUME_WORKFLOW(<workflow_id>);

-- Resume tasks for one source table
CALL SNOWCONVERT_AI.DATA_MIGRATION.RESUME_TABLE(<workflow_id>, '<source_identifier>');

-- Cancel a workflow (active tasks fail with a manual cancellation message)
CALL SNOWCONVERT_AI.DATA_MIGRATION.CANCEL_WORKFLOW(<workflow_id>);

-- Cancel tasks for one source table
CALL SNOWCONVERT_AI.DATA_MIGRATION.CANCEL_TABLE(<workflow_id>, '<source_identifier>');

-- Delete all tasks and table metadata for a workflow (cleanup)
CALL SNOWCONVERT_AI.DATA_MIGRATION.DELETE_WORKFLOW_TASKS(<workflow_id>);
```

`PAUSE_TABLE`, `RESUME_TABLE`, and `CANCEL_TABLE` leave the overall workflow status unchanged. `CANCEL_WORKFLOW` does not roll back rows already loaded into Snowflake.

### Internal procedures

AIM DMV also defines internal stored procedures such as `PULL_TASKS`, `PULL_SINGLE_TASK`, and `COMPLETE_TASK` that implement the distributed task queue. The Orchestrator and Workers call these automatically. **Do not call internal procedures directly** unless Snowflake Support instructs you to.

## Sample queries

Use these patterns as starting points. Replace `<workflow_id>` with your workflow’s `WORKFLOW_ID`.

### Find your latest workflow

Copy code

```
SELECT WORKFLOW_ID, WORKFLOW_NAME, WORKFLOW_TYPE, STATUS, CREATED_AT
FROM SNOWCONVERT_AI.DATA_MIGRATION.WORKFLOW
ORDER BY CREATED_AT DESC
LIMIT 10;
```

### Migration progress per table

Copy code

```
SELECT *
FROM SNOWCONVERT_AI.DATA_MIGRATION.TABLE_PROGRESS
WHERE WORKFLOW_ID = <workflow_id>
ORDER BY SOURCE_IDENTIFIER;
```

### Migration tables with errors

Copy code

```
SELECT SOURCE_IDENTIFIER, FAILED_PARTITIONS, EXAMPLE_ERROR_MESSAGE
FROM SNOWCONVERT_AI.DATA_MIGRATION.TABLE_PROGRESS_WITH_EXAMPLE_ERROR
WHERE WORKFLOW_ID = <workflow_id>
  AND FAILED_PARTITIONS > 0;
```

### Migration error details

Copy code

```
SELECT SOURCE_IDENTIFIER, PARTITION_NUMBER, ERROR_MESSAGE, CREATED_AT
FROM SNOWCONVERT_AI.DATA_MIGRATION.DATA_MIGRATION_ERROR
WHERE WORKFLOW_ID = <workflow_id>
ORDER BY SOURCE_IDENTIFIER, PARTITION_NUMBER;
```

### Validation status per table

Copy code

```
SELECT SOURCE_IDENTIFIER, L1_STATUS, L2_STATUS, L3_STATUS, OVERALL_STATUS
FROM SNOWCONVERT_AI.DATA_VALIDATION.TABLE_PROGRESS
WHERE WORKFLOW_ID = <workflow_id>
ORDER BY SOURCE_IDENTIFIER;
```

### Validation partition detail

Copy code

```
SELECT SOURCE_IDENTIFIER, PARTITION_NUMBER, L2_STATUS, L3_STATUS, OVERALL_STATUS
FROM SNOWCONVERT_AI.DATA_VALIDATION.TABLE_PROGRESS_DETAIL
WHERE WORKFLOW_ID = <workflow_id>
ORDER BY SOURCE_IDENTIFIER, PARTITION_NUMBER;
```

### Row-level mismatches (L3)

Copy code

```
SELECT TABLE_NAME, PARTITION_NUMBER, RESULT, SOURCE_INDEX_VALUES, TARGET_INDEX_VALUES
FROM SNOWCONVERT_AI.DATA_VALIDATION.ROW_VALIDATION_RESULTS
WHERE WORKFLOW_ID = <workflow_id>
  AND RESULT = 'MISMATCH'
ORDER BY TABLE_NAME, PARTITION_NUMBER
LIMIT 100;
```

### Provisional mismatches (accepted transformations)

While a table with `acceptedTransformations` is still running L3, row-hash mismatches can appear as `POSSIBLE_MISMATCH` until reconcile finishes. Use this query to inspect those provisional rows:

Copy code

```
SELECT TABLE_NAME, PARTITION_NUMBER, SOURCE_INDEX_VALUES
FROM SNOWCONVERT_AI.DATA_VALIDATION.ROW_VALIDATION_RESULTS
WHERE WORKFLOW_ID = <workflow_id>
  AND RESULT = 'POSSIBLE_MISMATCH'
ORDER BY TABLE_NAME, PARTITION_NUMBER;
```

For what `POSSIBLE_MISMATCH` means after the workflow completes, and when leftover rows are a problem, see [Caveat: POSSIBLE\_MISMATCH after the workflow finishes](./data-validation-advanced-configuration#caveat-possible_mismatch-after-the-workflow-finishes).

### Cell-level diffs (L3)

Copy code

```
SELECT TABLE_NAME, ROW_INDEX, COLUMN_NAME, SOURCE_VALUE, TARGET_VALUE
FROM SNOWCONVERT_AI.DATA_VALIDATION.CELL_VALIDATION_RESULTS
WHERE WORKFLOW_ID = <workflow_id>
ORDER BY TABLE_NAME, ROW_INDEX, COLUMN_NAME
LIMIT 100;
```

### Validation task errors and warnings

Copy code

```
SELECT SOURCE_IDENTIFIER, PARTITION_NUMBER, ERROR_MESSAGE
FROM SNOWCONVERT_AI.DATA_VALIDATION.DATA_VALIDATION_ERROR
WHERE WORKFLOW_ID = <workflow_id>;

SELECT SOURCE_IDENTIFIER, WARNING_MESSAGE
FROM SNOWCONVERT_AI.DATA_VALIDATION.DATA_VALIDATION_WARNING
WHERE WORKFLOW_ID = <workflow_id>;
```

Each `ERROR_MESSAGE` is prefixed with the task’s error code, for example `Data Validation failed (ConnectionError): ...`. See [Data validation error codes](../manual-migration/data-validation-configuration-reference#data-validation-error-codes) for what each code means and what to check.

### Correlate queries in QUERY\_HISTORY

Both the Orchestrator and Worker set Snowflake [`QUERY_TAG`](/sql-reference/parameters#query-tag) on every query:

Copy code

```
SELECT query_id, query_text, start_time
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE TRY_PARSE_JSON(query_tag):DMVF_WORKFLOW_ID = <workflow_id>
ORDER BY start_time DESC
LIMIT 50;
```

## Related content

- [Data Migration & Validation overview](./overview)
- [Data migration](./data-migration)
- [Data validation](./data-validation)
- [Accepted transformations](./data-validation#accepted-transformations)
