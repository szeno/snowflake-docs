# MCP servers

This topic describes how to extend the Cortex Code Agent SDK with external MCP (Model Context Protocol) servers.
MCP servers let your agent call external tools alongside built-in tools like `Read`, `Edit`, and `Bash`.

## Overview

The current Cortex runtime supports external MCP servers over these transports:

- `stdio`
- `http`
- `sse`

## Connecting external MCP servers

### Stdio servers

Stdio servers are external processes that communicate over standard input and output.

TypeScriptPython

Copy code

```
import { query } from "cortex-code-agent-sdk";

for await (const message of query({
  prompt: "Search our docs for authentication best practices",
  options: {
    cwd: process.cwd(),
    permissionMode: "bypassPermissions",
    allowDangerouslySkipPermissions: true,
    mcpServers: {
      "my-tools": {
        command: "node",
        args: ["my-mcp-server.js"],
      },
    },
  },
})) {
  // Handle messages...
}
```

Copy code

```
from cortex_code_agent_sdk import query, CortexCodeAgentOptions

async for message in query(
    prompt="Search our docs for authentication best practices",
    options=CortexCodeAgentOptions(
        permission_mode="bypassPermissions",
        allow_dangerously_skip_permissions=True,
        mcp_servers={
            "my-tools": {
                "command": "node",
                "args": ["my-mcp-server.js"],
            },
        },
    ),
):
    # Handle messages...
    pass
```

### HTTP and SSE servers

For remote MCP servers that communicate over HTTP or Server-Sent Events (SSE):

TypeScriptPython

Copy code

```
import { query } from "cortex-code-agent-sdk";

for await (const message of query({
  prompt: "Look up customer data",
  options: {
    cwd: process.cwd(),
    permissionMode: "bypassPermissions",
    allowDangerouslySkipPermissions: true,
    mcpServers: {
      "remote-api": {
        type: "http",
        url: "https://my-mcp-server.example.com/mcp",
        headers: { "Authorization": "Bearer ${MCP_TOKEN}" },
      },
    },
  },
})) {
  // Handle messages...
}
```

Copy code

```
from cortex_code_agent_sdk import query, CortexCodeAgentOptions

async for message in query(
    prompt="Look up customer data",
    options=CortexCodeAgentOptions(
        permission_mode="bypassPermissions",
        allow_dangerously_skip_permissions=True,
        mcp_servers={
            "remote-api": {
                "type": "http",
                "url": "https://my-mcp-server.example.com/mcp",
                "headers": {"Authorization": "Bearer ${MCP_TOKEN}"},
            },
        },
    ),
):
    # Handle messages...
    pass
```

You can also use `"type": "sse"` for servers that use SSE transport.

## Controlling which MCP tools are allowed

MCP tools are namespaced with the `mcp__` prefix in the format `mcp__<server-name>__<tool-name>`. Use the
`allowedTools` (TypeScript) or `allowed_tools` (Python) option to control which tools the agent can call:

TypeScriptPython

Copy code

```
import { query } from "cortex-code-agent-sdk";

for await (const message of query({
  prompt: "Search our documentation",
  options: {
    cwd: process.cwd(),
    permissionMode: "bypassPermissions",
    allowDangerouslySkipPermissions: true,
    allowedTools: [
      "mcp__my-tools__search_docs",
      "mcp__my-tools__*",
    ],
    mcpServers: {
      "my-tools": { command: "node", args: ["my-mcp-server.js"] },
    },
  },
})) {
  // Handle messages...
}
```

Copy code

```
from cortex_code_agent_sdk import query, CortexCodeAgentOptions

async for message in query(
    prompt="Search our documentation",
    options=CortexCodeAgentOptions(
        permission_mode="bypassPermissions",
        allow_dangerously_skip_permissions=True,
        allowed_tools=[
            "mcp__my-tools__search_docs",
            "mcp__my-tools__*",
        ],
        mcp_servers={
            "my-tools": {"command": "node", "args": ["my-mcp-server.js"]},
        },
    ),
):
    # Handle messages...
    pass
```

You can also use `disallowedTools` / `disallowed_tools` to block specific tools.

## Disabling MCP

To disable all MCP servers for a session, use the `noMcp` (TypeScript) or `no_mcp` (Python) option:

TypeScriptPython

Copy code

```
const session = await createCortexCodeSession({
  cwd: process.cwd(),
  noMcp: true,
});
```

Copy code

```
options = CortexCodeAgentOptions(no_mcp=True)
```

## Feature comparison

| Feature | Python | TypeScript |
| --- | --- | --- |
| External MCP servers (stdio) | Yes (`mcp_servers`) | Yes (`mcpServers`) |
| External MCP servers (HTTP/SSE) | Yes (`mcp_servers`) | Yes (`mcpServers`) |
| `allowedTools` / `allowed_tools` | Yes | Yes |
| `noMcp` / `no_mcp` | Yes | Yes |

Expand

Show lessSee more

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
