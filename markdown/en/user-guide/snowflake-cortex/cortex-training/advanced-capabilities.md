# Advanced capabilities

[Preview Feature — Open](/release-notes/preview-features)

Available in all commercial Amazon Web Services (AWS) regions. Requires enablement.

These capabilities are useful once a basic SFT or RL loop works: steering what the model can emit,
making sampling cheaper, keeping very large requests reliable, replaying MoE routing between
sampling and training, and fitting very long sequences. For each one, this page explains the problem
it addresses, what the feature does, what you gain, and the smallest snippet that turns it on.

## Background: the RL fine-tuning loop in brief

Most of the capabilities below exist because of how reinforcement learning (RL) fine-tuning is
organized. If you already know this loop, skip to the first feature.

1. **Sample.** A sampler (an inference engine) generates responses, called rollouts, from the
   current model for a batch of prompts.
2. **Score.** Your code assigns each rollout a reward, for example whether an answer was correct or
   a tool call succeeded.
3. **Train.** A trainer (a training engine) recomputes the model’s probability for every token the
   sampler produced, then updates the weights so that higher-reward rollouts become more likely.
4. **Sync.** The updated weights are copied to the sampler and the loop repeats.

Two facts about this loop explain most of what follows:

- **The sampler and the trainer are different programs.** They run the same model, but with
  different kernels and numerics. In step 3 the trainer has to reproduce the probabilities the
  sampler actually used. Small disagreements add noise to learning. This is often called
  *training/sampling mismatch*.
- **Sampling is often a large share of the cost, and sequences can be long.** Responses are
  generated one token at a time, and agentic tasks build up long contexts. That puts pressure on
  both latency and GPU memory.

All snippets assume a connected client:

Copy code

```
from cortex_training import CortexTrainingClient, SubJobConfig

client = CortexTrainingClient.from_connection_name("training")
```

## Constrained decoding and action masks

### The problem

Language models produce free text. When an application needs structured output, such as a JSON
object, a tool call, or an answer in a fixed format, a model sometimes produces something that does
not parse: a missing brace, an extra field, or prose wrapped around the JSON. The usual workarounds
are to prompt more firmly or to retry until the output parses. Both cost time and compute, and
neither is a guarantee. In RL the cost is higher, because every malformed rollout is a sample you
paid for that earns no useful reward for a reason unrelated to the task itself.

### What it does

Constrained decoding changes how the sampler picks each next token. At every step the sampler
already scores every token in the vocabulary. With a constraint, tokens that would make the output
invalid under your schema are ruled out first, and the sampler chooses among the tokens that remain.
As long as generation completes within `max_tokens`, the result conforms to the schema.

The **action masks** are a record of those restrictions: for each constrained position, which tokens
were allowed.

### Why the masks matter for RL

When the sampler is restricted, the probability it effectively used for each chosen token is measured
over the allowed tokens only. A trainer that recomputes probabilities over the whole vocabulary gets
a different number for the same token, so it credits or blames the model using probabilities the
sampler never used. Returning the masks lets the trainer apply the same restriction when it
recomputes log-probabilities, so the two sides agree.

### Benefits

- Output that parses, without retry loops or after-the-fact repair.
- Less wasted RL sampling: rollouts fail because of the task, not the format.
- Sampler and trainer agree on token probabilities when the masks are used in the RL loss.

### When to use it

Tool-calling and structured-output agents, or any setup where the policy must produce a fixed
format.

### Example

Copy code

```
schema = {
    "type": "object",
    "properties": {"answer": {"type": "string"}},
    "required": ["answer"],
    "additionalProperties": False,
}

request_id = client.generate(
    job_id,
    prompts=[prompt],
    sampling_params={
        "max_tokens": 128,
        "temperature": 0.0,
        "structured_outputs": {"json": schema},
        "return_action_masks": True,
    },
)
sample = client.poll_request(job_id, request_id)["results"][0]
sample["text"]          # '{"answer": "Paris"}'
sample["action_masks"]  # sparse description of the allowed tokens per position
```

`action_masks` is a dictionary with `seq_len`, `vocab_size`, the constrained positions, and the
allowed or denied token sets for those positions (`set_indices`, `set_modes_allow`, `set_offsets`,
`token_ids`). Without `structured_outputs` the same prompt is free to ignore your schema.

Where the masks take effect in training

The trainer applies action masks in the RL loss path: a `forward_backward` request that carries a
processing block on a job using the chunked LM head. A plain supervised request (labels only)
accepts the masks but does not use them. Pass them as a per-row list, one entry per sample in the
batch.

## Speculative decoding

### The problem

A language model produces text one token at a time, and every token needs a full pass through the
model. For large models that pass is limited by how fast the weights can be read from GPU memory,
not by arithmetic, so the GPU’s compute sits mostly idle while it waits for each token. Latency
grows with output length, and an RL sampler has to produce many long responses at every step.

### What it does

Speculative decoding adds a small, fast draft model that guesses the next several tokens. The large
target model then checks all of the guesses in a single pass: it keeps the longest run of guesses it
agrees with and corrects the first one it does not. Because the target model has the final say on
every token, the output follows the same distribution the target model would produce on its own. You
get the same quality, faster, when the draft guesses well.

### Benefits

- Lower latency and higher sampling throughput for the same model.
- No change to the training side: only the sampler is faster.
- In one check on a 27B model, throughput roughly doubled (see the notes below). The gain depends
  on how often the draft’s guesses are accepted, which is highest on predictable text.

### When to use it

Sampling-heavy workloads where generation, not training, dominates wall-clock time, such as long
rollouts or evaluation sweeps.

### Example

Enable it on the sampling sub-job with `vllm_config.speculative_config`. Pass the draft model as an
`<org>/<model>` Hub ID, the same convention as `model_name`:

Copy code

```
sampling = SubJobConfig.sampling_job(
    model_name="Qwen/Qwen3.8-27B",
    max_seq_len=16384,
    n_gpus=8,
    extra_sampling={
        "vllm_config": {
            "tensor_parallel_size": 1,
            "gpu_memory_utilization": 0.85,
            "speculative_config": {
                "method": "dflash",
                "model": "z-lab/Qwen3.8-27B-DFlash2",
                "num_speculative_tokens": 7,
            },
        },
    },
)
```

Performance notes

The draft model must be compatible with the target model. In one check on this model (one H200,
eight prompts, greedy decoding, 256 new tokens) throughput roughly doubled, from about 380 to 760
tokens per second. Seven of the eight outputs were identical to the run without speculation; the
eighth differed slightly, which small numerical differences can cause even when the distribution is
preserved. Measure on your own prompts before relying on a speedup.

## Large requests: automatic chunking

### The problem

RL and long-context training send large tensors to the service: many sequences, each tens of
thousands of tokens long, can add up to hundreds of megabytes for one batch. A single request that
large is fragile. It can hit size limits, time out part-way, or fail after the server has already
started work. And when a client retries after a failure, a naive retry can apply the same training
step twice, which quietly corrupts a run.

### What it does

The client splits large batches into chunks, verifies each one with a SHA-256 digest, and
reassembles large results the same way. You do not call anything extra.

- `forward_backward` always sends a chunk envelope (up to 60 MiB per chunk), so every call has an
  identity the server can use to recognize a retry.
- `generate` sends the frame unchanged when it fits and splits it above 60 MiB.
- `generate_stream` is not chunked; its body must stay under 60 MiB.

### Benefits

You can send whole batches without splitting them yourself. Corrupted or mismatched payloads are
detected by the digests, and transient network failures are retried automatically.

**Retries are safe.** Repeating a `forward_backward` chunk group with the same ID and content
returns the original result instead of starting a second execution. Reusing a group ID with
different content is rejected.

### Example

Copy code

```
import logging
from cortex_training import ChunkGroupError

log = logging.getLogger(__name__)

try:
    request_id = client.forward_backward(job_id, payload)  # any size
    result = client.poll_request(job_id, request_id)
except ChunkGroupError as err:
    log.error("chunked request failed: %s", err.detail)
    raise
```

A conflicting reuse raises `ChunkGroupConflictError` with
`detail["code"] == "chunk_group_conflict"`; a group that must restart from the first chunk raises
`ChunkGroupRestartError`. The client replays once on its own before raising the latter.

## MoE router replay

### The problem

Many recent large models are mixture-of-experts (MoE) models. Instead of sending every token through
the whole network, a small router in each layer picks a few specialist sub-networks, called experts,
for each token. In RL the sampler and the trainer both run the model, but with different software and
numerics, and the router’s choice can flip for the same token when two experts score almost the same.
If the trainer sends a token through different experts than the sampler did, it is no longer training
the computation that produced the data. A rollout contains many routing decisions, so small
disagreements add up, and the probabilities the trainer computes drift away from the ones the sampler
used.

### What it does

Router replay records which experts the router chose for each token during sampling, ships those
choices to the trainer, and has the trainer use them instead of routing for itself. The transfer
happens directly between sampling replicas and training ranks over NCCL, and each side keeps a
bounded cache so memory stays predictable.

### Benefits

- The trainer evaluates the same computation the sampler ran, removing a source of
  training/sampling mismatch that is specific to MoE models. This is intended to make RL on MoE
  models more stable.
- `best_effort` mode keeps training going when some rows have no recorded routing, and reports how
  many rows were replayed versus routed fresh.
- The cost is memory for the routing cache, which you size (see below).

### When to use it

RL on MoE models, where sampler and trainer would otherwise route differently.

### Example

Enable it on both sub-jobs. Start from the catalog profile for your model (for example
`moe-long-rl-lora-8x8`) for parallelism and LM-head settings, and add the `router_replay` blocks:

Copy code

```
training = SubJobConfig.training_job(
    model_name="Qwen/Qwen3.6-35B-A3B",
    optimizer={"name": "AdamW", "lr": 1e-4},
    max_seq_len=4096,
    train_batch_size=1,
    n_gpus=8,
    extra_training={
        # ... model_provider, sp_size, ep_size, etc. from the catalog profile ...
        "router_replay": {
            "enabled": True,
            "mode": "best_effort",  # or "strict" (default)
            "max_cache_bytes": 2 * 1024**3,
        },
    },
)
sampling = SubJobConfig.sampling_job(
    model_name="Qwen/Qwen3.6-35B-A3B",
    max_seq_len=4096,
    n_gpus=8,
    extra_sampling={
        "router_replay": {"enabled": True, "max_cache_bytes": 16 * 1024**3},
        "vllm_config": {"tensor_parallel_size": 8, "gpu_memory_utilization": 0.8},
    },
)

job_id = client.create_job(sub_jobs=[training, sampling])
client.wait_for_job(job_id)
training_id, sampling_id = f"{job_id}:training:0", f"{job_id}:sampling:0"
```

After creating the job, bootstrap the replay connection between sub-jobs:

Copy code

```
info = client.bootstrap_router_replay(
    job_id,
    source_sub_job_id=sampling_id,
    target_sub_job_id=training_id,
    sub_job_id=training_id,
    sub_job_type="training",
    max_cache_bytes=2 * 1024**3,
)
assert info["status"] == "ok"
```

Tag each sample with an ID when you generate it, so its routing is kept:

Copy code

```
params = [
    {"max_tokens": 256, "temperature": 1.0, "dss_sample_id": sid}
    for sid in sample_ids
]
request_id = client.generate(
    job_id, prompts=prompt_token_ids, sampling_params=params
)
rollouts = client.poll_request(job_id, request_id)["results"]
```

Then name the same IDs in the training request, together with the sampling sub-job that holds them:

Copy code

```
from cortex_training import wire

frame = wire.dumps(
    {
        "args": (),
        "kwargs": kwargs,
        "rr_sample_ids": sample_ids,
        "rr_discard": False,
    },
    metadata={
        "response_options": {"format": "dssst1", "delivery": "chunked"},
        "router_replay": {"sampling_job_id": sampling_id},
    },
)
result = client.poll_request(
    job_id, client.forward_backward(job_id, frame)
)
result["metrics"]["router_replay/rows_replayed"]
```

Release samples you will not train on so they stop occupying cache:

Copy code

```
client.router_replay_discard(
    job_id,
    ["sample-0001"],
    sub_job_id=sampling_id,
    sub_job_type="sampling",
)
```

### Choosing a mode

`strict` (the default) fails a training request if any row’s routing is missing, for example because
the sampler restarted after producing it. `best_effort` routes those rows with the trainer’s own
gate, replays the rest, and reports the split in the request’s metrics: `router_replay/rows_sent`,
`rows_replayed`, `rows_fresh`, `replayed_fraction`, `tokens_replayed`, and `tokens_fresh`. A
discarded or unknown ID is treated as a row without routing.

### Sizing the cache

One replay entry costs `seq_len * num_moe_layers * top_k` bytes. Size the sampling cache for the
busiest replica’s backlog of unconsumed rollouts, and the training cache for the rows resident on one
data-parallel shard, each with headroom. The sampling cache reports its occupancy and its evictions
(`n_evicted_lru`, `n_evicted_ttl`) in the response to a discard call, so you can see whether it is
too small.

### String stop sequences

When router replay is active, string stop values are rejected. Pass token-ID sequences as
`dss_stop_token_sequences` instead:

Copy code

```
stop_ids = [
    tokenizer.encode(s, add_special_tokens=False) for s in ["\n\n"]
]
params = {
    "max_tokens": 256,
    "dss_sample_id": sid,
    "dss_stop_token_sequences": stop_ids,
}
```

## Long-sequence training

### The problem

Agentic and reasoning tasks produce long sequences: long documents, tool outputs, multi-turn
histories, and long chains of thought, often tens or hundreds of thousands of tokens. Training on
them is limited by GPU memory for two reasons. The activations kept for the backward pass grow with
sequence length. And the output layer scores every token against the whole vocabulary, so its logits
tensor is enormous: in a test of a 196,608-token sequence, an unchunked output layer tried to
allocate 22.7 GiB in one piece and the job ran out of memory.

### What it does

Three techniques work together:

- **Sequence parallelism** (`sp_size`) splits each sample’s sequence across `sp_size` GPUs, so
  activation memory per GPU drops roughly by that factor.
- **A chunked LM head** computes the output layer in slices instead of materializing the full
  logits tensor.
- **CPU activation offload** keeps activations in host memory between the forward and backward
  passes, and an allocator setting reduces fragmentation.

### Benefits

You can train on much longer contexts without moving to larger GPUs or truncating your data. With
the configuration below, a single 196,608-token sequence fit on one 8xH200 node.

### When to use it

When a single sample no longer fits in memory. Sequence parallelism does not make a step cheaper:
the FLOPs are the same and it adds communication between GPUs, and offload can slow steps once the
copies stop overlapping with compute. Take the smallest `sp_size` that fits, and keep it at or below
the GPUs per node.

### Example

Copy code

```
training = SubJobConfig.training_job(
    model_name="Qwen/Qwen3.8-27B",
    optimizer={"name": "AdamW", "lr": 1e-5},
    max_seq_len=196608,
    train_batch_size=1,
    n_gpus=8,
    extra_training={
        "sp_size": 8,
        "fused_lm_head_token_chunk_size": 8192,
        "fused_cross_entropy": False,  # required with a chunked LM head
        "ac_config": {"mode": "full", "offload_config": {"enabled": True}},
        "cuda_allocator_conf": "expandable_segments:True",
    },
)
```

With this configuration a single 196,608-token sequence completed a forward/backward pass on one
8xH200 node in about two and a half minutes for the first call. Without the chunked LM head the same
request ran out of memory while allocating the logits.

Constraints

- `n_gpus` must be divisible by `sp_size`, and `sp_size` must divide the model’s attention-head
  count.
- CPU activation offload requires `ac_config.mode="full"`.
- The client rejects a chunked LM head unless `fused_cross_entropy` is `False`.
- The [model catalog](/user-guide/snowflake-cortex/cortex-training/models) lists long-sequence
  profiles for supported models.
