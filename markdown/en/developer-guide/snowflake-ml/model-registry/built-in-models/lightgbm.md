# LightGBM

The Snowflake ML Model Registry supports models created using LightGBM (models derived from the scikit-learn API wrapper, e.g. *lightgbm.LGBMClassifier* or the native API, e.g. *lightgbm.Booster*).

The following additional options can be used in the `options` dictionary when you call `log_model`:

| Option | Description |
| --- | --- |
| `target_methods` | A list of the names of the methods available on the model object. Models derived from the scikit-learn API (e.g. `LGBMClassifier`) have the following target methods by default, assuming the method exists: `predict`, `predict_proba`. Models derived from the native API (e.g. `Booster`) have the `predict` method by default. |
| `enable_explainability` | Whether to enable explainability for the model using SHAP. Defaults to `True`. When enabled, an `explain` method will be available on the logged model. |
| `cuda_version` | The version of the CUDA runtime to be used when deploying to a platform with GPU; defaults to 11.8. If manually set to `None`, the model cannot be deployed to a platform having a GPU. |

Expand

Show lessSee more

You must specify either the `sample_input_data` or `signatures` parameter when logging a LightGBM model so
that the registry knows the signatures of the target methods.

## Examples

These examples assume `reg` is an instance of `snowflake.ml.registry.Registry`.

### Scikit-Learn API (LGBMClassifier)

The following example demonstrates the key steps to train a LightGBM classifier using the scikit-learn API, log it to the Snowflake ML Model Registry, and use the registered model for inference and explainability. The workflow includes:

- Trains a LightGBM classifier on a sample dataset.
- Logs the model to the Snowflake ML Model Registry.
- Makes predictions and retrieves prediction probabilities.
- Gets SHAP values for the model’s predictions.

Copy code

```
import lightgbm as lgb
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

# Train LightGBM Classifier
classifier = lgb.LGBMClassifier(
    n_estimators=100,
    learning_rate=0.05,
    num_leaves=31
)
classifier.fit(cal_X_train, cal_y_train)

# Log the model
model_ref = reg.log_model(
    model=classifier,
    model_name="my_lightgbm_classifier",
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

### Native API (Booster)

The following example demonstrates the key steps to train a LightGBM model using the native Snowflake ML API, log it to the Snowflake ML Model Registry, and use the registered model for inference. The workflow does the following:

- Trains a LightGBM model on a sample dataset.
- Logs the model to the Snowflake ML Model Registry.
- Makes predictions.

Copy code

```
import lightgbm as lgb
import pandas as pd
from sklearn import datasets, model_selection

# Load dataset
cal_data = datasets.load_breast_cancer()
cal_X = pd.DataFrame(cal_data.data, columns=cal_data.feature_names)
cal_y = cal_data.target

# Normalize column names (replace spaces with underscores)
cal_X.columns = [col.replace(' ', '_') for col in cal_X.columns]

cal_X_train, cal_X_test, cal_y_train, cal_y_test = model_selection.train_test_split(
    cal_X, cal_y, test_size=0.2
)

# Prepare LightGBM Data Structure
lgb_train = lgb.Dataset(cal_X_train, cal_y_train)

# Define parameters and train the model
params = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'boosting_type': 'gbdt',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9,
}

num_round = 100
booster = lgb.train(
    params,
    lgb_train,
    num_round
)

# Log the model
model_ref = reg.log_model(
    model=booster,
    model_name="my_lightgbm_booster",
    version_name="v1",
    sample_input_data=cal_X_test,
)

# Make predictions
result_df = model_ref.run(cal_X_test[-10:], function_name="predict")
```
