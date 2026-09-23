# Understanding orchestration for dbt Projects on Snowflake

Orchestration is the process of scheduling, sequencing, and monitoring your deployed dbt project object executions. Every orchestration
approach for dbt Projects on Snowflake uses the same underlying mechanism: the
[EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project) SQL command. Whether you use Snowflake tasks
or an external tool like Apache Airflow, the orchestrator’s job is to call that command at the right time,
in the right order, with the right parameters.

You have two paths:

- **Snowflake tasks**: Native scheduling with no external infrastructure. Best for teams that want to reduce operational overhead and standardize on Snowflake.
- **External orchestrators** (Apache Airflow, Prefect, Dagster): For teams with existing orchestration
  infrastructure or cross-system workflows that extend beyond Snowflake.

If multiple schedules or workflow branches need to execute the same dbt project object at the same
time, Snowflake recommends `WRITEBACK = FALSE`. Snowflake stores the per-query result artifacts and archive regardless of this setting.
For retrieval instructions, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).
If writeback is required, use distinct, non-overlapping target and log directories. For examples, see
[Run a dbt project object concurrently](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod#label-dbt-project-concurrent-executions).

## Choosing an orchestration approach

| Consideration | Snowflake tasks | Apache Airflow |
| --- | --- | --- |
| Infrastructure | None. Fully managed by Snowflake. | Self-managed Airflow cluster or managed service. |
| Monitoring | Built-in Snowsight run history, event table, and per-query dbt artifact access. | Airflow UI, plus custom integrations. |
| Scheduling | CRON expression, fixed interval, `AFTER` (task chaining), or triggered when a stream has new data. | Airflow scheduler with DAG-level configuration. |
| Multi-step pipelines | `AFTER` clause chains tasks into a graph. | DAG dependencies with trigger rules (for example, all success, or one failed). |
| Dynamic parameters | `ENV_VARS` on `EXECUTE DBT PROJECT`, `--vars` in the `ARGS` string of `EXECUTE DBT PROJECT`, or dynamic per-run values from task `CONFIG`. See [Pass dynamic configuration at run time](#label-dbt-orchestration-pass-dynamic-config). | [Airflow Jinja templates](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html#jinja-templating) interpolated into SQL or CLI commands. |
| Cost | Warehouse credits for task execution only. | Airflow infrastructure cost plus warehouse credits. |
| Best for | Teams that are Snowflake-native, starting fresh, or consolidating tools. | Teams with existing Airflow DAGs or cross-system workflows. |

Expand

Show lessSee more

## Built-in monitoring at the dbt project object level

Regardless of how a dbt project object is executed, you get the same observability
and management capabilities. These features are tied to the deployed dbt project
object itself, not to the orchestrator:

- **Run history in Snowsight**: In the navigation menu, select **Transformation** > **dbt Projects** to view
  run history, task graphs, and query details for every execution of the dbt project object, whether
  triggered by a task, Airflow, or an ad-hoc SQL call.
- **Project DAG with column-level lineage**: Browse the model dependency graph from the project details page,
  inspect compiled SQL, and trace column-level lineage powered by Snowflake Horizon Catalog.
- **Event table logging and tracing**: Snowflake writes log entries and trace spans for each execution to
  the account’s active event table. [Query the event table](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-event-table) live during a run or after completion to diagnose
  failures.
- **Programmatic access to dbt artifacts**: Use
  [SYSTEM$LOCATE\_DBT\_ARTIFACTS](/sql-reference/functions/system_locate_dbt_artifacts) with a known
  execution query ID to retrieve `manifest.json`, `run_results.json`, and log files programmatically.
- **Cortex Code integration**: Use Cortex Code to inspect the files of your deployed dbt project object, debug production failures,
  and answer questions about your pipeline.

For details on enabling and using these features, see
[Monitor dbt Projects](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability) and
[View and manage information for existing dbt Projects](/user-guide/data-engineering/dbt-projects-on-snowflake-manage).

## Orchestrate with Snowflake tasks

Snowflake [tasks](/user-guide/tasks-intro) provide native scheduling for dbt project object execution. You don’t
need to provision or manage any external infrastructure. Create a task, set a schedule, and Snowflake
handles the rest.

### Benefits

- No infrastructure to provision or manage.
- Built-in monitoring in Snowsight with run history, task graphs, and query-level execution details.
- RBAC-governed scheduling: control who can create, own, and resume tasks.
- Built-in retry logic and alerting through [task graphs](/user-guide/tasks-graphs).

Tasks can also make external calls (for example, triggering a downstream API) through a stored procedure,
but this requires configuring [external access integrations](/developer-guide/external-network-access/creating-using-external-network-access)
and network policies.

### Schedule from Snowsight

You can create, view, and manage tasks to run a deployed dbt project object on a schedule from
two places in Snowsight: Workspaces or the object details page of the dbt project object. For
instructions, see
[Schedule execution of dbt project objects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-schedule-project-execution).

### Create a simple scheduled task

The following example creates a task that runs your deployed dbt project object every six hours:

Copy code

```
CREATE OR ALTER TASK my_db.my_schema.run_dbt_every_6h
  WAREHOUSE = transform_wh
  SCHEDULE = '360 minutes'
AS
  EXECUTE DBT PROJECT my_db.my_schema.my_project ARGS='run --target prod';
```

Resume the task to activate it:

Copy code

```
ALTER TASK my_db.my_schema.run_dbt_every_6h RESUME;
```

### Create a task graph with multiple steps

Use the `AFTER` clause to chain tasks into a [task graph](/user-guide/tasks-graphs). The following
example creates a two-step pipeline that runs models first, then runs tests after the models complete:

Copy code

```
-- Run all models in DAG order
CREATE OR ALTER TASK my_db.my_schema.run_dbt_models
  WAREHOUSE = transform_wh
  SCHEDULE = '360 minutes'
  AS
    EXECUTE DBT PROJECT my_db.my_schema.my_project ARGS='run --target prod';

-- Run tests after models complete successfully
CREATE OR ALTER TASK my_db.my_schema.run_dbt_tests
  WAREHOUSE = transform_wh
  AFTER my_db.my_schema.run_dbt_models
  AS
    EXECUTE DBT PROJECT my_db.my_schema.my_project ARGS='test --target prod';

-- Resume the root task to activate the graph
ALTER TASK my_db.my_schema.run_dbt_models RESUME;
```

When the root task fires, it runs all models first. Afterwards, the next task
runs automatically. If the first task fails, the next task doesn’t execute.

### Run a dbt project object concurrently from a task graph

Task graph branches can run independent data slices against the same dbt project object at the same
time. The following example creates two child tasks that start after the same root task. Both
executions use `WRITEBACK = FALSE`, so they don’t update target and log artifacts on the live
version:

Copy code

```
-- Start the task graph on a schedule
CREATE OR ALTER TASK my_db.my_schema.run_dbt_slices
  WAREHOUSE = transform_wh
  SCHEDULE = '360 minutes'
  AS
    SELECT 1;

-- Run the finance data slice
CREATE OR ALTER TASK my_db.my_schema.run_dbt_finance
  WAREHOUSE = transform_wh
  AFTER my_db.my_schema.run_dbt_slices
  AS
    EXECUTE DBT PROJECT my_db.my_schema.my_project
      ARGS = 'run --select tag:finance --target prod'
      WRITEBACK = FALSE;

-- Run the sales data slice concurrently
CREATE OR ALTER TASK my_db.my_schema.run_dbt_sales
  WAREHOUSE = transform_wh
  AFTER my_db.my_schema.run_dbt_slices
  AS
    EXECUTE DBT PROJECT my_db.my_schema.my_project
      ARGS = 'run --select tag:sales --target prod'
      WRITEBACK = FALSE;

-- Resume child tasks before the root task
ALTER TASK my_db.my_schema.run_dbt_finance RESUME;
ALTER TASK my_db.my_schema.run_dbt_sales RESUME;
ALTER TASK my_db.my_schema.run_dbt_slices RESUME;
```

When the root task runs, the two child tasks execute the finance and sales data slices concurrently.
Snowflake stores the per-query result artifacts and archive regardless of the `WRITEBACK` setting.
For retrieval instructions, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).

### Pass dynamic configuration at run time

Store a default configuration on the task with `CONFIG`, then map those values into the dbt project’s environment variables so you can change them per run without editing the task. Because `ENV_VARS` accepts a `{{ select ... }}` template that resolves to a `VARCHAR`, you can read a configuration value into each variable with [SYSTEM$GET\_TASK\_GRAPH\_CONFIG](/sql-reference/functions/system_get_task_graph_config):

Copy code

```
CREATE OR ALTER TASK my_db.my_schema.run_dbt_configurable
  WAREHOUSE = transform_wh
  SCHEDULE = '360 minutes'
  CONFIG = $${"target_db": "analytics_prod", "run_date": "2026-07-01"}$$
AS
  EXECUTE DBT PROJECT my_db.my_schema.my_project
    ARGS = 'run --target prod'
    ENVIRONMENT = 'prod'
    ENV_VARS = (
      'DBT_TARGET_DB' = '{{ select SYSTEM$GET_TASK_GRAPH_CONFIG(\'target_db\')::string }}',
      'DBT_RUN_DATE'  = '{{ select SYSTEM$GET_TASK_GRAPH_CONFIG(\'run_date\')::string }}'
    );
```

When you run the task manually, pass `USING CONFIG` to override the defaults for that single execution. Snowflake merges the dynamic configuration into the task’s default `CONFIG`, and the new values flow through `SYSTEM$GET_TASK_GRAPH_CONFIG` into the dbt project’s environment variables:

Copy code

```
EXECUTE TASK my_db.my_schema.run_dbt_configurable
  USING CONFIG = $${"target_db": "analytics_dev", "run_date": "2026-07-15"}$$;
```

Values resolve highest priority first: `ENV_VARS` on `EXECUTE DBT PROJECT` (or `--env-vars` in the CLI), then shell variables (with `--use-shell-env-vars`), then the active environment in `env.yml`. For the full `env.yml` precedence rules, see [Value precedence (highest to lowest)](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables#label-dbt-env-vars-value-precedence).

## Orchestrate with Apache Airflow

If your team already runs Apache Airflow for other pipelines, you can integrate dbt Projects on Snowflake
into your existing DAGs. This guide uses Airflow as the example, but any tool that can issue SQL to Snowflake on a schedule can orchestrate dbt project object executions.

### When to use Airflow

- Your team already manages Airflow for other data pipelines.
- dbt execution or Snowflake platform is one step in a larger cross-system workflow (for example, ingest data from an external
  source, then run dbt, then trigger a downstream system).
- You need Airflow-specific features like complex branching or external sensors.

If your team is just getting started with dbt or orchestration, Snowflake tasks are a simpler
option with no external infrastructure to manage.

### Prerequisites

Before you begin, make sure you have:

- A deployed dbt project object on Snowflake.
- Apache Airflow with the `apache-airflow-providers-snowflake` package installed.
- A Snowflake connection configured in Airflow with the account, user, authentication credentials (key pair
  recommended for production), warehouse, database, schema, and role.
- The role used in the Airflow connection must have the EXECUTE DBT PROJECT privilege on the dbt project
  object. For more information, see
  [Access control for dbt Projects](/user-guide/data-engineering/dbt-projects-on-snowflake-access-control).

### Configure the Snowflake connection in Airflow

When setting up the Snowflake connection in your Airflow admin panel or environment, configure the
following fields:

- **Connection type**: Snowflake
- **Account**: Your Snowflake account identifier (for example, `myorg-myaccount`)
- **Login**: The user or service account name
- **Authentication**: Key pair authentication is recommended for production. You can also use a password.
- **Warehouse**: The warehouse to use for the `EXECUTE DBT PROJECT` command
- **Database**: The database containing your dbt project object
- **Schema**: The schema containing your dbt project object
- **Role**: A role with the EXECUTE DBT PROJECT privilege on the dbt project object

Tip

Use a dedicated service account (for example, `airflow_service_user`) for production DAGs. This keeps
task privileges governed in one place and prevents broken pipelines when team members leave.

### Option 1: Use SQLExecuteQueryOperator (recommended)

The `SQLExecuteQueryOperator` from the Airflow Snowflake provider runs SQL statements directly through a
Snowflake connection. This is the simplest approach because it requires only a SQL connection with no
additional CLI installation.

#### Simple DAG: run then test

The following DAG runs dbt models daily at 6 AM, then runs tests after the models complete:

Copy code

```
from datetime import datetime
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

with DAG(
    dag_id="dbt_project_daily",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    default_args={"conn_id": "snowflake_default"},
) as dag:

    run_models = SQLExecuteQueryOperator(
        task_id="dbt_run",
        sql="EXECUTE DBT PROJECT my_db.my_schema.my_project ARGS='run --target prod';",
    )

    run_tests = SQLExecuteQueryOperator(
        task_id="dbt_test",
        sql="EXECUTE DBT PROJECT my_db.my_schema.my_project ARGS='test --target prod';",
    )

    run_models >> run_tests
```

#### Run a dbt project object concurrently

The following DAG runs two independent data slices from the same dbt project object. Because the
tasks don’t have a dependency between them, Airflow can run them concurrently. Both executions use
`WRITEBACK = FALSE`, so they don’t update target and log artifacts on the live version:

Copy code

```
from datetime import datetime
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

with DAG(
    dag_id="dbt_project_concurrent_slices",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    max_active_tasks=2,
    default_args={"conn_id": "snowflake_default"},
) as dag:

    run_finance = SQLExecuteQueryOperator(
        task_id="dbt_run_finance",
        sql=(
            "EXECUTE DBT PROJECT my_db.my_schema.my_project "
            "ARGS='run --select tag:finance --target prod' "
            "WRITEBACK = FALSE;"
        ),
    )

    run_sales = SQLExecuteQueryOperator(
        task_id="dbt_run_sales",
        sql=(
            "EXECUTE DBT PROJECT my_db.my_schema.my_project "
            "ARGS='run --select tag:sales --target prod' "
            "WRITEBACK = FALSE;"
        ),
    )
```

Snowflake stores the per-query result artifacts and archive regardless of the `WRITEBACK` setting.
For retrieval instructions, see [Access dbt artifacts and logs programmatically](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability#label-dbt-projects-artifacts-and-logs).

#### Pass per-run variables with ENV\_VARS

To override individual variables for a single run, add `ENVIRONMENT` and `ENV_VARS` to the `EXECUTE DBT PROJECT` statement. Airflow replaces macros like `{{ data_interval_start }}` with their run-time values before sending the statement to Snowflake:

Copy code

```
from datetime import datetime
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

with DAG(
    dag_id="dbt_project_per_run_vars",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    default_args={"conn_id": "snowflake_default"},
) as dag:

    run_models = SQLExecuteQueryOperator(
        task_id="dbt_run",
        sql=(
            "EXECUTE DBT PROJECT my_db.my_schema.my_project "
            "ARGS='run --target prod' "
            "ENVIRONMENT='prod' "
            "ENV_VARS=("
            "'DBT_RUN_START' = '{{ data_interval_start }}', "
            "'DBT_RUN_END' = '{{ data_interval_end }}');"
        ),
    )
```

Airflow substitutes the macros at run time, so Snowflake receives ordinary string values (for example, `'DBT_RUN_START' = '2026-07-15T00:00:00+00:00'`). You don’t need the `{{ select ... }}` SQL template here. That template is only for reading values at run time from a source like `SYSTEM$GET_TASK_GRAPH_CONFIG`, as in the [Snowflake task example](#label-dbt-orchestration-pass-dynamic-config). For the full `ENV_VARS` syntax and precedence rules, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

#### Sensor-triggered DAG: wait for upstream data

The following DAG uses an S3 sensor to wait for a file to land in an external bucket before
running the dbt project. This could be new source data landing from an ingestion pipeline or an
Iceberg catalog update. Teams often choose external orchestrators like Airflow when they need to
react to events in external systems that Snowflake tasks can’t observe natively.

Copy code

```
from datetime import datetime
from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

with DAG(
    dag_id="dbt_project_sensor_triggered",
    start_date=datetime(2026, 1, 1),
    schedule="0 */2 * * *",
    catchup=False,
    default_args={"conn_id": "snowflake_default"},
) as dag:

    wait_for_file = S3KeySensor(
        task_id="wait_for_upstream_file",
        bucket_name="my-data-lake",
        bucket_key="incoming/events/{{ ds }}/data.parquet",
        aws_conn_id="aws_default",
        poke_interval=60,
        timeout=7200,
        mode="reschedule",  # Free up the worker slot between pokes
    )

    run_models = SQLExecuteQueryOperator(
        task_id="dbt_run",
        sql="EXECUTE DBT PROJECT my_db.my_schema.my_project ARGS='run --target prod';",
    )

    run_tests = SQLExecuteQueryOperator(
        task_id="dbt_test",
        sql="EXECUTE DBT PROJECT my_db.my_schema.my_project ARGS='test --target prod';",
    )

    wait_for_file >> run_models >> run_tests
```

### Option 2: Use BashOperator with Snowflake CLI

If the Snowflake CLI is already installed in your Airflow worker environment, you can use the `BashOperator`
to call `snow dbt execute` directly. This approach is useful when you want CLI-native features like
`--run-async`.

Note

The BashOperator approach requires Snowflake CLI version 3.13.0 or later installed in the Airflow
worker environment. The `--connection` flag specifies a named connection defined in
`~/.snowflake/config.toml`. In production, commit only an empty connection skeleton and supply
credentials through environment variables using the format `SNOWFLAKE_CONNECTIONS_<NAME>_<PARAMETER>`. These are Snowflake CLI connection variables, distinct from the dbt project environment variables you configure in `env.yml`.
For details on defining connections, see
[Managing Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections).

#### Basic example

Copy code

```
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="dbt_project_cli",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
) as dag:

    run_models = BashOperator(
        task_id="dbt_run",
        bash_command="snow dbt execute --connection prod_conn my_project run --target prod",
    )

    run_tests = BashOperator(
        task_id="dbt_test",
        bash_command="snow dbt execute --connection prod_conn my_project test --target prod",
    )

    run_models >> run_tests
```

#### Pass shell environment variables with `--use-shell-env-vars`

Use this approach when your Airflow tasks already export `DBT_`-prefixed variables, or when you want per-run Airflow template values, such as the run’s data interval, to flow into dbt while keeping static configuration in `env.yml`. Pass a `DBT_`-prefixed `env` dict on the operator and add `--use-shell-env-vars` to `snow dbt execute`:

Copy code

```
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="dbt_project_cli_env_vars",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
) as dag:

    run_models = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "snow dbt execute --use-shell-env-vars --connection prod_conn "
            "my_project run --target prod"
        ),
        env={
            "DBT_DATA_INTERVAL_START": "{{ data_interval_start }}",
            "DBT_DATA_INTERVAL_END": "{{ data_interval_end }}",
            "DBT_CURRENT_SCHEMA": "ANALYTICS_PROD",
        },
        append_env=True,
    )
```

When the run starts, Snowflake CLI resolves values highest priority first: `--env-vars`, then the `DBT_`-prefixed shell variables that `--use-shell-env-vars` pulls in, then the active environment in the project’s `env.yml`. Because this example passes no `--env-vars`, the Airflow shell variables win over any matching keys in `env.yml`. For the full syntax and precedence rules, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

Note

This example requires Snowflake CLI 3.21 or later for the `--use-shell-env-vars` flag. The CLI reads only shell variables prefixed with `DBT_` (excluding `DBT_ENV_SECRET_*`). Set `append_env=True` on the operator so the task inherits the worker’s environment: without it, `BashOperator` passes only the `env` dict to the subprocess, and `snow` (along with your `SNOWFLAKE_CONNECTIONS_*` credentials) would be missing from `PATH`.

## Considerations

- **Serverless tasks can’t execute dbt project objects:** You must specify a warehouse
  when creating a task that executes the EXECUTE DBT PROJECT command.
- **The two-role model applies regardless of orchestrator:** Every `EXECUTE DBT PROJECT` statement
  involves a calling role (the task owner or Airflow connection role) and the profile role from [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml` (which
  controls what the dbt run can access). For details, see the orchestration section in
  [Best practices for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#orchestration).
- **Align your warehouse configuration:** Use the same warehouse in both your task definition (or Airflow
  connection) and the target in `dbt_projects_profiles.yml` or `profiles.yml`. If the warehouses differ, both warehouses wake up for a single run.
