# Per-user quotas

Per-user quotas let you enforce spending limits at a per-user granularity, preventing individual
users from generating unwanted costs. Quotas are particularly useful when deploying services where
individual users can accumulate significant charges in a short period of time, such as running
complex AI functions over a large dataset.

With per-user quotas, you can:

- Define monthly, weekly, and daily per-user credit limits that apply uniformly to all users in scope.
- Apply the quota to all users in your account, or select groups of users by user tags or roles to represent teams, cost centers, or business units, and include or exclude individual users by name.
- Block users automatically when they reach a per-user limit. Blocks are released automatically when the cycle resets or you raise the limit.
- Notify users when they approach or exceed their limits, based on actual or projected spend.
- Automate custom enforcement actions with stored procedures triggered at configurable thresholds, and reset affected states at the start of each month.
- Monitor per-user spending, utilization, and enforcement status in Snowsight.

## Per-user quota topics

The following topics cover each part of working with per-user quotas:

- [Create and configure a per-user quota](/user-guide/budgets/per-user-quotas-create): Create a
  quota with SQL or Snowsight, follow the recommended setup order, and set per-user limits.
- [Specify users in scope](/user-guide/budgets/per-user-quotas-user-scope): Choose which users a
  quota covers.
- [Block users at the limit](/user-guide/budgets/per-user-quotas-enforcement): Enable built-in
  block enforcement and handle requests for more headroom.
- [Notifications and actions](/user-guide/budgets/per-user-quotas-notifications): Notify users and
  admins, and run stored procedures at thresholds.
- [Monitor spending](/user-guide/budgets/per-user-quotas-monitor): Review per-user spending in SQL
  or Snowsight, and let users check their own usage.
- [Method reference](/user-guide/budgets/per-user-quotas-reference): Every method available on a
  quota object.

To create a quota, you need a role with the `SNOWFLAKE.QUOTA_CREATOR` database role, the `USAGE`
privilege on the target database and schema, and the `CREATE SNOWFLAKE.CORE.QUOTA` privilege on the
schema. For an example, see
[Create a custom role for quota administration](/user-guide/budgets/per-user-quotas-create#label-per-user-quota-admin-role).
For guidance on choosing limit values from your account’s actual usage, see
[Size Cortex Code per-user limits from real usage](/developer-guide/cortex-ai-cookbook/coco-user-budget-sizing).

## How per-user quotas work

A per-user quota is a first-class Snowflake object that defines per-user spending controls
within a specified database and schema. After you create a quota, you configure it by specifying
which users are in scope, what their quota thresholds are, and what actions to take when
thresholds are crossed.

### Quota cycles

Set at least one of the following limits. Each limit is the maximum number of credits a user can
consume in one cycle. Every cycle begins at 00:00 UTC, when each user’s usage counter resets to zero.

- **Monthly limit**: One calendar month, starting on the first of the month.
- **Weekly limit**: One week, starting on Monday.
- **Daily limit**: One day.

If you set more than one limit, Snowflake evaluates each configured limit independently. If the Block
action is enabled, a user who reaches any limit is blocked for the rest of that limit’s cycle, even if
they remain below the other limits.

### Enforcement actions

When a user reaches a limit, the quota can take an enforcement action:

- **Block** (built-in): Snowflake automatically blocks the user from issuing new AI requests once
  their spend reaches the limit, with no customer-authored code. Enforcement is evaluated within
  minutes of a spend event, applies per cycle, and is released automatically when the cycle resets.
  For more information, see
  [Block users at the limit](/user-guide/budgets/per-user-quotas-enforcement#label-per-user-quota-enforcement).
- **Custom action**: A stored procedure that you provide runs when a threshold is crossed, letting
  you implement custom enforcement such as revoking access based on a role, sending customized
  notifications, or writing an audit record. For more information, see
  [Configure custom actions](/user-guide/budgets/per-user-quotas-notifications#label-per-user-quota-custom-actions).

### User selection

A quota’s user scope has three parts:

- **Include**: All users in the account (the default), or a group of users selected by user tags,
  roles, or both. One operator combines the tags and roles in a group: `UNION` includes users who
  match at least one, and `INTERSECTION` includes users who match all of them.
- **Exclude**: Groups of users to remove from the scope, selected by user tags or roles.
- **Named users**: Individual users who are always in scope or always out of scope.

Roles select which users the quota monitors, not which usage counts toward the limit. Only direct
role grants count; inherited roles don’t. For each user in scope, all usage of the quota’s monitored
domains and resources counts toward that user’s limit, regardless of the active primary or secondary
roles.

Snowflake resolves users at evaluation time, so changes to tag assignments and role grants are
reflected in the quota without any reconfiguration. For more information, see
[Specify users in scope](/user-guide/budgets/per-user-quotas-user-scope#label-per-user-quota-user-scope).

### Threshold types

Thresholds determine when notifications or custom actions are triggered for a user. They’re
expressed as a percentage of the per-user limit for the cycle the threshold is configured against,
and can be evaluated using one of two methods:

- **Actual spend**: Triggers when a user’s accumulated spend within the current cycle exceeds the
  configured percentage of their per-user limit for that cycle. Use actual spend for hard
  enforcement.
- **Projected spend** (default): Triggers when the user’s current spending rate, extrapolated
  to the end of the cycle, indicates they’re likely to exceed the threshold. Use projected spend
  for early warning and prevention.

Projections need enough elapsed usage in the cycle to be meaningful, so they aren’t calculated during
approximately the first 12 hours of a daily or weekly cycle.

**Example: Actual spend**

Per-user quota: 300 credits. Threshold: 90% (Actual). The notification or action triggers when
the user has consumed 270 credits within the month.

**Example: Projected spend**

Per-user quota: 300 credits. Threshold: 90% (Projected). On day 1 of a 30-day month, the
threshold triggers if the user has spent 9 credits (because 9 × 30 = 270, which equals 90% of
the quota). This lets you intervene before users reach their limits.

## Supported domains

Per-user quotas monitor the following supported domains that emit per-user usage data. The per-user
spending limit applies to usage against one or more of the selected domains.

A single quota monitors either warehouse compute or AI domains, but not a mix of the two. The units
of measurement differ (Platform Credits for warehouse compute versus AI Credits for AI domains), so
warehouse and AI domains can’t be combined in the same quota. For more information about AI Credits,
see [Snowflake AI pricing](/user-guide/snowflake-cortex/pricing).

The following table lists each domain and the costs it monitors:

| Domain | Monitored costs |
| --- | --- |
| `WAREHOUSE` | Compute resources for query execution in warehouses, including warehouse metering and query acceleration costs. |
| `AI FUNCTION` | Credit usage for AI function operations attributed to the user. |
| `SNOWFLAKE INTELLIGENCE` | Credit usage for Snowflake CoWork (formerly Snowflake Intelligence) operations attributed to the user. |
| `CORTEX AGENT` | Credit usage for Cortex Agents operations attributed to the user. |
| `CORTEX CODE` | Credit usage for Snowflake CoCo (formerly Cortex Code) operations attributed to the user. Includes spend from Snowflake CoCo CLI, Snowflake CoCo in Snowsight, and Snowflake CoCo Desktop. |
| `AI GATEWAY` | Credit usage for AI Gateway operations attributed to the user. |

Expand

Show lessSee more

### Add domains and resources to a quota

You can specify one or more of the domains that you want to track with your quota. You can select
domains when you create the quota in Snowsight or with SQL, and you can change them after the quota
is created. The following examples assume a quota named `my_quota`; to create one, see
[Create a quota with SQL](/user-guide/budgets/per-user-quotas-create#label-per-user-quota-create).

Example: Add all AI functions to your quota:

Copy code

```
CALL my_quota!ADD_SHARED_RESOURCE('AI FUNCTION');
```

Example: Add the `AI_CLASSIFY` function to your quota:

Copy code

```
CALL my_quota!ADD_SHARED_RESOURCE('AI FUNCTION', 'AI_CLASSIFY');
```

Note

If you add the whole `AI FUNCTION` domain, you don’t need to add specific functions such as
`AI_CLASSIFY` separately.

Example: Add a specific Cortex Agent to the quota:

Copy code

```
CALL my_quota!ADD_SHARED_RESOURCE(
  'CORTEX AGENT',
  (SELECT SYSTEM$REFERENCE('CORTEX AGENT', 'myagent'))
);
```

Example: Add the Snowflake CoWork domain to the quota:

Copy code

```
CALL my_quota!ADD_SHARED_RESOURCE('SNOWFLAKE INTELLIGENCE');
```

Example: Add a specific warehouse to the quota:

Copy code

```
CALL my_quota!ADD_SHARED_RESOURCE(
  'WAREHOUSE',
  (SELECT SYSTEM$REFERENCE('WAREHOUSE', 'SNOWADHOC'))
);
```

### Add the AI Gateway

Add the AI Gateway by domain. Each account has a single gateway, named `SNOWFLAKE`, so the domain
covers it.

Copy code

```
CALL my_quota!ADD_SHARED_RESOURCE('AI GATEWAY');
```

## Use Snowflake CoCo to manage quotas

You can also work with per-user quotas through the **Cost Intelligence** skill in Snowflake CoCo,
using natural language instead of writing SQL or stepping through the Snowsight wizard. The Cost
Intelligence skill is available in both the Snowflake CoCo UI and the Snowflake CoCo CLI.

Use the skill to create and configure quotas, review per-user spending and utilization, and check
enforcement status by describing what you want in plain language. The skill translates your request
into the underlying quota operations described in these topics.

For more information about the Cost Intelligence skill, see
[Cost Intelligence](/user-guide/cortex-code/bundled-skills#cost-intelligence).

## Limitations and considerations

- Quotas support monthly, weekly, and daily cycles aligned to the UTC calendar. Custom cycle start dates
  aren’t supported.
- Custom actions and cycle-start actions are evaluated against the monthly cycle only. They don’t
  apply to weekly or daily limits.
- Snowsight offers custom actions and cycle-start actions only for quotas scoped to warehouses. To use
  them with an AI-related scope, configure them with SQL.
- No enforcement occurs until a per-user spending limit is set.
- You can’t set different limits for different users within the same quota. All users share
  the same per-user limits.
- Collective spending limits across all users in a quota aren’t supported. Each user’s limit
  is evaluated independently.
- Quota evaluation doesn’t happen in real time. Snowflake counts AI usage against a quota within minutes.
  Snowflake counts warehouse usage against a quota only after it attributes warehouse credits to individual
  queries, which can happen several hours after a query finishes. A slight lag might also occur between a
  user being blocked and the data appearing in Snowsight.
- Notifications are sent at most once per threshold per user within a 24-hour period for
  projected spend thresholds. Actual spend thresholds trigger at most once per cycle.
- Block enforcement applies only to AI domains, and enforcement can briefly lag spend. For details,
  see [Limitations of block enforcement](/user-guide/budgets/per-user-quotas-enforcement#label-per-user-quota-enforcement-limitations).

## Cost of per-user quotas

After you create a quota, Snowflake runs the `_QUOTA_MEASUREMENT_TASK` and
`_QUOTA_MEASUREMENT_FINALIZER` tasks in your account to measure per-user spending. These tasks don’t
currently consume billable credits and don’t appear in the
[SERVERLESS\_TASK\_HISTORY](/sql-reference/account-usage/serverless_task_history) view.

Quotas store a small amount of configuration and usage data, which is billed as standard storage.

## Related content

- [Monitor credit usage with budgets](/user-guide/budgets/monitor)
- [Custom budgets](/user-guide/budgets/custom-budget)
- [Notifications for budgets](/user-guide/budgets/notifications)
- [Custom actions for budgets](/user-guide/budgets/custom-actions)
- [Cycle-start actions for budgets](/user-guide/budgets/cycle-start-actions)
- [Budgets roles and privileges](/user-guide/cost-access-control)
- [MY\_BUDGET\_SUMMARY (SNOWFLAKE.LOCAL)](/sql-reference/functions/my_budget_summary-snowflake-local)
