Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Trigonometric)

# TANH

Computes the hyperbolic tangent of its argument.

## Syntax

Copy code

```
TANH( <real_expr> )
```

## Arguments

`input_expr`
:   The value or expression to operate on. The data type must be FLOAT.

## Returns

This function returns a value of type FLOAT.

## Examples

Copy code

```
SELECT TANH(1.5);
```

```
+--------------+
|    TANH(1.5) |
|--------------|
| 0.9051482536 |
+--------------+
```
