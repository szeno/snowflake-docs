# Snowflake-provided models

Snowflake provides a curated set of third-party, open models as model objects in the `SNOWFLAKE.MODELS` schema. These
models are already logged in the Snowflake Model Registry, so you don’t need to download weights from Hugging Face, set
up an external access integration, or call `log_model`. Get a reference to the model and deploy it as a
[Snowpark Container Services (SPCS)](/developer-guide/snowpark-container-services/overview) inference service in your own
database and schema.

Note

Snowflake-provided models are available for accounts on Amazon Web Services (AWS) and Google Cloud Platform (GCP). Support for Microsoft Azure isn’t available yet.

Model availability and specifications are subject to change.

## Available models

The following models are available in the `SNOWFLAKE.MODELS` schema. Select **Copy ID** on a card to copy the
model object name, and use that name with `Registry.get_model`.

### Qwen3.8-27B

`SNOWFLAKE.MODELS."QWEN3.8-27B"`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3.8-27B/blob/main/LICENSE)

Source: [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)

Task

Text-Generation, Image-Text-To-Text

Context

256K max

27B parameters

To list the models in the schema that your current role can access, run the following command:

Copy code

```
SHOW MODELS IN SCHEMA SNOWFLAKE.MODELS;
```

## Example

This example deploys a model from the catalog and sends it one prompt. Replace the placeholders with values for the
model you selected:

- `<model_name>`: the model object name from the card, without the `SNOWFLAKE.MODELS.` prefix. Quote the name when it
  contains a character such as a period.
- `<service_name>`: a fully qualified service name in a database and schema that you own. The service can’t be created
  in the `SNOWFLAKE` database.

Copy code

```
from snowflake.ml.registry import Registry

reg = Registry(session=session, database_name="SNOWFLAKE", schema_name="MODELS")
mv = reg.get_model('"<model_name>"').default

mv.create_service(
    service_name="<service_name>",
    service_compute_pool="MY_GPU_POOL",
    ingress_enabled=True,
)
```

Copy code

```
SELECT AI_COMPLETE('<service_name>', 'Summarize the benefits of columnar storage.');
```

Sampling parameters, such as `temperature` and `top_p`, depend on the model. Use the values published with the source
model linked from the card. The sections below cover prerequisites, service options, and other ways to call the service.

## Prerequisites

Before you deploy a Snowflake-provided model, make sure you have the following:

- An account on Amazon Web Services (AWS) or Google Cloud Platform (GCP). Microsoft Azure isn’t supported yet.
- Version 1.43.0 or later of the `snowflake-ml-python` package.
- A GPU [compute pool](/developer-guide/snowpark-container-services/working-with-compute-pool) that can hold the model.
- A role with the following privileges:
  - USAGE on the model object in `SNOWFLAKE.MODELS`.
  - USAGE or OWNERSHIP on the compute pool.
  - CREATE SERVICE on the schema where you create the inference service.
  - BIND SERVICE ENDPOINT on the account, if you enable ingress for the service.

## Deploy a model to SPCS

The [example](#example) creates the service with Snowflake’s default vLLM arguments. Those arguments balance throughput
and latency, so `inference_engine_options` is optional. Creating a GPU service can take 20 minutes or more, especially
if the compute pool must start or resize.

To change that balance, pass `engine_args_override` with the vLLM arguments you want. `mv` is the model version from
the [example](#example). The following call lowers the maximum context length so the service uses less GPU memory:

Copy code

```
mv.create_service(
    service_name="<service_name>",
    service_compute_pool="MY_GPU_POOL",
    ingress_enabled=True,
    inference_engine_options={
        "engine_args_override": ["--max-model-len=32768"],
    },
)
```

Larger values of `--max-model-len` require more GPU memory.

For the complete list of `create_service` arguments and default service behavior, see
[Deploy models for real-time inference (REST API)](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api).

## Run inference

After the service is running, you can call it from SQL, the Snowflake ML Python API, or an OpenAI-compatible client.

### Use AI\_COMPLETE

Pass the fully qualified service name as the `model` argument to AI\_COMPLETE:

Copy code

```
SELECT AI_COMPLETE(
  model            => '<service_name>',
  prompt           => 'Write a Python function that merges two sorted lists.',
  model_parameters => {
    'temperature': 0.7,
    'top_p':       0.8,
    'max_tokens':  1024
  }
);
```

When the model accepts image input, you can also pass images from a stage. For more information, see
[Bring-your-own model for AI\_COMPLETE](/developer-guide/snowflake-ml/inference/spcs-ai-complete).

### Use Python

Call `run` on the model version and specify the service name. The input uses OpenAI chat completion request fields:

Copy code

```
import pandas as pd

request = pd.DataFrame.from_records(
    [
        {
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": "Summarize the benefits of columnar storage."}],
                }
            ],
            "max_completion_tokens": 512,
            "temperature": 0.7,
        }
    ]
)

response = mv.run(request, service_name="<service_name>")
```

### Use the OpenAI Python client

The service exposes an OpenAI-compatible chat completions endpoint at `https://<ingress_host>/v1`. Call it with the
OpenAI Python client. Authenticate with a [programmatic access token (PAT)](/user-guide/programmatic-access-tokens) in
`extra_headers`. The client still requires an `api_key` argument. Set it to any non-empty string. The service
authenticates the request with the token in the header.

The ingress host comes from [SHOW ENDPOINTS](/sql-reference/sql/show-endpoints). Resolve it when you call the service,
because the host can change after you suspend and resume the service. For private connectivity, use
`privatelink_ingress_url` instead of `ingress_url`.

Set `model` to `<model_name>`, the model object name without the `SNOWFLAKE.MODELS.` prefix. `GET /v1/models` lists
the names the endpoint accepts.

Copy code

```
import openai

endpoints = session.sql("SHOW ENDPOINTS IN SERVICE <service_name>").collect()
ingress_host = next(
    str(endpoint["ingress_url"])
    for endpoint in endpoints
    if endpoint["ingress_url"] and str(endpoint["ingress_url"]).upper() != "NONE"
)

client = openai.OpenAI(
    base_url=f"https://{ingress_host}/v1",
    api_key="unused",
)

response = client.chat.completions.create(
    model="<model_name>",
    messages=[
        {
            "role": "user",
            "content": "Summarize the benefits of columnar storage.",
        }
    ],
    max_completion_tokens=512,
    temperature=0.7,
    extra_headers={"Authorization": f'Snowflake Token="{pat}"'},
)

print(response.choices[0].message.content)
```

The token’s role needs USAGE on the service. By default, only the service owner can call the endpoint. To allow another
role, grant the service role `ALL_ENDPOINTS_USAGE`. For more information, see
[Authentication](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api#label-real-time-inference-authentication)
and
[Authorization](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api#label-real-time-inference-authorization).

## Manage the service

You manage a service created from a Snowflake-provided model the same way as any other model inference service. You can
suspend it when you aren’t using it, scale it, and drop it. For more information, see
[Service Management & Scaling](/developer-guide/snowflake-ml/inference/service-management).

## Cost considerations

You pay for the SPCS compute pool that runs the inference service, including the time it takes to build the container
image. To control costs, suspend the service or the compute pool when you aren’t using them.

## Model licenses

Snowflake-provided models are third-party models. Your use of each model is subject to the license linked from its card.
