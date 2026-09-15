# <budget\_name>!SET\_USER\_TAGS

Adds user tags to a custom budget. Consumption by a shared resource counts toward the budget’s spending limit only if the resource is acted upon by a user with the specified tag-value pairs. For more information, see [Using budgets for AI features (shared resources)](/user-guide/budgets/budget-shared-resources).

You can configure the budget so that usage is included if a user is tagged with *any* of the specified tags (UNION) or configure it so usage is included only if the user is tagged with *all* of the specified tags (INTERSECTION).

Calling the method replaces any existing user tags that were added to the budget.

## Syntax

Copy code

```
<budget_name>!SET_USER_TAGS( <tag-pairs>, <operation_mode> )
```

## Arguments

`tag_pairs`
:   An [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) value that specifies tag references and tag values.

    A tag reference is a serialized string representation that resolves to a [tag](/user-guide/object-tagging/introduction). This string is the output of the
    [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function.

    Each element in the array should be an array containing a tag reference and a tag value. For example:

    Copy code

    ```
    [
      [ 'ENT_REF_TAG_10382726315710_8A8626AE765E2' , 'finance' ],
      ...
    ]
    ```

`operation_mode`
:   Specifies the matching logic to use for the specified tags. You can specify one of the following values:

    - `'UNION'`: Usage by a user is included in the budget if the user is tagged with *any* of the specified tag-value pairs. This corresponds to OR logic.
    - `'INTERSECTION'`: Usage by a user is included in the budget only if the user is tagged with *all* of the specified tag-value pairs. This corresponds to AND logic.

## Returns

Returns a VARCHAR value that indicates whether or not the tags were successfully set on the budget.

If the tags could not be set on the budget, the function returns an error message.

## Access control requirements

The following privileges and roles are required to call this method for a custom budget:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contain the budget instance.
- USAGE privilege on the database and schema that contain each tag.
- APPLYBUDGET privilege on each tag being added.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- You can only set tags on *custom budgets*.
- By default, you can add up to 20 user tags to the budget. To increase this limit, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
- To verify the results of the method, call the [GET\_BUDGET\_SCOPE](/sql-reference/classes/budget/methods/get_budget_scope) method.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Use the `my_budget` budget to track consumption when shared resources are acted upon by users tagged with *either* the tag-value combination
`cost_center = 'sales'` or the tag-value combination `team_tag = 'finance'`.

Copy code

```
CALL budget_db.budget_schema.my_budget!SET_USER_TAGS(
  [
      [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.cost_center', 'SESSION', 'APPLYBUDGET')), 'sales'],
      [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.team_tag', 'SESSION', 'APPLYBUDGET')), 'finance']
  ],
  'UNION');
```

Use the `my_budget` budget to track consumption when shared resources are acted upon by users tagged with *both* `cost_center = 'sales'` and `team_tag = 'finance'`.

Copy code

```
CALL budget_db.budget_schema.my_budget!SET_USER_TAGS(
  [
      [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.cost_center', 'SESSION', 'APPLYBUDGET')), 'sales'],
      [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.team_tag', 'SESSION', 'APPLYBUDGET')), 'finance']
  ],
  'INTERSECTION');
```
