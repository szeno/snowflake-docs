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

- **No GPU procurement.** With Cortex Training On Demand, pay for the GPU hours you use instead of
  holding idle capacity while non-GPU parts of your pipeline run.
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

## Access control

Each request runs as the role of the credential that signs it. The role needs a privilege on the
database and schema in the request, such as USAGE. Some operations also need the privileges in the
following table:

| Operation | Required privileges |
| --- | --- |
| Create a job, including a model deployment | USE CORTEX TRAINING on the account, and a privilege on an experiment (see below). |
| Create a job that imports weights from an external stage | The privileges to create a job, plus READ on the stage. |
| Create a model deployment from another job’s checkpoint | The privileges to create a job. The role must also be the source job’s owner role and have USAGE on the source job’s database and schema. |
| Get or cancel a job, run training or generation calls, list, export, or delete its checkpoints, and check a request’s status | The job’s owner role. |
| Stream chat completions from a model deployment | The deployment’s owner role, plus USAGE on the deployment’s database and schema. |

Expand

Show lessSee more

All other operations, such as listing jobs, checking GPU capacity, and listing models, need no
additional privileges. A list of jobs includes only the jobs that the role owns.

Cortex Training uses Snowflake ML Experiments to track each job’s runs and store its checkpoints.
Because every job records its run in an experiment, creating a job needs a privilege on one:

- **To have Cortex Training create the experiment for you** (you don’t pass `experiment_name`):
  CREATE EXPERIMENT on the schema.
- **To use an existing experiment** (you pass `experiment_name`): MODIFY on that experiment.

A job’s owner role is the role that created it. The owner role applies when it’s the primary role,
an active secondary role, or a role that either one inherits. Jobs and model deployments have no
privileges of their own that you can grant. To let another role use a job or a deployment, grant the
owner role to that role, or run related work under the same role.

The ACCOUNTADMIN role has the USE CORTEX TRAINING privilege. To let another role create jobs, an
account administrator grants the privilege to it:

Copy code

```
GRANT USE CORTEX TRAINING ON ACCOUNT TO ROLE my_training_role;
```

The grant takes effect immediately. If a role can already create jobs without the USE CORTEX
TRAINING privilege, grant the privilege to it anyway, so that the role keeps working when the
requirement applies to your account.

Grant the privilege to the roles that need to create jobs. If your account doesn’t need to limit
which roles can start GPU training, you can grant it to the PUBLIC role instead, which gives it to
every role in the account:

Copy code

```
GRANT USE CORTEX TRAINING ON ACCOUNT TO ROLE PUBLIC;
```

A request that lacks a required privilege fails with one of the following responses. When the object
might also not exist, the response is the same in both cases, so it doesn’t reveal whether the
object exists.

| Cause | HTTP status and error code |
| --- | --- |
| The role doesn’t have the USE CORTEX TRAINING privilege when it creates a job | 403, `003001` |
| The role can’t access the database or schema | 400, `517602` |
| The role doesn’t have the CREATE EXPERIMENT privilege on the schema, or can’t access or modify the named experiment | 400, `517602` |
| The role can’t access the external stage | 400, `517602` |
| The role isn’t the job’s owner role, or the job doesn’t exist | 404, `517601` |
| The role can’t access the source checkpoint for a model deployment | 404, `517601` |
| A chat completion request can’t access the database, schema, or model deployment | 404 |

Expand

Show lessSee more

Every 400 response in this table uses error code `517602`, which also applies to other invalid
requests. Use the error message to tell them apart.

Chat completion requests report a database or schema that the role can’t access as 404 instead of
400, so that an inference request can’t tell whether the database or schema exists.

## Billing

Cortex Training On Demand bills for on-demand GPU usage, in [AI Credits](/user-guide/snowflake-cortex/pricing).
For pricing, see the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
For pricing on reserved GPU capacity, contact your account team.

Important

Usage is metered **per second**, with no minimum. You pay only for the GPU time your jobs
hold, not for full hours.

### When on-demand billing starts and stops

For Cortex Training On Demand, billing works as follows:

- **Not billed** while a job is submitted, validated, or queued, before GPU capacity is assigned
  to it.
- **Billing starts** when Snowflake assigns GPU capacity to the job. This includes the
  initialization stage that follows, while the system loads the model onto the GPUs.
- **Billing ends** when the job reaches the terminal status. This happens when the job
  completes, fails, or is canceled, or when you drop a model deployment.

To stop charges for a job that you’re no longer using, cancel it. For more information, see
[Cancel a job](/user-guide/snowflake-cortex/cortex-training/job-management#label-cortex-training-cancel-job).

## Next steps

- [Get started with Cortex Training](/user-guide/snowflake-cortex/cortex-training/get-started)
- [Manage Cortex Training jobs](/user-guide/snowflake-cortex/cortex-training/job-management)
- [Cortex Training models](/user-guide/snowflake-cortex/cortex-training/models)
- [Cortex Training API reference](/user-guide/snowflake-cortex/cortex-training/api-reference)

## Legal notices

The data classification of inputs and outputs is as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Customer Data | Customer Data | Preview AI Features [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the Preview AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
