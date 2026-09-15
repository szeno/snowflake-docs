# <budget\_name>!ADD\_CUSTOM\_ACTION

Associates a stored procedure with a budget so that the procedure is called when projected or actual spending reaches a specified
threshold. The procedure must be associated by [reference](/sql-reference/references).

For more information, see [Custom actions for budgets](/user-guide/budgets/custom-actions).

## Syntax

Copy code

```
<budget_name>!ADD_CUSTOM_ACTION (
  { '<stored_procedure_reference>' | <reference_statement> },
  { <array_of_arguments> | <array_construct_statement> },
  [ { 'ACTUAL' | 'PROJECTED' }, ]
  <threshold> )
```

## Arguments

`'stored_procedure_reference'`
:   The serialized string representation that resolves to a procedure. This string is the output of
    the [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function.

`reference_statement`
:   A [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) statement that creates a reference for the procedure to be associated with the budget.

`array_of_arguments`
:   Array of arguments to pass to the stored procedure.

`array_construct_statement`
:   An [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct) statement that returns an array constructed from zero, one, or more
    inputs.

`{ 'ACTUAL' | 'PROJECTED'}`
:   Controls whether an action is triggered based on the actual or projected spend.

    `'ACTUAL'` — The stored procedure is called when the actual spend reaches the `threshold`.
    `'PROJECTED` — The stored procedure is called when spending is projected to reach the `threshold`.

    If omitted, defaults to `PROJECTED`.

`threshold`
:   Percentage of the budget limit. The stored procedure is called when Snowflake determines that actual or projected spending exceeds this
    percentage of the budget limit.

    Specify a number between 0 and 1,000, inclusive.

## Returns

Returns a VARCHAR value that indicates whether or not the procedure was successfully associated with the budget.

If the procedure could not be associated with the budget, the method returns an error message.

## Access control requirements

The following privileges and roles are required to call this method for a budget:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contain the budget instance.
- USAGE privilege on the database and schema that contain the stored procedure.
- USAGE privilege on the stored procedure.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Associate the `alert_team` stored procedure with the `budget_db.sch1.my_budget` budget so that it is
called when spending is forecast to reach 75% of the budget limit:

Copy code

```
CALL budget_db.sch1.my_budget!ADD_CUSTOM_ACTION(
  SYSTEM$REFERENCE('PROCEDURE', 'code_db.sch1.alert_team(string, string, string)', 'SESSION', 'USAGE'),
  ARRAY_CONSTRUCT('admin@example.com', 'Budget Alert', 'Spending at 75% of budget limit'),
  'PROJECTED',
  75);
```

Associate the `alert_team` stored procedure with the `budget_db.sch1.my_budget` budget so that it is called when
spending has reached 90% of the budget limit:

Copy code

```
CALL budget_db.sch1.my_budget!ADD_CUSTOM_ACTION(
  SYSTEM$REFERENCE('PROCEDURE', 'code_db.sch1.alert_team(string, number)', 'SESSION', 'USAGE'),
  ARRAY_CONSTRUCT('Critical budget threshold', 90),
  'ACTUAL',
  90);
```
