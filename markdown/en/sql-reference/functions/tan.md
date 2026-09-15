Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Trigonometric)

# TAN

Computes the tangent of its argument; the argument should be expressed in
radians.

## Syntax

Copy code

```
TAN( <input_expr> )
```

## Arguments

`input_expr`
:   The value or expression to operate on. The value must be in
    radians, not degrees. The data type must be FLOAT.

## Returns

This function returns a value of type FLOAT.

## Examples

Copy code

```
SELECT TAN(0), TAN(PI()/3), TAN(RADIANS(90));
```

```
+--------+-------------+----------------------+
| TAN(0) | TAN(PI()/3) |     TAN(RADIANS(90)) |
|--------+-------------+----------------------|
|      0 | 1.732050808 | 1.63312393531954e+16 |
+--------+-------------+----------------------+
```
