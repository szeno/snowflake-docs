# Coding Agent

A Coding Agent is a managed agent that brings Snowflake CoCo’s coding capabilities into your own applications through the Cortex Agents REST API or SQL. You add the `code_toolset_all` tool type to a Cortex Agent, and Snowflake provisions and manages a sandbox backed by the same runtime that powers CoCo (bash, file read/write/edit, grep, glob, web search, SQL execution, and skills), executes the tools, and streams results back to your application, so you don’t build or host an agent loop yourself. Any query that requires code generation, SQL execution, data transformation, or pipeline automation is handled inside the sandboxed runtime.

Use `code_toolset_all` when you want an autonomous coding agent with the full suite of development tools. It differs from two related surfaces:

- **`code_execution` tool**: a single Python sandbox tool you add alongside other agent tools (Cortex Analyst, Cortex Search). Use it when your agent’s primary function is not code generation. See [Cortex Agent code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool).
- **Cortex Code CLI**: the `cortex code` command-line client that runs locally on your machine. A Coding Agent exposes the same toolset as a hosted agent you call over the API instead.

`code_toolset_all` and `code_execution` are **mutually exclusive**: a single request can declare at most one of them. Specifying both returns an error.

## Quickstart

You can call a Coding Agent from two surfaces. Both accept the same core agent configuration — `messages`, `models`, `instructions`, `tools`, and `tool_resources` — so that part of the body is portable between them. Transport-specific fields are not: the REST API streams by default and accepts `stream`, while `AGENT_RUN` rejects `"stream": true` and always returns a single JSON value.

| Surface | Call | Response |
| --- | --- | --- |
| REST API | `POST /api/v2/cortex/agent:run` | Streams server-sent events (SSE) by default. Set `stream` to `false` for a single JSON response. |
| SQL | [AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/agent_run-snowflake-cortex) | A single JSON string. Streaming isn’t supported. |

Expand

Show lessSee more

Use the REST API when your application displays the agent’s tool calls and output as they happen. Use SQL when you want a coding agent inside a query, a stored procedure, or a scheduled task and don’t need incremental output.

To call either surface, use a role that has been granted the `SNOWFLAKE.CORTEX_USER` or `SNOWFLAKE.CORTEX_AGENT_USER` database role. See [API access roles](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-access-control). The REST API also requires an authorization token, such as a programmatic access token (PAT). In the example, `$SNOWFLAKE_ACCOUNT_BASE_URL` is your account URL (`https://<orgname>-<account_name>.snowflakecomputing.com`) and `$PAT` is that token.

The following examples need no agent object and no workspace: the entire configuration is in the request body, and the sandbox starts with an empty file system. They set the orchestration model to `auto`, which lets Snowflake select the highest-quality model available to your account. To pin a specific model instead, see [Orchestration model and instructions](#label-coding-agent-instructions).

REST APISQL

Copy code

```
curl -X POST "$SNOWFLAKE_ACCOUNT_BASE_URL/api/v2/cortex/agent:run" \
  --header 'Content-Type: application/json' \
  --header 'Accept: text/event-stream' \
  --header "Authorization: Bearer $PAT" \
  --data '{
    "models": { "orchestration": "auto" },
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Write a Python script that prints the first 10 Fibonacci numbers, run it, and show me the output."
          }
        ]
      }
    ],
    "tools": [
      { "tool_spec": { "type": "code_toolset_all", "name": "code_toolset_all" } }
    ],
    "tool_resources": {
      "code_toolset_all": {
        "permission_policy": { "type": "always_allow" }
      }
    }
  }'
```

Copy code

```
SELECT TRY_PARSE_JSON(
  SNOWFLAKE.CORTEX.AGENT_RUN(
    $${
      "models": { "orchestration": "auto" },
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Write a Python script that prints the first 10 Fibonacci numbers, run it, and show me the output."
            }
          ]
        }
      ],
      "tools": [
        { "tool_spec": { "type": "code_toolset_all", "name": "code_toolset_all" } }
      ],
      "tool_resources": {
        "code_toolset_all": {
          "permission_policy": { "type": "always_allow" }
        }
      }
    }$$,
    TRUE
  )
) AS resp;
```

The second argument creates a thread automatically and returns its `thread_id`, which you pass back in the next
request body to continue the conversation.

The response carries a `tool_use` and `tool_result` pair for each sandbox tool call the agent made, followed by a
final `text` block with its answer.

Both examples set `permission_policy` to `always_allow` so that a single call runs start to finish. The default,
`always_ask`, keeps an approval gate in front of state-modifying tool calls; the next two sections describe how each
surface handles it.

### Approve a tool call over the REST API

Under `always_ask`, the agent doesn’t execute a state-modifying tool call right away. It emits a `tool_use` event whose
`permission.options` array lists the choices available to the caller, and stops there.

To resume the turn, send another `agent:run` request that appends a `permission_decision` content block to the
conversation:

Copy code

```
{
  "role": "user",
  "content": [
    {
      "type": "permission_decision",
      "permission_decision": {
        "tool_use_id": "toolu_abc123",
        "decision": "Allow Once"
      }
    }
  ]
}
```

`tool_use_id` is the ID from the `tool_use` event, and `decision` must match one of the strings in that event’s
`permission.options` array. When you deny, add a `reason` explaining why: the agent receives it as the tool’s error
message and can adjust. For the field-level reference, see [PermissionDecision](#label-snowflake-agent-run-permissiondecision).

This is the approval loop an interactive application should implement: it keeps the gate in place and gives the user
the decision, so you don’t need `always_allow`.

### Approve a tool call from SQL

`AGENT_RUN` returns one JSON value per statement and can’t prompt, so it offers no interactive approval loop within a
single call. Under `always_ask`, the permission request comes back in the response and the statement ends without the
tool having run. Unattended callers — scheduled tasks, stored procedures — therefore need `always_allow`.

Important

`always_allow` removes the execution gate: the agent runs any command and modifies any resource its role can reach,
without confirmation. Before you set it, make sure every input to the run is trusted, including the prompt, the files
in any mounted workspace, attached skills, and content the agent fetches with `web_search` — any of these can steer
what the agent does. Run it under a least-privilege role that has access only to the data the task needs, and grant no
more than that. See [Sandbox permission policy](#label-coding-agent-permission-policy).

### Run longer than 15 minutes

REST API requests time out after 15 minutes, which a multi-step coding task can exceed. To run in the background
instead, create a thread, then set `"background": true` and `thread_id` in the request body. Reconnect to the run
with the [Stream Agent Run](/user-guide/snowflake-cortex/cortex-agents-run) endpoint, or, from SQL, poll
[THREAD\_MESSAGES (SNOWFLAKE.CORTEX)](/sql-reference/functions/thread_messages-snowflake-cortex) with the thread ID.

### Reuse a configuration

The previous examples configure the agent inline, which means every caller repeats the tool list and its resources. To
store the configuration once, create an [agent object](/user-guide/snowflake-cortex/cortex-agents-manage) whose
specification includes `code_toolset_all`, then reference it by name:

- REST API: `POST /api/v2/databases/{database}/schemas/{schema}/agents/{name}:run`
- SQL: [DATA\_AGENT\_RUN (SNOWFLAKE.CORTEX)](/sql-reference/functions/data_agent_run-snowflake-cortex)

### Next steps

- Give the agent durable files to work on: [Attaching a workspace](#label-coding-agent-workspace)
- Extend it with your own skills: [Attaching skills](#label-coding-agent-skills)
- Change its persona or orchestration model: [Orchestration model and instructions](#label-coding-agent-instructions)

## Included tools

When a request includes `code_toolset_all`, Snowflake automatically provisions the complete set of sandbox tools:

- **bash**: Execute shell commands
- **read**: Read file contents
- **write**: Create or overwrite files
- **edit**: Make targeted edits to existing files
- **grep**: Search file contents with regular expressions
- **glob**: Find files by pattern
- **web\_search**: Search the web
- **snowflake\_sql\_execute**: Execute SQL against Snowflake (read-only: `SELECT` and `SHOW` commands; can write to stages)
- **skill**: Execute agent skills

New tools added to the sandbox are automatically included without requiring changes to your request.

## Enabling the toolset

Add the `code_toolset_all` tool type to the `tools` list of your agent specification or request:

Copy code

```
{
  "tools": [
    {
      "tool_spec": {
        "type": "code_toolset_all",
        "name": "code_toolset_all"
      }
    }
  ]
}
```

No `tool_resources` entry is required for basic usage: the sandbox is provisioned automatically when this tool type is present. Most non-interactive callers still set one, because the default permission policy makes the agent ask before it runs a state-modifying tool. See [Sandbox permission policy](#label-coding-agent-permission-policy). The remaining sections describe optional configuration.

## Example request

The following `agent:run` request combines the most common configuration in a single call: the `code_toolset_all` tool, a mounted workspace, a skill attached from a Snowflake named stage, a disabled bundled skill, a permission policy, and orchestration model and instructions.

Copy code

```
{
  "messages": [
    {"role": "user", "content": [{"type": "text", "text": "Forecast next quarter's revenue and write the results to a file."}]}
  ],
  "models": {
    "orchestration": "claude-sonnet-4-5"
  },
  "instructions": {
    "system": "You are a data analysis assistant. Prefer Python with pandas for data manipulation."
  },
  "tools": [
    {
      "tool_spec": {
        "type": "code_toolset_all",
        "name": "code_toolset_all"
      }
    }
  ],
  "skills": [
    {
      "name": "forecaster",
      "source": {
        "type": "STAGE",
        "path": "@db1.schema1.skill_stage/skills/forecaster"
      }
    }
  ],
  "tool_resources": {
    "code_toolset_all": {
      "permission_policy": { "type": "always_allow" },
      "workspace_mounts": [
        {
          "name": "USER$.PUBLIC.DEFAULT$",
          "type": "workspace",
          "mount_path": "/workspace"
        }
      ],
      "disabled_skills": ["streamlit"]
    }
  }
}
```

Skills are declared in the top-level `skills` array (not under `tool_resources`), matching how skills are attached to a persistent agent. Sandbox behavior (permission policy, workspace mounts, and disabled skills) is configured under `tool_resources.code_toolset_all`.

## Sandbox permission policy

By default, tools that modify state (such as `bash`, `write`, `edit`, and `snowflake_sql_execute`) require user approval before execution. The caller delivers that approval as a `permission_decision` block on the next request; see [Approve a tool call over the REST API](#label-coding-agent-approve-rest). Control this behavior with `permission_policy` in `tool_resources` under the tool’s name.

| Policy value | Behavior |
| --- | --- |
| `always_ask` | Always prompt the user for approval before executing state-modifying tools (default) |
| `always_allow` | Skip permission checks and execute all tools without user approval |

Expand

Show lessSee more

Copy code

```
{
  "tools": [
    { "tool_spec": { "type": "code_toolset_all", "name": "code_toolset_all" } }
  ],
  "tool_resources": {
    "code_toolset_all": {
      "permission_policy": { "type": "always_allow" }
    }
  }
}
```

Important

Setting `permission_policy` to `always_allow` means the agent can execute any command or modify any accessible file without user confirmation. Only use this setting in trusted, automated workflows where human-in-the-loop approval is not needed.

The `permission_policy` field also applies to the `code_execution` tool type. See [Cortex Agent code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool).

## Attaching a workspace

To give the sandbox access to files in a Snowflake workspace, specify `workspace_mounts` in `tool_resources` under the tool’s name. Each entry describes a workspace to mount into the sandbox container:

Copy code

```
{
  "tools": [
    { "tool_spec": { "type": "code_toolset_all", "name": "code_toolset_all" } }
  ],
  "tool_resources": {
    "code_toolset_all": {
      "workspace_mounts": [
        {
          "name": "USER$.PUBLIC.DEFAULT$",
          "type": "workspace",
          "mount_path": "/workspace"
        }
      ]
    }
  }
}
```

The `workspace_mounts` array fields:

| Field | Description |
| --- | --- |
| `name` | Fully qualified Snowflake workspace name (for example, `USER$.PUBLIC.DEFAULT$`). Required. |
| `type` | Mount type. Use `workspace` for Snowflake workspaces. Defaults to `workspace` if omitted. |
| `mount_path` | Container filesystem path where the workspace is mounted. Defaults to `/workspace` if omitted. |

Expand

Show lessSee more

You can mount multiple workspaces by including multiple entries in the `workspace_mounts` array:

Copy code

```
"workspace_mounts": [
  {
    "name": "USER$.PUBLIC.DEFAULT$",
    "type": "workspace",
    "mount_path": "/workspace"
  },
  {
    "name": "DB.SCHEMA.SHARED_DATA",
    "type": "workspace",
    "mount_path": "/data"
  }
]
```

The workspace must exist and have a live version before it can be mounted. Workspaces are mounted read-write at version `live` by default. Skills defined in the mounted workspace (under `.snowflake/cortex/skills/`) are automatically attached to the agent session.

Note

The `mount_path` must be a **top-level** absolute path (for example, `/workspace`, `/project`, `/data`). Nested paths like `/workspace/mydata` are not supported: the sandbox runtime creates a symlink at the specified path but does not create intermediate parent directories. Each workspace requires a unique top-level mount path.

The `name` must be a Snowflake **workspace** object (created with `CREATE WORKSPACE`), not a regular internal stage. Regular stages cannot be mounted as workspaces.

## Attaching skills

The sandbox exposes skills to the agent from three sources:

- **Bundled skills**: Snowflake-provided skills (such as charting and dashboard skills) are included in every `code_toolset_all` sandbox by default. Use `disabled_skills` to remove ones you don’t want.
- **Workspace skills**: skills under `.snowflake/cortex/skills/` in a mounted workspace are attached automatically (see [Attaching a workspace](#attaching-a-workspace)).
- **Stage-based skills**: skills stored in a Snowflake named stage or Git repository, attached through the agent’s `skills` list.

Stage-based skills use the same mechanism documented in [Agent skills](/user-guide/snowflake-cortex/cortex-agents-skills): store each skill folder (with its `SKILL.md` and any scripts) in a named stage, then reference it in the top-level `skills` array. When the request also includes `code_toolset_all`, Snowflake mounts each referenced stage skill read-only into the sandbox and the agent can invoke it like any bundled skill, including running the skill’s Python scripts, since the sandbox provides the code execution environment those skills require.

Copy code

```
{
  "messages": [
    {"role": "user", "content": [{"type": "text", "text": "Use the forecaster skill on this dataset."}]}
  ],
  "tools": [
    { "tool_spec": { "type": "code_toolset_all", "name": "code_toolset_all" } }
  ],
  "skills": [
    {
      "name": "forecaster",
      "source": {
        "type": "STAGE",
        "path": "@db1.schema1.skill_stage/skills/forecaster"
      }
    }
  ]
}
```

The `USAGE` privilege on the stage is required to read the skill files. For the full skill authoring, storage, and management workflow (including Git-backed skills and skills with code), see [Agent skills](/user-guide/snowflake-cortex/cortex-agents-skills).

## Disabling skills

By default, the `code_toolset_all` sandbox includes all bundled skills. Selectively disable specific bundled skills using the `disabled_skills` field in `tool_resources`:

Copy code

```
{
  "tools": [
    { "tool_spec": { "type": "code_toolset_all", "name": "code_toolset_all" } }
  ],
  "tool_resources": {
    "code_toolset_all": {
      "disabled_skills": ["dashboard", "streamlit"]
    }
  }
}
```

The `disabled_skills` array contains the names of bundled skills to remove from the sandbox session. Disabled skills are not visible to the agent and cannot be invoked. This is useful when you want to restrict the agent to a subset of capabilities.

## Orchestration model and instructions

Customize the agent’s behavior with system-level `instructions`. When using `instructions`, use the `models` field (not `model`) to specify the orchestration model.

Copy code

```
{
  "messages": [
    {"role": "user", "content": [{"type": "text", "text": "help me analyze this data"}]}
  ],
  "tools": [
    { "tool_spec": { "type": "code_toolset_all", "name": "code_toolset_all" } }
  ],
  "models": {
    "orchestration": "claude-sonnet-4-5"
  },
  "instructions": {
    "system": "You are a data analysis assistant. Always use Python with pandas for data manipulation."
  }
}
```

The `instructions` object fields:

| Field | Description |
| --- | --- |
| `system` | Injected as the system prompt. Controls the agent’s persona and behavioral guidelines. |
| `response` | Appended as a response instruction. Controls how the agent formats and styles its answers. |
| `orchestration` | Sets the orchestration instruction. Guides tool selection preferences (for example, “prefer bash”). |

Expand

Show lessSee more

The `models` object fields:

| Field | Description |
| --- | --- |
| `orchestration` | Model name for the orchestration LLM call (for example, `claude-sonnet-4-5`). |

Expand

Show lessSee more

Important

The `instructions` and `models` fields cannot be combined with the `model` or `response_instruction` fields. These are two mutually exclusive field groups:

- **Workflow fields** (legacy): `model`, `response_instruction`
- **LLM orchestration fields**: `models`, `instructions`, `orchestration`

Mixing them returns an error.

## When to use each tool type

Use `code_toolset_all` when:

- You want an autonomous coding agent with file system access
- Your workflow requires reading, writing, and editing files
- You need shell command execution alongside SQL and web search

Use `code_execution` when:

- You need basic Python code execution alongside other tools (Cortex Analyst, Cortex Search)
- Your agent’s primary function is not code generation
- You want a lightweight sandbox for data processing and visualization

For the `code_execution` tool, default libraries, adding libraries through the Artifact Repository, and external network access, see [Cortex Agent code execution tool](/user-guide/snowflake-cortex/cortex-agents-code-execution-tool).
