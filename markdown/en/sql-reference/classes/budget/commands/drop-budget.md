# DROP BUDGET

*Fully qualified name*: SNOWFLAKE.CORE.BUDGET

Removes an instance of a *custom* budget.

See also:
:   [CREATE BUDGET](/sql-reference/classes/budget/commands/create-budget),
    [ALTER BUDGET](/sql-reference/classes/budget/commands/alter-budget),
    [SHOW BUDGET](/sql-reference/classes/budget/commands/show-budget)

## Syntax

Copy code

```
DROP SNOWFLAKE.CORE.BUDGET [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier (i.e. name) of the budget.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Budget | The role used to drop a budget must be granted this privilege on the budget. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- To refer to this class by its unqualified name, include the database and schema of the class in your
  [search path](/sql-reference/snowflake-db-classes#label-update-search-path).
- Dropped budgets cannot be recovered; they must be recreated.

## Examples

Drop budget `my_budget` in the current schema:

Copy code

```
DROP SNOWFLAKE.CORE.BUDGET my_budget;
```
