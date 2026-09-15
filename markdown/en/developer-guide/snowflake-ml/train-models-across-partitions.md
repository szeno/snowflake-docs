# Train models across data partitions

Use Many Model Training (MMT) to train multiple machine learning models efficiently across data partitions. It handles distributed orchestration, model storage, and artifact persistence automatically.

MMT partitions your Snowpark DataFrame by a specified column and trains separate models on each partition in parallel. Focus on your model training logic while MMT handles infrastructure complexity and scales automatically.

You can use MMT to train multiple models efficiently across different data segments. This tool is ideal for scenarios like training region-specific sales forecasting models, building personalized recommendation systems where each customer group requires its own model, or creating segment-specific predictive models. MMT handles the distributed model training automatically, eliminating the complexity of managing distributed computing infrastructure.

You can use MMT to train models using open source machine learning models and frameworks such as XGBoost, scikit-learn, PyTorch, and TensorFlow. MMT automatically serializes model artifacts, so that you can access them at the time of inference.

You can also implement the ModelSerde interface to train custom models or use unsupported ML frameworks. This allows you to integrate MMT with any machine learning framework or custom model architecture that you use.

Important

Before you use MMT, make sure you have the following:

- **Container Runtime Environment**: MMT requires a Snowflake ML container runtime environment.
- **Stage Access Permissions**: MMT automatically stores model artifacts in Snowflake stages. Ensure you have appropriate permissions to access the specified named stage.
- **ML Framework Support**: Built-in integrations are available for XGBoost, scikit-learn, PyTorch, and TensorFlow. For custom models, implement the ModelSerde interface.

The following section walks you through using MMT in an example workflow.

## Training a model with MMT

This section demonstrates the complete MMT workflow in five key steps:

1. **Import your data** - Load training data using Snowpark
2. **Define the training function** - Define the training function
3. **Train models across partitions** - Use MMT to train models on each partition in parallel
4. **Access trained models** - Retrieve and use the trained models for each partition
5. **Model persistence and retrieval** - Save models to stages and restore them later

The workflow automatically handles distributed training, model serialization, and artifact storage across your data partitions.

### Import your data

Use a Snowpark session to start importing your data. The Many Model Training function splits the data that you import into different partitions using the column that you specify.

Before you use MMT, create a Snowpark session. For more information, [Creating a Session for Snowpark Python](/developer-guide/snowpark/python/creating-session).

The following code uses a Snowpark session to import your training data.

Copy code

```
# Example: sales_data with columns: region, feature1, feature2, feature3, target
sales_data = session.table("SALES_TRAINING_DATA")
```

### Define the training function

After you get your data, you define the training function that MMT uses to train models across partitions. The training function receives a data connector and a context object that points it to the data partition on which it’s training. This section has examples defining a training function for training an XGBoost model in addition to examples that leverage TensorFlow and PyTorch.

Your training function must have this exact signature: `(data_connector, context)`.
For each data partition, MMT calls `train_xgboost_model` with the following arguments:

- `data_connector`: A data connector that provides access to the data that MMT partitions. `train_xgboost_model` converts that dataframe to pandas.
- `context`: An object that provides the `partition_id` to the `train_xgboost_model` function. This ID is the name of the column that you’re partitioning on.

You don’t call this function yourself. MMT handles the execution across all partitions.

Use the following code to define your training function. After you change the code to reflect the features in your data, you can pass it to the MMT function.

XGBoostPyTorchTensorFlowCustom model

Use XGBoost to train models across data partitions. XGBoost provides excellent performance for structured data and handles missing values automatically.

Copy code

```
def train_xgboost_model(data_connector, context):
    df = data_connector.to_pandas()
    print(f"Training model for partition: {context.partition_id}")

    # Prepare features and target
    X = df[['feature1', 'feature2', 'feature3']]
    y = df['target']

    # Train the model
    from xgboost import XGBRegressor
    model = XGBRegressor(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X, y)
    return model

trainer = ManyModelTraining(train_xgboost_model, "model_stage")
```

Use PyTorch to train deep learning models across data partitions. PyTorch offers flexible neural network architectures and dynamic computation graphs.

Copy code

```
def train_pytorch_model(data_connector, context):
    import torch
    import torch.nn as nn

    df = data_connector.to_pandas()
    # ... prepare data for PyTorch ...

    model = nn.Sequential(nn.Linear(10, 1))
    # ... training logic ...
    return model  # Automatically saved as model.pth

from snowflake.ml.modeling.distributors.many_model import TorchSerde
trainer = ManyModelTraining(train_pytorch_model, "models_stage", serde=TorchSerde())
```

Use TensorFlow to train deep learning models across data partitions. TensorFlow provides comprehensive tools for both research and production deployment.

Copy code

```
def train_tf_model(data_connector, context):
    import tensorflow as tf

    df = data_connector.to_pandas()
    # ... prepare data for TensorFlow ...

    model = tf.keras.Sequential([tf.keras.layers.Dense(1)])
    # ... training logic ...
    return model  # Automatically saved as model.h5

from snowflake.ml.modeling.distributors.many_model import TensorFlowSerde
trainer = ManyModelTraining(train_tf_model, "models_stage", serde=TensorFlowSerde())
```

Use custom models or unsupported ML frameworks by implementing the ModelSerde interface. This example shows scikit-learn with custom metadata handling.

Copy code

```
from snowflake.ml.modeling.distributors.many_model import ModelSerde
import json

class ScikitLearnSerde(ModelSerde):
    '''Custom serializer for scikit-learn models with metadata'''

    @property
    def filename(self) -> str:
        return "sklearn_model.joblib"

    def write(self, model, file_path: str) -> None:
        import joblib
        # Save model with metadata
        model_data = {
            'model': model,
            'feature_names': getattr(model, 'feature_names_in_', None),
            'model_type': type(model).__name__
        }
        joblib.dump(model_data, file_path)

    def read(self, file_path: str):
        import joblib
        return joblib.load(file_path)

def train_sklearn_model(data_connector, context):
    from sklearn.ensemble import RandomForestRegressor
    df = data_connector.to_pandas()
    X, y = df[['feature1', 'feature2']], df['target']

    model = RandomForestRegressor()
    model.fit(X, y)
    return model  # Automatically saved with metadata

trainer = ManyModelTraining(train_sklearn_model, "models_stage", serde=ScikitLearnSerde())
```

### Train models across partitions

After you’ve defined your training function, you can use MMT to train models across partitions. Specify the column to partition by and the stage where the models are saved.

The following code partitions the data by the `region` column and uses the `train_xgboost_model` function to train separate models for each region in parallel.

For example, if the following were the possible values for the `region` column:

- North
- South
- East
- West
- Central

The `ManyModelTraining` function would create a separate data partition for each of the preceding regions and train a model on each partition.

Copy code

```
from snowflake.ml.modeling.distributors.many_model import ManyModelTraining

trainer = ManyModelTraining(train_xgboost_model, "model_stage") # Specify the stage to store the models
training_run = trainer.run(
    partition_by="region",  # Train separate models for each region
    snowpark_dataframe=sales_data,
    run_id="regional_models_v1" # Specify a unique ID for the training run
)

# Monitor training progress
final_status = training_run.wait()
print(f"Training completed with status: {final_status}")
```

Models are stored in the stage at `run_id/{partition_id}` where `partition_id` is the partition column value.

### Access trained models

After MMT finishes, you have trained models for each data partition stored in your specified stage. Each model is trained on data specific to its partition. For example, a “North” model is trained only on North region data.

The training run object provides methods to access these models and check training status for each partition.

The following code retrieves the checks the status of the training run and retrieves the trained models for each partition:

Copy code

```
if final_status == RunStatus.SUCCESS:
    # Access models for each partition
    for partition_id in training_run.partition_details:
        trained_model = training_run.get_model(partition_id)
        print(f"Model for {partition_id}: {trained_model}")

        # You can now use the model for predictions or further analysis
        # Example: model.predict(new_data)
else:
    # Handle training failures
    for partition_id, details in training_run.partition_details.items():
        if details.status != "DONE":
            print(f"Training failed for {partition_id}")
            error_logs = details.logs
```

### Model Persistence and Retrieval

MMT automatically persists trained models to your specified Snowflake stage during the training process. Each model is stored with a structured path that includes the run ID and partition identifier, making it easy to organize and retrieve models later.

The automatic persistence means you don’t need to manually save models. MMT handles serialization and storage for you, eliminating the risk of losing trained models due to session timeouts or connection issues.

You can restore previous training runs and access their models even after your original session has ended. This persistence mechanism enables you to:

- Resume work across different sessions
- Share trained models with team members
- Build model versioning workflows
- Integrate with downstream inference pipelines

Models are automatically saved to the specified stage and can be retrieved later:

Copy code

```
# Restore training run from stage
restored_run = ManyModelTraining.restore_from("regional_models_v1", "model_stage")

# Access models from restored run
north_model = restored_run.get_model("North")
south_model = restored_run.get_model("South")
```

## Training custom models

For custom models or unsupported ML frameworks, implement the ModelSerde interface. You can define your own serialization and deserialization logic for custom models. This allows you to integrate MMT with any machine learning framework or custom model architecture that you use.

Copy code

```
from snowflake.ml.modeling.distributors.many_model import ModelSerde

class CustomModelSerde(ModelSerde):
    def serialize(self, model, path):
        # Custom serialization logic
        pass

    def deserialize(self, path):
        # Custom deserialization logic
        pass

def train_custom_model(data_connector, context):
    # Your custom training logic
    model = your_custom_model_training(data_connector.to_pandas())
    return model

trainer = ManyModelTraining(
    train_custom_model,
    "custom_model_stage",
    model_serde=CustomModelSerde()
)
```

## Integrating with Model Registry

MMT can be integrated with Snowflake’s Model Registry for enhanced model management. The Model Registry provides centralized model versioning, metadata tracking, and deployment management across your organization. This integration is particularly valuable when training multiple models with MMT, as it helps you organize, track, and govern all the partition-specific models from a single location.

Using the Model Registry with MMT enables you to do the following:

- Track different iterations of your partition-specific models
- Store model performance metrics, training parameters, and lineage information
- Manage which model versions are deployed to production for each partition
- Share models across teams with proper access controls and documentation
- Implement approval workflows and compliance tracking for model deployments

You can wrap all of the per-partition models in a single partitioned model and log it as one model version. This approach keeps related models grouped together and lets you serve predictions for every partition through a single inference call.

First, define a custom model that holds all per-partition models in its `ModelContext`. The `ModelContext` maps each partition ID to its trained model, so the `predict` method can look up the right model at inference time and route the batch to the corresponding partition’s model.

Copy code

```
import pandas as pd
from snowflake.ml.model import custom_model

partition_models = {
    partition_id: training_run.get_model(partition_id)
    for partition_id in training_run.partition_details
}

class PartitionedSalesModel(custom_model.CustomModel):
    def __init__(self, context: custom_model.ModelContext) -> None:
        super().__init__(context)
        self.partition_id_cache = None
        self.model = None

    @custom_model.inference_api
    def predict(self, input_df: pd.DataFrame) -> pd.DataFrame:
        current_partition = input_df["region"].iloc[0]
        if self.partition_id_cache != current_partition:
            self.partition_id_cache = current_partition
            self.model = self.context.model_ref(current_partition)

        preds = self.model.predict(input_df[["feature1", "feature2", "feature3"]])
        return pd.DataFrame({"prediction": preds})

partitioned_model = PartitionedSalesModel(custom_model.ModelContext(models=partition_models))
```

Next, log the partitioned model to the Model Registry as a single model version. Set `function_type="TABLE_FUNCTION"` so that you can invoke the model with a `PARTITION BY region` clause at inference time, which ensures each batch passed to `predict` contains rows from a single partition.

Copy code

```
from snowflake.ml.registry import Registry

registry = Registry(session=session)

mv = registry.log_model(
    model=partitioned_model,
    model_name="regional_sales_model_partitioned",
    version_name="v1",
    sample_input_data=...,
    options={"function_type": "TABLE_FUNCTION"},
)
```

For more information about partitioned models, see [Using partitioned models](/developer-guide/snowflake-ml/model-registry/partitioned-models).
