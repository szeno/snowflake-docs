# Cortex Agent SDK reference

— Open

Available to all accounts.

Use this reference when you need details about SDK response objects, thread message helpers, transport wrappers, error
classes, retry behavior, and per-request options. For workflow examples, see
[Conversations](/user-guide/snowflake-cortex/cortex-agent-sdk/conversations) and
[Use the direct Cortex Agent API](/user-guide/snowflake-cortex/cortex-agent-sdk/running-agents). For authentication
examples, see
[Authenticate Cortex Agent SDK requests](/user-guide/snowflake-cortex/cortex-agent-sdk/authentication).

## Response views

Response views wrap the typed message content union so you can use getters such as `text`, `tool_uses` or `toolUses`,
`tables`, and `charts` without switching on content discriminators yourself.

| Class | Wraps |
| --- | --- |
| `AgentResponseView` | An assistant response from a direct run. |
| `AgentResponse` | The high-level response returned by a conversation `Turn`. |
| `ThreadMessageView` | A persisted thread message returned by the direct threads resource. |

Expand

Show lessSee more

### Content getters

Each getter filters the content array down to one kind of item.

TypeScriptPython

Common members include:

- `view.text`: all text values concatenated in order
- `view.content`: full content array
- `view.texts`: text blocks
- `view.thinkings`: reasoning blocks
- `view.toolUses`: tool calls made by the model
- `view.toolResults`: tool results
- `view.toolResultsAggregated`: aggregated tool-result rollups
- `view.tables`: tabular results
- `view.charts`: chart artifacts
- `view.assets`: asset references
- `view.suggestedQueries`: suggested follow-up queries
- `view.images`: inline images
- `view.documents`: document references
- `view.artifacts`: persisted artifacts
- `view.permissionDecisions`: permission decisions emitted by the agent
- `view.actualUserMessages`: user-facing messages emitted by the agent

Common members include:

- `view.text`: all text values concatenated in order
- `view.content`: full content array
- `view.texts`: text blocks
- `view.thinkings`: reasoning blocks
- `view.tool_uses`: tool calls made by the model
- `view.tool_results`: tool results
- `view.tool_results_aggregated`: aggregated tool-result rollups
- `view.tables`: tabular results
- `view.charts`: chart artifacts
- `view.assets`: asset references
- `view.suggested_queries`: suggested follow-up queries
- `view.images`: inline images
- `view.documents`: document references
- `view.artifacts`: persisted artifacts
- `view.permission_decisions`: permission decisions emitted by the agent
- `view.actual_user_messages`: user-facing messages emitted by the agent

### Finder methods

Search response content by tool name.

TypeScriptPython

Copy code

```
import type { ToolResultContentItem, ToolUseContentItem } from "@snowflake/cortex-agent-sdk/types";

const anyCall: ToolUseContentItem | undefined = view.findToolUse();
const analystCall: ToolUseContentItem | undefined = view.findToolUse("analyst");
const sqlResult: ToolResultContentItem | undefined = view.findToolResult("system_execute_sql");
const allSqlCalls: ToolUseContentItem[] = view.getToolUsesByName("system_execute_sql");
```

The single-item finders return `undefined` when nothing matches.

Copy code

```
any_call = view.find_tool_use()
analyst_call = view.find_tool_use("analyst")
sql_result = view.find_tool_result("system_execute_sql")
all_sql_calls = view.get_tool_uses_by_name("system_execute_sql")
```

The single-item finders return `None` when nothing matches.

### `AgentResponseView`

`AgentResponseView` represents a completed assistant response from the direct API.

TypeScriptPython

Important members include:

- `view.role`: `"assistant"`, always
- `view.metadata`: `ResponseMetadata`, including `run_id`, `thread_id`, message IDs, and usage
- `view.events`: `ServerSentEvent[] | undefined`, populated when the view was built from a stream
- `view.requestId`: Snowflake request ID, when present
- `view.responseBody`: full parsed response body
- `view.response`: underlying HTTP response, available for headers and status only

You can create an `AgentResponseView` by calling a direct run method with `stream: false`, by calling
`AgentResponseView.fromStream(stream)` after draining an `AgentRunStream`, or by calling
`AgentResponseView.fromThreadMessage(message)` when reading a persisted assistant reply from thread history.

Important members include:

- `view.role`: `"assistant"`, always
- `view.metadata`: response metadata, including `run_id`, `thread_id`, message IDs, and usage
- `view.events`: ordered raw events, populated when the view was built from a stream
- `view.request_id`: Snowflake request ID, when present
- `view.response_body`: full parsed response body

### `ThreadMessageView`

`ThreadMessageView` wraps a raw thread message returned by the direct threads resource.

TypeScriptPython

Copy code

```
import {
  ThreadMessageView,
  type APIResponse,
  type DescribeThreadsResponse,
  type ThreadMessage,
} from "@snowflake/cortex-agent-sdk/api";

const detail: APIResponse<DescribeThreadsResponse> = await api.threads.describe(threadId);
for (const raw of detail.responseBody.messages ?? []) {
  const message: ThreadMessageView = new ThreadMessageView(raw as ThreadMessage);
  console.log(message.messageId, message.role, message.text);
}
```

Thread-specific members include `messageId`, `parentId`, `role`, `createdOn`, `requestId`, `messageType`, `status`,
`schemaVersion`, `tags`, and `raw`.

Copy code

```
from cortex_agent_sdk.api import ThreadMessageView

detail = api.threads.describe(thread_id)
for raw in detail.get("messages", []):
    message = ThreadMessageView(raw)
    print(message.message_id, message.role, message.text)
```

Thread-specific members include `message_id`, `parent_id`, `role`, `created_on`, `request_id`, `message_type`,
`status`, `schema_version`, `tags`, and `raw`.

In TypeScript, Snowflake thread and message identifiers are preserved as strings so `int64` IDs remain exact. Python returns those identifiers as `int`.

## Thread pagination

Use pagination helpers when listing threads through the direct API.

TypeScriptPython

`api.threads.list()` returns a response wrapper whose `.page` field is a `ThreadsPage`.

Copy code

```
import type { PagedAPIResponse, ThreadMetadata, ThreadsPage } from "@snowflake/cortex-agent-sdk/api";

const first: PagedAPIResponse<ThreadMetadata> = await api.threads.list({ page_size: 50 });
const page: ThreadsPage<ThreadMetadata> = first.page;

for await (const thread of page) {
  console.log(thread.thread_id, thread.thread_name);
}
```

You can also page manually:

Copy code

```
let current: ThreadsPage<ThreadMetadata> = (
  await api.threads.list({ page_size: 100 })
).page;
while (true) {
  for (const thread of current.data) {
    console.log(thread.thread_id);
  }
  if (!current.hasMore) break;
  current = (await current.getNextPage()).page;
}
```

Copy code

```
page = api.threads.list(page_size=50)
for thread in page:
    print(thread["thread_id"], thread.get("thread_name"))
```

## Transport wrappers

Direct API resource methods can expose parsed response bodies together with transport metadata. Use these wrappers when
you need request IDs, response headers, or status details from the underlying HTTP call.

### `APIResponse<T>`

TypeScriptPython

`APIResponse<T>` is returned by methods such as `api.threads.create()`, `api.agent.create()`, and
`api.requestWithResponse()`:

Copy code

```
import type { APIResponse } from "@snowflake/cortex-agent-sdk/api";
import type { AgentResponse as AgentResponseBody } from "@snowflake/cortex-agent-sdk/types";

const res: APIResponse<AgentResponseBody> = await api.requestWithResponse<AgentResponseBody>(
  "/api/v2/cortex/agent:run",
  { method: "POST", body: { ...body, stream: false } },
);

res.responseBody;
res.requestId;
res.response.headers.get("x-snowflake-request-id");
```

Use these members:

- `responseBody`: parsed JSON body
- `response`: raw HTTP `Response`
- `requestId`: `x-snowflake-request-id`, when present

The body has already been consumed to populate `responseBody`. Do not call `res.response.json()` or
`res.response.text()`.

The Python direct API returns parsed response objects for most resources. Response view and background-run objects
carry the request ID and parsed body when the server returns them.

Copy code

```
view = api.agent.run(
    {
        "messages": [{"role": "user", "content": [{"type": "text", "text": "Hello."}]}],
        "stream": False,
    }
)

print(view.response_body)
print(view.request_id)
```

### `ResponseCarrier<T>`

`ResponseCarrier<T>` is not a class that application code usually constructs directly. It is the shared TypeScript
base behind raw wrapper objects such as `AsyncRun` and `AgentResponseView`, which is why those objects expose the same
transport fields as `APIResponse<T>`: `responseBody`, `response`, and `requestId`.

TypeScriptPython

The following example reads the fields that those wrappers inherit from `ResponseCarrier<T>`:

Copy code

```
import type { AgentResponseView, AsyncRun } from "@snowflake/cortex-agent-sdk/api";

const view: AgentResponseView = await api.agent.run({
  messages: [{ role: "user", content: [{ type: "text", text: "Hello." }] }],
  stream: false,
});

const run: AsyncRun = await api.agent.run({
  messages: [{ role: "user", content: [{ type: "text", text: "Long task." }] }],
  stream: false,
  background: true,
});

console.log(view.responseBody, view.requestId);
console.log(run.responseBody, run.requestId);
```

The equivalent Python classes expose snake\_case members such as `response_body` and `request_id`.

Copy code

```
view = api.agent.run({"messages": messages, "stream": False})
run = api.agent.run({"messages": messages, "stream": False, "background": True})

print(view.response_body, view.request_id)
print(run.response_body, run.request_id)
```

### `api.requestWithResponse`

Use `requestWithResponse()` when you need the TypeScript direct API client’s request primitive and the
`APIResponse<T>` transport wrapper.

TypeScriptPython

Copy code

```
import type { APIResponse } from "@snowflake/cortex-agent-sdk/api";
import type { AgentResponse as AgentResponseBody } from "@snowflake/cortex-agent-sdk/types";

const res: APIResponse<AgentResponseBody> = await api.requestWithResponse<AgentResponseBody>(
  "/api/v2/cortex/agent:run",
  { method: "POST", body: { ...body, stream: false } },
);
```

It rejects `stream: true`. For streaming requests, use `api.agent.stream()`, `api.agent.run()`, `api.runs.stream()`, or
`api.runs.resume()`.

Use the Python direct resource methods for the same endpoints. The public Python API does not require a separate
`requestWithResponse()` wrapper for normal SDK usage.

## Error hierarchy

The SDK raises typed errors for API and client-side failures.

TypeScriptPython

```
Error
└── CortexAgentError
    └── CortexAgentAPIError
        ├── BadRequestError
        ├── AuthenticationError
        ├── PermissionDeniedError
        ├── NotFoundError
        ├── ConflictError
        ├── UnprocessableEntityError
        ├── RateLimitError
        └── InternalServerError
```

Every `CortexAgentError` can expose `name`, `status`, `requestId`, and `body`.

Copy code

```
import {
  CortexAgentAPIError,
  CortexAgentError,
  NotFoundError,
  RateLimitError,
} from "@snowflake/cortex-agent-sdk";

try {
  await api.threads.describe(threadId);
} catch (error) {
  if (error instanceof RateLimitError) {
    // 429
  } else if (error instanceof NotFoundError) {
    // 404
  } else if (error instanceof CortexAgentAPIError) {
    // other non-2xx HTTP responses
  } else if (error instanceof CortexAgentError) {
    // client-side failures such as validation or SSE parsing
  } else {
    throw error;
  }
}
```

```
Exception
└── CortexAgentError
    ├── CortexAgentAPIError  (alias: APIStatusError)
    │   ├── BadRequestError
    │   ├── AuthenticationError
    │   ├── PermissionDeniedError
    │   ├── NotFoundError
    │   ├── ConflictError
    │   ├── UnprocessableEntityError
    │   ├── RateLimitError
    │   └── InternalServerError
    ├── APIConnectionError
    │   └── APITimeoutError
    └── APIConnectionAbortedError
```

`APIConnectionError`, `APITimeoutError`, and `APIConnectionAbortedError` inherit from `CortexAgentError`, not from
`CortexAgentAPIError`. An `except CortexAgentAPIError` block does not catch DNS, TLS, timeout, or cancellation
failures.

Copy code

```
from cortex_agent_sdk import (
    APIConnectionAbortedError,
    APIConnectionError,
    APITimeoutError,
    AuthenticationError,
    CortexAgentAPIError,
    CortexAgentError,
    NotFoundError,
    RateLimitError,
)

try:
    api.threads.describe(thread_id)
except RateLimitError:
    # 429
    raise
except NotFoundError:
    # 404
    raise
except CortexAgentAPIError as err:
    print(err.status, err.request_id, err.body)
except APITimeoutError:
    raise
except APIConnectionError:
    raise
except APIConnectionAbortedError:
    raise
except CortexAgentError:
    raise
```

Every `CortexAgentError` exposes `message`, `status`, `request_id`, and `body`. Python exceptions do not have a
`name` attribute; use `type(err).__name__`.

If an auth-refresh callback fails, the SDK raises the original API error and attaches safe refresh metadata. In
TypeScript, read `err.authRefresh.provider`, `err.authRefresh.attempt`, `err.authRefresh.requestId`, and `err.cause`.
In Python, read `err.auth_refresh.provider`, `err.auth_refresh.attempt`, `err.auth_refresh.request_id`, and
`err.__cause__`.

## Retries

The SDK can retry transient transport failures:

- `408`
- `409`
- `429`
- `5xx`

Client-level retry defaults apply automatically only to retry-safe methods: `GET`, `HEAD`, and `OPTIONS`. For
mutating requests, including agent runs and resource creation, pass a per-request retry policy to opt in to replaying
the request after a transient failure.

TypeScriptPython

TypeScript retries use exponential backoff with `Retry-After` support and these defaults:

- Initial delay: `500ms`
- Multiplier: `2x`
- Maximum nominal delay: `30_000ms`
- Additive jitter: up to `500ms`
- Default `maxRetries`: `2`
- Default `retryStreaming`: `false`

Configure retries on the client for retry-safe methods:

Copy code

```
new CortexAgentClient({
  account,
  auth,
  retryPolicy: { maxRetries: 5 },
});
```

Or per request:

Copy code

```
await api.threads.describe(
  threadId,
  {},
  { retryPolicy: { maxRetries: 0 } },
);
```

Mutating requests require a per-request retry policy:

Copy code

```
await api.agent.run(
  {
    messages: [{ role: "user", content: [{ type: "text", text: "Summarize the thread." }] }],
    stream: false,
  },
  { retryPolicy: { maxRetries: 1 } },
);
```

Streaming requests are not retried by default, including pre-response network failures. Opt in explicitly when
reconnecting to a run stream:

Copy code

```
const stream = api.runs.resume(runId, {
  retryPolicy: { maxRetries: 1, retryStreaming: true },
});
await stream.done();
```

Python retries use exponential backoff with `Retry-After` support and these defaults:

- Initial delay: `0.5` seconds
- Multiplier: `2x`
- Maximum delay: `8` seconds
- Multiplicative jitter: shortens the computed delay by up to 25%
- Default `max_retries`: `2`
- Default `retry_streaming`: `False`

Three additional rules change whether a response is retried and how long the SDK waits:

- An `x-should-retry` header overrides the status-code decision. `true` retries the response, and `false` does not.
- `retry-after-ms` is preferred over `Retry-After`. The SDK reads `retry-after-ms` first and treats the value as
  milliseconds.
- A `Retry-After` delay longer than 60 seconds is ignored. The SDK uses normal backoff instead, capped at 8 seconds.

Configure retries on the client for retry-safe methods:

Copy code

```
client = CortexAgentClient(
    account=account,
    auth=auth,
    retry_policy={"max_retries": 5},
)
```

Or per request:

Copy code

```
api.threads.describe(thread_id, options={"retry_policy": {"max_retries": 0}})
```

Mutating requests require a per-request retry policy:

Copy code

```
api.agent.run(
    {
        "messages": [{"role": "user", "content": [{"type": "text", "text": "Summarize the thread."}]}],
        "stream": False,
    },
    options={"retry_policy": {"max_retries": 1}},
)
```

Streaming requests are not retried by default, including pre-response network failures. Opt in explicitly when
reconnecting to a run stream.

Mid-stream retry remains a caller concern.

## Request options

Raw resource request methods accept per-request options.

TypeScriptPython

The TypeScript `RequestOpts` type includes:

Copy code

```
export interface RequestOpts {
  signal?: AbortSignal;
  timeout?: number;
  retryPolicy?: RetryPolicy;
  headers?: Record<string, string>;
  query?: Record<string, string | number | boolean | undefined>;
  streamReadTimeoutMs?: number;
}
```

Use these fields for:

- `signal`: abort a request
- `timeout`: non-streaming request timeout in milliseconds
- `retryPolicy`: per-request retry override
- `headers`: custom headers merged into the request
- `query`: extra query parameters
- `streamReadTimeoutMs`: dead-socket timeout for streaming requests

On methods that also take query parameters, `opts` is the last argument:

Copy code

```
await api.threads.describe(threadId, {}, { retryPolicy: { maxRetries: 0 } }); // correct
await api.threads.describe(threadId, { retryPolicy: { maxRetries: 0 } }); // wrong: becomes a query param
```

Pass transport overrides through the `options` argument on resource methods. Python timeout values are in seconds.

Copy code

```
api.threads.describe(
    thread_id,
    options={
        "timeout": 30,
        "retry_policy": {"max_retries": 0},
        "headers": {"X-Trace-ID": "trace-123"},
        "stream_read_timeout": 180,
    },
)
```

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
