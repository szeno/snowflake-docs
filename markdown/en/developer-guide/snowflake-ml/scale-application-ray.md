# Scale an application using Ray

The Snowflake container runtime integrates with [Ray](https://docs.ray.io/), an open-source unified framework for scaling AI and Python applications. This integration allows you to use Ray’s distributed computing capabilities on Snowflake for your machine learning workloads.

Ray is pre-installed and runs as a background process within the Snowflake ML container runtime. You can access Ray from the Container Runtime in the following ways:

**Snowflake Notebooks**: An interactive environment where you can connect to Ray, define tasks, and scale your cluster dynamically for development and experimentation.

**Snowflake ML Jobs**: Submit your Ray applications as structured, repeatable jobs. You can specify the cluster size as part of the job configuration for production workloads.

When you run the container runtime within a Snowflake Notebook or ML Job, the Ray process is automatically initiated as part of that container.

Use the following Python code to connect to the cluster:

Copy code

```
import ray
# Connect to the pre-existing Ray cluster within the Snowflake environment
ray.init(address="auto", ignore_reinit_error=True)
print(f"Ray cluster resources: {ray.cluster_resources()}")
```

Important

Make sure you always use the `"auto"` address when you’re connecting to the Ray cluster.
Initializing with the `"auto"` address directs your application to the head node of the Ray cluster that Snowflake has provisioned for your session.

## Scaling your Ray cluster

After you connect to the Ray cluster, you can adjust its size to meet the computational demands of your workload.

Use the following approaches to scale your Ray cluster:

In a Snowflake NotebookIn a Snowflake ML Job

Within a notebook, you can dynamically scale your cluster up or down using the `scale_cluster` function. This is ideal for interactive workflows where resource needs might change.

When you specify `expected_cluster_size=5`, you get 1 head node and 4 worker nodes.

Copy code

```
from snowflake.ml.runtime_cluster import scale_cluster, get_nodes

# Check current cluster size
print(f"Current cluster size: {len(get_nodes())} nodes")

# Scale up to 4 nodes (1 head + 3 workers)
print("Scaling up cluster...")
scale_cluster(expected_cluster_size=4)
print(f"New cluster size: {len(get_nodes())} nodes")
```

For ML Jobs, you define the cluster size declaratively within your job definition. Specifying the cluster size in the job definition ensures that the required number of nodes is provisioned when the job starts.

For example, your job decorator might include:

Copy code

```
from snowflake.ml.jobs import remote

@remote(
  "MY_COMPUTE_POOL",
  stage_name="payload_stage",
  session=session,
  target_instances=5  # Specify the number of nodes
)
def distributed_ray():
  import ray
  ray.init(address="auto", ignore_reinit_error=True)
  print(f"Ray cluster resources: {ray.cluster_resources()}")

job = distributed_ray()
```

After you’ve finished using your cluster you can scale it down. For more information, see [Cleaning up](#label-scale-application-ray-cleaning-up).

### Monitoring with the Ray Dashboard

If you’re running a job from a Snowflake Notebook, you can use the Ray Dashboard to monitor your cluster. The dashboard is a web interface that allows you to view the cluster’s resources, jobs, tasks, and performance.
Use the following code to get the dashboard URL:

Copy code

```
from snowflake.ml.runtime_cluster import get_ray_dashboard_url

# This function is available in Notebooks to retrieve the dashboard URL
dashboard_url = get_ray_dashboard_url()
print(f"Access the Ray Dashboard here: {dashboard_url}")
```

Open the URL in a new browser tab, log in with your Snowflake credentials.

## Advanced use cases

This section covers advanced Ray features for complex workloads and for migrating existing applications.

### Creating and operating distributed workloads with Ray

Ray provides components that enable you to create and operate distributed workloads. These include foundational components via Ray Core with essential primitives for building and scaling these workloads.

It also includes the following libraries that enable you build your own workflows for data preprocessing, ML training, hyperparameter tuning, and model inference:

- **Ray Data**: Scalable data processing and transformation
- **Ray Train**: Distributed training and fine-tuning of ML models
- **Ray Tune**: Hyperparameter optimization with advanced search algorithms
- **Ray Serve**: Model serving and inference

The following sections describe how you can use these libraries directly, while native Snowflake interfaces built over Ray provide additional tools to build, deploy, and operationalize Ray-based applications.

#### Ray Core: Tasks and Actors

Ray provides the following distributed computing primitives:

- **Tasks**: Stateless functions that run remotely and return values
- **Actors**: Stateful classes that can be instantiated remotely and called multiple times
- **Objects**: Immutable values stored in Ray’s distributed object store
- **Resources**: CPU, GPU, and custom resource requirements for tasks and actors

The following example demonstrates how to use a basic Ray Task and Actors to do linear regression:

Copy code

```
import ray
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Initialize Ray (automatically connects to cluster in Snowflake ML)
ray.init(address="auto", ignore_reinit_error=True)

# Create sample data
large_dataset = np.random.randn(1000, 10)
batch_data = pd.DataFrame(np.random.randn(100, 5), columns=[f'feature_{i}' for i in range(5)])

# Ray Tasks - stateless remote functions
@ray.remote
def compute_heavy_task(data):
    """CPU-intensive computation example"""
    # Simulate heavy computation (matrix operations)
    result = np.dot(data, data.T)
    return np.mean(result)

# Ray Actors - stateful remote classes
@ray.remote
class DataProcessor:
    def __init__(self):
        # Load a simple model
        self.model = LinearRegression()
        # Train on dummy data
        X_dummy = np.random.randn(100, 5)
        y_dummy = np.random.randn(100)
        self.model.fit(X_dummy, y_dummy)

    def process_batch(self, batch):
        # Convert to numpy if it's a DataFrame
        if isinstance(batch, pd.DataFrame):
            batch_array = batch.values
        else:
            batch_array = batch
        return self.model.predict(batch_array)

# Submit tasks and get object references
future = compute_heavy_task.remote(large_dataset)
result = ray.get(future)  # Blocks until task completes
print(f"Task result: {result}")

# Create and use actors
processor = DataProcessor.remote()
batch_result = ray.get(processor.process_batch.remote(batch_data))
print(f"Batch processing result shape: {batch_result.shape}")
```

#### Ray Train: Distributed Training

Ray Train is a library that enables distributed training and fine-tuning of models. You can run your training code on a single machine or an entire cluster.

You can use Ray Train for both single-node and multi-node execution.

For multi-node training, you must handle the following:

- Distributed storage for checkpoints (no shared filesystem across nodes)
- Custom data loading
- Manual resource configuration to coordinate between data ingestion and training resource usage

For a streamlined experience, use the Optimized Training functions for XGBoost, LightGBM, and PyTorch. On the same Ray cluster, these functions handle:

- Snowflake stage-based checkpointing
- Native Snowflake data ingestion
- Built-in resource allocation for data ingestion and training

#### Ray Data: Scalable Data Processing

Ray Data provides scalable, distributed data processing for ML workloads. It can handle datasets larger than cluster memory through streaming execution and lazy evaluation.

Note

Snowflake offers a native integration to transform any Snowflake data source to Ray Data. For more information, see the Data Connector and Ray Data Ingestion pages.

Use Ray Data for:

- Processing large datasets that don’t fit in single-node memory
- Distributed data preprocessing and feature engineering
- Building data pipelines that integrate with other Ray libraries

Copy code

```
import ray
import ray.data as rd
import pandas as pd
import numpy as np
from snowflake.ml.runtime_cluster import scale_cluster

# Initialize Ray
ray.init(address="auto", ignore_reinit_error=True)

# Optional: Scale cluster for better performance with large datasets or CPU-intensive operations
# Scaling benefits Ray Data when:
# - Processing datasets larger than single-node memory (>10GB)
# - Performing CPU-intensive transformations (complex feature engineering, ML preprocessing)
# - Need faster processing through parallelization across multiple nodes
scale_cluster(expected_cluster_size=4)

# Create sample dataset
np.random.seed(42)
n_samples = 50000
n_features = 15

# Generate features with some correlation structure
base_features = np.random.randn(n_samples, 5)
derived_features = np.column_stack([
    base_features[:, 0] * base_features[:, 1],  # interaction
    np.sin(base_features[:, 2]),  # non-linear
    base_features[:, 3] ** 2,  # polynomial
    np.random.randn(n_samples, n_features - 8)  # additional random features
])

X = np.column_stack([base_features, derived_features])
y = (X[:, 0] + 0.5 * X[:, 1] - 0.3 * X[:, 2] + 0.1 * X[:, 5] + np.random.randn(n_samples) * 0.2 > 0).astype(int)

sample_data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(n_features)])
sample_data['target'] = y

print(f"Created dataset with {n_samples} samples and {n_features} features")

# Create Ray Dataset from pandas DataFrame
ray_dataset = rd.from_pandas(sample_data)

# Transform data with Ray Data operations
def preprocess_batch(batch):
    """Preprocess a batch of data"""
    # Get all feature columns
    feature_cols = [col for col in batch.columns if col.startswith('feature_')]

    # Normalize numerical features (first 3 for demo)
    for col in feature_cols[:3]:
        if col in batch.columns:
            batch[f'{col}_scaled'] = (batch[col] - batch[col].mean()) / batch[col].std()

    # Add derived features using actual column names
    if 'feature_0' in batch.columns and 'feature_1' in batch.columns:
        batch['feature_0_squared'] = batch['feature_0'] ** 2
        batch['feature_interaction'] = batch['feature_0'] * batch['feature_1']

    return batch

# Apply transformations lazily
processed_dataset = ray_dataset.map_batches(
    preprocess_batch,
    batch_format="pandas"
)

# Repartition for optimal performance across cluster nodes
processed_dataset = processed_dataset.repartition(num_blocks=8)

# Convert to different formats for downstream use
print("Converting to pandas...")
pandas_df = processed_dataset.to_pandas()  # Collect to pandas
print(f"Processed dataset shape: {pandas_df.shape}")
print(f"New columns: {list(pandas_df.columns)}")

# Iterate through batches for memory efficiency
print("Processing batches...")
batch_count = 0
for batch in processed_dataset.iter_batches(batch_size=1000, batch_format="pandas"):
    batch_count += 1
    print(f"Batch {batch_count}: {batch.shape}")
    if batch_count >= 3:  # Just show first 3 batches
        break

print(f"Total batches processed: {batch_count}")
```

#### Ray Tune: Distributed Hyperparameter Tuning

Ray Tune provides distributed hyperparameter optimization with advanced search algorithms and early stopping capabilities. For a more integrated and optimized experience when reading from Snowflake data sources, use the native Hyperparameter Optimization (HPO) API. For more information about using HPO optimization, see [Optimize a model’s hyperparameters](/developer-guide/snowflake-ml/container-hpo#label-optimize-model-hyperparameters).

If you’re looking for a more customizable approach to a distributed HPO implementation, use Ray Tune.

You can use Ray Tune for the following use cases:

- Hyperparameter optimization across multiple trials in parallel
- Advanced search algorithms (Bayesian optimization, population-based training)
- Large-scale hyperparameter sweeps requiring distributed execution

Copy code

```
import ray
from ray import tune
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from snowflake.ml.runtime_cluster import scale_cluster

# Initialize Ray
ray.init(address="auto", ignore_reinit_error=True)

# Optional: Scale cluster for hyperparameter tuning
# Scaling benefits Ray Tune when:
# - Running many trials in parallel
# - Each trial is computationally intensive
# - Need faster hyperparameter search
scale_cluster(expected_cluster_size=6)

# Create sample dataset
np.random.seed(42)
n_samples = 5000
n_features = 10

X = np.random.randn(n_samples, n_features)
y = ((X[:, 0] + X[:, 1] * X[:, 2] + np.sin(X[:, 3]) + np.random.randn(n_samples) * 0.3) > 0).astype(int)

# Split data
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

def train_function(config):
    """Training function that gets hyperparameters from Ray Tune"""
    # Train model with current hyperparameters
    model = RandomForestClassifier(
        n_estimators=config["n_estimators"],
        max_depth=config["max_depth"],
        min_samples_split=config["min_samples_split"],
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # Evaluate and report results
    val_predictions = model.predict(X_val)
    accuracy = accuracy_score(y_val, val_predictions)

    # Report metrics back to Ray Tune
    return {"accuracy": accuracy}

# Define search space
search_space = {
    "n_estimators": tune.randint(50, 200),
    "max_depth": tune.randint(3, 15),
    "min_samples_split": tune.randint(2, 10)
}

# Configure and run hyperparameter optimization
tuner = tune.Tuner(
    tune.with_resources(
        train_function,
        resources={"CPU": 2}
    ),
    param_space=search_space,
    tune_config=tune.TuneConfig(
        metric="accuracy",
        mode="max",
        num_samples=20,  # Number of trials
        max_concurrent_trials=4
    )
)

print("Starting hyperparameter optimization...")
results = tuner.fit()

# Get best results
best_result = results.get_best_result()
print(f"✅ Hyperparameter tuning completed!")
print(f"   Best accuracy: {best_result.metrics['accuracy']:.4f}")
print(f"   Best parameters: {best_result.config}")

# Show results summary
df_results = results.get_dataframe()
print(f"\nTop 5 results:")
top_results = df_results.nlargest(5, 'accuracy')
for i, (_, row) in enumerate(top_results.iterrows(), 1):
    print(f"  {i}. Accuracy: {row['accuracy']:.4f}, n_estimators: {row['config/n_estimators']}, max_depth: {row['config/max_depth']}")
```

#### Model Serving

For model serving, you can use Snowflake’s native capabilities. For more information, see [Deploy models for real-time inference (REST API)](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api).

#### Submit and manage distributed applications on Ray clusters

Use Ray Jobs to submit and manage distributed applications on Ray clusters with better resource isolation and lifecycle management. For all job-based executions that require access to a Ray Cluster, Snowflake recommends using an ML Job, where you can define the Ray application logic. For instances where you require direct access to the Ray Job interface, such as migrating an existing implementation, you could use the Ray Job primitive as is described in the [Ray documentation](https://docs.ray.io/en/latest/cluster/running-applications/job-submission/sdk.html).

Use Ray jobs for:

- Production ML pipelines and scheduled workflows
- Long-running workloads requiring fault tolerance
- Batch processing and large-scale data processing

Copy code

```
import ray
from ray.job_submission import JobSubmissionClient
import os

# Initialize Ray and get job client
ray.init(address="auto", ignore_reinit_error=True)

# Get Ray dashboard address for job submission
node_ip = os.getenv("NODE_IP_ADDRESS", "0.0.0.0")
dashboard_port = os.getenv("DASHBOARD_PORT", "9999")
dashboard_address = f"http://{node_ip}:{dashboard_port}"

client = JobSubmissionClient(dashboard_address)

# Simple job script
job_script = '''
import ray

@ray.remote
def compute_task(x):
    return x * x

# Submit tasks to Ray cluster
futures = [compute_task.remote(i) for i in range(5)]
results = ray.get(futures)
print(f"Results: {results}")
'''

# Submit job
job_id = client.submit_job(
    entrypoint=f"python -c '{job_script}'",
    runtime_env={"pip": ["numpy"]},
    submission_id="my-ray-job"
)

print(f"Submitted job: {job_id}")

# Monitor job status
status = client.get_job_status(job_id)
print(f"Job status: {status}")
```

### Scaling Ray Clusters with Options

From a Snowflake Notebook, you can scale your Ray clusters to precisely match computational demands. A cluster consists of a head node (coordinator) and worker nodes (for task execution).

Copy code

```
from snowflake.ml.runtime_cluster import scale_cluster, get_nodes

# Asynchronous scaling - returns immediately
scale_cluster(
    expected_cluster_size=2,
    is_async=True  # Don't wait for all nodes to be ready
)

# Scaling with custom options
scale_cluster(
    expected_cluster_size=3,
    options={
        "rollback_after_seconds": 300,  # Auto-rollback after 5 minutes
        "block_until_min_cluster_size": 2  # Return when at least 2 nodes ready
    }
)

# Scale down for cost efficiency
scale_cluster(expected_cluster_size=2)
```

#### Resource monitoring

Copy code

```
import ray
from snowflake.ml.runtime_cluster import get_nodes
from snowflake.ml.runtime_cluster.cluster_manager import (
    get_available_cpu, get_available_gpu, get_num_cpus_per_node
)

# Check available resources
available_cpus = get_available_cpu()
available_gpus = get_available_gpu()
cpus_per_node = get_num_cpus_per_node()

print(f"Available CPUs: {available_cpus}")
print(f"Available GPUs: {available_gpus}")
print(f"CPUs per node: {cpus_per_node}")

# Get Ray's view of resources
ray_resources = ray.available_resources()
print(f"Ray available resources: {ray_resources}")

# Calculate resource utilization
total_cpus = ray.cluster_resources().get('CPU', 0)
used_cpus = total_cpus - available_cpus
utilization = (used_cpus / total_cpus * 100) if total_cpus > 0 else 0
print(f"CPU Utilization: {utilization:.1f}%")
```

### Cleaning up

After you’re finished with the cluster, you can scale it down to avoid additional charges. Use the following code to scale it down:

Copy code

```
# Scale down when finished to conserve resources
print("Scaling down cluster...")
scale_cluster(expected_cluster_size=1)
print(f"Final cluster size: {len(get_nodes())} nodes")
```
