# Cortex Training API reference

[Preview Feature — Open](/release-notes/preview-features)

Available in all commercial Amazon Web Services (AWS) regions. Requires enablement.

This reference covers `CortexTrainingClient` in the customer-facing
`cortex_training` Python namespace. Install the package, then import the client:

Copy code

```
uv pip install git+https://github.com/snowflakedb/cortex-training.git
```

Copy code

```
from cortex_training import CortexTrainingClient, SubJobConfig, JobType
from cortex_training import (
    serialize_forward_backward_args,
    build_forward_backward_kwargs,
    build_forward_backward_payload,
)
```

Parameter descriptions below are taken from the SDK docstrings and method signatures in
`CortexTrainingClient` and `SubJobConfig`.

## CortexTrainingClient

HTTP client for the Cortex Training API.

Recommended construction for Snowflake accounts:

Copy code

```
client = CortexTrainingClient.from_pat(
    host="myaccount.snowflakecomputing.com",
    pat="...",
    database="MY_DB",
    schema="PUBLIC",
)
```

Base URL path used for requests:

```
https://{host}/api/v2/databases/{database}/schemas/{schema}/cortex-training
```

### from\_pat

Authenticate with a Programmatic Access Token (PAT).

Sends `Authorization: Bearer <pat>` plus the
`X-Snowflake-Authorization-Token-Type: PROGRAMMATIC_ACCESS_TOKEN` header
on every request. No login round-trip.

Copy code

```
CortexTrainingClient.from_pat(
    host,
    pat,
    database,
    schema,
    endpoint='cortex-training',
    verify_ssl=True,
    **kwargs,
)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `host` | `str` | required |  |
| `pat` | `str` | required |  |
| `database` | `str` | required |  |
| `schema` | `str` | required |  |
| `endpoint` | `str` | `'cortex-training'` |  |
| `verify_ssl` | `bool` | `True` |  |
| `**kwargs` | `Any` | `{}` |  |

Expand

Show lessSee more

### Constructor options

`from_pat` forwards optional constructor kwargs to `__init__`. You can also construct a client directly for local/mock use by passing `base_url`.

Copy code

```
CortexTrainingClient(
    base_url,
    database,
    schema,
    endpoint='cortex-training',
    poll_interval=0.5,
    poll_timeout=1800.0,
    poll_backoff_multiplier=1.25,
    poll_max_interval=6.0,
    pool_maxsize=1024,
    max_retries=10,
)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `base_url` | `str` | required |  |
| `database` | `str` | required |  |
| `schema` | `str` | required |  |
| `endpoint` | `str` | `'cortex-training'` |  |
| `poll_interval` | `float` | `0.5` |  |
| `poll_timeout` | `float` | `1800.0` |  |
| `poll_backoff_multiplier` | `float` | `1.25` |  |
| `poll_max_interval` | `float` | `6.0` |  |
| `pool_maxsize` | `int` | `1024` |  |
| `max_retries` | `int` | `10` |  |

Expand

Show lessSee more

## Job lifecycle

### create\_job

Create a job from a list of sub-jobs and return its server job\_id.

Each `SubJobConfig` is validated client-side before the request
is sent (see `SubJobConfig.validate`). `job_id` is optional;
when omitted the server generates one. `experiment_name` is optional;
when omitted the server auto-creates an experiment for the job.

Copy code

```
client.create_job(sub_jobs, job_id=None, experiment_name=None)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `sub_jobs` | `list[SubJobConfig]` | required |  |
| `job_id` | `str | None` | `None` |  |
| `experiment_name` | `str | None` | `None` |  |

Expand

Show lessSee more

### create\_job\_from\_body

Create a job from a raw REST CreateJob request body.

This is useful for tooling that already has the REST JSON payload,
while `create_job` remains the typed path for Python callers.

Copy code

```
client.create_job_from_body(body)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `body` | `dict` | required |  |

Expand

Show lessSee more

### wait\_for\_job

Poll until the job reaches `RUNNING`. Raises on terminal states or timeout.

Copy code

```
client.wait_for_job(job_id)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |

Expand

Show lessSee more

### get\_job

Copy code

```
client.get_job(job_id)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |

Expand

Show lessSee more

### list\_jobs

Copy code

```
client.list_jobs(status=None)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `status` | `str | None` | `None` |  |

Expand

Show lessSee more

### cancel\_job

Copy code

```
client.cancel_job(job_id)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |

Expand

Show lessSee more

### get\_capacity

Return the calling account’s reserved GPU capacity and current usage.

This method works only for reserved GPUs. For accounts that use
on-demand GPUs, `has_reservation` is `False` and the response doesn’t
reflect on-demand capacity.

Backed by the account-scoped endpoint `/cortex-training/capacity`
(not under `/{job_id}`). The account is resolved server-side from the
caller’s session — never from a request field — so a caller can only
ever read its own account’s capacity.

The returned dict includes these fields:

- `has_reservation` (bool): whether the account has a configured GPU
  reservation.
- `max_total_gpus` (int): the account’s GPU limit. `-1` means no limit.
- `reserved_gpus` (int): total GPUs reserved for the account.
  Deprecated: use `max_total_gpus` with `has_reservation` instead.
- `in_use_gpus` (int): GPUs held by the account’s jobs that are placing,
  initializing, or running.
- `pending_gpus` (int): GPUs requested by jobs still waiting for
  capacity. These count against the limit and reduce `available_gpus`.
- `available_gpus` (int): GPUs a new job could start with now. A value
  of 0 doesn’t block submission: a job within the limit is queued.

Copy code

```
client.get_capacity()
```

*No parameters.*

### get\_experiment\_run

Return `{experiment_name, experiment_run_name}` for `job_id`.

Backed by the endpoint `/cortex-training/{job_id}/experiment-run`.

Copy code

```
client.get_experiment_run(job_id)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |

Expand

Show lessSee more

## Training

These methods submit async requests. Each returns a `request_id` you pass to `poll_request`.

### forward\_backward

Submit a forward+backward pass. Returns request\_id.

Copy code

```
client.forward_backward(job_id, data)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |
| `data` | `bytes` | required |  |

Expand

Show lessSee more

### step

Submit an optimizer step. Returns request\_id.

Copy code

```
client.step(job_id, learning_rate=None)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |
| `learning_rate` | `float | None` | `None` |  |

Expand

Show lessSee more

### poll\_request

Poll until the async request completes. Returns the result dict.

Copy code

```
client.poll_request(job_id, request_id)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |
| `request_id` | `str` | required |  |

Expand

Show lessSee more

### get\_request\_status

Copy code

```
client.get_request_status(
    job_id,
    request_id,
    max_events=None,
    cursor=None,
)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |
| `request_id` | `str` | required |  |
| `max_events` | `int | None` | `None` |  |
| `cursor` | `str | None` | `None` |  |

Expand

Show lessSee more

## Checkpoints

### save

Submit a checkpoint save. Returns request\_id.

Copy code

```
client.save(job_id, checkpoint_id=None, checkpoint_type=None)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |
| `checkpoint_id` | `str | None` | `None` |  |
| `checkpoint_type` | `str | None` | `None` |  |

Expand

Show lessSee more

### load

Submit a checkpoint load into an existing job. Returns request\_id.

Copy code

```
client.load(
    job_id,
    checkpoint_id,
    source_job_id=None,
    target_sub_job_id=None,
)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required | The job to load the checkpoint into. |
| `checkpoint_id` | `str` | required | Checkpoint identifier (from a prior save). |
| `source_job_id` | `str | None` | `None` | Optional. Load from another job’s checkpoint store. |
| `target_sub_job_id` | `str | None` | `None` | Optional. Route the load to a specific training sub-job. Format: `"{job_id}:training:{index}"`. Omit to use the session’s default training sub-job. |

Expand

Show lessSee more

Returns `str`: request\_id for polling via `poll_request()`.

### list\_checkpoints

Copy code

```
client.list_checkpoints(job_id)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |

Expand

Show lessSee more

### export\_checkpoint

Copy code

```
client.export_checkpoint(job_id, checkpoint_id)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |
| `checkpoint_id` | `str` | required |  |

Expand

Show lessSee more

### delete\_checkpoint

Delete a checkpoint. Returns None on success.

Copy code

```
client.delete_checkpoint(job_id, checkpoint_id)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |
| `checkpoint_id` | `str` | required |  |

Expand

Show lessSee more

## Inference

### generate

Submit a generate request to a sampling sub-job. Returns request\_id.

The typed fields are serialized as a DSSST1 safetensors frame and sent
as `application/octet-stream`. Oversized frames are byte-chunked
across multiple POSTs; the final POST returns the pollable request id.
Poll with `poll_request`.

Prompt-length validation is asymmetric by input type:

- **Pre-tokenized prompts** (`list[int]`) are checked client-side
  against the sampling sub-job’s `max_seq_len` and fail fast with a
  `ValueError` when `len(prompt) >= max_seq_len` — the token count
  is exact, so this never rejects a prompt vLLM would accept.
- **String prompts** are *not* validated here. Counting their tokens
  would require replicating the server tokenizer (including special
  tokens), so an over-long string instead fails server-side in vLLM
  with a `maximum model length` error rather than client-side.

Copy code

```
client.generate(
    job_id,
    prompts,
    sampling_params=None,
    routing_key=None,
    strict=None,
)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |
| `prompts` | `list[str | list[int]]` | required |  |
| `sampling_params` | `dict | list[dict | None] | None` | `None` |  |
| `routing_key` | `str | list[str | None] | None` | `None` |  |
| `strict` | `bool | None` | `None` |  |

Expand

Show lessSee more

### weight\_sync

Sync model weights from a training sub-job into one or more sampling
sub-jobs (used in RL training loops). Returns request\_id.

Multi-sub-job sessions require the operation envelope to include a
routing hint; by default the operation is routed through the source
training sub-job.

Copy code

```
client.weight_sync(
    job_id,
    source_sub_job_id,
    target_sub_job_ids,
    weight_format=None,
    sub_job_id=None,
    sub_job_type=None,
)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required | The job owning both sub-jobs. |
| `source_sub_job_id` | `str` | required | Training sub-job to read weights from, e.g. `f"{job_id}:training:0"`. |
| `target_sub_job_ids` | `list[str]` | required | Sampling sub-jobs to update, e.g. `[f"{job_id}:sampling:0"]`. |
| `weight_format` | `str | None` | `None` | `"vllm"` (server default) or `"hf"` for full weights, or `"lora"` to broadcast only the adapter tensors. |
| `sub_job_id` | `str | None` | `None` |  |
| `sub_job_type` | `str | None` | `None` |  |

Expand

Show lessSee more

## Model deployments

A model deployment serves a base model or a `weights-only` checkpoint as an
OpenAI-compatible chat completions endpoint. These methods manage the
deployment; call the endpoint itself with any OpenAI-compatible client. Only
`EVALUATION` deployments are supported, and a deployment holds its GPUs until
you drop it.

A deployment is identified by an ID of the form `sf-ct-<UUID>`. Pass it as
`model` when you call the endpoint.

### Deployment spec

`create_model_deployment` takes a spec with exactly three top-level fields:

Copy code

```
{
  "deployment": {"class": "EVALUATION", "min_replicas": 1, "gpus_per_replica": 1, "gpu_type": "H200"},
  "source": {"type": "base_model", "model": "Qwen/Qwen3-1.7B"},
  "inference": {"max_seq_len": 8192}
}
```

| Field | Rule |
| --- | --- |
| `deployment.class` | `"EVALUATION"`. No other class is supported. |
| `deployment.gpu_type` | `H200` or `B300`, case-insensitive. |
| `deployment.gpus_per_replica` | 1, 2, 4, or 8. Each replica’s tensor-parallel size. |
| `deployment.min_replicas` | Positive integer. `min_replicas * gpus_per_replica` must be at most 8 or a multiple of 8. |
| `source.type` | `base_model` (with `model`) or `checkpoint` (with `job_id` and `checkpoint_id`). |
| `inference.max_seq_len` | Maximum sequence length the deployment serves. |

Expand

Show lessSee more

A checkpoint source must name a completed `weights-only` checkpoint and doesn’t
name a model: the client reads the model from the source training job. Which
models can be deployed, and the minimum GPUs per replica each needs, is
decided by the server.

The checkpoint can come from a full fine-tune or a LoRA training job. For a LoRA
checkpoint, the deployment serves the base model with your trained adapter, using
the LoRA settings from the training job. You can’t set LoRA settings in the spec.

### Deployment statuses

A deployment reports one of these statuses:

| Status | Meaning |
| --- | --- |
| `PENDING` | Waiting for GPU capacity. |
| `INITIALIZING` | GPUs are assigned and the model is loading. |
| `READY` | The endpoint is serving requests. |
| `FAILED` | The deployment failed. The metadata includes `failure: {code, message}`. |
| `DROPPING` | The deployment is being dropped. |
| `DROPPED` | The deployment was dropped and holds no GPUs. |
| `TERMINATED` | The deployment was torn down and holds no GPUs. |

Expand

Show lessSee more

### Calling the endpoint

The endpoint is `POST {base_url}/chat/completions`, where `base_url` is
`https://{host}/api/v2/databases/{database}/schemas/{schema}/cortex-training/inference/v1`.
The client exposes it as the `model_deployment_base_url` property, and
`wait_for_model_deployment` returns it as `base_url`. The endpoint behaves as follows:

| Item | Behavior |
| --- | --- |
| Authentication | `Authorization: Bearer <PAT>` and `X-Snowflake-Authorization-Token-Type: PROGRAMMATIC_ACCESS_TOKEN`. |
| `model` | The deployment ID, `sf-ct-<UUID>`. |
| Length limit | `max_completion_tokens`. The endpoint rejects `max_tokens` with HTTP 400 (`unsupported_parameter`). |
| Streaming | With `"stream": true`, the response is server-sent events: one `data:` line per `chat.completion.chunk`, then `data: [DONE]`. Add `"stream_options": {"include_usage": true}` to get a final chunk with token counts. |
| Not ready | HTTP 503 (`endpoint_failed`) while the deployment is `PENDING` or `INITIALIZING`, and briefly after it’s dropped. |
| Not found | HTTP 404 (`model_not_found`) for an unknown deployment, or one that failed or was dropped. |
| Not enabled | HTTP 403 or 405 while inference isn’t enabled for the account. |

Expand

Show lessSee more

Without `"stream": true`, the response is one `chat.completion` object.

### create\_model\_deployment

Create a model deployment from a [deployment spec](#label-cortex-training-deployment-spec) and return its metadata, including the `deployment` ID. The deployment starts in `PENDING`; call `wait_for_model_deployment` to wait until it’s `READY`.

Copy code

```
client.create_model_deployment(spec)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `spec` | `ModelDeploymentSpec | Mapping[str, Any]` | required |  |

Expand

Show lessSee more

### wait\_for\_model\_deployment

Poll until the deployment is `READY` and return its metadata, including `base_url`. Raises `ModelDeploymentWaitError` if the deployment reaches `FAILED`, `TERMINATED`, or `DROPPED`, and `ModelDeploymentWaitTimeout` when the client’s `poll_timeout` passes. A timeout doesn’t drop the deployment, which keeps holding GPUs until you drop it.

Copy code

```
client.wait_for_model_deployment(deployment_id)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `deployment_id` | `str` | required |  |

Expand

Show lessSee more

### get\_model\_deployment

Return the metadata for one deployment, including `deployment`, `status`, `model_source`, and the capacity fields. `base_url` is included unless the deployment is `FAILED`, `DROPPING`, `DROPPED`, or `TERMINATED`, and `failure` is included for a `FAILED` or `TERMINATED` deployment.

Copy code

```
client.get_model_deployment(deployment_id)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `deployment_id` | `str` | required |  |

Expand

Show lessSee more

### describe\_model\_deployment

Return one deployment’s status, endpoint, and configuration. The configuration is grouped under `spec` in the same `deployment`, `source`, and `inference` shape as the create spec, but it’s a read view and isn’t guaranteed to be a valid `create_model_deployment` input. A deployment created from a checkpoint currently reports a `base_model` source.

Copy code

```
client.describe_model_deployment(deployment_id)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `deployment_id` | `str` | required |  |

Expand

Show lessSee more

### list\_model\_deployments

Return the metadata for every deployment in the client’s database and schema. Pass `status` (for example, `"READY"` or `["PENDING", "INITIALIZING"]`, case-insensitive) to keep only deployments in those statuses. Entries don’t include `base_url`; use `get_model_deployment` to get it.

Copy code

```
client.list_model_deployments(status=None)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `status` | `str | Iterable[str] | None` | `None` |  |

Expand

Show lessSee more

### drop\_model\_deployment

Drop a deployment and release its GPUs. Safe to retry: a deployment that’s already `DROPPING` or `DROPPED` is reported as dropped. A `FAILED` or `TERMINATED` deployment holds no GPUs and can’t be dropped, so the method returns `{"dropped": False, "status": ...}` instead of raising an error.

Copy code

```
client.drop_model_deployment(deployment_id)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `deployment_id` | `str` | required |  |

Expand

Show lessSee more

### download\_model\_deployment\_logs

Download a deployment’s logs into `output_dir`. `log_type` is `"execution"` (the default) or `"stdout"`. Returns `{"deployment", "logs"}`, where `logs` lists each saved file’s `filename` and `saved_path` (plus `chunk_count` for `stdout`). Use these logs to find out why a deployment `FAILED`.

Copy code

```
client.download_model_deployment_logs(deployment_id, output_dir, log_type='execution')
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `deployment_id` | `str` | required |  |
| `output_dir` | `str | os.PathLike[str]` | required |  |
| `log_type` | `str` | `'execution'` |  |

Expand

Show lessSee more

### download\_model\_deployment\_metrics

Download a deployment’s metrics into `output_dir`. Returns `{"deployment", "metrics"}`, where `metrics` lists each saved file’s `filename`, `saved_path`, and `chunk_count`.

Copy code

```
client.download_model_deployment_metrics(deployment_id, output_dir)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `deployment_id` | `str` | required |  |
| `output_dir` | `str | os.PathLike[str]` | required |  |

Expand

Show lessSee more

## Logs

### fetch\_execution\_logs

Download every log file under the job’s experiment run stage.

Returns a list of `{"sub_job_id", "filename", "s3_uri", "content"}`
entries, one per object found under a `_logs/<sub_job_id>/` subtree
in the run’s stage. Filenames such as `execution.jsonl` and
`server.log` are both included; bodies are decoded as UTF-8.

Steps: `experiment-run` → `SYSTEM$GET_VSTAGE_WRITE_CREDS` →
`ListObjectsV2` (scoped by stage prefix) → `GetObject` per match.

Copy code

```
client.fetch_execution_logs(job_id)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |

Expand

Show lessSee more

### stream\_logs

Yield a sub-job’s log entries, polling with backoff.

Drains the log then, with `follow=True` (the default), keeps polling
for new entries until the caller stops iterating — suitable for a live
tail. With `follow=False` it stops once the log reports `eof`.

Copy code

```
client.stream_logs(
    job_id,
    sub_job_id=None,
    sub_job_type=None,
    cursor=None,
    max_lines=None,
    poll_interval=None,
    follow=True,
)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `job_id` | `str` | required |  |
| `sub_job_id` | `str | None` | `None` |  |
| `sub_job_type` | `str | None` | `None` |  |
| `cursor` | `str | None` | `None` |  |
| `max_lines` | `int | None` | `None` |  |
| `poll_interval` | `float | None` | `None` |  |
| `follow` | `bool` | `True` |  |

Expand

Show lessSee more

Returns `Iterator[dict]`.

## SubJobConfig

One sub-job within a CreateJob request.

### training\_job

Build a training `SubJobConfig`. All training fields are explicit.

Copy code

```
SubJobConfig.training_job(
    model_name,
    optimizer,
    max_seq_len,
    train_batch_size,
    n_gpus,
    gradient_clipping=None,
    multiplex_job_id=None,
    load_optimizer_states=None,
    extra_training=None,
    global_batch_size=None,
    dtype=None,
    seed=None,
    model_post_init=None,
    source_checkpoint_info=None,
)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `model_name` | `str` | required | Model identifier (e.g., “Qwen/Qwen3-1.7B”). |
| `optimizer` | `dict` | required | Optimizer config dict (e.g., {“name”: “AdamW”, “lr”: 0.0001}). |
| `max_seq_len` | `int` | required | Maximum sequence length for training. |
| `train_batch_size` | `int` | required | Per-device batch size. |
| `n_gpus` | `int` | required | Number of GPUs (DP size). |
| `gradient_clipping` | `float | None` | `None` | Optional gradient clipping threshold. |
| `multiplex_job_id` | `str | None` | `None` | Optional multiplex job identifier. |
| `load_optimizer_states` | `bool | None` | `None` | Whether to load optimizer states from checkpoints. Set to `False` when loading across different DP sizes (`n_gpus`) since optimizer states are DP-sharded and cannot be resized. When `None`, uses server default (True). **This is a creation-time setting and cannot be changed later.** |
| `extra_training` | `dict | None` | `None` | Additional training config keys (passthrough). |
| `global_batch_size` | `int | None` | `None` | Global batch size across all GPUs. |
| `dtype` | `str | None` | `None` | Model dtype (e.g., “bfloat16”). |
| `seed` | `int | None` | `None` | Random seed. |
| `model_post_init` | `list[str] | None` | `None` | List of post-initialization operations. |
| `source_checkpoint_info` | `dict | None` | `None` | Optional checkpoint to resume from at creation time (use `{"checkpoint_id": "...", "source_job_id": "..."}`). |

Expand

Show lessSee more

### sampling\_job

Build a sampling/log-probability `SubJobConfig`.

Copy code

```
SubJobConfig.sampling_job(
    model_name,
    max_seq_len,
    n_gpus,
    multiplex_job_id=None,
    extra_sampling=None,
    job_type=JobType.SAMPLING,
    global_batch_size=None,
    dtype=None,
    seed=None,
    model_post_init=None,
    source_checkpoint_info=None,
)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `model_name` | `str` | required |  |
| `max_seq_len` | `int` | required |  |
| `n_gpus` | `int` | required |  |
| `multiplex_job_id` | `str | None` | `None` |  |
| `extra_sampling` | `dict | None` | `None` |  |
| `job_type` | `JobType` | `JobType.SAMPLING` |  |
| `global_batch_size` | `int | None` | `None` |  |
| `dtype` | `str | None` | `None` |  |
| `seed` | `int | None` | `None` |  |
| `model_post_init` | `list[str] | None` | `None` |  |
| `source_checkpoint_info` | `dict | None` | `None` |  |

Expand

Show lessSee more

## JobType

Copy code

```
class JobType(str, Enum):
    TRAINING = "training"
    SAMPLING = "sampling"
    LOG_PROBABILITY = "log_probability"
```

## Payload helpers

Helpers that build the forward and backward pass payload in the client’s wire format.

### serialize\_forward\_backward\_args

Serialize `{"args": args, "kwargs": kwargs}` for Cortex Training fwd-bwd.

Copy code

```
serialize_forward_backward_args(args=(), kwargs=None)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `args` | `tuple` | `()` |  |
| `kwargs` | `dict[str, Any] | None` | `None` |  |

Expand

Show lessSee more

### build\_forward\_backward\_kwargs

Build tensor kwargs for a forward-backward training batch.

`payload` is intentionally JSON-shaped so CLI examples can stay readable:
callers may provide either tokenizable `texts` plus a `tokenizer` or
direct tensor data under `input_ids` / `labels` / `position_ids`.

Copy code

```
build_forward_backward_kwargs(payload)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `payload` | `dict[str, Any]` | required |  |

Expand

Show lessSee more

### build\_forward\_backward\_payload

Build a serialized fwd-bwd byte payload from readable JSON.

Copy code

```
build_forward_backward_payload(spec)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `spec` | `dict[str, Any]` | required |  |

Expand

Show lessSee more
