# Testing Informatica PowerCenter pipelines

This page describes how the Snowflake AIM Agent for Data Warehouses tests a converted **Informatica PowerCenter** workflow for equivalence with the original. The original workflow runs on your PowerCenter domain through `pmcmd`, the converted pipeline runs on Snowflake, and the tables each one wrote are compared row by row. For stored procedures and UDFs, which use a different flow and a different comparison model, see [Testing stored procedures and UDFs](/migrations/aim-for-datawarehouses/testing/sprocs-and-udfs).

Testing runs inside the migrate-objects loop. After a workflow is stabilized and deployed to Snowflake, it goes through a **seed → validate → fix** cycle and is only marked complete once the tables it writes match the tables the original workflow writes (or you choose to skip it).

Note

A pipeline can’t be tested by calling it with inputs and diffing a return value, because a pipeline’s output **is** the data it lands. So the comparison is table-to-table, and both sides have to actually run.

## The testing pipeline

For each Informatica code unit, the Snowflake AIM Agent for Data Warehouses drives two underlying commands:

| Command | Role |
| --- | --- |
| `scai test seed` | Scaffolds the workflow’s test definition (a YAML file). It reads the pipeline’s **write** dependencies from the Code Unit Registry (every table the workflow inserts, updates, merges, or deletes) and emits one source-to-target table pair per written table. |
| `scai test etl-validate` | Runs both sides: launches the original workflow through `pmcmd`, runs the converted pipeline on Snowflake, then compares each table pair. |

Expand

Show lessSee more

You normally don’t invoke these directly. You drive them conversationally, for example:

```
"Seed the ETL test for wf_LoadSales"
"Validate the next Informatica workflow"
```

To run the validation yourself, name the registered [pmcmd connection](#the-pmcmd-connection):

Copy code

```
scai test etl-validate --platform informatica --informatica-connection my-infa
```

To validate a single workflow, add `--where "id = '<code-unit-id>'"`. To validate workflows in lineage order, add `--with-lineage`.

Before starting a comparison, the agent runs a pre-flight check, `scai test etl-validate --platform informatica --check-env`, which you can also run yourself before a long run. It confirms that:

- The Snowflake connection and the source database connection open.
- The `pmcmd` executable is found.
- The stored `pmcmd` credentials authenticate.
- The Integration Service and domain resolve for every seeded workflow.

It is much cheaper to find a missing value there than partway through a run.

### Two-sided comparison

The framework runs the pipeline on both sides and compares what each one wrote. For each workflow:

1. The tables in the workflow’s write-set are backed up on both sides. See [Isolation](#isolation).
2. **Source side:** the original workflow runs on your PowerCenter domain, started through `pmcmd` and polled until it finishes. The rows it lands in the source database are the reference.
3. **Snowflake side:** the converted pipeline runs as whatever it became. See [What runs the converted side](#what-runs-the-converted-side).
4. **Comparison:** each declared source table is compared against its Snowflake counterpart, row by row, aligned on a key you confirm.
5. Both sides are restored from their backups.

### Isolation

Because both sides write real tables, each run isolates the workflow’s **write-set**: every table the workflow writes, plus the compared source tables. The two sides are isolated independently, so a validation doesn’t leave either system permanently changed:

- **Source database:** the framework, not PowerCenter, copies each write-set table in the database the workflow writes to into a run-scoped backup table before the workflow starts, and restores it afterward. Source-side isolation is supported when that database is SQL Server or Teradata.
- **Snowflake:** each write-set table is backed up as a zero-copy clone, and the target tables are cleared before the converted pipeline runs. Afterward, the tables are restored from the clones, and any write-set table that the run created is dropped.

Isolation is on by default. If a required privilege on either side is missing, the unit is **refused** and reported as a failure that names the missing privilege; it doesn’t run unisolated. For the privileges, see [Prerequisites](#prerequisites).

To turn isolation off on purpose, set `etl_source_isolation_strategy: none` or `etl_target_isolation_strategy: none` in `.scai/settings/test_config.yaml`. The workflow’s writes then persist on that side.

Note

ETL isolation works at the table level. It doesn’t use the database-level clone that procedure testing uses, described in [Considerations by source dialect](/migrations/aim-for-datawarehouses/testing/considerations-by-dialect), so it doesn’t need `CREATE DATABASE ON ACCOUNT`.

### The pmcmd connection

Everything `pmcmd` needs is registered once as a named Informatica connection:

Copy code

```
scai connection add-informatica-pmcmd
```

It prompts for the path to the `pmcmd` executable, the repository user and password, the Integration Service name, the Informatica domain, optionally the path to a `domains.infa` file, and a name for the connection. The password is prompted for and hidden rather than taken as an argument. The Integration Service and domain are required, so the pre-flight can resolve them before anything launches.

Verify the connection:

Copy code

```
scai connection test -l informatica -s my-infa
```

The test pings the Integration Service through `pmcmd` and reads its details, so a wrong service name, domain, or credential surfaces here.

When you validate without `--informatica-connection`, the connection selected by the project configuration is used, and then your default Informatica connection. Registering a connection doesn’t make it the default; to set it, run `scai connection set-default -l informatica -s my-infa`. Registering under a name that already exists fails, so to change a connection’s values, remove it with `scai connection remove -l informatica -s my-infa` and register it again.

Warning

A registered connection stores the password in **cleartext**, in `~/.snowflake/scai/connections/informatica.toml`. A file at the earlier location, `~/.snowflake/snowct/informatica.toml`, is moved there automatically. Storing it there buys **scope**, not encryption: the secret sits in one file in your home directory instead of being spread across project files and shell history. Treat that file as a secret, keep it out of version control, and never pass the password as a command-line argument, where it lands in shell history and process listings. `scai connection list -l informatica` masks stored passwords, so its output is safe to paste into a ticket.

### What runs the converted side

A PowerCenter workflow doesn’t convert to one fixed shape. The seeder picks the Snowflake-side target from what the conversion produced, in this order:

| Target | When it’s used | What runs |
| --- | --- | --- |
| Local dbt project | The workflow converted to a dbt project. | Runs `dbt run` against the project on disk, using the `dbt` on your path. No external orchestrator is involved. |
| Snowflake task graph | The workflow converted to Snowflake tasks. | Executes the deployed root task and asserts every task succeeded. Task graphs are created **suspended**; activating them is a separate, deliberate step. |

Expand

Show lessSee more

This page covers workflows that converted to one of these two targets.

Caution

If you narrow a local dbt project’s model selector (`select`) by hand, keep it matching. `dbt` exits 0 when a selector matches nothing, so a stale selector makes the test **pass having built no models**, and the comparison then runs against whatever was already in the tables. Remove the selector entirely to build the whole project instead.

#### How conversion options affect testing

The flags passed to `scai code convert`, described in [SnowConvert AI CLI ETL migration](/migrations/aim-for-datawarehouses/manual-migration/etl-migration#conversion-flags), change what the Snowflake side contains:

- **Default:** each mapping converts to a dbt project, tested as a local dbt project.
- **`--consolidate-dbt-model-chains`:** produces fewer dbt model files in the same project. It doesn’t change the number of dbt projects, the logic, or how the workflow is tested.
- **`--informatica-to-snowflake-scripting`:** converts mappings to Snowflake Scripting stored procedures. A workflow that also converted to a Snowflake task graph is tested through the task graph. A workflow whose parts are all Snowflake Scripting procedures, with no task graph, can’t be tested yet; the seeder skips it with the reason `pending_format`.

## Where test cases live

Each workflow’s test is stored as a YAML file in the project:

```
artifacts/<code-unit-id>/etl-test/<name>.yml
```

The file has two parts, under a `kind: etl` header:

- **`pipeline`:** how to launch the source workflow (`source`) and which converted target to run (`target`). This block is written by `scai test seed`; you don’t hand-author it.
- **`validation`:** the `tables` list of source-to-target pairs to compare. The seeder fills in one pair for each table the workflow writes.

The seeder derives each workflow’s PowerCenter folder and workflow name from the conversion. Where it can’t, it writes the placeholders `TODO_INFA_FOLDER` and `TODO_INFA_WORKFLOW`: replace them with the values from the workflow you are validating. Connection details, such as the `pmcmd` path and credentials, are never written to this file; they come from the registered connection.

For example:

Copy code

```
# artifacts/wf_LoadSales/etl-test/wf_LoadSales.yml
kind: etl

pipeline:
  source:
    type: informatica_workflow
    method: pmcmd
    folder: Sales_Folder
    workflow: wf_LoadSales
  target:
    type: dbt_project
    project_dir: etl-target
    profile: Sales_Folder
    timeout_seconds: 1800

validation:
  tables:
    - source_table:
        name: SALES_DB.dbo.FactSales
        columns:
          mode: exclude
          list: [ETL_LOAD_TS, SURROGATE_KEY]
      target_table:
        name: ANALYTICS.PUBLIC.FACT_SALES
        columns:
          mode: exclude
          list: [ETL_LOAD_TS, SURROGATE_KEY]
      comparison:
        index_columns: [SalesOrderID, LineItemID]

    - source_table:
        name: SALES_DB.dbo.DimCustomer
      target_table:
        name: ANALYTICS.PUBLIC.DIM_CUSTOMER
      comparison:
        index_columns: [CustomerID]
```

**The join key is the most important decision you make.** `index_columns` names the column or columns that uniquely key a row; without it there is no way to align a source row with its Snowflake counterpart. The seeder fills it from the table’s primary key when the registry records one, and leaves it empty otherwise. The agent then proposes keys for each pair and asks you to confirm or correct them, because the registry can miss dynamically named or conditionally written tables. A good key:

- Uniquely identifies each row, like a primary key or a composite business key.
- Is present on both sides.
- Is stable across runs, not generated fresh each time the workflow runs.

Exclude non-deterministic columns, such as sequence-generated surrogate keys, load timestamps, audit columns, and ETL batch IDs, with `columns: {mode: exclude, list: [...]}` on the table entries, or they will differ on every run and hide real failures.

Re-seeding with `--append` regenerates the `pipeline` block and the list of table pairs from the current registry, and keeps each surviving pair’s `comparison` block, including the `index_columns` you entered. Recheck any other edits to a table entry, such as column exclusions, after re-seeding. The parser is strict: an unrecognized key anywhere in the file is a hard parse error, which catches a typo at parse time instead of halfway through a run.

Results are written to the `VALIDATION` schema of your results database in Snowflake (the `testing_results_database` set in `test_config.yaml`, or the `validation_database` if that isn’t set) and surfaced through reporting views for later review. See [Reading test results](#reading-test-results).

## Reading test results

Each compared table resolves to one of the following statuses:

| Status | Meaning |
| --- | --- |
| `PASS` | The Snowflake table matches the source table. |
| `FAIL` | The two tables differ. The result rows carry the differences. |
| `ERROR` | A side failed to execute: the workflow errored, the dbt run or task graph failed, or a table could not be read. The result row carries the error. |
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

- **Dependency failure.** The workflow’s write-set couldn’t be resolved, so the seeder **skips the unit with a named reason** rather than half-testing it: `no_write_dependencies` (no written tables recorded), `missing_dependency` (an unfinished upstream unit), `missing_canonical_name` (a table with no canonical name), or `pending_format` and `no_executable_entry_point` (converted parts not yet in a form the run can execute). The mapping isn’t broken; a prerequisite hasn’t been finished. The agent reports the specific cause and moves on.
- **Conversion failure.** The two tables genuinely differ, which points at a gap in the converted logic. The agent surfaces the failing tables and their row-level differences, patches the converted code, and re-runs.

Two causes account for most differences before you go looking at the converted logic: a **join key that isn’t actually unique**, which makes unalignable rows read as differences, and **non-deterministic columns** that differ between two runs by design. Query `ETL_FAILURES` to see the differing rows.

For a unit converted to a Snowflake task graph, a single unresolvable write target is omitted from the table list instead of skipping the unit, so the graph still gets executed and validated. Asserting that every task succeeded is a meaningful check on its own.

Tip

While you iterate on a Snowflake task graph, `--skip-ssis-execution` skips launching the PowerCenter workflow, despite its name. Only the task graph check and the table comparison run, against whatever is already in the source tables, so those tables must already hold the source-side result for the comparison to be meaningful. The flag also skips isolation and the local dbt target.

## Prerequisites

Before validation runs, make sure:

- The converted pipeline is **deployed** to Snowflake, and a test definition exists for the unit.
- The PowerCenter domain is **live and reachable**, since the original workflow has to run to produce the reference rows.
- `pmcmd` is installed on the machine running the validation, and an Informatica connection is registered with `scai connection add-informatica-pmcmd`. The repository user must be able to start workflows in the folder through the Integration Service.
- A source connection is configured for the database the workflow writes to, and a Snowflake connection for the converted side.
- Your roles hold the isolation privileges on both sides.

On Snowflake, the role needs `CREATE TABLE` on each schema in the write-set, for the backup clones, and `SELECT`, `INSERT`, and `DELETE` on each table in it. `OWNERSHIP` satisfies these:

Copy code

```
GRANT CREATE TABLE ON SCHEMA analytics.public TO ROLE etl_tester;
GRANT SELECT, INSERT, DELETE ON ALL TABLES IN SCHEMA analytics.public TO ROLE etl_tester;
```

On the source database, the login needs:

- **SQL Server:** `CREATE TABLE` on the database, and `ALTER`, `SELECT`, `INSERT`, and `DELETE` on each schema involved.

  Copy code

  ```
  GRANT CREATE TABLE TO <LOGIN>;
  GRANT ALTER, SELECT, INSERT, DELETE ON SCHEMA::<SCHEMA> TO <LOGIN>;
  ```
- **Teradata:** `CREATE TABLE`, `DROP TABLE`, `SELECT`, `INSERT`, and `DELETE` on each database involved.

The run checks these privileges when each unit starts, not in the pre-flight.

## Troubleshooting

### Pre-flight fails: pmcmd not found

Confirm that `pmcmd` is installed on the machine running the validation and that the path in the registered connection is correct. Run `which pmcmd` (Linux or macOS) or `where pmcmd` (Windows) to find it.

### Pre-flight fails: Integration Service, domain, or credentials

The values in your registered connection don’t match the running PowerCenter environment, or the password is wrong or expired. Run `scai connection test -l informatica -s my-infa` to see which value failed, then remove the connection and register it again with the corrected values.

### Unit refused: isolation privileges unavailable

Your role on Snowflake or on the source database is missing a privilege listed in [Prerequisites](#prerequisites). Grant it and validate again.

### Differences on every run

Check for non-deterministic columns that weren’t excluded, and verify that the join key is actually unique.

### dbt run passes but the comparison finds differences

If you narrowed the dbt model selector, dbt might have exited 0 without building anything, and the comparison then ran against stale data. Remove or correct the selector and validate again.

### Placeholders in the test definition

`TODO_INFA_FOLDER` or `TODO_INFA_WORKFLOW` means the seeder couldn’t derive the folder or workflow name. Replace the placeholders with the values from the workflow you are validating.

## Related content

- [Testing SSIS pipelines](/migrations/aim-for-datawarehouses/testing/etl-pipelines/ssis): the same flow for SSIS.
- [Testing stored procedures and UDFs](/migrations/aim-for-datawarehouses/testing/sprocs-and-udfs): the capture, validate, and fix-loop flow for procedures.
- [Testing overview](/migrations/aim-for-datawarehouses/testing/overview): strategies and when to use each.
- [SnowConvert AI CLI ETL migration](/migrations/aim-for-datawarehouses/manual-migration/etl-migration): how Informatica workflows are converted.
- [Command reference](/migrations/aim-for-datawarehouses/manual-migration/SCAI_Command_Reference): the full `scai test seed` and `scai test etl-validate` option lists.
