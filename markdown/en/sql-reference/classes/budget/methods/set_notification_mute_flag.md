# <budget\_name>!SET\_NOTIFICATION\_MUTE\_FLAG

Enable or disable notifications for a [budget](/user-guide/budgets).

See also:
:   [<budget\_name>!GET\_NOTIFICATION\_EMAIL](/sql-reference/classes/budget/methods/get_notification_email),
    [<budget\_name>!GET\_NOTIFICATION\_INTEGRATION\_NAME](/sql-reference/classes/budget/methods/get_notification_integration_name),
    [<budget\_name>!GET\_NOTIFICATION\_MUTE\_FLAG](/sql-reference/classes/budget/methods/get_notification_mute_flag),
    [<budget\_name>!SET\_EMAIL\_NOTIFICATIONS](/sql-reference/classes/budget/methods/set_email_notifications)

## Syntax

Copy code

```
<budget_name>!SET_NOTIFICATION_MUTE_FLAG( { TRUE | FALSE } );
```

## Arguments

`{ TRUE | FALSE }`
:   - TRUE to disable notifications.
    - FALSE to enable notifications.

    Default: FALSE

## Returns

```
The notification mute flag has been updated to <true | false>.
```

## Access control requirements

- The following minimum privileges and roles are required to call this method for *custom budgets*:

  - Any [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
  - USAGE privilege on the database and schema that contains the budget instance.
- The following minimum privileges and roles are required to call this method for the *account budget*:

  Any [application role](/user-guide/budgets#label-budgets-application-roles) for the account budget.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Disable notifications for budget `my_budget` in schema `budget_db.budget_schema`:

Copy code

```
CALL budget_db.budget_schema.my_budget!SET_NOTIFICATION_MUTE_FLAG(TRUE);
```

Enable notifications for the account budget:

Copy code

```
CALL snowflake.local.account_root_budget!SET_NOTIFICATION_MUTE_FLAG(FALSE);
```
