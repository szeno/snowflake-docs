Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Cast)

# AS\_DECIMAL , AS\_NUMBER

Casts a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value to a fixed-point [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) value, with optional precision and scale.
This function doesn’t cast floating-point values.

AS\_DECIMAL is a synonym for AS\_NUMBER.

The [DECIMAL](/sql-reference/data-types-numeric#label-data-type-decimal) data type is synonymous with the NUMBER data type.

See also:
:   [AS\_\*<object\_type>\*](/sql-reference/functions/as) , [AS\_DOUBLE , AS\_REAL](/sql-reference/functions/as_double-real) , [AS\_INTEGER](/sql-reference/functions/as_integer)

## Syntax

Copy code

```
AS_DECIMAL( <variant_expr> [ , <precision> [ , <scale> ] ] )

AS_NUMBER( <variant_expr> [ , <precision> [ , <scale> ] ] )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

`precision`
:   The number of significant digits of the decimal number to store.

    The default is `38`.

`scale`
:   The number of significant digits after the decimal point.

    The default is `0`.

## Returns

The function returns a value of type NUMBER or NULL:

- If the type of the value in the `variant_expr` argument is DECIMAL or NUMBER, the function returns a value of type NUMBER.

- If the type of the value in the `variant_expr` argument doesn’t match the type of the output
  value, the function returns NULL.
- If the `variant_expr` argument is NULL, the function returns NULL.

## Usage notes

When reducing scale, this function rounds the result, which can cause out-of-range errors.

## Examples

Create a table and load data into it:

Copy code

```
CREATE OR REPLACE TABLE as_number_example (number1 VARIANT);

INSERT INTO as_number_example (number1)
  SELECT TO_VARIANT(TO_NUMBER(2.34, 6, 3));
```

Use the AS\_NUMBER function in a query to cast a VARIANT value to a NUMBER value:

Copy code

```
SELECT AS_NUMBER(number1, 6, 3) number_value
  FROM as_number_example;
```

```
+--------------+
| NUMBER_VALUE |
|--------------|
|        2.340 |
+--------------+
```
