Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Logarithmic)

# LN

Returns the natural logarithm of a numeric expression.

## Syntax

Copy code

```
LN(<expr>)
```

## Returns

If the input expression is of type DECFLOAT, the returned type is DECFLOAT. Otherwise, the
returned type is FLOAT.

## Examples

Copy code

```
SELECT x, ln(x) FROM tab;

--------+-------------+
   X    |    LN(X)    |
--------+-------------+
 1      | 0           |
 10     | 2.302585093 |
 100    | 4.605170186 |
 [NULL] | [NULL]      |
--------+-------------+
```
