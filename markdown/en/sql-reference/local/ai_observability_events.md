Schema:
:   [LOCAL](/sql-reference/local)

# AI\_OBSERVABILITY\_EVENTS table

`SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS` is a central [event table](/developer-guide/logging-tracing/event-table-setting-up) for AI observability telemetry in your account. Rows use the standard [event table column layout](/developer-guide/logging-tracing/event-table-columns) (for example `RECORD`, `RECORD_ATTRIBUTES`, `VALUE`, `TRACE`, and timestamps).

For a feature-level overview of monitoring and evaluations, see [AI Observability with Snowflake Cortex](/user-guide/snowflake-cortex/ai-observability).

## Columns

The table uses the standard Snowflake [event table column layout](/developer-guide/logging-tracing/event-table-columns). Filter and project with standard SQL (for example on `RECORD:name`, `RECORD_ATTRIBUTES`, or fields inside `VALUE`).

## What the table stores

Typical records include:

- Conversation **threads** (each made up of one or more **turns**), where each turn has one **trace** composed of **spans** such as planning, tool calls, SQL, chart generation, and response generation. For definitions, see [Terminology](/user-guide/snowflake-cortex/cortex-agents-monitor#label-cortex-agent-observability-terminology) and [Use threads with the Cortex Agent REST API](/user-guide/snowflake-cortex/cortex-agents-threads).
- Inputs and outputs associated with each span (subject to [redaction](#label-ai-observability-redaction))
- **User feedback** on Cortex Agent and CoWork responses. CoCo ratings are [product feedback to Snowflake](/user-guide/cortex-code/observability#label-coco-product-feedback) and aren’t stored here.
- **Evaluation runs** for Cortex Agents and External Agent (TruLens) applications
- Cortex Search **request logs** when `REQUEST_LOGGING` is enabled on a service

Ingested rows **can’t be modified**. Only administrators with the `SNOWFLAKE.AI_OBSERVABILITY_ADMIN` application role can delete rows for retention management.

Accounting for spend and token usage

`AI_OBSERVABILITY_EVENTS` is built for tracing and debugging individual requests, and telemetry is delivered on a **best-effort** basis, which means a span can occasionally be dropped or arrive late. Token and credit values in a span describe what that span reported, so totals you compute from the event table can come in under actual consumption.

To account for spend or reconcile token counts, use one of the following authoritative sources:

- **[Account Usage](/sql-reference/account-usage) and [Organization Usage](/sql-reference/organization-usage) views** for credits, tokens, and per-model breakdowns. Pick the view for the feature you’re billing, such as [CORTEX\_AGENT\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_agent_usage_history) for Cortex Agents, [SNOWFLAKE\_COCO\_USAGE\_HISTORY](/sql-reference/account-usage/snowflake_coco_usage_history) for CoCo, or [CORTEX\_AI\_FUNCTIONS\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_ai_functions_usage_history) for built-in AI functions. For the full mapping of features to views, see [AI cost management and governance](/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance).
- **The agent API response**, which returns complete token information and the model used for that request in its `usage.tokens_consumed` field. See [TokensConsumed](/user-guide/snowflake-cortex/cortex-agents-run#label-snowflake-agent-run-tokensconsumed).

Joining trace data to a usage view on `REQUEST_ID` is still a good way to attribute a known cost back to the prompt that caused it. Treat the usage view as the source of truth for the amount, and the event table as the explanation of what happened.

## What writes to the table

The following table lists features that emit rows into `AI_OBSERVABILITY_EVENTS`:

| Source | How data is emitted | Feature documentation |
| --- | --- | --- |
| **Cortex Agents** (including agents used by Snowflake CoWork) | Automatic logging for Agent API and Snowflake Intelligence conversations (one trace per turn); batch evaluation traces from the Snowsight **Evaluations** tab or `EXECUTE_AI_EVALUATION` (see [Terminology](/user-guide/snowflake-cortex/cortex-agents-monitor#label-cortex-agent-observability-terminology)) | [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor), [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations) |
| **External Agent** (TruLens) | TruLens Python SDK via Snowflake connector | [Trace and monitor applications with TruLens](/user-guide/snowflake-cortex/ai-observability/trace-applications-trulens) |
| **CoCo** | Automatic span records per prompt (`CodingAgentRun`, `CodingAgent.Step-0`). Product ratings (thumbs-up and thumbs-down) are feedback to Snowflake and aren’t stored in this table. | [Overview of Snowflake CoCo](/user-guide/cortex-code/cortex-code), [Product feedback](/user-guide/cortex-code/observability#label-coco-product-feedback) |
| **Cortex Search** | One event row per logged request when [`REQUEST_LOGGING`](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor#label-cortex-search-request-logging) is enabled | [Monitor Cortex Search requests](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor) |

Expand

Show lessSee more

**Cortex Analyst** stores **direct** Analyst request logs in `SNOWFLAKE.LOCAL.CORTEX_ANALYST_REQUESTS_RAW` and exposes them through the [CORTEX\_ANALYST\_REQUESTS](/sql-reference/local) table function and [CORTEX\_ANALYST\_REQUESTS\_V](/sql-reference/local/cortex_analyst_requests_v) view. That table does **not** include Analyst tool calls invoked by a Cortex Agent; those spans appear in `AI_OBSERVABILITY_EVENTS` as part of the agent trace. See [Administrator monitoring](/user-guide/snowflake-cortex/cortex-analyst/admin-observability).

## Query the table with SNOWFLAKE.LOCAL functions (recommended)

The **recommended** way to read `AI_OBSERVABILITY_EVENTS` is through the four `SNOWFLAKE.LOCAL` table functions below. Each function takes the database, schema, and name of the object you are inspecting, plus an **agent type** (`CORTEX AGENT`, `EXTERNAL AGENT`, or `CORTEX SEARCH SERVICE` where supported). Snowflake returns only events for that object and checks your privileges on it (for example `MONITOR` on a Cortex Agent or Cortex Search service, or `USAGE` on an External Agent). This scoped access matches how monitoring works in Snowsight and is the standard pattern for feature owners and operators.

Only [GET\_AI\_OBSERVABILITY\_EVENTS](/sql-reference/functions/get_ai_observability_events-snowflake-local) accepts `CORTEX SEARCH SERVICE` as `agent_type`. The other three functions apply to Cortex Agent and External Agent evaluations only.

| Function | Purpose |
| --- | --- |
| [GET\_AI\_OBSERVABILITY\_EVENTS](/sql-reference/functions/get_ai_observability_events-snowflake-local) | Return observability event rows (conversations, spans, traces, feedback). Use `CORTEX AGENT`, `EXTERNAL AGENT`, or `CORTEX SEARCH SERVICE` as `agent_type` where supported. |
| [GET\_AI\_OBSERVABILITY\_LOGS](/sql-reference/functions/get_ai_observability_logs-snowflake-local) | Return structured log lines and warnings from evaluation runs |
| [GET\_AI\_EVALUATION\_DATA](/sql-reference/functions/get_ai_evaluation_data-snowflake-local) | Return evaluation trace data for a named run |
| [GET\_AI\_RECORD\_TRACE](/sql-reference/functions/get_ai_record_trace-snowflake-local) | Return a single trace record from an evaluation run |

Expand

Show lessSee more

Example for a Cortex Agent:

Copy code

```
SELECT *
  FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_EVENTS(
    'MY_DB', 'MY_SCHEMA', 'MY_AGENT', 'CORTEX AGENT'
  ));
```

Example for a Cortex Search service (with `REQUEST_LOGGING` enabled):

Copy code

```
SELECT *
  FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_EVENTS(
    'MY_DB', 'MY_SCHEMA', 'MY_SEARCH_SERVICE', 'CORTEX SEARCH SERVICE'
  ));
```

For feature-specific examples and required privileges on the underlying object, see the monitoring topic for that feature in [AI Observability with Snowflake Cortex](/user-guide/snowflake-cortex/ai-observability).

Note

**Direct table access is for limited admin use**

You can `SELECT` from `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS` directly, but that path is **not** the recommended way to monitor a specific agent, External Agent application, or search service. Direct queries return events across the account (subject to your table access) and **do not** enforce object-level privileges the way the table functions do. Reserve direct access for narrow administrative tasks such as account-wide audits or custom retention workflows.

## Permissions

Grant **object privileges** on the Cortex Agent, External Agent, or Cortex Search service you want to inspect, then call the table functions with a role that has those privileges. You typically do **not** need `SNOWFLAKE.AI_OBSERVABILITY_READER` for this path.

| Access path | What to grant | When to use |
| --- | --- | --- |
| **Table functions** (recommended) | `MONITOR` (or OWNERSHIP) on the Cortex Agent or Cortex Search service; `USAGE` on the External Agent; plus `SNOWFLAKE.CORTEX_USER` where required by the feature | Routine monitoring and SQL queries scoped to one object |
| **`AI_OBSERVABILITY_READER`** | `GRANT APPLICATION ROLE SNOWFLAKE.AI_OBSERVABILITY_READER TO ROLE …` | Limited admin scenarios that must read the raw table directly (bypasses object scoping) |
| **`AI_OBSERVABILITY_ADMIN`** | `GRANT APPLICATION ROLE SNOWFLAKE.AI_OBSERVABILITY_ADMIN TO ROLE …` | Delete rows for retention management only |

Expand

Show lessSee more

Object privilege examples:

- **Cortex Agent**: `MONITOR` on the agent (see [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor))
- **Cortex Search service**: `MONITOR` on the service; enable `REQUEST_LOGGING` (see [Monitor Cortex Search requests](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor))
- **External Agent (TruLens)**: `USAGE` on the External Agent object; `MONITOR` does not apply (see [External Agent commands](/sql-reference/commands-external-agent))

To grant the application roles for direct table access or retention:

Copy code

```
GRANT APPLICATION ROLE SNOWFLAKE.AI_OBSERVABILITY_READER
  TO ROLE <admin_role_name>;

GRANT APPLICATION ROLE SNOWFLAKE.AI_OBSERVABILITY_ADMIN
  TO ROLE <admin_role_name>;
```

- **`AI_OBSERVABILITY_READER`**: Read the raw event table directly. Does not replace object privileges for the recommended table-function path.
- **`AI_OBSERVABILITY_ADMIN`**: Delete rows in the event table for retention management.

Direct `SELECT` on the table typically requires `ACCOUNTADMIN` or membership in a role granted `AI_OBSERVABILITY_READER`, in addition to warehouse and database access as usual.

For TruLens-specific role requirements (including `CREATE EXTERNAL AGENT`, tasks, and `SNOWFLAKE.CORTEX_USER`), see [Required privileges](/user-guide/snowflake-cortex/ai-observability/reference#label-ai-observability-required-privileges).

## Redaction and unredacted access

An account-level privilege, **READ UNREDACTED AI OBSERVABILITY EVENTS TABLE**, controls whether roles see **unredacted** content (full tool inputs and outputs, full conversation text, and user feedback text) in **Cortex Agent monitoring** in Snowsight and when calling the **`SNOWFLAKE.LOCAL` observability table functions** that read the event table.

Without the grant, roles can still read **metadata** in those paths (tool names, token usage, latency, evaluation trace summaries, model name, and error severity). This does **not** change Cortex Agent or External Agent **evaluation** job execution, scoring, or the **Evaluations** experience in Snowsight.

For details, see [Account Privilege READ UNREDACTED AI OBSERVABILITY EVENTS TABLE](/release-notes/bcr-bundles/un-bundled/bcr-read-unredacted-ai-observability-events) and [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor).
