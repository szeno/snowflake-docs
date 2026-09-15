Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$SHOW\_BUDGETS\_IN\_ACCOUNT

Returns the [budgets](/user-guide/budgets) in the account for which you have access privileges.

See also:
:   [CREATE BUDGET](/sql-reference/classes/budget/commands/create-budget)

## Syntax

Copy code

```
SYSTEM$SHOW_BUDGETS_IN_ACCOUNT()
```

## Returns

The function returns the following elements in a JSON object:

| Column Name | Data Type | Description |
| --- | --- | --- |
| DATABASE | TEXT | Name of the database to which the budget instance belongs. |
| SCHEMA | TEXT | Name of the schema to which the budget instance belongs. |
| CREATED\_ON | NUMBER | UTC timestamp when the budget instance was created. |
| ID | NUMBER | Internal/system identifier for the budget instance. |
| CURRENT\_VERSION | TEXT | Budget class version used to create the budget instance. |
| COMMENT | TEXT | Comment for the budget instance. |
| NAME | TEXT | Name of the budget instance. |

Expand

Show lessSee more

## Usage notes

The results include budgets for which the role executing the function has been granted any privileges.

## Examples

The following example retrieves the budgets in the account:

Copy code

```
SELECT SYSTEM$SHOW_BUDGETS_IN_ACCOUNT();
```
