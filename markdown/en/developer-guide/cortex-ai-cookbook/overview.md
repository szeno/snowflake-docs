# Cortex AI Cookbook

The Cortex AI Cookbook collects deployment patterns for Cortex AI, drawn from real Snowflake deployments. Each recipe explains the design and the security model, then gives you verified code to run in your own account and adapt.

Every recipe follows the same shape:

- **When to use this:** the problem the pattern solves, and when a simpler option is better.
- **How it works:** the architecture and the security model.
- **Quickstart and walkthrough:** numbered SQL scripts that build the pattern, with a teardown script that removes everything.
- **Verify:** queries that prove the pattern works in your account.

Each recipe has a code page that shows every file, and a zip file with all of them to download. Each recipe is a reference implementation: review it and adapt it to your environment before production use.

## Recipes

Recipes follow the AI lifecycle, in reading order: start at Scope and work through to Operate. Select stages to filter.

Scope2→Build11→Secure7→Evaluate8→Operate11

SearchTopicAllAI ObservabilityCortex AgentsCortex AI FunctionsCortex AI GatewayCortex CodeSemantic ViewsSnowflake MCPStatusAllGAPreview

| Recipe | Stage | Topics | Status |
| --- | --- | --- | --- |
| [Scoping agentic implementations: from 'talk to your data' to a testable agent spec](/en/developer-guide/cortex-ai-cookbook/scoping-agentic-implementations) A workshop method for turning a broad agent idea into personas, a question taxonomy, a registered evaluation dataset, and a phased delivery plan. | ScopeEvaluate | Cortex AgentsAI ObservabilityCortex AI Functions | GA |
| [Snowflake-managed MCP or the Cortex Agents REST API](/en/developer-guide/cortex-ai-cookbook/mcp-or-agent-rest-api) Decide how people reach a Cortex Agent, with identity and policies in each lane, then best practices for managed MCP servers and the Agents REST API. | ScopeSecureBuild | Snowflake MCPCortex Agents | GA |
| [Agentic schema mapping: messy CSVs to canonical tables with a Cortex Agent](/en/developer-guide/cortex-ai-cookbook/agentic-schema-mapping) A Cortex Agent profiles messy CSV files, proposes column mappings with AI\_COMPLETE, resolves free-text values, and loads approved mappings through allowlisted SQL. | Build | Cortex AI FunctionsCortex Agents | GA |
| [Embedded app context for a Cortex Agent](/en/developer-guide/cortex-ai-cookbook/embedded-app-context) Give an agent embedded in a Streamlit dashboard the page, filters, and persona the user is looking at, by prepending an app-context block to the user message. | Build | Cortex Agents | GA |
| [Attach documents to Cortex Agent conversations](/en/developer-guide/cortex-ai-cookbook/document-context) Let users attach PDFs, Office files, images, and CSVs to a custom agent frontend with a caller's-rights document tool, per-user stage folders, and authenticated middleware. | BuildSecure | Cortex Agents | GA |
| [Multi-agent orchestration with a CoWork profile](/en/developer-guide/cortex-ai-cookbook/multi-agent-orchestration) One Snowflake CoWork profile routes to specialist agents with the agent\_router tool, so Snowflake grants decide which specialist each user reaches. | BuildSecure | Cortex AgentsSemantic Views | Preview |
| [PII redaction with AI\_REDACT, AI\_COMPLETE extraction, and an entity cache](/en/developer-guide/cortex-ai-cookbook/pii-redaction) Redact PII in free text with AI\_REDACT, cover domain identifiers with AI\_COMPLETE structured extraction, and serve redactions from a stream-maintained cache. | BuildSecure | Cortex AI Functions | GA |
| [Causally grounded Cortex Agent that refuses when the data cannot answer](/en/developer-guide/cortex-ai-cookbook/agent-causal-grounding) A Cortex Agent whose every number comes from a persisted causal estimator, and which declines to answer for cohorts where no honest estimate exists. | BuildEvaluate | Cortex AgentsSemantic Views | GA |
| [Mixed-grain tables: diagnose and fix wrong agent answers with a GRAIN dimension and verified queries](/en/developer-guide/cortex-ai-cookbook/mixed-grain-and-verified-queries) An agent double-counts a table that holds daily and monthly rows. Diagnose it from wrong answers, fix the semantic view with a GRAIN enum, rules, and verified queries, re-test. | BuildEvaluate | Semantic ViewsCortex Agents | GA |
| [Long-running Cortex Agent runs over managed MCP](/en/developer-guide/cortex-ai-cookbook/long-running-agents-over-mcp) Split one long MCP tool call into a fast submit and a bounded fetch over background agent runs, so no call nears a client's timeout and caller's rights still apply. | BuildOperate | Snowflake MCPCortex Agents | GA |
| [OAuth token passthrough to a Cortex Agent](/en/developer-guide/cortex-ai-cookbook/oauth-token-passthrough) Relay each signed-in user's Entra ID token to a Cortex Agent so the agent runs as that person, with per-user results from a row access policy on CURRENT\_USER(). | Secure | Cortex Agents | GA |
| [Multi-tenant agents with session attributes and fail-closed policies](/en/developer-guide/cortex-ai-cookbook/multi-tenant-agents) Serve many tenants from one Cortex Agent: the app server names the end user in an immutable session attribute, and policies derive the tenant from an entitlement. | SecureBuild | Cortex AgentsSemantic Views | GA |
| [Semantic view description quality: a rubric, a linter, and how to apply fixes](/en/developer-guide/cortex-ai-cookbook/description-quality) Grade semantic view descriptions on preciseness, conciseness, non-circularity, and correctness, lint them in SQL, and apply fixes with CREATE OR ALTER or the YAML procedure. | Evaluate | Semantic ViewsCortex AI Functions | GA |
| [Evaluate and promote Cortex Agent versions](/en/developer-guide/cortex-ai-cookbook/agent-evaluations) Run Cortex Agent evaluations with pinned metric versions and a custom judge, compare two committed versions, and promote the winner by alias. | EvaluateOperate | Cortex Agents | GA |
| [Refine a semantic view from agent logs: triage, SME review, and verified queries](/en/developer-guide/cortex-ai-cookbook/refinement-loop-from-agent-logs) Mine Cortex Agent traces for guessed, exploratory, and no-data answers, get the right answer from a subject matter expert, ship it into the semantic view, and re-test. | EvaluateOperate | Semantic ViewsAI ObservabilityCortex Agents | GA |
| [Turn agent feedback and rephrased questions into an evaluation dataset](/en/developer-guide/cortex-ai-cookbook/agent-feedback-to-evals) Mine thumbs-down feedback and user rephrases from agent traces, confirm each with one LLM call, and write a deduplicated eval dataset. | EvaluateOperate | AI ObservabilityCortex Agents | GA |
| [Agent versioning and promotion](/en/developer-guide/cortex-ai-cookbook/agent-versioning-and-promotion) Commit, alias, promote, A/B route, and roll back Cortex Agent versions with runnable SQL and the behaviors observed along the way. | Operate | Cortex Agents | GA |
| [AI usage and cost attribution across agents, CoWork, Cortex Code, and AI functions](/en/developer-guide/cortex-ai-cookbook/ai-usage-cost-attribution) One reconciled view of Cortex AI credits by surface, user, agent, model, and cost center, plus budgets and per-user quotas. | Operate | AI ObservabilityCortex CodeCortex AI Functions | GA |
| [Diagnose slow Cortex Agent requests from their traces](/en/developer-guide/cortex-ai-cookbook/diagnose-agent-requests) A caller's-rights procedure that reads one agent request's trace, computes a time breakdown by span, and returns an LLM explanation. | Operate | AI ObservabilityCortex Agents | GA |
| [Size Cortex Code per-user limits from real usage](/en/developer-guide/cortex-ai-cookbook/coco-user-budget-sizing) Tiered per-user CoCo quotas, daily limits, and alert-only team budgets, starting from conservative defaults and sized from your own ACCOUNT\_USAGE. | Operate | AI ObservabilityCortex Code | GA |
| [LangChain agents on Cortex AI Gateway with MCP tools and traces](/en/developer-guide/cortex-ai-cookbook/langchain-mcp-agent-tracing) External LangChain agents reason through Cortex AI Gateway, act through a Snowflake MCP server, and are analyzed from gateway traces and per-user cost. | OperateBuild | Cortex AI GatewaySnowflake MCPAI Observability | Preview |
| [Cortex AI Gateway governance quickstart](/en/developer-guide/cortex-ai-cookbook/gateway-governance-quickstart) Route an app through Cortex AI Gateway with its own identity: both API formats, a model allowlist, traces, per-user cost, and a blocking quota. | OperateSecure | Cortex AI GatewayAI Observability | Preview |
| [Agent CI/CD with dbt: per-PR builds, versioned deploys, and an evaluation gate](/en/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt) dbt builds the tables and semantic view, the agent ships as a versioned spec from a stage, and an evaluation gate in GitHub Actions blocks promotion. | OperateEvaluate | Cortex AgentsSemantic Views | GA |

Expand

Show lessSee more
