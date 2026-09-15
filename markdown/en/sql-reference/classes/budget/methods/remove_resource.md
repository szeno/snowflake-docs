# <budget\_name>!REMOVE\_RESOURCE

Remove an object from a [custom budget](/user-guide/budgets). The object must be removed by
[reference](/sql-reference/references).

See also:
:   [<budget\_name>!ADD\_RESOURCE](/sql-reference/classes/budget/methods/add_resource),
    [<budget\_name>!GET\_LINKED\_RESOURCES](/sql-reference/classes/budget/methods/get_linked_resources)

## Syntax

Copy code

```
<budget_name>!REMOVE_RESOURCE( { '<object_reference>' | <reference_statement> } )
```

## Arguments

`'object_reference'`
:   The serialized string representation that resolves to an object. This string is the output of
    the [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function.

`reference_statement`
:   A [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) statement that creates a reference for the object to be removed from the
    budget.

Note

If you want to add a Snowflake Native App to a budget, when you call SYSTEM$REFERENCE, specify `'DATABASE'` (not `'APPLICATION'`)
for the `object_type` argument.

See [Removing a Snowflake Native App from a budget](#label-budget-method-remove-resource-example-native-app).

## Returns

Returns a VARCHAR value that indicates whether or not the object was successfully removed from the budget. For example:

```
Successfully removed resource from resource group
```

If the object could not be removed from the budget, the function returns an error message. See
[You can’t add or remove objects from a custom budget](/user-guide/budgets/troubleshoot#label-troubleshooting-budgets-modify-objects).

## Access control requirements

The following minimum privileges and roles are required to call this method on a *custom budget*:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contains the budget instance.
- USAGE privilege on the database and schema that contain the object (for schema objects).
- APPLYBUDGET privilege on the object being removed.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- This method can only be called on *custom budget* instances.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Examples

The following examples demonstrate how to remove an object from a custom budget:

- [Removing a table from a budget](#label-budget-method-remove-resource-example)
- [Removing a Snowflake Native App from a budget](#label-budget-method-remove-resource-example-native-app)

### Removing a table from a budget

- The following example creates and returns a reference for the `t1` table:

  Copy code

  ```
  SELECT SYSTEM$REFERENCE('TABLE', 't1', 'SESSION', 'APPLYBUDGET');
  ```

  The statement returns the reference in the output.

  ```
  ENT_REF_TABLE_5862683050074_5AEB8D58FB3ACF249F2E35F365A9357C46BB00D7
  ```

  The following statement uses the string literal for this reference to remove the `t1` table from the
  `budget_db.budget_schema.my_budget` budget:

  Copy code

  ```
  CALL budget_db.budget_schema.my_budget!REMOVE_RESOURCE(
    'ENT_REF_TABLE_5862683050074_5AEB8D58FB3ACF249F2E35F365A9357C46BB00D7');
  ```
- The following example removes the `t2` table from the `budget_db.budget_schema.my_budget` budget, using a SQL
  statement to specify the reference:

  Copy code

  ```
  CALL budget_db.budget_schema.my_budget!REMOVE_RESOURCE(
    SELECT SYSTEM$REFERENCE('TABLE', 't2', 'SESSION', 'APPLYBUDGET')
  ```

### Removing a Snowflake Native App from a budget

The following example removes the `my_app` application from the `budget_db.budget_schema.my_budget` budget.

Note that when calling [SYSTEM$REFERENCE](/sql-reference/functions/system_reference), you must pass in `'DATABASE'` (not `'APPLICATION'`)
for the `object_type` argument.

Copy code

```
CALL budget_db.budget_schema.my_budget!REMOVE_RESOURCE(
  SELECT SYSTEM$REFERENCE('DATABASE', 'my_app', 'SESSION', 'APPLYBUDGET'));
```

## Error messages

For a list of common error messages and their causes and solutions, see [You can’t add or remove objects from a custom budget](/user-guide/budgets/troubleshoot#label-troubleshooting-budgets-modify-objects).
