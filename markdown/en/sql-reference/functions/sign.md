Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Rounding and Truncation)

# SIGN

Returns the sign of its argument:

- -1 if the argument is negative.
- 1 if it is positive.
- 0 if it is 0.

## Syntax

Copy code

```
SIGN( <expr> )
```

## Examples

Copy code

```
SELECT SIGN(5), SIGN(-1.35e-10), SIGN(0);

---------+-----------------+---------+
 SIGN(5) | SIGN(-1.35E-10) | SIGN(0) |
---------+-----------------+---------+
 1       | -1              | 0       |
---------+-----------------+---------+
```
