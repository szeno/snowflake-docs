# Informatica PowerCenter - dbt output

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for Informatica PowerCenter migrations.

This page describes the **dbt output format** for Informatica PowerCenter: how Mappings are converted into [dbt projects](/user-guide/data-engineering/dbt-projects-on-snowflake) and Workflows into Snowflake [Task](/sql-reference/sql/create-task) graphs that run them. For the concept overview and supported-component matrix, see the [Informatica PowerCenter overview](../README). For the alternative output, see [Informatica to Snowflake Scripting](../snowflake-scripting/README).

## How a Mapping becomes a dbt project

Each Mapping is converted into a standalone dbt project with a three-tier model architecture.

| Layer | Materialization | Purpose |
| --- | --- | --- |
| `models/staging/` | View | Clean, type-safe access to source data referenced in `sources.yml`. Generated from Source Qualifier, Source Definition, and Flat File Source transformations. |
| `models/intermediate/` | Ephemeral by default | Transformation logic from the original Mapping. Generated from Expression, Joiner, Filter, Lookup, and other transformations. Ephemeral models aren’t persisted to the database, but some transformations override that default: a Sorter is materialized as a table so that its own `ORDER BY` is preserved, and an Update Strategy path can also change the materialization of the models it feeds. |
| `models/marts/` | Incremental or Table | Business-ready data models that correspond to Target Definitions. An Update Strategy transformation produces either an incremental model with a merge strategy or a table model, depending on the strategy it expresses. |

Expand

Show lessSee more

Each Mapping produces this project structure:

```
{MappingName}/
├── dbt_project.yml                   # Materialization config and hooks
├── profiles.yml                      # Snowflake connection profile
├── models/
│   ├── sources.yml                   # Source table definitions
│   ├── staging/
│   │   ├── stg_customers.sql
│   │   └── stg_regions.sql
│   ├── intermediate/
│   │   ├── int_expression.sql
│   │   └── int_joiner.sql
│   └── marts/
│       └── customer_dim.sql
└── macros/
    └── *.sql                         # Mapplet, reusable transformation, and unconnected Lookup macros
```

Important

Before deploying, replace the `YOUR_SCHEMA` and `YOUR_DB` placeholders in `sources.yml` and `profiles.yml` with your actual Snowflake schema and database names.

## Conversion paths

Most Mappings follow the default path: the Mapping becomes a dbt project, and the Session that runs it becomes a Task that calls `EXECUTE DBT PROJECT`.

One case skips the dbt project. When a Session reads a static flat file and writes it straight to a relational target, with no transformation logic in between, the conversion emits a Direct COPY instead: the Session becomes a Task that runs a `COPY INTO` statement against the staged file, and no dbt project is generated for that Mapping. Eligibility depends on the shape of the Session and its Mapping, so check the generated output to see which path each Session took. For the generated statements, see [Mappings and transformations](mappings-and-transformations) and [Workflows and orchestration](../workflows-and-orchestration).

## Data flow components

Each Mapping transformation is converted into a dbt model, a macro, or a project hook. The following components are supported. For a before/after example of each, see [Mappings and transformations](mappings-and-transformations).

| Informatica transformation | Category | dbt output | Naming pattern |
| --- | --- | --- | --- |
| Source Qualifier | Source | Staging model | `stg_raw__{source_name}` |
| Source Definition | Source | Staging model | `stg_raw__{source_name}` |
| Flat File Source | Source | Staging model with a `FILE_FORMAT` and stage binding | `stg_raw__{source_name}`, or no model when the Direct COPY path applies. See [Conversion paths](#label-informatica-dbt-conversion-paths). |
| Expression | Transformation | Intermediate model | `int_{transformation_name}` |
| Filter | Transformation | Intermediate model | `int_{transformation_name}` |
| Joiner | Transformation | Intermediate model | `int_{transformation_name}` |
| Lookup (connected) | Transformation | Intermediate model | `int_{transformation_name}` |
| Lookup (unconnected) | Transformation | dbt macro | `macros/ulkp_*.sql`, not an `int_` model |
| Aggregator | Transformation | Intermediate model | `int_{transformation_name}` |
| Router | Transformation | Intermediate model, one per output group | `int_{transformation_name}__{group_name}` |
| Sorter | Transformation | Table-materialized intermediate model that carries its own `ORDER BY` | `int_{transformation_name}` |
| Union | Transformation | Intermediate model | `int_{transformation_name}` |
| Normalizer | Transformation | Intermediate model | `int_{transformation_name}` |
| Rank | Transformation | Intermediate model | `int_{transformation_name}` |
| Sequence Generator | Transformation | Intermediate model | `int_{transformation_name}` |
| Update Strategy | Transformation | Intermediate model plus an incremental or table mart | `int_{transformation_name}` |
| Java Transformation | External logic | Pass-through intermediate model with an EWI or FDM message | `int_{transformation_name}`. The Java source isn’t applied. |
| Stored Procedure (connected) | External logic | Intermediate model that calls a per-row UDF, with an `INF0040` message | `int_{transformation_name}` |
| Stored Procedure (disconnected) | External logic | dbt hook in `dbt_project.yml` | `pre-hook` or `post-hook`, not an `int_` model |
| Mapplet | Reuse | dbt macro | `macros/{mapplet_name}.sql` |
| Reusable Expression transformation | Reuse | dbt macro | `macros/shared_models__*.sql`. A reusable Lookup follows its own connected or unconnected path instead. |
| Target Definition | Destination | Mart model | `{target_name}` |
| Flat File Target | Destination | Mart model with a `copy_into_stage` post\_hook, or a Direct COPY Session | `{target_name}` |

Expand

Show lessSee more

Note

Unlisted Mapping transformations generate an EWI code that flags the transformation for manual conversion. For a before/after example of each supported transformation, see [Mappings and transformations](mappings-and-transformations).

## Control flow components

Informatica Workflows define orchestration: which Sessions run, in what order, and with what variable context. A Workflow is converted into a graph of Snowflake [Tasks](/sql-reference/sql/create-task) linked by `AFTER` dependencies, and each Worklet is converted into a [stored procedure](/sql-reference/sql/create-procedure) that the graph calls.

| Element | Conversion target | Notes |
| --- | --- | --- |
| Workflow | Task graph | A root Task plus one Task per element, chained with `AFTER`. |
| Start | Root Task (`SELECT 1`) | Entry point of the graph, with no `AFTER` clause. |
| Session | Task running `EXECUTE DBT PROJECT` or `COPY INTO` | Runs the Session’s Mapping as a dbt project with `EXECUTE DBT PROJECT`, or runs `COPY INTO` when the Direct COPY path applies. See [Conversion paths](#label-informatica-dbt-conversion-paths). |
| Session overrides | Applied in the dbt project | Pre-SQL and post-SQL become model hooks, and a SQL Override replaces the source query. |
| Worklet | Stored procedure called with `CALL` | A reusable sub-workflow. |
| Decision, Assignment, and Email tasks | Inline scripting in the Task | Conditions, variable assignments, and notifications. |
| Parameter files | Loaded into `control_variables` at runtime | `.txt` and `.xml` formats are supported. |

Expand

Show lessSee more

For the generated SQL and an example of each element, see [Workflows and orchestration](../workflows-and-orchestration).

### Session location overrides

A Session can also override where its Mapping reads data: the owner name, the source table name, or just the connection. Those overrides become per-instance dbt variables, and the affected sources are emitted as variable-driven source groups, so each Session instance resolves its own owner and table without changing the shared models. Schema routing is handled by a macro in the generated project. When a Session overrides only the connection, the source keeps the schema and table names of the original definition.

Note

Unlisted Workflow elements (for example, Timer and Command tasks) are kept as a commented stub and marked with an EWI for manual conversion.

## Variable management

Informatica variables and parameters are managed through a table-driven system generated in the `etl_configuration/` folder. User-defined variables become dbt project variables (`{{ var('name') }}`) in the models, and a shared `control_variables` table tracks their values at runtime so orchestration can read and update them.

For the `control_variables` table, the supporting UDFs and procedures, parameter files, and variable scope, see [Variables and parameters](../variables-and-parameters).
