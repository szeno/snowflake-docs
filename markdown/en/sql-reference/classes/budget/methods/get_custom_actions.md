# <budget\_name>!GET\_CUSTOM\_ACTIONS

ListS all [custom actions](/user-guide/budgets/custom-actions) associated with a budget.

See also:
:   [<budget\_name>!ADD\_CUSTOM\_ACTION](/sql-reference/classes/budget/methods/add_custom_action), [<budget\_name>!REMOVE\_CUSTOM\_ACTIONS](/sql-reference/classes/budget/methods/remove_custom_actions)

## Syntax

Copy code

```
<budget_name>!GET_CUSTOM_ACTIONS()
```

## Returns

The method returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| ACTION\_ID | VARCHAR | Unique identifier for the combination of the stored procedure fully qualified name, array of arguments, threshold, and trigger type. |
| PROCEDURE\_FQN | VARCHAR | Fully qualified name of the stored procedure. |
| PROCEDURE\_ARGS | ARRAY | Array of arguments passed to the stored procedure. |
| SPEND\_STRATEGY | VARCHAR | Whether the custom action is triggered based on projected consumption or actual consumption. Valid values: `PROJECTED` or `ACTUAL`. |
| THRESHOLD | NUMBER | Percentage of the budget limit that triggers the stored procedure. |
| LAST\_TRIGGER\_ATTEMPT\_TIME | TIMESTAMP\_TZ | Last time the budget attempted to trigger the action, in UTC. |
| ADDED\_TIMESTAMP | TIMESTAMP\_TZ | Time when the action was added to the budget, in local time zone. |

Expand

Show lessSee more

## Access control requirements

- The following minimum privileges and roles are required to view results for *custom budgets*:

  - Any [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
  - USAGE privilege on the database and schema that contains the budget instance.
- The following role is required to view results for the *account budget*:

  - Any [application role](/user-guide/budgets#label-budgets-application-roles) for the account budget.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

## Examples

List all custom actions for budget `my_budget` in schema `budget_db.sch1`:

Copy code

```
CALL budget_db.sch1.my_budget!GET_CUSTOM_ACTIONS();
```

List all custom actions for the account budget:

Copy code

```
CALL snowflake.local.account_root_budget!GET_CUSTOM_ACTIONS();
```
