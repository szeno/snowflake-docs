# EXECUTE NOTEBOOK PROJECT

Note

Notebook Project Objects have been renamed to **Code Bundles**. The `NOTEBOOK PROJECT` grammar on this page continues to work, including inside existing tasks and schedules. For the current command and its new capabilities, see [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle) and [Snowflake Code Bundles](/developer-guide/code-bundles/code-bundles).

Executes a notebook stored in a notebook project (NPO). This command runs the notebook in a non-interactive (headless) mode and is useful for CI/CD
pipelines and other orchestrated workflows where you want to pass parameters or lock dependency versions for repeatable runs. The command can be run from:

- SQL files.
- Other Snowflake executables (Tasks).
- External orchestrators that issue SQL (for example, Airflow, Prefect, Dagster, CI/CD systems).

The command runs the notebook file you specify as `MAIN_FILE` using the runtime, compute pool, warehouse, and external access integrations you
configure.

Important

Before triggering a non-interactive run, ensure that your notebook sets its execution context (database and schema) or uses fully qualified
object names. For more information, see [Editing and running notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-edit-run).

See also:
[CREATE NOTEBOOK PROJECT](/sql-reference/sql/create-notebook-project), [CREATE TASK](/sql-reference/sql/create-task), [CI/CD workflow scenario](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-workflow-scenarios#label-nb-in-ws-schedule-scenario-b),
[Observability and logging for Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-observability-logging), [Running notebooks with parameters](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-parameters),
[Using secrets in Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-using-secrets)

## Syntax

Copy code

```
EXECUTE NOTEBOOK PROJECT <database_name>.<schema_name>.<project_name>
  MAIN_FILE = 'notebook.ipynb'
  COMPUTE_POOL = '<compute_pool_name>'
  QUERY_WAREHOUSE = '<warehouse_name>'
  RUNTIME = '<runtime_version>'
  [ ARGUMENTS = '<arg> [ <arg> ... ]' ]
  [ REQUIREMENTS_FILE = '<path/to/requirements.txt>' ]
  [ ARTIFACT_REPOSITORIES = ( <repository_name> [ , ... ] ) ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , ... ] ) ]
  [ SECRETS = ( <database_name>.<schema_name>.<secret_name> [ , ... ] ) ];
```

## Required parameters

`database_name.schema_name.project_name`
:   Fully qualified identifier of the notebook project to execute.

    Must reference an existing notebook project created with [CREATE NOTEBOOK PROJECT](/sql-reference/sql/create-notebook-project).

    Must be fully qualified unless it resides in the current DATABASE and SCHEMA.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`MAIN_FILE = 'notebook_file_name.ipynb'`
:   Specifies the main notebook file within the workspace to execute (`path/to/notebook.ipynb`).

    Must be an `.ipynb` notebook file located in the workspace referenced by the project.

    The path is relative to the workspace root.

`COMPUTE_POOL = 'compute_pool_name'`
:   Specifies the compute pool used when executing the notebook on a Container Runtime.

    Required when the notebook runtime uses Snowpark Container Services.

`QUERY_WAREHOUSE = 'warehouse_name'`
:   Specifies the virtual warehouse used for executing SQL and Snowpark queries from the notebook.

    Required if the notebook performs SQL or Snowpark operations and no warehouse is otherwise configured.

    When using container runtimes, the warehouse handles query pushdown; Python executes on the compute pool.

`RUNTIME = 'runtime_version'`
:   Specifies the runtime image or version for executing the notebook (for example, `'1.0'` or `'2.2-CPU-PY3.11'`).

    Determines the Python version and execution environment used for the notebook execution.

    Corresponds to a Container Runtime image (CPU or GPU) or warehouse runtime variant.

## Optional parameters

Depending on how the project and runtime are configured, you may need to set the following parameters. The descriptions below define their
purpose and typical usage.

`ARGUMENTS = 'arg [ arg ... ]'`
:   Optionally passes arguments to the notebook at runtime, which appear as command-line arguments in the `sys.argv` list.
    Arguments are useful for making notebook logic dynamic (for example, selecting an environment such as `--env prod`).

    Specify all arguments as a single quoted string, separating individual arguments with whitespace. In a Python cell,
    access the arguments using `sys.argv[0]` for the notebook name, `sys.argv[1]` for the first argument, and so on.

    The value must be a string literal or a [SQL variable](/sql-reference/session-variables) reference such as `:my_var`.
    Function calls and other expressions aren’t supported. For an example of passing a value computed at runtime, see
    [Pass arguments computed at runtime](#label-execute-notebook-project-dynamic-arguments).

    The value must be a string. Passing a non-string expression is interpreted as NULL.

    The `ARGUMENTS` syntax differs between the two commands: `EXECUTE NOTEBOOK PROJECT` takes a single string, while
    [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle) takes a parenthesized list of strings.

    Examples:

    Copy code

    ```
    ARGUMENTS = '--env prod';
    ```

    Copy code

    ```
    import sys
    print(sys.argv)
    ```

`REQUIREMENTS_FILE = '<path/to/requirements.txt>'`
:   Optionally specifies a `requirements.txt` file in a workspace or on a stage to pre-install exact versions of libraries (such as pandas
    or scikit-learn) and other Python dependencies before notebook execution. Pinning dependencies is critical for idempotency and helps
    make notebook runs more repeatable, reducing errors caused by changes in library versions. The file must be accessible to the executing role.

`EXTERNAL_ACCESS_INTEGRATIONS = ( integration_name [ , ... ] )`
:   Specifies one or more external access integrations that the notebook can use during execution.

    Required when the notebook makes outbound network calls (for example, to external APIs).

    Each integration name must reference an existing external access integration.

    Multiple external access integrations can be specified in a comma-separated list inside the parentheses.

    Example:

    Copy code

    ```
    EXTERNAL_ACCESS_INTEGRATIONS = (http_eai, s3_eai);
    ```

    Note

    The Snowflake-managed PyPI network rule `SNOWFLAKE.EXTERNAL_ACCESS.PYPI_RULE` is only accessible to the ACCOUNTADMIN role.
    Consequently, using this rule in an External Access Integration (EAI) for notebook objects or scheduled tasks may cause them to fail.
    To avoid this, create a user-defined network rule for PyPI and reference it in your external access integration. For more information,
    see [Snowflake-managed egress network rules](/user-guide/network-rules#label-snowflake-managed-egress-network-rules).

`SECRETS = ( database_name.schema_name.secret_name [ , ... ] )`
:   Optionally lists one or more [secrets](/sql-reference/sql/create-secret) that the notebook may read during execution
    (for example, API keys or OAuth tokens referenced from Snowpark or mounted files).

    Each entry must be a fully qualified secret name. Include this parameter (together with `EXTERNAL_ACCESS_INTEGRATIONS`) when the notebook performs
    authenticated outbound access that relies on secrets attached to the notebook service in Snowsight.

    For setup, UI scheduling, and Python examples, see [Using secrets in Notebooks in Workspaces](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-using-secrets).

## Access control requirements

The role executing `EXECUTE NOTEBOOK PROJECT` must have either OWNERSHIP or USAGE privileges on the notebook project object (NPO).

In addition, the executing role must have USAGE and MONITOR on the query warehouse, and USAGE or OWNERSHIP on:

- The compute pool.
- The database and schema containing the notebook project.
- Tasks, external access integrations, and secrets referenced by the command.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You can’t run the `EXECUTE NOTEBOOK PROJECT` command from a notebook cell.
- You can call `EXECUTE NOTEBOOK PROJECT` from tasks, enabling notebook runs as part of larger workflows. For details, see
  [Supported invocation contexts](#label-execute-notebook-project-invocation-contexts).
- Run history and run result visibility for executions triggered by this command depends on the viewing role’s NPO privileges and `IMPERSONATE` privilege over the initiating user. For details, see [Run history and result visibility](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-schedule#label-nb-in-ws-schedule-run-visibility).
- When you run a notebook using the `EXECUTE NOTEBOOK PROJECT` command:
  - Notebook code is executed on the compute pool specified by the COMPUTE\_POOL parameter using the runtime specified by the RUNTIME parameter.
  - SQL and Snowpark queries are executed using the warehouse specified by the QUERY\_WAREHOUSE parameter.

### Supported invocation contexts

`EXECUTE NOTEBOOK PROJECT` runs with caller’s rights, so it’s only supported in contexts that preserve the caller’s identity.
The following table shows where you can run the command:

| Context | Supported | Notes |
| --- | --- | --- |
| SQL worksheet or SQL file | Yes | Runs as the calling user. |
| Task body | Yes | Supported both as a single-statement body and inside a `BEGIN ... END` [Snowflake Scripting](/developer-guide/snowflake-scripting/index) block. |
| Stored procedure with `EXECUTE AS CALLER` | Yes | The procedure runs with the caller’s privileges. |
| Stored procedure with `EXECUTE AS OWNER` | No | Owner’s rights procedures can’t run the command. Use `EXECUTE AS CALLER` instead. |
| Stored procedure with `EXECUTE AS RESTRICTED CALLER` | No | Notebook projects don’t support [restricted caller’s rights](/developer-guide/restricted-callers-rights) yet. |
| Streamlit app | No | Streamlit in Snowflake apps run with [owner’s rights](/developer-guide/streamlit/object-management/owners-rights) by default, and the [restricted caller’s rights](/developer-guide/streamlit/features/restricted-callers-rights) option isn’t supported by this command. |
| Notebook cell | No | Nested execution isn’t supported. |

Expand

Show lessSee more

## Examples

Execute a notebook project:

Copy code

```
EXECUTE NOTEBOOK PROJECT "sales_detection_db"."schema"."DEFAULT_PROJ_B32BCFD4"
  MAIN_FILE = 'notebook_file.ipynb'
  COMPUTE_POOL = 'test_X_CPU'
  QUERY_WAREHOUSE = 'ENG_INFRA_WH'
  RUNTIME = 'V2.9-CPU-PY3.12'
  ARGUMENTS = '--env prod'
  REQUIREMENTS_FILE = 'path/to/requirements.txt'
  ARTIFACT_REPOSITORIES = (snowflake.snowpark.pypi_shared_repository)
  EXTERNAL_ACCESS_INTEGRATIONS = ('test_EAI')
  SECRETS = (sales_detection_db.schema.my_api_secret);
```

### Pass arguments computed at runtime

`ARGUMENTS` accepts a string literal or a SQL variable, but not a function call. To pass a value that’s computed at runtime,
assign it to a variable first inside a `BEGIN ... END` block, then reference the variable with a colon prefix.

The following task reads a value from its own [CONFIG](/sql-reference/sql/create-task) property with
[SYSTEM$GET\_TASK\_GRAPH\_CONFIG](/sql-reference/functions/system_get_task_graph_config) and passes it to the notebook:

Copy code

```
CREATE TASK my_db.my_schema.nightly_run
  WAREHOUSE = my_wh
  SCHEDULE = 'USING CRON 0 9 * * * America/Los_Angeles'
  CONFIG = $${"nb_arguments": "--env prod --threshold 0.85"}$$
AS
BEGIN
  LET nb_args VARCHAR := SYSTEM$GET_TASK_GRAPH_CONFIG('nb_arguments')::VARCHAR;
  EXECUTE NOTEBOOK PROJECT my_db.my_schema.my_project
    MAIN_FILE = 'notebook_file.ipynb'
    COMPUTE_POOL = 'system_compute_pool_cpu'
    QUERY_WAREHOUSE = 'my_wh'
    RUNTIME = 'V2.9-CPU-PY3.12'
    ARGUMENTS = :nb_args;
END;
```

Read the arguments in the notebook with `sys.argv`:

Copy code

```
import sys

# sys.argv[0] is the notebook name, so the arguments start at index 1.
print(sys.argv)  # ['notebook_file.ipynb', '--env', 'prod', '--threshold', '0.85']
```

The same pattern works with other values available at runtime, such as a predecessor task’s return value from
[SYSTEM$GET\_PREDECESSOR\_RETURN\_VALUE](/sql-reference/functions/system_get_predecessor_return_value) or a session variable
set with [SET](/sql-reference/sql/set).

Passing a function call directly to `ARGUMENTS` isn’t supported and fails to compile:

Copy code

```
-- Not supported.
ARGUMENTS = SYSTEM$GET_TASK_GRAPH_CONFIG('nb_arguments');
```
