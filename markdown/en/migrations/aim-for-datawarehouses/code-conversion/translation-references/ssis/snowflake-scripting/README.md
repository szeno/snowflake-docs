# SSIS - Snowflake Scripting output

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for SSIS migrations.

This page describes the **Snowflake Scripting output format** for SSIS. In this format, each Data Flow Task is converted into a Snowflake [stored procedure](/sql-reference/sql/create-procedure) that the package’s [Task](/sql-reference/sql/create-task) graph calls. The result is plain Snowflake SQL that you can deploy with any SQL client. This is an alternative to the default [dbt output format](../README), where each Data Flow Task becomes a dbt project instead.

The Control Flow of a package converts the same way in both formats: tasks, containers, variables, Execute Package, event handlers, and file loops all become a Task graph. For those conversions, see the [Control flow components](../README#control-flow-components) in the SSIS overview. Only the Data Flow Task changes.

Warning

The Snowflake Scripting output format is in active development. The set of supported Data Flow components is incomplete, and the generated code may change between releases. A component that isn’t converted is replaced by a placeholder that returns `NULL` for each of its columns, so a procedure can run successfully and still load `NULL` values. Resolve every [SSC-EWI-SSIS0001](../../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0001) before you use the output in production, and review every generated procedure before you run it. For components that this format doesn’t convert yet, use the [dbt output format](../README).

## The procedure model

Each Data Flow Task becomes one Snowflake stored procedure in the `public` schema. The procedure is named after the Data Flow Task, with spaces replaced by underscores and the original casing kept, so `Simple Data Flow` becomes `public.Simple_Data_Flow`. This is the same identifier the dbt output uses for its project, so switching formats doesn’t rename the object. When two Data Flow Tasks in a package produce the same name, a numeric suffix such as `Data_Flow_Task_1` keeps the names unique.

The procedure takes a single `scope` parameter, returns `VARCHAR`, and runs as the caller. The `scope` parameter carries the package name, so the procedure reads the same [package variables](../README#control-flow-components) that the Task graph set at runtime:

Copy code

```
CREATE OR REPLACE PROCEDURE public.Simple_Data_Flow (scope VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
   BEGIN
      -- The Data Flow becomes the procedure body.
   END
$$;
```

The Task that runs the Data Flow sets the scope and calls the procedure:

Copy code

```
CREATE OR REPLACE TASK public.completedataflow_complete_data_flow
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.completedataflow
AS
BEGIN
   LET scope VARCHAR := 'CompleteDataFlow';
   CALL public.Complete_Data_Flow(:scope);
END;
```

For comparison, the dbt output runs `EXECUTE DBT PROJECT public.Complete_Data_Flow ARGS='build --target dev'` in the same Task.

The conversion builds the procedure body in data-flow order. For the generated statements and complete examples, see [Data flows and components](data-flows-and-components):

1. If the Data Flow reads package variables, a `LET` declaration for each one reads its value with `GetControlVariableUDF` and the `scope` parameter.
2. Each source becomes a common table expression (CTE) named `cte_<component>`.
3. Each transformation becomes another CTE that reads the CTE of the component before it, in the order SSIS runs them.
4. The destination becomes an `INSERT` statement that carries the CTEs inside its source query.

## Output shapes

The shape of the Data Flow decides what the conversion generates. The shape depends on how many writes the Data Flow performs and on whether a step has to be read by more than one statement:

| Data Flow shape | Generated code | Where it runs |
| --- | --- | --- |
| One pipeline that ends in one destination | A chain of CTEs followed by one `INSERT`. | Stored procedure |
| A pipeline that writes more than once, such as a Multicast to several destinations, a Conditional Split with several outputs, or a Lookup with matched and unmatched outputs | The shared step is persisted as a `CREATE OR REPLACE TEMPORARY TABLE tmp_cte_<component>`, followed by one write for each destination. | Stored procedure |
| An OLE DB, ADO.NET, or Oracle table read that feeds an OLE DB or Oracle destination table directly, optionally through one Data Conversion or Row Count | A single `INSERT INTO ... SELECT` statement. This is the direct load that the dbt output also uses. | Inline in the package Task. No procedure is created. |
| An eligible Flat File Source that feeds an OLE DB Destination directly | A single `COPY INTO` statement. See [Direct COPY](data-flows-and-components#direct-copy). | Stored procedure |

Expand

Show lessSee more

A Snowflake CTE belongs to a single statement. A CTE chain is enough when the Data Flow is one pipeline with one write. When a step has to be read by a second write, the conversion persists it as a temporary table so that every later statement in the procedure can read it. This is the same CTE-promotion pattern that the [Informatica PowerCenter Snowflake Scripting output](../../informatica/snowflake-scripting/README) uses, so customers who convert both tools see one stored-procedure model.

## Supported components

Data Flow components that this format converts are listed below. Control Flow components aren’t listed because they convert the same way as in the dbt output. For the conversion of each Control Flow task and container, see the [SSIS overview](../README#control-flow-components).

| Component | Category | Status | Notes |
| --- | --- | --- | --- |
| OLE DB Source | Source | Available with limitations | Table or view reads and SQL command reads. A table name or SQL command that comes from a variable isn’t converted. |
| ADO.NET Source | Source | Available | None |
| Oracle Source | Source | Available | None |
| Excel Source | Source | Available with limitations | Reads a staged workbook through the generated `excel_source_udf` function. |
| Flat File Source | Source | Available with limitations | Converted only when the Data Flow is an eligible [Direct COPY](data-flows-and-components#direct-copy). Otherwise it becomes a placeholder. |
| Derived Column | Transformation | Available with limitations | An expression that can’t be converted turns the whole component into a placeholder. |
| Data Conversion | Transformation | Available | None |
| Conditional Split | Transformation | Available with limitations | Converted when one output continues the pipeline or when every output writes directly to a destination. |
| Multicast | Transformation | Available | A Multicast that feeds more than one destination persists a temporary table. |
| Union All | Transformation | Available | None |
| Merge | Transformation | Available | See [SSC-FDM-SSIS0002](../../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0002). |
| Merge Join | Transformation | Available | Inner, left outer, and full outer joins. See [SSC-FDM-SSIS0004](../../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0004). |
| Lookup | Transformation | Available with limitations | Only the OLE DB equality lookup shape described in [Lookup](data-flows-and-components#lookup). Other shapes become a placeholder. |
| Aggregate | Transformation | Available with limitations | One output only. Grouped and ungrouped aggregation. |
| Sort | Transformation | Available | Includes the option to remove duplicate rows. |
| Pivot | Transformation | Available with limitations | A static pivot over an input that declares its sort order. See [SSC-FDM-SSIS0021](../../../issues-and-troubleshooting/functional-difference/ssisFDM#ssc-fdm-ssis0021). |
| UnPivot | Transformation | Available | One target column or several aligned target columns. |
| Row Count | Transformation | Available with limitations | Rows pass through, but the output variable isn’t populated unless the Data Flow becomes a direct `INSERT`. |
| Cache Transform | Transformation | Available | Becomes a pass-through CTE. |
| OLE DB Command | Transformation | Available with limitations | Only a command that runs a stored procedure. A command that runs `INSERT`, `UPDATE`, or `DELETE` becomes a placeholder. |
| OLE DB Destination | Destination | Available | Table or view access modes. |
| Oracle Destination | Destination | Available | None |
| Excel Destination | Destination | Available with limitations | Written as an `INSERT` into a table named after the sheet. No Excel file is created. |

Expand

Show lessSee more

Components that aren’t listed, such as Character Map, Fuzzy Lookup, Script Component, Flat File Destination, and Copy Column, become a placeholder. See [Unsupported components](data-flows-and-components#unsupported-components). Raw File Source, Raw File Destination, and XML Source aren’t available in either output format.

## Unsupported components

A component that can’t be converted doesn’t stop the Data Flow and doesn’t send it back to dbt. The conversion emits a placeholder step that returns the expected columns as `NULL`, marked with [SSC-EWI-SSIS0001](../../../issues-and-troubleshooting/conversion-issues/ssisEWI#ssc-ewi-ssis0001), and still generates the rest of the procedure. The Task graph still calls the procedure, so the rest of the package stays reviewable and deployable. See [Unsupported components](data-flows-and-components#unsupported-components) for the generated code.

## Deploying and running

In the Snowflake Scripting format, the Data Flow procedures are created directly in Snowflake, so there’s no dbt project to deploy before the Tasks run. Deploy the output in this order:

1. Run the `etl_configuration/` files, which create the helper objects that the procedures and Tasks use: the variable procedures and functions, plus the file formats and stages for file loads.
2. Run each `<DataFlowName>.sql` file to create the Data Flow procedures.
3. Run each `<PackageName>.sql` file to create the Tasks.
4. Resume or run the root Task of the graph, exactly as you would with the dbt output.

To test a single Data Flow on its own, call its procedure with the package name as the scope: `CALL public.Simple_Data_Flow('SimpleDataFlow');`.

Before you run the procedures, replace any placeholder database and schema names, and land the files that file loads read. Flat file and Excel reads bind to the shared `public.landing_stage` the same way they do in the dbt output. For the ingestion manifest, the stage prefixes, and the Openflow flows that land the files, see [Ingestion](../README#ingestion).

## Reports

The conversion reports mark every Data Flow component that was converted in this format with the target element kind `SNOWFLAKE_SCRIPT_STATEMENT`, so you can see which parts of a package became Snowflake SQL. A component that produced a placeholder is reported as not supported with `SSC-EWI-SSIS0001` and also appears in the issues report.

## Shared references

Several references apply to both output formats, because the Control Flow conversion and the issue codes are the same regardless of format:

- [SSIS overview](../README): Control Flow tasks and containers, variables, ingestion, and the dbt output.
- [Data flows and components](data-flows-and-components): the generated code for each Data Flow component in this format.
- [SSIS EWI codes](../../../issues-and-troubleshooting/conversion-issues/ssisEWI) and [SSIS FDM codes](../../../issues-and-troubleshooting/functional-difference/ssisFDM): the issues the conversion can emit.
