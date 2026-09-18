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
| Source and Source Qualifier | Staging model or temporary table | Source reads become `stg_` staging models **or** `tmp_sq_<name>` temporary tables. Flat-file reads bind `@public.landing_stage/infpc/sources/<Folder>/<Def>/`; see [File ingestion](#label-informatica-file-ingestion). |
| Target | Mart model or write statement | Targets become marts models **or** the mapping procedure’s `INSERT` / `COPY INTO @public.landing_stage/infpc/targets/<Def>/`. A flat-file Target unloads to the stage, so it isn’t a file you land; see [File ingestion](#label-informatica-file-ingestion). |
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
- [File ingestion](#label-informatica-file-ingestion): how flat-file sources and lookups land on the stage the generated reads bind to.

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
| Lookup Procedure | Available | Available | XML `Lookup Procedure`. Covers connected lookups (including Use Any Value and Use All Values), unconnected lookups (as a hashed UDF), and flat-file lookups from `@public.landing_stage/infpc/sources/…`. Connected and unconnected flat-file lookups are both inventoried for landing; see [File ingestion](#label-informatica-file-ingestion). |
| Mapplet | Available | Available | Scripting: procedure named `<Folder>_<Def>_<8-hex>`. A mapplet with more than one input or output emits `SSC-EWI-INF0001`; a mapplet with no input takes no scope. dbt: macro. |
| Normalizer | Available | Available |  |
| Rank | Available | Available |  |
| Router | Available | Available |  |
| Sequence | Available | Available | XML `Sequence Generator`. |
| Sorter | Available | Available |  |
| Source Definition | Available | Available | Metadata only; emits no SQL of its own. A delimited flat-file definition is inventoried for landing; see [File ingestion](#label-informatica-file-ingestion). |
| Source Qualifier | Available | Available | Relational: temporary table. Scripting flat-file: reads from `@public.landing_stage/infpc/sources/<Folder>/<Def>/`. When a Source Qualifier has more than one associated source, the generated `FROM` uses only the first incoming source. See [File ingestion](#label-informatica-file-ingestion) for how the file reaches that path. |
| Stored Procedure | Available | Available | Connected Normal Stored Procedure emits a UDF CTE (`source_data` → `sp_result`) plus `SSC-EWI-INF0040`; this isn’t a Snowflake `CALL`. Disconnected or midstream Stored Procedure still emits `SSC-EWI-INF0001`. |
| Target Definition | Available | Available | Relational: `INSERT`. Scripting flat-file: `COPY INTO @public.landing_stage/infpc/targets/<Def>/`. The unload is a write, not a landing source; see [File ingestion](#label-informatica-file-ingestion). |
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

## File ingestion

A converted flat-file read doesn’t open the file on your PowerCenter host. It reads one generated stage, `public.landing_stage`, so every file a Mapping used to open on a filesystem has to arrive there first. The conversion inventories the files it expects and generates disabled Openflow flows that can land them, but it never moves a file and never writes a credential.

Landing is the **same for both [output formats](#output-formats)**: the prefixes below are the ones the dbt staging models, the Scripting `tmp_sq_` temporary tables, and the static [Direct copy loads](dbt/mappings-and-transformations) bind.

1. Find `ingestion-manifest.json`. There’s one manifest for the whole project, not one per Mapping, so a source definition that several Mappings read appears once. When the conversion writes an artifacts folder, look under `artifacts/ingestion/<session timestamp>/` (or `artifacts/ingestion/` if that run has no session timestamp). Otherwise the file is at `ETL/ingestion-manifest.json`.
2. Find the generated landing flows: `ETL/openflow/SnowConvert ETL Landing.json` for an S3-compatible source bucket, plus `ETL/openflow/SnowConvert ETL Landing (Azure).json` and `ETL/openflow/SnowConvert ETL Landing (GCS).json`. All three are generated. The store you stage through doesn’t have to match where the original file sat.
3. Map each original path to your object store. Use the original location recorded for that source to find the file, then upload it under the expected bucket prefix in the same source’s mapping. The original path is diagnostic: the conversion doesn’t infer a bucket from a drive letter or a UNC share.
4. Import a flow while it’s still disabled. Fill in the `SnowConvert file landing` parameter context for your source store and Snowflake connection, supply your own credentials, then enable the components. Each process group covers one PowerCenter folder (or Shared, for a definition with no folder) and copies listed objects to the matching stage prefix.
5. Confirm the file landed where the generated SQL reads. Source and lookup files land under `@public.landing_stage/infpc/sources/<Folder>/<Def>/`. For a known filename, that’s a path such as `@public.landing_stage/infpc/sources/SalesFolder/SRC_CUSTOMERS/customers.dat`.

### What gets inventoried

Identity is the owning PowerCenter folder plus the source definition, which is what `infpc/sources/<Folder>/<Def>/` encodes. The physical path is diagnostic, so two Mappings that read one definition share a single stage prefix, and two same-named definitions in different folders stay separate.

Inventoried today:

- Delimited flat-file Source Definitions and the Source Qualifiers that read them.
- Connected and unconnected flat-file Lookups.

Not inventoried:

- Flat-file Targets. A Target unloads to `@public.landing_stage/infpc/targets/<Def>/`, which is a file the conversion writes, not one you land.
- Fixed-width flat files. They have no Snowflake `FILE_FORMAT` equivalent, so they carry `SSC-EWI-INF0068` instead of a stage read.

Some inventoried sources still need a mapping before a generated flow will land them. A file that already lives in an object store (an `s3://`, `wasbs://`, or `gs://` location) is one case, and a definition whose driving Sessions name different files is another. The conversion doesn’t fold an object-store URI into the stage prefix, so the prefix stays `infpc/sources/<Folder>/<Def>/`.

### Session paths that resolve at runtime

When the Session names the file through PowerCenter parameters rather than a literal, for example `$$SourceDirectory` and `$$SourceFileName`, the path stays a runtime binding instead of becoming `UNKNOWN_FILE`. In the dbt format, the read renders those parameters as `var()`:

Copy code

```
SELECT
   $1 :: VARCHAR(10) AS EMPLOYEE_ID,
   $2 :: VARCHAR(100) AS FULL_NAME,
   $3 :: FLOAT AS SALARY
FROM
   @public.landing_stage/infpc/sources/TestFolder/SRC_DIRECT_CSV/{{ var('SourceDirectory') }}/{{ var('SourceFileName') }} (FILE_FORMAT => 'TestFolder_m_DIRECT_LOAD_SRC_DIRECT_CSV')
```

In the Snowflake Scripting format, the same read is built as a string and run with `EXECUTE IMMEDIATE`:

Copy code

```
LET sourcedirectory VARCHAR := public.GetControlVariableUDF('SourceDirectory', :scope) :: VARCHAR;
LET sourcefilename VARCHAR := public.GetControlVariableUDF('SourceFileName', :scope) :: VARCHAR;
EXECUTE IMMEDIATE 'CREATE OR REPLACE TEMPORARY TABLE tmp_sq_fl AS (SELECT FIELD1, FIELD2 FROM ( SELECT $1 :: VARCHAR(2) AS FIELD1, $2 :: VARCHAR(4) AS FIELD2 FROM @public.landing_stage/infpc/sources/ScriptingCases/fl/' || :sourcedirectory || '/' || :sourcefilename || ' (FILE_FORMAT => ''ScriptingCases_m_FlatFileSource_fl'') ) fl)'
```

Both formats run once those variables have values. The generated Openflow flows still omit the source until you map those parameter values to stage-relative path fragments, because the conversion never writes the parameter values.

Note

A parameterized path never converts to the `COPY INTO` shortcut in [Direct copy loads](dbt/mappings-and-transformations). That shortcut needs a literal filename that every driving Session agrees on, so a parameterized Session converts as a full dbt project or mapping procedure instead.

### When the filename can’t be resolved

The Session, not the Mapping, carries the source filename. When no driving Session supplies one, for example because the Mapping was exported without its Workflow, the read is emitted against `@public.landing_stage/infpc/sources/<Folder>/<Def>/UNKNOWN_FILE` and carries `SSC-EWI-INF0069`. Convert the Workflow alongside the Mapping and the same source binds its real filename instead. This is a mapping-only limitation, not the converted Workflow happy path.

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
