# <budget\_name>!REMOVE\_RESOURCE\_TAG

Preview Feature — Private

Support for this feature is currently not in production and is available only to selected accounts.

Removes a tag-value combination from a custom budget. When this tag-value pair was added to the budget using the
[ADD\_RESOURCE\_TAG](/sql-reference/classes/budget/methods/add_resource_tag) method, all resources tagged with the pair were included in the budget. Removing the tag-value
pair removes the tagged resources from the budget.

Important

This method is being deprecated. Use [<budget\_name>!SET\_RESOURCE\_TAGS](/sql-reference/classes/budget/methods/set_resource_tags) instead.

## Syntax

Copy code

```
<budget_name>!REMOVE_RESOURCE_TAG(
    { '<tag_reference>' | <reference_statement> },
    'tag_value' )
```

## Arguments

`'tag_reference'`
:   The serialized string representation that resolves to a tag. This string is the output of
    the [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function.

`reference_statement`
:   A [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) statement that creates a reference for the tag to be removed from the
    budget.

`'tag_value'`
:   Specifies the value of the tag-value combination that you are removing from the budget.

    If the tag was added to the budget with a different value, the tag continues to be associated with the budget after removing this
    specific tag-value combination.

## Returns

Returns a VARCHAR value that indicates whether or not the tag-value combination was successfully removed from the budget.

If the tag could not be removed from the budget, the function returns an error message.

## Access control requirements

The following minimum privileges and roles are required to call this method on a *custom budget*:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contains the budget instance.
- USAGE privilege on the database and schema that contain the tag.
- APPLYBUDGET privilege on the tag being removed.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- This method can only be called on *custom budget* instances.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Retrieve the tag reference before calling the method to remove the tag-value combination.
:   The following statement creates and returns a reference for the `cost_center` tag:

    Copy code

    ```
    SELECT SYSTEM$REFERENCE(
      'TAG',
      'cost_mgmt_db.tags.cost_center',
      'SESSION',
      'APPLYBUDGET');
    ```

    The statement returns the reference in the output.

    ```
    ENT_REF_TAG_10382726315710_8A8626AE765E29446C38A217CAD093FCC9A454C2
    ```

    The following statement uses the string literal for this reference to add the `cost_center = 'sales'` tag-value combination to the
    `budget_db.budget_schema.my_budget` budget:

    Copy code

    ```
    CALL budget_db.budget_schema.my_budget!REMOVE_RESOURCE_TAG(
      'ENT_REF_TAG_10382726315710_8A8626AE765E29446C38A217CAD093FCC9A454C2',
      'sales');
    ```

Include the SYSTEM$REFERENCE function in the argument directly
:   After executing the following statement, the budget will no longer track objects that are tagged with the tag-value combination
    `team_tag = 'finance'`.

    > Copy code
    >
    > ```
    > CALL budget_db.budget_schema.my_budget!REMOVE_RESOURCE_TAG(
    >     (SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.team_tag', 'SESSION', 'APPLYBUDGET')),
    >     'finance');
    > ```
