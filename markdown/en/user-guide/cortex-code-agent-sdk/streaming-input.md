# Multi-turn sessions and streaming input

This topic describes the main ways to send prompts to the Cortex Code Agent SDK: **single-prompt queries**
when you want `query()` to manage the session lifecycle for you, **streamed input** for incremental prompt
delivery, and **multi-turn sessions** for interactive conversations that maintain context across exchanges.

## Input patterns

The SDK provides three input patterns:

| Mode | When to use | API |
| --- | --- | --- |
| **Single prompt input** | Send one prompt with `query()` and let the SDK manage the session lifecycle for you. Output still streams until the agent produces a `ResultMessage`. | `query()` in both TypeScript and Python |
| **Streamed input** | Send user messages incrementally from an async iterable instead of a single prompt string | `query()` in both TypeScript and Python, plus `Query.streamInput()` in TypeScript |
| **Multi-turn session** | Interactive conversations: send multiple prompts, maintain context, control the session lifecycle | `createCortexCodeSession()` (TypeScript) or `CortexCodeSDKClient` (Python) |

Expand

Show lessSee more

## Single-prompt queries

The `query()` function is the simplest way to use the SDK. It can send either a single prompt string or an async
iterable of SDK user messages, and it streams back events until the agent produces a `ResultMessage`. In this mode,
“single prompt” refers to the input pattern: output still streams normally.

TypeScriptPython

Copy code

```
import { query } from "cortex-code-agent-sdk";

for await (const message of query({
  prompt: "Explain how the auth module works",
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
        prompt="Explain how the auth module works",
        options=CortexCodeAgentOptions(cwd="."),
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text, end="")

asyncio.run(main())
```

The `query()` function manages the full session lifecycle for you: it creates a session, sends the prompt,
yields events, and closes the session when the result arrives or the iterator is exhausted.

This is different from `maxTurns` / `max_turns`. A single-prompt query still allows the agent to take as many
internal turns as needed, subject to your configured turn limit. Setting `maxTurns: 1` or `max_turns=1` is a
separate constraint that limits the agent to one internal turn and can produce an `error_max_turns` result.

## Multi-turn sessions

For conversations that require multiple exchanges, use a session. The agent retains context between turns, so
later prompts can reference files read, analysis performed, and topics discussed in earlier turns.

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const session = await createCortexCodeSession({ cwd: process.cwd() });

// First turn
await session.send("Read the database connection module");
for await (const event of session.stream()) {
  if (event.type === "assistant") {
    for (const b of event.content) {
      if (b.type === "text") process.stdout.write(b.text);
    }
  }
  if (event.type === "result") break;
}

// Second turn -- context from the first turn is preserved
await session.send("What error handling patterns does it use?");
for await (const event of session.stream()) {
  if (event.type === "assistant") {
    for (const b of event.content) {
      if (b.type === "text") process.stdout.write(b.text);
    }
  }
  if (event.type === "result") break;
}

await session.close();
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions, AssistantMessage, ResultMessage

async with CortexCodeSDKClient(CortexCodeAgentOptions(cwd=".")) as client:
    # First turn
    await client.query("Read the database connection module")
    async for msg in client.receive_response():
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if hasattr(block, "text"):
                    print(block.text, end="")

    # Second turn -- context from the first turn is preserved
    await client.query("What error handling patterns does it use?")
    async for msg in client.receive_response():
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if hasattr(block, "text"):
                    print(block.text, end="")
```

### Session lifecycle

TypeScriptPython

1. Call `createCortexCodeSession(options)` to start a session. This spawns the CLI process.
2. Call `session.send(prompt)` to send a user message.
3. Iterate `session.stream()` to receive responses. Stop iterating when you see a `result` event.
4. Repeat steps 2–3 for additional turns.
5. Call `session.close()` to end the session and clean up the process.

1. Create a `CortexCodeSDKClient` and call `connect()` (or use `async with`).
2. Call `client.query(prompt)` to send a user message.
3. Iterate `client.receive_response()` to receive messages up to and including a `ResultMessage`.
4. Repeat steps 2–3 for additional turns.
5. Call `client.disconnect()` (or let the `async with` block exit).

## Continue a previous session

You can resume a conversation from a previous session. The agent loads the prior conversation history and continues
where it left off.

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

// Continue the most recent conversation
const session = await createCortexCodeSession({
  cwd: process.cwd(),
  continue: true,
});

await session.send("What were we working on?");
for await (const event of session.stream()) {
  if (event.type === "result") break;
}
await session.close();
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions

# Continue the most recent conversation
async with CortexCodeSDKClient(
    CortexCodeAgentOptions(continue_conversation=True)
) as client:
    await client.query("What were we working on?")
    async for msg in client.receive_response():
        pass  # process messages
```

You can also resume a specific session by ID:

TypeScriptPython

Copy code

```
const session = await createCortexCodeSession({
  cwd: process.cwd(),
  resume: "previous-session-id",
});
```

Copy code

```
async with CortexCodeSDKClient(
    CortexCodeAgentOptions(resume="previous-session-id")
) as client:
    ...
```

## Fork a session

Forking creates a new session that starts with the full conversation history of an existing session. The original
session is not modified. This is useful for exploring alternative approaches without losing the original conversation.

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const forked = await createCortexCodeSession({
  cwd: process.cwd(),
  resume: "previous-session-id",
  forkSession: true,
});

await forked.send("Let's try a different approach");
for await (const event of forked.stream()) {
  if (event.type === "result") break;
}
await forked.close();
```

Copy code

```
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions

async with CortexCodeSDKClient(
    CortexCodeAgentOptions(resume="previous-session-id", fork_session=True)
) as client:
    await client.query("Let's try a different approach")
    async for msg in client.receive_response():
        pass  # process messages
```

## Interrupt a turn

Your application can request an interrupt while the agent is processing a turn. This has the same effect as pressing
`Esc` in the CLI. The session stays alive for further prompts.

### Direct interrupt call

Call the `interrupt()` method to send an interrupt request directly:

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const session = await createCortexCodeSession({ cwd: process.cwd() });

await session.send("Analyze every file in this large codebase");

// Interrupt after 10 seconds
setTimeout(() => session.interrupt(), 10_000);

for await (const event of session.stream()) {
  if (event.type === "result") break;
}

// Session is still alive -- send another prompt
await session.send("Just summarize the top-level structure instead");
for await (const event of session.stream()) {
  if (event.type === "result") break;
}

await session.close();
```

Copy code

```
import asyncio
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions, ResultMessage

async with CortexCodeSDKClient(CortexCodeAgentOptions(cwd=".")) as client:
    await client.query("Analyze every file in this large codebase")

    # Interrupt after 10 seconds
    async def interrupt_later():
        await asyncio.sleep(10)
        await client.interrupt()

    asyncio.create_task(interrupt_later())

    async for msg in client.receive_response():
        pass

    # Session is still alive -- send another prompt
    await client.query("Just summarize the top-level structure instead")
    async for msg in client.receive_response():
        pass
```

### Abort controller / abort event

You can also pass an abort signal at session creation time. When the signal fires, the SDK automatically sends the
same interrupt request.

TypeScriptPython

Copy code

```
import { createCortexCodeSession } from "cortex-code-agent-sdk";

const controller = new AbortController();

const session = await createCortexCodeSession({
  cwd: process.cwd(),
  abortController: controller,
});

await session.send("Analyze every file in this large codebase");

// Trigger interrupt from anywhere
setTimeout(() => controller.abort(), 10_000);

for await (const event of session.stream()) {
  if (event.type === "result") break;
}
await session.close();
```

Copy code

```
import asyncio
from cortex_code_agent_sdk import CortexCodeSDKClient, CortexCodeAgentOptions

abort_event = asyncio.Event()

async with CortexCodeSDKClient(
    CortexCodeAgentOptions(cwd=".", abort_event=abort_event)
) as client:
    await client.query("Analyze every file in this large codebase")

    # Trigger interrupt from anywhere
    async def trigger_abort():
        await asyncio.sleep(10)
        abort_event.set()

    asyncio.create_task(trigger_abort())

    async for msg in client.receive_response():
        pass
```

Note

In TypeScript, pass an `AbortController` whose `abort()` method triggers the interrupt request. In Python, pass
an `asyncio.Event` whose `set()` method triggers the interrupt request. In both cases, the session stays alive
after interruption.

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
