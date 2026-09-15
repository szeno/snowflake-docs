# Work with the account budget

The account budget monitors spending for all credit usage in the account.

## Activating the account budget

To start using budgets to monitor credit usage for your account, activate the account budget. After you activate the account
budget, you can set the spending limit for the account and configure how notifications are sent when credit usage is
expected to exceed the spending limit. Notifications begin when projected spending is more than 10% above the spending limit.

You can activate the account budget by using Snowsight or by executing SQL statements.

The next sections explain how to activate the account budget:

- [Create a custom role to manage the account budget](#label-account-budget-admin-role)
- [Use Snowsight to activate the account budget](#label-ui-activate-account-budget)
- [Use SQL commands to activate the account budget](#label-sql-activate-account-budget)

### Create a custom role to manage the account budget

You can create a custom role to activate and modify the account budget. A user who is granted this role can administer the budget by taking
the following actions on the account budget:

- Activate and deactivate the account budget.
- Set the spending limit.
- Edit notification settings.
- Monitor credit usage for the account.

For a full list of roles and privileges required for the budget administrator role, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

The following example creates a role named `account_budget_admin` and grants the role the ability to monitor and manage the
account budget:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE ROLE account_budget_admin;

GRANT APPLICATION ROLE SNOWFLAKE.BUDGET_ADMIN TO ROLE account_budget_admin;

GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE account_budget_admin;
```

### Use Snowsight to activate the account budget

Note

Only a user with the ACCOUNTADMIN role or a role
[granted account budget admin privileges](#label-account-budget-admin-role) can activate and set up the account budget for a regular
account.

If you are activating the account budget for the [organization account](/user-guide/organization-accounts), use the GLOBALORGADMIN
role instead of the ACCOUNTADMIN role.

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Cost management**.
3. Select **Budgets**.
4. If prompted, select a warehouse.
5. In the dashboard, select **Set up Account Budget**.
6. Enter the target spending limit for the account.
7. Enter the email addresses to receive notification emails.

   Note

   Each email address added for budget notifications must be [verified](/user-guide/notifications/email-notifications#label-email-notification-verify-address). The
   notification email setup fails if any email address in the list is *not* verified.
8. Select **Finish Setup**.

### Use SQL commands to activate the account budget

Note

Only a user with the ACCOUNTADMIN role or a role
[granted account budget admin privileges](#label-account-budget-admin-role) can activate and set up the account budget in a regular
account.

If you are activating the account budget for the [organization account](/user-guide/organization-accounts), use the GLOBALORGADMIN
role instead of the ACCOUNTADMIN role.

1. Activate the account budget by calling the [account\_root\_budget!ACTIVATE](/sql-reference/classes/budget/methods/activate) method on the
   SNOWFLAKE.LOCAL.ACCOUNT\_ROOT\_BUDGET object:

   Copy code

   ```
   CALL SNOWFLAKE.LOCAL.ACCOUNT_ROOT_BUDGET!ACTIVATE();
   ```
2. Set the spending limit calling the [<budget\_name>!SET\_SPENDING\_LIMIT](/sql-reference/classes/budget/methods/set_spending_limit) method:

   Copy code

   ```
   CALL SNOWFLAKE.LOCAL.ACCOUNT_ROOT_BUDGET!SET_SPENDING_LIMIT(1000);
   ```
3. Set up notifications for the budget so that you receive notifications when your credit usage is expected to exceed your
   spending limits.

   See [Notifications for budgets](/user-guide/budgets/notifications).

## Deactivating the account budget

You can deactivate the account budget using Snowsight or SQL.

Deactivating the account budget resets the account budget to its state before activation:

- All historical account budget data is deleted.
- The background measurement task for the account budget is suspended.
- The account budget settings for spending limit and email notifications are reset.

Account budget deactivation does not affect custom budgets. To remove a custom budget from your account, use
the [DROP BUDGET](/sql-reference/classes/budget/commands/drop-budget) command.

Note

If the account budget is deactivated, you can’t create new custom budgets using Snowsight.
However, you can continue to [create custom budgets using SQL](/user-guide/budgets/custom-budget#label-create-custom-budget-sql).

### Use Snowsight to deactivate the account budget

You can deactivate the account budget using the **Budgets** page:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Cost management**.
3. Select **Budgets**.
4. Select the [![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png) more menu.
5. Select **Deactivate account budget**.

### Use SQL commands to deactivate the account budget

You can use the [account\_root\_budget!DEACTIVATE](/sql-reference/classes/budget/methods/deactivate) method to deactivate the account budget:

Copy code

```
CALL SNOWFLAKE.LOCAL.ACCOUNT_ROOT_BUDGET!DEACTIVATE();
```
