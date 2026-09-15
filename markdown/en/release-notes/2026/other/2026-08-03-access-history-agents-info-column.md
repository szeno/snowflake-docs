# Aug 3, 2026: ACCESS\_HISTORY view: New agents\_info column

Starting with release 10.27, the
[ACCESS\_HISTORY view (Account Usage)](/sql-reference/account-usage/access_history) and
[ACCESS\_HISTORY view (Organization Usage)](/sql-reference/organization-usage/access_history)
include an `agents_info` column that provides detailed information about agents that accessed
data on behalf of a user.

The `agents_info` column is an ordered JSON array of invoking agents, from the nearest agent to
the top-level agent. Each element in the array includes:

- `agentType`: The type of agent (`CORTEX_AGENT`, `CORTEX_LITE_AGENT`, or `EXTERNAL_AGENT`).
- `agentId`: The identifier for the specific agent, or NULL for `EXTERNAL_AGENT`.
- `agentName`: The fully qualified name of the Cortex Agent, or NULL for lite agents and external agents.

This column is NULL when no agent is involved in the object access.

This column is being gradually rolled out to all accounts over approximately one week.

For more information, see
[ACCESS\_HISTORY view (Account Usage)](/sql-reference/account-usage/access_history#columns).
