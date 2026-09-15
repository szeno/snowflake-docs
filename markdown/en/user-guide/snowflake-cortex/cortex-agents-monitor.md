# Monitor Cortex Agent requests

Use this topic for Cortex Agents deployed through Snowflake Intelligence or the Agent API. Observability shows **live** conversation history and execution traces: planning, tool calls, responses, and user feedback.

For **batch test runs** and GPA-style metrics, see [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations). For **custom AI applications** (agents, RAG pipelines, AI workflows on Snowflake compute or other hosts) observed with TruLens, see [Trace and monitor applications with TruLens](/user-guide/snowflake-cortex/ai-observability/trace-applications-trulens).

## Observability vs evaluations (Cortex Agents)

The following table compares live observability with batch evaluations for Cortex Agents:

|  | **Observability** (this topic) | **Evaluations** |
| --- | --- | --- |
| Purpose | Debug and audit **production** conversations and threads | Score the agent on a **dataset** before or after deployment |
| Snowsight | Agent → **Observability** tab | Agent → **Evaluations** tab |
| Typical use | Trace planning, tools, latency, feedback on real queries | Answer correctness, logical consistency, custom LLM judges |
| Documentation | This topic | [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations) |

Expand

Show lessSee more

## Terminology

Cortex Agent monitoring uses OpenTelemetry-style event data in `AI_OBSERVABILITY_EVENTS`. The following terms describe how conversations are grouped:

| Term | Meaning |
| --- | --- |
| **Thread** | A persisted conversation identified by `thread_id`. The **Observability** pane lists one row per thread. **Thread length** is the number of turns in that conversation. See [Use threads with the Cortex Agent REST API](/user-guide/snowflake-cortex/cortex-agents-threads). |
| **Turn** | One user message and the agent’s full response for that message (one `agent:run` request). Each turn is a single exchange in a thread. |
| **Trace** | The OpenTelemetry trace for one turn. All telemetry for that turn shares the same `trace_id` in the `TRACE` column of `AI_OBSERVABILITY_EVENTS`. **One turn = one trace.** |
| **Span** | One step inside a trace: LLM planning, a tool call, SQL execution, chart generation, response generation, and so on. **Many spans make up one trace.** |
| **Snowflake session** | The platform SQL session context (user, role, warehouse, and related attributes in `RESOURCE_ATTRIBUTES`). A Snowflake session is separate from a conversation thread. One session can include many threads and turns. |

Expand

Show lessSee more

```
Snowflake session
  └── Thread (thread_id)
        └── Turn 1 = Trace 1 (one trace_id)
              └── Spans: planning, tools, response, …
        └── Turn 2 = Trace 2
              └── Spans: …
```

When you query the event table, filter on `TRACE:trace_id` to scope results to a single turn. Filter on thread-related attributes or use Snowsight to work at thread level across multiple turns.

## Information collected in Cortex Agent logs

Cortex Agent logs include the following information:

- Conversation history associated with a **thread**
- For each **turn**, one **trace** made up of **spans**, including:

  - LLM planning
  - Tool execution (Cortex Search, Cortex Analyst, web search, code execution, MCP connector calls, custom tools, and other configured tools)
  - LLM response generation
  - SQL execution
  - Chart generation
- Inputs and outputs associated with each span
- User feedback for each agent response (one turn)

## View Cortex Agent logs in Snowsight

To view Cortex Agent conversation logs in Snowsight, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **Agents**.
3. Select the agent whose logs you want to view.
4. Navigate to the **Observability** pane of the agent view.

The **Observability** pane lists each conversation thread with its first input, user feedback, thread length, the user who ran it, and when it was last updated. Threads are ordered by when they were last updated. The pane shows threads across every version of the agent. Selecting a specific version in the agent versions panel doesn’t filter this pane. Use it to see all usage of an agent in one place.

### Agent versions in observability

A conversation can continue while you commit a new [agent version](/user-guide/snowflake-cortex/cortex-agents-versioning) or repoint an alias, so different turns in the same thread can be served by different versions. For that reason, Snowflake records the version and any alias used at invocation time for each turn instead of assigning one version to the whole thread.

Version information appears in the following places:

- In the thread list, the **Version** column shows the most recent version that served the thread. An icon next to the value marks threads that interacted with more than one version.
- Opening a thread’s trace view shows the version that served each turn, so you can tell exactly which configuration produced a given response.

When you query the page, the UI pairs recorded turns with the agent’s current version metadata:

- After you commit the live version as `VERSION$4`, turns recorded as `LIVE` (displayed as `DRAFT` in the UI) display `VERSION$4` once new traces labeled `VERSION$4` start arriving. Snowflake pairs those traces with the earlier draft-labeled data. Because every version starts as the live version, this prevents versions from appearing permanently as `LIVE`.
- The UI shows aliases currently assigned to the recorded version, regardless of which alias was used at invocation time. Reassigning an alias updates how existing traces for those versions are labeled.
- If the recorded version was deleted, or if the turn predates agent version tracking, the UI displays `—`.

Note

By default, the **Observability** pane loads data as your current role and uses your default warehouse. Use the **Role** and **Warehouse** selectors to override these defaults and query the monitoring data with a specific role and warehouse.

## Query Cortex Agent logs with SQL

The same thread, trace, and span data shown in the **Observability** tab is stored in `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS`. Use the **`SNOWFLAKE.LOCAL` observability table functions** (UDTFs) below to read rows scoped to a specific agent. Grant `MONITOR` on the agent to the querying role. Entries in the event table can’t be modified.

For the recommended access model, required object privileges, and when to use `AI_OBSERVABILITY_READER` for direct table access, see [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events).

Note

**Unredacted fields in monitoring and UDTF results**

An account-level privilege, **READ UNREDACTED AI OBSERVABILITY EVENTS TABLE**, controls whether roles can see **unredacted** content from `AI_OBSERVABILITY_EVENTS` (full tool inputs and outputs, full conversation text, and user feedback text) when you use **Cortex Agent monitoring** in Snowsight and when you call the **`SNOWFLAKE.LOCAL`** observability **user-defined table functions** (UDTFs) that read that event table. Without the grant, roles can still read **metadata** in those paths (tool names, token usage, latency, evaluation trace summaries, model name, and error severity). This does **not** change **Cortex Agent evaluation** job execution, scoring, or the **Evaluations** experience. An account admin must grant the privilege to see unredacted content; for details, see [Account Privilege READ UNREDACTED AI OBSERVABILITY EVENTS TABLE](/release-notes/bcr-bundles/un-bundled/bcr-read-unredacted-ai-observability-events).

### Observability table functions

Use the following UDTFs to read monitoring and evaluation data. [GET\_AI\_OBSERVABILITY\_EVENTS](/sql-reference/functions/get_ai_observability_events-snowflake-local) also accepts `CORTEX SEARCH SERVICE` as `agent_type` for Cortex Search request logs; see [Monitor Cortex Search requests](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor). The other three functions apply to Cortex Agent and External Agent evaluations only.

All four functions take the object database, schema, name, and `agent_type` (`CORTEX AGENT`, `EXTERNAL AGENT`, or `CORTEX SEARCH SERVICE` for `GET_AI_OBSERVABILITY_EVENTS` only).

| Function | Use when you want to… |
| --- | --- |
| [GET\_AI\_OBSERVABILITY\_EVENTS](/sql-reference/functions/get_ai_observability_events-snowflake-local) | Read production monitoring events: threads, spans, traces, and user feedback |
| [GET\_AI\_OBSERVABILITY\_LOGS](/sql-reference/functions/get_ai_observability_logs-snowflake-local) | Read structured log lines and warnings from evaluation runs |
| [GET\_AI\_EVALUATION\_DATA](/sql-reference/functions/get_ai_evaluation_data-snowflake-local) | Retrieve evaluation trace data for a named run |
| [GET\_AI\_RECORD\_TRACE](/sql-reference/functions/get_ai_record_trace-snowflake-local) | Retrieve one trace record from an evaluation run |

Expand

Show lessSee more

For evaluation workflows and examples of the last three functions, see [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations) (SQL section under evaluation results).

### Query monitoring events

Monitoring data for an agent is stored in `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS`. To read those rows programmatically, use [GET\_AI\_OBSERVABILITY\_EVENTS](/sql-reference/functions/get_ai_observability_events-snowflake-local). Pass the database name, schema name, object name, and `agent_type` `CORTEX AGENT` for a Cortex Agent, `EXTERNAL AGENT` for an External Agent used with [AI Observability](/user-guide/snowflake-cortex/ai-observability/trace-applications-trulens) (see [External Agent commands](/sql-reference/commands-external-agent)), or `CORTEX SEARCH SERVICE` for a Cortex Search service (see [Monitor Cortex Search requests](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor)). The result has the same [event table columns](/developer-guide/logging-tracing/event-table-columns) as the underlying table (for example `RECORD`, `RECORD_ATTRIBUTES`, `VALUE`, `TRACE`, and timestamps). You can filter with `WHERE` to focus on specific event kinds, time ranges, or attributes.

When `agent_type` is `EXTERNAL AGENT`, USAGE on that External Agent is sufficient to call the function; MONITOR does not apply. When `agent_type` is `CORTEX SEARCH SERVICE`, MONITOR (or OWNERSHIP) on the Cortex Search service is required and `REQUEST_LOGGING` must be enabled. OWNERSHIP on the External Agent is required to modify or drop the object with SQL.

The following example returns all observability events for an agent:

Copy code

```
SELECT *
  FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_EVENTS(
    '<database_name>',
    '<schema_name>',
    '<agent_name>',
    'CORTEX AGENT'
  ));
```

For TruLens applications and External Agent examples, see [Trace and monitor applications with TruLens](/user-guide/snowflake-cortex/ai-observability/trace-applications-trulens) and [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events).

### Generate monitoring reports with CoCo CLI

Use the `agent-observability-report` sub-skill of the CoCo [`agent-studio`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-agent-studio) skill in the [CoCo CLI](/user-guide/cortex-code/cortex-code-cli) to generate a report on agent monitoring metrics pulled from `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS`, including usage and adoption, latency percentiles, token economics, tool execution stats, conversation depth and completion, and a breakdown of user feedback. For more information about CoCo skills, see [CoCo CLI - Skills](/user-guide/cortex-code/extensibility#label-extensibility-skills).

### View feedback provided by users

End-user feedback is stored as observability events. To return **only** feedback events, filter on the record name `CORTEX_AGENT_FEEDBACK`:

Copy code

```
SELECT *
  FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_EVENTS(
    '<database_name>',
    '<schema_name>',
    '<agent_name>',
    'CORTEX AGENT'
  ))
  WHERE RECORD:name = 'CORTEX_AGENT_FEEDBACK';
```

The resulting rows include information about the agent, the user who provided feedback, the feedback text, and whether the feedback was positive or negative. For full argument and access details, see [GET\_AI\_OBSERVABILITY\_EVENTS (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_observability_events-snowflake-local).

This applies to Cortex Agents in your account, including agents used in [Overview of Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork). Thumbs-up and thumbs-down ratings in CoCo (Snowsight, Desktop, and the CLI) are product feedback to Snowflake, not Cortex Agent monitoring events, so they aren’t stored as `CORTEX_AGENT_FEEDBACK`. See [Product feedback](/user-guide/cortex-code/observability#label-coco-product-feedback).

## Access control and permissions

To view Cortex Agent logs, users must have the following privileges:

- OWNERSHIP or MONITOR privileges on the AGENT object
- The CORTEX\_USER database role

The following example uses the ACCOUNTADMIN role to create a new role `agent_monitoring_user_role`
with the required permissions to view Cortex Agent logs. This new role is then assigned to `some_user`.

Copy code

```
USE ROLE ACCOUNTADMIN;
CREATE ROLE agent_monitoring_user_role;
GRANT MONITOR ON AGENT my_agent TO ROLE agent_monitoring_user_role;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE agent_monitoring_user_role;
GRANT ROLE agent_monitoring_user_role TO USER some_user;
```

### Grant monitoring access to future agents

To grant a role monitoring access on future agents created in a schema, use the following SQL command:

Copy code

```
GRANT MONITOR ON FUTURE AGENTS IN SCHEMA <database_name>.<schema_name> TO ROLE <role_name>;
```
