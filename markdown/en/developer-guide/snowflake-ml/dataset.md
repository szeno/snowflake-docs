# Snowflake Datasets

Datasets are new Snowflake schema-level objects specifically designed for machine learning workflows. Snowflake Datasets
hold collections of data organized into versions. Each version holds a materialized snapshot of your data with
guaranteed immutability, efficient data access, and interoperability with popular deep learning frameworks.

Use Snowflake Datasets in the following situations:

- You need to manage and version large datasets for reproducible machine learning model training and testing.
- You need fine-grained file-level access and/or data shuffling for distributed training or data streaming.
- You need to integrate with external machine learning frameworks and tools.
- You need to track the lineage used to create an ML model.

Datasets are materialized data objects. You can use either Snowflake ML or SQL commands to interact with them.
They don’t appear in the Snowsight database object explorer.

Note

- Datasets incur storage costs. Delete unused datasets to minimize costs.
- Datasets created before the general availability release on [March 20, 2025](/release-notes/2025/other/2025-03-20-snowflake-ml-datasets), don’t support replication.
  For more information, see [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).

## Installation

The Dataset Python SDK is included in Snowpark ML (Python package `snowflake-ml-python`) starting in version 1.7.5.
For installation instructions, see [Using Snowflake ML Locally](/developer-guide/snowflake-ml/snowpark-ml#label-snowpark-ml-get-started).

## Required privileges

Creating Datasets requires the CREATE DATASET schema-level privilege. Modifying Datasets, for example adding or deleting
dataset versions, requires OWNERSHIP on the Dataset. Reading from a Dataset requires only the USAGE privilege on the
Dataset (or OWNERSHIP). For more information about granting privileges in Snowflake, see [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege).

Tip

Setting up privileges for the Snowflake Feature Store using either the `setup_feature_store` method or the
[privilege setup SQL script](/developer-guide/snowflake-ml/feature-store/rbac) also sets up Dataset privileges.
If you have already set up feature store privileges by one of these methods, no further action is needed.

## Creating and using Datasets

You can create and manage datasets with either SQL or Python. For information about using the SQL commands, see [SQL commands](#label-snowflake-ml-dataset-sql-commands).
For information about using the Python API, see [snowflake.ml.dataset](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/dataset).

Create a Dataset by passing a Snowpark DataFrame to the `snowflake.ml.dataset.create_from_dataframe` function.

Copy code

```
from snowflake import snowpark
from snowflake.ml import dataset

# Create Snowpark Session
# See https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-session
session = snowpark.Session.builder.configs(connection_parameters).create()

# Create a Snowpark DataFrame to serve as a data source
# In this example, we generate a random table with 100 rows and 1 column
df = session.sql(
  "select uniform(0, 10, random(1)) as x, uniform(0, 10, random(2)) as y from table(generator(rowcount => 100))"
)

# Materialize DataFrame contents into a Dataset
ds1 = dataset.create_from_dataframe(
    session,
    "my_dataset",
    "version1",
    input_dataframe=df)
```

Datasets are versioned. Each version is an immutable, point-in-time snapshot of the data managed by the Dataset. The
Python API includes a `Dataset.selected_version` property that indicates whether a given dataset is selected for use.
This property is automatically set by the `dataset.create_from_dataframe` and `dataset.load_dataset` factory
methods, so creating a dataset automatically selects the created version. The `Dataset.select_version` and
`Dataset.create_version` methods can also be used to explicitly switch between versions. Reading from a Dataset
reads from the active selected version.

Copy code

```
# Inspect currently selected version
print(ds1.selected_version) # DatasetVersion(dataset='my_dataset', version='version1')
print(ds1.selected_version.created_on) # Prints creation timestamp

# List all versions in the Dataset
print(ds1.list_versions()) # ["version1"]

# Create a new version
ds2 = ds1.create_version("version2", df)
print(ds1.selected_version.name)  # "version1"
print(ds2.selected_version.name)  # "version2"
print(ds1.list_versions())        # ["version1", "version2"]

# selected_version is immutable, meaning switching versions with
# ds1.select_version() returns a new Dataset object without
# affecting ds1.selected_version
ds3 = ds1.select_version("version2")
print(ds1.selected_version.name)  # "version1"
print(ds3.selected_version.name)  # "version2"
```

## Reading data from Datasets

Dataset version data is stored as evenly sized files in the Apache Parquet format. The API is extensible to support custom framework
connectors.

Reading from a Dataset requires an active selected version.

### Connect to TensorFlow

Datasets can be converted to TensorFlow’s `tf.data.Dataset` and streamed in batches for efficient training and evaluation.

Copy code

```
import tensorflow as tf

# Convert Snowflake Dataset to TensorFlow Dataset
tf_dataset = ds1.read.to_tf_dataset(batch_size=32)

# Train a TensorFlow model
for batch in tf_dataset:
    # Extract and build tensors as needed
    input_tensor = tf.stack(list(batch.values()), axis=-1)

    # Forward pass (details not included for brevity)
    outputs = model(input_tensor)
```

### Connect to PyTorch

Datasets also support conversion to PyTorch DataPipes and can be streamed in batches for efficient training and
evaluation.

Copy code

```
import torch

# Convert Snowflake Dataset to PyTorch DataPipe
pt_datapipe = ds1.read.to_torch_datapipe(batch_size=32)

# Train a PyTorch model
for batch in pt_datapipe:
    # Extract and build tensors as needed
    input_tensor = torch.stack([torch.from_numpy(v) for v in batch.values()], dim=-1)

    # Forward pass (details not included for brevity)
    outputs = model(input_tensor)
```

### Connect to Snowpark ML

Datasets can also be converted back to Snowpark DataFrames for integration with Snowpark ML Modeling. The converted
Snowpark DataFrame is not the same as the DataFrame that was provided during Dataset creation, but instead points to the
materialized data in the Dataset version.

Copy code

```
from snowflake.ml.modeling.ensemble import random_forest_regressor

# Get a Snowpark DataFrame
ds_df = ds1.read.to_snowpark_dataframe()

# Note ds_df != df
ds_df.explain()
df.explain()

# Train a model in Snowpark ML
xgboost_model = random_forest_regressor.RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    input_cols=["X"],
    label_cols=["Y"],
)
xgboost_model.fit(ds_df)
```

### Direct file access

The Dataset API also exposes an [fsspec](https://filesystem-spec.readthedocs.io/en/latest/) interface, which can be
used to build custom integrations with external libraries like PyArrow, Dask, or any other package that supports
`fsspec` and allows distributed and/or stream-based model training.

Copy code

```
print(ds1.read.files()) # ['snow://dataset/my_dataset/versions/version1/data_0_0_0.snappy.parquet']

import pyarrow.parquet as pq
pd_ds = pq.ParquetDataset(ds1.read.files(), filesystem=ds1.read.filesystem())

import dask.dataframe as dd
dd_df = dd.read_parquet(ds1.read.files(), filesystem=ds1.read.filesystem())
```

## Dataset, Feature Store, Model Registry, and ML Lineage

> Datasets are deeply integrated into the Snowflake ML ecosystem to provide a seamless end-to-end model development and
> MLOps experience inside Snowflake. Datasets can be produced from Snowflake Feature Store features by using the
> `FeatureStore.generate_dataset` API. Datasets can then be converted to Snowpark DataFrames and passed to Snowpark ML
> Modeling for model training. The trained model can then be logged to Snowflake Model Registry, automatically completing
> the ML Lineage graph linking source data, feature views, datasets, and models for full end-to-end governance.

### Use SQL to read from a dataset version

You can use standard Snowflake SQL commands to read data from a dataset version. You can use SQL commands to do the following operations:

- List files
- Infer schema
- Query data directly from stage.

Important

You must have the USAGE or OWNERSHIP privilege on the dataset to read from it.

#### List files from a dataset version

Use the `LIST snow_url` command to list files in a dataset version. Use the following SQL syntax to list all files within a dataset version:

Copy code

```
LIST 'snow://dataset/<dataset_name>/versions/<dataset_version>'
```

#### Analyze files and get column definitions

Use the [INFER\_SCHEMA](/sql-reference/functions/infer_schema) function to analyze files in a dataset version and retrieve column definitions. Use the following SQL example to list all files within a dataset version:

Copy code

```
INFER_SCHEMA(
  LOCATION => 'snow://dataset/<dataset_name>/versions/<dataset_version>',
  FILE_FORMAT => '<file_format_name>'
)
```

You must use the pattern specified in the example to get the location of the dataset version.

For `FILE_FORMAT`, specify `PARQUET`.

The following example creates a file format and runs the INFER\_SCHEMA function:

Copy code

```
CREATE FILE FORMAT my_parquet_format TYPE = PARQUET;

SELECT *
FROM TABLE(
    INFER_SCHEMA(
        FILE_FORMAT => 'snow://dataset/MYDS/versions/v1,
        FILE_FORMAT => 'my_parquet_format'
    )
);
```

#### Stage query

Query data directly from the files stored in a dataset version, in a similar manner to querying an external table. Use the following SQL example to help you get started:

Copy code

```
SELECT $1
FROM 'snow://dataset/foo/versions/V1'
( FILE_FORMAT => 'my_parquet_format',
PATTERN => '.*data.*' ) t;
```

## SQL commands

You can use SQL commands to create and manage datasets. For more information, see:

- [CREATE DATASET](/sql-reference/sql/create-dataset)
- [ALTER DATASET](/sql-reference/sql/alter-dataset)
- [SHOW DATASETS](/sql-reference/sql/show-datasets)
- [SHOW VERSIONS IN DATASET](/sql-reference/sql/show-versions-in-dataset)

## Current limitations and known issues

- Dataset names are SQL identifiers and subject to [Snowflake identifier requirements](/sql-reference/identifiers-syntax).
- Dataset versions are strings and have a maximum length of 128 characters. Some characters are not permitted and will
  produce an error message.
- Certain query operations on Datasets with wide schemas (more than about 4,000 columns) are not fully optimized. This
  should improve in upcoming releases.
