# Nov 18, 2026: Log mode for prompt injection guardrails

Prompt injection guardrails in [Cortex AI Guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails)
now support an optional `mode` setting in the `AI_SETTINGS` account parameter. Set `mode: LOG` to scan
and record possible prompt injections in CoCo, Snowflake CoWork, and Cortex Agents without changing
responses. Set `mode: BLOCK`, the default, to act on detections.

Use `LOG` mode to evaluate guardrails on your AI traffic before you block threats. Detections in `LOG`
mode appear in the [CORTEX\_AI\_GUARDRAILS\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_ai_guardrails_usage_history) view.

For more information, see [Set the guardrail mode](/user-guide/snowflake-cortex/cortex-ai-guardrails#label-cortex-ai-guardrails-mode).
