# CatBoost

The Snowflake ML Model Registry supports models created using CatBoost (models derived from `catboost.CatBoost`, such as
`catboost.CatBoostClassifier`, `catboost.CatBoostRegressor`, and `catboost.CatBoostRanker`).

The following additional options can be used in the `options` dictionary when you call `log_model`:

| Option | Description |
| --- | --- |
| `target_methods` | A list of the names of the methods available on the model object. CatBoost models have the following target methods by default, assuming the method exists: `predict`, `predict_proba`. |
| `enable_explainability` | Whether to enable explainability for the model using SHAP. Defaults to `True`. When enabled, an `explain` method will be available on the logged model. |
| `cuda_version` | The version of the CUDA runtime to be used when deploying to a platform with GPU; defaults to 11.8. If manually set to `None`, the model cannot be deployed to a platform having a GPU. |

Expand

Show lessSee more

You must specify either the `sample_input_data` or `signatures` parameter when logging a CatBoost model so
that the registry knows the signatures of the target methods.

## Examples

These examples assume `reg` is an instance of `snowflake.ml.registry.Registry`.

### CatBoostClassifier

The following example demonstrates the key steps to train a CatBoost classifier, log it to the Snowflake ML Model Registry, and use the registered model for inference and explainability. The workflow includes:

- Trains a CatBoost classifier on a sample dataset.
- Logs the model to the Snowflake ML Model Registry.
- Makes predictions and retrieves prediction probabilities.
- Gets SHAP values for the model’s predictions.

Copy code

```
import catboost
from sklearn import datasets, model_selection

# Load dataset
cal_data = datasets.load_breast_cancer(as_frame=True)
cal_X = cal_data.data
cal_y = cal_data.target

# Normalize column names (replace spaces with underscores)
cal_X.columns = [col.replace(' ', '_') for col in cal_X.columns]

cal_X_train, cal_X_test, cal_y_train, cal_y_test = model_selection.train_test_split(
    cal_X, cal_y, test_size=0.2
)

# Train CatBoost Classifier
classifier = catboost.CatBoostClassifier(
    iterations=100,
    learning_rate=0.1,
    depth=6,
    verbose=False
)
classifier.fit(cal_X_train, cal_y_train)

# Log the model
model_ref = reg.log_model(
    model=classifier,
    model_name="my_catboost_classifier",
    version_name="v1",
    sample_input_data=cal_X_test,
)

# Make predictions
result_df = model_ref.run(cal_X_test[-10:], function_name="predict")

# Get prediction probabilities
proba_df = model_ref.run(cal_X_test[-10:], function_name="predict_proba")

# Get explanations (SHAP values)
explanations_df = model_ref.run(cal_X_test[-10:], function_name="explain")
```

### CatBoostRegressor

The following example demonstrates the key steps to train a CatBoost regressor, log it to the Snowflake ML Model Registry, and use the registered model for inference. The workflow includes:

- Trains a CatBoost regressor on a sample dataset.
- Logs the model to the Snowflake ML Model Registry.
- Makes predictions.

Copy code

```
import catboost
from sklearn import datasets, model_selection

# Load dataset
cal_data = datasets.load_diabetes(as_frame=True)
cal_X = cal_data.data
cal_y = cal_data.target

cal_X_train, cal_X_test, cal_y_train, cal_y_test = model_selection.train_test_split(
    cal_X, cal_y, test_size=0.2
)

# Train CatBoost Regressor
regressor = catboost.CatBoostRegressor(
    iterations=100,
    learning_rate=0.1,
    depth=6,
    verbose=False
)
regressor.fit(cal_X_train, cal_y_train)

# Log the model
model_ref = reg.log_model(
    model=regressor,
    model_name="my_catboost_regressor",
    version_name="v1",
    sample_input_data=cal_X_test,
)

# Make predictions
result_df = model_ref.run(cal_X_test[-10:], function_name="predict")
```

### Disabling Explainability

If you do not need explainability features, you can disable them during logging to reduce model size and dependencies:

Copy code

```
model_ref = reg.log_model(
    model=classifier,
    model_name="my_catboost_classifier_no_explain",
    version_name="v1",
    sample_input_data=cal_X_test,
    options={"enable_explainability": False},
)
```
