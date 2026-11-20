# EXECUTE CODE BUNDLE

Note

Notebook Project Objects have been renamed to **Code Bundles**. The `NOTEBOOK PROJECT` grammar is still supported; for that syntax, see [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project). For background on the rename, see the [behavior change announcement](/release-notes/bcr-bundles/un-bundled/bcr-2393).

Runs a [Code Bundle](/developer-guide/code-bundles/code-bundles) at the specified entrypoint, or runs source files from a stage or workspace
without creating a Code Bundle first (an *anonymous run*). The command runs the code in a non-interactive (headless) mode and waits for the
run to finish. It’s useful for CI/CD pipelines and other orchestrated workflows where you want to pass parameters or lock dependency versions
for repeatable runs. You can run the command from:

- SQL files and SQL worksheets.
- Tasks and other Snowflake executables.
- External orchestrators that issue SQL (for example, Airflow, Prefect, Dagster, or CI/CD systems).

The compute type, runtime, dependencies, external access integrations, and secrets are defined in the `code_bundle.yml` specification. You
can change the specification for a single run with the `WITH SPECIFICATION` clause, which is merged over the stored specification.

Important

Before triggering a non-interactive run of a notebook, ensure that your notebook sets its execution context (database and schema) or uses fully qualified
object names. For more information, see [Editing and running notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-edit-run).

See also:
:   [CREATE CODE BUNDLE](/sql-reference/sql/create-code-bundle), [ALTER CODE BUNDLE](/sql-reference/sql/alter-code-bundle), [DESCRIBE CODE BUNDLE](/sql-reference/sql/desc-code-bundle),
    [SHOW CODE BUNDLES](/sql-reference/sql/show-code-bundles), [DROP CODE BUNDLE](/sql-reference/sql/drop-code-bundle), [CODE\_BUNDLE\_HISTORY](/sql-reference/functions/code_bundle_history),
    [CREATE TASK](/sql-reference/sql/create-task), [`code_bundle.yml` reference](/developer-guide/code-bundles/code-bundle-yml-reference),
    [Run ML Jobs with Code Bundles](/developer-guide/code-bundles/ml-code-bundles),
    [Submit Spark jobs on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle)

## Syntax

Run a Code Bundle:

Copy code

```
EXECUTE CODE BUNDLE <name>
  ENTRYPOINT = '<entrypoint>'
  [ ARGUMENTS = ( '<arg>' [ , '<arg>' ... ] ) ]
  [ EXECUTION_NAME = '<execution_name>' ]
  [ WITH SPECIFICATION $$ <yaml_spec> $$ ]
  [ INTO :<variable> ]
```

Run source files without creating a Code Bundle (anonymous run):

Copy code

```
EXECUTE CODE BUNDLE FROM '<source>'
  ENTRYPOINT = '<entrypoint>'
  [ ARGUMENTS = ( '<arg>' [ , '<arg>' ... ] ) ]
  [ EXECUTION_NAME = '<execution_name>' ]
  WITH SPECIFICATION $$ <yaml_spec> $$
  [ INTO :<variable> ]
```

## Required parameters

`name`
:   Identifier of the Code Bundle to run. Mutually exclusive with `FROM`.

    Must reference an existing Code Bundle created with [CREATE CODE BUNDLE](/sql-reference/sql/create-code-bundle). The run uses the Code
    Bundle’s default version.

    Must be fully qualified unless it resides in the current database and schema.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`FROM 'source'`
:   Runs source files directly, without creating a Code Bundle. Mutually exclusive with `name`. An
    anonymous run requires `WITH SPECIFICATION`, and the inline specification is the whole configuration: a `code_bundle.yml` file in the source
    location is ignored.

    The source you can use depends on the bundle type, compute type, and language in the inline specification:

    | Specification | Source |
    | --- | --- |
    | `type: custom`, `compute_type: warehouse`, `language: python` | A stage directory that contains the entrypoint file, for example `'@my_db.my_schema.my_stage/jobs'`. A `.jar` file is rejected. |
    | `type: custom`, `compute_type: warehouse`, `language: java` or `scala` | The stage path of the JAR file that contains the main class, for example `'@my_db.my_schema.my_stage/app/app.jar'`. A directory is rejected. Add other JAR files with `properties.java_dependencies.jars`; JAR files next to the main JAR aren’t added to the classpath. |
    | `type: custom`, `compute_type: compute_pool` | A workspace path, for example `'snow://workspace/USER$.PUBLIC."my_workspace"/versions/live'`. Stages aren’t supported. For a shared workspace, use a committed version; `versions/live` isn’t supported. |
    | `type: spark` | For Scala or Java, the stage path of the `.jar` file. For Python, the stage directory that contains the entrypoint file, with no trailing slash. See [Submit Spark jobs on Snowflake](/developer-guide/snowpark-connect/snowpark-connect-submit-code-bundle#submit-with-sql). |

    Expand

    Show lessSee more

`ENTRYPOINT = 'entrypoint'`
:   Specifies what Snowflake runs. The form depends on the language:

    - **Python script:** the path of a `.py` file, relative to the bundle root (for example, `main.py` or `jobs/main.py`). The file runs as a
      script, as with `python main.py`.
    - **Python method:** a `.py` file and the name of a function in it, separated by a colon (for example, `main.py:run`). Snowflake imports the
      file and calls the function, instead of running the file as a script, so code under `if __name__ == "__main__":` doesn’t run. The function’s
      return value becomes the run’s [return value](#label-execute-code-bundle-output).
    - **Notebook:** the path of a `.ipynb` file (for example, `notebooks/train.ipynb`). Notebooks run only on compute pools (Container Runtime).
    - **Java or Scala:** the fully qualified name of a class that defines `public static void main(String[] args)` (Java) or
      `def main(args: Array[String]): Unit` (Scala), for example `com.example.MyApp`. Calling another method of the class isn’t supported.
    - **Spark:** for Scala or Java, the fully qualified main class; for Python, the `.py` file name.

## Optional parameters

`ARGUMENTS = ( 'arg' [ , 'arg' ... ] )`
:   Passes one or more string arguments to the entrypoint at runtime. Arguments are useful for making logic dynamic (for example, selecting an
    environment such as `--env prod`).

    Specify each argument as a separate quoted string in the list:

    - In a Python entrypoint, the arguments appear in `sys.argv`: `sys.argv[0]` is the entrypoint name, `sys.argv[1]` is the first argument,
      and so on.
    - In a Java or Scala entrypoint, the arguments are passed to `main` as the `String[]` argument.

    Each value must be a string literal or a [SQL variable](/sql-reference/session-variables) reference such as `:my_var`.
    Function calls and other expressions aren’t supported. For an example of passing values computed at runtime, see
    [Pass arguments computed at runtime](#label-execute-code-bundle-dynamic-arguments).

    Only strings are supported; other data types (such as integers or Booleans) are interpreted as NULL.

    The `ARGUMENTS` syntax differs between the two commands: `EXECUTE CODE BUNDLE` takes a parenthesized list of strings, while
    [EXECUTE NOTEBOOK PROJECT](/sql-reference/sql/execute-notebook-project) takes a single string.

    Example:

    Copy code

    ```
    ARGUMENTS = ('--env', 'prod')
    ```

`EXECUTION_NAME = 'execution_name'`
:   A name for this run. Snowflake records it with the run, so you can find the run later by name, for example with
    `EXECUTION_NAME => '<execution_name>'` in [CODE\_BUNDLE\_HISTORY](/sql-reference/functions/code_bundle_history). The name doesn’t have to be
    unique. If you omit it, the run has no execution name.

    Execution names are most useful for anonymous runs, which have no Code Bundle name to filter on.

`WITH SPECIFICATION $$ yaml_spec $$`
:   Provides a `code_bundle.yml` specification inline, for this run only. The stored Code Bundle isn’t changed.

    - **Running a Code Bundle by name:** the inline specification is merged over the stored `code_bundle.yml`. Name only the fields you want to
      change; every other field keeps its stored value. For the merge rules, see
      [How WITH SPECIFICATION is merged](#label-execute-code-bundle-spec-merge).
    - **Anonymous run (`FROM`):** the inline specification is required and is the whole configuration. It must include `type` and
      `compute_type`, and every other field the run needs.

    The merged (or inline) specification is validated with the same rules as a `code_bundle.yml` file, so an invalid combination fails with the
    same error. For the fields, see the [`code_bundle.yml` reference](/developer-guide/code-bundles/code-bundle-yml-reference).

`INTO :variable`
:   In [Snowflake Scripting](/developer-guide/snowflake-scripting/index), assigns the run’s `RETURN_VALUE` to a variable. Declare the variable as
    `VARCHAR`. See [Capture the return value in a variable](#label-execute-code-bundle-into).

## Output

Note

Before the [RETURN\_VALUE behavior change](/release-notes/bcr-bundles/un-bundled/bcr-code-bundles-return-value), a successful run returned
a single column named `status` or `result` that contained a success message, such as `Statement executed successfully.` If your code or
tools read that column, update them.

A successful run returns one row with one column:

| Column | Data type | Description |
| --- | --- | --- |
| `RETURN_VALUE` | VARCHAR | The value that the run returned, or NULL. For a notebook on a compute pool, the value passed to `notebook.exit(value)`. For a Python method entrypoint (`file.py:method`), the value that the method returns. A Python `str` is returned as is; any other value is returned as JSON text, as produced by `json.dumps()` with its default settings (for example, `{"rows_loaded": 42}`, with non-ASCII characters escaped). Every other run returns NULL, including a Python script entrypoint and a Java or Scala entrypoint. |

Expand

Show lessSee more

`RETURN_VALUE` is also NULL in the following cases:

- The statement returns before the run finishes, for example when the run is executed asynchronously.
- The stages that Snowflake uses to cache notebook results in your account aren’t encrypted with `SNOWFLAKE_FULL` encryption.

On a compute pool, including notebook runs, returning a value requires [Container Runtime 3.0](/developer-guide/container-runtime/version-3) or later. Container Runtime 2.x
versions don’t support return values.

A return value that can’t be encoded as JSON fails the run with a `ReturnValueError`. On a compute pool, including notebook runs, the
encoded value can be at most 16 MiB; a larger value fails the run with a `ReturnValueError`. On a warehouse, the size limits for
stored procedure return values apply.

If the run fails, the command raises an error and returns no row. Decide whether a run succeeded from whether the statement raises an error,
not from `RETURN_VALUE`. To review past runs, use the [CODE\_BUNDLE\_HISTORY](/sql-reference/functions/code_bundle_history) table function.

## How WITH SPECIFICATION is merged

When you run a Code Bundle by name, the inline specification is applied as a patch over the stored `code_bundle.yml` (the same convention as
an RFC 7386 JSON merge patch): fields you name override the stored value, and fields you don’t name are inherited. How a field is merged
depends on its shape:

| Field shape | Examples | Behavior |
| --- | --- | --- |
| Scalar | `runtime_version`, `compute_type`, `requirements_file` | The inline value replaces the stored value. |
| Object or map | `compute_options`, `properties`, `stage_mounts`, `spark_conf` | Merged key by key: keys you name override the stored keys, and other stored keys are kept. |
| Empty object (`{}`) | Any object field | Changes nothing; the stored object is kept. |
| List | `secrets`, `external_access_integrations`, `artifact_repositories`, `env_vars`, dependency lists | The inline list replaces the whole stored list. To add one item, restate the full list. |
| `null` | Any field | Removes the field for this run. |

Expand

Show lessSee more

`env_vars` is a list, so naming one environment variable inline drops the other stored variables for that run. Restate every variable that
the run needs.

For example, the stored `code_bundle.yml` contains:

Copy code

```
bundle:
  type: custom
  compute_type: warehouse
  language: python
  compute_options:
    runtime_version: '3.10'
  secrets:
    - my_db.my_schema.api_key
```

The following statement changes only the Python version:

Copy code

```
EXECUTE CODE BUNDLE my_bundle
  ENTRYPOINT = 'main.py'
  WITH SPECIFICATION $$
bundle:
  compute_options:
    runtime_version: '3.11'
$$;
```

The specification used for the run is:

Copy code

```
bundle:
  type: custom
  compute_type: warehouse
  language: python
  compute_options:
    runtime_version: '3.11'   # from WITH SPECIFICATION
  secrets:
    - my_db.my_schema.api_key # inherited from code_bundle.yml
```

## Access control requirements

The role that runs the command must have the following privileges:

- **To run a Code Bundle by name:** OWNERSHIP or USAGE on the Code Bundle, and USAGE on the database and schema that contain it.
- **For an anonymous run:** read access to the `FROM` source, such as READ on an internal stage or access to the workspace.
- **For `compute_type: warehouse`:** USAGE on the current warehouse of the session. The run uses that warehouse.
- **For `compute_type: compute_pool`:** USAGE or OWNERSHIP on the compute pool, and USAGE on the query warehouse.
- **For objects referenced in the specification:**
  - READ or OWNERSHIP on each secret. USAGE on a secret isn’t sufficient.
  - USAGE or OWNERSHIP on each external access integration and artifact repository.
  - Read access to the stages in `stage_mounts` and to the stages that hold `properties.java_dependencies.jars`.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The command is synchronous: it returns when the run finishes. The query ID of the statement identifies the run in
  [CODE\_BUNDLE\_HISTORY](/sql-reference/functions/code_bundle_history) (`QUERY_ID => '<query_id>'`) and in the event table.
- To run the command without waiting for the run to finish, submit it asynchronously from your client (for example,
  `snow bundle execute --async` or `execute_async()` in the Python connector), then check the run’s status with its query ID. An asynchronous
  run returns NULL in `RETURN_VALUE`.
- You can’t run the `EXECUTE CODE BUNDLE` command from a notebook cell.
- You can call `EXECUTE CODE BUNDLE` from tasks, enabling runs as part of larger workflows. For details, see
  [Supported invocation contexts](#label-execute-code-bundle-invocation-contexts).
- Run history and run result visibility for executions triggered by this command depends on the viewing role’s Code Bundle privileges and `IMPERSONATE` privilege over the initiating user. For details, see [Run history and result visibility](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule#label-nb-in-ws-schedule-run-visibility).
- For an anonymous run from a workspace, if the workspace changes while Snowflake reads it, the run fails with error 099139. Run the
  statement again.

### Supported invocation contexts

`EXECUTE CODE BUNDLE` runs with caller’s rights, so it’s only supported in contexts that preserve the caller’s identity.
The following table shows where you can run the command:

| Context | Supported | Notes |
| --- | --- | --- |
| SQL worksheet or SQL file | Yes | Runs as the calling user. |
| Task body | Yes | Supported both as a single-statement body and inside a `BEGIN ... END` [Snowflake Scripting](/developer-guide/snowflake-scripting/index) block. |
| Stored procedure with `EXECUTE AS CALLER` | Yes | The procedure runs with the caller’s privileges. |
| Stored procedure with `EXECUTE AS OWNER` | No | Owner’s rights procedures can’t run the command. Use `EXECUTE AS CALLER` instead. |
| Stored procedure with `EXECUTE AS RESTRICTED CALLER` | Only with FULL MANAGEMENT | The caller must grant the FULL MANAGEMENT [high-level caller privilege](/developer-guide/restricted-callers-rights/high-level-caller-privileges). The run doesn’t apply [restricted caller’s rights](/developer-guide/restricted-callers-rights) semantics. |
| Streamlit app | No | Streamlit in Snowflake apps run with [owner’s rights](/developer-guide/streamlit/object-management/owners-rights) by default, and the [restricted caller’s rights](/developer-guide/streamlit/features/restricted-callers-rights) option isn’t supported by this command. |
| Notebook cell | No | Nested execution isn’t supported. |

Expand

Show lessSee more

## Examples

Run a Code Bundle:

Copy code

```
EXECUTE CODE BUNDLE my_bundle
  ENTRYPOINT = 'main.py';
```

Run a Code Bundle with arguments and an execution name:

Copy code

```
EXECUTE CODE BUNDLE my_bundle
  ENTRYPOINT = 'jobs/main.py'
  ARGUMENTS = ('--source-table', 'RAW_SALES', '--output-table', 'SALES_AGG')
  EXECUTION_NAME = 'nightly_sales_agg';
```

Run a notebook packaged in a Code Bundle (runs on a compute pool):

Copy code

```
EXECUTE CODE BUNDLE "sales_detection_db"."schema"."nightly_training"
  ENTRYPOINT = 'notebook_file.ipynb'
  ARGUMENTS = ('--env', 'prod');
```

Call a function in a Python file and return its result. If `main.py` defines `def run(): return {"rows_loaded": 42}`, the statement returns
`{"rows_loaded": 42}` in `RETURN_VALUE`:

Copy code

```
EXECUTE CODE BUNDLE my_bundle
  ENTRYPOINT = 'main.py:run';
```

Change one setting for a single run, keeping the rest of the stored specification:

Copy code

```
EXECUTE CODE BUNDLE my_bundle
  ENTRYPOINT = 'main.py'
  WITH SPECIFICATION $$
bundle:
  compute_options:
    runtime_version: '3.12'
$$;
```

Run Python files from a stage on a warehouse, without creating a Code Bundle:

Copy code

```
EXECUTE CODE BUNDLE FROM '@my_db.my_schema.my_stage/jobs'
  ENTRYPOINT = 'main.py'
  EXECUTION_NAME = 'adhoc_backfill'
  WITH SPECIFICATION $$
bundle:
  type: custom
  compute_type: warehouse
  language: python
  compute_options:
    runtime_version: '3.11'
$$;
```

Run a Java application from a JAR file on a warehouse, without creating a Code Bundle:

Copy code

```
EXECUTE CODE BUNDLE FROM '@my_db.my_schema.my_stage/app/app.jar'
  ENTRYPOINT = 'com.example.MyApp'
  ARGUMENTS = ('--label', 'value with space', '42')
  WITH SPECIFICATION $$
bundle:
  type: custom
  compute_type: warehouse
  language: java
  compute_options:
    runtime_version: '17'
  properties:
    java_dependencies:
      jars:
        - '@my_db.my_schema.libs/utils-1.0.jar'
$$;
```

Run files from a workspace on a compute pool, without creating a Code Bundle:

Copy code

```
EXECUTE CODE BUNDLE FROM 'snow://workspace/USER$.PUBLIC."my_workspace"/versions/live'
  ENTRYPOINT = 'train.py'
  WITH SPECIFICATION $$
bundle:
  type: custom
  compute_type: compute_pool
  language: python
  compute_options:
    compute_pool: system_compute_pool_cpu
    query_warehouse: my_wh
    runtime_version: 'V2.9-CPU-PY3.12'
$$;
```

### Capture the return value in a variable

In a Snowflake Scripting block, use `INTO` to assign `RETURN_VALUE` to a variable, then use it in later statements:

Copy code

```
DECLARE
  run_output VARCHAR;
BEGIN
  EXECUTE CODE BUNDLE my_db.my_schema.my_bundle
    ENTRYPOINT = 'main.py:run'
    INTO :run_output;
  RETURN PARSE_JSON(:run_output):rows_loaded;
END;
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
