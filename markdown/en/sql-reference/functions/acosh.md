Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Trigonometric)

# ACOSH

Computes the inverse (arc) hyperbolic cosine of its input.

## Syntax

Copy code

```
ACOSH( <input_expr> )
```

## Arguments

`input_expr`
:   The value or expression to operate on. Must be greater than or equal to 1.0.
    The data type must be FLOAT.

## Returns

This function returns a value of type FLOAT.

## Examples

Copy code

```
SELECT ACOSH(2.352409615);
```

```
+--------------------+
| ACOSH(2.352409615) |
|--------------------|
|                1.5 |
+--------------------+
```
