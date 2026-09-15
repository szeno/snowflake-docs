# Snowflake AIM Agent for Data Warehouses - Code Conversion

**Code conversion** is the stage of a migration that turns your source-platform logic — table and view DDL, stored procedures, functions, and scripts — into **Snowflake SQL** and the matching Snowflake objects, so you can deploy, test, and run the workload on Snowflake.

This page explains why conversion is necessary, why getting it right matters, and how the Snowflake AIM Agent for Data Warehouses does it — including the **AI-assisted remediation** that repairs code the deterministic pass can’t translate on its own. For the source systems and capabilities supported today, see the [code conversion support matrix](/migrations/aim-for-datawarehouses/overview#supported-source-systems). The object- and dialect-specific details live in the pages linked at the end.

## Why convert code?

A data warehouse is more than its data. Your source system (SQL Server, Redshift, Teradata, Oracle, and others) also holds the *logic* that shapes that data: DDL that defines tables and views, and procedural code — stored procedures and functions — written in a source-specific SQL dialect such as T-SQL or Redshift SQL.

For SAS sources, code conversion uses an AI-based approach rather than the deterministic layer described below — see [SAS Migration](/migrations/aim-for-datawarehouses/sas-migration).

Snowflake does not run those dialects. If you move only the data, the tables land but nothing that operated on them works: procedures don’t compile, functions don’t resolve, and views break. To migrate a workload you have to translate that logic into Snowflake SQL and recreate the equivalent Snowflake objects. That translation is code conversion.

## Why getting conversion right matters

Converted code is not finished when it compiles — it is finished when it produces the **same results as the source**. A procedure that runs but returns different numbers is more dangerous than one that fails outright, because the error is silent and flows downstream into reports and pipelines.

Correctness is hard because dialect differences are subtle. Data-type mapping, NULL handling, implicit casts, date and time arithmetic, transaction semantics, and dynamic SQL all differ between platforms, and small mistranslations compound. This is why the Snowflake AIM Agent for Data Warehouses pairs **deterministic conversion** — repeatable, high-fidelity translation — with **[two-sided testing](/migrations/aim-for-datawarehouses/testing/overview)** that compares source output against Snowflake output. Correctness is verified, not assumed.

## How the Snowflake AIM Agent for Data Warehouses converts code

The Snowflake AIM Agent for Data Warehouses (the Snowflake AIM Agent, running in [Snowflake CoCo](/user-guide/cortex-code/cortex-code)) drives conversion for you. Conversion is **Stage 4 (Convert)** of the guided migration workflow, and it runs in two layers:

| Layer | What happens |
| --- | --- |
| **Deterministic first** | SnowConvert applies repeatable, grammar-based translation to your source SQL. The same input always produces the same output, giving you a high-fidelity baseline instead of a best-effort rewrite. Most straightforward DDL and logic converts cleanly here. |
| **AI second** | When the deterministic pass leaves an unresolved issue or hits a construct with no direct equivalent, AI explains the issue in context, proposes a fix, and applies it interactively against the same converted code. |

Expand

Show lessSee more

To understand what needs conversion and where the risks are, run an **[assessment](/migrations/aim-for-datawarehouses/assessment)** with the Snowflake AIM Agent for Data Warehouses first. It categorizes your source objects, scores conversion complexity, flags dynamic SQL, and produces an interactive report you can review before you convert. After conversion, the agent presents a per-object summary and highlights objects that need manual review, and recurring fixes can be captured as **reusable rules** and propagated across the project so the same issue is not fixed by hand more than once. For the full taxonomy of Errors, Warnings, and Issues (EWIs) behind those results, see [Issues and troubleshooting](/migrations/aim-for-datawarehouses/code-conversion/issues-and-troubleshooting/README).

You don’t need to memorize commands — the guided flow reaches the Convert stage on its own, or you can ask directly:

Copy code

```
"Convert my source code"
```

For the full end-to-end workflow, prerequisites, supported source systems, and example prompts, see the [Snowflake AIM Agent for Data Warehouses overview](/migrations/aim-for-datawarehouses/overview).

The agent installs its own tooling (SnowConvert, `uv`, ODBC drivers, and Python packages) automatically the first time it runs — you don’t install these yourself. If Snowflake CoCo or that tooling isn’t set up, or the skill doesn’t trigger, see [Troubleshooting](/migrations/aim-for-datawarehouses/troubleshooting) to get unblocked.

## Conversion details

Once you understand the general workflow, use these pages for the object- and dialect-specific behavior:

- **[Translation references](/migrations/aim-for-datawarehouses/code-conversion/translation-references/transact/README)** — how each source dialect maps to Snowflake, including DDL, [CREATE FUNCTION](/migrations/aim-for-datawarehouses/code-conversion/translation-references/transact/transact-create-function), and stored procedures ([Snowflake Scripting](/migrations/aim-for-datawarehouses/code-conversion/translation-references/transact/transact-create-procedure-snow-script)).
- **[Function references](/migrations/aim-for-datawarehouses/code-conversion/function-references/udfs)** — the helper UDFs SnowConvert emits to reproduce source built-in behavior.
- **[Issues and troubleshooting](/migrations/aim-for-datawarehouses/code-conversion/issues-and-troubleshooting/README)** — the EWI taxonomy, [conversion issues](/migrations/aim-for-datawarehouses/code-conversion/issues-and-troubleshooting/conversion-issues/README), [functional differences](/migrations/aim-for-datawarehouses/code-conversion/issues-and-troubleshooting/functional-difference/README), and performance review.
- **[Teradata considerations](/migrations/aim-for-datawarehouses/code-conversion/considerations-teradata)** — dialect-specific guidance for Teradata sources.
- **[Troubleshooting](/migrations/aim-for-datawarehouses/troubleshooting)** — what to do when the agent or its tooling isn’t installed, the skill doesn’t trigger, or setup fails.
