Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Trigonometric)

# ASIN

Computes the inverse sine (arc sine) of its argument; the result is a number in the interval `[-pi/2, pi/2]`.

## Syntax

Copy code

```
ASIN( <input_expr> )
```

## Arguments

`input_expr`
:   The value or expression to operate on. Must be greater than or equal to -1.0 and
    less than or equal to +1.0. The data type must be FLOAT.

## Returns

This function returns a value of type FLOAT.

Returns the arc sine in radians (not degrees) in the range `[-pi/2, pi/2]`.

## Examples

Copy code

```
SELECT ASIN(0), ASIN(0.5), ASIN(1);
```

```
+---------+--------------+-------------+
| ASIN(0) |    ASIN(0.5) |     ASIN(1) |
|---------+--------------+-------------|
|       0 | 0.5235987756 | 1.570796327 |
+---------+--------------+-------------+
```
