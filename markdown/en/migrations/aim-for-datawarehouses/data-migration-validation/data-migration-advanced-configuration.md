# Data migration advanced configuration

Data migration workflows and workers have a full YAML and TOML configuration surface documented in [Data migration configuration reference](../manual-migration/data-migration-configuration-reference). Most projects don’t need to hand-edit that file: the Snowflake AIM Agent for Data Warehouses generates it for you and walks through the fields that matter for your source platform, then shows you the result before anything runs.

This page describes common situations where you’ll want to go beyond the defaults, the prompt that gets you there, and where to find the exact property if you want to review or edit it yourself.

Tip

After the agent generates a workflow, it always shows you the YAML and asks whether you want to change anything before running it. You can request any of the scenarios below at that point, or ask for them up front.

## Choosing an extraction strategy

Most platforms support a **server-side export** strategy that writes data directly to object storage (for example `unload` for Redshift, `dbms_cloud` for Oracle, `write_nos` for Teradata). When your source supports one and the prerequisites are in place (external stage, credentials, platform permissions), use it for **all** tables from that source. Data never flows through the Worker, and you avoid mixing `regular` with a server-side strategy on the same source without a good reason.

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

Views don’t expose the catalog metadata needed for automatic inference. If your migration includes a view, tell the agent which column to partition by.

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

The built-in extraction strategies (`regular`, `unload`, `write_nos`, `dbms_cloud`, `tpt`) cover most sources. If your environment needs a different extraction path, for example a proprietary driver, a bulk-export tool not covered by a built-in strategy, or a custom authentication flow, you can supply your own **extraction plugin** and register it on a Worker’s source connection.

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

Once an initial full load completes, switch qualifying tables to incremental synchronization instead of re-extracting everything on every run.

**Prompt:**

Copy code

```
Set up incremental sync for the ORDERS table using the UPDATED_AT column
```

The agent sets `synchronization.strategy: watermark` and `watermarkColumn`, or `checksum` when there’s no reliable watermark column, and asks whether to also track deletions. The watermark can be a pseudo-column or system column not in the migrated schema (for example Oracle `ORA_ROWSCN` when there’s no `UPDATED_AT` column). For `checksum`, you can supply a custom aggregate expression such as `MAX(ORA_ROWSCN)`. See [SynchronizationStrategy model](../manual-migration/data-migration-configuration-reference#synchronizationstrategy-model).

Both strategies have blind spots. `checksum` skips some legacy large-object types and can round some floating-point values; `watermark` misses rows that changed without advancing the watermark. Review [Changes a checksum may not detect](../manual-migration/data-migration-configuration-reference#changes-a-checksum-may-not-detect) before relying on either for a table where silent drift matters.

## Smoke-testing the pipeline before a real load

**Prompt:**

Copy code

```
Before we migrate for real, run this workflow as a preflight so I can confirm the whole pipeline works
```

The agent sets `preflight: true` at the workflow root, and `preflightKeepSchema: true` if you want the transient schema left behind for inspection. See [Preflight: a bounded dry run](../manual-migration/data-migration-configuration-reference#preflight-bounded-dry-run).

## Migrating to Apache Iceberg™ tables

On supported source platforms, you can land migrated data in Apache Iceberg™ tables instead of native Snowflake tables.

**Prompt:**

Copy code

```
Migrate the SALES schema to Iceberg tables using my external volume MY_EXTERNAL_VOLUME
```

The agent sets `target.tableType: "iceberg"` and fills in `target.icebergConfig` for you. See [Iceberg configuration](../manual-migration/data-migration-configuration-reference#iceberg-configuration-targeticebergconfig).

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
