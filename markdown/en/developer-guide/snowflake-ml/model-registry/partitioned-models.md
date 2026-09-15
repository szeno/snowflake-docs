# Using partitioned models

Many datasets can be partitioned into multiple independent subsets. For example, a dataset containing sales data
for a chain of stores can be partitioned by store number. A separate model can then be trained for each partition.
Training and inference operations on the partitions can be parallelized, reducing the wall-clock time for these
operations. Furthermore, since individual stores likely differ significantly in how their features affect their
sales, this approach can lead to more accurate inference at the store level.

The Snowflake Model Registry supports distributed processing of training and inference of partitioned data when:

- The dataset contains a column that reliably identifies partitions in the data.
- The data in each individual partition is uncorrelated with the data in the other partitions and contains enough
  rows to train the model.

Models may be stateless (training is performed each time inference is called) or stateful (training is performed once
before inference and retained for use in multiple inference operations).

With the Snowflake Model Registry, implement partitioned training and inference using
[custom models](/developer-guide/snowflake-ml/model-registry/bring-your-own-model-types). During inference, the model
inference method partitions the dataset, generates predictions for each partition in parallel using all the nodes and
cores in your warehouse, and combines the results into a single dataset afterward.

Note

For partitioned models, it’s important to distinguish the registered model from the individual models that
are created by or compose the registered model. Where possible, we will refer to the individual underlying models
as submodels.

## Defining and logging the model

The partitioned model class inherits from *snowflake.ml.model.custom\_model.CustomModel*. Inference methods are declared
with either the `@custom_model.partitioned_api` or the `@custom_model.inference_api` decorator, depending on how the
method processes each partition. See
[Bring your own model types via serialized files](/developer-guide/snowflake-ml/model-registry/bring-your-own-model-types) for information on defining standard custom models.

Use `@custom_model.partitioned_api` when the method operates on all the rows of a partition at once (for example, to
train a model on the partition or to produce a different number of output rows than input rows). The following example
is stateless: it processes each partition independently on every call and retains no fit state between calls:

Copy code

```
import pandas as pd

from snowflake.ml.model import custom_model

class ExampleStatelessPartitionedModel(custom_model.CustomModel):

  @custom_model.partitioned_api
  def predict(self, input: pd.DataFrame) -> pd.DataFrame:
      # All data in the partition will be loaded in the input dataframe.
      #… implement model logic here …
      return output_df

my_model = ExampleStatelessPartitionedModel()
```

Alternatively, use `@custom_model.inference_api`. When inference is partitioned, each call receives rows from a single
partition. The model can load a submodel only when the partition changes, caching it and reusing it while it keeps
receiving rows for the same partition. This reduces loading overhead when loading is expensive, such as deserializing
the submodel from bytes:

Copy code

```
from typing import Optional

import pandas as pd

from snowflake.ml.model import custom_model

class ExampleStatefulPartitionedModel(custom_model.CustomModel):

  def __init__(self, context: Optional[custom_model.ModelContext] = None) -> None:
      super().__init__(context)
      self.partition_id = None
      self.model = None

  @custom_model.inference_api
  def predict(self, input: pd.DataFrame) -> pd.DataFrame:
      # Load the submodel only when the partition changes, then reuse the cached model.
      partition_id = input["STORE_NUMBER"][0]
      if self.partition_id != partition_id:
          self.partition_id = partition_id
          self.model = ...    # Load the submodel for this partition (for example, deserialize the model bytes).

      output_df = self.model.predict(...)
      return output_df

my_model = ExampleStatefulPartitionedModel()
```

When logging the model, provide a `function_type` of `TABLE_FUNCTION` in the `options` dictionary along with any
other [options](/developer-guide/snowflake-ml/model-registry/overview#label-snowpark-model-registry-log-models-logging-options) your model requires.

Copy code

```
from snowflake.ml.registry import Registry

reg = Registry(session=sp_session, database_name="ML", schema_name="REGISTRY")
model_version = reg.log_model(my_model,
  model_name="my_model",
  version_name="v1",
  options={"function_type": "TABLE_FUNCTION"},    ###
  conda_dependencies=["scikit-learn"],
  sample_input_data=train_features
)
```

If your partitioned model also has regular (non-table) functions as methods, you can use the `method_options`
dictionary to specify the type of each method instead.

Copy code

```
model_version = reg.log_model(my_model,
    model_name="my_model",
    version_name="v1",
    options={
      "method_options": {                                 ###
        "METHOD1": {"function_type": "TABLE_FUNCTION"},   ###
        "METHOD2": {"function_type": "FUNCTION"}          ###
      }
    },
    conda_dependencies=["scikit-learn"],
    sample_input_data=train_features,
)
```

## Partitioned model inference

Use the `run` method of a Python `ModelVersion` object to invoke the table function methods in a partitioned
fashion, passing `partition_column` to specify the name of the column that contains a numeric or string value that
identifies the partition of each record. As usual, you may pass a Snowpark or pandas DataFrame (the latter is useful for
local testing). You will receive the same type of DataFrame as the result. In these examples, inference is partitioned
on a store number.

Copy code

```
model_version.run(
  input_df,
  function_name="PREDICT",
  partition_column="STORE_NUMBER"
)
```

You can also call the model table functions directly with SQL, as shown here.

Copy code

```
SELECT output1, output2, partition_column
  FROM input_table,
      TABLE(
          my_model!predict(input_table.input1, input_table.input2)
          OVER (PARTITION BY input_table.store_number)
      )
  ORDER BY input_table.store_number;
```

The input data is automatically split among the nodes and cores in your warehouse and the partitions are processed
in parallel.

For more information about table function syntax, see [Calling a UDF with SQL](/developer-guide/udf/udf-calling-sql#label-call-udf-calling-udf).

### Using parameters with partitioned models

Partitioned model methods decorated with `@partitioned_api` can accept optional inference parameters, the same way
as `@inference_api` methods. Define parameters as keyword-only arguments (after `*`), with type annotations and
default values:

Copy code

```
class PartitionedModelWithParams(custom_model.CustomModel):

  @custom_model.partitioned_api
  def predict(
      self,
      input_df: pd.DataFrame,
      *,
      n_estimators: int = 100,
      learning_rate: float = 0.1,
  ) -> pd.DataFrame:
      import xgboost
      training_data = ...

      my_model = xgboost.XGBRegressor(
          n_estimators=n_estimators,
          learning_rate=learning_rate,
      )
      my_model.fit(training_data)

      output_df = my_model.predict(...)
      return output_df
```

Pass parameters at inference time through `mv.run`:

Copy code

```
model_version.run(
    input_df,
    function_name="PREDICT",
    partition_column="STORE_NUMBER",
    params={"n_estimators": 200, "learning_rate": 0.05}
)
```

Or in SQL using positional or named arguments:

Copy code

```
-- Positional: input columns, then parameters
SELECT output1, output2, partition_column
  FROM input_table,
      TABLE(
          my_model!predict(input_table.input1, input_table.input2, 200, 0.05)
          OVER (PARTITION BY input_table.store_number)
      )
  ORDER BY input_table.store_number;

-- Named arguments (all arguments must be named)
SELECT output1, output2, partition_column
  FROM input_table,
      TABLE(
          my_model!predict(
              input1 => input_table.input1,
              input2 => input_table.input2,
              n_estimators => 200
          )
          OVER (PARTITION BY input_table.store_number)
      )
  ORDER BY input_table.store_number;
```

For more information about defining parameters, see
[Specifying model signatures](/developer-guide/snowflake-ml/model-registry/model-signature) and
[Defining inference parameters](/developer-guide/snowflake-ml/model-registry/bring-your-own-model-types#label-snowpark-model-registry-custom-model-context).

### Using batch inference jobs with partitioned models

Note

This feature requires `snowflake-ml-python` version 1.33.0 or later.

You can also use the `run_batch` method to run partitioned inference as a
[batch inference job](/developer-guide/snowflake-ml/inference/batch-inference-jobs) on
Snowpark Container Services (SPCS). This is useful for large-scale workloads that benefit from distributed
compute with configurable resources.

To partition the input data, pass the `partition_column` argument in `InputSpec`:

Copy code

```
from snowflake.ml.model.batch import InputSpec, OutputSpec

job = model_version.run_batch(
    input_df,
    compute_pool="my_compute_pool",
    input_spec=InputSpec(partition_column="STORE_NUMBER"),
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/results/"),
)
```

For full details on batch inference jobs, see
[Batch inference jobs](/developer-guide/snowflake-ml/inference/batch-inference-jobs).

## Stateless partitioned models

In the simplest application of partitioned models, training and inference are both done when `predict` is
called. The model is fitted, inference is run, and the fitted model is discarded immediately afterward. This type
of model is called “stateless” because no fit state is stored. Here is an example in which each partition trains
an XGBoost model:

Copy code

```
class ExampleStatelessPartitionedModel(custom_model.CustomModel):

  @custom_model.partitioned_api
  def predict(self, input_df: pd.DataFrame) -> pd.DataFrame:
      import xgboost
      # All data in the partition will be loaded in the input dataframe.
      # Construct training data by transforming input_df.
      training_data = ...

      # Train the model.
      my_model = xgboost.XGBRegressor()
      my_model.fit(training_data)

      # Generate predictions.
      output_df = my_model.predict(...)

      return output_df

my_model = ExampleStatelessPartitionedModel()
```

See the [Partitioned Model Quickstart Guide](https://quickstarts.snowflake.com/guide/partitioned-ml-model/)
for an example of a stateless partitioned model, including sample data.

## Stateful partitioned models

It’s also possible to implement stateful partitioned models that load stored submodel fit state. You do this by providing
models in memory via the `snowflake.ml.model.custom_model.ModelContext` or by providing file paths pointing to fitted
model artifacts and loading them during inference.

The following example shows how to provide models in memory to the model context.

Copy code

```
from snowflake.ml.model import custom_model

# `models` is a dict with model ids as keys, and fitted xgboost models as values.
models = {
  "model1": models[0],
  "model2": models[1],
  ...
}

model_context = custom_model.ModelContext(
  models=models
)
my_stateful_model = MyStatefulCustomModel(model_context=model_context)
```

When logging `my_stateful_model`, the submodels provided in the context are stored along with all model files.
They can then be accessed in the inference method logic by retrieving them from context, as shown below:

Copy code

```
class ExampleStatefulModel(custom_model.CustomModel):

  @custom_model.inference_api
  def predict(self, input: pd.DataFrame) -> pd.DataFrame:
    model1 = self.context.model_ref("model1")
    # ... use model1 for inference
```

It’s also possible to access the models programmatically by partition ID in the `predict` method. If a partition column is
provided as an input feature, it can be used to access a model fitted for the partition. For example, if the partition column
is `MY_PARTITION_COLUMN`, the following model class can be defined:

Copy code

```
class ExampleStatefulModel(custom_model.CustomModel):

  @custom_model.inference_api
  def predict(self, input: pd.DataFrame) -> pd.DataFrame:
    model_id = input["MY_PARTITION_COLUMN"][0]
    model = self.context.model_ref(model_id)
    # ... use model for inference
```

Similarly, submodels can be stored as artifacts and loaded at runtime. This approach is useful when the models are too
large to fit into memory. Provide string file paths to the model context. The filepaths are accessible during inference
with *self.context.path(artifact\_id)*. For more information, see [Defining model context by keyword arguments](/developer-guide/snowflake-ml/model-registry/bring-your-own-model-types#label-snowpark-model-registry-custom-model-context).

When submodels are provided in memory through the model context, they’re already loaded, so `model_ref` retrieves one
without any loading cost and there’s no need to cache. Caching (as shown in
[Defining and logging the model](#defining-and-logging-the-model)) helps when a submodel must instead be deserialized
from bytes, so it isn’t reloaded on every call.

## Example

See the [Partitioned Model Quickstart Guide](https://quickstarts.snowflake.com/guide/partitioned-ml-model/)
for an example, including sample data.

See the [Many Model Inference in Snowflake Quickstart Guide](https://quickstarts.snowflake.com/guide/many-model-inference-in-snowflake/)
for an example of a stateful partitioned custom model.
