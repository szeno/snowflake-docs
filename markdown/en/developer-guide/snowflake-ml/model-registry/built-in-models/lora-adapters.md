# LoRA adapters

Log a PEFT LoRA adapter as its own Model Registry version, linked to the base model version it was trained on.
Serve many adapters against that base on one GPU vLLM service, and pick which adapter answers each query.

An adapter version stores adapter weights only. The base version still holds the full model.

## Limitations

- Adapters are served on a vLLM service in Snowpark Container Services. They can’t run in a warehouse.
- Only LoRA adapters are supported.
- A service serves adapters for one base model version. To change its adapters, recreate the service.

## Log an adapter

:class:`~snowflake.ml.model.PeftAdapter` takes a `base_model` (`ModelVersion`) and exactly one source:

- `adapter_path`: a local directory.
- `adapter`: an in-memory `peft.PeftModel`. Requires `peft`.
- `adapter_repo`: a Hugging Face Hub repo. Requires `huggingface_hub`. `revision` and `token` (private repos)
  apply only here.

`subfolder` works with `adapter_path` and `adapter_repo`. The source must contain `adapter_config.json`.

Copy code

```
from snowflake.ml.registry import Registry
from snowflake.ml.model import PeftAdapter

reg = Registry(session=session, database_name="ML", schema_name="DEMOS")
base = reg.get_model("LLAMA3_8B").version("V1")

# Local PEFT directory
adapter_mv = reg.log_model(
    PeftAdapter(adapter_path="./example_lora_adapter", base_model=base),
    model_name="SUPPORT_TONE",
    version_name="V1",
)

# In-memory peft.PeftModel
adapter_mv = reg.log_model(
    PeftAdapter(adapter=peft_model, base_model=base),
    model_name="SUPPORT_TONE",
    version_name="V2",
)

# Hugging Face Hub. Use a commit hash as the revision in production.
adapter_mv = reg.log_model(
    PeftAdapter(
        adapter_repo="org/support-lora",
        revision="e1945c40cd546c78e41f1151f4db032b271faeaa",
        base_model=base,
    ),
    model_name="SUPPORT_TONE",
    version_name="V3",
)

# Nested directory in a Hub repo or local tree
adapter_mv = reg.log_model(
    PeftAdapter(
        adapter_repo="org/adapter-lib",
        subfolder="loras/style_v1",
        base_model=base,
    ),
    model_name="STYLE_V1",
    version_name="V1",
)
```

The adapter version uses the same methods and signatures as its base, so do not pass `signatures`,
`sample_input_data`, or `target_platforms` other than `SNOWPARK_CONTAINER_SERVICES`.

Make sure the adapter was trained on the base model version you specify.

### Supported base versions

`base_model` must be a full-weight model version in your account, or a Cortex Base Model version (`CORTEX_BASE`).
For a Cortex Base Model, log adapter versions under your own model.

A full-weight base must have a `model` parameter on `__call__`, which callers use to select an adapter. A Hugging
Face `text-generation` pipeline with a chat template gets this signature by default. Otherwise, pass it when you
log the base:

Copy code

```
from snowflake.ml.model import openai_signatures

base = reg.log_model(
    pipeline,
    model_name="LLAMA3_8B",
    version_name="V1",
    signatures=openai_signatures.OPENAI_CHAT_WITH_PARAMS_SIGNATURE,
)
```

`__call__` then takes:

- Input: `messages`
- Parameters: `temperature`, `max_completion_tokens`, `stop`, `n`, `stream`, `top_p`, `frequency_penalty`,
  `presence_penalty`, `response_format`, and `model` (optional string; omit it to call the base model)

To check an existing version, call `base.show_functions()`. If `__call__` has no `model` parameter, as with
`OPENAI_CHAT_SIGNATURE`, log the model again with `OPENAI_CHAT_WITH_PARAMS_SIGNATURE`.

## View an adapter’s base version

The link between an adapter and its base version is recorded as lineage.

Copy code

```
# Adapter → base version
adapter_mv.lineage(direction="upstream", domain_filter={"model"})

# Base → adapters logged against it (adapters you can't access are omitted)
base.get_adapters()
```

Copy code

```
SELECT *
  FROM TABLE(SNOWFLAKE.CORE.GET_LINEAGE(
    'ML.DEMOS.SUPPORT_TONE',
    'MODEL',
    'UPSTREAM',
    1
  ));
```

If you don’t have a privilege on the linked model, `GET_LINEAGE` shows it as `MASKED`.

## Create a service with adapters

Pass `adapters` on `create_service` as a dict from alias to adapter version.

Copy code

```
base.create_service(
    service_name="LLM_SVC",
    service_compute_pool="GPU_POOL",
    ingress_enabled=True,
    inference_engine_options={"engine": "vllm"},
    adapters={
        "support": support_mv,
        "sql_gen": sql_mv,
    },
)
```

You can also pass a list of adapter versions. Omit `adapters`, or pass `{}` or `[]`, for a service with no
adapters.

To serve a single adapter, create the service on the adapter version. This deploys its base version with only that
adapter attached.

Copy code

```
support_mv.create_service(
    service_name="SUPPORT_SVC",
    service_compute_pool="GPU_POOL",
    ingress_enabled=True,
    inference_engine_options={"engine": "vllm"},
)
```

Every adapter must have the deployed version as its base, and each adapter version can be attached once. For the
names callers use to select each adapter, see [Adapter names](#label-lora-adapters-names).

To set LoRA capacity, pass `--max-loras` (default 8) or `--max-lora-rank` (default: the largest rank among the
attached adapters) in `engine_args_override`. Snowflake configures LoRA serving and adapter loading for you.

Each service instance loads every attached adapter when it starts, including after a restart or scale-out. If
an adapter cannot be loaded, that instance does not become ready.

## Select an adapter per request

The adapter is selected by `model`, the same field OpenAI-compatible clients already send.

### Adapter names

Every attached adapter can be selected by its fully qualified version name,
`<database>.<schema>.<model>/VERSIONS/<version>` (for example, `ML.DEMOS.SUPPORT_TONE/VERSIONS/V1`). An alias you
set is an additional name for the same adapter.

| How the adapter is attached | Values of `model` that select it |
| --- | --- |
| `adapters={"support": support_mv}` | `support` or `ML.DEMOS.SUPPORT_TONE/VERSIONS/V1` |
| `adapters=[support_mv]` | `ML.DEMOS.SUPPORT_TONE/VERSIONS/V1` |
| `support_mv.create_service(...)` or `support_mv.run_batch(...)` | `ML.DEMOS.SUPPORT_TONE/VERSIONS/V1` |
| `inference.adapters` item with `alias: support` | `support` or `ML.DEMOS.SUPPORT_TONE/VERSIONS/V1` |
| `inference.adapters` item without `alias` | `ML.DEMOS.SUPPORT_TONE/VERSIONS/V1` |

Expand

Show lessSee more

To call the base model, omit `model`. From an OpenAI-compatible client, which always sends `model`, set it to the
base model’s name.

Aliases must be unique and non-empty, and are case-sensitive. In SQL, one row with an unmatched `model` fails the
whole query.

### Examples

In SQL, `model` can be a constant or a column, so each row can use a different adapter:

Copy code

```
SELECT LLM_SVC!"__CALL__"(msgs, model => 'support') FROM tickets;

-- per row
SELECT LLM_SVC!"__CALL__"(msgs, model => adapter_alias) FROM tickets;
```

With the REST API:

Copy code

```
POST https://<ingress-host-for-LLM_SVC>/--call--
{
  "dataframe_split": {
    "columns": ["MESSAGES"],
    "data": [[[{"role": "user", "content": "..."}]]]
  },
  "params": {"model": "support"}
}
```

OpenAI-compatible `/v1/chat/completions`: set `model` to the alias. `GET /v1/models` lists every value `model`
accepts.

Python against an existing service:

Copy code

```
base.run(
    messages,
    service_name="LLM_SVC",
    params={"model": "support"},
)
```

You can also call `run(..., service_name=...)` on an adapter version.

## See which adapters are on a service

Copy code

```
CALL LLM_SVC!GET_SERVICE_ADAPTERS();
```

The result lists each attached adapter’s `name`, `version`, and `alias`. You need the same privileges as to call
the service.

To list every adapter logged against a base, whether or not it is attached to a service, use
`base.get_adapters()`.

## Batch inference jobs

[Batch inference jobs](/developer-guide/snowflake-ml/inference/batch-inference-jobs) take the same `adapters`
value on `InferenceSpec.adapters`. Set `input_spec.params["model"]` to choose
one adapter for the whole job.

Copy code

```
from snowflake.ml.model.batch_inference import InferenceSpec, InputSpec, OutputSpec

base.run_batch(
    input_df,
    compute_pool="GPU_POOL",
    output_spec=OutputSpec(stage_location="@ML.DEMOS.STAGE/out/"),
    inference_spec=InferenceSpec(
        adapters={
            "support": support_mv,
            "sql_gen": sql_mv,
        },
    ),
    input_spec=InputSpec(params={"model": "support"}),
)
```

You can also call `run_batch` on an adapter version. To score the adapter, set `params.model` to its fully
qualified version name (see [Adapter names](#label-lora-adapters-names)). If omitted, the base model is used.

SQL `EXECUTE INFERENCE JOB SERVICE` takes the same list under `inference.adapters`. `alias` is optional:

Copy code

```
inference:
  adapters:
    - name: ML.DEMOS.SUPPORT_TONE
      version: V1
      alias: support
    - name: ML.DEMOS.SQL_GEN
      version: V3
      alias: sql_gen
```

Batch jobs with adapters require the vLLM engine. If the job’s `MODEL` is an adapter version, the job runs on its
base version with that adapter attached, and `inference.adapters` must be omitted.

## Privileges

The base model, each adapter model, and the service each have their own privileges. For example, a role that can
read the base model can’t read its adapters unless it’s granted access to them too. Privileges are granted on a
model and cover all of its versions.

| When | Who is checked | What they need |
| --- | --- | --- |
| Log an adapter | Logger | `CREATE MODEL` on the target schema. `USAGE`, `READ`, or `OWNERSHIP` on the base model. |
| Create the service | Deployer | `READ` or `OWNERSHIP` on a base in your account (`USAGE` for a Cortex Base Model). `READ` or `OWNERSHIP` on each attached adapter. `CREATE SERVICE` plus the usual deploy dependencies. |
| Call the service | Caller | `USAGE` on the service and `GRANT SERVICE ROLE …!INFERENCE_SERVICE_FUNCTION_USAGE`. No adapter grant. |
| List attached adapters | Caller | Same as call. |

Expand

Show lessSee more

Access to an adapter is checked when it is attached to a service. After that, any role that can call the service
can use any attached adapter, without a grant on the adapter model.

A common setup: a platform role owns the base and the service; a product role owns the adapter and grants
`READ` to the deployer.

Copy code

```
GRANT READ ON MODEL ML.DEMOS.LLAMA3_8B TO ROLE platform_deployer;
GRANT READ ON MODEL ML.DEMOS.SUPPORT_TONE TO ROLE platform_deployer;

GRANT USAGE ON SERVICE ML.DEMOS.LLM_SVC TO ROLE svc_caller;
GRANT SERVICE ROLE ML.DEMOS.LLM_SVC!INFERENCE_SERVICE_FUNCTION_USAGE TO ROLE svc_caller;
-- svc_caller can SELECT … model => 'support' with no grant on SUPPORT_TONE
```

When an instance restarts or scales out, it loads the base and adapters with the service owner role, not the
deployer. If that role loses `READ` on the base or an adapter model, including after an ownership transfer, new
instances do not become ready.

## Related

- [Hugging Face pipeline](/developer-guide/snowflake-ml/model-registry/built-in-models/hugging-face) — full-weight Hugging Face models
- [Deploy models for real-time inference (REST API)](/developer-guide/snowflake-ml/inference/real-time-inference-rest-api)
- [Batch inference jobs](/developer-guide/snowflake-ml/inference/batch-inference-jobs)
- [ML Lineage: Trace ML data flow](/developer-guide/snowflake-ml/ml-lineage)
- [snowflake.ml.model.ModelVersion](/developer-guide/snowpark-ml/reference/latest/api/model/snowflake.ml.model.ModelVersion)
