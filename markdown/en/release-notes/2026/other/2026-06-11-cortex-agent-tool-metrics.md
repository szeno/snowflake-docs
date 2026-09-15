# Jun 11, 2026: Cortex Agent tool evaluation metrics (*Preview*)

With this preview release, Cortex Agent evaluations include two new system metrics that measure how your agent uses tools:

- **Tool selection accuracy (TSA)** – Whether the agent’s orchestration layer invokes the tools you expect for a given query.
- **Tool execution accuracy (TEA)** – Whether each tool that runs receives appropriate input and returns output that meets your requirements.

You provide expected tool calls in your evaluation dataset through the `ground_truth_invocations` key, and enable the metrics in the Agent Evaluation YAML or with the system metric toggles in Snowsight.

For more information, see [Tool selection and execution metrics ground truth](/user-guide/snowflake-cortex/cortex-agents-evaluations#label-cortex-agent-evaluation-tool-metrics).
