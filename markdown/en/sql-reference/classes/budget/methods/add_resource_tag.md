# <budget\_name>!ADD\_RESOURCE\_TAG

Adds a tag to a custom budget. All resources that are tagged with the specified tag-value pair are included in the budget.

Important

This method is being deprecated. Use [<budget\_name>!SET\_RESOURCE\_TAGS](/sql-reference/classes/budget/methods/set_resource_tags) instead.

## Syntax

Copy code

```
<budget_name>!ADD_RESOURCE_TAG(
    { '<tag_reference>' | <reference_statement> },
    '<tag_value>')
```

## Arguments

`'tag_reference'`
:   The serialized string representation that resolves to a tag. This string is the output of the
    [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function.

`reference_statement`
:   A [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) statement that creates a reference for the tag to be added to the budget.

`'tag_value'`
:   The value of the tag you are adding to the budget.

## Returns

Returns a VARCHAR value that indicates whether or not the tag was successfully added to the budget.

If the tag could not be added to the budget, the function returns an error message.

## Access control requirements

The following privileges and roles are required to call this method for a custom budget:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contain the budget instance.
- USAGE privilege on the database and schema that contain the tag.
- APPLYBUDGET privilege on the tag being added.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- You can only add tags to *custom budgets*.
- Snowflake doesn’t start showing usage for the added resources until the budget is refreshed, which can take up to six hours. If you want
  to view usage sooner, run the [REFRESH\_USAGE](/sql-reference/classes/budget/methods/refresh_usage) method.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Retrieve the tag reference before calling the method to add a tag.
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
    CALL budget_db.budget_schema.my_budget!ADD_RESOURCE_TAG(
      'ENT_REF_TAG_10382726315710_8A8626AE765E29446C38A217CAD093FCC9A454C2',
      'sales');
    ```

Include the SYSTEM$REFERENCE function in the argument directly
:   After executing the following statement, the budget will track all objects that are tagged with the tag-value combination
    `team_tag = 'finance'`.

    > Copy code
    >
    > ```
    > CALL budget_db.budget_schema.my_budget!ADD_RESOURCE_TAG(
    >     (SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.team_tag', 'SESSION', 'APPLYBUDGET')),
    >     'finance');
    > ```
