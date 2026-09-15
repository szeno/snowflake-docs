# Snowflake ML release notes

This article contains the release notes for the Snowflake ML, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Note

These notes do not include changes in features that have not been publicly announced.
Such features may appear in the Snowflake ML source code but not in the public documentation.

See [Snowflake ML: End-to-End Agentic Machine Learning](/developer-guide/snowflake-ml/overview) for documentation.

## Verifying the snowflake-ml-python package

All Snowflake packages are signed, allowing you to verify their origin. To verify the `snowflake.ml.python` package, follow the steps below:

1. Install `cosign`. This example uses the Go installation:
   [Installing cosign with Go](https://edu.chainguard.dev/open-source/sigstore/cosign/how-to-install-cosign/#installing-cosign-with-go).
2. Download the file from a repository such as [PyPi](https://pypi.org/project/snowflake-ml-python/#files).
3. Download a `.sig` file for that release from the GitHub [releases page](https://github.com/snowflakedb/snowflake-ml-python/releases/).
4. Verify the signature using `cosign`. For example:

Copy code

```
cosign verify-blob snowflake_ml_python-1.7.0.tar.gz --key snowflake-ml-python-1.7.0.pub --signature resources.linux.snowflake_ml_python-1.7.0.tar.gz.sig

cosign verify-blob snowflake_ml_python-1.7.0.tar.gz --key snowflake-ml-python-1.7.0.pub --signature resources.linux.snowflake_ml_python-1.7.0
```

Note

This example uses the library and signature for version 1.7.0 of the package. Use the filenames of the version you are verifying.

## Version 1.7.2 (2024-11-21)

### New features

New model registry features:

- Model registry now supports asynchronous model inference service creation with the `block` option in the `Modelversion.create_service` method.
  Set this option to `False` to create the service asynchronously. The default is `True`.

### Bug fixes

Model explainability bug fixes:

- Fixed issue where `explain` is enabled for scikit-learn pipelines whose task is UNKNOWN, only to later fail when invoked.

## Version 1.7.1 (2024-11-05)

### New features

New model registry features:

- Null values are now ignored in the dataframe used for model signature inference. Only non-null values are used to infer signatures.
- Null values are now allowed in dataframes used for prediction.
- pandas extension data types are now supported in model signature inference.
- pandas `Series` can be used in input and output data.

New model monitoring features:

- The option `enable_monitoring` is now available when logging a model in the registry. This option gates access to private preview features of model monitoring.

### Bug fixes

Data bug fixes:

- Missing `snowflake.ml.data` exports in wheel have been added.

Dataset bug fixes:

- Missing `snowflake.ml.dataset` exports in wheel have been added.

Model registry bug fixes:

- Fixed issue where `tf_keras.Model` was not recognized as a keras model when logging.

## Version 1.7.0 (2024-10-22)

### Behavior changes

General behavior changes:

- Python 3.9 is now the minimum required version.

Data connector behavior changes:

- `to_torch_dataset` and `to_torch_datapipe` now create a dimension of 1 for scalar data.
  This allows more seamless integration with the PyTorch DataLoader, which creates batches by stacking inputs.
  The following example illustrates the difference.

  Copy code

  ```
  ds = connector.to_torch_dataset(shuffle=False, batch_size=3)
  ```

  - Input data: `"col1": [10, 11, 12]`

    - Previous result: `array([10., 11., 12.])` with shape `(3,)`
    - New result: `array([[10.], [11.], [12.]])` with shape `(3, 1)`
  - Input data: `[[0, 100], [1, 110], [2, 200]]`

    - Previous result: `array([[ 0, 100], [ 1, 110], [ 2, 200]])` with shape `(3,2)`
    - New result: No change
- You can now specify a batch size of `None` in `to_torch_dataset` to squeeze dimensions of 1 for better
  interoperability with the PyTorch DataLoader. `None` is the new default batch size.

Model Development behavior changes:

- The `eps` (epsilon) argument is no longer used with the `log_loss` metric. The argument is still accepted for
  backward compatibility, but its value is ignored, and the epsilon is now computed by the underlying scikit-lean
  implementation.

Model Registry behavior changes:

- External access integrations are no longer required when creating an inference service in Snowflake 8.40 or later.

### New features

New Model Registry features:

- You can now pass keyword arguments when instantiating `ModelContext` to provide a variable number of
  context values. For example:

  Copy code

  ```
  mc = custom_model.ModelContext(
   config = 'local_model_dir/config.json',
   m1 = model1
  )

  class ExamplePipelineModel(custom_model.CustomModel):
   def __init__(self, context: custom_model.ModelContext) -> None:
       super().__init__(context)
       v = open(self.context['config']).read()
       self.bias = json.loads(v)['bias']
   @custom_model.inference_api
   def predict(self, input: pd.DataFrame) -> pd.DataFrame:
       model_output = self.context['m1'].predict(input)
       return pd.DataFrame({'output': model_output + self.bias})
  ```
- Support for pandas’s `CategoricalDtype` for categorical columns.
- `log_model` method now accepts both `signature` and `sample_input_data` parameters
  to capture background data from explainability and data lineage.

### Bug fixes

Data Connector bug fixes:

- For multi-dimensional data, `to_torch_dataset` and `to_torch_datapipe` now return a numpy array with an appropriate
  data type instead of a list.

Feature Store bug fixes:

- Fixed an issue where `ExampleHelper` used an incomplete table name.
- Changed weather features aggregation time to one hour instead of one day.

Model Explainability bug fixes:

- Fixed an issue with explainability for XGBoost models by using a new SHAP library version.

## Version 1.6.4 (2024-10-17)

### Bug fixes

Model Registry bug fixes:

- Fix issue with using `ModelVersion.run` with Model Serving (inference on SPCS).

## Version 1.6.3 (2024-10-07)

### Behavior changes

Model Registry behavior changes:

- This release no longer contains the preview Model Registry API. Use the public API in `snowflake.ml.model_registry` instead.

### Bug fixes

Model Registry bug fixes:

- Fix unexpected package name normalizations for packages that do not follow [PEP-508](https://peps.python.org/pep-0508/)
  conventions when logging a model.
- Fix “Not a valid remote URI” error when logging MLflow models.
- Fix nested calls to `ModelVersion.run`.
- Fix `log_model` failure when a local package version number contains parts other than the base version.

### New features

New Model Registry features:

- You can now set a task type for the model in `log_model` via the `task` parameter.

New Feature Store features:

- `FeatureView` now supports `ON_CREATE` and `ON_SCHEDULE` initialization modes.

## Version 1.6.2 (2024-09-04)

### Bug fixes

- Fix a bug involving invalid names passed where fully-qualified names were required. These now correctly raise
  an exception.

Modeling bug fixes:

- Correctly log models built using XGBoost version 2 and higher.

Model explainability bug fixes:

- Workarounds and better error handling for XGBoost version 2.1.0 and higher.
- Correctly handle multiclass XGBoost classification models

### New features

New Feature Store features:

- The `update_feature_view` method now accepts a `FeatureView` object as an alternative to name and version.

## Version 1.6.1 (2024-08-13)

### Bug fixes

Feature Store bug fixes:

- Metadata size is no longer limited when generating a dataset.

Model Registry bug fixes:

- Fix an error message in the `run` method of model versions when a function name is not given and the model has
  multiple target methods.

### New features

New Modeling features:

- The `set_params` method is now available to set the parameters of the underlying scikit-learn estimator, if the
  Snowpark ML model has been fitted.

New Model Registry features:

- Support for model explainability in XGBoost, LightGBM, CatBoost, and scikit-learn models supported by the `shap` library.

## Version 1.6.0 (2024-07-29)

### Behavior changes

Feature Store behavior changes:

- Many positional arguments are now keyword arguments. The following table lists the affected arguments for each method.

  | Method | Arguments |
  | --- | --- |
  | `Entity` initializer | `desc` |
  | `FeatureView` initializer | `timestamp_col`, `refresh_freq`, `desc` |
  | `FeatureStore` initializer | `creation_mode` |
  | `FeatureStore.update_entity` | `desc` |
  | `FeatureStore.register_feature_view` | `block`, `overwrite` |
  | `FeatureStore.list_feature_views` | `entity_name`, `feature_view_name` |
  | `FeatureStore.get_refresh_history` | `verbose` |
  | `Feature:Store.retrieve_feature_values` | `spine_timestamp_col`, `exclude_columns`, `include_feature_view_timestamp_col` |
  | `FeatureStore.generate_training_set` | `save_as`, `spine_timestamp_col`, `spine_label_cols`, `exclude_columns`, `include_feature_view_timestamp_col` |
  | `FeatureStore.generate_dataset` | `version`, `spine_timestamp_col`, `spine_label_cols`, `exclude_columns`, `include_feature_view_timestamp_col`, `desc`, `output_type` |

  Expand

  Show lessSee more
- Add new column `warehouse` to the output of `list_feature_views`.

### Bug fixes

Modeling bug fixes:

- Fixed an issue in which `SimpleImputer` could not impute integer columns with integer values.

Model Registry bug fixes:

- Fixed an issue when providing a non-zero-index-based pandas Dataframe `ModelVersion.run`.

### New features

New Feature Store features:

- Added overloads to certain methods to accept both a `FeatureView` and name/version strings. Affected APIs include `read_feature_view`,
  `refresh_feature_view`, `get_refresh_history`, `resume_feature_view`, `suspend_feature_view`, and `delete_feature_view`.
- Added docstring inline examples for all public APIs.
- Added `ExampleHelper` utility class to help with loading source data to simplify public notebooks.
- Added `update_entity` method.
- Added `warehouse` argument to `FeatureView` constructor to override the default warehouse.

New Model Registry features:

- Added option to enable explainability when registering XGBoost, LightGBM, and Catboost models.
- Added support for logging a model from a `ModelVersion` object.

New modeling features:

- You can disable the 10GB training data size limit in distributed hyperparameter optimization by executing:

  Copy code

  ```
  from snowflake.ml.modeling._internal.snowpark_implementations import ( distributed_hpo_trainer, )
  distributed_hpo_trainer.ENABLE_EFFICIENT_MEMORY_USAGE = False
  ```

## Version 1.5.4 (2024-07-11)

### Bug fixes

Model Registry bug fixes:

- Fixed “401 Unauthorized” issue when deploying a model to Snowpark Container Services.

Feature Store bug fixes:

- Some exceptions in property setters have been downgraded to warnings, allowing you to change `desc`,
  `refresh_freq`, and `warehouse` in “draft” feature views.

Modeling bug fixes:

- Fixed issues with calling `OneHotEncoder` and `OrdinalEncoder` with a dictionary as the `categories` parameter and
  the data in a pandas DataFrame.

### New features

New Model Registry features:

- Allow overriding `device_map` and `device` when loading Hugging Face pipeline models.
- Add `set_alias` and `unset_alias` methods to `ModelVersion` instances to manage the model version’s aliases.
- Add `partitioned_inference_api` decorator to create partitioned inference methods in models.

New Feature Store features:

- New `refresh_freq`, `refresh_mode`, and `scheduling_state` columns have been added to the output of the
  `list_feature_views` method.
- The `update_feature_view` method now supports updating a feature view’s description.
- New methods `refresh_feature_view` and `get_refresh_history` manage updates of feature views.
- New method `generate_training_set` generates table-backed feature snapshots. `generate_dataset(..., output_type="table")` has been deprecated and generates a `DeprecationWarning`.

New Modeling features:

- `OneHotEncoder` and `OrdinalEncoder` now accept a list of array-like values for the `categories` argument.

## Version 1.5.3 (2024-06-17)

### Bug fixes

Model Registry bug fixes:

- Fix an issue causing incorrect results when using a pandas Dataframe with over 100,000 rows as the input of `ModelVersion.run` method in Stored Procedures.

Modeling bug fixes:

- Fix an issue with passing categories to `OneHotEncoder` and `OrdinalEncoder` as a dictionary or as a pandas DataFrame.

### New features

New Model Registry features:

- Model Registry now supports timestamp (TIMESTAMP\_NTZ) columns in input and output data.

New modeling features:

- `OneHotEncoder` and `OrdinalEncoder` now support a list of array-like values for the `categories` argument.

New Dataset features:

- `DatasetVersion` instances now have `label_cols` and `exclude_cols` properties.

## Version 1.5.2 (2024-06-10)

### Bug fixes

Model Registry bug fixes:

- Fixed an issue that prevented calls to `log_model` in a stored procedure.

Modeling bug fixes:

- Quick fix for `import snowflake.ml.modeling.parameters.enable_anonymous_sproc` not working due to package dependency error.

## Version 1.5.1 (2024-05-22)

### New features

New Model Registry features:

- `log_model`, `get_model`, and `delete_model` methods now support fully-qualified names.

New modeling features:

- You can now use an anonymous stored procedure during fitting, so that modeling does not require privileges to operate
  on the registry schema. Call `import snowflake.ml.modeling.parameters.enable_anonymous_sproc` to enable this feature.

### Bug fixes

Model registry bug fixes:

- Fix issue with loading older models.

## Version 1.5.0 (2024-05-01)

### Behavior changes

Model Registry behavior changes:

- The `fit_transform` method can now return either a Snowpark DataFrame or a pandas DataFrame, matching the kind of
  DataFrame passed to the method.

### New features

New Model Registry features:

- Added support for exporting models from the registry (`ModelVersion.export`).
- Added support for loading the underlying model object (`ModelVersion.load`).
- Added support for renaming models (`Model.rename`).

### Bug fixes

Model Registry bug fixes:

- Fixed the “invalid parameter `SHOW_MODEL_DETAILS_IN_SHOW_VERSIONS_IN_MODEL`” error.

## Version 1.4.1 (2024-04-18)

### New features

New Model Registry features:

- Added support for catboost models (`catboost.CatBoostClassifier`, `catboost.CatBoostRegressor`).
- Added support for lightgbm models (`lightgbm.Booster`, `lightgbm.LightGBMClassifier`, `lightgbm.LightGBMRegressor`).

### Bug fixes

Model Registry bug fixes:

- Fixed bug that caused `relax_version` option to not work.

## Version 1.4.0 (2024-04-08)

### Behavior changes

Model Registry behavior changes:

- The `apply` method is no longer included as a target method by default when logging an XGBoost model. If you need
  this method available in logged models, included it manually in the `target-methods` option:

  Copy code

  ```
  log_model(..., options={"target_methods": ["apply", ...]})
  ```

### New features

New model registry features:

- The registry now supports logging sentence transformer models (`sentence_transformers.SentenceTransformer`).
- The `version_name` argument is no longer required when logging a model. A random human-readable ID is generated if
  none is provided.

### Bug fixes

Model registry bug fixes:

- Fix issue where, when multiple models are called in the same query, models after the first returned incorrect results.
  This fix is applied when models are logged and does not benefit existing models; you must log your models again to
  correct this behavior.

Modeling bug fixes:

- Fix bug in registering a model where only methods mentioned in `save_model` were added to the model signature for
  Snowpark ML models.
- Fix bug in batch inference methods such as such as `predict` and `predict_log_probe` where, when `n_jobs` was
  not 1, the methods would not be executed.
- Fix bug in batch inference methods where they could not infer datatypes when the first row of data contained NULL.
- The output column names from distributed hyperparameter optimization are now correctly matched with the Snowflake identifier.
- Relaxed the versions of dependencies of distributed hyperparameter optimization methods; these were too strict and
  caused these methods to fail.
- scikit-learn is now listed as a dependency of the LightGBM package.

## Version 1.3.1 (2024-03-21)

### New features

FileSet/FileSystem updates:

- `snowflake.ml.fileset.sfcfs.SFFileSystem` can now be used in UDFs and stored procedures.

## Version 1.3.0 (2024-03-12)

### Behavior changes

Model registry behavior changes:

- As previously announced, the default for the `relax_version` option (in the `options` argument of `log_model`)
  is now `True`, allowing more reliable deployment in most cases by permitting dependency versions available in
  Snowflake.
- When running model methods, value range based input validation (which prevents input from overflowing) is now optional.
  This should improve performance and should not lead to issues for most types of models. To enable validation, pass the
  named argument `strict_input_validation=True` when calling the model’s `run` method.

Model development behavior changes:

- The `fit_predict` method now returns either a pandas or a Snowpark DataFrame, depending on the type of the input
  data, and is available on all classes where it is available in the underlying scikit-learn, xgboost, or lightgbm
  class.

### New features and updates

FileSet/FileSystem updates:

- Instances of `snowflake.ml.fileset.sfcfs.SFFileSystem` can now be serialized with `pickle`.

### Bug fixes

Model registry bug fixes:

- Fix a problem with importing `log_model` in some circumstances.
- Fix an incorrect error message when validating input Snowpark DataFrame with an array feature.

Model development bug fixes:

- Relax package versions for all inference methods when the installed version of a dependency is not available in the
  Snowflake conda channel.

## Version 1.2.3 (2024-02-26)

### New features and updates

Model development updates:

- All modeling classes now include a `score_samples` method to calculate the log-likelihood of the given samples.

Model registry updates:

- Decimal type features are automatically cast (with a warning) to a DOUBLE or FLOAT instead of producing an error.
- Improve error message for currently-unsupported `pip-requirements` option.
- You can now delete a version of a model.

### Bug fixes

Model development fixes:

- `precision_recall_fscore_support` returned incorrect results with `average="samples"`.

Model registry fixes:

- Descriptions, models, and tags were not retrieved correctly in newly-created registries under the private preview
  model registry API due to a recent Snowflake behavior change.

## Version 1.2.2 (2024-02-13)

### New features and updates

Model registry updates:

- You can now specify external access integrations when deploying a model to Snowpark Container Services using the
  private preview registry API, allowing models to access the internet to retrieve dependencies during deployment. The
  following endpoints are required for all deployments:

  - docker.com:80
  - docker.com:443
  - anaconda.com:80
  - anaconda.com:443
  - anaconda.org:80
  - anaconda.org:443
  - pypi.org:80
  - pypi.org:443

  For models derived from `HuggingFacePipeLineModel`, the following endpoints are required.

  - huggingface.com:80
  - huggingface.com:443
  - huggingface.co:80
  - huggingface.co:443

## Version 1.2.1 (2024-01-25)

### New features and updates

Model development updates:

- Infer column data type for transformers when possible.

Model registry updates:

- `relax_version` option (in `options` argument of `log_model`) relaxes dependencies of stated versions
  to allow newer minor versions when set to `True`.

## Version 1.2.0 (2024-01-12)

### New features and updates

Public preview release of model registry. See [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview).
The previous private preview release of the model registry has been deprecated, but will continue to be supported
while it includes features not yet available in the public preview version.

Model development updates:

- Added support for `fit_predict` method in AgglomerativeClustering, DBSCAN, and OPTICS classes.
- Added support for `fit_transform` method in MDS, SpectralEmbedding and TSNE class.
