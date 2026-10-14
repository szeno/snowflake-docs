# Cortex Agent SDK quickstart

— Open

Available to all accounts.

In this quickstart, you build a small application that starts an agent turn, reads events and structured results, and continues the conversation on a persistent thread.

## Prerequisites

TypeScriptPython

- **Node.js 22.22 or later**
- A **Snowflake account** with Cortex Agents available
- A **programmatic access token (PAT)**, or another supported credential type described in [Authenticate Cortex Agent SDK requests](/user-guide/snowflake-cortex/cortex-agent-sdk/authentication)

- Python 3.10 or later
- A Snowflake account and authentication token
- The Cortex Agent SDK for Python

## Setup

TypeScriptPython

Copy code

```
mkdir agent-quickstart && cd agent-quickstart
npm init -y
npm install "@snowflake/cortex-agent-sdk@>=0.0.2"
npm install --save-dev typescript tsx @types/node
```

Set `"type": "module"` in `package.json` so you can use `import` syntax:

Copy code

```
{ "type": "module" }
```

Copy code

```
export SNOWFLAKE_ACCOUNT="myaccount"
export SNOWFLAKE_PAT="<your-programmatic-access-token>"
```

The SDK expands `SNOWFLAKE_ACCOUNT` to the Snowflake API host. If the account identifier contains an underscore (`_`),
the SDK uses Snowflake’s canonical hyphenated host form.

Copy code

```
python -m venv .venv
source .venv/bin/activate
pip install "snowflake-cortex-agent-sdk>=0.0.2"
export SNOWFLAKE_ACCOUNT="<account_identifier>"
export SNOWFLAKE_PAT="<programmatic_access_token>"
```

The SDK expands `SNOWFLAKE_ACCOUNT` to the Snowflake API host. If the account identifier contains an underscore (`_`),
the SDK uses Snowflake’s canonical hyphenated host form.

## Step 1: Send your first turn

TypeScriptPython

Create `agent.ts`:

Copy code

```
import { CortexAgentClient, type AgentResponse, type Conversation, type Turn } from "@snowflake/cortex-agent-sdk";

const client: CortexAgentClient = new CortexAgentClient({ account: process.env.SNOWFLAKE_ACCOUNT!, auth: process.env.SNOWFLAKE_PAT! });
const conversation: Conversation = await client.conversations.create({
  thread: { origin_application: "agent-quickstart" },
  agent: { type: "inline", spec: { models: { orchestration: "claude-sonnet-4-5" } } },
});
const turn: Turn = await conversation.send("Explain Snowflake micro-partitions in three sentences.");
console.log(`Conversation ID: ${conversation.id}`);
const answer: AgentResponse = await turn.result();
console.log(answer.text);
```

Run `npx tsx agent.ts`.

Copy code

```
import os
from cortex_agent_sdk import AgentResponse, Conversation, CortexAgentClient, Turn

client: CortexAgentClient = CortexAgentClient(account=os.environ["SNOWFLAKE_ACCOUNT"], auth=os.environ["SNOWFLAKE_PAT"])
conversation: Conversation = client.conversations.create(
    origin_application="cortex_agent_sdk",
    agent={"type": "inline", "spec": {"models": {"orchestration": "auto"}}},
)
turn: Turn = conversation.send("In one sentence, what is Snowflake?")
answer: AgentResponse = turn.result()
print(answer.text)
```

`send()` starts durable asynchronous work and returns after Snowflake accepts the turn. The SDK manages the thread ID, parent message ID, run ID, and `background` and `stream` flags. `turn.id` is the server-assigned run ID; `result()` waits for the final assistant response.

## Step 2: Read events as they arrive

TypeScriptPython

Copy code

```
for await (const event of turn.events()) {
  if (event.event === "response.text.delta") process.stdout.write(event.text ?? "");
}
const answer: AgentResponse = await turn.result();
```

Copy code

```
turn: Turn = conversation.send("Name two Snowflake features.")
for event in turn.events():
    print(event)
answer: AgentResponse = turn.result()
```

Events are replayable, so reading them does not replace `result()`. Call `result()`, `events()`, and `cancel()` on the `Turn` returned by `send()`.

## Step 3: Read structured results

TypeScriptPython

Copy code

```
const view: AgentResponse = await turn.result();
console.log(view.text);
console.log(view.content);
console.log(view.usage);
console.log(view.requestId);
```

`AgentResponse` also exposes `toolUses`, `toolResults`, `tables`, `charts`, and `messageId` when the agent response
contains those values.

Copy code

```
answer: AgentResponse = turn.result()
print(answer.text)
print(answer.content)
print(answer.tables)
print(answer.charts)
print(answer.tool_uses)
print(answer.usage)
```

## Step 4: Send a follow-up

The same conversation retains history across turns. You can attach to `conversation.id` later to continue the same
thread from another process.

TypeScriptPython

Copy code

```
const second: Turn = await conversation.send("Which concept did you mention first, and why?");
const secondAnswer: AgentResponse = await second.result();
const history = await conversation.history();
const resumed: Conversation = await client.conversations.attach(conversation.id);
```

`conversation.id` is the thread ID. `history()` returns `Promise<ConversationMessage[]>`, newest first.

Copy code

```
second: Turn = conversation.send("Which concept did you mention first, and why?")
second_answer: AgentResponse = second.result()
history = conversation.history()
resumed: Conversation = client.conversations.attach(conversation.id)
```

## Step 5: Handle failures

TypeScriptPython

Copy code

```
import { AuthenticationError, CortexAgentAPIError, RateLimitError } from "@snowflake/cortex-agent-sdk";

try {
  const turn: Turn = await conversation.send("Analyze Q1 revenue.", { agent: { type: "inline", spec: {} } });
  console.log((await turn.result({ streamReadTimeoutMs: 180_000 })).text);
} catch (error) {
  if (error instanceof AuthenticationError) console.error("Token expired or invalid.");
  else if (error instanceof RateLimitError) console.error("Rate limited. Back off and retry.");
  else if (error instanceof CortexAgentAPIError) console.error(`API error ${error.status} (request ${error.requestId}):`, error.body);
  else throw error;
}
```

Copy code

```
from cortex_agent_sdk import AuthenticationError, CortexAgentAPIError, RateLimitError

try:
    turn: Turn = conversation.send(
        "Analyze Q1 revenue.",
        agent={"type": "inline", "spec": {}},
    )
    print(turn.result().text)
except AuthenticationError:
    print("Token expired or invalid.")
except RateLimitError:
    print("Rate limited. Back off and retry.")
except CortexAgentAPIError as error:
    print(f"API error {error.status} (request {error.request_id}): {error.body}")
```

## Next steps

- [Authenticate Cortex Agent SDK requests](authentication): Configure PAT, OAuth, key-pair JWT, Snowflake session token, and custom authentication.
- [Conversations](conversations): Branch, search, and manage multi-turn state.
- [Direct Agent API](running-agents): Use low-level run, thread, and agent-object resources.
- [SDK reference](sdk-reference): Configure retries, errors, and request options.

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
