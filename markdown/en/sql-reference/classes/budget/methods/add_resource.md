# <budget\_name>!ADD\_RESOURCE

Add an object to a [custom budget](/user-guide/budgets). The object must be added by
[reference](/sql-reference/references).

See also:
:   [<budget\_name>!REMOVE\_RESOURCE](/sql-reference/classes/budget/methods/remove_resource),
    [<budget\_name>!GET\_LINKED\_RESOURCES](/sql-reference/classes/budget/methods/get_linked_resources)

## Syntax

Copy code

```
<budget_name>!ADD_RESOURCE( { '<object_reference>' | <reference_statement> } )
```

## Arguments

`'object_reference'`
:   The serialized string representation that resolves to an object. This string is the output of
    the [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function.

`reference_statement`
:   A [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) statement that creates a reference for the object to be added to the budget.

Note

If you want to add a Snowflake Native App to a budget, when you call SYSTEM$REFERENCE, specify `'DATABASE'` (not `'APPLICATION'`)
for the `object_type` argument.

See [Adding a Snowflake Native App to a budget](#label-budget-method-add-resource-example-native-app).

## Returns

Returns a VARCHAR value that indicates whether or not the object was successfully added to the budget. For example:

```
Successfully added resource to resource group
```

If the object could not be added to the budget, the function returns an error message. See
[You can’t add or remove objects from a custom budget](/user-guide/budgets/troubleshoot#label-troubleshooting-budgets-modify-objects).

## Access control requirements

The following privileges and roles are required to call this method for a custom budget:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contain the budget instance.
- USAGE privilege on the database and schema that contain the object being added (for schema objects).
- APPLYBUDGET privilege on the object being added.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- You can only add objects to *custom budgets*.
- If you are directly adding individual objects, you can only add an object to one custom budget. In this case, if an object is currently
  included in one custom budget and you add that object to a second custom budget, Budgets removes the object from the first custom budget
  without issuing a warning.

  This behavior does not apply to using tags to add objects to budgets; an object with one or more tags can be
  included in multiple custom budgets if you are using tags to add the object to the budgets.
- You cannot create a reference for the SNOWFLAKE database; and you cannot add it
  to a budget.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Examples

The following examples demonstrate how to add an object to a custom budget:

- [Adding a table to a budget](#label-budget-method-add-resource-example)
- [Adding a Snowflake Native App to a budget](#label-budget-method-add-resource-example-native-app)

### Adding a table to a budget

- The following example creates and returns a reference for the `t1` table:

  Copy code

  ```
  SELECT SYSTEM$REFERENCE('TABLE', 't1', 'SESSION', 'APPLYBUDGET');
  ```

  The statement returns the reference in the output.

  ```
  ENT_REF_TABLE_5862683050074_5AEB8D58FB3ACF249F2E35F365A9357C46BB00D7
  ```

  The following statement uses the string literal for this reference to add the `t1` table to the
  `budget_db.budget_schema.my_budget` budget:

  Copy code

  ```
  CALL budget_db.budget_schema.my_budget!ADD_RESOURCE(
    'ENT_REF_TABLE_5862683050074_5AEB8D58FB3ACF249F2E35F365A9357C46BB00D7');
  ```
- The following example adds the `t2` table to the `budget_db.budget_schema.my_budget` budget, using a SQL statement
  to specify the reference:

  Copy code

  ```
  CALL budget_db.budget_schema.my_budget!ADD_RESOURCE(
    SELECT SYSTEM$REFERENCE('TABLE', 't2', 'SESSION', 'APPLYBUDGET'));
  ```

### Adding a Snowflake Native App to a budget

The following example adds the `my_app` application to the `budget_db.budget_schema.my_budget` budget.

Note that when calling [SYSTEM$REFERENCE](/sql-reference/functions/system_reference), you must pass in `'DATABASE'` (not `'APPLICATION'`)
for the `object_type` argument.

Copy code

```
CALL budget_db.budget_schema.my_budget!ADD_RESOURCE(
  SELECT SYSTEM$REFERENCE('DATABASE', 'my_app', 'SESSION', 'APPLYBUDGET'));
```

## Error messages

For a list of common error messages and their causes and solutions, see [You can’t add or remove objects from a custom budget](/user-guide/budgets/troubleshoot#label-troubleshooting-budgets-modify-objects).
