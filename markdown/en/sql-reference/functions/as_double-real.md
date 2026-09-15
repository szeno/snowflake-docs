Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Cast)

# AS\_DOUBLE , AS\_REAL

Casts a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value to a [floating-point value](/sql-reference/data-types-numeric#label-data-type-float).

AS\_DOUBLE is a synonym for AS\_REAL.

The [DOUBLE and REAL](/sql-reference/data-types-numeric#label-data-type-double-precision) data types are synonymous with the FLOAT data type.

See also:
:   [AS\_\*<object\_type>\*](/sql-reference/functions/as) , [AS\_DECIMAL , AS\_NUMBER](/sql-reference/functions/as_decimal-number) , [AS\_INTEGER](/sql-reference/functions/as_integer)

## Syntax

Copy code

```
AS_DOUBLE( <variant_expr> )

AS_REAL( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

The function returns a floating-point value or NULL:

- If the type of the value in the `variant_expr` argument is a floating-point value, the function returns the floating-point value.

- If the type of the value in the `variant_expr` argument doesn’t match the type of the output
  value, the function returns NULL.
- If the `variant_expr` argument is NULL, the function returns NULL.

## Examples

Create a table and load data into it:

Copy code

```
CREATE OR REPLACE TABLE as_double_example (double1 VARIANT);

INSERT INTO as_double_example (double1)
  SELECT TO_VARIANT(TO_DOUBLE(1.23));
```

Use the AS\_DOUBLE function in a query to cast a VARIANT value to a DOUBLE value:

Copy code

```
SELECT AS_DOUBLE(double1) double_value
  FROM as_double_float_example;
```

```
+--------------+
| DOUBLE_VALUE |
|--------------|
|         1.23 |
+--------------+
```
