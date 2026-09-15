# Resource budgets for Cortex Search

A resource budget lets you monitor Cortex Search spend and take automated actions, such as revoking access, when consumption exceeds configured limits. Budgets apply at an aggregated level to credits consumed by a specific Cortex Search service.

## How resource budgets work

Resource budgets use Snowflake’s tag-based cost attribution model. You create a tag, apply it to a
Cortex Search service, and then associate that tag with a budget. Snowflake tracks credit consumption for
the tagged service and evaluates spending against the budget limit periodically. The resource budget is
useful for limiting spending for the Cortex Search service.

Snowflake enforces resource budgets with the following flow:

1. You create a tag.
2. You apply the tag to the Cortex Search service.
3. You create a budget and specify the tag to track spending for. As part of creating the budget, you also set a monthly spending limit in credits.
4. You add a stored procedure to be executed when spending reaches a configured threshold of the budget. For example, you can invoke a stored procedure for alerting at 80% and another stored procedure for revoking access at 100%.
5. Snowflake tracks credit consumption for the tagged service.
6. When spending reaches a configured threshold of the budget, such as 80% or 100%, Snowflake executes the stored procedure defined for that threshold.

Snowflake calculates usage, evaluates thresholds, and triggers any configured actions periodically.
After the budget is exceeded, it might take up to eight hours with the standard budget (or two hours with the latency-optimized option) for the budget to be enforced.

## Create a tag

1. Create a tag to identify the cost center associated with the Cortex Search service:

   Copy code

   ```
   -- Create a tag with allowed cost center values
   CREATE TAG cost_mgmt_db.tags.cost_center
   ALLOWED_VALUES 'org-level'
   COMMENT = 'cost_center tag';
   ```
2. Apply the tag to the Cortex Search service to associate it with a cost center:

   Copy code

   ```
   -- Apply the cost center tag to the Cortex Search service
   ALTER CORTEX SEARCH SERVICE IF EXISTS my_search_service
     SET TAG cost_mgmt_db.tags.cost_center = 'org-level';
   ```

## Set up a resource budget

You can use either Snowsight or SQL to create a budget and associate it with a Cortex Search service.

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
12. For **Budget scope**, add the tag on the Cortex Search service to the resource budget.
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
3. Add the tag to the budget so that Snowflake tracks spending for the tagged service against this budget:

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

Now, Snowflake tracks credit consumption for `my_search_service` against the `my_budget` budget
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

### Revoke access and suspend the service

1. Create a stored procedure that revokes access to the Cortex Search service and suspends the service to stop ongoing costs. In the stored procedure, you can limit access to a specific role to revoke USAGE for that role. Suspending both the indexing and serving layers stops warehouse compute, embedding, and serving charges for the service.

   Copy code

   ```
   -- Create a stored procedure that revokes access and suspends the Cortex Search service
   CREATE OR REPLACE PROCEDURE budgets_db.budgets_schema.sp_revoke_search_access(
   service_name STRING, role_name STRING
   )
   RETURNS STRING
   LANGUAGE SQL
   AS
   BEGIN
   EXECUTE IMMEDIATE 'REVOKE USAGE ON CORTEX SEARCH SERVICE ' || service_name || ' FROM ROLE ' || role_name;
   EXECUTE IMMEDIATE 'ALTER CORTEX SEARCH SERVICE ' || service_name || ' SUSPEND';
   RETURN 'Access revoked and service suspended for ' || service_name;
   END;
   ```

   Important

   Ensure the `role_name` and the user do not have access to the Cortex Search service through other roles. The role that runs this stored procedure must have the OPERATE privilege on the Cortex Search service to suspend it. For guidance about configuring roles and privileges correctly, see [Required privileges](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-privileges).
2. Set a custom action that blocks access when 100% of the budget has been spent. You can also use custom actions for notifications.

   Copy code

   ```
   -- Provide access to the stored procedures
   GRANT USAGE ON DATABASE budgets_db TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON SCHEMA budgets_db.budgets_schema TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON PROCEDURE budgets_db.budgets_schema.sp_revoke_search_access(STRING, STRING)
   TO APPLICATION SNOWFLAKE;

   -- Block access at 100% of the budget
   CALL budgets_db.budgets_schema.my_budget!ADD_CUSTOM_ACTION(
   SYSTEM$REFERENCE('PROCEDURE',
      'budgets_db.budgets_schema.sp_revoke_search_access(string, string)'),
   ARRAY_CONSTRUCT('SERVICE_NAME', 'ROLE_NAME'),
   'ACTUAL',
   100);
   ```

> Note
>
> You can also use custom actions to take action when spending is forecasted to exceed the budget limit. For more information, see [Custom actions for budgets](/user-guide/budgets/custom-actions).

### Handling exceptions to spending limits

In some cases, you may need to reinstate access after the budget limit is reached, such as during earnings season or
other peak periods. You can configure thresholds beyond 100%, up to 500%, to handle these exception
scenarios.

The workflow assumes that access is revoked and the service is suspended using the configured stored procedure when spending reaches a budget threshold. The admin reinstates
a subset of the users and grants access back. When spending reaches 200%, the revocation procedure runs
again as a hard stop.

1. Create a stored procedure to resume the service and reinstate access to the role:

   Copy code

   ```
   -- Create a stored procedure that resumes the Cortex Search service and reinstates access
   CREATE OR REPLACE PROCEDURE budgets_db.budgets_schema.sp_reinstate_search_access(
   service_name STRING, role_name STRING
   )
   RETURNS STRING
   LANGUAGE SQL
   AS
   BEGIN
   EXECUTE IMMEDIATE 'ALTER CORTEX SEARCH SERVICE ' || service_name || ' RESUME';
   EXECUTE IMMEDIATE 'GRANT USAGE ON CORTEX SEARCH SERVICE ' || service_name || ' TO ROLE ' || role_name;
   RETURN 'Service resumed and access reinstated for ' || service_name;
   END;
   ```
2. During an exception period, an admin manually reinstates access by calling the reinstatement procedure. Configure a 200% threshold as a hard stop so the revocation procedure runs again if spending continues to grow:

   Copy code

   ```
   -- Issue a reinstatement for a subset of users
   CALL budgets_db.budgets_schema.sp_reinstate_search_access('my_search_service', 'power_user_role');

   -- Set another threshold at 200% as a hard stop
   CALL budgets_db.budgets_schema.my_budget!ADD_CUSTOM_ACTION(
   SYSTEM$REFERENCE(
      'PROCEDURE',
      'budgets_db.budgets_schema.sp_revoke_search_access(string, string)'
   ),
   ARRAY_CONSTRUCT('my_search_service', 'power_user_role'),
   'ACTUAL',
   200
   );
   ```

### Reinstate access

To ensure that users can access the Cortex Search service again at the start of the next budget period, configure the `sp_reinstate_search_access` procedure from the previous section to run when the budget cycle restarts.

1. Set a cycle-start action for the budget:

   Copy code

   ```
   GRANT USAGE ON DATABASE budgets_db TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON SCHEMA budgets_db.budgets_schema TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON PROCEDURE budgets_db.budgets_schema.sp_reinstate_search_access(STRING, STRING)
   TO APPLICATION SNOWFLAKE;

   CALL budgets_db.budgets_schema.my_budget!SET_CYCLE_START_ACTION(
   SYSTEM$REFERENCE('PROCEDURE', 'budgets_db.budgets_schema.sp_reinstate_search_access(string, string)'),
   ARRAY_CONSTRUCT('my_search_service', 'power_user_role')
   );
   ```

### Setting alerts based on projected spend

To receive an alert or perform an action based on forecasted spend rather than actual spend, you can set the trigger type to `PROJECTED`. For example, to call a stored procedure named `alert_team` when projected consumption reaches 75% of the budget limit, run the following command:

Copy code

```
CALL budgets_db.budgets_schema.my_budget!ADD_CUSTOM_ACTION(
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

- To view credit consumption per Cortex Search service, use the budget’s usage reporting method:

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
  > | Entity type | The object type (CORTEX\_SEARCH\_SERVICE) |
  > | Entity ID | The unique identifier of the Cortex Search service |
  > | Name | The display name of the Cortex Search service |
  > | Credits used | The total credits consumed during the specified period |
  > | Cloud services credits | Number of cloud service credits used |
  >
  > Expand
  >
  > Show lessSee more

## Budget enforcement latency

Budget calculations and threshold enforcement are conducted periodically:

1. Snowflake calculates credit consumption for the tagged Cortex Search service.
2. The system evaluates spending against all configured thresholds.
3. If a threshold is reached, the associated stored procedure is executed.
4. Usage dashboards are updated with the latest figures.

If you have enabled the low latency budget, your budgets are enforced within two hours after the budget is exceeded. Otherwise, it may take up to eight hours after the budget is exceeded for enforcement. You can trigger budget execution more frequently, such as every 60 minutes, to reduce the [refresh interval](/user-guide/budgets#label-budgets-refresh-interval).

Warning

There is an inherent delay between when credits are consumed and when the budget system detects the
threshold breach. During the enforcement interval, spending can exceed the configured threshold before
the action is executed. Plan your thresholds accordingly. For example, set an alert at 80% to give you time
to respond before the 100% action is triggered.

## Limitations

The following limitations apply to resource budgets for Cortex Search:

- **Single-service resources only:** Resource budgets apply to the entire Cortex Search service.
- **Enforcement latency:** Budget enforcement runs on a periodic cycle and may take up to eight hours after the budget is exceeded to enforce the budget. Spending can exceed a threshold during the interval before the action triggers.
- **Role-based access revocation and service suspension:** To revoke access at a threshold, you must revoke USAGE on the Cortex Search service from the affected roles. To stop ongoing indexing and serving costs, suspend the service using `ALTER CORTEX SEARCH SERVICE ... SUSPEND`.
- **Monthly period:** Budgets operate on a monthly cycle. You can’t configure resource budget periods.
- **Tag latency:** When you change a tag on an object, it can take up to eight hours after the change to be
  reflected in budgets that use tags. For more information, see [Custom budgets](/user-guide/budgets/custom-budget).
