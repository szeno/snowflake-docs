# Agent identity

Agent identity lets Snowflake recognize when an AI agent is active in a session, so you can govern
agent-driven access separately from ordinary human or service access.

Enterprise AI agents can be Snowflake-native (for example, Cortex Agents) or third-party (for
example, agents that connect through OAuth or their own service credentials). In many workflows the
session is opened by an agent, but authority and accountability still belong to a person. Agent
identity closes that gap so you can answer who authorized the access, which agent carried it out,
and whether the access was appropriate for the task.

## Overview

Snowflake’s agent identity capabilities support four governance functions:

| Function | What you can do |
| --- | --- |
| Identify | Detect agentic sessions and distinguish them from ordinary human sessions |
| Audit | Attribute queries and object access to an agent type, and to the user when the agent acts on a user’s behalf |
| Govern | Restrict what sensitive data an agent can see, even when the user’s role would allow more |
| Control | Limit what an agent can do in a session to a subset of the privileges the user’s roles already allow |

Expand

Show lessSee more

Two modes of agency matter for how you configure identity:

- **Delegated agents** act on behalf of a user. The session belongs to the user; Snowflake marks it
  agent-active so policies and audit views can treat the traffic as agentic.
- **Autonomous agents** act under their own identity and authorization. Create a
  [SERVICE\_AGENT](/user-guide/admin-user-management#label-user-management-types) user and authenticate
  with [workload identity federation](/user-guide/workload-identity-federation) or another supported
  non-interactive method. Every session for that user is agent-active.

## Identify agents

Snowflake marks a session as agentic based on the entry point and authentication method. When a
session is agent-active, the
[IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated) context function returns `TRUE`.

The following table lists the supported entry points:

| Entry point | Condition |
| --- | --- |
| Snowflake-native agents | A user acts through a Snowflake agent such as a [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents) or a [Cortex lite agent](/developer-guide/snowflake-rest-api/cortex-lite-agent/cortex-lite-agent-introduction), including CoCo clients and Snowflake CoWork |
| Snowflake-managed MCP server | Sessions through a [Snowflake-managed MCP server](/user-guide/snowflake-cortex/cortex-agents-mcp) are marked agentic automatically |
| Snowflake OAuth | A custom OAuth [security integration](/user-guide/oauth-custom#configuring-agent-sessions) is configured with `IS_AGENTIC = TRUE` |
| External OAuth | An External OAuth [security integration](/user-guide/oauth-ext-custom#configuring-agent-sessions) is configured with `IS_AGENTIC = TRUE` |
| `SERVICE_AGENT` user type | Sessions opened by a user created with type [SERVICE\_AGENT](/user-guide/admin-user-management#label-user-management-types) |

Expand

Show lessSee more

### Choose an identification path

Use the following table to choose how to identify the agent:

| If the agent… | Configure… |
| --- | --- |
| Runs inside Snowflake AI products (Cortex Agents, CoCo, CoWork, managed MCP) | Nothing extra. Snowflake marks the session agent-active automatically. |
| Needs its own Snowflake identity and privileges (autonomous) | A [`SERVICE_AGENT`](/user-guide/admin-user-management#label-user-management-types) user, typically with [workload identity federation](/user-guide/workload-identity-federation) (including SPIFFE and SPIRE), [key-pair authentication](/user-guide/key-pair-auth), or [programmatic access tokens](/user-guide/programmatic-access-tokens) |
| Acts on behalf of end users through a custom Snowflake OAuth client (delegated) | `IS_AGENTIC = TRUE` on the [custom OAuth integration](/user-guide/oauth-custom#configuring-agent-sessions). Snowflake doesn’t treat sessions that use other delegated methods, such as programmatic access tokens alone, as agentic unless you also use a supported agent identity path. |
| Acts on behalf of end users through an External OAuth client (delegated) | `IS_AGENTIC = TRUE` on the [External OAuth integration](/user-guide/oauth-ext-custom#configuring-agent-sessions). Snowflake doesn’t treat sessions that use other delegated methods, such as programmatic access tokens alone, as agentic unless you also use a supported agent identity path. |

Expand

Show lessSee more

## Audit agent activity

After Snowflake identifies an agentic session, it carries that context into existing audit views so
you can review agent activity.

### Query history: `agent_type`

The `agent_type` column in QUERY\_HISTORY identifies the agent that directly invoked a query:

| Value | Meaning |
| --- | --- |
| `CORTEX_AGENT` | A persistent, named Cortex Agent |
| `CORTEX_LITE_AGENT` | A Cortex lite agent (REST API or CoCo client) |
| `EXTERNAL_AGENT` | An external agent using `SERVICE_AGENT` or an OAuth integration with `IS_AGENTIC = TRUE` |

Expand

Show lessSee more

The column is NULL when no agent invoked the query. For details, see
[QUERY\_HISTORY view (Account Usage)](/sql-reference/account-usage/query_history#columns) and
[QUERY\_HISTORY view (Organization Usage)](/sql-reference/organization-usage/query_history).

### Access history: `agents_info`

The `agents_info` column in ACCESS\_HISTORY provides ordered agent details for object access, from
the nearest agent to the top-level agent. For example, when a Cortex Agent invokes tools that run
queries, the array can list that agent first, then any higher-level agent in the call chain. Each
element can include `agentType`, `agentId`, and `agentName`, depending on the agent. The column is
NULL when no agent was involved.

For details, see the
[ACCESS\_HISTORY view (Account Usage)](/sql-reference/account-usage/access_history#columns).

Together, these columns help you reconstruct the causal chain that compliance teams often need: a
user invoked an agent, specific queries followed, and specific objects were accessed.

## Govern sensitive data access

Identifying an agentic session lets you enforce data protection policies that behave differently when
an agent is active. Call
[IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated) in a policy body so regulated or
high-risk data isn’t returned to an agent, even when the user’s role would otherwise allow it.

A common pattern is a masking policy that hides a sensitive column whenever an agent is active:

Copy code

```
CREATE OR REPLACE MASKING POLICY email_agent_mask AS (val STRING) RETURNS STRING ->
  CASE
    WHEN SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')::BOOLEAN = TRUE THEN '********'
    WHEN CURRENT_ROLE() IN ('ANALYST') THEN val
    ELSE '********'
  END;
```

You can use the same check in row access, projection, aggregation, and join policies. For guidance
and examples, see:

- [Data protection policies for agentic interactions](/user-guide/data-protection-policies-snowsight#label-data-protection-policies-agentic)
- [Masking policies](/user-guide/security-column-intro#label-security-column-agent-active)
- [Tag-based masking policies](/user-guide/tag-based-policies#label-tag-based-policies-agent-active)
- [Row access policies](/user-guide/security-row-intro#label-security-row-agent-active)
- [Projection policies](/user-guide/projection-policies#label-projection-policy-agent-active)
- [Aggregation policies](/user-guide/aggregation-policies#label-agg-policy-agent-active)
- [Join policies](/user-guide/join-policies#label-join-policy-agent-active)

## Control agent access in a user session

Identifying an agentic session also lets you limit what the agent can do to a subset of the
privileges the user’s roles already allow. A
[Restricted Session Scope](/user-guide/restricted-session-scope) (RSS) is a privilege ceiling. It
intersects with the user privileges and never grants privileges the user doesn’t already have.

Set `AGENT_RESTRICTED_SESSION_SCOPE` on a session policy, then attach that policy to the account or
to users. The ceiling applies only when an agent is active
([IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated) returns `TRUE`).

Typical ways to use RSS include:

- Apply a read-only ceiling for agents that can still use AI-related objects, such as
  `SNOWFLAKE$DATA_READ_WITH_AI`. See
  [Account-wide read-only for agents](/user-guide/restricted-session-scope#label-agent-rss-example-readonly).
- Allow writes only in a sandbox and in each user’s personal database, while production stays
  read-only. See
  [Production read-only, write allowed in a sandbox and user’s personal database](/user-guide/restricted-session-scope#label-agent-rss-example-sandbox-write).
- Block elevated roles such as ACCOUNTADMIN, SYSADMIN, and SECURITYADMIN while an agent is active.
  See
  [Block privileged roles when an agent is active](/user-guide/restricted-session-scope#label-agent-rss-example-block-roles).
- Allow data work (read, sandbox write, program usage) while leaving grant and object management
  denied. See
  [Allow data work, block grant and object management](/user-guide/restricted-session-scope#label-agent-rss-example-data-ops).
- Limit agents to databases approved for AI use. See
  [Restrict access to approved databases](/user-guide/restricted-session-scope#label-agent-rss-example-approved-dbs).

RSS and agent-aware data protection policies are complementary. RSS controls which databases and
operations the agent can reach; masking and related policies control which column values are
visible within that scope.

For YAML structure, predefined scopes, and the full examples, see
[Restricted Session Scope for agents](/user-guide/restricted-session-scope).

## Related topics

- [IS\_AGENT\_ACTIVATED (SYS\_CONTEXT function)](/sql-reference/functions/is_agent_activated): Detect whether an agent is active in the current
  execution context
- [Restricted Session Scope for agents](/user-guide/restricted-session-scope): Set a privilege ceiling for agent-active sessions
- [Types of users](/user-guide/admin-user-management#label-user-management-types): `SERVICE_AGENT` and other user
  types
- [Snowflake OAuth](/user-guide/oauth-custom#configuring-agent-sessions): Mark custom OAuth clients
  as agentic
- [External OAuth](/user-guide/oauth-ext-custom#configuring-agent-sessions): Mark External OAuth
  clients as agentic
- [Workload identity federation](/user-guide/workload-identity-federation): Authenticate `SERVICE_AGENT` workloads with workload
  identity
- [Data protection policies for agentic interactions](/user-guide/data-protection-policies-snowsight#label-data-protection-policies-agentic): Use
  agent identity in data protection policies
- [QUERY\_HISTORY view](/sql-reference/account-usage/query_history): `agent_type` column for query attribution
- [ACCESS\_HISTORY view](/sql-reference/account-usage/access_history): `agents_info` column for object-access
  attribution
