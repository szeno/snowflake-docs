# MLFlow

You can use MLflow models that support PyFunc. If your MLFlow model has a signature, the `signature`
argument is inferred from the model. Otherwise, you must provide either `signature` or `sample_input_data`.

The following additional options can be used in the `options` dictionary when you call `log_model`:

| Option | Description |
| --- | --- |
| `model_uri` | The URI of the artifacts of the MLFlow model. Must be provided if it is not available in the model’s metadata as `model.metadata.get_model_info().model_uri`. |
| `ignore_mlflow_metadata` | If `True`, the model’s metadata is not imported to the model object in the registry. Default: `False` |
| `ignore_mlflow_dependencies` | If `True`, the dependencies in the model’s metadata are ignored, which is useful due to package available limitations in Snowflake warehouses. Default: `False` |

Expand

Show lessSee more

## Example

Copy code

```
import mlflow
from sklearn import datasets, model_selection, ensemble

db = datasets.load_diabetes(as_frame=True)
X_train, X_test, y_train, y_test = model_selection.train_test_split(db.data, db.target)
with mlflow.start_run() as run:
    rf = ensemble.RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
    rf.fit(X_train, y_train)

    # Use the model to make predictions on the test dataset.
    predictions = rf.predict(X_test)
    signature = mlflow.models.signature.infer_signature(X_test, predictions)
    mlflow.sklearn.log_model(
        rf,
        "model",
        signature=signature,
    )
    run_id = run.info.run_id

model_ref = registry.log_model(
    mlflow.pyfunc.load_model(f"runs:/{run_id}/model"),
    model_name="mlflowModel",
    version_name="v1",
    conda_dependencies=["mlflow<=2.4.0", "scikit-learn", "scipy"],
    options={"ignore_mlflow_dependencies": True}
)
model_ref.run(X_test)
```
