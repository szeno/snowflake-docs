# Cortex Agents shared resource budgets

A shared resource-level budget lets you set a credit spending limit for a subset of users on a Cortex Agent
object. Unlike a resource-level budget — which applies to the entire object and is typically aggregated use
across the entire account — a shared resource-level budget targets a specific group of users (for example, a
team) identified by a tag. This allows multiple teams to share the same Cortex Agent object while
maintaining independent spending limits per team.

To use a shared resource-level budget, you create a budget, add the Cortex Agent object as a “shared
resource”, associate a user tag with the budget, and then apply that tag to users. Snowflake tracks credit
consumption per tagged user group and evaluates spending against the budget independently. When a user is
subject to multiple budgets, each budget is evaluated independently and the user is stopped by whichever
threshold is reached first.

Shared resource-level budgets set a spending limit for a tagged group of users on a specific agent. To apply the same per-user credit limits to each user, across Cortex Agents and other AI domains, and optionally block users who reach a limit, use [per-user quotas](/user-guide/budgets/per-user-quotas).

## How shared resource-level budgets work

Shared resource-level budgets use a user-tag-based attribution model. Instead of tagging the Cortex Agent
object itself, you tag the users who access it. Snowflake tracks credit consumption for each tagged user group
against the associated budget.

The enforcement flow is:

1. You create a budget and set a monthly spending limit in credits for the user group.
2. You add the Cortex Agent object as a shared resource on the budget.
3. You create a tag and associate it with the budget using `SET_USER_TAGS`.
4. You apply the tag to individual users who belong to the group.
5. Snowflake tracks credit consumption for the tagged users on the shared resource.
6. When spending reaches a configured threshold, Snowflake executes the stored procedure you defined for that
   threshold.

Note

Shared resources don’t have tags applied at the object level. The tag is applied to users, not to the
Cortex Agent object. This is different from resource-level budgets, where the tag is applied directly
to the object.

## Set up a shared resource-level budget

Follow these steps to create a budget for a subset of users on a shared Cortex Agent object.

### Step 1: Create a budget

Create a budget object in the schema where you manage budgets:

Copy code

```
-- Create a budget object for the user group
USE SCHEMA budgets_db.budgets_schema;

CREATE SNOWFLAKE.CORE.BUDGET my_budget();
```

### Step 2: Set the spending limit

Set the monthly credit spending limit for the entire user group:

Copy code

```
-- Set a 500-credit monthly spending limit for the user group
CALL my_budget!SET_SPENDING_LIMIT(500);
```

### Step 3: Create a cost center tag

Create a tag to identify the cost center associated with the user group:

Copy code

```
-- Create a tag with allowed cost center values
CREATE TAG cost_mgmt_db.tags.cost_center
  ALLOWED_VALUES 'finance_dept', 'marketing_dept', 'hr_dept'
  COMMENT = 'cost_center tag';
```

### Step 4: Add the Cortex Agent object as a shared resource

Add the Cortex Agent object to the budget as a shared resource. This tells Snowflake which resource to
track spending against for the tagged users:

Add all objects as a shared resource on the budget

Copy code

```
CALL budgets_db.budgets_schema.my_budget!ADD_SHARED_RESOURCE(
        'CORTEX AGENT'
);
```

Alternatively, you can add the specific object as a shared resource on the budget

Copy code

```
CALL budgets_db.budgets_schema.my_budget!ADD_SHARED_RESOURCE(
           'CORTEX AGENT',
           (SELECT SYSTEM$REFERENCE('CORTEX AGENT', 'myagent'))
);
```

### Step 5: Associate the user tag with the budget

Add the user tag to the budget so that Snowflake tracks spending for tagged users against this budget. In the
example below, the finance team is limited to 500 credits per month.

Copy code

```
-- Associate the cost center tag with the budget as a user tag
CALL budgets_db.budgets_schema.my_budget!SET_USER_TAGS(
  [
    [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.cost_center', 'SESSION', 'APPLYBUDGET')),
    'finance_dept']
  ],
  'UNION');
```

### Step 6: Tag the users

Apply the tag to each user who belongs to the group. Snowflake tracks credit consumption for these users
against the shared resource budget:

Copy code

```
-- Tag users who belong to the finance department
ALTER USER IF EXISTS "user_1" SET TAG cost_center = 'finance_dept';
ALTER USER IF EXISTS "user_2" SET TAG cost_center = 'finance_dept';
ALTER USER IF EXISTS "user_3" SET TAG cost_center = 'finance_dept';
```

After you complete these steps, Snowflake tracks credit consumption for `user_1`, `user_2`, and `user_3`
on the Cortex Agent object against the `my_budget` budget with a 500-credit monthly limit.

You can set up multiple budgets — one for HR, another for marketing — each with its own spending limit and cost
center tag.

## Configure threshold actions

You can attach stored procedures that execute when spending by the user group reaches specific thresholds.
Thresholds are expressed as a percentage of the spending limit and apply to the monthly budget period.

### Set custom actions at thresholds

Configure stored procedures to run at different spending thresholds for the user group:

Copy code

```
-- Alert at 80% of the user group budget
CALL budgets_db.budgets_schema.my_budget!ADD_CUSTOM_ACTION(
  SYSTEM$REFERENCE(
    'PROCEDURE',
    'budgets_db.budgets_schema.sp_budget_alert(string, string, number)'
  ),
  ARRAY_CONSTRUCT('CA_1', 'finance_dept', 80),
  'ACTUAL',
  80
);

-- Block access at 100% of the user group budget
CALL budgets_db.budgets_schema.my_budget!ADD_CUSTOM_ACTION(
  SYSTEM$REFERENCE(
    'PROCEDURE',
    'budgets_db.budgets_schema.sp_revoke_group_access(string)'
  ),
  ARRAY_CONSTRUCT('finance_dept'),
  'ACTUAL',
  100
);
```

### Review configured actions

List all custom actions configured on a budget:

Copy code

```
-- View all custom actions on the budget
CALL budgets_db.budgets_schema.my_budget!GET_CUSTOM_ACTIONS();
```

### Example: Stored procedure to revoke access for a user group

The following stored procedure revokes a role from a group of users to block their access to the
Cortex Agent object. Snowflake recommends creating a dedicated role per user group to support this pattern:

Copy code

```
-- Create a stored procedure that revokes access for a user group
CREATE OR REPLACE PROCEDURE budgets_db.budgets_schema.sp_revoke_group_access(
  dept_name STRING
)
RETURNS STRING
LANGUAGE SQL
AS
BEGIN
  EXECUTE IMMEDIATE 'REVOKE ROLE ca_' || dept_name || '_role FROM ROLE ' || dept_name || '_role';
  RETURN 'Access revoked for group ' || dept_name;
END;
```

When the user group’s spending reaches 100% of the budget, Snowflake calls this stored procedure. The procedure
revokes the dedicated role, which removes access to the Cortex Agent object for all users in that group.

## Revoke and reinstate access

In some cases you need to reinstate access for a user group after a budget breach — for example, for specific
users during peak season. You can configure thresholds beyond 100% (up to 1000%) to handle these exception
scenarios.

### Budget breach and access revocation

When spending by the user group reaches the 100% threshold, the configured stored procedure executes and
revokes access for that group:

Copy code

```
-- At 100%: access is revoked automatically for the user group
-- Users tagged with finance_dept can no longer access the Cortex Agent object
```

### Reinstate access for exceptions

Configure a threshold beyond 100% with a stored procedure that reinstates access. This allows you to raise the
effective budget for exception periods:

Copy code

```
-- You have to add grants for this procedure
GRANT USAGE ON DATABASE budgets_db TO APPLICATION SNOWFLAKE;
GRANT USAGE ON SCHEMA budgets_db.budgets_schema TO APPLICATION SNOWFLAKE;
GRANT USAGE ON PROCEDURE budgets_db.budgets_schema.sp_revoke_ca_access(STRING, STRING)
  TO APPLICATION SNOWFLAKE;

-- Issue a reinstatement for a subset of users
sp_reinstate_group_access (ca_name, power_user_role)

-- Set another threshold at 200% as a hard stop
CALL budgets_db.budgets_schema.my_budget!ADD_CUSTOM_ACTION(
  SYSTEM$REFERENCE(
    'PROCEDURE',
    'budgets_db.budgets_schema.sp_revoke_group_access(string)'
  ),
  ARRAY_CONSTRUCT('finance_dept'),
  'ACTUAL',
  200
);
```

The reinstatement stored procedure grants the role back to the user group:

Copy code

```
-- Create a stored procedure that reinstates access for a user group
CREATE OR REPLACE PROCEDURE budgets_db.budgets_schema.sp_reinstate_group_access(
  ca_name STRING, power_user_role STRING
)
RETURNS STRING
LANGUAGE SQL
AS
BEGIN
  EXECUTE IMMEDIATE 'GRANT ROLE ca_' || ca_name || '_role TO ROLE ' || power_user_role || '_role';
  RETURN 'Access reinstated for group ' || power_user_role;
END;
```

In this example:

- At 100%, access is revoked automatically for the finance department users.
- An admin reinstates access for certain power users (as indicated by `power_user_role`).
- At 200%, the revocation procedure runs again as a hard stop.

You can configure thresholds at any percentage up to 1000%.

## Monitor usage

View credit consumption per user on the shared Cortex Agent object using the budget’s usage reporting
method:

Copy code

```
-- View usage for the current month
CALL budgets_db.budgets_schema.my_budget!GET_SERVICE_TYPE_USAGE_V2(
  '2026-02',
  '2026-03'
);
```

The output includes the following columns:

| Column | Description |
| --- | --- |
| SERVICE\_TYPE | The service category (CORTEX\_AGENTS) |
| ENTITY\_TYPE | The object type (CORTEX AGENT) |
| ENTITY\_ID | The internal identifier of the Cortex Agent object |
| NAME | The name of the Cortex Agent object |
| CREDITS\_USED | The total credits consumed during the specified period (sum of compute and cloud) |
| CREDITS\_COMPUTE | The number of compute credits used |

Expand

Show lessSee more

## Budget enforcement latency

Budget calculations and threshold enforcement are conducted periodically:

1. Snowflake calculates credit consumption for the tagged user group on the shared resource.
2. The system evaluates spending against all configured thresholds.
3. If a threshold is reached, the associated stored procedure executes.
4. Usage dashboards update with the latest figures.

If the low latency budget is enabled, budgets are enforced within two hours after the budget is exceeded.
Otherwise, it may take up to eight hours after the budget is exceeded for enforcement. To reduce the refresh
interval, you can trigger budget execution more frequently, such as every 60 minutes.

Warning

There is an inherent delay between when credits are consumed and when the budget system detects the threshold
breach. During the enforcement interval, spending can exceed the configured threshold before the action is
executed. Plan your thresholds accordingly. For example, set an alert at 80% to give you time to respond
before the 100% action is triggered.

## Budget precedence

When a user is subject to multiple budgets — for example, both a resource-level budget on the Cortex Agent
object and a shared resource-level budget for the user’s team — each budget is evaluated independently. The
user’s usage is limited by whichever threshold is reached first.

For example, consider the following configuration:

- A resource-level budget on `CA_1` with a 1,000-credit limit and a block action at 100%.
- A shared resource-level budget for the finance department on Cortex Agent with a 500-credit limit and a
  block action at 100%.

If the finance department reaches 500 credits (100% of their shared budget) before the overall Cortex Agent object
reaches 1,000 credits, the shared budget’s block action triggers first and revokes access for the finance
department. Other teams that use `CA_1` continue to have access until the resource-level budget threshold is
reached.

Conversely, if the overall Cortex Agent object reaches 1,000 credits before the finance department reaches 500 credits,
the resource-level budget’s block action triggers and revokes access for all users — including the finance
department — even though their team budget hasn’t been exhausted.

## Limitations

The following limitations apply to shared resource-level budgets for Cortex Agent:

- **No tags on shared resources**: Shared resources don’t have tags applied at the object level. Tags are
  applied to users only. This is different from resource-level budgets, where the tag is applied to the
  Cortex Agent object.
- **Individual user tagging**: You must tag each user individually. There is no bulk operation to tag all users
  in a role or group.
- **Enforcement latency**: Budget enforcement runs on a periodic cycle and may take up to eight hours to enforce
  the budget after the budget is exceeded. Spending can exceed a threshold during the interval before the action
  triggers.
- **Role-based access revocation**: To revoke access for a user group at a threshold, you must create a
  dedicated role for the group. Direct block actions on individual users aren’t yet supported.
- **Monthly period**: Budgets operate on a monthly cycle. You can’t configure custom budget periods.
- **Tag latency**: When you change a tag on a user, it can take up to eight hours for the change to be
  reflected in budgets that use tags.
