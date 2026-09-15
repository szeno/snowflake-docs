Categories:
:   [Table functions](/sql-reference/functions-table) (AI Observability)

# GET\_AI\_OBSERVABILITY\_EVENTS (SNOWFLAKE.LOCAL)

Return AI Observability events from the `AI_OBSERVABILITY_EVENTS` table in the [LOCAL schema](/sql-reference/local). Pass an **agent type** that matches the object you are inspecting:

- `CORTEX AGENT` for a Cortex Agent (see [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor))
- `EXTERNAL AGENT` for an External Agent object used with TruLens (see [External Agent commands](/sql-reference/commands-external-agent))
- `CORTEX SEARCH SERVICE` for a Cortex Search service with `REQUEST_LOGGING` enabled (see [Monitor Cortex Search requests](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor))

Each row uses the [event table column layout](/developer-guide/logging-tracing/event-table-columns) (including `RECORD`, `RECORD_ATTRIBUTES`, `VALUE`, and trace fields). Events can represent conversation activity, spans (planning, tools, response generation), Cortex Search request bodies, logs, user feedback, and other telemetry written for the object.

For Snowsight workflows and examples of filtering events (including feedback), see [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor). For how AI Observability stores data in the event table, see [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events).

Direct `SELECT` on `AI_OBSERVABILITY_EVENTS` bypasses object scoping and is for limited admin use only. Prefer this function for routine monitoring of a Cortex Agent, External Agent, or Cortex Search service.

See also:
:   [GET\_AI\_OBSERVABILITY\_LOGS (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_observability_logs-snowflake-local), [GET\_AI\_RECORD\_TRACE (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_record_trace-snowflake-local), [GET\_AI\_EVALUATION\_DATA (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_evaluation_data-snowflake-local)

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_EVENTS( <database>, <schema>, <agent_name>, <agent_type> )
```

## Arguments

`database`
:   Name of the database containing the object.

`schema`
:   Name of the schema containing the object.

`agent_name`
:   Name of the Cortex Agent, External Agent, or Cortex Search service whose observability events you want to retrieve.

`agent_type`
:   The object type string. Use `CORTEX AGENT` for a Cortex Agent, `EXTERNAL AGENT` for an External Agent object, or `CORTEX SEARCH SERVICE` for a Cortex Search service. This value is case-insensitive.

## Returns

A table of observability events. Column definitions follow the [event table schema](/developer-guide/logging-tracing/event-table-columns). Filter and project with standard SQL (for example on `RECORD:name`, `RECORD_ATTRIBUTES`, or severity fields inside `RECORD`) to narrow to specific event kinds.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CORTEX\_USER | Database role |  |
| USAGE | External Agent | Required on the External Agent identified by `agent_name` when `agent_type` is `EXTERNAL AGENT`. USAGE is sufficient to call this function; MONITOR does not apply. |
| MONITOR | Cortex Agent | Required on the Cortex Agent identified by `agent_name` when `agent_type` is `CORTEX AGENT`. |
| MONITOR | Cortex Search Service | Required on the Cortex Search service identified by `agent_name` when `agent_type` is `CORTEX SEARCH SERVICE`. Request logging must be enabled on the service. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

When `agent_type` is `EXTERNAL AGENT`, only USAGE on that object is required to call this function. OWNERSHIP on the External Agent is required to modify or remove the object with [ALTER EXTERNAL AGENT](/sql-reference/sql/alter-external-agent) or [DROP EXTERNAL AGENT](/sql-reference/sql/drop-external-agent).

For typical Cortex Agent monitoring setup (including grants for future agents), see [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor). For Cortex Search request logs, see [Monitor Cortex Search requests](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor). For External Agent access to observability data, see [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events).

## Examples

Return observability events for an agent:

Copy code

```
SELECT *
  FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_EVENTS(
    'my_database',
    'my_schema',
    'my_agent',
    'CORTEX AGENT'
  ));
```

To list only user feedback events, filter on the event name (see [View feedback provided by users](/user-guide/snowflake-cortex/cortex-agents-monitor#label-cortex-agents-view-feedback)):

Copy code

```
SELECT *
  FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_EVENTS(
    'my_database',
    'my_schema',
    'my_agent',
    'CORTEX AGENT'
  ))
  WHERE RECORD:name = 'CORTEX_AGENT_FEEDBACK';
```

The same function works for an externally instrumented application by passing `EXTERNAL AGENT` as `agent_type` and the External Agent object name in `agent_name` (see [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events)).

Return request logs for a Cortex Search service (`REQUEST_LOGGING` must be enabled on the service):

Copy code

```
SELECT *
  FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_EVENTS(
    'my_database',
    'my_schema',
    'my_search_service',
    'CORTEX SEARCH SERVICE'
  ));
```

For filtering and output fields, see [Monitor Cortex Search requests](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor).
