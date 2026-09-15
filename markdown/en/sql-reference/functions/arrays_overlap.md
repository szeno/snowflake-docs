Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAYS\_OVERLAP

Compares whether two arrays have at least one element in common. Returns TRUE if there is at least one element in common; otherwise returns FALSE. The function is NULL-safe, meaning it treats NULLs as known values for comparing equality.

See also:
:   [ARRAY\_INTERSECTION](/sql-reference/functions/array_intersection)

## Syntax

Copy code

```
ARRAYS_OVERLAP( <array1> , <array2> )
```

## Usage notes

- When you compare objects, the objects must be identical to return TRUE. For details, see [Examples](#examples) (in this topic).

- Both arguments must either be [structured ARRAYs](/sql-reference/data-types-structured) or
  [semi-structured ARRAYs](/sql-reference/data-types-semistructured#label-data-type-array).

- If you are passing in structured ARRAYs, the ARRAY in the second argument must be
  [comparable](/sql-reference/data-types-structured#label-structured-types-compare-struct-struct) to the ARRAY in the first argument.

## Examples

Here are some examples:

> Copy code
>
> ```
> SELECT ARRAYS_OVERLAP(array_construct('hello', 'aloha'), 
>                       array_construct('hello', 'hi', 'hey'))
>   AS Overlap;
> +---------+
> | OVERLAP |
> |---------|
> | True    |
> +---------+
> SELECT ARRAYS_OVERLAP(array_construct('hello', 'aloha'), 
>                       array_construct('hola', 'bonjour', 'ciao'))
>   AS Overlap;
> +---------+
> | OVERLAP |
> |---------|
> | False   |
> +---------+
> SELECT ARRAYS_OVERLAP(array_construct(object_construct('a',1,'b',2), 1, 2), 
>                       array_construct(object_construct('b',2,'c',3), 3, 4))
>   AS Overlap;
> +---------+
> | OVERLAP |
> |---------|
> | False   |
> +---------+
> SELECT ARRAYS_OVERLAP(array_construct(object_construct('a',1,'b',2), 1, 2), 
>                       array_construct(object_construct('a',1,'b',2), 3, 4))
>   AS Overlap;
> +---------+
> | OVERLAP |
> |---------|
> | True    |
> +---------+
> ```

The following example shows that NULL values are considered equal to other
NULL values. If each array contains a NULL value, then the arrays overlap, even
if no other (non-NULL) values overlap:

> Copy code
>
> ```
> SELECT ARRAYS_OVERLAP(ARRAY_CONSTRUCT(1, 2, NULL),
>                       ARRAY_CONSTRUCT(3, NULL, 5))
>  AS Overlap;
> +---------+
> | OVERLAP |
> |---------|
> | True    |
> +---------+
> ```
