# <budget\_name>!REMOVE\_CUSTOM\_ACTIONS

Remove one or more [custom actions](/user-guide/budgets/custom-actions) from a budget.

See also:
:   [<budget\_name>!ADD\_CUSTOM\_ACTION](/sql-reference/classes/budget/methods/add_custom_action), [<budget\_name>!GET\_CUSTOM\_ACTIONS](/sql-reference/classes/budget/methods/get_custom_actions)

## Syntax

Copy code

```
<budget_name>!REMOVE_CUSTOM_ACTIONS()

<budget_name>!REMOVE_CUSTOM_ACTIONS( <threshold> )

<budget_name>!REMOVE_CUSTOM_ACTIONS( <threshold>, '<stored_procedure>' )
```

## Arguments

`threshold`
:   Threshold percentage at which custom actions are triggered. If you don’t specify a procedure name, all custom actions set for this threshold
    are removed.

`'stored_procedure'`
:   Fully qualified name of the stored procedure associated with the custom action. Snowflake removes all custom actions that match the
    specified stored procedure and threshold.

    Note

    When passing the fully qualified name of the procedure, use the `PROCEDURE_FQN` value from the output of the
    [GET\_CUSTOM\_ACTIONS](/sql-reference/classes/budget/methods/get_custom_actions) method.

## Returns

Returns a VARCHAR value indicating the number of custom actions that were successfully removed.

## Access control requirements

The following privileges and roles are required to call this method for a budget:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contain the budget instance.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Remove all custom actions from budget `my_budget` in schema `budget_db.sch1`:

Copy code

```
CALL budget_db.sch1.my_budget!REMOVE_CUSTOM_ACTIONS();
```

Remove all custom actions that are triggered when consumption reaches 75% of the budget limit:

Copy code

```
CALL budget_db.sch1.my_budget!REMOVE_CUSTOM_ACTIONS(75);
```

Remove the custom action that calls the `code_db.sch1.my_sp` stored procedure when consumption reaches 75% of the budget limit:

Copy code

```
CALL budget_db.sch1.my_budget!REMOVE_CUSTOM_ACTIONS(75, 'code_db.sch1.my_sp');
```
