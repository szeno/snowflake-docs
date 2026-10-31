# Cortex Training

[Preview Feature — Open](/release-notes/preview-features)

Available in all commercial Amazon Web Services (AWS) regions. Requires enablement.

Cortex Training is a serverless LLM customization service within the Snowflake platform. It
lets you customize open-weight foundation models to improve accuracy or reduce cost for
domain-specific tasks in a resource-efficient way. Snowflake provides a managed path to model
customization and inference without requiring procurement of specialized infrastructure, cluster management,
distributed processing, or container orchestration.

Note

Cortex Training is in preview. Model availability, APIs, and specifications on these pages are
subject to change before general availability.

## Training APIs as a service

Traditional distributed training requires you to provision a GPU cluster and co-locate your
training script, data, and model weights on the same hardware. GPU-intensive work, such as
forward and backward passes and optimizer steps, also runs alongside non-GPU-intensive work,
such as data ingestion and tool calls. This can leave GPUs underused.

Cortex Training separates the workflow into a client side and a server side:

- **Your workspace (client side).** Your laptop or a CPU-only VM runs the training script:
  orchestration logic, data loading, and batch preparation. Input batches are serialized and
  sent to the platform over REST for forward-backward passes, optimizer steps, weight
  synchronization, and generation requests.
- **The managed platform (server side).** Snowflake holds the model weights and optimizer state
  and runs the GPU-intensive work. The platform executes forward passes, backward passes,
  optimizer steps, and generation, then returns results such as training loss to your client.

This separation keeps non-GPU work, such as data preparation and rollouts, in your workspace
while GPU work runs remotely. You don’t need a local GPU, and you don’t download model weights
to your machine.

### Platform architecture

You interact with Cortex Training through either supported SFT and RL framework integrations
or low-level training-loop APIs. For framework integrations, Snowflake connects to the engine
layer so GPU-bound operations run on the managed platform rather than in your local environment.

The server-side Cortex Training runtime includes the following layers and services:

- **Training frameworks.** Integrations for SFT and RL frameworks let you use existing training
  workflows.
- **Training and inference APIs.** REST endpoints support weight synchronization, forward and
  backward passes, optimizer steps, generation, inference, and evaluation workflows.
- **Serverless runtime.** The runtime executes the distributed training and inference jobs.
- **Resource and artifact services.** GPU multiplexing, multi-tenant scheduling, checkpoint and
  resume, artifact management, and zone management support the training lifecycle.
- **Managed GPU platform.** Snowflake operates the underlying GPU infrastructure.

## Why use it

- **No GPU procurement.** Pay for the GPU hours you use instead of holding idle capacity while
  non-GPU parts of your pipeline run.
- **No infrastructure management.** Snowflake maintains the distributed training infrastructure
  and its training and inference optimizations, so your team spends its time on modeling work.
- **High GPU utilization through job multiplexing.** Cortex Training dynamically schedules
  multiple training or inference jobs on the same GPUs. This increases utilization and provides
  more usable training and inference hours per dollar.
- **Framework flexibility.** Bring existing scripts built with popular open-source SFT
  (supervised fine-tuning) and RL (reinforcement learning) frameworks. Cortex Training integrates
  with frameworks such as VeRL, SkyRL, AReal, Unsloth, and Axolotl.
- **Open-weight model support.** Use open-weight models from sources such as Hugging Face across
  model sizes, parameter families, and dense or mixture-of-experts (MoE) architectures.
- **Zero data movement.** Train on data that already lives in Snowflake tables, internal stages,
  or S3 buckets reached through external stages. Training data and models remain on one platform,
  so there’s no export pipeline to build.

## Ways to run a job

Cortex Training supports two interaction patterns:

- **Low-level client APIs.** Use the Python client when you need fine-grained control over which
  training-loop steps run remotely and which run locally. This approach supports custom trainers
  and self-orchestrated pre-training, mid-training, SFT, and RL pipelines.
- **Training framework integrations.** Leverage popular OSS frameworks for SFT and RL to fine-tune
  open-weight models. The frameworks route GPU-bound operations to the Cortex Training backend.
  Ongoing framework integrations include VeRL, SkyRL, Prime-RL, and Unsloth, at different stages of
  upstream acceptance. Contact your account team for the current integration status and working
  project repositories.

## Running jobs with the client

The customer-facing [Cortex Training client](https://github.com/snowflakedb/cortex-training)
provides the `cortex_training` Python namespace and the `cortex-training` CLI. Use
the Python client to drive jobs against the Cortex Training backend.

Authentication uses a Snowflake programmatic access token
(PAT). See the [API reference](/user-guide/snowflake-cortex/cortex-training/api-reference) for
the full `CortexTrainingClient` surface.

## Jobs, sub-jobs, and artifacts

A job is made up of one or more sub-jobs. A training sub-job accepts forward-backward and
optimizer-step calls; a sampling sub-job serves generation requests. Submitting both in one job
lets an on-policy RL loop alternate between rollout generation and weight updates.

Every job automatically gets an experiment run in Snowflake ML Experiments. Checkpoints are saved
server-side and persisted to the experiment-run stage, so you can list them, load one into a
running job, or start a new job from a checkpoint saved by an earlier one.

## Supported models

Cortex Training supports a curated set of open models. See
[Cortex Training models](/user-guide/snowflake-cortex/cortex-training/models) for the full list,
including which models support fine-tuning versus inference and the maximum context length for
LoRA (low-rank adaptation) and full-parameter training.

## Billing

Cortex Training bills for on-demand GPU usage, in [AI Credits](/user-guide/snowflake-cortex/pricing).
For pricing on reserved GPU capacity, contact your account team.

### Rates

Each GPU that a job holds is charged at the hourly rate for its hardware type:

| GPU | AI Credits per GPU-hour |
| --- | --- |
| NVIDIA H200 (141 GB) | 4.80 |
| NVIDIA B300 (288 GB) | 9.00 |

Expand

Show lessSee more

Important

Usage is metered **per second**, with no minimum. You pay only for the GPU time your jobs
hold, not for full hours.

### When billing starts and stops

- **Not billed** while a job is submitted, validated, or queued, before GPU capacity is assigned
  to it.
- **Billing starts** when Snowflake assigns GPU capacity to the job. This includes the
  initialization stage that follows, while the system loads the model onto the GPUs.
- **Billing ends** when Snowflake releases the job’s GPU capacity. This happens when the job
  completes, fails, or is canceled, or when you drop a model deployment.

To stop charges for a job that you’re no longer using, cancel it. For more information, see
[Cancel a job](/user-guide/snowflake-cortex/cortex-training/job-management#label-cortex-training-cancel-job).

For example, a training job that holds 2 H200 GPUs for 90 minutes of billed time, including
initialization, uses 2 × 1.5 hours × 4.80 = 14.40 AI Credits.

## Next steps

- [Get started with Cortex Training](/user-guide/snowflake-cortex/cortex-training/get-started)
- [Manage Cortex Training jobs](/user-guide/snowflake-cortex/cortex-training/job-management)
- [Cortex Training models](/user-guide/snowflake-cortex/cortex-training/models)
- [Cortex Training API reference](/user-guide/snowflake-cortex/cortex-training/api-reference)

## Legal notices

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Generally available functions are Covered AI Features. Preview functions are Preview AI Features.  [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
