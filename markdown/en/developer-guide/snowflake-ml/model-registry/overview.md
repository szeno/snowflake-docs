# Snowflake Model Registry

Note

The model registry API described in this topic is generally available as of `snowflake-ml-python` package version 1.5.0.

After training your model, operationalizing the model and running inference in Snowflake starts with logging
the model in the Snowflake Model Registry. The Model Registry lets you securely manage models and their metadata in Snowflake,
regardless of origin and type, and makes running inference easy.

Important

The Snowflake Model Registry works with machine learning models developed in Python for the Snowflake ML
ecosystem. Models trained using [Snowflake ML Functions](/guides-overview-ml-functions) (for example,
[FORECAST](/sql-reference/classes/forecast)) do not appear in the model registry. Some model types,
such as [Cortex Fine-Tuned LLMs](/user-guide/snowflake-cortex/cortex-finetuning), appear in the model registry’s
[Snowsight UI](/developer-guide/snowflake-ml/model-registry/snowsight-ui), but are not managed by the model registry API.

The Snowflake Model Registry provides the following capabilities:

- Stores and manages model versions, model metrics, and model metadata.
- Serves models and runs distributed inference at scale using Python, SQL, or REST API endpoints.
- Manages model life cycle with flexible governance options and working with models from dev to prod environments.
- Monitors model performance and drift using Snowflake ML Observability.
- Securely manages model access with role based access control (RBAC).

The model registry stores machine learning models as first-class schema-level objects in Snowflake.

After you have logged a model, you can invoke its methods (equivalent to functions or stored procedures) to perform
model operations, such as [inference](/developer-guide/snowflake-ml/inference/native-batch-inference-sql)
, in a Snowflake [virtual warehouse](/user-guide/warehouses),
or serve the model in Snowpark Container Services for [GPU-based inference](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api).

The Snowflake Model Registry has [built-in types](/developer-guide/snowflake-ml/model-registry/built-in-models/overview) support for the most common model
types, including [scikit-learn](/developer-guide/snowflake-ml/model-registry/built-in-models/scikit-learn),
[xgboost](/developer-guide/snowflake-ml/model-registry/built-in-models/xgboost),
[LightGBM](/developer-guide/snowflake-ml/model-registry/built-in-models/lightgbm),
[Prophet](/developer-guide/snowflake-ml/model-registry/built-in-models/prophet),
[CatBoost](/developer-guide/snowflake-ml/model-registry/built-in-models/catboost),
[PyTorch](/developer-guide/snowflake-ml/model-registry/built-in-models/pytorch),
[TensorFlow](/developer-guide/snowflake-ml/model-registry/built-in-models/tensorflow),
[Keras](/developer-guide/snowflake-ml/model-registry/built-in-models/keras),
[Hugging Face pipelines](/developer-guide/snowflake-ml/model-registry/built-in-models/hugging-face),
[Sentence Transformer](/developer-guide/snowflake-ml/model-registry/built-in-models/sentence-transformer),
and [MLFlow pyfunc models](/developer-guide/snowflake-ml/model-registry/built-in-models/mlflow).
The Model Registry is also flexible and powerful enough to support your own previously-trained models, as well as any custom processing code.

Tip

See examples of these model types with end to end workflows in [Examples and Quickstarts](/developer-guide/snowflake-ml/model-registry/examples-and-quickstarts).

The main classes in the Snowflake Model Registry Python API are:

- [snowflake.ml.registry.Registry](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/registry/snowflake.ml.registry.Registry):
  Manages models within a schema.
- [snowflake.ml.model.Model](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/model/snowflake.ml.model.Model):
  Represents a model.
- [snowflake.ml.model.ModelVersion](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/model/snowflake.ml.model.ModelVersion):
  Represents a version of a model.

This topic describes how to perform registry operations in Python using the `snowflake-ml-python` library.
You can also perform many registry operations in SQL; see [Model Registry SQL](/sql-reference/commands-model).

## Required privileges

To create a model, you must either own the schema where the model is created or have the `CREATE MODEL` privilege on it.
To use a model, you must either own the model or have either USAGE or READ privilege on it.

1. The USAGE privilege allows grantees to use the model for warehouse inference without being able to see any of its internals.
2. The READ privilege allows grantees to use the model for SPCS inference and also see its metadata, such as its comments, tags, and metrics.

To give users USAGE access to all existing models in a schema, use
`GRANT USAGE ON ALL MODELS IN SCHEMA <schema> TO ROLE <role>;` You can also give users access to future models created in a schema
automatically via `GRANT USAGE ON FUTURE MODELS IN SCHEMA <schema> TO ROLE <role>;`. .

Similarly, you can give users READ access to all existing or future models in a schema by using the same syntax, but replacing
`USAGE` with `READ`.

If a user’s role has OWNER, USAGE or READ privilege on a model, it appears in the [Snowsight model registry page](/developer-guide/snowflake-ml/model-registry/snowsight-ui).
For details about how privileges work in Snowflake, see [Access control privileges](/user-guide/security-access-control-privileges).

## Current limitations

The following limits apply to models and model versions:

|  |  |
| --- | --- |
| Models | - Maximum of 1000 versions |
| Model versions | - Maximum of 10 methods - Maximum of 500 arguments per method - Maximum metadata (including metrics) of 100 KB - Maximum total model size of 15 GB (for warehouse deployed models) - Maximum config file size of 250 KB, including `conda.yml` and other manifest files that `log_model` generates internally.   (If a model has many functions and all of them have many arguments, for example, this limit might be exceeded.) |

Expand

Show lessSee more

## Opening the Snowflake Model Registry

Models are first-class Snowflake objects and can be organized within a database and schema along with other Snowflake
objects. The Snowflake Model Registry provides a Python class for managing models within a schema. Thus, any Snowflake schema
can be used as a registry. It is not necessary to initialize or otherwise prepare a schema for this purpose. Snowflake
recommends creating one or more dedicated schemas for this purpose, such as ML.REGISTRY. You can create the schema using
[CREATE SCHEMA](/sql-reference/sql/create-schema).

Before you can create or modify models in the registry, you must open the registry. Opening the registry returns a
reference to it, which you can then use to add new models and obtain references to existing models.

Copy code

```
from snowflake.ml.registry import Registry

reg = Registry(session=sp_session, database_name="ML", schema_name="REGISTRY")
```

## Registering models and versions

Note

You can also import a model from an external provider to Snowflake. For more information, see [Import and deploy models from an external service](/developer-guide/snowflake-ml/model-registry/snowsight-ui#label-model-import-external).

Adding a model to the registry is called *logging* the model. Log a model by calling the registry’s `log_model`
method. This method serializes the model — a Python object — and creates a Snowflake model object from it. This method also adds metadata, such as a description, to the model as specified in the `log_model` call.

Each model can have unlimited versions. To log additional versions of the model, call `log_model` again with
the same `model_name` but a different `version_name`.

You cannot add tags to a model when it is added to the registry, because tags are attributes of the model, and
`log_model` adds a specific model version, only creating a model when adding its first version. You can [update the model’s tags](#label-snowpark-model-registry-model-metadata) after logging the first version of the model.

In the following example, `clf`, short for “classifier,” is the Python model object, which was already
created elsewhere in your code. You can add a comment at registration time, as shown here. The combination of
name and version must be unique in the schema. You may specify `conda_dependencies` lists; the
specified packages will be deployed with the model.

Copy code

```
from snowflake.ml.model import task, type_hints
mv = reg.log_model(clf,
                   model_name="my_model",
                   version_name="v1",
                   conda_dependencies=["scikit-learn"],
                   comment="My awesome ML model",
                   metrics={"score": 96},
                   sample_input_data=train_features,
                   task=task.Task.TABULAR_BINARY_CLASSIFICATION)
```

The arguments of `log_model` are described here.

**Required arguments**

| Argument | Description |
| --- | --- |
| `model` | The Python model object of a supported model type. Must be serializable (“pickleable”). |
| `model_name` | The model’s name, used with `version_name` to identify the model in the registry. The name cannot be changed after the model is logged. Must be a [valid Snowflake identifier](/sql-reference/identifiers-syntax). |

Expand

Show lessSee more

Note

The combination of model name and version must be unique in the schema.

**Optional arguments**

| Argument | Description |
| --- | --- |
| `version_name` | String specifying the model’s version, used with `model_name` to identify the model in the registry. Must be a [valid Snowflake identifier](/sql-reference/identifiers-syntax). If missing, a human-readable version name is generated automatically. |
| `code_paths` | List of paths to directories of code to import when loading or deploying the model. |
| `comment` | Comment, for example a description of the model. |
| `conda_dependencies` | List of Conda packages required by your model. This argument specifies package names and optional versions in [Conda format](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/pkg-search.html), that is, `"[channel::]package [operator version]"`. If you do not specify a channel, the Snowflake channel is assumed when the model runs on a warehouse. conda-forge is assumed for models running on Snowpark Container Services (SPCS). |
| `ext_modules` | List of external modules to pickle with the model. Supported with scikit-learn, Snowpark ML, PyTorch, TorchScript, and custom models. |
| `metrics` | Dictionary that contains metrics linked to the model version. |
| `options` | Dictionary that contains options for model creation. The following options are available for all model types:   - `embed_local_ml_library`: whether to embed a copy of the local Snowpark ML library into the model. Default: `False`. - `relax_version`: whether to relax the version constraints of the dependencies. This replaces version specifiers like   `==x.y.z` with specifiers like `<=x.y, <(x+1)`. Default: `True`. - `save_location`: A string specifying the location (directory path) to save the model and metadata (e.g. `"/path/to/my/directory"`). - `function_type`: Sets the method function type globally to either “FUNCTION” or “TABLE\_FUNCTION”. To set method function types   individually see `function_type` in `method_options`. - `volatility`: Set the volatility for all model methods. Custom models default to `VOLATILE` and all other models default to `IMMUTABLE`.   To set method volatility individually, see `volatility` in `method_options`.   Note  `VOLATILE` model methods require a full table refresh when used in Dynamic Tables. For more information, see [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).   - `method_options`: A dictionary of per-method options, where the key is the name of a method and the value is a dictionary   that contains one or more of the options described here. The available options are:   - `case_sensitive`: Indicates whether the method and its signature are case-sensitive. Case-sensitive methods must be double-quoted     when used in SQL. This option also allows non-alphabetic characters in method names. Default: `False`.   - `max_batch_size`: Maximum batch size that the method will accept when called in the warehouse. Default: `None` (the batch     size is automatically determined).   - `function_type`: Set the method function type to “FUNCTION” or “TABLE\_FUNCTION”.   - `volatility`: Set the method volatility level to `IMMUTABLE` for deterministic functions or `VOLATILE` for non-deterministic functions. Deterministic functions always return the same result for the same input.   Copy code  ``` from snowflake.ml.model.volatility import Volatility  options = {   "embed_local_ml_library": True,   "relax_version": True,   "save_location": "/path/to/my/directory",   "function_type": "TABLE_FUNCTION",   "volatility": Volatility.IMMUTABLE,   "method_options": {     "predict": {       "case_sensitive": False,       "max_batch_size": 100,       "function_type": "TABLE_FUNCTION",       "volatility": Volatility.VOLATILE,     },   } ```  Individual model types may support additional options. See [Using built-in model types](/developer-guide/snowflake-ml/model-registry/built-in-models/overview). |
| `pip_requirements` | List of package specs for PyPI packages required by your model. To install those packages from an artifact repository (the built-in PyPI repository or a [customer-hosted repository](/developer-guide/udf/python/customer-hosted-python-artifact-repositories)), also set `artifact_repository_map`. Models that target a warehouse require an artifact repository for pip packages. For Snowpark Container Services (online or batch inference), specify a repository when the packages aren’t available on public PyPI, such as a private internal package. |
| `artifact_repository_map` | Dictionary mapping the artifact repository type (must be `"pip"`) to a repository name. For the built-in PyPI artifact repository, specify `{"pip": "snowflake.snowpark.pypi_shared_repository"}`. For a private PyPI-compatible repository, use the fully qualified name of a [customer-hosted artifact repository](/developer-guide/udf/python/customer-hosted-python-artifact-repositories) (for example, `{"pip": "my_db.my_schema.my_python_repo"}`).  When specified, pip requirements are installed from that repository when the model runs in a warehouse and when Snowflake builds the container image for SPCS online or batch inference. See [Use a private PyPI artifact repository](#label-snowpark-model-registry-private-pypi).  Copy code  ``` mv = reg.log_model(     clf,     model_name="my_model",     artifact_repository_map={         "pip": "snowflake.snowpark.pypi_shared_repository"     },     pip_requirements=['scikit-learn'],     sample_input_data=train_features, ) ``` |
| `resource_constraint` | Dictionary mapping of warehouse resource constraint keys and values, e.g. {“architecture”: “x86”}. This can be used to ensure the model runs in a warehouse with the necessary architecture. |
| `target_platforms` | List of target platforms to run the model. The only acceptable inputs are a combination of `"WAREHOUSE"` and `"SNOWPARK_CONTAINER_SERVICES"`, or a target platform constant. If `WAREHOUSE` is specified in `target_platforms`, and the model is not runnable in the warehouse (due to dependencies, gpu requirement, model size etc), `log_model()` fails. Default value in [Container Runtime](/developer-guide/snowflake-ml/container-runtime-ml) is `["SNOWPARK_CONTAINER_SERVICES"]` and both elsewhere. For partitioned models, the value must be `["WAREHOUSE"]` or `snowflake.ml.model.target_platform.WAREHOUSE_ONLY`. |
| `python_version` | The version of Python under which the model will run. Defaults to `None`, which designates the latest version available in the warehouse. |
| `sample_input_data` | A DataFrame that contains sample input data. The feature names required by the model and their types are extracted from this DataFrame. Either this argument or `signatures` must be provided for all models except Snowpark ML and MLFlow models and Hugging Face pipelines. |
| `signatures` | Model method signatures as a mapping from target method name to signatures of input and output. Either this argument or `sample_input_data` must be provided for all models except Snowpark ML and MLFlow models and Hugging Face pipelines. |
| `task` | The task defining the problem that the model is meant to solve. If left unspecified, Snowflake makes a best effort to infer the model task from the model class. If the model class can’t be inferred, the model task is set to `type_hints.Task.UNKNOWN`. You must set this parameter to use [ML Observability](/developer-guide/snowflake-ml/model-registry/model-observability).  It helps us identify which monitoring metrics are relevant to your model.  Valid values:   - `snowflake.ml.model.task.Task.TABULAR_BINARY_CLASSIFICATION` - `snowflake.ml.model.task.Task.TABULAR_REGRESSION` - `snowflake.ml.model.task.Task.TABULAR_MULTI_CLASSIFICATION` |
| `user_files` | A dictionary mapping stage subdirectory path to a list of local filepaths. Filepaths may use *?* and \*\*\* wildcards. For example, *{“subdir”: [“/path/to/my\_file.json”]}* will upload *my\_file.json* along with model files into the *subdir* stage subdirectory.  For snowflake-ml-python versions >=1.7.3 and <1.8.1, the user must set the following flag for user files to be included:  Copy code  ``` from snowflake.ml.model._model_composer.model_manifest import (     model_manifest ) model_manifest.ModelManifest._ENABLE_USER_FILES = True ``` |

Expand

Show lessSee more

`log_model` returns a `snowflake.ml.model.ModelVersion` object, which represents the version of the model
that was added to the registry.

After registration, the model itself cannot be modified (although you can change its metadata). To delete a model and all
its versions, use the registry’s [delete\_model](#label-snowpark-model-registry-deleting) method.

## Working with dependencies and target platforms

| **target\_platforms** | **Model Types** | **Default behavior of** *log\_model()* | **Other options** |
| --- | --- | --- | --- |
| *[“SNOWPARK\_CONTAINER\_SERVICES”]*  *snowflake.ml.model.target\_platform.SNOWPARK\_CONTAINER\_SERVICES\_ONLY*  (default in Container runtime) | Built-in model type | - *pip\_requirements* are automatically populated. - Package versions are picked up automatically from the   environment. - The model will not be runnable in *WAREHOUSE*. | - Users can override dependencies by specifying *conda\_dependencies* and/or *pip\_requirements*. - To install pip packages from a private or built-in PyPI repository, set *artifact\_repository\_map*. See [Use a private PyPI artifact repository](#label-snowpark-model-registry-private-pypi). |
| Custom Model | - The model will not be runnable in *WAREHOUSE*. - Users must provide all dependencies in   either of *conda\_dependencies* and *pip\_requirements*. | - To install pip packages from a private or built-in PyPI repository, set *artifact\_repository\_map*. See [Use a private PyPI artifact repository](#label-snowpark-model-registry-private-pypi). |
| *[“WAREHOUSE”]*  *snowflake.ml.model.target\_platform.WAREHOUSE\_ONLY*  (partitioned models) | Built-in model type | - *conda\_dependencies* are automatically populated. - Package versions are picked up automatically from the   environment. - If the model is not runnable in *WAREHOUSE*, *log\_model()*   will fail. | - Users can override dependencies by specifying *conda\_dependencies* and/or *pip\_requirements*. - To use a PyPI repository in the warehouse or when deploying to SPCS, use Artifact Repository. See [Use a private PyPI artifact repository](#label-snowpark-model-registry-private-pypi). |
| Custom Model | - If the model is not runnable in *WAREHOUSE*, *log\_model()*   will fail. - Users must provide all the dependencies in   *conda\_dependencies* and/or *pip\_requirements*. | - To use a PyPI repository in the warehouse or when deploying to SPCS, use Artifact Repository. See [Use a private PyPI artifact repository](#label-snowpark-model-registry-private-pypi). |
| *[“WAREHOUSE”, “SNOWPARK\_CONTAINER\_SERVICES”]*  *snowflake.ml.model.target\_platform.BOTH\_WAREHOUSE\_AND\_SNOWPARK\_CONTAINER\_SERVICES*  (default everywhere except in Container runtime) | Built-in model type | - *conda\_dependencies* are automatically populated. - Package versions are picked up automatically from the   environment. - If the model is not runnable in *WAREHOUSE*, *log\_model()*   will fail. | - Users can override dependencies by specifying *conda\_dependencies* and/or *pip\_requirements*. - To use a PyPI repository in the warehouse or when deploying to SPCS, use Artifact Repository. See [Use a private PyPI artifact repository](#label-snowpark-model-registry-private-pypi). |
| Custom Model | - If the model is not runnable in *WAREHOUSE*, *log\_model()*   will fail. - Users must provide all the dependencies in   *conda\_dependencies* and/or *pip\_requirements*. | - To use a PyPI repository in the warehouse or when deploying to SPCS, use Artifact Repository. See [Use a private PyPI artifact repository](#label-snowpark-model-registry-private-pypi). |

Expand

Show lessSee more

## Use a private PyPI artifact repository

If the model depends on packages that aren’t on public PyPI (internal libraries, or a governed mirror of PyPI),
point `log_model` at a Snowflake [artifact repository](/developer-guide/udf/python/udf-python-packages). Use the
built-in `snowflake.snowpark.pypi_shared_repository` for public PyPI, or a
[customer-hosted artifact repository](/developer-guide/udf/python/customer-hosted-python-artifact-repositories) for a
private index such as JFrog Artifactory, Nexus, Azure Artifacts, Google Artifact Registry, or AWS CodeArtifact.

To create a private repository object, you configure a secret, an API integration, and an
[`ARTIFACT REPOSITORY`](/sql-reference/sql/create-artifact-repository). For the full procedure, see
[Configure a customer-hosted artifact repository](/developer-guide/udf/python/customer-hosted-python-artifact-repositories#label-customer-hosted-repos-configure).

Snowflake installs those pip packages from the repository when the model runs in a warehouse and when it builds the
container image for [online inference](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api) or
[batch inference jobs](/developer-guide/snowflake-ml/inference/batch-inference-jobs) on Snowpark Container Services.
You don’t pass the repository again to `create_service` or `run_batch`. The mapping is stored with the model version.

The role that logs and deploys the model must be able to use the artifact repository (typically USAGE on a
customer-hosted repository, or the `SNOWFLAKE.PYPI_REPOSITORY_USER` database role for the built-in PyPI repository).

The following example logs a model that depends on an internal package and deploys it for online inference. The same
logged model can also call `run_batch` for batch inference.

Copy code

```
from snowflake.ml.model import target_platform
from snowflake.ml.model.batch import OutputSpec
from snowflake.ml.registry import Registry

reg = Registry(session=session)

mv = reg.log_model(
    model=my_model,
    model_name="internal_scoring_model",
    version_name="v1",
    target_platforms=target_platform.SNOWPARK_CONTAINER_SERVICES_ONLY,
    pip_requirements=["internal-scoring-lib==1.2.3", "scikit-learn"],
    artifact_repository_map={
        "pip": "my_db.my_schema.my_python_repo"
    },
    sample_input_data=train_features,
)

# Online inference
mv.create_service(
    service_name="internal_scoring_service",
    service_compute_pool="my_cpu_pool",
    ingress_enabled=True,
)

# Batch inference on the same model version
job = mv.run_batch(
    compute_pool="my_cpu_pool",
    X=session.table("my_feature_table"),
    output_spec=OutputSpec(stage_location="@my_db.my_schema.my_stage/path/"),
)
```

For a complete online-inference workflow, see
[Use a private PyPI artifact repository](/developer-guide/snowflake-ml/inference/real-time-inference-examples#label-real-time-inference-private-pypi).
If image build fails because a package isn’t found, check the `model-build` logs as described in
[Troubleshooting](/developer-guide/snowflake-ml/inference/real-time-inference-troubleshooting).

## Working with model artifacts

After a model has been logged, its artifacts (the files backing the model, including its serialized Python objects and
various metadata files such as its manifest) are available on an internal stage. Artifacts cannot be modified, but you
can view or download the artifacts of models you own.

Note

Having the USAGE privilege on a model does not allow you to access its artifacts; ownership is required.

You can access model artifacts from a stage using, for example, the [GET command](/sql-reference/sql/get)
or its equivalent in Snowpark Python,
[FileOperation.get](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.FileOperation.get).

However, you cannot address model artifacts using the usual stage path syntax. Instead, use a `snow://` URL, a more
general way to specify the location of objects in Snowflake. For example, a version inside a model can be specified by a
URL of the form `snow://model/<model_name>/versions/<version_name>/`.

Knowing the of name of the model and the version you want, you can use the
[LIST command](/sql-reference/sql/list) to view the artifacts of the model as follows:

Copy code

```
LIST 'snow://model/my_model/versions/V3/';
```

The output resembles:

```
name                                      size                  md5                      last_modified
versions/V3/MANIFEST.yml           30639    2f6186fb8f7d06e737a4dfcdab8b1350        Thu, 18 Jan 2024 09:24:37 GMT
versions/V3/functions/apply.py      2249    e9df6db11894026ee137589a9b92c95d        Thu, 18 Jan 2024 09:24:37 GMT
versions/V3/functions/predict.py    2251    132699b4be39cc0863c6575b18127f26        Thu, 18 Jan 2024 09:24:37 GMT
versions/V3/model.zip             721663    e92814d653cecf576f97befd6836a3c6        Thu, 18 Jan 2024 09:24:37 GMT
versions/V3/model/env/conda.yml          332        1574be90b7673a8439711471d58ec746        Thu, 18 Jan 2024 09:24:37 GMT
versions/V3/model/model.yaml       25718    33e3d9007f749bb2e98f19af2a57a80b        Thu, 18 Jan 2024 09:24:37 GMT
```

To retrieve one of these artifacts, use the SQL GET command:

Copy code

```
GET 'snow://model/model_my_model/versions/V3/MANIFEST.yml' file::///tmp/my_model/
```

Or the equivalent with Snowpark Python:

Copy code

```
session.file.get('snow://model/my_model/versions/V3/MANIFEST.yml', 'model_artifacts')
```

Note

The names and organization of a model’s artifacts can vary depending on the type of the model and might change.
The preceding example artifact list is intended to be illustrative, not authoritative.

## Deleting models

Use the registry’s `delete_model` method to delete a model and all its versions:

Copy code

```
reg.delete_model("mymodel")
```

Tip

You can also delete models in SQL using [DROP MODEL](/sql-reference/sql/drop-model).

## Getting models from the registry

To get information about each model, use the `show_models` method:

Copy code

```
model_df = reg.show_models()
```

Tip

In SQL, use [SHOW MODELS](/sql-reference/sql/show-models) to get a list of models.

The result of `show_models` is a pandas DataFrame. The available columns are listed here:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the model was created. |
| `name` | Name of the model. |
| `database_name` | Database in which the model is stored. |
| `schema_name` | Schema in which the model is stored. |
| `owner` | Role that owns the model. |
| `comment` | Comment for the model. |
| `versions` | JSON array listing versions of the model. |
| `default_version_name` | Version of the model used when referring to the model without a version. |

Expand

Show lessSee more

To get a list of the models in the registry instead, each as a `Model` instance, use the `models` method:

Copy code

```
model_list = reg.models()
```

To get a reference to a specific model from the registry by name, use the registry’s `get_model` method:

Copy code

```
m = reg.get_model("MyModel")
```

Note

`Model` instances are not copies of the original logged Python model object; they are references to the underlying
model object in the registry.

After you have a reference to a model, either one from the list returned by the `models` method or one retrieved using
`get_model`, you can work with [its metadata](#label-snowpark-model-registry-model-metadata) and
[its versions](#label-snowpark-model-registry-model-versions).

## Viewing and updating a model’s metadata

You can view and update a model’s metadata attributes in the registry, including its name, comment, tags, and metrics.

### Retrieving and updating comments

Use the model’s `comment` attribute to retrieve and update the model’s comment:

Copy code

```
print(m.comment)
m.comment = "A better description than the one I provided originally"
```

Note

The `description` attribute is a synonym for `comment`. The previous code can also be written this way:

Copy code

```
print(m.description)
m.description = "A better description than the one I provided originally"
```

Tip

You can also set a model’s comment in SQL by using [ALTER MODEL](/sql-reference/sql/alter-model).

### Retrieving and updating tags

Tags are metadata used to record a model’s purpose, algorithm, training data set, lifecycle stage, or other information
you choose. You can set tags when the model is registered or at any time afterward. You can also update the values of
existing tags or remove tags entirely.

Note

You must define the names of all tags (and potentially their possible values) first by using CREATE TAG. See
[Introduction to object tagging](/user-guide/object-tagging/introduction).

To get all of a model’s tags as a Python dictionary, use `show_tags`:

Copy code

```
print(m.show_tags())
```

To add a new tag or change the value of an existing tag, use `set_tag`:

Copy code

```
m.set_tag("live_version", "v1")
```

To retrieve the value of a tag, use `get_tag`:

Copy code

```
m.get_tag("live_version")
```

To remove a tag, use `unset_tag`:

Copy code

```
m.unset_tag("live_version")
```

Tip

You can also set a model’s comment in SQL by using [ALTER MODEL](/sql-reference/sql/alter-model).

### Renaming a model

Use the `rename` method to rename or move a model. Specify a fully qualified name as the new name to move the model to
a different database or schema.

Copy code

```
m.rename("MY_MODEL_TOO")
```

Tip

You can also rename a model in SQL using [ALTER MODEL](/sql-reference/sql/alter-model).

## Working with model versions

A model can have unlimited versions, each identified by a string. You can use any version naming convention that you
like. Logging a model actually logs a *specific version* of the model. To log additional versions of a model, call
`log_model` again with the same `model_name` but a different `version_name`.

Tip

In SQL, use [SHOW VERSIONS IN MODEL](/sql-reference/sql/show-versions-in-model) to see the versions of a model.

A version of a model is represented by an instance of the `snowflake.ml.model.ModelVersion` class.

To get a list of all the versions of a model, call the model object’s `versions` method. The result is a list of
`ModelVersion` instances:

Copy code

```
version_list = m.versions()
```

To get information about each model as a DataFrame instead, call the model’s `show_versions` method:

Copy code

```
version_df = m.show_versions()
```

The resulting DataFrame contains the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the model version was created. |
| `name` | Name of the version. |
| `database_name` | Database in which the version is stored. |
| `schema_name` | Schema in which the version is stored. |
| `model_name` | Name of the model that this version belongs to. |
| `is_default_version` | Boolean value indicating whether this version is the model’s default version. |
| `functions` | JSON array of the names of the functions available in this version. |
| `metadata` | JSON object containing metadata as key-value pairs (`{}` if no metadata is specified). |
| `user_data` | JSON object from the `user_data` section of the model definition manifest (`{}` if no user data is specified). |

Expand

Show lessSee more

### Deleting model versions

You can delete a model version by using the model’s `delete_version` method:

Copy code

```
m.delete_version("rc1")
```

Tip

You can also delete a model version in SQL by using [ALTER MODEL … DROP VERSION](/sql-reference/sql/alter-model-drop-version).

### Default version

A version of a model can be designated as the default model. Retrieve or set the model’s `default` attribute to obtain
the current default version (as a `ModelVersion` object) or to change it (using a string):

Copy code

```
default_version = m.default
m.default = "v2"
```

Tip

In SQL, use [ALTER MODEL](/sql-reference/sql/alter-model) to set the default version.

### Model version aliases

You can assign an alias to a model version by using the SQL [ALTER MODEL](/sql-reference/sql/alter-model) command.
You can use an alias wherever a version name is required, such as when getting a reference to a model version, in Python
or in SQL. A given alias can be assigned to only one model version at a time.

In addition to aliases you create, the following system aliases are available in all models:

- `DEFAULT` refers to the default version of the model.
- `FIRST` refers to the oldest version of the model by creation time.
- `LAST` refers to the newest version of the model by creation time.

Alias names you create must not be the same as any existing version name or alias in the model, including system aliases.

### Getting a reference to a model version

To get a reference to a specific version of a model as a `ModelVersion` instance, use the model’s `version` method.
Use the model’s `default` attribute to get the default version of the model:

Copy code

```
m = reg.get_model("MyModel")

mv = m.version("v1")
mv = m.default
```

After you have a reference to a specific version of a model (such as the variable `mv` in this example), you can
retrieve or update its comments or metrics and call the model’s methods (or functions) as shown in the following sections.

### Retrieving and updating comments

As with models, model versions can have comments, which can be accessed and set via the model version’s `comment` or
`description` attribute:

Copy code

```
print(mv.comment)
print(mv.description)

mv.comment = "A model version comment"
mv.description = "Same as setting the comment"
```

Tip

You can also change a model version’s comment in SQL by using [ALTER MODEL … MODIFY VERSION](/sql-reference/sql/alter-model-modify-version).

### Retrieving and updating metrics

Metrics are key-value pairs used to track prediction accuracy and other model version characteristics. You can set
metrics when creating a model version or set them using the `set_metric` method. A metric value can be any Python
object that can be serialized to JSON, including numbers, strings, lists, and dictionaries. Unlike tags, metric names
and possible values do not need to be defined in advance.

A test accuracy metric might be generated using sklearn’s `accuracy_score`:

Copy code

```
from sklearn import metrics

test_accuracy = metrics.accuracy_score(test_labels, prediction)
```

The confusion matrix can be generated similarly using sklearn:

Copy code

```
test_confusion_matrix = metrics.confusion_matrix(test_labels, prediction)
```

Then you can set these values as metrics:

Copy code

```
# scalar metric
mv.set_metric("test_accuracy", test_accuracy)

# hierarchical (dictionary) metric
mv.set_metric("evaluation_info", {"dataset_used": "my_dataset", "accuracy": test_accuracy, "f1_score": f1_score})

# multivalent (matrix) metric
mv.set_metric("confusion_matrix", test_confusion_matrix)
```

To retrieve a model version’s metrics as a Python dictionary, use `show_metrics`:

Copy code

```
metrics = mv.show_metrics()
```

To delete a metric, call `delete_metric`:

Copy code

```
mv.delete_metric("test_accuracy")
```

Tip

You can also modify a model version’s metrics (which are stored as metadata) in SQL by using
[ALTER MODEL … MODIFY VERSION](/sql-reference/sql/alter-model-modify-version).

### Retrieving model explanations

The model registry can explain a model’s results, telling you which input features contribute most to predictions, by calculating
[Shapley values](https://towardsdatascience.com/the-shapley-value-for-ml-models-f1100bff78d1). This preview feature is available by default in all
model views created in Snowflake 8.31 and later through the underlying model’s `explain` method. You can call `explain` from SQL or via a model view’s
`run` method in Python.

For details on this feature, see [Model Explainability](/developer-guide/snowflake-ml/model-registry/model-explainability).

### Exporting a model version

Use `mv.export` to export a model’s files to a local directory; the directory is created if it does not exist:

Copy code

```
mv.export("~/mymodel/")
```

By default, the exported files include the code, the environment to load the model, and model weights. To also
export the files needed to run the model in a warehouse, specify `export_mode = ExportMode.FULL`:

Copy code

```
mv.export("~/mymodel/", export_mode=ExportMode.FULL)
```

### Loading a model version

Use `mv.load` to load the original Python model object that was originally added to the registry. You can then
use the model for inference just as though you had defined it in your Python code:

Copy code

```
clf = mv.load()
```

To ensure proper functionality of a model loaded from the registry, the target Python environment (that is, the
versions of the Python interpreter and of all libraries) should be identical to the environment from which the model
was logged. Specify `force=True` in the `load` call to force the model to be loaded even if the environment is
different.

Tip

To make sure your environment is the same as the one where the model is hosted, download a copy of the conda environment
from the model registry:

Copy code

```
conda_env = session.file.get("snow://model/<modelName>/versions/<versionName>/runtimes/python_runtime/env/conda.yml", ".")
open("~/conda.yml", "w").write(conda_env)
```

Then create a new conda environment from this file:

Copy code

```
conda env create --name newenv --file=~/conda.yml
conda activate newenv
```

The optional `options` argument is a dictionary of options for loading the model. Currently, the argument supports
only the `use_gpu` option.

| Option | Type | Description | Default |
| --- | --- | --- | --- |
| `use_gpu` | `bool` | Enables GPU-specific loading logic. | `False` |

Expand

Show lessSee more

The following example illustrates the use of the `options` argument:

Copy code

```
clf = mv.load(options={"use_gpu": True})
```

## Calling model methods

Model versions can have *methods,* which are attached functions that can be executed to perform inference or other model
operations. The versions of a model can have different methods, and the signatures of these methods can also differ.

To call a method of a model version, use `mv.run`, where `mv` is a `ModelVersion` object. Specify the name of the
function to be called and pass a Snowpark or pandas DataFrame that contains the inference data, along with any required
parameters. The method is executed in a Snowflake warehouse.

The return value of the method is a Snowpark or pandas DataFrame, matching the type of DataFrame passed in.
Snowpark DataFrames are evaluated lazily, so the method is run only when the DataFrame’s `collect`, `show`,
or `to_pandas` method is called.

Note

Invoking a method runs it in the warehouse specified in the session you’re using to connect to the registry.
See [Specifying a Warehouse](/developer-guide/snowflake-ml/snowpark-ml#label-snowpark-ml-specify-warehouse).

The following example illustrates running the `predict` method of a model. This model’s `predict` method does not
require any parameters besides the inference data (`test_features` here). If it did, they would be passed as
additional arguments after the inference data.

Copy code

```
remote_prediction = mv.run(test_features, function_name="predict")
remote_prediction.show()   # assuming test_features is Snowpark DataFrame
```

To see what methods can be called on a given model, call `mv.show_functions`. The return value of this method is a
list of `ModelFunctionInfo` objects. Each of these objects includes the following attributes:

- `name`: The name of the function that can be called from Python or SQL.
- `target_method`: The name of the Python method in the original logged model.

Tip

You can also call model methods in SQL. See [Inference from SQL](/developer-guide/snowflake-ml/inference/native-batch-inference-sql).

## Sharing models

Models can both be shared and replicated. The following privileges are grantable to a shared model:

- USAGE: Allows the grantee to use the model for warehouse inference without being able to see any of its internals.
- READ: Allows the grantee to use the model for SPCS inference and also see its metadata. Metadata includes, but isn’t limited to, comments, tags, and metrics.

## Cost considerations

Using the Snowflake Model Registry incurs standard Snowflake consumption-based costs. These include:

- Cost of storing model artifacts, metadata, and functions. For general information about storage costs, see [Exploring storage cost](/user-guide/cost-exploring-data-storage).
- Cost of copying files between stages to Snowflake. See [COPY FILES](/sql-reference/sql/copy-files).
- Cost of serverless model object operations through the Snowsight UI or the SQL or Python interface, such as
  showing models and model versions and altering model comments, tags, and metrics.
- Warehouse compute costs, which vary depending on the type of model and the quantity of data used in inference.
  For general information about Snowflake compute costs, see [Understanding compute cost](/user-guide/cost-understanding-compute).
  Warehouse compute costs are incurred for:
  - Model and version creation operations
  - Invoking a model’s methods

### Monitoring model serving costs

To view estimated credit consumption for model serving (inference) workloads, whether run through a warehouse or through
Snowpark Container Services, use the [MODEL\_SERVING\_USAGE\_HISTORY view](/sql-reference/account-usage/model_serving_usage_history). For example:

Copy code

```
SELECT *
  FROM SNOWFLAKE.ACCOUNT_USAGE.MODEL_SERVING_USAGE_HISTORY;
```
