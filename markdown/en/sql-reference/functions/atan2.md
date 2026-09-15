Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Trigonometric)

# ATAN2

Computes the inverse tangent (arc tangent) of the ratio of its two arguments.
For example, if x > 0, then the expression `ATAN2(y, x)` is equivalent to `ATAN(y/x)`.

The arc tangent is the angle between:

- The X axis.
- The ray from the point (0,0) to the point (X, Y) (where X and Y are not both 0).

See also:
:   [ATAN](/sql-reference/functions/atan)

## Syntax

Copy code

```
ATAN2( <y> , <x> )
```

Note that the first parameter is the Y coordinate, not the X coordinate.

## Arguments

`y`
:   This parameter is the Y coordinate of the point at the end of the ray. The data type must be FLOAT.

`x`
:   This parameter is the X coordinate of the point at the end of the ray. The data type must be FLOAT.

## Returns

This function returns a value of type FLOAT.

The returned value is in radians, not degrees.

The returned value is a number in the interval `[-pi, pi]`.

## Usage notes

- If the data type of an argument is a numeric data type other than DOUBLE, then the value is converted to DOUBLE.
- If the data type of an argument is string, the value is converted to DOUBLE if possible.
- If the data type of an argument is any other data type, the function returns an error.
- If either argument is NULL, the returned value is NULL.

## Examples

Copy code

```
SELECT ATAN2(5, 5);
```

```
+--------------+
|  ATAN2(5, 5) |
|--------------|
| 0.7853981634 |
+--------------+
```
