# Inference with Cortex AI Gateway

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in Amazon Web Services (AWS) commercial regions only, excluding Asia Pacific (New Zealand), Asia Pacific (Malaysia), and Europe (Spain). For the full list of AWS commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

The Cortex AI Gateway exposes an inference endpoint that accepts requests in industry-standard API
formats. Any client that lets you override its base URL can send requests through the gateway,
including coding agents, agent frameworks, and the official OpenAI and Anthropic SDKs.

All inference runs within the Snowflake perimeter, and usage is attributed to the Snowflake user whose
token made the request, so gateway traffic appears in your existing cost and access reporting.

Note

The gateway is a different endpoint from [Cortex Inference](/user-guide/snowflake-cortex/cortex-rest-api),
which is served on the account under `/api/v2/cortex`. Both accept the same requests, but only traffic
through the gateway picks up its access control, traces, and cost attribution.

## Gateway endpoint

The gateway endpoint takes this form:

```
https://<account-host>/api/v2/aigateways/SNOWFLAKE
```

Append the path for the API you’re calling, either `/v1/chat/completions` or `/v1/messages`. See
[Choose your API](#label-cortex-ai-gateway-choose-your-api).

To get the endpoint for your account, use:

Copy code

```
DESCRIBE AI GATEWAY SNOWFLAKE;
```

Note

Accounts that use [private connectivity](/user-guide/private-connectivity-inbound) reach the gateway on a
different host, so the endpoint won’t match the form above. Use `DESCRIBE AI GATEWAY SNOWFLAKE` to get the endpoint in
that case: it returns the correct value either way.

## Pricing

Inference through the gateway is billed the same way as the
[Cortex Inference](/user-guide/snowflake-cortex/cortex-rest-api): on the number of tokens processed, at
each model’s rate. Refer to the
[Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf)
for each model’s cost.

For attributing that spend to teams and users, and for capping it, see
[Cost management for Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/cost-management).

## Choose your API

The gateway supports two industry-standard API specifications. Pick the one your client requires:

|  | Chat Completions API | Messages API |
| --- | --- | --- |
| Compatibility | [OpenAI Chat Completions API](https://platform.openai.com/docs/api-reference/chat/create) | [Anthropic Messages API](https://docs.anthropic.com/en/api/messages) |
| Path | `/v1/chat/completions` | `/v1/messages` |
| Supported models | All models except Claude (OpenAI, Grok, Llama, Mistral, DeepSeek, Snowflake) | Claude models only |
| SDK support | OpenAI Python and JavaScript SDKs | Anthropic Python SDK |
| Best for | Most clients and use cases | Existing Anthropic integrations |

Expand

Show lessSee more

Note

The OpenAI Responses API (`/v1/responses`) is coming soon to the gateway and not supported yet. If a client offers a choice of API
format, choose Chat Completions or Messages.

## Prerequisites

Before you begin, you need:

1. Your **gateway endpoint**, from `DESCRIBE AI GATEWAY SNOWFLAKE`. See
   [Gateway endpoint](#label-cortex-ai-gateway-url-format).
2. The **USAGE privilege** on the gateway. See
   [Access control](/user-guide/snowflake-cortex/cortex-ai-gateway#label-cortex-ai-gateway-access-control).
3. A **programmatic access token (PAT)** for authentication. See
   [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens).
4. A **model name** to use in requests. See
   [Model availability](/user-guide/snowflake-cortex/cortex-rest-api#label-cortex-complete-llm-model-availability).
5. **Access to the model itself.** The gateway respects model access control: a request still needs
   whatever access the underlying model requires, such as the `SNOWFLAKE.CORTEX_USER` database role or
   the controls described in [Privileges and model access for Cortex AI Functions](/user-guide/snowflake-cortex/aisql-privileges-and-access). USAGE on the
   gateway doesn’t widen the set of models a user is entitled to, so sending traffic through it doesn’t
   expand your security perimeter.

## Setting up authentication

The gateway expects the token as a bearer token:

```
Authorization: Bearer <SNOWFLAKE_PAT>
```

## Quickstart

OpenAI PythonOpenAI JavaScriptAnthropic Pythoncurl

Copy code

```
from openai import OpenAI

client = OpenAI(
  api_key="<SNOWFLAKE_PAT>",
  base_url="<gateway-endpoint>/v1"
)

response = client.chat.completions.create(
  model="openai-gpt-5",
  messages=[
    {"role": "user", "content": "How does a snowflake get its unique pattern?"}
  ]
)

print(response.choices[0].message.content)
```

Copy code

```
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: "<SNOWFLAKE_PAT>",
  baseURL: "<gateway-endpoint>/v1"
});

const response = await client.chat.completions.create({
  model: "openai-gpt-5",
  messages: [
    { role: "user", content: "How does a snowflake get its unique pattern?" }
  ],
});

console.log(response.choices[0].message.content);
```

The Anthropic SDK sends credentials in an `x-api-key` header by default, but the gateway expects a
`Bearer` token. Use an `httpx` client to set the correct header.

Copy code

```
import httpx
import anthropic

PAT = "<SNOWFLAKE_PAT>"

http_client = httpx.Client(
  headers={"Authorization": f"Bearer {PAT}"},
)

client = anthropic.Anthropic(
  api_key="not-used",
  base_url="<gateway-endpoint>",
  http_client=http_client,
  default_headers={"Authorization": f"Bearer {PAT}"},
)

response = client.messages.create(
  model="claude-sonnet-4-5",
  max_tokens=1024,
  messages=[
    {"role": "user", "content": "How does a snowflake get its unique pattern?"}
  ]
)

print(response.content[0].text)
```

The base URL omits the trailing `/v1`, because the Anthropic SDK appends `/v1/messages` itself.

Copy code

```
curl "<gateway-endpoint>/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <SNOWFLAKE_PAT>" \
  -d '{
    "model": "openai-gpt-5",
    "messages": [
      {"role": "user", "content": "How does a snowflake get its unique pattern?"}
    ]
  }'
```

## Supported features

The gateway exposes the same Chat Completions and Messages surfaces as Cortex Inference, so request
and response fields, and the features built on them, behave the same way. See the Cortex Inference
documentation for instructions on:

- **Streaming responses** over server-sent events for both APIs. See
  [Streaming](/user-guide/snowflake-cortex/cortex-rest-api#label-cortex-rest-api-streaming).
- **Tool calling.** See
  [Tool calling](/user-guide/snowflake-cortex/cortex-rest-api#label-cortex-rest-api-tool-calling-chain-of-thought).
- **Structured output.** See
  [Structured output](/user-guide/snowflake-cortex/cortex-rest-api#label-cortex-rest-api-structured-output).
- **Prompt caching.** See
  [Prompt caching](/user-guide/snowflake-cortex/cortex-rest-api#label-cortex-rest-api-prompt-caching).
- **Image input.** See
  [Image input](/user-guide/snowflake-cortex/cortex-rest-api#label-cortex-rest-api-image-input).
- **Thinking and reasoning.** See
  [Thinking and reasoning](/user-guide/snowflake-cortex/cortex-rest-api#label-cortex-rest-api-thinking-reasoning).

For the complete field-level request and response reference, see
[Cortex Inference](/user-guide/snowflake-cortex/cortex-rest-api).

## Instrument a coding agent

Agents differ in which API format they use, where their configuration lives, and how they send
credentials. Use the section for your agent.

### OpenCode

To point OpenCode at the gateway, define a custom provider in your
`~/.config/opencode/opencode.json` file. OpenCode uses the **Chat Completions API** through the
OpenAI-compatible adapter:

Copy code

```
{
  "$schema": "https://opencode.ai/config.json",
  "model": "snowflake-cortex/openai-gpt-5.4",
  "small_model": "snowflake-cortex/openai-gpt-5.4",
  "plugin": [
    [
      "@devtheops/opencode-plugin-otel",
      {
        "enabled": true,
        "tracePropagationProviders": ["snowflake-cortex"]
      }
    ]
  ],
  "provider": {
    "snowflake-cortex": {
      "options": {
        "baseURL": "<gateway-endpoint>/v1",
        "account": "<account-host>",
        "apiKey": "<SNOWFLAKE_PAT>",
        "headers": {
          "snow-agent-name": "opencode"
        }
      }
    }
  }
}
```

Where:

- `baseURL` is the gateway endpoint from `DESCRIBE AI GATEWAY SNOWFLAKE` with `/v1` appended.
- `account` is the host part of that endpoint, without the path.
- `model` and `small_model` are both qualified by the provider name, so they read
  `snowflake-cortex/<model>`. Setting `small_model` as well keeps OpenCode’s lightweight calls on the
  gateway rather than falling back to its default.
- The `snow-agent-name` header identifies the client on each request.
- The `plugin` entry loads the OpenTelemetry plugin and lists the providers it propagates trace context
  to. Naming `snowflake-cortex` in `tracePropagationProviders` makes OpenCode send a `traceparent`
  header on its gateway requests.

### Other clients

Any client that lets you set a custom base URL and bearer token, and connects using either the **Chat Completions API** or **Messages API** can use the gateway. Set the base URL
according to the API format the client uses, as described in [Gateway endpoint](#label-cortex-ai-gateway-url-format),
and supply your PAT as the bearer token.

## Monitor gateway inference

Requests sent through the gateway are recorded in two places:

- **Traces**, for what each request did: models called, timing, tokens, and errors. See
  [Observability for Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/observability).
- **Usage history**, for credits consumed. See
  [AI\_GATEWAY\_USAGE\_HISTORY view](/sql-reference/account-usage/ai_gateway_usage_history).

For cost attribution, budgets, and per-user quotas, see
[Cost management for Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/cost-management).

## Legal notices

Where your configuration of Cortex AI Gateway uses a model provided on the
[Model and Service Pass-Through Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/model-pass-through-terms/),
your use of that model is further subject to the terms for that model on that page.

The data classification of inputs and outputs is as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Customer Data | Customer Data | Preview AI Features [[1]](#footnote-1) |

Expand

Show lessSee more

[1]
Represents the defined term used in the Preview AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).
