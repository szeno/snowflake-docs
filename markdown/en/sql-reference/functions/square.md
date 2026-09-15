Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Exponent and Root)

# SQUARE

Returns the square of a numeric expression (i.e. a numeric expression multiplied by itself).

## Syntax

Copy code

```
SQUARE(expr)
```

## Returns

If the input expression is of type DECFLOAT, the returned type is DECFLOAT. Otherwise, the
returned type is FLOAT.

## Usage notes

- More efficient than the expression x\*x, so square(x) is preferred
  when a floating-point result is acceptable.

## Examples

Copy code

```
SELECT column1, square(column1)
FROM (values (0), (1), (-2), (3.15), (null)) v;

---------+-----------------+
 column1 | square(column1) |
---------+-----------------+
 0       | 0               |
 1       | 1               |
 -2      | 4               |
 3.15    | 9.9225          |
 [NULL]  | [NULL]          |
---------+-----------------+
```
