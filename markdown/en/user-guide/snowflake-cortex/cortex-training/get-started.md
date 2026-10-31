# Get started with Cortex Training

[Preview Feature — Open](/release-notes/preview-features)

Available in all commercial Amazon Web Services (AWS) regions. Requires enablement.

This guide walks you through installing the client, connecting to your account, running
a short fine-tuning loop end to end, and streaming responses from your fine-tuned model.

## Prerequisites

- A Snowflake account on Amazon Web Services (AWS) with Cortex Training enabled. To enable
  Cortex Training, contact your account team.
- A [programmatic access token (PAT)](/user-guide/programmatic-access-tokens) for
  authentication.
- Python 3.10 or later.

## Step 1: Install the client

Install the
[Cortex Training client](https://github.com/snowflakedb/cortex-training). The
package includes the `cortex-training` CLI and the `cortex_training` Python
namespace:

Copy code

```
uv pip install git+https://github.com/snowflakedb/cortex-training.git
```

You can use `pip` instead of `uv pip`.

Verify the CLI installation:

Copy code

```
cortex-training --help
cortex-training tui --help
```

## Step 2: Connect to your account

Create a client with your account host and PAT. The `database` and `schema` scope where your
jobs and checkpoints live.

Copy code

```
from cortex_training import CortexTrainingClient

client = CortexTrainingClient.from_pat(
    host="myaccount.snowflakecomputing.com",
    pat="YOUR_PROGRAMMATIC_ACCESS_TOKEN",
    database="MY_DB",
    schema="PUBLIC",
    endpoint="cortex-training",
)
```

## Step 3: Create a training job

Describe the base model and training parameters with `SubJobConfig.training_job`, then create
the job and wait for it to start.

Copy code

```
from cortex_training import SubJobConfig

sub_job = SubJobConfig.training_job(
    model_name="Qwen/Qwen3-8B",
    optimizer={"type": "adamw", "lr": 1e-5},
    max_seq_len=2048,
    train_batch_size=1,
    n_gpus=2,
)

job_id = client.create_job(sub_jobs=[sub_job])
client.wait_for_job(job_id)
```

## Step 4: Run the training loop

Each training step is two async calls: a forward and backward pass, then an optimizer step.
Poll each request for its result.

Copy code

```
from cortex_training import serialize_forward_backward_args

for batch in dataloader:
    payload = serialize_forward_backward_args(kwargs=batch)

    fb_request = client.forward_backward(job_id, payload)
    fb_result = client.poll_request(job_id, fb_request)
    print("loss:", fb_result["avg_loss"])

    step_request = client.step(job_id, learning_rate=1e-5)
    client.poll_request(job_id, step_request)
```

## Step 5: Save a checkpoint

Save a `weights-only` checkpoint when training finishes. You can use this checkpoint to run
inference.

Copy code

```
save_request = client.save(job_id, checkpoint_type="weights-only")
checkpoint = client.poll_request(job_id, save_request)
checkpoint_id = checkpoint["checkpoint_id"]
```

## Step 6: Run inference from your checkpoint

Create a sampling job that points at the saved checkpoint, then generate completions.

Copy code

```
sampling = SubJobConfig.sampling_job(
    model_name="Qwen/Qwen3-8B",
    max_seq_len=2048,
    n_gpus=1,
    source_checkpoint_info={
        "checkpoint_id": checkpoint_id,
        "source_job_id": job_id,
    },
)

sampling_job_id = client.create_job(sub_jobs=[sampling])
client.wait_for_job(sampling_job_id)

gen_request = client.generate(
    sampling_job_id,
    prompts=["Summarize the benefits of fine-tuning."],
    sampling_params={"max_tokens": 64},
)
result = client.poll_request(sampling_job_id, gen_request)
print(result)
```

## Step 7: Deploy your checkpoint to a streaming endpoint

A model deployment serves your checkpoint through an OpenAI-compatible chat completions
endpoint, so any OpenAI-compatible client can stream responses from it token by token.

Create the deployment from the `weights-only` checkpoint that you saved, then wait until it’s
`READY`. You don’t specify the model: the client reads it from the training job. This works
the same way for a checkpoint from a LoRA training job.

Copy code

```
spec = {
    "deployment": {
        "class": "EVALUATION",
        "min_replicas": 1,
        "gpus_per_replica": 1,
        "gpu_type": "H200",
    },
    "source": {
        "type": "checkpoint",
        "job_id": job_id,
        "checkpoint_id": checkpoint_id,
    },
    "inference": {"max_seq_len": 2048},
}

deployment_id = client.create_model_deployment(spec)["deployment"]
ready = client.wait_for_model_deployment(deployment_id)
base_url = ready["base_url"]
```

The deployment ID has the form `sf-ct-<UUID>`. Reaching `READY` can take several minutes,
because the deployment loads the model onto the GPUs first. To deploy a base model instead
of a checkpoint, set `source` to `{"type": "base_model", "model": "Qwen/Qwen3-8B"}`.

Next, install the `openai` package:

Copy code

```
uv pip install openai
```

Then stream a chat completion. Authenticate with your PAT, and pass the deployment ID as
`model`:

Copy code

```
from openai import OpenAI

openai_client = OpenAI(
    base_url=base_url,
    api_key="YOUR_PROGRAMMATIC_ACCESS_TOKEN",
    default_headers={"X-Snowflake-Authorization-Token-Type": "PROGRAMMATIC_ACCESS_TOKEN"},
)

stream = openai_client.chat.completions.create(
    model=deployment_id,
    messages=[{"role": "user", "content": "Summarize the benefits of fine-tuning."}],
    max_completion_tokens=256,
    stream=True,
)
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

Use `max_completion_tokens` to limit the response length. The deployment endpoint rejects
`max_tokens`.

Note

Inference isn’t available on all accounts yet. Until it’s enabled for your account, requests
to the endpoint return HTTP 403 or 405. Requests to a deployment that isn’t `READY` yet return
HTTP 503.

For the full list of deployment methods, spec rules, and endpoint behavior, see
[Model deployments](/user-guide/snowflake-cortex/cortex-training/api-reference#label-cortex-training-model-deployments).

## Step 8: Clean up

A deployment holds its GPUs until you drop it. Drop the deployment and cancel jobs you’re no
longer using to release GPUs.

Copy code

```
client.drop_model_deployment(deployment_id)
client.cancel_job(sampling_job_id)
client.cancel_job(job_id)
```
