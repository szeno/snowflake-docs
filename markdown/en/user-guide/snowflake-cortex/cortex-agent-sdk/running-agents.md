# Use the direct Cortex Agent API

— Open

Available to all accounts.

Use [conversations](/user-guide/snowflake-cortex/cortex-agent-sdk/conversations) for most application flows. The
conversation API manages threads, parent messages, durable turns, event replay, cancellation, and final-response
fallback behavior for you.

Use the direct API when you need to build the Agent API request body yourself, choose a wire-level response mode,
manage thread and run IDs directly, or create and update saved agent objects.

## Create a direct API client

Import the direct API client when you need low-level resources.

TypeScriptPython

Copy code

```
import { CortexAgentClient } from "@snowflake/cortex-agent-sdk/api";

const api: CortexAgentClient = new CortexAgentClient({
  account: process.env.SNOWFLAKE_ACCOUNT!,
  auth: process.env.SNOWFLAKE_PAT!,
});
```

The direct TypeScript client exposes `api.agent`, `api.codingAgent`, `api.threads`, `api.runs`, `api.feedback`, and
`api.requestWithResponse()`.

Copy code

```
from cortex_agent_sdk.api import CortexAgentClient

api: CortexAgentClient = CortexAgentClient(account="my_account", auth="<token>")
```

The direct Python client exposes `agent`, `coding_agent`, `threads`, `runs`, and `feedback`.

## Choose a run mode

Direct agent requests can stream events, return a completed response, or start durable background work.

| `stream` | `background` | Returns |
| --- | --- | --- |
| `true` or omitted | Any | Server-sent events. The TypeScript `stream*()` helpers return `AgentRunStream`. |
| `false` | `false` or omitted | A completed agent response view. |
| `false` | `true` | A background run handle. |

Expand

Show lessSee more

## Run an inline agent

Use an inline run when the request carries the agent specification.

TypeScriptPython

Stream with callbacks:

Copy code

```
import {
  CortexAgentClient,
  StreamEvent,
  type AgentRunStream,
} from "@snowflake/cortex-agent-sdk/api";

const api: CortexAgentClient = new CortexAgentClient(config);

const stream: AgentRunStream = api.agent.stream({
  models: { orchestration: "claude-sonnet-4-5" },
  messages: [{ role: "user", content: [{ type: "text", text: "Hi." }] }],
});

stream.on(StreamEvent.Text, (delta) => process.stdout.write(delta));
await stream.done();
```

Iterate raw events:

Copy code

```
import type { ServerSentEvent } from "@snowflake/cortex-agent-sdk/api";

for await (const item of api.agent.run({
  models: { orchestration: "claude-sonnet-4-5" },
  messages: [{ role: "user", content: [{ type: "text", text: "Hi." }] }],
})) {
  const event: ServerSentEvent = item;
  if (event.event === "response.text.delta") {
    process.stdout.write(event.text ?? "");
  }
}
```

Get the completed response:

Copy code

```
import type { AgentResponseView } from "@snowflake/cortex-agent-sdk/api";

const view: AgentResponseView = await api.agent.run({
  models: { orchestration: "claude-sonnet-4-5" },
  messages: [{ role: "user", content: [{ type: "text", text: "Hi." }] }],
  stream: false,
});

console.log(view.text);
console.log(view.requestId);
```

Stream events:

Copy code

```
from cortex_agent_sdk.api import CortexAgentClient

api: CortexAgentClient = CortexAgentClient(account="my_account", auth="<token>")

for event in api.agent.run(
    {
        "models": {"orchestration": "auto"},
        "messages": [{"role": "user", "content": [{"type": "text", "text": "Hi."}]}],
    }
):
    print(event)
```

Get the completed response:

Copy code

```
from cortex_agent_sdk.api import AgentResponseView

view: AgentResponseView = api.agent.run(
    {
        "models": {"orchestration": "auto"},
        "messages": [{"role": "user", "content": [{"type": "text", "text": "Hi."}]}],
        "stream": False,
    }
)

print(view.text)
print(view.request_id)
```

## Start background runs

Use background mode when work might outlive one HTTP request or client connection. If you are using the high-level
conversation API, every `conversation.send()` already starts durable server-side work and returns a `Turn`.

TypeScriptPython

Start a low-level background run:

Copy code

```
import type { AsyncRun } from "@snowflake/cortex-agent-sdk/api";

const run: AsyncRun = await api.agent.run({
  models: { orchestration: "claude-sonnet-4-5" },
  messages: [{ role: "user", content: [{ type: "text", text: "Prepare a detailed analysis." }] }],
  stream: false,
  background: true,
});

console.log(run.runId);
```

Reconnect to the run event stream:

Copy code

```
import type { ServerSentEvent } from "@snowflake/cortex-agent-sdk/api";

for await (const event of api.runs.stream(run.runId)) {
  const item: ServerSentEvent = event;
  if (item.event === "response.text.delta") {
    process.stdout.write(item.text ?? "");
  }
}
```

Cancel server-side work:

Copy code

```
await api.runs.cancel(run.runId);
```

Both `runs.stream()` and `runs.resume()` accept `startingAfter` to skip events whose `sequence_number` is less than or
equal to the cursor you pass.

Start a low-level background run:

Copy code

```
from cortex_agent_sdk.api import BackgroundRun

run: BackgroundRun = api.agent.run(
    {
        "models": {"orchestration": "auto"},
        "messages": [{"role": "user", "content": [{"type": "text", "text": "Prepare a detailed analysis."}]}],
        "stream": False,
        "background": True,
    }
)

print(run.run_id)
```

Reconnect to the run event stream:

Copy code

```
for event in api.runs.stream(run.run_id):
    print(event)
```

Cancel server-side work:

Copy code

```
api.runs.cancel(run.run_id)
```

## Manage threads directly

Use the threads resource only when you need to manage `thread_id` and `parent_message_id` yourself. For most
multi-turn application flows, use `client.conversations` instead.

TypeScriptPython

Low-level thread methods return `APIResponse<T>` wrappers.

Copy code

```
import {
  ThreadMessageView,
  type APIResponse,
  type DescribeThreadsResponse,
  type PagedAPIResponse,
  type SearchThreadsResponse,
  type SuccessResponse,
  type ThreadMetadata,
  type ThreadsPage,
} from "@snowflake/cortex-agent-sdk/api";

const created: APIResponse<ThreadMetadata> = await api.threads.create({
  origin_application: "my-app",
});

for await (const event of api.agent.run({
  thread_id: created.responseBody.thread_id,
  parent_message_id: "0",
  models: { orchestration: "claude-sonnet-4-5" },
  messages: [{ role: "user", content: [{ type: "text", text: "Summarize this week's ML papers." }] }],
})) {
  // Handle streaming events.
}

const listed: PagedAPIResponse<ThreadMetadata> = await api.threads.list({
  origin_application: "my-app",
  page_size: 50,
});

const page: ThreadsPage<ThreadMetadata> = listed.page;
for await (const thread of page) {
  console.log(thread.thread_id, thread.thread_name);
}

const detail: APIResponse<DescribeThreadsResponse> = await api.threads.describe(
  created.responseBody.thread_id,
  { page_size: 100 },
);

for (const raw of detail.responseBody.messages ?? []) {
  const message: ThreadMessageView = new ThreadMessageView(raw);
  console.log(`#${message.messageId} [${message.role}]`, message.text);
}

const updated: APIResponse<SuccessResponse> = await api.threads.update(created.responseBody.thread_id, {
  thread_name: "Weekly ML digest",
});

const search: APIResponse<SearchThreadsResponse> = await api.threads.search({
  query: "vector databases",
  limit: 10,
  query_type: "FUZZY",
});

const deleted: APIResponse<SuccessResponse> = await api.threads.delete(created.responseBody.thread_id);
```

Copy code

```
thread = api.threads.create(origin_application="my-app")

for event in api.agent.run(
    {
        "thread_id": thread["thread_id"],
        "parent_message_id": "0",
        "models": {"orchestration": "auto"},
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": "Summarize this week's ML papers."}],
            }
        ],
    }
):
    print(event)

threads = api.threads.list(origin_application="my-app", page_size=50)
detail = api.threads.describe(thread["thread_id"], page_size=100)
api.threads.update(thread["thread_id"], thread_name="Weekly ML digest")
api.threads.search(query="vector databases", limit=10, query_type="FUZZY")
api.threads.delete(thread["thread_id"])
```

## Manage agent objects

An agent object is a Snowflake object created with [CREATE AGENT](/sql-reference/sql/create-agent). It stores an agent
specification under a fully qualified name so you can reuse governed tools, resources, and instructions without sending
the full configuration on every request.

TypeScriptPython

Copy code

```
import type { APIResponse } from "@snowflake/cortex-agent-sdk/api";
import type { SuccessResponse } from "@snowflake/cortex-agent-sdk";
import type {
  DescribeAsResourceAgentResponse,
  ShowAsResourceAgentResponse,
} from "@snowflake/cortex-agent-sdk/types";

const schema: { database: string; schema: string } = { database: "MY_DB", schema: "PUBLIC" };
const target: { database: string; schema: string; name: string } = {
  ...schema,
  name: "my_analyst_agent",
};

const created: APIResponse<SuccessResponse> = await api.agent.create(
  schema,
  {
    name: target.name,
    models: { orchestration: "auto" },
    instructions: {
      orchestration: "Use the analyst tool for anything quantitative.",
      response: "Be concise.",
    },
    tools: [{ tool_spec: { type: "cortex_analyst_text_to_sql", name: "analyst" } }],
  },
  { createMode: "orReplace" },
);

const listed: APIResponse<ShowAsResourceAgentResponse[]> = await api.agent.list(schema);
const described: APIResponse<DescribeAsResourceAgentResponse> = await api.agent.describe(target);
const updated: APIResponse<SuccessResponse> = await api.agent.update(target, {
  comment: "Updated by the SDK",
});
const deleted: APIResponse<SuccessResponse> = await api.agent.delete(target, {
  ifExists: true,
});
```

`createMode` accepts `"orReplace"`, `"errorIfExists"`, or `"ifNotExists"`. The `agent_spec` field returned by
`describe()` is a JSON string.

Copy code

```
schema = {"database": "ANALYTICS", "schema": "PUBLIC"}
target = {**schema, "name": "SALES_AGENT"}

created = api.agent.create(
    {"name": target["name"], "models": {"orchestration": "auto"}},
    target=schema,
    create_mode="orReplace",
)
agents = api.agent.list(target=schema)
info = api.agent.describe(target=target)
updated = api.agent.update({"comment": "Updated by the SDK"}, target=target)
deleted = api.agent.delete(target=target, if_exists=True)
```

## Run agent objects directly

Use a saved agent object through the direct API when you need explicit wire-level controls. For the normal
conversation path, select the saved agent object in `conversation.send()`. See
[Conversations](/user-guide/snowflake-cortex/cortex-agent-sdk/conversations).

TypeScriptPython

Copy code

```
import type { AgentResponseView, DataAgentTarget } from "@snowflake/cortex-agent-sdk/api";

const target: DataAgentTarget = {
  database: "MY_DB",
  schema: "PUBLIC",
  name: "my_analyst_agent",
};

const view: AgentResponseView = await api.agent.runData(target, {
  messages: [{ role: "user", content: [{ type: "text", text: "Which product line grew fastest?" }] }],
  stream: false,
});
```

Use `runVersion()` instead of `runData()` to pin a direct run to a specific version.

Copy code

```
view = api.agent.run_data(
    {
        "messages": [{"role": "user", "content": [{"type": "text", "text": "Which products grew fastest?"}]}],
        "stream": False,
    },
    target={"database": "ANALYTICS", "schema": "PUBLIC", "name": "SALES_AGENT"},
)
```

Use `run_version()` instead of `run_data()` to pin a direct run to a specific version.

## Send feedback for an agent object

Feedback is available for saved agent objects. The feedback `request_id` is the HTTP request ID, not the run ID.

TypeScriptPython

Copy code

```
if (!answer.requestId) {
  throw new Error("The response did not include a request ID.");
}

await api.feedback.send(target, {
  request_id: answer.requestId,
  positive: true,
});
```

Copy code

```
if answer.request_id is None:
    raise RuntimeError("The response did not include a request ID.")

api.feedback.send(
    target={"database": "ANALYTICS", "schema": "PUBLIC", "name": "SALES_AGENT"},
    request_id=answer.request_id,
    positive=True,
    feedback_message="Helpful answer.",
    categories=["helpful"],
)
```

## Run the coding-agent toolset

Use the direct coding-agent resource when you need the Agent API response shape with the coding-agent toolset attached.
For the bundled Cortex Code session API with `query()` and long-lived local sessions, see
[Cortex Code](/user-guide/snowflake-cortex/cortex-agent-sdk/cortex-code).

`always_allow` automatically approves coding-agent tool operations that would otherwise require approval, including
destructive-looking shell commands. Use it only when your application intentionally trusts the input source and scopes
workspace mounts, stages, credentials, and network access for that workload. Use an approval-based permission policy
when a person or application approval flow must inspect tool requests before they run.

TypeScriptPython

Copy code

```
import type { AgentResponseView } from "@snowflake/cortex-agent-sdk/api";

const view: AgentResponseView = await api.codingAgent.run({
  models: { orchestration: "claude-sonnet-4-5" },
  messages: [{ role: "user", content: [{ type: "text", text: "Summarize this repository." }] }],
  permissionPolicy: "always_allow",
  workspaceMounts: [{ name: "USER$MYUSER.PUBLIC.DEFAULT$" }],
  stream: false,
});
```

Copy code

```
view = api.coding_agent.run(
    {
        "models": {"orchestration": "claude-sonnet-4-5"},
        "messages": [{"role": "user", "content": [{"type": "text", "text": "Summarize this repository."}]}],
        "permission_policy": "always_allow",
        "workspace_mounts": [{"name": "USER$MY_USER.PUBLIC.DEFAULT$"}],
        "stream": False,
    }
)
```

For approval-based flows, set `permissionPolicy` or `permission_policy` to `always_ask` and stream the run. When a
`response.tool_use` event includes permission options, show those options to the approver. Send the selected option
back as a `permission_decision` content item in a follow-up request.

The following example starts a coding-agent run, captures the approval request, sends `Allow this command` on the same
thread, and waits for the continued response.

TypeScriptPython

Copy code

```
import {
  CortexAgentClient,
  type AgentResponseView,
  type AsyncRun,
  type ServerSentEvent,
} from "@snowflake/cortex-agent-sdk/api";

const api: CortexAgentClient = new CortexAgentClient({
  account: process.env.SNOWFLAKE_ACCOUNT!,
  auth: process.env.SNOWFLAKE_PAT!,
});

const prompt =
  "Run this exact bash command and report the stdout: " +
  "rm -rf /tmp/cortex-agent-sdk-permission-example-does-not-exist && echo permission-example-ok";

function getToolUseId(event: ServerSentEvent): string {
  const id = (event as { tool_use_id?: unknown }).tool_use_id;
  if (typeof id !== "string") throw new Error("Permission event missing tool_use_id.");
  return id;
}

const thread = await api.threads.create({});
const threadId = String(thread.responseBody.thread_id);

const approvalRun: AsyncRun = await api.codingAgent.run({
  thread_id: threadId,
  parent_message_id: 0,
  messages: [{ role: "user", content: [{ type: "text", text: prompt }] }],
  permissionPolicy: "always_ask",
  models: { orchestration: "claude-sonnet-4-5" },
  stream: false,
  background: true,
});

let permissionEvent: ServerSentEvent | undefined;
for await (const event of approvalRun.events()) {
  if (event.event === "response.tool_use" && "permission" in event) {
    permissionEvent = event;
  }
}

const approvalResponse: AgentResponseView = await approvalRun.result();
if (!permissionEvent) throw new Error("The run did not request permission.");
if (!approvalResponse.messageId) throw new Error("The approval response did not include a message id.");

const continuedRun: AsyncRun = await api.codingAgent.run({
  thread_id: threadId,
  parent_message_id: approvalResponse.messageId,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "permission_decision",
          permission_decision: {
            tool_use_id: getToolUseId(permissionEvent),
            decision: "Allow this command",
          },
        },
      ],
    },
  ],
  permissionPolicy: "always_ask",
  models: { orchestration: "claude-sonnet-4-5" },
  stream: false,
  background: true,
});

const continuedResponse = await continuedRun.result();
console.log(continuedResponse.text);
```

Copy code

```
import os

from cortex_agent_sdk.api import AgentEvent, CortexAgentClient

api: CortexAgentClient = CortexAgentClient(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    auth=os.environ["SNOWFLAKE_PAT"],
)

prompt = (
    "Run this exact bash command and report the stdout: "
    "rm -rf /tmp/cortex-agent-sdk-permission-example-does-not-exist && echo permission-example-ok"
)

def get_tool_use_id(event: AgentEvent) -> str:
    value = event.get("tool_use_id")
    if not isinstance(value, str):
        raise RuntimeError("Permission event missing tool_use_id")
    return value

thread = api.threads.create()
thread_id = str(thread["thread_id"])

approval_run = api.coding_agent.run(
    {
        "thread_id": thread_id,
        "parent_message_id": 0,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        "permission_policy": "always_ask",
        "models": {"orchestration": "claude-sonnet-4-5"},
        "stream": False,
        "background": True,
    }
)

permission_event: AgentEvent | None = None
for event in api.runs.stream(approval_run.run_id):
    if event.get("event") == "response.tool_use" and "permission" in event:
        permission_event = event

approval_response = approval_run.wait()
if permission_event is None:
    raise RuntimeError("The run did not request permission")
if approval_response.message_id is None:
    raise RuntimeError("The approval response did not include a message id")

continued_run = api.coding_agent.run(
    {
        "thread_id": thread_id,
        "parent_message_id": approval_response.message_id,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "permission_decision",
                        "permission_decision": {
                            "tool_use_id": get_tool_use_id(permission_event),
                            "decision": "Allow this command",
                        },
                    }
                ],
            }
        ],
        "permission_policy": "always_ask",
        "models": {"orchestration": "claude-sonnet-4-5"},
        "stream": False,
        "background": True,
    }
)

continued_response = continued_run.wait()
print(continued_response.text)
```

## Streaming events

Streaming calls yield server-sent event values. Common events include:

- `response.text.delta`: text token produced
- `response.text`: text block complete
- `response.thinking.delta` and `response.thinking`: reasoning content
- `response.tool_use`: tool invocation
- `response.tool_result`: tool result
- `response.status`: status update
- `response.warning`: non-fatal warning
- `response`: terminal event with final `content`, `metadata`, and status

## About error `399528`

Sometimes `GET /agent/runs/{runId}` returns HTTP 200 with an SSE body whose first event is:

```
event: error
data: {"code":"399528","message":"run stream not attachable"}
```

This does not necessarily mean the run failed. The condition can indicate either of the following situations:

- A short startup race, where the run exists but live streaming is not ready yet
- A run whose live stream is unavailable even though the assistant reply will still be written to the thread

The SDK handles the condition as follows:

- `Turn.result()` hides this condition and falls back to thread polling automatically.
- `runs.stream()` and `runs.resume()` stay low-level and surface the SSE error event as-is.

## Next steps

- [Asynchronous Python client](/user-guide/snowflake-cortex/cortex-agent-sdk/async-python): Use asynchronous patterns in the Python Agent client
- [Cortex Agent SDK features](/user-guide/snowflake-cortex/cortex-agent-sdk/sdk-features): Use MCP servers, coding-agent options, and detailed streaming events
- [Cortex Code](/user-guide/snowflake-cortex/cortex-agent-sdk/cortex-code): Use the bundled coding-agent session API
- [SDK reference](/user-guide/snowflake-cortex/cortex-agent-sdk/sdk-reference): Use response views, transport wrappers, errors, retries, and request options

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
