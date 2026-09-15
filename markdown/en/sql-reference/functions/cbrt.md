Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Exponent and Root)

# CBRT

Returns the cubic root of a numeric expression.

## Syntax

Copy code

```
CBRT( <input_expr> )
```

## Returns

If the input expression is of type DECFLOAT, the returned type is DECFLOAT. Otherwise, the
returned type is FLOAT.

## Examples

Copy code

```
SELECT x, CBRT(x) FROM tab;

--------+-------------+
   x    |   cbrt(x)   |
--------+-------------+
 0      | 0           |
 2      | 1.25992105  |
 -10    | -2.15443469 |
 [NULL] | [NULL]      |
--------+-------------+
```
