# TabICL

The Snowflake Model Registry supports [TabICL](https://github.com/soda-inria/tabicl) tabular foundation models
(`tabicl.TabICLClassifier` and `tabicl.TabICLRegressor`) as of `snowflake-ml-python` 2.8.0. TabICL is an
in-context-learning (ICL) model for tabular classification and regression: `fit` prepares ICL state from labeled
rows rather than learning a separate set of task weights.

You log a TabICL estimator with `Registry.log_model`. The registry does not treat TabICL as a generic
[scikit-learn](/developer-guide/snowflake-ml/model-registry/built-in-models/scikit-learn) model, even though the
estimators subclass `sklearn.base.BaseEstimator`. At log time the registry bundles the TabICL foundation checkpoint
into the model artifact so serving can run offline.

## Bound and unbound serving

The registry chooses the serving mode from the estimator’s fitted state. There is no explicit toggle.

| Mode | When it applies | What is packaged | `predict` |
| --- | --- | --- | --- |
| Unbound (in-context learning) | You log an unfitted estimator. | Foundation checkpoint and constructor parameters only. Labeled context rows are supplied at inference time. | A partitioned table function. Each partition contains labeled context rows and unlabeled query rows. The output contains only the scored query rows. |
| Bound | You log a fitted estimator. | Foundation checkpoint, constructor parameters, and the training frame. The estimator is re-fit on that frame when the model loads. | A scalar function over named feature columns. One prediction per input row. |

Expand

Show lessSee more

Use unbound serving when you want to log the foundation once and score many different labeled contexts without
re-logging. Use bound serving when you have a single fitted task and want sklearn-style row-wise inference.

TabICL’s checkpoint is small enough to run in a Snowflake warehouse. You can also run inference in Snowpark
Container Services. Unbound `predict` is a partitioned table function, so it has no scalar service endpoint. Use
[`ModelVersion.run`](/developer-guide/snowflake-ml/model-registry/overview) in a warehouse or
[`ModelVersion.run_batch`](/developer-guide/snowflake-ml/inference/batch-inference-jobs) on a compute pool. Bound
`predict` is a regular function, so warehouse `run` and SPCS serving both apply.

## Logging options

The following additional options can be used in the `options` dictionary when you call `log_model`:

| Option | Description |
| --- | --- |
| `target_methods` | A list of the names of the methods available on the model object. The default target method is `predict`. |
| `target_column` | Name of the scalar label column. Defaults to `TARGET`. In unbound serving, a non-null value marks a context row. In bound serving, this column is split off of `sample_input_data` as the training labels. |
| `prediction_type` | Python type used to override the scored output column (for example `str` for class labels or `float` for regression). Ignored when you pass a full `signatures` argument. If you omit both `prediction_type` and `sample_input_data` in unbound serving, classifiers default `TARGET` and `PREDICTION` to string and regressors default them to double. |
| `cuda_version` | CUDA runtime version to use when deploying to a platform with a GPU. Defaults to the registry default. Set to `None` if the model must not be deployed to a GPU platform. |

Expand

Show lessSee more

Explainability is not supported for TabICL models. Setting `enable_explainability` to `True` raises an error.

The `tabicl` package is available from PyPI only, so set `artifact_repository_map` when you log the model, as shown in
the Log an unfitted classifier example below. If you omit this argument, `log_model` may add the built-in PyPI repository automatically for warehouse targets. That
automatic step doesn’t apply when you pass conda dependencies, and if the repository isn’t accessible, the registry
falls back to conda packaging, which can’t install `tabicl`. For a private PyPI-compatible repository, see
[Use a private PyPI artifact repository](/developer-guide/snowflake-ml/model-registry/overview#label-snowpark-model-registry-private-pypi).

## Unbound serving

An unfitted `TabICLClassifier` or `TabICLRegressor` is served unbound. The logged `predict` signature is generic
across feature names and widths:

- `FEATURES`: an OBJECT map from feature name to value per row. Values can mix numeric, string, and boolean types.
  Rows in a partition must share the same feature keys and types.
- `TARGET` (or the name you pass in `target_column`): a nullable scalar label. A non-null value marks an in-context
  example. A null value marks a row to score.
- Output: `OUTPUT_FEATURES` (the query row’s features, echoed under a distinct name so warehouse table-function
  invocation doesn’t collide with the input `FEATURES` column) and `PREDICTION`.

`predict` also accepts these inference parameters (passed as `params` to `run` or `run_batch`):

| Parameter | Description |
| --- | --- |
| `target_column` | Label column used to split context from query rows. Defaults to the value recorded at log time. |
| `context_filter` | Optional filter that selects context rows instead of using a non-null target. Use comparisons and boolean logic over top-level input columns, such as the target column. Other expressions are rejected. |
| `prediction_filter` | Optional filter that selects query rows instead of using a null target. Same restrictions as `context_filter`. |

Expand

Show lessSee more

You don’t need `sample_input_data` for unbound logging. If you pass a sample, it must be a pandas DataFrame with
`FEATURES` and the target column. The registry uses it to smoke-test fit/predict and to refine the scalar types. The
sample must include at least two labeled rows and at least one row with a null target, because the smoke test fits on
the labeled rows and predicts on the null-target rows.

The following examples assume `reg` is an instance of `snowflake.ml.registry.Registry` and `session` is an active
Snowpark session. For information on creating a registry object, see
[Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview).

### Log an unfitted classifier

Copy code

```
from tabicl import TabICLClassifier

mv = reg.log_model(
    TabICLClassifier(n_estimators=2, device="cpu", random_state=42),
    model_name="tabicl_unbound",
    version_name="v1",
    artifact_repository_map={"pip": "snowflake.snowpark.pypi_shared_repository"},
)
```

At log time, if the estimator doesn’t already point at a local `.ckpt` file via `model_path`, the registry
downloads the foundation checkpoint from the Hugging Face hub (`jingang/TabICL`) and copies it into the artifact.
Serving rebinds that bundled checkpoint with `allow_auto_download=False`, so inference doesn’t contact the network.

If you log the model from a Snowflake Notebook, attach an external access integration that allows egress to Hugging
Face. For the host list and an example integration, see
[Hugging Face pipeline](/developer-guide/snowflake-ml/model-registry/built-in-models/hugging-face). You can skip that integration by
setting `model_path` to a checkpoint you already downloaded.

### Warehouse inference

Pack each row’s features into an OBJECT, put labeled context rows and unlabeled query rows in the same partition,
and call `run` with `partition_column`:

Copy code

```
import numpy as np
import pandas as pd
from sklearn import datasets
from snowflake.snowpark.types import (
    MapType,
    StringType,
    StructField,
    StructType,
    VariantType,
)

iris = datasets.load_iris(as_frame=True)
features = iris.data
labels = np.asarray(iris.target_names)[iris.target]

order = np.random.default_rng(0).permutation(len(features))
context_idx, query_idx = order[:80], order[80:100]

rows = []
for i in context_idx:
    rows.append([{str(k): float(v) for k, v in features.iloc[i].items()}, str(labels[i]), "iris"])
for i in query_idx:
    rows.append([{str(k): float(v) for k, v in features.iloc[i].items()}, None, "iris"])

input_df = session.create_dataframe(
    rows,
    schema=StructType(
        [
            StructField("FEATURES", MapType(StringType(), VariantType())),
            StructField("TARGET", StringType()),
            StructField("PARTITION_KEY", StringType()),
        ]
    ),
)

predictions = mv.run(
    input_df,
    function_name="predict",
    partition_column="PARTITION_KEY",
    params={"target_column": "TARGET"},
)
predictions.show()
```

Each partition is fit on its context rows (cached by a context fingerprint for repeated calls with the same
context) and scores only the query rows.

### Batch inference on Snowpark Container Services

The same logged model and the same input shape work with `run_batch`. Pass the partition column and
`target_column` in `InputSpec`:

Copy code

```
from snowflake.ml.model.batch_inference import InputSpec, OutputSpec, ResourcesSpec, SaveMode

job = mv.run_batch(
    input_df,
    compute_pool="my_compute_pool",
    function_name="predict",
    input_spec=InputSpec(
        partition_column="PARTITION_KEY",
        params={"target_column": "TARGET"},
    ),
    output_spec=OutputSpec(
        stage_location="@my_db.my_schema.my_stage/tabicl_iris/",
        mode=SaveMode.OVERWRITE,
    ),
    resources_spec=ResourcesSpec(gpu_requests="1"),
)

job.wait()
```

For job configuration and how to read results from the output stage, see
[Batch inference jobs](/developer-guide/snowflake-ml/inference/batch-inference-jobs).

## Bound serving

Fit the estimator before logging it, and pass the training frame (named feature columns plus the target column) as
`sample_input_data`. The registry infers a static signature over those feature columns and stores the frame so the
estimator can be re-fit when the model loads.

Copy code

```
from sklearn import datasets, model_selection
from tabicl import TabICLClassifier
import pandas as pd

feature_columns = ["SEPAL_LENGTH", "SEPAL_WIDTH", "PETAL_LENGTH", "PETAL_WIDTH"]
data = datasets.load_iris()
features = pd.DataFrame(data.data, columns=feature_columns)
labels = pd.Series(data.target, name="TARGET")
x_train, x_test, y_train, _ = model_selection.train_test_split(
    features, labels, train_size=80, test_size=15, random_state=42, stratify=labels
)

model = TabICLClassifier(n_estimators=2, device="cpu", random_state=42)
model.fit(x_train, y_train.to_numpy())

training_frame = x_train.copy()
training_frame["TARGET"] = y_train.to_numpy()

mv = reg.log_model(
    model,
    model_name="tabicl_bound",
    version_name="v1",
    sample_input_data=training_frame,
    artifact_repository_map={"pip": "snowflake.snowpark.pypi_shared_repository"},
)

predictions = mv.run(x_test, function_name="predict")
```

The output is a DataFrame with a `PREDICTION` column, one row per input row.

## Limitations and considerations

- TabICL models don’t support explainability.
- A `snowflake.ml.model.custom_model.CustomModel` that holds a TabICL estimator is handled by the custom model handler,
  so the bound and unbound behavior on this page doesn’t apply. Log the estimator directly.
- Unbound input rows in a partition must share the same feature keys and types. Query rows missing a context feature
  receive a null for that key rather than failing.
- Unbound `predict` returns only query rows (M:N), not the original context rows.
- Logging downloads the foundation checkpoint unless `model_path` already points at a local `.ckpt` file.

## Related topics

- [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview)
- [Using built-in model types](/developer-guide/snowflake-ml/model-registry/built-in-models/overview)
- [Using partitioned models](/developer-guide/snowflake-ml/model-registry/partitioned-models)
- [Batch inference jobs](/developer-guide/snowflake-ml/inference/batch-inference-jobs)
- [scikit-learn](/developer-guide/snowflake-ml/model-registry/built-in-models/scikit-learn)
