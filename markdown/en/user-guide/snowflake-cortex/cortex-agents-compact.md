# Compact a Cortex Agent conversation

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The `agent:compact` endpoint summarizes a conversation and returns the summary as a compact representation that you can pass back to `agent:run` in place of the full message history. Compacting a long conversation reduces the number of tokens consumed by subsequent turns and keeps the conversation within the model context window.

You can supply the message transcript inline, and the summary is returned to the caller without being persisted. Alternately you can supply a thread ID, and the summary is persisted to the thread as a COMPACTION message; you then continue on the next `agent:run` by setting `parent_message_id` to the returned `end_message_id`.

See also: [Cortex Agents Run API](/user-guide/snowflake-cortex/cortex-agents-run), [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage), [Threads](/user-guide/snowflake-cortex/cortex-agents-threads)

## Endpoint

Copy code

```
POST /api/v2/cortex/agent:compact
```

### Request headers

| Header | Value |
| --- | --- |
| `Authorization` | (Required) Bearer <token> — Use a Snowflake JWT or OAuth token. |
| `Content-Type` | (Required) application/json |
| `Accept` | (Required) application/json — `agent:compact` returns a single JSON response; streaming is not supported. |
| `X-Snowflake-Authorization-Token-Type` | KEYPAIR\_JWT or OAUTH — required when using the corresponding token type. |

Expand

Show lessSee more

## Compaction modes

The endpoint behavior depends on whether you include a `thread_id` in the request body:

| Type | What to provide | What happens | Response fields |
| --- | --- | --- | --- |
| Inline | `model` + `messages` (full transcript) | Snowflake summarizes the supplied transcript. Nothing is persisted to a thread. | `summary` |
| Thread ID | `model` + `thread_id` (optionally + `end_message_id`) | Snowflake reads the thread up to `end_message_id`, summarizes it, and persists a COMPACTION message on the thread. To continue, call `agent:run` with `parent_message_id` set to the returned `end_message_id`; the persisted summary is folded in automatically. | `summary`, `end_message_id` |

Expand

Show lessSee more

Tip

Use **thread ID** when your application manages conversations with threads. The persisted COMPACTION message means your application does not need to carry the summary forward; on the next `agent:run`, set `parent_message_id` to the returned `end_message_id` and the summary is folded in from the thread.

Use **inline** when you manage conversation history client-side and want to compact a `messages` array before passing it to the next `agent:run` call.

## Request body

### Conditional parameters

Provide either `messages` (stateless mode) or `thread_id` (stateful mode). If both are provided, `thread_id` takes precedence and `messages` is ignored.

| Parameter | Type | Description |
| --- | --- | --- |
| `messages` | array | Required for stateless mode. The full conversation transcript to compact. Each element is a message object in the same format used by `agent:run`. The array must contain at least one user message. The transcript must start with a user message (an optional single leading system message is allowed) and alternate between user and assistant. |
| `thread_id` | integer | Required for stateful mode. The ID of the thread whose history will be summarized. If the user owns the thread they will be able to compact it. |

Expand

Show lessSee more

### Optional parameters

| Parameter | Type | Description |
| --- | --- | --- |
| `end_message_id` | integer | Stateful mode only. The ID of the last message in the thread to include in the compaction. Messages after this ID are excluded. Must be non-zero when provided. If omitted, Snowflake compacts the thread up to the newest assistant message in the thread (COMPACTION and other non-conversational rows, and any trailing user turn with no assistant reply, are skipped). |
| `model` | string | The model to use for summarization. When omitted, Snowflake auto-selects a model (same behavior as `agent:run`). If specified, Snowflake recommends using the same model as the corresponding `agent:run` calls. |

Expand

Show lessSee more

## Response body

The endpoint returns a single JSON object. The fields present depend on the mode:

| Field | Type | Mode | Description |
| --- | --- | --- | --- |
| `summary` | string | Both | A natural-language summary of the conversation up to the compacted point. In stateless mode, wrap this in a compaction content block and prepend it to the next `agent:run` call. |
| `end_message_id` | integer | Stateful only | The ID of the last message included in the compaction. Pass this value as `parent_message_id` on the next `agent:run` call to resume the thread, or use it as the compaction boundary for subsequent compact calls. |

Expand

Show lessSee more

## Cost and usage monitoring

Each `agent:compact` call is billed like other Cortex Agent requests: in AI Credits per million tokens processed, at the rate for the model used to generate the summary. For model rates, see [Cortex Agents pricing](/user-guide/snowflake-cortex/pricing).

Compaction usage appears in the [CORTEX\_AGENT\_USAGE\_HISTORY](/sql-reference/account-usage/cortex_agent_usage_history) view. These requests are attributed to the `compaction` origin application so that you can distinguish their token and credit usage from other Cortex Agent requests.

## Access control

The calling role must have the following privileges. Requirements are the same as for `agent:run`:

| Privilege | Object | Required for |
| --- | --- | --- |
| SNOWFLAKE.CORTEX\_USER or SNOWFLAKE.CORTEX\_AGENT\_USER database role | Snowflake account | All API calls to Cortex Agents endpoints. |
| UBAC | Thread | Stateful mode — reading and compacting the thread. |

Expand

Show lessSee more

## Usage notes

- `agent:compact` does not support streaming. The endpoint always returns a single JSON response.
- In stateful mode, the COMPACTION message written to the thread is opaque to the caller. To continue, call `agent:run` with `parent_message_id` set to the returned `end_message_id`; the orchestrator folds the persisted summary into that turn.
- Compacting a thread does not delete the original messages. The full message history remains readable via the thread API; only the summary is used for future `agent:run` turns.
- If `end_message_id` points to a message that does not exist on the thread, the endpoint returns an error.
- The quality of the summary depends on the model specified. Snowflake recommends using the same model for compaction as for the `agent:run` calls in the same conversation.
- Calling `agent:compact` on a thread that already has a COMPACTION message appends a new compaction. The most recent COMPACTION message is used for subsequent `agent:run` calls.

## Examples

### Compact a transcript without a thread

Compact a `messages` array that you are managing client-side. The summary is returned to the caller and is not persisted:

Copy code

```
curl -X POST "https://<account>.snowflakecomputing.com/api/v2/cortex/agent:compact" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "model": "auto",
    "messages": [
      { "role": "user",      "content": [{ "type": "text", "text": "What were total sales last quarter?" }] },
      { "role": "assistant", "content": [{ "type": "text", "text": "Total sales last quarter were $4.2M ..." }] },
      { "role": "user",      "content": [{ "type": "text", "text": "Which region performed best?" }] },
      { "role": "assistant", "content": [{ "type": "text", "text": "The Western region led with $1.8M ..." }] },
      { "role": "user",      "content": [{ "type": "text", "text": "How does that compare to Q3?" }] },
      { "role": "assistant", "content": [{ "type": "text", "text": "Q3 Western region was $1.5M, a 20% increase ..." }] }
    ]
  }'
```

Example response:

Copy code

```
{
  "summary": "The user asked about sales performance. Total sales last quarter were $4.2M. The Western region led with $1.8M, a 20% increase from $1.5M in Q3."
}
```

To continue the conversation, wrap the returned summary in a compaction content block and prepend it as the first message in the next `agent:run` call:

Copy code

```
{
  "models": { "orchestration": "auto" },
  "messages": [
    { "role": "user", "content": [{ "type": "compaction", "summary": "The user asked about sales performance. Total sales last quarter were $4.2M. The Western region led with $1.8M, a 20% increase from $1.5M in Q3." }] },
    { "role": "user", "content": [{ "type": "text", "text": "Which product lines drove Western region growth?" }] }
  ]
}
```

### Compact using thread ID

Compact a thread by ID. The summary is persisted as a COMPACTION message on the thread; continue by calling `agent:run` with `parent_message_id` set to the returned `end_message_id`:

Copy code

```
curl -X POST "https://<account>.snowflakecomputing.com/api/v2/cortex/agent:compact" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "model": "auto",
    "thread_id": 123
  }'
```

Example response:

Copy code

```
{
  "summary": "The user asked about sales performance. Total sales last quarter were $4.2M. The Western region led with $1.8M, a 20% increase from Q3.",
  "end_message_id": 456
}
```

After the compaction, continue with `agent:run` and set `parent_message_id` to the returned `end_message_id` so the persisted summary is folded into the next turn:

Copy code

```
curl -X POST "https://<account>.snowflakecomputing.com/api/v2/databases/my_db/schemas/my_schema/agents/my_agent:run" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "messages": [
      { "role": "user", "content": [{ "type": "text", "text": "Which product lines drove Western region growth?" }] }
    ],
    "thread_id": 123,
    "parent_message_id": 456
  }'
```

### Compact a thread up to a specific message

Use `end_message_id` to compact only part of a thread, leaving later messages outside the compaction boundary:

Copy code

```
curl -X POST "https://<account>.snowflakecomputing.com/api/v2/cortex/agent:compact" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "model": "auto",
    "thread_id": 123,
    "end_message_id": 456
  }'
```

## Limitations

- `agent:compact` does not support streaming. The endpoint returns a single JSON response only.
- Stateless compaction requires at least one user message. Messages must alternate between user and assistant roles. A single system message is allowed at the start of the array before the first user message.
- If you provide both `messages` and `thread_id`, `thread_id` takes precedence and `messages` is ignored.
- `end_message_id` is supported in stateful mode only; it is ignored in stateless mode.
- Compacting a thread does not remove the original messages from the thread history.
