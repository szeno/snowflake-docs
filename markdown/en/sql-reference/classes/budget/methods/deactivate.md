# account\_root\_budget!DEACTIVATE

Deactivate the account [budget](/user-guide/budgets).

See also:
:   [account\_root\_budget!ACTIVATE](/sql-reference/classes/budget/methods/activate)

## Syntax

Copy code

```
CALL account_root_budget!DEACTIVATE()
```

## Returns

```
Deactivated!
```

## Access control requirements

The role used to call this method must be granted the following role and privilege:

- BUDGET\_ADMIN [application role](/user-guide/budgets#label-budgets-application-roles)
- [Snowflake database role](/sql-reference/snowflake-db-roles) USAGE\_VIEWER

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- After you deactivate the account budget, you can no longer create new custom budgets using Snowsight.
  However, you can continue to create custom budgets using SQL.
- This method is only available on the account budget. Custom budgets can’t be deactivated. They must be dropped using
  the [DROP BUDGET](/sql-reference/classes/budget/commands/drop-budget) command.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Example

Deactivate the account budget for your account:

Copy code

```
CALL snowflake.local.account_root_budget!DEACTIVATE();
```
