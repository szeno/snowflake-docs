Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_SORT

Returns an [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array) that contains the elements of the input ARRAY sorted in ascending or descending order.
You can specify whether or not NULL elements are sorted before or after non-NULL elements.

## Syntax

Copy code

```
ARRAY_SORT( <array> [ , <sort_ascending> [ , <nulls_first> ] ] )
```

## Arguments

**Required**

`array`
:   The ARRAY of elements to sort.

**Optional**

`sort_ascending`
:   Specifies whether to sort the elements in ascending or descending order:

    - Specify TRUE to sort the elements in ascending order.
    - Specify FALSE to sort the elements in descending order.

    Default: TRUE

`nulls_first`
:   Specifies whether to place SQL NULL elements at the beginning or end of the sorted ARRAY:

    - Specify TRUE to place the SQL NULL elements first in the ARRAY.
    - Specify FALSE to place the SQL NULL elements last in the ARRAY.

    Default: FALSE if the ARRAY is sorted in ascending order; TRUE if the ARRAY is sorted in descending order.

    This argument only affects the order of SQL NULL elements. This does not affect the order of
    [JSON null](/user-guide/semistructured-considerations#label-variant-null) elements.

## Returns

This function returns an ARRAY that contains the elements of `array` in sorted order.

## Usage notes

- The sort order is equivalent to the order resulting from [flattening](/user-guide/querying-semistructured#label-flatten-arrays) the ARRAY and specifying an
  [ORDER BY](/sql-reference/constructs/order-by) clause with the corresponding ASC | DESC and NULLS FIRST | LAST parameters.
- If any of the input arguments is NULL, the function returns NULL.
- This function is not guaranteed to provide a stable sort when the ARRAY contains either of the following:
  - Elements of two different [numeric](/sql-reference/data-types-numeric) or [timestamp](/sql-reference/data-types-datetime#label-datatypes-timestamp)
    types.
  - Objects containing two different numeric or timestamp types.

## Examples

The following example returns an ARRAY of numbers with the elements from an input [ARRAY constant](/sql-reference/data-types-semistructured#label-array-constant)
sorted in ascending order. The elements include a JSON NULL (PARSE\_JSON(‘null’)) and a SQL NULL.

Note that in the sorted ARRAY, JSON NULLs (`null`) and SQL NULLs (`undefined`) are the last elements.

Copy code

```
SELECT ARRAY_SORT([20, PARSE_JSON('null'), 0, NULL, 10]);
```

```
+---------------------------------------------------+
| ARRAY_SORT([20, PARSE_JSON('NULL'), 0, NULL, 10]) |
|---------------------------------------------------|
| [                                                 |
|   0,                                              |
|   10,                                             |
|   20,                                             |
|   null,                                           |
|   undefined                                       |
| ]                                                 |
+---------------------------------------------------+
```

The following example returns an ARRAY of numbers with the elements sorted in descending order. Note that in the sorted ARRAY,
JSON NULLs (`null`) and SQL NULLs (`undefined`) are the first elements.

Copy code

```
SELECT ARRAY_SORT([20, PARSE_JSON('null'), 0, NULL, 10], FALSE);
```

```
+----------------------------------------------------------+
| ARRAY_SORT([20, PARSE_JSON('NULL'), 0, NULL, 10], FALSE) |
|----------------------------------------------------------|
| [                                                        |
|   undefined,                                             |
|   null,                                                  |
|   20,                                                    |
|   10,                                                    |
|   0                                                      |
| ]                                                        |
+----------------------------------------------------------+
```

The following example sorts the elements in ascending order. The example sets the `nulls_first` argument to TRUE to place
the SQL NULLs (`undefined`) first in the sorted ARRAY. (By default, SQL NULLs are placed at the end of an ARRAY sorted in
ascending order.)

Note that `nulls_first` has no effect on the placement of JSON NULLs (`null`).

Copy code

```
SELECT ARRAY_SORT([20, PARSE_JSON('null'), 0, NULL, 10], TRUE, TRUE);
```

```
+---------------------------------------------------------------+
| ARRAY_SORT([20, PARSE_JSON('NULL'), 0, NULL, 10], TRUE, TRUE) |
|---------------------------------------------------------------|
| [                                                             |
|   undefined,                                                  |
|   0,                                                          |
|   10,                                                         |
|   20,                                                         |
|   null                                                        |
| ]                                                             |
+---------------------------------------------------------------+
```

The following example sorts the elements in descending order. The example sets the `nulls_first` argument to FALSE to
place the SQL NULLs (`undefined`) last in the sorted ARRAY. (By default, SQL NULLs are placed at the beginning of an ARRAY
sorted in descending order.)

Note that `nulls_first` has no effect on the placement of JSON NULLs (`null`).

Copy code

```
SELECT ARRAY_SORT([20, PARSE_JSON('null'), 0, NULL, 10], FALSE, FALSE);
```

```
+-----------------------------------------------------------------+
| ARRAY_SORT([20, PARSE_JSON('NULL'), 0, NULL, 10], FALSE, FALSE) |
|-----------------------------------------------------------------|
| [                                                               |
|   null,                                                         |
|   20,                                                           |
|   10,                                                           |
|   0,                                                            |
|   undefined                                                     |
| ]                                                               |
+-----------------------------------------------------------------+
```

The following example uses the [ARRAY\_INSERT](/sql-reference/functions/array_insert) function to construct a sparsely populated ARRAY. (The example inserts the
values `1` and `2` at specific positions in the ARRAY.) The example then uses the ARRAY\_SORT function to sort this ARRAY.

Copy code

```
SELECT ARRAY_INSERT(ARRAY_INSERT(ARRAY_CONSTRUCT(), 3, 2), 6, 1) arr, ARRAY_SORT(arr);
```

```
+--------------+-----------------+
| ARR          | ARRAY_SORT(ARR) |
|--------------+-----------------|
| [            | [               |
|   undefined, |   1,            |
|   undefined, |   2,            |
|   undefined, |   undefined,    |
|   2,         |   undefined,    |
|   undefined, |   undefined,    |
|   undefined, |   undefined,    |
|   1          |   undefined     |
| ]            | ]               |
+--------------+-----------------+
```

The following example demonstrates that sorting an ARRAY with different numeric types results in an unstable sort. The example
uses an ARRAY that contains NUMBER values and a REAL value.

Copy code

```
SELECT ARRAY_SORT([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1e0::REAL]) AS array_of_different_numeric_types;
```

```
+----------------------------------+
| ARRAY_OF_DIFFERENT_NUMERIC_TYPES |
|----------------------------------|
| [                                |
|   1,                             |
|   1.000000000000000e+00,         |
|   1,                             |
|   1,                             |
|   1,                             |
|   1,                             |
|   1,                             |
|   1,                             |
|   1,                             |
|   1,                             |
|   1,                             |
|   1,                             |
|   1,                             |
|   1,                             |
|   1,                             |
|   1,                             |
|   1                              |
| ]                                |
+----------------------------------+
```
