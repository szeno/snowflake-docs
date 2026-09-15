Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_INTERSECTION

Returns an array that contains the matching elements in the two input arrays.

The function is NULL-safe, meaning it treats NULLs as known values for comparing equality.

See also:
:   [ARRAY\_EXCEPT](/sql-reference/functions/array_except) , [ARRAYS\_OVERLAP](/sql-reference/functions/arrays_overlap)

## Syntax

Copy code

```
ARRAY_INTERSECTION( <array1> , <array2> )
```

## Arguments

`array1`
:   An array that contains elements to be compared.

`array2`
:   An array that contains elements to be compared.

## Returns

This function returns an `ARRAY` that contains the elements of the input arrays that match.

If no elements overlap, the function returns an empty array.

If one or both arguments are NULL, the function returns NULL.

The order of the values within the returned array is unspecified.

## Usage notes

- When comparing data of type `OBJECT`, the objects must be identical to be considered matching. For details,
  see [Examples](#examples) (in this topic).
- The difference between `ARRAY_INTERSECTION` and the related `ARRAYS_OVERLAP` function is that the
  `ARRAYS_OVERLAP` function simply returns `TRUE` or `FALSE`, while `ARRAY_INTERSECTION` returns the actual
  overlapping values.
- In Snowflake, arrays are multi-sets, not sets. In other words, arrays can contain multiple copies of the same value.
  `ARRAY_INTERSECTION` compares arrays by using multi-set semantics (sometimes called “bag semantics”),
  which means that the function can return multiple copies of the same value. If one array has N copies of a value,
  and the other array has M copies of the same value, then the number of copies in the returned array is
  the smaller of N or M. For example, if N is 4 and M is 2, then the returned value contains 2 copies.

- Both arguments must either be [structured ARRAYs](/sql-reference/data-types-structured) or
  [semi-structured ARRAYs](/sql-reference/data-types-semistructured#label-data-type-array).

- If you are passing in structured ARRAYs:
  - The function returns an ARRAY of a type that can accommodate both input types.
  - The ARRAY in the second argument must be [comparable](/sql-reference/data-types-structured#label-structured-types-compare-struct-struct) to the ARRAY in the
    first argument.

## Examples

This example shows simple use of the function:

> Copy code
>
> ```
> SELECT array_intersection(ARRAY_CONSTRUCT('A', 'B'), 
>                           ARRAY_CONSTRUCT('B', 'C'));
> +------------------------------------------------------+
> | ARRAY_INTERSECTION(ARRAY_CONSTRUCT('A', 'B'),        |
> |                           ARRAY_CONSTRUCT('B', 'C')) |
> |------------------------------------------------------|
> | [                                                    |
> |   "B"                                                |
> | ]                                                    |
> +------------------------------------------------------+
> ```

The sets might have more than one matching value:

> Copy code
>
> ```
> SELECT array_intersection(ARRAY_CONSTRUCT('A', 'B', 'C'), 
>                           ARRAY_CONSTRUCT('B', 'C'));
> +------------------------------------------------------+
> | ARRAY_INTERSECTION(ARRAY_CONSTRUCT('A', 'B', 'C'),   |
> |                           ARRAY_CONSTRUCT('B', 'C')) |
> |------------------------------------------------------|
> | [                                                    |
> |   "B",                                               |
> |   "C"                                                |
> | ]                                                    |
> +------------------------------------------------------+
> ```

There might be more than instance of the same matching value. For example, in the query below, one array has three
copies of the letter ‘B’, and the other array has two copies of the letter ‘B’. The result contains two matches:

> Copy code
>
> ```
> SELECT array_intersection(ARRAY_CONSTRUCT('A', 'B', 'B', 'B', 'C'), 
>                           ARRAY_CONSTRUCT('B', 'B'));
> +---------------------------------------------------------------+
> | ARRAY_INTERSECTION(ARRAY_CONSTRUCT('A', 'B', 'B', 'B', 'C'),  |
> |                           ARRAY_CONSTRUCT('B', 'B'))          |
> |---------------------------------------------------------------|
> | [                                                             |
> |   "B",                                                        |
> |   "B"                                                         |
> | ]                                                             |
> +---------------------------------------------------------------+
> ```

This example uses a larger amount of data:

> Copy code
>
> ```
> CREATE OR REPLACE TABLE array_demo (ID INTEGER, array1 ARRAY, array2 ARRAY, tip VARCHAR);
>
> INSERT INTO array_demo (ID, array1, array2, tip)
>     SELECT 1, ARRAY_CONSTRUCT(1, 2), ARRAY_CONSTRUCT(3, 4), 'non-overlapping';
> INSERT INTO array_demo (ID, array1, array2, tip)
>     SELECT 2, ARRAY_CONSTRUCT(1, 2, 3), ARRAY_CONSTRUCT(3, 4, 5), 'value 3 overlaps';
> INSERT INTO array_demo (ID, array1, array2, tip)
>     SELECT 3, ARRAY_CONSTRUCT(1, 2, 3, 4), ARRAY_CONSTRUCT(3, 4, 5), 'values 3 and 4 overlap';
> INSERT INTO array_demo (ID, array1, array2, tip)
>     SELECT 4, ARRAY_CONSTRUCT(NULL, 102, NULL), ARRAY_CONSTRUCT(NULL, NULL, 103), 'NULLs overlap';
> INSERT INTO array_demo (ID, array1, array2, tip)
>     SELECT 5, array_construct(object_construct('a',1,'b',2), 1, 2),
>               array_construct(object_construct('a',1,'b',2), 3, 4), 
>               'the objects in the array match';
> INSERT INTO array_demo (ID, array1, array2, tip)
>     SELECT 6, array_construct(object_construct('a',1,'b',2), 1, 2),
>               array_construct(object_construct('b',2,'c',3), 3, 4), 
>               'neither the objects nor any other values match';
> INSERT INTO array_demo (ID, array1, array2, tip)
>     SELECT 7, array_construct(object_construct('a',1, 'b',2, 'c',3)),
>               array_construct(object_construct('c',3, 'b',2, 'a',1)), 
>               'the objects contain the same values, but in different order';
> ```
>
> Copy code
>
> ```
> SELECT ID, array1, array2, tip, ARRAY_INTERSECTION(array1, array2) 
>     FROM array_demo
>     WHERE ID <= 3
>     ORDER BY ID;
> +----+--------+--------+------------------------+------------------------------------+
> | ID | ARRAY1 | ARRAY2 | TIP                    | ARRAY_INTERSECTION(ARRAY1, ARRAY2) |
> |----+--------+--------+------------------------+------------------------------------|
> |  1 | [      | [      | non-overlapping        | []                                 |
> |    |   1,   |   3,   |                        |                                    |
> |    |   2    |   4    |                        |                                    |
> |    | ]      | ]      |                        |                                    |
> |  2 | [      | [      | value 3 overlaps       | [                                  |
> |    |   1,   |   3,   |                        |   3                                |
> |    |   2,   |   4,   |                        | ]                                  |
> |    |   3    |   5    |                        |                                    |
> |    | ]      | ]      |                        |                                    |
> |  3 | [      | [      | values 3 and 4 overlap | [                                  |
> |    |   1,   |   3,   |                        |   3,                               |
> |    |   2,   |   4,   |                        |   4                                |
> |    |   3,   |   5    |                        | ]                                  |
> |    |   4    | ]      |                        |                                    |
> |    | ]      |        |                        |                                    |
> +----+--------+--------+------------------------+------------------------------------+
> ```

This shows usage with NULL values:

> Copy code
>
> ```
> SELECT ID, array1, array2, tip, ARRAY_INTERSECTION(array1, array2) 
>     FROM array_demo
>     WHERE ID = 4
>     ORDER BY ID;
> +----+--------------+--------------+---------------+------------------------------------+
> | ID | ARRAY1       | ARRAY2       | TIP           | ARRAY_INTERSECTION(ARRAY1, ARRAY2) |
> |----+--------------+--------------+---------------+------------------------------------|
> |  4 | [            | [            | NULLs overlap | [                                  |
> |    |   undefined, |   undefined, |               |   undefined,                       |
> |    |   102,       |   undefined, |               |   undefined                        |
> |    |   undefined  |   103        |               | ]                                  |
> |    | ]            | ]            |               |                                    |
> +----+--------------+--------------+---------------+------------------------------------+
> ```

This example shows usage with the `OBJECT` data type:

> Copy code
>
> ```
> SELECT ID, array1, array2, tip, ARRAY_INTERSECTION(array1, array2) 
>     FROM array_demo
>     WHERE ID >= 5 and ID <= 7
>     ORDER BY ID;
> +----+-------------+-------------+-------------------------------------------------------------+------------------------------------+
> | ID | ARRAY1      | ARRAY2      | TIP                                                         | ARRAY_INTERSECTION(ARRAY1, ARRAY2) |
> |----+-------------+-------------+-------------------------------------------------------------+------------------------------------|
> |  5 | [           | [           | the objects in the array match                              | [                                  |
> |    |   {         |   {         |                                                             |   {                                |
> |    |     "a": 1, |     "a": 1, |                                                             |     "a": 1,                        |
> |    |     "b": 2  |     "b": 2  |                                                             |     "b": 2                         |
> |    |   },        |   },        |                                                             |   }                                |
> |    |   1,        |   3,        |                                                             | ]                                  |
> |    |   2         |   4         |                                                             |                                    |
> |    | ]           | ]           |                                                             |                                    |
> |  6 | [           | [           | neither the objects nor any other values match              | []                                 |
> |    |   {         |   {         |                                                             |                                    |
> |    |     "a": 1, |     "b": 2, |                                                             |                                    |
> |    |     "b": 2  |     "c": 3  |                                                             |                                    |
> |    |   },        |   },        |                                                             |                                    |
> |    |   1,        |   3,        |                                                             |                                    |
> |    |   2         |   4         |                                                             |                                    |
> |    | ]           | ]           |                                                             |                                    |
> |  7 | [           | [           | the objects contain the same values, but in different order | [                                  |
> |    |   {         |   {         |                                                             |   {                                |
> |    |     "a": 1, |     "a": 1, |                                                             |     "a": 1,                        |
> |    |     "b": 2, |     "b": 2, |                                                             |     "b": 2,                        |
> |    |     "c": 3  |     "c": 3  |                                                             |     "c": 3                         |
> |    |   }         |   }         |                                                             |   }                                |
> |    | ]           | ]           |                                                             | ]                                  |
> +----+-------------+-------------+-------------------------------------------------------------+------------------------------------+
> ```

Although NULL values in an array are treated as comparable values, if you pass NULL instead of an
array, then the result is NULL:

> Copy code
>
> ```
> SELECT array_intersection(ARRAY_CONSTRUCT('A', 'B'), 
>                           NULL);
> +------------------------------------------------+
> | ARRAY_INTERSECTION(ARRAY_CONSTRUCT('A', 'B'),  |
> |                           NULL)                |
> |------------------------------------------------|
> | NULL                                           |
> +------------------------------------------------+
> ```
