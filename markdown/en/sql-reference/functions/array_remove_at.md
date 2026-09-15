Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_REMOVE\_AT

Given a source [ARRAY](/sql-reference/data-types-semistructured#label-data-type-array), returns an ARRAY with the element at the specified position removed.

For example, `ARRAY_REMOVE_AT([2, 5, 7], 0)` returns an ARRAY with the element at position 0 removed (`[5, 7]`).

## Syntax

Copy code

```
ARRAY_REMOVE_AT( <array> , <position> )
```

## Arguments

`array`
:   The source array.

`position`
:   The (zero-based) position of the element to be removed. The function removes the element at this position.

    A negative position is interpreted as an index from the back of the array (e.g. `-1` removes the last element in the array).

## Returns

An ARRAY with the element at the specified position removed.

If `position` is NULL, the function returns NULL.

## Usage notes

- If the absolute value of `position` exceeds the length of `array`, the function returns `array` without
  any elements removed.

## Examples

The following example returns an ARRAY with elements with the first element removed.

Copy code

```
SELECT ARRAY_REMOVE_AT(
  [2, 5, 7],
  0);
```

```
+-------------------------------+
| ARRAY_REMOVE_AT([2, 5, 7], 0) |
|-------------------------------|
| [                             |
|   5,                          |
|   7                           |
| ]                             |
+-------------------------------+
```

The following example returns an ARRAY with elements with the last element removed.

Copy code

```
SELECT ARRAY_REMOVE_AT(
  [2, 5, 7],
  -1);
```

```
+--------------------------------+
| ARRAY_REMOVE_AT([2, 5, 7], -1) |
|--------------------------------|
| [                              |
|   2,                           |
|   5                            |
| ]                              |
+--------------------------------+
```

In the following example, `position` is greater than the length of the ARRAY, so the function returns the ARRAY without
making any changes.

Copy code

```
SELECT ARRAY_REMOVE_AT(
  [2, 5, 7],
  10);
```

```
+------------------+
| ARRAY_REMOVE_AT( |
|   [2, 5, 7],     |
|   10)            |
|------------------|
| [                |
|   2,             |
|   5,             |
|   7              |
| ]                |
+------------------+
```
