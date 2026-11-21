# How AIM DMV handles your data with AI

AIM Data Migration and Validation (AIM DMV) moves and compares your data with deterministic components that don’t use AI. The Snowflake AIM Agent for Data Warehouses is the only part that uses AI: it runs in [Snowflake CoCo](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code) and sends its context to a Snowflake-hosted model.

This page explains what each component does with your data, which information can reach the model’s context, and how you control that with the role you give Snowflake CoCo.

## Components that don’t use AI

These components run fixed code paths and make no calls to a large language model (LLM):

- **The Orchestrator.** It plans workflows, creates partitions and tasks, loads staged files, and evaluates validation results.
- **The Workers.** They read from your source system, upload files to Snowflake, and run validation queries on the source and Snowflake.
- **The SnowConvert AI CLI data commands** (`scai data ...`). They create, start, monitor and manage migration and validation workflows.

If you run AIM DMV from the SnowConvert AI CLI without the Snowflake AIM Agent for Data Warehouses, no part of the migration or validation sends your data to an AI model.

## What the Snowflake AIM Agent for Data Warehouses sends to the model

When you use the Snowflake AIM Agent for Data Warehouses, everything the agent reads becomes part of its context, which Snowflake CoCo sends to a Snowflake-hosted model. In a typical data migration or validation, that context includes:

- Object metadata and DDL from your source and Snowflake.
- SQL code, SnowConvert conversion output and EWIs.
- Workflow configuration files.
- The output of the `scai` commands the agent runs, including workflow and table status.
- Error and warning messages from failed tasks.

The agent runs SQL and `scai` commands, including validation status checks, with the target Snowflake connection you set for your AIM project, and source queries with your source connection. This target connection can be a different account, user or role from the connection Snowflake CoCo uses for model inference. The agent can read anything the target and source connections’ roles can read.

## Where data values can appear

Most of what the agent reads is metadata, but some AIM DMV outputs contain values from your data. If the agent can read them, they can reach the model’s context.

| Location | What it can contain |
| --- | --- |
| Your source tables and views, and the migrated tables and views in Snowflake | Your data itself. The agent samples rows from both when it validates a view. |
| `DATA_VALIDATION.METRICS_VALIDATION_RESULTS` | The source and target value of each metrics validation (L2) check, such as a column’s minimum and maximum values. |
| `DATA_VALIDATION.CELL_VALIDATION_RESULTS` | The source and target values of each cell that differs in row validation (L3). |
| `DATA_VALIDATION.ROW_VALIDATION_RESULTS` | Primary key or index values of rows that differ, are missing, or are duplicated. |
| `DATA_MIGRATION.PARTITION_METADATA` and `DATA_VALIDATION.PARTITION_METADATA` | The minimum and maximum partition column values of each partition. |
| `DATA_MIGRATION.TASK_QUEUE` | Task payloads with extraction and validation queries that include partition boundary values, and the last error message of each task. |
| `DATA_VALIDATION.DATA_VALIDATION_ERROR` and `DATA_MIGRATION.DATA_MIGRATION_ERROR` | Partition boundary values and error messages. Errors from your source system or driver can quote a value. |
| Orchestrator and Worker logs | Extraction, validation and load queries, including partition boundary values. |
| Validation reports that `scai data validate status` writes to your project | Copies of the metrics, row and cell validation results above. |

Expand

Show lessSee more

## How the agent sees validation results

When a validation workflow finishes, the agent checks its status. If every table passes, the agent reports the per-table result.

If a table fails, the agent retrieves the workflow’s validation reports so it can explain the failure. These reports include the row validation and cell validation results, so the differing source and target values and the keys of the affected rows can reach the model’s context.

When the agent validates a view it deployed, it also compares a sample of up to 10 rows from the source view with the same view in Snowflake.

## Limit what the agent can read

The agent reads what its database roles can read, and the files in your AIM project. To keep data values out of the model’s context:

1. Use a dedicated Snowflake role for your AIM project’s target Snowflake connection, separate from the role the Orchestrator and Workers use. Restricting only the connection Snowflake CoCo uses for inference doesn’t limit what the agent reads through the target connection. See [Required privileges](./required-privileges) for the Orchestrator and Worker role.
2. Don’t let that role read the tables listed in [Where data values can appear](#where-data-values-can-appear), whether through a direct grant, an inherited role or ownership, and don’t give the agent access to the Orchestrator and Worker logs.
3. Review data validation results yourself in the `SNOWCONVERT_AI` database or the `DATA_VALIDATION_DASHBOARD` app with a role that has access. See [The SNOWCONVERT\_AI database](./snowconvert-ai-database).
4. If you don’t want the agent to sample rows, use source and target connections whose roles can read metadata but not the data in your tables and views. The agent then can’t spot-check the views it validates.
5. Keep validation reports out of the project the agent works in. The agent reads the metrics, row and cell validation reports in the project’s `reports/data-validation/` folder whenever it checks a workflow’s status, even if it can’t query the tables. Delete reports that `scai data validate status` wrote earlier, or move them to a location the agent can’t access, along with any other local copies of your data.

Without access to these tables and reports, the agent can’t explain validation differences for you, and some status checks it runs can fail.

These steps cover the AIM DMV paths on this page. Anything else the agent’s roles can read, or any other file in its project, can also reach the model’s context.

## Telemetry

The Orchestrator and Workers send usage telemetry to Snowflake through the Snowflake connector, such as workflow type, table and partition counts, row and byte counts, durations, and failure categories. Telemetry doesn’t include row values, row differences, partition boundary values, or queries. It can include the error message of a failed task, and an error from your source system or driver can quote a value. Telemetry is never sent to an AI model.

## Related content

- [Data Migration & Validation overview](./overview)
- [Required privileges](./required-privileges)
- [The SNOWCONVERT\_AI database](./snowconvert-ai-database)
- [Snowflake AIM Agent for Data Warehouses](../overview)
