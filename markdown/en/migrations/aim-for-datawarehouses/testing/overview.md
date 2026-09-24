# Testing overview

Testing verifies that a converted **stored procedure or UDF** behaves the same on Snowflake as it did on the source system. For each object, the Snowflake AIM Agent for Data Warehouses runs it on your source database (**capture**) and on Snowflake (**validate**), then compares the output. Any mismatch drives an automated fix loop until the two sides agree.

Testing is part of the migrate-objects stage: after a procedure or function deploys, it is tested against a source-side baseline before it is considered done. This page explains the testing strategies available today and how to pick one based on the access you have. For the mechanics of the capture/validate/fix loop, see [Testing stored procedures and UDFs](/migrations/aim-for-datawarehouses/testing/sprocs-and-udfs). For per-dialect isolation and permissions, see [Considerations by source dialect](/migrations/aim-for-datawarehouses/testing/considerations-by-dialect).

Note

Testing covers **stored procedures and UDFs**. Whole-table and whole-schema data comparison is a separate feature — see [Data Validation](/migrations/aim-for-datawarehouses/data-migration-validation/data-validation). Testing of ETL pipelines (SSIS, Informatica) is on the roadmap.

## How testing works

The Snowflake AIM Agent for Data Warehouses orchestrates a three-step pipeline for each object:

| Step | What happens |
| --- | --- |
| **Seed** | Scaffold a test definition (a YAML file) for the object and populate its test cases: from a customer query-log CSV, from a generated query log on the testbed path, from the source database, or synthesized from the source SQL. |
| **Capture** | Execute the object on the **source** database to record the expected output (the baseline). Baselines are uploaded to Snowflake and reused across fix iterations. |
| **Validate** | Execute the converted object on Snowflake and compare its output against the captured baseline. Mismatches trigger the fix loop. |

Expand

Show lessSee more

Two properties matter for choosing a strategy:

- **The source database is the reference.** Whatever the source procedure produces is treated as correct; the goal is to make Snowflake match it. Establishing a baseline requires the Snowflake AIM Agent for Data Warehouses to execute the object against a **live source connection**.
- **Tests are isolated.** On the Snowflake side, each run executes against a fresh zero-copy clone of the workload database, so tests never mutate your real data. The source side uses transaction, snapshot, or backup-and-restore isolation depending on the dialect. See [Considerations by source dialect](/migrations/aim-for-datawarehouses/testing/considerations-by-dialect).

## Choosing a testing strategy

Two independent things determine how an object is tested. The Snowflake AIM Agent for Data Warehouses asks once per project whether the source has representative production-like data. That choice is **source-data tests** or **testbed tests**. Test-case inputs are decided per object from that path.

### 1. Test data: the rows the procedure runs against

Set once for the project:

- **Representative source data? Yes → source-data tests.** The procedure runs against the real rows already in your source database. No data is fabricated or inserted.
- **No → generate a testbed.** The [synthetic testbed generator](/migrations/aim-for-datawarehouses/testing/synthetic-testbed-generator) builds constraint-aware table data and a query log (FK-safe rows that respect types, nullability, and procedure branches) so logic can be exercised when source data is unavailable for testing. The Snowflake AIM Agent for Data Warehouses generates and loads that testbed for you; you do not start a separate generator step. Load **replaces rows** in those source tables: use an isolated source you can overwrite. A live source connection is still required for baselines.

These are mutually exclusive: **generated rows are loaded only on the testbed path.** In source-data mode, tests always run against your real source rows.

### 2. Test-case inputs: the parameter values each procedure is called with

How inputs are chosen depends on the path you picked:

- **Source-data path.** If you provide a query-log CSV, each procedure that appears in it is seeded with the **real parameter values** from those recorded calls. Any code unit **without** log coverage gets test cases generated from a static analysis of the source SQL (branch coverage, edge cases, and boundary values), mixed with real values sampled from the source when it’s reachable.
- **Testbed path.** You are not asked for a customer query-log CSV. Seed uses the **generated query log** (and querying the loaded catalog). Extra cases can still be synthesized from source SQL for objects that need more coverage.

On the source-data path, synthesized test-case generation still fills in inputs for any object your query logs don’t cover.

### Strategy matrix

All strategies require the object’s **source SQL** (the `CREATE PROCEDURE` / `CREATE FUNCTION` body plus the DDL of the tables and views it references) and a **live source connection** for baseline capture.

| Strategy | Representative source data | Query logs | What the Snowflake AIM Agent for Data Warehouses does | Fidelity |
| --- | --- | --- | --- | --- |
| **Source data: query-log inputs** | ✅ | ✅ | Seeds `test_cases` from the real parameter values in your execution-log CSV, then captures baselines against the live source. Applies per object. Procedures the log doesn’t cover fall back to synthesized inputs. | **Highest**: real data with real-world inputs. |
| **Source data: synthesized inputs** | ✅ | ❌ | Generates `test_cases` from source-SQL analysis (branches, edge cases, boundaries), mixed with real values sampled from the source, then captures baselines against the live source. Used when you have no logs, or for any object a log doesn’t cover. | High: real data drives common paths; synthesized cases add coverage. |
| **Testbed: generated data and query log** | ❌ | generated | Runs the [synthetic testbed generator](/migrations/aim-for-datawarehouses/testing/synthetic-testbed-generator) to produce and load constraint-aware table data and a synthetic query log, then captures baselines against the live source. | Good: proves semantic equivalence; business fidelity depends on the generated data and cases. |

Expand

Show lessSee more

Tip

On the source-data path you can mix approaches. By default, objects covered by your query logs use those logged inputs as-is. Even so, if you ask, the Snowflake AIM Agent for Data Warehouses can add synthesized cases for branches the logs don’t cover: logs give business fidelity, synthesis gives coverage.

### When you can’t reach the source

Every strategy above needs a live source connection to capture baselines, because the source is the reference. Consequences to plan for:

- **No source connectivity → no baseline.** Capture baselines while the source is still reachable, ideally before decommissioning it.
- **Read-only / limited source access.** Read-only procedures can still be tested. Procedures that write data (DML) require the framework to isolate their side effects; on some dialects this needs elevated source privileges (for example, snapshot isolation or a parent database with `CREATE DATABASE` rights). See [Considerations by source dialect](/migrations/aim-for-datawarehouses/testing/considerations-by-dialect).

Note

**A testbed still needs a live source.** The [synthetic testbed generator](/migrations/aim-for-datawarehouses/testing/synthetic-testbed-generator) simulates production data; it does not replace source access. When there is no source connectivity, there is no baseline path.

## Supported source dialects

| Dialect | Capture | Validate | Notes |
| --- | --- | --- | --- |
| SQL Server | ✅ | ✅ | Transaction or snapshot isolation on the source; DML procedures need snapshot isolation enabled. |
| Amazon Redshift | ✅ | ✅ | Transaction-based source isolation. |
| Teradata | ✅ | ✅ | Backup-and-restore source isolation; requires a parent database with `CREATE DATABASE` rights. Supports BTEQ scripts. |
| Oracle | ✅ | ✅ | `SAVEPOINT`-based source isolation. Procedures containing `COMMIT` (DML) are not yet supported. |
| PostgreSQL | ❌ | ❌ | Not yet supported for procedure/UDF testing. PostgreSQL data validation is separate — see [Data Validation](/migrations/aim-for-datawarehouses/data-migration-validation/data-validation). |

Expand

Show lessSee more

## Related content

- [Testing stored procedures and UDFs](/migrations/aim-for-datawarehouses/testing/sprocs-and-udfs) — the capture/validate/fix-loop flow and test-definition shape.
- [Synthetic testbed generator](/migrations/aim-for-datawarehouses/testing/synthetic-testbed-generator): constraint-aware table data and a query log when the source has no representative rows.
- [Considerations by source dialect](/migrations/aim-for-datawarehouses/testing/considerations-by-dialect) — isolation model and permissions per dialect.
- [Data Validation](/migrations/aim-for-datawarehouses/data-migration-validation/data-validation) — whole-table data comparison after migration.
