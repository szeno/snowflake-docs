# OAuth token exchange for agent delegation

OAuth token exchange lets an application trade a user’s credential for a short-lived Snowflake
access token. That token is limited by a privilege ceiling and labeled with the AI agent that acts
for the user. You can give an agent only the access a task needs, without creating a separate
service user or changing the user’s role grants.

Teams often give agents a shared service user with broad, long-lived privileges, because that is
simpler than scoping access for each task. Such “God-mode” accounts break accountability. You can’t
tell which person authorized an action, which agent took it, or whether the access matched the
task. Token exchange replaces the standing credential with a token issued per task that:

- Acts as the user, so access is never broader than what the user is granted.
- Carries a [Restricted Session Scope](/user-guide/restricted-session-scope) (RSS) that narrows that
  access further for the agent.
- Expires after a fixed lifetime, has no refresh token, and can’t be exchanged again.
- Labels the agent’s sessions with an agent identifier that your application supplies, so that its
  activity appears in query history and access history.

## Overview

| Function | What you can do |
| --- | --- |
| Delegate | Exchange a user’s OAuth access token, programmatic access token, or workload identity credential for an access token the agent uses for the user. |
| Bound | Attach a Restricted Session Scope to the token with a Rich Authorization Request (`authorization_details`). The scope sets a ceiling on what the agent can do in the session. |
| Attribute | Name the acting agent with the `act` parameter so that Snowflake records it with the session. |
| Audit | See agent activity in the `agent_type` column of query history and in the agent information in access history. |

Expand

Show lessSee more

Token exchange is based on
[OAuth 2.0 Token Exchange (RFC 8693)](https://datatracker.ietf.org/doc/html/rfc8693). The privilege
ceiling uses the `authorization_details` parameter from
[OAuth 2.0 Rich Authorization Requests (RFC 9396)](https://datatracker.ietf.org/doc/html/rfc9396).

Snowflake extends RFC 8693 in one important way. In RFC 8693, `act` is a claim that the
authorization server derives from a verified `actor_token`. In Snowflake, `act` is a request
parameter that your application sets. Snowflake doesn’t accept `actor_token`, doesn’t verify `act`,
and doesn’t put an `act` claim in the issued token. Instead, Snowflake records the acting party on
the session. In RFC 8693 terms, the issued token impersonates the user, and `act` is an audit
label.

## How delegation works

1. The user authenticates to Snowflake through your application by using a method they already
   use: [External OAuth](/user-guide/oauth-ext-overview),
   [Snowflake OAuth](/user-guide/oauth-snowflake-overview), a
   [programmatic access token](/user-guide/programmatic-access-tokens), or
   [workload identity federation](/user-guide/workload-identity-federation).
2. Before handing work to an agent, your application sends a token exchange request to the
   `/oauth/token` endpoint. The request includes the user’s credential, the RSS that bounds the
   agent, and the agent’s identity.
3. Snowflake validates the user’s credential and checks that the requested role is granted to the
   user. It then validates the RSS, creates a session bound to the RSS and the agent identity, and
   issues an access token linked to that session.
4. The agent uses the new token. Every session that it opens runs as the user, inside the RSS
   ceiling, and is attributed to the agent.

The user’s role grants never change. The RSS applies only to sessions that are created from the
exchanged token. The user’s other sessions keep their normal access. If the session that Snowflake
creates during the exchange ends, the token stops working, even if it hasn’t expired.

## Protect the subject token

Snowflake doesn’t authenticate the client that calls token exchange. Anyone who holds a valid
subject token can exchange it, including for a token without any RSS. If the agent can read the
subject token, the RSS gives no protection.

- Keep the subject token in your application’s trusted tier, which performs the exchange.
- Never pass the subject token to the agent. Keep it out of prompts, tool inputs, the agent’s
  environment, and logs.
- The issued token’s lifetime doesn’t depend on how long the subject token has left. A subject
  token that expires in a minute can still be exchanged for a token that lasts the full lifetime.

## Request a delegated token

Send a `POST` request to `https://<account_identifier>.snowflakecomputing.com/oauth/token`, with the
body encoded as `application/x-www-form-urlencoded`.

Copy code

```
curl -X POST "https://<account_identifier>.snowflakecomputing.com/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=urn:ietf:params:oauth:grant-type:token-exchange" \
  --data-urlencode "subject_token=${USER_ACCESS_TOKEN}" \
  --data-urlencode "subject_token_type=urn:ietf:params:oauth:token-type:access_token" \
  --data-urlencode "scope=session:role:ANALYST" \
  --data-urlencode 'authorization_details=[{"type":"snowflake-rss.v1","rss":"GOVERNANCE.SCOPES.INVOICE_AGENT"}]' \
  --data-urlencode 'act={"sub":"invoice-reconciliation-agent","type":"agent"}'
```

If the request succeeds, Snowflake returns HTTP 200. The response body is the issued access token
as plain text, without a surrounding JSON object or quotes:

```
eyJraWQiOiI...
```

The response has a `Content-Type` of `application/json`, but the body isn’t valid JSON. Read the
body as text instead of parsing it as JSON.

Treat the response as a credential. Don’t cache it in intermediaries, and don’t log it.

### Request parameters

| Parameter | Description |
| --- | --- |
| `grant_type` | Required. `urn:ietf:params:oauth:grant-type:token-exchange`. |
| `subject_token` | Required. The user’s credential. Send it in the request body. Snowflake also accepts it in an `Authorization: Bearer` header, but that header is more likely to be logged by proxies. |
| `subject_token_type` | Required. The type of `subject_token`. For supported values, see [Supported subject tokens](#label-oauth-token-exchange-subject-tokens). |
| `scope` | Recommended. `session:role:<role_name>` limits the agent’s sessions to that single role, with no secondary roles. The role must be granted to the user. If you omit `scope`, sessions use the user’s default role and default secondary roles, which can include every role granted to the user. An unquoted role name is converted to uppercase. To match a role whose name contains lowercase characters, enclose the name in double quotes, for example `session:role:"Data Analyst"`. A quoted name must match the stored role name exactly, including case. The [QUOTED\_IDENTIFIERS\_IGNORE\_CASE](/sql-reference/parameters#label-quoted-identifiers-ignore-case) parameter doesn’t apply to the role name in `scope`. |
| `authorization_details` | Recommended. A JSON array that contains one Restricted Session Scope entry. For details, see [Set the privilege ceiling](#label-oauth-token-exchange-privilege-ceiling). |
| `act` | Recommended. A JSON object that identifies the acting party. For details, see [Identify the acting agent](#label-oauth-token-exchange-acting-agent). |

Expand

Show lessSee more

`authorization_details` and `act` are optional in the protocol. If you omit them, the issued token
has the user’s full access in the selected role, and Snowflake doesn’t attribute it to an agent.
Make sure every exchange that your application performs for an agent includes both parameters.

Send each parameter once. Snowflake rejects a request that repeats a parameter.

### Supported subject tokens

| `subject_token_type` | Subject token |
| --- | --- |
| `urn:ietf:params:oauth:token-type:access_token` | An access token from a [Snowflake OAuth](/user-guide/oauth-snowflake-overview) or [External OAuth](/user-guide/oauth-ext-overview) security integration. |
| `programmatic_access_token` | A [programmatic access token](/user-guide/programmatic-access-tokens) for the user. |
| `urn:snowflake:token-type:wif` | A [workload identity federation](/user-guide/workload-identity-federation) credential. |

Expand

Show lessSee more

You can’t use a token that token exchange issued as a subject token, even if it has no Restricted
Session Scope or acting agent. So an agent can’t widen its scope or pass its access on.

## Set the privilege ceiling

The `authorization_details` parameter carries one entry of type `snowflake-rss.v1`. Its `rss` field
names the Restricted Session Scope that Snowflake attaches to the token:

Copy code

```
[{"type": "snowflake-rss.v1", "rss": "<scope>"}]
```

Snowflake honors only the `type` and `rss` fields. It ignores other fields, including the RFC 9396
common fields `locations`, `actions`, `datatypes`, `identifier`, and `privileges`. These fields
don’t restrict access.

An RSS is a ceiling, not a grant. In a session created from the token, an action succeeds only if
the user’s roles allow it *and* the RSS allows it. A scope never gives the agent a privilege the user
doesn’t already have. For example, suppose a stored procedure is granted to `PUBLIC`. Under
`SNOWFLAKE$DATA_READ`, the agent still can’t call it, because that scope doesn’t allow procedure
usage.

Use the following table to choose how to specify the scope:

| If you want to… | Set `rss` to… |
| --- | --- |
| Use a Snowflake-defined scope | A [predefined scope](/user-guide/restricted-session-scope#label-agent-rss-predefined-scope-yaml) name: `SNOWFLAKE$DATA_READ`, `SNOWFLAKE$DATA_READ_PROGRAM_USAGE`, or `SNOWFLAKE$DATA_READ_WITH_AI`. |
| Reuse a scope that an administrator manages centrally | The fully qualified three-part name of a [restricted session scope object](/user-guide/restricted-session-scope#label-agent-rss-create-object), for example `GOVERNANCE.SCOPES.INVOICE_AGENT`. |
| Define a scope for a single request | An inline RSS definition in YAML, using the same [syntax](/user-guide/restricted-session-scope#label-agent-rss-yaml-structure) as a restricted session scope object. The definition must span more than one line. |

Expand

Show lessSee more

For example, the following inline definition blocks the `SYSADMIN` role in the agent’s sessions:

Copy code

```
[{"type": "snowflake-rss.v1", "rss": "role_scopes:\n  blocked_roles:\n    - SYSADMIN\n"}]
```

Snowflake validates the scope when it issues the token and rejects the request if the scope is
invalid. Inline definitions can have up to 8,192 characters. If the RSS blocks the role that you
request in `scope`, Snowflake rejects either the exchange or the first session created from the
token. Either way, the agent can’t use the blocked role.

Token exchange doesn’t require an
[admin-managed RSS](/user-guide/restricted-session-scope#label-agent-rss-admin). Delegation and
agent attribution work the same way whether or not a session policy sets
`AGENT_RESTRICTED_SESSION_SCOPE`. The RSS in `authorization_details` is the ceiling that your
application sets for each token. If a session policy also sets an admin-managed RSS and the session
is [agentic](/user-guide/oauth-token-exchange#label-oauth-token-exchange-agentic), Snowflake enforces the intersection of both
ceilings.

### Managing named scopes

A token is bound to the restricted session scope object itself, not to a copy of its definition.
Changes that you make with [ALTER RESTRICTED SESSION SCOPE](/sql-reference/sql/alter-restricted-session-scope), including changes
that loosen the scope, apply right away to every token and session already issued from it. This has
two consequences:

- Limit ownership of restricted session scope objects to trusted administrators. Whoever can alter
  the object controls the ceiling for every agent token bound to it.
- To revoke every token bound to an object at once, alter the object so that it allows no
  privileges.

### What the ceiling doesn’t cover

An RSS limits which privileges a session can use. It doesn’t limit how much data the agent reads
within those privileges, and it doesn’t stop the agent from sending results elsewhere.
`SNOWFLAKE$DATA_READ` allows reading every object that the session’s role can read. To limit an
agent to specific databases, schemas, or objects, use a named or inline RSS.

## Identify the acting agent

The `act` parameter is a JSON object that names who is acting for the user:

Copy code

```
{"sub": "invoice-reconciliation-agent", "type": "agent"}
```

| Field | Description |
| --- | --- |
| `sub` | An identifier for the acting party. Use a stable value that you can trace back to a specific agent or deployment. The value appears in access history, so don’t put secrets or personal data in it. |
| `type` | `agent`, `service`, or `person`. Values are case-insensitive. `agent` marks the session as agentic. `service` and `person` don’t, but the session can still be agentic for [another reason](/user-guide/oauth-token-exchange#label-oauth-token-exchange-agentic). For details, see [Audit agent activity](#label-oauth-token-exchange-audit). |

Expand

Show lessSee more

`act` accepts only the `sub` and `type` fields, and both must be strings. Snowflake rejects nested
`act` objects. Each token records one acting party, the agent directly in front of the user.

Snowflake records the `act` value exactly as your application supplies it and doesn’t verify it. If
you omit `act`, or set `type` to a value other than `agent`, the token’s `scope` and RSS still
apply, but the session isn’t attributed to an agent.

The session is still agent-active if anything else makes it agentic, such as:

- The user is a [`SERVICE_AGENT`](/user-guide/admin-user-management#label-user-management-types)
  user.
- The subject token was issued through a security integration with
  [`IS_AGENTIC = TRUE`](/user-guide/oauth-custom#configuring-agent-sessions).

Otherwise, controls that apply only when an agent is active don’t apply to that session. These
include an [admin-managed RSS](/user-guide/restricted-session-scope#label-agent-rss-admin) on a
session policy and agent-aware masking policies. Use `act` for
attribution and auditing, not as an authentication factor or an access control. Access control for
the agent comes from the subject token, `scope`, and the RSS. Make sure that only trusted
application code can set `act`.

## Use the delegated token

Use the issued token as an OAuth access token for Snowflake. Sessions created from the token:

- Run as the user who owns the subject token, with the role selected in `scope`.
- Are bound by the RSS from `authorization_details`, on top of the user’s normal privileges.
- Are attributed to the agent named in `act`.

The delegated token is a bearer token: anyone who has it can use it until it expires. Give it only
to the agent process that needs it, keep it in memory, and don’t log it. To limit where the token
can be used, apply a [network policy](/user-guide/network-policies) to the user.

### Expiration and revocation

By default, the token expires one hour after Snowflake issues it. The response doesn’t include
`expires_in`. Read the expiration time from the token’s `exp` claim, or assume one hour minus clock
skew. Snowflake doesn’t issue a refresh token. When the token expires, your application exchanges
the user’s credential again, which re-checks the user’s role grants and the current scope.

There’s no endpoint to revoke a single delegated token. What revokes it depends on the subject
token:

| If the subject token is… | Revoke delegated tokens by… |
| --- | --- |
| A programmatic access token | Disabling or removing the programmatic access token. Delegated tokens issued from it stop working. |
| An OAuth access token or a workload identity credential | Waiting for them to expire. Revoking the subject credential doesn’t invalidate delegated tokens that were already issued. |

Expand

Show lessSee more

To cut off all of a user’s delegated tokens right away, disable the user. For tokens bound to a
named restricted session scope, you can also alter the object so that it allows no privileges.

## Audit agent activity

Snowflake stores the `act` value on every session created from the delegated token. Agentic
sessions appear in the audit views:

| Source | What it shows |
| --- | --- |
| [QUERY\_HISTORY](/sql-reference/account-usage/query_history): `agent_type` | `EXTERNAL_AGENT` for queries run in agentic sessions. The `user_name` column shows the user the agent acted for. |
| [ACCESS\_HISTORY](/sql-reference/account-usage/access_history): `agents_info` | The agent type and the `act.sub` value for each query that accessed data, together with the objects and columns accessed. |
| [`SYS_CONTEXT('SNOWFLAKE$CURRENT', 'AGENT_TYPE')`](/sql-reference/functions/sys_context_snowflake_current) | The agent type for the current session. |

Expand

Show lessSee more

An `act` with `type` set to `service` or `person` doesn’t by itself make queries appear as agent
activity in query history or access history. They still appear as agent activity if the session is
[agentic for another reason](/user-guide/oauth-token-exchange#label-oauth-token-exchange-agentic).

Because `act` is self-asserted, treat these records as claims made by your application, not as proof
of which software ran. For the same reason, don’t use `AGENT_TYPE` as the only control in a masking
policy, a row access policy, or another access decision. Unless the session is
[agentic for another reason](/user-guide/oauth-token-exchange#label-oauth-token-exchange-agentic), a caller that omits `act`, or sets
a different `type`, gets a session with no agent type, and agent-aware policies don’t apply to it.
Enforce limits on the agent with the RSS in `authorization_details` instead, because it applies to
every session created from the token.

Each delegated token records one acting party. To trace a request through several layers of agents
in your own system, put a value in `act.sub` that your application can map back to that chain.

## Limitations

- `authorization_details` accepts exactly one `snowflake-rss.v1` entry, and the response doesn’t
  echo it back.
- The `actor_token`, `actor_token_type`, `requested_token_type`, and `audience` parameters from
  RFC 8693 aren’t supported.
- Nested `act` claims and multi-hop delegation chains aren’t supported.
- Session tokens, tokens that token exchange issued, and tokens that carry a Restricted Session
  Scope can’t be used as subject tokens.
- The response body is the access token itself. It doesn’t include the `issued_token_type`,
  `token_type`, or `expires_in` fields.
- The token’s lifetime doesn’t depend on the subject token’s remaining lifetime.
- Error responses don’t use the error codes defined in RFC 6749 section 5.2. If a request is
  invalid, Snowflake returns HTTP 400. If the subject token or the requested role isn’t valid for
  the user, Snowflake returns HTTP 401. The response doesn’t always explain why the request was
  rejected.

## Related topics

- [Agent identity](/user-guide/agent-identity): How Snowflake identifies, audits, and governs AI agents
- [Restricted Session Scope for agents](/user-guide/restricted-session-scope): Define privilege ceilings for sessions in which an agent
  is active
- [External OAuth overview](/user-guide/oauth-ext-overview): Use an external identity provider’s access tokens as subject
  tokens
- [Snowflake OAuth overview](/user-guide/oauth-snowflake-overview): Issue Snowflake OAuth access tokens to applications
- [Using programmatic access tokens for authentication](/user-guide/programmatic-access-tokens): Create and manage tokens for users
- [Workload identity federation](/user-guide/workload-identity-federation): Authenticate workloads without long-lived secrets
- [Controlling network traffic with network policies](/user-guide/network-policies): Restrict where a user’s tokens can be used
- [Access History](/user-guide/access-history): Audit which objects and columns were accessed, and by which agent
