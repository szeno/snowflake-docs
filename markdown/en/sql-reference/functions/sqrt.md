Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Exponent and Root)

# SQRT

Returns the square-root of a non-negative numeric expression.

## Syntax

Copy code

```
SQRT(expr)
```

## Returns

If the input expression is of type DECFLOAT, the returned type is DECFLOAT. Otherwise, the
returned type is FLOAT.

## Examples

Copy code

```
SELECT x, sqrt(x) FROM tab;

--------+-------------+
   x    |   sqrt(x)   |
--------+-------------+
 0      | 0           |
 2      | 1.414213562 |
 10     | 3.16227766  |
 [NULL] | [NULL]      |
--------+-------------+
```
