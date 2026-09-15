Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_REVERSE

Returns an [array](/sql-reference/data-types-semistructured#label-data-type-array) with the elements of the input array in reverse order.

## Syntax

Copy code

```
ARRAY_REVERSE( <array> )
```

## Arguments

`array`
:   The source array.

## Returns

An array containing the elements of the input array in reverse order.

## Usage notes

- If the argument is NULL, the result will be NULL.
- When you pass a [structured array](/sql-reference/data-types-structured) to the function, the function returns a structured
  array of the same type.

## Examples

The following example returns an array containing the elements from the input array in reverse order:

Copy code

```
SELECT ARRAY_REVERSE([1,2,3,4]);
```

```
+--------------------------+
| ARRAY_REVERSE([1,2,3,4]) |
|--------------------------|
| [                        |
|   4,                     |
|   3,                     |
|   2,                     |
|   1                      |
| ]                        |
+--------------------------+
```
