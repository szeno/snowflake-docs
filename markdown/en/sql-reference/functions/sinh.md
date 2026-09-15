Categories:
:   [Numeric functions](/sql-reference/functions-numeric) (Trigonometric)

# SINH

Computes the hyperbolic sine of its argument.

## Syntax

Copy code

```
SINH( <input_expr> )
```

## Arguments

`input_expr`
:   The value or expression to operate on. The data type must be FLOAT.

## Returns

This function returns a value of type FLOAT.

## Examples

Copy code

```
SELECT SINH(1.5);
```

```
+-------------+
|   SINH(1.5) |
|-------------|
| 2.129279455 |
+-------------+
```
