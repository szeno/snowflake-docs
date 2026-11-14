# Monitor per-user quota spending

Quota admins can review spending for every user in a quota with SQL or in Snowsight. Individual
users can check their own usage against each quota that covers them.

## View user spending

To return finalized usage records by user and resource within a date range, call
`GET_SPENDING_DETAILS_BY_USERS`. A role granted the quota’s `ADMIN` or `VIEWER` instance role can
call this method:

Copy code

```
CALL my_quota!GET_SPENDING_DETAILS_BY_USERS('2026-04-01', '2026-04-30');
```

The method returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `USER_ID` | `NUMBER` | User ID. |
| `USER_NAME` | `VARCHAR` | Name of the user. |
| `SERVICE_TYPE` | `VARCHAR` | Resource type (for example, `WAREHOUSE_METERING` or `CORTEX_AGENTS`). |
| `ENTITY_TYPE` | `VARCHAR` | Type of the entity. |
| `ENTITY_NAME` | `VARCHAR` | Name of the entity, such as the warehouse name or AI function name. |
| `CREDITS_SPEND` | `FLOAT` | Credits consumed. |
| `USAGE_TIMESTAMP` | `TIMESTAMP_TZ(9)` | Usage hour of the underlying spend. |

Expand

Show lessSee more

Note

The date range must fall in either the current month or the prior calendar month for data to
be returned. Dates before the prior month don’t return any results. For older per-user AI usage,
query the [USER\_AI\_USAGE\_HISTORY](/sql-reference/account-usage/user_ai_usage_history) view.

## Check your quota usage

Any user can check their quotas by calling the
[MY\_BUDGET\_SUMMARY (SNOWFLAKE.LOCAL)](/sql-reference/functions/my_budget_summary-snowflake-local) table function. The function
returns only the calling user’s information, so users don’t need privileges on the quota or on the
`ACCOUNT_USAGE` schema, and administrators don’t need to grant any additional access. Users can run
the query from any SQL client, including Snowsight worksheets:

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.LOCAL.MY_BUDGET_SUMMARY());
```

The function returns one row for each of the user’s quotas and each cycle that has a per-user limit. Each
row shows the user’s usage, the per-user limit, the percentage consumed, the start and end of the
current cycle, whether the quota blocks users at the limit, and whether the user is currently blocked.

## Monitor quotas in Snowsight

Snowsight provides three levels of monitoring: a list of all quotas in your account, a deep dive
into a single quota, and a deep dive into an individual user’s spending.

To open the list, sign in to Snowsight. In the navigation menu, select **Admin** » **Cost management**,
then select the **Budgets** tab.

### Quotas list

The **Budgets** tab lists every quota and budget in your account. Quotas are tracked alongside
budgets so that you can govern all spend controls from one place.
This view includes the following elements:

- **Summary cards**: **Total budgets** (spend controls tracking spend), **Over limit**, and **No
  limit configured**. Each card shows the split between custom budgets and quotas.
- **Filter tabs**: Switch between **All budgets**, **Custom budgets**, and **Quotas**, and filter
  the list by **Type** and **Status**.
- **List columns**: The columns depend on the tab. On **All budgets**, the list shows **Name**,
  **Type**, **Status**, **Spend (credits)**, and **Limit (credits)**, with per-cycle spend and
  limits for quota rows. On **Quotas**, the list shows **Name**, **Quota status**, **Monthly
  per-user limit**, **Weekly per-user limit**, **Daily per-user limit**, **Users in quota**,
  **Enforcement**, and **Users blocked**. A cycle with no limit set reads `Not configured`.

Select a quota’s name to open the quota deep-dive view.

### Quota deep-dive

The quota deep-dive view summarizes spending and enforcement across all users in scope for a
single quota.
This view includes the following elements:

- **Avg monthly utilization**, **This week’s avg utilization**, and **Today’s avg utilization**:
  Average utilization across in-scope users for each cycle, measured against the per-user limit for
  that cycle.
- **User status**: A breakdown of in-scope users by status: **On track**, **Over monthly**, **Over
  weekly**, **Over daily**, and **Over multiple**.
- **Enforcement breakdown**: A breakdown of users with an enforcement action applied, such as the
  number of users blocked against a per-user limit.
- **Top user spend over time**: A graph of the highest-spending users over the current cycle,
  plotted against the per-user limit.
- **Quota details**: The quota’s configuration, including:
  - **Per-user limit**: The limit configured for each cycle (for example,
    `10,000 credits / month` and `5,000 credits / day`).
  - **Monthly avg user spend** and **Monthly highest user spend** across in-scope users.
  - **Quota scope**: The users in scope (all users in the account, or the tag, role, and username
    filters applied) and the monitored domains, such as AI functions, Snowflake CoCo, Cortex Agents, Snowflake CoWork, and the AI Gateway.
  - **Notifications**: The configured notification thresholds.
- **User table**: A searchable, filterable list of every user in scope. For each user, the table
  shows **Enforcement**, utilization and spend for each configured cycle (**Monthly utilization**
  and **Monthly spend**, **Weekly utilization** and **Weekly spend**, **Today’s utilization** and
  **Today’s spend**), and **Matched tags**.

Select a user in the table to open the user deep-dive view.

### User deep-dive

The user deep-dive view shows spending detail for a single user within a quota.
This view includes the following elements:

- **Monthly utilization**: The user’s spend against their monthly limit.
- **Weekly utilization**: The user’s spend against their weekly limit.
- **Today’s utilization**: The user’s spend so far today against their daily limit.
- **Spend by type**: A breakdown of the user’s spend by monitored domain, such as AI functions.
- **User details**: The **Per-user limit** for each cycle, the user’s **Current spend**, and their
  **Avg weekly spend** and **Avg daily spend**.
- **Matched tags**: The tags on the user that matched the quota’s tag scope.
- **Spend by day**: A graph and table of the user’s spend across the cycle. Switch between **Daily
  spend**, **Weekly spend**, and **Aggregated spend** to change how the graph is plotted. The table
  breaks out each day’s **Monthly utilization**, **Aggregated spend**, **Weekly utilization**,
  **Weekly spend**, **Daily utilization**, and **Daily spend**.

## Act on high utilization

When users approach or reach their limits, you can respond in the following ways:

- To warn users before they reach a limit, add projected spend thresholds. See
  [Configure notifications](/user-guide/budgets/per-user-quotas-notifications#label-per-user-quota-notifications).
- To give blocked users more headroom, raise the limit or move users to a quota with a higher limit.
  See [Respond to escalations](/user-guide/budgets/per-user-quotas-enforcement#label-per-user-quota-escalations).
- To stop spend at the limit, enable block enforcement. See
  [Block users at the limit](/user-guide/budgets/per-user-quotas-enforcement#label-per-user-quota-enforcement).

## Related content

- [Per-user quotas](/user-guide/budgets/per-user-quotas)
- [Block users at a per-user quota limit](/user-guide/budgets/per-user-quotas-enforcement)
- [Monitor budgets](/user-guide/budgets/monitor)
