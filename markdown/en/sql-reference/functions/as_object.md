Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Cast)

# AS\_OBJECT

Casts a [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) value to an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value.

See also:
:   [AS\_\*<object\_type>\*](/sql-reference/functions/as) , [AS\_ARRAY](/sql-reference/functions/as_array)

## Syntax

Copy code

```
AS_OBJECT( <variant_expr> )
```

## Arguments

`variant_expr`
:   An expression that evaluates to a value of type VARIANT.

## Returns

The function returns a value of type OBJECT or NULL:

- If the type of the value in the `variant_expr` argument is OBJECT, the function returns a value of type OBJECT.

- If the type of the value in the `variant_expr` argument doesn’t match the type of the output
  value, the function returns NULL.
- If the `variant_expr` argument is NULL, the function returns NULL.

## Usage notes

- This function doesn’t support a [structured type](/sql-reference/data-types-structured) as an input argument.

## Examples

Create a table and load data into it:

Copy code

```
CREATE OR REPLACE TABLE as_object_example (object1 VARIANT);

INSERT INTO as_object_example (object1)
  SELECT TO_VARIANT(TO_OBJECT(PARSE_JSON('{"Tree": "Pine"}')));
```

Use the AS\_OBJECT function in a query to cast a VARIANT value to an OBJECT value:

Copy code

```
SELECT AS_OBJECT(object1) AS object_value
  FROM as_object_example;
```

```
+------------------+
| OBJECT_VALUE     |
|------------------|
| {                |
|   "Tree": "Pine" |
| }                |
+------------------+
```
