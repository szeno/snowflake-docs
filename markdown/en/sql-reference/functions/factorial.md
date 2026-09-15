Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Exponent and Root)

# FACTORIAL

Computes the factorial of its input. The input argument must be an integer expression in the range of `0` to `33`.

## Syntax

Copy code

```
FACTORIAL( <integer_expr> )
```

## Examples

Copy code

```
SELECT FACTORIAL(0), FACTORIAL(1), FACTORIAL(5), FACTORIAL(10);

+--------------+--------------+--------------+---------------+
| FACTORIAL(0) | FACTORIAL(1) | FACTORIAL(5) | FACTORIAL(10) |
|--------------+--------------+--------------+---------------|
|            1 |            1 |          120 |       3628800 |
+--------------+--------------+--------------+---------------+
```
