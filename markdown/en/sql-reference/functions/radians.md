Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Trigonometric)

# RADIANS

Converts degrees to radians.

## Syntax

Copy code

```
RADIANS( <input_expr> )
```

## Arguments

`input_expr`
:   The value or expression to operate on. The data type must be FLOAT.

## Returns

This function returns a value of type FLOAT.

## Examples

Show the results of calling the RADIANS function:

Copy code

```
SELECT RADIANS(0), RADIANS(60), RADIANS(180), RADIANS(360), RADIANS(720);
```

```
+------------+-------------+--------------+--------------+--------------+
| RADIANS(0) | RADIANS(60) | RADIANS(180) | RADIANS(360) | RADIANS(720) |
|------------+-------------+--------------+--------------+--------------|
|          0 | 1.047197551 |  3.141592654 |  6.283185307 | 12.566370614 |
+------------+-------------+--------------+--------------+--------------+
```
