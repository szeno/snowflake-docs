# SnowConvert AI CLI - ETL Migration

SnowConvert AI CLI migrates ETL sources to Snowflake alongside your database code. Two ETL platforms are supported:

- **SSIS** — SQL Server Integration Services packages (`.dtsx`).
- **Informatica** — Informatica PowerCenter repository exports (XML).

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. Informatica PowerCenter migration is in preview; SSIS migration is generally available.

ETL migration is not a separate command. SnowConvert converts ETL sources through the same [`scai code convert`](./SCAI_Command_Reference) command used for database code. SnowConvert detects the ETL platform from the files in your project’s `source/` directory — SSIS from `.dtsx` packages and Informatica from PowerCenter XML — so there is no source-type flag to set. The flags below control the shape of the generated output.

## How ETL conversion works

This page assumes you already have a SnowConvert project that contains your ETL sources. See [What is SnowConvert AI CLI?](./README) for how to create a project and add source files.

Run the conversion from the project root:

Copy code

```
scai code convert
```

By default, each detected ETL source is converted to a **dbt project**, and the converted output is written to the project’s `snowflake/_etl/` directory. The flags in the following sections change the target output format or how the generated files are organized.

## Target output formats by platform

The default output format for both platforms is a dbt project. Flags redirect the output to an alternative format:

| Source | Default output format | Flag to change format | Resulting output format |
| --- | --- | --- | --- |
| **SSIS** | dbt project | `--simplify-ssis-dataflows` | Inline Snowflake SQL (simple data flows only) |
| **Informatica** | dbt project | `--informatica-to-snowflake-scripting` | Snowflake Scripting stored procedures |

Expand

Show lessSee more

A **dbt project** output is a set of `.sql` model files under `models/` — staging models (`stg_*`) that read the sources, intermediate models (`int_*`) for each transformation, and mart models for the targets — chained together with dbt `ref()` references.

When Informatica is converted to dbt (the default), you can add the `--consolidate-dbt-model-chains` flag (described in [Conversion flags](#conversion-flags)) to reduce the number of generated model files.

When either platform is converted to dbt, the `--consolidate-dbt-projects` and `--consolidate-as-single-dbt-project` flags change how many dbt projects you get. See [Choosing a dbt project layout](#choosing-a-dbt-project-layout).

## Conversion flags

All flags below are optional and off by default. They appear in `scai code convert --help` for any source dialect but take effect only when the project actually contains the matching ETL source.

### `--simplify-ssis-dataflows`

**What it does.** By default, each SSIS data flow is converted to a dbt project (one model per transformation). With this flag, a **simple** data flow is converted to a single inline Snowflake SQL statement instead. Complex data flows are unaffected and still become dbt projects.

A data flow counts as *simple* only when **both** conditions hold:

- It has **10 or fewer** transformations, and
- It uses **only** these transformation types: Sources, Targets, Derived Column, Row Count, and Conditional Split.

Any other transformation type (for example Aggregate, Lookup, Pivot) disqualifies the flow, which then falls back to a dbt project.

**Expected result.** For qualifying flows you get compact inline SQL rather than a folder of small dbt model files. Non-qualifying flows in the same package still produce dbt projects.

**When to use it.** Turn it on when your packages contain many trivial, straight-through data flows and you prefer concise SQL over a proliferation of tiny model files.

Copy code

```
scai code convert --simplify-ssis-dataflows
```

### `--informatica-to-snowflake-scripting`

**What it does.** By default, Informatica mappings are converted to dbt projects. With this flag, mappings are converted to **Snowflake Scripting stored procedures** instead — imperative SQL procedures that materialize each transformation step in sequence.

**Expected result.** Instead of a dbt `models/` folder, you get `CREATE PROCEDURE` scripts that run the mapping’s logic procedurally. Any transformation the engine cannot translate inline is emitted with a placeholder and an EWI (Error, Warning, or Information message) so you can review it.

**When to use it.** Choose scripting when the target team prefers native Snowflake stored procedures / procedural pipelines over a dbt project. Keep the default (dbt) when you want declarative, testable, `ref()`-linked models.

Copy code

```
scai code convert --informatica-to-snowflake-scripting
```

### `--consolidate-dbt-model-chains`

**What it does.** Applies only to the Informatica → dbt path (that is, when `--informatica-to-snowflake-scripting` is **not** set). It merges chained dbt models so a long linear chain of single-use intermediate models collapses into fewer, larger models.

**Expected result.** The same dbt project layout, but with fewer `.sql` files. It changes only how the output is organized, not the logic it implements.

**When to use it.** Use it for Informatica mappings with long transformation chains, when the un-consolidated output produces an unwieldy number of tiny intermediate models that are harder to review and maintain.

Copy code

```
scai code convert --consolidate-dbt-model-chains
```

### Choosing a dbt project layout

By default, each SSIS data flow and each Informatica mapping converts to its own dbt project. Two flags group that output into fewer projects. Use one of them, not both.

| Layout | Flag | SSIS output | Informatica output |
| --- | --- | --- | --- |
| One project per data flow or mapping | None (default) | One dbt project per data flow | One dbt project per mapping |
| One project per package or folder | `--consolidate-dbt-projects` | One dbt project per package | One dbt project per PowerCenter folder |
| One project for the whole workload | `--consolidate-as-single-dbt-project` | One dbt project for every package | One dbt project for every folder |

Expand

Show lessSee more

These flags change only dbt output. Don’t pass them for a platform that you convert to Snowflake Scripting.

#### `--consolidate-dbt-projects`

**What it does.** Groups SSIS dbt output into one dbt project per package instead of one per data flow, and Informatica PowerCenter dbt output into one dbt project per folder instead of one per mapping.

**Expected result.** Fewer dbt projects. In an Informatica folder project, each mapping’s models stay under `models/<mapping>/` and are tagged with the mapping name.

Copy code

```
scai code convert --consolidate-dbt-projects
```

#### `--consolidate-as-single-dbt-project`

**What it does.** Writes one dbt project, named `etl_dbt_project`, for the whole workload. It applies to SSIS packages and Informatica PowerCenter folders.

**Expected result.** A single dbt project. Models stay grouped inside it: SSIS models by package and data flow, and Informatica models by folder and mapping, under `models/<folder>/<mapping>/` and tagged `<folder>__<mapping>`.

**When to use it.** Use it when you want to deploy and run the whole ETL workload as one dbt project.

Copy code

```
scai code convert --consolidate-as-single-dbt-project
```

Note

When you convert with the [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview), it asks which dbt project layout you want before it converts, and passes the matching flag. It offers the single-project layout only when one platform, SSIS or Informatica, converts to dbt. When both platforms convert to dbt, you choose between the per-package-and-folder layout and the per-data-flow-and-mapping layout, and your answer applies to both.

## Ingesting non-standard Informatica exports

Note

`--informatica-bypass-workflow-validation` is a flag on **`scai code add`** (the step that adds source files to a project), not on `scai code convert`. It is experimental and off by default.

By default, `scai code add` validates that each Informatica PowerCenter XML file contains exactly one workflow and rejects files that do not conform. Pass `--informatica-bypass-workflow-validation` to accept **any** PowerCenter XML — for example partial exports, or files with zero or multiple workflows. Conversion of non-conforming files may produce unexpected results, so use this only as a fallback for non-standard exports.

Copy code

```
scai code add --informatica-bypass-workflow-validation
```

## Combining options

You can combine the ETL flags with general `scai code convert` options. For example, convert Informatica mappings to Snowflake Scripting and print the detailed EWI table:

Copy code

```
scai code convert --informatica-to-snowflake-scripting --show-ewis
```

General `scai code convert` flags — such as `--where`, `-x, --show-ewis`, `--context-path`, and `--overwrite-working-directory` — also apply to ETL conversions. Run `scai code convert --help` for the complete list, or see the [Command Reference](./SCAI_Command_Reference).

## Related

- [Assessment](/migrations/aim-for-datawarehouses/assessment) — SSIS package analysis before you migrate.
- [Informatica PowerCenter translation reference](/migrations/aim-for-datawarehouses/code-conversion/translation-references/informatica/README) — how PowerCenter elements map to Snowflake and dbt.
- [Command Reference](./SCAI_Command_Reference) — full `scai` command and flag list.
