# DROP PIPE

Removes the specified pipe from the current/specified schema.

See also:
:   [CREATE PIPE](/sql-reference/sql/create-pipe) , [ALTER PIPE](/sql-reference/sql/alter-pipe) , [SHOW PIPES](/sql-reference/sql/show-pipes) , [DESCRIBE PIPE](/sql-reference/sql/desc-pipe)

## Syntax

Copy code

```
DROP PIPE [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier for the pipe to drop. If the identifier contains spaces or special characters, the entire string must
    be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- Dropped pipes can’t be recovered; they must be recreated.

- When the IF EXISTS clause is specified and the target object doesn’t exist, the command completes successfully
  without returning an error.

## Examples

> Copy code
>
> ```
> DROP PIPE mypipe;
>
> +------------------------------+
> | status                       |
> |------------------------------|
> | MYPIPE successfully dropped. |
> +------------------------------+
> ```
