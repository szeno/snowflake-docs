# Cortex Code with the Cortex Agent SDK

— Open

Available to all accounts.

Use the Cortex Code interface to add an agentic coding loop to your application. It can stream messages, use tools,
ask for permission, and preserve sessions.

Cortex Code runs a separately installed Cortex Code CLI on the application host.
For Snowflake-managed coding-agent execution, use a [conversation](/user-guide/snowflake-cortex/cortex-agent-sdk/conversations)
with `agent: { type: "coding", spec: { ... } }` instead.

## Install the SDK

TypeScriptPython

Install the package:

Copy code

```
npm install "@snowflake/cortex-agent-sdk@>=0.0.2"
```

Import the Cortex Code interface from `@snowflake/cortex-agent-sdk/code`. Cortex Code requires Node.js 22.22 or
later.

Cortex Code requires a compatible `cortex` executable on `PATH`. Installing the SDK doesn’t install Cortex Code.
Set `cliPath` if the executable is in another location.

Install the package:

Copy code

```
pip install "snowflake-cortex-agent-sdk>=0.0.2"
```

Import the Cortex Code interface from `cortex_agent_sdk.cortexcode`.

Cortex Code requires a compatible `cortex` executable on `PATH`. Installing the SDK doesn’t install Cortex Code.
Set `CortexCodeAgentOptions.cli_path` if the executable is in another location.

## Run a one-shot query

Use the `query` function when you want to send one prompt and consume its events.

TypeScriptPython

`query()` returns an asynchronous iterable:

Copy code

```
import { query } from "@snowflake/cortex-agent-sdk/code";

for await (const event of query({
  prompt: "What does package.json declare as the package name?",
})) {
  if (event.type === "assistant") {
    for (const block of event.content) {
      if (block.type === "text") {
        process.stdout.write(block.text);
      }
    }
  }
  if (event.type === "result") {
    console.log(event.subtype);
  }
}
```

`query()` returns an asynchronous iterator of typed messages:

Copy code

```
import asyncio

from cortex_agent_sdk.cortexcode import (
    AssistantMessage,
    CortexCodeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)

async def main() -> None:
    async for message in query(
        prompt="What does pyproject.toml declare as the package name?",
        options=CortexCodeAgentOptions(connection="my_connection"),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text, end="")
        elif isinstance(message, ResultMessage):
            print(f"\nStatus: {message.subtype}")

asyncio.run(main())
```

## Run an interactive session

Use a session when you need multiple turns that share context or you need to interrupt or reconfigure a running
session.

TypeScriptPython

Create a session, send a prompt, and consume events through the terminal `result` event:

Copy code

```
import {
  createCortexCodeSession,
  type CortexCodeSession,
} from "@snowflake/cortex-agent-sdk/code";

await using session: CortexCodeSession = await createCortexCodeSession({
  model: "claude-sonnet-4-5",
});

await session.send("Read src/index.ts and list its exports.");
for await (const event of session.stream()) {
  if (event.type === "result") break;
}

await session.send("Which of those exports are types only?");
for await (const event of session.stream()) {
  if (event.type === "result") break;
}
```

`await using` closes the session automatically. If you don’t use `await using`, call `session.close()` when you are
finished.

Create a client, send a prompt, and consume messages through the terminal `ResultMessage`:

Copy code

```
import asyncio

from cortex_agent_sdk.cortexcode import CortexCodeAgentOptions, CortexCodeSDKClient

async def main() -> None:
    options = CortexCodeAgentOptions(
        connection="my_connection",
        model="claude-sonnet-4-5",
    )

    async with CortexCodeSDKClient(options) as client:
        await client.query("Read the package entry point and list its exports.")
        async for message in client.receive_response():
            print(message)

        await client.query("Which of those exports are types only?")
        async for message in client.receive_response():
            print(message)

asyncio.run(main())
```

`receive_response()` stops after yielding the turn’s `ResultMessage`. `receive_messages()` continues until the
transport closes.

## Handle events

One-shot queries and interactive sessions use the same event model. The names follow the conventions of each
language:

| Purpose | TypeScript event type | Python message class | Contents |
| --- | --- | --- | --- |
| Session lifecycle | `system` | `SystemMessage` | Initialization and run lifecycle information |
| Assistant response | `assistant` | `AssistantMessage` | Text, thinking, and tool-use blocks |
| User or tool result | `user` | `UserMessage` | User input or tool-result content |
| Partial output | `stream_event` | `StreamEvent` | Text or thinking updates when partial messages are enabled |
| Turn completion | `result` | `ResultMessage` | Result, usage, cost, session ID, and permission denials |

Expand

Show lessSee more

A terminal result with `is_error` set to `true` is an event or message, not a raised exception. Inspect its subtype,
errors, and permission denials. The session remains available for another turn unless you close it.

## Stream partial messages

Assistant messages arrive as complete blocks by default. Enable partial messages when you want text deltas while the
turn is running.

TypeScriptPython

Set `includePartialMessages` and handle `stream_event` events:

Copy code

```
import { query } from "@snowflake/cortex-agent-sdk/code";

for await (const event of query({
  prompt: "Summarize this repository",
  options: { includePartialMessages: true },
})) {
  if (event.type === "stream_event" && event.event.delta?.type === "text_delta") {
    process.stdout.write(event.event.delta.text);
  }
}
```

Set `include_partial_messages` and handle `StreamEvent` messages:

Copy code

```
import asyncio

from cortex_agent_sdk.cortexcode import CortexCodeAgentOptions, StreamEvent, query

async def main() -> None:
    options = CortexCodeAgentOptions(
        connection="my_connection",
        include_partial_messages=True,
    )
    async for message in query(prompt="Summarize this repository", options=options):
        if isinstance(message, StreamEvent):
            delta = message.event.get("delta", {})
            if delta.get("type") == "text_delta":
                print(delta.get("text", ""), end="")

asyncio.run(main())
```

Partial events contain text and thinking updates. Tool calls arrive in assistant messages, not partial events.

## Configure a session

The following commonly used settings are available in both languages:

| Purpose | TypeScript | Python |
| --- | --- | --- |
| Select the model and effort | `model`, `effort` | `model`, `effort` |
| Set the working directory | `cwd` | `cwd` |
| Select Snowflake configuration | `connection`, `profile` | `connection`, `profile` |
| Customize the system prompt | `systemPrompt`, `appendSystemPrompt` | `system_prompt`, `append_system_prompt` |
| Set a static tool policy | `allowedTools`, `disallowedTools` | `allowed_tools`, `disallowed_tools` |
| Make per-tool decisions | `canUseTool` | `can_use_tool` |
| Stream partial messages | `includePartialMessages` | `include_partial_messages` |
| Request structured output | `outputFormat` | `output_format` |

Expand

Show lessSee more

CLI mode also supports hooks, MCP servers, permission modes, custom agents, plugins, setting sources, additional
working directories, and CLI resume and continue controls. Don’t populate executable paths, extra CLI arguments, or
other privileged configuration from untrusted input.

## Control tool permissions

Use a callback to make a decision for each tool call. Use the allowed-tools and disallowed-tools settings when a
static policy is sufficient.

TypeScriptPython

Use `canUseTool` to allow read-only tools and deny other tools:

Copy code

```
import {
  createCortexCodeSession,
  type CortexCodeSession,
} from "@snowflake/cortex-agent-sdk/code";

const session: CortexCodeSession = await createCortexCodeSession({
  canUseTool: async (toolName, input) => {
    if (toolName === "Read" || toolName === "Grep") {
      return { behavior: "allow", updatedInput: input };
    }
    return { behavior: "deny", message: `${toolName} is not permitted here` };
  },
});
```

Use `can_use_tool` to allow read-only tools and deny other tools:

Copy code

```
from cortex_agent_sdk.cortexcode import (
    CortexCodeAgentOptions,
    PermissionResultAllow,
    PermissionResultDeny,
    ToolPermissionContext,
)

async def approve_read_only(
    tool_name: str,
    tool_input: dict,
    context: ToolPermissionContext,
):
    if tool_name in {"Read", "Grep"}:
        return PermissionResultAllow(updated_input=tool_input)
    return PermissionResultDeny(message=f"{tool_name} is not permitted here")

options = CortexCodeAgentOptions(can_use_tool=approve_read_only)
```

## Resume or fork a session

Resume continues the saved local session. Forking creates a new local session with the source history and leaves the
source session unchanged.

TypeScriptPython

To resume a session, pass the session ID in `resume`:

Copy code

```
import {
  forkSession,
  query,
  type ForkSessionResult,
  type SessionOptions,
} from "@snowflake/cortex-agent-sdk/code";

const options: SessionOptions = {
  connection: "my_connection",
  resume: previousSessionId,
};

for await (const event of query({ prompt: "Continue the review", options })) {
  if (event.type === "result") break;
}
```

Use `forkSession()` to branch from a session:

Copy code

```
const forked: ForkSessionResult = await forkSession(previousSessionId, {
  connection: "my_connection",
});

console.log(forked.sessionId);
```

To resume a session, pass the session ID in `resume`:

Copy code

```
options = CortexCodeAgentOptions(
    connection="my_connection",
    resume=previous_session_id,
)
```

Use `fork_session()` to branch from a session:

Copy code

```
from cortex_agent_sdk.cortexcode import CortexCodeAgentOptions, fork_session

new_session_id = await fork_session(
    previous_session_id,
    base_options=CortexCodeAgentOptions(connection="my_connection"),
)
```

You can also fork at a specific message. Use `upToMessageId` in TypeScript or `up_to_message_id` in Python.

## Next steps

- [Cortex Agent SDK features](/user-guide/snowflake-cortex/cortex-agent-sdk/sdk-features): Use MCP servers, coding-agent options, and detailed streaming events
- [SDK reference](/user-guide/snowflake-cortex/cortex-agent-sdk/sdk-reference): Review shared error, retry, and transport behavior

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
