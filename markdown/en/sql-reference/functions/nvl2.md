Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# NVL2

Returns values depending on whether the first input is NULL:

- If `expr1` is NOT NULL, then NVL2 returns `expr2`.
- If `expr1` is NULL, then NVL2 returns `expr3`.

## Syntax

Copy code

```
NVL2( <expr1> , <expr2> , <expr3> )
```

## Arguments

`expr1`
:   The expression to be checked to see whether it is NULL.

`expr2`
:   If `expr1` is not NULL, this expression will be evaluated and
    its value will be returned.

`expr3`
:   If `expr1` is NULL, this expression will be evaluated and
    its value will be returned.

## Usage notes

- All three expressions should have the same (or compatible) data type.

## Collation details

- The collation specification for `expr1` is ignored because all that matters about this expression is
  whether it is NULL or not.
- The collation specifications for `expr2` and `expr3` must be compatible.
- The value returned from the function is the
  highest-[precedence](/sql-reference/collation#label-determining-the-collation-used-in-an-operation) collation of `expr2` and
  `expr3`.

## Examples

If `a` is not null, then return `b`, else return `c`:

> Copy code
>
> ```
> SELECT a, b, c, NVL2(a, b, c) FROM i2;
>
> --------+--------+--------+---------------+
>    A    |   B    |   C    | NVL2(A, B, C) |
> --------+--------+--------+---------------+
>  0      | 5      | 3      | 5             |
>  0      | 5      | [NULL] | 5             |
>  0      | [NULL] | 3      | [NULL]        |
>  0      | [NULL] | [NULL] | [NULL]        |
>  [NULL] | 5      | 3      | 3             |
>  [NULL] | 5      | [NULL] | [NULL]        |
>  [NULL] | [NULL] | 3      | 3             |
>  [NULL] | [NULL] | [NULL] | [NULL]        |
> --------+--------+--------+---------------+
> ```
