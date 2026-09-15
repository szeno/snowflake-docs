# Resource budgets for Cortex Agents

A resource budget lets you monitor Cortex Agents spend for your account and take actions when it exceeds spending thresholds. This allows you
to control costs for Cortex Agents and take automated actions such as revoking access when spending
exceeds your configured limits. Resource budgets give you control over the credits consumed at an aggregated level for that specific Agent.

Resource budgets apply to the Cortex Agent object. To set the same monthly or daily credit limit for each user, and optionally block users who reach that limit on Cortex Agents and other AI domains, use [per-user quotas](/user-guide/budgets/per-user-quotas).

## How resource budgets work

Resource budgets use Snowflake’s tag-based cost attribution model. You create a tag, apply it to a
Cortex Agent object, and then associate that tag with a budget. Snowflake tracks credit consumption for
the tagged object and evaluates spending against the budget limit periodically. The resource budget is
useful for limiting the spend for the Cortex Agent object.

Snowflake enforces resource budgets with the following flow:

1. You create a tag.
2. You apply the tag to the Cortex Agent object.
3. You create a budget and specify the tag to track spending for. As part of creating the budget, you also set a monthly spending limit in credits.
4. You add a stored procedure to be executed when spending reaches a configured threshold of the budget. For example, you can invoke a stored procedure for alerting at 80% and another stored procedure for revoking access at 100%.
5. Snowflake tracks credit consumption for the tagged object.
6. When spending reaches a configured threshold of the budget, such as 80% or 100%, Snowflake executes the stored procedure defined for that threshold.

Snowflake calculates usage, evaluates thresholds, and triggers any configured actions periodically.
After the budget is exceeded, it might take up to eight hours with standard budget (or two hours with latency optimized option) for the budget to be enforced.

## Create a tag

1. Create a tag to identify the cost center associated with the Cortex Agent object:

   Copy code

   ```
   -- Create a tag with allowed cost center values
   CREATE TAG cost_mgmt_db.tags.cost_center
   ALLOWED_VALUES 'org-level'
   COMMENT = 'cost_center tag';
   ```
2. Apply the tag to the Cortex Agent object to associate it with a cost center:

   Copy code

   ```
   -- Apply the cost center tag to the Cortex Agent object
   ALTER AGENT IF EXISTS my_agent
     SET TAG cost_mgmt_db.tags.cost_center = 'org-level';
   ```

## Set up a resource budget

You can use either Snowsight or SQL to create a budget and associate it with a Cortex Agent object.

Snowsight UISQL

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Cost management**.
3. Select **Budgets**.
4. Select **+ Budget**.
5. For **Location to store**, select the name of the database and schema where you want to create the budget.
6. For **Name**, use `my_budget`.
7. For **Budget (credits per month)**, enter a value, such as **10000**, for the spending limit of the budget.
8. To decrease the [budget refresh interval](/user-guide/budgets#label-budgets-refresh-interval) so you can watch spending more closely, select **Enable low latency budget**.
9. For **Threshold**, enter a value, such as **80**, for the notification threshold.
10. For **Notify**, enter email addresses to receive notification emails.
11. Select **Next**.
12. For **Budget scope**, add the tag on the Cortex Agent object to the resource budget.
13. Select **Create**.

1. Create a budget instance in the schema where you manage budgets:

   Copy code

   ```
   -- Create a budget instance
   USE SCHEMA budgets_db.budgets_schema;

   CREATE SNOWFLAKE.CORE.BUDGET my_budget();
   ```
2. Set the monthly credit spending limit for the budget:

   Copy code

   ```
   -- Set a 10000-credit monthly spending limit
   CALL my_budget!SET_SPENDING_LIMIT(10000);
   ```
3. Add the tag to the budget so that Snowflake tracks spending for the tagged object against this budget:

   Copy code

   ```
   -- Associate the cost center tag with the budget
   CALL budgets_db.budgets_schema.my_budget!SET_RESOURCE_TAGS(
   [
      [(SELECT SYSTEM$REFERENCE('TAG',
         'cost_mgmt_db.tags.cost_center',
         'SESSION',
         'applybudget')),
         'org-level']
   ],
   'UNION');
   ```

Now, Snowflake tracks credit consumption for `my_agent` against the `my_budget` budget
with a 10,000-credit monthly limit.

## Configure threshold actions

You can attach stored procedures that are executed when spending reaches specific thresholds, which are
expressed as a percentage of the spending limit and apply to the monthly budget period. For more information, see [Custom actions for budgets](/user-guide/budgets/custom-actions).

### Send notifications

You can send notifications when spending reaches a threshold. For more information, see [Notifications for budgets](/user-guide/budgets/notifications).

1. Set the email to send notifications to:

   Copy code

   ```
   CALL my_budget!SET_EMAIL_NOTIFICATIONS(
     'budgets_notification_integration',
   'costadmin@example.com, budgetadmin@example.com'
   );
   ```
2. Set the notification threshold:

   Copy code

   ```
   CALL my_budget!SET_NOTIFICATION_THRESHOLD(80);
   ```

### Revoke access

1. Create a stored procedure that revokes access to Cortex Agents. In the stored procedure, you can limit access to a specific role to revoke USAGE for that role.

   Copy code

   ```
   -- Create a stored procedure that revokes access to the Cortex Agent object
   CREATE OR REPLACE PROCEDURE budgets_db.budgets_schema.sp_revoke_agent_access(
   agent_name STRING, role_name STRING
   )
   RETURNS STRING
   LANGUAGE SQL
   AS
   BEGIN
   EXECUTE IMMEDIATE 'REVOKE ROLE agent_' || agent_name || '_role FROM ROLE ' || role_name;
   RETURN 'Access revoked for ' || agent_name;
   END;
   ```

   Important

   Ensure the `role_name` and the user do not have access to Cortex Agents through other roles. For guidance about configuring roles and privileges correctly, see [User privileges and access control](/user-guide/snowflake-cortex/snowflake-cowork/deploy-agents#label-snowflake-intelligence-user-privileges).
2. Set a custom action that blocks access when 100% of the budget has been spent. You can also use custom actions for notifications.

   Copy code

   ```
   -- Provide access to the stored procedures
   GRANT USAGE ON DATABASE budgets_db TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON SCHEMA budgets_db.budgets_schema TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON PROCEDURE budgets_db.budgets_schema.sp_revoke_agent_access(STRING, STRING)
   TO APPLICATION SNOWFLAKE;

   -- Block access at 100% of the budget
   CALL budgets_db.budgets_schema.my_budget!ADD_CUSTOM_ACTION(
   SYSTEM$REFERENCE('PROCEDURE',
      'budgets_db.budgets_schema.sp_revoke_agent_access(string, string)'),
   ARRAY_CONSTRUCT('AGENT_NAME', 'ROLE_NAME'),
   'ACTUAL',
   100);
   ```

> Note
>
> You can also use custom actions to take action when spending is forecasted to exceed the budget limit. For more information, see [Custom actions for budgets](/user-guide/budgets/custom-actions).

### Handling exceptions to spending limits

In some cases, you may need to reinstate access after the budget limit is reached, like during earnings season or
other peak periods. You can configure thresholds beyond 100%, up to 500%, to handle these exception
scenarios.

The workflow assumes that access is revoked using the configured stored procedure when spending reaches a budget threshold. The admin reinstates
a subset of the users and grants access back. When spending reaches 200%, the revocation procedure runs
again as a hard stop.

1. Create a stored procedure to reinstate access to the role:

   Copy code

   ```
   -- Create a stored procedure that reinstates access to the Cortex Agent object
   CREATE OR REPLACE PROCEDURE budgets_db.budgets_schema.sp_reinstate_agent_access(
   agent_name STRING, role_name STRING
   )
   RETURNS STRING
   LANGUAGE SQL
   AS
   BEGIN
   EXECUTE IMMEDIATE 'GRANT ROLE agent_' || agent_name || '_role TO ROLE ' || role_name;
   RETURN 'Access reinstated for ' || agent_name;
   END;
   ```
2. Configure a threshold beyond 100% with a stored procedure that reinstates access. This allows you to raise the effective budget for exception periods. Access is revoked again when spending reaches 200% of the budget:

   Copy code

   ```
   -- Add grants for this procedure
   GRANT USAGE ON DATABASE budgets_db TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON SCHEMA budgets_db.budgets_schema TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON PROCEDURE budgets_db.budgets_schema.sp_revoke_agent_access(STRING, STRING)
   TO APPLICATION SNOWFLAKE;

   -- Issue a reinstatement for a subset of users
   CALL budgets_db.budgets_schema.sp_reinstate_agent_access('my_agent', 'power_user_role');

   -- Set another threshold at 200% as a hard stop
   CALL budgets_db.budgets_schema.my_budget!ADD_CUSTOM_ACTION(
   SYSTEM$REFERENCE(
      'PROCEDURE',
      'budgets_db.budgets_schema.sp_revoke_agent_access(string, string)'
   ),
   ARRAY_CONSTRUCT('my_agent', 'power_user_role'),
   'ACTUAL',
   200
   );
   ```

### Reinstate access

To ensure that users can access Cortex Agents again at the start of the next budget period, set the following stored procedure to be called when the budget cycle restarts.

1. Create a stored procedure to reinstate access to the role:

   Copy code

   ```
   -- Create a stored procedure that reinstates access to the Cortex Agent object
   CREATE OR REPLACE PROCEDURE budgets_db.budgets_schema.sp_reinstate_agent_access(
   agent_name STRING, role_name STRING
   )
   RETURNS STRING
   LANGUAGE SQL
   AS
   BEGIN
   EXECUTE IMMEDIATE 'GRANT ROLE agent_' || agent_name || '_role TO ROLE ' || role_name;
   RETURN 'Access reinstated for ' || agent_name;
   END;
   ```
2. Set a cycle-start action for the budget:

   Copy code

   ```
   GRANT USAGE ON DATABASE budgets_db TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON SCHEMA budgets_db.budgets_schema TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON PROCEDURE budgets_db.budgets_schema.sp_reinstate_agent_access(STRING, STRING)
   TO APPLICATION SNOWFLAKE;

   CALL budgets_db.budgets_schema.my_budget!SET_CYCLE_START_ACTION(
   SYSTEM$REFERENCE('PROCEDURE', 'budgets_db.budgets_schema.sp_reinstate_agent_access(string, string)'),
   ARRAY_CONSTRUCT('my_agent', 'power_user_role')
   );
   ```

### Setting alerts based on projected spend

To receive an alert or perform an action based on forecasted spend rather than actual spend, you can set the trigger type to `PROJECTED`. For example, to call a stored procedure named `alert_team` when projected consumption reaches 75% of the budget limit, run the following command:

Copy code

```
CALL budget_db.sch1.my_budget!ADD_CUSTOM_ACTION(
   SYSTEM$REFERENCE('PROCEDURE', 'code_db.sch1.alert_team(string, string, string)'),
   ARRAY_CONSTRUCT('admin@example.com', 'Budget Alert', 'Spending at 75% of budget limit'),
   'PROJECTED',
   75);
```

## List custom actions

- To list all custom actions configured on a budget, use the [GET\_CUSTOM\_ACTIONS](/sql-reference/classes/budget/methods/get_custom_actions) method:

  Copy code

  ```
  -- View all custom actions on the budget
  CALL budgets_db.budgets_schema.my_budget!GET_CUSTOM_ACTIONS();
  ```

For more information, see [Custom actions for budgets](/user-guide/budgets/custom-actions).

## Monitor usage

- To view credit consumption per Cortex Agent object, use the budget’s usage reporting method:

  Copy code

  ```
  -- View usage for the current month
  CALL budgets_db.budgets_schema.my_budget!GET_SERVICE_TYPE_USAGE_V2(
  '2026-02',
  '2026-03'
  );
  ```

  The output includes the following columns:

  > | Column | Description |
  > | --- | --- |
  > | Service type | The service category (AI) |
  > | Entity type | The object type (CORTEX\_AGENT) |
  > | Entity ID | The unique identifier of the Cortex Agent object |
  > | Name | The display name of the Cortex Agent object |
  > | Credits used | The total credits consumed during the specified period |
  > | Credits Cloud | Number of cloud service credits used |
  >
  > Expand
  >
  > Show lessSee more

## Budget enforcement latency

Budget calculations and threshold enforcement are conducted periodically:

1. Snowflake calculates credit consumption for the tagged Cortex Agent object.
2. The system evaluates spending against all configured thresholds.
3. If a threshold is reached, the associated stored procedure is executed.
4. Usage dashboards are updated with the latest figures.

If you have enabled the low latency budget, your budgets are enforced in two hours after the budget is exceeded. Otherwise, it may take up to eight hours after the budget is exceeded for enforcement. You can trigger budget execution more frequently, such as every sixty minutes, to reduce the [refresh interval](/user-guide/budgets#label-budgets-refresh-interval).

Warning

There is an inherent delay between when credits are consumed and when the budget system detects the
threshold breach. During the enforcement interval, spending can exceed the configured threshold before
the action is executed. Plan your thresholds accordingly. For example, set an alert at 80% to give you time
to respond before the 100% action is triggered.

## Limitations

The following limitations apply to resource budgets for Cortex Agents:

- **Single-team resources only:** Resource budgets apply to the entire Cortex Agent object.
- **Enforcement latency:** Budget enforcement runs on a periodic cycle and may take up to eight hours after the budget is exceeded to enforce the budget. Spending can exceed a threshold during the interval before the action triggers.
- **Role-based access revocation:** To revoke access at a threshold, you must create a dedicated role for
  the Cortex Agent object.
- **Monthly period:** Budgets operate on a monthly cycle. You can’t configure resource budget periods.
- **Tag latency:** When you change a tag on an object, it can take up to eight hours after the change to be
  reflected in budgets that use tags. For more information, see [Custom budgets](/user-guide/budgets/custom-budget).
- **Entry point determines attribution:** If a request starts in Snowflake CoWork and invokes a Cortex Agent,
  that usage is attributed to Snowflake CoWork. As a result, a budget whose scope includes only
  Cortex Agent-tagged resources (for example, tags applied only to agents) does not capture credits from
  requests initiated in Snowflake CoWork, even when those requests invoke a Cortex Agent.
  To cover this usage, include Snowflake CoWork resources in budget scope, or configure a separate
  Snowflake CoWork resource budget (see [Resource budgets for Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/cowork-resource-budgets)).
  Note, however, that Snowflake CoWork-scoped budgets apply to all usage attributed to the scoped
  Snowflake CoWork objects, not only to requests that invoke a specific Cortex Agent.
