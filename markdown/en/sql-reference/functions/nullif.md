Categories:
:   [Conditional expression functions](/sql-reference/expressions-conditional)

# NULLIF

Returns NULL if `expr1` is equal to `expr2`, otherwise returns `expr1`.

## Syntax

Copy code

```
NULLIF( <expr1> , <expr2> )
```

## Arguments

`expr1`
:   Any general expression of any data type.

`expr2`
:   Any general expression that evaluates to the same data type as `expr1`.

## Returns

The data type of the returned value is the data type of `expr1`.

## Collation details

- The [collation specifications](/sql-reference/collation#label-collation-specification) of all input arguments must be compatible.
- The collation of the result is the same as the collation of the first input.

## Examples

> Copy code
>
> ```
> SELECT a, b, NULLIF(a,b) FROM i;
>
> --------+--------+-------------+
>    a    |   b    | nullif(a,b) |
> --------+--------+-------------+
>  0      | 0      | [NULL]      |
>  0      | 1      | 0           |
>  0      | [NULL] | 0           |
>  1      | 0      | 1           |
>  1      | 1      | [NULL]      |
>  1      | [NULL] | 1           |
>  [NULL] | 0      | [NULL]      |
>  [NULL] | 1      | [NULL]      |
>  [NULL] | [NULL] | [NULL]      |
> --------+--------+-------------+
> ```
