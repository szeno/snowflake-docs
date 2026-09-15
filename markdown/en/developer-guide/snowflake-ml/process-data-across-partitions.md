# Process data with custom logic across partitions

Use the Distributed Partition Function (DPF) to process data in parallel across one or more nodes in a compute pool.
DPF handles distributed orchestration, errors, observability, and artifact persistence automatically. You can run DPF in either a [Snowflake Notebook](/user-guide/ui-snowsight/notebooks) or a [Snowflake ML Job](/developer-guide/snowflake-ml/ml-jobs/overview).

DPF supports the following execution modes:

- **DataFrame mode** (`run()`): Partition a Snowpark DataFrame by column values and execute your function on each
  partition concurrently. Data is prefetched in parallel for optimal throughput.
- **Stage mode** (`run_from_stage()`): Process files from a Snowflake stage where each file becomes a partition.
  Ideal for large-scale file processing with predictable memory usage.

You can use DPF to process large datasets efficiently across different data segments.

This tool is ideal for scenarios such as the following:

- Analyzing sales data by region
- Processing customer data by geographic segments
- Training ML models on each data partition
- Performing data transformations where each data partition requires the same processing logic

DPF handles the distributed data processing automatically. You don’t need to manage the distributed computing infrastructure.

DPF lets you write custom Python code using open source libraries on containerized infrastructure with GPU access.

Important

DPF automatically stores results and artifacts in Snowflake stages. Before you use DPF, make sure you have permissions to the stage where DPF stores results and artifacts.

## DataFrame mode: Process data by column partitions

Use DataFrame mode to partition a Snowpark DataFrame by a specified column and execute your Python function on each
partition in parallel. The following example demonstrates processing sales data by region.

1. [Define the processing function](#label-dpf-df-define-function)
2. [Initialize and run DPF](#label-dpf-df-run)
3. [Monitor progress and wait for completion](#label-dpf-df-monitor)
4. [Retrieve results from each partition](#label-dpf-df-retrieve)
5. [Handle errors](#label-dpf-df-errors)
6. [Restore results from a completed run](#label-dpf-df-restore)

### Define the processing function

Import the classes required to run distributed processing:

Copy code

```
from snowflake.ml.modeling.distributors.distributed_partition_function.dpf import DPF
from snowflake.ml.modeling.distributors.distributed_partition_function.dpf_run import DPFRun
from snowflake.ml.modeling.distributors.distributed_partition_function.entities import (
    RunStatus, ExecutionOptions
)
```

Define a processing function that takes two arguments:

- `data_connector`: A [DataConnector](/developer-guide/snowpark-ml/reference/latest/api/data/snowflake.ml.data.data_connector.DataConnector)
  that provides access to the partition’s data. Call `data_connector.to_pandas()` to load it as a pandas DataFrame,
  or use other methods like `to_torch_dataset()` or `to_ray_dataset()`.
- `context`: A [PartitionContext](#label-dpf-partition-context) object that provides the partition ID and methods for
  uploading and downloading artifacts.

Copy code

```
import json

def process_sales_data(data_connector, context):
    df = data_connector.to_pandas()
    print(f"Processing {len(df)} records for region: {context.partition_id}")

    # Perform region-specific analytics
    summary = {
        'region': context.partition_id,
        'total_sales': df['amount'].sum(),
        'avg_order_value': df['amount'].mean(),
        'customer_count': df['customer_id'].nunique(),
        'record_count': len(df)
    }

    # Store results in stage for subsequent access

    context.upload_to_stage(summary, "sales_summary.json",
        write_function=lambda obj, path: json.dump(obj, open(path, 'w')))
```

For each region, this function computes summary statistics and saves the results as a JSON file to the partition’s
dedicated stage directory.

### Initialize and run DPF

Create a `DPF` instance with your processing function and an output stage name, then call `run()` to start
distributed processing.

Important

The Snowpark DataFrame that you provide must be created from a table. For information about creating a DataFrame from
a table, see the [Constructing a DataFrame](/developer-guide/snowpark/python/working-with-dataframes#label-snowpark-python-dataframe-construct).

Copy code

```
dpf = DPF(process_sales_data, "analytics_stage")
run = dpf.run(
    partition_by="region",
    snowpark_dataframe=sales_data,
    run_id="regional_analytics_2024"
)
```

The `run()` method accepts the following parameters:

- `partition_by` (str): Column name to partition the DataFrame by. Each unique value creates a separate partition.
- `snowpark_dataframe`: The Snowpark DataFrame to partition and process.
- `run_id` (str): Unique identifier for this run. Creates a dedicated directory `@{stage_name}/{run_id}/` for all
  artifacts. Use descriptive names like `experiment_2024_01_15` or `model_v1_retrain`.
- `on_existing_artifacts` (str, optional): Action when artifacts for the `run_id` already exist.
  `"error"` (default) raises an error; `"overwrite"` replaces existing artifacts.
- `execution_options` ([ExecutionOptions](#label-dpf-execution-options), optional): Configuration for resource
  allocation and execution behavior.

### Monitor progress and wait for completion

Call `wait()` to block until the run completes. By default, it displays a progress bar.

Copy code

```
final_status = run.wait()  # Shows progress bar by default
print(f"Job completed with status: {final_status}")
```

The following is an example of the output:

```
Progress: 100%|██████████| 4/4 [02:15<00:00, 33.75s/it]
Job completed with status: RunStatus.SUCCESS
```

You can also check the status and progress at any time without blocking:

Copy code

```
# Check overall status
current_status = run.status

# Get progress grouped by partition status
progress = run.get_progress()
```

### Retrieve results from each partition

After the run completes successfully, retrieve results from each partition using the `partition_details` property.
Each partition’s details include a `stage_artifacts_manager` for accessing saved artifacts.

Copy code

```
if final_status == RunStatus.SUCCESS:
    import json
    all_results = []
    for partition_id, details in run.partition_details.items():
        # List available artifacts for this partition
        files = details.stage_artifacts_manager.list()
        print(f"Partition {partition_id} artifacts: {files}")

        # Load an artifact using a custom deserializer
        summary = details.stage_artifacts_manager.get("sales_summary.json",
            read_function=lambda path: json.load(open(path, 'r')))
        all_results.append(summary)

    # Combine results across all regions
    total_sales = sum(r['total_sales'] for r in all_results)
    total_customers = sum(r['customer_count'] for r in all_results)
```

The `stage_artifacts_manager` provides three methods:

- `list()`: Returns a list of filenames saved in the partition’s stage directory.
- `get(filename, read_function=None)`: Downloads and deserializes an artifact. Uses `pickle` by default, or
  a custom `read_function` if provided.
- `download(filename, local_dir)`: Downloads a raw file to a local directory and returns the local file path.

### Handle errors

If the run does not succeed, inspect individual partition details to diagnose failures:

Copy code

```
if final_status != RunStatus.SUCCESS:
    for partition_id, details in run.partition_details.items():
        if details.status != PartitionStatus.DONE:
            print(f"Partition {partition_id} status: {details.status}")
            try:
                error_logs = details.logs
                print(error_logs)
            except RuntimeError:
                print("Logs not available for this partition")
```

The overall `RunStatus` reflects the aggregate outcome:

- `SUCCESS`: All partitions completed successfully.
- `PARTIAL_FAILURE`: Some partitions succeeded, but at least one failed.
- `FAILURE`: No partitions completed successfully.
- `CANCELLED`: The run was cancelled.
- `IN_PROGRESS`: The run is still executing.

Each partition has a `PartitionStatus`:

- `PENDING`: Waiting to be processed.
- `RUNNING`: Currently being processed.
- `DONE`: Completed successfully.
- `FAILED`: The user function raised an exception.
- `CANCELLED`: Cancelled by the user.
- `INTERNAL_ERROR`: An internal system error occurred (for example, out-of-memory).

To import these enums:

Copy code

```
from snowflake.ml.modeling.distributors.distributed_partition_function.entities import (
    RunStatus, PartitionStatus
)
```

To cancel a running job:

Copy code

```
run.cancel()
```

Note

Partitions that have already completed are not affected by cancellation. Partial results, logs, and artifacts
from completed partitions remain available.

### Restore results from a completed run

You can restore a completed run from its persisted state and access the same results without re-running the process:

Copy code

```
from snowflake.ml.modeling.distributors.distributed_partition_function.dpf_run import DPFRun

restored_run = DPFRun.restore_from(run_id="regional_analytics_2024", stage_name="analytics_stage")

# Access results just like the original run
for partition_id, details in restored_run.partition_details.items():
    print(f"{partition_id}: {details.status}")
```

Note

Restored runs are read-only. You cannot call `wait()` or `cancel()` on a restored run.

## Stage mode: Process files from a stage

Use stage mode to process files from a Snowflake stage where each file becomes a partition. This is ideal for
large-scale file processing, such as processing a collection of Parquet files that have been staged.

### Define a processing function

The processing function signature is the same as DataFrame mode. The `data_connector` provides access to the file’s data,
and `context.partition_id` is the relative file path within the stage.

Copy code

```
def process_file(data_connector, context):
    df = data_connector.to_pandas()
    print(f"Processing file {context.partition_id}: {len(df)} rows")

    # Process data and save results
    result = {"row_count": len(df), "columns": list(df.columns)}
    import json
    context.upload_to_stage(result, "result.json",
        write_function=lambda obj, path: json.dump(obj, open(path, 'w')))
```

### Run DPF from stage

Call `run_from_stage()` instead of `run()`. Specify the input `stage_location` containing the source files
and optionally a `file_pattern` to filter which files to process.

Copy code

```
dpf = DPF(process_file, "output_stage")
run = dpf.run_from_stage(
    stage_location="@my_db.my_schema.input_stage/data/",
    run_id="file_processing_2024",
    file_pattern="*.parquet",
)
final_status = run.wait()
```

The `run_from_stage()` method accepts the following parameters:

- `stage_location` (str): Input stage path containing the source data files. Each file matching the `file_pattern`
  becomes a partition. Supports both simple and fully qualified stage names:

  - Simple: `"@my_stage/data/"`
  - Fully qualified: `"@my_db.my_schema.my_stage/data/"`
- `run_id` (str): Unique identifier for this run.
- `file_pattern` (str, optional): Glob pattern to filter files. Defaults to `"*.parquet"`.
- `on_existing_artifacts` (str, optional): `"error"` (default) or `"overwrite"`.
- `execution_options` ([ExecutionOptions](#label-dpf-execution-options), optional): Configuration for resource
  allocation and execution behavior.

Note

The `stage_location` is the *input* data source. The `stage_name` provided to `DPF()` is the *output*
location for artifacts like logs and results. These can be different stages.

Monitoring, result retrieval, error handling, and run restoration work the same way as
[DataFrame mode](#label-dpf-df-monitor).

For I/O-bound file processing, set `num_cpus_per_worker=1` in `ExecutionOptions` to maximize parallelism
(one actor per CPU). For CPU-bound workloads, use the default or increase `num_cpus_per_worker`.

Copy code

```
from snowflake.ml.modeling.distributors.distributed_partition_function.entities import ExecutionOptions

run = dpf.run_from_stage(
    stage_location="@my_stage/data/",
    run_id="io_bound_processing",
    execution_options=ExecutionOptions(num_cpus_per_worker=1),
)
```

## Configure execution options

Use `ExecutionOptions` to control resource allocation and execution behavior, such as CPU/GPU allocation per worker,
retry count, and fail-fast behavior. All fields are optional with sensible defaults.

Copy code

```
from snowflake.ml.modeling.distributors.distributed_partition_function.entities import ExecutionOptions

options = ExecutionOptions(
    num_cpus_per_worker=4,
    num_gpus_per_worker=1,
    fail_fast=True,
)

run = dpf.run(
    partition_by="region",
    snowpark_dataframe=sales_data,
    run_id="my_run",
    execution_options=options,
)
```

For the full list of parameters and worker scaling behavior, see the
[ExecutionOptions API reference](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/container-runtime/distributors.distributed_partition_function).

## Work with artifacts using PartitionContext

The `PartitionContext` object is passed as the second argument to your processing function. It provides methods for
interacting with artifacts and Snowflake sessions during partition execution.

### Upload artifacts

Use `upload_to_stage()` to save results from within your processing function. By default, objects are serialized
using pickle. Provide a `write_function` for custom serialization.

Copy code

```
def my_function(data_connector, context):
    df = data_connector.to_pandas()

    # Save a pickle object (default serialization)
    results = {'total': df['amount'].sum(), 'count': len(df)}
    context.upload_to_stage(results, "summary.pkl")

    # Save JSON data with a custom write function
    import json
    context.upload_to_stage(
        results, "summary.json",
        write_function=lambda obj, path: json.dump(obj, open(path, 'w'))
    )

    # Save a CSV file
    df_processed = df.groupby('category').sum()
    context.upload_to_stage(
        df_processed, "aggregated.csv",
        write_function=lambda df, path: df.to_csv(path, index=False)
    )
```

### Download artifacts

Use `download_from_stage()` to load artifacts within your processing function. You can use this function to
access artifacts from a prior run. For example, you can use it to load a model for inference.

Copy code

```
def my_inference_function(data_connector, context):
    # Load a pickle object from the current partition's stage path
    model = context.download_from_stage("model.pkl")

    # Load from a different stage path (e.g., from a prior training run)
    model = context.download_from_stage(
        "model.pkl",
        stage_path="@db.schema.stage/training_run/partition_0"
    )

    # Load JSON with a custom deserializer
    import json
    config = context.download_from_stage(
        "config.json",
        read_function=lambda path: json.load(open(path, 'r'))
    )
```

### Use Snowflake sessions

Use `with_session()` to execute operations that require a Snowflake session, such as writing results to a table.
This method uses a bounded session pool to avoid hitting Snowflake’s session limits when running many partitions
concurrently.

Copy code

```
def my_function(data_connector, context):
    df = data_connector.to_pandas()

    # Load a model from a prior training run
    model = context.download_from_stage("model.pkl")

    predictions = model.predict(df[['X1', 'X2']])

    results = df.copy()
    results['predictions'] = predictions
    results['partition_id'] = context.partition_id

    # Write results to a Snowflake table using the bounded session pool
    context.with_session(lambda session:
        session.create_dataframe(results)
            .write.mode("append")
            .save_as_table("predictions_table")
    )
```

Note

The function passed to `with_session()` is serialized using cloudpickle. Avoid capturing large objects or
non-serializable resources in the closure.

## Scale across multiple nodes

To run DPF across multiple nodes, scale your cluster before starting the run:

Copy code

```
from snowflake.ml.runtime_cluster import scale_cluster

# Scale to 3 nodes for increased parallelism
scale_cluster(3)

dpf = DPF(process_sales_data, "analytics_stage")
run = dpf.run(
    partition_by="region",
    snowpark_dataframe=sales_data,
    run_id="multi_node_run",
    execution_options=ExecutionOptions(use_head_node=True),
)
final_status = run.wait()
```

When running on multiple nodes, set `use_head_node=False` if you want the head node to act solely as a coordinator
without executing user functions. This can improve reliability for long-running workloads because an out-of-memory
error on a worker node does not affect the coordinator.

## Limitations and constraints

- **One concurrent run**: Only one DPF run can execute at a time. Starting a new run while another is in progress
  raises an error. Cancel the previous run with `run.cancel()` before starting a new one.
- **DataFrame requirements**: In DataFrame mode, the Snowpark DataFrame must contain exactly one query and no post-actions.
- **Single-node restriction**: `use_head_node=False` is not supported on single-node clusters.
- **Artifact path structure**: Artifacts are stored at `@{stage_name}/{run_id}/{partition_id}/`. This path
  structure is fixed and cannot be customized.
- **Restored runs are read-only**: Runs restored with `DPFRun.restore_from()` cannot call `wait()` or
  `cancel()`.

## Next steps

- Explore [Train models across data partitions](/developer-guide/snowflake-ml/train-models-across-partitions) to learn about training multiple ML models using DPF as the underlying
  infrastructure.
- For the complete API documentation, see the
  [Distributed Partition Function (DPF) API reference](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/container-runtime/distributors.distributed_partition_function).
- For end-to-end examples, see the
  [Snowflake ML sample notebooks](https://github.com/Snowflake-Labs/sf-samples/tree/main/samples/ml).
