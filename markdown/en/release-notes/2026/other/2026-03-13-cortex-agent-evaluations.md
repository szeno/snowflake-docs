# Mar 13, 2026: Cortex Agent evaluations (*General availability*)

Snowflake now offers Cortex Agent evaluations that allow you to monitor your agent’s behavior and performance. Evaluate your agent against both ground truth-based and reference-free evaluation metrics. During evaluation, your agent’s activity is traced and monitored so you can ensure that each step in the process advances towards your end goal.

Snowflake offers the following metrics to evaluate your agent against:

- **Answer correctness** – How closely the answer from an agent to your prepared query matches an expected answer. This metric is most useful when the dataset powering your Cortex Agent is static.
- **Logical consistency** – Measures consistency across agent instructions, planning, and tool calls. This metric is *reference-free*, meaning you don’t need to prepare any information in your dataset for evaluation.
- **Custom metrics** – Snowflake also allows you to create custom metrics. By defining a prompt and scoring system, you can take advantage of the LLM judging process to perform additional consistency checks or compliance with domain-specific requirements.

For information on how to create and run a Cortex Agent evaluation, see [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations).
