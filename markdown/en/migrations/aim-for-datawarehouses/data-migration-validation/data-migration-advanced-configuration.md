# Data migration advanced configuration

Data migration workflows and workers have a full YAML and TOML configuration surface documented in [Data migration configuration reference](../manual-migration/data-migration-configuration-reference). Most projects don’t need to hand-edit that file: the Snowflake AIM Agent for Data Warehouses generates it for you and walks through the fields that matter for your source platform, then shows you the result before anything runs.

This page describes common situations where you’ll want to go beyond the defaults, the prompt that gets you there, and where to find the exact property if you want to review or edit it yourself.

Tip

After the agent generates a workflow, it always shows you the YAML and asks whether you want to change anything before running it. You can request any of the scenarios below at that point, or ask for them up front.

## Choosing an extraction strategy

Most platforms support a **server-side export** strategy that writes data directly to object storage (for example `unload` for Redshift, `dbms_cloud` for Oracle, `write_nos` for Teradata). When your source supports one and the prerequisites are in place (external stage, credentials, platform permissions), use it for **all** tables from that source. Data never flows through the Worker, and you avoid mixing `regular` with a server-side strategy on the same source without a good reason. For **PostgreSQL**, **`regular`** (COPY, `use_copy = true`) is the recommended extract. **IBM DB2** has no server-side export. **`regular`** is the default, and **`cloud_direct`** is preferred when an object store and a matching external stage are available. Both strategies read through the Worker and write Parquet. See [Migrating Data from IBM DB2](./migrate-db2).

Use **`regular`** extraction only when data volume is genuinely small, or when object storage and the external stage aren’t set up yet. Once prerequisites are ready, switch the whole workflow to the server-side strategy rather than reserving it for “large tables only.”

**Prompt:**

Copy code

```
Use UNLOAD extraction for all tables in this migration
```

The agent selects the bulk strategy for your source platform, sets up the required external stage, and sets `extraction.strategy` and `extraction.externalStage` across the workflow. See [Extraction strategies](../manual-migration/data-migration-configuration-reference#extraction-strategies) for the full list and platform availability.

## Overriding partition keys

If you already know a good partition column, set it explicitly to avoid uneven partitions from a weak fallback selection. When you don’t specify `columnNamesToPartitionBy`, AIM DMV infers one automatically from source catalog metadata.

**Prompt:**

Copy code

```
Partition the ORDERS table by ORDER_DATE
```

The agent sets `columnNamesToPartitionBy` on the tables you name. See [What makes a good partition key](../manual-migration/data-migration-configuration-reference#what-makes-a-good-partition-key) for guidance on cardinality and composite keys, and [Automatic partition key selection](../manual-migration/data-migration-configuration-reference#automatic-partition-key-selection) for inference rules and physical column constraints.

Note

Data migration copies tables only. A source view, including a materialized view, fails before extraction, so migrate its base tables instead. A dynamic table isn’t a supported migration target either. See [Views and dynamic tables in migration](../manual-migration/data-migration-configuration-reference#views-and-dynamic-tables-in-migration). To compare a source view with its Snowflake counterpart after migration, see [Validating views](./data-validation-advanced-configuration#validating-views).

## Migrating INTERVAL columns

AIM DMV can migrate source `INTERVAL` columns either to a native Snowflake `INTERVAL` (`intervalHandling: "interval"`, the default) or to text (`intervalHandling: "varchar"`). Neither option is universally better.

On platforms whose `interval` type can mix year-month and day-time fields in one value (for example PostgreSQL), `"interval"` maps the column to Snowflake `INTERVAL DAY TO SECOND` and folds the year-month part into day-time. That keeps a native interval column, but months and years are treated as fixed-length spans, so calendar-accurate year-month precision is lost. Choose `"varchar"` when you need to preserve the original interval text, including exact year-month fields.

**Prompt:**

Copy code

```
For the EVENTS table, store INTERVAL columns as text instead of native INTERVAL so we keep exact year-month fields
```

The agent sets `intervalHandling: "varchar"` on the tables you name (or leaves the default `"interval"` when you prefer a native day-time interval). See [INTERVAL data type handling](../manual-migration/data-migration-configuration-reference#interval-data-type-handling) for the property reference, and your [Migrating Data from …](./data-migration#supported-source-platforms) page for platform-specific notes.

Note

Apache Iceberg™ targets always store `INTERVAL` columns as `VARCHAR`, because Iceberg has no native interval type.

## Preparing a custom extraction plugin

The built-in extraction strategies (`regular`, `unload`, `write_nos`, `dbms_cloud`, `cet_as`, `export_data`, and `cloud_direct`) cover most sources. If your environment needs a different extraction path, for example a proprietary driver, a bulk-export tool not covered by a built-in strategy, or a custom authentication flow, you can supply your own **extraction plugin** and register it on a Worker’s source connection.

At a high level, preparing a plugin means:

1. **Implement the extraction contract.** Write a class that, given a query or export statement, produces the extracted data at a destination the Worker can pick up. Most plugins only need to implement the “write the dataset” step; the Worker handles staging and cleanup around it.
2. **Match the expected output format.** Write **Parquet** (preferred) or a delimited **CSV** with no header row, so the Worker’s loader can read it the same way it reads built-in extractor output.
3. **Package it so the Worker can import it.** Install it as a Python package on the Worker, or make it available on the Worker’s `PYTHONPATH`.
4. **Register it in the Worker configuration.** Set `plugin_class` on the relevant `[connections.source.*]` section to the plugin’s fully qualified class name.

**Prompt:**

Copy code

```
I have a custom extraction plugin for this source. Help me register it in the Worker configuration.
```

The agent points you to the Worker TOML for your connection and sets `plugin_class` for you once you confirm the class name and that it’s importable on the Worker. See [Using a custom extraction plugin](../manual-migration/data-migration-configuration-reference#using-a-custom-extraction-plugin) in the configuration reference for the exact TOML property and an example.

Warning

A Worker imports and runs `plugin_class` in-process with its own privileges. Only point `plugin_class` at code you trust, and set it in Worker configuration only, never as part of a workflow that could be supplied by someone else.

## Incremental sync after the first load

Once an initial full load completes, switch qualifying tables to incremental synchronization instead of re-extracting everything on every run. A run is one migration command that you invoke. Incremental sync is that command run again, not a loop inside AIM DMV: a `watermark` or `checksum` run reuses the partition metadata that the earlier run stored, and `none` and `full-replace` runs reuse nothing. To repeat runs on a timetable, see [Running a migration on a schedule](#running-a-migration-on-a-schedule).

**Prompt:**

Copy code

```
Set up incremental sync for the ORDERS table using the UPDATED_AT column
```

The agent sets `synchronization.strategy: watermark` and `watermarkColumn: UPDATED_AT`. It sets `trackModifications` and `trackDeletions` to `true` only when the table has a primary key and the target is already populated. Otherwise it leaves them off, so updated rows are appended as a second version and deleted rows stay on the target. The watermark can be a pseudo-column or system column that isn’t migrated, such as Oracle `ORA_ROWSCN`. See [Choosing a synchronization strategy](../manual-migration/data-migration-configuration-reference#choosing-a-synchronization-strategy) for the full comparison.

**Prompt:**

Copy code

```
Keep the DIM_CUSTOMER table in sync. It has no UPDATED_AT column.
```

The agent sets `synchronization.strategy: checksum`. When the source has a cheap change signal, such as Oracle `ORA_ROWSCN` or a row-version column, it sets `checksumExpression` to a SQL aggregate over that signal, such as `MAX(ORA_ROWSCN)`. Otherwise it uses the default checksum. A partition whose checksum changed is cleared and reloaded, so the reload doesn’t append a second copy of rows that are already on the target. Every run still computes the checksum of every partition, including partitions that didn’t change. See [checksum](../manual-migration/data-migration-configuration-reference#checksum) and [Changes a checksum may not detect](../manual-migration/data-migration-configuration-reference#changes-a-checksum-may-not-detect) before you rely on it for a table where silent drift matters.

Each incremental strategy has blind spots. `checksum` skips some legacy large-object types and can round some floating-point values, and `watermark` misses rows that changed without advancing the watermark.

## Repeatable full reloads

`checksum` already avoids a second copy without a watermark, at the cost of computing a checksum for every partition on every run. Use a full reload when you want every partition extracted and replaced on every run, with no checksum.

**Prompt:**

Copy code

```
Reload the CUSTOMERS table completely on every run so the target matches the source and nothing is duplicated
```

The agent sets `synchronization.strategy: full-replace`. Each run extracts every partition and deletes that partition’s target rows before loading it, so a rerun overwrites the earlier load. For an Iceberg target, the agent leaves `full-replace` unset, because the orchestrator rejects it. A second `none` run fails when the Iceberg table already exists. A later `watermark` or `checksum` run reuses a Snowflake-managed Iceberg table after a completed run. See [Choosing a synchronization strategy](../manual-migration/data-migration-configuration-reference#choosing-a-synchronization-strategy) for the behavior of each strategy.

Warning

`full-replace` deletes every row in the target partition before loading it. Rows that you added to the target by hand, or that other processes wrote, are removed by the next run. Confirm that the target table belongs to the migration before you choose this strategy.

## Running a migration on a schedule

To repeat a migration on a timetable, for example a nightly incremental sync, create a Snowflake task that inserts a new workflow and resumes the SPCS services. [Submitting a validation from a Snowflake task](./data-validation-advanced-configuration#submitting-a-validation-from-a-snowflake-task) shows that task. For a migration, set `WORKFLOW_TYPE` to `data-migration` and `TARGET_CLOUD_STAGE_NAME` to `@SNOWCONVERT_AI.DATA_MIGRATION.TASK_RESULTS`. AIM DMV doesn’t create the task or start the next run itself. Each insert is one new workflow. You can also run `scai data migrate create-workflow` from a scheduler on a host. That command names the workflow with a timestamp and a unique suffix.

**Prompt:**

Copy code

```
Run the ORDERS incremental sync again
```

The agent submits the same workflow configuration again as a new run on the shared Orchestrator and Workers. It doesn’t schedule later runs. If the Orchestrator or a Worker isn’t running, the agent tells you which one and offers to start it. See [State and reruns](../manual-migration/data-migration-configuration-reference#state-and-reruns) for what each strategy reuses from earlier runs.

On SPCS, each externally scheduled run follows this sequence:

1. **Resume the services.** The Orchestrator and every Worker suspend themselves after `DM_IDLE_SHUTDOWN_MINUTES` without work, 60 minutes by default, so they’re usually suspended when the next run is due. Submitting a workflow doesn’t resume a suspended service: a workflow submitted while they’re suspended is created and stays `pending`. Resume the Orchestrator and every Worker service first, as described in [Resuming services before the next wave](./deploy-workers#resuming-services-before-the-next-wave).
2. **Run the workflow and wait for it.** Run `scai data migrate create-workflow --watch`, which blocks until the run finishes. Without `--watch`, the command returns as soon as the workflow is submitted, so its exit code doesn’t reflect the run.
3. **Check the result.** With `--watch`, the command exits `0` when the run finishes without failures, and `1` when a partition fails, a table doesn’t finish preprocessing, or the command can’t complete. Use `scai data migrate status <WORKFLOW_NAME>` for a run’s progress and errors, and `scai data migrate list` to find recent runs. See the [SCAI command reference](../manual-migration/SCAI_Command_Reference).
4. **Run again after a failure.** There’s no command that re-runs a failed migration workflow. Run the same command again, which creates a new workflow. To retry only the failed tasks of the existing workflow, see [Managing workflow lifecycle](./snowconvert-ai-database#workflow-management-procedures).
5. **Let idle shutdown stop the services.** After the run, each service suspends itself once it has been idle for its `DM_IDLE_SHUTDOWN_MINUTES`. See [Idle shutdown](./deploy-workers#idle-shutdown) and [Controlling cost on SPCS](./deploy-workers#controlling-cost-on-spcs).

`scai data migrate start` doesn’t use the SPCS services. It runs a local Orchestrator and Worker for as long as the command runs and blocks until the run finishes, so a scheduler on a host that can reach the source can run it without resuming anything.

Don’t start the next run of the same tables until the previous run finishes. When a run starts, it skips each table that another migration workflow is initializing or running, as long as that workflow has sent a heartbeat within the last 15 minutes and both workflows have the same affinity or either has none. Each skipped table is reported as `Skipped '<table>': already being processed by workflow '<name>' (created <time>, affinity '<affinity>') to avoid duplicate data / race conditions.` A workflow that’s still `pending` doesn’t hold its tables. When every table is skipped, the run finishes with exit code `0` and the warning “The migration finished without migrating any table: every configured table is already being migrated by another active workflow. Re-run once that workflow finishes.” Treat that warning as a run that did nothing.

Note

`scheduled_start_time` isn’t a scheduling setting. The Orchestrator’s idle-shutdown safety check reads it from a workflow’s stored configuration, but nothing in AIM DMV writes it, `scai` has no option for it, and the workflow configuration schema rejects it as an unknown key.

## Smoke-testing the pipeline before a real load

A **preflight** sends one partition of each table through the real pipeline into transient copies of your target tables, so you find connection, extraction, and load problems before the first real load. It doesn’t test the whole workload. It doesn’t show how long the full load takes or whether the rest of the data loads, and on a small table the one partition is the whole table, not a sample.

**Prompt:**

Copy code

```
Before we migrate for real, run this workflow as a preflight so I can check the pipeline
```

The agent sets `preflight: true` at the workflow root and runs the workflow. Before it runs, it checks that the real target tables are deployed: a preflight copies each target’s structure, so it can’t create a missing target the way a real load does. When the preflight finishes, the agent reports which tables completed and which failed, and reminds you that the result covers one partition per table. See [Preflight: a bounded dry run](../manual-migration/data-migration-configuration-reference#preflight-bounded-dry-run) for the prerequisites, which rows a preflight loads, and how to read the result.

**Prompt:**

Copy code

```
Run the preflight but keep the transient schema so I can look at what was loaded
```

The agent also sets `preflightKeepSchema: true`. After the run, it gives you the `PREFLIGHT_<workflowId>` schema in each target database and the `DROP SCHEMA` statement to run when you’re done, because AIM DMV doesn’t drop a kept schema for you. See [Keeping the preflight schema](../manual-migration/data-migration-configuration-reference#keeping-the-preflight-schema) and [Cleaning up after a preflight](../manual-migration/data-migration-configuration-reference#cleaning-up-after-a-preflight).

Decide before you start:

- **Whether to keep the transient schema.** Keep it to inspect the loaded rows, and drop it yourself afterward.
- **When to run it.** Run it before the first full load of the tables. A preflight between a full load and later `checksum` or `watermark` runs of the same tables makes those runs reuse the preflight’s single partition.

A preflight runs on the same Orchestrator, Workers, and compute pool as a real load. For cost, see [Controlling cost on SPCS](./deploy-workers#controlling-cost-on-spcs).

## Migrating to Apache Iceberg™ tables

On supported source platforms, you can land migrated data in Apache Iceberg™ tables instead of native Snowflake tables. The default profile is Iceberg **spec v2** with `storageMode: compatible`.

**Prompt:**

Copy code

```
Migrate the SALES schema to Iceberg spec v2 tables using my external volume MY_EXTERNAL_VOLUME
```

The agent sets `target.tableType: "iceberg"` and fills in `target.icebergConfig` (`icebergSpec: v2`, `storageMode: compatible`, your external volume, and a `baseLocationPrefix` when the volume is a customer bucket). See [Apache Iceberg™ tables (spec v2 and v3)](./iceberg) and [Iceberg configuration](../manual-migration/data-migration-configuration-reference#iceberg-configuration-targeticebergconfig).

## Reducing lock contention on the source

If migration reads are blocked by production writers, you can opt in to anti-locking query hints. This trades consistency guarantees (dirty reads) for reduced blocking, so use it only when locking is actually a problem.

**Prompt:**

Copy code

```
Source reads are getting blocked by production traffic. Can we reduce locking during migration?
```

The agent explains the platform-specific tradeoff and, if you confirm, sets the appropriate `queryModifiers` (for example `WITH (NOLOCK)` on SQL Server). See [Anti-locking and query modifiers](../manual-migration/data-migration-configuration-reference#anti-locking-and-query-modifiers) for per-platform defaults and the pros and cons.

## Protecting a busy source system

If extraction concurrency is overwhelming the source, cap the number of extraction tasks that run at once instead of tearing down Workers. **Rate limiting** holds matching tasks in `pending` while the Workers stay up.

**Prompt:**

Copy code

```
The source database is getting overloaded. Cap us at 5 concurrent extraction tasks.
```

Rate limits are rows in the `RATE_LIMIT` metadata table, not properties in the workflow file, so the agent shows you the `INSERT` statement to run. Two things to know before you rely on them: the limit is a target rather than a hard ceiling (brief overshoot to about twice the target is possible), and a value of `0` is the one exact setting, which pauses matching work entirely.

See [Rate limiting](../manual-migration/data-migration-configuration-reference#rate-limiting).

## Keeping or discarding staged files

Migration stages intermediate files while it runs and deletes them when the workflow succeeds. When you’re debugging a failing workflow, keep them instead.

**Prompt:**

Copy code

```
Keep the staged files for this run so I can look at what got extracted
```

The agent sets `cleanUpTransientResources` to `never`, or to `always` if you’d rather never accumulate staged files even after a failure. The default is `on-success`. See [Cleaning up transient resources](../manual-migration/data-migration-configuration-reference#cleaning-up-transient-resources).

## Renaming or remapping columns and types

**Prompt:**

Copy code

```
Rename CUST_NM to CUSTOMER_NAME during migration, and map the source NUMBER(38,10) columns to a smaller precision
```

The agent sets `columnNameMappings` and `columnTypeMappings` on the affected tables. See [ColumnTypeMapping and ColumnNameMapping models](../manual-migration/data-migration-configuration-reference#columntypemapping-model).

Note

These mappings apply to migration only. Validation has a separate mechanism, so tell the agent about any type remapping when you set up validation, or L1 will compare against the default expected types and report failures. See [Overriding L2 metrics or L1 type mapping](./data-validation-advanced-configuration#overriding-l2-metrics-or-l1-type-mapping).

## Limiting a migration to a subset of rows

Useful for an initial test run or a table you only want to partially migrate.

**Prompt:**

Copy code

```
For the first test run, only migrate orders where IS_DELETED = 0
```

The agent sets `whereClauseCriteria` on the affected table. See [TableConfiguration model](../manual-migration/data-migration-configuration-reference#tableconfiguration-model) and [Initial testing](./data-migration#initial-testing).

## Related content

- [Data migration](./data-migration)
- [Data migration configuration reference](../manual-migration/data-migration-configuration-reference)
- [Data validation advanced configuration](./data-validation-advanced-configuration)
- [Deploying workers](./deploy-workers)
- [Glossary](./glossary)
