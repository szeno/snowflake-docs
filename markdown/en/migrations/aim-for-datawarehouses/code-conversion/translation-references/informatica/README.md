# Informatica PowerCenter

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for Informatica PowerCenter migrations.

Informatica PowerCenter is automatically converted to Snowflake. Your exported PowerCenter repository (the mappings, workflows, transformations, and expressions) is read and runnable Snowflake code is produced, so you can migrate data pipelines without rewriting them by hand.

This guide is the translation reference: it explains how each Informatica element maps to Snowflake, what the generated code looks like, and where to review manual follow-ups.

## How Informatica concepts map to Snowflake

The following table maps each Informatica concept to its Snowflake or dbt counterpart:

| Informatica PowerCenter | Snowflake / dbt | Description |
| --- | --- | --- |
| Workflow | [Task](/sql-reference/sql/create-task) graph | The orchestration order becomes a graph of Snowflake Tasks. |
| Session | Snowflake Task that runs a Mapping | Each Session runs its Mapping’s dbt project (or calls its procedure). |
| Worklet | Stored procedure | A reusable sub-workflow becomes a stored procedure the Task graph calls. |
| Mapping | dbt project or stored procedure | The data flow becomes a standalone dbt project of models **or** a Snowflake stored procedure (`public.m_<Mapping>`), depending on output format. |
| Transformation | dbt model or inline CTE / temp table | Each transformation becomes a SQL model **or** a CTE / temporary table inside the mapping procedure. |
| Mapplet | dbt macro or stored procedure | A reusable transformation group becomes a dbt macro **or** a result-set stored procedure (`<Folder>_<Def>_<8-hex>` on the Scripting path). |
| Source and Source Qualifier | Staging model or temporary table | Source reads become `stg_` staging models **or** `tmp_sq_<name>` temporary tables (flat-file Scripting reads `@public.landing_stage/infpc/sources/<Folder>/<Def>/`). |
| Target | Mart model or write statement | Targets become marts models **or** the mapping procedure’s `INSERT` / `COPY INTO @public.landing_stage/infpc/targets/<Def>/`. |
| Mapping and Workflow variables | `control_variables` table | Variables and parameters move to a runtime control table. |
| Expression function | Snowflake SQL function | Built-in functions convert to Snowflake equivalents. |

Expand

Show lessSee more

## Output formats

Two output formats are produced. The generated Snowflake code differs by format, so this guide documents each one separately:

| Output format | Status | What you get | Reference |
| --- | --- | --- | --- |
| **dbt project** | Generally available | Each Mapping becomes a dbt project; Workflows become Task graphs that run those projects. | [Informatica to dbt](dbt/README) |
| **Snowflake Scripting** | Preview, in active development | Each Mapping becomes a Snowflake stored procedure; Workflows call those procedures directly. | [Informatica to Snowflake Scripting](snowflake-scripting/README) |

Expand

Show lessSee more

Several references are shared across both output formats, because the orchestration and the generated Snowflake expressions are the same regardless of format:

- [Workflows and orchestration](workflows-and-orchestration): how Workflows become Snowflake Task graphs.
- [Variables and parameters](variables-and-parameters): the `control_variables` table, parameter files, and variable scope.
- [Expression functions](expression-functions): Informatica functions and their Snowflake equivalents.
- [Data types](data-types): how PowerCenter data types map to Snowflake types.

## Supported components at a glance

The tables below list the Informatica components that are recognized and which output formats support them today. Unlisted components generate an EWI code that flags the component for manual conversion.

### Mapping transformations (data flow)

| Transformation or element | dbt | Snowflake Scripting | Notes |
| --- | --- | --- | --- |
| Aggregator | Available | Available |  |
| Expression | Available | Available | Chained `LOCAL VARIABLE` lagger ports become `LAG`. |
| Filter | Available | Available |  |
| Java Transformation | Available | Available | XML `Custom Transformation` (`TEMPLATENAME=Java Transformation`). Pass-through CTE plus `SSC-FDM-INF0045`; the Java source isn’t applied. |
| Joiner | Available | Available |  |
| Lookup Procedure | Available | Available | XML `Lookup Procedure`. Covers connected lookups (including Use Any Value and Use All Values), unconnected lookups (as a hashed UDF), and flat-file lookups from `@public.landing_stage/infpc/sources/…`. |
| Mapplet | Available | Available | Scripting: procedure named `<Folder>_<Def>_<8-hex>`. A mapplet with more than one input or output emits `SSC-EWI-INF0001`; a mapplet with no input takes no scope. dbt: macro. |
| Normalizer | Available | Available |  |
| Rank | Available | Available |  |
| Router | Available | Available |  |
| Sequence | Available | Available | XML `Sequence Generator`. |
| Sorter | Available | Available |  |
| Source Definition | Available | Available | Metadata only; emits no SQL of its own. |
| Source Qualifier | Available | Available | Relational: temporary table. Scripting flat-file: reads from `@public.landing_stage/infpc/sources/<Folder>/<Def>/`. When a Source Qualifier has more than one associated source, the generated `FROM` uses only the first incoming source. |
| Stored Procedure | Available | Available | Connected Normal Stored Procedure emits a UDF CTE (`source_data` → `sp_result`) plus `SSC-EWI-INF0040`; this isn’t a Snowflake `CALL`. Disconnected or midstream Stored Procedure still emits `SSC-EWI-INF0001`. |
| Target Definition | Available | Available | Relational: `INSERT`. Scripting flat-file: `COPY INTO @public.landing_stage/infpc/targets/<Def>/`. |
| Union Transformation | Available | Available | XML `Union`. |
| Update Strategy | Available | Available | Unrecognized dispatch shapes fall back to the dbt output. |
| App Multi-Group Source Qualifier | Not yet available | Not yet available |  |
| Application Source Qualifier | Not yet available | Not yet available |  |
| Salesforce Lookup | Not yet available | Not yet available |  |
| SQL Transform | Not yet available | Not yet available | XML `Custom Transformation` (`TEMPLATENAME=SQL Transform`). |
| Transaction Control | Not yet available | Not yet available | `SSC-EWI-INF0001` placeholder. See [Mappings and transformations](snowflake-scripting/mappings-and-transformations) for the Transaction Control example. |
| XML Source Qualifier | Not yet available | Not yet available |  |

Expand

Show lessSee more

### Workflow elements (control flow)

| Element | dbt | Snowflake Scripting | Notes |
| --- | --- | --- | --- |
| ASSIGNMENT | Available | Available | See [Workflows and orchestration](workflows-and-orchestration). |
| DECISION | Available | Available |  |
| EMAIL | Available | Available |  |
| SESSION | Available | Available | dbt: `EXECUTE DBT PROJECT`. Scripting: `CALL public.m_<Mapping>(:scope)`. |
| START | Available | Available | XML `TYPE="Start"`. |
| WORKLET | Available | Available |  |
| Command | Not yet available | Not yet available | `SSC-EWI-INF0003` placeholder. |
| Control | Not yet available | Not yet available |  |
| Event Wait | Not yet available | Not yet available |  |
| Timer | Not yet available | Not yet available |  |

Expand

Show lessSee more

These capabilities apply across the workflow, rather than to a single element:

| Capability | dbt | Snowflake Scripting | Notes |
| --- | --- | --- | --- |
| Session overrides (Pre/Post-SQL, SQL Override) | Available | Available | See [Workflows and orchestration](workflows-and-orchestration). |
| Variable and parameter management | Available | Available | `control_variables` table; see [Variables and parameters](variables-and-parameters). |

Expand

Show lessSee more

Note

The Snowflake Scripting output format is in active development, so the generated code may change between releases. Most data-flow transformations are converted, but a few are still only converted in the dbt format. See [Informatica to Snowflake Scripting](snowflake-scripting/README) for the current status.

## Naming and sanitization rules

To keep generated dbt model names and `ref()` calls valid and aligned, Informatica object names are sanitized: any character outside `A`–`Z`, `a`–`z`, `0`–`9`, and the underscore (`_`) is replaced with an underscore. Letter case is preserved.

| Informatica name | Generated name |
| --- | --- |
| `SQ_DimCurrency` | `SQ_DimCurrency` |
| `m_load-customer data` | `m_load_customer_data` |
| `LKP@Currency` | `LKP_Currency` |

Expand

Show lessSee more

dbt models follow the three-tier naming convention: staging models use the `stg_raw__` prefix, intermediate models use the `int_` prefix, and mart models take the target table name. See [Informatica to dbt](dbt/README) for details.

In the Snowflake Scripting format, mapping procedures are named `public.m_<Mapping>` (the `m_` prefix is added only when the Mapping name does not already start with it). Mapplets, reusable shared objects, and unconnected Lookup UDFs are named `<Folder>_<Def>_<8-hex SHA256 of identity>` so two objects with the same Informatica name in different folders can’t collide. Example mapplet: `ScriptingCases_AnActiveMapplet_eeb91c86`. Example unconnected Lookup UDF: `Lookup_SNOW_3702098_m_Lookup_DisconnUnconn_LKPTRANS_222878c0`.

## Get started

1. Run a conversion with [Snowflake AIM Agent for Data Warehouses](/migrations/aim-for-datawarehouses/overview).
2. Choose your output format: [Informatica to dbt](dbt/README) (generally available) or [Informatica to Snowflake Scripting](snowflake-scripting/README) (preview).
3. Use the shared [Expression functions](expression-functions) and [Data types](data-types) references as you review the generated code.
