# Example workflows

This page provides example workflows for deploying machine learning models for real-time inference using Snowpark Container Services (SPCS). Each example demonstrates the complete lifecycle from model registration to deployment and inference.

This includes:

- How to create services, make predictions, and access models via HTTP endpoints.
- How to use different model architectures (XGBoost, Hugging Face transformers, PyTorch) and compute options (CPU and GPU).
- How to install model dependencies from a private PyPI artifact repository.

## Deploy an XGBoost model for CPU-powered inference

The following code:

> - Deploys an XGBoost model for inference in SPCS
> - Uses the deployed model for inference.

Copy code

```
from snowflake.ml.registry import registry
from snowflake.ml.utils.connection_params import SnowflakeLoginOptions
from snowflake.snowpark import Session

from xgboost import XGBRegressor

# your model training code here output of which is a trained xgb_model

# Open model registry
reg = registry.Registry(session=session, database_name='my_registry_db', schema_name='my_registry_schema')

# Log the model in Snowflake Model Registry
model_ref = reg.log_model(
    model_name="my_xgb_forecasting_model",
    version_name="v1",
    model=xgb_model,
    conda_dependencies=["scikit-learn","xgboost"],
    sample_input_data=pandas_test_df,
    comment="XGBoost model for forecasting customer demand"
)

# Deploy the model to SPCS
model_ref.create_service(
    service_name="forecast_model_service",
    service_compute_pool="my_cpu_pool",
    ingress_enabled=True)

# See all services running a model
model_ref.list_services()

# Run on SPCS
model_ref.run(pandas_test_df, function_name="predict", service_name="forecast_model_service")

# Delete the service
model_ref.delete_service("forecast_model_service")
```

### Calling via HTTP (External Application)

Since this model has ingress enabled (`ingress_enabled=True`), you can call its public HTTP endpoint. The following example uses a PAT stored in the environment variable `PAT_TOKEN` to authenticate with a public Snowflake endpoint:

Copy code

```
import os
import json
import numpy as np
from pprint import pprint
import requests

def get_headers(pat_token):
    headers = {'Authorization': f'Snowflake Token="{pat_token}"'}
    return headers

headers = get_headers(os.getenv("PAT_TOKEN"))

# Put the endpoint url with method name `predict`
# The endpoint url can be found with `show endpoints in service <service_name>`.
URL = 'https://<random_str>-<organization>-<account>.snowflakecomputing.app/predict'

# Prepare data to be sent
data = {"data": np.column_stack([range(pandas_test_df.shape[0]), pandas_test_df.values]).tolist()}

# Send over HTTP
def send_request(data: dict):
    output = requests.post(URL, json=data, headers=headers)
    assert (output.status_code == 200), f"Failed to get response from the service. Status code: {output.status_code}"
    return output.content

# Test
results = send_request(data=data)
print(json.loads(results))
```

## Deploy a Hugging Face sentence transformer for GPU-powered inference

The following code trains and deploys a Hugging Face sentence transformer, including an HTTP endpoint.

This example requires the `sentence-transformers` package, a GPU compute pool and an image repository.

Copy code

```
from snowflake.ml.registry import registry
from snowflake.ml.utils.connection_params import SnowflakeLoginOptions
from snowflake.snowpark import Session
from sentence_transformers import SentenceTransformer

session = Session.builder.configs(SnowflakeLoginOptions("connection_name")).create()
reg = registry.Registry(session=session, database_name='my_registry_db', schema_name='my_registry_schema')

# Take an example sentence transformer from HF
embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Have some sample input data
input_data = [
    "This is the first sentence.",
    "Here's another sentence for testing.",
    "The quick brown fox jumps over the lazy dog.",
    "I love coding and programming.",
    "Machine learning is an exciting field.",
    "Python is a popular programming language.",
    "I enjoy working with data.",
    "Deep learning models are powerful.",
    "Natural language processing is fascinating.",
    "I want to improve my NLP skills.",
]

# Log the model with pip dependencies
pip_model = reg.log_model(
    embed_model,
    model_name="sentence_transformer_minilm",
    version_name="pip",
    sample_input_data=input_data,  # Needed for determining signature of the model
    pip_requirements=["sentence-transformers", "torch", "transformers"], # If you want to run this model in the Warehouse, you can use conda_dependencies instead
)

# Force Snowflake to not try to check warehouse
conda_forge_model = reg.log_model(
    embed_model,
    model_name="sentence_transformer_minilm",
    version_name="conda_forge_force",
    sample_input_data=input_data,
    # setting any package from conda-forge is sufficient to know that it can't be run in warehouse
    conda_dependencies=["sentence-transformers", "conda-forge::pytorch", "transformers"]
)

# Deploy the model to SPCS
pip_model.create_service(
    service_name="my_minilm_service",
    service_compute_pool="my_gpu_pool",  # Using GPU_NV_S - smallest GPU node that can run the model
    ingress_enabled=True,
    gpu_requests="1", # Model fits in GPU memory; only needed for GPU pool
    max_instances=4, # 4 instances were able to run 10M inferences from an XS warehouse
)

# See all services running a model
pip_model.list_services()

# Run on SPCS
pip_model.run(input_data, function_name="encode", service_name="my_minilm_service")

# Delete the service
pip_model.delete_service("my_minilm_service")
```

In SQL, you can call the service function as follows:

Copy code

```
SELECT my_minilm_service!encode('This is a test sentence.');
```

Similarly, you can call its HTTP endpoint as follows.

Copy code

```
import json
from pprint import pprint
import requests

# Put the endpoint url with method name `encode`
URL='https://<random_str>-<account>.snowflakecomputing.app/encode'

# Prepare data to be sent
data = {
    'data': []
}
for idx, x in enumerate(input_data):
    data['data'].append([idx, x])

# Send over HTTP
def send_request(data: dict):
    output = requests.post(URL, json=data, headers=headers)
    assert (output.status_code == 200), f"Failed to get response from the service. Status code: {output.status_code}"
    return output.content

# Test
results = send_request(data=data)
pprint(json.loads(results))
```

## Use a private PyPI artifact repository

If the model needs packages that aren’t on public PyPI, log it with `pip_requirements` and
`artifact_repository_map` pointing at a
[customer-hosted artifact repository](/developer-guide/udf/python/customer-hosted-python-artifact-repositories).
Snowflake installs those packages when it builds the inference image. For the logging arguments, see
[Use a private PyPI artifact repository](/developer-guide/snowflake-ml/model-registry/overview#label-snowpark-model-registry-private-pypi).

[Create the artifact repository](/developer-guide/udf/python/customer-hosted-python-artifact-repositories#label-customer-hosted-repos-configure)
first. The following example assumes `my_db.my_schema.my_python_repo` already exists and that your role can use it.

Copy code

```
from snowflake.ml.model import target_platform
from snowflake.ml.registry import Registry

reg = Registry(session=session, database_name="my_registry_db", schema_name="my_registry_schema")

mv = reg.log_model(
    my_model,
    model_name="internal_scoring_model",
    version_name="v1",
    target_platforms=target_platform.SNOWPARK_CONTAINER_SERVICES_ONLY,
    sample_input_data=pandas_test_df,
    pip_requirements=["internal-scoring-lib==1.2.3", "scikit-learn"],
    artifact_repository_map={
        "pip": "my_db.my_schema.my_python_repo"
    },
)

mv.create_service(
    service_name="internal_scoring_service",
    service_compute_pool="my_cpu_pool",
    ingress_enabled=True,
)

mv.run(pandas_test_df, function_name="predict", service_name="internal_scoring_service")
```

The same `artifact_repository_map` applies if you later call `run_batch` on this model version. You don’t pass the
repository to `create_service` or `run_batch`.

## Deploy a PyTorch model for GPU-powered inference

For an example of training and deploying a PyTorch deep learning recommendation model (DLRM) to SPCS for GPU inference, see this [quickstart](https://quickstarts.snowflake.com/guide/snowpark-container-services-model-serving-guide/)

## Deploy a Snowpark ML modeling model

Models developed using Snowpark ML modeling classes cannot be deployed to environments that have a GPU. As a workaround, you can extract the native model and deploy that. For example:

Copy code

```
# Train a model using Snowpark ML
from snowflake.ml.modeling.xgboost import XGBRegressor
regressor = XGBRegressor(...)
regressor.fit(training_df)

# Extract the native model
xgb_model = regressor.to_xgboost()
# Test the model with pandas dataframe
pandas_test_df = test_df.select(['FEATURE1', 'FEATURE2', ...]).to_pandas()
xgb_model.predict(pandas_test_df)

# Log the model in Snowflake Model Registry
mv = reg.log_model(xgb_model,
                   model_name="my_native_xgb_model",
                   sample_input_data=pandas_test_df,
                   comment = 'A native XGB model trained from Snowflake Modeling API',
                   )
# Now we should be able to deploy to a GPU compute pool on SPCS
mv.create_service(
    service_name="my_service_gpu",
    service_compute_pool="my_gpu_pool",
    image_repo="my_repo",
    max_instances=1,
    gpu_requests="1",
)
```
