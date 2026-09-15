Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_DISTINCT

Returns a new [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) that contains only the distinct elements from the input ARRAY. The function
excludes any duplicate elements that are present in the input ARRAY.

The function is not guaranteed to return the elements in the ARRAY in a specific order.

The function is NULL-safe, which means that it treats NULLs as known values when identifying duplicate elements.

## Syntax

Copy code

```
ARRAY_DISTINCT( <array> )
```

## Arguments

`array`
:   An array that might contain duplicate elements to be removed.

## Returns

This function returns an ARRAY that contains the elements of the input array without any duplicate elements. For example, if the
value `'x'` appears multiple times in the input ARRAY, only one element has the value `'x'` in the returned ARRAY.

If the input argument is NULL, the function returns NULL.

The order of the values within the returned array is unspecified.

## Usage notes

- For elements of the type [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object), the objects must be identical to be considered duplicate. For
  details, see [Examples](#examples) (in this topic).
- When identifying duplicate elements, the function considers NULL to be a known value (i.e. NULL is not a duplicate of any other
  value X besides NULL).

## Examples

The following example demonstrates how the function returns an ARRAY without the duplicate elements `A` and `NULL` from an
input [ARRAY constant](/sql-reference/data-types-semistructured#label-array-constant):

Copy code

```
SELECT ARRAY_DISTINCT(['A', 'A', 'B', NULL, NULL]);

+---------------------------------------------+
| ARRAY_DISTINCT(['A', 'A', 'B', NULL, NULL]) |
|---------------------------------------------|
| [                                           |
|   "A",                                      |
|   "B",                                      |
|   undefined                                 |
| ]                                           |
+---------------------------------------------+
```

The following example demonstrates how passing in NULL (instead of an ARRAY) returns NULL:

Copy code

```
SELECT ARRAY_DISTINCT(NULL);

+----------------------+
| ARRAY_DISTINCT(NULL) |
|----------------------|
| NULL                 |
+----------------------+
```

The following example demonstrates how the function removes duplicate OBJECTs that are elements in the input ARRAY. The example
uses [OBJECT constants](/sql-reference/data-types-semistructured#label-object-constant) and ARRAY constants to construct the OBJECTs and ARRAY.

Copy code

```
SELECT ARRAY_DISTINCT( [ {'a': 1, 'b': 2}, {'a': 1, 'b': 2}, {'a': 1, 'b': 3} ] );

+----------------------------------------------------------------------------+
| ARRAY_DISTINCT( [ {'A': 1, 'B': 2}, {'A': 1, 'B': 2}, {'A': 1, 'B': 3} ] ) |
|----------------------------------------------------------------------------|
| [                                                                          |
|   {                                                                        |
|     "a": 1,                                                                |
|     "b": 2                                                                 |
|   },                                                                       |
|   {                                                                        |
|     "a": 1,                                                                |
|     "b": 3                                                                 |
|   }                                                                        |
| ]                                                                          |
+----------------------------------------------------------------------------+
```

As shown in the example, the last element is not considered to be a duplicate because `b` has a different value (`3`, not
`2`).
