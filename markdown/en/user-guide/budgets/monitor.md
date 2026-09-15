# Monitor budgets

This topic describes how to monitor budget spending and identify the budget that tracks the credit usage of a specific resource.

## Creating a custom role to monitor budgets

You can delegate budget monitoring by creating a custom role that can be used by non-administrator users to monitor budgets.

### Create a custom role to monitor the account budget

You can create a custom role to enable non-account administrator users to monitor the account budget. For a full list of privileges
and roles that must be granted to a role to monitor the account budget, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

#### Example

Note

Only an account administrator can execute the statements in this example.

For example, create role `account_budget_monitor` and grant the role the ability to view credit usage for the
account budget:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE account_budget_monitor;

GRANT APPLICATION ROLE SNOWFLAKE.BUDGET_VIEWER TO ROLE account_budget_monitor;

GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE account_budget_monitor;
```

### Create a custom role to monitor a custom budget

You can create a custom role to enable non-account administrator users to monitor custom budgets. For a full list of privileges
and roles that must be granted to a role to monitor a custom budget, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

#### Example

Note

Only a budget owner (a role with the OWNERSHIP privilege) can execute the statements in this example.

Use the budget owner role to grant the custom role `budget_monitor` the ability to monitor the budget `my_budget` in schema
`budgets_db.budgets_schema`:

Copy code

```
USE ROLE custom_budget_owner;

GRANT USAGE ON DATABASE budgets_db TO ROLE budget_monitor;

GRANT USAGE ON SCHEMA budget_db.budgets_schema TO ROLE budget_monitor;

GRANT SNOWFLAKE.CORE.BUDGET ROLE budgets_db.budgets_schema.my_budget!VIEWER
  TO ROLE budget_monitor;

GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER TO ROLE budget_monitor;
```

## Monitoring budgets

You can monitor budgets using Snowsight or SQL.

### Use Snowsight to monitor budgets

You can view current and historical budget spending using the **Budgets** page in Snowsight.

Note

Only a user with the ACCOUNTADMIN role or a role granted the required privileges and role
can monitor budgets using Snowsight.

- For more information about using a custom account role to monitor the account budget, see [Create a custom role to monitor the account budget](#label-account-budget-monitor-role).
- For more information about using a custom account role to monitor custom budgets, see [Create a custom role to monitor a custom budget](#label-custom-budgets-monitor-role).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Cost management**.
3. Select **Budgets**.

In the **Current Month** view for a budget, you can review the credit usage per day up to the current day. You can see whether
you might exceed your budget for the month. The bar graph continues to the end of the month with your projected credit usage based on your
actual credit usage for the month. The **Spending limit** line indicates the spending limit at which a budget notification is triggered.

Select [![Clock icon](/static/images/snowsight/icons/clock-time-period-icon.svg)](/static/images/snowsight/icons/clock-time-period-icon.svg) (months to display) to filter the view by **Current Month** or longer time periods.

You can compare the **Spend** (current credit usage) to **Interval** (time left in the current month) to see if
your spending is outpacing your monthly budget.

You can filter the view by selecting [![Budgets icon](/static/images/snowsight/icons/budgets-icon.svg)](/static/images/snowsight/icons/budgets-icon.svg) **Budgets** or [![Resources icon](/static/images/snowsight/icons/resources-icon.svg)](/static/images/snowsight/icons/resources-icon.svg) **Resources**:

- You can select a custom budget in the **Budgets** view for details on a specific budget.

  Note

  The **Service Type** list for a custom budget includes an **Unused Resources** type. This service type is displayed
  when an object in a budget has no credit usage data to display. This can happen if the object has no credit usage for
  compute costs, or if you recently added an object to a budget and the [serverless background task](/user-guide/budgets/cost)
  has not yet executed.
- In the **Resources** view, you can filter and sort by **Service Type**, object **Name**, and **Credit Usage**.

### Use SQL commands to monitor budgets

To monitor the account budget, you must have the required privileges. For more information, see [Create a custom role to monitor the account budget](#label-account-budget-monitor-role).

Use the `account_budget_monitor` role to view the spending history for the account budget:

Copy code

```
USE ROLE account_budget_monitor;

CALL snowflake.local.account_root_budget!GET_SPENDING_HISTORY(
  TIME_LOWER_BOUND => DATEADD('days', -7, CURRENT_TIMESTAMP()),
  TIME_UPPER_BOUND => CURRENT_TIMESTAMP()
);
```

You can monitor the spending history by service type. To view the spending history for the search optimization serverless feature
for the account budget in an eight-month period, execute the following statements:

Copy code

```
USE ROLE account_budget_monitor;

SELECT *
   FROM table(snowflake.local.account_root_budget!GET_SERVICE_TYPE_USAGE_V2(
         '2025-05', '2025-12'))
   WHERE service_type = 'SEARCH_OPTIMIZATION';
```

To monitor a custom budget, you must have the required privileges. For more information, see [Create a custom role to monitor a custom budget](#label-custom-budgets-monitor-role).

Use the `budget_monitor` role to view spending history for a custom budget. For example, to view the spending history for custom
budget `na_finance_budget` in schema `budgets_db.budgets_schema`, execute the following statements:

Copy code

```
USE ROLE budget_monitor;

CALL budgets_db.budgets_schema.na_finance_budget!GET_SPENDING_HISTORY(
  TIME_LOWER_BOUND => DATEADD('days', -7, CURRENT_TIMESTAMP()),
  TIME_UPPER_BOUND => CURRENT_TIMESTAMP()
);
```

You can monitor the spending history by service type. For example, to view the spending history in a one year period for the materialized
views included in the budget, execute the following statements:

Copy code

```
USE ROLE budget_monitor;

SELECT *
   FROM table(budgets_db.budgets_schema.na_finance_budget!GET_SERVICE_TYPE_USAGE_V2(
         '2025-05', '2025-12'))
   WHERE service_type = 'MATERIALIZED_VIEW';
```

For more information, see [Budget methods](/sql-reference/classes/budget#label-budget-methods).

## Identifying the budgets that track a resource

If you want to determine which budgets track a resource, you can call the
[SYSTEM$SHOW\_BUDGETS\_FOR\_RESOURCE](/sql-reference/functions/system_show_budgets_for_resource) function.

For example:

Copy code

```
SELECT SYSTEM$SHOW_BUDGETS_FOR_RESOURCE('TABLE', 'my_db.my_schema.my_table');
```

```
+-----------------------------------------------------------------------+
| SYSTEM$SHOW_BUDGETS_FOR_RESOURCE('TABLE', 'MY_DB.MY_SCHEMA.MY_TABLE') |
|-----------------------------------------------------------------------|
| [BUDGETS_DB.BUDGETS_SCHEMA.MY_BUDGET]                                 |
+-----------------------------------------------------------------------+
```

The function returns the budget that the resource has been added to. It includes budgets that include the resource because of any of the following reasons:

- The resource was added directly to the budget.
- The resource has the tag/value combination that was added to the budget.
- The resource belongs to an object (for example, a database) that was added to the budget.
