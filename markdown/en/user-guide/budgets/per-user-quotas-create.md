# Create and configure a per-user quota

You can create a per-user quota by running SQL statements or in Snowsight. This topic covers the
role you need, the SQL workflow, the recommended setup order, per-user limits, and the Snowsight
wizard. For an overview of how quotas work, see [Per-user quotas](/user-guide/budgets/per-user-quotas).

## Create a custom role for quota administration

You can create quotas as an account administrator, or create a custom role for quota
administration. The following example creates a role named `quota_owner` and grants it the
database role and privileges required to create quotas in the schema
`cost_mgmt_db.quota_schema`. Run the example with the `ACCOUNTADMIN` role:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE quota_owner;

GRANT USAGE ON DATABASE cost_mgmt_db TO ROLE quota_owner;
GRANT USAGE ON SCHEMA cost_mgmt_db.quota_schema TO ROLE quota_owner;
GRANT DATABASE ROLE SNOWFLAKE.QUOTA_CREATOR TO ROLE quota_owner;
GRANT CREATE SNOWFLAKE.CORE.QUOTA ON SCHEMA cost_mgmt_db.quota_schema TO ROLE quota_owner;
```

## Create a quota with SQL

To create a per-user quota, use a role with the privileges to create a quota. The following
example creates a quota named `my_quota` in `cost_mgmt_db.quota_schema`:

Copy code

```
USE SCHEMA cost_mgmt_db.quota_schema;

CREATE SNOWFLAKE.CORE.QUOTA my_quota();
```

After you create the quota, configure it in the order described in the next section.

## Recommended setup order

Configure a new quota in the following order:

1. Create the quota.
2. Add the monitored domains with `ADD_SHARED_RESOURCE`. See
   [Supported domains](/user-guide/budgets/per-user-quotas#label-per-user-quota-supported-resources).
3. If you want to scope the quota to specific users instead of the default `ALL_USERS` scope, set the
   user scope with `SET_USER_TAGS`, `INCLUDE_USERS`, or `EXCLUDE_USERS`. See
   [Specify users in scope](/user-guide/budgets/per-user-quotas-user-scope#label-per-user-quota-user-scope).
4. Verify the scope with `GET_QUOTA_SCOPE` immediately. If you scoped by tags that changed recently,
   wait about 10 minutes, then verify with `GET_USERS`, which can take up to about 2 hours to reflect
   the change. Also check that per-user spending matches your expectations with
   `GET_SPENDING_DETAILS_BY_USERS`.
5. Set the per-user limits and notifications. See
   [Set per-user spending limits](#label-per-user-quota-spending-limit) and
   [Configure notifications](/user-guide/budgets/per-user-quotas-notifications#label-per-user-quota-notifications).
6. Enable block enforcement with `SET_BLOCK_ENFORCEMENT_ENABLED`. See
   [Block users at the limit](/user-guide/budgets/per-user-quotas-enforcement#label-per-user-quota-enforcement).

Note

If block enforcement is enabled while the scope is taking effect, users you excluded can be briefly
blocked and receive block emails before the change takes effect. These blocks clear automatically
within minutes. To avoid this, configure the scope and wait 10 minutes before enabling enforcement.

## Set per-user spending limits

The quota admin sets one or more per-user credit limits: monthly, weekly, daily, or any
combination. Each user in scope is assigned the same per-user limits, and limits are enforced
independently per user. There is no aggregation or collective cap across users.

The limit must be a whole number of credits from 1 to 1,000,000,000. Zero, negative, `NULL`, and
decimal values aren’t accepted and return an error. The same rule applies to every cycle.

### Set a monthly limit

Set the monthly spending limit per user to 120 credits:

Copy code

```
CALL my_quota!SET_PER_USER_LIMIT(120);
```

Retrieve the current configuration, including the per-user limits:

Copy code

```
CALL my_quota!GET_CONFIG();
```

### Set a weekly or daily limit

To set a weekly or daily limit, pass the cycle argument to `SET_PER_USER_LIMIT`. Without the
argument, the limit applies to the monthly cycle.

Copy code

```
-- Monthly limit (default).
CALL my_quota!SET_PER_USER_LIMIT(1000);

-- Weekly limit.
CALL my_quota!SET_PER_USER_LIMIT(500, 'WEEKLY');

-- Daily limit.
CALL my_quota!SET_PER_USER_LIMIT(120, 'DAILY');
```

Each cycle is evaluated independently of the others, so a user is blocked as soon as they reach any
limit you set. The daily limit resets at the start of each UTC day. The weekly limit follows the ISO
week and resets Monday at 00:00 UTC, so a user blocked by their weekly limit is released the following
Monday.

To remove a limit, pass the cycle to unset: `'MONTHLY'`, `'WEEKLY'`, or `'DAILY'`. The cycle is
required, including for the monthly limit. For example, remove the weekly limit:

Copy code

```
CALL my_quota!UNSET_PER_USER_LIMIT('WEEKLY');
```

## Create a quota in Snowsight

In Snowsight, you can create per-user quotas without writing SQL. Quotas are managed alongside
budgets on the **Budgets** tab.

Before you begin, make sure you’re using a role with privileges to create quota objects in your
target database and schema. If you plan to scope the quota by tag, make sure the relevant users
are tagged.

1. Sign in to Snowsight.
2. In the navigation menu, select **Admin** » **Cost management**, then select the **Budgets** tab.
3. Select **+ Budget** in the upper right, then select **Quota**.

A four-step wizard opens and tracks your progress in the left rail. The following sections describe
each step.

### Quota scope

The **Quota scope** page determines which users and resources the quota monitors.

- **Specify which users to monitor**: Choose **All users in the account**, or **A group of users
  (through tags)** to scope by user tag. When you monitor all users, you can optionally exclude
  users that carry specific tags.
- **Specify which resources to track**: Choose **AI-related features** to monitor AI functions,
  Snowflake CoCo, Cortex Agents, Snowflake CoWork, and the AI Gateway (select all of them or specific
  resources within each), or **Warehouses** to monitor warehouse compute.

### Basic information

The **Basic information** page sets the quota’s name, location, and limits.

- **Name**: A descriptive name for the quota. This is the name shown in the Budgets list.
- **Location**: The database and schema that own the quota object.
- **Monthly credit limit**: The monthly credit ceiling for each user in scope. Usage resets on the
  first of each month.
- **Weekly credit limit**: The weekly credit ceiling for each user in scope. Usage resets Monday at
  00:00 UTC. This field appears when you’re monitoring AI features.
- **Daily credit limit**: The daily credit ceiling for each user in scope. Usage resets daily at
  00:00 UTC. This field appears when you’re monitoring AI features. For AI features, set at least one
  of the daily or monthly credit limits.

Note

The available limit fields depend on the resource scope you chose on the **Quota scope** page. For
AI-related features, **Monthly credit limit**, **Weekly credit limit**, and **Daily credit limit**
appear, and at least one is required. For warehouses, only **Monthly credit limit** appears, and
it’s required.

### Alert notifications

The **Alert notifications** page configures who is notified when spend reaches a threshold. You can
add multiple alerts, and each one is evaluated independently. Alert notifications are available when
you set a monthly limit.

- **Alert based on**: Use **Actual spend** to alert on accumulated usage, or **Projected spend** to
  alert on the user’s current spending trend.
- **Alert at**: The percentage of the limit that triggers the alert.
- **Notify affected user**: Email the user in scope. Leave it cleared to notify only the summary
  recipients.
- **Summary emails**: Email addresses that receive a summary when one or more of the alerts are
  triggered.

### Enforcement and actions

The **Enforcement and actions** page configures how limits are enforced and adds custom automated
actions.

- **Enable enforcement**: When enabled, the quota blocks users who reach their per-user limit. You
  can choose whether blocked users receive an email. For more information, see
  [Block users at the limit](/user-guide/budgets/per-user-quotas-enforcement#label-per-user-quota-enforcement).
- **Custom actions**: Trigger stored procedures when monthly spend reaches a threshold. Custom
  actions are evaluated against the monthly credit limit and are independent of alert
  notifications. For more information, see
  [Configure custom actions](/user-guide/budgets/per-user-quotas-notifications#label-per-user-quota-custom-actions).

Note

The options on this page depend on the resource scope you chose. AI-related scopes show
**Enable enforcement**, because the wizard doesn’t offer custom actions for AI-related scopes. Warehouse
scopes show **Custom actions**, because block enforcement doesn’t apply to warehouses.

When you’re done, select **Create**. Snowflake provisions the quota and begins evaluating
consumption for all users in scope.

## Related content

- [Per-user quotas](/user-guide/budgets/per-user-quotas)
- [Specify users in scope for a per-user quota](/user-guide/budgets/per-user-quotas-user-scope)
- [Notifications and actions for per-user quotas](/user-guide/budgets/per-user-quotas-notifications)
- [Monitor per-user quota spending](/user-guide/budgets/per-user-quotas-monitor)
- [Per-user quota method reference](/user-guide/budgets/per-user-quotas-reference)
