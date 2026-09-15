# PyTorch

The Snowflake ML Model Registry supports models created using PyTorch (models derived from `torch.nn.Module`).

The following additional options can be used in the `options` dictionary when you call `log_model`:

| Option | Description |
| --- | --- |
| `target_methods` | A list of the names of the methods available on the model object. PyTorch models have the following target method by default: `forward`. |
| `cuda_version` | The version of the CUDA runtime to be used when deploying to a platform with GPU; defaults to 11.8. If manually set to `None`, the model cannot be deployed to a platform having a GPU. |
| `multiple_inputs` | Whether the model expects multiple tensor inputs. Defaults to `False`. When `True`, the model will accept a list of tensors as input instead of a single tensor. |

Expand

Show lessSee more

You must specify either the `sample_input_data` or `signatures` parameter when logging a PyTorch model so
that the registry knows the signatures of the target methods.

Note

When using pandas DataFrames (which use float64 by default), ensure your PyTorch model layers are created
with `dtype=torch.float64` to avoid dtype mismatch errors.

## Example

This example assumes `reg` is an instance of `snowflake.ml.registry.Registry`.

Copy code

```
import torch
import torch.nn as nn
from sklearn import datasets, model_selection

# Define a simple neural network for classification
class IrisClassifier(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        super().__init__()
        # Use float64 to match pandas DataFrame default dtype
        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim, dtype=torch.float64),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim, dtype=torch.float64),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim, dtype=torch.float64),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

# Load dataset
iris = datasets.load_iris(as_frame=True)
X = iris.data
y = iris.target

# Rename columns for valid Snowflake identifiers
X.columns = [col.replace(' ', '_').replace('(', '').replace(')', '') for col in X.columns]

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

# Create model
model = IrisClassifier(input_dim=4, hidden_dim=32, output_dim=3)

# Train the model
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()

X_train_tensor = torch.tensor(X_train.values)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.long)

model.train()
for epoch in range(100):
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()

# Log the model
model_ref = reg.log_model(
    model=model,
    model_name="my_iris_classifier",
    version_name="v1",
    sample_input_data=X_test,
)

# Make predictions
result_df = model_ref.run(X_test[-10:])
```
