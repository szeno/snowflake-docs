# Informatica PowerCenter - Variables and parameters

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for Informatica PowerCenter migrations.

Note

This reference applies to both output formats, **dbt** and **Snowflake Scripting**.

This page describes how Informatica PowerCenter variables and parameters are converted to Snowflake. User-defined variables are made available to each Mapping and are also tracked at runtime in a shared `control_variables` table, so values set during orchestration are available to later tasks. The `control_variables` table, the supporting procedures, and parameter files are the same for both [output formats](README); only how a variable is referenced inside an expression differs, as shown below. For how Workflows use these values, see [Workflows and orchestration](workflows-and-orchestration).

## Variable references in expressions

Inside a Mapping expression, an Informatica variable reference (`$$name`) is resolved to its value. In the **dbt** format it becomes a dbt project variable, `{{ var('name') }}` (rendered quoted for string variables so it compiles to a SQL string literal, unquoted for numeric variables). In the **Snowflake Scripting** format it becomes a `GetControlVariableUDF('name', :scope)` call against the `control_variables` table.

Informatica:

Copy code

```
VacationHours + $$m_vacation_bonus
$$m_country
```

Snowflake (`int_EXPTRANS.sql`):

Copy code

```
WITH source_data AS
(
   SELECT
      EmployeeKey,
      VacationHours
   FROM
      {{ ref('stg_raw__SQ_DimEmployee') }}
)
SELECT
   EmployeeKey AS EmployeeKey,
   VacationHours + {{ var('m_vacation_bonus') }} AS UpdatedVacationHours,
   '{{ var('m_country') }}' AS Country
FROM
   source_data
```

Each Mapping’s `dbt_project.yml` declares the variables with their default values:

Copy code

```
vars:
  m_vacation_bonus: 8
  m_country: USA
```

## The control\_variables table

A shared `control_variables` table is generated in the `etl_configuration/` folder. It stores the values of every Workflow variable and parameter, so orchestration can read and update them at runtime:

Copy code

```
CREATE TRANSIENT TABLE IF NOT EXISTS public.control_variables (
  variable_name VARCHAR NOT NULL,
  variable_value VARIANT,
  variable_type VARCHAR NOT NULL,
  variable_scope VARCHAR NOT NULL,
  is_parameter BOOLEAN DEFAULT FALSE,
  is_persistent BOOLEAN DEFAULT FALSE,
  last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

| Column | Type | Description |
| --- | --- | --- |
| `variable_name` | VARCHAR | Variable name. |
| `variable_value` | VARIANT | Value, stored as a VARIANT so it can hold any data type. |
| `variable_type` | VARCHAR | Original Informatica data type. |
| `variable_scope` | VARCHAR | The scope that owns the variable (see [Variable kinds and scope](#variable-kinds-and-scope)). |
| `is_parameter` | BOOLEAN | `TRUE` for parameters, `FALSE` for variables. |
| `is_persistent` | BOOLEAN | `TRUE` when the value persists across runs. |
| `last_updated_at` | TIMESTAMP | When the value was last updated. |

Expand

Show lessSee more

## Variable kinds and scope

Four kinds of user-defined variable are recognized and each is recorded under a `variable_scope` so values resolve at the right level:

| Informatica kind | Scope | Notes |
| --- | --- | --- |
| Workflow variable | Workflow name | Persists across the Workflow run. |
| Mapping variable | Workflow and Session name | Scoped to the Session that runs the Mapping. |
| Mapping parameter | Workflow and Session name | Same scope as a Mapping variable; `is_parameter` is `TRUE`. |
| Worklet variable | Worklet instance | Scoped to the Worklet instance, including nested instances. |

Expand

Show lessSee more

## Supporting UDFs and procedures

These helpers are generated in the `etl_configuration/` folder to manage the table:

| Component | Purpose |
| --- | --- |
| `GetControlVariableUDF` | Returns a variable’s value for a given name and scope. |
| `BuildDbtVarsJsonUDF` | Builds the JSON payload of all variables in a scope, passed to `EXECUTE DBT PROJECT` with `--vars`. |
| `InitVariablesFromConfig` | Loads default variable values from the generated config at the start of a run. |
| `UpdateControlVariable` | Updates a variable’s value and refreshes `last_updated_at`. |
| `InsertControlVariable` | Inserts a variable if it does not already exist. |
| `ClearVariables` | Removes the non-persistent variables for a scope. |
| `LoadParameterFile` | Applies parameter-file overrides from a Snowflake stage (see [Parameter files](#parameter-files)). |

Expand

Show lessSee more

## Parameter files

Informatica parameter files become runtime overrides applied from a Snowflake stage. At the start of a run, `LoadParameterFile` reads the file and applies values from least to most specific scope: a global section first, then each ancestor scope (Workflow, then Worklet), and finally the target scope, so the most specific value wins.

Because the original file path cannot be mapped automatically, a stage placeholder and an EWI are emitted to flag the parameter file for manual stage mapping.

Note

Replace the stage placeholder in the generated `LoadParameterFile` call with your actual Snowflake [stage](/sql-reference/sql/create-stage) and upload the parameter file there before running the orchestration.

## Built-in and system variables

Built-in variables such as `SYSDATE`, `SYSTIMESTAMP`, and `SESSSTARTTIME` are converted as expressions rather than stored in `control_variables`. For their Snowflake equivalents, see the [Expression functions](expression-functions#system-variables) reference. The `SETVARIABLE` family of functions is also covered there.
