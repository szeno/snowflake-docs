# <budget\_name>!REMOVE\_CYCLE\_START\_ACTION

Removes the [user-defined action](/user-guide/budgets/cycle-start-actions) that is triggered when the budget cycle restarts.

See also:
:   [<budget\_name>!SET\_CYCLE\_START\_ACTION](/sql-reference/classes/budget/methods/set_cycle_start_action), [<budget\_name>!GET\_CYCLE\_START\_ACTION](/sql-reference/classes/budget/methods/get_cycle_start_action)

## Syntax

Copy code

```
<budget_name>!REMOVE_CYCLE_START_ACTION()
```

## Returns

Returns a VARCHAR value indicating whether the cycle start action was successfully removed.

## Access control requirements

The following privileges and roles are required to call this method for a budget:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contain the budget instance.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Remove the cycle-start action from budget `my_budget` in schema `budget_db.sch1`:

Copy code

```
CALL budget_db.sch1.my_budget!REMOVE_CYCLE_START_ACTION();
```
