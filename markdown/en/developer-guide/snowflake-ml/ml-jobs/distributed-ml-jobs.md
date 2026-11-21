# Snowflake multi-node ML Jobs

Use Snowflake multi-node ML Jobs to run distributed machine learning (ML) workflows inside Snowflake ML Container Runtime across multiple compute nodes.
Distribute work across multiple nodes to process large datasets and complex models with improved performance. For information about Snowflake ML Jobs, see [Snowflake ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview).

Snowflake multi-node ML Jobs extend Snowflake ML Job capabilities by enabling distributed execution across multiple nodes. Snowflake multi-node ML Jobs bring you:

- **Scalable performance**: Horizontally scale to process datasets too large to fit on a single node
- **Reduced training time**: Speed up complex model training through parallelization
- **Resource efficiency**: Optimize resource utilization for data-intensive workloads
- **Framework integration**: Use distributed frameworks through [Distributed Modeling Classes](/developer-guide/snowpark-ml/reference/latest/modeling_distributors) and [Ray](https://www.ray.io/), or run an existing distributed training codebase with its launcher.

## Prerequisites

Multi-node ML Jobs build on the setup in [Prerequisites](/developer-guide/snowflake-ml/ml-jobs/overview#label-snowflake-ml-jobs-prerequisites), with two differences:

1. Install Snowflake ML Python 1.54.0 or later. Multi-node jobs require a later version than single-node jobs do.

   Copy code

   ```
   pip install 'snowflake-ml-python>=1.54.0'
   ```
2. Create a compute pool with enough nodes to support your multi-node job:

   Copy code

   ```
   CREATE COMPUTE POOL IF NOT EXISTS MY_COMPUTE_POOL
     MIN_NODES = 1
     MAX_NODES = <NUM_INSTANCES>
     INSTANCE_FAMILY = <INSTANCE_FAMILY>;
   ```

   Important

   `MAX_NODES` must be greater than or equal to `target_instances`.

## Choose an execution mode

Multi-node ML Jobs support two execution modes: **head/worker execution** and **direct per-instance execution**. They differ in where the payload entrypoint runs and how your code starts distributed work across the requested instances.

Both modes use the allocated instances as one ML Job, but they support different distributed codebases and result APIs. Choose the mode that matches how your codebase starts work across instances.

The following diagram compares where the payload entrypoint runs in each execution mode.

![In head/worker execution, instance 0 runs the entrypoint and distributes work to the other instances. In direct per-instance execution, every instance runs the same entrypoint and participates in the distributed workload.](/static/images/snowflake-ml/ml-jobs-multi-node-execution-mode.png)

### Head/worker execution

In head/worker execution, instance 0 serves as the head node and runs the payload entrypoint once. The remaining instances serve as worker nodes, and the head process distributes work to them. Choose this mode when your payload follows this pattern, such as when it uses Ray tasks or Snowflake’s distributed training APIs. This mode is the default and supports function, file, directory, and staged payloads.

For detailed guidance, including advanced `min_instances` configuration, see [Use `min\_instances` for flexible resource management](/developer-guide/snowflake-ml/ml-jobs/head-worker-execution#label-snowflake-ml-jobs-head-worker-instance-count).

### Direct per-instance execution

Direct per-instance execution starts the same payload entrypoint once on every instance. ML Jobs doesn’t assign head or worker roles to these entrypoints; your codebase determines any framework-specific roles. Choose this mode primarily for an existing distributed training codebase that already starts and coordinates processes with a multi-node launcher such as `torchrun`, `accelerate launch`, or `deepspeed`. Select this mode by setting `parallel=True` when you submit a file, directory, or staged payload.

For detailed guidance, see [Direct per-instance execution for multi-node ML Jobs](/developer-guide/snowflake-ml/ml-jobs/direct-per-instance-execution).

### Compare execution modes

The following table summarizes the differences between the two execution modes:

| Characteristic | Head/worker execution | Direct per-instance execution |
| --- | --- | --- |
| Entrypoint runs on | Instance 0 only | Every instance |
| Choose this mode when | Your payload starts on instance 0 and distributes work to the remaining instances, such as with Ray tasks or Snowflake’s distributed training APIs | Your existing distributed training codebase uses a multi-node launcher such as `torchrun`, `accelerate launch`, or `deepspeed` |
| `parallel` setting | Omit `parallel` or set `parallel=False` | Set `parallel=True` |
| Supported payloads | Functions, files, directories, and staged payloads | Files, directories, and staged payloads |
| Result method | `result()` | [`distributed_result()`](/developer-guide/snowflake-ml/ml-jobs/direct-per-instance-execution#label-snowflake-ml-jobs-retrieve-distributed-results) |
| Preflight validation | Not available | Optional `wiring` or `reference` validation |

Expand

Show lessSee more

## Shared limitations

The following limitation applies to both execution modes.

If the required number of instances (either `target_instances` or `min_instances`) isn’t available within the predefined timeout, the job fails. Ensure that your compute pool has sufficient capacity or adjust your instance requirements. Each execution mode page lists mode-specific issues.
