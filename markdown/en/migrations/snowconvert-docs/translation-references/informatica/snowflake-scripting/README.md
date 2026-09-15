# Informatica PowerCenter - Snowflake Scripting output

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for Informatica PowerCenter migrations.

This page describes the **Snowflake Scripting output format** for Informatica PowerCenter. In this format, each Mapping is converted into a Snowflake [stored procedure](/sql-reference/sql/create-procedure) and each Workflow into a [Task](/sql-reference/sql/create-task) graph that calls those procedures. This is an alternative to the generally available [dbt output format](../dbt/README), where each Mapping becomes a dbt project instead.

Warning

The Snowflake Scripting output format is in active development, and the generated code may change between releases. For production migrations, use the generally available [dbt output format](../dbt/README). Review every generated procedure before you run it.

## The procedure model

Each Mapping becomes one Snowflake stored procedure. The procedure is named `public.m_<Mapping>`, with the `m_` prefix added unless the Mapping name already starts with it. The procedure takes a single `scope` parameter, which carries the variable scope used to resolve [variables and parameters](../variables-and-parameters) at runtime:

Copy code

```
CREATE OR REPLACE PROCEDURE public.m_load_customers (scope VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   BEGIN
      -- The Mapping data flow becomes the procedure body.
   END
$$;
```

Inside the body, the data flow is built from the Mapping’s transformations: each Source Qualifier becomes a temporary table, each Expression becomes a common table expression (CTE) or a temporary table, and the Target becomes an `INSERT` statement for a relational target, or writes to a stage with `COPY INTO` for a flat-file target. For the details and a complete worked example, see [Mappings and transformations](mappings-and-transformations).

## Supported transformations

Most data-flow transformations are now converted in this format:

| Transformation | Status | Notes |
| --- | --- | --- |
| Source Definition | Available | Supplies table metadata. Emits no SQL of its own. |
| Source Qualifier | Available | Becomes a temporary table. A flat-file source reads from a stage and needs a stage path mapping. |
| Expression | Available | Becomes a CTE, or a temporary table when reused downstream. |
| Filter | Available | None |
| Router | Available | None |
| Joiner | Available | None |
| Union Transformation | Available | None |
| Aggregator | Available | Both grouped and ungrouped aggregation. |
| Sorter | Available | Includes the distinct (remove duplicates) option. |
| Rank | Available | None |
| Sequence | Available | XML `Sequence Generator`. Reusable and non-reusable. |
| Normalizer | Available | None |
| Lookup Procedure | Available | Covers connected lookups (including Use Any Value and Use All Values), unconnected lookups (hashed UDF named `<Folder>_<Def>_<8-hex>`), and flat-file lookups from `@public.landing_stage/infpc/sources/…`. |
| Mapplet | Available | Procedure named `<Folder>_<Def>_<8-hex>`. A mapplet with more than one input or output emits `SSC-EWI-INF0001`; a mapplet with no input takes no parameters. |
| Update Strategy | Available | Converted for the dispatch shapes described in [Mappings and transformations](mappings-and-transformations). Other shapes fall back to the dbt output. |
| Target Definition | Available | Becomes the write statement. A flat-file target writes with `COPY INTO` a stage. |
| Stored Procedure | Available | Connected Normal Stored Procedure emits a UDF CTE (`source_data` → `sp_result`) plus `SSC-EWI-INF0040`; this isn’t a Snowflake `CALL`. Disconnected or midstream Stored Procedure still emits `SSC-EWI-INF0001`. |
| Java Transformation | Available | Pass-through CTE plus `SSC-FDM-INF0045`; the Java source isn’t applied. See [Mappings and transformations](mappings-and-transformations). |
| App Multi-Group Source Qualifier | Not yet available | None |
| Application Source Qualifier | Not yet available | None |
| Salesforce Lookup | Not yet available | None |
| SQL Transform | Not yet available | XML `Custom Transformation` (`TEMPLATENAME=SQL Transform`). |
| Transaction Control | Not yet available | `SSC-EWI-INF0001` placeholder. See [Mappings and transformations](mappings-and-transformations) for the Transaction Control example. |
| XML Source Qualifier | Not yet available | None |

Expand

Show lessSee more

When a transformation isn’t converted in this format, a placeholder marked with an EWI code is emitted so you can convert it manually. See [Mappings and transformations](mappings-and-transformations) for how each supported transformation is generated and how unsupported ones are handled.

For these transformations in the dbt output format, see [dbt mappings and transformations](../dbt/mappings-and-transformations).

## Orchestration

Workflow orchestration is the same for both output formats. A Workflow becomes a graph of Snowflake Tasks, and the only difference is how a Session runs its Mapping: in the Snowflake Scripting format, the Session’s Task calls the Mapping procedure and forwards the variable scope:

Copy code

```
CALL public.m_load_customers(:scope);
```

For the full orchestration reference (Sessions, Worklets, and the Decision, Assignment, and Email tasks), see [Workflows and orchestration](../workflows-and-orchestration).

## Shared references

Several references apply to both output formats, because the generated Snowflake expressions and the orchestration are the same regardless of format:

- [Workflows and orchestration](../workflows-and-orchestration): how Workflows become Snowflake Task graphs.
- [Variables and parameters](../variables-and-parameters): the `control_variables` table, parameter files, and variable scope.
- [Expression functions](../expression-functions): Informatica functions and their Snowflake equivalents.
- [Data types](../data-types): how PowerCenter data types map to Snowflake types.

For the concept map and the full supported-component matrix, see the [Informatica PowerCenter overview](../README).
