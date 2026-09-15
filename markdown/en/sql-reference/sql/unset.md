# UNSET

Drops a [session variable](/sql-reference/session-variables).

See also:
:   [SHOW VARIABLES](/sql-reference/sql/show-variables) , [SET](/sql-reference/sql/set)

## Syntax

Copy code

```
UNSET <var>

UNSET ( <var> [ , <var> ... ] )
```

## Parameters

`var`
:   Specifies the identifier for the variable to drop.

## Usage notes

- The command supports dropping multiple variables in the same statement.
- The command does not require a running warehouse to execute.

## Examples

Copy code

```
UNSET V1;

UNSET V2;

UNSET (V1, V2);
```
