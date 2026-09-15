# <budget\_name>!SET\_SPENDING\_LIMIT

Set the spending limit for a [budget](/user-guide/budgets). The spending limit is expressed
in number of credits.

See also:
:   [<budget\_name>!GET\_SPENDING\_LIMIT](/sql-reference/classes/budget/methods/get_spending_limit)

## Syntax

Copy code

```
<budget_name>!SET_SPENDING_LIMIT(<number>)
```

## Arguments

`number`
:   The number of credits allocated to the budget per month. When total usage for all objects assigned to the budget reaches this
    number for the current month, the budget is considered to be at 100% of the spending limit.

    For the account budget, all [supported objects](/user-guide/budgets/custom-budget#label-budgets-supported-objects) contribute to the credit
    usage.

    If a value is not specified for a budget, the budget has no spending limit, will never reach 100% usage, and will not
    trigger notifications.

    Default: -1 (no spending limit).

## Returns

```
The spending limit has been updated to <n> credits.
```

## Access control requirements

- The following minimum privileges and roles are required to view results for *custom budgets*:

  - ADMIN [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
  - USAGE privilege on the database and schema that contains the budget instance.
- The following role is required to view results for the *account budget*:

  BUDGET\_ADMIN [application role](/user-guide/budgets#label-budgets-application-roles) for the account budget.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- The `number` argument must be a positive integer.
- Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
  return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Set the spending limit for the account budget to 500 credits per month:

Copy code

```
CALL snowflake.local.account_root_budget!SET_SPENDING_LIMIT(500);
```

Set the spending limit for budget `my_database.my_schema.my_budget` to 100 credits per month.

Copy code

```
CALL my_database.my_schema.my_budget!SET_SPENDING_LIMIT(100);
```
