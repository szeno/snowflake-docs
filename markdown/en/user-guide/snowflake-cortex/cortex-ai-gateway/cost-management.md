# Cost management for Cortex AI Gateway

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in Amazon Web Services (AWS) commercial regions only, excluding Asia Pacific (New Zealand), Asia Pacific (Malaysia), and Europe (Spain). For the full list of AWS commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

The gateway is a natural unit for cost reporting: inference requests from external agents and AI
clients land in a unified, governed source of truth, with attribution to the Snowflake user who made
each request. This topic covers how to see what the gateway is spending and how to limit it.

## Monitor gateway usage

Query [AI\_GATEWAY\_USAGE\_HISTORY view](/sql-reference/account-usage/ai_gateway_usage_history) for per-request detail, including
the gateway, user, model, and token counts. This is the view to use for showback, adoption reporting,
and identifying which applications drive spend.

## Choose a spending control

Snowflake offers two controls for gateway spend. They differ in what they scope and what actions
can be performed once a threshold is reached.

| Control | Scope | Enforcement | Use it when |
| --- | --- | --- | --- |
| [Shared resource budget](/user-guide/budgets/budget-shared-resources#label-budget-shared-resource-ai-gateway) | A group of users identified by a tag, pooled | Notification, plus stored procedures you write | Several teams share the gateway and each needs its own limit. |
| [Per-user quota](/user-guide/budgets/per-user-quotas#label-per-user-quota-ai-gateway) | Each user individually. Limits are never pooled. | Built-in blocking, applied within minutes | You need usage to actually stop, not just alert. |

Expand

Show lessSee more

Budget evaluation is periodic, so spend can pass a threshold before an action runs: up to 6.5 hours, or
one hour with the low-latency option. Quota blocks apply within minutes.

## Set up a control

- To budget by team or cost center, see
  [Add the AI Gateway](/user-guide/budgets/budget-shared-resources#label-budget-shared-resource-ai-gateway).
- To block individual users at a limit, see [Add the AI Gateway](/user-guide/budgets/per-user-quotas#label-per-user-quota-ai-gateway).

For how gateway cost management fits alongside other Cortex AI features, see
[AI cost management and governance](/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance).
