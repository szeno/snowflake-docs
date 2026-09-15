# <budget\_name>!REMOVE\_NOTIFICATION\_INTEGRATION

Removes a queue or webhook notification integration from a [custom budget or the account budget](/user-guide/budgets).

See also:
:   [<budget\_name>!ADD\_NOTIFICATION\_INTEGRATION](/sql-reference/classes/budget/methods/add_notification_integration),
    [<budget\_name>!GET\_NOTIFICATION\_INTEGRATIONS](/sql-reference/classes/budget/methods/get_notification_integrations)

## Syntax

Copy code

```
<budget_name>!REMOVE_NOTIFICATION_INTEGRATION( '<integration_name>' )
```

## Arguments

`'integration_name'`
:   The name of the queue or webhook notification integration to remove from the budget.

## Returns

Returns a VARCHAR value that indicates whether or not the notification integration was successfully removed.

- If the notification integration was removed successfully, the method returns `Integration removed successfully`.
- Otherwise, the method returns an error message.

## Access control requirements

The following minimum privileges and roles are required to call this method on a budget:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contains the budget instance.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Remove the notification integration `budgets_notification_integration` from custom budget `my_budget` in schema
`budget_db.budget_schema`:

Copy code

```
CALL budget_db.budget_schema.my_budget!REMOVE_NOTIFICATION_INTEGRATION(
  'budgets_notification_integration');
```

Remove the notification integration `budgets_notification_integration` from the account budget:

Copy code

```
CALL SNOWFLAKE.LOCAL.ACCOUNT_ROOT_BUDGET!REMOVE_NOTIFICATION_INTEGRATION(
  'budgets_notification_integration');
```
