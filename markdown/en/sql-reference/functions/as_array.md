Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Cast)

# AS\_ARRAY

Casts a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value to an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) value.

See also:
:   [AS\_\*<object\_type>\*](/sql-reference/functions/as) , [AS\_OBJECT](/sql-reference/functions/as_object)

## Syntax

Copy code

```
AS_ARRAY( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

The function returns a value of type ARRAY or NULL:

- If the type of the value in the `variant_expr` argument is ARRAY, the function returns a value of type ARRAY.

- If the type of the value in the `variant_expr` argument doesn’t match the type of the output
  value, the function returns NULL.
- If the `variant_expr` argument is NULL, the function returns NULL.

## Usage notes

- This function doesn’t support a [structured type](/sql-reference/data-types-structured) as an input argument.

## Examples

Create a table and load data into it:

Copy code

```
CREATE OR REPLACE TABLE as_array_example (
  array1 VARIANT,
  array2 VARIANT);

INSERT INTO as_array_example (array1, array2)
  SELECT
    TO_VARIANT(TO_ARRAY('Example')),
    TO_VARIANT(ARRAY_CONSTRUCT('Array-like', 'example'));
```

Use the AS\_ARRAY function in a query to cast a VARIANT value to ARRAY values:

Copy code

```
SELECT AS_ARRAY(array1) AS array1,
       AS_ARRAY(array2) AS array2
  FROM as_array_example;
```

```
+-------------+-----------------+
| ARRAY1      | ARRAY2          |
|-------------+-----------------|
| [           | [               |
|   "Example" |   "Array-like", |
| ]           |   "example"     |
|             | ]               |
+-------------+-----------------+
```
