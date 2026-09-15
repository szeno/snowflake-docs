Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Cast)

# AS\_INTEGER

Casts a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value to an [INTEGER](/sql-reference/data-types-numeric#label-data-type-integer). The function does
not cast non-integer values.

The INTEGER data type is synonymous with the [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) data type, except that precision
and scale can’t be specified for INTEGER values.

See also:
:   [AS\_\*<object\_type>\*](/sql-reference/functions/as)

    [AS\_DECIMAL , AS\_NUMBER](/sql-reference/functions/as_decimal-number) , [AS\_DOUBLE , AS\_REAL](/sql-reference/functions/as_double-real)

## Syntax

Copy code

```
AS_INTEGER( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

The function returns a value of type INTEGER or NULL:

- If the type of the value in the `variant_expr` argument is INTEGER, the function returns a value of type INTEGER.

- If the type of the value in the `variant_expr` argument doesn’t match the type of the output
  value, the function returns NULL.
- If the `variant_expr` argument is NULL, the function returns NULL.

## Examples

Create a table and load data into it:

Copy code

```
CREATE OR REPLACE TABLE as_integer_example (integer1 VARIANT);

INSERT INTO as_integer_example (integer1)
  SELECT TO_VARIANT(15);
```

Use the AS\_INTEGER function in a query to cast a VARIANT value to an INTEGER value:

Copy code

```
SELECT AS_INTEGER(integer1) AS integer_value
  FROM as_integer_example;
```

```
+---------------+
| INTEGER_VALUE |
|---------------|
|            15 |
+---------------+
```
