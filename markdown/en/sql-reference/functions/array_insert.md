Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_INSERT

Returns an array containing all elements from the source array as well as the new element.

## Syntax

Copy code

```
ARRAY_INSERT( <array> , <pos> , <new_element> )
```

See also:
:   [ARRAY\_APPEND](/sql-reference/functions/array_append) , [ARRAY\_PREPEND](/sql-reference/functions/array_prepend)

## Arguments

`array`
:   The source array.

`pos`
:   A (zero-based) position in the source array. The new element is inserted at this position. The original element from this position (if any) and all subsequent elements (if any) are shifted by
    one position to the right in the resulting array (i.e. inserting at position 0 has the same effect as using [ARRAY\_PREPEND](/sql-reference/functions/array_prepend)).

    A negative position is interpreted as an index from the back of the array (e.g. `-1` results in insertion before the last element in the array).

`new_element`
:   The element to be inserted. The new element is located at position `pos`. The relative order of the other elements from the source array is preserved.

## Returns

The data type of the returned value is `ARRAY`.

## Usage notes

- When you pass a [structured array](/sql-reference/data-types-structured) to the function, the function returns a structured
  array of the same type.
- If `array` is a [structured ARRAY](/sql-reference/data-types-structured), the type of the new element must
  be [coercible](/sql-reference/data-types-structured#label-structured-types-casting-implicit) to the type of the ARRAY.
- If the absolute value of `pos` exceeds the number of elements in `array`, additional empty elements are inserted between the new element and the elements from the source array.
- To append or prepend elements to an array, you should use [ARRAY\_APPEND](/sql-reference/functions/array_append) or [ARRAY\_PREPEND](/sql-reference/functions/array_prepend) instead.

## Examples

This shows a simple example of inserting into an array:

Copy code

```
SELECT ARRAY_INSERT(ARRAY_CONSTRUCT(0,1,2,3),2,'hello');
+--------------------------------------------------+
| ARRAY_INSERT(ARRAY_CONSTRUCT(0,1,2,3),2,'HELLO') |
|--------------------------------------------------|
| [                                                |
|   0,                                             |
|   1,                                             |
|   "hello",                                       |
|   2,                                             |
|   3                                              |
| ]                                                |
+--------------------------------------------------+
```

This shows an insert that uses an index larger than the number of existing elements in the array.

Copy code

```
SELECT ARRAY_INSERT(ARRAY_CONSTRUCT(0,1,2,3),5,'hello');
+--------------------------------------------------+
| ARRAY_INSERT(ARRAY_CONSTRUCT(0,1,2,3),5,'HELLO') |
|--------------------------------------------------|
| [                                                |
|   0,                                             |
|   1,                                             |
|   2,                                             |
|   3,                                             |
|   undefined,                                     |
|   "hello"                                        |
| ]                                                |
+--------------------------------------------------+
```

This shows an insert that uses a negative index.

Copy code

```
SELECT ARRAY_INSERT(ARRAY_CONSTRUCT(0,1,2,3),-1,'hello');
+---------------------------------------------------+
| ARRAY_INSERT(ARRAY_CONSTRUCT(0,1,2,3),-1,'HELLO') |
|---------------------------------------------------|
| [                                                 |
|   0,                                              |
|   1,                                              |
|   2,                                              |
|   "hello",                                        |
|   3                                               |
| ]                                                 |
+---------------------------------------------------+
```
