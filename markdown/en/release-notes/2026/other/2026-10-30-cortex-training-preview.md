# Oct 30, 2026: Cortex Training (*Preview*)

Cortex Training is now available in preview. Cortex Training is a serverless service for customizing
open-weight large language models. You run your training loop from your own workspace, and Snowflake
runs the GPU work: forward and backward passes, optimizer steps, and generation. You don’t need to
provision GPU clusters or manage training infrastructure, and your training data stays in Snowflake.

With Cortex Training, you can do the following:

- Run supervised fine-tuning (SFT) and reinforcement learning (RL) with LoRA or full-parameter
  training, using the Python client or popular open-source training frameworks.
- Save checkpoints, resume training from them, and run inference against them.
- Deploy a base model or a fine-tuned checkpoint to an OpenAI-compatible endpoint and stream chat
  completions from it.

Cortex Training is billed in AI Credits for on-demand GPU usage, metered per second.

This feature is available only in commercial Amazon Web Services (AWS) regions and requires
enablement. To enable Cortex Training, contact your account team.

For more information, see [Cortex Training](/user-guide/snowflake-cortex/cortex-training).
