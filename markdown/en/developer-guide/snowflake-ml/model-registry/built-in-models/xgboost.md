# XGBoost

The Snowflake ML Model Registry supports models created using XGBoost (models derived from `xgboost.XGBModel` or `xgboost.Booster`).

The following additional options can be used in the `options` dictionary when you call `log_model`:

| Option | Description |
| --- | --- |
| `target_methods` | A list of the names of the methods available on the model object. Models derived from `XGBModel` have the following target methods by default, assuming the method exists: `predict`, `predict_proba`. (Before v1.4.0, `apply` was also included.) Models derived from `Booster` have the `predict` method by default. |
| `cuda_version` | The version of the CUDA runtime to be used when deploying to a platform with GPU; defaults to 11.8. If manually set to `None`, the model cannot be deployed to a platform having a GPU. |

Expand

Show lessSee more

You must specify either the `sample_input_data` or `signatures` parameter when logging an XGBoost model so
that the registry knows the signatures of the target methods.

## Example

Copy code

```
import xgboost
from sklearn import datasets, model_selection

cal_X, cal_y = datasets.load_breast_cancer(as_frame=True, return_X_y=True)
cal_X_train, cal_X_test, cal_y_train, cal_y_test = model_selection.train_test_split(cal_X, cal_y)
params = dict(n_estimators=100, reg_lambda=1, gamma=0, max_depth=3, objective="binary:logistic")
regressor = xgboost.train(params, xgboost.DMatrix(data=cal_X_train, label=cal_y_train))
model_ref = registry.log_model(
    regressor,
    model_name="xgBooster",
    version_name="v1",
    sample_input_data=cal_X_test,
    options={
        "target_methods": ["predict"],
        "method_options": {
            "predict": {"case_sensitive": True},
        },
    },
)
model_ref.run(cal_X_test[-10:])
```
