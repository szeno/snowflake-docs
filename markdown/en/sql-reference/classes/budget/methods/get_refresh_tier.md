# <budget\_name>!GET\_REFRESH\_TIER

Retrieves the current [refresh interval of a budget](/user-guide/budgets#label-budgets-refresh-interval). The budget refresh interval controls how long it takes for a
budget to be refreshed with the most current consumption data.

See also:
:   [<budget\_name>!SET\_REFRESH\_TIER](/sql-reference/classes/budget/methods/set_refresh_tier)

## Syntax

Copy code

```
<budget_name>!GET_REFRESH_TIER()
```

## Returns

Returns one of the following VARCHAR values:

- `'TIER_1H'` — The budget refresh interval is one hour.
- `'TIER_6H'` — The budget refresh interval is up to 6.5 hours.

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

View the refresh interval for budget `my_budget` in schema `budget_db.budget_schema`:

Copy code

```
CALL budget_db.budget_schema.my_budget!GET_REFRESH_TIER();
```

View the refresh interval for the account budget:

Copy code

```
CALL SNOWFLAKE.LOCAL.ACCOUNT_ROOT_BUDGET!GET_REFRESH_TIER();
```
