# Cycle-start actions for budgets

You can configure a budget to automatically call a stored procedure when the budget cycle restarts. The cycle restarts when spending is
reset to 0 at the beginning of the budget’s monthly period. This lets you run automated actions at the beginning of each budget period,
such as re-enabling warehouses or sending notifications about the new cycle.

Cycle-start actions are particularly useful for cleaning up or reversing actions that were triggered by
[custom actions](/user-guide/budgets/custom-actions) during the previous budget cycle.

When you define a cycle-start action, you specify the stored procedure to call and the arguments to pass to it. The stored
procedure executes automatically each time the budget cycle restarts.

## Stored procedure requirements

The stored procedure that is called by a cycle-start action must meet the following requirements:

- The procedure must run with owner’s rights, not caller’s rights. For more information, see
  [Understanding caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights).
- The procedure can’t take more than 30 minutes to complete.
- The procedure can’t have an OUTPUT argument.
- Design your procedure to handle being called multiple times without causing duplicate or
  unintended effects.
- The procedure’s required arguments must be one of the following data types:
  - [Numeric data types](/sql-reference/data-types-numeric)
  - [String & binary data types](/sql-reference/data-types-text)
  - [Logical data types](/sql-reference/data-types-logical)
  - [Date & time data types](/sql-reference/data-types-datetime)

After you’ve created a stored procedure that meets these requirements, you must grant to the SNOWFLAKE application the USAGE privilege on
the procedure and its parent database and schema. For example, if the fully qualified name of your stored procedure is
`code_db.sch1.reset_resources`, run the following commands:

Copy code

```
GRANT USAGE ON DATABASE code_db TO APPLICATION SNOWFLAKE;
GRANT USAGE ON SCHEMA code_db.sch1 TO APPLICATION SNOWFLAKE;
GRANT USAGE ON PROCEDURE code_db.sch1.reset_resources(STRING, STRING) TO APPLICATION SNOWFLAKE;
```

Note

If you update the stored procedure after adding it as a cycle-start action, you must re-grant the USAGE privilege on the procedure to the
SNOWFLAKE application.

## Set a cycle-start action for a budget

You can set one cycle-start action per budget (either the account budget or a custom budget). A cycle-start action consists of the
following components:

- Stored procedure: A reference to the procedure to be called when the budget cycle restarts.
- Arguments: An array of arguments to pass to the stored procedure.

To set a cycle-start action for a budget, call the [SET\_CYCLE\_START\_ACTION](/sql-reference/classes/budget/methods/set_cycle_start_action)
method on the budget instance. For example, the following code sets a cycle-start action that calls the `reset_resources` stored
procedure when the budget cycle restarts:

Copy code

```
CALL budget_db.sch1.my_budget!SET_CYCLE_START_ACTION(
  SYSTEM$REFERENCE('PROCEDURE', 'code_db.sch1.reset_resources(STRING, STRING, STRING, STRING)'),
  ARRAY_CONSTRUCT('my_int', 'admin@example.com', 'Budget Alert', 'New budget cycle started'));
```

For an end-to-end example that includes creating the stored procedure that is called by the cycle-start action, see
[Extended example](#label-budget-cycle-start-actions-extended-example).

## Remove a cycle-start action from a budget

To remove a cycle-start action from a budget, call the [REMOVE\_CYCLE\_START\_ACTION](/sql-reference/classes/budget/methods/remove_cycle_start_action)
method on the budget instance:

Copy code

```
CALL budget_db.sch1.my_budget!REMOVE_CYCLE_START_ACTION();
```

## Extended example

The following example demonstrates how to write a stored procedure called by a cycle-start action, grant the necessary privileges on the
procedure, and then set the cycle-start action for the budget.

1. Create a stored procedure that [conforms to all the requirements](#label-budget-cycle-start-actions-stored-procedure):

   Copy code

   ```
   CREATE OR REPLACE PROCEDURE code_db.sch1.reset_resources(
    integration_name STRING,
    email_list STRING,
    email_subject STRING,
    email_content STRING)
   RETURNS STRING
   LANGUAGE JAVASCRIPT
   EXECUTE AS OWNER
   AS
   $$
    // Re-enable warehouses or reset configurations here
    var enable_wh = "ALTER WAREHOUSE my_warehouse RESUME;";
    var statement1 = snowflake.createStatement({sqlText: enable_wh});
    statement1.execute();

    // Send notification about new cycle
    var sql_command = "CALL SYSTEM$SEND_EMAIL('" + INTEGRATION_NAME + "', " +
                                            "'" + EMAIL_LIST + "', " +
                                            "'" + EMAIL_SUBJECT + "'," +
                                            "'" + EMAIL_CONTENT + "'" + ");";
    var statement2 = snowflake.createStatement({sqlText: sql_command});
    statement2.execute();
    return "Resources reset for new budget cycle";
   $$;
   ```
2. Grant privileges on the stored procedure to the SNOWFLAKE application:

   Copy code

   ```
   GRANT USAGE ON DATABASE code_db TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON SCHEMA code_db.sch1 TO APPLICATION SNOWFLAKE;
   GRANT USAGE ON PROCEDURE code_db.sch1.reset_resources(STRING, STRING, STRING, STRING)
     TO APPLICATION SNOWFLAKE;
   ```
3. Set the cycle-start action for the budget:

   Copy code

   ```
   CALL budget_db.sch1.my_budget!SET_CYCLE_START_ACTION(
     SYSTEM$REFERENCE('PROCEDURE', 'code_db.sch1.reset_resources(STRING, STRING, STRING, STRING)'),
     ARRAY_CONSTRUCT('my_int', 'admin@example.com', 'Budget Cycle Restarted', 'New budget cycle has begun'));
   ```

## Troubleshooting cycle-start actions

If a cycle-start action is not working as expected, use the following methods to diagnose the issue.

### Monitor cycle-start action execution

Snowflake uses a task to execute the cycle-start action. This tasks is named `_budget_cycle_start_task`. To check the
execution status of the cycle-start action task for a budget instance, run the following query. Replace `budget_name` with the name of
your budget.

Copy code

```
SELECT th.*, ci.name AS budget_name
  FROM SNOWFLAKE.ACCOUNT_USAGE.TASK_HISTORY th
  JOIN SNOWFLAKE.ACCOUNT_USAGE.CLASS_INSTANCES ci
    ON th.instance_id = ci.id
  WHERE ci.class_name = 'BUDGET'
    AND th.name ILIKE '_budget_cycle_start_task'
    AND ci.name = '<budget_name>'
  ORDER BY th.completed_time DESC
  LIMIT 10;
```

### Troubleshoot actions that aren’t triggering

If a cycle-start action is not triggering when expected, check for the following common issues. Assume your custom budget is
`budget_db.sch1.my_budget`.

**Stored procedure or privileges changed**

Verify that the stored procedure called by the cycle-start action is still valid and that the SNOWFLAKE application still has necessary
privileges. You can verify the privileges by running:

Copy code

```
SHOW GRANTS ON PROCEDURE code_db.sch1.reset_resources(STRING, STRING, STRING, STRING);
```

**Budget is not activated**

For account budgets only, verify that the budget is activated by calling the
[GET\_CONFIG](/sql-reference/classes/budget/methods/get_config) method and checking the `is_active` field.

Copy code

```
CALL budget_db.sch1.my_budget!GET_CONFIG();
```

**No cycle-start action is configured**

Verify that a cycle-start action is configured for the budget:

Copy code

```
CALL budget_db.sch1.my_budget!GET_CYCLE_START_ACTION();
```

**Budget cycle has not restarted yet**

The cycle-start action triggers only when the budget cycle restarts. Check when the current cycle began and when it will end
to determine when the next trigger will occur.
