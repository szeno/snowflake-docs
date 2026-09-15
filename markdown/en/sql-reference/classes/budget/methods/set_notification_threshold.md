# <budget\_name>!SET\_NOTIFICATION\_THRESHOLD

Sets a notification threshold for a [budget](/user-guide/budgets). Notifications are sent when Snowflake predicts that spending will
exceed the threshold.

## Syntax

Copy code

```
<budget_name>!SET_NOTIFICATION_THRESHOLD( <threshold_percent> );
```

## Arguments

`threshold_percent`
:   Percentage of the budget limit. Notifications are sent when Snowflake determines that spending will exceed this percentage of the budget
    limit.

    Accepted values: 0 - 1000

## Returns

Returns a VARCHAR value that indicates whether or not the notification threshold was successfully added.

## Access control requirements

The following minimum privileges and roles are required to call this method for *custom budgets*:

> - ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
> - USAGE privilege on the database and schema that contains the budget instance.

The following role is required to call this method for the *account budget*:

> - BUDGET\_ADMIN [application role](/user-guide/budgets#label-budgets-application-roles) for the account budget.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

## Examples

The following example sets the notification threshold of the account budget to 10% of the budget limit:

Copy code

```
CALL SNOWFLAKE.LOCAL.ACCOUNT_ROOT_BUDGET!SET_NOTIFICATION_THRESHOLD(10);
```
