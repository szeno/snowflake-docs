Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object Creation and Manipulation)

# ARRAYS\_ZIP

Returns an [array](/sql-reference/data-types-semistructured#label-data-type-array) of [objects](/sql-reference/data-types-semistructured#label-data-type-object), each of which contains key-value pairs
for an nth element in the input arrays. For example, in the returned array, the first object contains key-value pairs for each
first element in the input arrays, the second object contains key-value pairs for each second element in the input arrays, and so
on.

## Syntax

Copy code

```
ARRAYS_ZIP( <array> [ , <array> ... ] )
```

## Arguments

`array`
:   An input array.

    The input arrays can be of different lengths.

    If any of the input arrays is a [structured array](/sql-reference/data-types-structured), all input arrays must be
    structured arrays.

## Returns

Returns a value of one of the following types:

- If the input arrays are semi-structured arrays, the function returns a semi-structured array of structured objects.
- If the input arrays are structured arrays, the function returns a structured array of structured objects. The definition of
  the structured object depends on the number of input arrays and the types of values in the arrays.
- If any of the input arrays is NULL, the function returns NULL.

Each object contains the key-value pairs for the values of an nth element in the input arrays. The key (`$1`, `$2`, and so on)
represents the position of the input array.

For example, suppose that you pass in these arrays:

Copy code

```
SELECT ARRAYS_ZIP(
  [1, 2, 3],
  ['first', 'second', 'third'],
  ['i', 'ii', 'iii']
) AS zipped_arrays;
```

The function returns the following array of objects:

```
+---------------------+
| ZIPPED_ARRAYS       |
|---------------------|
| [                   |
|   {                 |
|     "$1": 1,        |
|     "$2": "first",  |
|     "$3": "i"       |
|   },                |
|   {                 |
|     "$1": 2,        |
|     "$2": "second", |
|     "$3": "ii"      |
|   },                |
|   {                 |
|     "$1": 3,        |
|     "$2": "third",  |
|     "$3": "iii"     |
|   }                 |
| ]                   |
+---------------------+
```

In the returned array:

- The first object contains the first elements of all input arrays.
- The second object contains the second elements of all input arrays.
- The third object contains the third elements of all input arrays.

The keys in the objects identify the input array:

- The `$1` key-value pairs contain the values from the first input array.
- The `$2` key-value pairs contain the values from the second input array.
- The `$3` key-value pairs contain the values from the third input array.

## Usage notes

- The returned array is as long as the longest input array. If some input arrays are shorter, the function uses a
  [JSON null](/user-guide/semistructured-considerations#label-variant-null) for the remaining elements missing in the shorter arrays.
- If the input array includes a NULL element, the function returns a JSON null for that element.

## Examples

The following examples demonstrate how the function works:

- [Single input array](#label-arrays-zip-example-single)
- [Multiple input arrays](#label-arrays-zip-example-multiple)
- [Input arrays of different lengths](#label-arrays-zip-example-different-lengths)
- [NULL and empty array handling](#label-arrays-zip-example-null)

### Single input array

The following example returns an array of objects containing the first, second, and third elements in a single array:

Copy code

```
SELECT ARRAYS_ZIP(
  [1, 2, 3]
) AS zipped_array;
```

```
+--------------+
| ZIPPED_ARRAY |
|--------------|
| [            |
|   {          |
|     "$1": 1  |
|   },         |
|   {          |
|     "$1": 2  |
|   },         |
|   {          |
|     "$1": 3  |
|   }          |
| ]            |
+--------------+
```

### Multiple input arrays

The following example returns an array of objects containing the first, second, and third elements in the input arrays:

Copy code

```
SELECT ARRAYS_ZIP(
  [1, 2, 3],
  [10, 20, 30],
  [100, 200, 300]
) AS zipped_array;
```

```
+---------------+
| ZIPPED_ARRAY  |
|---------------|
| [             |
|   {           |
|     "$1": 1,  |
|     "$2": 10, |
|     "$3": 100 |
|   },          |
|   {           |
|     "$1": 2,  |
|     "$2": 20, |
|     "$3": 200 |
|   },          |
|   {           |
|     "$1": 3,  |
|     "$2": 30, |
|     "$3": 300 |
|   }           |
| ]             |
+---------------+
```

### Input arrays of different lengths

The following example passes in input arrays of different lengths. For the values absent from the shorter arrays, the function
uses a JSON null in the object.

Copy code

```
SELECT ARRAYS_ZIP(
  [1, 2, 3],
  ['one'],
  ['I', 'II']
) AS zipped_array;
```

```
+------------------+
| ZIPPED_ARRAY     |
|------------------|
| [                |
|   {              |
|     "$1": 1,     |
|     "$2": "one", |
|     "$3": "I"    |
|   },             |
|   {              |
|     "$1": 2,     |
|     "$2": null,  |
|     "$3": "II"   |
|   },             |
|   {              |
|     "$1": 3,     |
|     "$2": null,  |
|     "$3": null   |
|   }              |
| ]                |
+------------------+
```

### NULL and empty array handling

As shown in the following example, passing in a NULL for any input array causes the function to return a SQL NULL:

Copy code

```
SELECT ARRAYS_ZIP(
  [1, 2, 3],
  NULL,
  [100, 200, 300]
) AS zipped_array;
```

```
+--------------+
| ZIPPED_ARRAY |
|--------------|
| NULL         |
+--------------+
```

In the following example, all of the input arrays are empty, which causes the function to return an empty object:

Copy code

```
SELECT ARRAYS_ZIP(
  [], [], []
) AS zipped_array;
```

```
+--------------+
| ZIPPED_ARRAY |
|--------------|
| [            |
|   {}         |
| ]            |
+--------------+
```

In the following example, some of the elements in the input arrays are NULL. In the returned objects, the values for these
elements are JSON nulls:

Copy code

```
SELECT ARRAYS_ZIP(
  [1, NULL, 3],
  [NULL, 20, NULL],
  [100, NULL, 300]
) AS zipped_array;
```

```
+-----------------+
| ZIPPED_ARRAY    |
|-----------------|
| [               |
|   {             |
|     "$1": 1,    |
|     "$2": null, |
|     "$3": 100   |
|   },            |
|   {             |
|     "$1": null, |
|     "$2": 20,   |
|     "$3": null  |
|   },            |
|   {             |
|     "$1": 3,    |
|     "$2": null, |
|     "$3": 300   |
|   }             |
| ]               |
+-----------------+
```
