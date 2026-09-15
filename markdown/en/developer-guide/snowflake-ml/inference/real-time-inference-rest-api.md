# Deploy models for real-time inference (REST API)

Note

- Generally available since snowflake-ml-python version 1.25.0.

Use real-time inference for interactive workflows that require low latency. You can deploy any model from the
[Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview) as a managed service with a dedicated HTTP endpoint.
Managed services feature autoscaling and are fully integrated within the Snowflake ecosystem, offering comprehensive observability.

Use online inference for your workflow when:

- Your application requires low latency for immediate responses
- Your model serves as a backend for a user-facing web or mobile application.
- The input to your model can fit within the HTTP payload of the request.
- The service must automatically scale horizontally to handle fluctuating request volumes.

## How it works

Snowflake simplifies the deployment pipeline by hosting your model as an HTTP server within **Snowpark Container Services (SPCS)**. This
architecture enables you to:

- **Abstract complexity:** Deploy sophisticated models without managing Docker images or Kubernetes clusters.
- **Scale performance:** Run large-scale models on distributed GPU clusters for high-performance requirements.
- **Ensure reliability:** Utilize built-in observability, traffic splitting, and shadow/canary deployments for seamless model upgrades.

### Prerequisites

Before you begin, make sure you have the following:

- Version 1.8.0 or later of the snowflake-ml-python Python package.
- A model logged in [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview).
- An understanding of [compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool) and
  related privileges on SPCS.

### Required privileges

Model Serving runs on top of [Snowpark Container Services](/developer-guide/snowpark-container-services/overview).
You need the following privileges to use Model Serving:

- USAGE or OWNERSHIP on the compute pool where the service runs.
  Alternatively, you can use the default System Compute Pools.
- BIND SERVICE ENDPOINT privilege on account to be able to create a public endpoint.
- OWNER or READ privilege on the model.

### Limitations

The following limitations apply to online model serving in Snowpark Container Services.

- Table functions aren’t supported. Your model must NOT have a table function to be deployed to Snowflake.
- Models developed using Snowpark ML modeling classes
  can’t be deployed to environments that have a GPU. As a workaround, you can extract the native model and deploy that. For more information,
  see [Deploy a model for online inference](#label-real-time-inference-deploy-a-model-for-online-inference).

### Deploy a model for online inference

Snowflake ML uses a model version object to create a model service that handles inference requests. To create a model version object, you
can either log a new model version or
obtain a reference to an existing model version.
After you get your model version object, you can use the following Python code to create a model service and deploy that service to SPCS:

Copy code

```
# reg is a snowflake.ml.registry.Registry object
example_mv_object = reg.get_model("mymodel_name").version("version_name") # a snowflake.ml.model.ModelVersion object

example_mv_object.create_service(service_name="myservice",
                  service_compute_pool="my_compute_pool",
                  ingress_enabled=True,
                  gpu_requests=None)
```

`create_service` requires the following arguments:

- service\_name: The name of the service that you’re creating. This name must be unique within your Snowflake account.
- service\_compute\_pool: The name of the compute pool that you’re using to run the model. The compute pool must already exist. If the model
  fits well in System Compute Pools, you can use them
  (`SYSTEM_COMPUTE_POOL_GPU` or `SYSTEM_COMPUTE_POOL_CPU`) too.
- ingress\_enabled: This is required to be True to call online inference from outside of Snowflake.
- `gpu_requests`: A string specifying the number of GPUs. For a model that can be run on either a CPU or multiple GPUs, this argument determines whether the model will be run on the CPU or on the GPUs. If the model is of a known type that can only run on a CPU (such as scikit-learn models), the image build fails if you request GPUs. If you’re deploying a new model, it can take up to 10 minutes to create the service for CPU-powered models and 20 minutes for GPU-powered models. If the compute pool is idle or requires resizing, it might take longer to create the service.

The preceding example only shows the required and most commonly used arguments. For a complete list of arguments, see the
ModelVersion API reference.

## Default service configuration

The server running the model that you’ve deployed uses defaults that work for most use cases:

- *Number of worker threads*: For a CPU-powered model, the number of processes that the server uses is twice the number of CPUs plus one.
  GPU-powered models use one worker process. You can override this using the num\_workers argument in the create\_service call. It is
  **recommended** to specify the smallest GPU node where the model fits into memory. Scale by increasing the number of instances. For example,
  if the model fits in the GPU\_NV\_S (GPU\_NV\_SM on Azure) instance type, use gpu\_requests=1 and scale up by increasing max\_instances. However
  if the smallest available node has 4 GPUs and you only need 2, use `num_workers=2` (that is, gpu available / gpus needed by the
  model).
- *Thread safety*: Some models are not thread-safe. Therefore, the service loads a separate copy of the model for each worker process. This
  can result in resource depletion for large models.
- *Node utilization*: By default, one inference server instance requests the whole node by requesting all the CPU and memory of the node it
  runs on. To customize resource allocation per instance, use arguments like cpu\_requests, memory\_requests, and gpu\_requests.
- *Endpoint*: The inference endpoint is named inference and uses port 5000. These cannot be customized. For optimal resource utilization,
  specify the smallest GPU node that can fit the model into memory. Increase the number of instances to scale to your workload. For example,
  if the model fits in the GPU\_NV\_S (GPU\_NV\_SM on Azure) instance type, use gpu\_requests=1 and scale up by increasing max\_instances.

## Container image build behavior

**The Snowflake conda channel is available only in warehouses and is the only source for warehouse dependencies. By default, conda
dependencies for SPCS models obtain their dependencies from conda-forge.**

Pip packages listed in `pip_requirements` are installed during this image build. To install them from a private
PyPI-compatible index, set `artifact_repository_map` when you [log the model](/developer-guide/snowflake-ml/model-registry/overview#label-snowpark-model-registry-private-pypi).
For a complete example, see [Use a private PyPI artifact repository](/developer-guide/snowflake-ml/inference/real-time-inference-examples#label-real-time-inference-private-pypi).

By default, Snowflake Model Serving builds the container image using the same compute pool that’s used to run the model. The compute pool is
likely overpowered for the process of building images (for example, GPUs are not used in building container images). For the most part,
this won’t significantly impact compute costs. However, if you’re concerned, you can specify a less powerful compute pool to build
images with the image\_build\_compute\_pool argument.

Calling create\_service() multiple times does not trigger a build every time you call it.

However, container images might be rebuilt if Snowflake made updates to the inference service, including fixes for vulnerabilities in
dependent packages. When this happens, create\_service automatically triggers a rebuild of the image.

## User interface

You can manage deployed models in the Model Registry Snowsight UI. For more information, see [Model inference services](/developer-guide/snowflake-ml/model-registry/snowsight-ui#label-model-inference-services).

## Invoking a deployed model

## HTTP endpoints

Every service comes with its internal DNS name. Deploying a service with ingress\_enabled also creates a public HTTP endpoint available
outside of Snowflake. Either endpoint can be used to call a service.

You can find the public HTTP endpoint of a service with ingress enabled using the [SHOW ENDPOINTS](/sql-reference/sql/show-endpoints) command.
The output contains an ingress\_url column, which has an entry of the format *unique-service-id*-*account-id*.snowflakecomputing.app. This is the publicly available HTTP endpoint for your service. For private link users, use privatelink\_ingress\_url instead of ingress\_url.

To get the internal DNS name on Snowflake, use the [DESCRIBE SERVICE](/sql-reference/sql/desc-service) command.
The dns\_name column of output from this command contains a service’s internal DNS name. To find your service’s port, use the SHOW ENDPOINTS
IN SERVICE command. The port or port\_range column contains the port used by a service. You can make internal calls to your service through
the URL http://*dns\_name*:*port*.

To call any particular methods of the model, use the method name as path to the URL (for example,
`https://unique-service-id-account-id.snowflakecomputing.app/method-name` or http://*dns\_name*:*port*/<method-name>). In a URL,
underscores (\_) in the method name are replaced by dashes (-) in the URL. For example, the method name predict\_proba is changed to
predict-proba in the URL.

To simplify things, in Python, the list\_services() API can be called on a ModelVersion object:

Copy code

```
# mv: snowflake.ml.model.ModelVersion
mv.list_services()
```

It outputs both the public endpoint (`inference_endpoint`) and the internal endpoint (`internal_endpoint`).

## Authentication

Snowflake supports multiple authentication protocols.
The simplest of all is to use [Programmatic Access Tokens (PAT)](/user-guide/programmatic-access-tokens)
where the token can be passed simply to the request header as `Authorization: Snowflake Token="your_pat_token"`

Note

All authorization failures such as an incorrect token or lack of network route to the service result in a 404 error. There is no way to distinguish authentication errors from invalid URLs.

## Authorization

By default only service owners can use the endpoint. To allow another role to access the endpoint, service owners can
[grant the service role](/sql-reference/sql/grant-service-role) ALL\_ENDPOINTS\_USAGE.

## Request body (or protocol or data format)

Snowflake supports two types of data formats for REST requests. They are inspired by the Pandas DataFrame, particularly because DataFrames are well
known in the industry and verifiable by customers using simple Python scripts with a Pandas DataFrame.

Tip

**Method-to-URL mapping:** When constructing your request URL, note that underscores (`_`) in your model’s method names are
automatically replaced by dashes (`-`). For example, if your model method is `predict_proba`, the endpoint URL path becomes
`/predict-proba`.

Here are the details about the formats:

1. `dataframe_split` is a compact, index/columns/data representation.

> - A representation that mirrors `pandas_df.to_json(orient="split")`.

1. `dataframe_records` is a key/value (record-oriented) representation.

> - A representation that mirrors `df.to_json(orient="records")`.

It is **recommended** to use `dataframe_split` format. Since `dataframe_records` repeats column names for each row, it typically
produces a larger request body than `dataframe_split`. This can have a performance impact for large batches or frequent calls.

Model endpoints continue to return a **single output format**, regardless of which input format you use.

1. `dataframe_split` **format (Recommended)**

This matches the structure produced by the Pandas “split” orientation. The request body wraps the following structure under a
`dataframe_split` key:

- `index`: A list of row indices.
- `columns`: A list of column names.
- `data`: A list of rows, where each row is a list of values aligned with the columns.

Example `cURL` request:

Copy code

```
curl -X POST "<endpoint_url>" \
  -H 'Authorization: Snowflake Token="<pat_token>"' \
  -H 'Content-Type: application/json' \
  -w "\n\n=== RESULT ===\nHTTP Status: %{http_code}\nTotal Time: %{time_total}s\nConnect Time: %{time_connect}s\nServer Processing: %{time_starttransfer}s\nResponse Size: %{size_download} bytes\nRequest Size: %{size_upload} bytes\n" \
 -d '{
       "dataframe_split": {
         "index": [0, 1],
         "columns": ["customer_id", "age", "monthly_spend"],
         "data": [
            [101, 32, 85.5],
             [102, 45, 120.0]
         ]
       }
     }'
```

1. `dataframe_records` **format**

`dataframe_records` matches the structure produced by **Pandas records orientation**:

- A **list of records**, where each record is a dictionary mapping **column names** to **values**.

The request body wraps this list under the `dataframe_records` key:

Example `cURL` request:

Copy code

```
curl -X POST "<endpoint_url>" \
  -H 'Authorization: Snowflake Token="<pat_token>"' \
  -H 'Content-Type: application/json' \
  -w "\n\n=== RESULT ===\nHTTP Status: %{http_code}\nTotal Time: %{time_total}s\nConnect Time: %{time_connect}s\nServer Processing: %{time_starttransfer}s\nResponse Size: %{size_download} bytes\nRequest Size: %{size_upload} bytes\n" \
 -d '{
       "dataframe_records": [
           {
             "customer_id": 101,
             "age": 32,
             "monthly_spend": 85.5
           },
           {
             "customer_id": 102,
             "age": 45,
             "monthly_spend": 120.0
           }
         ]
     }'
```

## Online feature store integration

Note

This feature is in public preview. For more information about preview features, see [Preview Features](/release-notes/preview-features).

If you are using [online feature store backed by Snowflake Postgres](/developer-guide/snowflake-ml/feature-store/online-feature-store), you can integrate it with real-time inference
for automatic feature lookup. This allows the model service to fetch feature values from a registered feature view
at inference time, reducing the data you need to include in each request.

### Map a feature view to a model method

Use the `feature_sources_per_function` parameter in `create_service()` to map a registered feature view to a model
method. The feature view must be registered with online serving enabled using `OnlineStoreType.POSTGRES`.

Copy code

```
from snowflake.ml.feature_store import FeatureView, OnlineConfig, OnlineStoreType

# Create and register a feature view with Postgres online store
profile_fv = FeatureView(
    name="USER_PROFILE_FEATURES",
    entities=[user_entity],
    feature_df=profile_df,
    timestamp_col="LAST_ACTIVITY_TS",
    refresh_freq="1m",
    online_config=OnlineConfig(
        enable=True,
        target_lag="10s",
        store_type=OnlineStoreType.POSTGRES,
    ),
    desc="User profile features for online inference",
)
registered_fv = fs.register_feature_view(profile_fv, version="V1")

# Deploy model with feature retrieval
mv.create_service(
    service_name="myservice",
    service_compute_pool="my_compute_pool",
    ingress_enabled=True,
    feature_sources_per_function={"predict": [registered_fv]},
)
```

The `feature_sources_per_function` parameter maps method names (such as `"predict"`) to a list of registered
`FeatureView` objects. Currently, only one feature view per function is supported.

### Feature validation

When you configure feature retrieval, the system validates which features can be fetched from the feature view by
comparing the feature view’s columns against the model’s signature. Only features that exist in both the feature view
and the model signature are eligible for automatic lookup.

### Inference requests with feature lookup

To trigger feature lookup at inference time, pass the entity IDs (the join keys defined in the feature view’s entity)
in your request. Use the same `dataframe_split` or `dataframe_records` format as regular inference requests.

For example, if your feature view uses `USER_ID` as the entity key, include only the entity ID in your request:

Copy code

```
# Request with only entity IDs - features are fetched from feature view
payload = {
    "dataframe_split": {
        "index": [0, 1],
        "columns": ["USER_ID"],
        "data": [
            ["user_123"],
            ["user_456"]
        ]
    }
}

response = requests.post(
    ENDPOINT_URL,
    headers=HEADERS,
    json=payload,
    timeout=30,
)
```

The model service automatically fetches the missing feature columns from the feature view before invoking the model.

### Override feature values

You can override specific feature values by including them in your request. When you pass a feature value in the
request, that value is used instead of fetching it from the feature view.

Copy code

```
# Request with entity ID and an overridden feature value
payload = {
    "dataframe_split": {
        "index": [0],
        "columns": ["USER_ID", "MONTHLY_SPEND"],
        "data": [
            ["user_123", 500.0]
        ]
    }
}
```

In this example, `MONTHLY_SPEND` is provided in the request and won’t be fetched from the feature view. Any other
features required by the model that aren’t in the request are still fetched from the feature view.

To skip feature view lookup entirely, pass all the features required by the model in your request.

## Passing parameters

If the model’s signature includes parameters defined with
[ParamSpec](/developer-guide/snowflake-ml/model-registry/model-signature), you can pass parameter values by
including a top-level `params` key in the JSON request body alongside `dataframe_split` or
`dataframe_records`. Only include the parameters you want to override; unspecified parameters use their default
values from the signature.

Example `cURL` request with parameters:

Copy code

```
curl -X POST "<endpoint_url>/predict" \
  -H 'Authorization: Snowflake Token="<pat_token>"' \
  -H 'Content-Type: application/json' \
  -d '{
        "dataframe_split": {
            "index": [0],
            "columns": ["input_text"],
            "data": [["Hello, world!"]]
        },
        "params": {"temperature": 0.9, "max_tokens": 512}
      }'
```

The `params` key works the same way with the `dataframe_records` format:

Copy code

```
curl -X POST "<endpoint_url>/predict" \
  -H 'Authorization: Snowflake Token="<pat_token>"' \
  -H 'Content-Type: application/json' \
  -d '{
        "dataframe_records": [
            {"input_text": "Hello, world!"}
        ],
        "params": {"temperature": 0.9, "max_tokens": 512}
      }'
```

## Python examples

1. `dataframe_split` format

Snowflake recommends generating the payload by using **Pandas JSON serialization**, and then deserializing with `json.loads` before
sending the request. This ensures that data types are handled consistently.

Copy code

```
import json
import pandas as pd
import requests

# Example DataFrame
df = pd.DataFrame(
    {
        "customer_id": [101, 102],
        "age": [32, 45],
        "monthly_spend": [85.5, 120.0],
    }
)

ENDPOINT_URL = "<your endpoint URL>"
HEADERS = {
    "Authorization": f'Snowflake Token="{PAT}"',
    "Content-Type": "application/json"
}

# Use Pandas to generate the JSON, then load it back to a Python dict
split_obj = json.loads(df.to_json(orient="split"))

payload = {
    "dataframe_split": split_obj
}

response = requests.post(
    ENDPOINT_URL,
    headers=HEADERS,
    json=payload,
    timeout=30,
)

result = response.json()
```

Key points:

- Use pd.DataFrame.to\_json (for example, `df.to_json(orient="split")`) to correctly handle types such as timestamps, floats, nulls, categoricals,
  and so on, which the native json serializer is unfamiliar with.
- `json.loads(...)` converts the JSON string to a Python dictionary so we can properly construct the payload.
- `requests.post(..., json=payload)` serializes the dictionary back to JSON for the HTTP request.

To include parameters, add a `params` key to the payload dictionary:

Copy code

```
payload = {
    "dataframe_split": split_obj,
    "params": {"temperature": 0.9, "max_tokens": 512}
}
```

1. `dataframe_records` format

As with `dataframe_split`, use Pandas JSON serialization and `json.loads`:

Copy code

```
import json
import pandas as pd
import requests

df = pd.DataFrame(
    {
        "customer_id": [101, 102],
        "age": [32, 45],
        "monthly_spend": [85.5, 120.0],
    }
)

ENDPOINT_URL = "<your endpoint invoke URL>"
HEADERS = {
    "Authorization": "Bearer <your token>",
    "Content-Type": "application/json",
}

records_obj = json.loads(df.to_json(orient="records"))

payload = {
    "dataframe_records": records_obj
}

response = requests.post(
    ENDPOINT_URL,
    headers=HEADERS,
    json=payload,
    timeout=30,
)

response.raise_for_status()
result = response.json()
```

## Next steps

Explore these detailed guides to optimize and manage your inference services:

- [Example workflows](/developer-guide/snowflake-ml/inference/real-time-inference-examples): See end-to-end code for XGBoost (CPU), Hugging Face (GPU), and PyTorch models.
- **Service Management & Scaling:** Learn about autoscaling, manual suspension, and hardware configuration.
- **Stable Endpoints & API Reference:** Deep dive into the Snowflake Gateway, authentication, and data protocols
  (`dataframe_split`).
- **Auto-capture Inference Logs:** Set up automated logging for model monitoring.
- **Gateway Monitoring & A/B Testing:** Monitor gateway-routed services and compare model services in A/B tests and shadow testing.
- **Troubleshooting:** Common fixes for package conflicts, OOM errors, and build failures.
