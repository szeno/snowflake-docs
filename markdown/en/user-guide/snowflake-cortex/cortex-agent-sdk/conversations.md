# Conversations with the Cortex Agent SDK

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Use conversations to maintain context across turns, processes, and application sessions. Start here for most
applications. Use the lower-level thread, run, and agent-object APIs only when you need direct control over stored
messages, thread metadata, run IDs, or wire-level Agent API requests.

## Use `Conversation`

`Conversation` is the recommended interface for most applications. A conversation represents a persistent thread and
its history. Set a default agent when you create it, and override that agent on individual turns when needed.

TypeScriptPython

Copy code

```
import type { AgentResponse, ClientToolUse, Conversation, PermissionRequest, Turn } from "@snowflake/cortex-agent-sdk";

const convo: Conversation = await client.conversations.create({
  thread: { origin_application: "my-app" },
  agent: {
    type: "inline",
    spec: { models: { orchestration: "claude-sonnet-4-5" } },
  },
});

const first: Turn = await convo.send("What is Snowflake?");
console.log(first.id);

const answer: AgentResponse = await first.result();
console.log(answer.text);

const second: Turn = await convo.send("How does it compare to a data lake?", {
  agent: {
    type: "data",
    spec: { database: "MY_DB", schema: "PUBLIC", name: "MY_AGENT" },
  },
});
const secondAnswer: AgentResponse = await second.result();
console.log(secondAnswer.text);
```

`client.conversations.create()` resolves to `Promise<Conversation>` because it creates the thread before returning.
Each `send()` uses the default agent unless its options specify an inline, data, or coding `agent` override.

Copy code

```
from cortex_agent_sdk import AgentResponse, Conversation, CortexAgentClient, Turn

client: CortexAgentClient = CortexAgentClient(account="my_account", auth="<token>")
conversation: Conversation = client.conversations.create(
    origin_application="my-app",
    agent={"type": "inline", "spec": {"models": {"orchestration": "auto"}}},
)

turn: Turn = conversation.send("What is Snowflake?")
answer: AgentResponse = turn.result()
print(answer.text)
```

`send()` returns a durable `Turn` after Snowflake accepts that turn. If a previous turn on this conversation is still
running, `send()` waits for it to finish first. `result()` waits and returns a memoized `AgentResponse`.

## Work with a turn

Use the `Turn` returned by `send()` to wait for the final response, read replayable events, or cancel the work.
`turn.id` is the server-assigned run ID.

TypeScriptPython

Copy code

```
const turn: Turn = await convo.send("Analyze five years of revenue.", {
  agent: { type: "inline", spec: { models: { orchestration: "claude-sonnet-4-5" } } },
});

for await (const event of turn.events()) {
  if (event.event === "response.text.delta") {
    process.stdout.write(event.text ?? "");
  }
}

const result: AgentResponse = await turn.result();
await turn.cancel();
```

To reconnect to an existing run’s event stream, pass `turn.id` to `client.runs.stream()` on the direct API client.

Copy code

```
for event in turn.events():
    print(event)

answer: AgentResponse = turn.result()
turn.cancel()
```

Call `result()`, `events()`, and `cancel()` on the `Turn` that `send()` returned.

## Select agents and send content

Select the agent and pass its configuration for each turn. You can also pass a typed content-item array instead of a
plain string to return a client-side tool result or send a document already uploaded to a Snowflake stage.

TypeScriptPython

Select an inline agent:

Copy code

```
const inlineTurn: Turn = await convo.send("Summarize Q1 revenue.", {
  agent: {
    type: "inline",
    spec: {
      models: { orchestration: "claude-sonnet-4-5" },
      instructions: { response: "Answer in two sentences." },
    },
  },
});
```

Select a named agent object:

Copy code

```
const dataTurn: Turn = await convo.send("Which product line grew fastest?", {
  agent: {
    type: "data",
    spec: {
      database: "MY_DB",
      schema: "PUBLIC",
      name: "my_agent",
      version: "VERSION$2", // Optional.
    },
  },
});
```

Select the coding agent:

`always_allow` automatically approves coding-agent tool operations that would otherwise require approval, including
destructive-looking shell commands. Use it only when your application intentionally trusts the input source and scopes
workspace mounts, stages, credentials, and network access for that workload. Use an approval-based permission policy
when a person or application approval flow must inspect tool requests before they run.

Copy code

```
const codingTurn: Turn = await convo.send("Write a summary to /workspace/summary.txt", {
  agent: {
    type: "coding",
    spec: {
      permissionPolicy: "always_allow",
      workspaceMounts: [{ name: "USER$MYUSER.PUBLIC.DEFAULT$" }],
      models: { orchestration: "claude-sonnet-4-5" },
    },
  },
});
```

For approval-based flows, create a coding conversation with `permissionPolicy: "always_ask"`. `send()` and
`sendPermissionDecisions()` both use that conversation’s agent. An inline conversation, such as `convo` above, has no
coding tools and does not emit permission requests. Stream events from the returned turn. When a
`response.tool_use` event includes permission options, show those options to the approver. Use
`sendPermissionDecisions()` to continue the conversation after the approver selects options. The helper waits for the
paused turn and uses its assistant message as the parent of the follow-up turn. If a turn requests multiple
permissions, include every selected decision in one `sendPermissionDecisions()` call. Any pending request omitted
from that call is denied. When you pass a `PermissionRequest`, the SDK rejects a decision that is not one of the
request’s `options`. To explain a denial to the model, include an optional `reason` in the decision object.

Copy code

```
const approvalConversation: Conversation = await client.conversations.create({
  thread: { origin_application: "my-app" },
  agent: {
    type: "coding",
    spec: {
      permissionPolicy: "always_ask",
      workspaceMounts: [{ name: "USER$MYUSER.PUBLIC.DEFAULT$" }],
      models: { orchestration: "claude-sonnet-4-5" },
    },
  },
});

const pendingTurn: Turn = await approvalConversation.send("Delete the temporary file.");
const requests = await pendingTurn.permissionRequests();

function selectedDecisionFor(permission: PermissionRequest): string {
  return permission.options.includes("Allow this command") ? "Allow this command" : "Deny";
}

function selectedPermissionDecision(permission: PermissionRequest) {
  const decision = selectedDecisionFor(permission);
  return {
    permission,
    decision,
    // `reason` is optional and is shown to the model when the decision denies the request.
    ...(decision === "Deny" ? { reason: "Deleting files is not allowed in this environment." } : {}),
  };
}

const response: AgentResponse = requests.length
  ? await (
      await approvalConversation.sendPermissionDecisions(
        requests.map(selectedPermissionDecision),
      )
    ).result()
  : await pendingTurn.result();
console.log(response.text);
```

### Execute client-side tools

To configure a generic client-side tool, include it in `tools` and omit a matching entry in `tool_resources`. The
service emits that tool use with `client_side_execute: true`. Call `clientToolUses()` on the pending turn, execute
every returned invocation in your application, then send every result in one `sendToolResults()` call. The helper
constructs the required `tool_result` content and uses the paused assistant message as the follow-up parent.

Copy code

```
const toolConversation: Conversation = await client.conversations.create({
  thread: { origin_application: "my-app" },
  agent: {
    type: "inline",
    spec: {
      models: { orchestration: "claude-sonnet-4-5" },
      tools: [
        {
          tool_spec: {
            type: "generic",
            name: "get_weather",
            description: "Get the current weather for a city.",
            input_schema: {
              type: "object",
              properties: { location: { type: "string" } },
              required: ["location"],
            },
          },
        },
      ],
      // No tool_resources.get_weather entry: the application executes this tool.
    },
  },
});

function executeClientTool(toolUse: ClientToolUse): Record<string, unknown> {
  // Dispatch to the application's weather service.
  return { location: toolUse.input.location, temperature_c: 18, condition: "clear" };
}

const pendingToolTurn: Turn = await toolConversation.send("What is the weather in San Francisco?");
const toolUses = await pendingToolTurn.clientToolUses();
const toolResponse: AgentResponse = toolUses.length
  ? await (
      await toolConversation.sendToolResults(
        toolUses.map((toolUse) => ({ toolUse, result: executeClientTool(toolUse) })),
      )
    ).result()
  : await pendingToolTurn.result();
console.log(toolResponse.text);
```

For other structured client content, pass a `ConversationInput` array to `send()`:

Copy code

```
import type { ConversationInput } from "@snowflake/cortex-agent-sdk";

const input: ConversationInput = [
  {
    type: "tool_result",
    tool_result: {
      tool_use_id: toolUseId,
      name: "weather",
      status: "success",
      content: [{ type: "json", json: { temperature_c: 21, condition: "clear" } }],
    },
  },
  { type: "text", text: "Give the user a one-sentence forecast." },
];
const toolTurn: Turn = await convo.send(input);

const document: ConversationInput = [
  {
    type: "document",
    source: {
      url: "@MY_DB.MY_SCHEMA.MY_STAGE/quarterly-results.txt",
      file_name: "quarterly-results.txt",
      media_type: "text/plain",
    },
  },
  { type: "text", text: "Summarize this document." },
];
const documentTurn: Turn = await convo.send(document);
```

Select alternate agent types:

For coding-agent turns, `permission_policy: "always_allow"` automatically approves tool operations that would
otherwise require approval. Use it only with trusted inputs and appropriately scoped workspace and account access. Use
an approval-based permission policy when your application is prepared to handle permission-request events and submit
approval decisions.

Copy code

```
data_turn: Turn = conversation.send(
    "Summarize Q1 revenue.",
    agent={
        "type": "data",
        "spec": {
            "database": "ANALYTICS",
            "schema": "PUBLIC",
            "name": "FINANCE_AGENT",
            # "version": "LIVE",
        },
    },
)

coding_turn: Turn = conversation.send(
    "Write the summary to a markdown file.",
    agent={
        "type": "coding",
        "spec": {
            "models": {"orchestration": "claude-sonnet-4-5"},
            "permission_policy": "always_allow",
            "workspace_mounts": [{"name": "USER$MY_USER.PUBLIC.DEFAULT$"}],
        },
    },
)
```

For approval-based flows, create a coding conversation with `permission_policy` set to `"always_ask"`. `send()` and
`send_permission_decisions()` both use that conversation’s agent. An inline conversation, such as `conversation`
above, has no coding tools and does not emit permission requests. Stream events from the returned turn. When a
`response.tool_use` event includes permission options, show those options to the approver. Use
`send_permission_decisions()` to continue the conversation after the approver selects options. The helper waits for
the paused turn and uses its assistant message as the parent of the follow-up turn. If a turn requests multiple
permissions, include every selected decision in one `send_permission_decisions()` call. Any pending request omitted
from that call is denied. When you pass a `PermissionRequest`, the SDK rejects a decision that is not one of the
request’s `options`. To explain a denial to the model, add an optional third `reason` item to the decision tuple.

Copy code

```
approval_conversation: Conversation = client.conversations.create(
    origin_application="my-app",
    agent={
        "type": "coding",
        "spec": {
            "models": {"orchestration": "claude-sonnet-4-5"},
            "permission_policy": "always_ask",
            "workspace_mounts": [{"name": "USER$MY_USER.PUBLIC.DEFAULT$"}],
        },
    },
)
pending_turn: Turn = approval_conversation.send("Delete the temporary file.")
permission_requests = pending_turn.permission_requests()

def selected_decision_for(permission):
    return "Allow this command" if "Allow this command" in permission.options else "Deny"

def selected_permission_decision(permission):
    decision = selected_decision_for(permission)
    if decision == "Deny":
        # The optional reason is shown to the model for a denied request.
        return (permission, decision, "Deleting files is not allowed in this environment.")
    return (permission, decision)

if permission_requests:
    continued_turn: Turn = approval_conversation.send_permission_decisions(
        [selected_permission_decision(permission) for permission in permission_requests]
    )
    response = continued_turn.result()
else:
    response = pending_turn.result()

print(response.text)
```

### Execute client-side tools

To configure a generic client-side tool, include it in `tools` and omit a matching entry in `tool_resources`. The
service emits that tool use with `client_side_execute: true`. Call `client_tool_uses()` on the pending turn, execute
every returned invocation in your application, then send every result in one `send_tool_results()` call. The helper
constructs the required `tool_result` content and uses the paused assistant message as the follow-up parent.

Copy code

```
from typing import Any

from cortex_agent_sdk import ClientToolUse

tool_conversation: Conversation = client.conversations.create(
    origin_application="my-app",
    agent={
        "type": "inline",
        "spec": {
            "models": {"orchestration": "claude-sonnet-4-5"},
            "tools": [
                {
                    "tool_spec": {
                        "type": "generic",
                        "name": "get_weather",
                        "description": "Get the current weather for a city.",
                        "input_schema": {
                            "type": "object",
                            "properties": {"location": {"type": "string"}},
                            "required": ["location"],
                        },
                    }
                }
            ],
            # No tool_resources["get_weather"] entry: the application executes this tool.
        },
    },
)

def execute_client_tool(tool_use: ClientToolUse) -> dict[str, Any]:
    # Dispatch to the application's weather service.
    return {"location": tool_use.input["location"], "temperature_c": 18, "condition": "clear"}

pending_tool_turn: Turn = tool_conversation.send("What is the weather in San Francisco?")
tool_uses = pending_tool_turn.client_tool_uses()
if tool_uses:
    continued_tool_turn = tool_conversation.send_tool_results(
        [(tool_use, execute_client_tool(tool_use)) for tool_use in tool_uses]
    )
    tool_response = continued_tool_turn.result()
else:
    tool_response = pending_tool_turn.result()
print(tool_response.text)
```

For other structured client content, pass a `ConversationInput` array to `send()`:

Copy code

```
from cortex_agent_sdk import ConversationInput

document: ConversationInput = [
    {
        "type": "document",
        "source": {
            "url": "@MY_DB.MY_SCHEMA.MY_STAGE/quarterly-results.txt",
            "file_name": "quarterly-results.txt",
            "media_type": "text/plain",
        },
    },
    {"type": "text", "text": "Summarize this document."},
]
document_turn: Turn = conversation.send(document)
```

## Continue a conversation

Attach to an existing thread to continue from the latest assistant message. Branch from an earlier assistant message
when you want the next turn to use that message as its parent.

TypeScriptPython

Copy code

```
const attached: Conversation = await client.conversations.attach(convo.id);
const attachedTurn: Turn = await attached.send("Where did we leave off?", {
  agent: { type: "inline", spec: { models: { orchestration: "claude-sonnet-4-5" } } },
});

const branch: Conversation = convo.branch(firstAssistantMessageId);
const branchTurn: Turn = await branch.send("Follow up on the first thing you said.", {
  agent: { type: "inline", spec: { models: { orchestration: "claude-sonnet-4-5" } } },
});
```

Inspect history and manage the thread:

Copy code

```
import type { ConversationMessage, SuccessResponse } from "@snowflake/cortex-agent-sdk";

convo.id; // string

const messages: ConversationMessage[] = await convo.history();
for (const message of messages) {
  console.log(`#${message.id} [${message.role}]`, message.text.slice(0, 80));
}

const renamed: SuccessResponse = await convo.rename("Q1 revenue analysis");
const deleted: SuccessResponse = await convo.delete();
```

Copy code

```
from cortex_agent_sdk import ConversationMessage

attached: Conversation = client.conversations.attach(conversation.id)
branch: Conversation = conversation.branch(message_id=123)
messages: list[ConversationMessage] = conversation.history()

conversation.rename("Quarterly analysis")
conversation.delete()
```

`attach()` continues from the latest assistant message. In Python, pass `message_id` to start from a specific message
instead. `branch()` creates a local branch from a specific message without changing the original object.

The agent passed to `create()` lives only on that conversation object. `attach()` does not copy it, so pass `agent` on
each later `send()`. If you omit it, the next turn uses an empty inline agent.

## Calls are serialized

Calls to `send()` are serialized inside one `Conversation` instance. Before the SDK dispatches another turn, it
resolves the prior turn and uses the latest assistant message as the parent. This guarantees correct parent message
ordering. A failed turn does not advance the conversation.

Note

If another client adds turns to the same thread, call `client.conversations.attach(threadId)` again when you need to
resync with the newest assistant message.

## List and search threads

TypeScript `client.conversations` can list and search threads without dropping to the direct API. Python
`ConversationsResource` does not include these methods; use the direct thread API described in
[Use the direct Cortex Agent API](/user-guide/snowflake-cortex/cortex-agent-sdk/running-agents).

Copy code

```
import type { SearchThreadsResponse, ThreadMetadata } from "@snowflake/cortex-agent-sdk/api";

const threads: ThreadMetadata[] = await client.conversations.list({
  origin_application: "cortex_agent_sdk",
  page_size: 20,
});

const matches: SearchThreadsResponse = await client.conversations.search({
  query: "quarterly revenue",
  limit: 5,
});
```

## Use the direct API when needed

In most cases, use `client.conversations`. The conversation helper creates the thread, tracks the current parent
message, starts durable turns, exposes result/event/cancel helpers, and keeps follow-up turns in order.

Use the direct API only when you want to manage `thread_id` and `parent_message_id` yourself, inspect raw transport
wrappers, or build a workflow around lower-level REST resources. For those APIs, see
[Use the direct Cortex Agent API](/user-guide/snowflake-cortex/cortex-agent-sdk/running-agents).

## Next steps

- [Direct Agent API](/user-guide/snowflake-cortex/cortex-agent-sdk/running-agents): Use low-level run, thread, and agent-object resources
- [SDK reference](/user-guide/snowflake-cortex/cortex-agent-sdk/sdk-reference): High-level return types and raw transport wrappers

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
