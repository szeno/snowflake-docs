# Snowpark Submit Python API

In addition to the Snowpark Submit CLI, you can submit and manage Spark workloads programmatically from Python scripts using
the Snowpark Submit Python API. The API uses your existing Snowpark session for authentication, making it a natural fit for
Python-based pipelines and notebooks that already work with Snowflake.

Like the CLI, the Python API supports Spark applications written in Python, Java, and Scala.

Use the Python API instead of the CLI when you want to:

- Embed job submission directly in a Python script or notebook.
- Capture job status or logs as structured data and act on them programmatically.
- Build a custom orchestration loop around submission, status polling, and cancellation.

For CLI-based job submission, see [Using Snowpark Submit](/developer-guide/snowpark-connect/snowpark-connect-using-submit).

## Prerequisites

- **Python 3.10 or later** (earlier than 3.13)
- **`snowpark-submit` installed**: `pip install snowpark-submit`
- **A Snowflake Connection in `connections.toml`**: A valid Snowflake connection with a warehouse and a compute pool specified. For more information, see [Manage Snowflake connections](/developer-guide/snowflake-cli/connecting/configure-connections).

## Quick start

The following example submits a PySpark script and waits for it to finish:

Copy code

```
from snowflake.snowpark import Session
from snowflake.snowpark_submit import SnowparkSubmit, WorkloadConfig

session = Session.builder.configs({
    "connection_name": "my_connection"  # A reference a connection in your connections.toml file
}).create()

client = SnowparkSubmit(session)

workload = WorkloadConfig(
    file="my_spark_app.py",
    compute_pool="MY_COMPUTE_POOL",
    workload_name="MY_FIRST_JOB",
    comment="My first Spark job on Snowflake",
)

result = client.submit(workload, wait_for_completion=True, display_logs=True)
print(f"Job completed with exit code: {result.exit_code}")
print(f"Full workload name: {result.workload_name}")
```

## Examples

### client.submit()

Submits a workload to Snowflake and optionally waits for it to complete.

Copy code

```
result = client.submit(
    workload_config=workload,           # WorkloadConfig instance or dict
    wait_for_completion=False,          # Block until the job finishes
    display_logs=False,                 # Print logs to the console
    fail_on_error=False,                # Raise RuntimeError on job failure
    number_of_most_recent_log_lines=100,
)
```

**Fire-and-forget:** Submit without blocking, then retrieve the workload name for later status checks.

Copy code

```
result = client.submit(workload)
print(f"Submitted: {result.workload_name}")
```

**Blocking with logs:** Wait for the job to finish and print logs in real time. Raise an exception if the job fails.

Copy code

```
result = client.submit(
    workload,
    wait_for_completion=True,
    display_logs=True,
    fail_on_error=True,
)
```

### client.status()

Returns the current status and logs for a workload that is running or has already completed. Use the full workload name
(with the timestamp suffix) that `client.submit()` returns.

Copy code

```
result = client.status(
    workload_name="MY_JOB_241217_120000",
    compute_pool="MY_POOL",
    wait_for_completion=False,
    display_logs=False,
    number_of_most_recent_log_lines=100,
)

print(f"Status: {result.workload_status}")
print(f"Service: {result.service_status}")
print(f"Exit code: {result.job_exit_code}")
```

Note

Log availability has a small latency of a few seconds to a minute. When an event table isn’t configured to store log
data, logs are retained for only a short period, such as five minutes or less.

### client.kill()

Terminates a running workload. Pass the full workload name (with the timestamp suffix).

Copy code

```
result = client.kill(
    workload_name="MY_JOB_241217_120000",
    compute_pool="MY_POOL",
)

if result.exit_code == 0:
    print("Workload terminated successfully")
```

### client.list\_workloads()

Lists workloads in a compute pool, optionally filtered by name prefix. Output is printed to the console.

Copy code

```
client.list_workloads(
    compute_pool="MY_POOL",
    prefix="MY_JOB",  # Optional: filter by name prefix
)
```

## Submitting Java and Scala applications

The Python API can submit Java and Scala JAR files, not just Python scripts. Set `file` to the path of a fat (uber) JAR
and `main_class` to the fully qualified class name.

Copy code

```
workload = WorkloadConfig(
    file="path/to/your-app.jar",
    compute_pool="MY_COMPUTE_POOL",
    workload_name="MY_JAVA_JOB",
    main_class="com.example.HelloSnowparkSubmit",
)

result = client.submit(workload, wait_for_completion=True)
```

For instructions on building fat JARs for Java and Scala, see the Java and Scala tabs in
[Using Snowpark Submit](/developer-guide/snowpark-connect/snowpark-connect-using-submit).

## API Reference

### SnowparkSubmit

The main client class. Accepts a Snowpark `Session` and exposes methods for submitting and managing workloads.

Copy code

```
from snowflake.snowpark import Session
from snowflake.snowpark_submit import SnowparkSubmit

session = Session.builder.configs({
    "connection_name": "my_connection"
}).create()

client = SnowparkSubmit(session)
```

### WorkloadConfig

A dataclass that describes the Spark workload to run. Pass a `WorkloadConfig` instance to `client.submit()`.

Copy code

```
from snowflake.snowpark_submit import WorkloadConfig

workload = WorkloadConfig(
    # Required
    file="my_script.py",           # Path to a .py or .jar file
    compute_pool="MY_POOL",        # SPCS compute pool

    # Optional — application
    workload_name="MY_JOB",        # Base name (a timestamp is appended automatically)
    main_class="com.example.App",  # Required for JAR files
    application_args=["arg1", "arg2"],
    name="My Application",
    comment="Job description",

    # Optional — dependencies
    py_files="utils.py,helpers.zip",
    files="config.json,data.csv",
    jars="dep1.jar,dep2.jar",
    requirements_file="requirements.txt",
    wheel_files="custom.whl",
    init_script="setup.sh",
    external_access_integrations="PYPI_ACCESS",

    # Optional — Spark configuration
    conf={
        "spark.executor.memory": "4g",
        "spark.sql.shuffle.partitions": "200",
    },

    # Optional — resources
    workload_memory="8G",
    workload_cpus=2.0,
    workload_gpus=1,

    # Optional — advanced
    snowflake_stage="@my_stage",
    snowflake_log_level="INFO",
    snowpark_connect_version="1.0.0",
    enable_local_file_access=False,
    show_error_trace=False,
    disable_otel_telemetry=False,
)
```

### StatusInfo

The return type for all API methods. Fields are `None` for operations that don’t produce that value.

| Field | Type | Description |
| --- | --- | --- |
| `exit_code` | `int` | `0` = success; non-zero = failure |
| `terminated` | `bool | None` | Whether the workload has finished |
| `workload_name` | `str | None` | Full workload name, including the appended timestamp |
| `service_status` | `str | None` | SPCS service status |
| `workload_status` | `str | None` | `PENDING`, `RUNNING`, `DONE`, or `FAILED` |
| `created_on` | `str | None` | Creation timestamp (UTC) |
| `started_at` | `str | None` | Start timestamp (UTC) |
| `terminated_at` | `str | None` | Termination timestamp (UTC) |
| `job_exit_code` | `int | None` | Exit code of the Spark job itself |
| `logs` | `list[str]` | Application log lines |
| `error` | `str | None` | Error message, if any |

Expand

Show lessSee more
