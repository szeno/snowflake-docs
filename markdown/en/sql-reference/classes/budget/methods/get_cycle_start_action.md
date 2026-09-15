# <budget\_name>!GET\_CYCLE\_START\_ACTION

Returns the [user-defined action](/user-guide/budgets/cycle-start-actions) that is triggered when the budget cycle restarts.

See also:
:   [<budget\_name>!SET\_CYCLE\_START\_ACTION](/sql-reference/classes/budget/methods/set_cycle_start_action), [<budget\_name>!REMOVE\_CYCLE\_START\_ACTION](/sql-reference/classes/budget/methods/remove_cycle_start_action)

## Syntax

Copy code

```
<budget_name>!GET_CYCLE_START_ACTION()
```

## Returns

The method returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| ACTION\_UUID | VARCHAR | Unique identifier for the cycle-start action. |
| PROCEDURE\_FQN | VARCHAR | Fully qualified name of the stored procedure. |
| PROCEDURE\_ARGS | ARRAY | Array of arguments passed to the stored procedure. |
| ADDED\_TIMESTAMP | TIMESTAMP\_TZ | Time when the action was added to the budget, in local time zone. |
| LAST\_TRIGGERED\_TIMESTAMP | TIMESTAMP\_TZ | Last time the budget triggered the action, in UTC. |

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

Get the cycle-start action for budget `my_budget` in schema `budget_db.sch1`:

Copy code

```
CALL budget_db.sch1.my_budget!GET_CYCLE_START_ACTION();
```

Get the cycle-start action for the account budget:

Copy code

```
CALL snowflake.local.account_root_budget!GET_CYCLE_START_ACTION();
```
