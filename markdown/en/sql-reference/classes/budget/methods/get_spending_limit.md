# <budget\_name>!GET\_SPENDING\_LIMIT

View the spending limit for a [budget](/user-guide/budgets).

See also:
:   [<budget\_name>!SET\_SPENDING\_LIMIT](/sql-reference/classes/budget/methods/set_spending_limit)

## Syntax

Copy code

```
<budget_name>!GET_SPENDING_LIMIT()
```

## Returns

- The number of credits set as the spending limit for the budget.
- `-1` if the spending limit is not set.

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

View the spending limit for budget `my_budget` in schema `budget_db.budget_schema`:

Copy code

```
CALL budget_db.budget_schema.my_budget!GET_SPENDING_LIMIT();
```

View the spending limit for the account budget:

Copy code

```
CALL snowflake.local.account_root_budget!GET_SPENDING_LIMIT();
```
