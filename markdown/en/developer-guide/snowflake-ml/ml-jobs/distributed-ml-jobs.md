# Snowflake Multi-Node ML Jobs

Use Snowflake Multi-Node ML Jobs to run distributed machine learning (ML) workflows inside Snowflake ML container runtimes across multiple compute nodes.
Distribute work across multiple nodes to process large datasets and complex models with improved performance. For information about Snowflake ML Jobs, see [Snowflake ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview).

Snowflake Multi-Node ML Jobs extend Snowflake ML Job capabilities by enabling distributed execution across multiple nodes. This brings you:

- **Scalable Performance**: Horizontally scale to process datasets too large to fit on a single node
- **Reduced Training Time**: Speed up complex model training through parallelization
- **Resource Efficiency**: Optimize resource utilization for data-intensive workloads
- **Framework Integration**: Seamlessly use distributed frameworks like [Distributed Modeling Classes](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/modeling_distributors) and [Ray](https://www.ray.io/).

When you run a Snowflake ML Job with multiple nodes, the following occurs:

- One node serves as the head node (coordinator)
- Additional nodes serve as worker nodes (compute resources)
- Together, the nodes form a single logical ML job entity in Snowflake

A single-node ML Job only has a head node. A multi-node job with three active nodes has one head node and two worker nodes. All three nodes participate in running your workload.

## Prerequisites

The following prerequisites are required to use Snowflake Multi-Node ML Jobs.

To set up multi-node jobs, do the following:

1. Install the Snowflake ML Python package.

   Copy code

   ```
   pip install snowflake-ml-python>=1.9.2
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

   You must set MAX\_NODES to be greater than or equal to the number of target instances that you’re using to run your training job.
   If you request more nodes than you intend to use for your training job, it might fail or behave unpredictably.
   For information about running a training job, see [Running multi-node ML jobs](#label-snowflake-ml-jobs-running-multi-node).

## Writing code for multi-node jobs

For multi-node jobs, your code needs to be designed for distributed processing using
[Distributed Modeling Classes](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/modeling_distributors)
or [Ray](https://www.ray.io/).

The following are key patterns and considerations when you use distributed modeling classes or Ray:

### Understanding node initialization and availability

In multi-node jobs, worker nodes can initialize asynchronously and at different times:

- Nodes might not all start simultaneously, especially if compute pool resources are limited
- Some nodes might start seconds or even minutes after others
- ML Jobs automatically wait for the specified `target_instances` to be available before executing your payload.
  The job fails with an error if the expected nodes aren’t available within the timeout period.
  For more information on customizing this behavior, see [Advanced Configuration: Using min\_instances](#label-snowflake-ml-jobs-advanced-config).

You can check available nodes in your job through Ray:

Copy code

```
import ray
ray.init(address="auto", ignore_reinit_error=True)  # Ray is automatically initialized in multi-node jobs
nodes_info = ray.nodes()
print(f"Available nodes: {len(nodes_info)}")
```

### Distributed Processing Patterns

There are multiple patterns you can apply in the payload body of the multi-node job for distributed processing. These patterns leverage [Distributed Modeling Classes](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/modeling_distributors) and [Ray](https://www.ray.io/):

#### Using Snowflake’s Distributed Training API

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

For more information about the available APIs, see [Distributed Modeling Classes](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/modeling_distributors) .

#### Using Native Ray Tasks

Another approach is to use Ray’s task-based programming model:

Copy code

```
# Inside the ML Job payload body
import ray

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

## Running multi-node ML jobs

You can run multi-node ML jobs using the same methods as single-node jobs, using the `target_instances` parameter:

### Using the Remote Decorator

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

### Running a Python File

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

### Running a Directory

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

### Advanced Configuration: Using min\_instances

For more flexible resource management, you can use the optional `min_instances` parameter to specify a minimum number of instances required for the job to proceed.
If `min_instances` is set, the job payload is executed as soon as the minimum number of nodes becomes available, even if that number is smaller than `target_instances`.

This is useful when you want to:

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

    # Check how many nodes we actually got
    available_nodes = len(ray.nodes())
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

## Managing Multi-Node Jobs

### Monitoring Job Status

Job status monitoring is unchanged from single node jobs:

Copy code

```
from snowflake.ml.jobs import MLJob, get_job, list_jobs

# List all jobs
jobs = list_jobs()

# Retrieve an existing job based on ID
job = get_job("<job_id>")  # job is an MLJob instance

# Basic job information
print(f"Job ID: {job.id}")
print(f"Status: {job.status}")  # PENDING, RUNNING, FAILED, DONE

# Wait for completion
job.wait()
```

### Accessing Logs by Node

In multi-node jobs, you can access logs from specific instances:

Copy code

```
# Get logs from the default (head) instance
logs_default = job.get_logs()

# Get logs from specific instances by ID
logs_instance0 = job.get_logs(instance_id=0)
logs_instance1 = job.get_logs(instance_id=1)
logs_instance2 = job.get_logs(instance_id=2)

# Display logs in the notebook/console
job.show_logs()  # Default (head) instance logs
job.show_logs(instance_id=0)  # Instance 0 logs (not necessarily the head node)
```

## Common Issues and Limitations

Use the following information to address common issues that you might encounter.

- **Node Connection Failures**: If worker nodes fail to connect to the head node, it’s possible that the head node completes its task and then turns itself down before the worker finishes its job. To avoid connection failures, implement result collection logic in the job.
- **Memory Exhaustion**: If jobs fail due to memory issues, increase the node size or use more nodes with less data per node.
- **Node Availability Timeout**: If the required number of instances (either `target_instances` or `min_instances`) are not available within the predefined timeout, the job will fail. Ensure your compute pool has sufficient capacity or adjust your instance requirements.
