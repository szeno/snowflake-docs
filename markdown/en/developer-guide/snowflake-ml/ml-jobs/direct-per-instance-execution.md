# Direct per-instance execution for multi-node ML Jobs

Important

Direct per-instance execution requires Snowflake ML Python 1.54.0 or later. It supports file, directory, and staged payloads. Callable payloads submitted with the `@remote` decorator aren’t supported.

Direct per-instance execution starts the same payload entrypoint once on every instance. ML Jobs doesn’t assign head or worker roles to these entrypoints; your codebase determines any framework-specific roles. Use this mode primarily for an existing distributed training codebase that already starts and coordinates processes with a multi-node launcher such as `torchrun`, `accelerate launch`, or `deepspeed`.

## Write code for the job

Start with an existing distributed training codebase that uses a launcher such as `torchrun`, `accelerate launch`, or `deepspeed`. Create or update its launcher script to map the topology environment variables provided by ML Jobs to the node count, node rank, rendezvous address, and port expected by the launcher. ML Jobs runs this script on every instance so that all instances join the same distributed workload.

### Available topology environment variables

ML Jobs provides the following topology environment variables to each payload entrypoint. Use them to configure the launcher for the current instance and the overall job topology:

| Environment variable | Description |
| --- | --- |
| `SNOWFLAKE_JOB_INDEX` | Zero-based index of the current instance |
| `SNOWFLAKE_JOBS_COUNT` | Number of target instances in the job |
| `MLRS_HEAD_IP` | IP address of instance 0 |
| `MLRS_NODE_IPS` | Comma-separated IP addresses in instance-index order; set when all target instance IP addresses are available |
| `MLRS_RDZV_PORT` | Port available for a workload rendezvous endpoint |
| `MLRS_EPHEMERAL_PORT_MIN` | Lower bound of the port range available to the workload |
| `MLRS_EPHEMERAL_PORT_MAX` | Upper bound of the port range available to the workload |

Expand

Show lessSee more

For example, the following Bash entrypoint maps the topology environment variables to the corresponding `torchrun` arguments:

Copy code

```
torchrun \
  --nnodes="$SNOWFLAKE_JOBS_COUNT" \
  --node-rank="$SNOWFLAKE_JOB_INDEX" \
  --master-addr="$MLRS_HEAD_IP" \
  --master-port="$MLRS_RDZV_PORT" \
  --nproc-per-node=<processes_per_instance> \
  train.py
```

Important

Multi-node `torchrun` must use a static rendezvous. Dynamic rendezvous isn’t supported. Use `MLRS_HEAD_IP` and `MLRS_RDZV_PORT` as the static rendezvous address and port, as shown in the preceding example.

For launchers that accept a DeepSpeed-style or Open MPI-style hostfile with `slots=N` entries, generate the hostfile from `MLRS_NODE_IPS` when that variable is available. The IP addresses are ordered by `SNOWFLAKE_JOB_INDEX`.

Copy code

```
if [[ -z "${MLRS_NODE_IPS:-}" ]]; then
  echo "MLRS_NODE_IPS is unavailable" >&2
  exit 1
fi

IFS=',' read -r -a NODE_IPS <<< "$MLRS_NODE_IPS"

HOSTFILE="${TMPDIR:-/tmp}/launcher-hostfile"
: > "$HOSTFILE"

for node_ip in "${NODE_IPS[@]}"; do
  printf '%s slots=%s\n' "$node_ip" "<processes_per_instance>" >> "$HOSTFILE"
done
```

If your workload needs additional listener ports, select them from the range defined by `MLRS_EPHEMERAL_PORT_MIN` and `MLRS_EPHEMERAL_PORT_MAX`.

## Examples

The [distributed training samples](https://github.com/Snowflake-Labs/sf-samples/tree/main/samples/ml/ml_jobs/distributed_training) demonstrate four ways to adapt existing codebases to direct per-instance execution:

- PyTorch DistributedDataParallel (DDP) with a static `torchrun` rendezvous.
- DeepSpeed with no-SSH hostfile launch.
- Open MPI with job-scoped SSH and `mpirun` launch.
- PrimeRL with an application-specific multi-role topology.

Start with the PyTorch DDP or DeepSpeed sample for common launcher patterns. Open MPI and PrimeRL demonstrate more advanced integrations.

## Run the job

### Configure the instance count

Set `target_instances` to the number of ML Job instances to allocate. The launcher separately controls how many training processes run on each instance. For example, `target_instances=2` with `torchrun --nproc-per-node=4` produces a framework world size of 8.

For a launcher that requires a fixed number of nodes, omit `min_instances` or set it equal to `target_instances`. ML Jobs then waits for the complete topology before starting the entrypoints and fails if the required instances aren’t available before the timeout.

Important

Set `min_instances` lower than `target_instances` only for custom workloads that support an incomplete topology. In this configuration, `MLRS_NODE_IPS` might be unavailable, preflight validation might fail while waiting for missing instances, and instances that never start might appear with an exit code of `None` in `distributed_result()`.

### Validate the topology before running the entrypoint

Pass the optional `preflight` argument to `submit_file`, `submit_directory`, or `submit_from_stage` to validate the distributed environment before the user entrypoint starts:

Copy code

```
# Pass preflight when you submit the job.
job = submit_directory(
    ...,
    parallel=True,
    preflight="wiring",  # Or "reference".
)
```

Choose one of the following validation levels:

| Value | What it validates |
| --- | --- |
| `wiring` | Whether every instance can receive consistent topology coordinates, can reach the shared PyTorch c10d rendezvous, and can complete an inter-instance collective using Gloo or NCCL. |
| `reference` | Whether the GPU instances can complete a fixed DDP training step using GPU 0 on each instance, in addition to the `wiring` validation. It also reports step timing with and without gradient synchronization and timing variation across instances. |

Expand

Show lessSee more

The preflight produces one of the following outcomes:

- **Passed:** ML Jobs runs the user entrypoint.
- **Failed:** ML Jobs doesn’t run the user entrypoint. The failure appears in `distributed_result()`.
- **Skipped:** ML Jobs reports the reference step as skipped when it doesn’t apply, such as on a CPU pool or a single-instance job, and continues after the applicable checks pass.

Note

Preflight validation covers the corresponding PyTorch c10d rendezvous and collective path. It doesn’t validate your launcher, training code, SSH setup, or other application-specific services and protocols. The reference step doesn’t exercise multiple processes or GPUs within an instance or predict application throughput.

To skip validation, omit `preflight` or pass `None`. The argument is available only when `parallel=True`.

### Submit a direct per-instance job

The following example submits a directory whose Bash entrypoint starts the codebase’s launcher:

Copy code

```
from snowflake.ml.jobs import submit_directory

job = submit_directory(
    "/path/to/codebase/",
    "MY_COMPUTE_POOL",
    entrypoint=["bash", "launch.sh"],
    stage_name="payload_stage",
    session=session,
    target_instances=2,
    parallel=True,
    preflight="wiring",
)
```

## Monitor the job

### Monitor job status

Job status monitoring is unchanged from single-node jobs. For more information, see [Managing ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview#label-snowflake-ml-job-management).

Copy code

```
from snowflake.ml.jobs import get_job, list_jobs

# List all jobs
jobs = list_jobs()

# Retrieve an existing job based on ID
job = get_job("<job_id>")  # job is an MLJob instance

# Basic job information
print(f"Job ID: {job.id}")
print(f"Status: {job.status}")  # PENDING, RUNNING, FAILED, DONE, CANCELLING, CANCELLED, INTERNAL_ERROR, DELETED

# Wait for completion
job.wait()
```

### Retrieve distributed results

On success, `distributed_result()` returns a `DistributedResult` with the following fields:

| Field | Description |
| --- | --- |
| `success` | Whether every target instance exited successfully |
| `exit_codes` | Mapping from instance index to that instance’s exit code; `None` means that an instance was lost or never recorded an outcome |
| `failed_instance` | Earliest-failing instance, or `None` on success |
| `return_value` | Return value recorded by instance 0 on success, when available; list-form command entrypoints normally return `None` |

Expand

Show lessSee more

If any instance doesn’t exit successfully, `distributed_result()` raises `DistributedJobError`. The exception’s `result` attribute contains the same structured per-instance outcome. The exception’s `__cause__` contains the reconstructed exception and remote traceback from the earliest-failing instance, when available.

Copy code

```
from snowflake.ml.jobs import DistributedJobError

try:
    result = job.distributed_result()
except DistributedJobError as error:
    print(error.result.exit_codes)
    print(error.result.failed_instance)
    if error.result.failed_instance is not None:
        print(
            job.get_logs(
                instance_id=error.result.failed_instance,
                verbose=True,
            )
        )
    raise
```

### Access per-instance logs

Use `get_logs()` or `show_logs()` with an instance ID to inspect the launcher and workload output from a specific instance. Pass `verbose=True` to include runtime and bootstrap output.

Copy code

```
# Get logs from specific instances
logs_instance0 = job.get_logs(instance_id=0)
logs_instance1 = job.get_logs(instance_id=1)

# Display logs in the notebook or console
job.show_logs(instance_id=0)
job.show_logs(instance_id=1, verbose=True)
```

### Access the Ray Dashboard

While the job is running, use `job.get_ray_dashboard_url()` to inspect nodes and runtime resources. Use per-instance logs to monitor launcher and workload progress, and use distributed results to inspect per-instance outcomes after the job completes. The Ray Dashboard isn’t available on the `CPU_X64_XS` instance family. For more information, see [Access the Ray Dashboard](/developer-guide/snowflake-ml/ml-jobs/overview#label-snowflake-ml-jobs-ray-dashboard).

Copy code

```
ray_dashboard_url = job.get_ray_dashboard_url()
```

## Common issues and limitations

Use the following information to address common issues that you might encounter.

- **Unsupported topology changes**: If your workload requires elastic membership or dynamic replacement of a failed instance, direct per-instance execution does not support this. Direct per-instance execution uses a fixed topology for the lifetime of the job.
- **Memory exhaustion**: If an instance runs out of memory, use a larger instance family, reduce the number of processes per instance, or distribute the workload across more instances.
- **Node availability timeout**: If the required number of instances isn’t available before the timeout, the job fails. For more information, see [Shared limitations](/developer-guide/snowflake-ml/ml-jobs/distributed-ml-jobs#label-snowflake-ml-jobs-node-availability-timeout).
- **Launcher hangs during rendezvous**: If a c10d-based launcher waits indefinitely, run the `wiring` preflight and verify that every entrypoint uses the same rendezvous address and port and its own `SNOWFLAKE_JOB_INDEX` as the node rank.
- **Dependency or model download failures**: If dependency or model downloads fail, verify that the job has an [external access integration](/developer-guide/external-network-access/creating-using-external-network-access) whose network rules allow every required external host.
