# Using Apache Airflow™ with CoCo CLI

CoCo provides built-in support for Apache Airflow™, providing a natural language interface to manage DAGs, debug
failures, author pipelines, analyze data, and track lineage across your Airflow deployments.

## Capabilities

| Capability | Description | Example Prompt |
| --- | --- | --- |
| Pipeline Monitoring | Health checks, DAG inspection, connection and variable visibility, scheduling control | “Is my Airflow instance healthy?” |
| Run Management | Trigger DAGs on demand, wait for results, pass custom configuration | “Test the daily\_etl DAG and let me know when it finishes” |
| Failure Debugging | Root cause analysis across run state, task instances, and logs with impact assessment and fix recommendations | “Why did my\_pipeline fail last night?” |
| DAG Authoring | Guided DAG creation using your existing patterns, connections, and providers with a discover-plan-implement-validate-test workflow | “Create a DAG that extracts from Snowflake and loads to S3 daily” |
| Data Analysis | Warehouse queries, table profiling, and freshness checks with pattern caching and concept-to-table learning | “How many active customers do we have this quarter?” |
| Data Lineage | Upstream origin tracing and downstream impact analysis through DAG source code with criticality ratings | “What would break if I change the customers table schema?” |
| Airflow 3 Migration | Automated code migration with Ruff rules, import fixes, context key replacements, and metadata access pattern updates | “Migrate my DAGs from Airflow 2 to Airflow 3” |
| dbt Integration | Run dbt Core or Fusion projects as Airflow DAGs via Astronomer Cosmos with parsing, execution, and profile configuration | “Set up my dbt project to run in Airflow using Cosmos” |
| Human-in-the-Loop | Approval gates, form inputs, and human-driven branching in DAGs (Airflow 3.1+) | “Add an approval step before the deploy task” |
| Local Environments | Start, stop, restart, and troubleshoot local Airflow environments with the Astro CLI | “Start my local Airflow environment” |

Expand

Show lessSee more

## Prerequisites

CoCo’s Airflow integration requires [uv](https://docs.astral.sh/uv/getting-started/installation/). If `uv` is
not installed, `cortex airflow` provides a helpful message with the install link.

## Setting up Airflow integration

Before you can manage your Airflow instance with CoCo, you must configure a connection. You can do this using
environment variables, or inside CoCo CLI with an interactive setup command.

Environment variable setup
:   Export the required variables in your shell before starting CoCo, as follows. You can use either token-based
    authentication or username/password authentication. If you always use the same Airflow instance, include code like
    this in your shell profile (`~/.bashrc` or `~/.zshrc`) to avoid having to re-enter it every time.

    Copy code

    ```
    # Token auth
    export AIRFLOW_API_URL=https://airflow.example.com
    export AIRFLOW_AUTH_TOKEN=your-api-token

    # Username/password auth
    export AIRFLOW_API_URL=https://airflow.example.com
    export AIRFLOW_USERNAME=your-username
    export AIRFLOW_PASSWORD=your-password
    ```

Interactive setup
:   Issue `/airflow` in CoCo to manage instances through a full screen UI. Both token and username/password authentication are supported.

    | Command | Description |
    | --- | --- |
    | `/airflow` | Manage Airflow instances (opens instance manager) |
    | `/airflow show` | Show current configuration (secrets are masked) |
    | `/airflow clear` | Remove all configuration |

    Expand

    Show lessSee more

    `/airflow` supports multiple named instances. Use the instance manager to add, switch between, or remove them.

## Airflow CLI commands

Use `cortex airflow` to interact with your Airflow instance from the terminal, as shown in the examples below.

Check instance health:

Copy code

```
cortex airflow health
```

List all DAGs:

Copy code

```
cortex airflow dags list
```

Get details on a specific DAG:

Copy code

```
cortex airflow dags get my_pipeline
```

View DAG source code:

Copy code

```
cortex airflow dags source my_pipeline
```

Trigger a DAG run:

Copy code

```
cortex airflow runs trigger my_pipeline
```

List recent runs for a DAG:

Copy code

```
cortex airflow runs list my_pipeline
```

Check task status for a specific run:

Copy code

```
cortex airflow tasks list my_pipeline <run_id>
```

Pause or unpause a DAG:

Copy code

```
cortex airflow dags pause my_pipeline
cortex airflow dags unpause my_pipeline
```

Issue `cortex airflow --help` for the full list of commands.

## Troubleshooting

Connection refused
:   **Symptom:** Airflow operations fail with connection errors.

    **Solution:** Verify your instance URL is correct and that the Airflow API is reachable. Check your current instance configuration and test connectivity with a health check.

Authentication failures
:   **Symptom:** Operations return 401 or 403 errors.

    **Solution:** Try the following steps:

    - Make sure that your token or credentials are correct.
    - Check to see if the token has expired; regenerate it if necessary.
    - Make sure the user and role have API access permissions in Airflow.

DAG not found
:   **Symptom:** Operations report that the DAG doesn’t exist.

    **Solution:** Check for import or parse errors that might be preventing the DAG from loading. Make sure the DAG ID matches exactly.

`uv` not installed
:   **Symptom:** `cortex airflow` displays “cortex airflow requires uv”.

    **Solution:** Install `uv` from [the uv site](https://docs.astral.sh/uv/getting-started/installation/).
