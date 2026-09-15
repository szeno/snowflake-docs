# Snowpark ML

The registry supports models created using [Snowpark ML modeling APIs](/developer-guide/snowflake-ml/modeling) (models derived from
`snowpark.ml.modeling.framework.base.BaseEstimator`).

The following additional options can be used in the `options` dictionary when you call `log_model`:

| Option | Description |
| --- | --- |
| `target_methods` | A list of the names of the methods available on the model object. Snowpark ML models have the following target methods by default, assuming the method exists: `predict`, `transform`, `predict_proba`, `predict_log_proba`, `decision_function`. |

Expand

Show lessSee more

You do not need to specify `sample_input_data` or `signatures` when logging a Snowpark ML model;
these are automatically inferred during fitting.

Note

Snowpark ML pipelines require an estimator. You can’t register a transformer-only Snowpark ML pipeline. Use a scikit-learn pipeline to register your transformers.

## Example

Copy code

```
import pandas as pd
import numpy as np
from sklearn import datasets
from snowflake.ml.modeling.xgboost import XGBClassifier

iris = datasets.load_iris()
df = pd.DataFrame(data=np.c_[iris["data"], iris["target"]], columns=iris["feature_names"] + ["target"])
df.columns = [s.replace(" (CM)", "").replace(" ", "") for s in df.columns.str.upper()]

input_cols = ["SEPALLENGTH", "SEPALWIDTH", "PETALLENGTH", "PETALWIDTH"]
label_cols = "TARGET"
output_cols = "PREDICTED_TARGET"

clf_xgb = XGBClassifier(
        input_cols=input_cols, output_cols=output_cols, label_cols=label_cols, drop_input_cols=True
)
clf_xgb.fit(df)
model_ref = registry.log_model(
    clf_xgb,
    model_name="XGBClassifier",
    version_name="v1",
)
model_ref.run(df.drop(columns=label_cols).head(10), function_name='predict_proba')
```
