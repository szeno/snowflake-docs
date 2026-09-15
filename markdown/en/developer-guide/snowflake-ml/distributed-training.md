# Distributed training

The Snowflake Container Runtime provides a flexible training environment that you can use to train models on Snowflake’s infrastructure. You can use open source packages, or use Snowflake ML distributed trainers for multi-node and multi-device training.

Distributed trainers automatically scale your machine learning workloads across multiple nodes and GPUs. Snowflake distributors intelligently manage cluster resources without requiring complex configuration, making distributed training accessible and efficient.

**Use standard open source libraries when you**

- Work with small datasets on single-node environments
- Rapidly prototype and experiment with models
- Lift and shift workflows without distributed requirements

**Use Snowflake Distributed Trainers To:**

- Train models on datasets that are larger than the memory of a single compute node
- Utilize multiple GPUs efficiently
- Automatically leverage all compute multi-node MLJobs or scaled notebook clusters

## Snowflake ML distributed training

Snowflake ML provides distributed trainers for popular machine learning frameworks, including XGBoost, LightGBM, and PyTorch. These trainers are optimized to run on Snowflake’s infrastructure and can automatically scale across multiple nodes and GPUs.

- **Automatic Resource Management** - Snowflake automatically discovers and uses all available cluster resources
- **Simplified Setup** - The Container Runtime environment is backed by a Ray cluster provided by Snowflake, with no user configuration required
- **Seamless Snowflake integration** - Direct compatibility with Snowflake data connectors and stages
- **Optional scaling configs** - Advanced users can fine-tune when needed

### Data loading

For both open source and Snowflake distributed trainers, the most performant way to ingest data is with the Snowflake Data Connector:

Copy code

```
from snowflake.ml.data.data_connector import DataConnector

# Load data
train_connector = DataConnector.from_dataframe(session.table('TRAINING_DATA'))
eval_connector = DataConnector.from_dataframe(session.table('EVAL_DATA'))
```

### Training methods

#### Open source training

Use standard open source libraries when you need maximum flexibility and control over your training process. With open source training, you directly use popular ML frameworks like XGBoost, LightGBM, and PyTorch with minimal modifications, while still benefiting from Snowflake’s infrastructure and data connectivity.

The following examples train a model with XGBoost and LightGBM.

XGBoostLightGBM

To train with open source XGBoost, after loading data with the data connector, convert it into a pandas dataframe and use the XGB library directly:

Copy code

```
import xgboost as xgb

train_df = train_connector.to_pandas()
eval_df = eval_connector.to_pandas()

# Create DMatrix
train_df = train_connector.to_pandas()
dtrain = xgb.DMatrix(train_df[INPUT_COLS], label=train_df[LABEL_COL])
deval = xgb.DMatrix(eval_df)

# Training parameters
params = {
   'objective': 'reg:squarederror',
   'max_depth': 6,
   'learning_rate': 0.1
}

# Train and evaluate model
evals_result = {}
model = xgb.train(
   params,
   dtrain,
   num_boost_round=100,
   evals=[(dtrain, 'train'), (deval, 'valid')],
   evals_result=evals_result
)

# Access the evaluation results
print(evals_result)
```

Copy code

```
from snowflake.ml.modeling.distributors.lightgbm import LightGBMEstimator, LightGBMScalingConfig

# Training parameters
params = {
   'objective': 'regression',
   'metric': 'rmse',
   'boosting_type': 'gbdt',
   'num_leaves': 31,
   'learning_rate': 0.05,
   'feature_fraction': 0.9
}

# Automatic scaling (recommended)
estimator = LightGBMEstimator(
   params=params
)

# Call with custom GPU scaling
gpu_estimator = LightGBMEstimator(
   params=params,
   scaling_config=LightGBMScalingConfig(use_gpu=True) # optional - available resources will be used automatically
)

# Train and evaluate
booster = estimator.fit(
   dataset=train_connector,
   input_cols=['age', 'income', 'credit_score'],
   label_col='default_risk',
   eval_set=eval_connector,
   verbose_eval=10
)

# Access results
booster = estimator.get_booster() # If you forgot to save the output of fit, get the booster from the estimator
feature_importance = booster.feature_importance(importance_type='gain')
```

#### Distributed training

The distributed `XGBEstimator` class has a similar API with a few key differences:

- The XGBoost training parameters are passed to the `XGBEstimator` during class initialization through the “params” parameter.
- The DataConnector object can be passed directly into the estimator’s `fit` function, along with the input columns defining the features and the label column defining the target.
- You can provide a scaling configuration when instantiating the `XGBEstimator` class. However, Snowflake defaults to using all available resources.

Copy code

```
from snowflake.ml.modeling.distributors.xgboost import XGBEstimator, XGBScalingConfig

# Training parameters
params = {
    'objective': 'reg:squarederror',
    'max_depth': 6,
    'learning_rate': 0.1
}

# Automatic scaling (recommended)
estimator = XGBEstimator(
    params=params
)

# Call with custom GPU scaling
gpu_estimator = XGBEstimator(
    params=params,
    scaling_config=XGBScalingConfig(use_gpu=True) # optional - available resources will be used automatically
)

# Train and evaluate
booster = estimator.fit(
    dataset=train_connector,
    input_cols=['age', 'income', 'credit_score'],
    label_col='default_risk',
    eval_set=eval_connector,
    verbose_eval=10
)

# Access results
booster = estimator.get_booster() # If you forgot to save the output of fit, get the booster from the estimator
feature_importance = booster.get_score(importance_type='gain')
```

#### Evaluating the model

Models can be evaluated by passing an `eval_set` and using `verbose_eval` to print the evaluation data to the console. Additionally, inference can be done as a second step. The distributed estimator offers a `predict` method for convenience, but it will not do inference in a distributed fashion. We recommend converting the fit model into an OSS xgboost estimator after training in order to do inference and to log to the model registry.

#### Registering the model

To register the model to the Snowflake model registry, use the open source booster provided by `estimator.get_booster` and returned from `estimator.fit`. For more information, see [XGBoost](/developer-guide/snowflake-ml/model-registry/built-in-models/xgboost).

#### PyTorch

The Snowflake PyTorch Distributor natively supports Distributed Data Parallel models on the Snowflake backend. To use DDP on Snowflake, leverage open source PyTorch modules with a few Snowflake specific modifications:

- Load data using the `ShardedDataConnector` to automatically shard data into the number of partitions that matches the `world_size` of the distributed trainer. Call `get_shard` within a Snowflake training context to retrieve the shard associated with that worker process.
- Inside the training function, use the `context` object to get process specific information like rank, local rank, and the data required for training.
- Save the model using the context’s `get_model_dir` to find the location to store the model to. This will store the model locally for single node training, and sync the model to a Snowflake stage for distributed training. If no stage location is provided, your user stage will be used by default.

#### Load data

Copy code

```
# Create ShardedDataConnector for data ingestion
from snowflake.ml.data.sharded_data_connector import ShardedDataConnector

example_snowpark_dataframe = session.table("EXAMPLE_TRAINING_DATA")

data_connector = ShardedDataConnector.from_dataframe(example_snowpark_dataframe)
```

#### Train model

Copy code

```
# Import necessary PyTorch libraries
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# Define a simple neural network
class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Define the training function
def train_func():
    import torch.distributed as dist
    from torch.nn.parallel import DistributedDataParallel as DDP
    from snowflake.ml.modeling.distributors.pytorch import get_context

    # Use the Snowflake context to get the necessary methods to manage and retrieve information about the distributed training environment
    context = get_context()
    rank = context.get_rank()
    dist.init_process_group(backend='gloo')
    device = torch.device(f"cuda:{context.get_local_rank()}"
                         if torch.cuda.is_available() else "cpu")

    # Initialize model, loss function, and optimizer
    model = SimpleNet(input_size=len(input_cols), hidden_size=32, output_size=1).to(device)
    model = DDP(model)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Retrieve training data
    dataset_map = context.get_dataset_map()
    torch_dataset = dataset_map['train'].get_shard().to_torch_dataset(batch_size=1024)
    dataloader = DataLoader(torch_dataset)

    # Training loop
    for epoch in range(10):
        for batch_dict in dataloader:
            features = torch.cat([batch_dict[col].T for col in input_cols], dim=1).float().to(device)
            labels = batch_dict[label_col].T.squeeze(0).float().to(device)
            output = model(features)
            loss = criterion(output, labels.unsqueeze(1))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print(f'Epoch [{epoch+1}/10], Loss: {loss.item():.4f}')

    # Save the model to the model directory provided by the context
    if context.get_rank() == 0:
        torch.save(
            model.module.state_dict(), os.path.join(context.get_model_dir(), "model.pt")
        )

# Set up PyTorchDistributor for distributed training
from snowflake.ml.modeling.distributors.pytorch import PyTorchDistributor, PyTorchScalingConfig, WorkerResourceConfig

pytorch_trainer = PyTorchDistributor(
    train_func=train_func,
    # Optional Scaling Configuration, for single node multi-GPU training.
    scaling_config=PyTorchScalingConfig(
        num_nodes=1,
        num_workers_per_node=1,
        resource_requirements_per_worker=WorkerResourceConfig(num_cpus=0, num_gpus=4)
    )
)

# Run the training process
pytorch_trainer.run(dataset_map={'train': data_connector})
```

#### Retrieving the model

If you are using multi-node DDP, the model is automatically synchronized to a Snowflake stage as the shared persistent storage.

The following code gets the model from a stage. It uses the `artifact_stage_location` parameter to specify the location of the stage that stores the model artifact.

The function saved in the `stage_location` variable gets the location of the model in the stage after training completes. The model artifact is saved under `"DB_NAME.SCHEMA_NAME.STAGE_NAME/model/{request_id}"`.

Copy code

```
response = pytorch_trainer.run(
        dataset_map={'train': data_connector},
        artifact_stage_location="DB_NAME.SCHEMA_NAME.STAGE_NAME",
    )

stage_location = response.get_model_dir()
```
