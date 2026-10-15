# Cortex Agent SDK features

— Open

Available to all accounts.

This topic covers feature-specific SDK patterns that build on the quickstart, conversations, and direct API topics.
Use these patterns when your application needs MCP tools, managed coding-agent controls, or detailed streaming-event
handling.

## Use MCP servers with direct agent runs

The direct Agent API client can attach Snowflake `MCP SERVER` objects to inline agent runs and saved agent object
specifications. Create and grant access to the MCP server first. For SQL examples and privileges, see
[Snowflake-managed MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp) and
[Connectors for Cortex Agents](/user-guide/snowflake-cortex/cortex-agents-mcp-connectors).

Pass MCP server references in the `mcp_servers` field of the agent request or saved agent specification. Use this
field with `api.agent.*` methods. Cortex Code uses a different `mcpServers` option, described in
[Use in-process MCP tools with Cortex Code](#label-cortex-agent-sdk-in-process-mcp).

TypeScriptPython

Attach an MCP server to an inline run:

Copy code

```
import {
  CortexAgentClient,
  type AgentRunStream,
} from "@snowflake/cortex-agent-sdk/api";

const api = new CortexAgentClient({
  account: process.env.SNOWFLAKE_ACCOUNT!,
  auth: process.env.SNOWFLAKE_PAT!,
});

const mcpServerName = "MY_DB.MY_SCHEMA.SQL_EXEC_MCP";

const stream: AgentRunStream = api.agent.stream({
  models: { orchestration: "claude-sonnet-4-5" },
  instructions: {
    orchestration: "Use the attached MCP SQL tool when the user asks for account context.",
    response: "Be concise.",
  },
  messages: [
    {
      role: "user",
      content: [{ type: "text", text: "Run SELECT CURRENT_ROLE() and report the result." }],
    },
  ],
  mcp_servers: [{ server_spec: { name: mcpServerName } }],
});

await stream.done();
```

Add the same MCP server to a saved agent object:

Copy code

```
await api.agent.create(
  { database: "MY_DB", schema: "MY_SCHEMA" },
  {
    name: "MY_AGENT",
    models: { orchestration: "claude-sonnet-4-5" },
    instructions: {
      orchestration: "Use the attached MCP SQL tool for current user and role questions.",
      response: "Be concise.",
    },
    mcp_servers: [{ server_spec: { name: mcpServerName } }],
  },
  { createMode: "orReplace" },
);
```

Attach an MCP server to an inline run:

Copy code

```
import os

from cortex_agent_sdk.api import CortexAgentClient

api = CortexAgentClient(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    auth=os.environ["SNOWFLAKE_PAT"],
)

mcp_server_name = "MY_DB.MY_SCHEMA.SQL_EXEC_MCP"

stream = api.agent.stream(
    {
        "models": {"orchestration": "claude-sonnet-4-5"},
        "instructions": {
            "orchestration": "Use the attached MCP SQL tool when the user asks for account context.",
            "response": "Be concise.",
        },
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": "Run SELECT CURRENT_ROLE() and report the result."}],
            }
        ],
        "mcp_servers": [{"server_spec": {"name": mcp_server_name}}],
    }
)

stream.until_done()
```

Add the same MCP server to a saved agent object:

Copy code

```
api.agent.create(
    {
        "name": "MY_AGENT",
        "models": {"orchestration": "claude-sonnet-4-5"},
        "instructions": {
            "orchestration": "Use the attached MCP SQL tool for current user and role questions.",
            "response": "Be concise.",
        },
        "mcp_servers": [{"server_spec": {"name": mcp_server_name}}],
    },
    target={"database": "MY_DB", "schema": "MY_SCHEMA"},
    create_mode="orReplace",
)
```

## Use in-process MCP tools with Cortex Code

Use an in-process SDK MCP server when a Cortex Code session needs access to state or functions inside your
application process. The SDK registers the server with the local Cortex Code CLI and dispatches tool calls back to your
handlers. This pattern doesn’t create a Snowflake `MCP SERVER` object.

In-process MCP tools are available only through the Cortex Code interface. For direct Agent API runs, use Snowflake
`MCP SERVER` objects with the `mcp_servers` field instead.

TypeScriptPython

Copy code

```
import {
  createCortexCodeSession,
  createSdkMcpServer,
  tool,
  type CortexCodeSession,
  type McpServerStatus,
} from "@snowflake/cortex-agent-sdk/code";

const inventory = { widget: 41 };

const server = createSdkMcpServer({
  name: "example-inventory",
  version: "1.0.0",
  tools: [
    tool(
      "widget_inventory_count",
      "Return the number of widgets currently in stock. Takes no arguments.",
      {},
      async () => ({
        content: [{ type: "text", text: `widget: ${inventory.widget} units` }],
      }),
    ),
  ],
});

await using session: CortexCodeSession = await createCortexCodeSession({
  onlyExplicitMcpServers: true,
  mcpServers: { "example-inventory": server },
  allowedTools: ["mcp__example-inventory__widget_inventory_count"],
});

const statuses: McpServerStatus[] = await session.mcpServerStatus();
console.log(statuses.find((status) => status.name === "example-inventory")?.tools);

await session.send("Use the widget_inventory_count tool and reply with just the number.");
for await (const event of session.stream()) {
  if (event.type === "result") break;
}

await session.setMcpServers({});
```

For SDK-managed in-process servers, use `setMcpServers()` to replace the server map. `toggleMcpServer()` applies to
transport-backed servers that the CLI owns.

Copy code

```
import asyncio

from cortex_agent_sdk.cortexcode import (
    CortexCodeAgentOptions,
    CortexCodeSDKClient,
    ResultMessage,
    create_sdk_mcp_server,
    tool,
)

@tool("widget_inventory_count", "Return the number of widgets currently in stock.", {})
async def widget_inventory_count(_arguments: dict[str, object]) -> dict[str, object]:
    return {"content": [{"type": "text", "text": "widget: 41 units"}]}

async def main() -> None:
    server = create_sdk_mcp_server(
        "example-inventory",
        tools=[widget_inventory_count],
    )

    options = CortexCodeAgentOptions(
        mcp_servers={"example-inventory": server},
        allowed_tools=["mcp__example-inventory__widget_inventory_count"],
    )

    async with CortexCodeSDKClient(options) as client:
        status = await client.get_mcp_status()
        print(status["mcpServers"])

        await client.query("Use the widget_inventory_count tool and reply with just the number.")
        async for message in client.receive_response():
            if isinstance(message, ResultMessage):
                break

asyncio.run(main())
```

When you define tool input schemas, validate arguments inside the handler. Schema metadata helps describe the tool to
the model, but your application remains responsible for rejecting invalid input.

## Configure managed coding-agent features

The direct API exposes `api.codingAgent` in TypeScript and `api.coding_agent` in Python for Snowflake-managed coding
agent runs. This resource expands coding-agent options into the standard Agent API request shape and sends the request
through `api.agent`.

Use these options when you need to configure the coding-agent toolset directly:

- `permissionPolicy` or `permission_policy`: choose whether tool operations are always allowed or ask for approval.
- `workspaceMounts` or `workspace_mounts`: mount a workspace that the coding agent can read and write.
- `disabledSkills` or `disabled_skills`: disable built-in skills for a run.
- `stageSkills` or `stage_skills`: load skills from a Snowflake stage.
- `stream` and `background`: choose the same response modes as other direct Agent API calls.

TypeScriptPython

Copy code

```
import {
  CortexAgentClient,
  expandCodingAgentRequest,
  type AgentResponseView,
} from "@snowflake/cortex-agent-sdk/api";

const api = new CortexAgentClient({
  account: process.env.SNOWFLAKE_ACCOUNT!,
  auth: process.env.SNOWFLAKE_PAT!,
});

const workspace = "USER$MY_USER.PUBLIC.DEFAULT$";

const wireShape = expandCodingAgentRequest({
  messages: [{ role: "user", content: [{ type: "text", text: "Inspect this workspace." }] }],
  permissionPolicy: "always_allow",
  disabledSkills: ["dashboard"],
  workspaceMounts: [{ name: workspace, mountPath: "/workspace" }],
  stageSkills: [{ name: "project_rules", path: "@MY_DB.MY_SCHEMA.MY_STAGE/skills/project_rules" }],
  models: { orchestration: "claude-sonnet-4-5" },
});

console.log(wireShape.tool_resources);

const view: AgentResponseView = await api.codingAgent.run({
  messages: [
    {
      role: "user",
      content: [{ type: "text", text: "Create /workspace/summary.txt with a one-line summary." }],
    },
  ],
  permissionPolicy: "always_allow",
  workspaceMounts: [{ name: workspace, mountPath: "/workspace" }],
  stream: false,
});

console.log(view.text);
```

Copy code

```
import os

from cortex_agent_sdk.api import CortexAgentClient, expand_coding_agent_request

api = CortexAgentClient(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    auth=os.environ["SNOWFLAKE_PAT"],
)

workspace = "USER$MY_USER.PUBLIC.DEFAULT$"

wire_shape = expand_coding_agent_request(
    {
        "messages": [{"role": "user", "content": [{"type": "text", "text": "Inspect this workspace."}]}],
        "permission_policy": "always_allow",
        "disabled_skills": ["dashboard"],
        "workspace_mounts": [{"name": workspace, "mount_path": "/workspace"}],
        "stage_skills": [{"name": "project_rules", "path": "@MY_DB.MY_SCHEMA.MY_STAGE/skills/project_rules"}],
        "models": {"orchestration": "claude-sonnet-4-5"},
    }
)

print(wire_shape["tool_resources"])

view = api.coding_agent.run(
    {
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": "Create /workspace/summary.txt with a one-line summary."}],
            }
        ],
        "permission_policy": "always_allow",
        "workspace_mounts": [{"name": workspace, "mount_path": "/workspace"}],
        "stream": False,
    }
)

print(view.text)
```

The SDK validates some coding-agent options before sending the request. For example, invalid workspace mount
configuration can raise a client-side `CortexAgentError`.

## Handle detailed streaming events

Use `AgentRunStream` callbacks when your application wants to update different UI regions for text, thinking,
tool-use status, tables, charts, warnings, and final metadata. Use the raw async iterator when you want to handle
server-sent event payloads yourself or tally event types emitted by a run.

TypeScriptPython

Copy code

```
import {
  CortexAgentClient,
  StreamEvent,
  type AgentRunStream,
  type ServerSentEvent,
} from "@snowflake/cortex-agent-sdk/api";

const api = new CortexAgentClient({
  account: process.env.SNOWFLAKE_ACCOUNT!,
  auth: process.env.SNOWFLAKE_PAT!,
});

const stream: AgentRunStream = api.agent.stream({
  models: { orchestration: "auto" },
  messages: [{ role: "user", content: [{ type: "text", text: "Analyze this data." }] }],
});

stream
  .on(StreamEvent.Status, (event) => console.log("status", event.status))
  .on(StreamEvent.Thinking, (delta) => process.stdout.write(delta))
  .on(StreamEvent.ToolUse, (event) => console.log("tool", event.name))
  .on(StreamEvent.ToolResult, (event) => console.log("tool result", event.tool_use_id))
  .on(StreamEvent.Table, (event) => console.log("table", event))
  .on(StreamEvent.Chart, (event) => console.log("chart", event))
  .on(StreamEvent.Warning, (event) => console.warn(event.message))
  .on(StreamEvent.End, (event) => console.log("done", event.metadata));

await stream.done();

for await (const event of api.agent.run({
  models: { orchestration: "auto" },
  messages: [{ role: "user", content: [{ type: "text", text: "Analyze this data." }] }],
})) {
  const item: ServerSentEvent = event;
  console.log(item.event);
}
```

Copy code

```
import os
from collections import Counter

from cortex_agent_sdk.api import CortexAgentClient, StreamEvent

api = CortexAgentClient(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    auth=os.environ["SNOWFLAKE_PAT"],
)

stream = api.agent.stream(
    {
        "models": {"orchestration": "auto"},
        "messages": [{"role": "user", "content": [{"type": "text", "text": "Analyze this data."}]}],
    }
)

stream.on(StreamEvent.STATUS, lambda event: print("status", event.get("status")))
stream.on(StreamEvent.THINKING, lambda delta, _accumulated: print(delta, end=""))
stream.on(StreamEvent.TOOL_USE, lambda event: print("tool", event.get("name")))
stream.on(StreamEvent.TOOL_RESULT, lambda event: print("tool result", event.get("tool_use_id")))
stream.on(StreamEvent.TABLE, lambda event: print("table", event))
stream.on(StreamEvent.CHART, lambda event: print("chart", event))
stream.on(StreamEvent.WARNING, lambda event: print("warning", event.get("message")))
stream.on(StreamEvent.END, lambda event: print("done", event.get("metadata")))
stream.until_done()

counts: Counter[str] = Counter()
for event in api.agent.run(
    {
        "models": {"orchestration": "auto"},
        "messages": [{"role": "user", "content": [{"type": "text", "text": "Analyze this data."}]}],
    }
):
    counts[str(event.get("event", ""))] += 1

print(counts)
```

For a list of common event names, see [Streaming events](/user-guide/snowflake-cortex/cortex-agent-sdk/running-agents#label-streaming-events).
For response view helpers, see [Cortex Agent SDK reference](/user-guide/snowflake-cortex/cortex-agent-sdk/sdk-reference).

## Next steps

- [Use the direct Cortex Agent API](/user-guide/snowflake-cortex/cortex-agent-sdk/running-agents): Run inline agents and saved agent objects.
- [Cortex Code with the Cortex Agent SDK](/user-guide/snowflake-cortex/cortex-agent-sdk/cortex-code): Embed a local Cortex Code session.
- [Cortex Agent SDK reference](/user-guide/snowflake-cortex/cortex-agent-sdk/sdk-reference): Review response objects, errors, retries, and request options.

## Legal notices

Where your configuration of Cortex Code uses a model provided on the
[Model and Service Pass-Through Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/model-pass-through-terms/),
your use of that model is further subject to the terms for that model on that page.

The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Covered AI Features [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
