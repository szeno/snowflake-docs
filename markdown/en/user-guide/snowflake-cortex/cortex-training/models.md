# Cortex Training models

[Preview Feature — Open](/release-notes/preview-features)

Available in all commercial Amazon Web Services (AWS) regions. Requires enablement.

Cortex Training supports a curated set of third-party, open models. Use the canonical model ID (for
example, `Qwen/Qwen3-8B`) as the `model_name` when you create a job. Copy a model ID
directly from any card below.

Each card shows whether **inference** and **training** are supported. For supported
training models, the card summarizes the maximum context length for **LoRA (low-rank
adaptation)** and **full-parameter** training.

Select **View recommended configurations** on a card for a copyable Python starting
configuration. Select supervised fine-tuning (SFT) or reinforcement learning (RL), then
use the **Use LoRA** checkbox to switch between the complete recommended LoRA and
full-parameter profiles. For models with a long-context profile, use the **Enable long
sequence** checkbox to switch from the standard sequence length with sequence parallelism
set to 1 to the maximum sequence length with sequence parallelism set to 8. The profiles
can differ in job topology and distributed training settings, not only in the PEFT
configuration. Tune batch sizes and optimization parameters for your workload.

Note

Model availability and specifications are subject to change during the preview.

## Available for training

These open weights models support fine-tuning. They also support inference.

Important

Saving and loading LoRA checkpoints for `Qwen/Qwen3.6-35B-A3B` requires the
`prime_rl` model provider. LoRA for this mixture-of-experts model currently supports the
attention projections (`q_proj`, `k_proj`, `v_proj`, and `o_proj`). Routed expert LoRA is
not yet supported. The Hugging Face MLP names `gate_proj`, `up_proj`, and `down_proj` do
not select routed expert parameters in the model implementation used by the `prime_rl`
provider.

### Qwen3 0.6B

`Qwen/Qwen3-0.6B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3-0.6B/blob/main/LICENSE)

InferenceSupported

32K max · 8 GPUs

TrainingSupported

LoRA 32K max · Full 32K max

View recommended configurations

### Qwen3 1.7B

`Qwen/Qwen3-1.7B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3-1.7B/blob/main/LICENSE)

InferenceSupported

32K max · 8 GPUs

TrainingSupported

LoRA 32K max · Full 32K max

View recommended configurations

### Qwen3 8B

`Qwen/Qwen3-8B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE)

InferenceSupported

32K max · 8 GPUs

TrainingSupported

LoRA 32K max · Full 32K max

View recommended configurations

### Qwen3.5 4B

`Qwen/Qwen3.5-4B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3.5-4B/blob/main/LICENSE)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

LoRA 256K max · Full 256K max

View recommended configurations

### Qwen3.6 35B-A3B

`Qwen/Qwen3.6-35B-A3B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3.6-35B-A3B/blob/main/LICENSE)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

LoRA 256K max · Full 256K max

View recommended configurations

### Qwen3.8 27B

`Qwen/Qwen3.8-27B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3.8-27B/blob/main/LICENSE)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

LoRA 256K max · Full 256K max

View recommended configurations

## Inference only

These models support inference (sampling) but not fine-tuning.

### DeepSeek V4 Flash

`deepseek-ai/DeepSeek-V4-Flash-0731`Copy ID

License: [MIT](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/main/LICENSE)

InferenceSupported

1024K max · 8 GPUs

TrainingNot supported

View recommended configurations

### GPT-OSS 120B

`openai/gpt-oss-120b`Copy ID

License: [Apache 2.0](https://huggingface.co/openai/gpt-oss-120b/blob/main/LICENSE)

InferenceSupported

128K max · 8 GPUs

TrainingNot supported

View recommended configurations

### GLM 5.2

`zai-org/GLM-5.2`Copy ID

License: [MIT](https://huggingface.co/zai-org/GLM-5.2/blob/main/LICENSE)

InferenceSupported

32K max · 16 GPUs

TrainingNot supported

View recommended configurations

### GLM 5.2 FP8

`zai-org/GLM-5.2-FP8`Copy ID

License: [MIT](https://huggingface.co/zai-org/GLM-5.2-FP8/blob/main/LICENSE)

InferenceSupported

1024K max · 16 GPUs

TrainingNot supported

View recommended configurations
