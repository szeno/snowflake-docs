# Testing overview

Testing verifies that a converted **stored procedure or UDF** behaves the same on Snowflake as it did on the source system. For each object, the Snowflake AIM Agent for Data Warehouses runs it on your source database (**capture**) and on Snowflake (**validate**), then compares the output. Any mismatch drives an automated fix loop until the two sides agree.

Testing is part of the migrate-objects stage: after a procedure or function deploys, it is tested against a source-side baseline before it is considered done. This page explains the testing strategies available today and how to pick one based on the access you have. For the mechanics of the capture/validate/fix loop, see [Testing stored procedures and UDFs](/migrations/aim-for-datawarehouses/testing/sprocs-and-udfs). For per-dialect isolation and permissions, see [Considerations by source dialect](/migrations/aim-for-datawarehouses/testing/considerations-by-dialect).

Note

Testing covers **stored procedures and UDFs**. Whole-table and whole-schema data comparison is a separate feature — see [Data Validation](/migrations/aim-for-datawarehouses/data-migration-validation/data-validation). Testing of ETL pipelines (SSIS, Informatica) is on the roadmap.

## How testing works

The Snowflake AIM Agent for Data Warehouses orchestrates a three-step pipeline for each object:

| Step | What happens |
| --- | --- |
| **Seed** | Scaffold a test definition (a YAML file) for the object and populate its test cases — from real query logs, from the source database, or synthesized from the source SQL. |
| **Capture** | Execute the object on the **source** database to record the expected output (the baseline). Baselines are uploaded to Snowflake and reused across fix iterations. |
| **Validate** | Execute the converted object on Snowflake and compare its output against the captured baseline. Mismatches trigger the fix loop. |

Expand

Show lessSee more

Two properties matter for choosing a strategy:

- **The source database is the reference.** Whatever the source procedure produces is treated as correct; the goal is to make Snowflake match it. Establishing a baseline requires the Snowflake AIM Agent for Data Warehouses to execute the object against a **live source connection**.
- **Tests are isolated.** On the Snowflake side, each run executes against a fresh zero-copy clone of the workload database, so tests never mutate your real data. The source side uses transaction, snapshot, or backup-and-restore isolation depending on the dialect. See [Considerations by source dialect](/migrations/aim-for-datawarehouses/testing/considerations-by-dialect).

## Choosing a testing strategy

Two independent things determine how an object is tested. The Snowflake AIM Agent for Data Warehouses settles the first once per project (Q1) and the second per object.

### 1. Test data — the rows the procedure runs against

Set once for the project:

- **Representative source data? Yes → source data.** The procedure runs against the real rows already in your source database. No data is fabricated or inserted.
- **No → synthetic data.** The framework generates and inserts a minimal synthetic dataset (seed rows) derived from the source SQL, so logic can be exercised even when the source has no representative data.

These are mutually exclusive: **synthetic seed rows are inserted only in synthetic-data mode.** In source-data mode, tests always run against your real source rows.

### 2. Test-case inputs — the parameter values each procedure is called with

Decided per object, based on whether that object has query-log coverage:

- **From query logs.** If you provide an execution-log CSV, each procedure that appears in it is seeded with the **real parameter values** from those recorded calls.
- **Synthesized.** Any code unit **without** query-log coverage gets test cases generated from a static analysis of the source SQL — branch coverage, edge cases, and boundary values — mixed with real values sampled from the source when it’s reachable.

So synthetic test-case generation is **not** limited to synthetic-data mode: it fills in inputs for any object your query logs don’t cover, even when you’re testing against real source data. Objects that *are* covered by the logs use those logged inputs as-is.

### Strategy matrix

All strategies require the object’s **source SQL** (the `CREATE PROCEDURE` / `CREATE FUNCTION` body plus the DDL of the tables and views it references) and a **live source connection** for baseline capture.

| Strategy | Representative source data | Query logs | What the agent does | Fidelity |
| --- | --- | --- | --- | --- |
| **Source data — query-log inputs** | ✅ | ✅ | Seeds `test_cases` from the real parameter values in your execution-log CSV, then captures baselines against the live source. Applies per object — procedures the log doesn’t cover fall back to synthesized inputs. | **Highest** — real data with real-world inputs. |
| **Source data — synthesized inputs** | ✅ | ❌ | Generates `test_cases` from source-SQL analysis (branches, edge cases, boundaries), mixed with real values sampled from the source, then captures baselines against the live source. Used when you have no logs — or for any object a log doesn’t cover. | High — real data drives common paths; synthesized cases add coverage. |
| **Synthetic data — synthesized inputs** | ❌ | — | Generates and inserts a minimal synthetic dataset from source-SQL analysis, along with synthesized `test_cases`, then captures baselines against the live source. | Good — proves semantic equivalence; business fidelity depends on the generated data and cases. |

Expand

Show lessSee more

Tip

You can mix approaches. By default, objects covered by your query logs use those logged inputs as-is. Even so, if you ask, the agent can add synthesized cases for branches the logs don’t cover — logs give business fidelity, synthesis gives coverage.

### When you can’t reach the source

Every strategy above needs a live source connection to capture baselines, because the source is the reference. Consequences to plan for:

- **No source connectivity → no baseline.** Capture baselines while the source is still reachable, ideally before decommissioning it.
- **Read-only / limited source access.** Read-only procedures can still be tested. Procedures that write data (DML) require the framework to isolate their side effects; on some dialects this needs elevated source privileges (for example, snapshot isolation or a parent database with `CREATE DATABASE` rights). See [Considerations by source dialect](/migrations/aim-for-datawarehouses/testing/considerations-by-dialect).

Note

**Coming soon — synthetic test bed.** A future capability will generate a coherent, constraint-aware synthetic dataset (and eventually a source-engine stand-in) so procedures can be tested without a live source connection at all. This is not available today; when there is no source access, there is currently no baseline path.

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
- [Considerations by source dialect](/migrations/aim-for-datawarehouses/testing/considerations-by-dialect) — isolation model and permissions per dialect.
- [Data Validation](/migrations/aim-for-datawarehouses/data-migration-validation/data-validation) — whole-table data comparison after migration.
