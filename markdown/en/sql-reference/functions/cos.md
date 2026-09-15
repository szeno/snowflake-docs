Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Trigonometric)

# COS

Computes the cosine of its argument; the argument should be expressed in
radians.

## Syntax

Copy code

```
COS( <input_expr> )
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
SELECT COS(0), COS(PI()/3), COS(RADIANS(90));
```

```
+--------+-------------+------------------+
| COS(0) | COS(PI()/3) | COS(RADIANS(90)) |
|--------+-------------+------------------|
|      1 |         0.5 |  6.123233996e-17 |
+--------+-------------+------------------+
```
