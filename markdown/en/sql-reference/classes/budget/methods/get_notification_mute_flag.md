# <budget\_name>!GET\_NOTIFICATION\_MUTE\_FLAG

View the status of the notification mute flag for a [budget](/user-guide/budgets). If the mute
flag is set to TRUE, no notifications are sent about the budget’s spending limit.

See also:
:   [<budget\_name>!GET\_NOTIFICATION\_EMAIL](/sql-reference/classes/budget/methods/get_notification_email),
    [<budget\_name>!GET\_NOTIFICATION\_INTEGRATION\_NAME](/sql-reference/classes/budget/methods/get_notification_integration_name),
    [<budget\_name>!SET\_EMAIL\_NOTIFICATIONS](/sql-reference/classes/budget/methods/set_email_notifications),
    [<budget\_name>!SET\_NOTIFICATION\_MUTE\_FLAG](/sql-reference/classes/budget/methods/set_notification_mute_flag)

## Syntax

Copy code

```
<budget_name>!GET_NOTIFICATION_MUTE_FLAG()
```

## Returns

- `TRUE` if notifications are disabled.
- `FALSE` if notifications are enabled.

## Access control requirements

- The following minimum privileges and roles are required to view results for *custom budgets*:

  - Any [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
  - USAGE privilege on the database and schema that contains the budget instance.
- The following role is required to view results for the *account budget*:

  - Any [application role](/user-guide/budgets#label-budgets-application-roles) for the account budget.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

## Examples

View the state of the notification mute flag for `my_budget` in schema `budget_db.budget_schema`:

Copy code

```
CALL budget_db.budget_schema.my_budget!GET_NOTIFICATION_MUTE_FLAG();
```

View the state of the notification mute flag for the account budget:

Copy code

```
CALL snowflake.local.account_root_budget!GET_NOTIFICATION_MUTE_FLAG();
```
