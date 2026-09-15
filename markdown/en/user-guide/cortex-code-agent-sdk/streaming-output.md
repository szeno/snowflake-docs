# Streaming output

This topic describes how to stream real-time responses from the Cortex Code Agent SDK.

By default, the SDK yields complete `AssistantMessage` objects after the model finishes generating each response. To
receive incremental updates as text and thinking blocks are generated, enable partial message streaming by setting
`includePartialMessages` (TypeScript) or `include_partial_messages` (Python) to `true`.

When partial messages are enabled, Cortex Code emits `StreamEvent` objects for partial text and thinking content.
Complete tool calls still arrive as `AssistantMessage` objects, and tool results still arrive as `UserMessage`
objects.

## Enable streaming output

When enabled, the SDK yields `StreamEvent` messages containing partial streaming events, in addition to the usual
`AssistantMessage`, `UserMessage`, and `ResultMessage` objects. Your code needs to:

1. Check each message’s type to distinguish `StreamEvent` from other types.
2. For `StreamEvent`, extract the `event` field and check its `type`.
3. Look for `content_block_delta` events where `delta.type` is `text_delta`.

TypeScriptPython

Copy code

```
import { query } from "cortex-code-agent-sdk";

for await (const message of query({
  prompt: "List the files in my project",
  options: {
    cwd: process.cwd(),
    includePartialMessages: true,
    allowedTools: ["Bash", "Read"],
  },
})) {
  if (message.type === "stream_event") {
    const event = message.event;
    if (event.type === "content_block_delta") {
      if (event.delta.type === "text_delta") {
        process.stdout.write(event.delta.text);
      }
    }
  }
}
```

Copy code

```
import asyncio
from cortex_code_agent_sdk import query, CortexCodeAgentOptions
from cortex_code_agent_sdk.types import StreamEvent

async def stream_response():
    async for message in query(
        prompt="List the files in my project",
        options=CortexCodeAgentOptions(
            cwd=".",
            include_partial_messages=True,
            allowed_tools=["Bash", "Read"],
        ),
    ):
        if isinstance(message, StreamEvent):
            event = message.event
            if event.get("type") == "content_block_delta":
                delta = event.get("delta", {})
                if delta.get("type") == "text_delta":
                    print(delta.get("text", ""), end="", flush=True)

asyncio.run(stream_response())
```

## StreamEvent reference

When partial messages are enabled, you receive raw streaming events wrapped in an object:

TypeScriptPython

Copy code

```
interface SDKPartialAssistantMessage {
  type: "stream_event";
  event: Record<string, unknown>;  // Raw streaming event
  parent_tool_use_id: string | null;
  uuid: string;
  session_id: string;
}
```

Copy code

```
@dataclass
class StreamEvent:
    uuid: str               # Unique identifier
    session_id: str          # Session identifier
    event: dict[str, Any]    # Raw streaming event
    parent_tool_use_id: str | None  # Parent tool ID if from a subagent
```

The `event` field contains the raw partial streaming event emitted by Cortex Code. Common event types:

| Event Type | Description |
| --- | --- |
| `content_block_start` | Start of a new text or thinking block |
| `content_block_delta` | Incremental text or thinking update |
| `content_block_stop` | End of the current text or thinking block |

Expand

Show lessSee more

## Message flow

With partial messages enabled, you commonly receive messages in the following order:

```
SystemMessage -- session initialization
StreamEvent (content_block_start) -- text or thinking block
StreamEvent (content_block_delta) -- text_delta or thinking_delta chunks...
StreamEvent (content_block_stop)
AssistantMessage -- complete text/thinking block, or complete tool_use block
UserMessage -- complete tool_result block
... more assistant/user turns ...
ResultMessage -- final result
```

Without partial messages enabled, you still receive the same complete assistant, user, and result messages, but not
`StreamEvent`. Depending on the session, the SDK can also emit `system` events such as initialization, status, and
background-task notifications.

## Stream text responses

To display text as it’s generated, look for `content_block_delta` events where `delta.type` is `text_delta`:

TypeScriptPython

Copy code

```
import { query } from "cortex-code-agent-sdk";

for await (const message of query({
  prompt: "Explain how databases work",
  options: { cwd: process.cwd(), includePartialMessages: true },
})) {
  if (message.type === "stream_event") {
    const event = message.event;
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
  }
}
console.log(); // Final newline
```

Copy code

```
import asyncio
from cortex_code_agent_sdk import query, CortexCodeAgentOptions
from cortex_code_agent_sdk.types import StreamEvent

async def stream_text():
    async for message in query(
        prompt="Explain how databases work",
        options=CortexCodeAgentOptions(cwd=".", include_partial_messages=True),
    ):
        if isinstance(message, StreamEvent):
            event = message.event
            if event.get("type") == "content_block_delta":
                delta = event.get("delta", {})
                if delta.get("type") == "text_delta":
                    print(delta.get("text", ""), end="", flush=True)
    print()  # Final newline

asyncio.run(stream_text())
```

## Build a streaming UI

The following example accumulates streamed text in a local buffer and re-renders the current response each time a new
`text_delta` arrives. In a real application, replace the `render` function with your framework’s state update
logic:

TypeScriptPython

Copy code

```
import { query } from "cortex-code-agent-sdk";

let currentText = "";

function render(text: string) {
  console.clear();
  console.log("Assistant:\n");
  process.stdout.write(text);
}

for await (const message of query({
  prompt: "Explain how databases work",
  options: {
    cwd: process.cwd(),
    includePartialMessages: true,
  },
})) {
  if (message.type === "stream_event") {
    const event = message.event;
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      currentText += event.delta.text;
      render(currentText);
    }
  } else if (message.type === "result") {
    console.log("\n\n--- Complete ---");
  }
}
```

Copy code

```
import asyncio
import sys
from cortex_code_agent_sdk import query, CortexCodeAgentOptions, ResultMessage
from cortex_code_agent_sdk.types import StreamEvent

def render(text: str) -> None:
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.write("Assistant:\n\n")
    sys.stdout.write(text)
    sys.stdout.flush()

async def streaming_ui():
    current_text = ""

    async for message in query(
        prompt="Explain how databases work",
        options=CortexCodeAgentOptions(
            cwd=".",
            include_partial_messages=True,
        ),
    ):
        if isinstance(message, StreamEvent):
            event = message.event
            if event.get("type") == "content_block_delta":
                delta = event.get("delta", {})
                if delta.get("type") == "text_delta":
                    current_text += delta.get("text", "")
                    render(current_text)
        elif isinstance(message, ResultMessage):
            print("\n\n--- Complete ---")

asyncio.run(streaming_ui())
```

## Known limitations

| Feature | Impact on streaming |
| --- | --- |
| **Structured output** | JSON result appears only in `ResultMessage.structured_output`, not as streaming deltas |

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
