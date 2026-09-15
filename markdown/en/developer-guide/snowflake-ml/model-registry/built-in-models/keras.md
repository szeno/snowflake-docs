# Keras

The Snowflake ML Model Registry supports Keras 3 models (`keras.Model` with Keras version >= 3.0.0).
Keras 3 is a multi-backend framework that supports TensorFlow, PyTorch, and JAX as backends.

Note

For Keras version < 3.0.0, use the [TensorFlow](/developer-guide/snowflake-ml/model-registry/built-in-models/tensorflow) handler.

The following additional options can be used in the `options` dictionary when you call `log_model`:

| Option | Description |
| --- | --- |
| `target_methods` | A list of the names of the methods available on the model object. Keras models have `predict` as the default target method. |
| `cuda_version` | The version of the CUDA runtime to be used when deploying to a platform with GPU; defaults to 11.8. If manually set to `None`, the model cannot be deployed to a platform having a GPU. |

Expand

Show lessSee more

You must specify either the `sample_input_data` or `signatures` parameter when logging a Keras model so
that the registry knows the signatures of the target methods.

Note

Keras models can only have one target method.

## Examples

These examples assume `reg` is an instance of `snowflake.ml.registry.Registry`.

### Sequential Model

The following example demonstrates training a Keras 3 sequential model, logging it to the Snowflake ML Model Registry, and running inference.

Copy code

```
import keras
from sklearn import datasets, model_selection

# Load dataset
iris = datasets.load_iris(as_frame=True)
X = iris.data
y = iris.target

# Rename columns for valid Snowflake identifiers
X.columns = [col.replace(' ', '_').replace('(', '').replace(')', '') for col in X.columns]

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

# Build Keras sequential model
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu'),
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
    model_name="my_keras_classifier",
    version_name="v1",
    sample_input_data=X_test,
)

# Make predictions
result_df = model_ref.run(X_test[-10:], function_name="predict")
```

### Functional API Model

The following example demonstrates creating a model using the Keras Functional API.

Copy code

```
import keras
import numpy as np
import pandas as pd

# Create sample data
n_samples, n_features = 100, 10
X = pd.DataFrame(
    np.random.rand(n_samples, n_features),
    columns=[f"feature_{i}" for i in range(n_features)]
)
y = np.random.randint(0, 2, n_samples).astype(np.float32)

# Build model using Functional API
inputs = keras.Input(shape=(n_features,))
x = keras.layers.Dense(32, activation='relu')(inputs)
x = keras.layers.Dense(16, activation='relu')(x)
outputs = keras.layers.Dense(1, activation='sigmoid')(x)
model = keras.Model(inputs=inputs, outputs=outputs)

model.compile(
    optimizer=keras.optimizers.SGD(learning_rate=0.01),
    loss=keras.losses.MeanSquaredError()
)

# Train the model
model.fit(X, y, epochs=10, verbose=0)

# Log the model
model_ref = reg.log_model(
    model=model,
    model_name="my_functional_model",
    version_name="v1",
    sample_input_data=X,
)

# Make predictions
result_df = model_ref.run(X[-10:], function_name="predict")
```

### Custom Subclass Model

The following example demonstrates creating a custom model by subclassing `keras.Model`.

Copy code

```
import keras
import numpy as np
import pandas as pd

# Define custom model with serialization support
@keras.saving.register_keras_serializable()
class BinaryClassifier(keras.Model):
    def __init__(self, hidden_units: int, output_units: int) -> None:
        super().__init__()
        self.dense1 = keras.layers.Dense(hidden_units, activation="relu")
        self.dense2 = keras.layers.Dense(output_units, activation="sigmoid")

    def call(self, inputs):
        x = self.dense1(inputs)
        return self.dense2(x)

    def get_config(self):
        base_config = super().get_config()
        config = {
            "dense1": keras.saving.serialize_keras_object(self.dense1),
            "dense2": keras.saving.serialize_keras_object(self.dense2),
        }
        return {**base_config, **config}

    @classmethod
    def from_config(cls, config):
        dense1_config = config.pop("dense1")
        dense1 = keras.saving.deserialize_keras_object(dense1_config)
        dense2_config = config.pop("dense2")
        dense2 = keras.saving.deserialize_keras_object(dense2_config)
        obj = cls(1, 1)
        obj.dense1 = dense1
        obj.dense2 = dense2
        return obj

# Create sample data
n_samples, n_features = 100, 10
X = pd.DataFrame(
    np.random.rand(n_samples, n_features),
    columns=[f"feature_{i}" for i in range(n_features)]
)
y = np.random.randint(0, 2, n_samples).astype(np.float32)

# Create and train model
model = BinaryClassifier(hidden_units=32, output_units=1)
model.compile(
    optimizer=keras.optimizers.SGD(learning_rate=0.01),
    loss=keras.losses.MeanSquaredError()
)
model.fit(X, y, epochs=10, verbose=0)

# Log the model
model_ref = reg.log_model(
    model=model,
    model_name="my_custom_classifier",
    version_name="v1",
    sample_input_data=X,
)

# Make predictions
result_df = model_ref.run(X[-10:], function_name="predict")
```
