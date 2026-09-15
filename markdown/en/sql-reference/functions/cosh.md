Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Trigonometric)

# COSH

Computes the hyperbolic cosine of its argument.

## Syntax

Copy code

```
COSH( <input_expr> )
```

## Arguments

`input_expr`
:   The value or expression to operate on. The data type must be FLOAT.

## Returns

This function returns a value of type FLOAT.

## Examples

Copy code

```
SELECT COSH(1.5);
```

```
+-------------+
|   COSH(1.5) |
|-------------|
| 2.352409615 |
+-------------+
```
