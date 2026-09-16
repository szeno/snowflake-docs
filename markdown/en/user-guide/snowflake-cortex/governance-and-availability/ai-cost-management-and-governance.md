# AI cost management and governance

Snowflake gives you a consistent way to understand, monitor, and manage AI usage alongside the rest of your platform activity. Across AI features, pricing is primarily based on consumption, including token-based usage where applicable, so teams can align spend to actual usage instead of fixed capacity. To support cost transparency, Cortex AI provides usage views that help you analyze activity over time, break down consumption, and connect usage to billing workflows already used across your organization. These views can be used for reporting, governance, showback, and internal monitoring. For detailed pricing by feature, model, and unit of consumption, refer to the [consumption table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf), which provides the current pricing structure across Snowflake AI capabilities.

## Usage views

Snowflake provides account usage views and organization usage views to help you track AI consumption using the same core approach used across the platform. These views support analysis of usage over time and can help teams understand how AI activity maps to overall spend, whether they are monitoring adoption, reviewing trends, or supporting internal reporting. This allows finance, platform, and engineering teams to work from a common system of record when evaluating usage. Pricing details remain available in the [consumption table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf), which outlines how individual AI features are billed. Together, usage views and pricing documentation provide a foundation for understanding and managing AI costs across your Snowflake environment.

Tip

In [Cortex Code](/user-guide/cortex-code/cortex-code), including the [CLI](/user-guide/cortex-code/cortex-code-cli), [Desktop](/user-guide/cortex-code/cortex-code-desktop), and [Snowsight](/user-guide/cortex-code/cortex-code-snowsight) interfaces, you can use the [`cost-intelligence`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-cost-intelligence) bundled skill to analyze AI usage and costs across Cortex features. Invoke the skill with `/cost-intelligence`, or describe your question in plain language and Cortex Code selects the skill automatically.

### Usage views for total cost

These views should be used when calculating AI usage and AI-related spend. Together, they provide the standard foundation for cost reporting across AI features.

| Name | Available in | SERVICE\_TYPE | Time Zone | Units | DATES |
| --- | --- | --- | --- | --- | --- |
| [AI\_GATEWAY\_USAGE\_HISTORY](/sql-reference/account-usage/ai_gateway_usage_history) | ACCOUNT\_USAGE, [ORGANIZATION\_USAGE](/sql-reference/organization-usage/ai_gateway_usage_history) | AI\_INFERENCE | UTC Converted to local [1] | Tokens | [Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open  Available to all accounts. |
| [CORTEX\_AGENT\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_agent_usage_history) | ACCOUNT\_USAGE, [ORGANIZATION\_USAGE](/sql-reference/organization-usage/cortex_agent_usage_history) | CORTEX\_AGENTS | UTC Converted to local [1] | Tokens, Tools | Data begins 11/10/2025 |
| [CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_ai_functions_usage_history) | ACCOUNT\_USAGE, [ORGANIZATION\_USAGE](/sql-reference/organization-usage/cortex_ai_functions_usage_history) | AI\_FUNCTIONS | UTC Converted to local [1] | Tokens | Data begins 1/5/2026 |
| [CORTEX\_CODE\_CLI\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_code_cli_usage_history) | ACCOUNT\_USAGE, [ORGANIZATION\_USAGE](/sql-reference/organization-usage/cortex_code_cli_usage_history) | CORTEX\_CODE\_CLI | UTC | Tokens, Tools | Data begins 2/16/2026 |
| [CORTEX\_CODE\_SNOWSIGHT\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_code_snowsight_usage_history) | ACCOUNT\_USAGE, [ORGANIZATION\_USAGE](/sql-reference/organization-usage/cortex_code_snowsight_usage_history) | CORTEX\_CODE\_SNOWSIGHT | UTC | Tokens, Tools | Data begins 3/13/2026, billing begins 4/1/2026 |
| [SNOWFLAKE\_COCO\_USAGE\_HISTORY](/sql-reference/account-usage/snowflake_coco_usage_history) | ACCOUNT\_USAGE, [ORGANIZATION\_USAGE](/sql-reference/organization-usage/snowflake_coco_usage_history) | SNOWFLAKE\_COCO | UTC | Tokens, Tools |  |
| [CORTEX\_ANALYST\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_analyst_usage_history) | ACCOUNT\_USAGE | AI\_SERVICES | UTC Converted to local [1] | Messages | 365 days of data |
| [CORTEX\_FINE\_TUNING\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_fine_tuning_usage_history) | ACCOUNT\_USAGE | AI\_SERVICES | UTC Converted to local [1] | Fine-tuning time | 365 days of data |
| [CORTEX\_PROVISIONED\_THROUGHPUT\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_provisioned_throughput_usage_history) | ACCOUNT\_USAGE | AI\_SERVICES | UTC | PTU Hours | 365 days of data |
| [CORTEX\_SEARCH\_DAILY\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_search_daily_usage_history) [2] | ACCOUNT\_USAGE | CORTEX\_SEARCH, CORTEX\_SEARCH\_BATCH | Local | Serving time, Tokens | 365 days of data |
| [SNOWFLAKE\_COWORK\_USAGE\_HISTORY](/sql-reference/account-usage/snowflake_cowork_usage_history_view) | ACCOUNT\_USAGE, [ORGANIZATION\_USAGE](/sql-reference/organization-usage/snowflake_cowork_usage_history) | SNOWFLAKE\_INTELLIGENCE | UTC Converted to local [1] | Tokens, Tools | Data begins 11/10/2025 |
| [CORTEX\_REST\_API\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_rest_api_usage_history) | ACCOUNT\_USAGE | AI\_INFERENCE | UTC | Tokens (note: in currency) | Data begins 11/1/2025 |
| [CORTEX\_AI\_GUARDRAILS\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_ai_guardrails_usage_history) | ACCOUNT\_USAGE | CORTEX\_AI\_GUARDRAILS | UTC | Tokens | Data begins 4/8/2026 |

Expand

Show lessSee more

[1] UTC Converted to local means if your account is altered to local time it will display in local time. The underlying data is still in UTC.

[2] CORTEX\_SEARCH\_DAILY\_USAGE\_HISTORY includes embeddings which need to be excluded from combined calculations as they are also shown in CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY.

### Usage views for additional analysis

Use these views when you need more granular or feature-specific insight. They complement the primary views, but are not intended to serve as the standard source for AI cost totals.

| Name | Service Type | Time Zone | Dates | Notes |
| --- | --- | --- | --- | --- |
| [CORTEX\_SEARCH\_SERVING\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_search_serving_usage_history) | AI\_SERVICES | UTC  Converted to local [1] | 365 days of data | This credit total includes the embedding costs captured in CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY. |
| CORTEX\_SEARCH\_BATCH\_QUERY\_USAGE\_HISTORY | AI\_SERVICES | UTC  Converted to local [1] | Data begins on 3/26/2026 | This credit total includes the embedding costs captured in CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY. |
| [CORTEX\_AISQL\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_aisql_usage_history) | AI\_SERVICES |  | Data starts on 11/21/2025 | Slated for deprecation on 1/15/2027  This view includes totals of all functions except AI\_EXTRACT. |
| [CORTEX\_DOCUMENT\_PROCESSING\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_document_processing_usage_history) | AI\_SERVICES |  | 365 days of data | Slated for deprecation on  This view includes document processing now captured in CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY. |
| [CORTEX\_FUNCTIONS\_QUERY\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_functions_query_usage_history) | AI\_SERVICES |  | Data ends on 11/21/2025 | Slated for deprecation on 11/22/2026  Please use CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY. |
| [CORTEX\_FUNCTIONS\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_functions_usage_history) | AI\_SERVICES |  | Data ends on 11/21/2025 | Slated for deprecation on 11/22/2026  Please use CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY. |

Expand

Show lessSee more

### Total cost of operations

Tokens, Messages, and others aren’t the only ways in which you’re billed for Cortex AI. You’re also billed for the query, warehouse time, and any other associated Snowflake charges. Through query\_id, warehouse\_id, and user\_id, you should be able to calculate your total cost of operation. For more details, please see the associated usage view or contact support.

## Budget features

Snowflake budgets help organizations monitor credit usage and respond when spending approaches or exceeds configured thresholds. These features can support internal planning, alerting, and broader governance processes for AI usage as part of an overall cost management strategy. A budget defines a monthly spending limit for an account or for a custom group of Snowflake objects. Budgets can send notifications when spend is projected to exceed the configured limit, and Snowflake also supports custom actions for budgets based on either projected or actual consumption. This allows teams to pair spend monitoring with operational responses, using the same core budgeting model across Snowflake cost management workflows.

### Resource budgets for AI features

[Resource budgets](/user-guide/snowflake-cortex/cortex-agents-resource-budgets) let administrators define a monthly credit limit for a tagged Cortex Agent object and evaluate spend against that budget on a periodic basis. Because they use Snowflake’s tag-based cost attribution model, they fit into broader governance and budget management patterns already used across the platform. Snowflake also announced [resource budgets for Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/cowork-resource-budgets) on the same date, extending this model across additional AI experiences. [Resource budgets for Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-resource-budgets) apply the same model to Cortex Search services.

### Shared resource budgets for AI features

A [shared resource budget](/user-guide/budgets/budget-shared-resources) lets you track and control credit consumption for AI features (such as AI Functions, Cortex Agents, Cortex Code, Snowflake CoWork, and the AI Gateway) broken down by the team or cost center consuming them. Instead of budgeting a resource that belongs to a single owner or with a single budget, this budget tracks AI features that are used by specific users. Those users are identified with tags, so you can group them into logical units like a cost center or team. For example, if both an engineering team and a finance team call the same AI function, you can set up separate budgets that each track only the credits consumed by their respective tagged users, even though both teams are using the same underlying AI feature.

### Per-user quotas for AI features

A [per-user quota](/user-guide/budgets/per-user-quotas) sets monthly and daily credit limits that apply to each user individually and, unlike a budget, can block usage without any stored procedure of your own. Quotas can cover warehouse compute and AI domains, including AI Functions, Cortex Agents, Cortex Code, Cortex AI Gateway, and Snowflake CoWork. Quotas are the only AI cost control with built-in enforcement: blocks are applied within minutes of the limit being reached, rather than on the periodic budget evaluation cycle, and the block is released when the cycle resets.

Two differences from budgets are worth keeping in mind when you choose between them:

- **Limits are per user, never pooled.** A 100-credit quota across 10 users permits up to 1,000 credits in total. Use a budget when you need a single shared ceiling.
- **Some overshoot is expected.** Because a block lands shortly after the spend event rather than at the instant the limit is crossed, usage can pass the limit before the block takes effect.

### Budget capability by feature

| Feature | Budget capabilities |
| --- | --- |
| Cortex Agents | [Resource budgets](/user-guide/snowflake-cortex/cortex-agents-resource-budgets), [shared resource budgets](/user-guide/budgets/budget-shared-resources), [per-user quotas](/user-guide/budgets/per-user-quotas) |
| Cortex AI Functions | [Shared resource budgets](/user-guide/budgets/budget-shared-resources), [per-user quotas](/user-guide/budgets/per-user-quotas) |
| Cortex Code CLI (Consumption) | [Shared resource budgets](/user-guide/budgets/budget-shared-resources), [daily credit usage limits](/user-guide/cortex-code/credit-usage-limit), [per-user quotas](/user-guide/budgets/per-user-quotas) |
| Cortex Code in Snowsight | [Shared resource budgets](/user-guide/budgets/budget-shared-resources), [daily credit usage limits](/user-guide/cortex-code/credit-usage-limit), [per-user quotas](/user-guide/budgets/per-user-quotas) |
| Cortex Code Desktop | [Shared resource budgets](/user-guide/budgets/budget-shared-resources), [daily credit usage limits](/user-guide/cortex-code/credit-usage-limit), [per-user quotas](/user-guide/budgets/per-user-quotas) |
| Snowflake CoWork | [Resource budgets](/user-guide/snowflake-cortex/snowflake-cowork/cowork-resource-budgets), [shared resource budgets](/user-guide/budgets/budget-shared-resources), [per-user quotas](/user-guide/budgets/per-user-quotas) |
| Cortex Search | [Resource budgets](/user-guide/snowflake-cortex/cortex-search/cortex-search-resource-budgets) |
| AI Gateway | [Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open  Available to all accounts.  [Shared resource budgets](/user-guide/budgets/budget-shared-resources#label-budget-shared-resource-ai-gateway), [per-user quotas](/user-guide/budgets/per-user-quotas#label-per-user-quota-ai-gateway) |

Expand

Show lessSee more

*Not supported nor planned: Cortex Analyst, Cortex Fine-tuning.*

### Budget timing, enforcement, and automated actions

For resource budgets and shared resource budgets, you can attach stored procedures that are executed when spending reaches specific thresholds, which are expressed as a percentage of the spending limit and apply to the monthly budget period.
Budget evaluation and enforcement are calculated periodically rather than instantaneously. After a budget threshold is exceeded, actions can take up to eight hours to take effect under normal operation, or up to two hours when using the latency-optimized option.
Budgets are useful for ongoing spend management and policy enforcement, while still being part of a broader cost governance strategy that may also include usage monitoring and internal operational review.

Per-user quota evaluation occurs within minutes. When block enforcement is enabled, Snowflake can automatically deny further AI requests for users who reach their limit. See [Per-user quotas](/user-guide/budgets/per-user-quotas).
