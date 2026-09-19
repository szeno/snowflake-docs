# Working with temporary agents

In addition to permanent agents, which is the default type when creating agents in Snowflake, Snowflake supports defining agents as temporary. Temporary agents are especially useful for scenarios where an agent object does not need to persist beyond the current session. For example, you can use them for dynamically constructed agents in one-off workflows, testing, or ephemeral agentic pipelines.

## Overview

Snowflake supports creating temporary agents for storing non-permanent, session-scoped agent configurations. By default, a temporary agent created with `CREATE TEMPORARY AGENT` exists only in the session in which it was created and persists for the remainder of that session. It is bound to the creating user, role, and session: other users and other sessions cannot see or use it. When the session ends, the agent object is automatically dropped and is not recoverable.

Temporary agents are useful in the following scenarios:

- Programmatic agent construction during a script or pipeline run where the agent configuration does not need to be reused.
- Testing agent tool configurations or model settings without creating a persistent object.
- Session-isolated agentic workflows where each session requires a distinct agent configuration.
- Reducing object management overhead in development and experimentation environments.

## Creating a temporary agent

To create a temporary agent, specify the `TEMPORARY` keyword (or `TEMP` abbreviation) in [CREATE AGENT](/sql-reference/sql/create-agent):

Copy code

```
-- TEMP is an accepted abbreviation of TEMPORARY
CREATE TEMPORARY AGENT my_temp_agent
  FROM SPECIFICATION
  $$
  models:
    orchestration: claude-sonnet-4-6
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "Analyst1"
  tool_resources:
    Analyst1:
      semantic_view: "my_db.my_schema.my_model"
  $$;
```

Note

Creating a temporary agent does not require the CREATE AGENT privilege on the schema in which the object is created. After creation, temporary agents cannot be converted to a permanent agent type.

## Interacting with a temporary agent

Once created, a temporary agent can be used in the same ways as a permanent agent within the same session. You can invoke it via the Cortex Agents REST API or via SQL:

Copy code

```
-- Invoke a temporary agent via the REST API (same endpoint as permanent agents)
POST /api/v2/databases/{database}/schemas/{schema}/agents/my_temp_agent:run
{
  "messages": [{ "role": "user", "content": [{ "type": "text", "text": "What were total sales last quarter?" }] }]
}
```

The agent behaves identically to a permanent agent during the session. All tool calls, conversation turns, and model interactions proceed normally. The only difference is that the agent object is automatically dropped when the session ends.

## Versioning and the LIVE version

Temporary agents operate exclusively on the LIVE version. Because temporary agents are session-scoped and not intended for long-term use, `ALTER AGENT ... COMMIT` and named version aliases (for example, `production`, `staging`) are not supported for temporary agents. All changes made to a temporary agent within a session apply directly to the LIVE version.

Note

Temporary agents do not support versioning operations (`COMMIT`, `VERSION$N`, or aliases). If you need versioning support, create a permanent agent instead. For permanent agent versioning, see [Cortex Agent versioning](/user-guide/snowflake-cortex/cortex-agents-versioning).

## Potential naming conflicts with permanent agents

Similar to temporary tables, temporary agents belong to a specified database and schema; however, because they are session-based, they are not bound by the same uniqueness requirements as permanent agents. This means you can create a temporary agent and a permanent agent with the same name within the same schema.

When a naming conflict exists, the temporary agent takes precedence within the session over any permanent agent with the same name in the same schema. This means:

- All agent invocations and DDL operations within the session target the temporary agent.
- The underlying permanent agent is hidden for the duration of the session but is not affected.
- Once the session ends and the temporary agent is dropped, the permanent agent becomes visible again.

Important

Use distinct names for temporary and permanent agents to avoid unexpected behavior, particularly in shared schema environments or when running automated pipelines.

## Explicitly dropping a temporary agent

Although temporary agents are automatically dropped when the session ends, Snowflake recommends explicitly dropping temporary agents once they are no longer needed. This is especially important in long-running sessions to keep the agent namespace clean and avoid potential naming conflicts.

Copy code

```
DROP AGENT my_temp_agent;
```

## Comparison of agent types

The following table summarizes the differences between permanent and temporary agents:

| Field | Temporary | Permanent |
| --- | --- | --- |
| Lifetime | Remainder of session | Until explicitly dropped |
| Visibility | Bound to the creating user, role, and session | All users with appropriate privileges |
| Versioning | LIVE version only; `COMMIT` and aliases not supported | Full versioning: `COMMIT`, `VERSION$N`, aliases (`production`, `staging`) |
| Time Travel / Fail-safe | None | Standard Snowflake Time Travel applies |

Expand

Show lessSee more

## Additional notes

### Automatic cleanup

When a session ends, whether by explicit logout, timeout, or connection termination, all temporary agents created in that session are automatically dropped by Snowflake. There is no recovery path once a temporary agent is dropped. If you need to reuse an agent configuration across sessions, create a permanent agent.

### Supported operations

The following operations are supported for temporary agents within the session:

- `CREATE TEMPORARY AGENT` / `CREATE TEMP AGENT`
- [ALTER AGENT](/sql-reference/sql/alter-agent) (modifications apply to the LIVE version only)
- [DESCRIBE AGENT](/sql-reference/sql/desc-agent)
- [SHOW AGENTS](/sql-reference/sql/show-agents) (temporary agents are visible in SHOW AGENTS output for the current session)
- [DROP AGENT](/sql-reference/sql/drop-agent)
- REST API invocation (`agent:run`)

### Unsupported operations

The following operations are not supported for temporary agents:

- `ALTER AGENT ... COMMIT` (version promotion)
- `VERSION$N` references or version aliases
- `SHOW VERSIONS IN AGENT`
