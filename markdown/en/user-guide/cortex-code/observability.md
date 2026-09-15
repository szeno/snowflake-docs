# Observability

Snowflake AI Observability provides monitoring and tracing capabilities for [CoCo](/user-guide/cortex-code/cortex-code). You can use it to review prompt history, trace agent execution, and attribute credit consumption to individual prompts or sessions.

Observability works the same way across all three CoCo surfaces: [CoCo in Snowsight](/user-guide/cortex-code/cortex-code-snowsight), [CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop), and the [CoCo CLI](/user-guide/cortex-code/cortex-code-cli). Each surface emits the same span records to the same event table and uses the same access model. The surface that originated a request is recorded in the `INTERFACE` column of the usage views described in [Cost attribution](#label-coco-cost-attribution).

## What’s tracked

Every CoCo interaction emits span-level records into the `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS` event table. Each user prompt is one **turn**, which corresponds to one OpenTelemetry **trace** (`trace_id`). That trace is made up of **spans**, including:

- **`CodingAgentRun`**: Top-level span for the turn. One record per turn.
- **`CodingAgent.Step-0`**: The primary model-call span for the turn. Contains the user prompt, model response, token counts, tool selection, latency, and a `request_id`.

Additional spans can capture planning, tool execution, SQL, chart generation, response generation, and inputs and outputs. For the same terms applied to Cortex Agents, see [Terminology](/user-guide/snowflake-cortex/cortex-agents-monitor#label-cortex-agent-observability-terminology).

## Product feedback

Thumbs-up and thumbs-down ratings on CoCo responses, including any comment you add, are **product feedback to Snowflake**, which uses it to improve CoCo. This applies to Snowsight, Desktop, and the CLI. Snowflake receives the request ID and your comment, not the prompt or the response.

Ratings aren’t stored in your account or in `AI_OBSERVABILITY_EVENTS`, so you can’t look one up by `request_id`. Prompt history and traces are stored there, as described earlier on this page.

[Cortex Agent feedback](/user-guide/snowflake-cortex/cortex-agents-monitor#label-cortex-agents-view-feedback), including CoWork, works differently: those agents are objects your account owns, so ratings are queryable as `CORTEX_AGENT_FEEDBACK` events. CoCo is a Snowflake-owned feature, so its ratings go to Snowflake.

A rating can stay selected after you refresh Snowsight. That’s temporary browser state, not a record in your account.

The `/feedback` command also doesn’t write to the event table. On Desktop it opens a feedback form, and on the CLI it saves a local `.tgz` bundle. See [CoCo CLI reference](/user-guide/cortex-code/cli-reference).

## Accessing observability data

For Cortex Agents, External Agents, and Cortex Search services, use [GET\_AI\_OBSERVABILITY\_EVENTS](/sql-reference/functions/get_ai_observability_events-snowflake-local) with the matching `agent_type`. That is the recommended path: results are scoped to the object and enforce privileges on it. See [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events).

CoCo doesn’t use a separate object type in that function. To query CoCo spans, filter `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS` by `RECORD:name` (for example `CodingAgent.Step-0`). That direct-table path is typical for CoCo and usually requires `AI_OBSERVABILITY_READER` or another admin role, as described in the LOCAL schema reference.

### Example: List recent prompts

Copy code

```
SELECT
    TIMESTAMP,
    RESOURCE_ATTRIBUTES['snow.user.name']::STRING AS user_name,
    RESOURCE_ATTRIBUTES['snow.session.role.primary.name']::STRING AS role_name,
    RECORD_ATTRIBUTES['snow.ai.observability.agent.planning.model']::STRING AS model,
    RECORD_ATTRIBUTES['snow.ai.observability.agent.planning.duration']::INT AS latency_ms,
    RECORD_ATTRIBUTES['snow.ai.observability.agent.planning.status']::STRING AS status
  FROM SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS
  WHERE RECORD_TYPE = 'SPAN'
    AND RECORD:name::STRING = 'CodingAgent.Step-0'
  ORDER BY TIMESTAMP DESC;
```

## Cost attribution

To attribute credit consumption to individual prompts, join the event table to [SNOWFLAKE\_COCO\_USAGE\_HISTORY](/sql-reference/account-usage/snowflake_coco_usage_history) on `REQUEST_ID`. That view covers all three CoCo surfaces and reports which one served the request in its `INTERFACE` column:

Copy code

```
SELECT
    obs.TIMESTAMP AS event_time,
    obs.RESOURCE_ATTRIBUTES['snow.user.name']::STRING AS user_name,
    usage.INTERFACE,
    obs.RECORD_ATTRIBUTES['snow.ai.observability.agent.planning.model']::STRING AS model,
    usage.TOKEN_CREDITS
  FROM SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS obs
    JOIN SNOWFLAKE.ACCOUNT_USAGE.SNOWFLAKE_COCO_USAGE_HISTORY usage
      ON obs.RECORD_ATTRIBUTES['snow.ai.observability.agent.planning.request_id']::STRING
         = usage.REQUEST_ID
  WHERE obs.RECORD_TYPE = 'SPAN'
    AND obs.RECORD:name::STRING = 'CodingAgent.Step-0'
  ORDER BY obs.TIMESTAMP DESC;
```

To attribute cost for a single turn, group on `TRACE['trace_id']`:

Copy code

```
SELECT
    obs.TRACE['trace_id']::STRING AS trace_id,
    obs.RESOURCE_ATTRIBUTES['snow.user.name']::STRING AS user_name,
    COUNT(*) AS step_count,
    SUM(usage.TOKEN_CREDITS) AS total_credits
  FROM SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS obs
    JOIN SNOWFLAKE.ACCOUNT_USAGE.SNOWFLAKE_COCO_USAGE_HISTORY usage
      ON obs.RECORD_ATTRIBUTES['snow.ai.observability.agent.planning.request_id']::STRING
         = usage.REQUEST_ID
  WHERE obs.RECORD_TYPE = 'SPAN'
    AND obs.RECORD:name::STRING = 'CodingAgent.Step-0'
  GROUP BY 1, 2
  ORDER BY total_credits DESC;
```

To scope either query to one surface, filter on `usage.INTERFACE` (`cli`, `desktop`, or `snowsight`). You can also query the per-surface views directly: [CORTEX\_CODE\_SNOWSIGHT\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_code_snowsight_usage_history), [CORTEX\_CODE\_DESKTOP\_USAGE\_HISTORY](/user-guide/cortex-code/cortex-code-desktop/cortex-code-desktop-usage-history-view), and [CORTEX\_CODE\_CLI\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_code_cli_usage_history).

Important

Use the usage views, not the event table, as the source of truth for credits and tokens. Trace delivery to `AI_OBSERVABILITY_EVENTS` is best effort, so join results can under-report cost. For details, see [AI\_OBSERVABILITY\_EVENTS](/sql-reference/local/ai_observability_events#label-ai-observability-events-billing).

## Access control

CoCo span queries use direct `SELECT` on `AI_OBSERVABILITY_EVENTS` because there is no CoCo-specific `agent_type` for the observability table functions. Grant `SNOWFLAKE.AI_OBSERVABILITY_READER` only when this role needs that direct-table access (for example operators running the examples above). For retention deletes, grant `SNOWFLAKE.AI_OBSERVABILITY_ADMIN`. For the recommended access model for agents, search services, and External Agents, see [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events).

Copy code

```
GRANT APPLICATION ROLE SNOWFLAKE.AI_OBSERVABILITY_READER
  TO ROLE <role_name>;
```

To join observability data with the usage views, the role also needs read access to the `SNOWFLAKE` database:

Copy code

```
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE
  TO ROLE <role_name>;
```

## More information

For the AI Observability overview and links to every Cortex feature, see [AI Observability with Snowflake Cortex](/user-guide/snowflake-cortex/ai-observability). For TruLens datasets, metrics, and runs, see [Snowflake AI Observability Reference](/user-guide/snowflake-cortex/ai-observability/reference). For the shared event table and `GET_AI_*` functions, see [LOCAL schema](/sql-reference/local/ai_observability_events).
