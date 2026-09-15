# DROP GIT REPOSITORY

Removes the specified Snowflake Git repository clone from the current/specified schema.

See also:
:   [ALTER GIT REPOSITORY](/sql-reference/sql/alter-git-repository), [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository), [DESCRIBE GIT REPOSITORY](/sql-reference/sql/desc-git-repository), [SHOW GIT BRANCHES](/sql-reference/sql/show-git-branches),
    [SHOW GIT REPOSITORIES](/sql-reference/sql/show-git-repositories), [SHOW GIT TAGS](/sql-reference/sql/show-git-tags)

## Syntax

Copy code

```
DROP GIT REPOSITORY [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the Git repository clone to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Usage notes

- Dropped Git repositories can’t be recovered; they must be recreated.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

> Copy code
>
> ```
> DROP GIT REPOSITORY my_repository;
> ```
>
> ```
> +-------------------------------------+
> |                status               |
> +-------------------------------------+
> | MY_REPOSITORY successfully dropped. |
> +-------------------------------------+
> ```
