# Data Migration & Validation glossary

Terms used across AIM DMV documentation, listed alphabetically.

## Accepted transformation

A declarative rule in a validation workflow that whitelists a specific source-to-target value pair on a column (or columns matching a regex pattern). AIM DMV does not report matching diffs as mismatches. Requires L3 row validation. See [Accepted transformations](./data-validation#accepted-transformations).

## AIM DMV

Snowflake AIM **Data Migration and Validation**: the combined framework for moving data into Snowflake and validating that it matches the source. Uses an Orchestrator, Workers, and the `SNOWCONVERT_AI` metadata database.

## Anti-locking / query modifiers

Optional SQL hints appended to source queries to reduce locking on busy source tables. Set `queryModifiers` with `objectModifier` (appended after the table in `FROM`) and `selectModifier` (inserted after `SELECT`). User-configured hints are **off by default**. See [Anti-locking and query modifiers](../manual-migration/data-migration-configuration-reference#anti-locking-and-query-modifiers).

## BCP

Bulk Copy Program extraction strategy for SQL Server. Optional high-throughput bulk export when `use_bcp` is enabled and the `bcp` utility is installed on the Worker host.

## Cell validation

The L3 step that compares individual column values when row fingerprinting detects a mismatch. Results are stored in `CELL_VALIDATION_RESULTS`.

## Compute pool

Snowflake object that hosts Snowpark Container Services. You create a compute pool before deploying Orchestrator or Worker services. See [Deploying workers](./deploy-workers).

## Custom metrics

Workflow-wide overrides for L2 aggregate metrics, by data type or by individual source column. Set `validationCustomMetrics` at the workflow root with `source` and `target` arrays. Column-scoped entries under `source` use `column: {table.fullyQualifiedName}.{columnName}` and can remove a metric by omitting `metricQuery`. See [Custom metrics](../manual-migration/data-validation-configuration-reference#custom-metrics-validationcustommetrics).

## DUPLICATE\_SOURCE, DUPLICATE\_TARGET, DUPLICATE\_BOTH\_SIDES

L3 row validation results for duplicated index-column keys: `DUPLICATE_SOURCE` (the key appears more than once on the source), `DUPLICATE_TARGET` (more than once on the target), and `DUPLICATE_BOTH_SIDES` (duplicated on both sides). See [Validation levels and result codes](../manual-migration/data-validation-configuration-reference#validation-levels-and-result-codes).

## External access integration

Snowflake object that grants an SPCS service permission to reach external hosts defined in a network rule. Required for Workers that connect to source databases or download drivers at runtime.

## Extraction strategy

How AIM DMV reads data from the source during **migration**, and how it extracts L3 signature Parquet during **validation**. When the source has a native export, that export is the recommended extract: **UNLOAD** (Redshift), **WRITE\_NOS** (Teradata), **DBMS\_CLOUD** (Oracle), **CETAS** (SQL Server / Synapse), **EXPORT DATA** ([BigQuery](./migrate-bigquery)), or **regular** (PostgreSQL). For IBM DB2, prefer **`cloud_direct`** when an object store and external stage are available, and use **`regular`** otherwise. Validation uses the same strategy names under `validation_configuration.extraction`. See [Extraction strategies](../manual-migration/data-migration-configuration-reference#extraction-strategies) and [L3 extraction](../manual-migration/data-validation-configuration-reference#l3-extraction).

## Hybrid table

Snowflake table type used for `SNOWCONVERT_AI` metadata when your account supports them (for example the task queue). When Hybrid Tables are not available, AIM DMV creates equivalent metadata as standard tables, which works but is slower and limits how far you can scale out Workers. See [Prerequisites](./overview#prerequisites) on the overview page.

This is unrelated to L3 row validation. See [L1 / L2 / L3](#l1--l2--l3).

## L1 / L2 / L3

Validation levels: **L1** schema, **L2** metrics (aggregates), **L3** row and cell comparison. See [Data validation](./data-validation#validation-levels).

## MISMATCH

L3 row validation result when source and target values differ after comparison. Distinct from task-level errors in `DATA_VALIDATION_ERROR`, which are classified into [error codes](../manual-migration/data-validation-configuration-reference#data-validation-error-codes). See [Validation results](./data-validation#validation-results).

## Network rule

Snowflake object listing host and port pairs that a service may reach (`MODE = EGRESS`, `TYPE = HOST_PORT`). Used with an external access integration for SPCS Workers.

## Normalization

SQL expressions applied during validation so source and target values are compared in a canonical form (for example consistent date or numeric formatting). Normalization makes values comparable; it does not declare which diffs are acceptable. Override built-in templates with `validationCustomNormalizations` at the workflow root. Distinct from [accepted transformations](#accepted-transformation). See [Customizing normalization and metrics](../manual-migration/data-validation-configuration-reference#customizing-normalization-and-metrics).

## NOT\_FOUND\_SOURCE, NOT\_FOUND\_TARGET

L3 row validation results for rows present on only one side: `NOT_FOUND_SOURCE` (the row exists on the target but is missing from the source) and `NOT_FOUND_TARGET` (the row exists on the source but is missing from the target). See [Validation levels and result codes](../manual-migration/data-validation-configuration-reference#validation-levels-and-result-codes).

## Orchestrator

AIM DMV component that runs in Snowflake, creates workflows and tasks, loads staged migration data, and evaluates validation results.

## Partition

A subset of a table’s rows processed as one unit during migration or validation. Boundaries are stored in `PARTITION_METADATA`.

## PAT (Programmatic Access Token)

A programmatic Snowflake authentication method recommended for Orchestrator and Worker connections. Key-pair authentication is also suitable. Avoid interactive methods such as SSO because AIM DMV opens many short-lived connections. See [Connecting to Snowflake with a PAT](./overview#connecting-to-snowflake-with-a-pat).

## POSSIBLE\_MISMATCH

Provisional L3 row result recorded when a table defines accepted transformations and row hashing finds a mismatch. Reconcile promotes genuine problems to `MISMATCH` or removes accepted-only rows. Should not remain on a completed workflow. See [Caveat: POSSIBLE\_MISMATCH after the workflow finishes](./data-validation-advanced-configuration#caveat-possible_mismatch-after-the-workflow-finishes).

## Preflight

A bounded migration dry run (`preflight: true`). Each table is capped at one partition and the data lands in a transient `PREFLIGHT_<workflowId>` schema instead of the configured target, so one partition per table goes through the pipeline without writing to production tables. The real target tables must already exist. Distinct from `scai data doctor`, which checks infrastructure and configuration health before a run starts. See [Preflight: a bounded dry run](../manual-migration/data-migration-configuration-reference#preflight-bounded-dry-run).

## Rate limit

A rule in the `RATE_LIMIT` metadata table that caps how many concurrently executing tasks can match a scope pattern. Used to protect a busy source system or a shared resource. The cap is a target rather than a hard ceiling. See [Rate limiting](../manual-migration/data-migration-configuration-reference#rate-limiting).

## Re-validation

A child workflow that re-runs only the failed partitions and levels of a finished validation workflow, created with `scai data validate revalidate`. Distinct from incremental validation, which skips unchanged partitions. See [Re-validating what failed](./data-validation#re-validating-what-failed).

## Query tag

Snowflake session parameter set on every Orchestrator and Worker query. Filter by `TRY_PARSE_JSON(query_tag):DMVF_WORKFLOW_ID` in `QUERY_HISTORY`.

## Row fingerprinting

Default L3 technique: MD5 hashes of normalized row content per partition. Mismatches trigger cell drill-down.

## SNOWCONVERT\_AI

Default Snowflake database where AIM DMV stores workflow metadata, task queue state, migration progress, and validation results. See [The SNOWCONVERT\_AI database](./snowconvert-ai-database).

## Snowpark Container Services (SPCS)

Snowflake feature for running containerized services in your account. See [Deploying workers](./deploy-workers).

## Sync strategy

How a workflow decides which source rows to extract on each run and how they land in the target. The strategies are **none** (extract every row and append it), **full-replace** (extract every row and delete each partition’s target rows before loading), **watermark** (extract rows above the last stored value of a monotonically increasing column), and **checksum** (re-extract only partitions whose checksum changed). Data migration uses all four. Data validation uses **none**, **watermark**, and **checksum** for [incremental validation](../manual-migration/data-validation-configuration-reference#incremental-validation). See [Choosing a synchronization strategy](../manual-migration/data-migration-configuration-reference#choosing-a-synchronization-strategy).

## Task / task queue

Unit of work assigned to a Worker. Pending and in-progress tasks are stored in `TASK_QUEUE`.

## Tolerance

Relative numeric threshold for L2 metrics comparison (`comparisonConfiguration.tolerance`, default `0.001`). Does not apply to L3 cell comparison.

## UNLOAD

Redshift extraction strategy that exports data through Redshift `UNLOAD` to S3, then loads into Snowflake.

## Worker

AIM DMV component that connects to the source system and Snowflake, executes migration extraction or validation queries, and reports results to the Orchestrator.

## Workflow

Configuration and runtime state for one migration or validation run. Identified by `WORKFLOW_ID` in `SNOWCONVERT_AI.DATA_MIGRATION.WORKFLOW`.

## WRITE\_NOS / TPT

Teradata extraction strategies: **WRITE\_NOS** exports through Teradata object storage integration; **TPT** uses Teradata Parallel Transporter.

## Related content

- [Data Migration & Validation overview](./overview)
- [Data validation](./data-validation)
- [The SNOWCONVERT\_AI database](./snowconvert-ai-database)
