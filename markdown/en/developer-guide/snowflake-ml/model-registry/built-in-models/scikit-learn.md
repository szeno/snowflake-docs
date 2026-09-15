# scikit-learn

The registry supports models created using scikit-learn (models derived from `sklearn.base.BaseEstimator` or
`sklearn.pipeline.Pipeline`).

The following additional options can be used in the `options` dictionary
when you call `log_model`:

| Option | Description |
| --- | --- |
| `target_methods` | A list of the names of the methods available on the model object. scikit-learn models have the following target methods by default, assuming the method exists: `predict`, `transform`, `predict_proba`, `predict_log_proba`, `decision_function`. |

Expand

Show lessSee more

You must specify either the `sample_input_data` or `signatures` parameter when logging a scikit-learn model
so that the registry knows the signatures of the target methods.

## Example

In this example, a `RandomForestClassifier` and `Pipeline` are trained and logged to the model registry.

Copy code

```
from snowflake.ml.registry import Registry
from sklearn import datasets, ensemble

# create a session and set DATABASE and SCHEMA
# session = ...

registry = Registry(session=session, database_name=DATABASE, schema_name=SCHEMA)

iris_X, iris_y = datasets.load_iris(return_X_y=True, as_frame=True)

# Rename columns so they are valid Snowflake identifiers
column_name_map = {
        'sepal length (cm)': 'sepal_length',
        'sepal width (cm)': 'sepal_width',
        'petal length (cm)': 'petal_length',
        'petal width (cm)': 'petal_width'
}
iris_X = iris_X.rename(columns=column_name_map)

# Train the model
clf = ensemble.RandomForestClassifier(random_state=42)
clf.fit(iris_X, iris_y)

# Log the model in the registry
model_ref = registry.log_model(
    clf,
    model_name="RandomForestClassifier",
    version_name="v1",
    sample_input_data=iris_X,
    options={
        "method_options": {
            "predict": {"case_sensitive": True},
            "predict_proba": {"case_sensitive": True},
            "predict_log_proba": {"case_sensitive": True},
        }
    },
)

# Generate predictions
model_ref.run(iris_X[-10:], function_name='"predict_proba"')

# Pipelines can also be logged in the registry
from sklearn import pipeline, preprocessing

pipe = pipeline.Pipeline([
    ('scaler', preprocessing.StandardScaler()),
    ('classifier', ensemble.RandomForestClassifier(random_state=42)),
])
pipe.fit(iris_X, iris_y)

model_ref = registry.log_model(
    pipe,
    model_name="Pipeline",
    version_name="v1",
    sample_input_data=iris_X,
    options={
        "method_options": {
            "predict": {"case_sensitive": True},
            "predict_proba": {"case_sensitive": True},
            "predict_log_proba": {"case_sensitive": True},
        }
    },
)

# Generate predictions
model_ref.run(iris_X[-10:], function_name='"predict_proba"')
```

Note

You can combine scikit-learn preprocessing with an XGBoost model as a scikit-learn pipeline.
