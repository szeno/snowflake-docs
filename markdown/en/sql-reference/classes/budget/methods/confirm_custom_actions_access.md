# <budget\_name>!CONFIRM\_CUSTOM\_ACTIONS\_ACCESS

Validate that the stored procedures associated with [custom actions](/user-guide/budgets/custom-actions) are still valid and that required access control privileges are still granted.

To fix any problems, see [Stored procedure requirements](/user-guide/budgets/custom-actions#label-budget-custom-actions-stored-procedure).

See also:
:   [<budget\_name>!ADD\_CUSTOM\_ACTION](/sql-reference/classes/budget/methods/add_custom_action), [<budget\_name>!GET\_CUSTOM\_ACTIONS](/sql-reference/classes/budget/methods/get_custom_actions)

## Syntax

Copy code

```
<budget_name>!CONFIRM_CUSTOM_ACTIONS_ACCESS()
```

## Returns

The method returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| PROCEDURE\_FQN | VARCHAR | Fully qualified name of the stored procedure. |
| IS\_VALID | BOOLEAN | If TRUE, the stored procedure is still valid and the SNOWFLAKE application still has the required privileges on the procedure. |
| REASON | VARCHAR | Explanation of why the custom action is no longer valid. |

Expand

Show lessSee more

## Access control requirements

- The following minimum privileges and roles are required to view results for *custom budgets*:

  - Any [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
  - USAGE privilege on the database and schema that contain the budget instance.
- The following role is required to view results for the *account budget*:

  - Any [application role](/user-guide/budgets#label-budgets-application-roles) for the account budget.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Verify the stored procedures and permissions for budget `my_budget` in schema `budget_db.sch1`:

Copy code

```
CALL budget_db.sch1.my_budget!CONFIRM_CUSTOM_ACTIONS_ACCESS();
```

Verify the stored procedures and permissions for the account budget:

Copy code

```
CALL snowflake.local.account_root_budget!CONFIRM_CUSTOM_ACTIONS_ACCESS();
```
