Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# OBJECT\_KEYS

Returns an array containing the list of keys in the top-most level of the input object.

## Syntax

Copy code

```
OBJECT_KEYS( <object> )
```

## Arguments

`object`
:   The value for which you want the keys. The input value must be one of the following:

    - An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object).
    - A [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) that contains a value of type OBJECT.

## Returns

The function returns an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) containing the keys.

If `object` is a [structured OBJECT](/sql-reference/data-types-structured), the function returns an ARRAY(VARCHAR).

## Usage notes

- If the object contains nested objects (e.g. objects within objects), this returns only the keys from the top-most level.

## Examples

### Basic example

The next example shows OBJECT\_KEYS working with both an [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) and a
[VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant) that contains a value of type OBJECT.

> Create a table that contains columns of types [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) and
> [VARIANT](/sql-reference/data-types-semistructured#label-data-type-variant).
>
> Copy code
>
> ```
> CREATE TABLE objects_1 (id INTEGER, object1 OBJECT, variant1 VARIANT);
> ```
>
> INSERT values:
>
> Copy code
>
> ```
> INSERT INTO objects_1 (id, object1, variant1) 
>   SELECT
>     1,
>     OBJECT_CONSTRUCT('a', 1, 'b', 2, 'c', 3),
>     TO_VARIANT(OBJECT_CONSTRUCT('a', 1, 'b', 2, 'c', 3))
>     ;
> ```
>
> Retrieve the keys from both the OBJECT and the VARIANT:
>
> Copy code
>
> ```
> SELECT OBJECT_KEYS(object1), OBJECT_KEYS(variant1) 
>     FROM objects_1
>     ORDER BY id;
> +----------------------+-----------------------+
> | OBJECT_KEYS(OBJECT1) | OBJECT_KEYS(VARIANT1) |
> |----------------------+-----------------------|
> | [                    | [                     |
> |   "a",               |   "a",                |
> |   "b",               |   "b",                |
> |   "c"                |   "c"                 |
> | ]                    | ]                     |
> +----------------------+-----------------------+
> ```

### Example of nested objects

This example shows that if the object contains nested objects, only the keys from the top-most level are returned.

> Copy code
>
> ```
> SELECT OBJECT_KEYS (
>            PARSE_JSON (
>                '{
>                     "level_1_A": {
>                                  "level_2": "two"
>                                  },
>                     "level_1_B": "one"
>                     }'
>                )
>            ) AS keys
>     ORDER BY 1;
> +----------------+
> | KEYS           |
> |----------------|
> | [              |
> |   "level_1_A", |
> |   "level_1_B"  |
> | ]              |
> +----------------+
> ```
