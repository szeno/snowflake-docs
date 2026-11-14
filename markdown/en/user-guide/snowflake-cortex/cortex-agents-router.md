# Route questions between agents with the agent router

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

An agent with an `agent_router` tool sends each question to one of the agents you list as its
subagents. You can create a router agent with SQL in any schema and call it with the
[Cortex Agents Run API](/user-guide/snowflake-cortex/cortex-agents-run#label-snowflake-data-agents-run-rest-api)
or [DATA\_AGENT\_RUN](/sql-reference/functions/data_agent_run-snowflake-cortex), without CoWork Admin
or Snowflake CoWork.

## Before you begin

- The role that creates the agent needs `CREATE AGENT` on the schema.
- The calling role needs one of the
  [API access roles](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-access-control)
  for Cortex Agents, plus `USAGE` on the router agent and on each subagent.

## Create a router agent

Copy code

```
CREATE AGENT MY_DB.MY_SCHEMA.ROUTER_AGENT
  FROM SPECIFICATION $$
models:
  orchestration: auto
tools:
  - tool_spec:
      type: agent_router
      name: router
tool_resources:
  router:
    subagents:
      - name: MY_DB.MY_SCHEMA.SALES_AGENT
        description: Answers questions about pipeline, quota, and closed deals.
      - name: MY_DB.MY_SCHEMA.SUPPORT_AGENT
        description: Answers questions about open tickets and escalations.
$$;
```

The key under `tool_resources` must match the router tool’s `name`, which is `router` in this
example. Without a matching entry, calls fail with error `399518`.

Each `subagents` entry takes these fields:

| Field | Description |
| --- | --- |
| `name` | Fully qualified name of the agent. Also the value returned as `subagent_name`. |
| `description` | Optional. What the agent is for. The router reads it when choosing an agent, and uses it to tell users which agent they can’t access. |

Expand

Show lessSee more

## Call the router agent

Copy code

```
SELECT TRY_PARSE_JSON(SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
  'MY_DB.MY_SCHEMA.ROUTER_AGENT',
  $${ "messages": [{ "role": "user", "content": [{ "type": "text", "text": "How many deals closed last quarter?" }] }] }$$
)) AS response;
```

With the REST API, send the same body to
`/api/v2/databases/MY_DB/schemas/MY_SCHEMA/agents/ROUTER_AGENT:run`.

When the router sends the question to a subagent, the response includes a `tool_use` item of type
`agent_router`. In its `input`, `subagent_name` is the agent that received the question:

Copy code

```
{
  "type": "tool_use",
  "tool_use": {
    "type": "agent_router",
    "input": { "subagent_name": "MY_DB.MY_SCHEMA.SALES_AGENT" }
  }
}
```

With `orchestration.tool_not_accessible: accept`, subagents the caller can’t use are skipped with
warning `399569`. With `reject`, they fail the request. For more information, see
[Inaccessible tool handling](/user-guide/snowflake-cortex/cortex-agents-inaccessible-tool-handling).

## Routing depth

Routing goes one level. A subagent reached through a router runs without its own `agent_router`
tool, so it can’t route further. To reach an agent more than one level down, list it in the
top-level router’s `subagents`, or give the intermediate agent that agent’s tools with an
[agent toolset](/user-guide/snowflake-cortex/cortex-agents-toolsets).

## Route between agents in Snowflake CoWork

A router agent that you attach to the Snowflake CoWork object is a Snowflake CoWork profile, and it
can live in any schema. For profile setup, see
[Set up profile routing in Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/set-up-cowork-profile-routing).
