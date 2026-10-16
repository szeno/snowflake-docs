# Snowflake CoWork: Dashboard data access enabled by default for agents

Snowflake CoWork agents can expand their data access to include a dashboard’s data sources when
answering conversational questions about that dashboard. A new property, `dashboard_data_access`,
controls whether an agent may use the data sources declared on a dashboard in addition to its own
configured data access. The property is set on the agent or profile, not on individual dashboards.

Important

This change isn’t part of a behavior change bundle. It is expected to begin rolling out gradually on
**October 26, 2026**. Dates are subject to change.

## Behavior change

Before the change:
:   There is no `dashboard_data_access` property on agents or profiles. When users ask questions about a
    dashboard, the agent can draw only on its own configured data access. A table that belongs to the
    dashboard but not to the agent cannot be queried, so the agent answers from what it can reach and
    explains what it cannot.

After the change:
:   The `dashboard_data_access` property is available on agents and profiles, and resolves to `TRUE`
    by default for all accounts. An agent whose specification does not include the property behaves as
    `TRUE`, so [DESCRIBE AGENT](/sql-reference/sql/desc-agent) does not show the property for an agent that has never
    set it.

    With the property set to `TRUE`, the dashboard’s underlying tables are added to the data the agent
    is already authorized to use, for that dashboard conversation. Users can ask questions about the
    data behind the dashboard they are viewing, within what their own role may read. The added access is
    scoped to those tables rather than to the columns or metrics shown in the dashboard’s tiles, so
    other columns of the same tables are reachable as well.

    With the property set to `FALSE`, no dashboard tables are added and the agent’s own configured data
    access is unchanged. A question that needs a dashboard table the agent is not otherwise authorized
    for cannot be answered from that table. Consider setting the property to `FALSE` for agents that
    operate in sensitive data environments.

## What doesn’t change

- The property applies only to dashboard conversations. If your users do not ask agents about
  dashboards, this change has no observable effect.
- An agent runs each query with the caller’s rights, so a user still sees only the data their own
  role is authorized to read. What this change widens is which tables the agent will draw on to
  answer a dashboard question, not whose data it can reach.
- Dashboard publishing continues to use role-based access. Users with the appropriate role can view
  a published dashboard and, if enabled, ask conversational questions using whichever profile or
  agent is assigned to them.

## Impact and preparation

No action is required. The property takes effect automatically, and agents answer dashboard
questions from the dashboard’s data sources as well as their own.

To stop an agent from using dashboard data sources, set the property to `FALSE` in that agent’s
specification. You can do this for each agent or profile independently:

Copy code

```
ALTER AGENT my_support_agent
  MODIFY LIVE VERSION SET SPECIFICATION =
  $$
  orchestration:
    capabilities:
      dashboard_data_access: false
  $$;
```

Include the rest of the agent’s specification in the statement. A new specification completely
replaces the existing one, and fields that are not included are removed. See
[ALTER AGENT](/sql-reference/sql/alter-agent).

Where the **Dashboard data** toggle is available in Snowsight, on the agent’s **Build** tab, it
sets the same property for that agent.

## See also

- [Overview of Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork)
- [ALTER AGENT](/sql-reference/sql/alter-agent)
- [DESCRIBE AGENT](/sql-reference/sql/desc-agent)
- [Behavior change policy](/release-notes/behavior-change-policy)
- [Unbundled behavior changes](/release-notes/bcr-bundles/un-bundled/unbundled-behavior-changes)

Ref: 2468
