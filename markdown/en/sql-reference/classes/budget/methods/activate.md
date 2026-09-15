# account\_root\_budget!ACTIVATE

Activate the account budget. You must activate the account budget in order
to use the [budgets](/user-guide/budgets) feature.

See also:
:   [account\_root\_budget!DEACTIVATE](/sql-reference/classes/budget/methods/deactivate)

## Syntax

Copy code

```
CALL account_root_budget!ACTIVATE()
```

## Returns

```
activated
```

## Access control requirements

Only a user with the ACCOUNTADMIN role or a role granted the following privileges can activate the account budget:

- Application role SNOWFLAKE.BUDGET\_ADMIN
- [Snowflake database role](/sql-reference/snowflake-db-roles) USAGE\_VIEWER

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- After the account budget is activated:

  - You must set the spending limit in order for the budget to start tracking credit usage.
  - You must [set up notifications for the budget](/user-guide/budgets/notifications). If you do not set up notifications
    for the budget, no notifications will be sent out.
- This method is only available on the account budget. Custom budgets do not require activation.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Example

Activate the account budget for your account:

Copy code

```
CALL snowflake.local.account_root_budget!ACTIVATE();
```

## Error messages

To troubleshoot issues with account budget activation, see [You can’t activate the account budget](/user-guide/budgets/troubleshoot#label-troubleshooting-budgets-activate).
