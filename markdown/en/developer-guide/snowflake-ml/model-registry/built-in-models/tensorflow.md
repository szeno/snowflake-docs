# TensorFlow

The Snowflake ML Model Registry supports models created using TensorFlow (models derived from `tensorflow.Module`)
and Keras v2 models (`keras.Model` with Keras version < 3.0.0).

Note

For Keras 3.0.0 or later, use the [Keras](/developer-guide/snowflake-ml/model-registry/built-in-models/keras) handler.

The following additional options can be used in the `options` dictionary when you call `log_model`:

| Option | Description |
| --- | --- |
| `target_methods` | A list of the names of the methods available on the model object. TensorFlow models have `__call__` as the default target method. Keras v2 models have `predict` as the default target method. |
| `cuda_version` | The version of the CUDA runtime to be used when deploying to a platform with GPU; defaults to 11.8. If manually set to `None`, the model cannot be deployed to a platform having a GPU. |
| `multiple_inputs` | Whether the model expects multiple tensor inputs. Defaults to `False`. When `True`, the model will accept a list of tensors as input instead of a single tensor. |

Expand

Show lessSee more

You must specify either the `sample_input_data` or `signatures` parameter when logging a TensorFlow model so
that the registry knows the signatures of the target methods.

Note

Keras v2 models can only have one target method.

Note

When using pandas DataFrames (which use float64 by default), ensure your TensorFlow model uses `tf.float64`
for variables and `tf.TensorSpec` input signatures to avoid dtype mismatch errors.

## Examples

These examples assume `reg` is an instance of `snowflake.ml.registry.Registry`.

### TensorFlow Module

The following example demonstrates creating a TensorFlow model by subclassing `tf.Module`, logging it to the Snowflake ML Model Registry, and running inference.

Copy code

```
import tensorflow as tf
import pandas as pd

# Define a simple TensorFlow module
class LinearModel(tf.Module):
    def __init__(self, name=None):
        super().__init__(name=name)
        self.weight = tf.Variable(2.0, dtype=tf.float64, name="weight")
        self.bias = tf.Variable(1.0, dtype=tf.float64, name="bias")

    @tf.function(input_signature=[tf.TensorSpec(shape=(None, 1), dtype=tf.float64)])
    def __call__(self, x):
        return self.weight * x + self.bias

# Create model instance
model = LinearModel(name="linear_model")

# Create sample input data as DataFrame
sample_df = pd.DataFrame({"input": [1.0, 2.0, 3.0, 4.0, 5.0]})

# Log the model
model_ref = reg.log_model(
    model=model,
    model_name="my_tf_linear_model",
    version_name="v1",
    sample_input_data=sample_df,
)

# Make predictions (default target method is __call__)
test_df = pd.DataFrame({"input": [6.0, 7.0, 8.0]})
result_df = model_ref.run(test_df)
```

### Keras v2 Sequential Model

The following example demonstrates training a Keras v2 sequential model, logging it to the Snowflake ML Model Registry, and running inference.

Copy code

```
import tf_keras as keras
from sklearn import datasets, model_selection

# Load dataset
iris = datasets.load_iris(as_frame=True)
X = iris.data
y = iris.target

# Rename columns for valid Snowflake identifiers
X.columns = [col.replace(' ', '_').replace('(', '').replace(')', '') for col in X.columns]

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

# Build Keras v2 model
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(3, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train the model
model.fit(X_train, y_train, epochs=50, verbose=0)

# Log the model
model_ref = reg.log_model(
    model=model,
    model_name="my_iris_classifier",
    version_name="v1",
    sample_input_data=X_test,
)

# Make predictions
result_df = model_ref.run(X_test[-10:], function_name="predict")
```
