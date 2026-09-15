# <budget\_name>!GET\_RESOURCE\_TAGS

Lists the tags that have been added to a [custom budget](/user-guide/budgets) using the [ADD\_RESOURCE\_TAG](/sql-reference/classes/budget/methods/add_resource_tag)
method. Resources tagged with these tag-value pairs are included in the budget.

Important

This method is being deprecated. Use [<budget\_name>!GET\_BUDGET\_SCOPE](/sql-reference/classes/budget/methods/get_budget_scope) instead.

## Syntax

Copy code

```
<budget_name>!GET_RESOURCE_TAGS()
```

## Returns

The method returns the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| TAG\_ID | NUMBER | System-generated identifier. |
| TAG\_VALUE | VARCHAR | Value of the tag. |
| TAG\_DATABASE | VARCHAR | Database that contains the tag. |
| TAG\_SCHEMA | VARCHAR | Schema that contains the tag. |
| TAG\_NAME | VARCHAR | Name of the tag. |

Expand

Show lessSee more

## Access control requirements

The following minimum privileges and roles are required to view results for custom budgets:

- ADMIN or VIEWER [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contains the budget instance.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- This method can only be called on *custom budget* instances.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Example

Get all tags that were added to the `budget_db.budget_schema.my_budget` budget using the ADD\_RESOURCE\_TAG method:

Copy code

```
CALL budget_db.budget_schema.my_budget!GET_RESOURCE_TAGS();
```
