# Load and write data

Use Snowflake ML to efficiently load data from Snowflake tables and stages into your machine learning workflows. Snowflake ML provides optimized data loading capabilities that take advantage of Snowflake’s distributed processing to accelerate data ingestion for your training and inference workflows.

You can load and process data using:

- **Snowflake Notebooks**: Interactive development environment for exploring data and building ML models. For more information, see [Notebooks on Container Runtime](/developer-guide/snowflake-ml/notebooks-on-spcs).
- **Snowflake ML Jobs**: Run your ML workloads asynchronously from any development environment. For more information, see [Snowflake ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview).

Both Notebooks and ML Jobs run on the Container Runtime, which provides preconfigured environments optimized for machine learning workloads with distributed processing capabilities. The Container Runtime uses Ray, an open-source framework for distributed computing, to efficiently process data across multiple compute nodes. For more information about the Container Runtime, see [Snowflake Container Runtime](/developer-guide/snowflake-ml/container-runtime-ml).

Snowflake ML provides different APIs for loading structured and unstructured data:

**Structured data (tables and datasets)**

- **DataConnector**: Load data from Snowflake tables and Snowflake Datasets. For more information, see [Load structured data from Snowflake tables](#label-load-data-from-snowflake-tables).
- **DataSink**: Write data back to Snowflake tables. For more information, see [Write structured data back to Snowflake tables](#label-load-data-write-data-back-to-snowflake-tables).

**Files in stages**

- **DataSource APIs**: Load data from various file formats (CSV, Parquet, images, and more) from Snowflake stages. For more information, see [Load data from Snowflake stages](#label-load-data-from-snowflake-stages).

**Performance optimizations (all data sources)**

- **Stage sharding**: Cut per-file I/O when reading many small files by consolidating them into larger shards. For more information, see [Optimize unstructured data loading with stage sharding](#label-optimize-unstructured-data-loading).
- **Disk cache**: Serve repeated reads from node-local disk instead of refetching from Snowflake. Enabled by default. For more information, see [Optimize with file-level disk cache](#label-optimize-with-disk-cache).

The following table can help you choose the right API for your use case:

**Data Sources and APIs**

| Data Type | Data Source | API for Loading | API for Writing |
| --- | --- | --- | --- |
| Structured | Snowflake Tables | DataConnector | DataSink |
| Structured | Snowflake Datasets | DataConnector | DataSink |
| Structured | CSV Files (Stage) | DataSource API | Datasink |
| Structured | Parquet Files (Stage) | DataSource API | DataSink |
| Unstructured | Other Staged Files | DataSource API | N/A |

Expand

Show lessSee more

## Load structured data from Snowflake tables

Use the Snowflake DataConnector to load structured data from Snowflake tables and Snowflake Datasets into a Snowflake Notebook or Snowflake ML Job. The DataConnector accelerates data loading by parallelizing the reads across multiple compute nodes.

The DataConnector works with either Snowpark DataFrames or Snowflake Datasets:

- **Snowpark DataFrames**: Provide direct access to the data in your Snowflake tables. Best used during development.
- **Snowflake Datasets**: Versioned schema-level objects. Best used for production workflows. For more information, see [Snowflake Datasets](/developer-guide/snowflake-ml/dataset).

After parallelizing the reads, the DataConnector can convert the data into one of following data structures:

- pandas dataframe
- PyTorch dataset
- TensorFlow dataset

### Create a DataConnector

You can create a DataConnector from a Snowpark DataFrame or a Snowflake Dataset.

Use the following code to create a DataConnector from a Snowpark DataFrame:

Copy code

```
from snowflake.ml.data.data_connector import DataConnector
from snowflake.snowpark.context import get_active_session

session = get_active_session()

# Create DataConnector from a Snowflake table
data_connector = DataConnector.from_dataframe(session.table("example-table-name"))
```

Use the following code to create a DataConnector from a Snowflake Dataset:

Copy code

```
from snowflake.ml.data.data_connector import DataConnector

# Create DataConnector from a Snowflake Dataset
data_connector = DataConnector.from_dataset(snowflake_dataset)
```

### Convert DataConnector to other formats

After creating a DataConnector, you can convert it to different data structures for use with various ML frameworks.

pandas dataframePyTorch datasetTensorFlow dataset

You can convert a DataConnector to a pandas dataframe for use with scikit-learn and other pandas-compatible libraries.

The following example loads data from a Snowflake table into a pandas dataframe and trains an XGBoost classifier:

Copy code

```
from snowflake.ml.data.data_connector import DataConnector
from snowflake.snowpark.context import get_active_session
import xgboost as xgb

session = get_active_session()

# Specify training table location
table_name = "TRAINING_TABLE"

# Load table into DataConnector
data_connector = DataConnector.from_dataframe(session.table(table_name))

# Convert to pandas dataframe
pandas_df = data_connector.to_pandas()

# Prepare features and labels
label_column_name = 'TARGET'
X, y = pandas_df.drop(label_column_name, axis=1), pandas_df[label_column_name]

# Train classifier
clf = xgb.Classifier()
clf.fit(X, y)
```

You can convert a DataConnector to a PyTorch dataset for use with PyTorch models and data loaders.

The following example loads data from a Snowflake table into a PyTorch dataset:

Copy code

```
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from snowflake.ml.data.data_connector import DataConnector

# Create DataConnector (see previous examples)
# data_connector = DataConnector.from_dataframe(...)

# Convert to PyTorch dataset
torch_dataset = data_connector.to_torch_dataset(batch_size=32)
dataloader = DataLoader(torch_dataset, batch_size=None)

label_col = 'TARGET'
feature_cols = ['FEATURE1', 'FEATURE2']

for batch_idx, batch in enumerate(dataloader):
    y = batch_data.pop(label_col).squeeze()
    X = torch.stack(
        [tensor.squeeze() for key, tensor in batch.items() if key in feature_cols]
    )
```

You can convert a DataConnector to a TensorFlow dataset for use with TensorFlow models. Data is loaded in a streaming fashion for maximum efficiency.

The following example converts a DataConnector to a TensorFlow dataset:

Copy code

```
from snowflake.ml.data.data_connector import DataConnector

# Create DataConnector (see previous examples)
# data_connector = DataConnector.from_dataframe(...)

# Convert to TensorFlow dataset
tf_ds = data_connector.to_tf_dataset(
    batch_size=4,
    shuffle=True,
    drop_last_batch=True
)

for batch in tf_ds:
    print(batch)
```

### Use with Snowflake’s distributed training APIs

For best performance, you can pass a DataConnector directly to Snowflake’s optimized distributed training APIs instead of converting to pandas, PyTorch, or TensorFlow datasets first.

The following example trains an XGBoost model using Snowflake’s distributed XGBoost estimator:

Copy code

```
from snowflake.ml.data.data_connector import DataConnector
from snowflake.ml.modeling.distributors.xgboost.xgboost_estimator import (
    XGBEstimator,
    XGBScalingConfig,
)
from snowflake.snowpark.context import get_active_session

session = get_active_session()

# Create DataConnector from a Snowpark dataframe
snowflake_df = session.table("TRAINING_TABLE")
data_connector = DataConnector.from_dataframe(snowflake_df)

# Create Snowflake XGBoost estimator
snowflake_est = XGBEstimator(
    n_estimators=1,
    objective="reg:squarederror",
    scaling_config=XGBScalingConfig(use_gpu=False),
)

# Train using the data connector
# When using a data connector, input_cols and label_col must be provided
fit_booster = snowflake_est.fit(
    data_connector,
    input_cols=NUMERICAL_COLS,
    label_col=LABEL_COL
)
```

### Use sharding with PyTorch distributor

You can use the ShardedDataConnector to shard your data across multiple nodes for distributed training with the Snowflake PyTorch distributor.

The following example trains a PyTorch model on the digits dataset using sharded data across multiple processes:

Copy code

```
from sklearn import datasets
from snowflake.ml.data.sharded_data_connector import ShardedDataConnector
from snowflake.ml.modeling.pytorch import (
    PyTorchTrainer,
    ScalingConfig,
    WorkerResourceConfig,
    getContext,
)
from torch import nn
from snowflake.snowpark.context import get_active_session

session = get_active_session()

# Create the Snowflake data from a Snowpark dataframe
digits = datasets.load_digits(as_frame=True).frame
digits_df = session.create_dataframe(digits)

# Create sharded data connector
sharded_data_connector = ShardedDataConnector.from_dataframe(digits_df)

# Define the PyTorch model
class DigitsModel(nn.Module):
    def __init__(self):
        super(DigitsModel, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(8 * 8, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

# Define training function that runs across multiple nodes or devices
# Each process receives a unique data shard
def train_func():
    import os
    import torch
    import torch.distributed as dist
    from torch.utils.data import DataLoader
    from torch import nn
    from torch.nn.parallel import DistributedDataParallel as DDP

    # Get context with data shards and model directory
    context = getContext()
    dataset_map = context.get_dataset_map()
    model_dir = context.get_model_dir()
    training_data = dataset_map["train"].get_shard().to_torch_dataset()
    train_dataloader = DataLoader(training_data, batch_size=batch_size, drop_last=True)

    dist.init_process_group()
    device = "cpu"
    label_col = '"target"'
    batch_size = 64

    model = DDP(DigitsModel())
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

    # Training loop
    for epoch in range(5):
        for batch, batch_data in enumerate(train_dataloader):
            y = batch_data.pop(label_col).flatten().type(torch.LongTensor).to(device)
            X = torch.concat(
                [tensor.to(torch.float32) for tensor in batch_data.values()],
                dim=-1,
            ).to(device)
            pred = model(X)
            loss = loss_fn(pred, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if batch % 100 == 0:
                print(f"Epoch {epoch}, Batch {batch}, Loss: {loss.item()}")

    # Save the model
    if dist.get_rank() == 0:
        torch.save(model.state_dict(), os.path.join(model_dir, "digits_model.pth"))

# Create PyTorch trainer with scaling configuration
pytorch_trainer = PyTorchTrainer(
    train_func=train_func,
    scaling_config=ScalingConfig(
        num_nodes=1,
        num_workers_per_node=4,
        resource_requirements_per_worker=WorkerResourceConfig(num_cpus=1, num_gpus=0),
    ),
)

# Run distributed training
response = pytorch_trainer.run(
    dataset_map=dict(
        train=sharded_data_connector,
    )
)
```

## Load data from Snowflake stages

Use the Snowflake DataSource APIs to read data from Snowflake stages. Each file format has a corresponding datasource class that defines how to read the data.

The following shows the file formats and corresponding APIs that you use to load the data:

- **Binary files**: `SFStageBinaryFileDataSource`
- **Text files**: `SFStageTextDataSource`
- **CSV files**: `SFStageCSVDataSource`
- **Parquet files**: `SFStageParquetDataSource`
- **Image files**: `SFStageImageDataSource`
- **Arrow IPC shard files**: `SFStageShardDataSource`. For more information, see [Optimize unstructured data loading with stage sharding](#label-optimize-unstructured-data-loading).

### Load and process data

When you create a Snowflake Datasource, you must provide the following:

- The name of the stage from which you’re reading the data
- The database that has the stage (defaults to current session)
- The schema that has the stage (defaults to current session)
- The pattern to the filter files being read from the datasource (optional)

The Data API or the Data Connector retrieves all files within the provided path that matches the file pattern.

After you define the Snowflake Datasource, you can load data into a Ray dataset. With the Ray dataset, you can do the following:

- Use the dataset with Ray APIs
- Pass the dataset to DataConnector
- Convert to pandas or PyTorch datasets if needed.

The following example does the following:

- Reads Parquet files from a Snowflake stage into a Ray dataset
- Converts the dataset to a DataConnector

Copy code

```
import ray
from snowflake.ml.ray.datasource.stage_parquet_file_datasource import SFStageParquetDataSource
from snowflake.ml.data.data_connector import DataConnector

data_source = SFStageParquetDataSource(
    stage_location="@stage/path/",
    database="DB_NAME", # optional
    schema="SCHEMA_NAME", # optional
    file_pattern='*.parquet', # optional
)

# Build Ray dataset from provided datasources
ray_ds = ray.data.read_datasource(data_source)

dc = DataConnector.from_ray_dataset(ray_ds)
```

## Optimize unstructured data loading with stage sharding

When you work with large numbers of small files, such as images, audio files, or other binary data, reading each file individually can create significant I/O overhead. Stage sharding consolidates many small files into a smaller number of large Arrow IPC shard files, reducing the number of operations required to read your data.

### When to use stage sharding

Stage sharding is most beneficial when:

- You have many small files (thousands to millions), such as images, audio files, or other binary data
- You read the same files multiple times during training (multiple epochs)

**Performance impact**: Reading from shards can be 6-10× faster than reading the same files individually. This was measured on a 100 GB dataset of 100,000 images, comparing `SFStageShardDataSource` against `SFStageImageDataSource`, with image decoding included in both. The gain comes from cutting the number of per-file read operations, so it scales with file count and diminishes as your average file size grows.

### How stage sharding works

Stage sharding is a two-step process:

1. **Generate shards (one-time)**: Consolidate many small files into a few large shard files
2. **Read from shards**: Load data from the consolidated shards instead of individual files

The original file bytes are preserved exactly as-is, so there’s no quality loss or re-encoding overhead.

### Generate shards

Use `generate_shards()` to consolidate your files. This is typically done once as a preprocessing step:

Copy code

```
from snowflake.ml.ray.stage_sharding import generate_shards

# Consolidate many small files into larger shards
generate_shards(
    src_stage_location="@MY_STAGE/raw_images",
    dest_stage_location="@MY_STAGE/shards_files",
    file_pattern="*.jpg",
    target_shard_size_mb=256,  # Size of each output shard
)
```

**Key parameters**:

- `src_stage_location`: Location of your original files
- `dest_stage_location`: Where to write the consolidated shards
- `file_pattern`: Filter files by extension (for example, `"*.jpg"` or `"*.png"`)
- `target_shard_size_mb`: Target size for each shard file (default: 256 MB)
  - Larger shards = fewer files but less parallelism
  - Choose based on your dataset size and worker count
  - Example: For a 2 GB dataset, 64 MB → ~30 shards; 256 MB → ~8 shards

### Read from shards

After generating shards, read them using `SFStageShardDataSource`:

Copy code

```
import ray
from snowflake.ml.ray.datasource import SFStageShardDataSource

# Read the sharded data
ds = ray.data.read_datasource(
    SFStageShardDataSource(
        stage_location="@MY_STAGE/shards_files/",
    )
)

# The data contains raw bytes: decode as needed.
# For images:
def decode_image(batch):
    from PIL import Image
    import io
    import numpy as np

    images = []
    for raw_bytes in batch["bytes"]:
        img = Image.open(io.BytesIO(raw_bytes))
        images.append(np.array(img))

    return {"image": images}

ds = ds.map_batches(decode_image, batch_format="numpy")
```

### Best practices for stage sharding

**Decode location**: Decode file contents (for example, JPEG to tensor) in a separate `map_batches()` step after reading, not during the read. This separation allows Ray to pipeline reading and decoding operations.

**File organization**: Store shards in a dedicated directory to avoid mixing with other files. Use `force_cleanup=True` in `generate_shards()` to replace existing shards.

## Optimize with file-level disk cache

The file-level disk cache stores frequently accessed data on local disk, accelerating repeated data access during multi-epoch training or when you run multiple experiments on the same dataset. Unlike stage sharding, which targets only files in stages, the disk cache works with **all data sources** including Snowflake tables, CSV files, Parquet files, images, and more.

**Note**: The disk cache is **enabled by default**. You can disable it by setting `use_file_cache=False`, or tune it with the `file_cache_config` parameter for fine-grained control. Because cached reads trade freshness for speed, review [Important considerations](#important-considerations) before you rely on the cache.

### When to use disk cache

The disk cache is most beneficial when:

- You run multi-epoch training, so the same data is read multiple times
- You run multiple experiments on the same dataset
- Your data fits (or mostly fits) on local disk per node

**Performance impact**: On cache hits, the disk cache can provide 10-14× faster data loading than fetching from a stage. Two conditions determine whether you see that speedup:

- **Epoch count**: The first epoch reads from the stage at normal speed and populates the cache. Only the second and later epochs read from local disk, so a single-epoch run sees no benefit and the cache typically pays for itself after two or three epochs.
- **Dataset size**: Dataset size is close to cache budget, which defaults to 50% of the node’s local NVMe storage (see `max_disk_pct` in [Configure disk cache](#configure-disk-cache)). For example, a GPU\_NV\_M node has 3800 GB of NVMe.

### How disk cache works

The disk cache operates transparently at the filesystem layer:

1. **First read (cold)**: Data is fetched from Snowflake and stored in local disk cache
2. **Subsequent reads (warm)**: Data is served directly from local disk
3. **Automatic management**: The cache manages eviction to stay within disk limits

The cache is persistent across runs and shared across Ray workers on the same compute node, maximizing reuse.

### Using the disk cache

No configuration is needed to use the disk cache:

Copy code

```
import ray
from snowflake.ml.ray.datasource import SFStageImageDataSource

data_source = SFStageImageDataSource(
    stage_location="@MY_STAGE/images/",
)

ray_ds = ray.data.read_datasource(data_source)
```

### Configure disk cache

For fine-grained performance tuning, pass a `file_cache_config` dictionary to customize cache behavior:

Copy code

```
from snowflake.ml.ray.datasource import SFStageImageDataSource

data_source = SFStageImageDataSource(
    stage_location="@MY_STAGE/images/",
    # Raise the disk budget and put the cache on a different mount.
    # See the following table for every supported parameter.
    file_cache_config={
        "max_disk_pct": 70,
        
        # Eviction check frequency in seconds (default: 30)
        # How often to check if eviction is needed (0 = check on every write)
        "evict_interval_sec": 30,
        
        # Custom cache directory (default: $TMPDIR/)
        # Use this to place cache on a dedicated mounted volume/filesystem
        "cache_dir": "/nvme-volume",
        
        # Subdirectory within cache root (default: "mlrs_disk_cache/file_cache")
        # Relative path for organizing cache within the root directory
        "disk_subdir": "mlrs_disk_cache/file_cache",
    }
)
```

**Configuration parameters explained**:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `max_disk_pct` | number | 50 | Maximum percentage of total disk space the cache can use. When exceeded, oldest files are evicted using LRU policy. Accepts integers or floats (for example, 50 or 67.5). |
| `evict_interval_sec` | number | 30 | Minimum seconds between eviction checks. Higher values reduce scan overhead but may allow temporary over-usage. Accepts integers or floats (for example, 30 or 0.5). Set to 0 to check on every write. |
| `cache_dir` | str | `$TMPDIR` | Root directory for the cache. Useful for directing cache to a specific mount (for example, fast NVMe storage). Must be node-local, not network-mounted. |
| `disk_subdir` | str | `"mlrs_disk_cache/file_cache"` | Subdirectory path within the cache root. Allows organizing cache structure within the root directory. |

Expand

Show lessSee more

### Use with different data sources

The following examples show the cache with stage files and with Snowflake tables.

**Stage files (images, Parquet, CSV)**:

Copy code

```
from snowflake.ml.ray.datasource import SFStageImageDataSource

data_source = SFStageImageDataSource(
    stage_location="@MY_STAGE/images/",
    file_pattern="*.jpg",
)
```

**Snowflake tables with DataConnector**:

Copy code

```
from snowflake.ml.data.data_connector import DataConnector
from snowflake.snowpark.context import get_active_session

session = get_active_session()

# The cache also covers the table path, and takes the same tuning knobs
data_connector = DataConnector.from_dataframe(
    session.table("TRAINING_TABLE"),
    file_cache_config={
        "max_disk_pct": 60,  # Adjust based on dataset size
    }
)
```

The disk cache works with the following data sources: `SFStageImageDataSource`, `SFStageParquetDataSource`, `SFStageCSVDataSource`, `SFStageShardDataSource`, `SFStageTextDataSource`, `SFStageBinaryFileDataSource`, and `DataConnector`.

### Important considerations

**Security and freshness**: The disk cache trades strict freshness for speed:

- Cache hits bypass Snowflake authorization checks
- File changes aren’t detected once cached
- The cache is best suited for immutable datasets during a training run

**Disk space**: The cache automatically manages disk usage and evicts old entries when needed. Monitor disk usage in production environments.

## Write structured data back to Snowflake tables

Use the Snowflake DataSink API to write structured data from your Notebook or ML Job back to a Snowflake table. You can write transformed or prediction datasets to Snowflake for further analysis or storage.

To define a data sink, provide the following:

- Stage name
- Database name (defaults to current session)
- Schema name (defaults to current session)
- File pattern to match specific files (optional)

The following example defines a data sink:

Copy code

```
from snowflake.ml.ray.datasink import SnowflakeTableDatasink
datasink = SnowflakeTableDatasink(
    table_name="table_name",
    database="db_name",
    schema="schema_name",
    auto_create_table=True, # create table if not exists
    override=True # replace vs insert to table
)
```

After you define a data sink, you can use the following code to write the Ray dataset to a Snowflake table.

Copy code

```
import ray

# Get Ray dataset from sources
ray_ds = ray.data.read_datasource(data_source)

# Setup transform operations, not executed yet
transformed_ds = ray_ds.map_batches(example_transform_batch_function)

# Start writing to Snowflake distributedly
transformed_ds.write_datasink(datasink)
```

## Best Practices and Considerations

For optimal performance and resource utilization, consider the following best practices:

**Performance optimization for unstructured data**: When you work with many small files, such as images, audio, or other binary data:

- Use **stage sharding** to cut per-file I/O by consolidating small files into larger shards
- Balance file-count reduction against read parallelism when you choose a shard size
- See [Optimize unstructured data loading with stage sharding](#label-optimize-unstructured-data-loading) for the measured speedup and its conditions

**Performance optimization with disk cache**: The file-level disk cache serves repeated reads from node-local disk and is **enabled by default**:

- Tune it with `file_cache_config` when your dataset exceeds the cache budget
- Point `cache_dir` at fast NVMe storage when the node has a dedicated mount
- See [Optimize with file-level disk cache](#label-optimize-with-disk-cache) for the measured speedup, its conditions, and the freshness tradeoffs

**Parallelism**: Design your data source implementations to leverage Ray’s distributed nature. Customize the parallelism and concurrency arguments to better suit your use case. You can manually define how many resources you’re allocating per task in each step.

**Partitioning**: By default, Ray’s internal logic will partition the dataset based on resources and data size. You can customize number of partitions to choose between large number of small tasks vs small number of big tasks based on use case with `ray_ds.repartition(X)`.

**Best practices**: Follow [Ray Data User Guide](https://docs.ray.io/en/latest/data/user-guide.html) for additional guidance.

**Ray API details**:

- [Ray Datasource](https://docs.ray.io/en/latest/data/api/doc/ray.data.read_datasource.html)
- [Ray Map Batches (batch transformation)](https://docs.ray.io/en/latest/data/api/doc/ray.data.Dataset.map_batches.html)

## Next steps

After loading your data, you can:

- [Transform and engineer features](/developer-guide/snowflake-ml/transform-data)
- [Train models](/developer-guide/snowflake-ml/modeling)
- [Use the Feature Store](/developer-guide/snowflake-ml/feature-store/overview) for feature management
