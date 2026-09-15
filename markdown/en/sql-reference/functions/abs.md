Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Rounding and Truncation)

# ABS

Returns the absolute value of a numeric expression.

## Syntax

Copy code

```
ABS( <num_expr> )
```

## Examples

Copy code

```
SELECT column1, abs(column1)
    FROM (values (0), (1), (-2), (3.5), (-4.5), (null));
+---------+--------------+
| COLUMN1 | ABS(COLUMN1) |
|---------+--------------|
|     0.0 |          0.0 |
|     1.0 |          1.0 |
|    -2.0 |          2.0 |
|     3.5 |          3.5 |
|    -4.5 |          4.5 |
|    NULL |         NULL |
+---------+--------------+
```
