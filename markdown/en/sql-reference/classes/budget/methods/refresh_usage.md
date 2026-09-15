# <budget\_name>!REFRESH\_USAGE

Preview Feature — Private

Support for this feature is currently not in production and is available only to selected accounts.

Causes the budget to retrieve consumption data so that the budget can compare it to the spending limit without waiting for the next
automatic retrieval of data.

## Syntax

Copy code

```
<budget_name>!REFRESH_USAGE()
```

## Returns

Returns a VARCHAR value that indicates whether the usage was successfully refreshed.

## Access control requirements

The following minimum privileges and roles are required to call this method for custom budgets:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contains the budget instance.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- This method can only be called on *custom budget* instances.
- It takes a few minutes for the budget to be refreshed with new usage data.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Example

Retrieve consumption data for the `budget_db.budget_schema.my_budget` budget:

Copy code

```
CALL budget_db.budget_schema.my_budget!REFRESH_USAGE();
```
