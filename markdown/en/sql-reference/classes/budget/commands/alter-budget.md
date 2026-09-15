# ALTER BUDGET

*Fully qualified name*: SNOWFLAKE.CORE.BUDGET

Modifies the properties of a *custom* budget:

- Renames the budget.
- Sets or unsets a tag.
- Sets or unsets the comment.

See also:
:   [CREATE BUDGET](/sql-reference/classes/budget/commands/create-budget),
    [SHOW BUDGET](/sql-reference/classes/budget/commands/show-budget),
    [DROP BUDGET](/sql-reference/classes/budget/commands/drop-budget)

## Syntax

Copy code

```
ALTER SNOWFLAKE.CORE.BUDGET [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER SNOWFLAKE.CORE.BUDGET [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER SNOWFLAKE.CORE.BUDGET [ IF EXISTS ] <name> UNSET COMMENT

ALTER SNOWFLAKE.CORE.BUDGET [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER SNOWFLAKE.CORE.BUDGET [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   Specifies the identifier (i.e. name) of the budget.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Specifies one or more budget properties to be set.

    `COMMENT = 'string_literal'`
    :   Sets the comment of the budget. This can also be done using the [COMMENT](/sql-reference/sql/comment) command.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies one (or more) properties and/or parameters to unset for the budget, which resets them to the defaults:

    - `COMMENT`
    - `TAG tag_name [ , tag_name ... ]`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege / Role | Object | Notes |
| --- | --- | --- |
| ADMIN | Budget | The role used to modify the properties of a custom budget must be granted this [instance role](/user-guide/budgets#label-budgets-instance-roles). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

- You can only modify the properties for a *custom* budget.
- To refer to this class by its unqualified name, include the database and schema of the class in your
  [search path](/sql-reference/snowflake-db-classes#label-update-search-path).

## Examples

Set the tag `dept` for the budget `my_budget` in the current schema:

Copy code

```
ALTER SNOWFLAKE.CORE.BUDGET my_budget SET TAG dept = 'finance';
```
