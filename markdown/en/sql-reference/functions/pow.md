Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Exponent and Root)

# POW, POWER

Returns a number (x) raised to the specified power (y).

## Syntax

Copy code

```
POW(x, y)

POWER (x, y)
```

## Returns

If the input expression is of type DECFLOAT, the returned type is DECFLOAT. Otherwise, the
returned type is FLOAT.

## Examples

Copy code

```
SELECT x, y, pow(x, y) FROM tab;

-----+-----+-------------+
  X  |  Y  |  POW(X, Y)  |
-----+-----+-------------+
 0.1 | 2   | 0.01        |
 2   | 3   | 8           |
 2   | 0.5 | 1.414213562 |
 2   | -1  | 0.5         |
-----+-----+-------------+
```
