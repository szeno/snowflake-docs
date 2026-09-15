Categories:
:   [Semi-structured and structured data functions](/sql-reference/functions-semistructured) (Array/Object)

# ARRAY\_PREPEND

Returns an array containing the new element as well as all elements from the source array. The new element is positioned at the beginning of the array.

See also:
:   [ARRAY\_APPEND](/sql-reference/functions/array_append) , [ARRAY\_INSERT](/sql-reference/functions/array_insert)

## Syntax

Copy code

```
ARRAY_PREPEND( <array> , <new_element> )
```

## Arguments

`array`
:   The source array.

`new_element`
:   The element to be prepended.

## Returns

This returns the updated array.

## Usage notes

- When you pass a [structured array](/sql-reference/data-types-structured) to the function, the function returns a structured
  array of the same type.
- If `array` is a [structured ARRAY](/sql-reference/data-types-structured), the type of the new element must
  be [coercible](/sql-reference/data-types-structured#label-structured-types-casting-implicit) to the type of the ARRAY.

## Examples

The example below shows that the prepended element is placed at the beginning of the array:

> Copy code
>
> ```
> SELECT ARRAY_PREPEND(ARRAY_CONSTRUCT(0,1,2,3),'hello');
> +-------------------------------------------------+
> | ARRAY_PREPEND(ARRAY_CONSTRUCT(0,1,2,3),'HELLO') |
> |-------------------------------------------------|
> | [                                               |
> |   "hello",                                      |
> |   0,                                            |
> |   1,                                            |
> |   2,                                            |
> |   3                                             |
> | ]                                               |
> +-------------------------------------------------+
> ```
