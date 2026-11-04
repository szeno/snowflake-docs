# Nov 3, 2026: Cortex AI Gateway inference, observability, and cost management (*General availability*)

Inference, observability, and cost management for Cortex AI Gateway are now generally available. The
gateway gives AI clients in your organization one governed endpoint to reach models, records a trace of
every request, and attributes spend to the users who made it.

The following capabilities are now generally available:

- Inference: send requests to the gateway endpoint in the OpenAI Chat Completions or Anthropic Messages
  API format, from the official SDKs or a coding agent. See
  [Inference with Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/inference).
- Observability: query the spans for each request, including the models called, timing, token counts,
  and errors, with `AGENT_TRACE_TABLE`. Client applications can also export their own OpenTelemetry
  traces to the gateway. See [Observability for Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/observability).
- Cost management: report on spend with the
  [AI\_GATEWAY\_USAGE\_HISTORY](/sql-reference/account-usage/ai_gateway_usage_history) view, track spend by
  team with [shared resource budgets](/user-guide/budgets/budget-shared-resources#label-budget-shared-resource-ai-gateway),
  and block individual users at a limit with
  [per-user quotas](/user-guide/budgets/per-user-quotas#label-per-user-quota-ai-gateway). See
  [Cost management for Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/cost-management).

This release also adds trace analytics, in preview. On the **Analytics** tab of the gateway’s
Observability page in Snowsight, you can chart model usage, request failures and latency, MCP tool calls, and
conversation length from the trace table without writing SQL. See
[Trace analytics for Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/observability/trace-analytics).

[Tools for Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/tools) remains in preview.

To get started, sign in to Snowsight and select **AI Gateway** in the navigation menu. For more
information, see [Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway).
