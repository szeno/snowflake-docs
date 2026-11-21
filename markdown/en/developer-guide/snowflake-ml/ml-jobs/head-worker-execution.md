# Head/worker execution for multi-node ML Jobs

In head/worker execution, instance 0 serves as the head node and runs the payload entrypoint once. The remaining instances serve as worker nodes, and the head process distributes work to them. Use this mode when your payload follows this pattern, such as when it uses Ray tasks or Snowflake’s distributed training APIs. This mode is the default and supports function, file, directory, and staged payloads.

## Write code for the job

Design your code for distributed processing with Snowflake’s distributed training APIs or Ray.

The following are key patterns and considerations:

### Understand node initialization and availability

In multi-node jobs, worker nodes can initialize asynchronously and at different times:

- Nodes might not all start simultaneously, especially if compute pool resources are limited
- Some nodes might start seconds or even minutes after others

Before running your payload, ML Jobs waits for the number of instances specified by `min_instances`, if set; otherwise, it waits for `target_instances`.
The job fails if the required number of instances isn’t available within the timeout period.
For more information, see [Use for flexible resource management](#label-snowflake-ml-jobs-head-worker-instance-count).

You can check available nodes in your job through Ray:

Copy code

```
import ray

# Connect to the Ray cluster initialized by ML Jobs.
ray.init(address="auto", ignore_reinit_error=True)
nodes_info = [node for node in ray.nodes() if node["Alive"]]
print(f"Available nodes: {len(nodes_info)}")
```

### Distributed processing patterns

There are multiple patterns you can apply in the payload body of the multi-node job for distributed processing. These patterns use [Distributed Modeling Classes](/developer-guide/snowpark-ml/reference/latest/modeling_distributors) and [Ray](https://www.ray.io/):

#### Use Snowflake’s distributed training APIs

Snowflake provides optimized trainers for common ML frameworks:

Copy code

```
# Inside the ML Job payload body
from snowflake.ml.modeling.distributors.xgboost import XGBEstimator, XGBScalingConfig

# Configure scaling for distributed execution
scaling_config = XGBScalingConfig()

# Create distributed estimator
estimator = XGBEstimator(
    n_estimators=100,
    params={"objective": "reg:squarederror"},
    scaling_config=scaling_config
)

# Train using distributed resources
# NOTE: data_connector and feature_cols excluded for brevity
model = estimator.fit(data_connector, input_cols=feature_cols, label_col="target")
```

For more information about the available APIs, see [Distributed Modeling Classes](/developer-guide/snowpark-ml/reference/latest/modeling_distributors).

#### Use native Ray tasks

Another approach is to use Ray’s task-based programming model:

Copy code

```
# Inside the ML Job payload body
import ray

# Connect to the Ray cluster initialized by ML Jobs.
ray.init(address="auto", ignore_reinit_error=True)

@ray.remote
def process_chunk(data_chunk):
    # Process a chunk of data
    return processed_result

# Distribute work across available workers
data_chunks = split_data(large_dataset)
futures = [process_chunk.remote(chunk) for chunk in data_chunks]
results = ray.get(futures)
```

For more information, see [Ray’s task programming documentation](https://docs.ray.io/en/latest/ray-core/tasks.html).

## Run the job

You can run multi-node ML Jobs using the same methods as single-node jobs by setting the `target_instances` parameter. Head/worker execution is the default, so omit `parallel` or set `parallel=False` explicitly when you submit the job.

### Use the remote decorator

Copy code

```
from snowflake.ml.jobs import remote

@remote(
    "MY_COMPUTE_POOL",
    stage_name="payload_stage",
    session=session,
    target_instances=3  # Specify the number of nodes
)
def distributed_training(data_table: str):

    from snowflake.ml.modeling.distributors.xgboost import XGBEstimator, XGBScalingConfig

    # Configure scaling for distributed execution
    scaling_config = XGBScalingConfig()

    # Create distributed estimator
    estimator = XGBEstimator(
        n_estimators=100,
        params={"objective": "reg:squarederror"},
        scaling_config=scaling_config
    )

    # Train using distributed resources
    # NOTE: data_connector and feature_cols excluded for brevity
    model = estimator.fit(data_connector, input_cols=feature_cols, label_col="target")

job = distributed_training("<my_training_data>")
```

### Run a Python file

Copy code

```
from snowflake.ml.jobs import submit_file

job = submit_file(
    "<script_path>",
    "MY_COMPUTE_POOL",
    stage_name="<payload_stage>",
    session=session,
    target_instances=<num_training_nodes>  # Specify the number of nodes
)
```

### Run a directory

Copy code

```
from snowflake.ml.jobs import submit_directory

job = submit_directory(
    "<script_directory>",
    "MY_COMPUTE_POOL",
    entrypoint="<script_name>",
    stage_name="<payload_stage>",
    session=session,
    target_instances=<num_training_nodes>  # Specify the number of nodes
)
```

### Use `min_instances` for flexible resource management

For more flexible resource management, you can use the optional `min_instances` parameter to specify a minimum number of instances required for the job to proceed.
If `min_instances` is set, the job payload runs as soon as the minimum number of nodes becomes available, even if that number is smaller than `target_instances`.

Use `min_instances` when you want to:

- Start training with fewer nodes if the full target isn’t immediately available
- Reduce wait times when compute pool resources are limited
- Implement fault-tolerant workflows that can adapt to varying resource availability

Copy code

```
from snowflake.ml.jobs import remote

@remote(
    "MY_COMPUTE_POOL",
    stage_name="payload_stage",
    session=session,
    target_instances=5,  # Prefer 5 nodes
    min_instances=3      # But start with at least 3 nodes
)
def flexible_distributed_training(data_table: str):
    import ray

    # Connect to the Ray cluster initialized by ML Jobs.
    ray.init(address="auto", ignore_reinit_error=True)

    # Check how many nodes are available
    available_nodes = sum(1 for node in ray.nodes() if node["Alive"])
    print(f"Training with {available_nodes} nodes")

    # Adapt your training logic based on available resources
    from snowflake.ml.modeling.distributors.xgboost import XGBEstimator, XGBScalingConfig

    scaling_config = XGBScalingConfig(
        num_workers=available_nodes
    )

    estimator = XGBEstimator(
        n_estimators=100,
        params={"objective": "reg:squarederror"},
        scaling_config=scaling_config
    )

    # Train using available distributed resources
    model = estimator.fit(data_connector, input_cols=feature_cols, label_col="target")

job = flexible_distributed_training("<my_training_data>")
```

## Monitor the job

### Monitor job status

Job status monitoring is unchanged from single-node jobs. For more information, see [Managing ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview#label-snowflake-ml-job-management).

Copy code

```
from snowflake.ml.jobs import MLJob, get_job, list_jobs

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

### Access logs by node

Use `get_logs()` or `show_logs()` to access logs from the head instance or a specific worker instance:

Copy code

```
# Get logs from the default (head) instance
logs_default = job.get_logs()

# Get logs from specific instances by ID
logs_instance0 = job.get_logs(instance_id=0)
logs_instance1 = job.get_logs(instance_id=1)
logs_instance2 = job.get_logs(instance_id=2)

# Display logs in the notebook or console
job.show_logs()  # Default (head) instance logs
job.show_logs(instance_id=0)  # Instance 0 (head node) logs
```

### Access the Ray Dashboard

While the job is running, use `job.get_ray_dashboard_url()` to inspect Ray tasks, actors, nodes, and runtime resources. The Ray Dashboard isn’t available on the `CPU_X64_XS` instance family. For more information, see [Access the Ray Dashboard](/developer-guide/snowflake-ml/ml-jobs/overview#label-snowflake-ml-jobs-ray-dashboard).

Copy code

```
ray_dashboard_url = job.get_ray_dashboard_url()
```

## Common issues and limitations

Use the following information to address common issues that you might encounter.

- **Node connection failures**: Worker nodes might fail to connect if the head node finishes and shuts down before workers complete. To prevent this, make the head process wait for all worker results (for example, with `ray.get()`) before it exits.
- **Memory exhaustion**: If jobs fail due to memory issues, use a larger instance family or distribute the workload across more instances.
- **Node availability timeout**: If the required number of instances isn’t available before the timeout, the job fails. For more information, see [Shared limitations](/developer-guide/snowflake-ml/ml-jobs/distributed-ml-jobs#label-snowflake-ml-jobs-node-availability-timeout).
