Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Cast)

# AS\_BOOLEAN

Casts a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value to a [BOOLEAN](/sql-reference/data-types-logical#label-data-type-boolean) value.

See also:
:   [AS\_\*<object\_type>\*](/sql-reference/functions/as)

## Syntax

Copy code

```
AS_BOOLEAN( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

The function returns a value of type BOOLEAN or NULL:

- If the type of the value in the `variant_expr` argument is BOOLEAN, the function returns a value of type BOOLEAN.

- If the type of the value in the `variant_expr` argument doesn’t match the type of the output
  value, the function returns NULL.
- If the `variant_expr` argument is NULL, the function returns NULL.

## Examples

Create a table and load data into it:

Copy code

```
CREATE OR REPLACE TABLE as_boolean_example (
  boolean1 VARIANT,
  boolean2 VARIANT);

INSERT INTO as_boolean_example (boolean1, boolean2)
  SELECT
    TO_VARIANT(TO_BOOLEAN(TRUE)),
    TO_VARIANT(TO_BOOLEAN(FALSE));
```

Use the AS\_BOOLEAN function in a query to cast VARIANT values to BOOLEAN values:

Copy code

```
SELECT AS_BOOLEAN(boolean1) boolean_true,
       AS_BOOLEAN(boolean2) boolean_false
  FROM as_boolean_example;
```

```
+--------------+---------------+
| BOOLEAN_TRUE | BOOLEAN_FALSE |
|--------------+---------------|
| True         | False         |
+--------------+---------------+
```
