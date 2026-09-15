# Jul 27, 2026: New agent\_type column in QUERY\_HISTORY views

The QUERY\_HISTORY views and table functions now include a new `agent_type` column that identifies
the type of agent that directly invoked a query. This column helps you audit and monitor
agent-initiated queries across your account.

Possible values for the `agent_type` column:

- `CORTEX_AGENT`: A persistent, named [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents).
- `CORTEX_LITE_AGENT`: A stateless, on-demand lite agent invoked through the
  [REST API](/developer-guide/snowflake-rest-api/cortex-lite-agent/cortex-lite-agent-introduction) or via a Snowflake CoCo client.
- `EXTERNAL_AGENT`: A third-party agent using a
  [SERVICE\_AGENT](/user-guide/admin-user-management#label-user-management-types) user type or a
  [custom OAuth integration](/user-guide/oauth-custom#configuring-agent-sessions) configured with
  `IS_AGENTIC = TRUE`.

The column is NULL if the query wasn’t invoked by an agent.

This column is being gradually rolled out to all accounts over approximately one week starting
July 27, 2026.

For the full column description, see
[agent\_type](/sql-reference/account-usage/query_history#columns).

This column is available in the following views and functions:

- [QUERY\_HISTORY view (Account Usage)](/sql-reference/account-usage/query_history)
- [QUERY\_HISTORY view (Organization Usage)](/sql-reference/organization-usage/query_history)
- [QUERY\_HISTORY table function (Information Schema)](/sql-reference/functions/query_history)
