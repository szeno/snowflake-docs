# Cortex Code Agent SDK

Feature - Preview

This feature is in preview.

The Cortex Code Agent SDK lets you build agentic AI applications using Python and TypeScript. Your agents can read
files, run commands, search codebases, execute SQL, and edit code, using the same tools and agent loop that power
Cortex Code.

The SDK includes built-in tools for file operations, shell commands, and code editing, so your agent can start working
immediately without you implementing tool execution.

TypeScriptPython

Copy code

```
import { query } from "cortex-code-agent-sdk";

for await (const message of query({
  prompt: "Explore the SALES.PUBLIC schema and give me a one-paragraph summary of the tables it contains.",
  options: { cwd: process.cwd() },
})) {
  if (message.type === "assistant") {
    for (const block of message.content) {
      if (block.type === "text") process.stdout.write(block.text);
    }
  }
}
```

Copy code

```
import asyncio
from cortex_code_agent_sdk import query, AssistantMessage, CortexCodeAgentOptions

async def main():
    async for message in query(
        prompt="Explore the SALES.PUBLIC schema and give me a one-paragraph summary of the tables it contains.",
        options=CortexCodeAgentOptions(cwd="."),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text, end="")

asyncio.run(main())
```

## Get started

### Prerequisites

| Requirement | Details |
| --- | --- |
| Cortex Code CLI | Install with `curl -LsS https://ai.snowflake.com/static/cc-scripts/install.sh | sh` |
| Snowflake connection | Configured through Snowflake CLI connection settings, typically in `~/.snowflake/connections.toml`. Existing setups in `~/.snowflake/config.toml` are also supported. Pass the `connection` option or set `default_connection_name` in the TOML file. See [Configuring connections](/developer-guide/snowflake-cli/connecting/configure-connections). |
| Node.js (TypeScript) | Version 22.0.0 or later |
| Python (Python SDK) | Version 3.10 or later |

Expand

Show lessSee more

### 1. Install the Cortex Code CLI

Install the CLI:

Copy code

```
curl -LsS https://ai.snowflake.com/static/cc-scripts/install.sh | sh
```

### 2. Install the SDK

Install the SDK from npm or PyPI:

TypeScriptPython

Copy code

```
npm install cortex-code-agent-sdk
```

Copy code

```
pip install cortex-code-agent-sdk
```

### 3. Configure your Snowflake connection

The SDK authenticates through your Snowflake CLI connection settings. Add a connection to
`~/.snowflake/connections.toml` or use an existing setup in `~/.snowflake/config.toml`
(see [Configuring connections](/developer-guide/snowflake-cli/connecting/configure-connections)):

Copy code

```
[my-connection]
account = "myorg-myaccount"
user = "myuser"
authenticator = "externalbrowser"
```

The SDK uses the CLI’s default connection unless you specify one explicitly through the `connection` option.

If the Cortex Code CLI is not on your `PATH`, point the SDK at it by setting
`CORTEX_CODE_CLI_PATH=/path/to/cortex` or by passing `cliPath` (TypeScript)
or `cli_path` (Python) in the SDK options.

### 4. Run your first agent

The following example creates an agent that connects to Snowflake, explores a schema, and profiles a table using
the built-in SQL tool and your default connection:

TypeScriptPython

Copy code

```
import { query } from "cortex-code-agent-sdk";

for await (const message of query({
  prompt:
    "Explore the SALES.PUBLIC schema and summarize its tables, then profile the ORDERS table: " +
    "report its row count, its columns and types, and the NULL rate of each column.",
  options: {
    cwd: process.cwd(),
    allowedTools: ["SQL"], // auto-approve the SQL tool so the agent can query without prompting
  },
})) {
  if (message.type === "assistant") {
    for (const block of message.content) {
      if (block.type === "text") process.stdout.write(block.text);
    }
  }
  if (message.type === "result") {
    console.log("\nDone:", message.subtype);
  }
}
```

Copy code

```
import asyncio
from cortex_code_agent_sdk import query, AssistantMessage, ResultMessage, CortexCodeAgentOptions

async def main():
    async for message in query(
        prompt=(
            "Explore the SALES.PUBLIC schema and summarize its tables, then profile the ORDERS table: "
            "report its row count, its columns and types, and the NULL rate of each column."
        ),
        options=CortexCodeAgentOptions(
            cwd=".",
            allowed_tools=["SQL"],  # auto-approve the SQL tool so the agent can query without prompting
        ),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text, end="")
        elif isinstance(message, ResultMessage):
            print(f"\nDone: {message.subtype}")

asyncio.run(main())
```

For a more complete tutorial, see [Quickstart](/user-guide/cortex-code-agent-sdk/quickstart).

## Capabilities

### Built-in tools

Your agent can read files, run commands, execute SQL, and search codebases without additional configuration.
Available tools can vary by environment and runtime capabilities:

| Tool | Description |
| --- | --- |
| **Read** | Read any file in the working directory |
| **Write** | Create new files |
| **Edit** | Make precise edits to existing files |
| **Bash** | Run terminal commands, scripts, and git operations |
| **Glob** | Find files by pattern (`**/*.ts`, `src/**/*.py`) |
| **Grep** | Search file contents with regex |
| **SQL** | Execute SQL queries against Snowflake |

Expand

Show lessSee more

### Multi-turn sessions

You can maintain context across multiple exchanges. The agent retains knowledge of the tables it queried, analysis
performed, and conversation history:

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  allowedTools: ["SQL"],
});

await session.send("List the tables in the SALES.PUBLIC schema with their row counts.");
for await (const event of session.stream()) {
  if (event.type === "result") break;
}

// Second turn - the agent still has the table list and row counts from context
await session.send("Now write a query that joins the two largest tables.");
for await (const event of session.stream()) {
  if (event.type === "result") break;
}

await session.close();
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions

async with CortexCodeSDKClient(CortexCodeAgentOptions(allowed_tools=["SQL"])) as client:
    await client.query("List the tables in the SALES.PUBLIC schema with their row counts.")
    async for msg in client.receive_response():
        pass  # process messages

    # Second turn - the agent still has the table list and row counts from context
    await client.query("Now write a query that joins the two largest tables.")
    async for msg in client.receive_response():
        pass  # process messages
```

You can also continue a previous session or fork it into a new one:

TypeScriptPython

Copy code

```
// Continue the most recent conversation
const session = await createCortexCodeSession({
  cwd: process.cwd(),
  continue: true,
});

// Or fork a resumed session into a new session ID
const forked = await createCortexCodeSession({
  cwd: process.cwd(),
  resume: "previous-session-id",
  forkSession: true,
});
```

Copy code

```
# Continue the most recent conversation
async with CortexCodeSDKClient(
    CortexCodeAgentOptions(continue_conversation=True)
) as client:
    await client.query("What were we working on?")

# Or fork a resumed session into a new session ID
async with CortexCodeSDKClient(
    CortexCodeAgentOptions(resume="previous-session-id", fork_session=True)
) as client:
    await client.query("Let's try a different approach")
```

### MCP servers

You can connect to external systems through the Model Context Protocol:

Copy code

```
from cortex_code_agent_sdk import CortexCodeAgentOptions

options = CortexCodeAgentOptions(
    mcp_servers={
        "my-tools": {
            "command": "node",
            "args": ["my-mcp-server.js"],
        },
    },
)
```

### Hooks

You can run custom code at key points in the agent lifecycle. Available hook events include `PreToolUse`,
`PostToolUse`, `Stop`, `UserPromptSubmit`, and more. Hooks are supported in both the Python and TypeScript SDKs.
See the [Python SDK reference](/user-guide/cortex-code-agent-sdk/python-reference) or the
[TypeScript SDK reference](/user-guide/cortex-code-agent-sdk/typescript-reference) for details.

### Structured output

You can force the agent to return a response matching a JSON Schema:

Copy code

```
const result = query({
  prompt: "Profile the ORDERS table in the SALES.PUBLIC schema",
  options: {
    cwd: ".",
    allowedTools: ["SQL"],
    outputFormat: {
      type: "json_schema",
      schema: {
        type: "object",
        properties: {
          table: { type: "string" },
          row_count: { type: "number" },
          columns: {
            type: "array",
            items: {
              type: "object",
              properties: {
                name: { type: "string" },
                type: { type: "string" },
                null_rate: { type: "number" },
              },
              required: ["name", "type", "null_rate"],
            },
          },
        },
        required: ["table", "row_count", "columns"],
      },
    },
  },
});
```

For more information, see [Structured output](/user-guide/cortex-code-agent-sdk/structured-output).

### Session control

You can control agent behavior through session options:

| Option | Description |
| --- | --- |
| `maxTurns` / `max_turns` | Limit the number of agentic turns before the agent stops |
| `effort` | Set model thinking effort (`"minimal"`, `"low"`, `"medium"`, `"high"`, `"max"`) |
| `abortController` / `abort_event` | Interrupt the running agent mid-turn. The session stays alive for further prompts. |
| `env` | Pass environment variables to the agent process |
| `additionalDirectories` / `add_dirs` | Add extra directories the agent can access beyond `cwd` |
| `plugins` | Load plugin directories for custom extensions |
| `systemPrompt` / `system_prompt` | Replace or append to the default system prompt |
| `settingSources` / `setting_sources` | Control which setting files are loaded (`"user"`, `"project"`, `"local"`) |

Expand

Show lessSee more

## Supported models

Set the model using the `model` option. Snowflake recommends `"auto"` for automatic selection of the highest quality
available model.

| Model | Identifier |
| --- | --- |
| Auto (recommended) | `auto` |
| Claude Opus 5 | `claude-opus-5` |
| Claude Opus 4.8 | `claude-opus-4-8` |
| Claude Opus 4.7 | `claude-opus-4-7` |
| Claude Opus 4.6 | `claude-opus-4-6` |
| Claude Opus 4.5 | `claude-opus-4-5` |
| Claude Sonnet 5 | `claude-sonnet-5` |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` |
| Claude Sonnet 4.5 | `claude-sonnet-4-5` |
| Claude Sonnet 4.0 | `claude-4-sonnet` |
| OpenAI GPT 5.5 (Preview) | `openai-gpt-5.5` |
| OpenAI GPT 5.4 | `openai-gpt-5.4` |
| OpenAI GPT 5.2 | `openai-gpt-5.2` |

Expand

Show lessSee more

### Cross-region inference

Model availability varies by region. An account administrator can enable cross-region inference to access models not
available locally:

Copy code

```
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'AWS_US';
```

For more information, see [Cross-region inference](/user-guide/snowflake-cortex/cross-region-inference).

## Next steps

- [Quickstart](/user-guide/cortex-code-agent-sdk/quickstart): Build an agent that finds and fixes bugs
- [Build a data copilot](/user-guide/cortex-code-agent-sdk/build-a-data-copilot): Build a data engineering copilot app that uses the SDK’s SQL tool against Snowflake
- [TypeScript SDK reference](/user-guide/cortex-code-agent-sdk/typescript-reference): Full TypeScript API reference and examples
- [Python SDK reference](/user-guide/cortex-code-agent-sdk/python-reference): Full Python API reference and examples
- [Multi-turn sessions and streaming input](/user-guide/cortex-code-agent-sdk/streaming-input): Maintain context across multiple exchanges
- [MCP servers](/user-guide/cortex-code-agent-sdk/mcp-custom-tools): Connect external MCP servers
- [System prompts](/user-guide/cortex-code-agent-sdk/system-prompts): Customize agent behavior with system prompts
- [Handle approvals and user input](/user-guide/cortex-code-agent-sdk/user-input): Control which tools the agent can use
- [Structured output](/user-guide/cortex-code-agent-sdk/structured-output): Return validated JSON from agent workflows
- [Streaming output](/user-guide/cortex-code-agent-sdk/streaming-output): Stream responses in real-time
- [Hooks](/user-guide/cortex-code-agent-sdk/hooks): Run custom code at key points in the agent lifecycle

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
