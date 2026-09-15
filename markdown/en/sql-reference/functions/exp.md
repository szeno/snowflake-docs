Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Exponent and Root)

# EXP

Computes Euler’s number `e` raised to a floating-point value.

## Syntax

Copy code

```
EXP( <input_expr> )
```

## Arguments

`input_expr`
:   The value or expression to operate on. The data type must be FLOAT or DECFLOAT.

## Returns

If the input expression is of type DECFLOAT, the returned type is DECFLOAT. Otherwise, the
returned type is FLOAT.

## Examples

> Copy code
>
> ```
> SELECT EXP(1), EXP(LN(10));
> -------------+-------------+
>    EXP(1)    | EXP(LN(10)) |
> -------------+-------------+
>  2.718281828 | 10          |
> -------------+-------------+
> ```
