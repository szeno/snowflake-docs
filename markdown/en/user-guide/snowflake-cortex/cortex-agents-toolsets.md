# Agent toolsets

An agent toolset lets one agent reference another agent by its fully qualified name and inherit that agent’s
tools at run time. When the calling agent runs, Snowflake resolves the referenced agent, verifies that the
caller has USAGE privilege on it, reads the referenced agent’s tool configuration, and unions those tools into
the calling agent’s effective tool set. The orchestrator only ever sees the flat, fully-expanded tools — the
`agent_toolset` entry itself is never forwarded.

This lets you build modular, composable agent architectures. For example, you can create a “toolkit” agent
that bundles a set of related tools (weather lookup, calculator, data fetcher) and then reference it from
multiple calling agents without duplicating the tool definitions in each one.

## How agent toolsets work

When a calling agent with an `agent_toolset` tool receives a request:

1. Snowflake reads the `tool_resources[<tool_name>].agent_name` field to identify the referenced agent.
2. Snowflake resolves the referenced agent by its fully qualified name and authorizes USAGE under the calling
   user’s role.
3. Snowflake reads the referenced agent’s stored specification and extracts its `tools` and `tool_resources`.
4. The referenced agent’s tools are unioned into the calling agent’s effective configuration.
5. The expanded tool set is sent to the orchestrator. The `agent_toolset` entry is removed.

This resolution happens recursively: if a referenced agent itself contains `agent_toolset` references, those
are expanded in turn, up to the configured depth and fan-out limits.

### Conflict resolution

When the calling agent and a referenced agent both define a tool with the same name, the calling agent’s
definition takes precedence. This lets you override an inherited tool locally without modifying the referenced
agent.

### Recursion prevention

To prevent infinite loops, Snowflake enforces the following limits:

- **Cycle detection**: A visited-set depth-first search prevents cycles. If agent A references agent B and
  agent B references agent A, the run fails with a cycle error.
- **Maximum depth**: The resolution traverses at most 5 levels of nesting (configurable by the account
  parameter `CORTEX_AGENT_TOOLSET_MAX_DEPTH`).
- **Maximum agents**: A single run expands at most 25 referenced agents total (configurable by the account
  parameter `CORTEX_AGENT_TOOLSET_MAX_AGENTS`).

### Access failures

If the calling user’s role lacks USAGE on a referenced agent, or the referenced agent does not exist, the
reference is silently skipped. The run still succeeds with the calling agent’s own tools. No error or
annotation is produced for the dropped reference.

## Configure an agent toolset

To add an agent toolset reference, include a tool with `type: agent_toolset` in the agent’s specification
and provide the referenced agent’s fully qualified name in `tool_resources`.

### Spec shape

Copy code

```
tools:
  - tool_spec:
      type: agent_toolset
      name: my_toolset
tool_resources:
  my_toolset:
    agent_name: MY_DB.MY_SCHEMA.REFERENCED_AGENT
```

The `name` field identifies the toolset reference and must match a key in `tool_resources`. The
`agent_name` field is the fully qualified name of the referenced agent (`database.schema.agent_name`).

### Create an agent with a toolset reference

SQLREST API

Copy code

```
CREATE AGENT my_db.my_schema.my_agent
  COMMENT = 'Agent that inherits tools from another agent'
  FROM SPECIFICATION $$
tools:
  - tool_spec:
      type: generic
      name: local_tool
  - tool_spec:
      type: agent_toolset
      name: shared_tools
tool_resources:
  shared_tools:
    agent_name: MY_DB.MY_SCHEMA.TOOLKIT_AGENT
$$;
```

Copy code

```
curl -X POST "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/databases/MY_DB/schemas/MY_SCHEMA/agents" \
  --header 'Content-Type: application/json' \
  --header "Authorization: Bearer $PAT" \
  --data '{
    "name": "MY_AGENT",
    "spec": {
      "models": {
        "orchestration": "claude-sonnet-4-6"
      },
      "tools": [
        {"tool_spec": {"type": "generic", "name": "local_tool"}},
        {"tool_spec": {"type": "agent_toolset", "name": "shared_tools"}}
      ],
      "tool_resources": {
        "shared_tools": {
          "agent_name": "MY_DB.MY_SCHEMA.TOOLKIT_AGENT"
        }
      }
    }
  }'
```

### Reference multiple agents

You can include multiple `agent_toolset` entries in a single agent. Each one is resolved independently:

Copy code

```
tools:
  - tool_spec:
      type: agent_toolset
      name: analytics_tools
  - tool_spec:
      type: agent_toolset
      name: communication_tools
tool_resources:
  analytics_tools:
    agent_name: MY_DB.MY_SCHEMA.ANALYTICS_AGENT
  communication_tools:
    agent_name: MY_DB.MY_SCHEMA.COMMS_AGENT
```

Tools from `analytics_tools` are expanded first. If `communication_tools` defines a tool with the same name
as one already present from `analytics_tools` or the calling agent, the earlier definition wins.

## Access control

The calling user’s role must have USAGE on both the calling agent and the referenced agent. The referenced
agent is resolved under the caller’s identity at run time, not at agent creation time.

| Privilege | Object | Required for |
| --- | --- | --- |
| USAGE | Calling agent | Running the agent |
| USAGE | Referenced agent | Expanding the toolset reference (silently skipped if missing) |
| USAGE | Database, schema | Accessing the database and schema containing each agent |

Expand

Show lessSee more

Because the referenced agent is resolved at run time, the referenced agent does not need to exist when the
calling agent is created. This supports workflows where you create agents in any order and grant privileges
later.

## Limitations

- **Write-time validation only checks structure**: At creation time, Snowflake validates that the
  `agent_toolset` tool has a name and that `tool_resources[<name>].agent_name` is non-empty. It does not
  resolve or authorize the referenced agent.
- **Run-time resolution**: If the referenced agent is dropped or privileges are revoked after the calling
  agent is created, the reference is silently skipped at run time.
- **No partial expansion**: If a referenced agent cannot be resolved, all of its tools are dropped. There is
  no partial inheritance.
- **Depth and fan-out limits**: Recursive expansion is bounded. Exceeding the configured limits results in a
  run error.
- **Cycle detection**: Circular references (direct or indirect) cause the run to fail.
