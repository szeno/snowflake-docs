# <budget\_name>!GET\_SHARED\_RESOURCES

Lists the shared resources that have been added to a [custom budget](/user-guide/budgets) using the
[ADD\_SHARED\_RESOURCE](/sql-reference/classes/budget/methods/add_shared_resource) method.

## Syntax

Copy code

```
<budget_name>!GET_SHARED_RESOURCES()
```

## Returns

The method returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| RESOURCE\_ID | NUMBER | System identifier of the resource. |
| NAME | VARCHAR | Name of the specific resource, or NULL if all resources of the domain type are included in the budget. |
| DOMAIN | VARCHAR | The type of resource. |

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

Get all shared resources that were added to the `budget_db.budget_schema.my_budget` budget:

Copy code

```
CALL budget_db.budget_schema.my_budget!GET_SHARED_RESOURCES();
```
