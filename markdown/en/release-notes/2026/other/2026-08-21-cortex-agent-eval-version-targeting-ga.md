# Aug 21, 2026: Version targeting for Cortex Agent and Cortex Analyst evaluations (*General availability*)

Cortex Agent and Cortex Analyst evaluations now let you control the versioned configuration used for scoring:

- **Cortex Agent version targeting** – The new `agent_version` key in the evaluation YAML `agent_params` block runs an evaluation against a specific agent version, alias, or shortcut, so a scheduled or CI/CD evaluation stays reproducible instead of tracking a mutable live version. You can also pick the version from a dropdown in Snowsight or through Cortex Code.
- **System metric versions** – All five system metrics accept a `version` key: `answer_correctness`, `logical_consistency`, `tool_selection_accuracy`, and `tool_execution_accuracy` for Cortex Agent evaluations, and `sql_correctness` for Cortex Analyst evaluations. A version pins the judge model along with the prompt, rubric, and thresholds behind a score. Versions `v2` and `v3` add GPT judges for accounts that don’t allow Anthropic models, and `v3` uses a 1M-token (`claude-sonnet-4-6`) or 1.05M-token (`openai-gpt-5.4`) context window, which reduces the odds of context window overload on long traces. Unversioned metrics use `v1` today and roll forward when that version is deprecated.
- **Cortex Agent custom metric judge models** – Custom metric definitions accept a `model` key that names the LLM judge for that metric. If you omit `model`, Snowflake uses `claude-4-sonnet` today and rolls forward when that model is deprecated.

Cortex Agent observability now also tracks the agent version per turn. The thread list marks threads that spanned more than one version, and the trace view shows the version that served each turn.

For more information, see [System metric versions](/user-guide/snowflake-cortex/cortex-agents-evaluations#label-agent-evaluation-metric-versions), [SQL correctness metric versions](/user-guide/snowflake-cortex/cortex-analyst-evaluations#label-analyst-evaluation-metric-versions), and [Agent versions in observability](/user-guide/snowflake-cortex/cortex-agents-monitor#label-cortex-agents-monitor-versions).
