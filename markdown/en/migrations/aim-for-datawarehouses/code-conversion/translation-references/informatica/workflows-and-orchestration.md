# Informatica PowerCenter - Workflows and orchestration

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts. This preview is available for Informatica PowerCenter migrations.

Note

This reference applies to both output formats, **dbt** and **Snowflake Scripting**.

This page describes how Informatica PowerCenter Workflows (the orchestration layer) are converted to Snowflake. A Workflow becomes a graph of Snowflake [Tasks](/sql-reference/sql/create-task) linked by `AFTER` dependencies, which preserves the original execution order.

The orchestration is the **same for both [output formats](README)** (dbt and Snowflake Scripting). The only difference is how a Session runs its Mapping, shown in [Session task](#session-task).

## Workflow and Start task

A Workflow becomes a set of `CREATE OR REPLACE TASK` statements. The Start task is the **root Task** of the graph: it carries no body beyond a `SELECT 1` (plus a metadata comment) and has no `AFTER` clause. Every other task declares an `AFTER` dependency on its predecessor.

Copy code

```
CREATE OR REPLACE TASK public.w_execute_product_mappings
AS
SELECT
    1;
```

## Session task

A Session runs a Mapping. Each Session becomes a Task chained after its predecessor; the Task body is where the two output formats differ.

In the **dbt** format, the Task runs the Mapping’s dbt project with [`EXECUTE DBT PROJECT`](/sql-reference/sql/execute-dbt-project):

Copy code

```
CREATE OR REPLACE TASK public.AdventureWorksETLs_w_execute_product_mappings_s_mapping_product_names
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.w_execute_product_mappings
AS
BEGIN
   EXECUTE DBT PROJECT public.m_product_names ARGS='build --target dev';
END;
```

When the Workflow carries variables, the variable payload is built and appended with `--vars`:

Copy code

```
LET dbt_vars_json VARCHAR := (SELECT public.BuildDbtVarsJsonUDF(:scope));
LET full_args VARCHAR := 'build --target dev --vars ' || :dbt_vars_json || '';
EXECUTE DBT PROJECT public.m_product_names ARGS = :full_args;
```

In the **Snowflake Scripting** format, the Task calls the Mapping’s [stored procedure](/sql-reference/sql/create-procedure) instead, forwarding the variable scope:

Copy code

```
CREATE OR REPLACE TASK public.AdventureWorksETLs_w_execute_product_mappings_s_mapping_product_names
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.w_execute_product_mappings
AS
BEGIN
   CALL public.m_product_names(:scope);
END;
```

Replace `DUMMY_WAREHOUSE` with your actual Snowflake warehouse. The Task name combines the folder, Workflow, and Session names, so a reusable Session used in several places produces a distinct Task each time while still running the same Mapping.

Note

When a Session defines per-instance connection overrides, `SSC-FDM-INF0063` is emitted, because Informatica does not export connection definitions. Set the generated database-override variables to your Snowflake database after migration.

## Session overrides

Informatica Sessions can override Mapping properties:

- A **SQL Override** on a Source Qualifier replaces the generated source query.
- **Pre-SQL** and **Post-SQL** (on a Source Qualifier or Target) run before and after the data load. In the dbt format they become `pre-hook` and `post-hook` settings on the model; in the Snowflake Scripting format they run inside the Mapping’s procedure.

## Worklet task

A Worklet is a reusable sub-workflow. Each Worklet is converted into a Snowflake [stored procedure](/sql-reference/sql/create-procedure) and called from the Task graph with `CALL`, forwarding the variable scope:

Copy code

```
CREATE OR REPLACE TASK public.workflow_execute_worklet_task
WAREHOUSE=DUMMY_WAREHOUSE
AFTER public.predecessor_task
AS
BEGIN
   CALL public.folder_worklet_name(:scope);
END;
```

## Decision task

A Decision task evaluates a condition and publishes the result for downstream tasks. The condition is translated to an `IFF` expression and returned with `SYSTEM$SET_RETURN_VALUE`:

Copy code

```
LET result VARCHAR := (SELECT IFF(1 = 1, 'true', 'false'));
CALL SYSTEM$SET_RETURN_VALUE(:result);
```

If the condition is empty, `TRUE` is used and an FDM is emitted. If the condition references a task status (for example, `$s_session.Status = SUCCEEDED`), it falls back to `TRUE` and an EWI is emitted, because task-status references are not supported.

## Assignment task

An Assignment task sets workflow variables. For each assignment, a local variable is declared from the translated expression, then persisted with the `UpdateControlVariable` procedure so later tasks read the new value:

Copy code

```
LET var1 VARCHAR := (SELECT 100 + 50);
CALL public.UpdateControlVariable('var1', 'workflow1', TO_VARIANT(:var1));
```

An assignment that references an earlier variable reads it back with `GetControlVariableUDF`, which preserves Informatica’s sequential evaluation order. See [Variables and parameters](variables-and-parameters) for the variable store.

## Email task

An Email task becomes a Snowflake email notification. A notification integration is created and the message is sent with `SYSTEM$SEND_EMAIL`:

Copy code

```
LET send_notification_sql VARCHAR := 'CREATE OR REPLACE NOTIFICATION INTEGRATION send_notification_email_integration
  TYPE = EMAIL
  ENABLED = TRUE
  ALLOWED_RECIPIENTS = ("user1@example.com", "user2@example.com")';
EXECUTE IMMEDIATE :send_notification_sql;
CALL SYSTEM$SEND_EMAIL('send_notification_email_integration', 'user1@example.com,user2@example.com', 'ETL Run Complete', 'Daily ETL has finished successfully.');
```

Snowflake email differs from Informatica in a few ways, so markers are emitted to review: the sender address is fixed by Snowflake (the original sender cannot be set), recipients must be verified, and variable tokens in the subject or body (such as `%n` or `$VAR`) are not resolved.

## Deploying and running

In the dbt format, deploy each Mapping’s dbt project before the orchestration runs, with the Snowflake CLI (`snow dbt deploy --schema schema_name --database database_name package_name`) or a Snowflake Workspace; the project name (for example, `public.m_product_names`) must match the deployed name. In the Snowflake Scripting format, the Mapping procedures are created directly in Snowflake, so the Tasks call them without a separate deploy step.

## Unsupported workflow elements

Workflow elements that have no direct Snowflake equivalent are kept as a commented stub inside the Task and marked with `SSC-EWI-INF0003` so you can convert them manually. Timer and Command tasks fall into this category today.
