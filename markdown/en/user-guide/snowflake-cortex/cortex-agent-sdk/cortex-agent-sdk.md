# Cortex Agent SDK

— Open

Available to all accounts.

The Cortex Agent SDK helps you build applications that reason over your governed Snowflake data and take action with
tools. Use it from Python or TypeScript to stream responses, preserve multi-turn conversations, run long tasks in the
background, and manage reusable agent objects.

You can also embed Cortex Code when your application needs an agentic coding loop that can inspect files, run
commands, use tools, and make changes in a workspace.

## What you can build

| Goal | SDK capability |
| --- | --- |
| Answer questions with governed data | Run inline agents or saved agent objects that use Cortex Analyst, Cortex Search, and custom tools. |
| Show progress as it happens | Stream text, tool calls, tool results, citations, and status events to your application. |
| Build a conversational experience | Use conversation helpers and persistent threads to maintain context across turns and application sessions. |
| Run longer tasks reliably | Start a background run, disconnect safely, and reconnect later by run ID. |
| Embed an agentic coding workflow | Use the Cortex Code CLI on your application host, or run the managed coding agent through a conversation. |

Expand

Show lessSee more

## Get started

You need a Snowflake account with Cortex Agents available and a supported credential. The SDK derives the API URL from
the `account` value and uses Snowflake’s canonical hyphenated host form when the account identifier contains an
underscore (`_`). Pass a full base URL only when you need a regional, PrivateLink, pre-production, or proxy endpoint.
The Python SDK requires Python 3.10 or later. The TypeScript SDK requires Node.js 22.22 or later.

Choose your language to install the SDK and send an agent turn.

TypeScriptPython

Install the SDK:

Copy code

```
npm install "@snowflake/cortex-agent-sdk@>=0.0.2"
```

Set `SNOWFLAKE_ACCOUNT` and `SNOWFLAKE_PAT` in your environment, and then start a conversation:

Copy code

```
import {
  CortexAgentClient,
  type AgentResponse,
  type Conversation,
  type Turn,
} from "@snowflake/cortex-agent-sdk";

const client: CortexAgentClient = new CortexAgentClient({
  account: process.env.SNOWFLAKE_ACCOUNT!,
  auth: process.env.SNOWFLAKE_PAT!,
});

const conversation: Conversation = await client.conversations.create({
  thread: { origin_application: "my-app" },
  agent: {
    type: "inline",
    spec: { models: { orchestration: "claude-sonnet-4-5" } },
  },
});

const turn: Turn = await conversation.send("Explain Snowflake micro-partitions in three sentences.");
console.log(`Conversation ID: ${conversation.id}`);

const answer: AgentResponse = await turn.result();
console.log(answer.text);
```

Install the package and use the conversation-first client:

Copy code

```
pip install "snowflake-cortex-agent-sdk>=0.0.2"
```

Copy code

```
from cortex_agent_sdk import AgentResponse, Conversation, CortexAgentClient, Turn

client: CortexAgentClient = CortexAgentClient(account="my_account", auth="<token>")
conversation: Conversation = client.conversations.create(
    origin_application="cortex_agent_sdk",
    agent={"type": "inline", "spec": {}},
)
turn: Turn = conversation.send("What can Cortex Agent do?")
answer: AgentResponse = turn.result()
print(answer.text)
```

The root client exposes `client.conversations` and `client.feedback`. Saved agent objects, streaming, and explicit
run or thread management are on `cortex_agent_sdk.api`.

For a complete setup and multi-turn example, see the [quickstart](/user-guide/snowflake-cortex/cortex-agent-sdk/quickstart).

## Authenticate

The SDK supports programmatic access tokens, OAuth access tokens, key pair JSON Web Tokens (JWTs), Snowflake session
tokens, and custom authenticators. Keep credentials outside your source code. The SDK asks the authenticator for
headers before every request attempt, and can run a refresh callback once by default when Snowflake returns a
recognized expired-token or expired-session response.

For authentication examples, header formats, session-token guidance, and refresh behavior, see
[Authenticate Cortex Agent SDK requests](/user-guide/snowflake-cortex/cortex-agent-sdk/authentication).

## Choose a coding interface

Choose the interface based on where you want the agent loop and tools to run.

| Interface | Use it when | How it runs |
| --- | --- | --- |
| Cortex Code CLI | Your application host can install Cortex Code and needs access to local files, commands, hooks, or MCP servers. | The SDK launches the local `cortex` executable. |
| Managed coding agent | You want durable, Snowflake-managed coding-agent turns without running a local CLI. | Create a conversation with `agent: { type: "coding", spec: { ... } }`, or provide that object as a per-turn `send()` override. |

Expand

Show lessSee more

For examples and supported options, see [Cortex Code](/user-guide/snowflake-cortex/cortex-agent-sdk/cortex-code) and
[Conversations](/user-guide/snowflake-cortex/cortex-agent-sdk/conversations).

## Next steps

- [Quickstart](/user-guide/snowflake-cortex/cortex-agent-sdk/quickstart): Build a durable, multi-turn agent application.
- [Authenticate Cortex Agent SDK requests](/user-guide/snowflake-cortex/cortex-agent-sdk/authentication): Configure PAT, OAuth, key-pair JWT, Snowflake session token, and custom authentication.
- [Conversations](/user-guide/snowflake-cortex/cortex-agent-sdk/conversations): Maintain conversation state across turns.
- [Direct Agent API](/user-guide/snowflake-cortex/cortex-agent-sdk/running-agents): Use low-level run, thread, and agent-object resources.
- [Use the asynchronous Python client](/user-guide/snowflake-cortex/cortex-agent-sdk/async-python): Run concurrent agent operations from Python.
- [SDK reference](/user-guide/snowflake-cortex/cortex-agent-sdk/sdk-reference): Configure responses, errors, retries, and request options.

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
