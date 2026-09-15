# Snowflake ML Python release notes

This article contains the release notes for the Snowflake ML Python, including the following when applicable:

- Behavior changes
- New features
- Customer-facing bug fixes

Note

These notes do not include changes in features that have not been publicly announced.
Such features might appear in the Snowflake ML Python source code but not in the public documentation.

See [Snowflake ML: End-to-End Agentic Machine Learning](/developer-guide/snowflake-ml/overview) for documentation.

## Verifying the `snowflake-ml-python` package

All Snowflake packages are signed, allowing you to verify their origin. To verify the `snowflake-ml-python` package, follow the steps below:

1. Install `cosign`. This example uses the Go installation:
   [Installing cosign with Go](https://edu.chainguard.dev/open-source/sigstore/cosign/how-to-install-cosign/#installing-cosign-with-go).
2. Download the file from a repository such as [PyPI](https://pypi.org/project/snowflake-ml-python/#files).
3. Download a `.sig` file for that release from the GitHub [releases page](https://github.com/snowflakedb/snowflake-ml-python/releases/).
4. Verify the signature using `cosign`. For example:

Copy code

```
cosign verify-blob snowflake_ml_python-1.27.0.tar.gz --key snowflake-ml-python-1.27.0.pub --signature resources.linux.snowflake_ml_python-1.27.0.tar.gz.sig
```

Note

This example uses the library and signature for version 1.27.0 of the package. Use the filenames of the version you are verifying.

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
- The `snowflake.ml.model.models.huggingface_pipeline.HuggingfacePipelineModel` class has been deprecated and will be removed in a future release.

## Version 2.1.0 (2026-09-14)

### New Features

- Experiment Tracking: Added `ExperimentTracking.get_metric_history`, which returns every logged step of a
  metric instead of only the value at the highest step reported by `list_metrics`. Pass a metric name to scope
  the result to one metric, or omit it to get every metric of the run. The result is a lazy Snowpark DataFrame
  with `name`, `step`, `value`, and `timestamp` columns, so filtering and aggregation run in Snowflake.
- Feature Store: `list_feature_views()` now surfaces the online feature table’s setup readiness in the
  `online_config` JSON as `setup_status`, `setup_error_msg` and `setup_time`, for both batch/streaming
  and realtime feature views. The keys are present only when setup-readiness information is available
  for the table, so test for key presence. `SETUP_NOTREADY` means setup has not concluded yet, not
  that setup failed; `SETUP_FAILED` is the failure signal. Note that `SETUP_READY` is also reported
  when nothing has ever been reported for the table, and in that case `setup_status` may later change
  to `SETUP_FAILED`.

### Bug Fixes

- Registry: Fixed logging of MLflow models created with `mlflow.sklearn.save_model()`. The model is
  now re-logged from the scikit-learn estimator using the serialization format it was saved with,
  instead of from MLflow’s PyFunc wrapper with the version-dependent default format.

### Behavior Changes

### Deprecations

## Version 2.0.0 (2026-09-10)

`snowflake-ml-python` 2.0 is a major release that removes deprecated APIs and slims down the
default install footprint.

### New Features

- Feature Store: added `alter_online_service(size=...)`, which changes the size of an existing Online Service. The
  call returns as soon as the request is recorded; the change runs in the background and can take hours on a large
  Online Service, which keeps serving online reads and stream ingestion throughout. Poll
  `get_online_service_status()` until `status` is `RUNNING` at the requested size.

### Bug Fixes

- Feature Store: `delete_feature_view` now drops the online feature table before the
  offline dynamic table or view, so a dependent FeatureGroup (error 099940) does not
  leave an orphaned offline object.

### Behavior Changes

- Registry: Models logged from a Snowflake Container Runtime notebook without an explicit
  `target_platforms` now default to both Warehouse and Snowpark Container Services instead of
  Snowpark Container Services only. Warehouse is no longer dropped from the default target
  platforms.
- Dependencies: `scikit-learn`, `xgboost`, and `shap` are no longer required dependencies of
  `snowflake-ml-python`. They are now optional extras. Install them with
  `pip install snowflake-ml-python[scikit-learn]`, `[xgboost]`, `[shap]`, or `[all]` when using
  the corresponding functionality. Extras are independent: `[xgboost]` and `[lightgbm]` install
  only those libraries, not `scikit-learn`. Native XGBoost or LightGBM models (for example
  logging to the Model Registry) only need `[xgboost]` or `[lightgbm]`.
  `snowflake.ml.modeling` estimators always require `scikit-learn`, so the XGBoost and LightGBM
  wrappers need `pip install "snowflake-ml-python[xgboost,scikit-learn]"` or
  `"snowflake-ml-python[lightgbm,scikit-learn]"`.
- Feature Store: Added an optional `feature_store` extra. Install `snowflake-ml-python[feature_store]`
  to pull in `httpx`, which is required for online feature serving reads. `httpx` is not installed by
  the default `snowflake-ml-python` install. Conda users still need to install `httpx` separately
  (for example `conda install httpx`) to use the online Feature Store.
- Modeling: Importing a `snowflake.ml.modeling` subpackage (for example
  `snowflake.ml.modeling.linear_model`, `snowflake.ml.modeling.xgboost`,
  `snowflake.ml.modeling.lightgbm`, or `snowflake.ml.modeling.preprocessing`) without the optional
  dependencies it needs now raises an actionable `ImportError` that names only the missing
  package(s), instead of a confusing missing-attribute error.
  `scikit-learn` and `xgboost` are attributed to the 2.0 dependency change; `lightgbm` was
  already an optional extra before 2.0.

### Deprecations

- Modeling: The `snowflake.ml.modeling` estimators and preprocessing transformers are deprecated and
  will be removed in a future release. Importing a `snowflake.ml.modeling` subpackage now emits a
  `DeprecationWarning`. Train models with the native scikit-learn, XGBoost, or LightGBM estimators
  and log them to the Snowflake Model Registry (`snowflake.ml.registry`) instead.

### Breaking Changes

- Generic: Require python >= 3.10. Python 3.9 is no longer supported.
- Removed the deprecated `snowflake.ml.utils.connection_params.SnowflakeLoginOptions` public API
  (deprecated since 1.8.5).
- Registry: `ModelVersion.run_batch` now runs on `EXECUTE INFERENCE JOB SERVICE`. The single
  `job_spec` argument is replaced by the `resources_spec`, `inference_spec`, and `image_build_spec`
  blocks, and input may be supplied as either a DataFrame (`X`) or an existing stage path
  (`input_stage_location`). `output_spec.stage_location` is treated as a base: results are written
  under a per-job subdirectory, `<stage_location>/<job_name>/`. `output_spec.base_stage_location`,
  `job_spec.job_name_prefix`, and `job_spec.block` no longer exist.
- Registry: Removed the `snowflake.ml.model.batch` module. Use `snowflake.ml.model.batch_inference`,
  which exports `BatchInferenceTask` alongside the input, output, resources, inference, and image
  build spec classes.
- Feature Store: Feature views created before 1.42.0 that use the `last_distinct_n` or
  `first_distinct_n` aggregation function can no longer be read offline. `generate_dataset`,
  `generate_training_set`, `retrieve_feature_values`, and `read_feature_view` now raise a
  `ValueError` for such feature views. Re-create the feature view to restore offline reads.
- Dependencies: `snowflake-snowpark-python` must now be `>=1.37.0`. Earlier releases import
  `pkg_resources`, which `setuptools` removed in 82.0.0, so they fail to import in environments
  with a current `setuptools`.

## Version 1.54.0 (2026-08-31)

### New Features

- Registry: `log_model(..., options={"case_sensitive": True})` and
  `options={"max_batch_size": N}` apply those settings to all methods. Per-method
  `method_options` still override the global values.
- Feature Store: `create_online_service` accepts a `size` kwarg naming the size to
  provision the Online Service at, one of `"XS"`, `"S"`, `"M"`, `"L"`, `"XL"`,
  `"2XL"`, `"3XL"` (case-insensitive). When omitted, the server-side default applies;
  accounts that cap the available size provision at their cap.
  `get_online_service_status()` now reports the provisioned `size`, which is `None`
  for services created before sizes were recorded.
- Experiment Tracking: Source provenance now also records the id of the enclosing ML
  job when a run is created from inside one.

### Bug Fixes

- Feature Store: Feature View metadata tags carrying unknown keys (including a legacy
  `refresh_mode`) no longer fail to deserialize; unknown keys are ignored on read and
  the tag still does not persist `refresh_mode`.
- Registry: Fixed `ModelVersion.load()` failing with `ValueError: ... is not a valid SQL identifier` when the model’s owner role is a quoted identifier.
- Feature Store: Fixed `FeatureStore.update_feature_view()` failing with `SQL compilation error: invalid value 'ADAPTIVE' for property 'REFRESH_MODE'` when enabling online
  storage for an existing feature view.

### Behavior Changes

### Deprecations

## Version 1.53.0 (2026-08-24)

### New Features

- ML Jobs: `submit_file`, `submit_directory`, and `submit_from_stage` accept a `parallel` kwarg
  (default `False`). With `parallel=True`, the entrypoint is executed directly on every instance
  with the job topology injected into the environment (`SNOWFLAKE_JOB_INDEX`, `SNOWFLAKE_JOBS_COUNT`,
  `MLRS_HEAD_IP`, `MLRS_RDZV_PORT`, `MLRS_NODE_IPS`). Not supported for callable (`@remote`) payloads.
- ML Jobs: added `MLJob.distributed_result()`, the result API for distributed (for example
  `parallel=True`) jobs, which have no single head result. On full success it returns a
  `DistributedResult` (`success`, per-instance `exit_codes`, `failed_instance`, and instance 0’s
  `return_value`); if any instance failed it raises `DistributedJobError`, which carries that
  `DistributedResult` as `.result` and the earliest-failing instance’s reconstructed exception as
  its cause. `DistributedResult` and `DistributedJobError` are exported from `snowflake.ml.jobs`.
- ML Jobs: `submit_file`, `submit_directory`, and `submit_from_stage` accept a `preflight` kwarg,
  supported only together with `parallel=True`. It takes the name of a check level, run on every
  instance before the entrypoint: `"wiring"` checks the rendezvous plus a small collective, and
  `"reference"` additionally times a short synthetic DDP step and reports its step times from
  instance 0. If a requested check fails, the job aborts without running the entrypoint and the
  failure surfaces through `distributed_result()`. A check that does not apply to the job
  (`"reference"` on a CPU pool or a single instance) is reported as skipped and the job continues.
  Covers only the PyTorch c10d rendezvous backend.
- Feature Store: Iceberg-backed feature views can enable online storage when using the Postgres
  online store (`OnlineConfig(store_type=OnlineStoreType.POSTGRES)`). Online storage with Iceberg
  remains unsupported for other store types.

### Bug Fixes

### Behavior Changes

- Feature Store: `register_feature_view` now records `FV_SOURCE_REFS` metadata for managed batch
  feature views (derived from the `feature_df` schema) when the caller does not supply
  `source_refs`. Streaming and realtime feature views are unaffected.

### Deprecations

## Version 1.52.0 (2026-08-20)

### New Features

### Bug Fixes

### Behavior Changes

- Feature Store: `stream_ingest` now reuses the Online Service ingest endpoint cached on the
  `StreamSource` by `get_stream_source`, avoiding a per-call server status round-trip.

### Deprecations

## Version 1.51.0 (2026-08-12)

### New Features

- ML Jobs: `artifact_repositories` now accepts a list of repositories, allowing multiple artifact
  repositories to be specified for a job.
- Registry: Added support for logging and running MLflow 3.x models.

### Bug Fixes

- Registry: Fixed a bug where an MLflow model logged with
  `target_platforms=["SNOWPARK_CONTAINER_SERVICES"]` could drop its pip dependencies, leaving the
  deployed model missing required packages.

### Behavior Changes

### Deprecations

## Version 1.50.0 (2026-08-03)

### New Features

### Bug Fixes

### Behavior Changes

### Deprecations

## Version 1.49.0 (2026-07-29)

### New Features

- Experiment Tracking: `ExperimentTracking` now captures best-effort source provenance (entry-point filename and any
  surrounding git commit, branch, and remote URL) for each new run by default. Pass `capture_source_info=False` to
  disable it. Collection is always non-fatal and never blocks run creation.

### Bug Fixes

- Registry: Fixed `ModelVersion.load()` failing with `Result for query <id> has expired` inside Snowflake Container
  Runtime notebooks. Model file downloads now use the `session.file.get` FileOperation API (the same mechanism used
  when logging a model) instead of a raw `GET` query, avoiding a dependency on `collect()` result sets.

### Behavior Changes

### Deprecations

## Version 1.48.0 (2026-07-22)

### New Features

- Experiment Tracking: `ExperimentTracking` now captures best-effort source provenance (entry-point filename and any
  surrounding git commit, branch, and remote URL) for each new run by default. Pass `capture_source_info=False` to
  disable it. Collection is always non-fatal and never blocks run creation.

### Bug Fixes

- Registry: Fixed a bug where logging a model with explainability enabled could fail with a data
  validation error (“There is no non-null data in column …”) when a numeric input column was
  entirely null within the background sample. The `explain` method now reuses the model’s existing
  input signature instead of re-inferring it from the sample.

### Behavior Changes

### Deprecations

## Version 1.47.0 (2026-07-15)

### New Features

- Experiment Tracking: Added `ExperimentTracking.list_model_versions` to retrieve the model versions that were
  logged under a run. Models logged via `log_model` inside a run are linked to that run through Snowflake lineage,
  and this method traverses that lineage to return the corresponding `ModelVersion` objects.

Copy code

```
from snowflake.ml.experiment import ExperimentTracking

exp = ExperimentTracking(session)
exp.set_experiment("MY_EXPERIMENT")
with exp.start_run(run_name="MY_RUN"):
    exp.log_model(model, model_name="MY_MODEL", sample_input_data=X)

model_versions = exp.list_model_versions(run_name="MY_RUN")
```

### Bug Fixes

- Experiment Tracking: Fix a bug where `.set_experiment` does not recreate an experiment deleted in Snowsight

### Behavior Changes

- Registry: `enable_explainability` now defaults to `False` for all model types when logging a model. Previously it
  defaulted to `True` for XGBoost, LightGBM, and CatBoost models and was auto-enabled for supported scikit-learn and
  Snowpark ML modeling models when running in the Warehouse. To generate an `explain` method, explicitly pass
  `options={"enable_explainability": True}` to `log_model` (this requires `sample_input_data` for supported model
  types).

### Deprecations

## Version 1.46.0 (2026-07-07)

### New Features

### Bug Fixes

### Behavior Changes

- Registry: For Snowpark ML Pipeline models with explainability enabled, explanations now cover only the columns the
  final estimator was actually trained on (its `input_cols`). Untransformed passthrough columns (e.g. raw string
  columns left in place by an encoder using new `output_cols`, or the label column) are no longer included in the
  explain output. This also fixes a failure where such passthrough columns could reach the SHAP explainer and raise an
  error during `log_model(..., enable_explainability=True)`.

### Deprecations

## Version 1.45.0 (2026-07-01)

### New Features

- Feature Store: `FeatureView` now supports an `initialization_warehouse` that is used for the initial build and any
  subsequent reinitializations of the backing dynamic table (a full scan of the source data), while `warehouse`
  continues to drive the lighter incremental refreshes. This mirrors the dynamic table `INITIALIZATION_WAREHOUSE`
  knob, lets you pair a larger warehouse for initialization with a smaller one for steady-state refresh, and is also
  used for the one-time backfill of streaming feature views. It can be set at registration, changed via
  `update_feature_view(initialization_warehouse=...)`, and is surfaced by `list_feature_views(verbose=True)`.

Copy code

```
draft_fv = FeatureView(
    name="F_TRIP",
    entities=[entity],
    feature_df=feature_df,
    refresh_freq="1d",
    warehouse="SMALL_WH",            # incremental refreshes
    initialization_warehouse="LARGE_WH",  # initial build / reinitialization
)
fv = fs.register_feature_view(draft_fv, version="1.0")
```

- Registry: LLM models deployed with the OpenAI chat signatures now support structured outputs
  through an optional `response_format` param matching the OpenAI Chat Completions API
  (`{"type": "json_schema", "json_schema": {"name": "...", "schema": {...}}}`), letting callers
  constrain model output to a JSON Schema.

Copy code

```
from pydantic import BaseModel
import pandas as pd

class CityCountry(BaseModel):
    city: str
    country: str

response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "city_country",
        "schema": CityCountry.model_json_schema(),
    },
}

x_df = pd.DataFrame.from_records(
    [
        {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What is the capital of France?"},
                    ],
                },
            ],
        }
    ]
)

mv.run(
    X=x_df,
    params={"response_format": response_format},
    service_name=...,
)
```

### Bug Fixes

### Behavior Changes

### Deprecations

## Version 1.44.0 (2026-06-23)

### New Features

### Bug Fixes

### Behavior Changes

### Deprecations

## Version 1.43.0 (2026-06-16)

### New Features

- Registry: `inference_engine_options["engine"]` now accepts case-insensitive strings in addition to
  `InferenceEngine` enum members. Supported values are `"vllm"` and `"python_generic"` (for example,
  `"vLLM"`, `"VLLM"`, and `"PYTHON_GENERIC"` are all accepted). This applies to `ModelVersion.create_service()`
  and `ModelVersion.run_batch()`.

Copy code

```
from snowflake.ml.registry import Registry

registry = Registry(session)
mv = registry.get_model("my_model").version("v1")

mv.create_service(
    service_name="my_vllm_service",
    service_compute_pool="GPU_COMPUTE_POOL",
    gpu_requests="1",
    inference_engine_options={
        "engine": "vLLM",
        "engine_args_override": ["--max-model-len=4096"],
    },
)

job = mv.run_batch(
    compute_pool="GPU_COMPUTE_POOL",
    X=input_df,
    output_spec=output_spec,
    inference_engine_options={
        "engine": "python_generic",
    },
)
```

### Bug Fixes

- Registry: Fixed `explain()` failing with type mismatch errors when passing a Snowpark DataFrame.
  Snowpark DataFrame columns are now explicitly cast to match model signature types before SQL
  generation. Table functions (used by `explain`) enforce stricter type coercion than scalar functions
  (used by `predict`), so columns that were implicitly coerced for `predict` would be rejected by
  `explain`.

### Behavior Changes

- Registry: `SentenceTransformers` models no longer hard-code a default inference batch size of 32.
  When `batch_size` is not specified at `log_model` time and is not overridden at inference, the
  `sentence-transformers` library default is used. To pin a specific size, pass `batch_size` via
  `log_model(..., options={"batch_size": N})` or as an inference-time parameter. All
  `SentenceTransformers` models logged with this release require a client/serving runtime on version
  1.43.0 or later (regardless of whether `batch_size` was specified).

### Deprecations

## Version 1.42.0 (2026-06-11)

### New Features

- Registry: Support `truncate_dim` for `SentenceTransformers` models. Truncation set at
  construction (`SentenceTransformer(..., truncate_dim=N)`) is captured when the model is logged
  and restored on reload. On clients with `sentence-transformers` 5.0.0 or later, `truncate_dim`
  is also exposed as a runtime parameter in the model signature.
- Registry: `log_model()` now captures a representative row from `sample_input_data` and stores it alongside the model
  so inference code snippets shown in the model registry UI can be pre-filled with realistic values. Pass
  `options={"capture_sample_input_data": False}` to opt out (e.g., for sensitive data); generic placeholder values
  will be used in the snippets instead.

### Bug Fixes

- Registry: Pin `transformers<5` for additional HuggingFace pipeline tasks removed in
  `transformers 5.x` (`summarization`, `text2text-generation`, `question-answering`, and
  `translation_*`), preventing deployment failures from missing pipeline classes.

### Behavior Changes

### Deprecations

## Version 1.41.0 (2026-05-27)

### New Features

- Registry: Extended `ParamSpec` support to MLflow PyFunc, LightGBM, XGBoost, and CatBoost models.
  Parameters declared in the model signature can now be passed at inference time.

### Bug Fixes

### Behavior Changes

### Deprecations

## Version 1.40.0 (2026-05-19)

### New Features

### Bug Fixes

- Feature Store: `get_feature_view()` now correctly preserves `online_config` for feature views whose
  names require SQL quoting (mixed case or special characters such as a space). Previously the returned
  FeatureView reported `online=False` even when online was enabled at registration, causing
  `read_feature_view(store_type=ONLINE)` to fail with “Online store is not enabled”.

### Behavior Changes

- Registry: `log_model(..., options=...)` now rejects unknown top-level keys and unknown keys inside each
  `method_options` entry (for example misspellings or options that belong to a different model framework).
  Previously those keys were ignored. Validation is based on the public save-option TypedDicts and runs
  before dependency reconciliation.
- Registry: `use_gpu` is declared on the CatBoost, XGBoost, PyTorch, and TorchScript save-option
  TypedDicts to match the save paths that already read this flag.

### Deprecations

## Version 1.39.0

### New Features

### Bug Fixes

- Feature Store: `update_feature_view` now correctly handles every transition between duration-based
  and CRON-based `refresh_freq`. Previously a CRON expression was forwarded to the Dynamic Table’s
  `TARGET_LAG` (which Snowflake rejects), `duration → cron` failed because the companion Task did not
  yet exist, and `cron → duration` left the Task orphaned and continuing to fire on its old schedule.
  All four `(old, new)` transitions now correctly create, alter, or drop the Task as needed, with
  symmetric rollback on failure.

### Behavior Changes

- Feature Store: For CRON-based feature views, `get_feature_view()`, `list_feature_views()`, and
  `register_feature_view()` now return the original cron expression as `refresh_freq` instead of
  `"DOWNSTREAM"`. The underlying Dynamic Table still uses `TARGET_LAG = 'DOWNSTREAM'` with a companion
  Task — this is purely a display change so the round-trip preserves what the user passed in.
- Registry: When `target_platforms` includes WAREHOUSE and pip installs are needed without a user-supplied
  `pip` artifact repository, `log_model` injects `snowflake.snowpark.pypi_shared_repository` after
  verifying access. This applies to explicit `pip_requirements` and to pip-only packaging when there are
  no user conda dependencies. If `pypi_shared_repository` is inaccessible in the pip-only case, automatic packaging
  dependencies fall back to conda instead of forcing pip-only without an index.

### Deprecations

## Version 1.38.0

### New Features

- Registry: Auto-inferred signatures for HuggingFace pipeline models now include task-specific `ParamSpecs`,
  allowing users to control inference behavior at prediction time via `params`. Generative tasks expose
  GenerationConfig parameters (e.g. `temperature`, `max_new_tokens`, `top_p`); non-generative tasks expose
  their own task-specific parameters (e.g. `top_k` for fill-mask, `aggregation_strategy` for
  zero-shot-classification).

### Bug Fixes

### Behavior Changes

- Registry: For HuggingFace `text-generation` pipelines whose tokenizer defines a chat template, the
  auto-inferred signature now matches the OpenAI Chat Completions API
  (`_OPENAI_CHAT_SIGNATURE_WITH_PARAMS_SPEC`). Inputs are a single `messages` column and inference
  controls (`temperature`, `max_completion_tokens`, `stop`, `n`, `stream`, `top_p`, `frequency_penalty`,
  `presence_penalty`) move from `inputs` to `params` with default values. Predictions return the OpenAI
  response shape (`id`, `object`, `created`, `model`, `choices`, `usage`); the generated text is at
  `choices[0].message.content` instead of `outputs[0].generated_text`.
- Registry: For HuggingFace `image-text-to-text`, `video-text-to-text`, and `audio-text-to-text`
  pipelines, the auto-inferred signature now uses `_OPENAI_CHAT_SIGNATURE_WITH_PARAMS_SPEC` instead of
  `_OPENAI_CHAT_SIGNATURE_SPEC`. The input column set narrows to just `messages`, and the inference
  controls move to `params` with default values; the output schema is unchanged.

### Deprecations

## Version 1.37.0 (2026-04-29)

### New Features

- Registry (PrPr): The `model_init_once` save option now applies to **TABLE\_FUNCTION** model methods (including
  partitioned table functions) for warehouse deployments, in addition to scalar **FUNCTION** methods. The generated
  handler uses the same eager `@udf_init_once` model load path as UDFs.
- Experiment Tracking: `end_run` now accepts an optional `status` argument (`"FINISHED"` or `"FAILED"`) to explicitly
  set the final run status. When a run’s context manager exits with an exception, the status is automatically set to
  `"FAILED"`.

### Bug Fixes

- Registry: Fixed `log_model()` failing for some Snowpark ML `Pipeline` models with explainability when the
  full pipeline could not be converted to a native object; task inference now uses the final estimator instead.
- Registry: `run_batch()` now raises a clear `ValueError` when a partitioned model’s output signature
  includes the partition column. Previously this produced duplicate columns in the output, causing
  cryptic Ray/Arrow errors (`AttributeError` or `KeyError`) deep in the batch inference pipeline.

### Behavior Changes

### Deprecations

## Version 1.36.0 (2026-04-22)

### New Features

- Feature Store: for latency-sensitive online feature view reads, set use\_session\_warehouse=True to
  re-use the warehouse from the current session and achieve the best latency.

### Bug Fixes

- Registry: Pin `transformers<5` when saving HuggingFace pipeline models that use tasks removed in
  `transformers 5.x` (`image-to-text`, `visual-question-answering`, `conversational`), preventing
  deployment failures from missing pipeline classes.

### Behavior Changes

- Registry: Logging a model with `pip_requirements` and no `artifact_repository_map` now raises a `ValueError`
  when `target_platforms` explicitly includes `"WAREHOUSE"`. Previously this combination would silently proceed,
  resulting in the warehouse deployment being silently dropped.

### Deprecations

## Version 1.35.0 (2026-04-17)

### New Features

### Bug Fixes

- Registry: Fixed `ParamSpec.from_mlflow_spec` dropping `shape`, which caused shaped scalar params
  (e.g., array of ints) from MLflow to fail validation during model import.

### Behavior Changes

- ML Jobs: `spec_overrides` now validates container keys and warns when keys other than `name` and `secrets`
  are provided. Additional keys are not officially supported and may not behave as expected.

### Deprecations

## Version 1.34.0 (2026-04-08)

### New Features

- Experiment Tracking: Added `list_params` and `list_metrics` methods to retrieve parameters and metrics
  for runs within an experiment. Both methods return a Dataframe and accept an optional `run_name` argument
  to filter to a specific run.

### Bug Fixes

- Feature Store: Fixed `generate_dataset()`/`generate_training_set()` SQL generation for Unicode and case-sensitive
  identifiers (for example Japanese column names), ensuring columns are quoted exactly once and preventing SQL
  compilation errors such as `unexpected '<column_name>'`.

### Behavior Changes

- Registry: `enable_explainability=True` is now allowed for SPCS-only and non-warehouse-runnable models. Previously
  this raised a `ValueError`.

### Deprecations

## Version 1.33.0 (2026-03-31)

### New Features

- Registry: Extended `ParamSpec` support to PyTorch models. Parameters declared in the model signature
  can now be passed at inference time, matching the existing support for custom models.
- Registry (PrPr): Added `model_init_once` model save option to `log_model`. When set to `True`, the
  model is loaded once per worker process at startup, eliminating model-loading overhead. Defaults to `False`.
- Experiment Tracking live logging is out of private preview
  and will become generally available over the next few weeks.
- Registry: Bumped `transformers` upper bound to `<6`, adding compatibility with Hugging Face Transformers v5.

### Bug Fixes

- Experiment Tracking live logging: Fixed a bug where the tracebacks for uncaught exceptions were not logged when
  the code was running in a `with exp.start_run()` block.
- Registry: Fixed a thread leak in `create_service(block=True)` where the log-streaming thread could outlive the
  error handler when service deployment fails.

### Behavior Changes

### Deprecations

## Version 1.32.0 (2026-03-26)

### New Features

- Registry: Extended `ParamSpec` support to scikit-learn models. Parameters declared in the model signature
  can now be passed at inference time, matching the existing support for custom models.
- Registry: `infer_signature()` now accepts a `dict` for the `params` argument (e.g.,
  `params={"temperature": 0.7, "max_tokens": 100}`), automatically inferring `ParamSpec` objects
  from the Python value types. The existing `Sequence[BaseParamSpec]` form is still supported.

### Bug Fixes

- Experiment Tracking live logging (PrPr): Fixed a bug where the tracebacks for uncaught exceptions were not logged
  when the code was running inside Snowflake notebooks.

### Behavior Changes

- Registry: The models from `huggingface.TransformersPipeline` and `transformers.Pipeline` will default to safetensors
  file format by default by using `safe_serialization=True` parameter to the `save_pretrained` call. This creates
  safetensors files instead of PyTorch binaries or pt files, addressing security vulnerability CVE-2025-32434.

### Deprecations

## Version 1.31.0 (2026-03-19)

### New Features

### Bug Fixes

- Registry: Fixed custom model handler to explicitly persist `PARTITIONED=False` in model metadata for
  `@inference_api` methods. Previously, custom models using `@inference_api` with `TABLE_FUNCTION` type
  were incorrectly reported as partitioned.
- Registry: Fixed sklearn and SnowML model handlers to explicitly persist `PARTITIONED=False` metadata for
  the `explain` method, preventing it from being incorrectly reported as partitioned at read time.
- Registry: Fixed inconsistent `infer_signature` for columns containing NaN values. Previously,
  the inferred dtype (`DOUBLE` vs `INT64`) depended on whether NaN rows survived truncation, causing
  downstream validation failures. Now, the original pandas column dtype is respected during `infer_signature`,
  so columns with mix of integer and `np.nan` or `None` are consistently inferred as `DOUBLE` regardless of NaN position.
- Registry: Fixed a bug where invalid parameter types (e.g., passing a string to an integer parameter)
  were silently coerced instead of raising an error. Parameters are now strictly validated against their
  declared types before inference. This may break code that relied on the silent coercion behavior
  (e.g., `mv.run(..., params={"max_tokens": "100"})` or `mv.run(..., params={"some_int_param": True})`).
- ML Job: Fixed explicitly named `MLJobDefinition` objects so they can be overwritten in place and invoked
  repeatedly without job name collisions; the `generate_suffix` argument has been removed.
- Experiment Tracking live logging (PrPr): Fixed a bug that generated too many lines of log that consist entirely of
  whitespace.

### Behavior Changes

- Registry: Warehouse partitioned model inference no longer includes non-partition input columns (which were always
  NULL) in the output. The output now contains only the model’s output columns and the partition column.

### Deprecations

## Version 1.30.0

### New Features

- Experiment Tracking live logging (PrPr): In SPCS, call `set_live_logging_status(True)` to automatically capture and
  persist outputs to stdout and stderr while a run is active. The captured logs can be viewed from the Experiments UI.
- Registry: Support logging MLflow models created via `mlflow.*.save_model()` to the Snowflake Model
  Registry. Previously, only models logged through `mlflow.*.log_model()` were supported. This also
  enables logging custom `mlflow.pyfunc.PythonModel` subclasses saved locally.

### Bug Fixes

- Registry: Fixed Prophet model handler to correctly mark the `predict` method as partitioned, ensuring it
  uses a partitioned `TABLE_FUNCTION` when deployed to Snowflake.
- Registry: Support `text-generation` models without chat template. The model will have signatures to automatically take
  plain strings as input without needing to specify the signatures in `log_model`.
  The signature can be overridden if the user chooses to.

### Behavior Changes

- Registry: Huggingface models with task `text-generation` that do not have chat templates will be logged with signature
  that supports plain text (string) as input.

### Deprecations

- Registry: Removed support for logging Hugging Face Pipelines in config-only mode. Config-only
  models could not run in warehouse and required an External Access Integration (EAI) with egress
  to Hugging Face hosts. Use remote logging or local download instead — these approaches support
  warehouse execution and store model weights at log time, enabling fully air-gapped services.

## Version 1.29.0 (2026-02-24)

### New Features

- Model serving: Introducing `InferenceEngine.PYTHON_GENERIC` enum value.
  Users can pass `InferenceEngine.PYTHON_GENERIC` to use a Python-based inference server for model serving.

### Bug Fixes

- Registry: Fixed a bug where using inference parameters (ParamSpec) with table function or
  partitioned model methods would fail at runtime with a `NameError`.
- Registry: Fixed a bug where MLflow models with string columns failed during inference with
  “Can not safely convert string to <U0>” errors due to MLflow’s schema validation not handling
  `pd.StringDtype` correctly.

### Behavior Changes

- Dependencies: Removed `snowflake.core` as a runtime dependency. If you use `snowflake.core` (e.g.,
  `TaskDag`, `Root`, `Task`), add `snowflake.core` explicitly to your dependencies.

### Deprecations

## Version 1.28.0 (2026-02-17)

### New Features

### Bug Fixes

### Behavior Changes

### Deprecations

## Version 1.27.0 (2026-02-12)

### Bug Fixes

Model Registry bug fixes:

- Fixed failure of `model_version.run` caused by requiring READ privilege on the model instead of USAGE when the
  user’s role had only the USAGE privilege.

Feature store bug fixes:

- Fixed failure of `register_feature_view` with `overwrite=True` when the existing feature view is external and the
  new feature view is managed, or vice versa.

## Version 1.26.0 (2026-02-05)

### New Features

New Model Registry features:

- Model signatures can now include inference parameters via `ParamSpec`, allowing you to define
  constant parameters to be passed at inference time without including them in the input data.
  Example:

  Copy code

  ```
  import pandas as pd
  from snowflake.ml.model import custom_model, model_signature
  from snowflake.ml.registry import Registry

  # Define a custom model with inference parameters
  class MyModelWithParams(custom_model.CustomModel):
   @custom_model.inference_api
   def predict(
       self,
       input_df: pd.DataFrame,
       *,
       temperature: float = 1.0,  # keyword-only param with default
   ) -> pd.DataFrame:
       return pd.DataFrame({"output": input_df["feature"] * temperature})

  # Create sample data
  model = MyModelWithParams(custom_model.ModelContext())
  sample_input = pd.DataFrame({"feature": [1.0, 2.0, 3.0]})
  sample_output = model.predict(sample_input, temperature=1.0)

  # Define ParamSpec for the inference parameter
  params = [
   model_signature.ParamSpec(
       name="temperature",
       dtype=model_signature.DataType.FLOAT,
       default_value=1.0,
   ),
  ]

  # Infer signature with params
  sig = model_signature.infer_signature(
   input_data=sample_input,
   output_data=sample_output,
   params=params,
  )

  # Log model with the signature
  registry = Registry(session)
  mv = registry.log_model(
   model=model,
   model_name="my_model_with_params",
   version_name="v1",
   signatures={"predict": sig},
  )

  # Run inference with custom parameter value
  result = mv.run(sample_input, function_name="predict", params={"temperature": 2.0})
  ```

New Feature Store features:

- New `auto_prefix` parameter and `with_name` method to prevent column name collisions when joining multiple feature
  views in dataset generation.
- Dynamic Iceberg tables can now be used as backing storage for Feature Views. Use `StorageConfig` with
  `StorageFormat.ICEBERG` to store data in Apache Iceberg format on external cloud storage. A new
  `default_iceberg_external_volume` parameter is available in `FeatureStore` to set a default external volume for
  Iceberg feature views.

## Version 1.25.1 (2026-02-03)

No public-facing changes. This release includes changes to a preview feature that has not been publicly announced.

## Version 1.25.0 (2026-01-28)

### New Features

New Model Serving features:

- The `create_service` method accepts a new `autocapture` argument to indicate whether inference data should be captured
  (see [Autocapture inference logs for realtime inference](/developer-guide/snowflake-ml/inference/auto-capture-inference-logs)).
- The `create_service` and `log_model_and_create_service` methods now accept an optional `min_instances` argument
  to specify the minimum number of instances for the service. The service automatically scales between the specified
  minimum and maximum instances based on traffic and hardware utilization. If `min_instances` is 0, the service
  automatically suspends when no traffic is detected for a period of time. The default value for `min_instances` is 0.

## Version 1.24.0 (2026-01-22)

### New Features

New Feature Store features:

- Tile-based aggregation support using a new `Feature` API for efficient and point-in-time correct time-series
  feature computation using pre-computed tiles.

New Model Registry features:

- SentenceTransformer models now support automatic signature inference. When logging a SentenceTransformer model,
  `sample_input_data` is optional. The signature is automatically inferred from the model’s embedding dimension when
  sample input data is not provided. The `encode`, `encode_query`, `encode_document`, `encode_queries`,
  `encode_documents` methods are supported.

  Copy code

  ```
  import sentence_transformers
  from snowflake.ml.registry import Registry

  # Create model
  model = sentence_transformers.SentenceTransformer("all-MiniLM-L6-v2")

  # Log model without sample_input_data - signature is auto-inferred
  registry = Registry(session)
  mv = registry.log_model(
   model=model,
   model_name="my_sentence_transformer",
   version_name="v1",
  )

  # Run inference with auto-inferred signature (input: "text", output: "output")
  import pandas as pd
  result = mv.run(pd.DataFrame({"text": ["Hello world"]}))
  ```

## Version 1.23.0 (2026-01-15)

### New Features

New ML Jobs features:

- ML Jobs now support Python 3.11 and Python 3.12. Jobs automatically select a runtime environment
  matching the client Python version.

### Bug Fixes

Model Registry bug fixes:

- Empty output in HuggingFace’s Token Classification (Named Entity Recognition) models no longer causes failures.

Model Serving bug fixes:

- Container statuses are now correctly reported and should not be blank.

## Version 1.22.0 (2026-01-09)

### New Features

New Model Registry features:

- You can now remotely log a transformer pipeline model using a Snowpark Container Services (SPCS) job.

  Copy code

  ```
  # create reference to the model
  model = huggingface.TransformersPipeline(
   model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
   task="text-generation",
  )

  # Remotely log the model, a SPCS job will run async and log the model
  mv = registry.log_model(
   model=model,
   model_name="tinyllama_remote_log",
   target_platforms=["SNOWPARK_CONTAINER_SERVICES"],
   signatures=openai_signatures.OPENAI_CHAT_SIGNATURE,
  )
  ```

## Version 1.21.0 (2026-01-05)

### Behavior changes

ML Jobs behavior changes:

- The behavior of the `additional_payloads` parameter is changing. Use the `imports` argument to declare additional
  dependencies, such as ZIP files and Python modules. Local directories and Python files are automatically compressed,
  and their internal layout is determined by the specified import path. The import path applies only to local
  directories, Python files, and staged python files; it has no effect on other import types. When referencing files in a
  stage, only individual files are supported, not directories.

Experiment Tracking behavior changes:

- `ExperimentTracking` is now a singleton class.

### Bug Fixes

Experiment Tracking bug fixes:

- Reaching the run metadata size limit in `log_metrics` or `log_params` now issues a warning instead of raising an exception.

Model Registry bug fixes:

- `ModelVersion.run` now raises a `ValueError` if the model is a SPCS-only model and `service_name` is not provided.

### New preview features

- The `create_service` method now accepts the Boolean argument `autocapture` to indicate whether inference data is automatically captured.

### New release features

New Model Registry features:

- The new `snowflake.ml.model.models.huggingface.TransformersPipeline` class is intended to replace `snowflake.ml.model.models.huggingface_pipeline.HuggingfacePipelineModel`,
  although the older class is not yet deprecated. The new class knows model signatures for common tasks so that you do not need to specify them manually.
  The supported tasks are currently:

  - `fill-mask`
  - `question-answering`
  - `summarization`
  - `table-question-answering`
  - `text2text-generation`
  - `text-classification` (alias `sentiment-analysis`)
  - `text-generation`
  - `token-classification` (alias `ner`)
  - `translation`
  - `translation_xx_to_yy`
  - `zero-shot-classification` (lets you log models without loading them into memory)
- The `list_services` API now shows an internal endpoint that can be called from another SPCS node or notebook without Enterprise Application Integration.
  It also indicates whether autocapture is enabled for each service.

New DataConnector features:

- New `to_huggingface_dataset` method converts Snowflake data to HuggingFace datasets. Supports both in-memory
  `Dataset` (`streaming=False`) and streaming `IterableDataset` (`streaming=True`) modes.

### Deprecation notices

- The `snowflake.ml.model.models.huggingface_pipeline.HuggingfacePipelineModel` class has been deprecated and will be removed in a future release.
