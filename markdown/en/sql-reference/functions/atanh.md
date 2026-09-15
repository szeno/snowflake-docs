Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Trigonometric)

# ATANH

Computes the inverse (arc) hyperbolic tangent of its argument.

## Syntax

Copy code

```
ATANH( <input_expr> )
```

## Arguments

`input_expr`
:   The value or expression to operate on. Must be a value between -1.0 and +1.0
    (inclusive). The data type must be FLOAT.

## Returns

This function returns a value of type FLOAT.

## Examples

Copy code

```
SELECT ATANH(0.9051482536);
```

```
+---------------------+
| ATANH(0.9051482536) |
|---------------------|
|                 1.5 |
+---------------------+
```
