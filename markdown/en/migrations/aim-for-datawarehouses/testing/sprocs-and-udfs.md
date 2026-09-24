# Testing stored procedures and UDFs

This page describes how the Snowflake AIM Agent for Data Warehouses tests a converted stored procedure or UDF for behavioral equivalence with its source counterpart. For strategy selection (source-data vs testbed), see [Testing overview](/migrations/aim-for-datawarehouses/testing/overview).

Testing runs inside the migrate-objects loop. After a procedure or function is deployed to Snowflake, it goes through a **deploy → test → fix** cycle and is only marked complete once its output matches the source-side baseline (or you choose to skip it).

## The testing pipeline

For each object, the Snowflake AIM Agent for Data Warehouses drives three underlying commands:

| Command | Role |
| --- | --- |
| `scai test seed` | Scaffolds the object’s test definition (a YAML file) and populates its test cases — from a query-log CSV, from the source database, or synthesized from the source SQL. |
| `scai test capture` | Executes the object on the **source** database and records the expected output as a baseline. Baselines are uploaded to Snowflake, so the framework can compare against them repeatedly while you iterate on a fix — without re-querying the source. |
| `scai test validate` | Executes the converted object on Snowflake and compares its output against the captured baseline. |

Expand

Show lessSee more

You normally don’t invoke these directly — you drive them conversationally, for example:

```
"Capture baselines for dbo.GetCustomerOrders"
"Deploy and test the next procedure"
```

### Two-sided comparison

The framework runs the object on both sides and compares results:

- **Source side (capture):** the original procedure runs against your source database. Its result sets, output parameters, and table changes become the baseline.
- **Snowflake side (validate):** the converted procedure runs against a fresh, isolated clone of the workload database. Its output is compared to the baseline.

The comparison handles the cases that make procedure testing hard:

- Procedures that return **multiple result sets**.
- Procedures that use **OUTPUT / INOUT parameters**.
- Procedures that **modify tables** (DML) — the framework compares the *table changes*, not just a return value.

## Where test cases live

Each object’s tests are stored as a YAML file in the project:

```
artifacts/<database>/<schema>/<object_type>/<sanitized_name>/test/<sanitized_name>.yml
```

The file has two parts:

- **`steps`** — the sequence of setup, call, and assertion statements, in both the source dialect and Snowflake SQL. This block is written by `scai test seed`; you don’t hand-author it.
- **`test_cases`** — the inputs each run exercises. These are populated from query logs, from synthesized analysis, or a mix.

Baselines are uploaded to the Snowflake stage `@SNOWCONVERT_AI.TESTING.BASELINES`; no copy is kept on your machine (so source data stays within your Snowflake account). Test outcomes are written to `SNOWCONVERT_AI.TESTING.RESULTS` and surfaced through reporting views for later review.

## Reading test results

Each test case resolves to one of the following statuses:

| Status | Meaning |
| --- | --- |
| `PASS` | Snowflake output matches the source baseline. |
| `FAIL` | Snowflake output differs from the baseline. |
| `ERROR` | The object raised an exception during execution. |
| `NO_BASELINE` | No captured baseline exists yet for this test case — run capture first. |

Expand

Show lessSee more

## The fix loop

When a test does not pass, the Snowflake AIM Agent for Data Warehouses distinguishes two kinds of failure before attempting any change:

- **Dependency failure.** The error points to a missing object (an unmigrated table, view, function, or procedure). The SQL isn’t broken — a prerequisite hasn’t been migrated yet. The agent reports the specific dependency and moves on; testing resumes once that object is deployed and passing.
- **Conversion failure.** The converted SQL itself is wrong. The agent applies known migration rules, patches the code, re-runs only the failed cases, and repeats until they pass or you decide to skip the object.

Because baselines are stored in Snowflake, each fix iteration re-validates against the same expected output without re-querying the source.

Tip

Fixes you make can be captured as reusable rules and propagated across the project, so the same correction applies automatically to other objects. See the rule engine in the [Snowflake AIM Agent for Data Warehouses overview](/migrations/aim-for-datawarehouses/overview).

## Prerequisites

Before testing runs, make sure:

- The object’s **source SQL body** and the DDL of its referenced tables/views are in the project (extracted from the source or imported).
- The converted object is **deployed** to Snowflake.
- Your Snowflake role and source login hold the required privileges. The Snowflake AIM Agent for Data Warehouses checks these when you opt into testing and surfaces the exact grants to apply if anything is missing. See [Considerations by source dialect](/migrations/aim-for-datawarehouses/testing/considerations-by-dialect).

## Related content

- [Testing overview](/migrations/aim-for-datawarehouses/testing/overview) — strategies and when to use each.
- [Synthetic testbed generator](/migrations/aim-for-datawarehouses/testing/synthetic-testbed-generator): constraint-aware table data and a query log for capture and validate.
- [Considerations by source dialect](/migrations/aim-for-datawarehouses/testing/considerations-by-dialect) — isolation model and permissions per dialect.
