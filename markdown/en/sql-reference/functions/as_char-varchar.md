Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Cast)

# AS\_CHAR , AS\_VARCHAR

Casts a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value to a [VARCHAR](/sql-reference/data-types-text#label-data-types-text-varchar) value. This function
only converts [CHAR](/sql-reference/data-types-text#label-data-types-char) and VARCHAR values.

The AS\_CHAR and AS\_VARCHAR functions are synonymous.

The CHAR data type is synonymous with the VARCHAR data type, except for its default length.

See also:
:   [AS\_\*<object\_type>\*](/sql-reference/functions/as)

## Syntax

Copy code

```
AS_CHAR( <variant_expr> )

AS_VARCHAR( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

The function returns a value of type VARCHAR or NULL:

- If the type of the value in the `variant_expr` argument is CHAR or VARCHAR, the function returns a value of type VARCHAR.

- If the type of the value in the `variant_expr` argument doesn’t match the type of the output
  value, the function returns NULL.
- If the `variant_expr` argument is NULL, the function returns NULL.

## Examples

Create a table and load data into it:

Copy code

```
CREATE OR REPLACE TABLE as_varchar_example (varchar1 VARIANT);

INSERT INTO as_varchar_example (varchar1)
  SELECT TO_VARIANT('My VARCHAR value');
```

Use the AS\_VARCHAR function in a query to cast a VARIANT value to a VARCHAR value:

Copy code

```
SELECT AS_VARCHAR(varchar1) varchar_value
  FROM as_varchar_example;
```

```
+------------------+
| VARCHAR_VALUE    |
|------------------|
| My VARCHAR value |
+------------------+
```
