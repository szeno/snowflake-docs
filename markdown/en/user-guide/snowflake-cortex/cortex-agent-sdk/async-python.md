# Use the asynchronous Python client

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Use the asynchronous client to run independent conversations concurrently without blocking an event loop.

## Mapping

| Synchronous | Asynchronous |
| --- | --- |
| `CortexAgentClient` | `AsyncCortexAgentClient` |
| `Conversation` | `AsyncConversation` |
| `Turn` | `AsyncTurn` |
| `conversation.send()` | `await conversation.send()` |
| `turn.result()` | `await turn.result()` |

## Send a turn

Copy code

```
from cortex_agent_sdk import (
    AgentResponse,
    AsyncConversation,
    AsyncCortexAgentClient,
    AsyncTurn,
)

async with AsyncCortexAgentClient(account="my_account", auth="<token>") as client:
    conversation: AsyncConversation = await client.conversations.create(
        origin_application="cortex_agent_sdk",
        agent={"type": "inline", "spec": {"models": {"orchestration": "auto"}}},
    )
    turn: AsyncTurn = await conversation.send("What is Snowflake Arctic?")
    answer: AgentResponse = await turn.result()
    print(answer.text)
```

## Read events

Copy code

```
turn: AsyncTurn = await conversation.send("Prepare an analysis.")

async for event in turn.events():
    print(event)

answer: AgentResponse = await turn.result()
```

## Cancel, history, and attach

Copy code

```
from cortex_agent_sdk import ConversationMessage

await turn.cancel()

history: list[ConversationMessage] = await conversation.history()
await conversation.rename("Arctic Q&A")

resumed: AsyncConversation = await client.conversations.attach(conversation.id)
```

Call `cancel()`, `result()`, and `events()` on the `AsyncTurn` that `send()` returned. `turn.id` is the
server-assigned run ID. The root client does not recover a turn from that ID. `attach()` does not keep the agent
from the conversation that created the thread. Pass `agent` on each later `send()`, or the turn uses an empty inline
agent.

## Concurrency and ordering

Independent conversations can run concurrently with `asyncio.gather()`. Calls to `send()` on the same conversation
are serialized so each request uses the previous successful assistant message as its parent.

## Next steps

- [Cortex Code](/user-guide/snowflake-cortex/cortex-agent-sdk/cortex-code)
- [SDK reference](/user-guide/snowflake-cortex/cortex-agent-sdk/sdk-reference)

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
