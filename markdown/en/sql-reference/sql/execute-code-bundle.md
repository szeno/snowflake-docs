# EXECUTE CODE BUNDLE

Note

Notebook Project Objects have been renamed to **Code Bundles**. The `NOTEBOOK PROJECT` grammar is still supported; for that syntax, see [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project). For background on the rename, see the [behavior change announcement](/release-notes/bcr-bundles/un-bundled/bcr-2393).

Executes a [Code Bundle](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule#label-nb-in-ws-schedule-npo) at the specified entrypoint. This command runs the code in a non-interactive (headless) mode and is useful for CI/CD
pipelines and other orchestrated workflows where you want to pass parameters or lock dependency versions for repeatable runs. The command can be run from:

- SQL files.
- Other Snowflake executables (Tasks).
- External orchestrators that issue SQL (for example, Airflow, Prefect, Dagster, CI/CD systems).

The compute type, runtime, dependencies, external access integrations, and secrets are defined in the Code Bundle’s `code_bundle.yml` specification. You can override the stored specification at run time with the `WITH SPECIFICATION` clause.

Important

Before triggering a non-interactive run of a notebook, ensure that your notebook sets its execution context (database and schema) or uses fully qualified
object names. For more information, see [Editing and running notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-edit-run).

See also:
[CREATE CODE BUNDLE](/sql-reference/sql/create-code-bundle), [SHOW CODE BUNDLES](/sql-reference/sql/show-code-bundles), [CREATE TASK](/sql-reference/sql/create-task), [CI/CD workflow scenario](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-workflow-scenarios#label-nb-in-ws-schedule-scenario-b),
[Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging), [Running notebooks with parameters](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-parameters),
[Using secrets in Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-using-secrets)

## Syntax

Copy code

```
EXECUTE CODE BUNDLE <name>
  ENTRYPOINT = '<path>'
  [ ARGUMENTS = ( '<arg>' [ , '<arg>' ... ] ) ]
  [ WITH SPECIFICATION $$ <yaml_spec> $$ ];
```

## Required parameters

`name`
:   Identifier of the Code Bundle to execute.

    Must reference an existing Code Bundle created with [CREATE CODE BUNDLE](/sql-reference/sql/create-code-bundle).

    Must be fully qualified unless it resides in the current DATABASE and SCHEMA.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ENTRYPOINT = 'path'`
:   Specifies the file within the bundle that Snowflake executes (for example, `main.py` or `notebooks/train.ipynb`).

    The path is relative to the bundle root.

    `.ipynb` notebook files run only on compute pools (Container Runtime).

## Optional parameters

`ARGUMENTS = ( 'arg' [ , 'arg' ... ] )`
:   Optionally passes one or more string arguments to the entrypoint at runtime, which appear as command-line arguments in the `sys.argv` list.
    Arguments are useful for making logic dynamic (for example, selecting an environment such as `--env prod`).

    Specify each argument as a separate quoted string in the list. In a Python entrypoint, access the arguments using `sys.argv[0]` for the
    entrypoint name, `sys.argv[1]` for the first argument, and so on.

    Each value must be a string literal or a [SQL variable](/sql-reference/session-variables) reference such as `:my_var`.
    Function calls and other expressions aren’t supported. For an example of passing values computed at runtime, see
    [Pass arguments computed at runtime](#label-execute-code-bundle-dynamic-arguments).

    Only strings are supported; other data types (such as integers or Booleans) are interpreted as NULL.

    The `ARGUMENTS` syntax differs between the two commands: `EXECUTE CODE BUNDLE` takes a parenthesized list of strings, while
    [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project) takes a single string.

    Examples:

    Copy code

    ```
    ARGUMENTS = ('--env', 'prod');
    ```

    Copy code

    ```
    import sys
    print(sys.argv)
    ```

`WITH SPECIFICATION $$ yaml_spec $$`
:   Optionally provides an inline `code_bundle.yml` specification that overrides the specification stored with the Code Bundle. This is useful for
    testing different configurations (for example, a different compute type or runtime version) without modifying the bundle.

    Example:

    Copy code

    ```
    EXECUTE CODE BUNDLE my_bundle
      ENTRYPOINT = 'main.py'
      WITH SPECIFICATION
      $$
      bundle:
        type: custom
        compute_type: compute_pool
        language: python
        compute_options:
          compute_pool: system_compute_pool_cpu
          query_warehouse: my_db.my_schema.my_wh
          runtime_version: 'V2.9-CPU-PY3.12'
      $$;
    ```

## Access control requirements

The role executing `EXECUTE CODE BUNDLE` must have either OWNERSHIP or USAGE privileges on the Code Bundle.

If the Code Bundle is configured to run on compute pools (`compute_type: compute_pool`), the executing role must also have:

- USAGE and MONITOR on the query warehouse.
- USAGE or OWNERSHIP on the compute pool and on the database and schema containing the Code Bundle.
- READ or OWNERSHIP on any secrets referenced in the specification. USAGE on a secret is not sufficient.
- USAGE or OWNERSHIP on the external access integrations, artifact repositories, and other objects referenced in the specification.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can’t run the `EXECUTE CODE BUNDLE` command from a notebook cell.
- You can call `EXECUTE CODE BUNDLE` from tasks, enabling runs as part of larger workflows. For details, see
  [Supported invocation contexts](#label-execute-code-bundle-invocation-contexts).
- Run history and run result visibility for executions triggered by this command depends on the viewing role’s Code Bundle privileges and `IMPERSONATE` privilege over the initiating user. For details, see [Run history and result visibility](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule#label-nb-in-ws-schedule-run-visibility).

### Supported invocation contexts

`EXECUTE CODE BUNDLE` runs with caller’s rights, so it’s only supported in contexts that preserve the caller’s identity.
The following table shows where you can run the command:

| Context | Supported | Notes |
| --- | --- | --- |
| SQL worksheet or SQL file | Yes | Runs as the calling user. |
| Task body | Yes | Supported both as a single-statement body and inside a `BEGIN ... END` [Snowflake Scripting](/developer-guide/snowflake-scripting/index) block. |
| Stored procedure with `EXECUTE AS CALLER` | Yes | The procedure runs with the caller’s privileges. |
| Stored procedure with `EXECUTE AS OWNER` | No | Owner’s rights procedures can’t run the command. Use `EXECUTE AS CALLER` instead. |
| Stored procedure with `EXECUTE AS RESTRICTED CALLER` | No | Code Bundles don’t support [restricted caller’s rights](/developer-guide/restricted-callers-rights) yet. |
| Streamlit app | No | Streamlit in Snowflake apps run with [owner’s rights](/developer-guide/streamlit/object-management/owners-rights) by default, and the [restricted caller’s rights](/developer-guide/streamlit/features/restricted-callers-rights) option isn’t supported by this command. |
| Notebook cell | No | Nested execution isn’t supported. |

Expand

Show lessSee more

## Examples

Execute a Code Bundle:

Copy code

```
EXECUTE CODE BUNDLE my_bundle
  ENTRYPOINT = 'main.py';
```

Execute a Code Bundle with arguments:

Copy code

```
EXECUTE CODE BUNDLE my_bundle
  ENTRYPOINT = 'jobs/main.py'
  ARGUMENTS = ('--source-table', 'RAW_SALES', '--output-table', 'SALES_AGG');
```

Execute a notebook packaged in a Code Bundle (runs on a compute pool):

Copy code

```
EXECUTE CODE BUNDLE "sales_detection_db"."schema"."nightly_training"
  ENTRYPOINT = 'notebook_file.ipynb'
  ARGUMENTS = ('--env', 'prod');
```

### Pass arguments computed at runtime

`ARGUMENTS` accepts string literals or SQL variables, but not function calls. To pass a value that’s computed at runtime,
assign it to a variable first inside a `BEGIN ... END` block, then reference the variable with a colon prefix.

The following task reads values from its own [CONFIG](/sql-reference/sql/create-task) property with
[SYSTEM$GET\_TASK\_GRAPH\_CONFIG](/sql-reference/functions/system_get_task_graph_config) and passes them to the entrypoint:

Copy code

```
CREATE TASK my_db.my_schema.nightly_run
  WAREHOUSE = my_wh
  SCHEDULE = 'USING CRON 0 9 * * * America/Los_Angeles'
  CONFIG = $${"source_table": "raw_sales", "output_table": "sales_agg"}$$
AS
BEGIN
  LET source_table VARCHAR := SYSTEM$GET_TASK_GRAPH_CONFIG('source_table')::VARCHAR;
  LET output_table VARCHAR := SYSTEM$GET_TASK_GRAPH_CONFIG('output_table')::VARCHAR;
  EXECUTE CODE BUNDLE my_db.my_schema.my_bundle
    ENTRYPOINT = 'jobs/main.py'
    ARGUMENTS = ('--source-table', :source_table, '--output-table', :output_table);
END;
```

Read the arguments in the entrypoint with `sys.argv`:

Copy code

```
import sys

# sys.argv[0] is the entrypoint name, so the arguments start at index 1.
print(sys.argv)  # ['jobs/main.py', '--source-table', 'raw_sales', '--output-table', 'sales_agg']
```

The same pattern works with other values available at runtime, such as a predecessor task’s return value from
[SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE](/sql-reference/functions/system_get_predecessor_return_value) or a session variable
set with [SET](/sql-reference/sql/set).

Passing a function call directly to `ARGUMENTS` isn’t supported and fails to compile:

Copy code

```
-- Not supported.
ARGUMENTS = (SYSTEM$GET_TASK_GRAPH_CONFIG('source_table'));
```
