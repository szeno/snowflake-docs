# Container Runtime on multi-node clusters

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

In this preview, [Container Runtime](/developer-guide/snowflake-ml/container-runtime-ml) allows you to run
ML workloads on multi-node clusters in Snowflake Notebooks. The `snowflake-ml-python` library includes APIs to set the
number of nodes in the compute pool available for ML workloads, allowing the resources available to a workload to be
scaled without resizing the compute pool. Another API retrieves a list of active nodes.

A multi-node cluster assigns one node to be the *head* node. Additional nodes are called *worker* nodes. The head node
orchestrates parallel operations in the cluster and also contributes its computing resources to running the workload. A
multi-node cluster with one active node has only a head node. A multi-node cluster with three active nodes has one head
node and two worker nodes, and all three nodes participate in running your workload.

## Prerequisites

To use multi-node clusters to run your ML workloads, you need:

- An active Snowflake account with access to notebooks. See [Snowflake Notebooks](/user-guide/ui-snowsight/notebooks).
- Privileges to create and manage notebooks that use the container runtime.
  See [Notebooks on Container Runtime](/developer-guide/snowflake-ml/notebooks-on-spcs).

### Configure a compute pool

To use a multi-node setup, you need a compute pool with at least two nodes. You can either [create a new compute pool](/sql-reference/sql/create-compute-pool)
or [alter an existing one](/sql-reference/sql/alter-compute-pool). In either command, pass a MAX\_NODES argument to set the pool’s maximum capacity.
It’s good practice to provision one or more extra nodes so you can easily scale up or down for larger or smaller workloads.

To see a compute pool’s capacity, use the [DESCRIBE COMPUTE POOL](/sql-reference/sql/desc-compute-pool) command.
The capacity is in the MAX\_NODES column of the returned table.

Copy code

```
DESCRIBE COMPUTE POOL my_pool;
```

To set a compute pool’s capacity, use the [ALTER COMPUTE POOL](/sql-reference/sql/alter-compute-pool) command.

Copy code

```
ALTER COMPUTE POOL <compute_pool_name>
    SET MAX_NODES = <total_capacity>;
```

## Running a workload on a multi-node cluster

Choosing a multi-node compute pool for your notebook is the only action required to use multiple nodes in the compute
pool to run an ML workload.

In the notebook, set the number of active nodes using the `snowflake.ml.runtime_cluster.scale_cluster` Python API.
The number of active nodes in a compute pool is the number of nodes available to run a workload, up to the pool’s
MAX\_NODES. The method takes the total number of active nodes required, including the head node and all worker nodes, as its primary parameter.

Note

This function is blocking by default (that is, it waits until the scaling operation finishes) and has a 12-minute timeout.
If the operation times out, it will automatically roll back to its previous state.

Scaling operations don’t persist across sessions. That is, if a notebook ends with a non-zero number of worker
nodes, it will not automatically scale up the next time the notebook is started. You must call the scaling API again to
set the number of worker nodes.

### Syntax

Copy code

```
snowflake.ml.runtime_cluster.scale_cluster(
    expected_cluster_size: int,
    *,
    notebook_name: Optional[str] = None,
    is_async: bool = False,
    options: Optional[Dict[str, Any]] = None
) -> bool
```

#### Arguments

- `expected_cluster_size` (int): The number of active nodes in the compute pool, up to the pool’s MAX\_NODES.
  This includes the head node and all worker nodes.
- `notebook_name` (Optional[str]): The name of the notebook where the workload is run. The compute pool to be scaled is the
  pool that the specified notebook is running on. If not provided, it will be automatically determined from the current context.
  An exception is raised if the wrong notebook name is used.
- `is_async` (bool): Controls whether the function blocks waiting for scaling:

  - If False (default): The function blocks until the cluster is fully ready or the operation times out.
  - If True: The function returns immediately after confirming the scaling request has been accepted.
- `options` (Optional[Dict[str, Any]]): Advanced configuration options:

  - `rollback_after_seconds` (int): Maximum time before automatic rollback if scaling is not completed. The default is 720 seconds.
  - `block_until_min_cluster_size` (int): Minimum number of nodes that must be ready before the function returns.

#### Returns

`True` if the compute pool is successfully scaled to the specified number of active nodes. Otherwise, an exception
is raised.

### Example

Copy code

```
from snowflake.ml.runtime_cluster import scale_cluster

# Example 1: Scale up the cluster
scale_cluster(3) # Scales the cluster to 3 total nodes (1 head + 2 workers)

# Example 2: Scale down the cluster
scale_cluster(1) # Scales the cluster to 1 head + 0 workers

# Example 3: Asynchronous scaling - function returns immediately after request is accepted
scale_cluster(5, is_async=True)

# Example 4: Scaling with custom options - wait for at least 2 nodes to be ready
scale_cluster(5, options={"block_until_min_cluster_size": 2})
```

## Get the available number of nodes

Use the `get_nodes` API to get information about the active nodes in the cluster. The function takes no arguments.

### Syntax

Copy code

```
get_nodes() -> list
```

#### Returns

A list containing details of the active nodes in the cluster. Each element of the list is a dictionary with the following keys:

- `name` (str): The name of the node.
- `cpus` (int): The number of CPUs on the node.
- `gpus` (int): The number of GPUs on the node.

### Example

Copy code

```
from snowflake.ml.runtime_cluster import get_nodes

# Example: Get the active nodes in the cluster
nodes = get_nodes()
print(len(nodes), nodes)
```

The output of the example code is as follows:

```
2 [{'name': "IP1", 'cpus': 4, 'gpus': 0}, {'name': "IP2", 'cpus': 8, 'gpus': 1}]
```

## Distributed training on multi-node clusters

The Container Runtime supports distributed training of LightGBM, XGBoost, and PyTorch models.
The distributed training APIs for LightGBMEstimator, XGBEstimator, and PyTorch are documented in detail in the
[API Reference](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/distributors).

### Scaling configuration

All models provide an optional scaling configuration parameter that allows you to specify the resource for the training
job. The scaling configuration is an instance of a model-specific class: `LightGBMScalingConfig`,
`XGBScalingConfig`, or `PyTorchScalingConfig` depending on the model type.

LightGBM and XGBoost scaling configuration objects have the following attributes:

- `num_workers`: The number of worker processes to use for training. The default is -1, which sets the number
  of worker processes automatically.
- `num_cpu_per_worker`: Number of CPUs allocated per worker process. The default is -1, which sets the number of CPUs
  per worker process automatically.
- `use_gpu`: Whether to use the GPU for training. The default is None, allowing the estimator to choose based on the environment.
  When using the GPU, be sure to also configure the model parameters to use the GPU.

Note

Generally, leave `num_workers` and `num_cpu_per_worker` at their default values, so Container Services
determines the best way to distribute these resources. The runtime assigns a worker for each node in the compute pool,
and the necessary CPUs or GPUs for each worker to complete the task.

PyTorch scaling configuration objects have the following attributes:

- `num_cpus`: The number of CPU cores to reserve for each worker.
- `num_gpus`: The number of GPUs to reserve for each worker. The default is 0, indicating no GPUs are reserved.

### Distributed training of LightGBM/XGBoost models

Memory usage
:   Typically, a node with *n* GB of RAM can train a model on *n/4* to *n/3* of data without running out of memory. The
    maximum dataset size depends on the number of worker processes and the training algorithm used.

Compute performance
:   Performance of multi-node training depends on model parameters such as tree depth, number of trees, and maximum
    number of bins. Increasing these parameter values can increase the total training time on a dataset.

#### Example

The following example shows how to train an XGBoost model on a multi-node cluster. Training of LightGBM models is similar.

Copy code

```
from snowflake.ml.modeling.distributors.xgboost import XGBEstimator, XGBScalingConfig
from snowflake.ml.data.data_connector import DataConnector
from implementations.ray_data_ingester import RayDataIngester
table_name = "MULTINODE_SAMPLE_TRAIN_DS"

# Use code like the following to generate example data
"""
# Create a table in current database/schema and store data there
def generate_dataset_sql(db, schema, table_name) -> str:
    sql_script = f"CREATE TABLE IF NOT EXISTS {db}.{schema}.{table_name} AS \n"
    sql_script += f"select \n"
    for i in range(1, 10):
        sql_script += f"uniform(0::float, 10::float, random()) AS FT_{i}, \n"
    sql_script += f"FT_1 + FT_2 AS TARGET, \n"
    sql_script += f"from TABLE(generator(rowcount=>({10000})));"
    return sql_script
session.sql(generate_dataset_sql(session.get_current_database(), session.get_current_schema(), table_name)).collect()
"""

sample_train_df = session.table(table_name)
INPUT_COLS = list(sample_train_df.columns)
LABEL_COL = "TARGET"
INPUT_COLS.remove(LABEL_COL)

params = {
    "eta": 0.1,
    "max_depth": 8,
    "min_child_weight": 100,
    "tree_method": "hist",
}

scaling_config = XGBScalingConfig(
    use_gpu=False
)

estimator = XGBEstimator(
    n_estimators=50,
    objective="reg:squarederror",
    params=params,
    scaling_config=scaling_config,
)
data_connector = DataConnector.from_dataframe(
    sample_train_df, ingestor_class=RayDataIngester
)

xgb_model = estimator.fit(
    data_connector, input_cols=INPUT_COLS, label_col=LABEL_COL
)
```

### Distributed training of PyTorch models

PyTorch models are trained using a training function (`train_func`) that is called in each worker process.

#### Using the context APIs

During the execution of the training function, you can use context APIs to access essential metadata about the
training environment and for parameter forwarding from the caller to the training functions. See
[Related classes](https://docs.snowflake.com/developer-guide/snowpark-ml/reference/latest/distributors#id2) for
documentation of the PyTorch context class.

The context object exposes runtime metadata that you can use to customize the behavior of the training function. You can
retrieve these using the provided methods `get_node_rank`, `get_local_rank`, `get_world_size`, and others.

Tho following code is an example of retrieving the values `test` and `train` from the context object; these are
passed in a key called `dataset_map` (which you can see in the training function example later in this topic).
These values are used to create PyTorch dataset objects that are then passed to the model.

Copy code

```
dataset_map = context.get_dataset_map()
train_dataset = DecodedDataset(dataset_map["train"].get_shard().to_torch_dataset())
test_dataset = DecodedDataset(dataset_map["test"].to_torch_dataset())

hyper_parms = context.get_hyper_params()
num_epochs = int(hyper_parms['num_epochs'])
```

#### Metrics reporting

> Use the `metrics_reporter` method of the context object to send metrics from the training function to the
> controlling code. This enables real-time monitoring and debugging of the training process, as shown in the following
> example.
>
> Copy code
>
> ```
> context.get_metrics_reporter().log_metrics({"train_func_train_time": int(now-start_time)})
> ```

#### Example

The following example is a training function for a PyTorch model.

Copy code

```
def train_func():
    import io
    import base64
    import time
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import torch.optim as optim
    import torch.distributed as dist
    from torch.nn.parallel import DistributedDataParallel as DDP
    from torchvision import transforms
    from torch.utils.data import IterableDataset
    from torch.optim.lr_scheduler import StepLR
    from PIL import Image
    from snowflake.ml.modeling.distributors.pytorch import get_context

    class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.conv1 = nn.Conv2d(1, 32, 3, 1)
            self.conv2 = nn.Conv2d(32, 64, 3, 1)
            self.dropout1 = nn.Dropout(0.25)
            self.dropout2 = nn.Dropout(0.5)
            self.fc1 = nn.Linear(9216, 128)
            self.fc2 = nn.Linear(128, 10)

        def forward(self, x):
            x = self.conv1(x)
            x = F.relu(x)
            x = self.conv2(x)
            x = F.relu(x)
            x = F.max_pool2d(x, 2)
            x = self.dropout1(x)
            x = torch.flatten(x, 1)
            x = self.fc1(x)
            x = F.relu(x)
            x = self.dropout2(x)
            x = self.fc2(x)
            output = F.log_softmax(x, dim=1)
            return output

    class DecodedDataset(IterableDataset):
        def __init__(self, source_dataset):
            self.source_dataset = source_dataset
            self.transforms = transforms.ToTensor()  # Ensure we apply ToTensor transform

        def __iter__(self):
            for row in self.source_dataset:
                base64_image = row['IMAGE']
                image = Image.open(io.BytesIO(base64.b64decode(base64_image)))
                # Convert the image to a tensor
                image = self.transforms(image)  # Converts PIL image to tensor

                labels = row['LABEL']
                yield image, int(labels)

    def train(model, device, train_loader, optimizer, epoch):
        model.train()
        batch_idx = 1
        for data, target in train_loader:
            # print(f"data : {data} \n target: {target}")
            # raise RuntimeError("test")
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            optimizer.step()
            if batch_idx % 100 == 0:
                print('Train Epoch: {} [Processed {} images]\tLoss: {:.6f}'.format(epoch, batch_idx * len(data), loss.item()))
            batch_idx += 1

    context = get_context()
    rank = context.get_local_rank()
    device = f"cuda:{rank}"
    is_distributed = context.get_world_size() > 1
    if is_distributed:
        dist.init_process_group(backend="nccl")
    print(f"Worker Rank : {context.get_rank()}, world_size: {context.get_world_size()}")

    dataset_map = context.get_dataset_map()
    train_dataset = DecodedDataset(dataset_map["train"].get_shard().to_torch_dataset())
    test_dataset = DecodedDataset(dataset_map["test"].to_torch_dataset())

    batch_size = 64
    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=batch_size,
        pin_memory=True,
        pin_memory_device=f"cuda:{rank}"
    )
    test_loader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=batch_size,
        pin_memory=True,
        pin_memory_device=f"cuda:{rank}"
    )

    model = Net().to(device)
    if is_distributed:
        model = DDP(model)
    optimizer = optim.Adadelta(model.parameters())
    scheduler = StepLR(optimizer, step_size=1)

    hyper_parms = context.get_hyper_params()
    num_epochs = int(hyper_parms['num_epochs'])
    start_time = time.time()
    for epoch in range(num_epochs):
        train(model, device, train_loader, optimizer, epoch+1)
        scheduler.step()
    now = time.time()
    context.get_metrics_reporter().log_metrics({"train_func_train_time": int(now-start_time)})
    test(model, device, test_loader, context)
```

The following code illustrates how to kick off distributed training given the preceding training function. The example
creates a PyTorch distributor object to run the training on multiple nodes, connects the training and test data to the
training function via a context object, and establishes the scaling configuration before running the trainer.

Copy code

```
# Set up PyTorchDistributor
from snowflake.ml.modeling.distributors.pytorch import PyTorchDistributor, PyTorchScalingConfig, WorkerResourceConfig
from snowflake.ml.data.sharded_data_connector import ShardedDataConnector
from snowflake.ml.data.data_connector import DataConnector

df = session.table("MNIST_60K")

train_df, test_df = df.random_split([0.99, 0.01], 0)

# Create data connectors for training and test data
train_data = ShardedDataConnector.from_dataframe(train_df)
test_data = DataConnector.from_dataframe(test_df)

pytorch_trainer = PyTorchDistributor(
    train_func=train_func,
    scaling_config=PyTorchScalingConfig(  # scaling configuration
        num_nodes=2,
        num_workers_per_node=1,
        resource_requirements_per_worker=WorkerResourceConfig(num_cpus=0, num_gpus=1),
    )
)

# Run the trainer.
results = pytorch_trainer.run(  # accepts context values as parameters
    dataset_map={"train": train_data, "test": test_data},
    hyper_params={"num_epochs": "1"}
)
```

## Known limitations and common issues

These limitations and issues are likely to be addressed before multi-node training on Container Runtime is generally available.

### Scaling operation times out

The scaling operation can fail because the new nodes are not ready within the 12-minute timeout. Possible causes include:

- *Insufficient pool capacity.* You have requested more nodes than the pool’s MAX\_NODES. Increase the pool’s MAX\_NODES.
- *Resource contention.* 12 minutes may not be enough time to warm the added nodes. Set the pool’s MIN\_NODES
  to a larger number to keep some of the nodes warm, or increase the number of active nodes using more than one call to
  `scale_cluster` with a smaller increment. Another option is to use asynchronous mode to skip waiting for all the nodes to be ready:

  - Use asynchronous mode for non-blocking operations:

  Copy code

  ```
  scale_cluster(3, is_async=True)
  ```

  - Increase the timeout threshold:

  Copy code

  ```
  scale_cluster(3, options={"rollback_after_seconds": 1200})
  ```

### Notebook Name Errors

If you see an error message like “Notebook <name> does not exist or not authorized”, this means the automatically
detected notebook name doesn’t match the current notebook. This can happen when:

- Your notebook name contains special characters like dots and spaces
- The automatic notebook name detection is not working correctly

Solution: Explicitly provide the notebook name parameter. Note that the notebook name needs double quotes to be treated
as an [identifier](/sql-reference/identifiers-syntax):

Copy code

```
# Explicitly specifying the notebook name if naming auto detection doesn't work
try:
    scale_cluster(2)
except Exception as e:
    print(e)  # Output: "Notebook "WRONG_NOTEBOOK" does not exist or not authorized"
    scale_cluster(2, notebook_name='"MY_NOTEBOOK"')
```

### SPCS services are not cleaned up after failed scaling operation

When scaling operations fail, the system should clean up all resources created in the operation. However, if this fails,
one or more SPCS services may be left in PENDING or FAILED state. Services in the PENDING state might become ACTIVE
later, or if there is no capacity in the compute pool, stay PENDING forever.

To remove services in the PENDING or FAILED states, scale the cluster to have one node (zero worker nodes). To clean up
all launched services, end the current notebook session by clicking on “End Session” in the notebook interface.
