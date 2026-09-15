# Jun 16, 2026: Account Usage New CORTEX\_AI\_GUARDRAILS\_USAGE\_HISTORY view

The ACCOUNT\_USAGE schema now includes a new
[CORTEX\_AI\_GUARDRAILS\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_ai_guardrails_usage_history)
view that provides visibility into the usage history of
[Cortex AI Guardrails](/user-guide/snowflake-cortex/cortex-ai-guardrails).

The information in the view includes guardrail scan results, credit and token consumption, and
whether any scan was flagged. Each row represents a single guardrail scan for one tool use within
an agent request. A request with multiple tool results produces multiple rows, one per tool use
scanned. Each row includes the agentic source (Cortex Code, Snowflake Intelligence, or Cortex
Agents), granular token and credit breakdowns, and metadata such as the role used.

For more information, see [CORTEX\_AI\_GUARDRAILS\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_ai_guardrails_usage_history).
