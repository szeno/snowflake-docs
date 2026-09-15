Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Trigonometric)

# ASINH

Computes the inverse (arc) hyperbolic sine of its argument.

## Syntax

Copy code

```
ASINH( <input_expr> )
```

## Arguments

`input_expr`
:   The value or expression to operate on. The data type must be FLOAT.

## Returns

This function returns a value of type FLOAT.

## Examples

Copy code

```
SELECT ASINH(2.129279455);
```

```
+--------------------+
| ASINH(2.129279455) |
|--------------------|
|                1.5 |
+--------------------+
```
