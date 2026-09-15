# Custom actions for budgets

You can configure a budget to automatically call a stored procedure when a spending threshold is reached. This lets you take automated
actions in response to credit consumption, such as suspending warehouses, sending custom alerts, or logging spending events to a table.
Custom actions don’t replace the [notifications](/user-guide/budgets/notifications) that Snowflake sends when consumption is expected
to exceed your budget limit.

When you define a custom action, you specify whether it calls the stored procedure based on *projected* credit consumption or *actual*
credit consumption, and then set the threshold. When projected or actual consumption reaches the threshold, the stored procedure executes.

## Stored procedure requirements

The stored procedure that is called by a custom action must meet the following requirements:

- The procedure must run with owner’s rights, not caller’s rights. For more information, see
  [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).
- The procedure can’t take more than 30 minutes to complete.
- The procedure can’t have an OUTPUT argument.
- Snowflake retries failed actions once, so design your procedure to handle being called multiple times without causing duplicate or
  unintended effects.
- The procedure’s required arguments must be one of the following data types:
  - [Numeric data types](/sql-reference/data-types-numeric)
  - [String & binary data types](/sql-reference/data-types-text)
  - [Logical data types](/sql-reference/data-types-logical)
  - [Date & time data types](/sql-reference/data-types-datetime)

After you’ve created a stored procedure that meets these requirements, you must grant to the SNOWFLAKE application the USAGE privilege on
the procedure and its parent database/schema. For example, if the fully qualified name of your stored procedure is
`code_db.sch1.alert_team`, run the following commands:

Copy code

```
GRANT USAGE ON DATABASE code_db TO APPLICATION SNOWFLAKE;
GRANT USAGE ON SCHEMA code_db.sch1 TO APPLICATION SNOWFLAKE;
GRANT USAGE ON PROCEDURE code_db.sch1.alert_team(STRING, NUMBER) TO APPLICATION SNOWFLAKE;
```

Note

If you update the stored procedure after adding it to a custom action, you must re-grant the USAGE privilege on the procedure to the
SNOWFLAKE application.

## Add a custom action to a budget

You can add multiple custom actions to the account budget or to a custom budget, but you can’t add more than 10 custom actions to the same
budget. A custom action consists of the following components:

- Stored procedure: A reference to the procedure to be called.
- Arguments: An array of arguments to pass to the stored procedure.
- Threshold: The percentage of the budget limit that triggers the custom action (for example, 75%).
- Trigger type: Whether the custom action is triggered based on projected consumption or actual consumption.

To add a custom action to a budget, call the [ADD\_CUSTOM\_ACTION](/sql-reference/classes/budget/methods/add_custom_action) method on
the budget instance. For example, the following code adds a custom action that calls the `send_email_notification` stored procedure
when spending is forecast to exceed 75% of the budget limit:

Copy code

```
CALL budget_db.sch1.my_budget!ADD_CUSTOM_ACTION(
  SYSTEM$REFERENCE('PROCEDURE', 'code_db.sch1.alert_team(string, string, string)'),
  ARRAY_CONSTRUCT('admin@example.com', 'Budget Alert', 'Spending at 75% of budget limit'),
  'PROJECTED',
  75);
```

For an end-to-end example that includes creating the stored procedure that is called by the custom action, see [Extended example](#label-budget-custom-actions-extended-example).

## Remove a custom action from a budget

To remove a custom action from a budget, call the [REMOVE\_CUSTOM\_ACTIONS](/sql-reference/classes/budget/methods/remove_custom_actions)
method on the budget instance. You can use this method to do the following:

- **Remove all custom actions from a budget**. For example:

  Copy code

  ```
  CALL budget_db.sch1.my_budget!REMOVE_CUSTOM_ACTIONS();
  ```
- **Remove all custom actions that have a specified threshold**. For example, to remove all custom actions that are triggered when
  consumption reaches 75%, run the following command:

  Copy code

  ```
  CALL budget_db.sch1.my_budget!REMOVE_CUSTOM_ACTIONS(75);
  ```
- **Remove a specified custom action from a budget**. For example, to remove the custom action that calls the `my_sp` stored procedure
  when consumption reaches 75%, run the following command:

  Copy code

  ```
  CALL budget_db.sch1.my_budget!REMOVE_CUSTOM_ACTIONS(75, 'code_db.sch1.my_sp');
  ```

  Tip

  If you are removing a specific action, use the fully qualified procedure name that is returned by the
  [GET\_CUSTOM\_ACTIONS](/sql-reference/classes/budget/methods/get_custom_actions) method.

## Extended example

The following example demonstrates how to write a stored procedure called by a custom action, grant the necessary privileges on the
procedure, and then add the custom action to the budget.

1. Create a stored procedure that [conforms to all the requirements](#label-budget-custom-actions-stored-procedure):

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE code_db.sch1.alert_team(
    integration_name string,
    email_list string,
    email_subject string,
    email_content string)
   RETURNS STRING
   LANGUAGE JAVASCRIPT
   EXECUTE AS OWNER
   AS
   $$
    var sql_command = "CALL SYSTEM$SEND_EMAIL('" + INTEGRATION_NAME + "', " +
                                            "'" +  EMAIL_LIST + "', " +
                                            "'" + EMAIL_SUBJECT + "'," +
                                            "'" + EMAIL_CONTENT + "'" + ");";
    var statement1 = snowflake.createStatement({sqlText: sql_command});
    statement1.execute();
    return "alert sent";
   $$;
   ```
2. Grant privileges on the stored procedure to the SNOWFLAKE application:

   Copy code

   ```
   GRANT USAGE ON DATABASE code_db TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON SCHEMA code_db.sch1 TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON PROCEDURE code_db.sch1.alert_team(STRING, STRING, STRING, STRING)
     TO APPLICATION SNOWFLAKE;
   ```
3. Add the custom action to the budget so that it is triggered when consumption reaches 90% of the budget’s spending limit:

   Copy code

   ```
   CALL budget_db.sch1.my_budget!ADD_CUSTOM_ACTION(
     SYSTEM$REFERENCE('PROCEDURE', 'code_db.sch1.alert_team(string, string, string, string)'),
     ARRAY_CONSTRUCT('my_int', 'admin@example.com', 'Budget Alert', 'Spending at 90% of budget limit'),
     'ACTUAL',
     90);
   ```

## Troubleshooting custom actions

If a custom action is not working as expected, use the following methods to diagnose the issue.

### Monitor custom action execution

Snowflake uses tasks to execute custom actions. These tasks follow the naming convention `BUDGET_CUSTOM_ACTION_TRIGGER_AT_%`. To check the
execution status of all custom action tasks for a budget instance, run the following query:

Copy code

```
SELECT th.*, ci.name AS budget_name
  FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY th
  JOIN SNOWFLAKE.ACCOUNT_USAGE.CLASS_INSTANCES ci
    ON th.instance_id = ci.id
  WHERE ci.class_name = 'BUDGET'
    AND th.name ILIKE 'BUDGET_CUSTOM_ACTION_TRIGGER_AT_%'
    AND ci.name = '<budget_name>'
  ORDER BY th.completed_time DESC
  LIMIT 10;
```

### View action trigger history

To see which custom actions have been triggered from a specific budget over a time period, run the following query:

Copy code

```
SELECT th.*, ci.name as budget_name
  FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY th
  JOIN SNOWFLAKE.ACCOUNT_USAGE.CLASS_INSTANCES ci
    ON th.instance_id = ci.id
  WHERE ci.class_name = 'BUDGET'
    AND th.name ILIKE 'BUDGET_CUSTOM_ACTION_TRIGGER_AT_%'
    AND ci.name = '<budget_name>'
    AND th.COMPLETED_TIME >= DATEADD('day', -7, CURRENT_TIMESTAMP())
  ORDER BY th.completed_time DESC;
```

To check the trigger history for a specific custom action, first get the action ID by calling the
[GET\_CUSTOM\_ACTIONS](/sql-reference/classes/budget/methods/get_custom_actions) method:

Copy code

```
CALL <budget_name>!GET_CUSTOM_ACTIONS();
```

Then use the action ID in the following query:

Copy code

```
SELECT th.*, ci.name AS budget_name
  FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY th
  JOIN SNOWFLAKE.ACCOUNT_USAGE.CLASS_INSTANCES ci
    ON th.instance_id = ci.id
  WHERE ci.class_name = 'BUDGET'
    AND th.name ILIKE 'BUDGET_CUSTOM_ACTION_TRIGGER_AT_%'
    AND th.query_text ILIKE '%<action_id>%'
    AND ci.name = '<budget_name>'
    AND th.COMPLETED_TIME >= DATEADD('day', -7, CURRENT_TIMESTAMP())
  ORDER BY th.completed_time DESC;
```

### Troubleshoot actions that aren’t triggering

If a custom action is not triggering when expected, check for the following common issues. Assume your custom budget is
`budget_db.sch1.my_budget`.

**Stored procedure or privileges changed**

Verify that the stored procedure called by the custom action is still valid and that the SNOWFLAKE application still has necessary
privileges. Call the [CONFIRM\_CUSTOM\_ACTIONS\_ACCESS](/sql-reference/classes/budget/methods/confirm_custom_actions_access) method to
validate the stored procedure and access control privileges:

Copy code

```
CALL budget_db.sch1.my_budget!CONFIRM_CUSTOM_ACTIONS_ACCESS();
```

**Budget is not activated**

For account budgets only, verify that the budget is activated by calling the
[GET\_CONFIG](/sql-reference/classes/budget/methods/get_config) method and checking the `is_active` field.

Copy code

```
CALL budget_db.sch1.my_budget!GET_CONFIG();
```

**Budget has no spending limit**

Custom actions won’t trigger if the budget doesn’t have a spending limit configured. Check the spending limit:

Copy code

```
CALL budget_db.sch1.my_budget!GET_SPENDING_LIMIT();
```

**Budget is not tracking any resources**

Verify that the budget is tracking resources by checking the spending history:

Copy code

```
CALL budget_db.sch1.my_budget!GET_SPENDING_HISTORY();
```

**Custom action has recently triggered**

To prevent excessive triggering, Snowflake limits how frequently a custom action can execute:

- If the custom action runs when credit consumption is projected to reach a spending threshold, the stored procedure won’t be called more
  than once a day.
- If the custom action runs when credit consumption reaches a limit on actual spending, the stored procedure won’t be called more than once
  a month.

Check the `LAST_TRIGGER_ATTEMPT_TIME` field by calling the
[GET\_CUSTOM\_ACTIONS](/sql-reference/classes/budget/methods/get_custom_actions) method.
