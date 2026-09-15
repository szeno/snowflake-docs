# Inaccessible tool handling

By default, `orchestration.tool_not_accessible` is `accept`: a Cortex Agent run continues when the caller’s role can’t access any of the tools in the agent specification. If you omit the field, Snowflake uses `accept`. This applies to agent runs from the REST API, SQL, and conversations in Snowflake CoWork. The agent uses the tools that role can access and reports the rest as warnings. You don’t need a separate agent object for each privilege class.

Configure this behavior on the agent specification with `orchestration.tool_not_accessible`. The setting applies when you create or update an agent object, and when you pass the full specification to `POST /api/v2/cortex/agent:run`. You can’t change it on an `agents/{name}:run` request; update the agent object instead.

There is no account-level setting for this behavior. Set the mode in each agent specification. For direct calls to `POST /api/v2/cortex/agent:run` that don’t use an agent object, set the mode in each request body.

## Where to set the field

An agent specification contains three different keys named `orchestration`. Set `tool_not_accessible` on the top-level one:

| Field | Type | What it holds |
| --- | --- | --- |
| `orchestration` | [OrchestrationConfig](/user-guide/snowflake-cortex/cortex-agents-rest-api#label-snowflake-agent-object-orchestrationconfig) object | Run controls: `tool_not_accessible`, `budget`, and `capabilities`. Set `tool_not_accessible` here. |
| `models.orchestration` | string | The orchestration model, for example `claude-4-sonnet`. |
| `instructions.orchestration` | string | Natural-language instructions that steer tool selection. |

Expand

Show lessSee more

The following specification sets all three. Only the top-level `orchestration` block controls inaccessible-tool handling:

Copy code

```
models:
  orchestration: claude-4-sonnet

orchestration:
  tool_not_accessible: accept
  budget:
    seconds: 30
    tokens: 16000

instructions:
  orchestration: 'Use the search tool for all refund questions.'
```

The same specification in JSON:

Copy code

```
{
  "models": {
    "orchestration": "claude-4-sonnet"
  },
  "orchestration": {
    "tool_not_accessible": "accept",
    "budget": {
      "seconds": 30,
      "tokens": 16000
    }
  },
  "instructions": {
    "orchestration": "Use the search tool for all refund questions."
  }
}
```

## Access modes

Set `tool_not_accessible` on the top-level `orchestration` object, as shown in [Where to set the field](#label-cortex-agents-inaccessible-tool-where-to-set). Values are case-insensitive.

| Value | Behavior |
| --- | --- |
| `accept` | Continue the run. Snowflake emits a `response.warning` event for each inaccessible tool that the caller named, and the agent uses the remaining accessible tools. This is the default when the field is omitted. |
| `reject` | Collect every inaccessible tool in the checked set, then reject the run with a single HTTP 4XX error that lists all of them. |
| `legacy` | Reject the run at the first inaccessible Cortex Search, Cortex Analyst, MCP, or skill tool. Use this when a caller depends on that first-failure HTTP 4XX wire format. |

Expand

Show lessSee more

## Which tools Snowflake checks

In every mode, Snowflake checks access at the start of the run for Cortex Search (`cortex_search`), Cortex Analyst (`cortex_analyst_text_to_sql`), MCP (`mcp`), and skill (`skill`) tools.

The following tools aren’t included in this pre-check. If the caller lacks privileges on them, the run still starts. A call to one of these tools fails at execution time, the agent receives that failure as a tool result, and it continues reasoning and tries to answer with what it has:

- Custom tools (`generic` and `function` types, including user-defined functions and stored procedures)
- SQL execution (`sql_exec`)
- Code execution (`code_execution`)
- Any other tool type

`agent_toolset` references are unchanged: if the caller lacks `USAGE` on the referenced agent, Snowflake skips that reference and continues. For details, see [Agent toolsets](/user-guide/snowflake-cortex/cortex-agents-toolsets).

## Named tools versus discovered tools

How Snowflake reports an inaccessible resource depends on whether the caller named it:

- **Named in the specification:** If `tool_resources` points at a specific object (a Cortex Search service, semantic view or model, skill, or MCP `server_name`), Snowflake treats that resource as explicit. In `accept` mode you get a warning. In `reject` or `legacy` mode the run can fail.
- **Discovered for you:** If Snowflake enumerates the resource set (for example, MCP `selection: all`), inaccessible items are omitted with no warning. The caller never named those objects, so Snowflake doesn’t list them.

## Behavior by tool

### Cortex Search

Each search tool is checked independently. If the caller’s role lacks `USAGE` on that Cortex Search service, that tool is inaccessible. Other search tools in the same spec are unaffected.

### Cortex Analyst

Snowflake checks whether the caller can access the semantic model or semantic view behind the tool. If it can’t, the entire Analyst tool is inaccessible.

This check doesn’t cover the objects inside the model, such as `SELECT` on the tables it references or `USAGE` on an embedded Cortex Search service. A missing privilege on one of those objects surfaces later, when Analyst runs.

### Skills

Each skill is its own tool entry. An inaccessible skill doesn’t block other skills in the same spec.

### MCP servers

When `tool_resources` includes an explicit `server_name`, a missing server or missing `USAGE` on that MCP server makes that MCP tool inaccessible.

When the agent uses MCP `selection: all`, Snowflake includes only the servers the caller can use. Servers the caller can’t use are omitted with no warning.

Configuration and availability issues after the server is authorized (for example, an unresolved URL or an incomplete OAuth flow) still surface as the existing `response.warning` events. Those aren’t access-mode failures.

## Warnings and errors

In `accept` mode, Snowflake sends one `event: response.warning` per inaccessible named tool before the first model call. The stream then continues. Warning text doesn’t distinguish “the object doesn’t exist” from “the object exists but this role isn’t authorized.” Both cases use the same message.

Example:

Copy code

```
event: response.warning
data: {"code": "399569", "message": "TOOL_NOT_ACCESSIBLE: Search1 (cortex_search) - The Cortex Search Service does not exist or access is not authorized for the current role: db.schema.css1"}
```

Clients that already handle `response.warning` (for example, MCP availability warnings) don’t need a new event type.

In `reject` mode, the HTTP 4XX body lists every inaccessible tool in the checked set. In `legacy` mode, the HTTP 4XX body describes the first Cortex Search, Analyst, MCP, or skill failure.

Where the warning appears depends on how you run the agent:

- **Cortex Agents REST API, streaming response:** The client receives a `response.warning` SSE event before the first model call. Applications should display or otherwise handle this event so users know the answer might not use every configured tool.
- **Cortex Agents REST API, non-streaming response:** The final JSON response includes the warning in its top-level `warnings` array.
- **`SNOWFLAKE.CORTEX.DATA_AGENT_RUN`:** The function returns the final aggregated JSON response, including the top-level `warnings` array. Parse the returned string as JSON to inspect it.
- **Snowflake CoWork:** The warning is displayed with the answer in the conversation.

For example, a non-streaming REST response or parsed `DATA_AGENT_RUN` result includes:

Copy code

```
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "..."
    }
  ],
  "warnings": [
    {
      "code": "399569",
      "message": "TOOL_NOT_ACCESSIBLE: Search1 (cortex_search) - The Cortex Search Service does not exist or access is not authorized for the current role: db.schema.css1"
    }
  ]
}
```

The warning is also recorded in the agent trace in `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS`, so administrators can audit it after the run. View the trace in the agent **Observability** tab or query it with [GET\_AI\_OBSERVABILITY\_EVENTS (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_observability_events-snowflake-local). Entries in the event table can’t be modified. For access requirements and query examples, see [Query Cortex Agent logs with SQL](/user-guide/snowflake-cortex/cortex-agents-monitor#label-cortex-agents-query-observability-events).

## Choose a mode

- Use `accept` (the default) when one agent should serve users with different tool grants, and the agent can still answer with the remaining tools.
- Use `reject` when you want a strict gate: the run must not start unless every named, checked tool is accessible. The error lists all of those failures at once, which is useful when you’re debugging grants.
- Use `legacy` only if an existing client depends on a first-failure HTTP 4XX error for Search, Analyst, MCP, or skills.

In `accept` mode, the agent tries to match the question to the tools the caller can access. If it isn’t confident those tools are enough, it typically explains that it needs access to more tools rather than guessing. If it is confident, it answers with the accessible tools. Give each tool a clear name and a detailed description in the specification so the agent can tell which inaccessible tools would have been relevant. This matching is best-effort: if a tool has no description, the agent has no way to know that tool was needed.

Granting the caller’s default role the privileges in [Additional privileges for tools](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-tool-privileges) is still required for any tool you expect the agent to use. Inaccessible-tool handling doesn’t bypass Snowflake privileges; it only controls whether a missing privilege aborts the whole run.

## Change the mode on a versioned agent

`tool_not_accessible` lives in the agent specification, so changing it means changing the spec of the version that serves your traffic.

Named versions are immutable. If your agent’s default version is a committed named version, editing the live version isn’t enough: commit a new named version with the mode you want, then point the default version or the alias your callers use at it.

Copy code

```
ALTER AGENT my_agent ADD LIVE VERSION FROM LAST;

-- SET SPECIFICATION replaces the whole specification, so include your existing settings.
ALTER AGENT my_agent MODIFY LIVE VERSION SET SPECIFICATION =
$$
<existing agent specification>
orchestration:
  tool_not_accessible: legacy
$$;

ALTER AGENT my_agent COMMIT COMMENT = 'Keep first-failure rejection';

ALTER AGENT my_agent SET DEFAULT_VERSION = LAST;
```

If your default version is already `LIVE`, updating the live version’s specification is enough. For the version lifecycle, see [Cortex Agent versioning](/user-guide/snowflake-cortex/cortex-agents-versioning).
