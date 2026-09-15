Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Trigonometric)

# SIN

Computes the sine of its argument; the argument should be expressed in
radians.

## Syntax

Copy code

```
SIN( <input_expr> )
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
SELECT SIN(0), SIN(PI()/3), SIN(RADIANS(90));
```

```
+--------+--------------+------------------+
| SIN(0) |  SIN(PI()/3) | SIN(RADIANS(90)) |
|--------+--------------+------------------|
|      0 | 0.8660254038 |                1 |
+--------+--------------+------------------+
```
