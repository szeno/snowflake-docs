# Snowflake Container Runtime

## Overview

The Snowflake Container Runtime is a set of preconfigured customizable environments built for machine learning on Snowpark Container Services,
covering interactive experimentation and batch ML workloads such as model training, hyperparameter tuning, batch
inference and fine tuning. They include the most popular machine learning and deep learning frameworks. Used with
Snowflake notebooks, they provide an end-to-end ML experience.

## Execution environment

The Container Runtime provides an environment populated with packages and libraries that support a wide variety
of ML development tasks inside Snowflake. In addition to the pre-installed packages, you can import packages from
external sources like public PyPI repositories, or internally-hosted package repositories that provide a list of
packages approved for use inside your organization.

Executions of your custom Python ML workloads and supported training APIs occur within Snowpark Container Services, which offers the ability
to run on CPU or GPU compute pools. When using the Snowflake ML APIs, the Container Runtime distributes the processing
across available resources.

Container Runtimes are versioned, allowing you to select specific runtime environments, pin your workloads to a specific version,
and migrate to updated container runtime environments at your own pace.

## Distributed processing

The Snowflake ML modeling and data loading APIs are built on top of Snowflake ML’s distributed processing framework,
which maximizes resource utilization by fully leveraging the available compute power. By default, this framework uses
all GPUs on multi-GPU nodes, offering significant performance improvements compared to open-source packages and reduces
overall runtime.

![Diagram showing how workload is distributed for ML processing.](/static/images/container-runtimes/container-runtime-distribution.png)

Machine learning workloads, including data loading, are executed in a Snowflake-managed compute environment. The
framework allows dynamic scaling of resources based on the specific requirements of the task at hand, such as training
models or loading data. The number of resources, including GPU and memory allocation for each task, can be easily
configured through the provided APIs.

## Optimized data loading

The Container Runtime provides a set of data connector APIs that enable connecting Snowflake data sources (including
tables, DataFrames, and Datasets) to popular ML frameworks such as PyTorch and TensorFlow, taking full advantage of
multiple cores or GPUs. Once loaded, the data can be processed using open source packages, or any of the Snowflake ML
APIs, including the distributed versions that are described below. These APIs are found in the `snowflake.ml.data`
namespace.

The :class:`snowflake.ml.data.data_connector.DataConnector` class connects Snowpark DataFrames or Snowflake ML Datasets to
TensorFlow or PyTorch DataSets or Pandas DataFrames. Instantiate a connector using one of the following class methods:

> - `DataConnector.from_dataframe <snowflake.ml.data.data_connector.DataConnector.from_dataframe>`: Accepts a Snowpark DataFrame.
> - `DataConnector.from_dataset <snowflake.ml.data.data_connector.DataConnector.from_dataset>`: Accepts a Snowflake ML Dataset, specified by name and version.
> - `DataConnector.from_sources <snowflake.ml.data.data_connector.DataConnector.from_sources>`: Accepts list of sources, each of which can be a DataFrame or a Dataset.

Once you have instantiated the connector (calling the instance, for example, `data_connector`), call the following
methods to produce the desired kind of output.

- `data_connector.to_tf_dataset`: Returns a TensorFlow Dataset suitable for use with TensorFlow.
- `data_connector.to_torch_dataset`: Returns a PyTorch Dataset suitable for use with PyTorch.

For more information on these APIs, see the [Snowflake ML API reference](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/data).

## Building with open source

With the foundational CPU and GPU images that come pre-populated with popular ML packages, and the flexibility to
install additional libraries using `pip`, users can employ familiar and innovative open source frameworks inside Snowflake
Notebooks, without moving data out of Snowflake. You can scale processing by using Snowflake’s distributed
APIs for data loading, training, and hyperparameter optimization, with the familiar APIs of popular OSS
packages, with small changes to the interface to allow for scaling configurations.

The following code illustrates creating an XGBoost classifier using these APIs:

Copy code

```
from snowflake.snowpark.context import get_active_session
from snowflake.ml.data.data_connector import DataConnector
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

session = get_active_session()

# Use the DataConnector API to pull in large data efficiently
df = session.table("my_dataset")
pandas_df = DataConnector.from_dataframe(df).to_pandas()

# Build with open source

X = df_pd[['feature1', 'feature2']]
y = df_pd['label']

# Split data into test and train in memory
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=34)

# Train in memory
model = xgb.XGBClassifier()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)
```

The CPU container runtime has different packages than the GPU container runtime. The following sections list the packages available within each container runtime.

## Snowflake Container Runtime packages

The full list of available packages in Snowflake Container Runtime is maintained as part of the [Container Runtime Release Notes](/developer-guide/snowflake-ml/container-runtime/releases).

## Optimized training

Container Runtime offers a set of distributed training APIs, including distributed versions of LightGBM, PyTorch,
and XGBoost, that take full advantage of the available resources in the container environment. These are found in the
`snowflake.ml.modeling.distributors` namespace. The APIs of the distributed classes are similar to those of the
standard versions.

For more information on these APIs, see the [API reference](https://docs.snowflake.com/developer-guide/snowpark-ml/reference/latest/container-runtime/index).

### XGBoost

The primary XGBoost class is :class:`snowflake.ml.modeling.distributors.xgboost.XGBEstimator`. Related classes include:

- :class:`snowflake.ml.modeling.distributors.xgboost.XGBScalingConfig`

For an example of working with this API, see the
[XGBoost on GPU](https://github.com/Snowflake-Labs/sfguide-getting-started-with-container-runtime-apis/blob/main/XGBoost_on_GPU_Quickstart.ipynb)
example notebook in the Snowflake Container Runtime GitHub repository.

### LightGBM

The primary LightGBM class is :class:`snowflake.ml.modeling.distributors.lightgbm.LightGBMEstimator`. Related classes include:

- :class:`snowflake.ml.modeling.distributors.lightgbm.LightGBMScalingConfig`

For an example of working with this API, see the
[LightGBM on GPU](https://github.com/Snowflake-Labs/sfguide-getting-started-with-container-runtime-apis/blob/main/LightGBM_on_GPU_Quickstart.ipynb)
example notebook in the Snowflake Container Runtime GitHub repository.

### PyTorch

The primary PyTorch class is `snowflake.ml.modeling.distributors.pytorch.PyTorchDistributor`. Related classes and functions include:

- :class:`snowflake.ml.modeling.distributors.pytorch.WorkerResourceConfig`
- :class:`snowflake.ml.modeling.distributors.pytorch.PyTorchScalingConfig`
- :class:`snowflake.ml.modeling.distributors.pytorch.Context`
- :class:`snowflake.ml.modeling.distributors.pytorch.get_context`

For an example of working with this API, see the
[PyTorch on GPU](https://github.com/Snowflake-Labs/sfguide-getting-started-with-container-runtime-apis/blob/main/PyTorch_on_GPU_Quickstart.ipynb)
example notebook in the Snowflake Container Runtime GitHub repository.

## Next steps

- To try a Snowflake Notebook using Container Runtime, see [Notebooks on Container Runtime](/developer-guide/snowflake-ml/notebooks-on-spcs).
