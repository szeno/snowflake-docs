# Sep 15, 2026: Cortex AI Gateway (*Preview*)

We are pleased to announce the preview of Cortex AI Gateway, the control plane where you govern how AI
applications and third-party agents in your organization reach models.

It gives platform, security, and FinOps teams a single place to grant model access, attribute spend, and
audit AI activity, while application teams get a standard endpoint to build against.

Snowflake provisions the gateway for you. Each account has a single gateway object named `SNOWFLAKE`.
`ACCOUNTADMIN` can grant and revoke privileges on it for different roles.
`USAGE` is granted to `PUBLIC` by default, so the gateway is reachable out of the box; revoke it if you
want to restrict traffic to specific roles.

With this preview, you can:

- **Send inference through the gateway endpoint** using the OpenAI Chat Completions or Anthropic
  Messages API formats, from the official SDKs or a coding agent such as OpenCode. For details,
  see [Inference with Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/inference).
- **Inspect what agents did** with a per-gateway trace table. Query spans to see the
  models called, step timing, token counts, and errors for any request. For details,
  see [Observability for Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/observability).
- **Report on usage** with the new
  [AI\_GATEWAY\_USAGE\_HISTORY](/sql-reference/account-usage/ai_gateway_usage_history) view in the
  ACCOUNT\_USAGE schema, which records the gateway, user, model, and token consumption for each request.
  Snowsight also surfaces agent activity out of the box, with request and response counts, token counts,
  and latency across models, so you can inspect what agents are doing without writing SQL.
- **Control spend** by adding the gateway as a *shared resource* to a custom budget, so you can track
  credit consumption by the team or cost center consuming it.
  Per-user quotas block individual users at a limit. For details, see
  [Using budgets for AI features (shared resources)](/user-guide/budgets/budget-shared-resources) and [Per-user quotas](/user-guide/budgets/per-user-quotas). For
  guidance on choosing between them, see [Cost management for Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/cost-management). Snowsight
  charts gateway credit usage across models and users, so you can see where spend is going
  before setting a limit.

Inference through the gateway respects model access control: a request still needs whatever access the
underlying model requires, such as the
`SNOWFLAKE.CORTEX_USER` database role or the controls described in
[Privileges and model access for Cortex AI Functions](/user-guide/snowflake-cortex/aisql-privileges-and-access). The gateway governs the path traffic takes,
not the set of models a user is entitled to, so it doesn’t expand your security perimeter. Traffic is
recorded at the metadata level by default, with prompts and responses captured only if you turn payload
logging on.

To get started, sign in to Snowsight and select **AI & ML** » **Cortex AI Gateway**.

For more information, see [Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway).
