# Trace analytics for Cortex AI Gateway

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Trace analytics charts the gateway’s trace table in Snowsight: which models your users call, how often
requests fail, which MCP tools agents call, and how long conversations run. Each chart is computed from
[AGENT\_TRACE\_TABLE](/user-guide/snowflake-cortex/cortex-ai-gateway/observability) for the time range you
choose.

To open it, sign in to Snowsight, select **AI Gateway** > **Observability**, and then select the
**Analytics** tab. It has four views: Models, Reliability, Tools, and Sessions.

## Before you begin

- Set `logging.enabled` to `true` in the gateway specification. See [Gateway specification](/user-guide/snowflake-cortex/cortex-ai-gateway#label-cortex-ai-gateway-specification).
- Select a warehouse in the page header. The charts run their queries on it.
- Use a role with one of these privileges on the gateway:

| Privilege | What the charts cover |
| --- | --- |
| MONITOR or OWNERSHIP | Every user’s traces. |
| USAGE | Only your own traces. |

Expand

Show lessSee more

## What the charts count

The charts count two kinds of span:

- **Model requests**: spans with `gen_ai.operation.name` set to `chat`.
- **Tool calls**: MCP tool calls, spans with `gen_ai.operation.name` set to `execute_tool`.

Spans that clients send to the gateway over OTLP aren’t included. See
[Send client traces to the gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/observability#label-cortex-ai-gateway-client-traces).

Input tokens include cache reads, and output tokens include reasoning tokens.

Note

Trace analytics is provided for informational purposes to help you monitor and troubleshoot gateway
usage. Metrics are approximate, may be incomplete or delayed, and aren’t intended to be used as a measure
of service performance or availability.

## Models

The Models view covers model requests: which models are called, by how many users, and with how many
tokens.

The summary cards show **Requests**, successful and failed; **Input tokens**, including cache reads;
**Output tokens**; and **Active users**, the distinct users who sent a model request.

| Chart or table | What it shows |
| --- | --- |
| Requests per model | Requests per hour or day, stacked by the model that served them. |
| Users per model | Distinct users per hour or day, stacked by model. |
| Input tokens per model, Output tokens per model | Tokens per hour or day, stacked by model. |
| Input tokens per request, Output tokens per request, Tokens per request | P50, P90, and P99 per request over time. Tokens per request is input plus output. |
| Cache read tokens per request | P50, P90, and P99 of cached input tokens per request, for providers that report cache use. |
| Requests per user, Tokens per user | P50, P90, and P99 across users of each user’s requests or tokens per hour or day. |
| Most used models | Models ranked by requests, with tokens, share of requests, and distinct users. |

Expand

Show lessSee more

## Tools

The Tools view covers MCP tool calls through the gateway, by server and tool. A turn is one model
request plus the tool calls that follow it. Tool latency and failure rates are on the Reliability view.

The summary cards show **Tool calls**; **MCP servers called**; the median **Tool calls per turn**,
counting turns with no tool call as zero; and **Turns with a tool call**, the percentage of turns that
made at least one.

| Chart or table | What it shows |
| --- | --- |
| Tool calls per MCP server, Tool calls per tool | Tool calls per hour or day, stacked by server or tool. |
| Tool calls per turn | A histogram of turns by number of tool calls, and P50, P90, and P99 over time. |
| Repeated tool calls | Percentage of tool calls that repeat an earlier call with the same arguments in the same turn. Only calls that report their arguments are counted. |
| Most used tools | Tools ranked by calls, with MCP server, share of calls, and distinct users. |

Expand

Show lessSee more

## Reliability

The Reliability view covers latency, failures, and prompt cache use for model requests and tool calls.

The summary cards cover model requests. They show **Latency**, the median time from when the gateway
receives a successful request to its last token; **Cache hit rate**, the percentage of input tokens read
from the prompt cache, for providers that report cache use; **Failure rate**, the percentage of requests
with an outcome other than Success or Cancelled; and **Rate limited**, the percentage rejected with HTTP 429.

| Chart or table | What it shows |
| --- | --- |
| End-to-end latency | P50, P90, and P99 latency of successful model requests over time. |
| Cache hit rate | P50, P90, and P99 across requests of each request’s cache hit rate. |
| Rate limits by model | HTTP 429 rejections per hour or day, stacked by model. |
| Rate limit rate | Percentage of requests rejected with HTTP 429, over time. |
| Model request failure rate | P50, P90, and P99 across users of each user’s failure rate. |
| Tool request failure rate | P50, P90, and P99 across tools of each tool’s failure rate. |
| Tool failure rate by MCP server, Tool failure rate by tool | Percentage of tool calls that failed, for each server or tool, over time. |
| Unsuccessful requests | Model requests that didn’t succeed, per hour or day, stacked by [outcome](#label-cortex-ai-gateway-trace-analytics-outcomes). |
| Outcome breakdown | Percentage of model requests with each outcome. Unknown requests are counted in a note below the chart. |
| Highest model failure rates | Model and error pairs with the most failures, such as `503 Service unavailable`, with count, failure rate, and trend. |
| Highest tool failure rates | Tools ranked by failure rate, with MCP server, calls, failed calls, and P50 and P95 latency. |

Expand

Show lessSee more

## Sessions

The Sessions view covers conversations: how long they run and how responses end. A session is the set
of requests that share a `gen_ai.conversation.id`. Requests without one aren’t in any session. See
[How traces are structured](/user-guide/snowflake-cortex/cortex-ai-gateway/observability#label-cortex-ai-gateway-trace-structure).

The summary cards show the median **Turns per session**, **Tool calls per session**, **Tokens per
session**, and **Session duration**, measured from a session’s first request to its last, including idle
time.

| Chart or table | What it shows |
| --- | --- |
| Turns per session, Tool calls per session, Tokens per session, Session duration | P50, P90, and P99 by the day the session started. |
| Stop reasons | Why responses ended, by model: natural end, tool call, token limit, content filter, other, or not reported. |
| Long sessions | Sessions above the 95th percentile for turns or tool calls, with conversation ID, agent, client, user, turns, tool calls, tokens, duration, and percentile. |

Expand

Show lessSee more

When you filter the Sessions view by model, only sessions whose model requests all used the selected
models are shown. With two models selected, that’s sessions that used only the first, only the second,
or both.

## Request outcomes

Each model request and tool call gets an outcome from its HTTP status code:

| Outcome | Meaning |
| --- | --- |
| Success | The request completed without an error. |
| Throttled | Rejected with HTTP 429 because a rate limit was reached. |
| Policy denied | Rejected with HTTP 401 or 403, for example because the caller lacked access or a quota blocked the user. |
| Cancelled | The client cancelled the request before it completed (HTTP 499). |
| Invalid request | Rejected with any other 4xx status, such as a malformed request or an unknown model. |
| Server failure | The gateway or model provider returned an HTTP 5xx status. |
| Unknown | No status code was recorded. |

Expand

Show lessSee more

Failure rates and rate-limit rates exclude Unknown requests.

## Cost considerations

Each view queries the trace table on the warehouse you selected, which consumes warehouse credits.
Longer time ranges and busier gateways scan more data. For the cost of storing traces, see
[Cost considerations](/user-guide/snowflake-cortex/cortex-ai-gateway/observability#label-cortex-ai-gateway-observability-cost).
