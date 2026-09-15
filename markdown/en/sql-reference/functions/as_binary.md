Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Cast)

# AS\_BINARY

Casts a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value to a [BINARY](/sql-reference/data-types-text#label-data-type-binary) value.

See also:
:   [AS\_\*<object\_type>\*](/sql-reference/functions/as)

## Syntax

Copy code

```
AS_BINARY( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

The function returns a value of type BINARY or NULL:

- If the type of the value in the `variant_expr` argument is BINARY, the function returns a value of type BINARY.

- If the type of the value in the `variant_expr` argument doesn’t match the type of the output
  value, the function returns NULL.
- If the `variant_expr` argument is NULL, the function returns NULL.

## Examples

Create a table and load data into it:

Copy code

```
CREATE OR REPLACE TABLE as_binary_example (binary1 VARIANT);

INSERT INTO as_binary_example (binary1)
  SELECT TO_VARIANT(TO_BINARY('F0A5'));
```

Use the AS\_BINARY function in a query to cast a VARIANT value to a BINARY value:

Copy code

```
SELECT AS_BINARY(binary1) AS binary_value
  FROM as_binary_example;
```

```
+--------------+
| BINARY_VALUE |
|--------------|
| F0A5         |
+--------------+
```
