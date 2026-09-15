# Snowflake ML release notes

This article contains the release notes for the Snowflake ML, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Note

These notes do not include changes in features that have not been publicly announced.
Such features might appear in the Snowflake ML source code but not in the public documentation.

See [Snowflake ML: End-to-End Agentic Machine Learning](/developer-guide/snowflake-ml/overview) for documentation.

## Verifying the `snowflake-ml-python` package

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

## Deprecation notices

- `snowflake.ml.fileset.FileSet` has been deprecated and will be removed in a future release. Use
  [snowflake.ml.dataset.Dataset](/developer-guide/snowflake-ml/dataset) and
  [snowflake.ml.data.DataConnector](/developer-guide/snowpark-ml/reference/latest/api/data/snowflake.ml.data.data_connector.DataConnector) instead.
- The “CamelCase” function names in `snowflake.ml.cortex` have been deprecated and will be removed in a future
  release. Use the “snake\_case” names for these functions instead. For example, use `classify_text` instead of
  `ClassifyText`.
- The `partitioned_inference_api` decorator has been deprecated and will be removed in a future release. Use `custom_model.partitioned_api` instead.
- The `additional_payloads` argument of the `MLJob.submit_*` methods has been deprecated and will be removed in a future release.
  Use the `imports` argument instead.

## Version 1.20.0 (2025-12-02)

### Bug fixes

Experiment Tracking bug fixes:

- Exceeding the run metadata size limit in `log_metrics` or `og_params` issues a warning rather than raising an exception.

### New features

New Model Registry features:

- vLLM is now supported as an inference back-end. The `create_service` API accepts a new argument, `inference_engine_options`,
  which allows you to specify the inference engine to use and other engine-specific options. To specify vLLM, set the `inference_engine` option to `InferenceEngine.VLLM`.
  The following code is an example of creating a service using the vLLM inference engine:

  Copy code

  ```
  from snowflake.ml.model.inference_engine import InferenceEngine

  mv = snowflake_registry.log_model(
   model=generator,
   model_name=...,
   ...,
   # Specifying OPENAI_CHAT_SIGNATURE is necessary to use vLLM inference engine
   signatures=openai_signatures.OPENAI_CHAT_SIGNATURE,
  )

  mv.create_service(
   service_name=my_serv,
   service_compute_pool=...,
   ...,
   inference_engine_options={
       "engine": InferenceEngine.VLLM,
       "engine_args_override": [
           "--max-model-len=2048",
           "--gpu-memory-utilization=0.9"
       ]
   }
  )
  ```

  - Prophet is now supported as a modeling framework.

## Version 1.19.0 (2025-11-13)

### Bug fixes

Model Registry bug fixes:

- `get_version_by_alias` now requires an exact match of the version’s Snowflake identifier.

### New preview features

- Experiment Tracking API (`snowflake.ml.ExperimentTracking` module)
- Online feature serving in Feature Store.

## Version 1.18.0 (2025-10-23)

### New features

New Model Registry features:

- The `create_service` API validates that a model has a GPU runtime configuration and throws a descriptive error if
  the configuration is missing

### Deprecations

Support for Python 3.9 has been deprecated. Python 3.10 or later is recommended.

## Version 1.17.0 (2025-10-20)

### New features

New modeling features:

- Support for `xgboost` 3.x

New ML Jobs features:

- `MLJobs.result` API is more broadly cross-version compatible and support pandas DataFrames,
  pyarrow Tables, and NumPy arrays.
- Job submission now uses v2 of the job submission API by default. v2 APIs use the latest container
  runtime imade by default. Set the MLRS\_USE\_SUBMIT\_JOB\_V2 to false to use v1 of the job submission API.
- Now supports retriieving details of deleted jobs, including status, compute pool, and target instances.

## Version 1.16.0 (2025-10-06)

### Bug fixes

Model Registry bug fixes:

- Remove redundant pip dependency warnings when `artifact_repository_map` is provided for warehouse model deployments.

### New features

New modeling features:

- Support for `scikit-learn` versions earlier than 1.8.

New ML Jobs features:

- Support for configuring the runtime image via the `runtime_environment` parameter at submission time. You may specify an image tag or a full image URL.

  Examples for `@remote` decorator and `submit_file` function:

  Copy code

  ```
  @remote(compute_pool, stage_name = 'payload_stage', runtime_environment = '1.8.0')

  submit_file('/path/to/repo/test.py', compute_pool, stage_name = 'payload_stage',
    runtime_environment = '/mydb/myschema/myrepo/myimage:latest')
  ```

New Model Registry features:

- Ability to mark model methods as volatile or immutable. Volatile methods may return different results when called multiple times with the same input,
  while immutable methods always return the same result for the same input. Methods in supported model types are immutable by default, while methods
  in custom models are volatile by default. Use the `Volatility` enum to specify the volatility of model methods when logging a model as follows:

  Copy code

  ```
  from snowflake.ml.model.volatility import Volatility

  options = {
   "embed_local_ml_library": True,
   "relax_version": True,
   "save_location": "/path/to/my/directory",
   "function_type": "TABLE_FUNCTION",
   "volatility": Volatility.IMMUTABLE,
   "method_options": {
       "predict": {
           "case_sensitive": False,
           "max_batch_size": 100,
           "function_type": "TABLE_FUNCTION",
           "volatility": Volatility.VOLATILE,
       },
  }
  ```

## Version 1.15.0 (2025-09-29)

### Behavior changes

Model Registry behavior changes:

- Drop support for deprecated `conversational` task type for Hugging Face models. This task type has been
  deprecated by Hugging Face for some time and is due for removal from their API imminently.

## Version 1.14.0 (2025-09-18)

### New features

New ML Jobs features:

- The `additional_payloads` argument of the `MLJob.submit_*` methods has been renamed `imports` to better reflect its purpose.
  `additional_payloads` has been deprecated and will be removed in a future release.

## Version 1.13.0 (2025-09-11)

### New features

New Model Registry features:

- You can now log a HuggingFace model without having to load the model in memory using `huggingface_pipeline.HuggingFacePipelineModel`.
  Requires the `huggingface_hub` package. To disable downloading from the HuggingFace repository, pass `download_snapshot=False` when
  instantiating `huggingface_pipeline.HuggingFacePipelineModel`.
- You can now use XGBoost’s `enable_categorical=True` models with pandas DataFrames
- When listing services, the PrivateLink inference endpoint is shown in the `ModelVersion` list.

## Version 1.12.0 (2025-09-04)

### Bug fixes

Model Registry bug fixes:

- Fixed an issue where the string representation of dictionary-type output columns was being incorrectly created during structured output deserialization,
  losing the original data type.
- Fixed an inference server performance issue for wide (500+ features) and JSON inputs.

### New features

New Model Registry features:

- You can now log text-generation models with signatures compatible with OpenAI chat completion compatible signature, as shown in the following example:

  Copy code

  ```
  from snowflake.ml.model import openai_signatures
  import pandas as pd

  mv = snowflake_registry.log_model(
   model=generator,
   model_name=...,
   ...,
   signatures=openai_signatures.OPENAI_CHAT_SIGNATURE,
  )

  # create a pd.DataFrame with openai.client.chat.completions arguments like below:
  x_df = pd.DataFrame.from_records(
   [
       {
           "messages": [
               {"role": "system", "content": "Complete the sentence."},
               {
                   "role": "user",
                   "content": "A descendant of the Lost City of Atlantis, who swam to Earth while saying, ",
               },
           ],
           "max_completion_tokens": 250,
           "temperature": 0.9,
           "stop": None,
           "n": 3,
           "stream": False,
           "top_p": 1.0,
           "frequency_penalty": 0.1,
           "presence_penalty": 0.2,
       }
   ],
  )
  ```

New Model Monitoring features:

- Model monitors now support segment columns to enable filtered analysis, specified in the `segment_columns` field in the model monitor source options.
  Segment columns must exist in the source table and be of string type. `add_segment_column` and `drop_segment_column` methods are provided
  to add or remove segment columns in existing model monitors.

## Version 1.11.0 (2025-08-12)

### New features

New Model Registry features:

- Made `image_repo` argument optional in `ModelVersion.create_service`. If not specified, a default image repository is used.

### Bug fixes

ML Jobs bug fixes:

- Fixed `TypeError: SnowflakeCursor.execute() got an unexpected keyword argument '_force_qmark_paramstyle'` inside stored procedure.
- Fixed `Error: Unable to retrieve head IP address` when not all instances start within the timeout period.

## Version 1.10.0 (2025-08-01)

### New features

New Model Registry features:

- Added progress bars for `ModelVersion.create_service` and `ModelVersion.log_model`.
- Logs from `ModelVersion.create_service` are now written to a file. The location of the log file is shown in the console.

## Version 1.9.2 (2025-07-28)

### Bug fixes

DataConnector bug fixes:

- Fixed a problem that caused errors mentioning `self._session`.

Model Registry bug fixes:

- Fixed a bug when passing None to array (`pd.dtype('O')`) in model signature and pandas data handler.

## Version 1.9.1 (2025-07-18)

### Bug fixes

Model Registry bug fixes:

- Fix a bug with setting the PAD token when the HuggingFace text-generation model had multiple EOS tokens. The handler now picks the first EOS token as PAD token.

### New features

New DataConnector features:

- DataConnector objects can now be pickled.

New Dataset features:

- Dataset objects can now be pickled.

New Model Registry features:

- Models hosted on Snowpark Container Services now support wide input (500+ features).

## Version 1.9.0 (2025-06-25)

### Behavior changes

ML Jobs behavior changes:

- Removed `scope` parameter from `list_jobs` method.
- Added optional `database` and `schema` parameters to `list_jobs` method.
- The `list_jobs` method now returns a pandas DataFrame rather than a Snowpark DataFrame.
- The `list_jobs` method now returns the following columns: `name`, `status`, `message`, `database_name`, `schema_name`,
  `owner`, `compute_pool`, `target_instances`, `created_time`, and `completed_time`.

Model registry behavior changes:

- Set `relax_version` to false when `pip_requirements` is specified in `log_model` call.
- `UserWarning` is raised only on specified `target_platforms` to address spurious warnings

### Bug fixes

Model registry bug fixes:

- Fixed failure in converting Snowpark DataFrame to pandas DataFrame when QUOTED\_IDENTIFIERS\_IGNORE\_CASE parameter is enabled
- Fixed duplicate `UserWarning` log entries during model packaging

### New features

New model registry features:

- New APIs for representing target platforms (`snowflake.ml.model.target_platform.TargetPlatform`), target platform
  constant,s and tasks (`snowflake.ml.model.task.Task`).
- The `target_platform` argument in the `log_model` method now accepts a `TargetPlatformMode` constant, which can be
  WAREHOUSE\_ONLY, SNOWPARK\_CONTAINER\_SERVICES\_ONLY, or BOTH\_WAREHOUSE\_AND\_SNOWPARK\_CONTAINER\_SERVICES.

New ML Jobs features:

- Less-frequently-used job submission arguments have been moved to `**kwargs`.
- Platform metrics are enabled by default.

With this release, single-node ML Job APIs are now stable and have been designated Generally Available.

## Version 1.8.6 (2025-06-18)

### New features

New model registry features:

- Added service container information to logs

## Version 1.8.5 (2025-05-27)

### Behavior changes

ML Jobs behavior changes:

- Argument `num_instances` has been renamed to `target_instances` in job submission APIs and is now required.

### Bug fixes

Model Registry bug fixes:

- Fixed a bug in listing and deleting container services.
- Fixed a bug with logging scikit-learn pipelines where the `explain` function was not created.
- Logging a container-only model no longer checks to make sure the required version of `snowflake-ml-python` is available in the Snowflake conda channel.

Explainability bug fixes:

- Minimum `streamlit` version has been decreased to 1.30 to improve compatibility.

Modeling bug fixes:

- `xgboost` is now a required dependency again (it was optional in v1.8.4).

### New features

ML Jobs new features:

- Job decorator now has `min_instances` argument that makes a job wait for the specified number of workers to be ready before starting.

## Version 1.8.4 (2025-05-12)

### Behavior changes

ML Jobs behavior changes:

- The `id` property is now the job’s fully-qualified name. A new property, `name`, has been introduced to represent the ML Job name.
- The `list_jobs` method now returns the ML Job name instead of the job ID.

Model Registry behavior changes:

- In `log_model`, enabling explainability when the model is deployed only to Snowpark Container Services is now an error instead of a warning and will prevent the log operation from completing.

### Bug fixes

Model Registry bug fixes:

- Fixed a bug in which logging PyTorch and TensorFlow models that caused `UnboundLocalError: local variable 'multiple_inputs' referenced before assignment.`

### New features

New Model Registry features:

- Automatically enable explainability for models that can be deployed to a warehouse.

New Explainability features:

- New visualization functions in `snowflake.ml.monitoring` plot explanations in notebooks.
- Support for categorical transforms in scikit-learn pipelines.

New Modeling features:

- Support categorical types for `xgboost.DMatrix` inputs in XGBoost models.

## Version 1.8.3 (2025-04-28)

### New features

New Model Registry features:

- Default to a CUDA container image, if available, when logging a GPU-capable model for deployment to Container Runtime for ML.
- Model versions have a `run_job` method that runs inference methods as a single-node Snowpark Container Services job. This method is available for all models, including those that are not deployed to Container Runtime for ML.
- The target platform defaults to a Snowflake warehouse when logging a partitioned model.

## Version 1.8.2 (2025-04-15)

### New features

The [ML Jobs](/developer-guide/snowflake-ml/ml-jobs/overview) API, which allows you to run code on
Container Runtime for ML from your local workstation, is available in preview. Accordingly, documentation for this API is available
in the Snowflake ML API Reference, and changes to the API appear in these release notes. New features in the ML Jobs API
might not appear here until they are publicly announced, but they do appear in the API reference.

New Model Registry features:

- You can specify the path to write the model versions files that are stored in the model’s Snowflake stage using the `save_location` option in the `log_model` method.
- When logging models in Container Runtime for ML, model dependencies are now included in `pip_requirements` by default.

## Version 1.8.1 (2025-03-20)

### Bug fixes

Model Registry bug fixes:

- Fix `unsupported model type` error when logging a scikit-learn model with a `score_samples` inference method.
- Fix failure of inference service creation on an existing suspended service.

### New features

New Model Registry features:

- Creating a copy of a model version with `log_model` with unsupported arguments now raises an exception.

## Version 1.8.0 (2025-03-20)

### Behavior changes

Model Registry behavior changes:

- Automatically-inferred signatures in `transformers.Pipeline` have been changed to use the `FeatureGroupSpec` task class, including:

  - Signature for fill-mask tasks:

    Before v1.8.0v1.8.0 and later

    Copy code

    ```
      ModelSignature(
    inputs=[
        FeatureSpec(name="inputs", dtype=DataType.STRING),
    ],
    outputs=[
        FeatureSpec(name="outputs", dtype=DataType.STRING),
    ],
    )
    ```

    Copy code

    ```
    ModelSignature(
        inputs=[
      FeatureSpec(name="inputs", dtype=DataType.STRING),
        ],
        outputs=[
      FeatureGroupSpec(
          name="outputs",
          specs=[
              FeatureSpec(name="sequence", dtype=DataType.STRING),
              FeatureSpec(name="score", dtype=DataType.DOUBLE),
              FeatureSpec(name="token", dtype=DataType.INT64),
              FeatureSpec(name="token_str", dtype=DataType.STRING),
          ],
          shape=(-1,),
      ),
        ],
    )
    ```
  - Signature for token classification tasks:

    Before v1.8.0v1.8.0 and later

    Copy code

    ```
    ModelSignature(
        inputs=[
      FeatureSpec(name="inputs", dtype=DataType.STRING),
        ],
        outputs=[
      FeatureSpec(name="outputs", dtype=DataType.STRING),
        ],
    )
    ```

    Copy code

    ```
    ModelSignature(
        inputs=[FeatureSpec(name="inputs", dtype=DataType.STRING)],
        outputs=[
      FeatureGroupSpec(
          name="outputs",
          specs=[
              FeatureSpec(name="word", dtype=DataType.STRING),
              FeatureSpec(name="score", dtype=DataType.DOUBLE),
              FeatureSpec(name="entity", dtype=DataType.STRING),
              FeatureSpec(name="index", dtype=DataType.INT64),
              FeatureSpec(name="start", dtype=DataType.INT64),
              FeatureSpec(name="end", dtype=DataType.INT64),
          ],
          shape=(-1,),
      ),
        ],
    )
    ```
  - Signature for question-answering tasks:

    Before v1.8.0v1.8.0 and later

    Copy code

    ```
    ModelSignature(
        inputs=[
      FeatureSpec(name="question", dtype=DataType.STRING),
      FeatureSpec(name="context", dtype=DataType.STRING),
        ],
        outputs=[
      FeatureSpec(name="outputs", dtype=DataType.STRING),
        ],
    )
    ```

    Copy code

    ```
    ModelSignature(
        inputs=[
      FeatureSpec(name="question", dtype=DataType.STRING),
      FeatureSpec(name="context", dtype=DataType.STRING),
        ],
        outputs=[
      FeatureGroupSpec(
          name="answers",
          specs=[
              FeatureSpec(name="score", dtype=DataType.DOUBLE),
              FeatureSpec(name="start", dtype=DataType.INT64),
              FeatureSpec(name="end", dtype=DataType.INT64),
              FeatureSpec(name="answer", dtype=DataType.STRING),
          ],
          shape=(-1,),
      ),
        ],
    )
    ```
  - Signature for question-answering tasks when `top_k` is greater than 1:

    Before v1.8.0v1.8.0 and later

    Copy code

    ```
    ModelSignature(
        inputs=[
      FeatureSpec(name="question", dtype=DataType.STRING),
      FeatureSpec(name="context", dtype=DataType.STRING),
        ],
        outputs=[
      FeatureSpec(name="outputs", dtype=DataType.STRING),
        ],
    )
    ```

    Copy code

    ```
    ModelSignature(
        inputs=[
      FeatureSpec(name="question", dtype=DataType.STRING),
      FeatureSpec(name="context", dtype=DataType.STRING),
        ],
        outputs=[
      FeatureGroupSpec(
          name="answers",
          specs=[
              FeatureSpec(name="score", dtype=DataType.DOUBLE),
              FeatureSpec(name="start", dtype=DataType.INT64),
              FeatureSpec(name="end", dtype=DataType.INT64),
              FeatureSpec(name="answer", dtype=DataType.STRING),
          ],
          shape=(-1,),
      ),
        ],
    )
    ```
  - Signature for text-classification tasks when `top_k` is `None`:

    Before v1.8.0v1.8.0 and later

    Copy code

    ```
    ModelSignature(
        inputs=[
      FeatureSpec(name="text", dtype=DataType.STRING),
      FeatureSpec(name="text_pair", dtype=DataType.STRING),
        ],
        outputs=[
      FeatureSpec(name="label", dtype=DataType.STRING),
      FeatureSpec(name="score", dtype=DataType.DOUBLE),
        ],
    )
    ```

    Copy code

    ```
    ModelSignature(
        inputs=[
      FeatureSpec(name="text", dtype=DataType.STRING),
        ],
        outputs=[
      FeatureSpec(name="label", dtype=DataType.STRING),
      FeatureSpec(name="score", dtype=DataType.DOUBLE),
        ],
    )
    ```
  - Signature for text-classification tasks when `top_k` is not `None`:

    Before v1.8.0v1.8.0 and later

    Copy code

    ```
    ModelSignature(
        inputs=[
      FeatureSpec(name="text", dtype=DataType.STRING),
      FeatureSpec(name="text_pair", dtype=DataType.STRING),
        ],
        outputs=[
      FeatureSpec(name="outputs", dtype=DataType.STRING),
        ],
    )
    ```

    Copy code

    ```
    ModelSignature(
        inputs=[
      FeatureSpec(name="text", dtype=DataType.STRING),
        ],
        outputs=[
      FeatureGroupSpec(
          name="labels",
          specs=[
              FeatureSpec(name="label", dtype=DataType.STRING),
              FeatureSpec(name="score", dtype=DataType.DOUBLE),
          ],
          shape=(-1,),
      ),
        ],
    )
    ```
  - Signature for text-generation tasks:

    Before v1.8.0v1.8.0 and later

    Copy code

    ```
    ModelSignature(
        inputs=[FeatureSpec(name="inputs", dtype=DataType.STRING)],
        outputs=[
      FeatureSpec(name="outputs", dtype=DataType.STRING),
        ],
    )
    ```

    Copy code

    ```
    ModelSignature(
        inputs=[
      FeatureGroupSpec(
          name="inputs",
          specs=[
              FeatureSpec(name="role", dtype=DataType.STRING),
              FeatureSpec(name="content", dtype=DataType.STRING),
          ],
          shape=(-1,),
      ),
        ],
        outputs=[
      FeatureGroupSpec(
          name="outputs",
          specs=[
              FeatureSpec(name="generated_text", dtype=DataType.STRING),
          ],
          shape=(-1,),
      )
        ],
    )
    ```
- PyTorch and TensorFlow models now expect a single tensor input and output by default when they are logged to the Model Registry. To
  use multiple tensors (previous behavior), set `options={"multiple_inputs": True}`.

  Example with single tensor input:

  Copy code

  ```
  import torch

  class TorchModel(torch.nn.Module):
   def __init__(self, n_input: int, n_hidden: int, n_out: int, dtype: torch.dtype = torch.float32) -> None:
       super().__init__()
       self.model = torch.nn.Sequential(
           torch.nn.Linear(n_input, n_hidden, dtype=dtype),
           torch.nn.ReLU(),
           torch.nn.Linear(n_hidden, n_out, dtype=dtype),
           torch.nn.Sigmoid(),
       )

   def forward(self, tensor: torch.Tensor) -> torch.Tensor:
       return cast(torch.Tensor, self.model(tensor))

  # Sample usage:
  data_x = torch.rand(size=(batch_size, n_input))

  # Log model with single tensor
  reg.log_model(
   model=model,
   ...,
   sample_input_data=data_x
  )

  # Run inference with single tensor
  mv.run(data_x)
  ```

  For multiple tensor inputs or outputs, use:

  Copy code

  ```
  reg.log_model(
   model=model,
   ...,
   sample_input_data=[data_x_1, data_x_2],
   options={"multiple_inputs": True}
  )
  ```
- `enable_explainability` now defaults to `False` when the model can be deployed to Snowpark Container Services.

### Bug fixes

Modeling bug fixes:

- Fix a bug in some metrics that allowed an unsupported version of numpy to be installed automatically in the stored
  procedure, resulting in a numpy error on execution.

Model Registry bug fixes:

- Fix a bug that leads to incorrect `Model does not have _is_inference_api` error message when assigning a supported model as a property of a `CustomModel`.
- Fix a bug where inference does not work when models with more than 500 input features are deployed to SPCS.

### New features

New Model Registry features:

- Support for using a single `torch.Tensor`, `tensorflow.Tensor` and `tensorflow.Variable` as input or output data.
- Support for `xgboost.DMatrix datatype` for XGBoost models.

## Version 1.7.5 (2025-03-06)

`snowflake-ml-python` 1.7.5 adds support for Python 3.12.

### Bug fixes

Model Registry bug fixes:

- Fixed a compatibility issue where, when using `snowflake-ml-python` 1.7.0 or later to save a `tensorflow.keras` model with keras 2.x,
  the model could not be run in Snowflake. This issue occurred when `relax_version` is set to `True` (or default) and a new version of `snowflake-ml-python` is available. If you have logged an affected model, you can recover it by loading it using `ModelVerison.load`
  and logging it again with the latest version of `snowflake-ml-python`.
- Removed the validation that prevents data that does not have non-null values from being passed to `ModelVersion.run`.

### New features

New Model Registry features:

- Support for Hugging Face model configurations with auto-mapping functionality.
- Support for keras 3.x models with tensorflow and pytorch backends.

New Model Explainability features:

- Support for native and `snowflake-ml-python` sklearn pipelines.

## Version 1.7.4 (2025-01-28)

Important

`snowflake.ml.fileset.FileSet` has been deprecated and will be removed in a future release. Use
[snowflake.ml.dataset.Dataset](/developer-guide/snowflake-ml/dataset) and
[snowflake.ml.data.DataConnector](/developer-guide/snowpark-ml/reference/latest/api/data/snowflake.ml.data.data_connector.DataConnector) instead.

### Bug fixes

Registry bug fixes:

- Fixed an issue in which Hugging Face pipelines were loaded using an incorrect data type.
- Fixed an issue in which only one row was actually used when inferring a model signature.

### New features

New Cortex features:

- New `guardrails` option on the `Complete` function.

## Version 1.7.3 (2025-01-09)

### Dependency upgrades

- `fsspec` and `s3fs` must be 2024.6.1 or later and less than 2026.
- `mlflow` must be 2.16.0 or later and less than 3.

### New features

New Cortex features:

- Cortex functions now have “snake\_case” names. For example, `ClassifyText` is now `classify_text`. The old “CamelCase” names still work, but will be removed in a future release.

New Model Registry features:

- Registry now supports more than 500,000 features.
- Added `user_files` argument to `Registry.log_model` for including images or other files with the model.
- Added support for handling Hugging Face model configurations with auto-mapping functionality.

New Data features:

- Added the `DataConnector.from_sql` constructor.

### Bug fixes

Registry bug fixes:

- Fixed a bug that occurred when providing a non-range index pandas DataFrame as the input to `ModelVersion.run`.
- Improved random model registry name generation to avoid collisions.
- Fixed an issue when inferring a signature or running inference with Snowpark DataFrame that has a column whose type is ARRAY and contains a NULL value.
- `ModelVersion.run` now accepts a fully-qualified service name.
- Fixed an error in `log_model` for any scikit-learn models with only data preprocessing, including preprocessing-only pipeline models.

Monitoring bug fixes:

- Fixed an issue with creating monitors using fully-qualified names.
