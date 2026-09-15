# Train models

Use Snowflake ML to develop machine learning and deep learning models with popular open-source frameworks.
Snowflake ML provides flexible development environments, efficient data access, and powerful compute resources without the management overhead.

You can train a model within either a Snowflake Notebook or a Snowflake ML Job.

Snowflake Notebooks are interactive environments that you can use for machine learning. For more information about using Snowflake Notebooks for machine learning workflows, see [Notebooks on Container Runtime](/developer-guide/snowflake-ml/notebooks-on-spcs).

Snowflake ML Jobs allow you to run ML workflows from any environment. For more information about using Snowflake ML Jobs, see [Snowflake ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview).

With Snowflake Experiments, you can compare your trained models in an organized manner. Use information logged during model training to evaluate the results and select the best model for your needs. For more information, see [Run an experiment to compare and select models](/developer-guide/snowflake-ml/experiments).

## Train with open source

When you use a Snowflake Notebook or ML Job, you get access to the Container Runtime. The Container Runtime is an environment that has popular packages and frameworks that you can use to train your models.
The packages include scikit-learn, numpy, and scipy. For more information, see [Snowflake Container Runtime](/developer-guide/snowflake-ml/container-runtime-ml).

The following example trains a logistic regression model using scikit-learn:

Copy code

```
import pandas as pd
from snowflake.ml.data.data_connector import DataConnector
from snowflake.snowpark.context import get_active_session
from sklearn.linear_model import LogisticRegression

# Get the active Snowpark session
session = get_active_session()

# Specify training table location
table_name = "TRAINING_TABLE"  # Replace with your actual Snowflake table name

# Load table into DataConnector
data_connector = DataConnector.from_dataframe(session.table(table_name))

# Convert to pandas DataFrame
pandas_df = data_connector.to_pandas()

# Assuming 'TARGET' is the label column in your Snowflake table
label_column_name = 'TARGET'

# Separate features (X) and target (y)
X, y = pandas_df.drop(label_column_name, axis=1), pandas_df[label_column_name]

# Initialize and fit a Logistic Regression model
logistic_regression_model = LogisticRegression(max_iter=1000)  # Increased max_iter for convergence
logistic_regression_model.fit(X, y)
```

In addition to scikit-learn, you can use the XGBoost and LightGBM libraries to develop powerful classification, regression, and ranking models.

The following example loads data from a Snowflake table using the Snowflake DataConnector, converts it to a pandas DataFrame, and trains an XGBoost model.
The DataConnector accelerates data loading and pandas dataframe conversion. For more information about the DataConnector, see [Load structured data from Snowflake tables](/developer-guide/snowflake-ml/load-data#label-load-data-from-snowflake-tables)

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

pandas_df = data_connector.to_pandas()
label_column_name = 'TARGET'
X, y = pandas_df.drop(label_column_name, axis=1), pandas_df[label_column_name]

clf = xgb.Classifier()
clf.fit(X, y)
```

## Train deep learning models

You can use a GPU-powered container runtime image to train deep learning models with PyTorch, TensorFlow, and other frameworks. You can use the pre-installed libraries or you can extend the base image with packages from either public or private repositories.

You can get GPU compute on demand from your available compute pools. You only pay for the resources that you use.

With the GPU container runtime image, you can use features such as distributed training to accelerate the development of large-scale models.

For an example of efficient data loading with DataConnector and distributed training, see [Running Distributed PyTorch Models on Snowflake: An End-to-End ML Solution](https://www.snowflake.com/en/developers/solutions-center/running-distributed-pytorch-models-on-snowflake-an-end-to-end-ml-solution/).

The following example loads data efficiently:

Copy code

```
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from snowflake.ml.data.data_connector import DataConnector

example_snowpark_dataframe = session.table("EXAMPLE_TRAINING_DATA")

# Connector from a Snowflake table
data_connector = DataConnector.from_dataframe(example_snowpark_dataframe)

# Load as a torch dataset
torch_dataset = data_connector.to_torch_dataset(batch_size=32)
train_loader = DataLoader(torch_dataset, batch_size=None)

label_col = 'TARGET'
feature_cols = ['FEATURE1', 'FEATURE2']

for batch_idx, batch in enumerate(dataloader):
    y = batch_data.pop(label_col).squeeze()
    X = torch.stack(
        [tensor.squeeze() for key, tensor in batch.items() if key in feature_cols]
    )
```

The following example trains a model:

Copy code

```
# ------------------------
# Tiny MLP for binary classification
# ------------------------
input_dim = X.shape[1]

class MLP(nn.Module):
    def __init__(self, d_in):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_in, 64), nn.ReLU(),
            nn.Linear(64, 32), nn.ReLU(),
            nn.Linear(32, 1)  # logits
        )

    def forward(self, x):
        return self.net(x).squeeze(1)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MLP(input_dim).to(DEVICE)
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.BCEWithLogitsLoss()

# ------------------------
# Train
# ------------------------
EPOCHS = 5

for epoch in range(1, EPOCHS + 1):
    model.train()
    for xb, yb in train_loader:
        xb, yb = xb.to(DEVICE), yb.to(DEVICE)
        logits = model(xb)
        loss = criterion(logits, yb)
        opt.zero_grad()
        loss.backward()
        opt.step()
    acc = evaluate(val_loader)
    print(f"epoch {epoch} val_acc={acc:.3f}")
```

## Handle complex training tasks

Training models on large datasets, complex model architectures and hyperparameters requires significant time, cost, and access to resources that facilitate such complex processing. With Snowflake ML, you can train such models in confidence.

### Fully managed training infrastructure

Snowflake ML provides fully managed training infrastructure through Notebooks and ML Jobs on Container Runtime. You don’t need to manage custom images or provision resources. You can bring your workload, select the appropriate compute nodes from the admin-determined list, and start training.

### Efficient and accelerated data movement

Loading large amounts of data into memory for processing with training packages can be slow, especially when you’re trying to read directly into an object such as a pandas dataframe. Snowflake ML makes data loading efficient by using the distributed processing of the underlying compute pools. Use the Data Connector to load from your Snowflake tables and stages into open source objects such as pandas dataframes, PyTorch datasets, and TensorFlow datasets.

### Distributed training and hyperparameter tuning

Training ML models on large datasets can exceed the resources of a single node. With Snowflake’s distributed APIs, you can scale feature engineering and training workflows across multiple nodes for improved performance. With the distributed APIs, you can do the following:

- Leverage distributed preprocessing functions in `snowflake.ml.modeling.preprocessing`.
- Scale your model training out across one or more nodes using optimized training APIs in [Snowflake Container Runtime](/developer-guide/snowflake-ml/container-runtime-ml).
- Accelerate hyperparameter tuning with Snowflake ML’s [distributed HPO](/developer-guide/snowflake-ml/container-hpo), optimized for data stored in Snowflake. You can also use open source libraries like `hyperopt` or `optuna`.

In addition to using Snowflake’s distributed APIs to scale your workflows, you can also use Ray. Ray is an open-source framework that provides a simple and flexible way to scale Python applications. It allows you to run your code in parallel across multiple nodes. For more information about using Ray with Snowflake ML, see the [Ray Getting Started Guide](https://docs.ray.io/en/latest/ray-overview/getting-started.html).

## Integrate with MLOps

Snowflake provides a fully integrated MLOps platform that you can access through Snowflake Notebooks and ML Jobs. This enables you to train models using production-ready features, manage experiments and models, and deploy trained models to production.

You can use the following features for your MLOps workflow:

- Create and manage features via the Feature Store
- Run feature pre-processing at scale with OSS and SnowflakeML APIs
- Manage experiments with built-in experiment tracking
- Register and manage the trained model
- Run inference pipelines against the registered model
- Monitor the deployed model for drift and accuracy

## Next steps

After training your models, you can:

- [Tune hyperparameters](/developer-guide/snowflake-ml/container-hpo) to optimize performance
- [Train across partitions](/developer-guide/snowflake-ml/train-models-across-partitions) for large-scale model training
- [Register models](/developer-guide/snowflake-ml/model-registry/overview) in the Model Registry
- [Deploy models](/developer-guide/snowflake-ml/inference/native-batch-inference-sql) for inference
