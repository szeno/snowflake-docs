# AI Governance

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

AI Governance is an account-wide Snowsight page that lets you govern and audit AI usage in your account. It gives platform
administrators and data governance teams a single place to oversee both [Cortex Code](/user-guide/cortex-code/cortex-code)
and every [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents) in the account. Instead of reviewing users or agents one
at a time, you get an aggregate view of AI usage metrics, who is accessing what data through your agents, and what has
changed about how your agents are configured.

Use AI Governance to answer account-level questions such as the following:

- How many users are using Cortex Code, from which clients, and with which models?
- Which agents are most used, and by whom?
- Which agents touch sensitive data, and which agents lack governance tags?
- Who changed an agent’s configuration, and when?

AI Governance complements Cortex Agents’ own [monitoring](/user-guide/snowflake-cortex/cortex-agents-monitor) surface. Use
Cortex Agent monitoring to debug a single agent’s live conversations and execution traces. Use AI Governance to govern and
audit AI usage across the whole account.

## Access AI Governance

In Snowsight, select **Governance & security** from the navigation menu, then select **AI governance**. The page requires an
active warehouse: if none is selected, you’re prompted to choose or resume one before any data loads.

AI Governance has two tabs:

- **Dashboard**: account-wide AI usage metrics for Cortex Code and Cortex Agents.
- **Agents**: an audit of agent activity and data exposure, plus a changelog of governance-relevant changes to your agents.

## Dashboard

The dashboard summarizes AI usage across your account. A **Time window** control at the top of the page rolls every card up
over the last 7, 30, or 90 days.

### Cortex Code

The **CoCo** section summarizes Cortex Code usage in your account:

| Card | What it shows |
| --- | --- |
| Active users | The number of distinct users who used Cortex Code in the selected time window, with the change from the prior window. |
| Invocations | The total number of Cortex Code invocations in the selected time window, with the change from the prior window. |
| Billed credits | The credits billed for Cortex Code usage in the selected time window. |
| Usage over time | A trend chart of Cortex Code invocations or tokens. |
| Most-used models | The models that Cortex Code uses most, by invocations or tokens. |
| Usage by client | Invocations or tokens broken down by client: Snowsight UI, desktop app, CLI, and other clients. |

Expand

Show lessSee more

### Cortex Agents

The **Cortex Agents** section summarizes agent usage in your account. An **Agent** filter narrows every card in this section to
one or more specific agents. Leave it empty to include all agents.

| Card | What it shows |
| --- | --- |
| Total agents | The number of distinct agents in the account (or in your current agent selection). |
| Active users | The number of distinct users who invoked an agent in the selected time window. |
| Invocations | The total number of agent invocations in the selected time window. |
| Agents missing tags | Agents that don’t have a governance tag applied, so you can find and tag them. |
| Most-used agents | Agents ranked by invocation volume. |
| Most-used models | The orchestration models your agents use most. |
| Agents accessing sensitive data | Agents whose tool calls touch classified or sensitive data. Selecting an agent here opens the **Agents** tab scoped to that agent. |
| Invocations over time | A trend chart of invocations or tokens, viewable in total or broken down by agent or by model. |
| Top users | The users who invoke agents most. |

Expand

Show lessSee more

## Agents

The **Agents** tab lets you audit what your agents are doing and what has changed about how they are configured. It has two
views, switched with a toggle at the top of the tab.

### Activity

The Activity view lists every agent in the account alongside a data-exposure summary: the objects it has accessed, how many of
those objects are sensitive, and rollups of invocations, users, and last invocation. Use the search box, the agent filter, the
time filter, and the column picker to narrow the table to what you need, and select a row to open a drawer with the full
exposure detail for that agent.

### Changelog

The Changelog view lists governance-relevant changes to your agents, such as creating, altering, or replacing an agent,
sourced from [Access History](/user-guide/access-history). For each change, the view shows the agent, its location, when it was
modified, who modified it, the operation, and details of the change. Filter by agent, operation, user, or time, or search
across all of them.

## Access control

AI Governance draws its data from account-level usage and access views. You don’t need privileges on individual agents to
view it. The `ACCOUNTADMIN` role, or any role that meets the following requirements, can view the dashboard:

| Requirement | What it’s needed for |
| --- | --- |
| An active warehouse | Every tab. AI Governance runs queries to render, the same as any other Snowsight page. |
| `IMPORTED PRIVILEGES` on the `SNOWFLAKE` database | Every card and table that reads account-level usage and access data. This is the broadest option and replaces the two database roles below. |
| The `SNOWFLAKE.USAGE_VIEWER` [database role](/sql-reference/account-usage#label-enabling-usage-for-other-roles) | Cortex Code and Cortex Agent usage metrics on the **Dashboard** tab. |
| The `SNOWFLAKE.GOVERNANCE_VIEWER` [database role](/sql-reference/account-usage#label-enabling-usage-for-other-roles) | Agent data-exposure metrics and the agent changelog on the **Agents** tab, which read [`ACCESS_HISTORY`](/sql-reference/account-usage/access_history). See [Access History](/user-guide/access-history) for details. |
| [Object tagging](/user-guide/object-tagging/introduction) and classification already applied to the data your agents use | The **Agents missing tags** and **Agents accessing sensitive data** cards. AI Governance doesn’t apply tags or classify data itself. |

Expand

Show lessSee more

If your role can’t read one of these sources, the affected card or table reports an error in place of its data. The rest of
the page still loads, so a missing privilege limits what you see rather than blocking the page.

## Cost

Rendering the page requires an active warehouse. The queries that populate each tab run on the warehouse you select, so that
compute is billed as normal warehouse usage.

## Considerations

Note the following while this feature is in preview:

- **Data refreshes at least daily.** Dashboard and agent audit metrics are drawn from precomputed views that refresh at least daily, so they aren’t real time. A recent invocation might not appear immediately on the dashboard.
- **Time windows are day-aligned.** The Dashboard’s 7-day, 30-day, and 90-day windows compare full calendar days, not a
  rolling 24-hour period, so figures near the edge of a window can shift slightly compared to a live query.
- **Agent invocation counts are deduplicated.** Agent invocation counts reflect distinct invocation roots, matching what
  Cortex Agents reports elsewhere in the product. This can be lower than a raw row count if a single invocation produced
  multiple underlying events.
- **Only Cortex Code and Cortex Agents are covered.** Other AI workloads, such as custom applications built on Snowflake
  Cortex functions, aren’t included.

## Related content

- [Cortex Code](/user-guide/cortex-code/cortex-code)
- [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents)
- [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor)
- [Object Tagging](/user-guide/object-tagging/introduction)
- [Access History](/user-guide/access-history)
