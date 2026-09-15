# <budget\_name>!GET\_LINKED\_RESOURCES

List the objects that we explicitly added to a [custom budget](/user-guide/budgets).

The list does not include:

- Objects that were added automatically (for example, compute pools and warehouses created and owned by a Snowflake Native App).
- Objects that were added when a tag was added to the budget.

Important

This method is being deprecated. Use [<budget\_name>!GET\_BUDGET\_SCOPE](/sql-reference/classes/budget/methods/get_budget_scope) instead.

## Syntax

Copy code

```
<budget_name>!GET_LINKED_RESOURCES()
```

## Returns

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| RESOURCE\_ID | NUMBER | Internal identifier for the object. |
| NAME | VARCHAR | Name of the object. |
| DOMAIN | VARCHAR | Domain of the object. Valid values:   - `COMPUTE_POOL` - `DATABASE` - `MATERIALIZED_VIEW` - `PIPE` - `SCHEMA` - `TABLE` - `TASK` - `WAREHOUSE`   Note  If the object is a Snowflake Native App, the value in this column is `DATABASE` (not `APPLICATION`). |
| SCHEMA\_NAME | VARCHAR | Name of the schema that contains the object. NULL if the object is not a schema-level object. |
| DATABASE\_NAME | VARCHAR | Name of the database that contains the object. NULL if the object is not a database-level or schema-level object. |

Expand

Show lessSee more

## Access control requirements

The following minimum privileges and roles are required to view results for custom budgets:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contains the budget instance.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- This method can only be called on *custom budget* instances.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Example

Get all objects that were added to the `budget_db.budget_schema.my_budget` budget:

Copy code

```
CALL budget_db.budget_schema.my_budget!GET_LINKED_RESOURCES();
```
