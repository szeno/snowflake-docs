# Testing SSIS pipelines

This page describes how the Snowflake AIM Agent for Data Warehouses tests a converted **SSIS** package for equivalence with the original. The original package runs on your SQL Server instance, the converted pipeline runs on Snowflake, and the tables each one wrote are compared row by row. For stored procedures and UDFs, which use a different flow and a different comparison model, see [Testing stored procedures and UDFs](/migrations/aim-for-datawarehouses/testing/sprocs-and-udfs).

Testing runs inside the migrate-objects loop. After a package is stabilized and deployed to Snowflake, it goes through a **seed → validate → fix** cycle and is only marked complete once the tables it writes match the tables the original package writes (or you choose to skip it).

Note

A pipeline can’t be tested by calling it with inputs and diffing a return value, because a pipeline’s output **is** the data it lands. So the comparison is table-to-table, and both sides have to actually run.

## The testing pipeline

For each SSIS code unit, the Snowflake AIM Agent for Data Warehouses drives two underlying commands:

| Command | Role |
| --- | --- |
| `scai test seed` | Scaffolds the package’s test definition (a YAML file). It reads the pipeline’s **write** dependencies from the Code Unit Registry (every table the package inserts, updates, merges, or deletes) and emits one source-to-target table pair per written table. |
| `scai test etl-validate` | Runs both sides: launches the original package on SQL Server, runs the converted pipeline on Snowflake, then compares each table pair. |

Expand

Show lessSee more

You normally don’t invoke these directly. You drive them conversationally, for example:

```
"Seed the ETL test for Sales_ETL"
"Validate the next SSIS package"
```

To run the validation yourself:

Copy code

```
scai test etl-validate --platform ssis --source-connection my-sqlserver
```

To validate a single package, add `--where "id = '<code-unit-id>'"`; to run only packages whose names match a pattern, add `--pipeline '%Load%'`.

Before starting a comparison, the agent runs a pre-flight check, `scai test etl-validate --platform ssis --check-env`, which you can also run yourself before a long run. It confirms that:

- The source SQL Server connection opens and answers a query.
- The Snowflake connection does the same.
- The SSISDB catalog is deployed on the instance and readable.

It is much cheaper to find a closed port there than partway through a run. The pre-flight doesn’t check SQL Agent permissions or isolation privileges; those are checked when each package runs.

Note

The pre-flight probes the SSISDB catalog even when your packages are deployed to the legacy MSDB package store, so it reports a failure on an instance without SSISDB. On such an instance, treat that one check as expected.

### Two-sided comparison

The framework runs the pipeline on both sides and compares what each one wrote. For each package:

1. The tables in the package’s write-set are backed up on both sides. See [Isolation](#isolation).
2. **Source side:** the original `.dtsx` package runs on your SQL Server instance, through the [launch method](#how-the-original-package-is-launched) in its test definition, and is polled until it finishes. The rows it lands are the reference.
3. **Snowflake side:** the converted pipeline runs as whatever it became. See [What runs the converted side](#what-runs-the-converted-side).
4. **Comparison:** each declared source table is compared against its Snowflake counterpart, row by row, aligned on a key you confirm.
5. Both sides are restored from their backups.

### Isolation

Because both sides write real tables, each run isolates the package’s **write-set**: every table the package writes, plus the compared source tables. The two sides are isolated independently, so a validation doesn’t leave either system permanently changed:

- **SQL Server:** before the package starts, the framework copies each write-set table into a run-scoped backup table, and restores it afterward.
- **Snowflake:** each write-set table is backed up as a zero-copy clone, and the target tables are cleared before the converted pipeline runs. Afterward, the tables are restored from the clones, and any write-set table that the run created is dropped.

Isolation is on by default. Before each package runs, the framework checks the isolation privileges on both sides. If a required privilege is missing, it prints a warning that names each missing privilege, and then **refuses the unit**: the package doesn’t run, and the unit is reported as a failure. It never runs unisolated. For the privileges, see [Prerequisites](#prerequisites).

To turn isolation off on purpose, set `etl_source_isolation_strategy: none` or `etl_target_isolation_strategy: none` in `.scai/settings/test_config.yaml`. The package’s writes then persist on that side.

Note

ETL isolation works at the table level. It doesn’t use the database-level clone or the transaction rollback that procedure testing uses, described in [Considerations by source dialect](/migrations/aim-for-datawarehouses/testing/considerations-by-dialect), so it doesn’t need `CREATE DATABASE ON ACCOUNT` or snapshot isolation.

### How the original package is launched

Which mechanism starts the package is a per-unit setting, `execution.source.method`, and the right choice depends on how your source connection authenticates. If your connection uses a user name and password, it uses SQL Server Authentication. If it uses a trusted connection (`auth_method: windows`), it uses Windows Authentication.

| Method | How it launches | When to use it |
| --- | --- | --- |
| `agent_job` | Starts a SQL Agent job, then polls the job history for the outcome. The job is created on first run if it doesn’t already exist. | The seeded default, and the method that works with SQL Server Authentication. |
| `ssisdb_catalog` | Creates and starts an execution through the SSISDB catalog, then polls it. Applies any package `parameters` you declared. | Windows Authentication only. The default when a hand-written test definition omits `method`. |
| `auto` | When validation runs on Windows, checks the authentication scheme of the live SQL Server session: Windows Authentication selects `ssisdb_catalog`, anything else falls back to `agent_job`. On any other operating system, always selects `agent_job`. | When the same project is run from hosts that authenticate differently. |

Expand

Show lessSee more

Important

SQL Server’s SSISDB catalog rejects SQL Server Authentication logins outright (error 27123), whatever privileges they hold. That is why `agent_job` is the seeded default: it reaches the same package through SQL Agent and works under either authentication mode. Package `parameters` are applied only by `ssisdb_catalog`; `agent_job` runs the package as its job step is defined.

With `agent_job` and no `job_name` of your own, the run derives a deterministic job name, `scai_etl_<folder>_<project>_<package>` (the package name without `.dtsx`), and creates the job if it’s missing. It skips creation when a job of that name already exists, so re-running is safe. Set `job_name` to an existing job to opt out of that and drive the job as-is.

#### Catalog and MSDB packages

Packages can be deployed either to the Integration Services catalog (SSISDB, the default) or to the legacy MSDB package store, and the two need different job steps. The test definition records which one in `execution.source.package_store` (`ssisdb` or `msdb`).

**You normally don’t set this yourself.** When `scai test seed` runs with a SQL Server source connection (the one named with `--source-connection`, or your default), it looks the package up in both stores and writes `package_store`, `folder`, and, for SSISDB, `project`. If the package is in both stores, SSISDB wins. A seeded file that already has these fields needs no changes.

The fields are left out, rather than guessed, when the seed had no source connection or didn’t find the package. A test definition without `package_store` is treated as SSISDB, so what happens next depends on where the package really is:

- **SSISDB:** nothing to do. The run looks up the `folder` and `project` in SSISDB when it starts.
- **MSDB:** the run looks in SSISDB, doesn’t find the package, and fails with `SSISDB.catalog has no project containing a package named …`. Re-run `scai test seed` with the source connection so it can find the package, or add `package_store: msdb` and the `folder` to `execution.source` yourself.

One MSDB case always needs a hand edit: a package stored in the MSDB root folder. The seed writes `package_store: msdb` with no `folder`, because the root has no folder name, and the run then fails with `package_store=msdb requires an explicit 'folder'`. Create a SQL Agent job for the package and set `job_name` to it, which skips the lookup entirely.

### What runs the converted side

An SSIS package doesn’t convert to one fixed shape. The seeder picks the Snowflake-side target from what the conversion produced:

| Target | When it’s used | What runs |
| --- | --- | --- |
| Snowflake task graph | The package converted to Snowflake tasks. | Executes the deployed root task and asserts every task succeeded. Task graphs are created **suspended**; activating them is a separate, deliberate step. |
| Local dbt project | The package converted to a dbt project, with no task graph. | Runs `dbt run` against the project on disk, using the `dbt` on your path. |

Expand

Show lessSee more

Caution

If you narrow a local dbt project’s model selector (`select`) by hand, keep it matching. `dbt` exits 0 when a selector matches nothing, so a stale selector makes the test **pass having built no models**, and the comparison then runs against whatever was already in the tables. Remove the selector entirely to build the whole project instead.

#### How conversion options affect testing

The flags passed to `scai code convert`, described in [SnowConvert AI CLI ETL migration](/migrations/aim-for-datawarehouses/manual-migration/etl-migration#conversion-flags), change what the Snowflake side contains:

- **A package with a task graph** is tested through the task graph, whatever form its data flows took. Flags that change how data flows are converted don’t change how the package is tested.
- **`--consolidate-dbt-projects`** converts each package to one dbt project, instead of one dbt project per data flow. For a package without a task graph, a single project gives the seeder one `project_dir` to run. When a package has several dbt projects and no task graph, the seeder writes the placeholder `TODO_ETL_PROJECT_DIR` and warns; set `project_dir` before you validate.

## Where test cases live

Each package’s test is stored as a YAML file in the project:

```
artifacts/<code-unit-id>/etl-test/<name>.yml
```

The file has two parts:

- **`execution`:** how to launch the source package (`source`) and which converted target to run (`target`). This block is written by `scai test seed`; you don’t hand-author it.
- **`comparison`:** the `tables` list of source-to-target pairs to compare. The seeder fills in one pair for each table the package writes.

At seed time, the seeder also finds where the package is deployed and writes `package_store`, `folder`, and `project` into `execution.source`, because the registry doesn’t record deployment state. See [Catalog and MSDB packages](#catalog-and-msdb-packages) for when those fields are missing and what to do.

For example:

Copy code

```
# artifacts/LoadSales/etl-test/LoadSales.yml
package: LoadSales

execution:
  source:
    method: agent_job
    package_store: ssisdb
    folder: Sales
    project: SalesETL
    package: LoadSales.dtsx
  target:
    project_dir: snowflake/_etl/LoadSales/df_load_sales/
    select: df_load_sales
    timeout_seconds: 1800

comparison:
  tables:
    - source: SourceDB.dbo.FactSales
      target: SALES_DB.DBO.FACTSALES
      index_columns: [SalesOrderID, SalesOrderDetailID]
      target_index_columns: [SALESORDERID, SALESORDERDETAILID]
      source_columns: {mode: exclude, list: [ModifiedDate]}
      target_columns: {mode: exclude, list: [MODIFIEDDATE]}

    - source: SourceDB.dbo.DimProduct
      target: SALES_DB.DBO.DIMPRODUCT
      index_columns: [ProductID]
      target_index_columns: [PRODUCTID]
```

**The join key is the most important decision you make.** `index_columns` names the column or columns that uniquely key a row; without it there is no way to align a source row with its Snowflake counterpart. The seeder fills it from the table’s primary key when the registry records one, and leaves it out otherwise. When a key column’s name differs on Snowflake, for example because unquoted names are uppercased, the seeder also writes `target_index_columns`, and `column_mappings` for other renamed columns. The agent then proposes keys for each pair and asks you to confirm or correct them, because the registry can miss dynamically named or conditionally written tables. A good key:

- Uniquely identifies each row, like a primary key or a composite business key.
- Is present on both sides, under the same name or mapped with `target_index_columns`.
- Is stable across runs, not generated fresh each time the package runs.

Exclude non-deterministic columns, such as identity values and columns set by `GETDATE()`, `SYSDATETIME()`, or `NEWID()`, with `source_columns` and `target_columns` (`{mode: exclude, list: [...]}`), or they will differ on every run and hide real failures.

Re-seeding with `--append` regenerates the table pairs from the current registry and keeps everything else you typed on each surviving pair, including `index_columns`, `target_index_columns`, `column_mappings`, and column exclusions. It regenerates the whole `execution` block, though, so re-apply any hand edits to `method`, `folder`, `job_name`, `package_store`, or `parameters` after re-seeding.

The parser is strict: an unrecognized key anywhere in the file is a hard parse error, which catches a typo at parse time instead of halfway through a run. Credentials never belong in a per-unit file; the SQL Server connection lives once per project, in the source connection or in `test_config.yaml`.

Results are written to the `VALIDATION` schema of your results database in Snowflake (the `testing_results_database` set in `test_config.yaml`, or the `validation_database` if that isn’t set) and surfaced through reporting views for later review. See [Reading test results](#reading-test-results).

## Reading test results

Each compared table resolves to one of the following statuses:

| Status | Meaning |
| --- | --- |
| `PASS` | The Snowflake table matches the source table. |
| `FAIL` | The two tables differ. The result rows carry the differences. |
| `ERROR` | A side failed to execute: the package errored, the dbt run or task graph failed, or a table could not be read. The result row carries the error. |
| `SKIPPED` | The table was not compared. The row carries the reason. |

Expand

Show lessSee more

Results land in the `VALIDATION.RESULTS` table and are surfaced through these views:

| View | Contents |
| --- | --- |
| `ETL_SUMMARY` | One row for each unit and run, with counts of passed, failed, errored, and skipped parts and a pass rate. |
| `ETL_FAILURES` | Only the `FAIL` and `ERROR` rows, with their messages and details. |
| `ETL_LATEST` | The most recent result for each part, including each compared table pair. |
| `ETL_RESULTS_DETAIL` | Every result row, with its status, skip reason, message, and details. |

Expand

Show lessSee more

Each source-side and Snowflake-side execution step is also logged to the `VALIDATION.ETL_EXECUTION_LOG` table. For example, to list everything that didn’t pass in the latest run of each part:

Copy code

```
SELECT code_unit_id, part_id, status, message, details:error::STRING AS error, executed_at
  FROM my_validation_db.VALIDATION.ETL_LATEST
  WHERE status <> 'PASS'
  ORDER BY executed_at DESC;
```

For a compared table pair, `part_id` has the form `<source-table>-><target-table>`.

On each unit it actually ran, `scai test etl-validate` stamps the result on the registry entry: completed when the unit passed, and failed with a comparison error when it did not. A unit skipped for lack of a test definition gets no stamp and stays pending. The CLI owns that stamp, so a result is never inferred from narration.

## The fix loop

When a validation does not pass, the Snowflake AIM Agent for Data Warehouses distinguishes two kinds of failure before attempting any change:

- **Dependency failure.** The package’s write-set couldn’t be resolved, so the seeder **skips the unit with a named reason** rather than half-testing it: `no_write_dependencies` (no written tables recorded), `missing_dependency` (an unfinished upstream unit), `missing_canonical_name` (a table with no canonical name), or `pending_format` (converted parts not yet in a form the run can execute). The SQL isn’t broken; a prerequisite hasn’t been finished. The agent reports the specific cause and moves on.
- **Conversion failure.** The two tables genuinely differ, which points at a gap in the converted logic. The agent surfaces the failing tables and their row-level differences, patches the converted code, and re-runs.

Two causes account for most differences before you go looking at the converted logic: a **join key that isn’t actually unique**, which makes unalignable rows read as differences, and **non-deterministic columns** that differ between two runs by design. Query `ETL_FAILURES` to see the differing rows.

For a unit converted to a Snowflake task graph, a single unresolvable write target is omitted from the table list instead of skipping the unit, so the graph still gets executed and validated. Asserting that every task succeeded is a meaningful check on its own.

Tip

While you iterate on a Snowflake task graph, `--skip-ssis-execution` skips launching the source package. Only the task graph check and the table comparison run, against whatever is already in the source tables, so those tables must already hold the source-side result for the comparison to be meaningful. The flag also skips isolation and the local dbt target, so it doesn’t help when iterating on a dbt project.

## Prerequisites

Before validation runs, make sure:

- The converted pipeline is **deployed** to Snowflake, and a test definition exists for the unit.
- SQL Server is **live and reachable**, since the original package has to run to produce the reference rows.
- A source connection to SQL Server is configured, and a Snowflake connection for the converted side.
- The source login can launch the package with the method in its test definition, and both sides hold the isolation privileges.

| Purpose | Needs |
| --- | --- |
| Launch through `agent_job` | Read access to the SQL Agent job and job-history tables in `msdb`, and permission to start a job. Auto-creating the job also needs permission to add a job, a job step, and a job server; in practice, membership in a SQL Agent role such as `SQLAgentUserRole`. Pre-create the job and name it in `job_name` if you’d rather not grant that. |
| Launch through `ssisdb_catalog` | A Windows Authentication login, read access to the SSISDB catalog views, and permission to run its execution procedures. |
| Isolation on SQL Server | `CREATE TABLE` on the database, and `ALTER`, `SELECT`, `INSERT`, and `DELETE` on each schema involved, to create, populate, and drop the run-scoped backup tables. |
| Isolation on Snowflake | `CREATE TABLE` on each schema in the write-set, for the backup clones, and `SELECT`, `INSERT`, and `DELETE` on each table in it. `OWNERSHIP` satisfies these. |

Expand

Show lessSee more

For example, to grant the isolation privileges:

Copy code

```
-- SQL Server
GRANT CREATE TABLE TO <LOGIN>;
GRANT ALTER, SELECT, INSERT, DELETE ON SCHEMA::<SCHEMA> TO <LOGIN>;
```

Copy code

```
-- Snowflake
GRANT CREATE TABLE ON SCHEMA sales_db.dbo TO ROLE etl_tester;
GRANT SELECT, INSERT, DELETE ON ALL TABLES IN SCHEMA sales_db.dbo TO ROLE etl_tester;
```

## Troubleshooting

### Run fails: SSISDB catalog has no project containing the package

If the package is deployed to MSDB, the test definition is missing `package_store: msdb`, so the run looked for it in SSISDB. Re-run `scai test seed` with a SQL Server source connection, or add `package_store: msdb` and `folder` to `execution.source`. The error suggests setting `folder` and `project`, but that only helps for an SSISDB package. If the package really is in SSISDB, check that it’s deployed under that name.

### Run fails: MSDB package requires an explicit folder

The test definition says `package_store: msdb` but has no `folder`, which happens when the package is in the MSDB root folder. Add the `folder` if the package is in a named folder; otherwise set `job_name` to a SQL Agent job that runs the package.

### Error 27123: SSISDB catalog rejects the login

The test definition uses `ssisdb_catalog` with a SQL Server Authentication login. Switch to `agent_job`, or connect with Windows Authentication.

### Unit refused: isolation privileges unavailable

The warning before the refusal names each missing privilege. Grant the privileges listed in [Prerequisites](#prerequisites) and validate again.

### Differences on every run

Check for non-deterministic columns, such as identity values and `GETDATE()` or `NEWID()` results, that weren’t excluded, and verify that the join key is actually unique.

### Hand edits lost after re-seeding

`--append` regenerates the `execution` block. Re-apply edits to `method`, `folder`, `job_name`, `package_store`, or `parameters`.

### Placeholder in the test definition

`TODO_ETL_PROJECT_DIR` means the package has several dbt projects and no task graph, so the seeder couldn’t pick one. Set `project_dir`, or convert with `--consolidate-dbt-projects`.

## Related content

- [Testing Informatica PowerCenter pipelines](/migrations/aim-for-datawarehouses/testing/etl-pipelines/informatica): the same flow for Informatica.
- [Testing stored procedures and UDFs](/migrations/aim-for-datawarehouses/testing/sprocs-and-udfs): the capture, validate, and fix-loop flow for procedures.
- [Testing overview](/migrations/aim-for-datawarehouses/testing/overview): strategies and when to use each.
- [SnowConvert AI CLI ETL migration](/migrations/aim-for-datawarehouses/manual-migration/etl-migration): how SSIS packages are converted.
- [Command reference](/migrations/aim-for-datawarehouses/manual-migration/SCAI_Command_Reference): the full `scai test seed` and `scai test etl-validate` option lists.
