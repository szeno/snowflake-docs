# <budget\_name>!GET\_NOTIFICATION\_INTEGRATIONS

Returns information about the queue and webhook notification integrations associated with a
[custom budget or the account budget](/user-guide/budgets).

To get the name of the email notification integration associated with the budget, call
[<budget\_name>!GET\_NOTIFICATION\_INTEGRATION\_NAME](/sql-reference/classes/budget/methods/get_notification_integration_name) instead.

See also:
:   [<budget\_name>!ADD\_NOTIFICATION\_INTEGRATION](/sql-reference/classes/budget/methods/add_notification_integration),
    [<budget\_name>!GET\_NOTIFICATION\_INTEGRATION\_NAME](/sql-reference/classes/budget/methods/get_notification_integration_name),
    [<budget\_name>!REMOVE\_NOTIFICATION\_INTEGRATION](/sql-reference/classes/budget/methods/remove_notification_integration)

## Syntax

Copy code

```
<budget_name>!GET_NOTIFICATION_INTEGRATIONS()
```

## Returns

Returns tabular data containing information about the notification integrations associated with the budget. The data includes a
row for each queue or webhook notification integration associated with the budget. The rows include the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `integration_name` | VARCHAR | Name of the notification integration. |
| `last_notification_time` | NUMBER | UTC timestamp when the last notification was sent. If no notifications were sent out yet, the value in this column is `-1`. |
| `added_date` | DATE | Date when the notification integration was added to the budget. |

Expand

Show lessSee more

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

View the names of the queue and webhook notification integrations, if any, for `my_budget` in schema `budget_db.budget_schema`:

Copy code

```
CALL budget_db.budget_schema.my_budget!GET_NOTIFICATION_INTEGRATIONS();
```

View the names of the queue and webhook notification integrations, if any, for the account budget:

Copy code

```
CALL SNOWFLAKE.LOCAL.ACCOUNT_ROOT_BUDGET!GET_NOTIFICATION_INTEGRATIONS();
```
