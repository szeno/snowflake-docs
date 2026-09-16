# Cortex AI Gateway

[Preview Feature](/release-notes/preview-features) — Open

Available to accounts in Amazon Web Services (AWS) commercial regions only, excluding Asia Pacific (New Zealand), Asia Pacific (Malaysia), and Europe (Spain). For the full list of AWS commercial regions, see [Supported cloud regions](/user-guide/intro-regions).

Cortex AI Gateway is where you govern how AI clients in your organization reach the models and systems
they act on. It gives platform teams one place to grant access to models, attribute spend, and see what
AI has done on behalf of your users, while application teams get a single endpoint to build against.

Snowflake creates the gateway for you. Each account has a single gateway object, named `SNOWFLAKE`,
provisioned automatically, so there’s nothing to create before you start.
`ACCOUNTADMIN` may grant and revoke privileges on it for different users. `USAGE` is granted to `PUBLIC`
by default, so the gateway is reachable without any setup; revoke it if you want to restrict who can
send traffic.

To open Cortex AI Gateway, sign in to Snowsight and select **AI & ML** > **Cortex AI Gateway**.

## Capabilities

| Capability | What it does |
| --- | --- |
| [Inference](/user-guide/snowflake-cortex/cortex-ai-gateway/inference) | Gives coding agents, third-party clients, and SDKs a single governed endpoint to send model requests to. |
| [Observability](/user-guide/snowflake-cortex/cortex-ai-gateway/observability) | Records traces and spans for every request, including the models called, step timing, token counts, errors, and custom attributes. |
| [Cost management](/user-guide/snowflake-cortex/cortex-ai-gateway/cost-management) | Attributes gateway spend to teams and users, and applies budgets and per-user quotas to it. |

Expand

Show lessSee more

Note

Cortex AI Gateway is a different object from the `GATEWAY` used in Snowflake ML. Cortex AI Gateway governs Cortex AI inference traffic: model access, cost attribution, and usage
monitoring. A Snowflake ML gateway routes traffic across model serving endpoints, including traffic splitting and shadowing, most commonly used for Snowflake ML
model upgrades and A/B testing. See
[CREATE GATEWAY](/sql-reference/sql/create-gateway).

## Access control

The following privileges apply to the gateway:

| Privilege | Grants the ability to |
| --- | --- |
| USAGE | Send inference requests through the gateway. |
| MONITOR | Query gateway usage data, including the related Account Usage views. |

Expand

Show lessSee more

Grant a role the ability to send inference requests:

Copy code

```
GRANT USAGE ON AI GATEWAY SNOWFLAKE TO ROLE my_role;
```

Grant a role the ability to review usage without sending requests:

Copy code

```
GRANT MONITOR ON AI GATEWAY SNOWFLAKE TO ROLE cost_admin;
```

Remove access:

Copy code

```
REVOKE USAGE ON AI GATEWAY SNOWFLAKE FROM ROLE my_role;
```

Revoking USAGE is how you stop a role from sending inference requests, including as an automated
response to a budget threshold. For an example of a stored procedure that a budget calls at a
threshold, see [Extended example](/user-guide/budgets/custom-actions#label-budget-custom-actions-extended-example).

USAGE on the gateway doesn’t widen what a user can reach. A request still needs whatever access the
underlying model requires, such as the `SNOWFLAKE.CORTEX_USER` database role or the model access
controls described in [Privileges and model access for Cortex AI Functions](/user-guide/snowflake-cortex/aisql-privileges-and-access). The gateway governs
the path traffic takes, not the set of models a user is entitled to.

## View the gateway

List the gateway in your account, which also returns the endpoint to send requests to:

Copy code

```
SHOW AI GATEWAYS;
```

Use that endpoint rather than assembling a URL by hand: accounts that use
[private connectivity](/user-guide/private-connectivity-inbound) reach the gateway on a different host.
See [Gateway endpoint](/user-guide/snowflake-cortex/cortex-ai-gateway/inference#label-cortex-ai-gateway-url-format).

View its configuration:

Copy code

```
DESCRIBE AI GATEWAY SNOWFLAKE;
```

## Monitor a gateway

Gateway monitoring is split across two kinds of surfaces:

- **Activity** surfaces request and response counts, token counts, and latency. For request-level
  detail, see [Observability for Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/observability).
- **Cost** surfaces credit usage across models and users. For cost reporting, see
  [Cost management for Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/cost-management).

## Gateway specification

The gateway’s behavior comes from its specification, which controls which models it exposes and what it
records. View the current specification with:

Copy code

```
DESCRIBE AI GATEWAY SNOWFLAKE;
```

A specification that exposes a named set of models looks like this:

Copy code

```
schema_version: 1
models:
  - name: claude-sonnet-4-6
    type: cortex
  - name: claude-haiku-4-5
    type: cortex
  - name: claude-opus-5
    type: cortex
logging:
  enabled: true
  capture_payload:
    request_response: true
```

To expose every model the account has access to, without maintaining the list, use a `name` of `'*'`:

Copy code

```
schema_version: 1
models:
  - name: '*'
logging:
  enabled: true
  capture_payload:
    request_response: false
```

| Field | Description |
| --- | --- |
| `schema_version` | The version of the specification format. Use `1`. |
| `models` | The models the gateway exposes. Each entry takes a `name` and a `type`. A `name` of `'*'` enables every model available to the account. |
| `models[].type` | Where the model is served from. `cortex` covers the models Snowflake hosts through Cortex. |
| `logging.enabled` | Whether the gateway records traces for the requests that pass through it. This is the switch everything else depends on: while it’s `false`, nothing is recorded no matter what `capture_payload` is set to. See [Observability for Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/observability). |
| `logging.capture_payload.request_response` | Whether prompts and model responses are recorded alongside the metadata. `false` means they aren’t captured. Takes effect only when `logging.enabled` is `true`. Turning this on records the content of requests and responses, so treat the trace table as sensitive once it’s enabled. |

Expand

Show lessSee more

### Change the specification

`ALTER AI GATEWAY ... FROM SPECIFICATION` replaces the specification as a whole rather than patching
the fields you name, so start from what `DESCRIBE AI GATEWAY` returns, edit that, and submit all of it.
A field you leave out falls back to its default.

For example, to start capturing prompts and responses while leaving the rest of the specification as it
was:

Copy code

```
ALTER AI GATEWAY SNOWFLAKE FROM SPECIFICATION $$
schema_version: 1
models:
  - name: claude-sonnet-4-6
    type: cortex
  - name: claude-haiku-4-5
    type: cortex
  - name: claude-opus-5
    type: cortex
logging:
  enabled: true
  capture_payload:
    request_response: true
$$;
```

Run `DESCRIBE AI GATEWAY SNOWFLAKE` afterwards to confirm what the gateway is now running.

## What the gateway logs

With `logging.enabled` set in the specification, every request through the gateway is recorded at the
metadata level: who made it, which model served it, token counts, and timing. Prompts and
model responses are **not** captured unless `logging.capture_payload.request_response` is also turned
on.

For what the metadata surfaces, see [Observability for Cortex AI Gateway](/user-guide/snowflake-cortex/cortex-ai-gateway/observability) and
[AI\_GATEWAY\_USAGE\_HISTORY view](/sql-reference/account-usage/ai_gateway_usage_history).
