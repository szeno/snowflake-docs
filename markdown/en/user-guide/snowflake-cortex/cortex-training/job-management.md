# Manage Cortex Training jobs

[Preview Feature — Open](/release-notes/preview-features)

Available in all commercial Amazon Web Services (AWS) regions. Requires enablement.

After you [create a job](/user-guide/snowflake-cortex/cortex-training/get-started),
use the `cortex-training` command-line interface (CLI) or
`CortexTrainingClient` to inspect status, download logs, list checkpoints, and
cancel or resume work.

## Quick start

Replace `JOB_ID` or `job_id` with the identifier returned when you created the
job. Before running CLI commands, authenticate once with
`cortex-training login --config config.json`. Python examples reuse the
`CortexTrainingClient` from the getting-started guide.

CLIPython

Copy code

```
cortex-training capacity
cortex-training list --status running
cortex-training get JOB_ID
cortex-training wait JOB_ID
cortex-training download-log JOB_ID --output-dir ./logs
cortex-training cancel JOB_ID
```

For a live tail while the job is running:

Copy code

```
cortex-training tui JOB_ID
```

Copy code

```
client.get_capacity()
client.list_jobs(status="running")
client.get_job(job_id)
client.wait_for_job(job_id)
client.fetch_execution_logs(job_id)
client.cancel_job(job_id)
```

For a live tail while the job is running:

Copy code

```
for entry in client.stream_logs(job_id, follow=True):
    print(entry)
```

## GPU capacity

CLIPython

Copy code

```
cortex-training capacity
```

Copy code

```
client.get_capacity()
```

Note

Capacity reporting works only for reserved GPUs. If your account uses on-demand GPUs,
`has_reservation` is `false` and the response doesn’t reflect on-demand capacity.

Example response for an account with a GPU reservation:

Copy code

```
{
  "has_reservation": true,
  "max_total_gpus": 64,
  "reserved_gpus": 64,
  "in_use_gpus": 8,
  "pending_gpus": 16,
  "available_gpus": 40
}
```

| Field | Meaning |
| --- | --- |
| `has_reservation` | Whether the account has a configured GPU reservation. |
| `max_total_gpus` | The account’s GPU limit. `-1` means no limit. |
| `reserved_gpus` | Total GPUs reserved for the account. Deprecated: use `max_total_gpus` with `has_reservation` instead. |
| `in_use_gpus` | GPUs held by the account’s jobs that are placing, initializing, or running. |
| `pending_gpus` | GPUs requested by jobs that are still waiting for capacity. These count against the limit and reduce `available_gpus`. |
| `available_gpus` | GPUs a new job could start with now. |

Expand

Show lessSee more

When `available_gpus` is `0`, you can still submit a job within the limit. The job is queued
until capacity frees up. If a job stays in `PENDING`, check capacity together with the job details.

## List jobs

CLIPython

Copy code

```
cortex-training list
cortex-training list --status running
cortex-training list --status failed
```

Copy code

```
client.list_jobs()
client.list_jobs(status="running")
client.list_jobs(status="failed")
```

Each entry includes `job_id`, `status`, timestamps, and `sub_jobs`. The Python
method returns the following list; the CLI wraps the same list in a `jobs`
field. Example (identifiers redacted):

Copy code

```
[
  {
    "job_id": "11111111-2222-3333-4444-555555555555",
    "status": "FAILED",
    "reason": "sub_job_readiness",
    "created_at": "2026-05-28T20:46:03Z",
    "updated_at": "2026-05-28T20:47:28Z",
    "sub_jobs": [
      {
        "sub_job_id": "11111111-2222-3333-4444-555555555555:training:0",
        "status": "FAILED",
        "job_type": "TRAINING",
        "model_name": "Qwen/Qwen3-0.6B"
      },
      {
        "sub_job_id": "11111111-2222-3333-4444-555555555555:sampling:0",
        "status": "FAILED",
        "job_type": "SAMPLING",
        "model_name": "Qwen/Qwen3-0.6B"
      }
    ]
  }
]
```

## Job details

CLIPython

Copy code

```
cortex-training get JOB_ID
```

Copy code

```
client.get_job(job_id)
```

The object has the same shape as one element from the job list.

| Field | Meaning |
| --- | --- |
| `status` | Lifecycle such as `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`, or `CANCELLED`. |
| `reason` | Terminal or transition reason when set (for example, `cancelled_by_client`). |
| `sub_jobs` | Per worker group: `sub_job_id`, `job_type`, `model_name`, and configuration. |
| `created_at` / `updated_at` | UTC timestamps. |

Expand

Show lessSee more

Sub-job IDs use the pattern `job_id:type:index`. For example,
`JOB_ID:training:0` and `JOB_ID:sampling:0` on a colocated RL job.

## Wait for a job

CLIPython

Copy code

```
cortex-training wait JOB_ID
```

Copy code

```
client.wait_for_job(job_id)
```

The command or method blocks until the job reaches `RUNNING`. It raises an
error if the job reaches a terminal state first or the poll timeout expires.

## Checkpoints

CLIPython

Copy code

```
cortex-training checkpoints JOB_ID
```

Copy code

```
client.list_checkpoints(job_id)
```

The CLI wraps checkpoints in a `checkpoints` field, as shown here. The Python
method returns the list inside that field.

Copy code

```
{
  "checkpoints": [
    {
      "checkpoint_id": "cp_33158699-c227-4d5a-b7ba-cf1da92bfa8c",
      "created_at": "2026-06-17T20:51:40.783112791Z"
    }
  ]
}
```

Short runs, cancellations, or failures before the first save often return an
empty `checkpoints` array.

## Logs and metrics

Every job gets an experiment run in Snowflake ML Experiments, where training
metrics such as loss and learning rate are logged.

### Download execution logs

CLIPython

Copy code

```
cortex-training download-log JOB_ID --output-dir ./logs
```

The command writes one directory per sub-job under `--output-dir`.

Copy code

```
logs = client.fetch_execution_logs(job_id)
for item in logs:
    print(item["sub_job_id"], item["filename"])
```

Each entry contains `sub_job_id`, `filename`, `s3_uri`, and `content`.

Use `execution.jsonl` as the durable execution record. It contains structured
events such as operation names, durations, request and response sizes, and
errors. It is not a metrics export for reward, KL, GPU utilization, memory,
throughput, tokens per second, or MFU.

Downloads can be empty if the job ended before the log uploader registered or
no operations ran. Confirm the job status, then retry after the job has reached
training or sampling work.

### Stream live logs

CLIPython

Copy code

```
cortex-training tui JOB_ID
```

Run `cortex-training tui` without a job ID to open a job picker. Useful keys
include `/` to filter, `p` to pause, `s` to save visible logs, `r` to refresh,
and `q` to quit.

Copy code

```
for entry in client.stream_logs(job_id, follow=True):
    print(entry)
```

Live logs are available while the job is running. After the job ends, download
`execution.jsonl` for the durable record.

## Cancel, resume, and retry

### Cancel a job

CLIPython

Copy code

```
cortex-training cancel JOB_ID
```

Copy code

```
client.cancel_job(job_id)
```

The job details typically then show `status: CANCELLED` and
`reason: cancelled_by_client`.

### Resume from a checkpoint

To resume at job creation time, set `source_checkpoint_info` in the sub-job
configuration. To load a checkpoint into an existing running training job:

CLIPython

Copy code

```
cortex-training --job-id JOB_ID load CHECKPOINT_ID
```

To load from another job or select a target training sub-job:

Copy code

```
cortex-training --job-id JOB_ID load CHECKPOINT_ID --source-job-id SOURCE_JOB_ID
cortex-training --job-id JOB_ID load CHECKPOINT_ID --target-sub-job-id JOB_ID:training:0
```

Copy code

```
request_id = client.load(
    job_id,
    checkpoint_id,
    source_job_id=source_job_id,                # optional
    target_sub_job_id=f"{job_id}:training:0",   # optional
)
client.poll_request(job_id, request_id)
```

Changing data-parallel size (`n_gpus`) relative to the checkpoint requires
`load_optimizer_states=False` at job creation time. Optimizer state cannot be
reshaped at load time. Sampling sub-jobs are not valid load targets.

### Re-run after a failure

There is no one-click retry. Submit a new job with the same or adjusted
configuration. Use a saved checkpoint to continue instead of starting over.
