# Cost controls for CoCo

Snowflake gives account administrators several complementary ways to manage and control CoCo credit
consumption. This page summarizes your options and links to detailed documentation for each.

Each control suits a different need: daily credit limits give you a quick per-user cap on a single CoCo
surface, while budgets and per-user quotas add spend visibility and flexible, automated controls for CoCo
across your teams. Choose the option, or combination, that best matches how you want to manage CoCo spend.

## Cost control options

The following table maps common goals to the control that fits them:

| If you want to | Use |
| --- | --- |
| Track CoCo spend by team or cost center and get alerted as spend approaches a limit | [Budgets](/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance) |
| Get notified as users approach their limits and enforce per-user daily and monthly credit limits for CoCo, with automatic blocking | [Per-user quotas](/user-guide/budgets/per-user-quotas) |
| Set a simple per-user daily estimated credit limit for a specific CoCo surface (CLI, Desktop, or Snowsight) | [Daily credit usage limits](/user-guide/cortex-code/credit-usage-limit) |

Expand

Show lessSee more

## Budgets

Budgets let you track and control CoCo credit consumption broken down by the team or cost center consuming
it. With a budget, you can do the following:

- Tag the users who belong to a business unit and add CoCo as a shared resource, so the budget tracks only
  the credits those users consume.
- Get notified when CoCo spend is projected to exceed the limit, and trigger custom actions at defined
  thresholds.
- Manage ongoing spend, which budgets suit well because budget evaluation is periodic rather than
  immediate.
- Extend the same budgets model to other Snowflake AI features if you want to manage them alongside CoCo.

For details, see
[AI cost management and governance](/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance)
and [shared resource budgets](/user-guide/budgets/budget-shared-resources).

## Per-user quotas

Per-user quotas give you both proactive visibility and enforcement for CoCo at per-user granularity. With a
quota, you can do the following:

- Define daily and monthly per-user credit limits that apply uniformly to all users in scope.
- Receive notifications, based on actual or projected spend, as users approach or reach those limits, so you
  can act early.
- Block a user automatically at their limit or run a custom stored procedure. Blocks release automatically
  when the cycle resets or you raise the limit.
- Apply a quota to all users or a tagged subset, and monitor per-user CoCo spending in Snowsight.
- Cover all CoCo surfaces (CLI, Desktop, and Snowsight), and govern other AI features in the same quota if
  needed.

For details, see [Per-user quotas](/user-guide/budgets/per-user-quotas).

## Daily credit usage limits

Daily estimated credit usage limits block a user from a specific CoCo surface once their estimated usage in
a rolling 24-hour window exceeds a configured threshold. They’re set with per-surface account and user
parameters, and are the simplest option when you want a straightforward per-user cap on the CLI, Desktop, or
Snowsight surface.

For the full parameter reference, values, per-surface examples, and an audit script, see
[Daily credit usage limits for CoCo](/user-guide/cortex-code/credit-usage-limit).

## Related content

- [CoCo](/user-guide/cortex-code/cortex-code)
- [Daily credit usage limits for CoCo](/user-guide/cortex-code/credit-usage-limit)
- [Per-user quotas](/user-guide/budgets/per-user-quotas)
- [AI cost management and governance](/user-guide/snowflake-cortex/governance-and-availability/ai-cost-management-and-governance)
