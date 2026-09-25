# Observability for Cortex AI Gateway

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in Amazon Web Services (AWS) commercial regions only, excluding Asia Pacific (New Zealand), Asia Pacific (Malaysia), and Europe (Spain). For the full list of AWS commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

Cortex AI Gateway records traces and spans for all requests traversing the gateway. Traces give you
full execution transparency into agent behavior: which models were invoked, step timing, token
consumption, and failure reasons.

Query traces with the `AGENT_TRACE_TABLE` table function:

Copy code

```
-- Retrieve request and response records for the SNOWFLAKE gateway
SELECT * FROM TABLE(AGENT_TRACE_TABLE('SNOWFLAKE'));
```

Querying `AGENT_TRACE_TABLE` requires the MONITOR privilege on the gateway object. See
[Access control](/user-guide/snowflake-cortex/cortex-ai-gateway#label-cortex-ai-gateway-access-control).

Note

Traces the gateway records, and traces client applications export to it, land directly in customer-owned
event tables inside your Snowflake security boundary, where access is governed by native Snowflake RBAC.
Credit and usage metering is collected separately and surfaced in
[AI\_GATEWAY\_USAGE\_HISTORY view](/sql-reference/account-usage/ai_gateway_usage_history).

By default the gateway records metadata about each request, not its content. Prompt and response
payloads are captured only when payload capture is explicitly enabled. See
[Change the specification](/user-guide/snowflake-cortex/cortex-ai-gateway#label-cortex-ai-gateway-change-specification).

## How traces are structured

The gateway models AI activity using standard OpenTelemetry execution hierarchies:

- **Conversation thread** (`conversation_id`): an optional identifier grouping related multi-turn
  interactions over time.
- **Trace** (`trace_id`): a single end-to-end execution, or agent turn, which can encompass multiple
  model calls.
- **Span** (`span_id`): a single atomic unit of work within a trace, such as one inference call. Each
  span records timing, status, the model requested, token counts, and outcome metadata.

Each span is one row. Group rows by `trace_id` to assemble a trace, and a `conversation_id` groups
related traces into one thread:

```
conversation_id          Optional. Groups related turns in one thread.
    └── trace_id         One agent turn, which may encompass multiple model invocations.
        └── span         operation = 'chat'          An inference call.
```

Every inference span has `gen_ai.operation.name` set to `chat`.

To inspect traces, spans, and conversations without assembling any of this yourself, use the AI Gateway
Observability page in Snowsight.

Note

Both identifiers come from the request itself:

- `conversation_id` is populated from a specific request header, so it’s only present when the client
  sends it.
- `trace_id` comes from the request’s `traceparent` header, following the
  [W3C Trace Context](https://www.w3.org/TR/trace-context/) convention.

## Send client traces to the gateway

The spans the gateway records are what it sees from the outside: one span per request it serves. A client
that uses OpenTelemetry can also export its own traces to the gateway, which adds the client’s view of
the same work, including the steps it took between requests.

Client telemetry is off until you turn it on in the gateway specification:

Copy code

```
ALTER AI GATEWAY SNOWFLAKE FROM SPECIFICATION $$
schema_version: 1
models:
  - name: '*'
logging:
  enabled: true
  enable_client_telemetry: true
$$;
```

`FROM SPECIFICATION` replaces the whole specification, so start from what `DESCRIBE AI GATEWAY` returns.
See [Change the specification](/user-guide/snowflake-cortex/cortex-ai-gateway#label-cortex-ai-gateway-change-specification).

The gateway then accepts OTLP traces over `http/protobuf` or `http/json` at
`<gateway-endpoint>/telemetry/v1/traces`, authenticated with the same programmatic access token you use
for inference. Get the endpoint from `DESCRIBE AI GATEWAY SNOWFLAKE`, as described in
[Gateway endpoint](/user-guide/snowflake-cortex/cortex-ai-gateway/inference#label-cortex-ai-gateway-url-format).

Client-exported spans land in `AGENT_TRACE_TABLE` alongside the spans the gateway records, so a single
query covers both.

The attributes a client exports are the client’s own, so they vary by client and aren’t described here.
When the client propagates its trace context on the requests it sends, its spans share a `trace_id` with
the gateway’s, so grouping on it reassembles a turn from both sides. See
[Trace context propagation](#label-cortex-ai-gateway-trace-propagation).

### What the exporter has to be set to

Whatever client you’re configuring, its OTLP trace exporter needs these three values:

| Setting | Value |
| --- | --- |
| Protocol | `http/protobuf` or `http/json`. |
| Endpoint | `<gateway-endpoint>/telemetry/v1/traces`. |
| Authorization header | `Bearer <SNOWFLAKE_PAT>`, the same credential inference uses. |

Expand

Show lessSee more

A client that reads the standard OpenTelemetry environment variables takes these as
`OTEL_EXPORTER_OTLP_TRACES_PROTOCOL`, `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`, and
`OTEL_EXPORTER_OTLP_TRACES_HEADERS`, with `OTEL_TRACES_EXPORTER` set to `otlp`. Clients that keep
telemetry behind a switch of their own need that turned on as well.

### Example: OpenCode

OpenCode exports through an OpenTelemetry plugin, configured in
`~/.config/opencode/opencode.json`:

Copy code

```
{
  "plugin": [
    [
      "@devtheops/opencode-plugin-otel",
      {
        "enabled": true,
        "protocol": "http/protobuf",
        "endpoint": "<gateway-endpoint>/telemetry",
        "otlpHeaders": "Authorization=Bearer <SNOWFLAKE_PAT>",
        "tracePropagationProviders": ["snowflake-cortex"]
      }
    ]
  ]
}
```

`endpoint` takes the base, and the exporter appends the OTLP path, so requests arrive at
`<gateway-endpoint>/telemetry/v1/traces`.

### Trace context propagation

For client spans and gateway spans to join into one turn, the client has to send a `traceparent` header
on its requests. Without it both sides are still recorded, they just don’t share a `trace_id`.

For how to turn propagation on when setting up a coding agent, see
[Instrument a coding agent](/user-guide/snowflake-cortex/cortex-ai-gateway/inference#label-cortex-ai-gateway-coding-agents).

## What the gateway records

Traces are stored in a Snowflake [event table](/developer-guide/logging-tracing/event-table-setting-up),
so they use the standard event table schema: identifiers and timing are top-level columns, while
semantic detail lives in the `scope`, `record`, `record_attributes`, and `resource_attributes` objects,
which you extract with the colon operator and cast. For the full schema, see
[Event table columns](/developer-guide/logging-tracing/event-table-columns). Because every gateway row is a span,
`record_type` is always `SPAN`. For the fields a span carries, see
[the `SPAN` record type](/developer-guide/logging-tracing/event-table-columns#label-event-table-record-column-span).

### Span identity and outcome

| Column or attribute | Description |
| --- | --- |
| `start_timestamp`, `timestamp` | When the span started and ended. Subtract them for duration. |
| `trace:"trace_id"` | Which execution the span belongs to. Group on this to reassemble a turn. |
| `trace:"span_id"` | The span’s own identifier. |
| `record:"parent_span_id"` | The parent span. `NULL` marks the root span of a trace. |
| `record:"name"` | The operation and model, such as `chat claude-sonnet-5`. |
| `record:"kind"` | The span kind. The gateway’s own spans are `SPAN_KIND_SERVER`. |
| `scope:"name"` | What emitted the span. The gateway’s own spans are `aigateway/tracing`. See [Send client traces to the gateway](#label-cortex-ai-gateway-client-traces). |
| `record:"status":"code"` | The outcome: `STATUS_CODE_OK`, `STATUS_CODE_ERROR`, or `STATUS_CODE_UNSET`. |
| `record:"status":"message"` | Either `client_error` or `server_error`. Set only when the span failed. |

Expand

Show lessSee more

### Gateway and user

These live in `resource_attributes`, because they describe the process that emitted the span rather than
the individual request.

| Attribute | Description |
| --- | --- |
| `resource_attributes:"ai_gateway_id"` | The identifier of the gateway that served the request. |
| `resource_attributes:"gateway_name"` | The name of the gateway that served the request. |
| `resource_attributes:"user"` | The user who sent the request. |

Expand

Show lessSee more

### Request and response

| Attribute | Description |
| --- | --- |
| `record_attributes:"gen_ai.operation.name"` | The operation. Inference calls are `chat`. |
| `record_attributes:"gen_ai.provider.name"` | The provider that served the request, `anthropic` or `openai`. |
| `record_attributes:"gen_ai.request.model"` | The model requested. `unknown` when the model couldn’t be resolved. |
| `record_attributes:"gen_ai.response.model"` | The model that served the response. Set on responses only. |
| `record_attributes:"gen_ai.conversation.id"` | The conversation thread the turn belongs to, taken from the `x-snowflake-ai-gateway-conversation-id` header, or `x-claude-code-session-id` when that isn’t present. |
| `record_attributes:"gen_ai.usage.input_tokens"`, `record_attributes:"gen_ai.usage.output_tokens"` | Total input tokens, including cached input tokens, and total output tokens for the span. |
| `record_attributes:"gen_ai.usage.cache_creation.input_tokens"`, `record_attributes:"gen_ai.usage.cache_read.input_tokens"` | Prompt cache write and read tokens. These counts are subsets of `gen_ai.usage.input_tokens`, not additional tokens. Populated intermittently. |
| `record_attributes:"gen_ai.request.max_tokens"` | The `max_tokens` value sent with the request. |
| `record_attributes:"gen_ai.request.temperature"`, `record_attributes:"gen_ai.request.seed"` | Sampling parameters, set only when the caller sends them. `seed` applies to OpenAI Chat Completions only. |
| `record_attributes:"gen_ai.output.type"` | The output type, `text`. Unset for reasoning-only responses. |
| `record_attributes:"gen_ai.client.operation.duration"` | Client-observed duration of the inference call. |
| `record_attributes:"openai.api.type"` | The OpenAI API surface used, `chat_completions`. |
| `record_attributes:"gen_ai.input.messages"`, `record_attributes:"gen_ai.output.messages"`, `record_attributes:"gen_ai.system_instructions"` | Prompt, response, and system prompt content. Populated only when request and response capture is enabled. |

Expand

Show lessSee more

Don’t add the cache counts to `gen_ai.usage.input_tokens`, because doing so counts those tokens twice.
Calculate non-cached input as `input tokens - cache read input tokens - cache write input tokens`.

For credits consumed, see [AI\_GATEWAY\_USAGE\_HISTORY view](/sql-reference/account-usage/ai_gateway_usage_history).

### HTTP

| Attribute | Description |
| --- | --- |
| `record_attributes:"http.request_id"` | The request identifier. Set on every span. |
| `record_attributes:"http.status_code"` | The HTTP status code of the response. A value of 400 or greater marks a failed span. |
| `record_attributes:"http.request.header.*"` | Selected request headers, including `:method`, `user-agent`, `content-length`, `anthropic-beta`, and `x-claude-code-session-id`. Snowflake-internal headers are excluded. |

Expand

Show lessSee more

## Query traces

Two queries cover most of what you need: one that lists turns, and one that opens a turn up into its
spans.

Neither filters on scope, so both cover client-exported spans as well as the gateway’s own. Add
`scope:"name"::string = 'aigateway/tracing'` to either to see only what the gateway recorded.

### List turns

Each span is one row, so this rolls the rows of a trace into a single row per turn:

Copy code

```
WITH ev AS (
  SELECT trace:"trace_id"::string                                       AS trace_id,
         trace:"span_id"::string                                        AS span_id,
         record_attributes:"gen_ai.request.model"::string               AS model,
         record_attributes:"gen_ai.input.messages"::string              AS llm_input,
         record_attributes:"gen_ai.conversation.id"::string             AS conversation_id,
         resource_attributes:"user"::string                             AS user_name,
         TRY_TO_NUMBER(record_attributes:"http.status_code"::string)     AS http_status,
         start_timestamp,
         timestamp
  FROM TABLE(AGENT_TRACE_TABLE('SNOWFLAKE'))
  WHERE timestamp >= '<start>' AND timestamp < '<end>'
)
SELECT trace_id,
       MIN(start_timestamp)                                          AS started_at,
       DATEDIFF('millisecond', MIN(start_timestamp), MAX(timestamp)) AS duration_ms,
       COUNT(*)                                                      AS span_count,
       MAX(user_name)                                                AS user_name,
       MIN_BY(model, IFF(model IS NULL, NULL, timestamp))            AS model,
       COUNT(DISTINCT model)                                         AS model_count,
       MAX(conversation_id)                                          AS conversation_id,
       MIN_BY(llm_input, IFF(llm_input IS NULL, NULL, timestamp))    AS first_input,
       IFF(COUNT_IF(http_status >= 400) = 0, 'SUCCESS', 'FAILURE')   AS status
FROM ev
GROUP BY trace_id
ORDER BY started_at DESC
LIMIT 10000;
```

### Inspect one turn

Take a `trace_id` from the previous query. One row per span means no rollup is needed:

Copy code

```
SELECT trace:"span_id"::string                                              AS span_id,
       record:"name"::string                                                AS span_name,
       record_attributes:"gen_ai.operation.name"::string                    AS operation,
       start_timestamp                                                      AS span_start,
       DATEDIFF('millisecond', start_timestamp, timestamp)                  AS duration_ms,
       DATEDIFF('millisecond', MIN(start_timestamp) OVER (), start_timestamp) AS offset_ms,
       record:"status":"code"::string                                       AS status,
       TRY_TO_NUMBER(record_attributes:"http.status_code"::string)          AS http_status,
       record_attributes:"gen_ai.request.model"::string                     AS model,
       TRY_TO_NUMBER(record_attributes:"gen_ai.usage.input_tokens"::string)  AS input_tokens,
       TRY_TO_NUMBER(record_attributes:"gen_ai.usage.output_tokens"::string) AS output_tokens
FROM TABLE(AGENT_TRACE_TABLE('SNOWFLAKE'))
WHERE timestamp >= '<start>' AND timestamp < '<end>'
  AND trace:"trace_id"::string = '<trace_id>'
ORDER BY span_start
LIMIT 2000;
```

To read the prompts and responses, add the content attributes. They’re large, so select them only when
you need them:

Copy code

```
record_attributes:"gen_ai.input.messages"        AS input_messages,
record_attributes:"gen_ai.output.messages"       AS output_messages,
record_attributes:"gen_ai.system_instructions"   AS system_instructions
```

Note

Capturing message content is opt in, so these attributes are populated only when the gateway
specification has both `logging.enabled` and `logging.capture_payload.request_response` set to `true`.
Payload capture records nothing on its own while logging is off. To turn them on, see
[Change the specification](/user-guide/snowflake-cortex/cortex-ai-gateway#label-cortex-ai-gateway-change-specification).

Once it’s on, the captured prompts and responses are retained in the event table in your own account.
Treat that data as sensitive: it contains everything your users sent through the gateway.

## Cost considerations

Traces are stored in an event table, so gateway observability is billed the way other telemetry data is:
Snowflake charges for the serverless compute used to ingest the traces, and for the storage they occupy
in the event table. Refer to the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
for the applicable rates. For more detail on how telemetry ingestion is billed and how to keep it down,
see [Costs of telemetry data collection](/developer-guide/logging-tracing/logging-tracing-billing).

Turning on payload capture records the full prompts and responses, so it increases the volume stored per
request.

## Usage notes

- **Individual records are capped at 1 MB.** Records larger than that are truncated. Truncation behavior preserves the beginning and the end of the record, and truncates the middle sections.
