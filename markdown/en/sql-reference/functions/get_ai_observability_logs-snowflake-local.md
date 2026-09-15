Categories:
:   [Table functions](/sql-reference/functions-table) (Cortex Agents)

# GET\_AI\_OBSERVABILITY\_LOGS (SNOWFLAKE.LOCAL)

Retrieve log data for an AI Observability event, such as a warning or failure, for a Cortex Agent or an External Agent application (see [External Agent commands](/sql-reference/commands-external-agent)).

Call this function to retrieve information about what events occurred during an evaluation run. For more information, see [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations) and [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events).

See also:
:   [GET\_AI\_OBSERVABILITY\_EVENTS (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_observability_events-snowflake-local) , [GET\_AI\_RECORD\_TRACE (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_record_trace-snowflake-local) , [GET\_AI\_EVALUATION\_DATA (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_evaluation_data-snowflake-local) , [EXECUTE\_AI\_EVALUATION](/sql-reference/functions/execute_ai_evaluation)

## Syntax

Copy code

```
SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_LOGS( <database>, <schema>, <agent_name>, <agent_type> )
```

## Arguments

`database`
:   Name of the database containing the agent.

`schema`
:   Name of the schema containing the agent.

`agent_name`
:   Name of the agent to retrieve a record for.

`agent_type`
:   The agent type string. Use `CORTEX AGENT` for a Cortex Agent evaluation or `EXTERNAL AGENT` for an External Agent object (see [External Agent commands](/sql-reference/commands-external-agent)). This value is case-insensitive.

## Returns

For details on the information contained in AI Observability events, see [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CORTEX\_USER | Database role |  |
| USAGE | Cortex Agent or External Agent | Required on the object identified by `agent_name`. For `EXTERNAL AGENT`, USAGE on the External Agent is sufficient to call this function (MONITOR does not apply). |
| MONITOR | Cortex Agent | Required on the Cortex Agent identified by `agent_name` when `agent_type` is `CORTEX AGENT`. Does not apply when `agent_type` is `EXTERNAL AGENT`. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

When `agent_type` is `EXTERNAL AGENT`, only USAGE on that object is required to call this function. OWNERSHIP on the External Agent is required to modify or remove the object with [ALTER EXTERNAL AGENT](/sql-reference/sql/alter-external-agent) or [DROP EXTERNAL AGENT](/sql-reference/sql/drop-external-agent).

For the full access control permissions required by Cortex Agent evaluations, see [Cortex Agent evaluations: access control requirements](/user-guide/snowflake-cortex/cortex-agents-evaluations#label-agent-evaluation-access-control). For External Agent objects, see [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events).

## Examples

The following example checks for errors and warnings for a run called `run-1`, where the agent is named `evaluated_agent` stored on the schema `eval_db.eval_schema`:

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_LOGS(
  'eval_db',
  'eval_schema',
  'evaluated_agent',
  'CORTEX AGENT')
)
  WHERE TRUE
    AND (record:"severity_text"='ERROR' or record:"severity_text"='WARN')
    AND record_attributes:"snow.ai.observability.run.name"='run-1';
```
