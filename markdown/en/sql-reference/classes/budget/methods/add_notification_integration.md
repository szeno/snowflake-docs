# <budget\_name>!ADD\_NOTIFICATION\_INTEGRATION

Adds a queue or webhook [notification integration](/sql-reference/sql/create-notification-integration) to a
[custom budget or the account budget](/user-guide/budgets).

See also:
:   [<budget\_name>!GET\_NOTIFICATION\_INTEGRATIONS](/sql-reference/classes/budget/methods/get_notification_integrations),
    [<budget\_name>!REMOVE\_NOTIFICATION\_INTEGRATION](/sql-reference/classes/budget/methods/remove_notification_integration)

## Syntax

Copy code

```
<budget_name>!ADD_NOTIFICATION_INTEGRATION( '<integration_name>' )
```

## Arguments

`'integration_name'`
:   The name of the queue or webhook notification integration to add to the budget.

## Returns

Returns a VARCHAR value that indicates whether or not the notification integration was successfully added.

- If the notification integration was added successfully, the method returns `Integration added successfully`.
- Otherwise, the method returns an error message.

## Access control requirements

The following privileges and roles are required to call this method for a custom budget:

- ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
- USAGE privilege on the database and schema that contain the budget instance.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

In addition, you must grant the following privileges to the SNOWFLAKE application:

- The USAGE privilege on the notification integration.

If the notification integration is for a webhook that uses a secret object, you must also grant the following privileges to the
SNOWFLAKE application:

- The READ privilege on that secret.
- The USAGE privilege on the schema containing that secret.
- The USAGE privilege on the database containing that schema.

For information, see:

- [Setting up email notification](/user-guide/budgets/notifications#label-budgets-create-notification-integration-email)
- [Setting up queue notification](/user-guide/budgets/notifications#label-budgets-create-notification-integration-queue)
- [Setting up webhook notification](/user-guide/budgets/notifications#label-budgets-create-notification-integration-webhook)

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

## Examples

The following example adds the notification integration `budgets_notification_integration` to the account budget:

Copy code

```
CALL SNOWFLAKE.LOCAL.ACCOUNT_ROOT_BUDGET!ADD_NOTIFICATION_INTEGRATION(
  'budgets_notification_integration',
);
```
