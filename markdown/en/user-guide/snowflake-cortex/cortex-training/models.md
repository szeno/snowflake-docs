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
full-parameter profiles when both are available. For models with standard and long-context
profiles, use the **Enable long sequence** checkbox to switch between the model’s two
context tiers. The profiles can differ in job topology and distributed training settings,
not only in the PEFT configuration. Tune batch sizes and optimization parameters for your
workload.

Note

Model availability and specifications are subject to change during the preview.

## Available for training

These open weights models support fine-tuning. They also support inference.

Important

Saving and loading LoRA checkpoints for `Qwen/Qwen3.6-35B-A3B` requires the
`arctic` model provider. LoRA for this mixture-of-experts model currently supports the
attention projections (`q_proj`, `k_proj`, `v_proj`, and `o_proj`). Routed expert LoRA is
not yet supported. The Hugging Face MLP names `gate_proj`, `up_proj`, and `down_proj` do
not select routed expert parameters in the model implementation used by the `arctic`
provider.

### DeepSeek-V4.1-Flash-1017

`deepseek-ai/DeepSeek-V4.1-Flash-1017`Copy ID

License: [MIT](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017/blob/main/LICENSE)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

LoRA 256K max · Full 256K max

View recommended configurations

### gemma-3-4b-it

`google/gemma-3-4b-it`Copy ID

License: [Gemma](https://ai.google.dev/gemma/terms)

InferenceSupported

128K max · 8 GPUs

TrainingSupported

Full 128K max

View recommended configurations

### gemma-4-31B-it

`google/gemma-4-31B-it`Copy ID

License: [Gemma](https://ai.google.dev/gemma/terms)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

Full 256K max

View recommended configurations

### GLM-5.3-Flash

`zai-org/GLM-5.3-Flash`Copy ID

License: [MIT](https://huggingface.co/zai-org/GLM-5.3-Flash/blob/main/LICENSE)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

LoRA 256K max

View recommended configurations

### GLM-5.3-Flash-BF16

`zai-org/GLM-5.3-Flash-BF16`Copy ID

License: [MIT](https://huggingface.co/zai-org/GLM-5.3-Flash-BF16/blob/main/LICENSE)

InferenceSupported

256K max · 16 GPUs

TrainingSupported

Full 256K max

View recommended configurations

### medgemma-1.5-4b-it

`google/medgemma-1.5-4b-it`Copy ID

License: [Health AI Developer Foundations](https://developers.google.com/health-ai-developer-foundations/terms)

InferenceSupported

128K max · 8 GPUs

TrainingSupported

Full 128K max

View recommended configurations

### medgemma-4b-it

`google/medgemma-4b-it`Copy ID

License: [Health AI Developer Foundations](https://developers.google.com/health-ai-developer-foundations/terms)

InferenceSupported

128K max · 8 GPUs

TrainingSupported

Full 128K max

View recommended configurations

### NVIDIA-Nemotron-3-Nano-30B-A3B-BF16

`nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16`Copy ID

License: [NVIDIA Nemotron Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-nemotron-open-model-license/)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

Full 256K max

View recommended configurations

### NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16

`nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16`Copy ID

License: [OpenMDW-1.1](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16/blob/main/LICENSE)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

Full 256K max

View recommended configurations

### Qwen3-0.6B

`Qwen/Qwen3-0.6B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3-0.6B/blob/main/LICENSE)

InferenceSupported

32K max · 1 GPU

TrainingSupported

LoRA 32K max · Full 32K max

View recommended configurations

### Qwen3-1.7B

`Qwen/Qwen3-1.7B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3-1.7B/blob/main/LICENSE)

InferenceSupported

32K max · 8 GPUs

TrainingSupported

LoRA 32K max · Full 32K max

View recommended configurations

### Qwen3-30B-A3B

`Qwen/Qwen3-30B-A3B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3-30B-A3B/blob/main/LICENSE)

InferenceSupported

40K max · 8 GPUs

TrainingSupported

Full 40K max

View recommended configurations

### Qwen3-4B-Instruct-2507

`Qwen/Qwen3-4B-Instruct-2507`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507/blob/main/LICENSE)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

Full 256K max

View recommended configurations

### Qwen3-8B

`Qwen/Qwen3-8B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE)

InferenceSupported

32K max · 2 GPUs

TrainingSupported

LoRA 32K max · Full 32K max

View recommended configurations

### Qwen3.5-2B

`Qwen/Qwen3.5-2B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3.5-2B/blob/main/LICENSE)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

LoRA 256K max · Full 256K max

View recommended configurations

### Qwen3.5-4B

`Qwen/Qwen3.5-4B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3.5-4B/blob/main/LICENSE)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

LoRA 256K max · Full 256K max

View recommended configurations

### Qwen3.5-9B

`Qwen/Qwen3.5-9B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3.5-9B/blob/main/LICENSE)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

LoRA 64K max · Full 256K max

View recommended configurations

### Qwen3.6-35B-A3B

`Qwen/Qwen3.6-35B-A3B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3.6-35B-A3B/blob/main/LICENSE)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

LoRA 256K max · Full 256K max

View recommended configurations

### Qwen3.8-27B

`Qwen/Qwen3.8-27B`Copy ID

License: [Apache 2.0](https://huggingface.co/Qwen/Qwen3.8-27B/blob/main/LICENSE)

InferenceSupported

256K max · 8 GPUs

TrainingSupported

LoRA 256K max · Full 256K max

View recommended configurations

## Inference only

These models support inference (sampling) but not fine-tuning.

### GLM-5.3

`zai-org/GLM-5.3`Copy ID

License: [GLM-5.3 License](https://huggingface.co/zai-org/GLM-5.3/blob/main/LICENSE)

InferenceSupported

704K max · 8 GPUs

TrainingNot supported

View recommended configurations

### gpt-oss-120b

`openai/gpt-oss-120b`Copy ID

License: [Apache 2.0](https://huggingface.co/openai/gpt-oss-120b/blob/main/LICENSE)

InferenceSupported

128K max · 8 GPUs

TrainingNot supported

View recommended configurations
